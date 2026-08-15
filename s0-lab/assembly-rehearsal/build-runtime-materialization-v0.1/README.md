# S0 public build/runtime materialization implementation candidate v0.1

This directory contains a bounded PUBLIC implementation candidate for the
CONTROL-integrated build/runtime materialization design v0.5.

It implements:

- exact v0.1-v0.5 design-manifest and target authentication;
- authenticated v0.5 semantic-relation reconstruction;
- the sole 20-field publication no-replace policy JCS-plus-LF identity;
- effective 46 to 63 to 97 to 111 to 115 mutation-matrix composition;
- target-set, virtual-path, Windows directory identity, DLL-directory, runtime
  row, resource-limit, and diagnostic-record codecs;
- a Draft 2020-12 schema-registry adapter kept outside the runnable candidate
  path until its exact dependency closure is supplied; and
- an authenticated-snapshot verifier and PUBLIC synthetic tests.

The runnable candidate deliberately stops at
`BLOCKED-MISSING-EXTERNAL-PIN`. It has no API for caller-selected toolchain,
CPython, dependency, Windows-platform, build-profile, or runtime-tree pins.
It cannot compile, build, create a runtime tree, call a native API, launch a
candidate process, access a network or provider, run a rehearsal, or execute
S0/E0.

The implementation manifest is externally pinned by SHA-256. The verifier
authenticates its ten targets and the five design-package closures before
copying only authenticated bytes into a temporary snapshot. Its child Python
process runs unit tests only; the candidate itself creates no process and
performs no filesystem operation.

This is construction evidence for a PUBLIC non-executing prerequisite layer.
It is not build, binary, runtime, Windows, rehearsal, or S0 evidence.
