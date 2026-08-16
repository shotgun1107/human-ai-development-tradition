# S0 v0.14 public build/runtime materialization implementation candidate report v0.4

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.4 REVISION OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v04`
- `baseline_review_commit`: `0b1bc528b3ba255b01c395f2c2fa1756ef879afb`
- `v0.3_review_sha256`: `b7e4fa3ccbd9c75c1aa00cbae4e5a3b460846533e551002b2ed1f437d4275cc1`
- `implementation_manifest_sha256`: `9067671d2e36c50104a8463c1a771df6d36b51ff910c0243d00aeab7763ff594`
- `candidate_status`: bounded PUBLIC implementation revision candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

The v0.4 candidate repairs the three major findings recorded by the
authenticated v0.3 independent review at the author-side implementation
level. The intended entry point still authenticates the exact five-version
design chain, reconstructs the effective v0.5 contract, and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`.

No compiler, native source, binary, runtime tree, platform API, provider,
model, rehearsal, S0, or E0 operation was added or performed.

## 2. Finding dispositions

### BRM-I03-IR-001: repaired in candidate

`EffectiveDesign` now rejects any digest field that is not exact lowercase
64-character SHA-256 text before equality is evaluated. Both accepted digest
fields are replaced with the immutable reconstructed constants. Equality-
spoofing caller objects therefore cannot survive construction. The source
manifest-hash tuple also requires exact string entries.

### BRM-I03-IR-002: repaired in candidate

DLL directory identities now hash the exact retained preimage
`windows_directory_identity_key=<ascii-lowercase-key>` plus one LF.
Application directory remains index zero; every remaining directory is sorted
by strict unsigned-ASCII bytes of its identity key.

Direct aggregate construction now requires exact nonempty tuples, contiguous
indices, application-parent binding at directory zero, unique DLL names and
paths, exact identity-key order, a closed used directory set, and repeated
denied-root checks. Application rebinding, empty aggregates, unused
directories, denied directory aliases, case-preserving digest drift, and
raw-path ordering all reject.

### BRM-I03-IR-003: repaired in candidate

`BuildRuntimeDiagnostic` requires `mutation_row_count` to be an exact integer,
so JSON Boolean `false` cannot stand in for zero. `InMemoryRecordDiagnostic`
now parses the body as strict UTF-8 JSON, requires an exact object, and
requires byte equality with its own canonical JCS-plus-LF re-encoding before
accepting the digest. Runtime and DLL diagnostic aggregate integer/string
identity fields received the same adjacent exact-type checks.

## 3. Verification evidence

The PUBLIC synthetic suite contains 23 tests. It retains the predecessor
authentication, immutable-design, runtime-row, path, blocking, and forbidden-
surface cases and adds exact reproductions for:

- equality-spoofing relation and publication-policy digest objects;
- the effective DLL identity preimage and case-insensitive digest equality;
- identity-key rather than raw-path directory ordering;
- application rebinding, empty aggregates, unused directories, and denied
  directory aliases;
- Boolean mutation-count drift and noncanonical record bodies; and
- adjacent runtime diagnostic aggregate type drift.

A direct post-change run passed all 23 tests with no failure, error, or skip.
The final authenticated-snapshot verifier authenticated the ten implementation
rows, all five design manifests and their 6/7/9/9/7 targets, the approving
design review, the CONTROL decision, and the v0.1-v0.3 implementation reviews.
Its isolated `python -I -B` child passed the same 23 tests. Snapshot-only import
and the original-input swap sentinel passed, while candidate filesystem,
process, native, network, and provider call counts remained zero.

## 4. Deliberately closed work

The ten external pin classes remain incomplete. This candidate therefore does
not compile, link, inspect, materialize, publish, quarantine, call
`CreateProcessW`, `NtCreateFile`, or `SetFileInformationByHandle`, validate an
ambient schema registry, create a design-bound runtime/DLL plan, launch a
candidate, run a rehearsal, or execute S0/E0.

No exported diagnostic is execution authority. Independent review remains
required before CONTROL may consider a successor.

## 5. Maximum claim

Maximum claim: the repository contains a PUBLIC, non-executing v0.4 revision
candidate with author-side repairs for the v0.3 review findings. It continues
to refuse all unresolved external-pin and real-materialization boundaries.
This is not implementation or validation of a real build, runtime, Windows
behavior, rehearsal, S0, central system, Project Brain integration, or
model-to-model transfer.
