# S0 public build/runtime materialization implementation candidate v0.6

This directory contains the bounded PUBLIC v0.6 revision of the
CONTROL-integrated build/runtime materialization candidate. It addresses the
one major finding in the authenticated v0.5 implementation review without
opening any build, materialization, native, process, network, provider,
rehearsal, S0, or E0 gate.

The candidate retains:

- exact v0.1-v0.5 design-manifest and target authentication;
- exact-string manifest logical paths before caller-dispatched comparison;
- stable authenticated snapshots at every semantic authority transition;
- exact-string semantic digest identities and immutable effective-design data;
- RFC 8785 object-key ordering by UTF-16 code units at every JSON depth;
- strict canonical JSON-object records with byte-derived identities;
- exact `TargetRow` reconstruction at the target-set boundary;
- the runtime-row, path-identity, resource, DLL-preimage, ordering, closed
  aggregate, and denied-root rules; and
- authenticated-snapshot PUBLIC synthetic verification.

The v0.6 repair reconstructs and stores fresh exact child values at every
exported runtime/DLL aggregate boundary. It rebuilds all eight `RuntimeRow`
fields, all three `DllRow` fields, all four `DllDirectoryDiagnostic` fields,
and all seven `DllResolutionRowDiagnostic` fields before any aggregate or
coherence decision. Reflectively mutated caller children therefore reject,
and later reflective mutation of caller-supplied source children cannot alter
the freshly stored aggregate children.

Runtime and DLL structural results remain diagnostics with
`authority_status=BLOCKED-MISSING-EXTERNAL-PIN`. They are not validated
materialization plans. The public `plan_runtime_tree`,
`derive_dll_directories`, and `plan_dll_resolution` entry points always reject
until a later gate authenticates an exact externally pinned runtime profile
and DLL map.

The schema adapter remains unconditionally fail-closed and imports no ambient
schema package. Filesystem close/readback observations remain
`UNAVAILABLE-NOT-MATERIALIZED`.

The intended candidate entry point terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`. It cannot compile, build, create a runtime
tree, call a native API, launch a candidate process, access a network or
provider, run a rehearsal, or execute S0/E0.

The implementation manifest is externally pinned by SHA-256. The verifier
authenticates its targets, the five design-package closures, the approving
v0.5 design review, the CONTROL decision, and the v0.1-v0.5 predecessor
implementation reviews before copying authenticated bytes into a temporary
snapshot. Its child Python process runs unit tests only; candidate code creates
no process or filesystem object.

This is PUBLIC construction evidence for a non-executing prerequisite layer.
It is not build, binary, runtime, Windows, rehearsal, or S0 evidence.
