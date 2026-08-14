# S0 v0.14 public end-to-end runtime/preloader bounded integration implementation v0.1 independent review

Status: fresh independent PUBLIC implementation/security review; offline candidate only

## 1. Verdict and finding counts

Verdict: `PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`

- BLOCKING: 0
- MAJOR: 0
- MINOR: 1

This verdict is limited to the exact candidate commit and authenticated public
inputs below. It does not establish rehearsal PASS, S0 or E0 execution, live
or native safety, runtime materialization, a trusted build, platform behavior,
F0 isolation under execution, production readiness, the central system,
Project Brain integration, operational safety, economic value, or
model-to-model transfer.

## 2. Authenticated baseline and input inventory

- worktree: `C:\tmp\s0i14-review`;
- branch: `codex/s0-assembly-rpnp-integration-implementation-v01-review`;
- reviewed HEAD: `f16c68dbc6e28b2483eff7b940ebf890a1d26402`;
- candidate remote ref:
  `refs/remotes/origin/codex/s0-assembly-rpnp-integration-implementation-v01`;
- candidate remote ref value:
  `f16c68dbc6e28b2483eff7b940ebf890a1d26402`;
- initial tracked, staged, and untracked anomaly counts: `0 / 0 / 0`.

The candidate's implementation manifest is SHA-256
`1c225e0cb4480aadf5309e59634e086d0c3fbf6df6977522d61249a14796d35d`.
It contains exactly three unique ASCII-sorted rows, and all three targets
matched. The candidate verification manifest is SHA-256
`c94f6b470d1102f43e4c22aa738460c22469da0af7fc027ef743dfe1e9119e31`;
its four targets matched. All eight candidate files at the reviewed commit
were read.

The externally pinned predecessor manifests reproduced exactly and every
target was authenticated before semantic reliance:

| Public closure | Manifest SHA-256 | Exact rows |
|---|---|---:|
| assembly implementation v0.1 | `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623` | 32 |
| runtime/preloader implementation v0.3 | `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2` | 11 |
| runtime/preloader design v0.4 | `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589` | 6 |
| integration design v0.1 | `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b` | 5 |
| integration design v0.2 | `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c` | 6 |

Each manifest had canonical row form, exact count, unique sorted paths, and
matching target hashes. The assembly candidate report, runtime/preloader v0.4
rereview preservation record, and predecessor v0.1/v0.2/v0.3 schemas also
matched their supplied pins:
`520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005`,
`9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`,
`92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af`,
`e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f`,
and `1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd`.

The exact allowlist was fully read. No F0 path content or filename was opened,
listed, searched, quoted, summarized, or used.

## 3. Independent methodology

The review reconstructed behavior from authenticated repository bytes without
using builder conversation, a prior reviewer result, CONTROL summary, hidden
result, provider, model, network, native API, or live process path. It:

1. audited the effective integration v0.1 plus v0.2 offline boundary and the
   retained runtime/preloader v0.4 constraints;
2. traced candidate imports, public parameters, bridge call sites, result
   construction, and verifier snapshot/process separation;
3. ran the exact candidate verifier against the externally observed three-row
   manifest pin;
4. ran an additional in-memory adversarial matrix for manifest and target
   mutations, bridge ordering/count, exact traces, fixed result flags, source
   imports/calls, and forbidden dependency-injection parameters; and
5. constructed one non-exact mutable-target counterexample for the finding
   below.

All synthetic values used by the tests were public and in memory. No S0/E0,
executor, score, hidden oracle, native/provider/network call, root creation,
platform probe, or official rehearsal occurred.

## 4. Predecessor-claim disposition

The candidate preserves the effective offline integration claims except for
the MINOR exact-type gap below.

- All 32/11/6/5/6 manifest closures are authenticated in the verifier before
  candidate import. The child receives a materialized byte snapshot and its
  imports resolve from snapshot paths, not the original workspace.
- The candidate authenticates the runtime/preloader and both integration
  design closures before its sole high-level bridge call. The high-level
  bridge reauthenticates the assembly and runtime/preloader v0.4 closures in
  the same call and privately snapshots runtime material.
- The candidate never calls the standalone runtime-profile validator,
  `NeutralPreloader.prepare`, admission diagnostic, or source-audit API. It
  exposes no callback, executable, dependency-root, path, subprocess,
  observer, consumer, backend, or loader injection parameter.
- Candidate source has no ambient filesystem, `PATH`, `PYTHONPATH`, provider,
  model, network, native, output-root, or process surface. Its one admitted
  bridge is called at most once and never before closure authentication.
- Success has exactly `OFFLINE-NEW`,
  `OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED`, `OFFLINE-PLAN-VALIDATED`, and
  `OFFLINE-DIAGNOSTIC-COMPLETE`. Rejection has exactly `OFFLINE-NEW` and
  `OFFLINE-REJECTED`.
- Every returned diagnostic is byte-bound and fixes
  `candidate_only=true`, `native_api_reachable=false`, and
  `rehearsal_pass=false`.
- The verifier's one Python unittest subprocess is orchestration, not
  candidate runtime behavior. The verifier reports that distinction and does
  not claim a native/provider/network candidate call.

## 5. Findings

### ARPNP-INT-IR-001 - MINOR - mutable manifest target values pass as exact bytes

Evidence: `candidate.py` lines 43-56 exact-type the mapping container, but
line 53 passes each value directly to `hashlib.sha256` without requiring
`type(value) is bytes` or taking a private byte snapshot.

The integration boundary requires original raw bytes and exact byte mappings
in the same operation. A deterministic counterexample replaced one
authenticated runtime/preloader target value with a `bytearray` containing
the same bytes. Closure verification passed, the bridge was called, and the
candidate returned the full success trace with `failure_class=null`.

Impact is MINOR because these closure target values are used only to verify
the public design/implementation closures and are not forwarded to the bridge
or converted into live authority. The returned result remains candidate-only,
native-unreachable, and non-PASS. The gap nevertheless makes the report's
"exact byte mappings" claim too broad and admits caller-mutable material at
the public boundary.

Smallest correction: before hashing, require every target key to have exact
type `str` and every target value exact type `bytes`; preferably copy the
three mappings into private immutable mappings at entry. Add bytearray and
memoryview rejection tests for each closure.

## 6. Test evidence

The exact verifier completed with exit code zero:

- candidate manifest and rows: PASS, `3`;
- predecessor pin and target authentication: PASS, `32/11/6/5/6`;
- snapshot-only execution: PASS;
- original-input pre/post swap sentinel: PASS;
- focused tests: `5/5 PASS`;
- candidate native/process/network/provider calls: `0`;
- verifier orchestration process:
  `authenticated-snapshot-python-unittest-runner`;
- rehearsal pass: `false`.

The independent in-memory matrix added 16 rejection cases. Changed, missing,
extra, duplicate, reordered, uppercase, and malformed manifest material, plus
changed/missing/extra targets in each of the three candidate closure mappings,
all produced only the rejected trace and called the bridge zero times. The
authenticated happy path called the bridge exactly once and retained the
three fixed authority flags. AST/signature checks found no forbidden candidate
import, filesystem/process/network/native call, or dependency-injection
parameter.

## 7. Limits

This review did not authenticate a build or interpreter/runtime closure,
compile or load a binary, execute native preloader behavior, test Windows
handle inheritance, exercise `CreateProcessW` or `NtCreateFile`, materialize
an atomic root, run a platform probe, or execute an official assembly
rehearsal. The verifier uses the current Python interpreter only as explicitly
reported test orchestration; this review does not promote it to an
authenticated runtime package.

## 8. Exact next gate

CONTROL should explicitly disposition `ARPNP-INT-IR-001`; the smallest safe
action is to apply the exact-byte/snapshot correction and preserve a focused
regression test. Subject to that disposition, this review makes only the
separately opened `build-and-runtime-materialization` gate eligible for
consideration. It does not open that gate or any source/build/binary/import,
real-Windows platform-probe, live-candidate, official rehearsal, F0, S0, E0,
central-system, production, commit, push, PR, or release gate.
