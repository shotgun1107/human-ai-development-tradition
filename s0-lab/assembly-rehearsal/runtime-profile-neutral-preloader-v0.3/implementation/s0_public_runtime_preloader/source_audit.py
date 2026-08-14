"""Non-authoritative structural diagnostic for already supplied source bytes.

This module is defense in depth.  It is not a capability proof, sandbox, or
acceptance authority.  Exact manifest authentication and independent source
review remain mandatory.
"""

from __future__ import annotations

import ast

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
    "profile.py": {"copy"},
    "schema.py": {"re"},
    "semantic.py": set(),
    "source_audit.py": {"ast"},
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
    "profile.py": {"copy.deepcopy"},
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
    },
}
_ALLOWED_ABSOLUTE_FROM = {
    "__future__": {"annotations"},
    "dataclasses": {"dataclass"},
    "pathlib": {"PurePosixPath"},
    "types": {"MappingProxyType"},
    "typing": {"Mapping"},
}
_ALLOWED_RELATIVE_FROM = {
    "canonical": {
        "canonical_json_bytes",
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
    "profile": {"ValidatedProfileCandidate", "validate_runtime_profile_candidate"},
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
