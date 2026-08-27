from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


SCHEMA_ID = "S0-EXTERNAL-ARTIFACT-AUTHORITY-ACQUISITION-V0.1-VERIFICATION-1"
EXPECTED_TEST_COUNT = 44

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
    "verification/acquire_live_authority.py": "02bd439e80ee931cd656caf6cebd4935b9237a1c857837abfc3fb8caaf4ecdd4",
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


class VerificationFailure(Exception):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(
    candidate_root: Path,
    authenticode_root: Path,
    lifecycle_root: Path,
) -> tuple[dict[str, str], str]:
    candidate_files = {
        path.relative_to(candidate_root).as_posix()
        for root in (candidate_root / "implementation", candidate_root / "tests")
        for path in root.rglob("*.py")
        if path.is_file()
    }
    candidate_files.add("verification/acquire_live_authority.py")
    verification_files = {
        path.name
        for path in (candidate_root / "verification").glob("*.py")
        if path.is_file()
    }
    if verification_files != {"acquire_live_authority.py", "verify_candidate.py"}:
        raise VerificationFailure("verification_inventory_mismatch")
    if candidate_files != set(CANDIDATE_PINS):
        raise VerificationFailure("candidate_inventory_mismatch")
    authenticode_files = {
        path.name for path in authenticode_root.glob("*.py") if path.is_file()
    }
    if authenticode_files != set(AUTHENTICODE_PINS):
        raise VerificationFailure("authenticode_inventory_mismatch")
    lifecycle_files = {
        path.name for path in lifecycle_root.glob("*.py") if path.is_file()
    }
    if lifecycle_files != set(LIFECYCLE_PINS):
        raise VerificationFailure("lifecycle_inventory_mismatch")

    measured = {
        f"candidate:{relative}": sha256_file(candidate_root / relative)
        for relative in sorted(CANDIDATE_PINS)
    }
    measured.update(
        {
            f"authenticode:{name}": sha256_file(authenticode_root / name)
            for name in sorted(AUTHENTICODE_PINS)
        }
    )
    measured.update(
        {
            f"lifecycle:{name}": sha256_file(lifecycle_root / name)
            for name in sorted(LIFECYCLE_PINS)
        }
    )
    verifier_sha256 = sha256_file(
        candidate_root / "verification" / "verify_candidate.py"
    )
    return measured, verifier_sha256


def expected_inventory() -> dict[str, str]:
    expected = {
        f"candidate:{relative}": digest
        for relative, digest in sorted(CANDIDATE_PINS.items())
    }
    expected.update(
        {
            f"authenticode:{name}": digest
            for name, digest in sorted(AUTHENTICODE_PINS.items())
        }
    )
    expected.update(
        {
            f"lifecycle:{name}": digest
            for name, digest in sorted(LIFECYCLE_PINS.items())
        }
    )
    return expected


def require_equal(
    actual: dict[str, str],
    expected: dict[str, str],
    *,
    label: str,
) -> None:
    if actual != expected:
        raise VerificationFailure(label)


def run_sentinels(expected: dict[str, str]) -> dict[str, bool]:
    altered = dict(expected)
    first = sorted(altered)[0]
    altered[first] = "0" * 64 if altered[first] != "0" * 64 else "1" * 64
    hash_mismatch_detected = False
    try:
        require_equal(expected, altered, label="sentinel_hash_mismatch")
    except VerificationFailure as exc:
        hash_mismatch_detected = str(exc) == "sentinel_hash_mismatch"
    if not hash_mismatch_detected:
        raise VerificationFailure("hash_mismatch_sentinel_failed")

    mutation_detected = False
    with tempfile.TemporaryDirectory(prefix="s0-v01-verification-") as temporary:
        sentinel = Path(temporary) / "sentinel.bin"
        sentinel.write_bytes(b"before")
        before = {"sentinel": sha256_file(sentinel)}
        sentinel.write_bytes(b"after")
        after = {"sentinel": sha256_file(sentinel)}
        try:
            require_equal(after, before, label="sentinel_mutation")
        except VerificationFailure as exc:
            mutation_detected = str(exc) == "sentinel_mutation"
    if not mutation_detected:
        raise VerificationFailure("mutation_sentinel_failed")
    return {
        "hash_mismatch_detected": hash_mismatch_detected,
        "mutation_detected": mutation_detected,
    }


def run_tests(candidate_root: Path, repository_root: Path) -> int:
    command = [
        sys.executable,
        "-I",
        "-B",
        "-m",
        "unittest",
        "discover",
        "-s",
        str(candidate_root / "tests"),
        "-p",
        "test_*.py",
        "-v",
    ]
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=repository_root,
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=30,
        check=False,
    )
    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran ([0-9]+) tests? in ", combined)
    if completed.returncode != 0:
        raise VerificationFailure("offline_tests_failed")
    if match is None:
        raise VerificationFailure("offline_test_count_missing")
    count = int(match.group(1))
    if count != EXPECTED_TEST_COUNT:
        raise VerificationFailure("offline_test_count_mismatch")
    return count


def retained_root_diagnostic(retained_root: Path) -> int:
    """Reauthenticate one supplied retained root without network or native trust."""

    candidate_root = Path(__file__).resolve().parents[1]
    authenticode_package_root = (
        candidate_root.parent
        / "windows-authenticode-verifier-v0.4"
        / "implementation"
    )
    verification_root = candidate_root / "verification"
    sys.path.insert(0, str(verification_root))
    sys.path.insert(0, str(authenticode_package_root))
    sys.path.insert(0, str(candidate_root / "implementation"))
    try:
        import acquire_live_authority as live
        from s0_external_artifact_authority_acquisition import (
            buildtools,
            candidate,
            metadata,
            pins,
            wheel,
        )
        from s0_external_artifact_authority_acquisition.errors import AuthorityError
        from s0_windows_authenticode_verifier import verifier as auth_verifier

        artifact_root = retained_root.resolve(strict=True) / "artifacts"
        if not artifact_root.is_dir():
            raise VerificationFailure("retained_artifact_root_missing")
        expected_names = {spec.filename for spec in live.SPECS}
        observed_entries = tuple(artifact_root.iterdir())
        if (
            len(expected_names) != 18
            or any(not path.is_file() for path in observed_entries)
            or {path.name for path in observed_entries} != expected_names
        ):
            raise VerificationFailure("retained_artifact_inventory_mismatch")

        raw_by_label: dict[str, bytes] = {}
        pre: dict[str, str] = {}
        for spec in live.SPECS:
            raw = (artifact_root / spec.filename).read_bytes()
            if len(raw) != spec.size or hashlib.sha256(raw).hexdigest() != spec.sha256:
                raise VerificationFailure(f"retained_artifact_authentication_failed:{spec.label}")
            raw_by_label[spec.label] = raw
            pre[spec.label] = spec.sha256

        cpython = metadata.validate_cpython_source_metadata(
            raw_by_label["cpython_release_page"],
            raw_by_label["cpython_ftp_index"],
            raw_by_label["cpython_sigstore"],
        )
        microsoft = metadata.validate_microsoft_release_metadata(
            raw_by_label["microsoft_release_history"]
        )
        pypi = {}
        wheels = {}
        for spec in live.SPECS:
            if spec.pin_id is None:
                continue
            if spec.label.endswith("_metadata"):
                pypi[spec.pin_id] = metadata.validate_pypi_metadata(
                    spec.pin_id, raw_by_label[spec.label]
                )
            elif spec.label.endswith("_wheel"):
                wheels[spec.pin_id] = wheel.validate_wheel(
                    spec.pin_id, raw_by_label[spec.label]
                )
        closure = wheel.validate_jsonschema_closure(pypi, wheels)

        native_calls: list[str] = []

        def forbidden(name: str):
            def fail(*_args, **_kwargs):
                native_calls.append(name)
                raise AssertionError(f"native trust invoked:{name}")

            return fail

        rebound_names = (
            "authenticate_installed_implementation",
            "authenticate_acquisition_record",
            "collect_observation",
            "evaluate_observation",
        )
        originals = tuple(getattr(auth_verifier, name) for name in rebound_names)
        try:
            for name in rebound_names:
                setattr(auth_verifier, name, forbidden(name))
            try:
                buildtools.verify_buildtools_and_propose_pin(
                    release_history_raw=raw_by_label["microsoft_release_history"],
                    verifier_full_path="C:\\retained\\vs_BuildTools.exe",
                    file_handle=1,
                    sequence_id="1" * 64,
                    producer_process_id=1,
                    created_filetime_hex="0000000000000001",
                    acquired_path=(
                        "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
                        "retained\\vs_BuildTools.exe"
                    ),
                    volume_serial_hex="2" * 16,
                    file_id_hex="3" * 32,
                )
                raise VerificationFailure("retained_public_blocker_missing")
            except AuthorityError as exc:
                if str(exc) != "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED":
                    raise
            try:
                buildtools._require_issued_buildtools_proposal(object())
                raise VerificationFailure("retained_public_checker_blocker_missing")
            except AuthorityError as exc:
                if str(exc) != "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED":
                    raise
        finally:
            for name, original in zip(rebound_names, originals, strict=True):
                setattr(auth_verifier, name, original)
        if native_calls:
            raise VerificationFailure("retained_native_trust_invoked")

        state = candidate.assemble_candidate_state(
            cpython=cpython,
            microsoft=microsoft,
            jsonschema_closure=closure,
        )
        if (
            "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED"
            not in state.blockers
            or "BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING" not in state.blockers
            or state.buildtools_proposal_sha256 is not None
            or state.active_buildtools_authority is not False
            or state.process_authority is not False
            or any(value is not False for _name, value in state.nonclaims)
        ):
            raise VerificationFailure("retained_final_authority_nonclaim_mismatch")

        # Prove that candidate consumption returned all bounded registries to zero.
        recovery_cpython = metadata.validate_cpython_source_metadata(
            raw_by_label["cpython_release_page"],
            raw_by_label["cpython_ftp_index"],
            raw_by_label["cpython_sigstore"],
        )
        recovery_microsoft = metadata.validate_microsoft_release_metadata(
            raw_by_label["microsoft_release_history"]
        )
        recovery_pypi = {}
        for spec in live.SPECS:
            if spec.pin_id is not None and spec.label.endswith("_metadata"):
                recovery_pypi[spec.pin_id] = metadata.validate_pypi_metadata(
                    spec.pin_id, raw_by_label[spec.label]
                )
        recovery_closure = wheel.validate_jsonschema_closure(recovery_pypi, wheels)
        if not metadata._release_issued_metadata_evidence(recovery_cpython, "cpython"):
            raise VerificationFailure("retained_cpython_recovery_release_failed")
        if not metadata._release_issued_metadata_evidence(recovery_microsoft, "microsoft"):
            raise VerificationFailure("retained_microsoft_recovery_release_failed")
        if not wheel._release_issued_jsonschema_closure(recovery_closure):
            raise VerificationFailure("retained_closure_recovery_release_failed")

        post = {
            spec.label: hashlib.sha256(
                (artifact_root / spec.filename).read_bytes()
            ).hexdigest()
            for spec in live.SPECS
        }
        if post != pre:
            raise VerificationFailure("retained_pre_post_mutation")
        evidence = {
            "acquired_byte_actions": {
                "compiled": False,
                "executed": False,
                "imported": False,
                "installed": False,
                "linked": False,
            },
            "blockers_retained": [
                "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED",
                "BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING",
            ],
            "closure_pin_count": len(closure.wheel_pin_ids),
            "final_authority": False,
            "native_trust_invocation_count": len(native_calls),
            "public_checker_blocked": True,
            "public_proposal_blocked": True,
            "registry_recovery": {
                "closure": True,
                "cpython": True,
                "microsoft": True,
                "pypi": True,
            },
            "retained_file_count": len(pre),
            "retained_file_sha256": {key: post[key] for key in sorted(post)},
            "retained_pre_post_stable": True,
            "status": "PASS",
            "wheel_validation_count": len(wheels),
        }
        print(json.dumps(evidence, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, VerificationFailure) as exc:
        print(
            json.dumps(
                {
                    "error": str(exc),
                    "network_used": False,
                    "status": "FAIL",
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 1


def main() -> int:
    candidate_root = Path(__file__).resolve().parents[1]
    repository_root = candidate_root.parents[2]
    authenticode_root = (
        candidate_root.parent
        / "windows-authenticode-verifier-v0.4"
        / "implementation"
        / "s0_windows_authenticode_verifier"
    )
    lifecycle_root = (
        candidate_root.parent
        / "build-runtime-materialization-external-pin-recovery-v0.2"
        / "implementation"
        / "s0_public_external_pin_recovery"
    )
    try:
        expected = expected_inventory()
        pre, verifier_pre = inventory(
            candidate_root,
            authenticode_root,
            lifecycle_root,
        )
        require_equal(pre, expected, label="pre_hash_mismatch")
        sentinels = run_sentinels(expected)
        count = run_tests(candidate_root, repository_root)
        post, verifier_post = inventory(
            candidate_root,
            authenticode_root,
            lifecycle_root,
        )
        require_equal(post, expected, label="post_hash_mismatch")
        require_equal(post, pre, label="pre_post_mutation")
        if verifier_post != verifier_pre:
            raise VerificationFailure("verifier_pre_post_mutation")
        evidence = {
            "acquired_byte_actions": {
                "compiled": False,
                "executed": False,
                "imported": False,
                "installed": False,
                "linked": False,
            },
            "file_count": len(expected),
            "file_sha256": {key: post[key] for key in sorted(post)},
            "network_used": False,
            "offline_test_count": count,
            "schema_id": SCHEMA_ID,
            "sentinels": sentinels,
            "status": "PASS",
            "verifier_pre_post_stable": True,
            "verifier_sha256": verifier_post,
        }
        print(json.dumps(evidence, sort_keys=True, separators=(",", ":")))
        return 0
    except (OSError, subprocess.SubprocessError, VerificationFailure) as exc:
        evidence = {
            "error": str(exc),
            "network_used": False,
            "schema_id": SCHEMA_ID,
            "status": "FAIL",
        }
        print(json.dumps(evidence, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    if not sys.argv[1:]:
        raise SystemExit(main())
    if len(sys.argv) == 3 and sys.argv[1] == "--retained-root":
        raise SystemExit(retained_root_diagnostic(Path(sys.argv[2])))
    print(
        json.dumps(
            {"error": "arguments_invalid", "network_used": False, "status": "FAIL"},
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    raise SystemExit(2)
