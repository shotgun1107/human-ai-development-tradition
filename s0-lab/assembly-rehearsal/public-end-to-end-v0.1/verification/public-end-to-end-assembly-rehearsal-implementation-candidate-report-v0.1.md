# S0 v0.14 public end-to-end assembly rehearsal bounded implementation candidate report v0.1

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BOUNDED PUBLIC IMPLEMENTATION CANDIDATE OPEN`
- `report_kind`: public implementation-candidate and offline verification report only
- `base_commit`: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- `base_tree`: `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- `implementation_manifest_sha256`: `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`
- `design_package_manifest_sha256`: `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802`
- `design_independent_review_sha256`: `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137`
- `implementation_status`: bounded public candidate implemented and offline-tested
- `live_runtime_status`: fail-closed before launch or output mutation
- `official_rehearsal_status`: not executed
- `rehearsal_pass`: false
- `F0_content_access`: none

## 1. CONTROL disposition

`IMPLEMENTATION-CANDIDATE-COMPLETE; LIVE-PLATFORM-GATE-BLOCKED`

The authenticated public candidate now contains the controller, exact request
and one-row request manifest, exact-answer stub, child bootstrap, verifier
observer, Win64 publication adapter, live consumer, implementation manifest,
and offline tests required to review the assembly boundary.

This is not an official rehearsal PASS and is not yet eligible for live
platform execution. The effective v0.3 plus v0.4 plus v0.5 design does not
freeze an authenticated CPython, standard-library, or `jsonschema` transitive
runtime closure. It also does not define a neutral preloader that can
authenticate the verifier, bootstrap, Python executable, and runtime profile
before importing or executing them. The live harness therefore rejects before
creating an output root, starting a child, binding Win32, or calling
`MoveFileExW`.

## 2. Authenticated authority and scope

The candidate was built from exact Git commit
`41e0b684a7cca387be6d264c4a5b63de2561fd7c` and tree
`a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`. The effective design authority is
v0.3 plus the v0.4 replacements plus the v0.5 replacements. The v0.5 design
package and independent rereview reproduced the two external hashes recorded
above.

The assembly implementation manifest has exactly 32 unique canonical rows,
5,280 bytes, and SHA-256
`0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`.
Every row existed as a regular public file and matched its recorded SHA-256.
The parent authentication path also reproduced the full I0, I1, I2, and I3
implementation-manifest inventories as 15, 26, 16, and 17 rows. The child
source allowlist is narrower: the actual authenticated import closures are
7, 7, 7, and 8 Python files.

No F0 content or filename was opened, listed, searched, quoted, summarized,
derived from, or supplied to another role. No hidden oracle, fixture author,
executor, judge, provider/model, network, or S0/E0 input was used.

## 3. Implemented candidate

The public implementation contains these authority-separated parts:

1. A child controller with the exact ten-state sequence, fixed request
   reconstruction, I0 authentication/transform/answer validation, I1 external
   manifest grant and one-shot invocation, I2/I3 contract authentication,
   deterministic run-record-v3 construction, four-name output reservation,
   cleanup/quarantine diagnostics, and exactly two publication requests.
2. A candidate-owned eager one-frame stub with no retry and exact counters
   `1/1/1/1/0`.
3. A verifier-parent observer with one private capability, exact ordered ASCII
   IPC, two 23-field immutable move events, pre/post file identity continuity,
   and a private one-use witness.
4. A literal Win64 `MoveFileExW` adapter with exact `WinDLL`, export,
   `argtypes`, `restype`, extended paths, numeric flags zero, last-error reset,
   immediate failure capture, success sentinel, local fixed NTFS check,
   alternate-stream rejection, reparse rejection, and single-link file check.
5. A same-process live consumer that atomically spends the witness on the
   first terminal attempt, verifies current identities and exact bytes, and
   issues a non-publicly-constructible process-local decision only for an
   authenticated real backend.
6. A standalone `-I -S -B` child bootstrap and parent harness. The parent
   authenticates the external implementation pin, current design and review,
   component manifests, required component source closures, the 90-row public
   bundle, fixed inputs, request, candidate, verifier, and source audits before
   any diagnostic child launch.
7. Import, open, directory, FFI, network, process, publication, and filesystem
   mutation sentinels. A denied operation is latched; later substantive stages
   cannot recover by catching the first exception. Cleanup retains only the
   exact four owned output names and output-root enumeration exception.

The controller performs no fallible candidate operation after the second
parent `OK\n`. Candidate controller `COMPLETE` remains diagnostic-only and is
not rehearsal PASS.

## 4. Exact reconstructed objects

| Object | Verified result |
|---|---|
| request | 8 fields, 7,917 bytes, SHA-256 `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2` |
| request manifest | 135 bytes, SHA-256 `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7` |
| run-record-v3 | 38 fields, 2,224 bytes, SHA-256 `73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6` |
| receipt-v2 with the three current external pins | 21 fields, 1,173 bytes, SHA-256 `33ba242af401116a1c9905a2b8eb7d7fef442e7630b240ef44e702918d9ea456` |

The receipt bytes were reconstructed in memory for verification. They were not
published as a rehearsal result and do not supply a witness or PASS authority.

## 5. Offline verification results

All 47 repository tests passed:

| Suite | Tests | Result |
|---|---:|---|
| candidate | 22 | PASS |
| verifier | 17 | PASS |
| process harness | 8 | PASS |
| total | 47 | PASS |

The tests cover strict JSON and exact canonical bytes, every run-record and
receipt field mutation, external pin forms, exact stub counters, second-entry
and double-close behavior, exact IPC order and hostile frames, all ten states,
failure-class and call-count routing, cleanup and quarantine, component
manifest mutations, denied-boundary precedence, latched runtime violations,
source-audit mutations, ABI signature mutations, capability/witness copying
and serialization, copied pairs, final-file replacement, trace mutations,
wrong child/pipe/root, witness replay, rejected-attempt retry, fake backend
rejection, live-decision fabrication, exact failure diagnostic parsing, fresh
output-root creation, and unconditional live fail-closed behavior.

An additional diagnostic-only same-process integration loaded the actual
public I0-I3 implementations from their authenticated source manifests. It
called only the named assembly APIs once each, produced the exact 2,224-byte
record and 1,173-byte receipt, and observed the two publication requests in
order. A test-only `os.rename` channel was used, so this result is explicitly
`offline-not-success-diagnostic-only`, with `rehearsal_pass=false`. It is not
Win32 publication evidence.

The isolated `-I -S -B` bootstrap was also executed without an admitted
runtime profile. It emitted no publication request, made no output change, and
failed closed as required.

## 6. Adversarial defects found and corrected

Implementation review found and corrected the following concrete defects:

- a pre-move publication failure could be mislabeled quarantined because
  cleanup removed the pending file before resolving uncertain ownership;
- Python `bool` values could satisfy integer stub counters;
- a rejected live-consumer attempt did not initially spend its witness;
- a second stub entry could expose `transport_calls=2`;
- component import could relabel `BoundaryViolation` as authentication failure;
- component authentication initially read every manifest row rather than only
  the named API closure;
- a fake or structurally forged backend and directly constructed live decision
  could approach live acceptance;
- runtime violations were not latched;
- the Win32 preflight omitted fixed-drive, root alternate-stream, and hardlink
  checks;
- the initial source audit was too weak against alternate loaders, exports,
  extra calls, retry/fallback paths, type mutations, and delayed last-error
  capture;
- the bootstrap initially omitted the bundle metadata root and admitted a
  caller-controlled dependency path;
- the parent initially accepted an arbitrary live Python executable;
- the first harness form lost exact child failure diagnostics and accepted an
  already-created output directory; and
- early child closure lists omitted transitive authenticated component files.

Regression tests now cover each corrected class. These corrections do not
provide live-platform evidence.

## 7. Remaining unverified claims and blockers

The following remain unverified:

1. actual `MoveFileExW` behavior on the supported Windows 10/11 local fixed
   NTFS profile;
2. the full real collision, interruption, reparse, alternate-stream,
   cross-volume, network, removable-media, and file-replacement matrix;
3. two fresh deterministic real executions and same-process live-consumer
   acceptance;
4. authentication of the exact Python executable, CPython runtime, standard
   library, extension modules, `jsonschema`, and its transitive dependencies;
5. pre-import authentication of verifier and bootstrap bytes by a neutral
   launcher; and
6. a fresh independent implementation rereview of the final manifest.

Items 4 and 5 are blocking prerequisites for any live or official rehearsal
execution. They are not safely supplied by checking a package version,
accepting an arbitrary dependency directory, trusting the current interpreter,
or self-hashing after verifier import.

## 8. Facts, inferences, proposals, and claim limit

- Facts are the Git identity, exact public hashes, manifest authentication,
  source inventory, and test outputs reported above.
- Test results are the 47 offline tests, parent authentication, AST parse, the
  actual-component diagnostic flow, and the isolated bootstrap fail-closed
  result.
- The CONTROL inference is that the bounded public implementation candidate is
  complete enough for independent implementation rereview, but not eligible
  for live-platform or rehearsal execution.
- The proposal is a minimal public design supplement that freezes the runtime
  profile manifest/schema, exact executable and dependency closure, neutral
  preloader, launch flags/environment, path normalization, and runtime audit
  event policy. That supplement requires its own fresh independent design
  review before code may open the live path.

The maximum claim is public bounded implementation-candidate completion and
offline verification only. This report does not establish official rehearsal
PASS, S0, E0, F0 isolation under execution, provider/model behavior, a hidden
oracle, executor/judge independence, central-system implementation, Project
Brain integration, operational safety, economic value, production readiness,
or model-to-model transfer.

## 9. Recommended next gate

The next action should not be official rehearsal execution. The smallest safe
next step is a public runtime-profile and neutral-preloader design supplement,
followed by a fresh independent review of that supplement and this exact
implementation manifest.

No commit, push, PR, release, or `main` integration is authorized by this
report.
