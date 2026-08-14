# S0 v0.14 public end-to-end runtime/preloader bounded integration implementation v0.1 minor rereview

Status: fresh independent PUBLIC minor rereview; offline candidate only

## 1. Verdict and finding counts

Verdict: `PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`

- BLOCKING: 0
- MAJOR: 0
- MINOR: 0
- prior finding `ARPNP-INT-IR-001`: independently closed at candidate level

This verdict is limited to the exact revision and authenticated PUBLIC inputs
identified below. It does not establish runtime materialization, a trusted
build, native or live safety, a platform probe, official rehearsal PASS, S0 or
E0 execution, F0 isolation under execution, production readiness, the central
system, Project Brain integration, operational safety, economic value, or
model-to-model transfer.

## 2. Authenticated baseline and input inventory

- worktree: `C:\tmp\s0i14-minor-review`;
- branch:
  `codex/s0-assembly-rpnp-integration-implementation-v01-minor-rereview`;
- reviewed HEAD: `edcebb6434cd1a86736fb612ee26b1b0ec7b1311`;
- revision remote ref:
  `refs/remotes/origin/codex/s0-assembly-rpnp-integration-implementation-v01-minor-revision`;
- revision remote ref value:
  `edcebb6434cd1a86736fb612ee26b1b0ec7b1311`;
- initial dirty-entry count, including untracked entries: `0`.

The prior official review Markdown reproduced SHA-256
`ddf5d4ade01c4d87a2e027d8487a9c5a34e317a3df3aee1e19d624492849dbc0`,
and its same-basename sidecar was exact.

All eight candidate files were read. The candidate implementation manifest
reproduced SHA-256
`7469f62d67c9d5f416f38db7e4a14b5f3819e739cf38a71f1fec452421a7fabe`.
It contained exactly three canonical, unique, ASCII-sorted rows, and all three
targets matched. The candidate verification manifest reproduced SHA-256
`8f8140d678e5846639ff382b32035c342dc8b2dd7d929da5ff37a759f8aa9d7b`;
its exact four-row closure matched, including the candidate report and its
sidecar.

Every externally pinned predecessor manifest and target closure was
authenticated before semantic reliance:

| PUBLIC closure | Manifest SHA-256 | Exact rows |
|---|---|---:|
| assembly implementation v0.1 | `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623` | 32 |
| runtime/preloader implementation v0.3 | `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2` | 11 |
| runtime/preloader design v0.4 | `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589` | 6 |
| integration design v0.1 | `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b` | 5 |
| integration design v0.2 | `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c` | 6 |

Each manifest had a final LF, canonical rows, the exact row count, unique
sorted paths, and matching target hashes. The exact auxiliary assembly report,
runtime/preloader v0.4 rereview preservation record, and predecessor
v0.1/v0.2/v0.3 schemas reproduced their required SHA-256 pins:

- `520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005`;
- `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- `92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af`;
- `e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f`;
  and
- `1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd`.

No F0 path content or filename was opened, listed, searched, quoted,
summarized, or used. No builder/reviewer conversation, CONTROL summary,
hidden result, provider, model, native API, network, live process path,
executor output, score, or oracle was used.

## 3. `ARPNP-INT-IR-001` disposition

Disposition: `CLOSED` at the bounded candidate level.

The corrected `_verify_manifest` performs the following ordered checks for
each of the runtime/preloader implementation, integration v0.1, and
integration v0.2 closure maps before the bridge can be called:

1. require the exact mapping container type to be `dict` or
   `mappingproxy`;
2. copy `targets.items()` to a private tuple;
3. require every key to satisfy `type(path) is str` and every value to satisfy
   `type(value) is bytes`;
4. copy those exact pairs into a new private dictionary and expose it only
   through `MappingProxyType`; and
5. perform all target hash and exact-path-set checks against that immutable
   snapshot, not the caller-owned mapping.

The exact-type predicates reject `bytearray`, `memoryview`, a `bytes`
subclass, and a `str` subclass. A mapping subclass is also rejected. Exact
`dict` and exact `mappingproxy` inputs remain admitted.

An independent in-memory matrix exercised eight cases against each of the
three maps: `bytearray`, `memoryview`, `bytes` subclass, `str` subclass,
changed bytes, a missing target, an extra target, and a `dict` subclass. All
24 cases returned only `OFFLINE-NEW`, `OFFLINE-REJECTED`, retained
`candidate_only=true`, `native_api_reachable=false`, and
`rehearsal_pass=false`, and called the bridge zero times.

Three additional deterministic probes mutated the caller-owned map during
the first target hash, once per closure field. In every probe, the mutation
occurred only after item capture and private snapshot construction. Hashing
continued from the unchanged private snapshot and the mocked offline bridge
was called exactly once. This distinguishes snapshot isolation from merely
hashing the caller-owned mapping. A real authenticated happy path also called
the real bridge exactly once and returned the exact success trace.

The added candidate test covers `bytearray`, `memoryview`, and a `str`
subclass across all three maps. The independent matrix supplies the additional
`bytes`-subclass, mapping-subclass, per-map changed/missing/extra, and
during-hash mutation evidence required for this rereview.

## 4. Non-regression and authority-boundary findings

No new finding was identified.

The exact candidate-path diff from the prior reviewed commit
`f16c68dbc6e28b2483eff7b940ebf890a1d26402` changes only the target snapshot
and exact-type correction, its focused regression test, and the corresponding
candidate manifests/report records. The verifier source and candidate package
exports are unchanged.

The candidate still authenticates all three closure maps before its sole
high-level `prepare_assembly_runtime_launch` bridge call. Its public signature
has exactly six required keyword-only parameters and no callback, executable,
path, process, provider, network, native, backend, loader, or other dependency
injection parameter. Independent AST inspection found exactly one syntactic
bridge call and no ambient filesystem, native, process, or network import or
call surface.

The bridge still reauthenticates the exact assembly implementation and
runtime/preloader v0.4 design closures. The downstream preloader path still
copies exact byte mappings, snapshots static material, constructs only an
offline plan, and fixes `candidate_only=true` and
`native_api_reachable=false`. The candidate does not call the standalone
profile validator, native preloader, admission diagnostic, source-audit API,
or any live consumer.

Success remains exactly:

1. `OFFLINE-NEW`;
2. `OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED`;
3. `OFFLINE-PLAN-VALIDATED`; and
4. `OFFLINE-DIAGNOSTIC-COMPLETE`.

Rejection remains exactly `OFFLINE-NEW`, `OFFLINE-REJECTED`. Every returned
diagnostic is byte-bound and fixes `candidate_only=true`,
`native_api_reachable=false`, and `rehearsal_pass=false`. A bridge result that
purports to carry live reachability is converted to the rejected trace. No
offline result can transition into or authorize the separately designed live
state machine.

## 5. Test evidence

The exact candidate verifier was rerun with the observed lowercase
implementation-manifest SHA-256 and exited zero. It reported:

- candidate manifest and exact rows: PASS, `3`;
- predecessor pin and target authentication: PASS, `32/11/6/5/6`;
- snapshot-only execution: PASS;
- original-input pre/post swap sentinel: PASS;
- focused tests: PASS, `6/6`;
- candidate native/process/network/provider calls: `0`;
- verifier orchestration process:
  `authenticated-snapshot-python-unittest-runner`; and
- rehearsal pass: `false`.

Independent evidence added:

- exact-type and pre-call mutation rejection: PASS, `24/24`;
- rejection bridge count: `0` in every case;
- private immutable snapshot-before-hash probes: PASS, `3/3` maps;
- exact `mappingproxy` happy-path bridge count: `1`;
- authenticated real happy-path bridge count: `1`;
- sole candidate source bridge call: `1`;
- dependency-injection parameters: `0`; and
- fixed offline traces and authority flags: PASS.

All additional synthetic values were PUBLIC and in memory. The only child
process was the candidate verifier's explicitly reported isolated Python
unittest orchestration. No native, provider, network, model, or live candidate
path was invoked.

## 6. Limits

This rereview did not authenticate a build or Python interpreter/runtime
closure, compile or load a binary, execute native preloader behavior, create a
root or process through the candidate, test Windows handle inheritance,
exercise `CreateProcessW` or `NtCreateFile`, run a platform probe, install a
live guard, issue or consume a witness, perform a commit handshake, execute an
official assembly rehearsal, run S0 or E0, access F0, or use a hidden oracle.

The current Python interpreter was used only for bounded offline test
orchestration. It is not promoted to an authenticated runtime package. Passing
unit tests and offline diagnostic construction are not live-safety or
rehearsal evidence.

## 7. Next CONTROL action

CONTROL may record `ARPNP-INT-IR-001` as independently closed for this exact
revision. It may then separately consider whether to open the
`build-and-runtime-materialization` gate. This rereview does not open that
gate and does not authorize source/build/binary/import review, a real-Windows
platform probe, a live candidate, an official rehearsal, F0, S0, E0, commit,
push, PR, merge, release, central-system, or production work.
