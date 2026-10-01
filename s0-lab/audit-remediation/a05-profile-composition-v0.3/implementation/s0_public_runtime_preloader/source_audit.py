"""Non-authoritative structural diagnostic for already supplied source bytes.

This module is defense in depth.  It is not a capability proof, sandbox, or
acceptance authority.  Exact manifest authentication and independent source
review remain mandatory.
"""

from __future__ import annotations

import ast
import re
from types import MappingProxyType

from .errors import RuntimeProfileError


EXPECTED_FILES = (
    "__init__.py",
    "canonical.py",
    "errors.py",
    "evidence.py",
    "integration.py",
    "preloader.py",
    "profile.py",
    "schema.py",
    "semantic.py",
    "source_audit.py",
)
_ALLOWED_DIRECT_MODULES = {
    "__init__.py": set(),
    "canonical.py": {"hashlib", "json", "re"},
    "errors.py": set(),
    "evidence.py": {"re"},
    "integration.py": set(),
    "preloader.py": set(),
    "profile.py": set(),
    "schema.py": {"re"},
    "semantic.py": set(),
    "source_audit.py": {"ast", "re"},
}
_ALLOWED_MODULE_ATTRIBUTES = {
    "canonical.py": {
        "hashlib.sha256",
        "json.JSONDecodeError",
        "json.dumps",
        "json.loads",
        "re.compile",
    },
    "evidence.py": {"re.compile"},
    "profile.py": set(),
    "schema.py": {"re.search"},
    "source_audit.py": {
        "ast.Attribute",
        "ast.AsyncFunctionDef",
        "ast.ClassDef",
        "ast.ExceptHandler",
        "ast.FunctionDef",
        "ast.Import",
        "ast.ImportFrom",
        "ast.Load",
        "ast.MatchAs",
        "ast.MatchMapping",
        "ast.MatchStar",
        "ast.Module",
        "ast.Name",
        "ast.arg",
        "ast.iter_child_nodes",
        "ast.parse",
        "ast.walk",
        "re.findall",
        "re.search",
    },
}
_ALLOWED_ABSOLUTE_FROM = {
    "__future__": {"annotations"},
    "dataclasses": {"dataclass", "replace"},
    "pathlib": {"PurePosixPath"},
    "types": {"MappingProxyType"},
    "typing": {"Mapping"},
}
_ALLOWED_RELATIVE_FROM = {
    "canonical": {
        "canonical_json_bytes",
        "parse_manifest",
        "load_json_bytes",
        "require_sha256",
        "safe_virtual_path",
        "sha256_bytes",
        "verify_manifest_material",
    },
    "errors": {"RuntimeProfileError"},
    "evidence": {
        "LaunchMaterialSet",
        "OfflineAdmissionDiagnostic",
        "OfflineLaunchEvidenceDiagnostic",
        "build_launch_identity",
        "build_offline_launch_evidence_diagnostic",
        "build_offline_admission_diagnostic",
        "load_launch_control",
        "serialize_launch_evidence_v2",
        "parse_launch_evidence_v2",
        "validate_launch_evidence_v2",
    },
    "integration": {
        "AssemblyArtifactBundle",
        "AssemblyArtifactValidation",
        "prepare_assembly_runtime_launch",
        "validate_assembly_artifact_bundle",
    },
    "preloader": {
        "NeutralPreloader",
        "OfflinePreparedLaunch",
        "OfflinePreloaderInputs",
        "OrderedHandleLocators",
        "prepare_offline_admission_diagnostic",
    },
    "profile": {"ValidatedProfileCandidate", "ValidatedSuccessorProfileCandidate", "validate_runtime_profile_candidate", "SuccessorProfileMaterial", "validate_successor_profile_candidate"},
    "source_audit": {"NATIVE_API_INVENTORY", "validate_native_inventory", "inspect_native_source", "pe_imports"},
    "schema": {"FixedDraft202012Validator"},
    "semantic": {
        "ArtifactMaterial",
        "BinaryMaterial",
        "BYTE_VERIFIED_RELATIONS",
        "DEFERRED_STATIC_RELATIONS",
        "HandleObservation",
        "OFFLINE_POSTCREATION_RELATIONS",
        "OFFLINE_PRECREATION_RELATIONS",
        "PostcreationObservation",
        "PrecreationObservation",
        "PredecessorProfileMaterial",
        "StaticMaterialBundle",
        "SystemImageMaterial",
        "_snapshot_postcreation_observation",
        "_snapshot_static_material",
        "validate_postcreation_relation",
        "validate_precreation_relations",
        "validate_static_relations",
    },
}
_FORBIDDEN_NAMES = {
    "__builtins__",
    "__cached__",
    "__file__",
    "__import__",
    "__loader__",
    "__package__",
    "__spec__",
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "input",
    "locals",
    "open",
    "setattr",
    "vars",
}
_FORBIDDEN_ATTRIBUTES = {
    "__annotations__",
    "__base__",
    "__bases__",
    "__builtins__",
    "__class__",
    "__closure__",
    "__code__",
    "__dict__",
    "__getattribute__",
    "__globals__",
    "__loader__",
    "__mro__",
    "__reduce__",
    "__reduce_ex__",
    "__spec__",
    "__subclasses__",
    "__traceback__",
    "absolute",
    "ag_frame",
    "chmod",
    "cr_frame",
    "create_module",
    "cwd",
    "exec_module",
    "exists",
    "expanduser",
    "f_builtins",
    "f_code",
    "f_globals",
    "f_locals",
    "find_spec",
    "get_data",
    "get_filename",
    "gi_frame",
    "glob",
    "hardlink_to",
    "home",
    "is_block_device",
    "is_char_device",
    "is_dir",
    "is_fifo",
    "is_file",
    "is_junction",
    "is_mount",
    "is_socket",
    "iterdir",
    "listdir",
    "load_module",
    "lstat",
    "mkdir",
    "mro",
    "open",
    "owner",
    "popen",
    "read_bytes",
    "read_text",
    "readlink",
    "rename",
    "resolve",
    "rglob",
    "rmdir",
    "samefile",
    "scandir",
    "stat",
    "symlink_to",
    "system",
    "tb_frame",
    "touch",
    "unlink",
    "walk",
    "write_bytes",
    "write_text",
}


def _attribute_chain(node: ast.Attribute) -> str | None:
    parts = [node.attr]
    value = node.value
    while isinstance(value, ast.Attribute):
        parts.append(value.attr)
        value = value.value
    if not isinstance(value, ast.Name):
        return None
    return ".".join((value.id, *reversed(parts)))


def inspect_source_text(filename: str, raw: bytes) -> None:
    """Inspect one exact admitted filename without executing or opening it."""

    if filename not in EXPECTED_FILES or type(raw) is not bytes:
        raise RuntimeProfileError("source audit input is outside the exact inventory")
    if not raw or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise RuntimeProfileError("candidate source bytes are not canonical text")
    try:
        text = raw.decode("utf-8", errors="strict")
        tree = ast.parse(text, filename=filename)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise RuntimeProfileError("candidate source is not strict valid Python") from exc
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    direct_modules = _ALLOWED_DIRECT_MODULES[filename]
    allowed_attributes = _ALLOWED_MODULE_ATTRIBUTES.get(filename, set())
    imported_bindings = {
        alias.asname or alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        alias.asname or alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)) and not isinstance(
            parents.get(node), ast.Module
        ):
            raise RuntimeProfileError("candidate source contains a non-top-level import")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname is not None or alias.name not in direct_modules:
                    raise RuntimeProfileError("candidate source import is outside positive closure")
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" or alias.asname is not None for alias in node.names):
                raise RuntimeProfileError("candidate source uses a wildcard or alias import")
            module = node.module or ""
            allowed = (
                _ALLOWED_RELATIVE_FROM.get(module)
                if node.level == 1
                else _ALLOWED_ABSOLUTE_FROM.get(module)
                if node.level == 0
                else None
            )
            if allowed is None or any(alias.name not in allowed for alias in node.names):
                raise RuntimeProfileError("candidate from-import is outside positive closure")
        elif isinstance(node, ast.Name) and node.id in _FORBIDDEN_NAMES:
            raise RuntimeProfileError("candidate source uses dynamic or ambient authority")
        elif (
            isinstance(node, ast.Name)
            and not isinstance(node.ctx, ast.Load)
            and node.id in imported_bindings
        ):
            raise RuntimeProfileError("candidate source rebinds an imported authority")
        elif isinstance(node, ast.arg) and node.arg in imported_bindings:
            raise RuntimeProfileError("candidate source shadows an imported authority")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and (
            node.name in imported_bindings
        ):
            raise RuntimeProfileError("candidate source shadows an imported authority")
        elif isinstance(node, ast.ExceptHandler) and node.name in imported_bindings:
            raise RuntimeProfileError("candidate source shadows an imported authority")
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)) and (
            node.name in imported_bindings
        ):
            raise RuntimeProfileError("candidate source pattern-shadows an imported authority")
        elif isinstance(node, ast.MatchMapping) and node.rest in imported_bindings:
            raise RuntimeProfileError("candidate source pattern-shadows an imported authority")
        elif isinstance(node, ast.Attribute):
            chain = _attribute_chain(node)
            if node.attr in _FORBIDDEN_ATTRIBUTES and chain not in allowed_attributes:
                raise RuntimeProfileError("candidate source uses interpreter or file authority")
            if chain is not None and chain.split(".", 1)[0] in direct_modules:
                if chain not in allowed_attributes:
                    raise RuntimeProfileError("candidate source uses an unapproved module attribute")
            if (
                chain is not None
                and chain.split(".", 1)[0] in imported_bindings
                and not isinstance(node.ctx, ast.Load)
            ):
                raise RuntimeProfileError("candidate source mutates an imported authority")
        if (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in direct_modules
        ):
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                raise RuntimeProfileError("candidate source launders an imported module")


def inspect_source_structure(sources: dict[str, bytes]) -> tuple[str, ...]:
    """Inspect an already supplied exact byte mapping; never touch a path."""

    if type(sources) is not dict or tuple(sorted(sources)) != EXPECTED_FILES:
        raise RuntimeProfileError("candidate source inventory is not exact")
    for filename, raw in sources.items():
        if type(filename) is not str or type(raw) is not bytes:
            raise RuntimeProfileError("candidate source mapping is not exact bytes")
        inspect_source_text(filename, raw)
    return EXPECTED_FILES


NATIVE_API_INVENTORY = MappingProxyType({
    "guard": MappingProxyType({
        "decision_semantic_calls": ("CompareStringOrdinal", "GetCurrentProcessId", "GetFileInformationByHandleEx", "GetFileType", "GetHandleInformation", "GetNamedPipeInfo", "GetProcessId", "InterlockedCompareExchange", "InterlockedExchange", "IsProcessInJob", "MultiByteToWideChar", "NtQueryInformationProcess", "NtQueryObject", "PeekNamedPipe", "QueryFullProcessImageNameW", "ReadFile", "WaitForSingleObject", "WriteFile",),
        "supporting_calls": ("CloseHandle", "GetCurrentProcess", "GetLastError", "SecureZeroMemory",),
        "direct_import_families": ("kernel32.dll", "ntdll.dll", "python312.dll", "static-crt-support",),
    }),
    "preloader": MappingProxyType({
        "decision_semantic_calls": ("AssignProcessToJobObject", "BCryptCloseAlgorithmProvider", "BCryptCreateHash", "BCryptDestroyHash", "BCryptFinishHash", "BCryptGetProperty", "BCryptHashData", "BCryptOpenAlgorithmProvider", "CompareStringOrdinal", "CreateFileW", "CreateJobObjectW", "CreatePipe", "CreateProcessW", "DuplicateHandle", "FindFirstFileW", "FindNextFileW", "GetCurrentProcessId", "GetDriveTypeW", "GetExitCodeProcess", "GetFileAttributesExW", "GetFileAttributesW", "GetFileInformationByHandleEx", "GetFileSizeEx", "GetFileType", "GetFinalPathNameByHandleW", "GetFullPathNameW", "GetHandleInformation", "GetVolumeInformationByHandleW", "GetVolumePathNameW", "InitializeProcThreadAttributeList", "MultiByteToWideChar", "NtCreateFile", "NtQueryObject", "OpenProcess", "PeekNamedPipe", "ReadFile", "ResumeThread", "SetFilePointerEx", "SetHandleInformation", "SetInformationJobObject", "UpdateProcThreadAttribute", "WaitForSingleObject", "WideCharToMultiByte", "WriteFile",),
        "supporting_calls": ("CloseHandle", "DeleteProcThreadAttributeList", "FindClose", "GetCurrentProcess", "GetLastError", "GetTickCount", "Sleep", "TerminateProcess",),
        "direct_import_families": ("bcrypt.dll", "kernel32.dll", "ntdll.dll", "static-crt-support",),
    }),
    "materializer": MappingProxyType({
        "decision_semantic_calls": ("AccessCheck", "BCryptCloseAlgorithmProvider", "BCryptCreateHash", "BCryptDestroyHash", "BCryptFinishHash", "BCryptGetProperty", "BCryptHashData", "BCryptOpenAlgorithmProvider", "DuplicateHandle", "FindFirstFileW", "FindFirstStreamW", "FindNextFileW", "FindNextStreamW", "FlushFileBuffers", "GetDriveTypeW", "GetFileInformationByHandleEx", "GetFinalPathNameByHandleW", "GetSecurityInfo", "GetTokenInformation", "GetVolumeInformationByHandleW", "NtCreateFile", "NtQueryObject", "ReadFile", "SetFilePointerEx", "WriteFile",),
        "supporting_calls": ("CloseHandle", "FindClose", "GetLastError", "LocalFree",),
        "direct_import_families": ("advapi32.dll", "bcrypt.dll", "kernel32.dll", "ntdll.dll", "static-crt-support",),
    }),
})


def _cpp_identifiers(raw: bytes) -> list[str]:
    if type(raw) is not bytes or not raw or len(raw) > 1024 * 1024:
        raise RuntimeProfileError("native source byte bound differs")
    try:
        source = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RuntimeProfileError("native source encoding differs") from exc
    # Remove comments and literals before call classification. This is a bounded
    # structural audit; independent C++/compiler/import review remains required.
    cleaned: list[str] = []
    i = 0
    while i < len(source):
        if source.startswith("//", i):
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
        elif source.startswith("/*", i):
            end = source.find("*/", i + 2)
            if end < 0:
                raise RuntimeProfileError("unterminated native comment")
            i = end + 2
            cleaned.append(" ")
        elif source[i] in {'"', "'"}:
            quote = source[i]
            i += 1
            while i < len(source) and source[i] != quote:
                i += 2 if source[i] == "\\" else 1
            if i >= len(source):
                raise RuntimeProfileError("unterminated native literal")
            i += 1
            cleaned.append(" ")
        else:
            cleaned.append(source[i])
            i += 1
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*|::|->|[(){};.*&#]", "".join(cleaned))


def inspect_native_source(role: str, raw: bytes) -> tuple[str, ...]:
    if role not in NATIVE_API_INVENTORY:
        raise RuntimeProfileError("native source role is not exact")
    expected = set(NATIVE_API_INVENTORY[role]["decision_semantic_calls"]) | set(
        NATIVE_API_INVENTORY[role]["supporting_calls"]
    )
    all_frozen = set().union(*(
        set(row["decision_semantic_calls"]) | set(row["supporting_calls"])
        for row in NATIVE_API_INVENTORY.values()
    ))
    tokens = _cpp_identifiers(raw)
    calls = {tokens[i] for i in range(len(tokens) - 1) if tokens[i + 1] == "("}
    observed = calls & all_frozen
    if observed != expected:
        raise RuntimeProfileError("native source relied API set differs from effective role inventory")
    forbidden = {
        "GetProcAddress", "LoadLibraryA", "LoadLibraryW", "LoadLibraryExA", "LoadLibraryExW",
        "CreateProcessA", "CreateProcessAsUserW", "CreateProcessWithTokenW", "ShellExecuteW",
        "WinExec", "system", "_wsystem", "NtOpenFile", "ZwCreateFile", "OpenProcessToken",
        "OpenThreadToken", "DuplicateToken", "DuplicateTokenEx", "SetThreadToken",
        "ImpersonateSelf", "NtSetInformationFile", "SetFileInformationByHandle",
    }
    if calls & forbidden:
        raise RuntimeProfileError("native source contains an alternate API route")
    # Locally defined wrappers are not foreign APIs. Unknown Windows-family
    # names require rejection rather than silently disappearing from inventory.
    local: set[str] = set()
    for i in range(len(tokens) - 1):
        if tokens[i + 1] != "(":
            continue
        depth = 1
        end = i + 2
        while end < len(tokens) and depth:
            depth += (tokens[end] == "(") - (tokens[end] == ")")
            end += 1
        while end < len(tokens) and tokens[end] in {"const", "noexcept", "override", "final"}:
            end += 1
        if end < len(tokens) and tokens[end] in {"{", ":"}:
            local.add(tokens[i])
    for call in calls - expected - local:
        if re.search(
            r"^(?:Get|Set|Create|Open|Close|Find|ReadFile|WriteFile|AccessCheck|"
            r"Duplicate|Nt[A-Z]|Zw[A-Z]|Rtl[A-Z]|BCrypt|Crypt|LoadLibrary|"
            r"Query[A-Z]|WaitFor|Interlocked|FlushFile|DeviceIoControl|"
            r"Reg[A-Z]|Virtual[A-Z]|Heap[A-Z]|LocalFree|MapView|UnmapView)",
            call,
        ):
            raise RuntimeProfileError("native source contains an unclassified Windows API")
    return tuple(sorted(observed))


def pe_imports(raw: bytes) -> tuple[tuple[str, str], ...]:
    """Read the exact PE32+ import tables of already authenticated binary bytes."""
    if type(raw) is not bytes or not 512 <= len(raw) <= 64 * 1024 * 1024 or raw[:2] != b"MZ":
        raise RuntimeProfileError("native binary is not bounded PE bytes")

    def integer(offset: int, size: int) -> int:
        if offset < 0 or offset + size > len(raw):
            raise RuntimeProfileError("PE field is out of bounds")
        return int.from_bytes(raw[offset:offset + size], "little")

    pe = integer(0x3C, 4)
    if raw[pe:pe + 4] != b"PE\0\0" or integer(pe + 4, 2) != 0x8664:
        raise RuntimeProfileError("native binary is not Windows x64 PE")
    count = integer(pe + 6, 2)
    optional = pe + 24
    optional_size = integer(pe + 20, 2)
    if integer(optional, 2) != 0x20B or not 1 <= count <= 96 or optional_size < 240:
        raise RuntimeProfileError("native PE optional header differs")
    sections = optional + optional_size

    def address(rva: int, size: int = 1) -> int:
        if rva < integer(optional + 60, 4) and rva + size <= len(raw):
            return rva
        for index in range(count):
            offset = sections + index * 40
            virtual = integer(offset + 12, 4)
            raw_size = integer(offset + 16, 4)
            pointer = integer(offset + 20, 4)
            if virtual <= rva and rva + size <= virtual + raw_size:
                result = pointer + rva - virtual
                if result + size <= len(raw):
                    return result
        raise RuntimeProfileError("native PE RVA is outside backed bytes")

    def string(rva: int) -> str:
        chars = bytearray()
        for index in range(1024):
            char = raw[address(rva + index)]
            if not char:
                try:
                    return chars.decode("ascii", errors="strict")
                except UnicodeDecodeError as exc:
                    raise RuntimeProfileError("native PE import is not ASCII") from exc
            chars.append(char)
        raise RuntimeProfileError("native PE import string exceeds bound")

    # Delay-load and CLR routes are outside this native contract.
    if integer(optional + 112 + 13 * 8, 4) or integer(optional + 112 + 14 * 8, 4):
        raise RuntimeProfileError("native binary has a delayed or managed import route")
    directory = integer(optional + 120, 4)
    directory_size = integer(optional + 124, 4)
    if not directory or directory_size < 20:
        raise RuntimeProfileError("native PE import directory is absent")
    imports: set[tuple[str, str]] = set()
    for index in range(128):
        if index * 20 + 20 > directory_size:
            raise RuntimeProfileError("native import descriptor exceeds directory")
        descriptor = address(directory + index * 20, 20)
        fields = tuple(integer(descriptor + n * 4, 4) for n in range(5))
        if fields == (0, 0, 0, 0, 0):
            return tuple(sorted(imports))
        library = string(fields[3]).lower()
        if "/" in library or "\\" in library or not library.endswith(".dll"):
            raise RuntimeProfileError("native import family is not canonical")
        thunk = fields[0] or fields[4]
        for position in range(8192):
            value = integer(address(thunk + position * 8, 8), 8)
            if not value:
                break
            if value & (1 << 63):
                raise RuntimeProfileError("ordinal native imports are outside exact symbol contract")
            symbol = string(value + 2)
            if (library, symbol) in imports:
                raise RuntimeProfileError("duplicate native import")
            imports.add((library, symbol))
        else:
            raise RuntimeProfileError("native import thunk exceeds bound")
    raise RuntimeProfileError("native import descriptors exceed bound")


def validate_native_inventory(
    role: str, *, source_raw: bytes, binary_raw: bytes, profile_inventory: dict,
    import_resolution: dict[str, tuple[str, str]], crt_imports: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    """Check supplied source/profile/PE equality; never assert loaded-image truth."""
    expected = NATIVE_API_INVENTORY.get(role)
    if expected is None or profile_inventory != {key: list(values) for key, values in expected.items()}:
        raise RuntimeProfileError("profile native API partition differs")
    calls = inspect_native_source(role, source_raw)
    if type(import_resolution) is not dict or set(import_resolution) != set(calls):
        raise RuntimeProfileError("source/import resolution call set differs")
    imports = set(pe_imports(binary_raw))
    if type(crt_imports) is not tuple or crt_imports != tuple(sorted(set(crt_imports))):
        raise RuntimeProfileError("CRT support import list is not sorted unique")
    covered = set(crt_imports)
    families = set(expected["direct_import_families"]) - {"static-crt-support"}
    for call, target in import_resolution.items():
        if type(target) is not tuple or len(target) != 2:
            raise RuntimeProfileError("native import resolution row is not exact")
        if target == ("compiler-intrinsic", call):
            if call not in {"InterlockedCompareExchange", "InterlockedExchange", "SecureZeroMemory"}:
                raise RuntimeProfileError("native API is not an admitted intrinsic")
        else:
            if target[0] not in families or target[1] != call or target not in imports:
                raise RuntimeProfileError("native API import is absent, alternate, or wrong-family")
            covered.add(target)
    if covered != imports or {family for family, _ in imports} - families:
        raise RuntimeProfileError("unclassified binary import or missing CRT support import")
    return calls
