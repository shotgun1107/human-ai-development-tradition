# S0 public build/runtime materialization implementation candidate v0.3

This directory contains the bounded PUBLIC v0.3 revision of the
CONTROL-integrated build/runtime materialization candidate. It addresses the
three major findings in the authenticated v0.2 implementation review without
opening any build, materialization, native, process, network, provider,
rehearsal, S0, or E0 gate.

The candidate implements:

- exact v0.1-v0.5 design-manifest and target authentication;
- stable authenticated snapshots at every semantic authority transition;
- an `EffectiveDesign` that rederives and byte-compares all relations, the
  complete policy, all 115 mutation rows, and all twelve resource authorities
  against its authenticated source closure;
- canonical byte-derived diagnostics with no caller-settable execution bit;
- a recursively immutable policy, matrix, resource map, and runtime diagnostic
  index;
- the exact eight-field runtime-row grammar, including provenance, closed
  classification, semantic-role, phase, and byte-length rules;
- case-fold-independent file/directory prefix collision detection and
  exact-or-descendant denied-root rejection;
- exact three-field DLL-map row and ordered directory/binding structure
  diagnostics; and
- authenticated-snapshot PUBLIC synthetic verification.

The runtime and DLL structural results are explicitly diagnostics with
`authority_status=BLOCKED-MISSING-EXTERNAL-PIN`. They are not validated
materialization plans. The public `plan_runtime_tree`,
`derive_dll_directories`, and `plan_dll_resolution` entry points always reject
until an exact externally pinned runtime profile and DLL map are authenticated
by a later gate. Caller-selected A/B ordering therefore cannot become plan
authority.

The schema adapter also remains unconditionally fail-closed and imports no
ambient schema package. Filesystem close/readback observations remain
`UNAVAILABLE-NOT-MATERIALIZED`.

The intended candidate entry point still terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`. It cannot compile, build, create a runtime
tree, call a native API, launch a candidate process, access a network or
provider, run a rehearsal, or execute S0/E0.

The implementation manifest is externally pinned by SHA-256. The verifier
authenticates its ten targets, the five design-package closures, the approving
design review, the CONTROL decision, and both predecessor implementation
reviews before copying authenticated bytes into a temporary snapshot. Its
child Python process runs unit tests only; candidate code creates no process
or filesystem object.

This is PUBLIC construction evidence for a non-executing prerequisite layer.
It is not build, binary, runtime, Windows, rehearsal, or S0 evidence.
