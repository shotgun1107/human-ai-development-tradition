"""Bounded A05 data-flow checks; NOT a historical/native/assembly/S0 pass.

The positive composition lane replaces the unavailable historical validator,
design closure, overlay-schema validation, native closure, and predecessor pins
with explicitly named unittest doubles. Current closure, snapshots, canonical
composition, launch/evidence/admission consumers, and negative gates stay real.
Benign in-memory parameters are not historical fixtures or executable payloads.
Only this file and the two explicitly allowed verification outputs are written.
"""

from __future__ import annotations

import ast
from collections import UserDict
from contextlib import ExitStack, contextmanager
from dataclasses import FrozenInstanceError, fields, replace
import hashlib
import json
from pathlib import Path
import stat
import sys
from types import MappingProxyType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch


ROOT = Path("C:/Users/SSAFY/Documents/ai-development-tradition")
CANDIDATE = ROOT / "s0-lab/audit-remediation/a05-profile-composition-v0.3"
PREDECESSOR = ROOT / "s0-lab/audit-remediation/a05-profile-composition-v0.2"
PREDECESSOR_SOURCE = PREDECESSOR / "implementation/s0_public_runtime_preloader"
PREVIOUS = ROOT / "s0-lab/audit-remediation/a05-profile-composition-v0.1"
PREVIOUS_SOURCE = PREVIOUS / "implementation/s0_public_runtime_preloader"
SOURCE = CANDIDATE / "implementation/s0_public_runtime_preloader"
ORIGINAL = ROOT / "docs/maintenance/audit-2026-09-09/f03-source-recovery-2026-09-16/implementation/s0_public_runtime_preloader"
RECOVERY = ROOT / "docs/maintenance/audit-2026-09-09/f03-input-recovery-2026-09-17"
INTERPRETER = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
MODULE_PINS = {
    "__init__.py": "a2e40d7a44f79f3c0f96b790c2249fcb6efe7dba2abf821ea3ee96302f1570c3",
    "canonical.py": "f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4",
    "errors.py": "20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86",
    "evidence.py": "e0f1d9de22eb8b7a727dbef146f808c59d44accbbb96fa3367ee2d0dfdbdd964",
    "integration.py": "7d40c5091c43354287fade09f8e11d2ca6a830492d390385d8b13cee361a3dfd",
    "preloader.py": "718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee",
    "profile.py": "efae38b6a99763c0dca61efe2813c11672cf784a28ea1f0747937f80e260501a",
    "schema.py": "97b00ab0bb9417b63c5871332751e8c14dea80423414810e99aa2b443f9d6317",
    "semantic.py": "1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d",
    "source_audit.py": "50399a565232136736e041ea028b76ed8767d18327553ecf2ec6ec5b0bfe2d36",
}
PREDECESSOR_PINS = dict(MODULE_PINS, **{
    "profile.py": "0c0c451a0be41c5593fb3937192da61ae1728534d12e114e0fda9b7a4e297c14",
})
PREVIOUS_PINS = dict(PREDECESSOR_PINS, **{
    "source_audit.py": "c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99",
})
ORIGINAL_PINS = dict(PREVIOUS_PINS, **{
    "profile.py": "c5c1f6c6c937e45b9da246b24783134570a48923501757ab4683173a5367fe89",
    "preloader.py": "b6f343c7a0a0c3ebe075eed386ff53d08abda507116ca19d1e7b7985aabd1c59",
})
HISTORICAL_PATH = RECOVERY / "historical/runtime-profile-v0.4.json"
SCHEMA_PATH = RECOVERY / "design/findclose-amendment-v0.1/runtime-profile-v0.5.schema.json"
MAP_PATH = RECOVERY / "design/findclose-amendment-v0.1/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json"
HISTORICAL_SCHEMA_PATH = ROOT / "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.json"
PINS = {SOURCE / name: digest for name, digest in MODULE_PINS.items()}
PINS.update({ORIGINAL / name: digest for name, digest in ORIGINAL_PINS.items()})
PINS.update({PREVIOUS_SOURCE / name: digest for name, digest in PREVIOUS_PINS.items()})
PINS.update({PREDECESSOR_SOURCE / name: digest for name, digest in PREDECESSOR_PINS.items()})
PINS.update({
    PREDECESSOR / "tests/test_profile_composition.py": "c06c03bcef51ca143f078aab5f9fe0ca3d959e46abf250d0a77f6f53c56c0de1",
    PREDECESSOR / "verification/test-results.json": "ea204f87902ea5accc53ee0188a2c3a90a1d3288a9a086475e07fd72dff56433",
    PREDECESSOR / "verification/test-stdout.txt": "296546ef7fef781821d9060278a10ef1fdd214b774899f56a47343c357f5d518",
})
PINS.update({
    PREVIOUS / "candidate-files.sha256": "b2505ce58732de16185f434f9e4ece1c8c2345aba80bc165f3a2df43cc217802",
    PREVIOUS / "tests/test_profile_composition.py": "a1a20ede2c99ebb6e0fa8b8196d6e809f63d13f22418fd7ad193806830fc6812",
    PREVIOUS / "verification/test-results.json": "03277de88f8c3353c72aefcc7fbb3723fb633bd385b89027b8cf9cc92a71af77",
    PREVIOUS / "diagnostics/test_source_closure.py": "97cc7c13dcbce10a2d6785cd1e00f7f3c46255c07397be282ae0d6ce17d59279",
    PREVIOUS / "diagnostics/source-closure-results.json": "0788ea1856080b729f8e6a6d3fa1c99cc95d216dadd9b825a9e0d25af98039c3",
    PREVIOUS / "diagnostics/source-closure-stdout.txt": "94fdf5acb546fbc2d86c77e6f391dfef6092331db61e1f2329488becb57e5573",
})
PINS.update({
    ROOT / "AGENTS.md": "393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e",
    HISTORICAL_PATH: "266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e",
    SCHEMA_PATH: "04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e",
    MAP_PATH: "f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623",
    HISTORICAL_SCHEMA_PATH: "3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd",
    INTERPRETER: "4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a",
})
REPRODUCIBLE_COMMAND = (
    "& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' "
    "-I -S -B -X utf8 "
    "'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/"
    "a05-profile-composition-v0.3/tests/test_profile_composition.py'"
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticate():
    observed = {}
    for path, expected in PINS.items():
        raw = path.read_bytes()
        value = digest(raw)
        if value != expected:
            raise RuntimeError("frozen allowlisted input hash differs: " + path.name)
        observed[str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)] = value
    return observed


# Authenticate the manifest before using its exact 17 paths for hash-only checks.
_previous_manifest_raw = (PREVIOUS / "candidate-files.sha256").read_bytes()
if digest(_previous_manifest_raw) != PINS[PREVIOUS / "candidate-files.sha256"]:
    raise RuntimeError("previous frozen manifest hash differs")
_previous_rows = [line.split("  ", 1) for line in _previous_manifest_raw.decode("utf-8").splitlines() if line]
if len(_previous_rows) != 17:
    raise RuntimeError("previous frozen manifest count differs")
for _expected, _relative in _previous_rows:
    if not _relative.startswith("s0-lab/audit-remediation/a05-profile-composition-v0.1/") or ".." in Path(_relative).parts:
        raise RuntimeError("previous frozen manifest target outside allowlist")
    PINS[ROOT / _relative] = _expected

PRE_HASHES = authenticate()
SELF_HASH = digest(Path(__file__).read_bytes())
if Path(sys.executable).resolve() != INTERPRETER.resolve() or sys.version_info[:3] != (3, 12, 10):
    raise RuntimeError("interpreter identity/version differs")
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.utf8_mode):
    raise RuntimeError("required interpreter flags absent")


def deny_external_execution(event, arguments):
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.startfile", "ctypes.dlopen"}:
        raise RuntimeError("bounded test prohibits network/process/native loading")


sys.addaudithook(deny_external_execution)
sys.path.insert(0, str(SOURCE.parent))
from s0_public_runtime_preloader import canonical as canon  # noqa: E402
from s0_public_runtime_preloader import evidence as evidence_mod  # noqa: E402
from s0_public_runtime_preloader import preloader as loader  # noqa: E402
from s0_public_runtime_preloader import profile as profile_mod  # noqa: E402
from s0_public_runtime_preloader import semantic as semantic  # noqa: E402
from s0_public_runtime_preloader import source_audit as audit_mod  # noqa: E402
from s0_public_runtime_preloader.errors import RuntimeProfileError  # noqa: E402


HISTORICAL_RAW = HISTORICAL_PATH.read_bytes()
HISTORICAL_SCHEMA = HISTORICAL_SCHEMA_PATH.read_bytes()
SUCCESSOR_SCHEMA = SCHEMA_PATH.read_bytes()
SUCCESSOR_MAP = MAP_PATH.read_bytes()
ORIGINAL_PROFILE_AST = ast.parse((ORIGINAL / "profile.py").read_bytes())
CANDIDATE_PROFILE_AST = ast.parse((SOURCE / "profile.py").read_bytes())
SOURCE_BYTES = {name: (SOURCE / name).read_bytes() for name in MODULE_PINS}
PREVIOUS_SOURCE_BYTES = {name: (PREVIOUS_SOURCE / name).read_bytes() for name in PREVIOUS_PINS}
PREDECESSOR_SOURCE_BYTES = {name: (PREDECESSOR_SOURCE / name).read_bytes() for name in PREDECESSOR_PINS}
SOURCE_OBSERVATIONS = []
BYTE_RELATIONS = semantic.BYTE_VERIFIED_RELATIONS
DEFERRED_RELATIONS = semantic.DEFERRED_STATIC_RELATIONS
PACKAGE_NAMES = (
    "runtime-files.sha256", "runtime-profile-v0.1.json", "runtime-profile-v0.2.json",
    "runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json",
)
MOCKS = [
    "Positive composition: validate_runtime_profile_candidate returns a coherent data-only P4 wrapper; no historical success asserted.",
    "Positive composition: P1-P3 pin constants are temporarily replaced with harmless unit-parameter hashes; P4 is actual pinned raw input.",
    "Positive composition: _successor_design_bytes and _successor_native_bytes are no-op call spies.",
    "Positive composition: FixedDraft202012Validator.validate is a no-op for the minimal overlay; real v0.5 schema/map byte pins remain checked.",
    "Bound tests: _MAX_RUNTIME_BYTES temporarily set to 3; 512-file count bound tested without replacement.",
    "Consumer tests: unavailable upstream gates use the same composition doubles; downstream launch parsing, identity, evidence, precreation and admission are real.",
    "Negative diagnostic tests individually replace preceding gates to isolate their target; no mock result establishes real prerequisites.",
]
UNVERIFIED = [
    "Complete positive original historical P4 validator and original archive/native/assembly execution.",
    "Native ArtifactMaterial.virtual_path to current runtime-manifest key mapping; no aliases or binding inferred.",
    "Actual native binary/executed/imported byte closure, installed interpreter stdlib/native closure, and hostile interpreter/global compromise.",
    "Windows ACL, volume/root identity, symlink/junction/reparse, rename/replacement, retained handles, repository exclusion, and TOCTOU through output/evidence writes.",
    "External artifact URL, redirect, digest/size/provenance download verification; no external request occurs.",
    "S0/E0 fixtures, hidden oracle, execution/scoring, provider calls, operational safety, economic value, and model transfer.",
]


def manifest(files):
    return b"".join((digest(files[name]) + "  " + name + "\n").encode("ascii") for name in sorted(files))


def control_bytes(label):
    return canon.canonical_json_bytes({
        "application_path": "C:\\unit\\" + label + ".exe",
        "application_virtual_path": "runtime/application.bin",
        "bootstrap_virtual_path": "runtime/bootstrap.py",
        "command_line": label + " unit-argument",
        "current_directory": "C:\\unit",
        "environment_block": ["UNIT_KIND=" + label],
        "preloader_virtual_path": "runtime/preloader.bin",
        "verifier_virtual_path": "runtime/verifier.py",
    })


def runtime_files(label):
    return {
        "runtime/launch-inputs.json": control_bytes(label),
        "runtime/application.bin": (label + " application data").encode(),
        "runtime/bootstrap.py": (label + " bootstrap data").encode(),
        "runtime/preloader.bin": (label + " preloader data").encode(),
        "runtime/verifier.py": (label + " verifier data").encode(),
    }


class UnitParameters:
    """Deliberately incomplete static bundle; must never pass real P4 validation."""

    def __init__(self):
        self.predecessor_raws = tuple(canon.canonical_json_bytes({"unit_parameter": n}) for n in range(1, 4))
        self.unit_pins = tuple(digest(raw) for raw in self.predecessor_raws) + (digest(HISTORICAL_RAW),)
        self.artifact = semantic.ArtifactMaterial("unit/semantic.py", b"benign unit bytes")
        self.overlay = canon.canonical_json_bytes({
            "semantic_validator": {"implementation": {
                "virtual_path": self.artifact.virtual_path, "sha256": self.artifact.sha256,
            }},
            "launch_handle_set_evidence": {"evidence_schema_id": "S0-LAUNCH-HANDLE-SET-EVIDENCE-2"},
        })
        self.current_files = runtime_files("current")
        self.current_manifest = manifest(self.current_files)
        self.package_files = dict(zip(PACKAGE_NAMES, (self.current_manifest, *self.predecessor_raws, HISTORICAL_RAW, self.overlay), strict=True))
        self.package_manifest = manifest(self.package_files)
        self.source_maps = {"design_files": {}, "implementation_files": {}, "native_sources": {}, "native_binaries": {}, "import_resolution": {}, "crt_imports": {}}
        self.kwargs = dict(
            profile_raw=self.overlay, schema_raw=SUCCESSOR_SCHEMA, interface_map_raw=SUCCESSOR_MAP,
            semantic_validator=self.artifact, implementation_manifest_raw=b"unit implementation manifest\n",
            implementation_manifest_sha256=digest(b"unit implementation manifest\n"),
            runtime_authority=self.artifact, build_trace=self.artifact,
            effective_package_manifest_raw=self.package_manifest, effective_package_files=self.package_files,
            current_runtime_manifest_raw=self.current_manifest,
            expected_current_runtime_manifest_sha256=digest(self.current_manifest),
            current_runtime_files=self.current_files, **self.source_maps,
        )
        self.successor = profile_mod.SuccessorProfileMaterial(**self.kwargs)
        historical_files = runtime_files("historical")
        historical_manifest = manifest(historical_files)
        predecessors = tuple(semantic.PredecessorProfileMaterial(raw, b"{}\n", digest(b"{}\n")) for raw in self.predecessor_raws)
        images = tuple(semantic.SystemImageMaterial(
            "unit/" + name + ".dll", b"unit image data", "a" * 32, "0x1", "0x1", "0x1",
            name, "0x1", (("UnitExport", "0x1"),), name + ".dll!UnitExport",
        ) for name in ("kernel32", "ntdll"))
        self.static = semantic.StaticMaterialBundle(
            predecessors, semantic.ArtifactMaterial("runtime-files.sha256", historical_manifest),
            historical_files, b"historical unit package\n", {}, (self.artifact,) * 8,
            self.artifact, self.artifact, images, self.artifact,
        )
        self.base = profile_mod.ValidatedProfileCandidate(
            json.loads(HISTORICAL_RAW), HISTORICAL_RAW, digest(HISTORICAL_RAW), BYTE_RELATIONS,
        )

    def validate(self, successor=None, static=None):
        return profile_mod.validate_successor_profile_candidate(
            profile_raw=HISTORICAL_RAW, schema_raw=HISTORICAL_SCHEMA,
            static_material=self.static if static is None else static,
            successor=self.successor if successor is None else successor,
        )

    @contextmanager
    def missing_prerequisite_doubles(self):
        with ExitStack() as stack:
            doubles = {}
            doubles["historical"] = stack.enter_context(patch.object(profile_mod, "validate_runtime_profile_candidate", return_value=self.base))
            stack.enter_context(patch.object(profile_mod, "_PREDECESSOR_PROFILE_PINS", self.unit_pins))
            doubles["design"] = stack.enter_context(patch.object(profile_mod, "_successor_design_bytes"))
            doubles["schema"] = stack.enter_context(patch.object(profile_mod.FixedDraft202012Validator, "validate"))
            doubles["native"] = stack.enter_context(patch.object(profile_mod, "_successor_native_bytes"))
            yield doubles

    def rows(self, **updates):
        values = dict(manifest_raw=self.current_manifest, manifest_sha256=digest(self.current_manifest),
                      files=profile_mod._snapshot_current_files(self.current_files, "unit current"),
                      package_raw=self.package_manifest,
                      package_files=profile_mod._snapshot_current_files(self.package_files, "unit package"),
                      historical_raw=HISTORICAL_RAW, overlay_raw=self.overlay)
        values.update(updates)
        with patch.object(profile_mod, "_PREDECESSOR_PROFILE_PINS", self.unit_pins):
            return profile_mod._current_package_rows(**values)


class PreservationAndGates(unittest.TestCase):
    def setUp(self):
        self.data = UnitParameters()

    def test_original_semantic_evidence_integration_canonical_and_schema_are_byte_identical(self):
        # source_audit now has four separately checked, explicitly frozen set deltas.
        for name in ("semantic.py", "evidence.py", "integration.py", "canonical.py", "schema.py"):
            with self.subTest(module=name):
                self.assertEqual((SOURCE / name).read_bytes(), (ORIGINAL / name).read_bytes())

    def test_historical_design_and_native_gate_bodies_are_unchanged(self):
        def body(tree, name):
            return ast.dump(next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name), include_attributes=False)
        for name in ("validate_runtime_profile_candidate", "_successor_design_bytes", "_successor_native_bytes"):
            with self.subTest(function=name):
                self.assertEqual(body(ORIGINAL_PROFILE_AST, name), body(CANDIDATE_PROFILE_AST, name))

    def test_frozen_pins_and_historical_relation_scope_are_preserved(self):
        self.assertEqual(profile_mod._PREDECESSOR_PROFILE_PINS, (
            "e0f7559d16068cc4cb6589a87fdb2129915ab018a76e41cfc09b4259d543008e",
            "3a0f2fd92629e4a3eb419ab2ae2dbc586bf83ae7152a8b08cfdcabc966028125",
            "9741561972db10c39b824b60364219a07e1e1a440f154b562bae91f864aeb8c5",
            digest(HISTORICAL_RAW),
        ))
        self.assertEqual(self.data.base.static_relations_scope, "historical-profile-v0.4")
        self.assertEqual(self.data.base.deferred_static_relations, DEFERRED_RELATIONS)

    def test_actual_historical_schema_pin_failure_prevents_successor_work(self):
        with patch.object(profile_mod, "_successor_design_bytes") as design:
            with self.assertRaisesRegex(RuntimeProfileError, "schema bytes differ"):
                profile_mod.validate_successor_profile_candidate(
                    profile_raw=HISTORICAL_RAW, schema_raw=b"{}\n", static_material=self.data.static, successor=object())
            design.assert_not_called()

    def test_actual_historical_semantic_rejection_prevents_successor_work(self):
        # Real pinned P4 schema and P4 JSON are evaluated; incomplete unit predecessors reject.
        with patch.object(profile_mod, "_successor_design_bytes") as design:
            with patch.object(profile_mod, "validate_static_relations", wraps=semantic.validate_static_relations) as real_semantics:
                with self.assertRaisesRegex(RuntimeProfileError, "profile-predecessor-hashes-equal"):
                    self.data.validate()
                real_semantics.assert_called_once()
            design.assert_not_called()

    def test_historical_validator_is_first_even_with_invalid_successor(self):
        with patch.object(profile_mod, "validate_runtime_profile_candidate", side_effect=RuntimeProfileError("unit historical failure")) as historical:
            with patch.object(profile_mod, "_successor_design_bytes") as design:
                with self.assertRaisesRegex(RuntimeProfileError, "unit historical failure"):
                    self.data.validate(successor=object())
                historical.assert_called_once_with(profile_raw=HISTORICAL_RAW, schema_raw=HISTORICAL_SCHEMA, static_material=self.data.static)
                design.assert_not_called()

    def test_real_predecessor_pin_gate_rejects_substitution_and_order(self):
        with patch.object(profile_mod, "validate_runtime_profile_candidate", return_value=self.data.base):
            with patch.object(profile_mod, "_successor_design_bytes") as design:
                with self.assertRaisesRegex(RuntimeProfileError, "predecessor profile pins differ"):
                    self.data.validate()
                design.assert_not_called()
        with self.data.missing_prerequisite_doubles() as doubles:
            reversed_static = replace(self.data.static, predecessors=tuple(reversed(self.data.static.predecessors)))
            with self.assertRaisesRegex(RuntimeProfileError, "predecessor profile pins differ"):
                self.data.validate(static=reversed_static)
            doubles["design"].assert_not_called()

    def test_actual_design_gate_rejects_missing_frozen_material(self):
        with self.assertRaisesRegex(RuntimeProfileError, "design manifest pin differs"):
            profile_mod._successor_design_bytes(self.data.successor)

    def test_actual_schema_map_pin_gates_reject_before_native_or_composition(self):
        for field in ("schema_raw", "interface_map_raw"):
            with self.subTest(field=field), self.data.missing_prerequisite_doubles() as doubles:
                with self.assertRaisesRegex(RuntimeProfileError, "effective schema/map pins differ"):
                    self.data.validate(replace(self.data.successor, **{field: b"{}\n"}))
                doubles["native"].assert_not_called()

    def test_actual_overlay_schema_rejects_incomplete_unit_overlay(self):
        schema = canon.load_json_bytes(SUCCESSOR_SCHEMA, canonical=False)
        with self.assertRaises(RuntimeProfileError):
            profile_mod.FixedDraft202012Validator(schema).validate(json.loads(self.data.overlay))

    def test_semantic_validator_binding_rejects_swapped_artifact(self):
        with self.data.missing_prerequisite_doubles() as doubles:
            changed = replace(self.data.successor, semantic_validator=semantic.ArtifactMaterial("unit/semantic.py", b"different"))
            with self.assertRaisesRegex(RuntimeProfileError, "semantic validator bytes differ"):
                self.data.validate(changed)
            doubles["native"].assert_not_called()

    def test_actual_native_gate_rejects_implementation_pin_difference(self):
        changed = replace(self.data.successor, implementation_manifest_sha256="0" * 64)
        with self.assertRaisesRegex(RuntimeProfileError, "implementation source pin differs"):
            profile_mod._successor_native_bytes(changed)

    def test_ordered_gate_spies_and_native_failure_prevent_current_composition(self):
        with self.data.missing_prerequisite_doubles() as doubles:
            calls = Mock()
            for name in ("historical", "design", "schema", "native"):
                calls.attach_mock(doubles[name], name)
            doubles["native"].side_effect = RuntimeProfileError("unit native failure")
            with patch.object(profile_mod, "_current_package_rows") as closure:
                with self.assertRaisesRegex(RuntimeProfileError, "unit native failure"):
                    self.data.validate()
                closure.assert_not_called()
            self.assertEqual([call[0] for call in calls.mock_calls], ["historical", "design", "schema", "native"])


class CurrentClosure(unittest.TestCase):
    def setUp(self):
        self.data = UnitParameters()

    def test_real_current_byte_closure_accepts_exact_benign_parameter_material(self):
        self.assertEqual(tuple(self.data.rows()), PACKAGE_NAMES)
        self.assertNotEqual(self.data.current_manifest, self.data.static.runtime_files_manifest.raw)

    def test_current_manifest_expected_digest_rejects_bad_types_values_and_mismatch(self):
        for value in (None, b"0" * 64, "A" * 64, "0" * 63, "0" * 64):
            with self.subTest(value=str(value)):
                with self.assertRaises(RuntimeProfileError):
                    self.data.rows(manifest_sha256=value)

    def test_current_file_missing_extra_changed_nonbyte_reject(self):
        missing = dict(self.data.current_files)
        missing.pop("runtime/application.bin")
        extra = dict(self.data.current_files, **{"runtime/extra.bin": b"extra"})
        changed = dict(self.data.current_files, **{"runtime/application.bin": b"changed"})
        nonbyte = dict(self.data.current_files, **{"runtime/application.bin": bytearray(b"mutable")})
        for label, values in (("missing", missing), ("extra", extra), ("changed", changed), ("nonbyte", nonbyte)):
            with self.subTest(case=label), self.assertRaises(RuntimeProfileError):
                self.data.rows(files=values)

    def test_manifest_duplicate_reorder_case_alias_dot_and_traversal_reject(self):
        rows = self.data.current_manifest.splitlines(keepends=True)
        malformed = {
            "duplicate": b"".join(rows + [rows[-1]]),
            "reordered": b"".join(reversed(rows)),
            "case_alias": (digest(b"x") + "  runtime/A.bin\n" + digest(b"x") + "  runtime/a.bin\n").encode(),
            "dot": (digest(b"x") + "  runtime/./a.bin\n").encode(),
            "traversal": (digest(b"x") + "  runtime/../a.bin\n").encode(),
            "bom": b"\xef\xbb\xbf" + self.data.current_manifest,
            "crlf": self.data.current_manifest.replace(b"\n", b"\r\n"),
            "missing_lf": self.data.current_manifest[:-1],
        }
        for label, raw in malformed.items():
            files = self.data.current_files
            if label in {"case_alias", "dot", "traversal"}:
                files = {line.split(b"  ")[1].decode(): b"x" for line in raw.splitlines()}
            with self.subTest(case=label), self.assertRaises(RuntimeProfileError):
                self.data.rows(manifest_raw=raw, manifest_sha256=digest(raw), files=files)

    def test_snapshot_rejects_bad_paths_aliases_nonbytes_and_custom_mappings(self):
        for key in ("runtime/./a", "./a", "../a", "runtime/../a", "runtime//a", "/a", "runtime/a/", "C:/a", "runtime\\a", "runtime/a.", "runtime/a ", "a" * 256, "", 1):
            with self.subTest(path=str(key)), self.assertRaises(RuntimeProfileError):
                profile_mod._snapshot_current_files({key: b"x"}, "unit")
        for value in ({"runtime/A": b"x", "runtime/a": b"x"}, {"runtime/a": bytearray(b"x")}, UserDict({"runtime/a": b"x"}), [], None):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(RuntimeProfileError):
                profile_mod._snapshot_current_files(value, "unit")

    def test_runtime_resource_count_bound_and_labelled_small_byte_limit(self):
        self.assertEqual(profile_mod._MAX_RUNTIME_FILES, 512)
        self.assertEqual(profile_mod._MAX_RUNTIME_BYTES, 512 * 1024 * 1024)
        self.assertEqual(len(profile_mod._snapshot_current_files({f"unit/{n:03d}": b"x" for n in range(512)}, "unit")), 512)
        with self.assertRaises(RuntimeProfileError):
            profile_mod._snapshot_current_files({f"unit/{n:03d}": b"x" for n in range(513)}, "unit")
        with patch.object(profile_mod, "_MAX_RUNTIME_BYTES", 3):
            self.assertEqual(profile_mod._snapshot_current_files({"unit/a": b"abc"}, "unit")["unit/a"], b"abc")
            with self.assertRaises(RuntimeProfileError):
                profile_mod._snapshot_current_files({"unit/a": b"ab", "unit/b": b"cd"}, "unit")

    def test_manifest_size_bounds_reject_without_large_allocation(self):
        raw = b"x" * (512 * (64 + 2 + 1024 + 1) + 1)
        with self.assertRaisesRegex(RuntimeProfileError, "manifest exceeds its byte bound"):
            self.data.rows(manifest_raw=raw, manifest_sha256=digest(raw))
        with self.assertRaisesRegex(RuntimeProfileError, "package manifest exceeds its byte bound"):
            self.data.rows(package_raw=b"x" * (6 * (64 + 2 + 1024 + 1) + 1))

    def test_package_missing_extra_reordered_duplicate_and_changed_rows_reject(self):
        missing = dict(self.data.package_files)
        missing.pop(PACKAGE_NAMES[-1])
        extra = dict(self.data.package_files, **{"runtime-profile-v0.6.json": b"extra"})
        cases = [(manifest(missing), missing), (manifest(extra), extra)]
        rows = self.data.package_manifest.splitlines(keepends=True)
        cases.extend([(b"".join(reversed(rows)), self.data.package_files), (b"".join(rows[:-1] + [rows[-2]]), self.data.package_files)])
        for name in PACKAGE_NAMES:
            changed = dict(self.data.package_files)
            changed[name] = b"altered row\n"
            cases.append((manifest(changed), changed))
        for index, (raw, files) in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(RuntimeProfileError):
                self.data.rows(package_raw=raw, package_files=files)

    def test_mixed_current_manifest_files_package_historical_and_overlay_reject(self):
        alternative = runtime_files("alternative")
        other_manifest = manifest(alternative)
        for updates in (
            {"manifest_raw": other_manifest, "manifest_sha256": digest(other_manifest), "files": alternative},
            {"manifest_raw": self.data.static.runtime_files_manifest.raw, "manifest_sha256": digest(self.data.static.runtime_files_manifest.raw)},
            {"historical_raw": b"{}\n"}, {"overlay_raw": b"{}\n"},
        ):
            with self.subTest(fields=sorted(updates)), self.assertRaises(RuntimeProfileError):
                self.data.rows(**updates)

    def test_mapping_insertion_order_is_not_manifest_row_order(self):
        self.assertEqual(tuple(self.data.rows(files=dict(reversed(tuple(self.data.current_files.items()))),
                                              package_files=dict(reversed(tuple(self.data.package_files.items()))))), PACKAGE_NAMES)


class SnapshotsAndComposition(unittest.TestCase):
    def setUp(self):
        self.data = UnitParameters()

    def test_missing_current_inputs_and_wrong_material_types_fail_closed(self):
        for name in ("current_runtime_manifest_raw", "expected_current_runtime_manifest_sha256", "current_runtime_files"):
            kwargs = dict(self.data.kwargs)
            kwargs.pop(name)
            with self.subTest(missing=name), self.assertRaises(TypeError):
                profile_mod.SuccessorProfileMaterial(**kwargs)
        for name in ("profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw", "effective_package_manifest_raw", "current_runtime_manifest_raw"):
            with self.subTest(nonbytes=name), self.assertRaises(RuntimeProfileError):
                profile_mod.SuccessorProfileMaterial(**dict(self.data.kwargs, **{name: bytearray(b"x")}))
        with self.data.missing_prerequisite_doubles(), self.assertRaisesRegex(RuntimeProfileError, "successor material is not exact"):
            self.data.validate(successor=self.data.base)

    def test_constructor_snapshots_original_maps_and_nested_import_rows(self):
        nested = {"guard": {"unit.dll": ["symbol", "target"]}}
        material = profile_mod.SuccessorProfileMaterial(**dict(self.data.kwargs, import_resolution=nested))
        original_value = material.current_runtime_files["runtime/application.bin"]
        self.data.current_files["runtime/application.bin"] = b"later caller mutation"
        self.data.package_files.clear()
        nested["guard"]["unit.dll"].append("later")
        self.assertEqual(material.current_runtime_files["runtime/application.bin"], original_value)
        self.assertEqual(len(material.effective_package_files), 6)
        self.assertEqual(material.import_resolution["guard"]["unit.dll"], ("symbol", "target"))
        with self.assertRaises(TypeError):
            material.current_runtime_files["runtime/application.bin"] = b"cannot change"
        with self.assertRaises(FrozenInstanceError):
            material.current_runtime_manifest_raw = b"cannot rebind"

    def test_caller_mutation_before_snapshot_is_not_validated_as_old_bytes(self):
        self.data.current_files["runtime/application.bin"] = b"changed before constructor"
        changed = profile_mod.SuccessorProfileMaterial(**self.data.kwargs)
        with self.data.missing_prerequisite_doubles(), self.assertRaisesRegex(RuntimeProfileError, "target bytes differ"):
            self.data.validate(changed)

    def test_effective_raw_object_digest_and_historical_identity_are_distinct(self):
        with self.data.missing_prerequisite_doubles():
            result = self.data.validate()
        self.assertIs(type(result), profile_mod.ValidatedSuccessorProfileCandidate)
        self.assertEqual(result.profile_raw, canon.canonical_json_bytes(profile_mod._json_value(result.profile)))
        self.assertEqual(result.profile_sha256, digest(result.profile_raw))
        self.assertEqual(result.historical_profile_raw, HISTORICAL_RAW)
        self.assertEqual(result.historical_profile_sha256, digest(HISTORICAL_RAW))
        self.assertNotEqual(result.profile_sha256, result.historical_profile_sha256)
        self.assertTrue(result.candidate_only)
        self.assertEqual(result.static_relations, BYTE_RELATIONS)
        self.assertEqual(result.deferred_static_relations, DEFERRED_RELATIONS)
        self.assertEqual(result.static_relations_scope, "historical-profile-v0.4")
        self.assertNotIn("semantic_relations", result.profile)
        self.assertEqual(result.profile["historical_semantic_relations"], tuple(json.loads(HISTORICAL_RAW)["semantic_relations"]))

    def test_effective_profile_binds_current_package_manifest_overlay_and_prior_closure(self):
        with self.data.missing_prerequisite_doubles():
            result = self.data.validate()
        closure = result.profile["package_closure"]
        self.assertEqual(closure["row_count"], 6)
        self.assertEqual(closure["effective_rows"], PACKAGE_NAMES)
        self.assertEqual(closure["runtime_files_manifest"]["sha256"], digest(self.data.current_manifest))
        self.assertEqual(closure["effective_package_manifest_sha256"], digest(self.data.package_manifest))
        self.assertEqual(result.profile["successor_overlay_sha256"], digest(self.data.overlay))
        self.assertEqual(result.profile["historical_package_closure"]["row_count"], 5)
        self.assertNotEqual(closure["runtime_files_manifest"]["sha256"], result.profile["historical_package_closure"]["runtime_files_manifest"]["sha256"])

    def test_validated_data_rejects_object_raw_hash_inconsistency_and_relation_promotion(self):
        changed = json.loads(HISTORICAL_RAW)
        changed["revision"] = "changed"
        for updates in ({"profile": changed}, {"profile_sha256": "0" * 64}, {"profile_raw": bytearray(HISTORICAL_RAW)},
                        {"candidate_only": False}, {"static_relations": BYTE_RELATIONS + DEFERRED_RELATIONS},
                        {"deferred_static_relations": ()}, {"static_relations_scope": "all-current-native"}):
            with self.subTest(fields=sorted(updates)), self.assertRaises(RuntimeProfileError):
                replace(self.data.base, **updates)

    def test_successor_result_rejects_coherent_but_unbound_effective_profile(self):
        with self.data.missing_prerequisite_doubles():
            result = self.data.validate()
            changed = profile_mod._json_value(result.profile)
            changed["package_closure"]["effective_package_manifest_sha256"] = "0" * 64
            changed_raw = canon.canonical_json_bytes(changed)
            with self.assertRaisesRegex(RuntimeProfileError, "not bound to its current and historical material"):
                replace(result, profile=changed, profile_raw=changed_raw, profile_sha256=digest(changed_raw))
            with self.assertRaisesRegex(RuntimeProfileError, "not bound to its current and historical material"):
                replace(result, profile=json.loads(HISTORICAL_RAW), profile_raw=HISTORICAL_RAW, profile_sha256=digest(HISTORICAL_RAW))

    def test_successor_result_rejects_mutated_digest_and_file_bindings(self):
        with self.data.missing_prerequisite_doubles():
            result = self.data.validate()
            for updates in ({"historical_profile_sha256": "0" * 64}, {"effective_package_manifest_sha256": "0" * 64},
                            {"current_runtime_manifest_sha256": "0" * 64}, {"successor_overlay_raw": b"{}\n"},
                            {"current_runtime_files": {"runtime/unit": b"other"}}):
                with self.subTest(fields=sorted(updates)), self.assertRaises(RuntimeProfileError):
                    replace(result, **updates)

    def test_returned_snapshots_are_recursively_immutable_after_caller_mutation(self):
        with self.data.missing_prerequisite_doubles():
            result = self.data.validate()
        current_snapshot = dict(result.current_runtime_files)
        self.data.current_files.clear()
        self.data.package_files.clear()
        self.assertEqual(dict(result.current_runtime_files), current_snapshot)
        self.assertEqual(len(result.effective_package_files), 6)
        with self.assertRaises(TypeError):
            result.profile["package_closure"]["runtime_files_manifest"]["sha256"] = "0" * 64
        with self.assertRaises(TypeError):
            result.effective_package_files[PACKAGE_NAMES[0]] = b"mutated"
        with self.assertRaises(FrozenInstanceError):
            result.profile_sha256 = "0" * 64


class PreloaderDataFlow(unittest.TestCase):
    def setUp(self):
        self.data = UnitParameters()
        locators = tuple(f"0x{n:016x}" for n in range(1, 6))
        self.inputs = loader.OfflinePreloaderInputs(
            "1" * 64, "2" * 64, "C:\\unit\\workspace",
            loader.OrderedHandleLocators(*locators), locators, "a" * 32, "a" * 32,
        )

    def prepare(self):
        return loader.NeutralPreloader().prepare(
            profile_raw=HISTORICAL_RAW, schema_raw=HISTORICAL_SCHEMA,
            static_material=self.data.static, successor=self.data.successor, inputs=self.inputs,
        )

    def test_consumers_take_current_control_artifacts_package_and_historical_p4_identity(self):
        # Only upstream prerequisites are doubled; every consumer below validation is real.
        real_validate = profile_mod.validate_successor_profile_candidate
        captured = {}

        def snapshot_then_mutate_callers(**kwargs):
            result = real_validate(**kwargs)
            captured["validated"] = result
            self.data.current_files.clear()
            self.data.package_files.clear()
            return result

        original_files = dict(self.data.current_files)
        with self.data.missing_prerequisite_doubles():
            with patch.object(loader, "validate_successor_profile_candidate", side_effect=snapshot_then_mutate_callers) as validation:
                prepared = self.prepare()
                validation.assert_called_once()
        result = captured["validated"]
        values = evidence_mod.parse_launch_evidence_v2(prepared.evidence.raw)
        self.assertEqual(prepared.application_path, "C:\\unit\\current.exe")
        self.assertEqual(prepared.command_line, "current unit-argument")
        self.assertEqual(prepared.environment_block, ("UNIT_KIND=current",))
        self.assertEqual(values["launch_control_sha256"], digest(original_files["runtime/launch-inputs.json"]))
        for field, path in (("preloader_image_sha256", "runtime/preloader.bin"),
                            ("application_sha256", "runtime/application.bin"),
                            ("bootstrap_sha256", "runtime/bootstrap.py"), ("verifier_sha256", "runtime/verifier.py")):
            self.assertEqual(values[field], digest(original_files[path]))
            self.assertNotEqual(values[field], digest(self.data.static.runtime_files[path]))
        self.assertEqual(values["runtime_package_sha256"], digest(result.effective_package_manifest_raw))
        self.assertEqual(values["runtime_profile_v0_4_sha256"], digest(HISTORICAL_RAW))
        self.assertEqual(prepared.runtime_profile_sha256, result.profile_sha256)
        self.assertNotEqual(prepared.runtime_profile_sha256, values["runtime_profile_v0_4_sha256"])
        self.assertEqual(prepared.historical_runtime_profile_v0_4_sha256, digest(HISTORICAL_RAW))
        self.assertTrue(prepared.candidate_only)
        self.assertFalse(prepared.native_api_reachable)
        self.assertEqual(prepared.static_relations_scope, "historical-profile-v0.4")
        self.assertEqual(prepared.deferred_static_relations, DEFERRED_RELATIONS)

    def test_admission_uses_historical_p4_digest_and_current_package(self):
        with self.data.missing_prerequisite_doubles() as doubles:
            prepared = self.prepare()
            observed = semantic.PostcreationObservation(prepared.evidence.sha256, 123, 123, "createprocess-success-bound-v0.4")
            diagnostic = loader.prepare_offline_admission_diagnostic(
                profile_raw=HISTORICAL_RAW, schema_raw=HISTORICAL_SCHEMA, static_material=self.data.static,
                successor=self.data.successor, inputs=self.inputs, observation=observed,
            )
            self.assertEqual(doubles["historical"].call_count, 2)
        value = json.loads(diagnostic.raw)
        self.assertEqual(value["runtime_profile_v0_4_sha256"], digest(HISTORICAL_RAW))
        self.assertEqual(value["effective_runtime_package_sha256"], digest(self.data.package_manifest))
        self.assertNotEqual(value["runtime_profile_v0_4_sha256"], prepared.runtime_profile_sha256)
        self.assertTrue(value["candidate_only"])
        self.assertFalse(value["rehearsal_pass"])

    def test_preloader_revalidates_each_call_and_rejects_current_file_tamper(self):
        with self.data.missing_prerequisite_doubles() as doubles:
            self.prepare()
            self.prepare()
            self.assertEqual(doubles["historical"].call_count, 2)
            altered = dict(self.data.successor.current_runtime_files)
            altered["runtime/application.bin"] = b"altered after earlier prepare"
            self.data.successor = replace(self.data.successor, current_runtime_files=altered)
            with self.assertRaisesRegex(RuntimeProfileError, "target bytes differ"):
                self.prepare()
            self.assertEqual(doubles["historical"].call_count, 3)

    def test_missing_current_control_or_artifact_never_falls_back_to_history(self):
        for missing in ("runtime/launch-inputs.json", "runtime/application.bin"):
            self.data = UnitParameters()
            files = dict(self.data.current_files)
            files.pop(missing)
            raw = manifest(files)
            packages = dict(self.data.package_files)
            packages[PACKAGE_NAMES[0]] = raw
            self.data.successor = replace(self.data.successor, current_runtime_files=files,
                                          current_runtime_manifest_raw=raw, expected_current_runtime_manifest_sha256=digest(raw),
                                          effective_package_files=packages, effective_package_manifest_raw=manifest(packages))
            with self.subTest(missing=missing), self.data.missing_prerequisite_doubles():
                with self.assertRaisesRegex(RuntimeProfileError, "outside authenticated runtime files"):
                    self.prepare()



class RealSourceClosure(unittest.TestCase):
    """Real checker over source bytes; no missing-prerequisite doubles apply."""

    def rejected(self, label, sources, expected):
        try:
            audit_mod.inspect_source_structure(sources)
        except RuntimeProfileError as exc:
            SOURCE_OBSERVATIONS.append({
                "case": label, "status": "REJECT", "error": str(exc),
                "real_checker": True, "source_inventory": sorted(sources),
            })
            self.assertIn(expected, str(exc))
        else:
            self.fail("real checker unexpectedly admitted " + label)

    def appended_profile(self, raw):
        return {**SOURCE_BYTES, "profile.py": SOURCE_BYTES["profile.py"] + b"\n" + raw}

    def test_real_exact_ten_candidate_files_pass(self):
        self.assertEqual(tuple(sorted(SOURCE_BYTES)), audit_mod.EXPECTED_FILES)
        observed = audit_mod.inspect_source_structure(dict(SOURCE_BYTES))
        self.assertEqual(observed, audit_mod.EXPECTED_FILES)
        SOURCE_OBSERVATIONS.append({
            "case": "exact_ten_v03_candidate_files", "status": "PASS",
            "real_checker": True, "source_sha256": {name: digest(raw) for name, raw in SOURCE_BYTES.items()},
        })

    def test_exact_four_set_delta_preserves_all_other_source_bytes(self):
        old = PREVIOUS_SOURCE_BYTES["source_audit.py"]
        changes = (
            (b'"profile.py": {"copy"},', b'"profile.py": set(),'),
            (b'"profile.py": {"copy.deepcopy"},', b'"profile.py": set(),'),
            (b'"dataclasses": {"dataclass"},', b'"dataclasses": {"dataclass", "replace"},'),
            (b'"profile": {"ValidatedProfileCandidate", "validate_runtime_profile_candidate", "SuccessorProfileMaterial", "validate_successor_profile_candidate"},',
             b'"profile": {"ValidatedProfileCandidate", "ValidatedSuccessorProfileCandidate", "validate_runtime_profile_candidate", "SuccessorProfileMaterial", "validate_successor_profile_candidate"},'),
        )
        for prior, current in changes:
            self.assertEqual(old.count(prior), 1)
            old = old.replace(prior, current, 1)
        self.assertEqual(old, SOURCE_BYTES["source_audit.py"])
        for name in MODULE_PINS:
            if name != "source_audit.py":
                with self.subTest(unchanged_module=name):
                    self.assertEqual(PREDECESSOR_SOURCE_BYTES[name] if name == "profile.py" else SOURCE_BYTES[name],
                                     PREVIOUS_SOURCE_BYTES[name])
                    # The current profile method delta is checked exactly by the v0.3 cases.
        self.assertEqual(audit_mod._ALLOWED_ABSOLUTE_FROM["dataclasses"], {"dataclass", "replace"})
        self.assertEqual(audit_mod._ALLOWED_RELATIVE_FROM["profile"], {
            "ValidatedProfileCandidate", "ValidatedSuccessorProfileCandidate",
            "validate_runtime_profile_candidate", "SuccessorProfileMaterial", "validate_successor_profile_candidate",
        })
        self.assertEqual(audit_mod._ALLOWED_DIRECT_MODULES["profile.py"], set())
        self.assertEqual(audit_mod._ALLOWED_MODULE_ATTRIBUTES["profile.py"], set())

    def test_checker_functions_other_constants_and_native_inventory_unchanged(self):
        def unchanged_nodes(raw):
            changed = {"_ALLOWED_DIRECT_MODULES", "_ALLOWED_MODULE_ATTRIBUTES",
                       "_ALLOWED_ABSOLUTE_FROM", "_ALLOWED_RELATIVE_FROM"}
            tree = ast.parse(raw)
            return [
                ast.dump(node, include_attributes=False) for node in tree.body
                if not (isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id in changed for target in node.targets))
            ]
        self.assertEqual(unchanged_nodes(PREVIOUS_SOURCE_BYTES["source_audit.py"]),
                         unchanged_nodes(SOURCE_BYTES["source_audit.py"]))

    def test_dataclasses_field_and_asdict_remain_rejected(self):
        for symbol in (b"field", b"asdict"):
            with self.subTest(symbol=symbol.decode()):
                self.rejected("dataclasses." + symbol.decode(),
                              self.appended_profile(b"from dataclasses import " + symbol + b"\n"),
                              "candidate from-import is outside positive closure")

    def test_nonadmitted_local_profile_symbol_remains_rejected(self):
        sources = {**SOURCE_BYTES, "preloader.py": SOURCE_BYTES["preloader.py"] +
                   b"\nfrom .profile import _PREDECESSOR_PROFILE_PINS\n"}
        self.rejected("nonadmitted_local_profile_symbol", sources,
                      "candidate from-import is outside positive closure")

    def test_copy_import_and_imported_deepcopy_use_rejected(self):
        for label, raw in (
            ("copy_import", b"import copy\n"),
            ("copy_import_with_deepcopy_use", b"import copy\ncopy.deepcopy({})\n"),
            ("from_copy_import_deepcopy", b"from copy import deepcopy\n"),
        ):
            with self.subTest(case=label):
                self.rejected(label, self.appended_profile(raw), "outside positive closure")

    def test_wildcard_alias_and_nontoplevel_imports_remain_rejected(self):
        for label, raw, expected in (
            ("wildcard", b"from dataclasses import *\n", "wildcard or alias import"),
            ("alias", b"from dataclasses import replace as alternate\n", "wildcard or alias import"),
            ("nontoplevel", b"def unit_local_import():\n    from dataclasses import replace\n", "non-top-level import"),
            ("other_absolute_module", b"from collections import Counter\n", "outside positive closure"),
        ):
            with self.subTest(case=label):
                self.rejected(label, self.appended_profile(raw), expected)

    def test_missing_extra_and_wrong_mapping_inventory_rejected(self):
        missing = dict(SOURCE_BYTES)
        missing.pop("errors.py")
        extra = {**SOURCE_BYTES, "extra.py": b"pass\n"}
        for label, sources in (("missing_file", missing), ("extra_file", extra),
                               ("mapping_substitute", UserDict(SOURCE_BYTES))):
            with self.subTest(case=label):
                self.rejected(label, sources, "candidate source inventory is not exact")

    def test_nonbyte_source_input_rejected(self):
        self.rejected("nonbyte_source", {**SOURCE_BYTES, "profile.py": bytearray(SOURCE_BYTES["profile.py"])},
                      "candidate source mapping is not exact bytes")

    def test_original_36_cases_retained_with_explicit_preservation_adaptation(self):
        def methods(raw):
            return {
                cls.name + "." + node.name: ast.dump(node, include_attributes=False)
                for cls in ast.parse(raw).body if isinstance(cls, ast.ClassDef)
                for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
            }
        prior = methods((PREVIOUS / "tests/test_profile_composition.py").read_bytes())
        current = methods(Path(__file__).read_bytes())
        self.assertEqual(len(prior), 36)
        renamed = "PreservationAndGates.test_original_semantic_evidence_integration_and_source_audit_are_byte_identical"
        replacement = "PreservationAndGates.test_original_semantic_evidence_integration_canonical_and_schema_are_byte_identical"
        for name, body in prior.items():
            with self.subTest(previous_test=name):
                if name == renamed:
                    self.assertIn(replacement, current)
                else:
                    self.assertEqual(body, current[name])
        self.assertEqual(len(set(current) - {name for name in current if name.startswith("RealSourceClosure.")}), 36)

    def test_previous_rejection_evidence_retains_original_byte_identity(self):
        prior = json.loads((PREVIOUS / "diagnostics/source-closure-results.json").read_bytes())
        self.assertEqual(prior["diagnostic"], "a05-profile-composition-v0.1-source-closure")
        self.assertEqual([row["status"] for row in prior["matrix"]], ["pass", "reject", "reject", "reject"])
        self.assertEqual(prior["matrix"][1]["source_hashes"], PREVIOUS_PINS)
        self.assertTrue(prior["all_pinned_inputs_unchanged"])
        for row in prior["matrix"][1:]:
            self.assertEqual(row["error"], "candidate from-import is outside positive closure at #")
        SOURCE_OBSERVATIONS.append({
            "case": "prior_v01_diagnostic_evidence", "status": "HISTORICAL_REJECTION_PRESERVED",
            "evidence_sha256": PINS[PREVIOUS / "diagnostics/source-closure-results.json"],
            "not_a_current_candidate_failure": True,
        })



    def test_constructor_field_tuples_are_complete_ordered_and_getattr_free(self):
        cls = next(node for node in ast.parse(SOURCE_BYTES["profile.py"]).body
                   if isinstance(node, ast.ClassDef) and node.name == "SuccessorProfileMaterial")
        method = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "__post_init__")
        loops = [node for node in method.body if isinstance(node, ast.For)]
        expected_groups = (
            ("profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw",
             "effective_package_manifest_raw", "current_runtime_manifest_raw"),
            ("current_runtime_files", "effective_package_files"),
            ("design_files", "implementation_files", "native_sources", "native_binaries", "import_resolution", "crt_imports"),
        )
        self.assertEqual(len(loops), 3)
        observed = []
        for loop, expected in zip(loops, expected_groups, strict=True):
            self.assertIsInstance(loop.target, ast.Tuple)
            self.assertEqual([item.id for item in loop.target.elts], ["name", "value"])
            self.assertIsInstance(loop.iter, ast.Tuple)
            names = []
            for item in loop.iter.elts:
                self.assertIsInstance(item, ast.Tuple)
                self.assertEqual(len(item.elts), 2)
                label, value = item.elts
                self.assertIsInstance(label, ast.Constant)
                self.assertIsInstance(value, ast.Attribute)
                self.assertIsInstance(value.value, ast.Name)
                self.assertEqual(value.value.id, "self")
                self.assertEqual(value.attr, label.value)
                names.append(label.value)
            self.assertEqual(tuple(names), expected)
            observed.extend(names)
        self.assertEqual(len(observed), 14)
        self.assertEqual(len(set(observed)), 14)
        self.assertFalse(any(isinstance(node, ast.Name) and node.id == "getattr" for node in ast.walk(method)))

    def test_only_constructor_read_rewrite_preserves_exact_other_bytes(self):
        expected = PREDECESSOR_SOURCE_BYTES["profile.py"]
        replacements = (
            (
                b'        for name in (\n            "profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw",\n            "effective_package_manifest_raw", "current_runtime_manifest_raw",\n        ):\n            if type(getattr(self, name)) is not bytes:\n',
                b'        for name, value in (\n            ("profile_raw", self.profile_raw),\n            ("schema_raw", self.schema_raw),\n            ("interface_map_raw", self.interface_map_raw),\n            ("implementation_manifest_raw", self.implementation_manifest_raw),\n            ("effective_package_manifest_raw", self.effective_package_manifest_raw),\n            ("current_runtime_manifest_raw", self.current_runtime_manifest_raw),\n        ):\n            if type(value) is not bytes:\n',
            ),
            (
                b'        for name in ("current_runtime_files", "effective_package_files"):\n            object.__setattr__(self, name, _snapshot_current_files(getattr(self, name), name))\n',
                b'        for name, value in (\n            ("current_runtime_files", self.current_runtime_files),\n            ("effective_package_files", self.effective_package_files),\n        ):\n            object.__setattr__(self, name, _snapshot_current_files(value, name))\n',
            ),
            (
                b'        for name in (\n            "design_files", "implementation_files", "native_sources", "native_binaries",\n            "import_resolution", "crt_imports",\n        ):\n            value = getattr(self, name)\n',
                b'        for name, value in (\n            ("design_files", self.design_files),\n            ("implementation_files", self.implementation_files),\n            ("native_sources", self.native_sources),\n            ("native_binaries", self.native_binaries),\n            ("import_resolution", self.import_resolution),\n            ("crt_imports", self.crt_imports),\n        ):\n',
            ),
        )
        for before, after in replacements:
            self.assertEqual(expected.count(before), 1)
            expected = expected.replace(before, after, 1)
        self.assertEqual(expected, SOURCE_BYTES["profile.py"])
        for name in MODULE_PINS:
            if name != "profile.py":
                with self.subTest(unchanged_module=name):
                    self.assertEqual(SOURCE_BYTES[name], PREDECESSOR_SOURCE_BYTES[name])
        def outside_constructor(raw):
            tree = ast.parse(raw)
            for cls in tree.body:
                if isinstance(cls, ast.ClassDef) and cls.name == "SuccessorProfileMaterial":
                    cls.body = [node for node in cls.body
                                if not (isinstance(node, ast.FunctionDef) and node.name == "__post_init__")]
            return ast.dump(tree, include_attributes=False)
        self.assertEqual(outside_constructor(PREDECESSOR_SOURCE_BYTES["profile.py"]),
                         outside_constructor(SOURCE_BYTES["profile.py"]))

    def test_each_of_six_raw_fields_rejects_nonexact_bytes(self):
        class BytesSubclass(bytes):
            pass
        data = UnitParameters()
        for name in ("profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw",
                     "effective_package_manifest_raw", "current_runtime_manifest_raw"):
            for bad in (None, bytearray(b"unit"), BytesSubclass(b"unit")):
                with self.subTest(field=name, value_type=type(bad).__name__):
                    with self.assertRaisesRegex(RuntimeProfileError, "successor " + name + " is not exact bytes"):
                        profile_mod.SuccessorProfileMaterial(**dict(data.kwargs, **{name: bad}))

    def test_each_of_eight_map_fields_rejects_nonexact_dictionary_types(self):
        data = UnitParameters()
        names = ("current_runtime_files", "effective_package_files", "design_files", "implementation_files",
                 "native_sources", "native_binaries", "import_resolution", "crt_imports")
        for name in names:
            for bad in (None, [], UserDict({"unit/value": b"unit"})):
                with self.subTest(field=name, value_type=type(bad).__name__):
                    with self.assertRaisesRegex(RuntimeProfileError, name + " is not"):
                        profile_mod.SuccessorProfileMaterial(**dict(data.kwargs, **{name: bad}))

    def test_raw_digest_and_map_failure_order_is_preserved(self):
        data = UnitParameters()
        raw_names = ("profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw",
                     "effective_package_manifest_raw", "current_runtime_manifest_raw")
        map_names = ("current_runtime_files", "effective_package_files", "design_files", "implementation_files",
                     "native_sources", "native_binaries", "import_resolution", "crt_imports")
        for index, name in enumerate(raw_names):
            bad = {field: None for field in raw_names[index:] + map_names}
            bad["expected_current_runtime_manifest_sha256"] = "bad"
            with self.subTest(first_raw_failure=name):
                with self.assertRaisesRegex(RuntimeProfileError, "successor " + name + " is not exact bytes"):
                    profile_mod.SuccessorProfileMaterial(**dict(data.kwargs, **bad))
        bad = {name: None for name in map_names}
        bad["expected_current_runtime_manifest_sha256"] = "bad"
        with self.assertRaisesRegex(RuntimeProfileError, "CONTROL-expected current runtime manifest digest"):
            profile_mod.SuccessorProfileMaterial(**dict(data.kwargs, **bad))
        for index, name in enumerate(map_names):
            bad = {field: None for field in map_names[index:]}
            with self.subTest(first_map_failure=name):
                with self.assertRaisesRegex(RuntimeProfileError, name + " is not"):
                    profile_mod.SuccessorProfileMaterial(**dict(data.kwargs, **bad))

    def test_distinct_values_snapshot_all_fourteen_fields_and_nested_collections(self):
        data = UnitParameters()
        raw_names = ("profile_raw", "schema_raw", "interface_map_raw", "implementation_manifest_raw",
                     "effective_package_manifest_raw", "current_runtime_manifest_raw")
        raws = {name: ("unit " + name).encode() for name in raw_names}
        source_artifact = semantic.ArtifactMaterial("unit/source.cpp", b"source distinct data")
        binary_artifact = semantic.ArtifactMaterial("unit/native.bin", b"binary distinct data")
        nested_resolution = ["unit.dll", "UnitSymbol"]
        nested_crt = [["crt-unit.dll", "CrtUnitSymbol"]]
        mutable_maps = {
            "current_runtime_files": {"unit/current": b"current distinct data"},
            "effective_package_files": {"unit/package": b"package distinct data"},
            "design_files": {"unit/design.json": b"design distinct data"},
            "implementation_files": {"unit/implementation.py": b"implementation distinct data"},
            "native_sources": {"guard": source_artifact},
            "native_binaries": {"guard": binary_artifact},
            "import_resolution": {"guard": {"UnitCall": nested_resolution}},
            "crt_imports": {"guard": nested_crt},
        }
        expected = {
            **{name: dict(value) for name, value in mutable_maps.items()
               if name not in {"import_resolution", "crt_imports"}},
            "import_resolution": {"guard": {"UnitCall": ("unit.dll", "UnitSymbol")}},
            "crt_imports": {"guard": (("crt-unit.dll", "CrtUnitSymbol"),)},
        }
        # These are constructor parameters, not coherent historical/native material.
        kwargs = dict(data.kwargs, **raws, **{name: MappingProxyType(value) for name, value in mutable_maps.items()})
        material = profile_mod.SuccessorProfileMaterial(**kwargs)
        for name, raw in raws.items():
            self.assertIs(getattr(material, name), raw)
        for name, value in expected.items():
            self.assertEqual(getattr(material, name), value)
            with self.assertRaises(TypeError):
                getattr(material, name)["mutation"] = b"no"
        nested_resolution.append("later")
        nested_crt[0].append("later")
        for value in mutable_maps.values():
            value.clear()
        for name, value in expected.items():
            self.assertEqual(getattr(material, name), value)
        with self.assertRaises(TypeError):
            material.import_resolution["guard"]["UnitCall"] = ("changed",)
        with self.assertRaises(FrozenInstanceError):
            material.design_files = {}

    def test_getattr_reintroduced_at_each_original_read_site_is_rejected(self):
        mutations = (
            ("bytes_read_site", b"            if type(value) is not bytes:\n",
             b"            if type(getattr(self, name)) is not bytes:\n"),
            ("current_map_read_site", b"            object.__setattr__(self, name, _snapshot_current_files(value, name))\n",
             b"            object.__setattr__(self, name, _snapshot_current_files(getattr(self, name), name))\n"),
            ("other_map_read_site", b"            if type(value) not in {dict, _MAPPING_PROXY_TYPE}:\n",
             b"            value = getattr(self, name)\n            if type(value) not in {dict, _MAPPING_PROXY_TYPE}:\n"),
        )
        for label, before, after in mutations:
            with self.subTest(site=label):
                self.assertEqual(SOURCE_BYTES["profile.py"].count(before), 1)
                sources = {**SOURCE_BYTES, "profile.py": SOURCE_BYTES["profile.py"].replace(before, after, 1)}
                self.rejected("reintroduced_getattr_" + label, sources,
                              "candidate source uses dynamic or ambient authority")

    def test_previous_v02_full_inventory_rejected_by_unchanged_real_checker(self):
        self.assertEqual(SOURCE_BYTES["source_audit.py"], PREDECESSOR_SOURCE_BYTES["source_audit.py"])
        self.rejected("exact_ten_v02_sources_under_identical_checker", dict(PREDECESSOR_SOURCE_BYTES),
                      "candidate source uses dynamic or ambient authority")
        previous_result = json.loads((PREDECESSOR / "verification/test-results.json").read_bytes())
        self.assertEqual(previous_result["tests_run"], 47)
        self.assertEqual(previous_result["errors"], 1)
        self.assertFalse(previous_result["passed"])

    def test_previous_47_cases_retained_with_one_explicit_profile_preservation_adjustment(self):
        def methods(raw):
            return {
                cls.name + "." + node.name: ast.dump(node, include_attributes=False)
                for cls in ast.parse(raw).body if isinstance(cls, ast.ClassDef)
                for node in cls.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
            }
        prior = methods((PREDECESSOR / "tests/test_profile_composition.py").read_bytes())
        current = methods(Path(__file__).read_bytes())
        self.assertEqual(len(prior), 47)
        changed = "RealSourceClosure.test_exact_four_set_delta_preserves_all_other_source_bytes"
        for name, body in prior.items():
            with self.subTest(previous_test=name):
                if name == changed:
                    self.assertIn(name, current)
                elif name == "RealSourceClosure.test_real_exact_ten_candidate_files_pass":
                    self.assertEqual(body.replace("exact_ten_v02_candidate_files", "exact_ten_v03_candidate_files"), current[name])
                else:
                    self.assertEqual(body, current[name])
        self.assertEqual(len(current), 56)


class DeterministicResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"test": test.id(), "status": "FAIL", "detail": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"test": test.id(), "status": "ERROR", "detail": self._exc_info_to_string(err, test)})

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.records.append({"test": subtest.id(), "status": "FAIL_SUBTEST", "detail": self._exc_info_to_string(err, test)})


def check_output_location(path):
    # Maintenance observation, not an attacker-resistant retained-handle policy.
    if path not in {CANDIDATE / "verification/test-results.json", CANDIDATE / "verification/test-stdout.txt"}:
        raise RuntimeError("test output is not exactly allowlisted")
    for component in (path, *path.parents):
        if component.exists() and (component.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise RuntimeError("test output ancestry contains a reparse point")
    if not path.resolve().is_relative_to(CANDIDATE.resolve()):
        raise RuntimeError("test output resolved outside candidate root")


def main():
    for name in ("test-results.json", "test-stdout.txt"):
        if (CANDIDATE / "verification" / name).exists():
            raise RuntimeError("verification output already exists; refusing overwrite")
    result = DeterministicResult()
    unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]).run(result)
    post_hashes = authenticate()
    if post_hashes != PRE_HASHES or digest(Path(__file__).read_bytes()) != SELF_HASH:
        raise RuntimeError("pre/post source/input/test authentication differs")
    repo_modules = {}
    for name, module in sorted(sys.modules.items()):
        filename = getattr(module, "__file__", None)
        if filename and Path(filename).is_relative_to(ROOT):
            path = Path(filename)
            if path != Path(__file__) and path not in {SOURCE / key for key in MODULE_PINS}:
                raise RuntimeError("unexpected repository module imported")
            repo_modules[name] = str(path.relative_to(ROOT))
    records = sorted(result.records, key=lambda row: row["test"])
    stdout = "\n".join(row["status"] + " " + row["test"] for row in records)
    stdout += f"\nTests run: {result.testsRun}; failures: {len(result.failures)}; errors: {len(result.errors)}\n"
    stdout += "Scope: bounded data-flow units with explicitly mocked upstream prerequisites plus real exact-source closure checks; no complete historical/native/assembly/S0 pass.\n"
    stdout += "Real source closure: " + json.dumps(SOURCE_OBSERVATIONS, sort_keys=True) + "\n"
    for row in records:
        if "detail" in row:
            stdout += "\n" + row["detail"]
    report = {
        "candidate": "a05-profile-composition-v0.3", "role": "TEST/VERIFICATION",
        "branch_authenticated_before_run": "codex/windows-build-toolchain-environment-v0.1",
        "head_authenticated_before_run": "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a",
        "tree_authenticated_before_run": "82c02f37fd13ecfc8c7b888bb66127989b6d4f34",
        "command": REPRODUCIBLE_COMMAND, "python_version": "3.12.10",
        "test_source_sha256": SELF_HASH, "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "passed": result.wasSuccessful(),
        "records": records, "mocked_prerequisites": MOCKS, "unverified_and_nonclaims": UNVERIFIED,
        "original_bounded_cases_retained": 36, "previous_v02_cases_retained": 47,
        "new_v03_cases": 9, "source_closure_and_constructor_cases": 20,
        "source_closure_observations": SOURCE_OBSERVATIONS,
        "source_closure_uses_doubles": False,
        "previous_frozen_manifest_entries_unchanged": 17,
        "pre_input_sha256": PRE_HASHES, "post_input_sha256": post_hashes,
        "repository_modules_imported": repo_modules, "test_stdout_sha256": digest(stdout.encode("utf-8")),
        "artifact_location_check": "exact allowed output paths with observed non-reparse ancestry; not hostile-filesystem isolation",
        "independent_review_verdict": "not produced by TEST role",
    }
    outputs = {
        CANDIDATE / "verification/test-results.json": (json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode(),
        CANDIDATE / "verification/test-stdout.txt": stdout.encode("utf-8"),
    }
    for path in outputs:
        check_output_location(path)
    (CANDIDATE / "verification").mkdir(exist_ok=True)
    for path, raw in outputs.items():
        check_output_location(path)
        with path.open("xb") as output:
            output.write(raw)
        if path.read_bytes() != raw:
            raise RuntimeError("test output readback differs")
    print(stdout, end="")
    for path, raw in outputs.items():
        print(str(path.relative_to(CANDIDATE)) + " SHA256 " + digest(raw))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
