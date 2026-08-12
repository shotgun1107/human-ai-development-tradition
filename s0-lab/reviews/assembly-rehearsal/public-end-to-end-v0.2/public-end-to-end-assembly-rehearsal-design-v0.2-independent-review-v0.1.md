# S0 v0.14 public end-to-end assembly rehearsal design v0.2 independent review v0.1

- `review_role`: fresh public-only independent design reviewer
- `review_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.2 INDEPENDENT REVIEW OPEN`
- `review_head`: `18a9562a9da48ce5743fc183c8c68c15d00cf249`
- `review_kind`: design review only; no implementation or rehearsal execution
- `F0_content_access`: none
- `verdict`: `REVISE-AND-REVIEW`

## 1. Verdict

`REVISE-AND-REVIEW`

The v0.2 proposal closes B-01, B-02, B-03, M-01, M-02, and M-03 at
proposal-text level. The exact request, one-row manifest, I1 grant, ten-state
success path, fixed-stub exhaustion rule, and 36-field success record are now
independently reconstructable.

One prior major, M-04, remains open, and this review finds three new majors.
The publication path does not yet assign one stable class and call count to
all final-path collision timings; the unnamed primitive does not freeze the
platform and crash-durability meaning of successful publication; a failed
cleanup can leave byte-for-byte pass-valued pending evidence without a frozen
consumer rule; and the success record omits the assembly implementation,
reviewed v0.2 design, and close-counter provenance needed to bind the retained
record to the code and stub behavior that allegedly produced it.

Finding counts are: zero blocking, four major, and zero minor.

This verdict is only a public design-review result. It is not an
implementation, rehearsal, provider/model call, I2/I3 import, role-isolation
test, S0 result, central-system result, or Project Brain result.

## 2. Authenticated basis

Repository authentication completed before substantive review:

| Check | Authenticated value | Result |
|---|---|---|
| origin | `https://github.com/shotgun1107/human-ai-development-tradition.git` | PASS |
| branch | `codex/s0-public-assembly-rehearsal-design-v02-review` | PASS |
| HEAD | `18a9562a9da48ce5743fc183c8c68c15d00cf249` | PASS |
| remote candidate | `18a9562a9da48ce5743fc183c8c68c15d00cf249` | PASS |
| initial tracked worktree/index differences | `0` | PASS |
| initial untracked entries | `0` | PASS |

The current root `AGENTS.md` SHA-256 was
`7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86`.
The readiness audit and every v0.1/v0.2 design or review artifact with an
available replacement-extension sidecar passed exact sidecar filename,
format, and content-hash checks.

| Artifact | SHA-256 | Result |
|---|---|---|
| I0-I3 readiness audit v0.1 | `0ca3e51e8a566a94ed168325d18f5fe6196a132de5c4c6979c8ab7348483ffbf` | PASS |
| v0.1 design | `67a49650219b7587f2698c869336f8a767c55a787235c379b643268a9ec2879a` | PASS |
| v0.1 interface map | `9758ccd14acbf7e5463bff37e4c6f4a20a073cec7196f35af62a3341f253ce8b` | PASS |
| v0.1 acceptance plan | `a2f4b07606d673ec474a6faa138115aaadd576b29493be632dc75ce307377971` | PASS |
| v0.1 review brief | `ae8689a64ce72a60d796e1e8d05d66b5ba65c2d2e5ae9f91cd2ca2c588f96760` | PASS |
| v0.1 official independent review | `9bb097acba46bfcfd6eee88ffbf0e41709f371f08fbd2226f6bdb86b615f95dd` | PASS |
| v0.2 design revision | `70b0a29327dc73a9b5268ea6146ecfe7e82c2709c856190a531c3a338e065475` | PASS |
| v0.2 interface map | `31417e75f5f4e40e12fea02cbd21b4d1a0908e938f911b75f34ee773a6c50f76` | PASS |
| v0.2 acceptance plan | `d68d83d234a158952333a580404207b871f9dd0de1bc28870eb37e016a191edf` | PASS |
| v0.2 review brief | `011dabcae4f6e77b35485d6334262067b24c1cf34e1e6328d147138f1b38ec3a` | PASS |
| v0.1 review response | `9dcb2d2e68f9812712075f529f4f84afb77683b2457cdd8c11a866d7a71107f4` | PASS |

All four implementation manifests and every listed row authenticated before
source reliance:

| Component | Manifest SHA-256 | Rows | Format/missing/hash failures |
|---|---|---:|---:|
| I0 | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` | 15 | 0 |
| I1 | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | 26 | 0 |
| I2 | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` | 16 | 0 |
| I3 | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | 17 | 0 |

The public bundle manifest SHA-256 was
`e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637`.
It contained exactly 90 canonical, unique, contained rows. All 90 files were
present and matched their listed hashes; the bundle root contained exactly
those 90 files plus the manifest, with zero unlisted files.

| Fixed input | Bytes | SHA-256 | Result |
|---|---:|---|---|
| canonical B2 input | 4,276 | `bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863` | PASS |
| P01 B2 package | 4,518 | `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7` | PASS |
| B2 questions | 3,182 | `661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90` | PASS |
| public P01 response | 1,936 | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` | PASS |
| answer schema | 2,167 | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | PASS |
| I2 public contract | authenticated | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | PASS |
| I3 public contract | authenticated | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` | PASS |

## 3. Method and boundary

This review used the authenticated public design inputs, the four component
READMEs, the full public-bundle manifest and row authentication, and only the
manifest-listed source needed for I0 bundle verification/transform/answer
validation, I1 manifest-grant/request authentication/strict one-shot behavior,
and I2/I3 contract verification. Component tests, component verification
reports, and the rehearsal were not run.

The request, request-manifest, grant-binding, and success-record bytes were
reconstructed in memory from authenticated source bytes and the documented
canonical serialization rules. No request, response, stub, controller, run
record, fixture, oracle, executor, or judge artifact was created. No provider,
model, network, browser, MCP, or web service was invoked.

The three F0 content families remained denied. Their contents and individual
filenames were not opened, searched, enumerated, quoted, hashed, summarized,
or used. Facts below are authenticated byte/source observations. Review
conclusions and required revisions are labeled separately.

## 4. Independent reconstruction

### 4.1 Exact request and manifest

Parsing the authenticated 4,518-byte package and 3,182-byte question object,
constructing the exact eight-field envelope, recursively sorting object keys,
using `ensure_ascii=true` and compact separators, and adding one ASCII LF
produced:

- request length: `7,917` bytes;
- request SHA-256: `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2`.

The independently constructed manifest row was the lowercase request digest,
two ASCII spaces, the exact request path, and one LF. It produced:

- manifest length: `135` bytes;
- manifest SHA-256: `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7`.

These values match the v0.2 package exactly.

### 4.2 Full I1 grant identity

The actual I1 grant binding contains:

| Grant field | Exact value |
|---|---|
| manifest path | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/request-files.sha256` |
| manifest SHA-256 | `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7` |
| entry prefix | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/` |
| allowed count | `1` |
| allowed path | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/request.json` |
| purpose | `s0-public-assembly-rehearsal-v01` |

Applying I1's exact `I1-EXTERNAL-MANIFEST-GRANT-1` line binding produced 400
ASCII bytes and grant identity SHA-256
`98109a80d3e97e121cd3c6efc31c8c12a350b43884a302c000eabad761cb0f26`.
I1 then requires the same object identity and the separately supplied
authority digest, manifest path, request path, and purpose at runner entry.
M-01 is closed.

### 4.3 Full-bundle and fixed-case boundary

Authenticated I0 source confirms that `verify_public_bundle` resolves only the
public-practice v0.1 root, recursively discovers its metadata, rejects
symlinks, compares the discovered regular-file set with the exact 90-row
manifest, reads and hashes every row, parses every JSON row, and checks both
public blocks. The v0.2 allowlist admits exactly that manifest and those 90
rows, plus directory metadata traversal only under that root. The fixed B2/P01
case files are selected only after full-bundle verification.

This positive traversal does not require F0 or an otherwise unclassified file.
B-01 is closed at proposal-text level.

### 4.4 Stub, close exhaustion, and call counters

Authenticated I1 source stops at the first final frame and invokes `close()`
on the actual iterator in `finally`; it does not generically consume or detect
a later frame. The v0.2 proposal correctly moves trailing-frame evidence into
the exact candidate-owned iterator.

| Tabletop | Observed counters `(calls/script/yielded/close/unconsumed)` | Outcome |
|---|---|---|
| one exact final frame | `1/1/1/1/0` | I1 can return; later exact response and answer checks remain required |
| correct final then one trailing scripted frame | `1/2/1/1/1` | stub `close()` raises; I1 propagates cleanup failure; `AR-INVOKE` |
| no final frame in one scripted frame | `1/1/1/1/0` | I1 rejects incomplete stream; `AR-INVOKE` |
| request rejected by I1 authority validation | `0/1/0/0/not-computed` | stub is not entered; `AR-INVOKE` |
| second stub entry | counter advances to `2` before rejection | `AR-INVOKE`; never a successful one-call run |

The proposal therefore no longer attributes generic trailing-frame detection
to I1, and B-02 is closed. M-07 below concerns the retained evidence for this
rule, not whether the fixed stub can implement it.

### 4.5 Ten states and zero/one-call accounting

The successful order is exactly:

`NEW -> PREFLIGHT_AUTHENTICATED -> REQUEST_RECONSTRUCTED -> OUTPUT_RESERVED -> RUNNER_ENTERED -> INVOKED_ONCE -> RESPONSE_CAPTURED -> ANSWER_VALIDATED -> TEMP_RECORD_VERIFIED -> COMPLETE`.

The controller sets `RUNNER_ENTERED` immediately before calling I1. It does
not infer transport entry from that controller state. I1 request rejection can
therefore truthfully remain at `RUNNER_ENTERED` with zero stub calls. Stub
entry, iteration, bounds, strict-JSON, or close failure remains at
`RUNNER_ENTERED` with one observed call. `INVOKED_ONCE` is reached only after a
successful I1 return and successful counter check. M-03 is closed.

### 4.6 All 36 successful-record values

Independent construction produced exactly these values:

| # | Field | Value |
|---:|---|---|
| 1 | `actual_response_sha256` | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` |
| 2 | `answer_validation_error_count` | `0` |
| 3 | `block_id` | `BLK-PRACTICE0002` |
| 4 | `bundle_manifest_sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` |
| 5 | `canonical_sha256` | `bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863` |
| 6 | `claim_kind` | `public-model-free-assembly-rehearsal-only-not-s0` |
| 7 | `denied_input_access_count` | `0` |
| 8 | `design_base_commit` | `f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c` |
| 9 | `design_revision` | `0.2` |
| 10 | `expected_response_sha256` | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` |
| 11 | `final_frames` | `1` |
| 12 | `i0_manifest_sha256` | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` |
| 13 | `i1_manifest_sha256` | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` |
| 14 | `i2_disposition` | `contract-authenticated-no-import-route` |
| 15 | `i2_manifest_sha256` | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` |
| 16 | `i3_disposition` | `contract-authenticated-no-import-attempt` |
| 17 | `i3_manifest_sha256` | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` |
| 18 | `package_sha256` | `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7` |
| 19 | `public_bundle_entry_count` | `90` |
| 20 | `questions_sha256` | `661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90` |
| 21 | `rehearsal_id` | `S0-PUBLIC-AR-B2-P01-001` |
| 22 | `representation_id` | `P01` |
| 23 | `request_manifest_path` | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/request-files.sha256` |
| 24 | `request_manifest_sha256` | `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7` |
| 25 | `request_path` | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/request.json` |
| 26 | `request_sha256` | `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2` |
| 27 | `response_frames` | `1` |
| 28 | `result` | `public-assembly-rehearsal-pass-not-s0` |
| 29 | `retry_count` | `0` |
| 30 | `schema_id` | `S0-PUBLIC-ASSEMBLY-RUN-RECORD-2` |
| 31 | `state` | `COMPLETE` |
| 32 | `stub_script_frame_count` | `1` |
| 33 | `stub_transport_id` | `S0-PUBLIC-EXACT-ANSWER-STUB-1` |
| 34 | `stub_unconsumed_frame_count_on_close` | `0` |
| 35 | `stub_yielded_frame_count` | `1` |
| 36 | `transport_calls` | `1` |

Canonical ASCII serialization with sorted keys, compact separators, and one
LF produced exactly 2,046 bytes and SHA-256
`bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`.
The object, length, and hash all match the v0.2 interface map. M-02 is closed
as an exact-value finding; M-07 concerns omitted provenance fields.

### 4.7 Publication semantics

The proposed positive order is sound in its core commit discipline: reserve
`run-record.pending`, write/fsync/close it, reopen and compare exact bytes and
hash, then perform one no-replace move in the same directory and perform no
fallible success check afterward. This closes the original B-03 scenario in
which final pass-valued bytes were written before read-back verification.

The proposal also says every prepublication failure removes pending, a
collision preserves a prior final, and cleanup failure is separately
diagnosed. Sections 5 and 6 explain why the remaining collision, residue,
durability, and provenance rules are not yet exact enough for implementation
consideration.

### 4.8 I2/I3 no-import disposition and closed boundaries

The exact I2 `verify_contract_file` authenticates its contract digest and
public construction bindings. That contract expressly blocks complete import
validation, durable ledger, project-lifetime uniqueness, atomic append,
witness validation, actual registry authority, and platform enforcement. The
exact I3 `verify_contract_file` authenticates its contract digest and I2
bindings. I3 likewise leaves durable ledger, atomic append, witness,
registry/platform authority, protected material, F0, and E0/S0 closed.

For repository-resident public-practice data, the only truthful dispositions
are therefore:

- `i2_disposition=contract-authenticated-no-import-route`;
- `i3_disposition=contract-authenticated-no-import-attempt`.

No I2 route/event/ledger/witness/identifier or I3
admission/outcome/classification/completion/destination authority is created.
Any such creation is `AR-BOUNDARY`. The wider denied set remains F0, hidden
oracle, provider/model/network/tools, executor/judge/scoring/condition map,
keys/signatures/trust activation, signer media, VM/ACL, E0/S0, central system,
and Project Brain.

## 5. Prior finding dispositions

| Finding | Disposition | Independent conclusion |
|---|---|---|
| B-01 | CLOSED | Actual I0 recursive traversal fits exactly the authenticated manifest plus all 90 rows and approved metadata traversal; it needs no F0 or unclassified content bytes. |
| B-02 | CLOSED | Generic I1 trailing detection is disclaimed. The exact stub's iterator close can reject a correct final followed by one unconsumed scripted frame. |
| B-03 | CLOSED for the original final-path defect | Exact pass bytes remain pending until close/read-back/hash verification; final creation is the last primitive. M-06 addresses residual pending evidence after failed cleanup. |
| M-01 | CLOSED | All grant fields, one-row manifest bytes/hash, and the derivable grant identity are exact. |
| M-02 | CLOSED for exact serialization | All 36 values reconstruct to the exact 2,046-byte record and frozen hash. M-07 addresses omitted evidence fields, not ambiguity in the listed values. |
| M-03 | CLOSED | `RUNNER_ENTERED` is separate from the stub's first-instruction counter, giving truthful zero-call request rejection and one-call transport/iteration/close failures. |
| M-04 | OPEN, major | Final collision timing, silent close/counter mismatch, and determinism-versus-record-check ordering still permit incompatible primary classes or call counts. |

## 6. Findings

### M-04 (major, carried) - Failure routing is still not unique at three boundaries

**Facts.** The acceptance table says an existing pending or final name is
`AR-RESERVE` with zero calls. The positive sequence exclusively creates only
the pending name and does not freeze an exact pre-invocation final-name check.
The atomic-publication probe separately requires a final collision to preserve
the prior final, while the mutation table says an atomic-publish failure is
`AR-RECORD` with no final file. A final created before the run, between a
non-atomic absence check and invocation, or immediately before the move can
therefore be routed as `AR-RESERVE/0` or `AR-RECORD/1`, and the last form does
leave the prior final present.

I1 also treats a missing/non-callable iterator `close` as successful. The
design requires the exact stub to expose `close_count=1`, but it does not name
the primary class for a post-return close/counter mismatch when I1 itself did
not raise. Finally, an unknown field or nonzero retry changes the exact frozen
record and can be detected either as `AR-DETERMINISM` by a semantic audit or
as `AR-RECORD` by the 2,046-byte/hash check; their order is not frozen.

**Review conclusion.** M-04 is not closed. At least three required mutations
still lack one exact ordered operation, rejecting state, call count, and
primary class.

**Required revision.** Freeze the output-reservation algorithm and distinguish
an initial final collision from a later race collision. Reconcile the
"no final file" assertion with preservation of an existing destination. Add
an exact post-I1 stub-integrity operation and class. Place the deterministic
field audit explicitly before or after canonical record verification and
freeze the resulting precedence.

### M-05 (major, new) - Atomic publication and durability are platform-ambiguous

**Facts.** The design names a semantic placeholder,
`same-volume-atomic-no-replace-move` / `atomic_no_replace_move`, but deliberately
defers its platform implementation. It requires collision safety and a
never-partial destination, yet also calls the published final "durable success
evidence." The frozen sequence fsyncs the file content but does not define the
parent-directory metadata durability step, supported operating-system/filesystem
matrix, power-loss versus process-interruption failure model, or exact primitive
whose guarantees are being relied upon.

**Review conclusion.** Collision/race probes are good future tests, and the
unsupported-host rule prevents a silent fallback. They do not make the word
"durable" or the crash outcome implementation-independent. Two implementations
can satisfy the prose with materially different rename and persistence
guarantees.

**Required revision.** Freeze either one supported platform primitive and its
documented guarantees or an exact per-platform primitive matrix. Define the
failure model, source/destination identity checks, parent-directory persistence
requirement, collision/race result, and prohibited copy/delete fallback. If
power-loss durability is out of scope, replace the durable claim with the exact
weaker observed semantics.

### M-06 (major, new) - Cleanup-failed pending bytes have no frozen evidence-consumer rule

**Facts.** Before publication, `run-record.pending` already contains the exact
2,046-byte object with `state=COMPLETE` and
`result=public-assembly-rehearsal-pass-not-s0`. A write/read-back/publish failure
followed by an unlink failure can leave those exact bytes at the pending path.
The design says `cleanup_status=failed` is recorded separately, but it defines
no canonical failure record or durable association between that diagnostic and
the residual file.

**Review conclusion.** The original B-03 final-path bug is repaired, but the
remaining success predicate is path-conventional rather than fully frozen.
A retained or copied pending file is byte-indistinguishable from the final
record and self-describes as complete. The design does not explicitly require
all consumers to authenticate the final pathname and successful publication
event, nor does it define quarantine or fail-closed handling of residue.

**Required revision.** Freeze the evidence-consumer rule: bytes are never
success evidence without the exact final pathname and authenticated successful
publication outcome. Define how cleanup-failed pending residue is marked,
quarantined, or associated with a failure diagnostic without overwriting it.
Add hostile tests that copy or present pending bytes as a final record and
require rejection.

### M-07 (major, new) - The success record does not bind assembly code, v0.2 design, or close execution

**Facts.** The 36-field record pins I0-I3 manifests and the old
`design_base_commit`, but it contains neither the future assembly
implementation-manifest SHA-256 nor a v0.2 design/interface artifact hash or
reviewed revision commit. `design_revision=0.2` is an unbound label. The record
also omits `stub_close_count`, even though success expressly requires the five
counters `1/1/1/1/0`. I1 itself accepts an iterator without a callable close.

**Review conclusion.** The exact record can be produced by different
controller/stub bytes and does not itself establish that close ran once or
that the producing implementation was the independently reviewed candidate.
An external verifier report may later carry that provenance, but the current
design calls the final record durable success evidence without freezing the
required association.

**Required revision.** Bind the success evidence to the externally pinned
assembly implementation manifest and the reviewed v0.2 successor design
identity. Add `stub_close_count=1` or freeze an equally exact authenticated
companion receipt that binds all five stub counters, the implementation pin,
the design pin, the final-record hash, and the publication outcome. Recompute
and refreeze the canonical success bytes/hash.

### Minor findings

None.

## 7. Failure-class and precedence audit

| First failed ordered operation | Expected primary class | Calls | Review disposition |
|---|---|---:|---|
| denied path/capability or fabricated I2/I3 operation | `AR-BOUNDARY` | 0 or observed current count | Unique override; closed |
| component/bundle/source/schema/contract/request/grant authentication | `AR-AUTH` | 0 | Unique; closed |
| authenticated I0 transform differs | `AR-TRANSFORM` | 0 | Unique; closed |
| exclusive pending creation fails | `AR-RESERVE` | 0 | Unique for pending; closed |
| initial or racing final collision | `AR-RESERVE` or `AR-RECORD` | 0 or 1 | M-04 |
| I1 authority rejection before stub entry | `AR-INVOKE` | 0 | Unique and truthful |
| stub entry/iteration/bounds/strict JSON/close exception | `AR-INVOKE` | 1 | Unique and truthful |
| I1 returns but exact response differs | `AR-RESPONSE` | 1 | Unique |
| I0 answer errors nonempty | `AR-ANSWER` | 1 | Unique |
| pending serialization/write/fsync/close/read-back/hash failure | `AR-RECORD` | 1 | Unique primary; M-06 governs residue |
| atomic publication failure without destination collision | `AR-RECORD` | 1 | Unique if primitive semantics are fixed; M-05 |
| missing close or post-return counter mismatch | not frozen | 1 | M-04/M-07 |
| unknown/nondeterministic field or nonzero retry | `AR-DETERMINISM` or `AR-RECORD` | 1 per execution | M-04 |

Denied access remains the only override. For other operations, cleanup failure
can remain a secondary diagnostic without changing an existing primary, but
an otherwise successful prepublication operation plus failed cleanup must be
`AR-RECORD` and cannot publish success.

## 8. Required hostile traces

| Counterexample | Rejecting state/operation | Calls | Required result | Review result |
|---|---|---:|---|---|
| authenticated manifest but reconstructed package differs | after `PREFLIGHT_AUTHENTICATED`, before `REQUEST_RECONSTRUCTED` | 0 | `AR-TRANSFORM` | Unique and fail-closed |
| denied path introduced through configuration | first normalized attempted access | 0 | `AR-BOUNDARY` | Unique without opening denied content |
| output pending name exists | transition to `OUTPUT_RESERVED` | 0 | `AR-RESERVE` | Unique; no overwrite |
| final name exists before run | reservation/prepublish boundary | 0 or 1 | `AR-RESERVE`, 0 | M-04: exact check/transition is absent |
| request fails I1 authority validation | `RUNNER_ENTERED` | 0 | `AR-INVOKE` | Truthful zero-call evidence |
| stub called once and never produces final | `RUNNER_ENTERED` | 1 | `AR-INVOKE` | Truthful one-call evidence |
| correct final then one trailing frame | iterator close from `RUNNER_ENTERED` | 1 | `AR-INVOKE`; one unconsumed | Fixed stub proves exhaustion |
| strict invalid or non-object JSON | I1 parse before return | 1 | `AR-INVOKE` | Unique |
| valid JSON but wrong fixed-response bytes/hash | after `INVOKED_ONCE`, before `RESPONSE_CAPTURED` | 1 | `AR-RESPONSE` | Unique |
| exact response but nonempty I0 errors | `RESPONSE_CAPTURED`, before `ANSWER_VALIDATED` | 1 | `AR-ANSWER` | Unique |
| pending close/read-back differs | before `TEMP_RECORD_VERIFIED` | 1 | `AR-RECORD`, remove pending | Unique primary; cleanup residue is M-06 |
| destination appears immediately before publish | at atomic commit | 1 | stable class; preserve destination | M-04: conflicts with zero-call/no-final table claims |
| publish reports success but metadata is lost after crash | commit/durability boundary | 1 | exact declared outcome | M-05: failure model and platform guarantee are not frozen |
| iterator has no callable close but returns exact response | post-I1 stub-integrity check | 1 | reject with one class | M-04/M-07: no exact class and no close field in record |
| timestamp/unknown field or `retry_count=1` enters record | semantic/canonical record check | 1 | `AR-DETERMINISM` | M-04: ordering against `AR-RECORD` is not frozen |
| pending pass bytes are presented without publication | evidence-consumer boundary | 1 | reject as non-success | M-06: consumer rule is not frozen |
| variant creates an I2 route or I3 admission | preflight/static boundary | 0 | `AR-BOUNDARY` | Unique; no import semantics fabricated |

## 9. Maximum claim

The authenticated v0.2 public design package now makes the request, manifest,
I1 grant identity, full-bundle boundary, fixed-stub exhaustion behavior,
ten-state progression, zero/one-call evidence, 36 listed success-record values,
and I2/I3 no-import dispositions independently reconstructable. It is not yet
acceptable for public implementation consideration because four major
publication, routing, residue, and provenance defects remain.

No controller, request artifact, stub, rehearsal, provider/model call,
signer-media import, role isolation, S0 execution, scoring, central system,
Project Brain integration, operational safety, economic value, or
model-to-model transfer has been implemented, executed, or validated by this
review.

## 10. Exact next gate

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`

That gate should revise only the public design package to close M-04 through
M-07 and submit a replacement-extension successor package to a fresh
public-only independent review. It does not authorize controller
implementation, rehearsal execution, provider/model use, F0 access, S0
execution, commit, push, PR, release, or main merge.
