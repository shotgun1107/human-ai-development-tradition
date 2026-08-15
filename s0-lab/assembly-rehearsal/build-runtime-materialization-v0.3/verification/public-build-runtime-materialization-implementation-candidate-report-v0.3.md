# S0 v0.14 public build/runtime materialization implementation candidate report v0.3

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.3 REVISION OPEN`
- `branch`: `codex/s0-build-runtime-materialization-implementation-v03`
- `baseline_review_commit`: `4f2085b5bc76a30fc39d4d82904395a33e08b432`
- `v0.2_review_sha256`: `321f8a29edabbd2592e60cac3c58c46af3cba35e157956cf710b92615df9af59`
- `implementation_manifest_sha256`: `4c91cc9c248894e8ec2f30cc5339061f591e21ac63429a2b046194a7458095a5`
- `candidate_status`: bounded PUBLIC implementation revision candidate
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_api_reachable`: false
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. Outcome

The v0.3 candidate addresses the three major findings recorded by the
authenticated v0.2 independent review at the author-side implementation
level. The intended entry point still authenticates the exact five-version
design chain, reconstructs the effective v0.5 contract, and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`.

No compiler, native source, binary, runtime tree, platform API, provider,
model, rehearsal, S0, or E0 operation was added or performed.

## 2. Finding dispositions

### BRM-I02-IR-001: repaired in candidate

`EffectiveDesign` now carries its authenticated source authority. Construction
creates a stable source snapshot, independently reconstructs the expected
relations, full policy, all 115 mutation rows, and all twelve resource limits,
then requires exact equality. Invented rows or resources reject.

All accepted semantic values are copied into recursively immutable private
backing values. Runtime structure diagnostics no longer accept a caller-owned
mapping. Their `path_index` is reconstructed from immutable rows on access, so
clearing an unrelated caller mapping cannot change an accepted object.

### BRM-I02-IR-002: repaired in candidate

Runtime virtual paths remain in exact unsigned-ASCII input order, while prefix
collision analysis independently sorts the Windows case-folded identity set.
The previously accepted `Runtime/A/b` followed by `runtime/a` now rejects.

Denied path checks compare both exact folded roots and descendants. Therefore
the exact case alias `S0-LAB/CONTROL/F0-SEALED` and every child reject.

### BRM-I02-IR-003: repaired by completing the codec and closing plan authority

`RuntimeRow` now has exactly the retained schema's eight fields: virtual path,
semantic role, provenance-manifest SHA-256, provenance path, positive bounded
byte length, content SHA-256, closed classification enum, and closed
load/read-phase grammar.

`DllRow` implements the exact three-field map-row grammar and rejects denied
path identities. Caller-supplied rows may be examined only through explicitly
blocked structure diagnostics. Those diagnostics repeat the directory and DLL
bindings but carry no plan or execution authority.

Because the exact external runtime profile and authenticated `dll_map` are not
available in this gate, `plan_runtime_tree`, `derive_dll_directories`, and
`plan_dll_resolution` unconditionally reject with
`BLOCKED-MISSING-EXTERNAL-PIN`. Both A/B and B/A caller orders therefore fail
to create a validated plan. A later gate must supply and authenticate the
missing profile before implementing that authority transition.

## 3. Verification evidence

The author-side PUBLIC synthetic suite contains 20 tests. It retains the v0.2
positive and negative cases and adds independent reproductions for:

- invented 115-row matrices and twelve-resource mappings;
- caller-backed mapping-proxy mutation;
- raw-case versus Windows-case prefix-order inversion;
- exact and descendant denied-root identities;
- all eight runtime-row field grammars and lower bounds;
- DLL map basename, denied path, directory-alias, and alternate-order cases;
  and
- unconditional runtime/DLL plan blocking without an authenticated profile.

The final authenticated-snapshot verifier authenticated all ten implementation
rows, all five design manifests and their 6/7/9/9/7 targets, the approving
design review, the CONTROL decision, and both predecessor implementation
reviews. Its isolated `python -I -B` child passed all 20 tests with no failure,
error, or skip. The original-input swap sentinel passed. Static tests found
zero candidate filesystem, process, native, network, provider, model, build,
materialization, rehearsal, S0, or E0 call surfaces.

## 4. Deliberately closed work

The ten external pin classes remain incomplete. This candidate therefore does
not compile, link, inspect, materialize, publish, quarantine, call
`CreateProcessW`, `NtCreateFile`, or `SetFileInformationByHandle`, validate an
ambient schema registry, create a design-bound runtime/DLL plan, launch a
candidate, run a rehearsal, or execute S0/E0.

No exported diagnostic is execution authority. Independent review remains
required before CONTROL may consider a successor.

## 5. Maximum claim

Maximum claim: the repository contains a PUBLIC, non-executing v0.3 revision
candidate with author-side repairs for the v0.2 review findings. It continues
to refuse all unresolved external-pin and real-materialization boundaries.
This is not implementation or validation of a real build, runtime, Windows
behavior, rehearsal, S0, central system, Project Brain integration, or
model-to-model transfer.
