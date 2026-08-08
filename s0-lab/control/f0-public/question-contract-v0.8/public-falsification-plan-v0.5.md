# URC-0.8 public falsification plan v0.5

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.8 REDESIGN OPEN`
- predecessor: `public-falsification-plan-v0.4.md`
- predecessor SHA-256: `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7`
- companion: `universal-response-contract-v0.8-candidate.md`
- excluded: implementation, bank/fixture/oracle authoring, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Normative composition and purpose

The effective v0.5 plan is the authenticated v0.4 plan at the predecessor hash above, composed with this document. V0.4 sections 2, 7, 9, 10.1-10.3, 11.1-11.2, and 12.1/12.3 are inherited without semantic change. This document replaces v0.4 sections 1, 3-6, 8, 10.4, 11.3, 12.2, and 13. Runtime and seed-domain token `URC-0.7` becomes `URC-0.8`; thresholds, formulas, grids, N candidates, schedules, and ceilings do not change.

P0-P4 remain noncompensatory. This plan only states how a future public experiment could be falsified. It does not open any implementation or execution gate.

## 2. Role isolation rules

- Omission from a positive allowlist is denial.
- Every transfer is a CONTROL-signed, hash-addressed ledger row. Conversation text, an unmanifested directory, and worktree proximity are not channels.
- Worktrees isolate edits, not secrets or independent knowledge.
- Paired authors, scanners, reviewers, builders, judges, comparator operators, generators, and analysis-map builders are distinct fresh roots and do not inherit one another.
- A person, account, task ancestry, or storage grant cannot cross incompatible roles. Compatible deterministic custodial tasks may share an operator only when the frozen role-conflict matrix expressly permits it.
- Executors never receive labels, expected values, comparators, condition maps, other packages, or other outputs.
- The CONTROL registrar is content-blind. Content intake, condition-map custody, and final decision joining are separate roles.
- No sealed, private, hidden-oracle, real, customer, personal, secret, or past-project material enters any public role.

## 3. Complete per-role matrix

| Role | Positive inputs | Explicit denylist | Only output / store |
|---|---|---|---|
| CONTROL registrar | reviewed public-design hashes; role/store attestations; artifact digests; pass/reject digests; final anonymous analysis hash | bank/prompt contents; labels; raw or anonymous semantic outputs; condition map; executor reasoning; sealed material | signed gate/status manifests in registrar store |
| content-intake custodian | frozen author bank/prompt contents and author signature | labels; representations before routing; outputs; condition map; sealed material | immutable content vault, exact recipient copies, content digest |
| simulation builder/operator | frozen statistical specification, generator bounds, pre-bank manifest | bank facts; labels; prompts; confirmatory output; condition map | implementation hashes, benchmark, calibration, and power summaries in compute store |
| public fact author | frozen authoring protocol, synthetic constraints, selected N | labels; representations; outputs; sealed/real material | frozen canonical bank and prompts to content intake |
| label author A / B | frozen contract and one exact content-intake copy | the other label bundle; representations; outputs; condition map | separate signed label bundle in A/B vault |
| label-comparison custodian | signed bundles A and B | representations; packages; outputs; condition map | equality digest and agreed bundle only on byte equality |
| representation builder | exact content-intake copy and frozen transformation specification | labels; expected values; mutations; outputs | A-D representations and equality manifest |
| package builder / scanner 1 | one assigned representation; questions; runner allowlist; frozen scanner specification | labels; expected answers; other outputs; sealed material | signed package, inventory, scan-1 table and hashes |
| scanner 2 | frozen scanner specification and completed signed package only | scan-1 table/internals; labels; outputs | independent inventory and scan-2 table |
| scan-comparison custodian | scan-1 and scan-2 tables | package prose; labels; outputs; condition map | equality/pass or reject digest |
| semantic-leakage reviewer 1 / 2 | completed package and agreed label bundle | executor outputs; condition narrative/map; other reviewer output; sealed material | separate signed pass/reject table |
| leakage-comparison custodian | two signed leakage tables | package prose beyond hashed identity; outputs; condition map | equality/pass or reject digest |
| comparator builder 1 / 2 | frozen metadata, cause/evaluation/consumption, canonicalization, mutation specifications | other comparator internals; confirmatory outputs; condition map | implementation hash and public mutation-result table |
| expected-catalog generator 1 / 2 | frozen catalog specifications and, after labels, agreed label bundle | comparator output/internals; confirmatory output; condition map | abstract and bank-instance expected tables with counts/hashes |
| catalog-comparison custodian | both independent expected tables | comparator output; confirmatory output; condition map | byte-equality digest and agreed expected table |
| P1 catalog reviewer 1 / 2 | frozen specifications, agreed expected table, invariant/rejection summaries | comparator output; confirmatory output; condition map; other reviewer output | separate signed catalog review |
| P1-review comparison custodian | two signed catalog reviews | bank prose beyond hashed IDs; outputs; condition map | exact agreement/pass or reject digest |
| condition-map and schedule custodian | signed packages; A-D identities; bank hash; schedule rules; opaque run-ID namespace | labels; expected answers; raw outputs; semantic judgments | encrypted semantic condition map; opaque balanced schedule/routing map |
| blinded-analysis-map builder 1 / 2 | frozen P2-P4 formulas, semantic condition/schedule map, opaque cell namespace | labels; expected answers; confirmatory output; other builder output | separate blinded coefficient/stratum map |
| analysis-map comparison custodian | two blinded maps | labels; output; semantic condition names after comparison | agreed blinded map and equality digest |
| run dispatcher/transport recorder | signed opaque schedule and assigned package; raw response byte stream | labels; expected answers; semantic condition map; prior outputs | signed dispatch/run log, monotonic endpoints, first raw response to write-only vault |
| public executor | one signed package, common resource manifest, opaque run ID | labels; mappings; comparators; mutations; other packages/outputs; network/tools not allowed | first raw response byte stream to transport recorder |
| raw-output custodian/anonymizer | write-only raw vault; opaque routing map; signed run logs; anonymization rules | labels; expected answers; A-D semantic map; comparator logic | raw hashes, anonymous semantic bundle, anonymous timing/byte table |
| semantic judge 1 / 2 | agreed adjudication bundle; anonymous parseable outputs; reason rubric | semantic condition map; timing/cost/load; other judge; sealed material | separate signed anonymous semantic judgments |
| judgment-comparison custodian | two signed judgment tables | semantic condition map; timing; raw package identity | equality digest and agreed semantic table |
| comparator operator 1 / 2 | assigned frozen comparator; agreed labels; anonymous outputs; agreed semantic table; agreed P1 expected table for mutation phase | semantic condition map; timing; other comparator internals | anonymous atom/event/total table and P1 comparison table |
| adjudication-comparison custodian | both comparator tables | raw prose; semantic condition map; timing | equality digest and agreed derived binary/metric table |
| analysis role | agreed derived table; anonymous timing/byte table; calibrated constants; opaque packet/cell IDs; agreed blinded analysis map | raw prose; executor reasoning; labels beyond derived truth; semantic condition map | frozen anonymous P2-P4 statistics, decision inputs, and hash |
| final-decision custodian | frozen anonymous analysis; semantic condition map released after analysis hash; frozen decision table | raw outputs; authority to reanalyze or change thresholds | mechanical join and public decision record |

Custodians perform only the stated deterministic routing, hashing, comparison, anonymization, or join. They do not author, label, review semantics, execute, judge, implement a comparator, or analyze.

## 4. Complete transfer ledger

Every positive cross-role input in section 3 has one or more rows below. Stores named as recipients are ACL-enforced artifacts, not implicit human recipients.

| Step | Producer | Artifact | Recipient | Required check |
|---:|---|---|---|---|
| 1 | registrar | reviewed design hashes and pre-bank manifest | simulation builder/operator | hash and role grant |
| 2 | simulation builder/operator | benchmark, null-audit, power summaries | registrar | signed summary hashes and ceilings only |
| 3 | fact author | frozen canonical bank/prompts | content-intake custodian | author signature, selected N, content hash |
| 4 | content-intake custodian | content digest only | registrar | no content bytes |
| 5 | content-intake custodian | byte-identical frozen content copies | label A, label B, representation builder | recipient-specific signed copy manifest |
| 6 | label A / B | separate signed bundles | label-comparison custodian | separate ACL channels |
| 7 | label-comparison custodian | equality digest | registrar | no label contents |
| 8 | label-comparison custodian | agreed bundle | adjudication-label vault for generators, leakage reviewers, judges, comparator operators | exact equality; recipient ACLs open only at listed phases |
| 9 | representation builder | representations/equality manifest | package builder, condition-map custodian | canonical-fact equality and hashes |
| 10 | representation builder | equality digest | registrar | no representation content |
| 11 | package builder/scanner 1 | completed package | scanner 2, leakage-review vault, condition-map custodian | signed package hash |
| 12 | package builder/scanner 1 | scan-1 table | scan-comparison custodian | separate ACL channel |
| 13 | scanner 2 | scan-2 table | scan-comparison custodian | no scan-1 access |
| 14 | scan-comparison custodian | equality/pass or reject digest | registrar | exact inventory and scan equality |
| 15 | leakage-review vault | completed package plus agreed labels | leakage reviewer 1, leakage reviewer 2 | separate read-only grants |
| 16 | leakage reviewer 1 / 2 | signed review tables | leakage-comparison custodian | separate ACL channels |
| 17 | leakage-comparison custodian | agreement/pass or reject digest | registrar | exact agreement |
| 18 | comparator builder 1 / 2 | implementation hash and mutation table | comparator vaults; registrar receives hashes only | separate internals and signed versions |
| 19 | expected-catalog generator 1 / 2 | abstract expected table | catalog-comparison custodian | frozen generator/spec hashes |
| 20 | catalog-comparison custodian | agreed abstract table and digest | P1 reviewer 1, P1 reviewer 2; registrar gets digest only | byte equality |
| 21 | agreed-label vault | agreed label bundle | expected-catalog generator 1, generator 2 | only after label equality |
| 22 | expected-catalog generator 1 / 2 | bank-instance expected table/coverage manifest | catalog-comparison custodian | frozen generator, no rule change |
| 23 | catalog-comparison custodian | agreed bank-instance table and digest | P1 reviewer 1, P1 reviewer 2; comparator operators; registrar gets digest only | byte equality |
| 24 | P1 reviewer 1 / 2 | signed catalog review | P1-review comparison custodian | separate ACL channels |
| 25 | P1-review comparison custodian | agreement/pass or reject digest | registrar | exact agreement |
| 26 | condition-map/schedule custodian | semantic condition/schedule map plus formulas | blinded-map builder 1, builder 2 | pre-call frozen map hash; separate grants |
| 27 | blinded-map builder 1 / 2 | blinded coefficient/stratum maps | analysis-map comparison custodian | separate builds |
| 28 | analysis-map comparison custodian | agreed blinded map | analysis role; registrar gets digest only | byte equality before calls |
| 29 | condition-map/schedule custodian | opaque schedule and routing map | dispatcher/transport recorder; raw-output custodian | balance proof and opaque IDs |
| 30 | dispatcher/transport recorder | one assigned signed package/request | one fresh executor | assignment and pre-send monotonic timestamp |
| 31 | executor | first raw response byte stream | dispatcher/transport recorder | no retry, prior-output access, or second response |
| 32 | dispatcher/transport recorder | raw response plus signed dispatch/run log and endpoints | write-only raw-output vault | durable-final-byte timestamp and raw hash |
| 33 | raw-output custodian | anonymous semantic bundle | judges and comparator operators | identity stripping and raw-hash link |
| 34 | raw-output custodian | anonymous timing/byte table | analysis role | no semantic content or condition map |
| 35 | judges 1 / 2 | signed semantic tables | judgment-comparison custodian | separate ACL channels |
| 36 | judgment-comparison custodian | agreed semantic table | comparator operators | exact equality or stop |
| 37 | comparator operators 1 / 2 | derived tables | adjudication-comparison custodian | separate implementations |
| 38 | adjudication-comparison custodian | agreed derived table | analysis role | byte equality or stop |
| 39 | analysis role | frozen anonymous statistics, decision inputs, and hash | registrar and final-decision custodian | condition map still withheld; registrar receives hash/status only |
| 40 | condition-map/schedule custodian | semantic condition map | final-decision custodian | only after authenticated analysis hash |
| 41 | final-decision custodian | mechanical map/analysis join under frozen table | public decision record; registrar gets record digest | no reanalysis or threshold change |

An unlisted transfer, missing ledger artifact, positive-input/ledger mismatch, denylist conflict, or extra reader invalidates the bank version. The pre-call custody checker proves a bijection between each matrix output/input edge and these rows and records zero unmatched edges.

## 5. Blinded analysis-design map

The semantic condition map is withheld from the analysis role. Two independent builders instead derive a byte-identical map whose rows contain only opaque IDs and the coefficients needed to execute the frozen formulas.

For P2 each opaque cell row contains:

- observer stratum ID, packet ID, stream ID, and the twelve question IDs;
- leakage-stream membership;
- equivalence-pair ID; and
- difference weight `+1` for the first member and `-1` for the second member.

The analysis role computes each stream mean, each packet difference, four leakage tests, and two equivalence tests from these fields without receiving the words `original`, `neutral`, `O1`, or `O2`. The builders prove that every opaque cell appears once and every pair has one `+1` and one `-1` member.

For P3 each opaque cell row contains packet/question IDs and one frozen contrast coefficient:

- target grammar C/D: `+1/2` each;
- target grammar A/B: `-1/2` each;
- comparison grammar C/D: `-1/2` each; and
- comparison grammar A/B: `+1/2` each.

The map does not contain the semantic grammar or representation names. It contains only opaque stratum IDs, the coefficient, and a proof that each packet has two of each coefficient-sign/grammar-role combination required by the inherited `z[k]` formula.

For P4 each row additionally contains:

- schema-pool role `target|comparison` encoded as opaque `P0|P1` with the frozen numerator/difference direction;
- one of four opaque target-stratum IDs for the max-minus-min calculation;
- time/byte burden role `numerator|denominator`; and
- packet-cluster resampling ID.

The public formula manifest fixes which opaque value is numerator, target pool, difference minuend, and range population. Thus analysis is executable but semantic condition identity remains withheld. Both builders sign a sufficiency matrix proving that every P2-P4 statistic consumes only columns present in the derived table, timing table, constants, and blinded map. The map freezes before calls and cannot encode results because none exist.

After analysis freezes, the final-decision custodian alone joins the semantic map to the frozen anonymous statistics. It applies the already frozen decision table and cannot recompute a statistic, relabel a cell, change a sign, or reopen analysis.

## 6. Bank size and single freeze sequence

The inherited candidate N sequence remains `240, 336, 432, 528, 624, 720`, with all divisibility and no-duplicate rules unchanged.

The only authorized sequence is:

1. Obtain fresh independent public-only review of URC-0.8 and this plan.
2. Freeze typed templates, authoring/metadata specifications, canonical-cause rules, abstract/availability catalog generators, abstract catalogs, statistical formulas, simulation version, role grants, custody stores, ceilings, and N sequence.
3. Freeze the immutable pre-bank power manifest using the authenticated v0.8 composition hashes.
4. Benchmark simulation plus worst-case catalog generation/comparison/storage/review; stop on any ceiling failure.
5. Fit/audit every null boundary, run power, and select the smallest sufficient N.
6. Author and hash the untouched synthetic public bank of exactly N questions.
7. Label independently, hash both bundles, and reject the whole bank on any byte difference.
8. Run the already frozen catalog generators once on the agreed labels; freeze the bank-instance expected table and coverage manifest after generator equality and two P1 review signatures.
9. Freeze representations, equality manifest, 24-code control, packages, scanners, comparators, anonymization, and custody manifests.
10. Complete both scans and both semantic-leakage reviews; reject on difference or rejection.
11. Freeze the balanced schedule, semantic condition map, agreed blinded analysis map, exact model revision, service configuration, run manifests, and cost preflight.
12. Run P0-P2; run P3-P4 only if earlier gates pass.
13. Freeze judgments, comparator tables, derived table, and anonymous analysis hash before releasing the semantic condition map to the final-decision custodian.
14. Mechanically join the frozen map and analysis under the decision table; do not reanalyze.

The pre-bank generator/catalog freeze and the post-label instance-table freeze are different named artifacts. The second stage has no discretion to add, delete, or alter a mutation or expected equation. Nothing is dropped, edited, relabeled, replaced, or selectively rerun after labels or confirmatory output are visible.

## 7. Replacement P0 and P1 requirements

P0 retains every v0.4 requirement and additionally requires exact independent agreement that:

- the canonical cause-key constructor is biconditional and author cause IDs are impossible;
- all coordinate selectors return the full deterministic source set, including both basis and responsibility when both are wrong;
- every C1-C7 branch and quantifier follows the frozen T/F/U tables;
- decisive-T, decisive-F, and unresolved mutations have exact sources and consequences;
- target-record typing and every repeated-component maximum are enforced before satisfiability;
- abstract and availability catalogs meet their declared row bounds and contain explicit rejection witnesses;
- both generators and both catalog reviewers agree; and
- every role-matrix edge, ledger row, signature, timestamp producer, scan, map, and store grant has zero unmatched or conflicting entries.

One unspecified branch, nonunique cause, unknown schema-valid formula, missing row, generator difference, reviewer difference, or custody mismatch fails P0.

P1 retains independent byte-identical labels and both independent comparators. Its mutation catalog additionally contains:

- every canonical-key same/different boundary and forbidden author alias;
- basis-only, responsibility-only, and both-coordinate `wrong_direct` and `stronger_sources` cases;
- all C1-C7 decisive-T/unrelated-U, decisive-F/unrelated-U, and unresolved-U cases;
- all permitted decision, dual-tag, obligation-to-M1, and affected-closure sharing cases;
- repeated-component counts from zero through each maximum;
- record and non-record target forms, including every invalid target-record edge; and
- every abstract catalog row plus the frozen bank-instance projection.

Expected values come only from the two frozen expected-catalog generators. Comparator tables are compared to the already agreed expected table, never to one another as an authority. Any expected-generator, catalog-review, comparator, semantic-judge, or label difference fails P1.

## 8. Prospective and confirmatory seeds

The inherited non-circular seed rule is preserved. The immutable manifest contains the effective v0.8 contract/plan hashes, generator/catalog hashes, statistical/simulation hashes, RNG versions, candidate N sequence, grids, constant grid, replicate ceilings, benchmark environment, custody-map hashes, and resource ceilings.

Each pre-bank stream uses `PCG64-DXSM` seeded by the unsigned first 128 bits of SHA-256 over:

`URC-0.8|PREBANK|<manifest-hash>|<phase>|<test>|<N>|<grid-id>|<stream-id>`.

No prospective seed contains a bank hash. Post-bank seeds remain limited to the inherited control permutation, anonymization, packet permutation, schedule, and P4 resampling uses.

## 9. Revision, transport, and elapsed custody

The inherited revision/load/drift rules remain. The dispatcher/transport recorder, not the model executor, owns the transport log. Immediately before the first request byte is sent it records the monotonic start; it receives the executor's first raw byte stream; immediately after the final raw byte is durably stored it records the monotonic end. It signs the raw hash, endpoints, scheduled wave, revision/fingerprint, tier, region, throttling, errors, and no-retry status as one run-log artifact.

The raw-output custodian verifies the raw hash and endpoint signature before anonymization and derives the anonymous timing/byte table. A missing, nonmonotonic, multiply produced, or unmatched endpoint invalidates the suite. The inherited elapsed interval, pooling, median, ratio, bootstrap, schedule, concurrency-three, seven-day, and no-retry definitions do not change.

## 10. Revised nonoverlapping human and resource ledger

| Task ledger | Maximum hours |
|---|---:|
| registrar, content intake, schedule/map custody, final join, and grant administration | 50 |
| synthetic fact authoring and cleanup | 40 |
| label A/B and deterministic label comparison | 50 |
| contract/leakage/catalog review, semantic judging, and comparison | 45 |
| simulation/comparator/generator implementation, scans, analysis, and incident reserve | 55 |
| **Aggregate** | **240** |

Catalog generator implementation belongs only to the fifth row; catalog review belongs only to the fourth. Each labor event is logged once, paired incompatible roles remain distinct, and hours are never double-booked. The pre-bank benchmark records projected CPU, RAM, temporary/persistent storage, generated row counts, comparison time, reviewer active time, and signing time for the 276,480-row abstract bound and 2,949,120-row bank-instance bound. Any projection beyond 240 hours or an inherited compute/storage/calendar/monetary ceiling stops before bank authoring.

All inherited N=720 call/token arithmetic, USD 500 compute, USD 3,000 total, 100 GiB confirmatory storage, 30-day end-to-end, seven-day confirmatory, per-call, and no-retry ceilings remain unchanged and unvalidated.

## 11. Comparator reliability replacement

Both frozen comparators still run the mutation catalog 100 times and must be byte-identical across all 200 runs. They must also match the frozen agreed expected table for every run on format atoms, T/F/U availability, canonical surface-to-cause keys, code truth/source sets, prior/residual/consumed sets, events, diagnostics, and totals. Agreement between two identically wrong comparators is failure if either differs from the independent expected table. Semantic judges and P1 reviewers must agree exactly; CONTROL cannot select a view.

## 12. Equality, stopping, rollback, and claim limit

The inherited A-D equality requirements and noncompensatory stops remain. Additional stops are: author-entered/noncanonical causes, an unclassified T/F/U branch, repeated-component overflow, invalid target-record relation, catalog count/coverage mismatch, generator/reviewer disagreement, unmatched custody edge, missing scan/run log/timestamp/map/signature, analysis-map insufficiency, premature condition-map release, or post-map reanalysis.

Failure preserves the authenticated inputs and untouched evidence, invalidates reuse of an exposed bank, and opens no later gate automatically.

Even a future complete pass would support only:

> Under the frozen synthetic public bank, exact model revision, observer prompts, representations, 24-code control, audited dependence grids, balanced schedule, bounded catalog generators, custody and blinded-analysis maps, resource ceilings, and frozen algorithms, URC-0.8 did not cross the precommitted public rejection thresholds.

It would not establish superiority outside that bounded experiment, sealed compatibility, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

The only next action authorized by this redesign package is a fresh public-only independent read-only review under a separate exact gate.
