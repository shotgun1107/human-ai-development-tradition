"""Canonical launch evidence and locator-free admission frame v4."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from .canonical import canonical_json_bytes, require_sha256, safe_virtual_path, sha256_bytes
from .errors import RuntimeProfileError
from .semantic import HandleBinding


_LOCATOR = re.compile(r"^0x[0-9a-f]{16}$")


@dataclass(frozen=True)
class LaunchIdentity:
    run_nonce: str
    preloader_image_sha256: str
    runtime_package_sha256: str
    application_virtual_path: str
    application_sha256: str
    bootstrap_virtual_path: str
    bootstrap_sha256: str
    verifier_virtual_path: str
    verifier_sha256: str

    def __post_init__(self) -> None:
        for value in (
            self.run_nonce,
            self.preloader_image_sha256,
            self.runtime_package_sha256,
            self.application_sha256,
            self.bootstrap_sha256,
            self.verifier_sha256,
        ):
            require_sha256(value, "launch identity hash or nonce")
        for value in (
            self.application_virtual_path,
            self.bootstrap_virtual_path,
            self.verifier_virtual_path,
        ):
            safe_virtual_path(value)


@dataclass(frozen=True)
class LaunchEvidence:
    raw: bytes
    sha256: str
    handles: tuple[HandleBinding, ...]


@dataclass(frozen=True)
class AdmissionFrame:
    raw: bytes
    sha256: str
    actual_verifier_pid: int
    launch_evidence_sha256: str


def _ascii_field(name: str, value: object) -> bytes:
    if type(name) is not str or not name or "=" in name or "\n" in name:
        raise RuntimeProfileError("evidence field name is not exact ASCII text")
    text = str(value)
    if not text or any(ord(char) < 0x20 or ord(char) > 0x7E for char in text):
        raise RuntimeProfileError("evidence field value is not printable ASCII")
    if "=" in text or "\n" in text or "\r" in text:
        raise RuntimeProfileError("evidence field value contains a delimiter")
    return f"{name}={text}\n".encode("ascii")


def build_launch_evidence(
    profile: Mapping[str, object],
    identity: LaunchIdentity,
    handles: tuple[HandleBinding, ...],
) -> LaunchEvidence:
    process = profile["process_creation_policy"]
    launch = profile["launch_handle_set_evidence"]
    assert isinstance(process, Mapping) and isinstance(launch, Mapping)
    if len(handles) != 5:
        raise RuntimeProfileError("launch evidence requires exactly five handles")
    expected = tuple(
        (item["role"], item["kind"], item["access"])
        for item in process["ordered_handles"]
    )
    actual = tuple((item.role, item.kind, item.access) for item in handles)
    locators = tuple(item.locator for item in handles)
    if actual != expected:
        raise RuntimeProfileError("launch evidence handle order or policy differs")
    if (
        any(_LOCATOR.fullmatch(value) is None for value in locators)
        or len(set(locators)) != 5
        or any(value in {"0x0000000000000000", "0xffffffffffffffff"} for value in locators)
    ):
        raise RuntimeProfileError("launch evidence locator set is invalid")

    fields: list[tuple[str, object]] = [
        ("schema_id", launch["evidence_schema_id"]),
        ("run_nonce", identity.run_nonce),
        ("preloader_image_sha256", identity.preloader_image_sha256),
        ("runtime_package_sha256", identity.runtime_package_sha256),
        ("application_virtual_path", identity.application_virtual_path),
        ("application_sha256", identity.application_sha256),
        ("bootstrap_virtual_path", identity.bootstrap_virtual_path),
        ("bootstrap_sha256", identity.bootstrap_sha256),
        ("verifier_virtual_path", identity.verifier_virtual_path),
        ("verifier_sha256", identity.verifier_sha256),
        ("creation_flags_numeric", process["creation_flags_numeric"]),
        ("startupinfoex_dwflags", process["startupinfoex_dwflags"]),
        ("b_inherit_handles", "true" if process["b_inherit_handles"] else "false"),
        ("attribute_count", process["attribute_count"]),
        ("attribute_id_numeric", process["attribute_id_numeric"]),
        ("handle_array_bytes_x64", process["handle_array_bytes_x64"]),
        ("handle_count", process["handle_count"]),
        ("precreation_verifier_pid", 0),
    ]
    for index, handle in enumerate(handles):
        fields.extend(
            (
                (f"handle_{index}_role", handle.role),
                (f"handle_{index}_kind", handle.kind),
                (f"handle_{index}_access", handle.access),
                (f"handle_{index}_locator", handle.locator),
            )
        )
    raw = b"".join(_ascii_field(name, value) for name, value in fields)
    return LaunchEvidence(raw, sha256_bytes(raw), handles)


def build_admission_frame(
    profile: Mapping[str, object],
    *,
    evidence: LaunchEvidence,
    actual_verifier_pid: int,
    runtime_profile_v0_4_sha256: str,
    effective_runtime_package_sha256: str,
) -> AdmissionFrame:
    if type(actual_verifier_pid) is not int or actual_verifier_pid <= 0:
        raise RuntimeProfileError("actual verifier PID is invalid")
    require_sha256(runtime_profile_v0_4_sha256, "v0.4 profile hash")
    require_sha256(effective_runtime_package_sha256, "runtime package hash")
    policy = profile["admission_frame_policy"]
    assert isinstance(policy, Mapping)
    value: dict[str, object] = {
        "actual_verifier_pid": actual_verifier_pid,
        "createprocess_result_policy_id": "createprocess-success-bound-v0.4",
        "effective_runtime_package_sha256": effective_runtime_package_sha256,
        "guard_observation_policy_id": policy["guard_observation_policy_id"],
        "kernel_semantics_policy_id": policy["kernel_semantics_policy_id"],
        "launch_handle_set_evidence_sha256": evidence.sha256,
        "preloader_responsibility_id": policy["preloader_responsibility_id"],
        "runtime_profile_v0_1_sha256": profile["v0_1_profile_sha256"],
        "runtime_profile_v0_2_sha256": profile["v0_2_profile_sha256"],
        "runtime_profile_v0_3_sha256": profile["v0_3_profile_sha256"],
        "runtime_profile_v0_4_sha256": runtime_profile_v0_4_sha256,
        "schema_id": policy["schema_id"],
    }
    raw = canonical_json_bytes(value)
    if len(raw) > policy["maximum_bytes"]:
        raise RuntimeProfileError("admission frame exceeds its exact bound")
    forbidden = ("locator", "handle_value", "numeric_handle")
    if any(any(token in key for token in forbidden) for key in value):
        raise RuntimeProfileError("admission frame exposes forbidden locator authority")
    return AdmissionFrame(raw, sha256_bytes(raw), actual_verifier_pid, evidence.sha256)

