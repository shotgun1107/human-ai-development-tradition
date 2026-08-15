# S0 public build/runtime materialization implementation candidate v0.2

This directory contains the bounded PUBLIC v0.2 revision of the
CONTROL-integrated build/runtime materialization candidate. It repairs the
one blocking and four major findings in the authenticated v0.1 implementation
review without opening any build, materialization, native, process, network,
provider, rehearsal, S0, or E0 gate.

The candidate implements:

- exact v0.1-v0.5 design-manifest and target authentication;
- full file-closure reauthentication at every semantic authority transition;
- byte-derived, canonical diagnostics whose public fields cannot diverge from
  their raw record;
- a recursively immutable 20-field publication policy and mutation rows;
- exact runtime-row types, fixed 20,000-file and 2-GiB ceilings, Windows-case
  denied-prefix handling, and file/directory prefix-collision rejection;
- one non-executing DLL-resolution plan binding every DLL name, path, hash,
  parent, Windows identity, identity digest, and directory index;
- target-set and semantic-relation codecs;
- an in-memory record diagnostic that explicitly reports filesystem close and
  readback observations as unavailable; and
- an authenticated-snapshot verifier with PUBLIC synthetic hostile tests.

The schema adapter is now unconditionally fail-closed. It imports neither
`jsonschema` nor `referencing` and cannot validate caller-selected schemas.
Schema validation remains `BLOCKED-MISSING-EXTERNAL-PIN` until a later gate
supplies and authenticates the exact dependency and schema authority closure.

The intended entry point still terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`. It has no caller-selected toolchain, CPython,
dependency, Windows-platform, build-profile, or runtime-tree pin surface. It
cannot compile, build, create a runtime tree, call a native API, launch a
candidate process, access a network or provider, run a rehearsal, or execute
S0/E0.

The implementation manifest is externally pinned by SHA-256. The verifier
authenticates its ten targets, the five design-package closures, the approving
design review, the CONTROL decision, and the v0.1 implementation review before
copying authenticated bytes into a temporary snapshot. Its child Python
process runs unit tests only; candidate code creates no process or filesystem
object.

This is PUBLIC construction evidence for a non-executing prerequisite layer.
It is not build, binary, runtime, Windows, rehearsal, or S0 evidence.
