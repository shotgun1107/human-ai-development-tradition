# URC-0.11 public falsification plan v0.8

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.11 REDESIGN OPEN`
- companion: `universal-response-contract-v0.11-candidate.md`
- predecessor evidence: authenticated plans v0.4-v0.7 and v0.10 independent review v0.1
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
| `P8` | this `public-falsification-plan-v0.8.md` | its matching same-basename sidecar after this file freezes |

P6's failed effective-plan construction remains evidence only. Exact authenticated slices named below remain usable byte sources.

### 1.2 Total transitive section map

Every v0.10 effective-plan slot is retained or replaced exactly once.

| Effective slot | Effective v0.10 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `P8` section 1, heading `## 1. Complete effective-plan construction` |
| 2 | slot 2 | retain | full `P4` section 2, heading `## 2. Facts, inferences, and proposals` |
| 3 | slot 3 | retain | full `P5` section 2, heading `## 2. Role isolation rules` |
| 4 | slot 4 | replace | full `P8` section 2, heading `## 2. Corrected complete role matrix` |
| 5 | slot 5 | replace | full `P8` sections 3-4, from `## 3. Exact named store identities` through `## 4. Closed matrix-ledger bijection` |
| 6 | slot 6 | retain | full `P5` section 5, heading `## 5. Blinded analysis-design map` |
| 7 | slot 7 | retain | full `P7` section 5, heading `## 5. Restored bank balance and freeze sequence` |
| 8 | slot 8 | replace | full `P8` section 5, heading `## 5. Replacement P0 and P1 requirements` |
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
| 25 | slot 25 | replace | full `P8` section 6, heading `## 6. Equality, stopping, rollback, and claim limit` |

No P4-P7 effective range is unspecified. P7 sections 1-4, 6, and 7 are replaced; its authenticated section 5 remains exact.

### 1.3 One complete plan-record grammar

Use only companion candidate section 3.3 steps 1-7 for source authentication, heading resolution, slicing, and heading-digest computation. Do not emit the companion contract record. For plan records, emit this complete grammar once:

```text
slot=<decimal slot>\n
source=<P4|P5|P6|P7|P8>\n
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
transform_1_to_hex=76302e3131
transform_1_required_occurrences=1
transform_2_from_hex=5552432d302e38
transform_2_to_hex=5552432d302e3131
transform_2_required_occurrences=1
```

The hex pairs mean exact ASCII `v0.8` to `v0.11` and `URC-0.8` to `URC-0.11`. Apply blocks sequentially to the authenticated raw P5 section 8 slice. Before each replacement, its exact source byte sequence must occur once and only once; otherwise construction rejects. Replacement is global for that one occurrence, with no normalization or case folding. Neither replacement changes a formula, seed field, threshold, or allowed seed use.

The effective stream is ASCII `URC-0.11-PLAN-EFFECTIVE\n` followed by the 25 records with no separator beyond the grammar bytes. `effective_plan_sha256` is SHA-256 of that stream and freezes only in a later reviewed manifest after the P8 sidecar exists.

## 2. Corrected complete role matrix

The inherited isolation rules remain. Omission is denial; worktrees isolate edits only; paired independent roles are distinct fresh roots; conversation text and ambient repository access are not transfer channels. “Public specification” means only independently reviewed public bytes and never bank content, labels, outputs, condition maps, or sealed material.

| Role | Positive inputs | Explicit denylist | Only output / store |
|---|---|---|---|
| CONTROL registrar | authenticated reviewed public specification bytes/hashes, role/store assignment matrix, artifact/pass/reject digests, anonymous analysis hash | bank/prompt contents, labels, raw/anonymous semantic outputs, condition map, executor reasoning, sealed material | recipient-specific signed public-specification grants E00A-H/E01 and signed append-only status manifests in `registrar-store` |
| public status reader | signed status manifests delivered from `registrar-store` by E52 | every bank/prompt byte, label, output, condition map, comparator/judge internals, sealed material | none; terminal read-only role |
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
| judgment-comparison custodian | two judgment tables | condition map, timing, raw package identity | equality digest and agreed semantic table, both delivered by E43 |
| comparator operator 1 / 2 | assigned comparator, agreed labels/expected table, anonymous output, agreed semantic table and judgment equality digest | condition map, timing, other comparator internals | anonymous atom/event/total and P1 comparison tables |
| adjudication-comparison custodian | both comparator tables | raw prose, condition map, timing | equality digest and agreed derived table, both delivered by E45 |
| analysis role | agreed derived table and adjudication equality digest, timing table, selected calibrated constants, public formula manifest, opaque IDs, agreed blinded map, frozen statistical decision table | raw prose, executor reasoning, semantic condition map | frozen anonymous P2-P4 statistics/decision inputs/hash |
| final-decision custodian | frozen anonymous analysis, post-hash semantic map, frozen decision table | raw output, reanalysis, threshold changes | mechanical join and public decision record in `final-decision-vault` |

## 3. Exact named store identities

Each row names a literal global store ID, one writer, and all readers.

| Store ID | Only writer | Authorized readers |
|---|---|---|
| `registrar-store` | CONTROL registrar through E51 only | public status reader through E52 only |
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
| `final-decision-vault` | final-decision custodian | public record publisher; registrar by digest only |

No synonym, unlisted mirror, conversation copy, or ambient directory is an authorized store.

## 4. Closed matrix-ledger bijection

### 4.1 Exact public grants and operational edge types

E00A-H are eight signed public-specification grants. E01-E52 are exactly 52 authorized operational edge types. Edge IDs identify channels, not chronological steps. E51 may carry repeated append-only status records, one per authenticated status transition; every record contains the triggering evidence digest, prior status-record digest or the all-zero genesis digest, new status, signature, and monotonic timestamp.

| Edge | Producer | Artifact | Recipient/store | Required check |
|---|---|---|---|---|
| E00A | registrar | authoring protocol, constraints, selected N | fact author | exact reviewed public bytes/hashes |
| E00B | registrar | frozen contract and label specification | label A/B | byte-identical signed grant |
| E00C | registrar | transformation, runner-allowlist, scanner, and leakage-review specifications | representation builder, package builder/scanner 1, scanner 2, leakage reviewers as applicable | recipient-specific signed manifest |
| E00D | registrar | metadata, ID-order, semantic-atom, strength, cause, mutation, comparator, and catalog specifications | comparator builders, generators, P1 reviewers, comparator operators as applicable | exact reviewed public bytes/hashes |
| E00E | registrar | A-D identity, bank-hash, schedule, and P2-P4 map/formula specifications | condition-map custodian, blinded-map builders as applicable | exact reviewed public bytes/hashes |
| E00F | registrar | semantic-reason rubric | judges | byte-identical signed grant |
| E00G | registrar | common-resource, transport, and anonymization specifications | dispatcher, executor, raw custodian as applicable | exact reviewed public bytes/hashes |
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
| E25 | comparator builders | implementation/mutation tables | `comparator-vault-1` and `comparator-vault-2`; registrar gets hashes only | separate internals |
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
| E43 | judgment comparison | equality digest and agreed semantic table | comparator operators | digest covers both signed inputs and agreed table; exact equality |
| E44 | comparator operators | derived tables | adjudication comparison | independent implementations |
| E45 | adjudication comparison | equality digest and agreed derived table | analysis | digest covers both signed inputs and agreed table; byte equality |
| E46 | `analysis-input-vault` | constants and public formula manifest | analysis | exact pre-call hashes |
| E47 | `analysis-map-vault` | blinded coefficient/stratum map | analysis | exact map hash |
| E48 | analysis | frozen statistics/decision inputs/hash | registrar and final-decision custodian | semantic map withheld |
| E49 | `condition-map-vault` | semantic condition map | final-decision custodian | only after authenticated E48 hash |
| E50 | final-decision custodian | mechanical join/decision record | `final-decision-vault`; public gets record and registrar gets digest only | no reanalysis or threshold change |
| E51 | registrar | signed append-only status record | `registrar-store` | triggering inbound digest authenticated; prior-record digest chain, signature, and monotonic timestamp valid |
| E52 | `registrar-store` | exact signed status record and digest chain | public status reader | read-only delivery; signature, chain, and requested digest match; no experimental bytes |

### 4.2 Role-to-edge index

Every cross-role positive matrix input and every only-output/store maps to these exact edges. Store-mediated reads and writes use the literal section-3 IDs. The registrar's reviewed public roots are the sole pre-run root inputs and are not experimental cross-role transfers.

| Role | Inbound edges | Outbound edges |
|---|---|---|
| registrar | reviewed public roots; E02,E05,E08,E14,E21,E24,E25,E27,E29,E31,E35,E48,E50 | E00A-E00H,E01,E51 |
| public status reader | E52 | none |
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
| judgment comparison | E42 | E43 |
| comparator operators | E00D,E12,E25,E29,E40,E43 | E44 |
| adjudication comparison | E44 | E45 |
| analysis | E00H,E41,E45,E46,E47 | E48 |
| final-decision custodian | E00H,E48,E49 | E50 |

E51 is the only registrar-store write and E52 is its only read. E43 routes both the judgment equality digest and agreed semantic table. E45 routes both the adjudication equality digest and agreed derived table. No declared output may be dropped, ambiently copied, or reconstructed by an unlisted recipient.

## 5. Replacement P0 and P1 requirements

P0 retains every authenticated pass and additionally requires exact agreement on:

- the 31-slot contract and 25-slot plan constructions and both effective hashes;
- one-field-once record grammars, heading digests, slot-10 source inventory, and the two exact one-occurrence transforms;
- every semantic atom, its exact availability dependency and T/F/U result, the three-level operational-strength table, `stronger`, `permits_direct`, cause mapping, selectors, consumption, and P3 Y consequence;
- global `id_order_key` ordering inside every record-ID array and complete outer `cause_ref` order;
- all C4 dependent/target/direct positive and negative branches;
- maxima 20 metadata, four invalid-citation, four extra-affected, and 28 total causes;
- the exact availability bit order and 1,792 rows;
- 921,600 abstract, 407 cause-key, and maximum bank-instance counts;
- exactly `N/24` questions in each row, development-example exclusion, and zero duplicate keys;
- eight E00 public grants, 52 E01-E52 operational edge types, every literal store ID, and the role-to-edge table; and
- E51/E52 registrar-store custody plus delivery of both comparison digests in E43/E45.

P1 mutations include every semantic-atom/strength/direct-permission case listed by the companion, `R10`/`R2`, prefixes, quotes, backslashes, ASCII punctuation, presentation-order permutations, every 28 single and 378 pair cause row, all C4 branches/aliases/U cases, every availability mask, every abstract row, bank balance and duplicate rejections, all store read/write routes, status-chain genesis/append/signature/digest failures, missing or altered E43/E45 digests, and the frozen bank-instance projection. Two independent expected generators, two P1 reviewers, and both comparators must agree exactly. Agreement between identically wrong implementations is failure.

## 6. Equality, stopping, rollback, and claim limit

Inherited A-D equality and noncompensatory P0-P4 stops remain. Additional stops are an incomplete effective map, effective-hash difference, transform-count mismatch, duplicate record field, noncanonical heading digest, undefined or unequal semantic atom, noncanonical inner ID or outer cause order, ordinal cause ID, empty true-branch selector, unclassified C4 source, incorrect catalog count, unbalanced row, development-example reuse, duplicate key, unmatched edge/store/reader, broken registrar status chain, missing comparison digest, unauthorized registrar output, missing specification/package/constant/formula delivery, premature semantic-map release, or post-map reanalysis.

Failure preserves authenticated evidence, forbids reuse of an exposed bank, and opens no later gate.

Even a future complete pass would support only:

> Under the frozen synthetic public bank, exact model revision, observer prompts, representations, 24-code control, audited dependence grids, balanced and duplicate-controlled bank, complete semantic-atom contract, bounded catalogs, published custody bijection, resource ceilings, and frozen algorithms, URC-0.11 did not cross the precommitted public rejection thresholds.

It would not establish validity outside that bounded experiment, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only next action authorized by this redesign is fresh public-only independent review under a separate exact gate.
