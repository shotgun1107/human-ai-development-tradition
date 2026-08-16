# S0 v0.14 public build/runtime materialization implementation candidate report v0.5

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.5 REVISION OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v05`
- `baseline_review_commit`: `eb5da0cb4a38113b1225c3dbb352fcd810584739`
- `v0.4_review_sha256`: `f6e61510a2d63966d72d5d88018d3e0dbcaeb0d3a391dba27cc3902a071a486f`
- `implementation_manifest_sha256`: `9e3dd30dc3e179313763c1624041386b025c6bf273c49bd767f03bfbb36799ca`
- `candidate_status`: bounded PUBLIC implementation revision candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

The v0.5 candidate repairs the two major and one minor findings recorded by
the authenticated v0.4 independent review at the author-side implementation
level. The intended entry point still authenticates the exact five-version
design chain, reconstructs the effective v0.5 contract, and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`.

No compiler, native source, binary, runtime tree, platform API, provider,
model, rehearsal, S0, or E0 operation was added or performed.

## 2. Finding dispositions

### BRM-I04-IR-001: repaired in candidate

`target_set_preimage` now accepts only a nonempty exact tuple whose elements
are exact `TargetRow` instances. It reconstructs every row through the closed
`TargetRow` validator before reading fields. Duck rows, list containers,
post-construction traversal mutation, negative or Boolean lengths, and
malformed digests therefore reject before preimage construction.

### BRM-I04-IR-002: repaired in candidate

`jcs_lf` now recursively orders every JSON object by the UTF-16 big-endian
code-unit representation of its property names before serialization. This
matches RFC 8785 ordering for BMP and supplementary-plane keys while retaining
the existing integer-only bounded number domain. Invalid surrogate text
rejects. `construct_in_memory_record` and `InMemoryRecordDiagnostic` now
derive and recheck the same exact ordering.

### BRM-I04-IR-003: repaired in candidate

`_authenticate_manifest` requires `ManifestBundle.logical_path` to be an exact
string before comparison. Equality-spoof and exception-raising comparison
objects both take the stable authentication-error path, and the public
candidate returns its documented `CANDIDATE-REJECTED` diagnostic.

## 3. Verification evidence

The PUBLIC synthetic suite contains 26 tests. It retains all predecessor
authentication, authority, runtime, DLL, record, path, blocking, and
forbidden-surface cases and adds exact reproductions for:

- duck, list-backed, and post-construction-mutated target rows;
- supplementary-plane U+10000 versus BMP U+E000 RFC 8785 property order;
- canonical record construction using that UTF-16 order; and
- equality-spoofing and exception-raising manifest logical-path objects.

A direct run and the final authenticated-snapshot verifier both passed all 26
tests with no failure, error, or skip. The verifier authenticated the ten
implementation rows, all five design manifests and their 6/7/9/9/7 targets,
the approving design review, the CONTROL decision, and the v0.1-v0.4
implementation reviews. Snapshot-only import and the original-input swap
sentinel passed, while candidate filesystem, process, native, network, and
provider call counts remained zero.

## 4. Deliberately closed work

The ten external pin classes remain incomplete. This candidate therefore does
not compile, link, inspect, materialize, publish, quarantine, call
`CreateProcessW`, `NtCreateFile`, or `SetFileInformationByHandle`, validate an
ambient schema registry, create a design-bound runtime/DLL plan, launch a
candidate, run a rehearsal, or execute S0/E0.

No exported diagnostic is execution authority. Independent review remains
required before CONTROL may consider a successor.

## 5. Maximum claim

Maximum claim: the repository contains a PUBLIC, non-executing v0.5 revision
candidate with author-side repairs for the v0.4 review findings. It continues
to refuse all unresolved external-pin and real-materialization boundaries.
This is not implementation or validation of a real build, runtime, Windows
behavior, rehearsal, S0, central system, Project Brain integration, or
model-to-model transfer.
