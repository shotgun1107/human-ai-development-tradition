# S0 v0.14 I3 public import-decision contract v0.2 independent rereview v0.1

- `review_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 INDEPENDENT REREVIEW OPEN`
- `review_role`: fresh independent public design rereviewer
- `baseline_worktree`: `C:\Users\SSAFY\AppData\Local\Temp\ai-development-tradition-s0-i3-v02-independent-rereview`
- `baseline_branch`: `codex/s0-i3-public-import-decision-contract-v02-independent-rereview`
- `baseline_head`: `9df5bf8ae4a834fdcb0ca0b89eb03d0e04a6e5bb`
- `baseline_tree`: `3b1000a249eac84e8c621d7f173186305930c9cd`
- `baseline_parent`: `d2167aebe6b295b99982bed15f5a0d79720c899d`
- `initial_status_count`: `0`
- `finding_count`: `0`
- `verdict`: `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

## 1. Boundary, independence, and method

I did not author or advise on either I3 v0.1 or v0.2. I did not trust the
v0.2 author disposition as proof of closure. I used no subagent and read only
the 35 authenticated inputs in section 2. I did not search or enumerate the
repository, inspect another review, use outside sources, read F0, inspect
implementation code, create code or cases, or run an import, platform,
provider, model, E0, or S0 operation.

Before substantive reading, I authenticated the exact worktree, branch,
commit, tree, sole parent, clean status, and all supplied input hashes. I then
read and reconstructed the boundary, the v0.1 review findings, the v0.1
candidate, the v0.3/v0.4 authority text, and the strict-parsed I2 JSON before
reading the v0.2 closure proposal. This preserves the required review order
and makes the conclusions below independent of the v0.2 author's claims.

The review is limited to byte grammar, field and identity binding,
classification totality and determinism, completion finalization,
testability, and exact I2 compatibility inside the frozen I3 boundary.

## 2. Authenticated inputs and validator results

All 35 supplied SHA-256 values matched before substantive reading and were
still treated as the immutable review inputs:

| # | Input | SHA-256 |
|---:|---|---|
| 1 | `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` |
| 2 | `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| 3 | `s0-lab/control/i3/i3-public-import-decision-contract-boundary-v0.1.md` | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` |
| 4 | `s0-lab/control/i3/i3-public-import-decision-contract-boundary-v0.1.sha256` | `8f0f71e1f2887463d17ba46fba7f8c53c4bcc638c631c200354cc044c1cae5fc` |
| 5 | `s0-lab/reviews/i3/import-decision-contract-v0.1/independent-review-v0.1.md` | `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c` |
| 6 | `s0-lab/reviews/i3/import-decision-contract-v0.1/independent-review-v0.1.sha256` | `8195702dd5b6733d69e8cfa4df9a30bb6b4d1ae0519d953c221ce95d01db9fec` |
| 7 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-decision-contract-v0.2.md` | `f04dae684b7373a4c613c3f0e357ef8266f0bf307e78e78d105cb04168f61594` |
| 8 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-decision-contract-v0.2.sha256` | `2d946671db0d3cdf994baa519947f79be6ca43a8eb723b4600e0a9feda119edc` |
| 9 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-field-binding-table-v0.2.md` | `b034fadf16e7b5d11594c6987ba714e791ef2b2d02409589c6e7b90126e2fa02` |
| 10 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-field-binding-table-v0.2.sha256` | `7d05db2a7e789b3bb429f89d34a7b98f5706776df25e23da9ff18d339fc981f9` |
| 11 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-classification-table-v0.2.md` | `82f787c737f0a255970679b4c501b93061de7b7778e10843d71c047aa69ea706` |
| 12 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-classification-table-v0.2.sha256` | `ac39b8c7dc9b297de705f5cdc7fa79c63eb43e238b04f406596e8093acff4681` |
| 13 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-implementation-test-brief-v0.2.md` | `182df459eee2877d5c4710794ad7a7c86a56a44abe7ce14d09e629fc1c29ac62` |
| 14 | `s0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-implementation-test-brief-v0.2.sha256` | `b0adc20604711bd013a9472daf9baebdc43bf2be2669bb367de2c4b608c03bf0` |
| 15 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-decision-contract-v0.1.md` | `1786b97b36988894d0fcd5083e9657502cb9ba2443fcde4909f2f261c6a1bd83` |
| 16 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-decision-contract-v0.1.sha256` | `753eb01f7d57f0371ac01c5d4babfbddbbd3f4af89b971d0a1afb86ae5e851bd` |
| 17 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-field-binding-table-v0.1.md` | `e19156d4ce73be157649213e8f90fbd05ea9d3b59b6c346acba61a409cdb2ab3` |
| 18 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-field-binding-table-v0.1.sha256` | `4e06b27075e545c59bbbfe0e337da43875401f13dbf6c1611f7c1f7c720ce6bf` |
| 19 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-classification-table-v0.1.md` | `3251273da2c9f7f05968a4b1bf08ef4808dc9387682ba8b7b0c84977454003b3` |
| 20 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-classification-table-v0.1.sha256` | `6a4ef7b0148647c4ee9b0de6b6b04e3afc061de0fe977f60f87a0fa950863ffc` |
| 21 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-implementation-test-brief-v0.1.md` | `694efd7a93080d1d536d9005db5bcd9859fcf86f6ed7748d947eb14f78aac101` |
| 22 | `s0-lab/control/i3/import-decision-contract-v0.1/i3-public-import-implementation-test-brief-v0.1.sha256` | `1d5095d9af73ad724c9e663f57ee4c73c9c95b15a48f756476abae679923adf7` |
| 23 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.md` | `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b` |
| 24 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.sha256` | `90b2643bd2128339261ea0eae6c334ae757d5fa096cae3e9d73b8ff7ae606757` |
| 25 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.md` | `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a` |
| 26 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.sha256` | `14ad4440f996f6b637b8adb667b3975a9040ee70d8da503d5be700646438d72b` |
| 27 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.md` | `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3` |
| 28 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.sha256` | `d2bac18a3bef1ec769e9f97149fa6d74bd4536b7454151ec6113fe355f9a86d7` |
| 29 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| 30 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256` | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| 31 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| 32 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256` | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| 33 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| 34 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256` | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| 35 | `s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json` | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |

The authenticated validator self-test returned all 11 named self-test cases
as `PASS` and final `SELF_TEST=PASS`. The host's default script policy blocked
the first launcher before the validator executed; the same authenticated
script then ran with a process-scoped execution-policy bypass and passed. No
repository setting or file was changed by that launcher choice.

Exactly 16 admitted Markdown/sidecar pairs were validated: the boundary, the
v0.1 review, all four v0.1 I3 artifacts, all four v0.2 I3 artifacts, and all
six v0.3/v0.4 authority artifacts. Every independently labeled check for file
presence, strict UTF-8, BOM absence, final LF, trailing-whitespace absence,
sidecar presence and canonical text, and sidecar record/hash returned `PASS`;
the final result was `OVERALL=PASS`.

The I2 JSON passed strict UTF-8 decoding and strict JSON parsing with duplicate
member rejection. I independently confirmed its exact schema/version, one
unique 31-field event order, 13 lifecycle variants, three route maps, 21
non-root signer IDs, and the nine unsupported boundaries. Its 31-field event
contains zero configuration-hash fields.

## 3. Independent contract reconstruction

### 3.1 Exact admission and outcome bytes

The admission grammar has exactly this ordered 21-field sequence:

```text
import_admission_schema
authority_id
campaign_id
ceremony_id
signer_id
import_class
from_state
to_state
package_sha256
package_object_id
attachment_capability_id
result_media_kind
result_media_id
reserved_media_event_id
admission_frozen_media_event_id
pending_media_event_id
completion_media_event_id
outcome_schema
outcome_max_bytes
admission_event_id
decision
```

It is strict ASCII `name=value` with LF after every line, including line 21.
The schema, authority, media kind, outcome schema, byte limit, and decision are
fixed literals. All value domains and the three class/state mappings are
closed. `R`, `A`, `P`, `C`, and `result_media_id` are nonzero and pairwise
distinct, and `admission_event_id=A`. The admission hash covers all 21 lines
including the final LF.

The outcome grammar has exactly this ordered 26-field sequence:

```text
import_outcome_schema
tcb_service_id
campaign_id
ceremony_id
signer_id
import_class
from_state
to_state
package_sha256
package_object_id
attachment_capability_id
admission_event_id
admission_record_sha256
result_media_kind
result_media_id
reserved_media_event_id
admission_frozen_media_event_id
pending_media_event_id
completion_media_event_id
before_state
after_state
before_configuration_state_sha256
after_configuration_state_sha256
decision
reason
outcome_body_sha256
```

It has the same strict ASCII/LF rejection boundary. The body hash is SHA-256
of lines 1-25 including the LF after `reason`. Full `H` is SHA-256 of all 26
lines including the LF after `outcome_body_sha256`. A selectable frame begins
at byte zero of the sole exactly 2,048-byte medium, ends by line 26, and has
only zero bytes afterward; padding is excluded from `H`. A direct lexical
upper-bound reconstruction places every allowed admission and outcome below
their applicable limits, so all canonical tuples are reachable.

The only canonical outcome tuples are:

| Class | Decision/reason | State | Configuration hashes |
|---|---|---|---|
| `accepted` | `accepted/none` | `SRC/DST` | both nonzero and unequal |
| `parse-rejected` | `rejected/parse-rejected` | `SRC/SRC` | equal and nonzero |
| `validation-rejected` | `rejected/validation-rejected` | `SRC/SRC` | equal and nonzero |
| `state-commit-failed` | `rejected/state-commit-failed` | `SRC/indeterminate` | before nonzero, after `Z` |

A wrong field, body hash, route tuple, decision/reason tuple, state tuple, or
configuration tuple makes the frame internally invalid. Exact canonical
record bytes cannot be recovered through a host-status assertion.

### 3.2 Exact route maps and cross-bindings

The three and only three route maps reconstruct as:

| Import class | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

Admission, outcome, and actual shared I2 event fields bind campaign, ceremony,
non-root signer, route, package hash/object, capability, media kind/ID,
`R/A/P/C`, admission ID/hash, outcome class, frame hash, and appliance states.
Class selects only its listed state pair. The admission hash, body hash, and
full `H` are recomputed rather than caller-selected. I2 separately validates
its global predecessor hash, route-local predecessor ID, exact lifecycle, and
supplied-set ownership rules.

There is no event-hash cycle: the outcome commits planned completion ID `C`,
and the later event commits outcome hash `H`; the outcome does not bind the
future event hash.

### 3.3 Sole media representation and scan

The caller supplies one immutable finite sequence of byte strings. The sole
count is its length. Empty, one-member, and multiple-member sequences are all
well typed. A malformed outer value, lazy or unbounded producer, non-byte
member, invalid enum, missing required fact, or non-byte admission argument is
only `I3_INPUT_ERROR` and never an experimental class. Noncanonical bytes are
well typed and enter classification.

For a pending route, the scan derives count, the sole medium when count is one,
exact 2,048-byte length, exact schema-prefix count, structural completion at
zero, complete-candidate count, candidate end, nonzero tail, internal frame
canonicality, `H`, and external exactness. It never chooses a favorable member
from multiple media or a favorable frame from multiple candidates. A complete
26-line block is not missing merely because its syntax or body hash is bad.

### 3.4 Total, deterministic, exclusive classification

Both pre-pending rows are total over their well-typed inputs and ignore
apparent outcome bytes:

| Row | Result |
|---|---|
| `PRE-R` | `none/Z/none/none`, direct terminal from reserved required |
| `PRE-A` | `none/Z/none/none`, direct terminal from admission-frozen required |

For pending, the nine rows reconstruct in exact order:

| Order | Row | Decisive partition | Result |
|---:|---|---|---|
| 1 | `P-CRASH` | abnormal end | `crash/Z/SRC/indeterminate` |
| 2 | `P-MISSING` | normal end, exactly one exact-size medium, no duplicate evidence, all-zero or no complete candidate | `missing/Z/SRC/indeterminate` |
| 3 | `P-DUPLICATE` | multiple media, prefixes, candidates, or nonzero tail | `duplicate/Z/SRC/indeterminate` |
| 4 | `P-DISAGREE-H` | one canonical frame at zero with zero tail, but external evidence not exact | `disagreement/H/SRC/indeterminate` |
| 5 | `P-DISAGREE-Z` | no selectable internally canonical frame | `disagreement/Z/SRC/indeterminate` |
| 6 | `P-PARSE-REJECTED` | canonical parse-rejection tuple and all external evidence exact | `parse-rejected/H/SRC/SRC` |
| 7 | `P-VALIDATION-REJECTED` | canonical validation-rejection tuple and all external evidence exact | `validation-rejected/H/SRC/SRC` |
| 8 | `P-STATE-COMMIT-FAILED` | canonical state-commit-failure tuple and all external evidence exact | `state-commit-failed/H/SRC/indeterminate` |
| 9 | `P-ACCEPTED` | canonical accepted tuple and all external evidence exact | `accepted/H/SRC/DST` |

Crash precedence explicitly discards apparent bytes. Missing excludes every
duplicate predicate. Duplicate precedes frame selection. Thereafter a unique
canonical frame partitions solely on external exactness: false reaches row 4,
true reaches exactly one of rows 6-9. Absence of such a frame reaches row 5.
The tuple enums make rows 6-9 disjoint. Thus every well-typed pending input
selects exactly one row, repeated input selects the same row, and every row is
reachable without authority or operator choice.

### 3.5 Exact I2 mapping and finalization separation

The strict I2 JSON has exactly these 31 event fields, once each and in order:

```text
signer_media_event_schema
namespace
sequence
previous_event_sha256
event_id
prior_route_event_id
campaign_id
ceremony_id
signer_id
route_kind
route_class
request_id
attachment_capability_id
admission_event_id
admission_record_sha256
media_object_sha256
media_object_id
result_media_id
result_media_kind
reserved_media_event_id
admission_frozen_media_event_id
pending_media_event_id
completion_media_event_id
outcome_schema
outcome_frame_sha256
outcome_class
before_appliance_state
after_appliance_state
state
terminal_from
decision
```

The I3 mapping is byte-compatible with the exact I2 lifecycle: pre-pending is
`none/none/Z`; accepted is `SRC/DST/H`; parse and validation rejection are
`SRC/SRC/H`; state-commit failure is `SRC/indeterminate/H`; crash, missing,
and duplicate are `SRC/indeterminate/Z`; disagreement is
`SRC/indeterminate/H` for one uniquely selectable internally canonical frame
and `SRC/indeterminate/Z` otherwise. Abnormal-end crash remains `Z` even when
bytes look canonical because crash precedence intentionally ignores them.

Classification never grants destination authority. Only classification
`accepted`, the exact matching I2 `consumed/accepted` event using `C` and `H`,
and append status `persisted` produce `consumed-accepted` and make exact `DST`
available. Exact persisted terminal events produce only
`terminal-rejected`. A missing, malformed, mismatching, conflicting,
unavailable, failed, or unpersisted completion produces
`no-completion-claim`. The finalizer cannot reclassify, redraw `C`, infer an
append, append a replacement, retry, or create a post-terminal event.

## 4. Predecessor finding dispositions

### `I3-IR-B01` - closed with no residual finding

I independently traced the same internally canonical frame at byte zero with
zero tail across every end value. Normal end with exact external evidence
reaches its explicit tuple class with `H`. Unknown and not-started end make
external evidence non-exact and therefore reach `P-DISAGREE-H` with the same
recomputed `H`. Abnormal end reaches the earlier crash row and uses `Z`.

A bad body hash, illegal tuple, malformed grammar, wrong-size medium,
nonzero-offset-only candidate, or other noncanonical/nonselectable bytes use
`Z`; multiple media/candidates/prefixes or nonzero tail use duplicate/`Z`.
The resulting disagreement `H/Z` and crash `Z` map exactly to the authenticated
I2 terminal variants. The v0.1 contradiction is removed consistently from the
main contract, binding table, classification table, and test brief.

### `I3-IR-M01` - closed with no residual finding

There is one normative media representation: one immutable finite sequence of
byte strings. Count is derived only from sequence length and cannot disagree
with a separate byte value because no separate count exists. Empty, one, and
multiple members are classified respectively through disagreement/`Z`, the
one-medium scan, and duplicate/`Z`. Malformed outer/member types are only
`I3_INPUT_ERROR`. The interface, classification table, binding table, and
future tests now use the same representation.

### `I3-IR-M02` - closed with no residual finding

The strict I2 event has no before/after configuration-hash fields. V0.2 does
not invent them or require direct equality to them. The outcome parser checks
both hashes internally against the four exact state/decision tuples. Changing
either hash changes the recomputed body hash and full `H`; the actual I2
completion field `outcome_frame_sha256=H` therefore transitively commits both
hash bytes. Finalization compares only fields that exist in I2. This preserves
the 31-field event unchanged while retaining a testable byte commitment.

## 5. Hostile traces

| Trace | Exact result |
|---|---|
| reserved phase with any apparent bytes | `none/Z/none/none`; only exact persisted direct terminal can complete |
| admission-frozen phase with any apparent bytes | `none/Z/none/none`; only exact persisted direct terminal can complete |
| pending abnormal end with no bytes | `crash/Z/SRC/indeterminate` |
| pending abnormal end with a canonical frame | `crash/Z/SRC/indeterminate`; apparent frame ignored |
| pending unknown end with one canonical zero-tail frame | `disagreement/H/SRC/indeterminate` |
| pending not-started end with one canonical zero-tail frame | `disagreement/H/SRC/indeterminate` |
| uncertain end with bad body hash or illegal tuple | `disagreement/Z/SRC/indeterminate` |
| normal end, one all-zero 2,048-byte member | `missing/Z/SRC/indeterminate` |
| normal end, one partial or truncated member with no complete candidate | `missing/Z/SRC/indeterminate` |
| empty sequence after pending | `disagreement/Z/SRC/indeterminate` |
| one member shorter or longer than 2,048 bytes | `disagreement/Z/SRC/indeterminate` |
| one complete 26-line block at zero with malformed syntax | `disagreement/Z/SRC/indeterminate` |
| one complete candidate only at nonzero offset | `disagreement/Z/SRC/indeterminate` |
| multiple media members | `duplicate/Z/SRC/indeterminate`; no member selected |
| multiple prefixes or complete candidates in one medium | `duplicate/Z/SRC/indeterminate`; no frame selected |
| canonical frame plus any nonzero tail byte | `duplicate/Z/SRC/indeterminate`; no frame selected |
| canonical frame with one external identity, route, state, object, event, admission, or status conflict | `disagreement/H/SRC/indeterminate` |
| complete frame with bad body hash | `disagreement/Z/SRC/indeterminate` |
| complete frame with illegal decision/state/configuration tuple | `disagreement/Z/SRC/indeterminate` |
| exact parse-rejected tuple and all external evidence exact | `parse-rejected/H/SRC/SRC` |
| exact validation-rejected tuple and all external evidence exact | `validation-rejected/H/SRC/SRC` |
| exact state-commit-failed tuple and all external evidence exact | `state-commit-failed/H/SRC/indeterminate` |
| exact accepted tuple and all external evidence exact | `accepted/H/SRC/DST`, but destination still unavailable |
| accepted plus exact consumed event and persisted append | `consumed-accepted`; exact `DST` becomes available |
| any non-accepted class plus exact terminal event and persisted append | `terminal-rejected`; destination unavailable |
| any class plus missing, wrong, malformed, conflicting, or unpersisted completion | `no-completion-claim`; destination unavailable |
| malformed media outer value/member or non-byte admission argument | only `I3_INPUT_ERROR`; no classification or event claim |

The traces also cover cross-signer, cross-route, cross-package,
cross-campaign, replay, duplicate ID, wrong chain, wrong `H/Z`, and external
completion conflict through the exact binding and finalizer rules. Each fails
without redraw, inferred append, selective replay, or retry.

## 6. Nonregression and future testability

Relative to v0.1, I found only the three intended semantic repairs: uncertain
end evidence now retains `H` for a unique canonical frame; count and bytes are
replaced by one media sequence; and impossible direct configuration-hash event
bindings are replaced by internal tuple validation plus transitive commitment
through `H`. The 21-line admission bytes, 26-line outcome bytes, body/full
hash boundaries, 2,048-byte zero-tail rule, route maps, class precedence,
I2 states/lifecycle, closed authority, and finalization rule otherwise remain
unchanged.

The package does not copy or create a competing I2 event grammar. It requires
reuse of the authenticated I2 parser, serializer, hash, lifecycle, chain, and
supplied-set validation. It adds no retry, redraw, inferred append, role,
signer, store, reader, edge, signature scope, ledger namespace, or A-D
opportunity. Durable append, lifetime uniqueness, witness/provider truth,
actual registry authority, and platform enforcement remain later closed
dependencies rather than hidden I3 requirements.

The future requirements are finite and mechanically partitioned: 21 admission
positions, 26 outcome positions, four canonical tuples, three route maps,
two pre-pending rows, nine pending rows, eight three-valued statuses, four end
values, media counts partitioned as zero/one/multiple, exact 2,048-byte scan
boundaries, 13 I2 lifecycle variants, and a finite finalizer matrix. Byte
mutation around the exact grammars plus the declared structural partitions is
sufficient to test malformed space without pretending to enumerate every
possible byte string. No future requirement depends on model judgment or an
unstated platform behavior.

## 7. Findings and verdict

Blocking findings: zero. Major findings: zero. Minor findings: zero.

The three authenticated predecessor findings are closed, the v0.2 package is
total and deterministic within the frozen public I3 boundary, and no I2 or
authority regression was found.

`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

## 8. Evidence limits and exact next permissible gate

This rereview establishes only a zero-finding public design disposition. It
does not validate an implementation, parser, classifier, media, import,
durable ledger or witness, project-lifetime uniqueness, atomic append, actual
authority, VM/platform/provider enforcement, protected material, F0, fixture,
oracle, E0, S0, the central system, Project Brain, operational safety,
economic value, or model-to-model transfer.

The exact next permissible gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 CONTROL INTEGRATION DECISION OPEN`

That gate, if separately opened, may consider only CONTROL integration of this
public design package. This rereview does not open implementation, fixtures,
execution, commit, push, merge, main integration, or any later gate.
