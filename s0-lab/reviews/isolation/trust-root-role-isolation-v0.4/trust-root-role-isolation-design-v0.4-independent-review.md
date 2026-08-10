# S0 v0.14 trust-root and role-isolation v0.4 independent review

- `review_kind`: fresh public-only hostile limited design review
- `review_date`: 2026-08-10 KST
- `review_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 INDEPENDENT REVIEW OPEN`
- `worktree`: `C:\Users\SSAFY\AppData\Local\Temp\ai-development-tradition-s0-isolation-v04-independent-review`
- `branch`: `codex/s0-isolation-v04-independent-review`
- `reviewed_commit`: `d55c642d688fea847b469e8221ef63dfcb159052`
- `reviewed_tree`: `1867dd953f072a189c3f57df22f317ba2f98d609`
- `verdict`: `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`
- `finding_count`: zero blocking, zero major, zero minor
- `claim_kind`: public design review only

No implementation, cryptographic, platform, provider, model, acceptance, E0,
or S0 test was run. No schema, parser, vector, point operation, key, signature,
fixture, oracle, package, VM, account, network, ACL, vault, store, signer,
ledger, witness, provider session, executor, or model session was created or
exercised.

## 1. Review authority, independence, and boundary

This reviewer was the sole fresh independent reviewer for the exact gate above.
The reviewer did not author or advise on v0.4, did not run or inherit author-side
QA, did not inherit or seek another v0.4 reviewer conclusion, and used no
subagent. The authenticated v0.3 rereview was used only as predecessor finding
evidence after the effective design had been independently reconstructed; it
was not used as an answer key. The v0.4 author response was likewise treated as
explanatory evidence without closure authority.

Only the exact 34 authenticated paths in section 2 were read. No repository-wide
enumeration or broad search was used. No unlisted repository file, sealed
material, oracle, fixture, condition map, executor output, E0 material,
implementation code outside the four admitted I1 public inputs, old invalid
review, or advisory note was read. Worktree separation is treated as edit
isolation only, not secrecy or independent information security.

The only external source opened was the candidate-linked official RFC 8032, and
only to confirm that sections 5.1.2 and 5.1.3 describe Ed25519 encoding and
decoding. It supplied no coordinate, literal, vector, point-order evidence, or
replacement claim. See [RFC 8032 sections 5.1.2 and 5.1.3](https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1.2).

Candidate inputs remained read-only. The only writes are this authorized review
Markdown and its same-basename SHA-256 sidecar.

## 2. Baseline, authentication, and validation

### 2.1 Git handoff facts

Before substantive content was read, the following facts were checked:

| Check | Required and observed value | Result |
|---|---|---|
| branch | `codex/s0-isolation-v04-independent-review` | pass |
| HEAD | `d55c642d688fea847b469e8221ef63dfcb159052` | pass |
| HEAD tree | `1867dd953f072a189c3f57df22f317ba2f98d609` | pass |
| parent count | exactly one | pass |
| sole parent | `81a32c97dc9f1e50d742dd009034ac678ff66494` | pass |
| parent tree | `adb81e1d6dc73249287addb457ac2d459a1f41a6` | pass |
| initial porcelain status | zero entries | pass |
| parent-to-candidate diff | exactly five v0.4 Markdown files and their five same-basename sidecars, all added | pass |

The ten added paths are the v0.4 main revision, identity/authority addendum,
acceptance-plan addendum, v0.3 review response, and v0.4 independent-review
brief, each with its sidecar. There was no other added path, modification, or
deletion.

### 2.2 Exact 34-path SHA-256 authentication

Every supplied path existed and its independently computed file SHA-256
matched before its content was relied upon. For a sidecar row, the value below
is the hash of the sidecar file itself.

| # | Exact input | Verified SHA-256 |
|---:|---|---|
| 1 | `AGENTS.md` | `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` |
| 2 | `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| 3 | `s0-lab/i1/spec/public-runtime-v0.14.json` | `fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08` |
| 4 | `s0-lab/i1/spec/public-runtime-files.sha256` | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` |
| 5 | `s0-lab/i1/verification/implementation-files.sha256` | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` |
| 6 | `s0-lab/i1/verification/implementation-manifest.sha256` | `1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6` |
| 7 | `s0-lab/control/s0-protocol-v0.3-canonical-r1.md` | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` |
| 8 | `s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256` | `88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3` |
| 9 | `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md` | `512714d8745bb78c08b0b6fd085f978c84fb0b7d2439dbbae0138d2f92ef9b90` |
| 10 | `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.sha256` | `7ef1b8461efcf822baf0f29854d02e08c3f42dc519a1fffe02a997140aa7e392` |
| 11 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md` | `e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4` |
| 12 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256` | `41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3` |
| 13 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md` | `3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1` |
| 14 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.sha256` | `566bba9b81d4ed5216f9c49c01448154f0a2a53ee6d9cfa13e0d9993475df70c` |
| 15 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md` | `534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1` |
| 16 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.sha256` | `29ec3013bab28aa1265653ad4badc034381fa91cbd40a0aa44443359a9d70060` |
| 17 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.md` | `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b` |
| 18 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.sha256` | `90b2643bd2128339261ea0eae6c334ae757d5fa096cae3e9d73b8ff7ae606757` |
| 19 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.md` | `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a` |
| 20 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.sha256` | `14ad4440f996f6b637b8adb667b3975a9040ee70d8da503d5be700646438d72b` |
| 21 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.md` | `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3` |
| 22 | `s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.sha256` | `d2bac18a3bef1ec769e9f97149fa6d74bd4536b7454151ec6113fe355f9a86d7` |
| 23 | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/trust-root-role-isolation-design-v0.3-independent-rereview.md` | `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9` |
| 24 | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/trust-root-role-isolation-design-v0.3-independent-rereview.sha256` | `955a51e46dc7901a9c08acf82723d3861677331f7ab4e87f0a9983751fad9612` |
| 25 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| 26 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256` | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| 27 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| 28 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256` | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| 29 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| 30 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256` | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| 31 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/review-response-v0.3.md` | `6ddb194426353a42a907d8b7ba9b5fe5feac5b29c20d6a59daa09cbcfc853478` |
| 32 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/review-response-v0.3.sha256` | `04522b1a9221019fb6f83efaf04da895c031135bc5c51d2b3cf5240a9f409b86` |
| 33 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-independent-review-brief-v0.4.md` | `d6d80771a4793a3153ae35cb4cbcc6177eb8f72ac4c779daaebb8adb6e797a96` |
| 34 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-independent-review-brief-v0.4.sha256` | `954da2f732018336ace0b1609caeb7c9d20db7ad27bba80d3e6b6666433a9e35` |

### 2.3 Canonical and file-specific validation results

The authenticated canonical validator was used. A direct invocation was first
blocked before script execution by the local PowerShell execution policy; the
same authenticated script was then launched with `-ExecutionPolicy Bypass`.
Its actual SelfTest passed all eleven cases, including byte-level UTF-8 BOM,
invalid UTF-8, final-LF, trailing-whitespace, and canonical/noncanonical
sidecar controls.

All 14 admitted Markdown/same-basename-sidecar pairs were then supplied to the
same validator as one array. Every independently labeled file-presence, UTF-8,
BOM, final-LF, trailing-whitespace, sidecar-presence, sidecar-text,
sidecar-record/hash, and artifact-overall check passed. Final result was
`OVERALL=PASS`. An earlier `-File` array-binding attempt stopped in PowerShell
argument parsing before validator execution and supplied no evidence; the
successful array invocation is the validation result relied upon here.

The four file-specific I1 inputs received only permitted read-only JSON and
manifest checks:

- the runtime JSON parsed and its declared arrays reproduced 32 role rows, 40
  positions, eight paired rows, 27 stores, 46 reader entries, 64 edges, 22
  signer roles, 14 status edges, 15 status states, and 17 status-receipt
  entries;
- all store writer/reader role-position bindings and referenced edge IDs were
  present, with zero binding errors;
- `public-runtime-files.sha256` had seven canonical unique records and bound
  the admitted runtime JSON;
- `implementation-files.sha256` had 26 canonical unique records and cross-bound
  the admitted runtime JSON and public-runtime manifest; and
- `implementation-manifest.sha256` had one canonical record binding the
  admitted implementation manifest hash.

These are integrity, topology-count, and public cross-binding checks, not an
implementation or acceptance result.

## 3. Independent effective-composition reconstruction

The effective candidate is the authenticated predecessor composition followed
by the bounded v0.4 overlay:

1. the authenticated v0.1 base survives through the authenticated v0.2 overlay;
2. the authenticated v0.3 overlay survives except at the exact v0.4 replacement
   scopes;
3. v0.3 design section 2.6 and its partial additive import-event grammar are
   replaced in full by v0.4 design section 2;
4. v0.3 section 2.5 changes only for the now-exact two direct pre-pending
   terminal records;
5. the v0.2 common signer-media grammar and import-zero result-medium rule are
   replaced only for `route_kind=import`; non-root request and root-ceremony
   schemas remain unchanged;
6. v0.3 design section 3 and all `TRI2-VEC-01` authority are replaced in full
   by v0.4 design section 3;
7. v0.3 matrix sections 7 and 8 and import-event serialization implications
   change only as stated in the v0.4 matrix;
8. the v0.3 acceptance meanings of `ISO-K20`, `ISO-K28`, the two pre-pending
   terminal records, and directly related hostile traces change only as stated
   in the v0.4 plan; and
9. review responses grant no design authority, while the v0.4 brief governs
   only this review.

No v0.4 clause changes an unlisted v0.1, v0.2, or v0.3 meaning. The candidate
diff is limited to the five v0.4 public pairs, the predecessor inputs are
byte-authenticated and immutable, and the candidate repeatedly preserves the
topology, signature-scope, ledger, A-D, provider, implementation, protected-
material, E0, and S0 boundaries. This independently supports the bounded claim
that v0.4 changes only the two open predecessor findings.

## 4. Independent `TRI2-M01` reconstruction

### 4.1 Complete record and exact byte contract

The import event contains exactly these 31 fields, once each and in this order:

1. `signer_media_event_schema`
2. `namespace`
3. `sequence`
4. `previous_event_sha256`
5. `event_id`
6. `prior_route_event_id`
7. `campaign_id`
8. `ceremony_id`
9. `signer_id`
10. `route_kind`
11. `route_class`
12. `request_id`
13. `attachment_capability_id`
14. `admission_event_id`
15. `admission_record_sha256`
16. `media_object_sha256`
17. `media_object_id`
18. `result_media_id`
19. `result_media_kind`
20. `reserved_media_event_id`
21. `admission_frozen_media_event_id`
22. `pending_media_event_id`
23. `completion_media_event_id`
24. `outcome_schema`
25. `outcome_frame_sha256`
26. `outcome_class`
27. `before_appliance_state`
28. `after_appliance_state`
29. `state`
30. `terminal_from`
31. `decision`

The sole schema/version field is line 1 with the exact value
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1`; its terminal `-1` is the version. No
second version field is permitted. Each emitted record is exactly 31 ASCII
`name=value` lines, every line ends with byte `0A`, and the final decision line
also ends in `0A`. BOM, CR, NUL, blank line, trailing whitespace, duplicate,
missing, reordered, unknown, or extra field rejects. Therefore the v0.2 common
schema, v0.3 additive-block reading, 30/32-field forms, duplicate
`result_media_id`, and alternative version field have no parsing authority.

There is no self-hash field. The event preimage is the concatenation of all 31
ASCII lines and their 31 LF bytes; `event_sha256` is SHA-256 of those exact
bytes. `previous_event_sha256` is the hash of the immediately prior event in
the global `signer-media` namespace, or 64 zeroes only at namespace sequence
zero. `prior_route_event_id` is separately the immediately prior event ID for
this import route. A correct global predecessor cannot compensate for a wrong
route predecessor, and the converse also rejects.

### 4.2 Route bindings, class states, and event identities

Let `Z` be 64 ASCII zeroes. `R`, `A`, `P`, and `C` are distinct, nonzero,
project-lifetime unique reserved, admission-frozen, pending, and completion
event IDs. Their exact use is not interchangeable. An early terminal uses `C`,
burns unused later-route IDs, and permits no reuse.

| Route class | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

Across a route, campaign, ceremony, signer, class, capability, nonzero result-
medium ID, result kind, all four preallocated IDs, and outcome schema remain
byte-equal. `route_kind=import` and `request_id=Z` are constant. Before
admission freeze, `admission_event_id`, admission-record hash, package hash,
and package object ID are all `Z` (`ADM0`). At and after admission freeze they
are the immutable tuple `(A, exact admission-byte hash, admission-bound package
hash, admission-bound package object ID)` (`ADM1`).

### 4.3 Total lifecycle table

`H` is governed by section 4.4 of this review.

| Variant | Event/prior | Admission | Frame | Outcome | Before/after | State/from/decision |
|---|---|---|---|---|---|---|
| reserved | `R` / `Z` | `ADM0` | `Z` | `none` | `none -> none` | `reserved` / `none` / `reserved` |
| admission frozen | `A` / `R` | `ADM1` | `Z` | `none` | `none -> none` | `admission-frozen` / `none` / `approved` |
| pending | `P` / `A` | `ADM1` | `Z` | `none` | `SRC -> none` | `pending` / `none` / `executing` |
| accepted completion | `C` / `P` | `ADM1` | `H` | `accepted` | `SRC -> DST` | `consumed` / `none` / `accepted` |
| terminal from reserved | `C` / `R` | `ADM0` | `Z` | `none` | `none -> none` | `terminal` / `reserved` / `rejected` |
| terminal from admission frozen | `C` / `A` | `ADM1` | `Z` | `none` | `none -> none` | `terminal` / `admission-frozen` / `rejected` |
| parse rejection | `C` / `P` | `ADM1` | `H` | `parse-rejected` | `SRC -> SRC` | `terminal` / `pending` / `rejected` |
| validation rejection | `C` / `P` | `ADM1` | `H` | `validation-rejected` | `SRC -> SRC` | `terminal` / `pending` / `rejected` |
| state-commit failure | `C` / `P` | `ADM1` | `H` | `state-commit-failed` | `SRC -> indeterminate` | `terminal` / `pending` / `rejected` |
| crash | `C` / `P` | `ADM1` | `Z` | `crash` | `SRC -> indeterminate` | `terminal` / `pending` / `rejected` |
| missing | `C` / `P` | `ADM1` | `Z` | `missing` | `SRC -> indeterminate` | `terminal` / `pending` / `rejected` |
| duplicate | `C` / `P` | `ADM1` | `Z` | `duplicate` | `SRC -> indeterminate` | `terminal` / `pending` / `rejected` |
| disagreement | `C` / `P` | `ADM1` | exact section 4.4 rule | `disagreement` | `SRC -> indeterminate` | `terminal` / `pending` / `rejected` |

No other tuple parses. There is no terminal from consumed, no event after
consumed or terminal, and no direct reserved-to-pending, reserved-to-consumed,
or admission-frozen-to-consumed transition. Thus a wrong event ID, prior-route
ID, admission tuple, frame hash, outcome, before/after state, terminal source,
or decision has one result: reject the event without authorized state advance.

### 4.4 Complete-frame hash, authority, and order

`H` is SHA-256 of one complete canonical outcome frame, including the
`outcome_body_sha256` line and final LF. A frame can supply `H` only when it is
uniquely selectable, at most 2,048 bytes, followed only by zeroes, canonical,
body-hash correct, and has an allowed decision/reason/state tuple.

- `accepted`, `parse-rejected`, `validation-rejected`, and
  `state-commit-failed` require `H`.
- `crash`, `missing`, and `duplicate` require `Z`; crash precedence ignores
  apparent bytes, and duplicate evidence never selects a frame.
- `disagreement` requires `H` for exactly one internally canonical frame that
  conflicts with admission, host, ledger, witness, or anti-replay evidence. It
  requires `Z` for malformed, oversized, bad-body-hash, invalid-tuple, or
  non-uniquely-selectable bytes.

Raw observations remain bounded failure evidence outside the event hash. A
ledger event hash cannot select one duplicate frame.

Authority is separated: CONTROL host preflight reserves identities, freezes
admission, and authorizes attachment; the pinned target
`S0-IMPORT-TRANSITION-TCB-1` alone emits the unsigned frame; CONTROL post-run
admission alone applies frozen classification precedence; and the ledger/
witness provider alone verifies uniqueness, legal transition, both chains,
and durable atomic acceptance or rejection. The provider cannot create a
success classification.

The exact order is `R`, `A`, powered-off attachment and `P`, one boot,
controlled stop, both-media detachment, final classification, then exactly one
consumed or terminal `C`. A pre-pending failure may terminalize only from the
last durable `R` or `A`. If `C` conflicts or ledger/witness append fails, no
replacement ID, reconstructed completion, redraw, waiver, or retry is allowed.
An accepted target frame cannot make `DST` available until consumed `C`
persists.

The outcome frame binds the planned completion ID, while completion binds the
frame hash. The frame contains neither the future event hash nor a future
ledger head, and the event has no self-hash field. There is no frame/event hash
cycle. The unsigned frame/event creates no signature, signer, registry
authority, experimental topology object, signature scope, or fourth ledger.

These rules supply one byte serialization for every import-event state, both
complete pre-pending terminal records, deterministic frame-hash selection,
both mandatory chains, and a closed one-shot lifecycle. `TRI2-M01` is closed at
the public-design-text level for this review.

## 5. Independent `TRI2-m01` reconstruction

The v0.2 false attribution to RFC 9381 section 5.4.5 remains removed. The v0.3
`y0` and `y1` coordinates, relation `y1 = p - y0`, and all four
`TRI2-VEC-01` literals are withdrawn from effective vector, implementation,
and acceptance authority. They remain historical failure evidence only; no
old coordinate, relation, row, literal, or copied label can satisfy
`ISO-K28`.

The authenticated v0.2 `S0-ED25519-STRICT-1` text remains authoritative and
unchanged outside the withdrawn order-eight evidence bullet. Its exact public-
key decode/re-encode, nonidentity, order-`L`, signature-point, `S < L`, and
uncofactored-equation predicates and all application points survive. The v0.4
overlay neither weakens nor substitutes that profile.

No replacement coordinate or literal is frozen, no vector is created, and no
point-order result is claimed. Before key generation, a separately opened
`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR AUTHORING OPEN` gate must freeze a
`TRI2-VEC-02` artifact with exactly four pairwise-distinct candidate encodings.
For every row, separately frozen construction and independent verification
must establish the exact literal derivation, RFC 8032 canonical decode,
byte-identical re-encode, `P != I`, `[8]P = I`, `[4]P != I`, `[L]P != I`, and
strict rejection as both `A` and `R` where applicable. The artifact,
derivation, and independent verification must all be frozen before use.
Missing, ambiguous, inconsistent, or failed evidence blocks key generation
without old-literal fallback, substitution, waiver, or retry.

Withdrawal plus this explicit pre-key-generation blocker is a safe public-
design closure: unsupported data has no authority, while the strict rejection
predicate remains intact and no absent future vector is treated as a pass.
`TRI2-m01` is closed at the public-design-text level for this review.

## 6. Mandatory hostile tabletop traces

The following traces apply independently to all three import classes. A
terminal append is attempted only with the exact preallocated `C` and usable
ledger/witness; an append conflict or failure remains bounded failure evidence
and authorizes no invented completion.

| Mutation or observation | Unique fail-closed rule |
|---|---|
| Old common schema, v0.3 additive block, duplicate `result_media_id`, second version field, 30/32 fields, reorder, extra/missing line or field | Exact sole schema and 31-field ordered grammar reject the record under `ISO-K20`. |
| CR, BOM, NUL, blank line, trailing whitespace, or missing final LF | Exact ASCII/LF byte contract rejects; no event hash or state authority exists. |
| Wrong global predecessor with correct route predecessor, or the converse | The global hash chain and route-local ID chain are separate and both mandatory; ledger/witness rejects the append. |
| Any lifecycle row with wrong `R/A/P/C`, prior ID, ADM tuple, frame hash, outcome, before/after state, terminal source, or decision | The total lifecycle table admits no alternative tuple; reject without state advance or replacement. |
| Terminal from reserved has admission bytes or appliance state; terminal from admission-frozen has zero/changed ADM fields or appliance state | The exact direct-terminal rows require respectively `ADM0` or `ADM1`, both with zero frame, `none`, and `none -> none`; reject every invented-state variant. |
| Pending has `before=none`, wrong class source, known after-state, non-none outcome, or frame hash | Pending is exactly `SRC -> none`, `outcome_class=none`, frame `Z`; reject. |
| Consumed lacks the exact accepted frame or durable append | Only accepted `H`, `SRC -> DST`, and persisted consumed `C` make `DST` available; otherwise no success exists. |
| Parse/validation rejection changes state | Those canonical frames require `SRC -> SRC`; an inconsistent frame becomes disagreement and cannot advance state. |
| State-commit failure claims a known after-state | The canonical failure requires `SRC -> indeterminate`; an invalid tuple becomes disagreement and grants no destination authority. |
| Crash, missing, or duplicate claims a frame hash or known after-state | Each requires frame `Z` and `SRC -> indeterminate`; crash also ignores apparent bytes and duplicate selects none. |
| Disagreement hashes malformed/non-unique bytes | Malformed, invalid, oversized, bad-hash, or non-unique bytes require frame `Z`; reject nonzero hash. |
| Disagreement records zero for one uniquely selectable canonical but conflicting frame | The exact unique-frame rule requires `H`; reject zero hash. |
| Cross-signer, cross-class, cross-package, cross-campaign, capability, medium, event-ID, or route-field substitution | Byte-equal route bindings, exact admission tuple, frame bindings, and both chains reject the substitution as disagreement or pre-pending admission failure. |
| Early terminal followed by reuse of unused IDs | Early terminal burns unused IDs, route termination forbids later records, and project-lifetime uniqueness rejects reuse. |
| Completion conflict followed by redraw or append failure followed by reconstructed success | No new ID, append, or completion may be invented; destination stays unavailable and the route cannot retry. |
| Any retry, selective replay, replacement completion, or waiver | One-shot lifecycle, spent capability/IDs, and `ISO-K20` reject it. |
| Unsigned frame/event treated as signature, signer, key, registry authority, experimental role/store/reader/edge, signature scope, or fourth ledger | Explicit authority and topology boundaries reject that interpretation. |
| One old v0.3 coordinate, relation, or literal remains authoritative or the withdrawn table is evidence | Full withdrawal and effective `ISO-K28` reject the vector package and block key generation. |
| Missing `TRI2-VEC-02` is treated as pass, a row is absent/duplicated, or independent derivation/decode/re-encode/order/rejection evidence is skipped | The future prerequisites are conjunctive and noncompensatory; key generation remains blocked. |
| Strict predicate is weakened, copied-label evidence is trusted, or v0.4 claims vector execution/point order | The inherited strict profile remains exact, and v0.4 makes no vector or point-order result claim; reject the package/claim. |
| Count, fairness, signature-scope, ledger-namespace, provider, closed-gate, or maximum-claim drift | Frozen inventories and nonclaims reject the candidate; no such v0.4 drift was found. |

Every mandatory mutation has one exact fail-closed interpretation. No
unhandled, multiply interpreted, waived, or operator-selected mutation was
found.

## 7. Frozen inventory and non-regression

### 7.1 Counts and topology

| Inventory | Effective value | Review result |
|---|---:|---|
| aggregated role rows | 32 | preserved |
| role positions | 40 | preserved |
| paired rows | 8 | preserved |
| experimental section-4 signers | 21 | preserved |
| positions with signer `none` | 19 | preserved |
| non-row root | 1 | preserved |
| registry IDs | 22 | preserved |
| experimental stores | 27 | preserved |
| explicit readers | 46 | preserved |
| experimental edge rows | 64 | preserved |
| noncompensatory acceptance rows | 107 | preserved |
| exclusive signature scopes | 3 | preserved |
| ledger namespaces | 3 | preserved |
| future executor invocation/session units | 8 | preserved |
| maximum concurrency | 3 | preserved |

The 107 acceptance rows remain platform 19, channel 14, media/route 22,
independence eight, trust/signer 34, and lifecycle ten. V0.4 adds or removes no
row. All remain noncompensatory: one failure, skip, waiver, ambiguous result,
missing record, substituted test, or operator-selected interpretation fails.

The three signature scopes remain exactly `preactivation-pop-v1`,
`section4-generic-envelope-v1`, and `inherited-signature-unresolved`. The three
ledger namespaces remain ceremony, signer-media, and invocation. The outcome
medium, unsigned frame, TCB service, classification, and event are control
objects on an existing administrative route, not additions to the 27/46/64
experimental topology.

### 7.2 A-D opportunity and closed authority

Conditions A-D retain the same source information, authority, model condition,
time, output, question, scoring opportunity, two blocks, and one fresh session
per condition/block. The eight execution opportunities and concurrency maximum
three remain unchanged. V0.4 supplies no condition-specific role, signer,
store, reader, edge, route, model call, output opportunity, hidden input, or
scoring advantage.

Signer-custody, external/provider, inherited-signature, ledger/witness,
implementation, vector execution, key generation, protected-material,
provider/model, E0, and S0 prerequisites remain unresolved or closed as
applicable. No v0.4 text claims implementation, operational safety, economic
value, model-to-model transfer, central-system completion, Project Brain
integration, E0, or S0 validation.

## 8. Findings, verdict, and maximum claim

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |
| total | 0 |

Both predecessor findings are closed only at the authenticated public-design-
text level described above. No regression or new finding was found.

`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

The maximum supported claim is that this authenticated v0.4 public design is
internally complete for the bounded `TRI2-M01` and `TRI2-m01` repairs,
preserves the audited public isolation/fairness/topology boundaries, and may be
considered separately by CONTROL for integration. This verdict does not itself
open CONTROL integration or any later gate.

The only next gate that CONTROL may separately decide whether to open is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 CONTROL INTEGRATION DECISION OPEN`

Implementation, vector authoring, key generation, protected material,
provider/model sessions, fixture/oracle work, E0, S0, and `main` integration
remain closed.

## 9. Evidence classification and limits

- Facts are the authenticated Git identities and diff, file hashes, validator
  outputs, literal admitted document clauses, parsed public JSON/manifests, and
  reproduced counts/cross-bindings.
- Inferences are the effective-composition reconstruction, lifecycle and
  hostile paper traces, finding closures, zero-finding count, severity
  assessment, and verdict.
- Proposals: none are made by this review. Candidate future-gate prerequisites
  and the brief's possible next authority are reported as design facts, not
  implemented recommendations.
- Test results are limited to Git inspection, SHA-256 hashing, canonical text
  validation and validator SelfTest, read-only JSON parsing, manifest-shape and
  cross-binding checks, and manual public tabletop traces.

No cryptographic vector construction, point decoding, scalar multiplication,
order checking, key/signature operation, schema/parser execution,
implementation inspection, platform/provider acceptance, protected-data
access, model call, E0 test, or S0 test occurred. This review establishes no
live ledger, witness, TCB, appliance, operational-safety, economic-value,
central-system, Project Brain, or model-transfer result.
