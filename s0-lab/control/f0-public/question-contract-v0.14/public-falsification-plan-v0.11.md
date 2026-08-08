# URC-0.14 public falsification plan v0.11

- status: **public CONTROL redesign proposal; not independently reviewed or executed**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.14 REDESIGN OPEN`
- companion: `universal-response-contract-v0.14-candidate.md`
- predecessor evidence: authenticated plans v0.4-v0.10 and v0.13 independent review v0.1
- excluded: implementation, bank/fixture/oracle authoring, key generation, simulation, model calls, scoring, sealed work, and S0 conclusions

## 1. Complete effective-plan construction

### 1.1 Authenticated source identities

The effective plan is a direct four-source composition:

| Source ID | Exact file | SHA-256 source |
|---|---|---|
| `P4` | `question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` |
| `P5` | `question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` |
| `P6` | `question-contract-v0.9/public-falsification-plan-v0.6.md` | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` |
| `P11` | this `public-falsification-plan-v0.11.md` | its matching same-basename sidecar after this file freezes |

P7-P10 and their reviews are authenticated predecessor evidence, not byte sources. P11 section 6 republishes the previously reviewed balance and freeze sequence with the current package identity, while sections 2-5 replace all prior custody slices.

### 1.2 Total transitive section map

Every effective v0.13 plan slot is retained or replaced exactly once.

| Effective slot | Effective v0.13 coverage | Action | Exact effective source slice |
|---:|---|---|---|
| 1 | slot 1 | replace | full `P11` section 1, heading `## 1. Complete effective-plan construction` |
| 2 | slot 2 | retain | full `P4` section 2, heading `## 2. Facts, inferences, and proposals` |
| 3 | slot 3 | retain | full `P5` section 2, heading `## 2. Role isolation rules` |
| 4 | slot 4 | replace | full `P11` section 2, heading `## 2. Corrected complete role matrix` |
| 5 | slot 5 | replace | full `P11` sections 3-5, from `## 3. Exact named store identities` through `## 5. Closed matrix-ledger bijection` |
| 6 | slot 6 | retain | full `P5` section 5, heading `## 5. Blinded analysis-design map` |
| 7 | slot 7 | replace | full `P11` section 6, heading `## 6. Current bank balance and freeze sequence` |
| 8 | slot 8 | replace | full `P11` section 7, heading `## 7. Replacement P0 and P1 requirements` |
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
| 25 | slot 25 | replace | full `P11` section 8, heading `## 8. Equality, stopping, rollback, and claim limit` |

No P4-P10 effective range is unspecified. Every P10-derived effective slice is replaced; P10 remains authenticated failure evidence only.

### 1.3 One complete plan-record grammar

Use only companion candidate section 3.3 steps 1-7 for source authentication, heading resolution, slicing, and heading-digest computation. Do not emit the companion contract record. For plan records, emit this complete grammar once:

```text
slot=<decimal slot>\n
source=<P4|P5|P6|P11>\n
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
transform_1_to_hex=76302e3134
transform_1_required_occurrences=1
transform_2_from_hex=5552432d302e38
transform_2_to_hex=5552432d302e3134
transform_2_required_occurrences=1
```

The pairs mean exact ASCII `v0.8` to `v0.14` and `URC-0.8` to `URC-0.14`. Apply them sequentially to the authenticated raw P5 section 8 slice. Before each replacement, its exact source byte sequence must occur once and only once; otherwise construction rejects. Replacement is global for that one occurrence, without normalization or case folding. Neither replacement changes a formula, seed field, threshold, or allowed seed use.

The effective stream is ASCII `URC-0.14-PLAN-EFFECTIVE\n` followed by the 25 records with no separator beyond the grammar bytes. `effective_plan_sha256` is SHA-256 of that stream and freezes only in a later reviewed manifest after the P11 sidecar exists.

## 2. Corrected complete role matrix

The inherited isolation rules remain. Omission is denial; worktrees isolate edits only; paired independent roles are distinct fresh roots; conversation text and ambient repository access are not transfer channels. “Public specification” means only independently reviewed public bytes and never bank content, labels, outputs, condition maps, or sealed material. The `control-root-authority` is a pre-run public trust identity governed by section 4.1, not an experimental actor and not one of the 32 roles below.

| Role | Positive inputs | Explicit denylist | Only output / store |
|---|---|---|---|
| CONTROL registrar | authenticated reviewed public specification bytes/hashes, separately authenticated root anchor and root-signed registry, role/store/key assignment matrix, individual signed evidence-receipt envelopes, anonymous analysis hash, publication-receipt digest | bank/prompt contents, labels, protected payload bytes except expressly digest-only receipts, raw/anonymous semantic outputs, condition map, executor reasoning, sealed material, root private key | recipient-specific signed public-specification grants E00A-H/E01; verified receipt-envelope copies in `registrar-receipt-vault`; deterministic bundles and atomic signed status-envelope/bundle pairs in `registrar-store` |
| public status reader | user-approved integration commit and manifest hash, root anchor, root-signed registry, and paired status envelopes/evidence bundles delivered by E52 | every protected bank/prompt byte, label, output, condition map, comparator/judge internals, sealed material | none; terminal read-only role |
| public record publisher | publication/transport/signing specification and authenticated registry by E00G; exact final decision record and digest by E53 | raw output, labels, condition map, anonymous tables, threshold inputs, sealed material | byte-identical decision record plus signed canonical publication receipt in `public-decision-store` by E54; E56 receipt-envelope digest and signed evidence receipt to registrar |
| public record reader | root anchor, authenticated registry, exact decision record, and publication receipt delivered by E55 | every nonpublic experimental artifact and sealed material | none; terminal read-only role |
| content-intake custodian | frozen author bank/prompts and signature; signing grant/key assignment | labels, outputs, condition map, sealed material | immutable content/exact copies in `content-vault`; E05 content digest and signed evidence receipt to registrar |
| simulation builder/operator | frozen statistical/catalog specifications and pre-bank manifest; signing grant/key assignment | bank facts, prompts, labels, confirmatory output, condition map | implementation/benchmark/calibration/power summaries; selected constants/public formula manifest; three signed E02 evidence receipts to registrar |
| public fact author | frozen authoring protocol, constraints, selected N | labels, representations, outputs, sealed/real material | frozen bank/prompts to content intake |
| label author A / B | exact content copy and frozen contract | other label, representations, outputs, condition map | separate signed bundles in `label-vault-A` and `label-vault-B` respectively |
| label-comparison custodian | signed A/B bundles; signing grant/key assignment | representations, packages, outputs, condition map | equality digest and signed E08 evidence receipt to registrar; agreed bundle only in `agreed-label-vault` |
| representation builder | exact content copy, frozen transformation specification, signing grant/key assignment | labels, expected values, outputs | representations/equality manifest in `representation-vault`; equality digest and signed E14 evidence receipt to registrar |
| package builder / scanner 1 | assigned representation, questions, runner allowlist, scanner specification | labels, expected answers, outputs, sealed material | signed package in `signed-package-vault`; scan-1 table in `scan-vault-1` |
| scanner 2 | completed signed package and scanner specification | scan-1 table/internals, labels, outputs | scan-2 table in `scan-vault-2` |
| scan-comparison custodian | scan-1/scan-2 tables; signing grant/key assignment | package prose, labels, outputs, condition map | equality/pass or reject digest and signed E21 evidence receipt to registrar |
| leakage reviewer 1 / 2 | signed package, agreed labels, leakage-review specification | executor output, condition map/narrative, other reviewer, sealed material | separate signed tables in `leakage-vault-1` and `leakage-vault-2` respectively |
| leakage-comparison custodian | two leakage tables; signing grant/key assignment | package prose beyond hash, outputs, condition map | equality/pass or reject digest and signed E24 evidence receipt to registrar |
| comparator builder 1 / 2 | frozen metadata, ID-order, semantic-atom, cause/evaluation/consumption, canonicalization, mutation specifications; own signing grant/key assignment | other comparator internals, confirmatory output, condition map, other builder receipt | exact implementation/mutation-table bytes and digest in own comparator vault for own operator; own fixed-role signed E25 evidence receipt separately to registrar |
| expected-catalog generator 1 / 2 | frozen catalog, semantic-atom, and ID-order specifications and later agreed labels | comparator output/internals, confirmatory output, condition map | abstract and bank-instance tables in own generator vault |
| catalog-comparison custodian | both generator tables; signing grant/key assignment | comparator/confirmatory output, condition map | agreed table bytes in `catalog-vault`; signed E27/E29 evidence receipts separately to registrar |
| P1 reviewer 1 / 2 | frozen specifications, agreed tables, rejection summaries | comparator/confirmatory output, condition map, other review | signed catalog reviews in own P1 review vault |
| P1-review comparison custodian | two P1 reviews; signing grant/key assignment | bank prose beyond hashed IDs, outputs, condition map | agreement/pass or reject digest and signed E31 evidence receipt to registrar |
| condition-map/schedule custodian | finalized signed packages, representations/equality manifest, A-D identities, bank hash, schedule rules, opaque run IDs | labels, expected answers, raw output, judgments | semantic map in `condition-map-vault`; opaque schedule/routing; assigned signed package to dispatcher |
| blinded-map builder 1 / 2 | frozen P2-P4 formulas, semantic condition/schedule map, opaque namespace | labels, expected answers, output, other builder | separate blinded coefficient/stratum maps |
| analysis-map comparison custodian | two blinded maps; signing grant/key assignment | labels, outputs, semantic names after comparison | exact agreed blinded-map bytes in `analysis-map-vault`; signed E35 evidence receipt separately to registrar |
| dispatcher/transport recorder | opaque schedule/routing and one assigned signed package | labels, expected answers, semantic map, prior outputs | request, signed run log, monotonic endpoints, first raw response in `raw-output-vault` |
| public executor | one signed package, common resources, opaque run ID | labels, mappings, comparators, mutations, other packages/outputs, forbidden tools/network | first raw response stream only |
| raw-output custodian/anonymizer | raw vault, routing map, run logs, anonymization rules | labels, expected answers, semantic condition map, comparator logic | raw hashes, anonymous semantic bundle, anonymous timing/byte table |
| semantic judge 1 / 2 | agreed labels, anonymous parseable output, reason rubric, own signing grant/key assignment | condition map, timing/cost/load, other judge, sealed material | own signed canonical anonymous judgment-table envelope in own judgment vault |
| judgment-comparison custodian | two signed judgment-table envelopes; signing specification/key assignment | condition map, timing, raw package identity | signed canonical E43 comparison envelope/digest, both authenticated source envelopes, and agreed semantic table record bytes |
| comparator operator 1 / 2 | own comparator-vault implementation/mutation-table bytes through E25, agreed labels/expected table, anonymous output, E43 bundle, own signing grant/key assignment | condition map, timing, other comparator internals and other comparator vault | own signed canonical anonymous atom/event/total and P1 derived-table envelope |
| adjudication-comparison custodian | both signed derived-table envelopes; signing specification/key assignment | raw prose, condition map, timing | signed canonical E45 comparison envelope/digest, both authenticated source envelopes, and agreed derived table record bytes |
| analysis role | E45 bundle, exact blinded map through E47, timing table, selected calibrated constants, public formula manifest, opaque IDs, frozen statistical decision table; signing grant/key assignment | raw prose, executor reasoning, semantic condition map | exact frozen anonymous P2-P4 statistics/decision-input bytes and hash to final-decision custodian; signed E48 evidence receipt separately to registrar |
| final-decision custodian | exact frozen anonymous statistics/decision-input bytes and hash through E48, post-hash semantic map, frozen decision table; signing grant/key assignment | raw output, reanalysis, threshold changes | mechanical join/exact public decision record in `final-decision-vault`; signed E50 evidence receipt separately to registrar |

## 3. Exact named store identities

Each row names a literal global store ID, one writer, and all readers.

| Store ID | Only writer | Authorized readers |
|---|---|---|
| `registrar-receipt-vault` | CONTROL registrar after signature/role/edge/kind verification on status-source receipt deliveries | CONTROL registrar for fixed-order bundle construction only |
| `registrar-store` | CONTROL registrar through atomic E51 status-envelope/bundle pair writes only | public status reader through E52 only |
| `public-decision-store` | public record publisher through E54 only | public record reader through E55; registrar by E56 receipt artifacts only |
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
| `catalog-vault` | catalog-comparison custodian | P1 reviewers, comparator operators; registrar receives only separate signed receipts |
| `p1-review-vault-1` | P1 reviewer 1 | P1-review comparison custodian |
| `p1-review-vault-2` | P1 reviewer 2 | P1-review comparison custodian |
| `condition-map-vault` | condition-map custodian | blinded-map builders before calls; final-decision custodian only after E48 |
| `analysis-map-vault` | analysis-map comparison custodian | analysis role through E47 |
| `raw-output-vault` | dispatcher/transport recorder | raw-output custodian |
| `judgment-vault-1` | semantic judge 1 | judgment-comparison custodian |
| `judgment-vault-2` | semantic judge 2 | judgment-comparison custodian |
| `final-decision-vault` | final-decision custodian through E50 only | public record publisher through E53; registrar receives only separate signed E50 receipt |

No synonym, unlisted mirror, conversation copy, or ambient directory is an authorized store. E43/E45 source envelopes and E48 analysis payload are direct recipient artifacts, not new stores or ambient copies. Protected payload bytes never enter either registrar store.

## 4. Canonical custody records, hashes, and signatures

All grammars in this section are exact ASCII with LF endings, no BOM, no CR, and one final LF. Decimal integers use ASCII `0` or a nonzero first digit followed by digits; leading zeroes reject. SHA-256 and signature hex use lowercase ASCII. SHA-256 values are exactly 64 hex characters. Ed25519 public keys are 64 lowercase hex characters encoding 32 raw bytes; signatures are 128 lowercase hex characters encoding 64 raw bytes.

### 4.1 Noncircular CONTROL root and key registry

The verification trust root is not obtained from the registry it verifies. Before any experimental edge or signed-artifact acceptance, a later user-approved CONTROL integration decision must designate one exact Git commit as the public trust root and record the exact SHA-256 of these anchor `record_bytes`:

```text
anchor_schema=URC-0.14-CONTROL-ROOT-1\n
root_role=control-root-authority\n
public_key_hex=<64 lowercase hex>\n
key_id=<SHA-256 of the exact 32 raw public-key bytes>\n
```

The anchor has no self-referential commit value. The designated commit must contain the byte-identical anchor record, sidecar, exact registry envelope, and integration decision naming both artifact hashes. A verifier starts from the user-approved commit identity and anchor hash, authenticates anchor bytes from that commit, checks `key_id`, and only then uses that key to verify the registry. This redesign creates no key and opens no integration.

Registry unsigned `record_bytes` are:

```text
registry_schema=URC-0.14-KEY-REGISTRY-1\n
registry_version=1\n
anchor_record_sha256=<SHA-256 of exact anchor record_bytes>\n
entry_count=22\n
<exactly 22 entry blocks in the fixed order below>
```

Each block is:

```text
entry_<n>_role=<exact role ID>\n
entry_<n>_public_key_hex=<64 lowercase hex>\n
entry_<n>_key_id=<SHA-256 of that entry's exact 32 raw public-key bytes>\n
entry_<n>_status=active\n
```

The fixed ASCII-byte order, numbered 1 through 22, is: `adjudication-comparison`, `analysis`, `analysis-map-comparison`, `catalog-comparison`, `comparator-builder-1`, `comparator-builder-2`, `comparator-operator-1`, `comparator-operator-2`, `content-intake`, `control-registrar`, `control-root-authority`, `final-decision-custodian`, `judgment-comparison`, `label-comparison`, `leakage-comparison`, `p1-review-comparison`, `public-record-publisher`, `representation-builder`, `scan-comparison`, `semantic-judge-1`, `semantic-judge-2`, `simulation-builder`.

Only `control-root-authority` signs the exact registry through section 4.2. Verify the separately authenticated anchor first; then require signer role/key equality with the anchor, equality of the registry root entry, all 22 roles once in fixed order, and every recomputed key ID. Another signer, anchor, order, role set, duplicate key assignment, byte form, missing entry, or inactive/revoked entry rejects before E00G. Registry v1 has no rotation or revocation operation. Any key change requires a new version, independent review, and newly user-approved integration root. No private key is stored here or delivered by an edge.

### 4.2 One generic signed envelope

For any section-4 `record_bytes` explicitly governed by sections 4.1 and 4.3-4.6, define `record_sha256=SHA256(record_bytes)`. Inherited artifacts called “signed” outside those sections retain their inherited signing specifications. The only section-4 signature preimage is:

```text
URC-0.14-SIGNED-ARTIFACT\n
signer_role=<one exact active registry role ID>\n
signer_key_sha256=<that role's registry key ID>\n
record_length=<decimal byte length>\n
<exact record_bytes>
record_sha256=<64 lowercase hex>\n
```

Because `record_bytes` ends in LF, the next field starts immediately after that LF with no separator. Ed25519 signs exactly this preimage. The signed envelope is that preimage followed by:

```text
signature_algorithm=Ed25519\n
signature_hex=<128 lowercase hex>\n
```

Verification recomputes byte length, record hash, key ID, role assignment, and signature against the authenticated registry. No alternate JSON, field order, whitespace, length prefix, concatenation, hash, signature scope, or key is permitted.

### 4.3 Canonical status evidence receipts and registrar assembly

Every non-genesis status event arrives at the registrar as individual producer-signed evidence receipts. Exact receipt `record_bytes` are:

```text
evidence_receipt_schema=URC-0.14-STATUS-EVIDENCE-1\n
edge=<one exact edge in the table below>\n
producer_role=<the row's exact role ID>\n
artifact_kind=<the row's exact artifact kind>\n
artifact_sha256=<64 lowercase hex>\n
required_check_result=accepted\n
```

For artifact bytes, `artifact_sha256` is SHA-256 of exact accepted bytes. For a digest-only artifact, it copies the authenticated 64-hex value and never hashes the ASCII digest again. The table fixes counts, roles, kinds, and bundle order:

| Status edge | Receipt count | Ordered `(producer_role, artifact_kind)` entries |
|---|---:|---|
| E02 | 3 | `(simulation-builder, benchmark-summary)`, `(simulation-builder, audit-summary)`, `(simulation-builder, power-summary)` |
| E05 | 1 | `(content-intake, content-digest)` |
| E08 | 1 | `(label-comparison, equality-digest)` |
| E14 | 1 | `(representation-builder, equality-digest)` |
| E21 | 1 | `(scan-comparison, pass-reject-digest)` |
| E24 | 1 | `(leakage-comparison, pass-reject-digest)` |
| E25 | 2 | `(comparator-builder-1, implementation-mutation-table-digest)`, `(comparator-builder-2, implementation-mutation-table-digest)` |
| E27 | 1 | `(catalog-comparison, agreed-abstract-table-digest)` |
| E29 | 1 | `(catalog-comparison, agreed-instance-table-digest)` |
| E31 | 1 | `(p1-review-comparison, pass-reject-digest)` |
| E35 | 1 | `(analysis-map-comparison, agreed-map-digest)` |
| E48 | 1 | `(analysis, frozen-analysis-digest)` |
| E50 | 1 | `(final-decision-custodian, decision-record-digest)` |
| E56 | 1 | `(public-record-publisher, publication-receipt-envelope-digest)` |

Each listed producer sends its own signed receipt envelope separately to the registrar on the named edge. For E02 the simulation-builder sends three separate envelopes. For E25 builder 1 and builder 2 each send exactly its own envelope and are denied the other's receipt; neither constructs a bundle. The registrar verifies signer, signature, edge, role, kind, digest syntax, and result, then writes an exact immutable envelope copy into `registrar-receipt-vault` under key `(edge, producer_role, artifact_kind)`. Duplicate keys, replacement, extra receipt, or a receipt arriving after that edge's status pair freezes reject. Receipt arrival may occur before its status turn, but bundle construction is forbidden until every lower-bit status pair freezes and the complete row-specific receipt set exists.

For a non-genesis edge, the registrar alone constructs exact evidence-bundle bytes:

```text
evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n
edge=<exact non-genesis edge>\n
entry_count=<the table's exact decimal count>\n
```

Immediately after the header, for every integer `i` from 1 through `entry_count` in ascending order, emit `entry_<i>_envelope_length=<decimal byte length>\n` followed immediately by the immutable signed receipt-envelope bytes selected by table row and position. Angle-bracket notation is grammar notation and is not emitted; no ellipsis or separator is emitted. Each envelope ends in LF, the next entry field follows immediately, and the bundle ends at the final envelope's final LF. The registrar may select only the exact vault key fixed for that position and may not alter or resign a receipt. Define `event_evidence_bundle_sha256=SHA256(exact bundle bytes)`.

The one genesis ROOT bundle is instead exactly:

```text
evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n
edge=ROOT\n
entry_count=0\n
control_integration_manifest_sha256=<64 lowercase hex>\n
```

It has no entry or receipt and binds the authenticated CONTROL-integration manifest. It is constructed only after the user-approved integration root authenticates that manifest. No empty invented artifact, alternate ROOT schema, individual digest, ASCII digest rehash, unordered concatenation, omitted/extra receipt, or alternate container may substitute for either bundle form.

### 4.4 Closed registrar status machine

The status chain is a public custody-progress receipt, not an S0 or empirical-success claim. Bit order is exactly E02, E05, E08, E14, E21, E24, E25, E27, E29, E31, E35, E48, E50, and E56 at bits 0 through 13.

The only states are `A-0000`, `A-0001`, `A-0003`, `A-0007`, `A-000f`, `A-001f`, `A-003f`, `A-007f`, `A-00ff`, `A-01ff`, `A-03ff`, `A-07ff`, `A-0fff`, `A-1fff`, and `A-3fff`. `A` means only that the registrar authenticated the exact bundle/receipts and required checks; it never means an empirical claim, representation superiority, or S0 passed.

Unsigned status `record_bytes` are:

```text
status_schema=URC-0.14-STATUS-1\n
sequence=<decimal 0..14>\n
previous_record_sha256=<64 lowercase hex>\n
event_edge=<ROOT|E02|E05|E08|E14|E21|E24|E25|E27|E29|E31|E35|E48|E50|E56>\n
event_commitment_sha256=<64 lowercase hex>\n
evidence_mask=<exact four lowercase hex>\n
status_code=A-<same exact four lowercase hex>\n
monotonic_timestamp_ns=<decimal integer>\n
```

Genesis has sequence 0, 64 zeroes as previous digest, event `ROOT`, SHA-256 of the exact section-4.3 ROOT bundle as event commitment, mask `0000`, and status `A-0000`. For sequence `n` from 1 through 14, event is bit `n-1`, previous digest is SHA-256 of the preceding exact status record, event commitment is SHA-256 of the exact companion non-genesis bundle, mask sets bits 0 through `n-1`, status is `A-` plus that mask, and timestamp strictly increases. No edge repeats, skips, arrives out of order as a transition, clears a bit, or selects another state.

E51 atomically appends exactly one signed status envelope and its exact companion bundle for every sequence including genesis. Partial or duplicate writes reject. Thus the store has one uniform pair-write rule and ROOT is a canonical zero-receipt companion rather than an exception. E52 delivers all stored pairs from genesis through the requested digest. The public reader authenticates root/registry, checks the ROOT manifest binding, verifies every later receipt and registrar signature, recomputes bundle/status hashes, and checks count, order, sequence, edge, prefix mask, state, and time. This verifies the public receipt chain and commitments, not protected payload truth.

### 4.5 Recipient-verifiable E43 and E45 comparisons

Each judge E42 output and comparator-operator E44 output is a section-4.2 signed envelope. Its length-delimited `record_bytes` are exact canonical table payload and contain no signer identity; signer role/signature are only in the envelope. Two roles must independently produce byte-identical record bytes although their envelopes differ.

E43 comparison `record_bytes` are:

```text
comparison_schema=URC-0.14-COMPARISON-1\n
edge=E43\n
left_role=semantic-judge-1\n
left_envelope_sha256=<SHA-256 of exact left signed envelope>\n
left_record_sha256=<SHA-256 of exact left record_bytes>\n
right_role=semantic-judge-2\n
right_envelope_sha256=<SHA-256 of exact right signed envelope>\n
right_record_sha256=<SHA-256 of exact right record_bytes>\n
agreed_record_sha256=<same exact common record_bytes SHA-256>\n
comparison_result=equal\n
```

E45 comparison `record_bytes` use the same fields with `edge=E45` and fixed roles `comparator-operator-1` and `comparator-operator-2`.

For each edge, the comparison custodian authenticates both envelopes, extracts each exact record, recomputes envelope/record hashes, and requires byte-identical records. It signs the comparison record through section 4.2; `comparison_digest` is SHA-256 of exact comparison record bytes. E43/E45 deliver in order the exact left source envelope, exact right source envelope, signed comparison envelope, named comparison digest, and agreed record bytes. Every recipient repeats all signature, extraction, hash, role, and byte-equality checks. Unequal records, bad signatures, wrong roles, envelope/record substitution, swaps, alternate extraction, or custodian-only attestation reject.

### 4.6 Unique public publication receipt

The publisher copies the E53 decision record byte-for-byte into `public-decision-store`. Publication-receipt `record_bytes` are:

```text
publication_schema=URC-0.14-PUBLICATION-1\n
publisher_role=public-record-publisher\n
source_edge=E53\n
source_record_sha256=<E53 decision record SHA-256>\n
published_store=public-decision-store\n
published_record_sha256=<stored decision record SHA-256>\n
publication_result=byte-identical\n
monotonic_timestamp_ns=<decimal integer>\n
```

The two hashes must equal. The publisher signs through section 4.2 and E54 atomically stores exact record plus receipt. E55 delivers both unchanged. E56 sends SHA-256 of the exact receipt envelope plus the publisher's signed E56 evidence receipt to registrar. Changed bytes, unequal digest, invalid key/signature, partial write, or second publication stops and produces no accepted E56 receipt.

## 5. Closed matrix-ledger bijection

### 5.1 Exact public grants and operational edges

E00A-H remain eight public-specification grants. E01-E56 remain exactly 56 operational edge types. An edge row may explicitly split protected payload and public receipt recipients; omission remains denial. Registrar receipt-vault writes are the registrar-side terminal action of the named incoming evidence edge, not a new edge.

| Edge | Producer | Artifact | Recipient/store | Required check |
|---|---|---|---|---|
| E00A | registrar | authoring protocol, constraints, selected N | fact author | exact reviewed public bytes/hashes |
| E00B | registrar | frozen contract and label specification | label A/B | byte-identical signed grant |
| E00C | registrar | transformation, runner-allowlist, scanner, leakage-review specifications | representation builder, package builder/scanner 1, scanner 2, leakage reviewers as applicable | recipient-specific signed manifest |
| E00D | registrar | metadata, ID-order, semantic-atom, strength, cause, mutation, comparator, catalog specifications | comparator builders, generators, P1 reviewers, comparator operators as applicable | exact reviewed public bytes/hashes |
| E00E | registrar | A-D identity, bank-hash, schedule, P2-P4 map/formula specifications | condition-map custodian, blinded-map builders as applicable | exact reviewed public bytes/hashes |
| E00F | registrar | semantic-reason rubric | judges | byte-identical signed grant |
| E00G | registrar | authenticated integration decision/manifest hash, root/registry, and common-resource, transport, anonymization, custody/signing/publication specifications | section-4 signers/verifiers and dispatcher/executor/raw custodian as applicable | user-approved integration commit first; role grant; no private keys |
| E00H | registrar | frozen statistical decision table and formula identity | analysis, final-decision custodian | no selected constants or results |
| E01 | registrar | frozen statistical/catalog specifications and pre-bank manifest | simulation builder | full signed public bytes, role grant, hashes |
| E02 | simulation builder | three summary digests and three separately signed receipts | registrar, which writes verified receipt envelopes to `registrar-receipt-vault` | exact three roles/kinds and no semantic content |
| E03 | simulation builder | selected calibrated constants and public formula manifest | `analysis-input-vault` | signed exact bytes before calls |
| E04 | fact author | frozen bank/prompts and signature | content-intake custodian, which verifies/writes `content-vault` | selected N and content hash |
| E05 | content intake | content digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | no content bytes; exact role/kind/signature |
| E06 | `content-vault` | exact content copies | label A, label B, representation builder | recipient manifests |
| E07 | label A/B | signed bundles | own label vault; label comparison only reader | separate ACLs |
| E08 | label comparison | equality digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | no label contents; exact role/kind/signature |
| E09 | label comparison | exact agreed bundle | `agreed-label-vault` | byte equality only |
| E10 | `agreed-label-vault` | agreed bundle | generators | phase grant after equality |
| E11 | `agreed-label-vault` | agreed bundle | leakage reviewers | package-review phase grant |
| E12 | `agreed-label-vault` | agreed bundle | judges, comparator operators | adjudication phase grant |
| E13 | representation builder | exact representations/equality manifest | `representation-vault`; package builder and condition-map custodian read | canonical equality |
| E14 | representation builder | equality digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | no representation content; exact role/kind/signature |
| E15 | `representation-vault` | assigned representation/questions | package builder | signed assignment |
| E16 | package builder | completed signed packages | `signed-package-vault` | package/hash manifest |
| E17 | package builder/scanner 1 | scan-1 table | `scan-vault-1` | scanner-1 signature |
| E18 | `signed-package-vault` | completed package | scanner 2 | no scan-1 access |
| E19 | scanner 2 | scan-2 table | `scan-vault-2` | scanner-2 signature |
| E20 | both scan vaults | both scan tables | scan comparison | exact inventory/scan comparison |
| E21 | scan comparison | pass/reject digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | exact role/kind/signature |
| E22 | `signed-package-vault` | signed package | leakage reviewers | separate from label grant E11 |
| E23 | leakage reviewers | signed tables | own leakage vault; comparison only reader | separate ACLs |
| E24 | leakage comparison | pass/reject digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | exact role/kind/signature |
| E25 | comparator builder 1 / comparator builder 2 | each exact implementation/mutation-table bytes+digest to own vault; each own signed receipt separately to registrar | `comparator-vault-1` / `comparator-vault-2` respectively; registrar writes each verified receipt copy to `registrar-receipt-vault` | no cross-builder transfer; both payloads available to own operators; fixed receipt keys |
| E26 | generators | abstract tables | own generator vault; catalog comparison only reader | frozen generator/spec hashes |
| E27 | catalog comparison | exact agreed abstract table/rejection summary to `catalog-vault`; signed digest receipt separately to registrar | catalog vault; registrar writes verified receipt copy to `registrar-receipt-vault` | byte equality; split protected payload/public receipt |
| E28 | generators | bank-instance tables | own generator vault; catalog comparison only reader | agreed labels through E10 only |
| E29 | catalog comparison | exact agreed instance table/rejection summary to `catalog-vault`; signed digest receipt separately to registrar | catalog vault; registrar writes verified receipt copy to `registrar-receipt-vault` | byte equality; split protected payload/public receipt |
| E30 | P1 reviewers | signed reviews | own P1-review vault; comparison only reader | separate ACLs |
| E31 | P1-review comparison | pass/reject digest and signed receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | exact role/kind/signature |
| E32 | `signed-package-vault` | finalized packages/hashes | condition-map custodian | scan/leakage-passed hashes only |
| E33 | condition-map custodian | semantic condition/schedule map | `condition-map-vault`; blinded-map builders pre-call readers | pre-call freeze/separate grants |
| E34 | blinded-map builders | blinded maps | analysis-map comparison | independent builds |
| E35 | analysis-map comparison | exact agreed blinded-map bytes to `analysis-map-vault`; signed digest receipt separately to registrar | analysis map vault; registrar writes verified receipt copy to `registrar-receipt-vault` | byte equality; split protected payload/public receipt |
| E36 | condition-map custodian | opaque schedule/routing plus assigned signed package | dispatcher; routing copy to raw custodian | balance/package-hash match |
| E37 | dispatcher | signed request/package | executor | pre-send timestamp |
| E38 | executor | first raw response stream | dispatcher | no retry/read-back |
| E39 | dispatcher | raw response plus run log/endpoints | `raw-output-vault` | durable-final-byte timestamp/hash |
| E40 | raw custodian | anonymous semantic bundle | judges, comparator operators | identity stripping/raw link |
| E41 | raw custodian | anonymous timing/byte table | analysis | no semantic names |
| E42 | judges | own signed canonical judgment-table envelope | own judgment vault; judgment comparison only reader | source signatures/roles/canonical records |
| E43 | judgment comparison | two source envelopes, signed comparison envelope/digest, agreed semantic record | comparator operators | every section-4.5 recomputation succeeds |
| E44 | comparator operators | own signed canonical derived-table envelope | adjudication comparison | source signatures/roles/canonical records |
| E45 | adjudication comparison | two source envelopes, signed comparison envelope/digest, agreed derived record | analysis | every section-4.5 recomputation succeeds |
| E46 | `analysis-input-vault` | constants and public formula manifest | analysis | exact pre-call hashes |
| E47 | `analysis-map-vault` | exact blinded coefficient/stratum map bytes and digest | analysis | bytes/digest equal E35 stored payload |
| E48 | analysis | exact frozen anonymous statistics/decision-input bytes+hash to final-decision custodian; signed digest receipt separately to registrar | final-decision custodian; registrar writes verified receipt copy to `registrar-receipt-vault` | split protected payload/public receipt; semantic map withheld |
| E49 | `condition-map-vault` | semantic condition map | final-decision custodian | only after authenticated E48 receipt/status commitment |
| E50 | final-decision custodian | exact mechanical join/decision record to `final-decision-vault`; signed digest receipt separately to registrar | final decision vault; registrar writes verified receipt copy to `registrar-receipt-vault` | no reanalysis/threshold change; atomic payload store |
| E51 | registrar | signed status envelope plus exact companion bundle | `registrar-store` | atomic pair for ROOT and all 14 evidence states; exact sections 4.3-4.4 |
| E52 | `registrar-store` | exact envelope/bundle chain from genesis | public status reader | root/registry/receipts/bundles/status invariants verify |
| E53 | `final-decision-vault` | exact decision record and digest | public record publisher | E50 digest/bytes match; no other vault access |
| E54 | public record publisher | byte-identical decision record and signed publication receipt | `public-decision-store` | exact section-4.6 atomic write/equality/signature |
| E55 | `public-decision-store` | exact decision record and signed publication receipt | public record reader | root/registry/hashes/equality/signature verify |
| E56 | public record publisher | publication-receipt envelope digest and signed evidence receipt | registrar, which writes verified receipt copy to `registrar-receipt-vault` | no decision bytes; exact role/kind/signature |

### 5.2 Role-to-edge index

Every positive matrix input and only output/store maps to these edges. Store-mediated reads/writes use section-3 IDs. The user-approved root commit is the sole registry trust input and is not experimental evidence.

| Role | Inbound edges | Outbound edges |
|---|---|---|
| registrar | reviewed public roots; E02,E05,E08,E14,E21,E24,E25,E27,E29,E31,E35,E48,E50,E56 | E00A-E00H,E01,E51 |
| public status reader | E00G,E52 | none |
| public record publisher | E00G,E53 | E54,E56 |
| public record reader | E00G,E55 | none |
| content intake | E04,E00G | E04,E05,E06 |
| simulation builder | E01,E00G | E02,E03,E46 |
| fact author | E00A | E04 |
| label A/B | E00B,E06 | E07 |
| label comparison | E00G,E07 | E08-E12 |
| representation builder | E00C,E00G,E06 | E13-E15 |
| package builder/scanner 1 | E00C,E15 | E16-E18,E20,E22,E32 |
| scanner 2 | E00C,E18 | E19,E20 |
| scan comparison | E00G,E20 | E21 |
| leakage reviewers | E00C,E11,E22 | E23 |
| leakage comparison | E00G,E23 | E24 |
| comparator builders | E00D,E00G | E25 |
| generators | E00D,E10 | E26,E28 |
| catalog comparison | E00G,E26,E28 | E27,E29 |
| P1 reviewers | E00D,E27,E29 | E30 |
| P1-review comparison | E00G,E30 | E31 |
| condition-map custodian | E00E,E13,E32 | E33,E36,E49 |
| blinded-map builders | E00E,E33 | E34 |
| analysis-map comparison | E00G,E34 | E35,E47 |
| dispatcher | E00G,E36,E38 | E37,E39 |
| executor | E00G,E37 | E38 |
| raw custodian | E00G,E36,E39 | E40,E41 |
| judges | E00F,E00G,E12,E40 | E42 |
| judgment comparison | E00G,E42 | E43 |
| comparator operators | E00D,E00G,E12,E25,E29,E40,E43 | E44 |
| adjudication comparison | E00G,E44 | E45 |
| analysis | E00G,E00H,E41,E45,E46,E47 | E48 |
| final-decision custodian | E00G,E00H,E48,E49 | E50 |

The root authority has no experimental edge and is outside this 32-row experimental index; its sole act is the pre-run registry signature authenticated through a later user-approved Git integration root. E51 is the only registrar-store write and E52 its only read. Receipt-vault copies contain only signed public receipt envelopes, never protected payloads. No output may be dropped, ambiently copied, reformatted, or reconstructed by an unlisted recipient.

## 6. Current bank balance and freeze sequence

The candidate sequence is `N = 240, 336, 432, 528, 624, 720`. Every value is divisible by 24, 12, and 8. Selected N freezes before fact authoring and cannot later decrease.

For every accepted bank:

- each of the 24 globally admissible rows has exactly `N/24` questions;
- no development example, development-example ID, or development-example content hash appears in the bank;
- no two questions are exact duplicates or noun-, entity-, identifier-, or number-swapped duplicates with the same relation/predicate/operation/answer skeleton; and
- a public duplicate-key specification and development-example denylist freeze before authoring, and any matching key or denylist entry rejects the untouched bank.

The only freeze sequence is:

1. Freeze the v0.14 design triplet (`universal-response-contract-v0.14-candidate.md`, `public-falsification-plan-v0.11.md`, and `review-response-v0.9.md`) and their same-basename sidecars, then obtain a fresh independent review of exactly those design inputs; only review verdict `PASS-FOR-CONTROL-INTEGRATION-ONLY` may satisfy this step. The review record is an output of this step, not one of its own inputs.
2. Freeze the 31-slot contract and 25-slot plan constructions, authoring/metadata/ID-order specifications, duplicate-key specification and denylist, 921,600-row abstract catalog, 1,792-row availability catalog, 407-row cause-key catalog, generators, statistics, roles, stores, edges, receipt/bundle grammars, root/registry acceptance, ceilings, and N sequence.
3. Freeze the pre-bank power manifest and benchmark environment.
4. Benchmark simulation plus two generations/comparisons of every catalog and the maximum 2,949,120-row bank-instance projection.
5. Stop if CPU, RAM, storage, calendar, human, signing, or monetary projections exceed inherited ceilings.
6. Fit/audit null boundaries, run power, and select the first sufficient N.
7. Author the untouched bank; enforce exact 24-row balance, development-example exclusion, and duplicate-key rejection before labels.
8. Label independently; reject the whole bank on any byte difference.
9. Generate the instance projection once with frozen generators; compare and obtain both P1 signatures.
10. Freeze representations, packages, scanners, comparators, maps, schedules, constants, public formula manifest, exact model revision, and cost preflight.
11. Run P0-P2; run P3-P4 only after earlier passes.
12. Freeze judgments, derived tables, and anonymous analysis payload/hash before semantic-map release and mechanical final join.

Nothing is dropped, edited, relabeled, replaced, or selectively rerun after labels or confirmatory output are visible. Rejected abstract rows remain in the 921,600-row product and resource benchmark.

## 7. Replacement P0 and P1 requirements

P0 retains every authenticated predecessor pass and additionally requires exact agreement on:

- the 31-slot contract and 25-slot plan constructions, source inventories, transforms, and effective hashes;
- the byte-identical U11 semantic slice and every semantic-atom, strength, permission, cause, selector, consumption, response, and P3 consequence;
- eight E00 grants, exactly E01-E56, 27 literal stores, and 32 matrix/index rows;
- one authenticated root, exact 22-entry registry, root-only signature, and role/key IDs;
- exact protected-payload versus public-receipt split on E25, E27, E29, E35, E48, and E50;
- every receipt grammar, exact 14-edge count/role/kind table, immutable receipt-vault key, registrar-only assembly, E02 count three, E25 two independent deliveries, and all other counts one;
- exact zero-receipt ROOT bundle, atomic E51 pairs for all 15 states, commitments, masks, sequences, previous hashes, and timestamps;
- E42/E44 source signatures, exact extraction, E43/E45 envelope/record hashes, delivery, and recipient recomputation;
- E53-E56 publication; and
- the v0.14-specific only freeze sequence.

P1 retains inherited semantic/order mutations and adds: protected-payload omission; payload delivery to registrar; receipt used as executable payload; receipt-vault duplicate/replacement/wrong key; unauthorized registrar receipt edit; bundle construction before lower-bit freeze; E25 one receipt missing, both receipts from one role, builder-to-builder transfer, or builder-assembled bundle; wrong ROOT manifest hash, nonzero ROOT entry count, genesis without bundle, invented empty bundle, or partial E51 pair; E35 map digest without bytes; E48 digest without anonymous analysis payload; stale package version in freeze step; plus every anchor/registry, bundle framing, signature, E43/E45, and publication mutation inherited from v0.13. Every mutation rejects independently. Two expected generators, two P1 reviewers, and both comparators must agree exactly; identically wrong agreement is failure.

## 8. Equality, stopping, rollback, and claim limit

Inherited A-D equality and noncompensatory P0-P4 stops remain. Additional stops are an incomplete effective map, effective-hash difference, transform mismatch, semantic regression, noncanonical ID/cause order, incorrect catalog count, unbalanced row, development-example reuse, duplicate key, unmatched role/edge/store/reader, protected-payload omission or registrar exposure, receipt-vault mismatch, unauthorized bundle assembly, invalid ROOT/genesis pair, invalid receipt/bundle/status transition, unauthenticated root, changed registry, invalid signature/key, E43/E45 mismatch, unauthorized publication, changed decision bytes, invalid publication receipt, stale freeze version, premature semantic-map release, or post-map reanalysis.

No predecessor is edited in place. Any failure returns to authenticated public protocol/review evidence and requires a separately gated successor on untouched material. No finding can be waived by agreement, and no failed package can be relabeled as passed.

A future independent proposal-text pass would authorize at most CONTROL consideration of this public contract/plan. It would not authorize key generation, schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, model execution, scoring, sealed access, or S0 execution. Even a later completed public experiment could support only its frozen synthetic scope, not S0 generally, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.
