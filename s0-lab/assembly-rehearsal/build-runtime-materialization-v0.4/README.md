# S0 public build/runtime materialization implementation candidate v0.4

This directory contains the bounded PUBLIC v0.4 revision of the
CONTROL-integrated build/runtime materialization candidate. It addresses the
three major findings in the authenticated v0.3 implementation review without
opening any build, materialization, native, process, network, provider,
rehearsal, S0, or E0 gate.

The candidate implements:

- exact v0.1-v0.5 design-manifest and target authentication;
- stable authenticated snapshots at every semantic authority transition;
- exact-string, lowercase SHA-256 identity fields on the reconstructed
  `EffectiveDesign`, with caller comparison objects rejected;
- an `EffectiveDesign` that rederives and byte-compares all relations, the
  complete policy, all 115 mutation rows, and all twelve resource authorities;
- the exact eight-field runtime-row grammar and immutable runtime diagnostics;
- case-fold-independent runtime path prefix and denied-root checks;
- DLL directory identities computed from
  `windows_directory_identity_key=<ascii-lowercase-key>` plus one LF;
- application-directory-first DLL diagnostics whose remaining directories are
  sorted by identity key and whose rows/directories form one closed used set;
- exact-type, canonical JSON object diagnostics with byte-derived hashes; and
- authenticated-snapshot PUBLIC synthetic verification.

The runtime and DLL structural results remain diagnostics with
`authority_status=BLOCKED-MISSING-EXTERNAL-PIN`. They are not validated
materialization plans. The public `plan_runtime_tree`,
`derive_dll_directories`, and `plan_dll_resolution` entry points always
reject until an exact externally pinned runtime profile and DLL map are
authenticated by a later gate.

The schema adapter also remains unconditionally fail-closed and imports no
ambient schema package. Filesystem close/readback observations remain
`UNAVAILABLE-NOT-MATERIALIZED`.

The intended candidate entry point terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`. It cannot compile, build, create a runtime
tree, call a native API, launch a candidate process, access a network or
provider, run a rehearsal, or execute S0/E0.

The implementation manifest is externally pinned by SHA-256. The verifier
authenticates its targets, the five design-package closures, the approving
v0.5 design review, the CONTROL decision, and the v0.1-v0.3 predecessor
implementation reviews before copying authenticated bytes into a temporary
snapshot. Its child Python process runs unit tests only; candidate code creates
no process or filesystem object.

This is PUBLIC construction evidence for a non-executing prerequisite layer.
It is not build, binary, runtime, Windows, rehearsal, or S0 evidence.
