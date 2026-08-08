# URC-0.12 public falsification plan v0.9

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.12 REDESIGN OPEN`
- companion: `universal-response-contract-v0.12-candidate.md`
- predecessor evidence: authenticated plans v0.4-v0.8 and v0.11 independent review v0.1
- excluded: implementation, bank/fixture/oracle authoring, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Complete effective-plan construction

### 1.1 Authenticated source identities

The effective plan is a direct five-source composition:

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `P4` | `question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| `P5` | `question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` |
| `P6` | `question-contract-v0.9/public-falsification-plan-v0.6.md` | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` |
| `P7` | `question-contract-v0.10/public-falsification-plan-v0.7.md` | `07edb8ec3044874f39ed60f1a6952eb64e369715fc1501fd309888c9b24d09dd` |
| `P9` | this `public-falsification-plan-v0.9.md` | its matching same-basename sidecar after this file freezes |

P8 and its review are authenticated predecessor evidence, not byte sources. All effective v0.11 custody slices are replaced below; P7 section 5 remains the latest unchanged bank-balance/freeze source.

### 1.2 Total transitive section map

Every v0.11 effective-plan slot is retained or replaced exactly once.

| Effective slot | Effective v0.11 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `P9` section 1, heading `## 1. Complete effective-plan construction` |
| 2 | slot 2 | retain | full `P4` section 2, heading `## 2. Facts, inferences, and proposals` |
| 3 | slot 3 | retain | full `P5` section 2, heading `## 2. Role isolation rules` |
| 4 | slot 4 | replace | full `P9` section 2, heading `## 2. Corrected complete role matrix` |
| 5 | slot 5 | replace | full `P9` sections 3-5, from `## 3. Exact named store identities` through `## 5. Closed matrix-ledger bijection` |
| 6 | slot 6 | retain | full `P5` section 5, heading `## 5. Blinded analysis-design map` |
| 7 | slot 7 | retain | full `P7` section 5, heading `## 5. Restored bank balance and freeze sequence` |
| 8 | slot 8 | replace | full `P9` section 6, heading `## 6. Replacement P0 and P1 requirements` |
| 9 | slot 9 | retain | full `P4` section 7, heading `## 7. P2 — no-record leakage and neutral-token equivalence` |
| 10 | slot 10 | retain with two fixed transforms | full `P5` section 8, heading `## 8. Prospective and confirmatory seeds` |
| 11 | slot 11 | retain | full `P4` section 9, heading `## 9. P3 — representation-alignment equivalence` |
| 12 | slot 12 | retain | preamble `P4` section 10, from `## 10. Deterministic N and guaranteed-balanced schedule` to immediately before `### 10.1 Smallest sufficient N` |
| 13 | slot 13 | retain | full `P4` section 10.1, heading `### 10.1 Smallest sufficient N` |
| 14 | slot 14 | retain | full `P4` section 10.2, heading `### 10.2 P2 schedule` |
| 15 | slot 15 | retain | full `P4` section 10.3, heading `### 10.3 P3 schedule construction and proof` |
| 16 | slot 16 | retain | full `P5` section 9, heading `## 9. Revision, transport, and elapsed custody` |
| 17 | slot 17 | retain | preamble `P4` section 11, from `## 11. Feasibility and ceilings` to immediately before `### 11.1 Simulation benchmark` |
| 18 | slot 18 | retain | full `P4` section 11.1, heading `### 11.1 Simulation benchmark` |
| 19 | slot 19 | retain | full `P4` section 11.2, heading `### 11.2 Confirmatory ceilings at N=720` |
| 20 | slot 20 | retain | full `P6` section 7, heading `## 7. Revised human and resource ledger` |
| 21 | slot 21 | retain | preamble `P4` section 12, from `## 12. P4 — comparator reliability and burden` to immediately before `### 12.1 Output consequences` |
| 22 | slot 22 | retain | full `P4` section 12.1, heading `### 12.1 Output consequences` |
| 23 | slot 23 | retain | full `P5` section 11, heading `## 11. Comparator reliability replacement` |
| 24 | slot 24 | retain | full `P4` section 12.3, heading `### 12.3 Exact burden metrics` |
| 25 | slot 25 | replace | full `P9` section 7, heading `## 7. Equality, stopping, rollback, and claim limit` |

No P4-P8 effective range is unspecified. Every P8-derived effective slice is replaced; the predecessor file remains failure evidence only.

### 1.3 One complete plan-record grammar

Use only companion candidate section 3.3 steps 1-7 for source authentication, heading resolution, slicing, and heading-digest computation. Do not emit the companion contract record. For plan records, emit this complete grammar once:

```text
slot=<decimal slot>\n
source=<P4|P5|P6|P7|P9>\n
source_sha256=<64 lowercase hex>\n
slice_start_heading_sha256=<64 lowercase hex>\n
slice_end_heading_sha256=<64 lowercase hex>\n
slice_mode=<full|preamble>\n
transform_count=<decimal 0|2>\n
<zero or two transform blocks in ascending transform number>
length=<decimal transformed-content byte count>\n
<transformed content bytes>
```

Each transform block is exactly:

```text
transform_<n>_from_hex=<lowercase even-length hex>\n
transform_<n>_to_hex=<lowercase even-length hex>\n
transform_<n>_required_occurrences=<decimal positive count>\n
```

All metadata bytes are ASCII. Heading digests are SHA-256 over exact strict-UTF-8 heading text bytes without final LF and without normalization. Every named field occurs exactly once. There is no inherited or inserted second `slice_mode`.

Every slot except 10 emits `transform_count=0` and no transform block. Slot 10 emits `transform_count=2` and these blocks in this order:

```text
transform_1_from_hex=76302e38
transform_1_to_hex=76302e3132
transform_1_required_occurrences=1
transform_2_from_hex=5552432d302e38
transform_2_to_hex=5552432d302e3132
transform_2_required_occurrences=1
```

The hex pairs mean exact ASCII `v0.8` to `v0.12` and `URC-0.8` to `URC-0.12`. Apply blocks sequentially to the authenticated raw P5 section 8 slice. Before each replacement, its exact source byte sequence must occur once and only once; otherwise construction rejects. Replacement is global for that one occurrence, with no normalization or case folding. Neither replacement changes a formula, seed field, threshold, or allowed seed use.

The effective stream is ASCII `URC-0.12-PLAN-EFFECTIVE\n` followed by the 25 records with no separator beyond the grammar bytes. `effective_plan_sha256` is SHA-256 of that stream and freezes only in a later reviewed manifest after the P9 sidecar exists.

## 2. Corrected complete role matrix

The inherited isolation rules remain. Omission is denial; worktrees isolate edits only; paired independent roles are distinct fresh roots; conversation text and ambient repository access are not transfer channels. “Public specification” means only independently reviewed public bytes and never bank content, labels, outputs, condition maps, or sealed material.

| Role | Positive inputs | Explicit denylist | Only output / store |
|---|---|---|---|
| CONTROL registrar | authenticated reviewed public specification bytes/hashes, role/store/key assignment matrix, artifact/pass/reject digests, anonymous analysis hash, publication-receipt digest | bank/prompt contents, labels, raw/anonymous semantic outputs, condition map, executor reasoning, sealed material | recipient-specific signed public-specification grants E00A-H/E01 and signed canonical status envelopes in `registrar-store` |
| public status reader | signed status envelopes delivered from `registrar-store` by E52; public registrar key registry | every bank/prompt byte, label, output, condition map, comparator/judge internals, sealed material | none; terminal read-only role |
| public record publisher | publication/transport/signing specification and public key registry by E00G; exact final decision record and digest by E53 | raw output, labels, condition map, anonymous tables, threshold inputs, sealed material | byte-identical decision record plus signed canonical publication receipt in `public-decision-store` by E54 |
| public record reader | exact decision record and publication receipt delivered by E55; public publisher key registry | every nonpublic experimental artifact and sealed material | none; terminal read-only role |
| content-intake custodian | frozen author bank/prompts and signature | labels, outputs, condition map, sealed material | immutable content and exact copies in `content-vault` |
| simulation builder/operator | frozen statistical/catalog specifications and pre-bank manifest | bank facts, prompts, labels, confirmatory output, condition map | implementation/benchmark/calibration/power summaries; selected constants and public formula manifest to `analysis-input-vault` |
| public fact author | frozen authoring protocol, constraints, selected N | labels, representations, outputs, sealed/real material | frozen bank/prompts to content intake |
| label author A / B | exact content copy and frozen contract | other label, representations, outputs, condition map | separate signed bundles in `label-vault-A` and `label-vault-B` respectively |
| label-comparison custodian | signed A/B bundles | representations, packages, outputs, condition map | equality digest; agreed bundle only in `agreed-label-vault` |
| representation builder | exact content copy and frozen transformation specification | labels, expected values, outputs | representations/equality manifest in `representation-vault` |
| package builder / scanner 1 | assigned representation, questions, runner allowlist, scanner specification | labels, expected answers, outputs, sealed material | signed package in `signed-package-vault`; scan-1 table in `scan-vault-1` |
| scanner 2 | completed signed package and scanner specification | scan-1 table/internals, labels, outputs | scan-2 table in `scan-vault-2` |
| scan-comparison custodian | scan-1/scan-2 tables | package prose, labels, outputs, condition map | equality/pass or reject digest |
| leakage reviewer 1 / 2 | signed package, agreed labels, leakage-review specification | executor output, condition map/narrative, other reviewer, sealed material | separate signed tables in `leakage-vault-1` and `leakage-vault-2` respectively |
| leakage-comparison custodian | two leakage tables | package prose beyond hash, outputs, condition map | equality/pass or reject digest |
| comparator builder 1 / 2 | frozen metadata, ID-order, semantic-atom, cause/evaluation/consumption, canonicalization, mutation specifications | other comparator internals, confirmatory output, condition map | implementation/mutation table in `comparator-vault-1` and `comparator-vault-2` respectively |
| expected-catalog generator 1 / 2 | frozen catalog, semantic-atom, and ID-order specifications and later agreed labels | comparator output/internals, confirmatory output, condition map | abstract and bank-instance tables in `generator-vault-1` and `generator-vault-2` respectively |
| catalog-comparison custodian | both generator tables | comparator/confirmatory output, condition map | agreed tables/digests in `catalog-vault` |
| P1 reviewer 1 / 2 | frozen specifications, agreed tables, rejection summaries | comparator/confirmatory output, condition map, other review | signed catalog reviews in `p1-review-vault-1` and `p1-review-vault-2` respectively |
| P1-review comparison custodian | two P1 reviews | bank prose beyond hashed IDs, outputs, condition map | agreement/pass or reject digest |
| condition-map/schedule custodian | finalized signed packages, representations/equality manifest, A-D identities, bank hash, schedule rules, opaque run IDs | labels, expected answers, raw output, judgments | semantic map in `condition-map-vault`; opaque schedule/routing; assigned signed package to dispatcher |
| blinded-map builder 1 / 2 | frozen P2-P4 formulas, semantic condition/schedule map, opaque namespace | labels, expected answers, output, other builder | separate blinded coefficient/stratum maps |
| analysis-map comparison custodian | two blinded maps | labels, outputs, semantic names after comparison | agreed blinded map in `analysis-map-vault` |
| dispatcher/transport recorder | opaque schedule/routing and one assigned signed package | labels, expected answers, semantic map, prior outputs | request, signed run log, monotonic endpoints, first raw response in `raw-output-vault` |
| public executor | one signed package, common resources, opaque run ID | labels, mappings, comparators, mutations, other packages/outputs, forbidden tools/network | first raw response stream only |
| raw-output custodian/anonymizer | raw vault, routing map, run logs, anonymization rules | labels, expected answers, semantic condition map, comparator logic | raw hashes, anonymous semantic bundle, anonymous timing/byte table |
| semantic judge 1 / 2 | agreed labels, anonymous parseable output, reason rubric | condition map, timing/cost/load, other judge, sealed material | separate signed anonymous judgments in `judgment-vault-1` and `judgment-vault-2` respectively |
| judgment-comparison custodian | two judgment tables; signing specification and key assignment | condition map, timing, raw package identity | signed canonical E43 comparison record/digest and agreed semantic table |
| comparator operator 1 / 2 | assigned comparator, agreed labels/expected table, anonymous output, agreed semantic table and E43 comparison record | condition map, timing, other comparator internals | anonymous atom/event/total and P1 comparison tables |
| adjudication-comparison custodian | both comparator tables; signing specification and key assignment | raw prose, condition map, timing | signed canonical E45 comparison record/digest and agreed derived table |
| analysis role | agreed derived table and E45 comparison record, timing table, selected calibrated constants, public formula manifest, opaque IDs, agreed blinded map, frozen statistical decision table | raw prose, executor reasoning, semantic condition map | frozen anonymous P2-P4 statistics/decision inputs/hash |
| final-decision custodian | frozen anonymous analysis, post-hash semantic map, frozen decision table | raw output, reanalysis, threshold changes | mechanical join and exact public decision record in `final-decision-vault` |

## 3. Exact named store identities

Each row names a literal global store ID, one writer, and all readers.

| Store ID | Only writer | Authorized readers |
|---|---|---|
| `registrar-store` | CONTROL registrar through E51 only | public status reader through E52 only |
| `public-decision-store` | public record publisher through E54 only | public record reader through E55; registrar by publication-receipt digest through E56 only |
| `content-vault` | content-intake custodian | label A, label B, representation builder |
| `label-vault-A` | label author A | label-comparison custodian |
| `label-vault-B` | label author B | label-comparison custodian |
| `agreed-label-vault` | label-comparison custodian | generators, leakage reviewers, judges, comparator operators |
| `representation-vault` | representation builder | package builder, condition-map custodian |
| `signed-package-vault` | package builder | scanner 2, leakage reviewers, condition-map custodian |
| `scan-vault-1` | package builder/scanner 1 | scan-comparison custodian |
| `scan-vault-2` | scanner 2 | scan-comparison custodian |
| `leakage-vault-1` | leakage reviewer 1 | leakage-comparison custodian |
| `leakage-vault-2` | leakage reviewer 2 | leakage-comparison custodian |
| `comparator-vault-1` | comparator builder 1 | comparator operator 1 |
| `comparator-vault-2` | comparator builder 2 | comparator operator 2 |
| `generator-vault-1` | expected-catalog generator 1 | catalog-comparison custodian |
| `generator-vault-2` | expected-catalog generator 2 | catalog-comparison custodian |
| `analysis-input-vault` | simulation builder/operator | analysis role only after calibration freeze |
| `catalog-vault` | catalog-comparison custodian | P1 reviewers, comparator operators, registrar by digest only |
| `p1-review-vault-1` | P1 reviewer 1 | P1-review comparison custodian |
| `p1-review-vault-2` | P1 reviewer 2 | P1-review comparison custodian |
| `condition-map-vault` | condition-map custodian | blinded-map builders before calls; final-decision custodian only after E48 |
| `analysis-map-vault` | analysis-map comparison custodian | analysis role |
| `raw-output-vault` | dispatcher/transport recorder | raw-output custodian |
| `judgment-vault-1` | semantic judge 1 | judgment-comparison custodian |
| `judgment-vault-2` | semantic judge 2 | judgment-comparison custodian |
| `final-decision-vault` | final-decision custodian through E50 only | public record publisher through E53; registrar by decision-record digest through E50 only |

No synonym, unlisted mirror, conversation copy, or ambient directory is an authorized store.

## 4. Canonical custody records, hashes, and signatures

All grammars in this section are exact ASCII with LF line endings, no BOM, no CR, and one final LF. Decimal integers use ASCII `0` or a nonzero first digit followed by digits; leading zeroes reject. SHA-256 and signature hex use lowercase ASCII. SHA-256 values are exactly 64 hex characters. Ed25519 signatures are exactly 128 hex characters encoding the 64 raw signature bytes.

Before any use, E00G delivers a signed public key registry containing the exact 32-byte Ed25519 public key and lowercase SHA-256 key ID for each signing role used here: `control-registrar`, `judgment-comparison`, `adjudication-comparison`, and `public-record-publisher`. A key ID is SHA-256 of the raw 32 public-key bytes. A missing, duplicate, changed, revoked, or role-mismatched key stops before artifact acceptance. No private key is stored in this repository or delivered by any edge.

For any `record_bytes`, define `record_sha256=SHA256(record_bytes)`. The only signature preimage is:

```text
URC-0.12-SIGNED-ARTIFACT\n
signer_role=<closed role ID>\n
signer_key_sha256=<64 lowercase hex>\n
record_length=<decimal byte length>\n
<exact record_bytes>
record_sha256=<64 lowercase hex>\n
```

`record_bytes` already ends in LF; therefore the next ASCII field begins immediately after that one final LF and no separator is inserted. Ed25519 signs exactly this preimage. The signed envelope is the exact preimage followed by:

```text
signature_algorithm=Ed25519\n
signature_hex=<128 lowercase hex>\n
```

Envelope verification recomputes the length, record hash, key ID, role assignment, and signature. No alternate JSON, field order, whitespace, length prefix, concatenation, hash, signature scope, or key is permitted.

### 4.1 Closed registrar status machine

The status chain is a public custody-progress receipt, not an S0 or empirical-success claim. Its evidence order and bit positions are exactly:

| Bit | Evidence edge |
|---:|---|
| 0 | E02 |
| 1 | E05 |
| 2 | E08 |
| 3 | E14 |
| 4 | E21 |
| 5 | E24 |
| 6 | E25 |
| 7 | E27 |
| 8 | E29 |
| 9 | E31 |
| 10 | E35 |
| 11 | E48 |
| 12 | E50 |
| 13 | E56 |

The only status values are `A-0000` through the successful prefix masks `A-0001`, `A-0003`, `A-0007`, `A-000f`, `A-001f`, `A-003f`, `A-007f`, `A-00ff`, `A-01ff`, `A-03ff`, `A-07ff`, `A-0fff`, `A-1fff`, and `A-3fff`. `A` means only that the registrar accepted the next authenticated evidence artifact under that edge's published required check. It never means that S0, representation superiority, or an empirical claim passed.

The exact unsigned status `record_bytes` grammar is:

```text
status_schema=URC-0.12-STATUS-1\n
sequence=<decimal 0..14>\n
previous_record_sha256=<64 lowercase hex>\n
event_edge=<ROOT|E02|E05|E08|E14|E21|E24|E25|E27|E29|E31|E35|E48|E50|E56>\n
event_artifact_sha256=<64 lowercase hex>\n
evidence_mask=<exact four lowercase hex>\n
status_code=A-<same exact four lowercase hex>\n
monotonic_timestamp_ns=<decimal integer>\n
```

The genesis record has sequence 0, previous digest 64 zeroes, event `ROOT`, the authenticated CONTROL-integration manifest SHA-256 as `event_artifact_sha256`, mask `0000`, and status `A-0000`. For sequence `n` from 1 through 14, the event edge must be bit `n-1` in the table, the previous digest must equal SHA-256 of the immediately preceding exact status `record_bytes`, the artifact digest must equal the exact artifact accepted on that edge, the mask must set precisely bits 0 through `n-1`, the status must equal `A-` plus that mask, and the timestamp must be strictly greater than the preceding timestamp. No edge can repeat, skip, arrive as a status transition out of order, clear a bit, or select another status.

An artifact that fails its edge's required check creates no status record, stops the dependent workflow, and preserves its authenticated failure evidence outside `registrar-store` under the already authorized producer/custodian route. An operational artifact may already exist in its listed store, but its status-source delivery to the registrar is not sent until every lower-bit receipt freezes; there is no registrar-side buffer or alternate store. E51 signs and appends exactly the next permitted envelope. E52 delivers the complete envelope chain from genesis through the requested digest. The public status reader can recompute every record hash, signature, sequence, edge, prefix mask, status value, and timestamp ordering without seeing protected experimental bytes.

### 4.2 Unique E43 and E45 comparison records

The E43 unsigned comparison `record_bytes` are exactly:

```text
comparison_schema=URC-0.12-COMPARISON-1\n
edge=E43\n
left_role=semantic-judge-1\n
left_artifact_sha256=<judgment-vault-1 signed table SHA-256>\n
right_role=semantic-judge-2\n
right_artifact_sha256=<judgment-vault-2 signed table SHA-256>\n
agreed_artifact_sha256=<agreed semantic table SHA-256>\n
comparison_result=equal\n
```

The E45 unsigned comparison `record_bytes` are exactly:

```text
comparison_schema=URC-0.12-COMPARISON-1\n
edge=E45\n
left_role=comparator-operator-1\n
left_artifact_sha256=<operator-1 derived table SHA-256>\n
right_role=comparator-operator-2\n
right_artifact_sha256=<operator-2 derived table SHA-256>\n
agreed_artifact_sha256=<agreed derived table SHA-256>\n
comparison_result=equal\n
```

For each edge, `comparison_digest` is exactly SHA-256 of its `record_bytes`. The assigned comparison custodian signs those bytes with the section-4 envelope. E43/E45 deliver the signed envelope, the separately named `comparison_digest`, and the exact agreed table bytes. The recipient recomputes the two fixed-role input hashes, agreed-table hash, record hash, key, signature, and byte equality. Unequal inputs create no agreed table and no E43/E45 artifact; the workflow stops. Left/right swapping, raw concatenation, omitted length, alternate field order, another role ID, another hash, or a digest over only the agreed table rejects.

### 4.3 Unique public publication receipt

The public record publisher must copy the E53 decision record byte-for-byte into `public-decision-store`. Its unsigned publication-receipt `record_bytes` are exactly:

```text
publication_schema=URC-0.12-PUBLICATION-1\n
publisher_role=public-record-publisher\n
source_edge=E53\n
source_record_sha256=<E53 decision record SHA-256>\n
published_store=public-decision-store\n
published_record_sha256=<stored decision record SHA-256>\n
publication_result=byte-identical\n
monotonic_timestamp_ns=<decimal integer>\n
```

The two record hashes must be equal. The publisher signs the receipt with the section-4 envelope and E54 atomically stores the exact decision record plus signed receipt. E55 delivers both unchanged to the terminal public record reader. E56 delivers only SHA-256 of the exact signed receipt envelope to the registrar. Any changed record, unequal digest, invalid signature/key, partial write, or second publication stops and produces no E56.

## 5. Closed matrix-ledger bijection

### 5.1 Exact public grants and operational edges

E00A-H are eight signed public-specification grants. E01-E56 are exactly 56 authorized operational edge types. Edge IDs identify channels, while section 4 separately fixes status ordering.

| Edge | Producer | Artifact | Recipient/store | Required check |
|---|---|---|---|---|
| E00A | registrar | authoring protocol, constraints, selected N | fact author | exact reviewed public bytes/hashes |
| E00B | registrar | frozen contract and label specification | label A/B | byte-identical signed grant |
| E00C | registrar | transformation, runner-allowlist, scanner, and leakage-review specifications | representation builder, package builder/scanner 1, scanner 2, leakage reviewers as applicable | recipient-specific signed manifest |
| E00D | registrar | metadata, ID-order, semantic-atom, strength, cause, mutation, comparator, and catalog specifications | comparator builders, generators, P1 reviewers, comparator operators as applicable | exact reviewed public bytes/hashes |
| E00E | registrar | A-D identity, bank-hash, schedule, and P2-P4 map/formula specifications | condition-map custodian, blinded-map builders as applicable | exact reviewed public bytes/hashes |
| E00F | registrar | semantic-reason rubric | judges | byte-identical signed grant |
| E00G | registrar | common-resource, transport, anonymization, section-4 custody/signing/publication specifications, and public key registry | dispatcher, executor, raw custodian, comparison custodians, public readers, public record publisher as applicable | exact reviewed bytes; role-specific grant; no private keys |
| E00H | registrar | frozen statistical decision table and formula identity | analysis, final-decision custodian | no selected constants or results |
| E01 | registrar | frozen statistical/catalog specifications and pre-bank manifest | simulation builder | full signed public bytes, role grant, and hashes |
| E02 | simulation builder | benchmark/audit/power summary hashes | registrar | ceilings; no semantic content |
| E03 | simulation builder | selected calibrated constants and public formula manifest | `analysis-input-vault` | signed exact bytes before calls |
| E04 | fact author | frozen bank/prompts and signature | content-intake custodian, which atomically verifies and writes `content-vault` | selected N and content hash |
| E05 | `content-vault` | content digest only | registrar | no content bytes |
| E06 | `content-vault` | exact content copies | label A, label B, representation builder | recipient manifests |
| E07 | label A/B | signed bundles | `label-vault-A` and `label-vault-B`; label comparison is the only reader | separate ACLs |
| E08 | label comparison | equality digest | registrar | no label contents |
| E09 | label comparison | agreed bundle | `agreed-label-vault` | exact equality only |
| E10 | `agreed-label-vault` | agreed bundle | generators | phase grant after equality |
| E11 | `agreed-label-vault` | agreed bundle | leakage reviewers | package-review phase grant |
| E12 | `agreed-label-vault` | agreed bundle | judges, comparator operators | adjudication phase grant |
| E13 | representation builder | representations/equality manifest | `representation-vault`; package builder and condition-map custodian are readers | canonical equality |
| E14 | representation builder | equality digest | registrar | no representation content |
| E15 | `representation-vault` | assigned representation/questions | package builder | signed assignment |
| E16 | package builder | completed signed packages | `signed-package-vault` | package/hash manifest |
| E17 | package builder/scanner 1 | scan-1 table | `scan-vault-1` | scanner-1 signature |
| E18 | `signed-package-vault` | completed package | scanner 2 | no scan-1 access |
| E19 | scanner 2 | scan-2 table | `scan-vault-2` | scanner-2 signature |
| E20 | `scan-vault-1` and `scan-vault-2` | both scan tables | scan comparison | exact inventory/scan comparison |
| E21 | scan comparison | pass/reject digest | registrar | exact agreement |
| E22 | `signed-package-vault` | signed package | leakage reviewers | separate from label grant E11 |
| E23 | leakage reviewers | signed tables | `leakage-vault-1` and `leakage-vault-2`; leakage comparison is the only reader | separate ACLs |
| E24 | leakage comparison | pass/reject digest | registrar | exact agreement |
| E25 | comparator builders | implementation/mutation tables | `comparator-vault-1` and `comparator-vault-2`; registrar gets the two fixed-role hashes only | separate internals; both expected role hashes present |
| E26 | generators | abstract tables | `generator-vault-1` and `generator-vault-2`; catalog comparison is the only reader | frozen generator/spec hashes |
| E27 | catalog comparison | agreed abstract table and rejection summary | `catalog-vault`; P1 reviewers are readers and registrar gets digest only | byte equality |
| E28 | generators | bank-instance tables | `generator-vault-1` and `generator-vault-2`; catalog comparison is the only reader | agreed labels via E10 only |
| E29 | catalog comparison | agreed instance table and rejection summary | `catalog-vault`; P1 reviewers and comparator operators are readers | byte equality |
| E30 | P1 reviewers | signed reviews | `p1-review-vault-1` and `p1-review-vault-2`; P1-review comparison is the only reader | separate ACLs |
| E31 | P1-review comparison | pass/reject digest | registrar | exact agreement |
| E32 | `signed-package-vault` | finalized packages/hashes | condition-map custodian | scan/leakage-passed hashes only |
| E33 | condition-map custodian | semantic condition/schedule map | `condition-map-vault`; blinded-map builders are pre-call readers | pre-call freeze and separate grants |
| E34 | blinded-map builders | blinded maps | analysis-map comparison | independent builds |
| E35 | analysis-map comparison | agreed blinded map | `analysis-map-vault`; registrar gets digest only | byte equality |
| E36 | condition-map custodian | opaque schedule/routing plus assigned signed package | dispatcher; routing copy to raw custodian | balance and package-hash match |
| E37 | dispatcher | signed request/package | executor | pre-send timestamp |
| E38 | executor | first raw response stream | dispatcher | no retry/read-back |
| E39 | dispatcher | raw response plus run log/endpoints | `raw-output-vault` | durable-final-byte timestamp/hash |
| E40 | raw custodian | anonymous semantic bundle | judges, comparator operators | identity stripping/raw link |
| E41 | raw custodian | anonymous timing/byte table | analysis | no semantic names |
| E42 | judges | signed judgments | `judgment-vault-1` and `judgment-vault-2`; judgment comparison is the only reader | separate ACLs |
| E43 | judgment comparison | signed canonical comparison envelope, comparison digest, and agreed semantic table | comparator operators | exact section-4.2 bytes, digest, Ed25519 signature, and table hash |
| E44 | comparator operators | derived tables | adjudication comparison | independent implementations |
| E45 | adjudication comparison | signed canonical comparison envelope, comparison digest, and agreed derived table | analysis | exact section-4.2 bytes, digest, Ed25519 signature, and table hash |
| E46 | `analysis-input-vault` | constants and public formula manifest | analysis | exact pre-call hashes |
| E47 | `analysis-map-vault` | blinded coefficient/stratum map | analysis | exact map hash |
| E48 | analysis | frozen statistics/decision inputs/hash | registrar and final-decision custodian | semantic map withheld |
| E49 | `condition-map-vault` | semantic condition map | final-decision custodian | only after authenticated E48 hash |
| E50 | final-decision custodian | exact mechanical join/decision record | `final-decision-vault`; registrar gets decision-record digest only | no reanalysis or threshold change; atomic store write |
| E51 | registrar | next signed canonical status envelope | `registrar-store` | exact section-4.1 transition, digest, key, signature, and timestamp order |
| E52 | `registrar-store` | exact signed status-envelope chain | public status reader | read-only delivery; every section-4.1 invariant verifies |
| E53 | `final-decision-vault` | exact decision record and digest | public record publisher | E50 store digest and bytes match; no other vault access |
| E54 | public record publisher | byte-identical decision record and signed canonical publication receipt | `public-decision-store` | exact section-4.3 atomic write, equality, key, and signature |
| E55 | `public-decision-store` | exact decision record and signed publication receipt | public record reader | hashes, equality, publisher key, and signature verify |
| E56 | `public-decision-store` | signed publication-receipt envelope digest only | registrar | no decision-record bytes; digest matches E54 receipt envelope |

### 5.2 Role-to-edge index

Every cross-role positive matrix input and every only-output/store maps to these exact edges. Store-mediated reads and writes use the literal section-3 IDs. The registrar's reviewed public roots are the sole pre-run root inputs and are not experimental cross-role transfers.

| Role | Inbound edges | Outbound edges |
|---|---|---|
| registrar | reviewed public roots; E02,E05,E08,E14,E21,E24,E25,E27,E29,E31,E35,E48,E50,E56 | E00A-E00H,E01,E51 |
| public status reader | E00G,E52 | none |
| public record publisher | E00G,E53 | E54 |
| public record reader | E00G,E55 | none |
| content intake | E04 | E04,E05,E06 |
| simulation builder | E01 | E02,E03,E46 |
| fact author | E00A | E04 |
| label A/B | E00B,E06 | E07 |
| label comparison | E07 | E08-E12 |
| representation builder | E00C,E06 | E13-E15 |
| package builder/scanner 1 | E00C,E15 | E16-E18,E20,E22,E32 |
| scanner 2 | E00C,E18 | E19,E20 |
| scan comparison | E20 | E21 |
| leakage reviewers | E00C,E11,E22 | E23 |
| leakage comparison | E23 | E24 |
| comparator builders | E00D | E25 |
| generators | E00D,E10 | E26,E28 |
| catalog comparison | E26,E28 | E27,E29 |
| P1 reviewers | E00D,E27,E29 | E30 |
| P1-review comparison | E30 | E31 |
| condition-map custodian | E00E,E13,E32 | E33,E36,E49 |
| blinded-map builders | E00E,E33 | E34 |
| analysis-map comparison | E34 | E35,E47 |
| dispatcher | E00G,E36,E38 | E37,E39 |
| executor | E00G,E37 | E38 |
| raw custodian | E00G,E36,E39 | E40,E41 |
| judges | E00F,E12,E40 | E42 |
| judgment comparison | E00G,E42 | E43 |
| comparator operators | E00D,E12,E25,E29,E40,E43 | E44 |
| adjudication comparison | E00G,E44 | E45 |
| analysis | E00H,E41,E45,E46,E47 | E48 |
| final-decision custodian | E00H,E48,E49 | E50 |

E51 is the only registrar-store write and E52 its only read. E53-E56 are the only public-decision publication path. E43 and E45 use the one comparison grammar and fixed left/right roles. No declared output may be dropped, ambiently copied, reformatted, or reconstructed by an unlisted recipient.

## 6. Replacement P0 and P1 requirements

P0 retains every authenticated pass and additionally requires exact agreement on:

- the 31-slot contract and 25-slot plan constructions and both effective hashes;
- one-field-once record grammars, heading digests, slot-10 source inventory, and the two exact one-occurrence transforms;
- the byte-identical U11 semantic slice and all semantic-atom, strength, direct-permission, cause, selector, consumption, and P3 consequences;
- global `id_order_key` ordering inside every record-ID array and complete outer `cause_ref` order;
- all C4 branches, cause/catalog bounds, availability rows, abstract rows, and bank-instance projection;
- exact N/24 bank balance, development-example exclusion, and zero duplicate keys;
- eight E00 grants, 56 E01-E56 edge types, 26 literal store IDs, and every role/index cell;
- the status enum, bit/edge table, 15-record maximum chain, exact record/envelope grammar, key IDs, signatures, prefix masks, and timestamps;
- the fixed-role E43/E45 record bytes, hashes, signatures, and agreed-table hashes; and
- the E53-E56 publisher, public store, reader, receipt, and registrar-digest path.

P1 mutations include every inherited semantic and ordering case plus missing/duplicate/reordered status edges, non-prefix masks, wrong status strings, bad genesis/previous hash/sequence/time, alternate field order/whitespace/length/hash/key/role/signature, E43/E45 left-right swaps and concatenation variants, agreed-table hash changes, unauthorized publisher reads, decision-byte changes, partial/double publication, receipt changes, missing E56, every store read/write route, and the frozen bank-instance projection. Two independent expected generators, two P1 reviewers, and both comparators must agree exactly. Agreement between identically wrong implementations is failure.

## 7. Equality, stopping, rollback, and claim limit

Inherited A-D equality and noncompensatory P0-P4 stops remain. Additional stops are an incomplete effective map, effective-hash difference, transform-count mismatch, duplicate record field, noncanonical heading digest, semantic regression, noncanonical ID/cause order, incorrect catalog count, unbalanced row, development-example reuse, duplicate key, unmatched role/edge/store/reader, invalid status transition or envelope, alternate digest/signature preimage, invalid key assignment, E43/E45 record mismatch, unauthorized publication access, changed public decision bytes, invalid publication receipt, missing E56, premature semantic-map release, or post-map reanalysis.

Failure preserves authenticated evidence, forbids reuse of an exposed bank, and opens no later gate.

Even a future complete pass would support only:

> Under the frozen synthetic public bank, exact model revision, observer prompts, representations, 24-code control, audited dependence grids, balanced and duplicate-controlled bank, complete semantic contract, bounded catalogs, canonical custody/signature records, closed public publication path, resource ceilings, and frozen algorithms, URC-0.12 did not cross the precommitted public rejection thresholds.

It would not establish validity outside that bounded experiment, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only next action authorized by this redesign is fresh public-only independent review under a separate exact gate.
