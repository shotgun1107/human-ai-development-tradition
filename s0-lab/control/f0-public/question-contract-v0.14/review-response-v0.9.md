# URC-0.14 response to v0.13 independent review

- status: **author response proposal; not an independent verdict**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.14 REDESIGN OPEN`
- reviewed predecessor: `s0-lab/reviews/f0-public/question-contract-v0.13/urc-v0.13-independent-review-v0.1.md`
- reviewed predecessor SHA-256: `4098e2060cf5c48677981999fe3fdb1c0683f1cb3a319811a5c64ec41170dd76`
- companion proposal: `universal-response-contract-v0.14-candidate.md` and `public-falsification-plan-v0.11.md`

## 1. Scope and claim discipline

The v0.13 review returned `REVISE-AND-REVIEW` with zero blocking, three major, and one minor finding. This response proposes bounded corrections for V13-M01 through V13-M03 and V13-m01. It preserves authenticated predecessors and the U11 semantic slice rather than editing them in place.

The mappings below are author claims for a fresh public-only reviewer to attack. They do not establish closure, integration suitability, implementation, feasibility, validation, S0 success, or any empirical result.

## 2. V13-M01 — mandatory payloads replaced by receipts

### 2.1 Review defect

V0.13 correctly added status receipts but its E25, E35, and E48 edge rows named only digest/receipt artifacts where downstream roles required implementation-table bytes, agreed blinded-map bytes, or frozen anonymous analysis bytes. A receipt authenticated existence but did not deliver the protected payload.

### 2.2 Proposed correction

Plan sections 2, 3, and 5.1 explicitly split protected payload and public receipt destinations:

- E25 writes each exact implementation/mutation-table payload and digest to its matching comparator vault for its matching operator, while each builder separately sends only its signed receipt to the registrar;
- E35 writes exact agreed blinded-map bytes to `analysis-map-vault` for E47 and separately sends only its signed digest receipt to the registrar;
- E48 sends exact frozen anonymous P2-P4 statistics/decision-input bytes and hash to final-decision custodian and separately sends only its signed digest receipt to the registrar;
- E27, E29, and E50 are republished with the same explicit payload/receipt split to prevent the repaired rule from remaining local or ambiguous; and
- neither registrar store is authorized to contain protected payload bytes.

This preserves downstream executability while keeping public status evidence digest-only.

### 2.3 Required hostile checks

The next review should perform each edge literally and verify that each downstream consumer receives exact payload bytes, that registrar receives only public signed receipts, and that digest/receipt substitution cannot satisfy a payload input. It should also attack wrong vault, cross-builder vault access, payload/digest mismatch, payload exposure to registrar, and an unlisted mirror.

## 3. V13-M02 — no admissible genesis write

### 3.1 Review defect

V0.13 made E51 and `registrar-store` pair-only while declaring that genesis had no bundle. Genesis alone violated atomic-pair rules, and any invented ROOT bundle violated the non-genesis receipt table.

### 3.2 Proposed correction

Plan sections 4.3 and 4.4 define one exact canonical ROOT bundle with:

- the same v0.14 bundle schema;
- `edge=ROOT`;
- `entry_count=0`;
- no receipt entries; and
- the exact authenticated CONTROL-integration manifest SHA-256.

Genesis commits to SHA-256 of those exact ROOT-bundle bytes. E51 atomically stores a signed status envelope plus companion bundle for sequence 0 and every later sequence. E52 therefore has one uniform pair-chain beginning at genesis, without an exception, empty invented artifact, or second writer.

### 3.3 Required hostile checks

The next review should attack genesis without a bundle, an omitted or changed integration-manifest hash, nonzero ROOT receipt count, alternate ROOT schema/field order, a generic empty non-ROOT bundle, partial pair write, duplicate genesis, and another writer or edge.

## 4. V13-M03 — no E25 two-producer bundle assembler

### 4.1 Review defect

V0.13 fixed E25's two receipt roles and byte order but required an already formed bundle without granting either isolated builder the other's receipt or naming an assembler/transfer.

### 4.2 Proposed correction

Plan sections 3, 4.3, and 5 authorize one uniform registrar assembly path:

- every status producer sends individual signed receipt envelopes to registrar on its named evidence edge;
- registrar verifies each receipt and writes its immutable copy to new `registrar-receipt-vault` under exact `(edge, producer_role, artifact_kind)` key;
- E25 builder 1 and builder 2 each send only their own receipt and remain denied the other's receipt;
- only registrar may construct evidence bundles, selecting exact vault keys in the fixed receipt-table order;
- duplicates, replacements, missing/extra receipts, changed bytes, wrong signer/role/kind, or assembly before all lower-bit pairs freeze reject; and
- E51 stores only the resulting deterministic bundle and signed status envelope in `registrar-store`.

The receipt vault has one writer and one reader, both registrar, contains only signed public receipt envelopes, and adds no protected-payload channel. This also makes E02 and all one-entry bundles use the same assembly rule.

### 4.3 Required hostile checks

The next review should try builder-to-builder transfer, builder-assembled bundle, registrar alteration/resigning, two receipts from one role, missing builder, wrong vault key, receipt replacement, premature assembly, and a hidden transport aggregator.

## 5. V13-m01 — stale v0.10 freeze reference

### 5.1 Review defect

The retained P7 freeze sequence still required review of v0.10, so a checker could satisfy the current package's first normative step with an historical review.

### 5.2 Proposed correction

Effective-plan slot 7 no longer sources P7. P11 section 6 republishes the complete bank-balance and only-freeze sequence and requires fresh independent review of the complete v0.14 package and sidecars with exact verdict `PASS-FOR-CONTROL-INTEGRATION-ONLY`. All later balance, catalog, resource, freeze, no-edit, and no-rerun constraints remain.

### 5.3 Required hostile checks

The next review should verify slot 7 comes only from P11, contains no normative v0.10/v0.13 review token, names the current package, requires exact allowed verdict, and does not weaken any inherited balance/freeze step.

## 6. Preserved predecessor properties

The proposal retains without intentional semantic change:

- the complete U11 semantic atom, availability, strength, permission, cause, selector, C1-C7, consumption, response, and P3 rules;
- global record-ID and cause ordering;
- 24-row balance, duplicate/example restrictions, schedules, stochastic models, 240-hour resource ledger, isolation, rollback, and claim ceiling;
- the v0.13 noncircular root and fixed 22-role key registry construction;
- recipient-verifiable E42-E45 source-envelope comparison;
- public publisher/reader and E53-E56 publication path; and
- eight E00 grants, E01-E56, and 32 experimental matrix/index roles.

The only intended inventory change is one public-receipt-only store, increasing literal stores from 26 to 27.

## 7. Author-side consistency checks required before review

Before freezing this proposal, CONTROL must verify:

1. every named frozen input against its sidecar and no input hash change;
2. unique 31-slot and 25-slot effective constructions;
3. exactly two count-one P5 slot-10 transforms to v0.14;
4. eight E00 grants, E01-E56, 27 stores, and 32 matrix/index rows;
5. 22 unique registry roles in fixed ASCII order;
6. 14 status edges totaling 17 receipts, with E02 count three and E25 count two;
7. one canonical ROOT bundle, registrar-only bundle assembly, and exact E51/E52 pair topology;
8. explicit payload/receipt splits for E25/E35/E48 and no protected registrar payload;
9. a v0.14-specific complete freeze sequence; and
10. canonical validator self-test plus independent UTF-8, BOM, final-LF, trailing-whitespace, sidecar-record/hash reports, exact six-file change set, and task-specific branch/HEAD checks.

These are construction and document-consistency checks only. They are not cryptographic execution, key generation, role feasibility, implementation, or experiment results.

## 8. Requested next disposition

After the six v0.14 files freeze and are committed under separate user approval, the appropriate next gate is a fresh public-only `F0-PUBLIC QUESTION CONTRACT V0.14 INDEPENDENT REVIEW OPEN`. The reviewer should receive an exact public allowlist, authenticate every input, independently reconstruct both effective streams, attack all four mappings above, and recheck predecessor passes for non-regression.

No key generation, schema, bank, fixture, oracle, generator, comparator, runner, simulation, model call, scoring, sealed work, or S0 execution gate is opened by this response.
