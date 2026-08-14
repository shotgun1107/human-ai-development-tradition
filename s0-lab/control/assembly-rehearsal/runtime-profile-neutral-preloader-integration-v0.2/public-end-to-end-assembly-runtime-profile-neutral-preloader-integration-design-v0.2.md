# Public end-to-end assembly runtime profile and neutral preloader bounded integration design v0.2

Status: public integration-design revision candidate; no implementation or execution

## 1. Authority, scope, and provenance

This package is the bounded successor to the v0.1 integration design. It
repairs only the atomic-root ownership and state-composition defects returned
by the fresh v0.1 independent rereview. It does not reopen the predecessor
assembly or runtime/preloader designs and does not authorize code, build,
runtime materialization, native execution, a platform probe, or an assembly
rehearsal.

- gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL RUNTIME PROFILE + NEUTRAL
  PRELOADER BOUNDED INTEGRATION DESIGN V0.2 REVISION OPEN`;
- repository: `human-ai-development-tradition`;
- predecessor integration-design commit:
  `80af894b4d97f5bbb60f1c43fdfde87a15fd3873`;
- predecessor integration-design tree:
  `a604245d4711b145963e927a9c6dff55a74dd8f1`;
- predecessor integration package-manifest SHA-256:
  `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b`;
- assembly v0.5 design-package manifest SHA-256:
  `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802`;
- approving assembly v0.5 rereview SHA-256:
  `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137`;
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

The effective protocol authority remains assembly v0.3 plus v0.4
replacements plus v0.5 replacements, composed with runtime/preloader v0.1
through v0.4. This v0.2 package replaces only the v0.1 integration clauses
implicated by `ARPNP-INT-RR-001` and `ARPNP-INT-RR-002`. Every other v0.1
integration clause remains authoritative.

## 2. Independent-rereview findings and revision decision

The valid fresh v0.1 rereview returned
`RETURN-TO-INTEGRATION-DESIGN-REVISION` with zero BLOCKING, two MAJOR, and zero
MINOR findings.

1. `ARPNP-INT-RR-001` found that v0.1 placed
   `OUTPUT-ROOT-RESERVED` before `PRELOADER-STARTED` even though effective
   runtime/preloader authority assigns sole parent-relative root creation and
   continuous original-handle retention to the native preloader.
2. `ARPNP-INT-RR-002` found that v0.1 ended in one generic `TERMINAL` without
   binding it to the child controller's ten states, the publication witness,
   the runtime-admission commit states, or the `SPENT` and `REJECTED`
   terminals.

CONTROL chooses the smallest compatible correction:

- retain the effective preloader-owned root design and remove the contradictory
  parent reservation state; and
- replace the generic outer terminal with exact component-state composition
  and two distinct live terminals.

No parent-to-preloader root-handle transfer is added because the preloader is
the sole creator and first holder of the root object.

## 3. Current implementation boundary remains unchanged

The authenticated current assembly candidate remains an offline diagnostic
implementation and still has no runtime/preloader call. Its diagnostic harness
creates a path-based output directory in the verifier parent. That behavior is
not the future live atomic-root implementation and cannot be reused as such.

The current live assembly entry remains unconditionally fail-closed. The
authenticated runtime/preloader v0.3 Python package remains an offline bridge:

- `prepare_assembly_runtime_launch` authenticates raw assembly and runtime
  artifacts and reaches the high-level snapshotted preloader path;
- its return value is permanently `candidate_only=True` and
  `native_api_reachable=False`; and
- neither the standalone validator nor source-audit diagnostic is an authority
  surface.

The v0.1 disposition of the two preserved RPNP MINOR findings remains
unchanged. A later implementation that exposes either finding to an authority
path fails this integration design.

## 4. Exact atomic-root ownership

### 4.1 Intent supplied by CONTROL

The public live entry may name one intended fresh output-root path. CONTROL
must authenticate exact output-parent identity evidence and derive one
canonical leaf. The pathname and identity evidence are intent only. They are
not a root object identity, a transferable handle authority, or evidence that
a root exists.

Before the native preloader starts, CONTROL must prove the leaf and every
case-folding alias absent relative to the retained authenticated parent. It
must not create, open, reserve, rename, or otherwise materialize the output
root. In particular, CONTROL must not use `os.mkdir`, `CreateDirectory*`,
`CreateFile*`, or `NtCreateFile` for the leaf.

### 4.2 Sole creator and original authority

The authenticated native preloader is the sole output-root creator. After
all source, runtime, binary, import, and platform states are authenticated,
CONTROL starts exactly that preloader. Under the effective predecessor
policy, the preloader obtains and retains its own live output-parent handle,
authenticates it against CONTROL's bound parent identity, and rechecks the
canonical leaf plus every case-folding alias as absent. No output-parent or
root handle is inherited from CONTROL. The preloader binds that retained
parent, leaf, absence result, nonce, and external pins in private state
`PRE-ROOT-ABSENT`.

Only then may it perform the single direct authenticated
`ntdll.dll!NtCreateFile` call frozen by effective runtime/preloader v0.3 and
represented by v0.4. Success must satisfy the exact eleven-argument ABI,
`FILE_CREATE`, root-relative name, reparse defenses, return status, and all
returned-object postconditions. No second create, pathname reopen, alternate
API, alias retry, or cleanup-and-retry route exists.

The exact returned handle becomes the preloader's original root authority.
The preloader validates it without closing or reopening it and retains it
continuously through verifier termination and the final preloader recheck.
Only that successful transaction advances the preloader from
`PRE-ROOT-ABSENT` to `ROOT-CREATED-HELD`.

### 4.3 Verifier duplicate and identity continuity

The preloader creates one inheritable reduced-access duplicate of the retained
original. It proves same-object identity before verifier creation and places
only the duplicate in position four of the effective ordered five-handle
array. The original is never inherited.

The verifier guard consumes the inherited duplicate once, validates its
object kind, reduced access, non-reparse properties, stable volume/file
identity, and equality to the retained-root identity in the authenticated
admission transaction. A path, numeric locator, copied wrapper, or serialized
identity cannot substitute.

There is therefore no root-handle handoff from CONTROL to the preloader. The
only cross-process root transfer is the effective preloader-to-verifier
same-object reduced duplicate supplied by the exact five-handle list.

### 4.4 Failure and quarantine

Before the sole successful create call, the output leaf must remain absent.
Collision, alias insertion, identity drift, or create failure rejects without
claiming a root object.

After `NtCreateFile` reports `FILE_CREATED`, every later failure is post-output
and must preserve the effective quarantined-root routing. Closing a handle,
deleting by path, or obtaining an absent path afterward cannot relabel the run
as clean pre-output failure or upgrade it to success.

## 5. Component state machines retained exactly

### 5.1 Native preloader

The effective native-preloader states remain:

1. `PRE-ROOT-ABSENT`;
2. `ROOT-CREATED-HELD`;
3. `VERIFIER-LAUNCHED`;
4. `COMMIT-REQUESTED`; and
5. terminal `COMMIT-REPLIED` or terminal `FAILED`.

The preloader remains in `ROOT-CREATED-HELD` while the verifier is created
suspended. Exact handle-list construction, successful `CreateProcessW`, job
assignment, and resume are all required before `VERIFIER-LAUNCHED`.

### 5.2 Verifier runtime admission

Because effective v0.3 moved root creation into the preloader, the live
verifier admission begins only in:

1. `ROOT-CREATED-BOUND`;
2. `COMMITTING`;
3. `COMMIT-ACKED`;
4. terminal `SPENT`; or
5. terminal `REJECTED`.

The exact guard transaction constructs `ROOT-CREATED-BOUND` from live handles
and the authenticated admission frame before Python candidate import. Invalid
transition attempts from a nonterminal state atomically enter `REJECTED`.
Attempts against `SPENT` or `REJECTED` fail without mutation.

### 5.3 Assembly child controller

The assembly controller retains its exact ten-state order:

1. `NEW`;
2. `PREFLIGHT_AUTHENTICATED`;
3. `REQUEST_RECONSTRUCTED`;
4. `OUTPUT_RESERVED`;
5. `RUNNER_ENTERED`;
6. `INVOKED_ONCE`;
7. `RESPONSE_CAPTURED`;
8. `ANSWER_VALIDATED`;
9. `TEMP_RECORD_VERIFIED`; and
10. `COMPLETE`.

The controller's `OUTPUT_RESERVED` is reservation of the fixed four names
inside the already authenticated inherited root. It is not creation or
reopening of the root directory.

`COMPLETE` means only that the child finished this controller sequence after
the exact publication replies. It remains diagnostic-only and is neither a
live decision nor rehearsal PASS.

## 6. Exact outer live integration composition

The live coordinator uses this exact monotonic order:

1. `NEW`;
2. `PUBLIC-SOURCE-AUTHENTICATED`;
3. `RUNTIME-PACKAGE-AUTHENTICATED`;
4. `BINARY-IMPORTS-AUTHENTICATED`;
5. `PLATFORM-PROFILE-ADMITTED`;
6. `PRELOADER-STARTED`;
7. `ROOT-CREATED-HELD`;
8. `VERIFIER-CREATED-SUSPENDED`;
9. `VERIFIER-RESUMED`;
10. `ADMISSION-ROOT-CREATED-BOUND`;
11. `ASSEMBLY-CONTROLLER-ACTIVE`;
12. `PUBLICATION-WITNESS-ISSUED`;
13. `ASSEMBLY-CONTROLLER-COMPLETE`;
14. `ADMISSION-COMMITTING`;
15. `ADMISSION-COMMIT-ACKED`; and
16. exactly one terminal: `LIVE-CONSUMED` or `REJECTED`.

The old generic `TERMINAL` and contradictory `OUTPUT-ROOT-RESERVED` states do
not exist in v0.2.

## 7. Transition predicates and owners

| Outer transition | Sole owner and required current-run evidence |
|---|---|
| `PRELOADER-STARTED` | CONTROL has completed the four preceding authentication states, proves the leaf absent in its authenticated input view, and starts exactly the authenticated native-preloader image with the frozen launch control. No root exists yet; the preloader must independently bind the live parent handle and recheck absence before its create call. |
| `ROOT-CREATED-HELD` | Native preloader alone completes the sole `NtCreateFile` transaction, all returned-object postconditions, and continuous original-handle retention. |
| `VERIFIER-CREATED-SUSPENDED` | Native preloader alone constructs the exact five-handle list, launch evidence, and successful suspended `CreateProcessW` result while retaining the original root. It has not yet claimed `VERIFIER-LAUNCHED`. |
| `VERIFIER-RESUMED` | Native preloader completes child-end close rules, job assignment, launch binding, and the one resume; its state becomes `VERIFIER-LAUNCHED`. |
| `ADMISSION-ROOT-CREATED-BOUND` | The verifier native guard's one-use bind validates all five live handles, the admission frame, current PID/image, parent relation, and root same-object identity before Python candidate import. |
| `ASSEMBLY-CONTROLLER-ACTIVE` | Runtime sentinels are installed and healthy, then the authenticated assembly child begins at controller state `NEW`. |
| `PUBLICATION-WITNESS-ISSUED` | The verifier-parent observer has accepted exactly the two ordered publication requests, performed the two exact moves, and issued the private unused witness bound to the current child, pipe, root identity, trace, files, and receipt. |
| `ASSEMBLY-CONTROLLER-COMPLETE` | The child traverses all ten states in order, reaches exact `COMPLETE`, produces the diagnostic completion object, emits no extra frame or stderr, and terminates successfully. The state is still not PASS. |
| `ADMISSION-COMMITTING` | The exact live admission is still `ROOT-CREATED-BOUND`, the publication witness exists and is unused, child completion is authenticated, and the verifier sends the sole commit request; the admission becomes `COMMITTING` and preloader becomes `COMMIT-REQUESTED`. |
| `ADMISSION-COMMIT-ACKED` | The preloader completes every root, parent, process, job, file-set, pipe, and external-pin recheck, sends exact `OK\n` plus EOF, and enters `COMMIT-REPLIED`; the verifier admission enters `COMMIT-ACKED`. Preloader `OK` alone is not authority. |
| `LIVE-CONSUMED` | The same-process live consumer makes the first terminal attempt, atomically spends both the exact witness and admission, revalidates current files and receipt bindings, advances the admission to `SPENT`, and issues the registered current-run `LiveDecision`. |
| `REJECTED` | Any failed predicate, invalid transition, skipped/reordered state, consumer rejection, timeout, interruption, quarantine, or nested `FAILED`/`REJECTED` result atomically rejects the outer run. Existing admission and witness authority is terminally consumed or rejected exactly once where available. |

No state may be entered from a serialized state name, child exit code,
candidate object, prior-run evidence, or caller-supplied transition result.
Every predicate is evaluated from authenticated current-run bytes, handles,
processes, channels, and private capabilities owned by the named component.

## 8. Terminal and authority rules

`REJECTED` is immutable and never authority. A retry must use a fresh nonce,
process chain, output parent/leaf, root transaction, pipes, handles, admission,
witness, manifest snapshot, and consumer attempt.

`LIVE-CONSUMED` is reachable only with runtime admission `SPENT`, a consumed
private publication witness, preloader `COMMIT-REPLIED`, exact assembly child
`COMPLETE`, and a current-process live-consumer decision. None of those facts
alone can substitute for their conjunction.

Even `LIVE-CONSUMED` means only the bounded same-process live-consumer
acceptance defined by effective assembly v0.5. It is not by itself official
rehearsal PASS, S0, E0, F0 evidence, production authority, or serialized
success authority. An official rehearsal remains a later separately opened
CONTROL gate.

After process exit, every record, receipt, state log, evidence frame, file,
hash, report, and decision description is diagnostic only. No outer state or
terminal label can recreate the private live decision.

## 9. Separate offline lane

The offline conformance lane never enters the live state machine. Its exact
candidate-only order is:

1. `OFFLINE-NEW`;
2. `OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED`;
3. `OFFLINE-PLAN-VALIDATED`; and
4. terminal `OFFLINE-DIAGNOSTIC-COMPLETE` or `OFFLINE-REJECTED`.

It may call only the exact assembly-specific high-level offline bridge. It
makes zero native calls, creates no root or process, installs no live guard,
issues no witness, performs no commit, and cannot transition or be promoted
into any live state. Its result must retain `candidate_only=true`,
`native_api_reachable=false`, and `rehearsal_pass=false`.

## 10. Fail-close release conditions

The unreachable rejection in the current assembly live entry may be removed
only in one later reviewed implementation revision that proves all v0.1
release conditions plus these v0.2 additions:

1. the preloader is the sole root creator and CONTROL performs no leaf create
   or path reopen;
2. the exact original handle is retained continuously and the verifier
   receives only the proven same-object reduced duplicate;
3. every live outer transition enforces the predicate and owner in Section 7;
4. the child traverses all ten controller states and `COMPLETE` remains
   diagnostic-only;
5. publication produces the exact private unused witness before commit;
6. the runtime admission reaches `COMMIT-ACKED` only after the preloader's
   independent current-run recheck;
7. the live consumer jointly spends the admission and witness before
   `LIVE-CONSUMED`; and
8. no generic terminal, process exit, file, receipt, report, preloader reply,
   or state string releases authority.

A passing offline plan, schema validation, unit suite, source audit, hash
comparison, platform-profile string, or prior live result cannot release the
fail-close.

## 11. Required deterministic mutations

A later implementation must reject before the affected action or authority
consumption when any of these occurs:

- CONTROL or the current verifier parent creates the root leaf;
- root creation occurs before `PRELOADER-STARTED` or before all authentication
  states;
- a path, reopened handle, second create, alternate API, case alias, reparse,
  or post-check replacement substitutes for the original root;
- the original closes before final preloader recheck;
- the verifier duplicate has wrong access, wrong role, wrong identity, or is
  not the same object;
- `ADMISSION-ROOT-CREATED-BOUND` is claimed before verifier resume or after
  candidate import;
- any child-controller state is skipped, repeated, reordered, or fabricated;
- publication witness issuance is missing, early, copied, reused, or bound to
  another root, child, pipe, trace, file, or receipt;
- commit starts before authenticated child `COMPLETE` and publication witness;
- preloader reply is missing, malformed, early, duplicated, or treated alone
  as success;
- the consumer is missing, rejected, retried, or supplied a stale/copy witness
  or admission;
- generic `TERMINAL`, child `COMPLETE`, process exit zero, files, hashes, or a
  serialized result is treated as live authority; or
- an offline diagnostic is promoted into the live machine.

Every skip, early terminal, alternate owner, or nested-state mismatch must be
an explicit mutation case, not only an inferred invariant.

## 12. Gate order and closed claims

The required order remains:

1. fresh independent rereview of this exact v0.2 package;
2. separate bounded public assembly v0.2 integration implementation gate;
3. fresh independent implementation and security rereview;
4. separate build and runtime-materialization gate;
5. source/build/binary/import and schema/semantic mutation review;
6. separate bounded real-Windows platform-probe gate;
7. assembly live-candidate reconsideration; and
8. only afterward, official public assembly rehearsal reconsideration.

No gate opens automatically. This package establishes only a bounded public
integration-design revision candidate. It does not establish an
implementation, trusted build, runtime material, binary, native behavior,
platform identity, live assembly, official rehearsal, F0 or oracle access,
S0, E0, the central system, Project Brain integration, production readiness,
operational safety, economic value, or model-to-model transfer.
