# Public end-to-end assembly runtime profile and neutral preloader bounded integration design v0.1

Status: public integration-design candidate; no implementation or execution

## 1. Authority, scope, and provenance

This document freezes the missing boundary between the authenticated public
assembly implementation candidate and the authenticated bounded runtime-
profile/neutral-preloader candidate. It does not reopen either predecessor
design and does not authorize code, build, runtime materialization, native
execution, a platform probe, or an assembly rehearsal.

- gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL RUNTIME PROFILE + NEUTRAL
  PRELOADER BOUNDED INTEGRATION DESIGN V0.1 OPEN`;
- repository: `human-ai-development-tradition`;
- base commit:
  `dc1c385562738f9fed1d97775c707625be0f5bb7`;
- base tree:
  `21309ce5aaabaefe357c67fb72a547940e11f9cc`;
- assembly implementation-manifest SHA-256:
  `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`;
- assembly candidate-report SHA-256:
  `520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005`;
- runtime/preloader v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving runtime/preloader v0.4 design-rereview record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- runtime/preloader v0.3 implementation-manifest SHA-256:
  `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2`;
- runtime/preloader v0.3 candidate-report SHA-256:
  `6e828246b91ddcc6d1b219289096ea87827fe0dde517fe3e15d444c74abe125d`;
- approving runtime/preloader v0.3 implementation-rereview record SHA-256:
  `03d35804483564a13668edb54e92ab00e6f5195ca4b371ee8d20a748a552c34a`.

The effective protocol authority remains assembly v0.3 plus v0.4 replacements
plus v0.5 replacements, composed with runtime/preloader design v0.1 through
v0.4. The runtime/preloader v0.3 Python package is bounded implementation
evidence. It does not replace the native responsibilities frozen by the v0.4
design.

## 2. Authenticated current-state reconstruction

CONTROL authenticated the runtime/preloader manifest as 11 exact public
targets and the assembly manifest as 32 exact public targets. Neither closure
contains an F0 path.

The current assembly candidate contains no import or call of
`s0_public_runtime_preloader`, `prepare_assembly_runtime_launch`,
`NeutralPreloader`, or `validate_runtime_profile_candidate`.

The current assembly live entry remains intentionally unreachable:

- `run_live_public_candidate` rejects when no external runtime-profile hash is
  supplied and then rejects unconditionally because no live runtime-profile
  schema is admitted;
- the child bootstrap accepts only an already established exact
  `jsonschema==4.26.0` module and otherwise fails before candidate import; and
- the assembly report classifies exact CPython/dependency authentication and
  neutral pre-import launch as blocking prerequisites.

The runtime/preloader v0.3 package provides an authenticated offline bridge:

- `prepare_assembly_runtime_launch` authenticates the exact assembly
  implementation manifest, its 32 targets, the assembly report, the v0.4
  design package, and the approving design record;
- it then calls `NeutralPreloader.prepare`, which exact-types and snapshots
  static material before invoking the standalone profile validator; and
- the returned `OfflinePreparedLaunch` is permanently `candidate_only=True`
  and `native_api_reachable=False`.

The package does not materialize a runtime, load a binary, create a process,
bind a platform identity, or issue live authority.

## 3. CONTROL integration decision

The integration decision is:

`DEFER-RPNP-MINORS; KEEP-LIVE-FAIL-CLOSED; DESIGN-ONE-EXACT-BRIDGE`

The two preserved MINOR findings do not require a runtime/preloader v0.4 code
revision before this integration design:

1. the standalone `validate_runtime_profile_candidate` input-snapshot gap is
   unreachable when assembly uses only `prepare_assembly_runtime_launch`; and
2. `source_audit.inspect_source_structure` is not an acceptance or authority
   predicate and must remain outside every live decision.

Either finding becomes blocking for integration if a later implementation
calls the standalone validator directly, consumes a `ValidatedProfileCandidate`
as authority, treats source-audit success as capability proof, or bypasses the
assembly-specific bridge.

## 4. Exact Python API boundary

### 4.1 Sole admitted offline assembly entry

The only admitted Python entry for assembly precreation integration is:

`s0_public_runtime_preloader.prepare_assembly_runtime_launch`

It must receive original raw bytes and exact byte mappings in the same
operation. A caller must not substitute a prior validation object, cached
relation tuple, profile object, launch plan, or self-reported hash.

The function is an offline conformance bridge only. Its return value cannot
authorize output mutation, process creation, native import, child launch,
publication, consumer acceptance, or rehearsal PASS.

### 4.2 Required future admission bridge

A future integration implementation may add exactly one assembly-specific
postcreation diagnostic entry:

`prepare_assembly_runtime_admission_diagnostic`

That entry must reauthenticate the same assembly artifacts and raw runtime
inputs in the same call before delegating to
`prepare_offline_admission_diagnostic`. It must remain candidate-only and must
not accept an `AssemblyArtifactValidation`, `ValidatedProfileCandidate`, or
`OfflinePreparedLaunch` as reusable authority.

### 4.3 Forbidden authority surfaces

Assembly code must not use any of these as authority:

- `validate_runtime_profile_candidate`;
- `ValidatedProfileCandidate`;
- `validate_assembly_artifact_bundle` results outside the same bridge call;
- `NeutralPreloader.prepare` directly from assembly code;
- `source_audit.inspect_source_text` or
  `source_audit.inspect_source_structure`;
- caller-created dataclasses, wrappers, hashes, manifest rows, or evidence
  objects; or
- a diagnostic result whose schema or type is candidate-only.

## 5. Two noninterchangeable integration lanes

### 5.1 Offline conformance lane

The next bounded implementation candidate may:

1. authenticate the integration-design package and every predecessor pin;
2. load exact raw assembly, runtime-profile, schema, manifest, and runtime-file
   bytes without ambient discovery;
3. call `prepare_assembly_runtime_launch`;
4. compare its candidate-only plan with frozen v0.4 constants; and
5. emit only an explicitly offline diagnostic with `rehearsal_pass=false`.

This lane must make zero native preloader calls, zero child-creation calls,
zero output mutations, and zero provider, model, network, F0, or oracle calls.

### 5.2 Future native live lane

The live lane is separate. It requires a later authenticated native preloader
implementation, exact build and runtime package, binary/import review, and a
separately opened real-Windows platform-probe gate.

The Python offline plan is test evidence for that native implementation. It
is not the native implementation, cannot be converted into one by a boolean
or wrapper, and cannot release the current assembly fail-close by itself.

## 6. Artifact and manifest graph

The next implementation candidate root is reserved as:

`s0-lab/assembly-rehearsal/public-end-to-end-v0.2/`

The implementation gate must assign exact logical paths beneath that root for
assembly source, native-preloader source, tests, and verification reports. It
must not modify the authenticated v0.1 assembly or runtime/preloader v0.3
packages in place.

Before any future live import or executable load, an externally pinned closed
manifest chain must authenticate:

1. the assembly v0.2 implementation sources and tests;
2. the native-preloader sources and build recipe;
3. compiler, linker, SDK, CRT, and direct-import inputs;
4. the produced native-preloader binary and its PE/import identity;
5. `runtime-files.sha256` and every runtime-file target;
6. the exact five-row effective runtime package:
   `runtime-files.sha256`, `runtime-profile-v0.1.json`,
   `runtime-profile-v0.2.json`, `runtime-profile-v0.3.json`, and
   `runtime-profile-v0.4.json`; and
7. the admitted platform-profile evidence used to bind loaded image and
   system-image identities.

The runtime-file manifest must assign exactly one artifact to every required
role:

- native preloader executable;
- Python executable;
- CPython runtime DLL;
- standard-library closure;
- extension-module closure;
- `jsonschema` and complete transitive dependency closure;
- assembly child bootstrap bytes; and
- verifier and guard bytes loaded by the child.

No ambient `PATH`, `PYTHONPATH`, registry lookup, user or system site package,
current interpreter, arbitrary dependency directory, network download,
fallback loader, or post-import self-hash may satisfy a missing row.

Large public build or runtime material need not be committed by this design
gate. A future materialization gate must choose one fresh out-of-repository
root, authenticate its identity and every target before use, and record only
publication-eligible public evidence. It must never place secrets, personal
data, credentials, F0 content, or a hidden oracle in that root or repository.

## 7. Future live entry and forbidden injection

The future assembly live entry remains
`s0_public_assembly_verifier.harness.run_live_public_candidate` but must be
revised under a separate implementation gate.

Its public inputs may name a workspace root, one fresh output root, one fully
manifest-authenticated runtime-package root, externally supplied exact
manifest/profile hashes, and a bounded timeout. The runtime root is not a
dependency search path; every loaded byte must be one authenticated manifest
target and must be bound into the platform profile.

The public entry must not accept:

- `python_executable`;
- `preloader_executable`;
- `dependency_root`;
- `sys_path` or import-search additions;
- caller-supplied allowed-read paths;
- loader, backend, observer, consumer, subprocess, or native-call callbacks;
  or
- a caller-created authority, witness, decision, or prepared-launch object.

Executable and module paths must be derived only from the authenticated launch
control at fixed virtual path `runtime/launch-inputs.json`. The corresponding
target bytes, runtime manifest row, profile bindings, file identity, and loaded
image identity must agree.

## 8. Authentication and launch state machine

The integration parent uses this exact monotonic state order:

1. `NEW`;
2. `PUBLIC-SOURCE-AUTHENTICATED`;
3. `RUNTIME-PACKAGE-AUTHENTICATED`;
4. `BINARY-IMPORTS-AUTHENTICATED`;
5. `PLATFORM-PROFILE-ADMITTED`;
6. `OUTPUT-ROOT-RESERVED`;
7. `PRELOADER-STARTED`;
8. `VERIFIER-CREATED-SUSPENDED`;
9. `ADMISSION-BOUND`;
10. `VERIFIER-RESUMED`; and
11. `TERMINAL`.

Any failure before `OUTPUT-ROOT-RESERVED` must leave the output path absent.
Any invalid transition enters an immutable rejected terminal condition. A
retry must not reuse a witness, plan, process, output root, pipe, handle,
manifest snapshot, or authority object.

The first five states are authentication only. The final six are prohibited
until all implementation, source/build/binary review, and platform-probe gates
have separately passed. The offline conformance candidate must stop before
`OUTPUT-ROOT-RESERVED`.

After live authorization, CONTROL launches exactly the authenticated native
preloader. That preloader alone constructs the ordered five-handle array and
calls the direct authenticated `kernel32.dll!CreateProcessW` import under the
v0.4 policy. The verifier child installs runtime sentinels before importing
assembly candidate modules. The native preloader and pinned kernel, not the
Python offline plan or child guard, own process-wide inheritance claims.

## 9. Exact fail-close release conditions

The unreachable raises in the current assembly live entry may be removed only
in the same reviewed implementation revision that proves all of these:

1. this design package passed a fresh independent design rereview with zero
   BLOCKING and zero MAJOR findings;
2. every public source and runtime manifest is externally pinned and fully
   authenticated before import, load, output reservation, or process start;
3. assembly uses only the exact bridge boundary in Section 4;
4. the standalone validator and source diagnostic have zero authority call
   paths;
5. the native-preloader source/build/binary/import closure passed independent
   review;
6. every deferred v0.4 semantic relation has authenticated evidence or remains
   fail-closed;
7. the real-Windows decoy, opposite-end, loaded-image, atomic-root, and
   interruption probes passed under their own gate;
8. the live API contains none of the forbidden injection surfaces in Section
   7; and
9. a mutation of any hash, row, path, file identity, loaded identity, import,
   launch field, handle role, state, or evidence binding fails before the
   affected action.

A non-null runtime-profile hash, schema-valid JSON, package version, source-
audit PASS, offline prepared plan, or passing regression suite alone cannot
release the fail-close.

## 10. Gate order

The required order after this design gate is:

1. fresh independent rereview of this exact integration-design package;
2. separate bounded public assembly v0.2 integration implementation gate;
3. fresh independent implementation and security rereview;
4. separate build and runtime-materialization gate;
5. source/build/binary/import and schema/semantic mutation review;
6. separate bounded real-Windows platform-probe gate;
7. assembly live-candidate reconsideration; and
8. only afterward, official public assembly rehearsal reconsideration.

No gate opens automatically and no earlier PASS substitutes for a later
evidence class.

## 11. Closed claims

This package establishes only a bounded public integration-design candidate.
It does not claim that runtime material, a native preloader, a trusted build,
loaded-image closure, platform behavior, live assembly, S0, E0, F0 execution,
oracle independence, provider/model behavior, the central system, Project
Brain integration, operational safety, economic value, production readiness,
or model-to-model transfer has been implemented or validated.
