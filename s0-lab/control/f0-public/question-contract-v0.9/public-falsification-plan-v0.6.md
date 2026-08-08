# URC-0.9 public falsification plan v0.6

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.9 REDESIGN OPEN`
- predecessor: `public-falsification-plan-v0.5.md`
- predecessor SHA-256: `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f`
- companion: `universal-response-contract-v0.9-candidate.md`
- excluded: implementation, bank/fixture/oracle authoring, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Complete effective-plan construction

### 1.1 Authenticated source identities

The effective plan is a direct three-source composition. It does not treat plan v0.5 as a self-contained copy of text inherited from plan v0.4.

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `P4` | `question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| `P5` | `question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` |
| `P6` | this `public-falsification-plan-v0.6.md` | its matching same-basename sidecar after this file freezes |

### 1.2 Total transitive section map

Every v0.4 section/subsection is classified, and every v0.5 replacement section is inherited or replaced. A coverage cell joined with `/` records the transitive predecessor range; only the exact effective-source slice contributes bytes.

| Effective slot | Transitive predecessor coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | `P4` §1 / `P5` §1 | replace | `P6` §1, from `## 1. Complete effective-plan construction` through the same heading |
| 2 | `P4` §2 | inherit | exact `P4` §2, from `## 2. Facts, inferences, and proposals` through the same heading |
| 3 | `P4` §3 / `P5` §2 | inherit replacement | exact `P5` §2, from `## 2. Role isolation rules` through the same heading |
| 4 | `P4` §3 / `P5` §3 | replace replacement | `P6` §2, from `## 2. Corrected complete role matrix` through the same heading |
| 5 | `P4` §3 / `P5` §4 | replace replacement | `P6` §§3-4, from `## 3. Named store identities` through `## 4. Published matrix/ledger bijection` |
| 6 | `P4` §§4-6 / `P5` §5 | inherit replacement | exact `P5` §5, from `## 5. Blinded analysis-design map` through the same heading |
| 7 | `P4` §§4-6 / `P5` §6 | replace replacement | `P6` §5, from `## 5. Corrected freeze sequence and catalog resources` through the same heading |
| 8 | `P4` §§4-6 / `P5` §7 | replace replacement | `P6` §6, from `## 6. Replacement P0 and P1 requirements` through the same heading |
| 9 | `P4` §7 | inherit | exact `P4` §7, from `## 7. P2 — no-record leakage and neutral-token equivalence` through the same heading |
| 10 | `P4` §8 / `P5` §8 | inherit replacement with fixed transform | exact `P5` §8, from `## 8. Prospective and confirmatory seeds` through the same heading |
| 11 | `P4` §9 | inherit | exact `P4` §9, from `## 9. P3 — representation-alignment equivalence` through the same heading |
| 12 | `P4` §10 parent heading/preamble | inherit | exact `P4` §10 preamble, from `## 10. Deterministic N and guaranteed-balanced schedule` to immediately before `### 10.1 Smallest sufficient N` |
| 13 | `P4` §10.1 | inherit | exact `P4` §10.1, from `### 10.1 Smallest sufficient N` through the same heading |
| 14 | `P4` §10.2 | inherit | exact `P4` §10.2, from `### 10.2 P2 schedule` through the same heading |
| 15 | `P4` §10.3 | inherit | exact `P4` §10.3, from `### 10.3 P3 schedule construction and proof` through the same heading |
| 16 | `P4` §10.4 / `P5` §9 | inherit replacement | exact `P5` §9, from `## 9. Revision, transport, and elapsed custody` through the same heading |
| 17 | `P4` §11 parent heading/preamble | inherit | exact `P4` §11 preamble, from `## 11. Feasibility and ceilings` to immediately before `### 11.1 Simulation benchmark` |
| 18 | `P4` §11.1 | inherit | exact `P4` §11.1, from `### 11.1 Simulation benchmark` through the same heading |
| 19 | `P4` §11.2 | inherit | exact `P4` §11.2, from `### 11.2 Confirmatory ceilings at N=720` through the same heading |
| 20 | `P4` §11.3 / `P5` §10 | replace replacement | `P6` §7, from `## 7. Revised human and resource ledger` through the same heading |
| 21 | `P4` §12 parent heading/preamble | inherit | exact `P4` §12 preamble, from `## 12. P4 — comparator reliability and burden` to immediately before `### 12.1 Output consequences` |
| 22 | `P4` §12.1 | inherit | exact `P4` §12.1, from `### 12.1 Output consequences` through the same heading |
| 23 | `P4` §12.2 / `P5` §11 | inherit replacement | exact `P5` §11, from `## 11. Comparator reliability replacement` through the same heading |
| 24 | `P4` §12.3 | inherit | exact `P4` §12.3, from `### 12.3 Exact burden metrics` through the same heading |
| 25 | `P4` §13 / `P5` §12 | replace replacement | `P6` §8, from `## 8. Equality, stopping, rollback, and claim limit` through the same heading |

No v0.4 or v0.5 normative range is unspecified. Replaced composition prose contributes no bytes except the new `P6` §1 construction record.

### 1.3 Effective plan hash

Use the section-slicing and record algorithm in companion candidate §3.3 with source IDs `P4|P5|P6`, this file's sidecar as the `P6` source SHA, the 25 rows above as ordered slots, and ASCII prefix `URC-0.9-PLAN-EFFECTIVE\n`. Insert ASCII lines `slice_mode=<full|preamble>\n` and `transform=<value>\n` immediately before the `length` line in every record. Slots 12, 17, and 21 use `preamble`; all others use `full`. A preamble slice starts at the named level-2 heading and ends immediately before its named first level-3 child heading. It includes the parent heading bytes and any intervening bytes. A missing, duplicate, reordered, or additional earlier level-3 heading rejects construction.

The transform value is `none` except slot 10, where it is `replace-all:URC-0.8->URC-0.9:count=2`.

Authenticate and slice before transforming. In slot 10, require exactly two nonoverlapping ASCII occurrences of `URC-0.8`, replace both byte-for-byte with `URC-0.9`, and hash the transformed content bytes and their transformed byte length. Any other occurrence count rejects construction. No formula, seed field, threshold, or allowed seed use changes.

## 2. Corrected complete role matrix

The inherited general isolation rules remain. Omission is denial; worktrees are edit isolation only; paired independent roles are distinct fresh roots; conversation text is not a transfer channel.

| Role | Positive inputs | Explicit denylist | Only output / store |
|---|---|---|---|
| CONTROL registrar | reviewed design hashes, role/store attestations, artifact/pass/reject digests, anonymous analysis hash | bank/prompt contents, labels, raw/anonymous semantic outputs, condition map, executor reasoning, sealed material | signed status manifests in `registrar-store` |
| content-intake custodian | frozen author bank/prompts and signature | labels, outputs, condition map, sealed material | immutable content and exact copies in `content-vault` |
| simulation builder/operator | frozen statistics/catalog specifications and pre-bank manifest | bank facts, prompts, labels, confirmatory output, condition map | implementation/benchmark/calibration/power summaries; selected constants and public formula manifest to `analysis-input-vault` |
| public fact author | frozen authoring protocol, constraints, selected N | labels, representations, outputs, sealed/real material | frozen bank/prompts to content intake |
| label author A / B | exact content copy and frozen contract | other label, representations, outputs, condition map | separate signed bundles in `label-vault-A` and `label-vault-B` respectively |
| label-comparison custodian | signed A/B bundles | representations, packages, outputs, condition map | equality digest; agreed bundle only in `agreed-label-vault` |
| representation builder | exact content copy and transformation specification | labels, expected values, outputs | representations/equality manifest in `representation-vault` |
| package builder / scanner 1 | assigned representation, questions, runner allowlist, scanner specification | labels, expected answers, outputs, sealed material | signed package to `signed-package-vault`; scan-1 table to `scan-vault-1` |
| scanner 2 | completed signed package and scanner specification | scan-1 table/internals, labels, outputs | scan-2 table to `scan-vault-2` |
| scan-comparison custodian | scan-1/scan-2 tables | package prose, labels, outputs, condition map | equality/pass or reject digest |
| leakage reviewer 1 / 2 | signed package and agreed labels | executor output, condition map/narrative, other reviewer, sealed material | separate signed tables in `leakage-vault-1` and `leakage-vault-2` respectively |
| leakage-comparison custodian | two leakage tables | package prose beyond hash, outputs, condition map | equality/pass or reject digest |
| comparator builder 1 / 2 | frozen metadata, cause/evaluation/consumption, canonicalization, mutation specifications | other comparator internals, confirmatory output, condition map | implementation/mutation table in `comparator-vault-1` and `comparator-vault-2` respectively |
| expected-catalog generator 1 / 2 | frozen catalog specifications and later agreed labels | comparator output/internals, confirmatory output, condition map | abstract and bank-instance tables in `generator-vault-1` and `generator-vault-2` respectively |
| catalog-comparison custodian | both generator tables | comparator/confirmatory output, condition map | agreed tables/digests in `catalog-vault` |
| P1 reviewer 1 / 2 | frozen specifications, agreed tables, rejection summaries | comparator/confirmatory output, condition map, other review | signed catalog reviews in `p1-review-vault-1` and `p1-review-vault-2` respectively |
| P1-review comparison custodian | two P1 reviews | bank prose beyond hashed IDs, outputs, condition map | agreement/pass or reject digest |
| condition-map/schedule custodian | finalized signed packages, A-D identities, bank hash, schedule rules, opaque run IDs | labels, expected answers, raw output, judgments | encrypted semantic map in `condition-map-vault`; opaque schedule/routing; assigned signed package to dispatcher |
| blinded-map builder 1 / 2 | frozen P2-P4 formulas, semantic condition/schedule map, opaque namespace | labels, expected answers, output, other builder | separate blinded coefficient/stratum maps |
| analysis-map comparison custodian | two blinded maps | labels, outputs, semantic names after comparison | agreed blinded map in `analysis-map-vault` |
| dispatcher/transport recorder | opaque schedule/routing and one assigned signed package | labels, expected answers, semantic map, prior outputs | request, signed run log, monotonic endpoints, first raw response to `raw-output-vault` |
| public executor | one signed package, common resources, opaque run ID | labels, mappings, comparators, mutations, other packages/outputs, forbidden tools/network | first raw response stream only |
| raw-output custodian/anonymizer | raw vault, routing map, run logs, anonymization rules | labels, expected answers, semantic condition map, comparator logic | raw hashes, anonymous semantic bundle, anonymous timing/byte table |
| semantic judge 1 / 2 | agreed labels, anonymous parseable output, reason rubric | condition map, timing/cost/load, other judge, sealed material | separate signed anonymous judgments in `judgment-vault-1` and `judgment-vault-2` respectively |
| judgment-comparison custodian | two judgment tables | condition map, timing, raw package identity | equality digest and agreed semantic table |
| comparator operator 1 / 2 | assigned comparator, agreed labels/expected table, anonymous output, agreed semantic table | condition map, timing, other comparator internals | anonymous atom/event/total and P1 comparison tables |
| adjudication-comparison custodian | both comparator tables | raw prose, condition map, timing | equality digest and agreed derived table |
| analysis role | agreed derived/timing tables, selected calibrated constants, public formula manifest, opaque IDs, agreed blinded map, frozen statistical decision table | raw prose, executor reasoning, semantic condition map | frozen anonymous P2-P4 statistics/decision inputs/hash |
| final-decision custodian | frozen anonymous analysis, post-hash semantic map, frozen decision table | raw output, reanalysis, threshold changes | mechanical join and public decision record in `final-decision-vault` |

## 3. Named store identities

Names below are exact global IDs. A synonym is forbidden.

| Store ID | Only writer | Authorized readers |
|---|---|---|
| `registrar-store` | CONTROL registrar | public status reader by signed digest |
| `content-vault` | content-intake custodian | label A/B, representation builder |
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
| `condition-map-vault` | condition-map custodian | final-decision custodian only after analysis hash |
| `analysis-map-vault` | analysis-map comparison custodian | analysis role |
| `raw-output-vault` | dispatcher/transport recorder | raw-output custodian |
| `judgment-vault-1` | semantic judge 1 | judgment-comparison custodian |
| `judgment-vault-2` | semantic judge 2 | judgment-comparison custodian |
| `final-decision-vault` | final-decision custodian | public record publisher; registrar by digest only |

The former names `adjudication-label vault` and bare `agreed-label vault` are invalid. Only `agreed-label-vault` exists.

## 4. Published matrix/ledger bijection

### 4.1 Complete transfer edges

| Edge | Producer | Artifact | Recipient/store | Required check |
|---|---|---|---|---|
| E00A | registrar | authoring protocol, constraints, selected N grant | fact author | reviewed public hashes |
| E00B | registrar | frozen contract/label specification | label A/B | byte-identical public grant |
| E00C | registrar | runner allowlist, scanner and leakage-review specifications | package builder/scanner 1, scanner 2, leakage reviewers | recipient-specific signed manifest |
| E00D | registrar | metadata, cause, mutation and catalog specifications | comparator builders, generators, P1 reviewers, comparator operators | exact reviewed hashes |
| E00E | registrar | A-D identity, bank-hash, schedule, and P2-P4 formula specifications | condition-map custodian, blinded-map builders | exact reviewed hashes |
| E00F | registrar | semantic-reason rubric | judges | byte-identical public grant |
| E00G | registrar | common resource, transport and anonymization manifests | dispatcher, executor, raw custodian | exact reviewed hashes |
| E00H | registrar | frozen statistical decision table/formula identity | analysis, final-decision custodian | no selected constants or results |
| E01 | registrar | reviewed hashes/pre-bank manifest | simulation builder | role grant and hash |
| E02 | simulation builder | benchmark/audit/power summary hashes | registrar | ceilings; no semantic content |
| E03 | simulation builder | selected calibrated constants and public formula manifest | `analysis-input-vault` | signed exact bytes before calls |
| E04 | fact author | frozen bank/prompts | content intake | signature and selected N |
| E05 | content intake | content digest | registrar | no content bytes |
| E06 | content intake | exact content copies | label A/B, representation builder | recipient manifests |
| E07 | label A/B | signed bundles | label comparison | separate ACLs |
| E08 | label comparison | equality digest | registrar | no label contents |
| E09 | label comparison | agreed bundle | `agreed-label-vault` | exact equality only |
| E10 | `agreed-label-vault` | agreed bundle | generators | phase grant after equality |
| E11 | `agreed-label-vault` | agreed bundle | leakage reviewers | package-review phase grant |
| E12 | `agreed-label-vault` | agreed bundle | judges, comparator operators | adjudication phase grant |
| E13 | representation builder | representations/equality manifest | `representation-vault` | canonical equality |
| E14 | representation builder | equality digest | registrar | no representation content |
| E15 | `representation-vault` | assigned representation/questions | package builder | signed assignment |
| E16 | package builder | completed signed packages | `signed-package-vault` | package/hash manifest |
| E17 | package builder/scanner 1 | scan-1 table | `scan-vault-1` | scanner-1 signature |
| E18 | `signed-package-vault` | completed package | scanner 2 | no scan-1 access |
| E19 | scanner 2 | scan-2 table | `scan-vault-2` | scanner-2 signature |
| E20 | `scan-vault-1` and `scan-vault-2` | both scan tables | scan comparison | exact inventory/scan comparison |
| E21 | scan comparison | pass/reject digest | registrar | exact agreement |
| E22 | `signed-package-vault` | signed package | leakage reviewers | package grant separate from label grant E11 |
| E23 | leakage reviewers | signed tables | leakage comparison | separate ACLs |
| E24 | leakage comparison | pass/reject digest | registrar | exact agreement |
| E25 | comparator builders | implementation/mutation tables | `comparator-vault-1` and `comparator-vault-2`; registrar gets hashes | separate internals |
| E26 | generators | abstract tables | `generator-vault-1` and `generator-vault-2`; catalog comparison is the only reader | frozen generator/spec hashes |
| E27 | catalog comparison | agreed abstract table and rejection summary | `catalog-vault` and P1 reviewers | byte equality |
| E28 | generators | bank-instance tables | `generator-vault-1` and `generator-vault-2`; catalog comparison is the only reader | agreed labels via E10 only |
| E29 | catalog comparison | agreed instance table and rejection summary | `catalog-vault`, P1 reviewers, comparator operators | byte equality |
| E30 | P1 reviewers | signed reviews | `p1-review-vault-1` and `p1-review-vault-2`; P1-review comparison is the only reader | separate ACLs |
| E31 | P1-review comparison | pass/reject digest | registrar | exact agreement |
| E32 | `signed-package-vault` | finalized packages/hashes | condition-map custodian | only scan/leakage-passed hashes |
| E33 | condition-map custodian | semantic condition/schedule map | blinded-map builders | pre-call freeze; separate grants |
| E34 | blinded-map builders | blinded maps | analysis-map comparison | independent builds |
| E35 | analysis-map comparison | agreed blinded map | `analysis-map-vault`; registrar gets digest | byte equality |
| E36 | condition-map custodian | opaque schedule/routing plus assigned signed package | dispatcher; routing copy to raw custodian | balance and package-hash match |
| E37 | dispatcher | signed request/package | executor | pre-send timestamp |
| E38 | executor | first raw response stream | dispatcher | no retry/read-back |
| E39 | dispatcher | raw response plus run log/endpoints | `raw-output-vault` | durable-final-byte timestamp/hash |
| E40 | raw custodian | anonymous semantic bundle | judges, comparator operators | identity stripping/raw link |
| E41 | raw custodian | anonymous timing/byte table | analysis | no semantic names |
| E42 | judges | signed judgments | `judgment-vault-1` and `judgment-vault-2`; judgment comparison is the only reader | separate ACLs |
| E43 | judgment comparison | agreed semantic table | comparator operators | exact equality |
| E44 | comparator operators | derived tables | adjudication comparison | independent implementations |
| E45 | adjudication comparison | agreed derived table | analysis | byte equality |
| E46 | `analysis-input-vault` | constants and public formula manifest | analysis | exact pre-call hashes |
| E47 | `analysis-map-vault` | blinded coefficient/stratum map | analysis | exact map hash |
| E48 | analysis | frozen statistics/decision inputs/hash | registrar and final-decision custodian | semantic map withheld |
| E49 | condition-map custodian | semantic condition map | final-decision custodian | only after authenticated E48 hash |
| E50 | final-decision custodian | mechanical join/decision record | `final-decision-vault`; public reader gets record and registrar gets digest | no reanalysis or threshold change |

### 4.2 Role-to-edge bijection index

Every matrix input/output appears here. Every ledger edge appears under the responsible producer and recipient roles. For a store-mediated edge, the section-3 only-writer owns the outbound responsibility and the stated authorized reader owns the inbound responsibility. Stores are exact nodes, not additional roles.

| Role | Inbound edges | Outbound edges |
|---|---|---|
| registrar | E02,E05,E08,E14,E21,E24,E25,E27,E29,E31,E35,E48,E50 | E00A-E00H,E01 |
| content intake | E04 | E05,E06 |
| simulation builder | E01 | E02,E03,E46 |
| fact author | E00A | E04 |
| label A/B | E00B,E06 | E07 |
| label comparison | E07 | E08-E12 |
| representation builder | E06 | E13-E15 |
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

No public specification, rubric, resource manifest, selected constant, package, label, map, output, signature, or decision table is available through ambient access. If a matrix input has no exact edge above, the bank version stops before the receiving role begins.

## 5. Corrected freeze sequence and catalog resources

The inherited candidate N sequence remains `240, 336, 432, 528, 624, 720`.

1. Obtain fresh independent review of the v0.9 package.
2. Freeze authoring/metadata specifications, 921,600-row abstract catalog, 1,792-row availability catalog, 407-row cause-key catalog, generators, statistics, roles, stores, ledger, ceilings, and N sequence.
3. Freeze the pre-bank power manifest and benchmark environment.
4. Benchmark simulation plus both generations/comparisons of all catalogs and the maximum 2,949,120-row bank-instance projection.
5. Stop if CPU, RAM, storage, calendar, human, signing, or monetary projections exceed inherited ceilings.
6. Fit/audit null boundaries, run power, and select the first sufficient N.
7. Author and independently label the untouched bank; reject on any difference.
8. Generate the instance projection once with frozen generators; compare and obtain both P1 signatures.
9. Freeze representations, packages, scanners, comparators, maps, schedules, constants, public formula manifest, exact model revision, and cost preflight.
10. Run P0-P2; run P3-P4 only after earlier passes.
11. Freeze judgments, derived tables, and anonymous analysis hash before semantic-map release and mechanical final join.

There is no quotienting of the 921,600 abstract tuples. Rejected rows occupy resources and remain in benchmark counts. No post-label generator or expected-value choice exists.

## 6. Replacement P0 and P1 requirements

P0 retains every authenticated pass and additionally requires exact agreement on:

- the 31-slot contract and 25-slot plan constructions and both effective hashes;
- canonical cause-key bytes with unsigned bytewise order and no ordinal IDs;
- all C4 dependent/target/direct positive and negative branches;
- maxima 20 metadata, four invalid-citation, four extra-affected, and 28 total causes;
- the exact availability bit order and 1,792 rows;
- 921,600 abstract, 407 cause-key, and maximum bank-instance counts;
- the named store identities, 50 transfer edges, and role-to-edge table; and
- delivery of assigned package, selected calibrated constants, public formula manifest, agreed labels, maps, timestamps, signatures, and decision record.

P1 mutations include every canonical-byte ordering boundary (`R10`/`R2`, prefix, escape, ASCII punctuation), every 28 single and 378 pair cause row, all C4 branches/aliases/U cases, all availability masks, every abstract row, and the frozen bank-instance projection. Two expected generators, two P1 reviewers, and both comparators must match the independent expected table. Agreement between identically wrong comparators is failure.

## 7. Revised human and resource ledger

| Task ledger | Maximum hours |
|---|---:|
| registrar, intake, schedule/map custody, final join, grants | 50 |
| synthetic fact authoring and cleanup | 40 |
| label A/B and deterministic comparison | 50 |
| contract/leakage/catalog review, judging, comparison | 45 |
| simulation/comparator/generator implementation, scans, analysis, incident reserve | 55 |
| **Aggregate** | **240** |

Every event belongs to one row and incompatible roles remain separate. The benchmark explicitly uses 921,600 abstract rows rather than the rejected 276,480 figure and includes the 1,792 availability, 407 cause-key, and maximum 2,949,120 instance rows twice for generation plus comparison, hashes, signatures, reviewer time, and storage. Exceeding 240 hours or any inherited CPU/RAM/storage/calendar/USD ceiling stops before authoring.

Inherited N=720 call/token arithmetic, visible ceilings, USD 500 compute, USD 3,000 total, 100 GiB confirmatory storage, 30-day end-to-end, seven-day confirmatory, per-call limits, and no-retry rules remain unchanged and unvalidated.

## 8. Equality, stopping, rollback, and claim limit

Inherited A-D equality and noncompensatory stops remain. Additional stops are an incomplete effective map, effective-hash difference, noncanonical cause bytes/order, ordinal cause ID, unclassified C4 source, incorrect catalog count, missing dynamic cause/availability axis, unmatched edge/store/reader, missing assigned package, missing constant/formula manifest, premature semantic-map release, or post-map reanalysis.

Failure preserves authenticated evidence, forbids reuse of an exposed bank, and opens no later gate.

Even a future complete pass would support only:

> Under the frozen synthetic public bank, exact model revision, observer prompts, representations, 24-code control, audited dependence grids, balanced schedule, corrected bounded catalogs, published custody bijection, resource ceilings, and frozen algorithms, URC-0.9 did not cross the precommitted public rejection thresholds.

It would not establish validity outside that bounded experiment, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer. The only next action authorized by this redesign is fresh public-only independent read-only review under a separate exact gate.
