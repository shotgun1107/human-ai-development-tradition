from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib
import json
import os
from pathlib import Path
import secrets
import ssl
import sys
import tempfile
from typing import Any
import urllib.error
import urllib.request


SCHEMA_ID = "S0-EXTERNAL-ARTIFACT-AUTHORITY-ACQUISITION-V0.1-LIVE-EVIDENCE-1"
CHUNK_SIZE = 64 * 1024
REQUEST_TIMEOUT_SECONDS = 30
MAX_REDIRECTS = 3

CANDIDATE_PINS = {
    "implementation/s0_external_artifact_authority_acquisition/__init__.py": "d96b293c7e93f319fb90547251b4c8044fb7c2f131061a7ab7c09befcfd28ced",
    "implementation/s0_external_artifact_authority_acquisition/_issuance.py": "a93f9bb961715d61ca9c6545e30b3126b017e8edbf60246ab7a7c206ce7dcf32",
    "implementation/s0_external_artifact_authority_acquisition/buildtools.py": "4cd204b2b032929dfb9a7a524bfdee3f077d2aaa337768c00bcbad1b2d513fef",
    "implementation/s0_external_artifact_authority_acquisition/candidate.py": "380471c778a43fded2037260bb5186e5df94a3a54e3f2b2a9551b165371e617d",
    "implementation/s0_external_artifact_authority_acquisition/canonical.py": "bc783bffc11a6394748468729066b1866f68eacfd19bbb0590363e0058b55fea",
    "implementation/s0_external_artifact_authority_acquisition/errors.py": "3792fd5467e39b18dcc58bb063e6075c422c8f6b2d7d061c1c537cd6ea6c1221",
    "implementation/s0_external_artifact_authority_acquisition/metadata.py": "d9c5276da4169d880f9388c515ce1f2bdd62670b1d7f6edce5973b000eb04221",
    "implementation/s0_external_artifact_authority_acquisition/pins.py": "63b205b3643b93f136bcc62a3b5e057baa8a3a4137b4c7810df86cde3b66e55d",
    "implementation/s0_external_artifact_authority_acquisition/wheel.py": "c17676c51e17d5f369263bca0991d9ab5336fa7062a6ae599aedb6aa6ef4fc37",
    "tests/test_authority_acquisition.py": "edfaff91f13d1fc90fa2f0cd4bfcc64cd2a827b08e7e6e6cb08a8c871ef571c6",
    "tests/test_entrypoint_isolation.py": "115f29570babc687b151d966207e6ac7dd7777ce714bb763a1881646fcb47cb2",
    "tests/test_issuance_lifecycle.py": "716be93977ea6943bf7230ab348fe2e0aa76c67d82fb4eda82e3471b464dfd8e",
    "tests/test_metadata_representation.py": "23699e824b23799046db7420e0361e106e6934bb24896163f5082a18e55c4433",
    "tests/test_wheel_closure.py": "85366c6dbb44a1130c8722e1a54dcd89518c66b04e4b67d35809e59e4239cf69",
}

AUTHENTICODE_PINS = {
    "__init__.py": "f855d1fb94a9ce6fb0a509f11fecee080334c6f23f458b6a1d6517cb0b5bbdb0",
    "acquisition.py": "b59179d826a0728beefcb57ab49b49e65b2d460465469e2120bdda7d12f3cb71",
    "authority.py": "8e0bb2f2bc8b4bc9741ba8ebd94fdb3292fef9723e72be533e8e98167b7ea430",
    "canonical.py": "bb675526391f4298366ce70a9c5d7754a46ba9dbe263b976da7a71c6a0b9f7f4",
    "contract.py": "dd339a13c0ecbd1a2b006ff30fb6682c60fc5dbd6dfb736926232b0902f98278",
    "model.py": "8674f664c91e3d033ce2efcfe45008f297d72730350e53a1dcb6cba5acf623b3",
    "semantic.py": "3598317944243a57f24e694c6313fca92435960fdda87e2a9b964787255598db",
    "verifier.py": "6a2602dadb78360f1f9f22011485234b355df5ffe019c176cda1e0442d93d22e",
    "win32.py": "2bcfff0b3fffe9785de1e8574e7bf6eb0bbb81a776d00974e274ea0bf3a4856a",
}

LIFECYCLE_PINS = {
    "__init__.py": "56b43e5091371afa2ac2b96ac0220744537e5bc1b6bf0274da822a1ee9c18ccb",
    "acquisition.py": "3b8790b981dbf372e2147866c3fed11affb34dc92a4ccd3b78a8c84cebebc9f6",
    "candidate.py": "23365c09e2369024adce3faa5bba83bcb6ab71cd0d6c7e0f9506e022cf762d43",
    "canonical.py": "bafea3f6e2b4f19e98edbbea0a70a05750e9f2fa12b57c84f963269e6ed7a461",
    "errors.py": "bdb75b464b3e381d53acd44d477c8f837c170ccbe7844b019969c451ed6168d2",
    "materialize.py": "b5cd48c1a0a714f164c71ff30df430a27b0eb2e4452795e30c8dbad1cb37f5a5",
    "pins.py": "8ec74ae91a452a6c4367977364462ce273d6ff6307a0b8b43f517f54c224576d",
    "win32_secure.py": "b9c64a30cdf3e15c1334b4078ee4572cabf696c1ba4dada1e67abb43af013149",
}


@dataclass(frozen=True, slots=True)
class SourceSpec:
    label: str
    filename: str
    url: str
    sha256: str
    size: int
    retain_raw: bool
    pin_id: str | None = None


SPECS = (
    SourceSpec("cpython_artifact", "python-3.12.10-embed-amd64.zip", "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip", "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3", 11133606, False),
    SourceSpec("cpython_release_page", "python-31210-release.html", "https://www.python.org/downloads/release/python-31210/", "cc64f3159f7cbe565abe8b032439668b3cdbcd1768b1a08f7c7c79bcab881473", 9943, True),
    SourceSpec("cpython_ftp_index", "python-3.12.10-ftp-index.html", "https://www.python.org/ftp/python/3.12.10/", "e6f937dbe22df020bcf8f2f3b251da05f0e4c9cdd4ceeea58b27cd528a562e58", 8974, True),
    SourceSpec("cpython_sigstore", "python-3.12.10-embed-amd64.zip.sigstore", "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip.sigstore", "8aa5b4e555fd8b73b3dfef2f04328739f52d30706655930dcdf6111603d015be", 4915, True),
    SourceSpec("microsoft_release_history", "microsoft-release-history.html", "https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history", "8ead78ae6b47e27b40beb10d387e038719703c2b8c194840ec7eeaad2b970401", 287876, True),
    SourceSpec("buildtools_artifact", "vs_BuildTools.exe", "https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe", "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29", 4473936, False),
    SourceSpec("jsonschema_metadata", "jsonschema-4.26.0.json", "https://pypi.org/pypi/jsonschema/4.26.0/json", "d0c9ccdfa30c3cdc57b048c2be21123dfb0c2f4d6bef2e8324dcb4eac985cfcf", 9468, True, "jsonschema-4.26.0-py3-none-any"),
    SourceSpec("jsonschema_wheel", "jsonschema-4.26.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/69/90/f63fb5873511e014207a475e2bb4e8b2e570d655b00ac19a9a0ca0a385ee/jsonschema-4.26.0-py3-none-any.whl", "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce", 90630, True, "jsonschema-4.26.0-py3-none-any"),
    SourceSpec("attrs_metadata", "attrs-26.1.0.json", "https://pypi.org/pypi/attrs/26.1.0/json", "a882bf941fb4a0bb748d0194df544121cc130f5fb15a710ab6b804c17d2899b7", 11038, True, "attrs-26.1.0-py3-none-any"),
    SourceSpec("attrs_wheel", "attrs-26.1.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl", "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309", 67548, True, "attrs-26.1.0-py3-none-any"),
    SourceSpec("jsonschema_specifications_metadata", "jsonschema-specifications-2025.9.1.json", "https://pypi.org/pypi/jsonschema-specifications/2025.9.1/json", "91810d8f79384375ad0c0cf631e06903e2790b030d3fad2f1ad657b20ddd839e", 5037, True, "jsonschema-specifications-2025.9.1-py3-none-any"),
    SourceSpec("jsonschema_specifications_wheel", "jsonschema_specifications-2025.9.1-py3-none-any.whl", "https://files.pythonhosted.org/packages/41/45/1a4ed80516f02155c51f51e8cedb3c1902296743db0bbc66608a0db2814f/jsonschema_specifications-2025.9.1-py3-none-any.whl", "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe", 18437, True, "jsonschema-specifications-2025.9.1-py3-none-any"),
    SourceSpec("referencing_metadata", "referencing-0.37.0.json", "https://pypi.org/pypi/referencing/0.37.0/json", "a67968d8e03aa45e650fc2ff0d07796676db1a7841ce8e810bf2dba5af689464", 4842, True, "referencing-0.37.0-py3-none-any"),
    SourceSpec("referencing_wheel", "referencing-0.37.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/2c/58/ca301544e1fa93ed4f80d724bf5b194f6e4b945841c5bfd555878eea9fcb/referencing-0.37.0-py3-none-any.whl", "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231", 26766, True, "referencing-0.37.0-py3-none-any"),
    SourceSpec("rpds_py_metadata", "rpds-py-2026.6.3.json", "https://pypi.org/pypi/rpds-py/2026.6.3/json", "fff1fa33d84392d5684f0c1a40fc23f0a2027113c966498a1f64614bc83b02c2", 106094, True, "rpds-py-2026.6.3-cp312-cp312-win_amd64"),
    SourceSpec("rpds_py_wheel", "rpds_py-2026.6.3-cp312-cp312-win_amd64.whl", "https://files.pythonhosted.org/packages/04/3a/f0ee4d4dde9d3b69dedf1b5f74e7a40017046d55052d173e418c6a94f960/rpds_py-2026.6.3-cp312-cp312-win_amd64.whl", "2c958bf94822e9290a40aaf2a822d4bc5c88099093e3948ad6c571eca9272e5f", 220394, True, "rpds-py-2026.6.3-cp312-cp312-win_amd64"),
    SourceSpec("typing_extensions_metadata", "typing-extensions-4.16.0.json", "https://pypi.org/pypi/typing-extensions/4.16.0/json", "2140da00d62dde967f52d0be0ae28444f1d6a3fe603f52c83c23988c32122d5a", 5631, True, "typing-extensions-4.16.0-py3-none-any"),
    SourceSpec("typing_extensions_wheel", "typing_extensions-4.16.0-py3-none-any.whl", "https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl", "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8", 45571, True, "typing-extensions-4.16.0-py3-none-any"),
)


class LiveFailure(Exception):
    def __init__(self, code: str, details: dict[str, object] | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.details = details or {}


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.events: list[dict[str, object]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.events.append({"code": int(code), "from": req.full_url, "to": newurl})
        if len(self.events) > MAX_REDIRECTS:
            raise LiveFailure("redirect_bound_exceeded", {"redirects": self.events})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity_mapping(identity) -> dict[str, object]:
    return {
        "field_types": {
            "file_id_hex": "lowercase_hex_string",
            "volume_serial_decimal": "unsigned_decimal_string",
            "volume_serial_hex": "lowercase_hex_string",
        },
        "file_id_hex": identity.file_id.lower(),
        "volume_serial_decimal": str(identity.volume_serial),
        "volume_serial_hex": f"{identity.volume_serial:016x}",
    }


def authenticate_inputs(candidate_root: Path, auth_root: Path, lifecycle_root: Path) -> dict[str, str]:
    verification_expected = {"acquire_live_authority.py", "verify_candidate.py"}
    candidate_files = {
        path.relative_to(candidate_root).as_posix()
        for root in (candidate_root / "implementation", candidate_root / "tests")
        for path in root.rglob("*.py")
        if path.is_file()
    }
    if {path.name for path in (candidate_root / "verification").glob("*.py")} != verification_expected:
        raise LiveFailure("candidate_verification_inventory_mismatch")
    if candidate_files != set(CANDIDATE_PINS):
        raise LiveFailure("candidate_inventory_mismatch")
    if {path.name for path in auth_root.glob("*.py")} != set(AUTHENTICODE_PINS):
        raise LiveFailure("authenticode_inventory_mismatch")
    if {path.name for path in lifecycle_root.glob("*.py")} != set(LIFECYCLE_PINS):
        raise LiveFailure("lifecycle_inventory_mismatch")

    measured: dict[str, str] = {}
    for relative, expected in sorted(CANDIDATE_PINS.items()):
        observed = sha256_file(candidate_root / relative)
        if observed != expected:
            raise LiveFailure("candidate_hash_mismatch", {"path": relative})
        measured[f"candidate:{relative}"] = observed
    for name, expected in sorted(AUTHENTICODE_PINS.items()):
        observed = sha256_file(auth_root / name)
        if observed != expected:
            raise LiveFailure("authenticode_hash_mismatch", {"path": name})
        measured[f"authenticode:{name}"] = observed
    for name, expected in sorted(LIFECYCLE_PINS.items()):
        observed = sha256_file(lifecycle_root / name)
        if observed != expected:
            raise LiveFailure("lifecycle_hash_mismatch", {"path": name})
        measured[f"lifecycle:{name}"] = observed
    measured["candidate:verification/acquire_live_authority.py"] = sha256_file(Path(__file__).resolve())
    measured["candidate:verification/verify_candidate.py"] = sha256_file(
        candidate_root / "verification" / "verify_candidate.py"
    )
    return measured


def create_external_root(win32_secure, repository_root: Path):
    parent = Path(tempfile.gettempdir()).resolve()
    for _attempt in range(8):
        destination = parent / f"s0-v01-live-{secrets.token_hex(12)}"
        try:
            return win32_secure.secure_create_directory_root(
                repository_root=repository_root,
                destination=destination,
            )
        except Exception as exc:
            if str(exc) != "destination_not_fresh":
                raise
    raise LiveFailure("external_root_collision_bound_exceeded")


def expected_content_encoding(spec: SourceSpec) -> str:
    return "gzip" if spec.label == "cpython_release_page" else "identity"


def content_length_required(spec: SourceSpec) -> bool:
    return spec.label != "microsoft_release_history"


def validate_response_header_policy(
    spec: SourceSpec,
    *,
    content_encoding: str | None,
    content_length: str | None,
    details: dict[str, object],
) -> int | None:
    observed_encoding = (content_encoding or "identity").strip().lower()
    expected_encoding = expected_content_encoding(spec)
    details["content_encoding"] = observed_encoding
    details["content_encoding_expected"] = expected_encoding
    details["content_length_required"] = content_length_required(spec)
    if observed_encoding != expected_encoding:
        raise LiveFailure("content_encoding_mismatch", details)
    if content_length is None:
        if content_length_required(spec):
            raise LiveFailure("content_length_missing", details)
        return None
    try:
        parsed_length = int(content_length)
    except ValueError as exc:
        raise LiveFailure("content_length_invalid", details) from exc
    if parsed_length != spec.size:
        details["content_length"] = parsed_length
        raise LiveFailure("content_length_mismatch", details)
    return parsed_length


def validate_representation_magic(
    spec: SourceSpec,
    prefix: bytes,
    details: dict[str, object],
) -> None:
    is_gzip = prefix.startswith(b"\x1f\x8b\x08")
    details["raw_magic_hex"] = prefix[:16].hex()
    if expected_content_encoding(spec) == "gzip":
        if not is_gzip:
            raise LiveFailure("gzip_magic_mismatch", details)
    elif is_gzip:
        raise LiveFailure("identity_source_has_gzip_magic", details)


def download_to_root(spec: SourceSpec, root, *, keep_open: bool):
    created = root.create_file(("artifacts",), spec.filename)
    partial: dict[str, object] = {
        "expected_sha256": spec.sha256,
        "expected_size": spec.size,
        "label": spec.label,
        "phase": "request_setup",
        "request_accept_encoding": "identity",
        "requested_url": spec.url,
    }
    raw = bytearray() if spec.retain_raw else None
    prefix = bytearray()
    try:
        redirect_handler = RedirectRecorder()
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
            redirect_handler,
        )
        request = urllib.request.Request(
            spec.url,
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "identity",
                "User-Agent": "s0-v0.1-live-authority-test/1",
            },
            method="GET",
        )
        digest = hashlib.sha256()
        observed_size = 0
        partial["phase"] = "request_open"
        with opener.open(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            final_url = response.geturl()
            content_encoding = response.headers.get("Content-Encoding")
            content_length = response.headers.get("Content-Length")
            partial.update(
                {
                    "content_length": content_length,
                    "content_type": response.headers.get("Content-Type"),
                    "final_url": final_url,
                    "http_status": int(response.status),
                    "phase": "response_headers",
                    "redirect_count": len(redirect_handler.events),
                    "redirects": redirect_handler.events,
                }
            )
            if response.status != 200:
                raise LiveFailure("http_status_mismatch", partial)
            if final_url != spec.url or redirect_handler.events:
                raise LiveFailure("redirect_or_final_url_mismatch", partial)
            parsed_length = validate_response_header_policy(
                spec,
                content_encoding=content_encoding,
                content_length=content_length,
                details=partial,
            )
            partial["content_length"] = parsed_length
            partial["phase"] = "body_stream"
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                observed_size += len(chunk)
                if observed_size > spec.size:
                    raise LiveFailure("source_size_bound_exceeded", partial)
                created.write_all(chunk)
                digest.update(chunk)
                if len(prefix) < 16:
                    prefix.extend(chunk[: 16 - len(prefix)])
                if raw is not None:
                    raw.extend(chunk)
        partial["phase"] = "post_body_validation"
        validate_representation_magic(spec, bytes(prefix), partial)
        observed_sha256 = digest.hexdigest()
        partial.update({"observed_sha256": observed_sha256, "observed_size": observed_size})
        if observed_size != spec.size:
            raise LiveFailure("source_size_mismatch", partial)
        if observed_sha256 != spec.sha256:
            raise LiveFailure("source_sha256_mismatch", partial)
        partial["phase"] = "retained_file_validation"
        created.flush()
        persisted = created.readback_sha256(spec.size, CHUNK_SIZE)
        if persisted != spec.sha256:
            partial["persisted_sha256"] = persisted
            raise LiveFailure("persisted_sha256_mismatch", partial)
        snapshot = created.final_reauthenticate(spec.size)
        partial.update(
            {
                "destination": created.destination,
                "identity": identity_mapping(snapshot.identity),
                "persisted_sha256": persisted,
                "reparse_point": False,
            }
        )
        root.revalidate()
        if keep_open:
            return bytes(raw) if raw is not None else None, partial, created
        created.close()
        return bytes(raw) if raw is not None else None, partial, None
    except BaseException as primary_exc:
        close_failure: dict[str, object] | None = None
        try:
            created.close()
        except Exception as close_exc:
            close_failure = {
                "code": "download_handle_close_failed",
                "exception_class": type(close_exc).__name__,
                "message": str(close_exc),
            }
        if isinstance(primary_exc, LiveFailure):
            if close_failure is not None:
                primary_exc.details["secondary_failures"] = [close_failure]
            raise
        details = dict(partial)
        details.update(
            {
                "exception_class": type(primary_exc).__name__,
                "exception_message": str(primary_exc),
            }
        )
        if close_failure is not None:
            details["secondary_failures"] = [close_failure]
        raise LiveFailure("source_request_exception", details) from primary_exc


def write_secure_file(root, parent: tuple[str, ...], filename: str, raw: bytes) -> dict[str, object]:
    created = root.create_file(parent, filename)
    try:
        created.write_all(raw)
        created.flush()
        observed = created.readback_sha256(len(raw), CHUNK_SIZE)
        expected = hashlib.sha256(raw).hexdigest()
        if observed != expected:
            raise LiveFailure("evidence_readback_sha256_mismatch")
        snapshot = created.final_reauthenticate(len(raw))
        return {
            "identity": identity_mapping(snapshot.identity),
            "path": created.destination,
            "sha256": expected,
            "size": len(raw),
        }
    finally:
        created.close()


def static_candidate_state(candidate_module) -> dict[str, object]:
    return {
        "blockers": list(candidate_module.INITIAL_BLOCKERS),
        "buildtools_acquired_path": None,
        "buildtools_proposal_sha256": None,
        "buildtools_verifier_full_path": None,
        "nonclaims": {name: False for name in candidate_module.NONCLAIM_NAMES},
        "active_buildtools_authority": False,
        "acquired_or_downloaded_byte_executed": False,
        "build": False,
        "central_system": False,
        "compiled": False,
        "e0": False,
        "economic_value": False,
        "imported": False,
        "installed": False,
        "linked": False,
        "model_to_model_transfer": False,
        "offline_toolchain_layout": False,
        "operational_safety": False,
        "process_authority": False,
        "project_brain_integration": False,
        "rehearsal": False,
        "runtime": False,
        "s0": False,
    }


def proposal_mapping(proposal) -> dict[str, object]:
    return {
        "acquired_path": proposal.acquired_path,
        "acquired_byte_executed": proposal.acquired_byte_executed,
        "acquisition_authority_manifest_sha256": proposal.acquisition_authority_manifest_sha256,
        "acquisition_record_sha256": proposal.acquisition_record_sha256,
        "active_authority": proposal.active_authority,
        "artifact_id": proposal.artifact_id,
        "authenticode_decision_sha256": proposal.authenticode_decision_sha256,
        "authenticode_implementation_manifest_sha256": proposal.authenticode_implementation_manifest_sha256,
        "executed_code_authority_established": proposal.executed_code_authority_established,
        "filename": proposal.filename,
        "process_authority_granted": proposal.process_authority_granted,
        "sha256": proposal.sha256,
        "size": proposal.size,
        "status": proposal.status,
        "trust_policy_pass": proposal.trust_policy_pass,
        "url": proposal.url,
        "verifier_full_path": proposal.verifier_full_path,
    }


def verifier_mapping(result) -> dict[str, object]:
    return {
        "decision_sha256": result.decision_sha256,
        "executed_code_authority_established": result.executed_code_authority_established,
        "failure_relations": list(result.failure_relations),
        "observation_sha256": result.observation_sha256,
        "process_authority_granted": result.process_authority_granted,
        "runtime_authority_scope": result.runtime_authority_scope,
        "trace_sha256": result.trace_sha256,
        "trust_policy_pass": result.trust_policy_pass,
    }


def self_test() -> int:
    script = Path(__file__).resolve()
    candidate_root = script.parents[1]
    authenticode_root = (
        candidate_root.parent
        / "windows-authenticode-verifier-v0.4"
        / "implementation"
    )
    sys.path.insert(0, str(authenticode_root))
    sys.path.insert(0, str(candidate_root / "implementation"))
    canonical = importlib.import_module("s0_external_artifact_authority_acquisition.canonical")
    buildtools = importlib.import_module("s0_external_artifact_authority_acquisition.buildtools")
    auth_verifier = importlib.import_module("s0_windows_authenticode_verifier.verifier")

    class MaximumIdentity:
        volume_serial = 0xFFFFFFFFFFFFFFFF
        file_id = "f" * 32

    primary = {
        "code": "content_length_mismatch",
        "details": {
            "content_encoding": "identity",
            "content_length": 10000,
            "content_type": "text/html; charset=utf-8",
            "final_url": "https://www.python.org/downloads/release/python-31210/",
            "http_status": 200,
            "label": "cpython_release_page",
            "phase": "response_headers",
            "redirect_count": 0,
            "redirects": [],
            "request_accept_encoding": "identity",
            "requested_url": "https://www.python.org/downloads/release/python-31210/",
        },
        "exception_class": "LiveFailure",
        "message": "content_length_mismatch",
        "phase": "download:cpython_release_page",
    }
    secondary = {
        "code": "simulated_cleanup_failure",
        "exception_class": "RuntimeError",
        "message": "simulated_cleanup_failure",
    }
    test_evidence = {
        "blocker": primary,
        "external_root": {"identity": identity_mapping(MaximumIdentity())},
        "schema_id": SCHEMA_ID,
        "secondary_failures": [secondary],
        "status": "FAIL",
    }
    try:
        by_label = {spec.label: spec for spec in SPECS}
        release = by_label["cpython_release_page"]
        ftp = by_label["cpython_ftp_index"]
        microsoft = by_label["microsoft_release_history"]
        binary = by_label["buildtools_artifact"]
        validate_response_header_policy(
            release,
            content_encoding="gzip",
            content_length="9943",
            details={},
        )
        validate_representation_magic(release, b"\x1f\x8b\x08test", {})
        validate_response_header_policy(
            ftp,
            content_encoding="identity",
            content_length="8974",
            details={},
        )
        validate_representation_magic(ftp, b"<html>", {})
        validate_response_header_policy(
            microsoft,
            content_encoding="identity",
            content_length=None,
            details={},
        )
        validate_representation_magic(microsoft, b" <!DOCTYPE", {})
        validate_response_header_policy(
            binary,
            content_encoding="identity",
            content_length="4473936",
            details={},
        )
        validate_representation_magic(binary, b"MZ", {})
        rejected_cases = 0
        for callback in (
            lambda: validate_response_header_policy(
                release,
                content_encoding="identity",
                content_length="9943",
                details={},
            ),
            lambda: validate_response_header_policy(
                ftp,
                content_encoding="gzip",
                content_length="8974",
                details={},
            ),
            lambda: validate_representation_magic(release, b"not-gzip", {}),
            lambda: validate_response_header_policy(
                microsoft,
                content_encoding="identity",
                content_length="287499",
                details={},
            ),
        ):
            try:
                callback()
            except LiveFailure:
                rejected_cases += 1
        if rejected_cases != 4:
            raise LiveFailure("self_test_header_policy_rejection_mismatch")

        verifier_calls: list[str] = []

        def forbidden_native(*_args, **_kwargs):
            verifier_calls.append("native")
            raise AssertionError("public blocker invoked v0.4/native trust")

        acquired_path = (
            "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
            "bounded\\vs_BuildTools.exe"
        )
        verifier_full_path = "C:\\bounded\\vs_BuildTools.exe"
        adapter_arguments = {
            "release_history_raw": b"bounded-self-test-release-history",
            "verifier_full_path": verifier_full_path,
            "file_handle": 7,
            "sequence_id": "1" * 64,
            "producer_process_id": 11,
            "created_filetime_hex": "0000000000000001",
            "acquired_path": acquired_path,
            "volume_serial_hex": "2" * 16,
            "file_id_hex": "3" * 32,
        }
        originals = (
            auth_verifier.authenticate_installed_implementation,
            auth_verifier.authenticate_acquisition_record,
            auth_verifier.collect_observation,
            auth_verifier.evaluate_observation,
        )
        try:
            auth_verifier.authenticate_installed_implementation = forbidden_native
            auth_verifier.authenticate_acquisition_record = forbidden_native
            auth_verifier.collect_observation = forbidden_native
            auth_verifier.evaluate_observation = forbidden_native
            try:
                buildtools.verify_buildtools_and_propose_pin(**adapter_arguments)
                raise LiveFailure("self_test_public_blocker_missing")
            except buildtools.AuthorityError as exc:
                if str(exc) != "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED":
                    raise
            try:
                buildtools._require_issued_buildtools_proposal(object())
                raise LiveFailure("self_test_public_checker_blocker_missing")
            except buildtools.AuthorityError as exc:
                if str(exc) != "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED":
                    raise
        finally:
            (
                auth_verifier.authenticate_installed_implementation,
                auth_verifier.authenticate_acquisition_record,
                auth_verifier.collect_observation,
                auth_verifier.evaluate_observation,
            ) = originals
        if verifier_calls:
            raise LiveFailure("self_test_public_blocker_invoked_native_trust")
        split_path_preflight = {
            "acquired_path": acquired_path,
            "adapter_blocker": "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED",
            "native_trust_invoked": False,
            "network_used": False,
            "status": "FAIL-CLOSED-AS-EXPECTED",
            "verifier_full_path": verifier_full_path,
        }
        test_evidence["split_path_preflight"] = split_path_preflight

        raw = canonical.canonical_json_lf(test_evidence)
        with tempfile.TemporaryDirectory(prefix="s0-v01-live-self-test-") as temporary:
            evidence_path = Path(temporary) / "live-authority-evidence.json"
            sidecar_path = Path(temporary) / "live-authority-evidence.json.sha256"
            evidence_path.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            sidecar = f"{digest}  live-authority-evidence.json\n".encode("ascii")
            sidecar_path.write_bytes(sidecar)
            reread = evidence_path.read_bytes()
            reread_sidecar = sidecar_path.read_bytes()
            parsed = json.loads(reread.decode("utf-8"))
            if canonical.canonical_json_lf(parsed) != raw:
                raise LiveFailure("self_test_canonical_reread_mismatch")
            if reread_sidecar != sidecar or hashlib.sha256(reread).hexdigest() != digest:
                raise LiveFailure("self_test_sidecar_mismatch")
            if parsed["blocker"] != primary or parsed["secondary_failures"] != [secondary]:
                raise LiveFailure("self_test_primary_masked")
            if parsed["split_path_preflight"] != split_path_preflight:
                raise LiveFailure("self_test_split_path_serialization_mismatch")
            if parsed["external_root"]["identity"]["volume_serial_decimal"] != str(0xFFFFFFFFFFFFFFFF):
                raise LiveFailure("self_test_uint64_identity_mismatch")
        result = {
            "evidence_sha256": digest,
            "network_used": False,
            "header_policy_accept_cases": 4,
            "header_policy_reject_cases": rejected_cases,
            "primary_preserved": True,
            "schema_id": SCHEMA_ID,
            "sidecar_reread": True,
            "public_blocker_precedence": True,
            "public_checker_blocker": True,
            "split_path_fail_closed_serialization": True,
            "split_path_native_trust_invoked": False,
            "status": "PASS",
            "uint64_identity_canonical": True,
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except BaseException as exc:
        print(
            json.dumps(
                {
                    "error": {"exception_class": type(exc).__name__, "message": str(exc)},
                    "network_used": False,
                    "schema_id": SCHEMA_ID,
                    "status": "FAIL",
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 1


def main() -> int:
    script = Path(__file__).resolve()
    candidate_root = script.parents[1]
    repository_root = candidate_root.parents[2]
    auth_package_root = candidate_root.parent / "windows-authenticode-verifier-v0.4" / "implementation"
    auth_root = auth_package_root / "s0_windows_authenticode_verifier"
    lifecycle_package_root = candidate_root.parent / "build-runtime-materialization-external-pin-recovery-v0.2" / "implementation"
    lifecycle_root = lifecycle_package_root / "s0_public_external_pin_recovery"

    root = None
    buildtools_file = None
    initial_identity = None
    evidence_file: dict[str, object] | None = None
    sidecar_file: dict[str, object] | None = None
    output_root: str | None = None
    process_blocker: dict[str, object] | None = None
    secondary_failures: list[dict[str, object]] = []
    phase = "preflight"
    active_source: str | None = None
    exit_code = 1
    evidence: dict[str, object] = {
        "acquired_byte_actions": {
            "compiled": False,
            "executed": False,
            "imported": False,
            "installed": False,
            "linked": False,
        },
        "blocker": None,
        "candidate_state": None,
        "downloads": [],
        "network_used": False,
        "schema_id": SCHEMA_ID,
        "secondary_failures": secondary_failures,
        "status": "FAIL",
    }
    try:
        pre_hashes = authenticate_inputs(candidate_root, auth_root, lifecycle_root)
        phase = "imports"
        for path in (candidate_root / "implementation", auth_package_root, lifecycle_package_root):
            sys.path.insert(0, str(path))

        canonical = importlib.import_module("s0_external_artifact_authority_acquisition.canonical")
        candidate = importlib.import_module("s0_external_artifact_authority_acquisition.candidate")
        buildtools = importlib.import_module("s0_external_artifact_authority_acquisition.buildtools")
        metadata = importlib.import_module("s0_external_artifact_authority_acquisition.metadata")
        pins = importlib.import_module("s0_external_artifact_authority_acquisition.pins")
        wheel = importlib.import_module("s0_external_artifact_authority_acquisition.wheel")
        win32_secure = importlib.import_module("s0_public_external_pin_recovery.win32_secure")

        evidence["candidate_state"] = static_candidate_state(candidate)
        phase = "external_root_create"
        root = create_external_root(win32_secure, repository_root)
        output_root = root.destination
        initial_identity = root.identity
        root.create_directory(("artifacts",))
        root.create_directory(("evidence",))
        evidence["external_root"] = {
            "identity": identity_mapping(initial_identity),
            "path": output_root,
            "repository_excluded": True,
            "reparse_point": False,
        }

        raws: dict[str, bytes] = {}
        observations: list[dict[str, object]] = []
        evidence["network_used"] = True
        for spec in SPECS:
            active_source = spec.label
            phase = f"download:{spec.label}"
            raw, observation, retained = download_to_root(
                spec,
                root,
                keep_open=spec.label == "buildtools_artifact",
            )
            observations.append(observation)
            if raw is not None:
                raws[spec.label] = raw
            if retained is not None:
                buildtools_file = retained
        evidence["downloads"] = observations
        active_source = None
        phase = "candidate_source_validation"

        cpython_evidence = metadata.validate_cpython_source_metadata(
            raws["cpython_release_page"],
            raws["cpython_ftp_index"],
            raws["cpython_sigstore"],
        )
        microsoft_evidence = metadata.validate_microsoft_release_metadata(
            raws["microsoft_release_history"]
        )
        metadata_evidence: dict[str, Any] = {}
        wheel_evidence: dict[str, Any] = {}
        for spec in SPECS:
            if spec.pin_id is None:
                continue
            if spec.label.endswith("_metadata"):
                metadata_evidence[spec.pin_id] = metadata.validate_pypi_metadata(
                    spec.pin_id, raws[spec.label]
                )
            elif spec.label.endswith("_wheel"):
                wheel_evidence[spec.pin_id] = wheel.validate_wheel(
                    spec.pin_id, raws[spec.label]
                )
        phase = "candidate_closure_validation"
        closure = wheel.validate_jsonschema_closure(metadata_evidence, wheel_evidence)
        evidence["closure"] = {
            "dependency_graph": [
                {"dependencies": list(dependencies), "pin_id": pin_id}
                for pin_id, dependencies in closure.dependency_graph
            ],
            "extras_selected": closure.extras_selected,
            "imported": closure.imported,
            "installed": closure.installed,
            "metadata_aggregate_size": closure.metadata_aggregate_size,
            "pypi_json_requires_dist_inventory": [
                {"pin_id": pin_id, "requires_dist": list(requires_dist)}
                for pin_id, requires_dist in closure.pypi_json_requires_dist_inventory
            ],
            "runtime_authority": closure.runtime_authority,
            "wheel_metadata_requires_dist_inventory": [
                {"pin_id": pin_id, "requires_dist": list(requires_dist)}
                for pin_id, requires_dist in closure.wheel_metadata_requires_dist_inventory
            ],
            "wheel_aggregate_size": closure.wheel_aggregate_size,
            "wheel_pin_ids": list(closure.wheel_pin_ids),
        }
        base_state = candidate.assemble_candidate_state(
            cpython=cpython_evidence,
            microsoft=microsoft_evidence,
            jsonschema_closure=closure,
        )
        evidence["candidate_state"] = dict(base_state.to_mapping())

        phase = "buildtools_retained_handle_validation"
        if buildtools_file is None:
            raise LiveFailure("buildtools_retained_handle_missing")
        if buildtools_file.revalidate().length != 4473936:
            raise LiveFailure("buildtools_retained_size_mismatch")
        evidence["authenticode_verifier"] = {
            "blocker": "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED",
            "invoked": False,
        }
        phase = "buildtools_public_adapter"
        proposal = buildtools.verify_buildtools_and_propose_pin(
            release_history_raw=raws["microsoft_release_history"],
            verifier_full_path="C:\\blocked-before-native\\vs_BuildTools.exe",
            file_handle=1,
            sequence_id="1" * 64,
            producer_process_id=1,
            created_filetime_hex="0000000000000001",
            acquired_path=(
                "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
                "blocked-before-native\\vs_BuildTools.exe"
            ),
            volume_serial_hex="2" * 16,
            file_id_hex="3" * 32,
        )
        evidence["buildtools_proposal"] = proposal_mapping(proposal)
        phase = "final_candidate_assembly"
        state = candidate.assemble_candidate_state(
            cpython=cpython_evidence,
            microsoft=microsoft_evidence,
            jsonschema_closure=closure,
            buildtools_proposal=proposal,
        )
        evidence["candidate_state"] = dict(state.to_mapping())
        evidence["cpython_validation"] = {
            "certificate_chain_verification": cpython_evidence.certificate_chain_verification,
            "certificate_der_sha256": cpython_evidence.certificate_der_sha256,
            "certificate_der_size": cpython_evidence.certificate_der_size,
            "release_page_content_encoding": (
                cpython_evidence.release_page_content_encoding
            ),
            "release_page_decoded_entity_sha256": (
                cpython_evidence.release_page_decoded_entity_sha256
            ),
            "release_page_decoded_entity_size": (
                cpython_evidence.release_page_decoded_entity_size
            ),
            "release_page_decoder_authority_established": (
                cpython_evidence.release_page_decoder_authority_established
            ),
            "release_page_representation": cpython_evidence.release_page_representation,
            "signature_size": cpython_evidence.signature_size,
            "signature_verification": cpython_evidence.signature_verification,
            "sigstore_cryptographic_verification": cpython_evidence.sigstore_cryptographic_verification,
            "tlog_entry_count": cpython_evidence.tlog_entry_count,
            "transparency_log_verification": cpython_evidence.transparency_log_verification,
        }
        buildtools_file.close()
        buildtools_file = None
        root.revalidate()

        phase = "post_hash_authentication"
        post_hashes = authenticate_inputs(candidate_root, auth_root, lifecycle_root)
        if post_hashes != pre_hashes:
            raise LiveFailure("candidate_dependency_pre_post_mismatch")
        evidence["input_hashes_pre"] = pre_hashes
        evidence["input_hashes_post"] = post_hashes
        evidence["input_hashes_stable"] = True
        evidence["external_root"]["identity_before_evidence_write"] = identity_mapping(root.identity)
        if root.identity != initial_identity:
            raise LiveFailure("external_root_identity_changed")
        evidence["status"] = "PASS"
        phase = "evidence_write"
        exit_code = 0
    except BaseException as exc:
        process_blocker = {
            "exception_class": type(exc).__name__,
            "message": str(exc),
            "phase": phase,
        }
        if active_source is not None:
            process_blocker["source"] = active_source
        if isinstance(exc, LiveFailure):
            process_blocker["code"] = exc.code
            if exc.details:
                process_blocker["details"] = exc.details
        evidence["blocker"] = process_blocker
        evidence["status"] = "FAIL"
        exit_code = 1
        try:
            if "pre_hashes" in locals():
                post_hashes = authenticate_inputs(candidate_root, auth_root, lifecycle_root)
                evidence["input_hashes_pre"] = pre_hashes
                evidence["input_hashes_post"] = post_hashes
                evidence["input_hashes_stable"] = post_hashes == pre_hashes
                if post_hashes != pre_hashes:
                    secondary_failures.append({
                        "code": "candidate_dependency_pre_post_mismatch",
                        "exception_class": "LiveFailure",
                        "message": "candidate_dependency_pre_post_mismatch",
                        "phase": "failure_post_hash_authentication",
                    })
        except BaseException as hash_exc:
            secondary_failures.append({
                "code": "post_hash_check_failure",
                "exception_class": type(hash_exc).__name__,
                "message": str(hash_exc),
                "phase": "failure_post_hash_authentication",
            })
    finally:
        if buildtools_file is not None:
            try:
                buildtools_file.close()
            except BaseException as exc:
                secondary_failures.append({
                    "code": "buildtools_handle_close_failed",
                    "exception_class": type(exc).__name__,
                    "message": str(exc),
                    "phase": "cleanup_buildtools_handle",
                })
        if root is not None:
            try:
                if initial_identity is not None:
                    root.revalidate()
                    if root.identity != initial_identity:
                        raise LiveFailure("external_root_identity_changed_before_evidence")
                evidence_raw = canonical.canonical_json_lf(evidence)
                evidence_file = write_secure_file(
                    root,
                    ("evidence",),
                    "live-authority-evidence.json",
                    evidence_raw,
                )
                sidecar_raw = (
                    f"{evidence_file['sha256']}  live-authority-evidence.json\n".encode("ascii")
                )
                sidecar_file = write_secure_file(
                    root,
                    ("evidence",),
                    "live-authority-evidence.json.sha256",
                    sidecar_raw,
                )
                root.revalidate()
                if initial_identity is not None and root.identity != initial_identity:
                    raise LiveFailure("external_root_identity_changed_after_evidence")
            except BaseException as exc:
                secondary_failures.append({
                    "code": "evidence_write_or_revalidation_failed",
                    "exception_class": type(exc).__name__,
                    "message": str(exc),
                    "phase": "evidence_write",
                })
            try:
                root.close()
            except BaseException as exc:
                secondary_failures.append({
                    "code": "external_root_handle_close_failed",
                    "exception_class": type(exc).__name__,
                    "message": str(exc),
                    "phase": "cleanup_external_root_handle",
                })
        if process_blocker is None and secondary_failures:
            process_blocker = secondary_failures[0]
        if process_blocker is not None or secondary_failures:
            exit_code = 1

    result = {
        "blocker": process_blocker,
        "evidence": evidence_file,
        "external_root": output_root,
        "process_status": "PASS" if exit_code == 0 else "FAIL",
        "schema_id": SCHEMA_ID,
        "secondary_failures": secondary_failures,
        "sidecar": sidecar_file,
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return exit_code


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        raise SystemExit(self_test())
    if sys.argv[1:]:
        print(json.dumps({"error": "arguments_invalid", "status": "FAIL"}, separators=(",", ":")))
        raise SystemExit(2)
    raise SystemExit(main())
