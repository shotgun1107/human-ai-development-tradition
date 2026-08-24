# S0 v0.14 public build/runtime external-pin bundle recovery plan v0.1

## 1. Purpose

This package records a company-side recovery selection for the ten external
pin classes already frozen by the authenticated build/runtime materialization
design. It does not recreate, overwrite, or claim equivalence to any
unpublished home-PC bytes.

The recovery base is exact `main` commit
`39263f431a82649ddc0bbd3545ed6d95b0780adc` with tree
`6697b497565ddde92dffc6b9eb8ee528ea4a2e83`.

The package is a PUBLIC selection and acquisition plan only. No artifact was
downloaded, installed, compiled, linked, inspected, materialized, loaded, or
executed while producing it.

## 2. Authenticated predecessor authority

The following predecessor identities were recomputed from the synchronized
Git tree:

- v0.5 design-package manifest SHA-256:
  `ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c`;
- approving v0.5 design review SHA-256:
  `5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`;
- v0.5 design CONTROL decision SHA-256:
  `d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`;
- v0.6 implementation manifest SHA-256:
  `c653931163e1818fe17b0f53b7d7e6d9e843cde3eea8752b952c8b30dd796798`;
- v0.6 independent review SHA-256:
  `821dc552b91efe1e7590b449e5e407b58ea9989590ac7149526e926c45a8f263`;
  and
- v0.6 main-integration decision SHA-256:
  `d9292c9dd495afebdc6a7fc2b648acef31be0de5f4be418e232c503fa16e33c8`.

The effective predecessor remains `BLOCKED-MISSING-EXTERNAL-PIN`. Its design
defines eight manifest identities plus the canonical build profile and
approving review as ten external pin classes.

## 3. Company recovery observations

The company environment was inspected without installation or build action.

- Windows AMD64 is present.
- A Windows SDK root is present, but it is not an authenticated platform or
  toolchain manifest.
- A Python command is present, but the command wrapper and ambient installation
  are not accepted as the CPython distribution pin.
- Visual Studio 2022 Build Tools, MSVC `cl`, `link`, `msbuild`, `dumpbin`,
  CMake, and Ninja were not available through the inspected command surface.
- `jsonschema` 4.26.0 was not installed in the inspected interpreter.
- no tracked external-pin-named file exists in the synchronized repository.

These are availability observations, not authority evidence.

## 4. Recovery selection

### 4.1 Toolchain

The selected acquisition candidate is fixed Visual Studio Build Tools 2022
17.14.39, build `17.14.37614.0`, not an evergreen bootstrapper. The selected
scope is:

- workload `Microsoft.VisualStudio.Workload.VCTools`;
- component `Microsoft.VisualStudio.Component.VC.Tools.x86.x64`;
- component `Microsoft.VisualStudio.Component.Windows11SDK.26100`; and
- language `en-US`.

The official release history identifies 17.14.39 as the August 18, 2026 fixed
Current-channel release. Microsoft documents 17.14 as supported through
January 2032. Microsoft also documents `--layout`, component-limited offline
acquisition, and `--noWeb` installation.

No bootstrapper or layout byte is trusted until its download byte, fixed
product version, complete layout inventory, and exact target hashes are
captured. The layout must fit the inherited 24 GiB toolchain-bundle ceiling.
An oversized layout requires a reviewed design change; it must not be silently
accepted.

### 4.2 CPython

The selected distribution candidate is the official CPython 3.12.10 Windows
AMD64 embeddable package:

- artifact: `python-3.12.10-embed-amd64.zip`;
- official SPDX SHA-256:
  `4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3`;
- release page:
  `https://www.python.org/downloads/release/python-31210/`; and
- artifact URL:
  `https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip`.

Selection does not authenticate an extracted distribution. A later acquisition
step must verify the zip hash, reject aliases and extra files, extract to a new
empty root, and create an exact target manifest before any import or process.

### 4.3 Python dependency root

The selected root is the PyPI `jsonschema` 4.26.0 universal wheel:

- artifact: `jsonschema-4.26.0-py3-none-any.whl`;
- SHA-256:
  `d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce`;
- size: 90,630 bytes; and
- metadata authority:
  `https://pypi.org/pypi/jsonschema/4.26.0/json`.

Its required dependency roots are `attrs`, `jsonschema-specifications`,
`referencing`, and `rpds-py`. The inherited repository dependency uses the
`format` extra, so every selected format dependency and transitive dependency
must also receive an exact version and artifact hash. The full dependency
closure is unresolved in v0.1 and remains nonauthority.

### 4.4 Source, platform, and runtime profile

The native source and materializer/inspector source do not exist as approved
recovery inputs. They require a separate source-authoring gate and independent
security review. Neither may be invented by a downloader or inferred from a
binary.

The Windows platform manifest must be authored from a separately approved
bounded observation procedure. Ambient OS version text or installed SDK
presence is not a pin.

The runtime-tree profile depends on every other source, toolchain, CPython,
dependency, and platform closure. It remains unselected until those closures
are exact.

## 5. Ten-class recovery status

| Class | Status |
|---|---|
| native source | missing; source authoring required |
| materializer and inspector source | missing; source authoring required |
| offline toolchain bundle | fixed candidate selected; not downloaded |
| compiler/linker/SDK/headers/libraries/CRT | components selected; not downloaded |
| CPython distribution | official artifact selected; not downloaded |
| Python dependencies | root selected; transitive closure unresolved |
| Windows platform | local observation only; manifest missing |
| canonical build profile | present in authenticated design closure |
| runtime-tree profile | blocked on all prior closures |
| approving review | present and authenticated |

Complete manifest identities available now: 0 / 8 external manifest classes.
Predecessor nonmanifest authorities available now: 2 / 2.

## 6. Next bounded action

The next safe action is acquisition planning, not build execution. It must:

1. obtain the fixed Build Tools bootstrapper and create a component-limited
   offline layout in a fresh out-of-repository directory;
2. obtain the exact CPython zip, SPDX, and Sigstore material;
3. resolve and download the exact Python wheel closure without installation;
4. verify all downloaded bytes and reduce each closed directory to a canonical
   manifest identity; and
5. stop before compiler invocation, source authoring, installation, or runtime
   materialization.

Acquisition writes potentially many gigabytes outside the repository and uses
the network. It requires explicit user approval after this plan is reviewed.

## 7. Nonclaims

This recovery package is not an external pin bundle. It is not proof of a
toolchain, source, compiler, Python distribution, dependency closure, Windows
platform, runtime tree, build, binary, materialization, native behavior,
rehearsal, S0, central system, or Project Brain.

F0 content was not accessed. No secret, credential, customer, personal, or
home-PC local byte is included.
