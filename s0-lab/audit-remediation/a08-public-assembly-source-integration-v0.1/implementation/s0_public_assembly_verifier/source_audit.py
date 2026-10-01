"""Pre-import source audit for the candidate/verifier authority split."""

from __future__ import annotations

import ast
from pathlib import Path

from .errors import auth_failure


CANDIDATE_FORBIDDEN_IMPORT_ROOTS = {
    "_cffi_backend",
    "_ctypes",
    "aiohttp",
    "anthropic",
    "asyncio",
    "boto3",
    "botocore",
    "cffi",
    "ctypes",
    "ftplib",
    "httpx",
    "multiprocessing",
    "openai",
    "paramiko",
    "requests",
    "shutil",
    "smtplib",
    "socket",
    "ssl",
    "subprocess",
    "telnetlib",
    "urllib3",
    "webbrowser",
    "win32api",
    "win32con",
    "win32event",
    "win32file",
    "win32process",
    "s0_public_assembly_verifier",
}
CANDIDATE_FORBIDDEN_REFERENCES = {
    "CDLL",
    "LiveConsumer",
    "MoveFileExW",
    "PublicationObserver",
    "PublicationWitness",
    "PyDLL",
    "WinDLL",
    "cdll",
    "oledll",
    "rename",
    "replace",
    "windll",
}


def _python_sources(root: Path) -> tuple[Path, ...]:
    return tuple(sorted(path for path in root.rglob("*.py") if path.is_file() and not path.is_symlink()))


def audit_candidate_source(candidate_root: Path) -> tuple[str, ...]:
    sources = _python_sources(candidate_root)
    if not sources:
        raise auth_failure("candidate source inventory is empty")
    checked: list[str] = []
    for path in sources:
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=path.name)
        except SyntaxError as exc:
            raise auth_failure("candidate source is not valid Python") from exc
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name.split(".")[0] in CANDIDATE_FORBIDDEN_IMPORT_ROOTS for alias in node.names):
                raise auth_failure("candidate source imports verifier-owned authority")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in CANDIDATE_FORBIDDEN_IMPORT_ROOTS:
                raise auth_failure("candidate source imports verifier-owned authority")
            if isinstance(node, (ast.Name, ast.Attribute)):
                reference = node.id if isinstance(node, ast.Name) else node.attr
                if reference in CANDIDATE_FORBIDDEN_REFERENCES:
                    raise auth_failure("candidate source references verifier-owned authority")
        checked.append(path.name)
    return tuple(checked)


def audit_win32_source_text(text: str) -> None:
    if type(text) is not str:
        raise auth_failure("Win32 source audit input is not text")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise auth_failure("Win32 source is not valid Python") from exc
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    forbidden_loaders = {
        "ctypes.CDLL",
        "ctypes.OleDLL",
        "ctypes.PyDLL",
        "ctypes.cdll.LoadLibrary",
        "ctypes.oledll.LoadLibrary",
        "ctypes.pydll.LoadLibrary",
        "ctypes.windll.LoadLibrary",
    }
    if any(_call_name(call.func) in forbidden_loaders for call in calls):
        raise auth_failure("Win32 source contains a forbidden DLL loader")
    if any(
        _call_name(call.func) == "getattr"
        and call.args
        and _expr_name(call.args[0]) == "ctypes"
        for call in calls
    ):
        raise auth_failure("Win32 source dynamically resolves a ctypes authority")
    win_dll_calls = [call for call in calls if _call_name(call.func) == "ctypes.WinDLL"]
    if len(win_dll_calls) != 2 or not all(
        len(call.args) == 1
        and isinstance(call.args[0], ast.Constant)
        and call.args[0].value == "kernel32"
        and len(call.keywords) == 1
        and call.keywords[0].arg == "use_last_error"
        and isinstance(call.keywords[0].value, ast.Constant)
        and call.keywords[0].value.value is True
        for call in win_dll_calls
    ):
        raise auth_failure("Win32 source does not have exactly the two fixed kernel32 loaders")

    loops = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.For, ast.AsyncFor, ast.While))
    ]
    for loop in loops:
        if any(
            isinstance(child, ast.Call)
            and _call_name(child.func)
            in {"self._move.call", "self._move_file_ex", "ctypes.WinDLL"}
            for child in ast.walk(loop)
        ):
            raise auth_failure("Win32 publication authority appears in a retry loop")

    forbidden_publication_names = {
        "CopyFile2",
        "CopyFileW",
        "DeleteFileW",
        "MoveFileW",
        "ReplaceFileW",
        "MOVEFILE_COPY_ALLOWED",
        "MOVEFILE_REPLACE_EXISTING",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in forbidden_publication_names:
            raise auth_failure("Win32 source contains a fallback publication authority")
        if isinstance(node, ast.Name) and node.id in forbidden_publication_names:
            raise auth_failure("Win32 source contains a fallback publication authority")
        if isinstance(node, ast.Constant) and node.value in forbidden_publication_names:
            raise auth_failure("Win32 source names a fallback publication authority")

    if sum(
        isinstance(node, ast.Attribute) and node.attr == "MoveFileExW"
        for node in ast.walk(tree)
    ) != 1:
        raise auth_failure("Win32 source must bind exactly one MoveFileExW export")
    if sum(
        isinstance(node, ast.Attribute) and node.attr == "_move_file_ex"
        for node in ast.walk(tree)
    ) != 2:
        raise auth_failure("Win32 source has an extra or missing bound MoveFileExW reference")
    if sum(_call_name(call.func) == "self._move.call" for call in calls) != 1:
        raise auth_failure("Win32 backend must have exactly one publication call site")

    configure = _function(tree, "_configure_move_file_ex")
    _require_exact_function_ast(
        configure,
        """
def _configure_move_file_ex(function: object) -> object:
    function.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
    function.restype = ctypes.c_int32
    return function
""",
        "MoveFileExW signature configuration",
    )
    expected_argtypes = ["ctypes.c_wchar_p", "ctypes.c_wchar_p", "ctypes.c_uint32"]
    argtypes_ok = restype_ok = False
    for statement in configure.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1 or not isinstance(statement.targets[0], ast.Attribute):
            continue
        target = statement.targets[0]
        if target.attr == "argtypes" and isinstance(statement.value, ast.List):
            argtypes_ok = [_expr_name(item) for item in statement.value.elts] == expected_argtypes
        if target.attr == "restype":
            restype_ok = _expr_name(statement.value) == "ctypes.c_int32"
    if not argtypes_ok or not restype_ok:
        raise auth_failure("Win32 source lacks the exact argtypes/restype binding")

    binding_init = _method(tree, "MoveFileExBinding", "__init__")
    _require_exact_function_ast(
        binding_init,
        """
def __init__(self) -> None:
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    self._move_file_ex = _configure_move_file_ex(kernel32.MoveFileExW)
""",
        "MoveFileExW loader/export binding",
    )

    call_method = _method(tree, "MoveFileExBinding", "call")
    _require_exact_function_ast(
        call_method,
        r'''
def call(self, source: str, destination: str, flags: int = 0) -> MoveResult:
    if type(source) is not str or type(destination) is not str:
        raise auth_failure("MoveFileExW paths must be exact strings")
    if not source.startswith("\\\\?\\") or not destination.startswith("\\\\?\\"):
        raise auth_failure("MoveFileExW paths must use the extended-length prefix")
    if "\x00" in source or "\x00" in destination:
        raise auth_failure("MoveFileExW paths must not contain embedded NUL")
    if type(flags) is not int or flags != 0:
        raise auth_failure("MoveFileExW flags must be exact numeric zero")
    flag_value = ctypes.c_uint32(flags)
    ctypes.set_last_error(0)
    result = self._move_file_ex(source, destination, flag_value)
    if result == 0:
        last_error = ctypes.get_last_error()
    else:
        last_error = 0
    return MoveResult(ctypes.c_int32(result).value, ctypes.c_uint32(last_error).value)
''',
        "MoveFileExW exact call path",
    )
    if not _contains_exact_flags_zero_guard(call_method):
        raise auth_failure("Win32 source lacks the exact numeric-zero flags guard")
    reset_index = next(
        (index for index, statement in enumerate(call_method.body) if _statement_call_name(statement) == "ctypes.set_last_error" and _single_zero_argument(statement)),
        None,
    )
    invocation_index = next(
        (index for index, statement in enumerate(call_method.body) if _assign_direct_call(statement, "result", "self._move_file_ex")),
        None,
    )
    branch_index = next(
        (index for index, statement in enumerate(call_method.body) if isinstance(statement, ast.If) and _is_result_zero_test(statement.test)),
        None,
    )
    if reset_index is None or invocation_index is None or branch_index is None or not reset_index < invocation_index < branch_index:
        raise auth_failure("Win32 call/reset/branch order is not frozen")
    branch = call_method.body[branch_index]
    assert isinstance(branch, ast.If)
    if not branch.body or not _assign_exact_call(branch.body[0], "last_error", "ctypes.get_last_error"):
        raise auth_failure("failure-path last-error read is not the immediately following branch operation")
    if not branch.orelse or not _assign_exact_constant(branch.orelse[0], "last_error", 0):
        raise auth_failure("success-path last-error sentinel is not literal integer zero")

    move_method = _method(tree, "Win32PublicationBackend", "move_no_replace")
    _require_exact_function_ast(
        move_method,
        """
def move_no_replace(self, source: Path, destination: Path) -> MoveResult:
    source_text = _extended_path(_root_bound_path(self.output_root, source))
    destination_text = _extended_path(_root_bound_path(self.output_root, destination))
    return self._move.call(source_text, destination_text, 0)
""",
        "single no-replace publication adapter",
    )


def _require_exact_function_ast(
    actual: ast.FunctionDef,
    expected_source: str,
    label: str,
) -> None:
    expected_module = ast.parse(expected_source)
    expected = expected_module.body[0]
    assert isinstance(expected, ast.FunctionDef)
    if ast.dump(actual, include_attributes=False) != ast.dump(
        expected,
        include_attributes=False,
    ):
        raise auth_failure(f"Win32 source mutated the exact {label}")


def _call_name(value: ast.expr) -> str:
    return _expr_name(value)


def _expr_name(value: ast.expr) -> str:
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        prefix = _expr_name(value.value)
        return f"{prefix}.{value.attr}" if prefix else value.attr
    return ""


def _function(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise auth_failure(f"Win32 source lacks required function {name}")


def _method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return child
    raise auth_failure(f"Win32 source lacks required method {class_name}.{method_name}")


def _statement_call_name(statement: ast.stmt) -> str:
    if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
        return _call_name(statement.value.func)
    return ""


def _single_zero_argument(statement: ast.stmt) -> bool:
    assert isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call)
    call = statement.value
    return len(call.args) == 1 and isinstance(call.args[0], ast.Constant) and call.args[0].value == 0 and not call.keywords


def _assign_direct_call(statement: ast.stmt, target: str, name: str) -> bool:
    return (
        isinstance(statement, ast.Assign)
        and len(statement.targets) == 1
        and isinstance(statement.targets[0], ast.Name)
        and statement.targets[0].id == target
        and isinstance(statement.value, ast.Call)
        and _call_name(statement.value.func) == name
    )


def _is_result_zero_test(value: ast.expr) -> bool:
    return (
        isinstance(value, ast.Compare)
        and isinstance(value.left, ast.Name)
        and value.left.id == "result"
        and len(value.ops) == 1
        and isinstance(value.ops[0], ast.Eq)
        and len(value.comparators) == 1
        and isinstance(value.comparators[0], ast.Constant)
        and value.comparators[0].value == 0
    )


def _assign_exact_call(statement: ast.stmt, target: str, call_name: str) -> bool:
    return (
        isinstance(statement, ast.Assign)
        and len(statement.targets) == 1
        and isinstance(statement.targets[0], ast.Name)
        and statement.targets[0].id == target
        and isinstance(statement.value, ast.Call)
        and _call_name(statement.value.func) == call_name
        and not statement.value.args
        and not statement.value.keywords
    )


def _assign_exact_constant(statement: ast.stmt, target: str, value: object) -> bool:
    return (
        isinstance(statement, ast.Assign)
        and len(statement.targets) == 1
        and isinstance(statement.targets[0], ast.Name)
        and statement.targets[0].id == target
        and isinstance(statement.value, ast.Constant)
        and statement.value.value == value
    )


def _contains_exact_flags_zero_guard(function: ast.FunctionDef) -> bool:
    for node in ast.walk(function):
        if not isinstance(node, ast.Compare) or not isinstance(node.left, ast.Name) or node.left.id != "flags":
            continue
        if (
            len(node.ops) == 1
            and isinstance(node.ops[0], ast.NotEq)
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Constant)
            and node.comparators[0].value == 0
        ):
            return True
    return False


def audit_win32_source(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise auth_failure("Win32 verifier source path is invalid")
    audit_win32_source_text(path.read_text(encoding="utf-8"))
