"""Live, non-executing acquisition harness for the two public URL pins.

This TEST-owned harness is intentionally not a general downloader.  A later
TEST runner may invoke it once to acquire exactly the Visual Studio Build
Tools bootstrapper and the CPython 3.12.10 embeddable ZIP named by the
candidate.  Redirects are blocked, every output stays outside the repository,
and the unique temporary root is never removed, including after failure.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Iterable
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener


_FROZEN_CPYTHON_SHA256 = (
    "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3"
)
_READ_SIZE = 1024 * 1024
_USER_AGENT = "s0-external-pin-live-verification/0.1"


class HarnessFailure(RuntimeError):
    """A fail-closed live-harness condition."""


class _RedirectBlockingHandler(HTTPRedirectHandler):
    """Reject every redirect while retaining an auditable attempt count."""

    def __init__(self) -> None:
        super().__init__()
        self.redirect_count = 0

    def redirect_request(  # type: ignore[override]
        self,
        request: Request,
        response,
        code: int,
        message: str,
        headers,
        new_url: str,
    ) -> None:
        del new_url
        self.redirect_count += 1
        raise HTTPError(
            request.full_url,
            code,
            f"redirect blocked: {message}",
            headers,
            response,
        )


def _canonical_json_line(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _response_chunks(response) -> Iterable[bytes]:
    while True:
        chunk = response.read(_READ_SIZE)
        if not chunk:
            return
        yield chunk


def _require_acquisition_pin_contract(pin: object, label: str) -> None:
    required_attributes = (
        "name",
        "filename",
        "url",
        "expected_size",
        "max_size",
        "expected_sha256",
    )
    missing = [name for name in required_attributes if not hasattr(pin, name)]
    if missing:
        raise HarnessFailure(
            f"{label} pin does not satisfy candidate acquisition contract: "
            + ",".join(missing)
        )


def _acquire_from_exact_uri(
    *,
    pin: object,
    destination: Path,
    repository_root: Path,
    acquire_pinned_artifact,
    request_log: list[str],
):
    url = getattr(pin, "url")
    if type(url) is not str or not url:
        raise HarnessFailure("candidate pin URL is absent or invalid")

    redirect_handler = _RedirectBlockingHandler()
    opener = build_opener(redirect_handler)
    request = Request(
        url,
        headers={
            "Accept-Encoding": "identity",
            "User-Agent": _USER_AGENT,
        },
        method="GET",
    )
    request_log.append(url)
    with opener.open(request, timeout=120) as response:
        final_uri = response.geturl()
        if redirect_handler.redirect_count != 0:
            raise HarnessFailure("redirect count is not zero")
        if final_uri != url:
            raise HarnessFailure("response final URI differs from the pinned URI")
        if response.getcode() != 200:
            raise HarnessFailure("response status is not 200")
        return acquire_pinned_artifact(
            pin,
            chunks=_response_chunks(response),
            observed_uri=final_uri,
            redirect_count=redirect_handler.redirect_count,
            destination=destination,
            repository_root=repository_root,
            max_chunk_size=_READ_SIZE,
        )


def _artifact_report(evidence, workflow_status: str) -> dict[str, object]:
    return {
        "authenticated": evidence.authenticated,
        "candidate_process_authority": evidence.process_authority,
        "expected_sha256": evidence.expected_sha256,
        "expected_size": evidence.expected_size,
        "final_uri": evidence.source_uri,
        "path": evidence.destination,
        "redirect_count": evidence.redirect_count,
        "sha256": evidence.observed_sha256,
        "size": evidence.observed_size,
        "status": workflow_status,
    }


def _observe_partial_file(path: Path) -> dict[str, object]:
    observation: dict[str, object] = {
        "exists": os.path.lexists(path),
        "path": str(path),
        "sha256": None,
        "size": None,
    }
    if not observation["exists"]:
        return observation
    try:
        item = os.lstat(path)
        if stat.S_ISREG(item.st_mode) and not stat.S_ISLNK(item.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as source:
                while True:
                    chunk = source.read(_READ_SIZE)
                    if not chunk:
                        break
                    digest.update(chunk)
            observation["size"] = item.st_size
            observation["sha256"] = digest.hexdigest()
    except OSError as exc:
        observation["observation_error"] = type(exc).__name__
    return observation


def _decision_report(decision) -> tuple[list[dict[str, str]], dict[str, bool]]:
    blockers = [
        {
            "description": blocker.description,
            "id": blocker.blocker_id,
        }
        for blocker in decision.blockers
    ]
    claims = {
        "build_claimed": decision.build_claimed,
        "build_validated": decision.build_validated,
        "e0_claimed": decision.e0_claimed,
        "e0_validated": decision.e0_validated,
        "install_claimed": decision.installation_claimed,
        "install_validated": decision.install_validated,
        "process_executed": False,
        "process_authority_granted": decision.process_authority_granted,
        "rehearsal_claimed": decision.rehearsal_claimed,
        "rehearsal_validated": decision.rehearsal_validated,
        "runtime_claimed": decision.runtime_claimed,
        "runtime_validated": decision.runtime_validated,
        "s0_claimed": decision.s0_claimed,
        "s0_validated": decision.s0_validated,
    }
    if any(claims.values()):
        raise HarnessFailure("candidate emitted a positive process or validation claim")
    return blockers, claims


def main() -> int:
    harness_path = Path(__file__).resolve(strict=True)
    repository_root = harness_path.parents[4].resolve(strict=True)
    external_root = Path(
        tempfile.mkdtemp(prefix="s0-live-external-pin-")
    ).resolve(strict=True)
    downloads_root = external_root / "downloads"
    downloads_root.mkdir(mode=0o700, exist_ok=False)

    report: dict[str, object] = {
        "artifacts": {},
        "blockers": [],
        "candidate_eligible": False,
        "claims": {
            "build_claimed": False,
            "install_claimed": False,
            "process_executed": False,
            "runtime_claimed": False,
        },
        "error": None,
        "external_root": str(external_root),
        "external_root_preserved": True,
        "jsonschema_acquired": False,
        "request_log": [],
        "schema": "s0-live-external-pin-verification-v0.1",
        "staging": None,
        "status": "FAILED-CLOSED",
    }

    build_tools_path: Path | None = None
    cpython_path: Path | None = None
    staging_path: Path | None = None

    try:
        if _is_within(external_root, repository_root):
            raise HarnessFailure("temporary root is inside the repository")

        implementation_root = harness_path.parents[1] / "implementation"
        sys.path.insert(0, str(implementation_root))
        from s0_public_external_pin_recovery.acquisition import (  # noqa: PLC0415
            acquire_pinned_artifact,
        )
        from s0_public_external_pin_recovery.candidate import (  # noqa: PLC0415
            evaluate_candidate,
        )
        from s0_public_external_pin_recovery.materialize import (  # noqa: PLC0415
            stage_zip_archive,
        )
        from s0_public_external_pin_recovery.pins import (  # noqa: PLC0415
            CPYTHON_PIN,
            CPYTHON_SHA256,
            CPYTHON_URL,
            JSONSCHEMA_URL,
            VS_BUILD_TOOLS_PIN,
            VS_BUILD_TOOLS_SHA256,
            VS_BUILD_TOOLS_URL,
        )

        decision = evaluate_candidate()
        blockers, claims = _decision_report(decision)
        report["blockers"] = blockers
        report["claims"] = claims
        report["candidate_eligible"] = decision.eligible
        if decision.eligible or not decision.blocked:
            raise HarnessFailure("candidate decision did not remain blocked")

        if JSONSCHEMA_URL is not None:
            raise HarnessFailure("jsonschema unexpectedly has an acquisition URL")
        if CPYTHON_SHA256 != _FROZEN_CPYTHON_SHA256:
            raise HarnessFailure("frozen CPython SHA-256 changed")
        if VS_BUILD_TOOLS_SHA256 is not None:
            raise HarnessFailure("Build Tools unexpectedly has an expected SHA-256")
        if CPYTHON_PIN.url != CPYTHON_URL:
            raise HarnessFailure("CPython pin URL differs from its frozen constant")
        if VS_BUILD_TOOLS_PIN.url != VS_BUILD_TOOLS_URL:
            raise HarnessFailure("Build Tools pin URL differs from its frozen constant")

        _require_acquisition_pin_contract(VS_BUILD_TOOLS_PIN, "Build Tools")
        _require_acquisition_pin_contract(CPYTHON_PIN, "CPython")

        build_tools_path = downloads_root / VS_BUILD_TOOLS_PIN.filename
        cpython_path = downloads_root / CPYTHON_PIN.filename
        staging_path = external_root / "cpython-3.12.10-embed-amd64-staged"

        request_log = report["request_log"]
        assert isinstance(request_log, list)
        build_tools_evidence = _acquire_from_exact_uri(
            pin=VS_BUILD_TOOLS_PIN,
            destination=build_tools_path,
            repository_root=repository_root,
            acquire_pinned_artifact=acquire_pinned_artifact,
            request_log=request_log,
        )
        if (
            build_tools_evidence.expected_sha256 is not None
            or build_tools_evidence.authenticated
            or build_tools_evidence.process_authority
            or build_tools_evidence.status != "unauthenticated"
        ):
            raise HarnessFailure("Build Tools did not remain unauthenticated")
        report["artifacts"]["vs_build_tools"] = _artifact_report(
            build_tools_evidence,
            "ACQUIRED-UNAUTHENTICATED",
        )

        cpython_evidence = _acquire_from_exact_uri(
            pin=CPYTHON_PIN,
            destination=cpython_path,
            repository_root=repository_root,
            acquire_pinned_artifact=acquire_pinned_artifact,
            request_log=request_log,
        )
        if (
            cpython_evidence.expected_sha256 != _FROZEN_CPYTHON_SHA256
            or cpython_evidence.observed_sha256 != _FROZEN_CPYTHON_SHA256
            or not cpython_evidence.authenticated
            or cpython_evidence.status != "authenticated"
        ):
            raise HarnessFailure("CPython did not match its authenticated pin")
        report["artifacts"]["cpython"] = _artifact_report(
            cpython_evidence,
            "ACQUIRED-AUTHENTICATED",
        )

        staging_evidence = stage_zip_archive(
            cpython_path,
            _FROZEN_CPYTHON_SHA256,
            staging_path,
            repository_root=repository_root,
        )
        if (
            staging_evidence.process_authority_granted
            or staging_evidence.installed
            or staging_evidence.executed
            or staging_evidence.imported
        ):
            raise HarnessFailure("CPython staging was not inert")
        report["staging"] = {
            "archive_sha256": staging_evidence.archive_sha256,
            "directory_count": staging_evidence.directory_count,
            "file_count": staging_evidence.file_count,
            "path": staging_evidence.destination_path,
            "target_set_sha256": staging_evidence.target_set_sha256,
            "total_size": staging_evidence.total_size,
        }

        if request_log != [VS_BUILD_TOOLS_URL, CPYTHON_URL]:
            raise HarnessFailure("network request set or order differs from the two pins")
        report["status"] = "LIVE-ACQUISITION-COMPLETED-CANDIDATE-BLOCKED"
        sys.stdout.buffer.write(_canonical_json_line(report))
        return 0
    except Exception as exc:
        report["error"] = {
            "message": str(exc),
            "type": type(exc).__name__,
        }
        artifacts = report["artifacts"]
        assert isinstance(artifacts, dict)
        if build_tools_path is not None and "vs_build_tools" not in artifacts:
            artifacts["vs_build_tools_partial"] = _observe_partial_file(
                build_tools_path
            )
        if cpython_path is not None and "cpython" not in artifacts:
            artifacts["cpython_partial"] = _observe_partial_file(cpython_path)
        if staging_path is not None and report["staging"] is None:
            report["staging"] = {
                "exists": os.path.lexists(staging_path),
                "path": str(staging_path),
            }
        sys.stdout.buffer.write(_canonical_json_line(report))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
