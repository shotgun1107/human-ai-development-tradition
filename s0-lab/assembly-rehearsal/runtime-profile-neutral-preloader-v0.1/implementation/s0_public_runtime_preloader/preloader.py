"""Offline neutral-preloader plan construction; no native API is reachable."""

from __future__ import annotations

from dataclasses import dataclass

from .errors import PlatformGateClosed, RuntimeProfileError
from .evidence import LaunchEvidence, LaunchIdentity, build_launch_evidence
from .profile import AuthenticatedRuntimeProfile, is_authenticated_runtime_profile
from .semantic import HandleBinding


@dataclass(frozen=True)
class OrderedHandleLocators:
    admission_read: str
    commit_request_write: str
    commit_reply_read: str
    output_root: str
    preloader_process: str

    def ordered(self) -> tuple[str, str, str, str, str]:
        return (
            self.admission_read,
            self.commit_request_write,
            self.commit_reply_read,
            self.output_root,
            self.preloader_process,
        )


@dataclass(frozen=True)
class PreloaderInputs:
    application_path: str
    command_line: str
    environment_block: tuple[str, ...]
    current_directory: str
    handle_locators: OrderedHandleLocators
    identity: LaunchIdentity

    def __post_init__(self) -> None:
        for value in (self.application_path, self.command_line, self.current_directory):
            if type(value) is not str or not value or "\x00" in value:
                raise RuntimeProfileError("preloader string input is malformed")
        if type(self.environment_block) is not tuple or any(
            type(item) is not str or "=" not in item or "\x00" in item
            for item in self.environment_block
        ):
            raise RuntimeProfileError("environment block is not one exact tuple")
        if self.environment_block != tuple(sorted(set(self.environment_block))):
            raise RuntimeProfileError("environment block is not sorted and unique")
        if type(self.handle_locators) is not OrderedHandleLocators:
            raise RuntimeProfileError("preloader handle locator authority is not exact")


@dataclass(frozen=True)
class PreparedLaunch:
    api: str
    application_path: str
    command_line: str
    environment_block: tuple[str, ...]
    current_directory: str
    creation_flags_numeric: int
    startupinfoex_dwflags: int
    b_inherit_handles: bool
    attribute_count: int
    attribute_id_numeric: int
    ordered_handle_values: tuple[int, int, int, int, int]
    handle_array_bytes_x64: int
    evidence: LaunchEvidence
    runtime_profile_sha256: str

    def invoke_native_process_creation(self) -> None:
        """The real call is deliberately unavailable until a platform gate."""

        raise PlatformGateClosed("native process creation gate is closed")


class NeutralPreloader:
    """Construct the only exact v0.4 launch plan from authenticated authority."""

    __slots__ = ()

    def prepare(
        self,
        authority: AuthenticatedRuntimeProfile,
        inputs: PreloaderInputs,
    ) -> PreparedLaunch:
        if not is_authenticated_runtime_profile(authority):
            raise RuntimeProfileError("preloader requires exact runtime profile authority")
        if type(inputs) is not PreloaderInputs:
            raise RuntimeProfileError("preloader inputs are not exact")
        profile = authority.profile
        process = profile["process_creation_policy"]
        assert isinstance(process, dict) or hasattr(process, "__getitem__")
        handle_policy = process["ordered_handles"]
        locators = inputs.handle_locators.ordered()
        handles = tuple(
            HandleBinding(item["role"], item["kind"], item["access"], locator)
            for item, locator in zip(handle_policy, locators, strict=True)
        )
        evidence = build_launch_evidence(profile, inputs.identity, handles)
        values = tuple(int(item.locator[2:], 16) for item in handles)
        if len(values) != 5 or any(value <= 0 or value == 0xFFFFFFFFFFFFFFFF for value in values):
            raise RuntimeProfileError("preloader handle array is invalid")
        return PreparedLaunch(
            api=process["api"],
            application_path=inputs.application_path,
            command_line=inputs.command_line,
            environment_block=inputs.environment_block,
            current_directory=inputs.current_directory,
            creation_flags_numeric=int(process["creation_flags_numeric"], 16),
            startupinfoex_dwflags=process["startupinfoex_dwflags"],
            b_inherit_handles=process["b_inherit_handles"],
            attribute_count=process["attribute_count"],
            attribute_id_numeric=int(process["attribute_id_numeric"], 16),
            ordered_handle_values=values,  # type: ignore[arg-type]
            handle_array_bytes_x64=process["handle_array_bytes_x64"],
            evidence=evidence,
            runtime_profile_sha256=authority.profile_sha256,
        )
