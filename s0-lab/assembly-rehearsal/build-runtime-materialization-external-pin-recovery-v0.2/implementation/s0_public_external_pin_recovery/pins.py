"""Closed external-artifact pin authority for implementation v0.2."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, TypeAlias

from .errors import AuthorityError


FALLBACK_MAX_SIZE: Final = 24 * 1024 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ArtifactPin:
    """A validated compatibility view of one external-artifact row.

    Frozen dataclasses can be altered through low-level Python mutation, so
    instances of this class never carry authority.  Authority consumers use
    closure-held tuples of exact immutable primitives instead.
    """

    pin_id: str
    filename: str
    url: str | None
    expected_sha256: str | None
    expected_size: int | None
    max_size: int

    def __post_init__(self) -> None:
        if type(self.pin_id) is not str or not self.pin_id:
            raise TypeError("pin_id must be a non-empty exact string")
        if type(self.filename) is not str or not self.filename:
            raise TypeError("filename must be a non-empty exact string")
        if "/" in self.filename or "\\" in self.filename or self.filename in {".", ".."}:
            raise ValueError("filename must be a single path component")
        if self.url is not None and type(self.url) is not str:
            raise TypeError("url must be an exact string or None")
        if self.url == "":
            raise ValueError("url must not be empty")
        if self.expected_sha256 is not None:
            if type(self.expected_sha256) is not str:
                raise TypeError("expected_sha256 must be an exact string or None")
            if len(self.expected_sha256) != 64 or any(
                character not in "0123456789abcdef"
                for character in self.expected_sha256
            ):
                raise ValueError("expected_sha256 must be 64 lowercase hexadecimal characters")
        if self.expected_size is not None and (
            type(self.expected_size) is not int or self.expected_size <= 0
        ):
            raise ValueError("expected_size must be a positive exact integer or None")
        if type(self.max_size) is not int or self.max_size <= 0:
            raise ValueError("max_size must be a positive exact integer")
        required_max_size = (
            self.expected_size
            if self.expected_size is not None
            else FALLBACK_MAX_SIZE
        )
        if self.max_size != required_max_size:
            raise ValueError(
                "max_size must equal expected_size, or the 24 GiB fallback when size is absent"
            )


VS_BUILD_TOOLS_RELEASE: Final = "17.14.39"
VS_BUILD_TOOLS_BUILD: Final = "17.14.37614.0"
VS_BUILD_TOOLS_ARTIFACT: Final = "vs_BuildTools.exe"
VS_BUILD_TOOLS_URL: Final = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
    "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
    "vs_BuildTools.exe"
)
VS_BUILD_TOOLS_SHA256: Final[None] = None
VS_BUILD_TOOLS_SIZE: Final[None] = None
VS_BUILD_TOOLS_PIN_ID: Final = "vs-build-tools-17.14.39-17.14.37614.0"
VS_BUILD_TOOLS_WORKLOAD: Final = "Microsoft.VisualStudio.Workload.VCTools"
VS_BUILD_TOOLS_COMPONENTS: Final = (
    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
    "Microsoft.VisualStudio.Component.Windows11SDK.26100",
)
VS_BUILD_TOOLS_PIN: Final = ArtifactPin(
    pin_id=VS_BUILD_TOOLS_PIN_ID,
    filename=VS_BUILD_TOOLS_ARTIFACT,
    url=VS_BUILD_TOOLS_URL,
    expected_sha256=VS_BUILD_TOOLS_SHA256,
    expected_size=VS_BUILD_TOOLS_SIZE,
    max_size=FALLBACK_MAX_SIZE,
)

CPYTHON_ARTIFACT: Final = "python-3.12.10-embed-amd64.zip"
CPYTHON_URL: Final = (
    "https://www.python.org/ftp/python/3.12.10/"
    "python-3.12.10-embed-amd64.zip"
)
CPYTHON_SHA256: Final = (
    "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3"
)
CPYTHON_SIZE: Final[None] = None
CPYTHON_PIN_ID: Final = "cpython-3.12.10-embed-amd64"
CPYTHON_PIN: Final = ArtifactPin(
    pin_id=CPYTHON_PIN_ID,
    filename=CPYTHON_ARTIFACT,
    url=CPYTHON_URL,
    expected_sha256=CPYTHON_SHA256,
    expected_size=CPYTHON_SIZE,
    max_size=FALLBACK_MAX_SIZE,
)

JSONSCHEMA_ARTIFACT: Final = "jsonschema-4.26.0-py3-none-any.whl"
JSONSCHEMA_URL: Final[None] = None
JSONSCHEMA_SHA256: Final = (
    "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce"
)
JSONSCHEMA_SIZE: Final = 90630
JSONSCHEMA_PIN_ID: Final = "jsonschema-4.26.0-py3-none-any"
JSONSCHEMA_PIN: Final = ArtifactPin(
    pin_id=JSONSCHEMA_PIN_ID,
    filename=JSONSCHEMA_ARTIFACT,
    url=JSONSCHEMA_URL,
    expected_sha256=JSONSCHEMA_SHA256,
    expected_size=JSONSCHEMA_SIZE,
    max_size=JSONSCHEMA_SIZE,
)

VERIFIER_MANIFEST_SHA256: Final = (
    "ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c"
)


PinSnapshot: TypeAlias = tuple[str, str, str | None, str | None, int | None, int]


def _snapshot_exact_pin(pin: ArtifactPin) -> PinSnapshot:
    """Read every authority field exactly once into immutable built-ins."""

    return (
        pin.pin_id,
        pin.filename,
        pin.url,
        pin.expected_sha256,
        pin.expected_size,
        pin.max_size,
    )


_PIN_SNAPSHOTS: Final[tuple[PinSnapshot, ...]] = (
    (
        VS_BUILD_TOOLS_PIN_ID,
        VS_BUILD_TOOLS_ARTIFACT,
        VS_BUILD_TOOLS_URL,
        VS_BUILD_TOOLS_SHA256,
        VS_BUILD_TOOLS_SIZE,
        FALLBACK_MAX_SIZE,
    ),
    (
        CPYTHON_PIN_ID,
        CPYTHON_ARTIFACT,
        CPYTHON_URL,
        CPYTHON_SHA256,
        CPYTHON_SIZE,
        FALLBACK_MAX_SIZE,
    ),
    (
        JSONSCHEMA_PIN_ID,
        JSONSCHEMA_ARTIFACT,
        JSONSCHEMA_URL,
        JSONSCHEMA_SHA256,
        JSONSCHEMA_SIZE,
        JSONSCHEMA_SIZE,
    ),
)


def _freeze_pin_authority(
    snapshots: tuple[PinSnapshot, ...],
) -> tuple[
    Mapping[str, ArtifactPin],
    Callable[[str | ArtifactPin], ArtifactPin],
    Callable[[str | ArtifactPin], PinSnapshot],
]:
    approved_snapshots: Mapping[str, PinSnapshot] = MappingProxyType(
        {snapshot[0]: snapshot for snapshot in snapshots}
    )
    artifact_pin_type = ArtifactPin
    authority_error_type = AuthorityError
    snapshot_pin = _snapshot_exact_pin

    def make_view(snapshot: PinSnapshot) -> ArtifactPin:
        return artifact_pin_type(
            pin_id=snapshot[0],
            filename=snapshot[1],
            url=snapshot[2],
            expected_sha256=snapshot[3],
            expected_size=snapshot[4],
            max_size=snapshot[5],
        )

    approved_pins: Mapping[str, ArtifactPin] = MappingProxyType(
        {pin_id: make_view(snapshot) for pin_id, snapshot in approved_snapshots.items()}
    )

    def resolve_snapshot(pin: str | ArtifactPin) -> PinSnapshot:
        """Return only a closure-held tuple of exact immutable primitives."""

        if type(pin) is str:
            frozen = approved_snapshots.get(pin)
            if frozen is None:
                raise authority_error_type("unknown external-artifact pin ID")
            return frozen

        if type(pin) is not artifact_pin_type:
            raise authority_error_type(
                "pin must be an exact built-in ID or exact ArtifactPin"
            )

        supplied = snapshot_pin(pin)
        frozen = approved_snapshots.get(supplied[0])
        if frozen is None or supplied != frozen:
            raise authority_error_type(
                "ArtifactPin does not equal its frozen authority row"
            )
        return frozen

    def resolve_approved_pin(pin: str | ArtifactPin) -> ArtifactPin:
        """Return a fresh compatibility view of one frozen authority row.

        The returned object is not authority and is never retained by a trusted
        consumer.  Exact type and full-row equality checks reject subclasses,
        proxies, mutated exports, and caller-selected fields.
        """

        return make_view(resolve_snapshot(pin))

    return approved_pins, resolve_approved_pin, resolve_snapshot


(
    APPROVED_PINS,
    resolve_approved_pin,
    _resolve_approved_pin_snapshot,
) = _freeze_pin_authority(_PIN_SNAPSHOTS)
del _freeze_pin_authority
