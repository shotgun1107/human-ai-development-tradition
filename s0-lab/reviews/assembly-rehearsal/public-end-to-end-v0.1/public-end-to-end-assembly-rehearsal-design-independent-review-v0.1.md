# S0 v0.14 public end-to-end assembly rehearsal design independent review v0.1

- `review_role`: fresh public-only independent design reviewer
- `review_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN INDEPENDENT REVIEW OPEN`
- `review_head`: `49ecc05dacebf043ed8b2b479eb021018d4b4fe6`
- `review_kind`: design review only; no implementation or execution
- `F0_content_access`: none
- `verdict`: `REVISE-AND-REVIEW`

## 1. Verdict

`REVISE-AND-REVIEW`

The public case, intended I0/I1 composition, I2/I3 non-applicability decision,
nine-state success path, and deterministic-repeat objective are substantially
reconstructable. The package nevertheless has three blocking and four major
findings. In particular, the positive path cannot both call the actual I0
bundle verifier and obey the acceptance plan's stated file allowlist; the
actual I1 first-final API cannot observe the plan's required post-final-frame
mutation; and a read-back failure occurs after the design's cleanup interval,
so a record containing a pass result may remain after the run has failed.

This verdict is only a design-review result. It is not an implementation,
rehearsal, provider/model, I2/I3 runtime-isolation, signer-import, or S0 result.

## 2. Authenticated basis

Repository authentication completed before substantive review:

| Check | Authenticated value | Result |
|---|---|---|
| origin | `https://github.com/shotgun1107/human-ai-development-tradition.git` | PASS |
| branch | `codex/s0-public-assembly-rehearsal-design-v01-review` | PASS |
| HEAD | `49ecc05dacebf043ed8b2b479eb021018d4b4fe6` | PASS |
| remote candidate | `49ecc05dacebf043ed8b2b479eb021018d4b4fe6` | PASS |
| initial worktree/index change count | `0` | PASS |

The following public text/design pairs had valid replacement-extension
sidecars with exact filename and SHA-256 matches:

| Artifact | SHA-256 | Result |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | read and applied |
| I0-I3 readiness audit | `0ca3e51e8a566a94ed168325d18f5fe6196a132de5c4c6979c8ab7348483ffbf` | PASS |
| assembly design | `67a49650219b7587f2698c869336f8a767c55a787235c379b643268a9ec2879a` | PASS |
| interface map | `9758ccd14acbf7e5463bff37e4c6f4a20a073cec7196f35af62a3341f253ce8b` | PASS |
| acceptance plan | `a2f4b07606d673ec474a6faa138115aaadd576b29493be632dc75ce307377971` | PASS |
| independent-review brief | `ae8689a64ce72a60d796e1e8d05d66b5ba65c2d2e5ae9f91cd2ca2c588f96760` | PASS |

The implementation manifests themselves had these hashes, matching every pin
in the design. Every row was format-checked, resolved, and hash-checked before
the listed implementation was used as evidence.

| Component | Manifest SHA-256 | Rows verified | Result |
|---|---|---:|---|
| I0 | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` | 15 | PASS |
| I1 | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | 26 | PASS |
| I2 | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` | 16 | PASS |
| I3 | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | 17 | PASS |

The fixed public case and public contracts also matched the design exactly:

| Input | SHA-256 | Bytes | Result |
|---|---|---:|---|
| canonical input | `bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863` | 4,276 | PASS |
| P01 package | `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7` | 4,518 | PASS |
| questions | `661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90` | 3,182 | PASS |
| public response | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` | 1,936 | PASS |
| answer schema | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | 2,167 | PASS |
| I2 contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | authenticated | PASS |
| I3 contract | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` | authenticated | PASS |

No authenticated input changed before this review record was written.

## 3. Method and boundary

The review used only the exact public allowlist in the review instruction. It
read the four component READMEs and only manifest-listed implementation source
needed to verify these named APIs: I0 bundle verification, transformation and
answer validation; I1 external-manifest grant, manifest entry authentication,
strict JSON, and one-shot execution; and I2/I3 contract verification. Tests,
component verification reports, unrelated repository files, network sources,
providers, models, fixtures, oracles, executors, judges, and rehearsal outputs
were not used.

The three F0 content families remained denied. Their contents were not opened,
searched, enumerated, quoted, hashed, or used. This review did not run the
controller or any rehearsal and did not create a request artifact, stub,
fixture, oracle, executor, judge, response, or run record.

Facts below come from authenticated artifacts or authenticated source.
Inferences and required revisions are labeled as review conclusions rather
than implementation results.

## 4. Independent reconstruction

### 4.1 Fixed public case

The only case is rehearsal `S0-PUBLIC-AR-B2-P01-001`, block
`BLK-PRACTICE0002`, representation `P01`. The canonical input has thirteen
ordered public practice facts. The transformed package retains those facts and
adds the P01 observed-time view. The seven-question projection and fixed
seven-answer public response match the P01 package hash. I0's actual
`transform_canonical` returns the frozen P01 byte format, and its actual
`validate_answer_candidate_bytes` authenticates the schema, questions, and
package before applying neutral schema and question-policy validation.

Applying the design's recursive-key ordering and JSON serialization rules to
the authenticated package and questions reconstructs one 7,917-byte request
with SHA-256
`990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2`.
This is an independent derivation, not a pin stated in the design package.

### 4.2 Intended component call graph

The intended call order is:

1. authenticate external component pins and fixed public bytes;
2. call I2 `verify_contract_file` and I3 `verify_contract_file`;
3. call I0 `verify_public_bundle`;
4. parse the fixed canonical input, call I0 `transform_canonical(..., "P01")`,
   and compare exact bytes with the fixed P01 package;
5. reconstruct the request and compare it with the future frozen request;
6. call I1 `bind_external_manifest_grant`,
   `load_authenticated_manifest`, and `authenticate_manifest_entry`;
7. reserve the output exclusively;
8. call I1 `run_one_shot` once with the public stub;
9. require the fixed response hash and call I0
   `validate_answer_candidate_bytes`;
10. write, fsync, close, re-read, and hash the canonical record.

This uses the actual I0 and I1 APIs rather than duplicating their transform,
answer-policy, request-authority, or one-shot logic. Findings B-01 and B-02
show where the surrounding design and acceptance conditions do not match what
those actual APIs do.

### 4.3 I1 authority path

The authority mechanism is correct in kind: an independently supplied exact
manifest path, manifest SHA-256, namespace prefix, sorted one-path allowlist,
and purpose are bound into the same `ManifestGrant`; the manifest is loaded
through that grant; the request entry is authenticated from it; and the same
grant and expected values are required by `run_one_shot`. The exact purpose is
`s0-public-assembly-rehearsal-v01`.

The exact manifest path, request path, namespace prefix, manifest bytes and
manifest SHA-256 are not specified. Therefore the exact I1 request-authority
path cannot be reconstructed from this design. This is finding M-01.

### 4.4 State, success record, and repeat

The intended success state order is:

`NEW -> PREFLIGHT_AUTHENTICATED -> REQUEST_RECONSTRUCTED -> OUTPUT_RESERVED -> INVOKED_ONCE -> RESPONSE_CAPTURED -> ANSWER_VALIDATED -> RECORD_COMMITTED -> COMPLETE`.

There is no backward, retry, resume, overwrite, append, or partial-success
transition. Success requires one call, zero retries, one final response frame,
the exact public-response hash, zero I0 errors, durable record operations, and
read-back hashing. The two repeats use fresh empty output roots and must yield
identical record bytes and hashes; the second run is an independent execution,
not a retry.

Most successful-record values are fixed by the interface map and design. The
record's `schema_id` and `claim_kind` values are not fixed, and the request
manifest identity cannot be fixed until M-01 is resolved. Consequently the
record is not yet uniquely reconstructable. This is finding M-02.

### 4.5 I2/I3 disposition

The no-import disposition is honest. I2 and I3 authenticate exact public
contract bytes and their internal bindings, but the fixed repository public
case does not traverse signer media. No I2 route/event and no I3
admission/outcome should be fabricated. The exact record dispositions are
`contract-authenticated-no-import-route` and
`contract-authenticated-no-import-attempt`. These are contract-preflight and
non-applicability statements only, not signer-import, trust-root activation,
registry, ledger, witness, or operational-isolation success.

### 4.6 Denied boundaries

The proposed future verifier can reject configured paths before opening them,
use an exact allowlist, statically audit candidate path/import surfaces, and
intercept file-open attempts in the candidate process. This can detect a
denied path introduced through configuration without enumerating or opening
F0 content. The evidence would remain bounded process-level observation, not
OS or hostile-process isolation proof.

Finding B-01 is distinct: the design's own required I0 call traverses public
files outside the acceptance plan's declared exact-case allowlist.

## 5. Findings

### B-01 — Actual I0 bundle verification exceeds the declared execution allowlist

**Fact.** The design and positive acceptance sequence require
`s0_i0.verify_public_bundle(workspace_root)`. The authenticated I0
implementation recursively enumerates the entire public-practice v0.1 bundle,
requires the complete 90-entry manifest file set, reads and hashes every
manifest entry, parses every JSON entry, and performs both-block package and
fact checks. The acceptance plan's boundary evidence permits only the exact
public case files named in the design, plus the separately named contracts,
schema, component sources, candidate namespace, and validator.

**Review conclusion.** With the stated sentinel/allowlist, the positive run
must reject I0's first non-case bundle access. If the verifier silently allows
the full bundle instead, it violates the reviewed boundary. The flow therefore
cannot be constructed as specified.

**Required revision.** Either remove the full-bundle call and name an existing
I0 exact-file authentication path that supplies equivalent required evidence,
or explicitly freeze and review the full 90-entry public bundle inventory as
an execution input. Align the design, acceptance allowlist, sentinel, and
maximum claim. Do not describe the call as reading only the five fixed files.

### B-02 — Required post-final-frame rejection is unobservable through I1

**Fact.** I1 `run_one_shot` intentionally stops at the first frame whose
`final` flag is true and closes the iterator without consuming a later
response. A normal iterable containing the correct final frame followed by an
extra frame therefore returns the correct response; the later frame is never
observed. The acceptance plan nevertheless requires `bytes follow the final
frame -> AR-INVOKE`.

**Review conclusion.** Such a transport can satisfy the response hash and I0
answer validation and reach `COMPLETE`. This is a false success against an
explicit hostile acceptance criterion. The currently specified adapter cannot
prove the criterion through the actual unmodified I1 API.

**Required revision.** Choose one reviewed rule: conform acceptance to I1's
first-final-only contract, or define an exact candidate-owned stub/iterator
protocol whose close operation proves that no scripted frame remains and make
that proof part of success. Do not claim generic trailing-frame detection from
I1.

### B-03 — Read-back failure is outside the cleanup interval

**Fact.** The record contains
`result=public-assembly-rehearsal-pass-not-s0` before persistence. The design
removes an incomplete reservation on failures after reservation and before
committed close. `COMPLETE`, however, requires a read-back hash after close.
The required hostile case includes final read-back failure, and the acceptance
plan requires no success record and zero persistent incomplete records after
failure.

**Review conclusion.** A close can succeed, the pass-valued record can remain
at the final path, and read-back can then fail. The run is not `COMPLETE`, but
the stated cleanup rule no longer applies. A pass-looking artifact may persist
without the required final verification.

**Required revision.** Extend fail-closed cleanup through successful read-back
equality, or keep the record at an explicitly incomplete temporary path and
publish it only after close and read-back verification. Define cleanup-failure
precedence for this post-close phase.

### M-01 — Exact I1 request grant identity is not frozen

The design fixes the grant purpose and one-entry shape but not the exact
manifest path, request path, namespace prefix, manifest row/path text, or
manifest digest. Different implementations can therefore create different
authority bindings while claiming the same design. Freeze these exact values
and state where the independently reviewed pin enters the trusted caller.

### M-02 — Canonical successful record is not uniquely specified

The field inventory is exact, but the values for `schema_id` and `claim_kind`
are absent. The exact request-manifest identity is also missing because of
M-01. Byte-identical repetition only proves that one implementation is stable;
it does not make independently constructed implementations byte-identical.
Freeze every field value or an exact derivation rule and publish the expected
record bytes/hash in the successor design.

### M-03 — Invocation state and zero-call/one-call accounting are not atomic

The design calls `OUTPUT_RESERVED -> INVOKED_ONCE` the sole I1 call but does
not say whether state/call accounting advances before call entry, when
`transport.invoke_once` is entered, or only after `run_one_shot` returns. If
transport construction fails there may be zero calls; if the iterator never
finalizes there is one call but no return. The exact rejecting state is thus
not reconstructable, and a failure report can misstate zero versus one call.
Define an observable transport-call counter and the precise transition point,
including constructor, call-entry, iterator, and cleanup exceptions.

### M-04 — Not every failure has one stable class

The acceptance plan allows invalid/non-object JSON to be either `AR-INVOKE` or
`AR-RESPONSE`, even though the design promises stable independently testable
labels. It also names a deterministic-repeat failure without assigning one of
the eight stable classes; the required retry-mislabel counterexample has no
unique class. Freeze precedence and one class for strict-JSON failure,
repeat-byte mismatch, nondeterministic fields, and nonzero retry claims.

### Minor findings

None.

## 6. Required-question dispositions

| # | Disposition | Evidence and conclusion |
|---:|---|---|
| 1 | PASS with B-01 | The design calls actual I0 transform and answer-validator APIs and exact-byte compares their results. The additional whole-bundle call conflicts with the declared allowlist. |
| 2 | MAJOR M-01 | The existing I1 external-manifest grant path is used in kind; its exact path/prefix/manifest identity is not reconstructable. |
| 3 | FAIL B-02, M-03 | I1 enforces one invocation, zero retry, bounds, strict cleanup, and first-final selection. The design cannot enforce the separate trailing-frame rejection and does not place failed-call accounting exactly. |
| 4 | PASS with M-01 | The eight-field request object and serialization are deterministic and carry package plus questions. The request bytes are derivable, but their filesystem authority identity is not frozen. |
| 5 | PASS | I2/I3 exact contract verification plus explicit no-import dispositions are honest. Fabricated accepted signer-media semantics are denied. |
| 6 | PASS with M-03/M-04 | Reservation precedes invocation and validation precedes commit; no retry/resume/overwrite transition exists. Failed-call state and some failure classes remain ambiguous. |
| 7 | MAJOR M-02 | Timestamps, randomness, host paths, and environment data are excluded, but not every record value or request-manifest binding is fixed. |
| 8 | FAIL B-03, M-03/M-04 | Most cleanup and call-count expectations are present. Post-close read-back failure can leave a pass-looking record, and call/class evidence is not unique. |
| 9 | PASS with B-01 | Exact allowlist validation plus an open sentinel can detect configured denied paths without touching F0. The current positive I0 call itself exceeds the non-F0 exact-case allowlist. |
| 10 | FAIL as written | The intended controller is small, but the current criteria cannot all be met without revising the boundary or first-final criterion. No general I4/security subsystem is justified. |
| 11 | PASS | The package consistently limits itself to a public model-free design candidate and denies S0, provider, scoring, role-isolation, trust-root activation, central-system, and Project Brain claims. |
| 12 | PASS with blockers | The positive composed flow, hostile mutations, state invariants, byte-identical repeat, exact changes, and stability checks go beyond component unit tests. B-01 through B-03 prevent the plan from being executable as written. |

## 7. Required hostile traces

| Counterexample | Calls | Rejecting state | Failure | Disposition |
|---|---:|---|---|---|
| request manifest authentic but reconstructed I0 package differs | 0 | `PREFLIGHT_AUTHENTICATED`; transition to `REQUEST_RECONSTRUCTED` denied | `AR-TRANSFORM` | Unique and fail-closed. |
| output collision before invocation | 0 | `REQUEST_RECONSTRUCTED`; transition to `OUTPUT_RESERVED` denied | `AR-RESERVE` | Existing output remains untouched. |
| transport called once but never produces final frame | 1 | not uniquely fixed between `OUTPUT_RESERVED` and `INVOKED_ONCE` | `AR-INVOKE` | Cleanup is required; exact state/call accounting needs M-03. |
| valid JSON response with wrong public-response hash | 1 | `RESPONSE_CAPTURED`; no validation transition | `AR-RESPONSE` | Reservation must be removed. |
| exact public-response hash but non-empty I0 errors | 1 | `RESPONSE_CAPTURED`; transition to `ANSWER_VALIDATED` denied | `AR-ANSWER` | Reservation must be removed. |
| record write succeeds but close fails | 1 | `RECORD_COMMITTED`; transition to `COMPLETE` denied | `AR-RECORD` | Pre-close cleanup applies. |
| record write and close succeed but read-back fails/differs | 1 | `RECORD_COMMITTED`; transition to `COMPLETE` denied | `AR-RECORD` | B-03: cleanup is not guaranteed and a pass-looking file can remain. |
| second execution is labeled as a retry | 1 per execution | record construction or repeat comparison | unspecified stable class | Must fail because each independent run requires `retry_count=0`; M-04 fixes the class. |
| variant adds an I2 accepted route without real import | 0 | `NEW`; preflight/static boundary denies progress | `AR-BOUNDARY` | No route/event/admission/outcome may be created. |
| denied path arrives through configuration | 0 | `NEW`; configuration allowlist/open sentinel denies progress | `AR-BOUNDARY` | Detection must compare the attempted normalized path without opening or enumerating F0. |

Additional hostile trace required by the acceptance plan:

| Counterexample | Actual trace | Required result | Review result |
|---|---|---|---|
| correct final frame followed by another frame | I1 stops at the first final frame, closes a normal iterator, returns the correct bytes, and permits later validation/commit | `AR-INVOKE` | B-02: false success is possible. |
| strict JSON parse failure | I1 raises from inside `run_one_shot` | one stable class | M-04: plan permits `AR-INVOKE` or `AR-RESPONSE`. |
| I0 full-bundle access under exact-case sentinel | I0 enumerates and reads non-case public bundle entries | positive composed run | B-01: positive run must boundary-fail or widen the allowlist. |

## 8. Maximum claim

The authenticated public design package defines a narrow model-free intent for
composing actual I0 transform/answer validation with I1 one-shot request
authentication, while treating I2/I3 signer-import behavior as explicitly
non-applicable. Independent review found the design is not yet acceptable for
public implementation consideration. No controller, rehearsal, provider/model
call, signer import, role isolation, S0 execution, scoring, central system,
Project Brain integration, operational safety, economic value, or
model-to-model transfer has been implemented or validated.

## 9. Exact next gate

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`

That gate should revise only the public design package to close B-01 through
B-03 and M-01 through M-04, then submit the replacement-extension design
artifacts to a fresh public-only independent review. It does not authorize
controller implementation, rehearsal execution, provider/model use, F0
access, S0 execution, commit, push, PR, or main merge.
