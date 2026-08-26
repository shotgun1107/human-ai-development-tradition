"""Immutable public pins used by the external-pin recovery workflow."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArtifactPin:
    """A frozen description of one externally acquired artifact."""

    filename: str
    url: str | None
    sha256: str | None
    size: int | None
    authenticated: bool

    @property
    def name(self) -> str:
        """Compatibility name for acquisition evidence."""

        return self.filename

    @property
    def expected_size(self) -> int | None:
        """Compatibility spelling for the exact pinned size."""

        return self.size

    @property
    def expected_sha256(self) -> str | None:
        """Compatibility spelling for the exact pinned digest."""

        return self.sha256

    @property
    def max_size(self) -> int:
        """Return the exact size or the hard ceiling for an unknown size."""

        if self.size is not None:
            return self.size
        return 24 * 1024 * 1024 * 1024


VS_BUILD_TOOLS_RELEASE = "17.14.39"
VS_BUILD_TOOLS_BUILD = "17.14.37614.0"
VS_BUILD_TOOLS_ARTIFACT = "vs_BuildTools.exe"
VS_BUILD_TOOLS_URL = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
    "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
    "vs_BuildTools.exe"
)
VS_BUILD_TOOLS_SHA256: None = None
VS_BUILD_TOOLS_SIZE: None = None
VS_BUILD_TOOLS_AUTHENTICATED = False
VS_BUILD_TOOLS_WORKLOAD = "Microsoft.VisualStudio.Workload.VCTools"
VS_BUILD_TOOLS_COMPONENTS = (
    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
    "Microsoft.VisualStudio.Component.Windows11SDK.26100",
)
VS_BUILD_TOOLS_PIN = ArtifactPin(
    filename=VS_BUILD_TOOLS_ARTIFACT,
    url=VS_BUILD_TOOLS_URL,
    sha256=VS_BUILD_TOOLS_SHA256,
    size=VS_BUILD_TOOLS_SIZE,
    authenticated=VS_BUILD_TOOLS_AUTHENTICATED,
)

CPYTHON_ARTIFACT = "python-3.12.10-embed-amd64.zip"
CPYTHON_URL = (
    "https://www.python.org/ftp/python/3.12.10/"
    "python-3.12.10-embed-amd64.zip"
)
CPYTHON_SHA256 = "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3"
CPYTHON_SIZE: None = None
CPYTHON_AUTHENTICATED = True
CPYTHON_PIN = ArtifactPin(
    filename=CPYTHON_ARTIFACT,
    url=CPYTHON_URL,
    sha256=CPYTHON_SHA256,
    size=CPYTHON_SIZE,
    authenticated=CPYTHON_AUTHENTICATED,
)

JSONSCHEMA_ARTIFACT = "jsonschema-4.26.0-py3-none-any.whl"
JSONSCHEMA_URL: None = None
JSONSCHEMA_SHA256 = (
    "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce"
)
JSONSCHEMA_SIZE = 90630
JSONSCHEMA_AUTHENTICATED = True
JSONSCHEMA_PIN = ArtifactPin(
    filename=JSONSCHEMA_ARTIFACT,
    url=JSONSCHEMA_URL,
    sha256=JSONSCHEMA_SHA256,
    size=JSONSCHEMA_SIZE,
    authenticated=JSONSCHEMA_AUTHENTICATED,
)

VERIFIER_MANIFEST_SHA256 = (
    "ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c"
)
