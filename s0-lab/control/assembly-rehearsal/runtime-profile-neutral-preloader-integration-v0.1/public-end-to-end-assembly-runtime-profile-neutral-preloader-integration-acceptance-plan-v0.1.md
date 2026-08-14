# Public end-to-end assembly runtime profile and neutral preloader bounded integration acceptance plan v0.1

Status: design-level acceptance obligations; no implementation or execution

## 1. Purpose and threshold

This plan defines the evidence required to accept or reject the v0.1 bounded
integration design. It does not accept an implementation and does not
authorize runtime materialization, native execution, a platform probe, or a
public assembly rehearsal.

Design acceptance requires:

- exact Git and package authentication;
- zero unresolved BLOCKING findings;
- zero unresolved MAJOR findings;
- explicit disposition of every MINOR finding;
- one noncircular API and artifact boundary; and
- preservation of the current live fail-close.

## 2. Package authentication

The independent reviewer must reject the package before semantic review if:

- the exact design commit, tree, sole parent, or branch does not reproduce;
- the design-package manifest is not canonical, ASCII-sorted, unique, and
  exactly five rows;
- any logical artifact hash differs from its manifest row or sidecar;
- any Markdown artifact fails the canonical text-artifact validator after a
  successful validator SelfTest;
- either JSON artifact fails strict duplicate-key-rejecting parsing;
- the interface map does not validate against the exact Draft 2020-12 schema;
- an external predecessor pin does not reproduce;
- the worktree or index is not clean; or
- the role reads an unlisted path or any F0 content.

F0 verification is aggregate-only and must reproduce `32 / 11 / 10` with
zero worktree, index, untracked, ignored, skip-worktree, or assume-unchanged
anomalies.

## 3. Current-state reconstruction questions

The reviewer must independently establish all of these facts from admitted
bytes:

1. the assembly 32-target closure contains no import or call of the
   runtime/preloader package;
2. the live assembly entry rejects unconditionally before launch;
3. the child bootstrap requires an already authenticated runtime dependency
   closure and does not discover one;
4. `prepare_assembly_runtime_launch` reauthenticates exact assembly and design
   bytes before calling the snapshotted `NeutralPreloader` path;
5. the returned launch remains `candidate_only=True` and
   `native_api_reachable=False`; and
6. neither preserved RPNP false-PASS condition is reachable through the
   admitted assembly bridge, even though the bridge internally invokes the
   standalone validator only after creating its private snapshot.

Any contrary fact is at least MAJOR because it invalidates the integration
decision's premise.

## 4. API-boundary acceptance matrix

| Proposition | Required design disposition | Failure condition |
|---|---|---|
| Assembly precreation uses one exact Python bridge | Sole current entry is `prepare_assembly_runtime_launch` | Assembly may call `NeutralPreloader.prepare` or the standalone validator directly |
| Postcreation diagnostic reauthenticates in one call | Future wrapper must authenticate original assembly and runtime bytes before delegation | A cached validation, plan, evidence object, or relation tuple may substitute for raw bytes |
| Offline result is not live authority | Candidate-only and native-unreachable are permanent | A wrapper, flag, subclass, or constructed decision can upgrade it |
| Source audit is defense in depth only | Zero acceptance or authority consumers | Audit success can release fail-close or replace source review |
| Executable selection is manifest-derived | Fixed launch-control row and authenticated identities | Public caller supplies Python/preloader executable or loader callback |
| Runtime closure is exact | Every loaded byte is a manifest target authenticated before import/load | Ambient site, `PATH`, registry, network, fallback, or self-hash supplies a byte |

## 5. Artifact-graph acceptance

The design passes artifact review only if every future evidence class has one
owner and no circular claim:

- CONTROL authenticates public source, runtime, build, binary, and platform
  inputs before the affected action;
- the native preloader source/build/binary review proves construction of the
  ordered five-entry handle list and the exact `CreateProcessW` call;
- the runtime-file manifest owns Python, CPython, standard-library,
  extension-module, `jsonschema`, bootstrap, verifier, guard, and native-
  preloader target bytes;
- the platform profile owns loaded-image, system-image, direct-import, file-
  identity, and supported-Windows predicates;
- the child guard validates only the five known inherited objects and makes no
  process-wide unknown-handle absence claim; and
- the offline Python bridge owns only deterministic candidate diagnostics.

Schema validity, hash strings, package versions, CONTROL statements, child
guard observations, and offline plans must not be substituted for evidence
owned by another component.

## 6. State and fail-close review

The reviewer must verify that the interface map fixes one ordered integration
state machine and that:

- no output path is created or mutated before `OUTPUT-ROOT-RESERVED`;
- the offline lane stops before that state;
- no import, binary load, or process start precedes the corresponding closed
  manifest authentication;
- an invalid transition enters immutable rejection;
- no retry reuses a plan, witness, process, root, pipe, handle, snapshot, or
  authority object;
- the current unconditional live rejection remains in place through the
  design and design-rereview gates; and
- removing it requires all nine release conditions in the design, not merely
  a non-null runtime-profile hash.

## 7. Required later implementation mutations

A later implementation candidate must include deterministic rejection tests
for at least these mutations:

1. direct assembly call to `validate_runtime_profile_candidate`;
2. direct assembly call to `NeutralPreloader.prepare`;
3. reusable `ValidatedProfileCandidate`, artifact validation, launch plan, or
   admission object passed as authority;
4. source-audit PASS used to release a live branch;
5. public `python_executable`, `preloader_executable`, `dependency_root`,
   allowed-read list, loader, backend, observer, consumer, or subprocess
   injection;
6. manifest path, row, order, count, hash, duplicate, traversal, absolute,
   reparse, alias, or post-check substitution;
7. runtime target omitted from the closed loader/import dependency graph;
8. wrong Python, DLL, extension, standard-library, or `jsonschema` target;
9. launch control at any path other than `runtime/launch-inputs.json`;
10. executable bytes, file identity, loaded identity, and profile identity
    disagreement;
11. output reservation or child start before complete authentication;
12. any state skip, retry, or terminal reuse;
13. any handle role, order, access, count, array size, flag, environment,
    command, current-directory, evidence, PID, or admission mismatch; and
14. any attempt to treat the offline plan as a native call result.

Every mutation must fail before the affected import, output mutation, binary
load, native call, process creation, or authority consumption.

## 8. Required later evidence and gate order

Design PASS permits only consideration of the following separate sequence:

1. bounded assembly v0.2 integration implementation candidate;
2. fresh independent implementation and security rereview;
3. build and runtime-materialization gate;
4. source/build/binary/import and schema/semantic mutation review;
5. bounded real-Windows platform probe;
6. live assembly candidate reconsideration; and
7. official rehearsal reconsideration.

The implementation review must authenticate source before build. The binary
review must authenticate exact build output and direct imports before load.
The platform probe must bind actual file and loaded-image identities, exercise
opposite ends and inheritable decoys, and reproduce atomic-root and
interruption behavior. None of those results may be inferred from this design.

## 9. Required independent verdict

The fresh design reviewer must return exactly one of:

- `PASS-FOR-BOUNDED-ASSEMBLY-RUNTIME-PRELOADER-INTEGRATION-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `RETURN-TO-INTEGRATION-DESIGN-REVISION`; or
- `INVALID-REVIEW` after an authentication or role-boundary failure.

A PASS requires zero BLOCKING and zero MAJOR findings. A PASS does not open an
implementation gate, authorize Git publication, materialize a runtime, call a
native API, run a platform probe or rehearsal, access F0 or an oracle, or
establish S0 or production acceptance.
