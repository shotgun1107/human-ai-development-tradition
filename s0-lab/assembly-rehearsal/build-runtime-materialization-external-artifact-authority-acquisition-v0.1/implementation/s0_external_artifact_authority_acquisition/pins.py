"""Closed primitive pin authority for candidate v0.1."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, TypeAlias

from .canonical import require_exact_int, require_exact_text, require_https_url, require_sha256
from .errors import AuthorityError


MAX_METADATA_BYTES: Final = 1024 * 1024
MAX_WHEEL_AGGREGATE_BYTES: Final = 1024 * 1024
CPYTHON_SIGSTORE_MEDIA_TYPE: Final = (
    "application/vnd.dev.sigstore.bundle.v0.3+json"
)
CPYTHON_SIGSTORE_POLICY_IDENTITY: Final = "thomas@python.org"
CPYTHON_SIGSTORE_OIDC_ISSUER: Final = "https://accounts.google.com"
AUTHENTICODE_IMPLEMENTATION_MANIFEST_SHA256: Final = (
    "ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c"
)


@dataclass(frozen=True, slots=True)
class SourcePin:
    source_id: str
    url: str
    sha256: str
    size: int
    max_size: int


@dataclass(frozen=True, slots=True)
class ArtifactPin:
    artifact_id: str
    filename: str
    url: str
    sha256: str
    size: int
    max_size: int
    authority_state: str


@dataclass(frozen=True, slots=True)
class WheelPin:
    pin_id: str
    project: str
    version: str
    filename: str
    url: str
    sha256: str
    size: int
    metadata_source_id: str
    requires_python: str
    tag: str
    dist_info_dir: str
    requires_dist: tuple[str, ...]
    wheel_requires_dist: tuple[str, ...]
    purelib: bool


SourceSnapshot: TypeAlias = tuple[str, str, str, int, int]
ArtifactSnapshot: TypeAlias = tuple[str, str, str, str, int, int, str]
WheelSnapshot: TypeAlias = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    int,
    str,
    str,
    str,
    str,
    tuple[str, ...],
    tuple[str, ...],
    bool,
]


_SOURCE_ROWS: Final[tuple[SourceSnapshot, ...]] = (
    (
        "cpython-3.12.10-release-page",
        "https://www.python.org/downloads/release/python-31210/",
        "cc64f3159f7cbe565abe8b032439668b3cdbcd1768b1a08f7c7c79bcab881473",
        9943,
        MAX_METADATA_BYTES,
    ),
    (
        "cpython-3.12.10-ftp-index",
        "https://www.python.org/ftp/python/3.12.10/",
        "e6f937dbe22df020bcf8f2f3b251da05f0e4c9cdd4ceeea58b27cd528a562e58",
        8974,
        MAX_METADATA_BYTES,
    ),
    (
        "cpython-3.12.10-embed-amd64-sigstore-bundle",
        "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip.sigstore",
        "8aa5b4e555fd8b73b3dfef2f04328739f52d30706655930dcdf6111603d015be",
        4915,
        MAX_METADATA_BYTES,
    ),
    (
        "microsoft-vs-2022-release-history-17.14.39",
        "https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history",
        "8ead78ae6b47e27b40beb10d387e038719703c2b8c194840ec7eeaad2b970401",
        287876,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-jsonschema-4.26.0",
        "https://pypi.org/pypi/jsonschema/4.26.0/json",
        "d0c9ccdfa30c3cdc57b048c2be21123dfb0c2f4d6bef2e8324dcb4eac985cfcf",
        9468,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-attrs-26.1.0",
        "https://pypi.org/pypi/attrs/26.1.0/json",
        "a882bf941fb4a0bb748d0194df544121cc130f5fb15a710ab6b804c17d2899b7",
        11038,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-jsonschema-specifications-2025.9.1",
        "https://pypi.org/pypi/jsonschema-specifications/2025.9.1/json",
        "91810d8f79384375ad0c0cf631e06903e2790b030d3fad2f1ad657b20ddd839e",
        5037,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-referencing-0.37.0",
        "https://pypi.org/pypi/referencing/0.37.0/json",
        "a67968d8e03aa45e650fc2ff0d07796676db1a7841ce8e810bf2dba5af689464",
        4842,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-rpds-py-2026.6.3",
        "https://pypi.org/pypi/rpds-py/2026.6.3/json",
        "fff1fa33d84392d5684f0c1a40fc23f0a2027113c966498a1f64614bc83b02c2",
        106094,
        MAX_METADATA_BYTES,
    ),
    (
        "pypi-json-typing-extensions-4.16.0",
        "https://pypi.org/pypi/typing-extensions/4.16.0/json",
        "2140da00d62dde967f52d0be0ae28444f1d6a3fe603f52c83c23988c32122d5a",
        5631,
        MAX_METADATA_BYTES,
    ),
)


CPYTHON_ARTIFACT_ID: Final = "cpython-3.12.10-embed-amd64"
BUILDTOOLS_ARTIFACT_ID: Final = "vs-build-tools-17.14.39-17.14.37614.0"

_ARTIFACT_ROWS: Final[tuple[ArtifactSnapshot, ...]] = (
    (
        CPYTHON_ARTIFACT_ID,
        "python-3.12.10-embed-amd64.zip",
        "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip",
        "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
        11133606,
        11133606,
        "PINNED-SOURCE-INPUT",
    ),
    (
        BUILDTOOLS_ARTIFACT_ID,
        "vs_BuildTools.exe",
        "https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe",
        "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29",
        4473936,
        4473936,
        "EXPECTED-PROPOSAL-ONLY",
    ),
)


_JSONSCHEMA_REQUIRES_DIST: Final = (
    "attrs>=22.2.0",
    "jsonschema-specifications>=2023.03.6",
    "referencing>=0.28.4",
    "rpds-py>=0.25.0",
    'fqdn; extra == "format"',
    'idna; extra == "format"',
    'isoduration; extra == "format"',
    'jsonpointer>1.13; extra == "format"',
    'rfc3339-validator; extra == "format"',
    'rfc3987; extra == "format"',
    'uri-template; extra == "format"',
    'webcolors>=1.11; extra == "format"',
    'fqdn; extra == "format-nongpl"',
    'idna; extra == "format-nongpl"',
    'isoduration; extra == "format-nongpl"',
    'jsonpointer>1.13; extra == "format-nongpl"',
    'rfc3339-validator; extra == "format-nongpl"',
    'rfc3986-validator>0.1.0; extra == "format-nongpl"',
    'rfc3987-syntax>=1.1.0; extra == "format-nongpl"',
    'uri-template; extra == "format-nongpl"',
    'webcolors>=24.6.0; extra == "format-nongpl"',
)

_JSONSCHEMA_WHEEL_REQUIRES_DIST: Final = tuple(
    item if index < 4 else item.replace('"', "'")
    for index, item in enumerate(_JSONSCHEMA_REQUIRES_DIST)
)

_REFERENCING_REQUIRES_DIST: Final = (
    "attrs>=22.2.0",
    "rpds-py>=0.7.0",
    'typing-extensions>=4.4.0; python_version < "3.13"',
)

_REFERENCING_WHEEL_REQUIRES_DIST: Final = (
    "attrs>=22.2.0",
    "rpds-py>=0.7.0",
    "typing-extensions>=4.4.0; python_version < '3.13'",
)

_WHEEL_ROWS: Final[tuple[WheelSnapshot, ...]] = (
    (
        "jsonschema-4.26.0-py3-none-any",
        "jsonschema",
        "4.26.0",
        "jsonschema-4.26.0-py3-none-any.whl",
        "https://files.pythonhosted.org/packages/69/90/f63fb5873511e014207a475e2bb4e8b2e570d655b00ac19a9a0ca0a385ee/jsonschema-4.26.0-py3-none-any.whl",
        "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
        90630,
        "pypi-json-jsonschema-4.26.0",
        ">=3.10",
        "py3-none-any",
        "jsonschema-4.26.0.dist-info",
        _JSONSCHEMA_REQUIRES_DIST,
        _JSONSCHEMA_WHEEL_REQUIRES_DIST,
        True,
    ),
    (
        "attrs-26.1.0-py3-none-any",
        "attrs",
        "26.1.0",
        "attrs-26.1.0-py3-none-any.whl",
        "https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl",
        "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309",
        67548,
        "pypi-json-attrs-26.1.0",
        ">=3.9",
        "py3-none-any",
        "attrs-26.1.0.dist-info",
        (),
        (),
        True,
    ),
    (
        "jsonschema-specifications-2025.9.1-py3-none-any",
        "jsonschema-specifications",
        "2025.9.1",
        "jsonschema_specifications-2025.9.1-py3-none-any.whl",
        "https://files.pythonhosted.org/packages/41/45/1a4ed80516f02155c51f51e8cedb3c1902296743db0bbc66608a0db2814f/jsonschema_specifications-2025.9.1-py3-none-any.whl",
        "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe",
        18437,
        "pypi-json-jsonschema-specifications-2025.9.1",
        ">=3.9",
        "py3-none-any",
        "jsonschema_specifications-2025.9.1.dist-info",
        ("referencing>=0.31.0",),
        ("referencing>=0.31.0",),
        True,
    ),
    (
        "referencing-0.37.0-py3-none-any",
        "referencing",
        "0.37.0",
        "referencing-0.37.0-py3-none-any.whl",
        "https://files.pythonhosted.org/packages/2c/58/ca301544e1fa93ed4f80d724bf5b194f6e4b945841c5bfd555878eea9fcb/referencing-0.37.0-py3-none-any.whl",
        "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231",
        26766,
        "pypi-json-referencing-0.37.0",
        ">=3.10",
        "py3-none-any",
        "referencing-0.37.0.dist-info",
        _REFERENCING_REQUIRES_DIST,
        _REFERENCING_WHEEL_REQUIRES_DIST,
        True,
    ),
    (
        "rpds-py-2026.6.3-cp312-cp312-win_amd64",
        "rpds-py",
        "2026.6.3",
        "rpds_py-2026.6.3-cp312-cp312-win_amd64.whl",
        "https://files.pythonhosted.org/packages/04/3a/f0ee4d4dde9d3b69dedf1b5f74e7a40017046d55052d173e418c6a94f960/rpds_py-2026.6.3-cp312-cp312-win_amd64.whl",
        "2c958bf94822e9290a40aaf2a822d4bc5c88099093e3948ad6c571eca9272e5f",
        220394,
        "pypi-json-rpds-py-2026.6.3",
        ">=3.11",
        "cp312-cp312-win_amd64",
        "rpds_py-2026.6.3.dist-info",
        (),
        (),
        False,
    ),
    (
        "typing-extensions-4.16.0-py3-none-any",
        "typing-extensions",
        "4.16.0",
        "typing_extensions-4.16.0-py3-none-any.whl",
        "https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl",
        "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8",
        45571,
        "pypi-json-typing-extensions-4.16.0",
        ">=3.9",
        "py3-none-any",
        "typing_extensions-4.16.0.dist-info",
        (),
        (),
        True,
    ),
)


def _source_view(row: SourceSnapshot) -> SourcePin:
    return SourcePin(*row)


def _artifact_view(row: ArtifactSnapshot) -> ArtifactPin:
    return ArtifactPin(*row)


def _wheel_view(row: WheelSnapshot) -> WheelPin:
    return WheelPin(*row)


def _validate_source_row(row: SourceSnapshot) -> None:
    require_exact_text(row[0], label="source_id", maximum_length=160)
    require_https_url(row[1], label="source")
    require_sha256(row[2], label="source")
    require_exact_int(row[3], label="source_size", minimum=1, maximum=row[4])
    if row[4] != MAX_METADATA_BYTES:
        raise AuthorityError("source_max_size_invalid")


def _validate_artifact_row(row: ArtifactSnapshot) -> None:
    require_exact_text(row[0], label="artifact_id", maximum_length=160)
    filename = require_exact_text(row[1], label="artifact_filename", maximum_length=255)
    if filename in {".", ".."} or "/" in filename or "\\" in filename:
        raise AuthorityError("artifact_filename_invalid")
    require_https_url(row[2], label="artifact")
    require_sha256(row[3], label="artifact")
    require_exact_int(row[4], label="artifact_size", minimum=1, maximum=row[5])
    if row[4] != row[5] or row[6] not in {
        "PINNED-SOURCE-INPUT",
        "EXPECTED-PROPOSAL-ONLY",
    }:
        raise AuthorityError("artifact_authority_state_invalid")


def _validate_wheel_row(row: WheelSnapshot) -> None:
    for index, label in ((0, "wheel_pin_id"), (1, "wheel_project"), (2, "wheel_version")):
        require_exact_text(row[index], label=label, maximum_length=160)
    filename = require_exact_text(row[3], label="wheel_filename", maximum_length=255)
    if not filename.endswith(".whl") or "/" in filename or "\\" in filename:
        raise AuthorityError("wheel_filename_invalid")
    require_https_url(row[4], label="wheel")
    require_sha256(row[5], label="wheel")
    require_exact_int(row[6], label="wheel_size", minimum=1, maximum=MAX_WHEEL_AGGREGATE_BYTES)
    for index, label in (
        (7, "wheel_metadata_source"),
        (8, "wheel_requires_python"),
        (9, "wheel_tag"),
        (10, "wheel_dist_info"),
    ):
        require_exact_text(row[index], label=label, maximum_length=255)
    if type(row[11]) is not tuple or any(type(item) is not str for item in row[11]):
        raise AuthorityError("wheel_requires_dist_invalid")
    if type(row[12]) is not tuple or any(type(item) is not str for item in row[12]):
        raise AuthorityError("wheel_metadata_requires_dist_invalid")
    if type(row[13]) is not bool:
        raise AuthorityError("wheel_purelib_invalid")


def _freeze_authority(
    rows: tuple[tuple[object, ...], ...],
    *,
    view_type: type,
    make_view: Callable[[tuple[object, ...]], object],
    validate_row: Callable[[tuple[object, ...]], None],
    label: str,
) -> tuple[Mapping[str, object], Callable[[object], tuple[object, ...]]]:
    frozen_rows: dict[str, tuple[object, ...]] = {}
    for row in rows:
        if type(row) is not tuple:
            raise AuthorityError(f"{label}_authority_row_invalid")
        validate_row(row)
        row_id = row[0]
        if type(row_id) is not str or row_id in frozen_rows:
            raise AuthorityError(f"{label}_authority_id_invalid")
        frozen_rows[row_id] = row
    frozen = MappingProxyType(frozen_rows)
    views: Mapping[str, object] = MappingProxyType(
        {row_id: make_view(row) for row_id, row in frozen.items()}
    )
    captured_type = view_type

    def resolve(value: object) -> tuple[object, ...]:
        if type(value) is str:
            row = frozen.get(value)
            if row is None:
                raise AuthorityError(f"{label}_pin_unknown")
            return row
        if type(value) is not captured_type:
            raise AuthorityError(f"{label}_pin_type_invalid")
        supplied = tuple(getattr(value, field) for field in value.__dataclass_fields__)
        row = frozen.get(supplied[0])
        if row is None or supplied != row:
            raise AuthorityError(f"{label}_pin_not_frozen_row")
        return row

    return views, resolve


SOURCE_PINS, resolve_source_snapshot = _freeze_authority(
    _SOURCE_ROWS,
    view_type=SourcePin,
    make_view=_source_view,
    validate_row=_validate_source_row,
    label="source",
)
ARTIFACT_PINS, resolve_artifact_snapshot = _freeze_authority(
    _ARTIFACT_ROWS,
    view_type=ArtifactPin,
    make_view=_artifact_view,
    validate_row=_validate_artifact_row,
    label="artifact",
)
WHEEL_PINS, resolve_wheel_snapshot = _freeze_authority(
    _WHEEL_ROWS,
    view_type=WheelPin,
    make_view=_wheel_view,
    validate_row=_validate_wheel_row,
    label="wheel",
)

SOURCE_PINS = SOURCE_PINS
ARTIFACT_PINS = ARTIFACT_PINS
WHEEL_PINS = WHEEL_PINS
del _freeze_authority


WHEEL_PIN_IDS: Final = tuple(row[0] for row in _WHEEL_ROWS)
PYPI_METADATA_SOURCE_IDS: Final = tuple(row[7] for row in _WHEEL_ROWS)
PYPI_JSON_REQUIRES_DIST_INVENTORY: Final = tuple(
    (row[0], row[11]) for row in _WHEEL_ROWS
)
WHEEL_METADATA_REQUIRES_DIST_INVENTORY: Final = tuple(
    (row[0], row[12]) for row in _WHEEL_ROWS
)
JSONSCHEMA_DEPENDENCY_GRAPH: Final = (
    (
        "jsonschema-4.26.0-py3-none-any",
        (
            "attrs-26.1.0-py3-none-any",
            "jsonschema-specifications-2025.9.1-py3-none-any",
            "referencing-0.37.0-py3-none-any",
            "rpds-py-2026.6.3-cp312-cp312-win_amd64",
        ),
    ),
    (
        "jsonschema-specifications-2025.9.1-py3-none-any",
        ("referencing-0.37.0-py3-none-any",),
    ),
    (
        "referencing-0.37.0-py3-none-any",
        (
            "attrs-26.1.0-py3-none-any",
            "rpds-py-2026.6.3-cp312-cp312-win_amd64",
            "typing-extensions-4.16.0-py3-none-any",
        ),
    ),
    ("attrs-26.1.0-py3-none-any", ()),
    ("rpds-py-2026.6.3-cp312-cp312-win_amd64", ()),
    ("typing-extensions-4.16.0-py3-none-any", ()),
)


__all__ = [
    "ARTIFACT_PINS",
    "AUTHENTICODE_IMPLEMENTATION_MANIFEST_SHA256",
    "ArtifactPin",
    "ArtifactSnapshot",
    "BUILDTOOLS_ARTIFACT_ID",
    "CPYTHON_ARTIFACT_ID",
    "CPYTHON_SIGSTORE_MEDIA_TYPE",
    "CPYTHON_SIGSTORE_OIDC_ISSUER",
    "CPYTHON_SIGSTORE_POLICY_IDENTITY",
    "JSONSCHEMA_DEPENDENCY_GRAPH",
    "MAX_METADATA_BYTES",
    "MAX_WHEEL_AGGREGATE_BYTES",
    "PYPI_METADATA_SOURCE_IDS",
    "PYPI_JSON_REQUIRES_DIST_INVENTORY",
    "SOURCE_PINS",
    "SourcePin",
    "SourceSnapshot",
    "WHEEL_PINS",
    "WHEEL_METADATA_REQUIRES_DIST_INVENTORY",
    "WHEEL_PIN_IDS",
    "WheelPin",
    "WheelSnapshot",
    "resolve_artifact_snapshot",
    "resolve_source_snapshot",
    "resolve_wheel_snapshot",
]
