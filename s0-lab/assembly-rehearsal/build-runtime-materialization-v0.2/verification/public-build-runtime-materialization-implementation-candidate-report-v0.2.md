# S0 v0.14 public build/runtime materialization implementation candidate report v0.2

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.2 REVISION OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v02`
- `baseline_review_commit`: `f188a7932d2472ae0700e1f3a70a2184cbb93860`
- `v0.1_review_sha256`: `fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b`
- `implementation_manifest_sha256`: `13d5d3dea763fa3bfaa095e1d3f235734323acacf153dab788b7cb6baac73128`
- `candidate_status`: bounded PUBLIC implementation revision candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

The v0.2 candidate repairs all five findings recorded by the authenticated
v0.1 independent review at the author-side implementation level. The intended
entry point still authenticates the exact five-version design chain,
reconstructs the effective v0.5 contract, and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`.

No compiler, native source, binary, runtime tree, platform API, provider,
model, rehearsal, S0, or E0 operation was added or performed.

## 2. Finding dispositions

### BRM-I01-IR-001: repaired in candidate

`AuthenticatedDesign` now reauthenticates the complete immutable file closure
against all five external manifest pins and both auxiliary pins whenever a
semantic authority transition occurs. Reusing its private marker over mutated
bytes rejects.

`BuildRuntimeDiagnostic` now contains only canonical raw bytes and their
digest. Every public property is derived from those bytes, and its exact key
set, schema ID, trace, terminal state, status, counts, fixed relation/policy
digests, and all false authority bits are revalidated at construction.

`RuntimeMaterializationPlan` no longer stores a caller-settable execution bit.
It exposes a read-only property that is always false, while its constructor
revalidates row types, order, identities, roles, aggregates, fixed resource
ceilings, path-prefix rules, and exact immutable index.

### BRM-I01-IR-002: repaired in candidate

The publication policy and every effective mutation row are recursively
frozen. Lists become tuples and objects become immutable mappings. The
effective design constructor independently recomputes the relation and policy
identities and validates all 115 rows and twelve resource limits.

### BRM-I01-IR-003: repaired in candidate

Runtime planning now rejects non-`RuntimeRow` duck types, file/directory prefix
collisions, caller bounds above 20,000 files or 2,147,483,648 bytes, and
Windows-case aliases of every denied public repository prefix. The new DLL
resolution plan binds each exact DLL name, path, SHA-256, parent directory,
Windows identity key, identity digest, and directory index.

This remains a virtual, non-executing plan. Physical file identity and runtime
observation remain blocked for later authorized gates.

### BRM-I01-IR-004: repaired by removing the success surface

The shipped schema module imports no ambient schema packages and exposes no
schema-success path. Both registry authentication and profile validation
unconditionally reject with `BLOCKED-MISSING-EXTERNAL-PIN`. A future exact
dependency closure requires a separate gate and review.

### BRM-I01-IR-005: repaired by truthful unavailability

The in-memory record helper now returns only a canonical-body diagnostic. It
contains no closed-file or readback digest. Both observation slots are exactly
`None` and the observation status is
`UNAVAILABLE-NOT-MATERIALIZED`; construction rejects any contrary claim.

## 3. Verification evidence

The author-side PUBLIC synthetic suite contains 18 tests. It covers the v0.1
positive and negative cases plus the exact five review reproductions:

- mutated pinned files under a reused authentication marker;
- changed diagnostic fields and changed effective-design digests;
- nested policy mutation;
- duck-typed runtime rows, prefix collisions, oversized caller limits, and
  denied-prefix case aliases;
- forged plan aggregates and attempted execution-bit replacement;
- DLL basename/path and directory-identity mismatches;
- ambient schema-success attempts; and
- false close/readback observation attempts.

The final authenticated-snapshot verifier authenticated all ten implementation
rows, all five design manifests and their 6/7/9/9/7 targets, the approving
design review, the CONTROL decision, and the v0.1 implementation review. Its
isolated `python -I -B` child passed all 18 tests with no failure, error, or
skip. The original-input swap sentinel passed. Static tests found zero
candidate filesystem, process, native, network, provider, model, build,
materialization, rehearsal, S0, or E0 call surfaces.

## 4. Deliberately closed work

The ten external pin classes remain incomplete. This candidate therefore does
not compile, link, inspect, materialize, publish, quarantine, call
`CreateProcessW`, `NtCreateFile`, or `SetFileInformationByHandle`, validate an
ambient schema registry, launch a candidate, run a rehearsal, or execute S0/E0.

No exported diagnostic or plan is execution authority. Independent review is
still required before CONTROL may consider a successor.

## 5. Maximum claim

Maximum claim: the repository contains a PUBLIC, non-executing v0.2 revision
candidate with author-side repairs for the v0.1 review findings. It continues
to refuse the unresolved external-pin boundary. This is not implementation or
validation of a real build, runtime, Windows behavior, rehearsal, S0, central
system, Project Brain integration, or model-to-model transfer.
