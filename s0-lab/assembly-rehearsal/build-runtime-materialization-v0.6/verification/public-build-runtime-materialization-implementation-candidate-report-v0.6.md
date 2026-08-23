# S0 v0.14 public build/runtime materialization implementation candidate report v0.6

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.6 REVISION OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v06`
- `baseline_review_commit`: `a2c2ccf4d4d96b6ffd5fba4a2cf5d7885d46b600`
- `v0.5_review_sha256`: `3a1a219bf41a5d38cf1b4df3545ee44ab96b8e4cdea314e0565f9f6593575c68`
- `implementation_manifest_sha256`: `c653931163e1818fe17b0f53b7d7e6d9e843cde3eea8752b952c8b30dd796798`
- `candidate_status`: bounded PUBLIC implementation revision candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

The v0.6 candidate repairs the one major finding recorded by the authenticated
v0.5 independent review at the author-side implementation level. The intended
entry point still authenticates the exact five-version design chain,
reconstructs the effective v0.5 contract, and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`.

No compiler, native source, binary, runtime tree, platform API, provider,
model, rehearsal, S0, or E0 operation was added or performed.

## 2. Finding disposition

### BRM-I05-IR-001: repaired in candidate

The runtime validator now reconstructs every exact `RuntimeRow` from all eight
public fields before reading aggregate fields and stores only rebuilt rows.
Both `inspect_runtime_tree_structure` and direct
`RuntimeTreeStructureDiagnostic` construction apply the closed child
contract.

The DLL input factory reconstructs every exact `DllRow` from all three fields
before reading names or paths. `DllResolutionStructureDiagnostic` reconstructs
all four `DllDirectoryDiagnostic` fields and all seven
`DllResolutionRowDiagnostic` fields before coherence checks and stores only
rebuilt children. Invalid post-construction mutations and Boolean integer
aliases reject. Later reflective mutation of caller-supplied source children
cannot alter the freshly stored aggregate children; fresh reaggregation of a
mutated stored child rejects.

Adjacent exported boundaries were audited. `target_set_preimage` already
reconstructs every `TargetRow`; `DllResolutionRowDiagnostic` already
reconstructs its embedded `DllRow`; and `EffectiveDesign` reauthenticates and
deep-copies its complete state. No adjacent aggregate bypass was identified.

## 3. Verification evidence

The PUBLIC synthetic suite contains 30 tests. It retains all predecessor
authentication, authority, runtime, DLL, record, path, blocking, and
forbidden-surface cases and adds exact hostile matrices for:

- all eight runtime-row fields, including Boolean length and denied/traversal
  provenance identities;
- all four DLL-directory fields;
- all seven DLL-resolution child fields;
- all three DLL input-row fields; and
- defensive child copying, later caller mutation, and reaggregation rejection.

A direct run and the final authenticated-snapshot verifier both passed all 30
tests with no failure, error, or skip. The verifier authenticated the ten
implementation rows, all five design manifests and their 6/7/9/9/7 targets,
the approving design review, the CONTROL decision, and the v0.1-v0.5
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

Maximum claim: the repository contains a PUBLIC, non-executing v0.6 revision
candidate with an author-side repair for the v0.5 review finding. It continues
to refuse all unresolved external-pin and real-materialization boundaries.
This is not implementation or validation of a real build, runtime, Windows
behavior, rehearsal, S0, central system, Project Brain integration, or
model-to-model transfer.
