# URC-0.13 independent hostile public-only review

- Review type: `fresh independent hostile public-only design review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `b9b1a0edbd269a5c1c004220ca2a6029dfad47e7`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.13 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, key generation, model call, scoring, executor work, sealed access, S0 execution, branch change, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** Before substantive reading, the required origin, branch, HEAD, and clean worktree matched exactly. All eighteen allowlisted Markdown files were read in full and no other substantive repository file was inspected. The seventeen required same-basename sidecars each matched its Markdown bytes. `AGENTS.md` has no expected sidecar; its independently computed digest is recorded below.

| Exact input | Verified SHA-256 | Authentication |
|---|---|---|
| `AGENTS.md` | `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d` | computed; no sidecar expected |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matching sidecar |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/public-falsification-plan-v0.6.md` | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/universal-response-contract-v0.10-candidate.md` | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/public-falsification-plan-v0.7.md` | `07edb8ec3044874f39ed60f1a6952eb64e369715fc1501fd309888c9b24d09dd` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/universal-response-contract-v0.11-candidate.md` | `ae4620c1b532906538252ed503cf39211c46371d4e1eebdbe9a5ef5136528807` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/universal-response-contract-v0.12-candidate.md` | `c536e0d8316c432cdc14d70c8de7c7505f4ad7e675652246c78658720c6c5de4` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/public-falsification-plan-v0.9.md` | `c651de01e2f7420fe54692e6c69862a7224ff08bd517a96a800bf48cab77a5f8` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/review-response-v0.7.md` | `447b37d6d2266286ceea28f1abc173254edfd5bdca7cb72cce10da49c6b02c2e` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.12/urc-v0.12-independent-review-v0.1.md` | `626c07dad70f6943146974c2c2f19c9998a752b61e429570d78ffe231bfb66dc` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/universal-response-contract-v0.13-candidate.md` | `994ad92b48bdf5d5bd779a6b2fd13a7bbc13bbfd4420beb7066a26910f7e849c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/public-falsification-plan-v0.10.md` | `6e82b1586df4fcb4a2c12bae9519ca1a9073ccbdb5ba4fcc33f8d789e3b15973` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/review-response-v0.8.md` | `4cf728bce26030c6c41b8d7431c27407ad24e88ae9ef1639ca30cc0fa01efc36` | matching sidecar |

No repository-wide search, E0 artifact, sealed/private/oracle material, fixture, schema, runner, implementation, output, web source, or external source was used. Sidecars were treated only as authentication metadata. Worktree separation was treated as edit isolation, not secret isolation.

## 2. Review rubric

- **PASS**: the authenticated proposal text uniquely determines the reviewed result without a result-affecting author, builder, signer, comparator, custodian, registrar, publisher, reader, analyst, or unlisted transport choice. This does not mean implemented or validated.
- **FAIL**: a contradiction, missing normative definition, unsatisfied precondition, omitted required payload, missing authorized writer or transfer, unverifiable required check, incomplete ACL route, or executable counterexample remains.
- **UNCLEAR**: materially different conforming constructions or workflows remain possible and the allowlisted text does not select one.

Finding severities are:

- **blocking**: prevents unique effective-document construction or a mandatory P0/P1 expected result;
- **major**: materially breaks custody, cryptographic trust, blinding, reproducibility, fairness, or feasibility; and
- **minor**: a localized precision defect that must be corrected before freeze.

## 3. Independent effective-document reconstruction

### 3.1 Thirty-one-slot contract

**PASS for byte construction.** U7, U9, U10, U11, and U13 authenticate. Every exact heading resolves once; all full and preamble ranges satisfy the published level and order rules; every effective v0.12 slot is classified once; and U11 section 4 enters unchanged as slot 21. Contract records have no transform fields.

The exact source run is: slots 1-5 U13; 6-14 U7; 15-19 U9; 20 U10; 21 U11; 22-25 U9; 26-30 U7; and 31 U13. Preamble slots are 2, 6, 12, 17, 23, and 26. Slot 25 is the consecutive U9 sections 8.2-8.5 full range.

Independent strict-UTF-8, raw-LF-preserving reconstruction produced:

```text
effective_contract_slots=31
effective_contract_raw_slice_bytes=34060
effective_contract_transformed_slice_bytes=34060
effective_contract_stream_bytes=43593
effective_contract_sha256=9e73c09649dabc1eae9bb2de38f254dc3d4e5b70c84b7c3ff844a3c58afaf372
```

### 3.2 Twenty-five-slot plan

**PASS for byte construction.** P4, P5, P6, P7, and P10 authenticate. P9 is evidence only. All 25 slots resolve and are classified once. Preamble slots are 12, 17, and 21. The authenticated raw P5 section 8 slice is 721 bytes and contains exactly one ASCII `v0.8` and one ASCII `URC-0.8`. The two ordered count-one transforms produce a 723-byte slot.

The exact source sequence is: P10, P4, P5, P10, P10, P5, P7, P10, P4, P5, P4, P4, P4, P4, P4, P5, P4, P4, P4, P6, P4, P4, P5, P4, P10.

Independent reconstruction produced:

```text
effective_plan_slots=25
effective_plan_raw_slice_bytes=69774
effective_plan_transformed_slice_bytes=69776
effective_plan_stream_bytes=78122
effective_plan_sha256=ed34f6941a75a9923c3be35df19832b1d5ec9b4a764b429e78bb756ee4b95411
```

These are independent in-memory construction-test results. They are not implementations, frozen manifests, simulations, cryptographic executions, or empirical results. The author response did not supply these values as expected answers.

## 4. Required predecessor-finding dispositions

| Finding | Decision | Independent v0.13 assessment |
|---|---|---|
| V12-M01 — status evidence does not uniquely bind plural or digest-only edge artifacts | **PARTIAL PASS; OVERALL FAIL** | The exact receipt grammar, copied-digest rule, E02/E25 counts, role/kind order, length-delimited bundle, bundle hash, and status commitment close the predecessor's byte-choice counterexample. Closure is still incomplete because the pair-only store has no genesis write and E25 has no uniquely authorized two-producer bundle assembler/delivery. See V13-M02 and V13-M03. |
| V12-M02 — key registry lacks canonical bytes and a noncircular trust root | **PASS AT PROPOSAL-TEXT LEVEL** | The anchor grammar, user-approved exact Git commit and anchor hash, 22-entry fixed-order registry, root-only signer, anchored-key equality, registry envelope, and substitution/review rules select one public acceptance path. The external root is expressly a pre-run trust input, not an experimental role or evidence edge. Key creation, custody, integration, and feasibility remain unopened. |
| V12-M03 — E43/E45 recipients cannot recompute source hashes and equality | **PASS AT PROPOSAL-TEXT LEVEL** | E42/E44 now produce role-signed envelopes whose length-delimited records are identity-free canonical table payloads. E43/E45 separately bind envelope and record hashes, deliver both source envelopes plus the comparison envelope/digest and agreed record, and require every recipient to authenticate, extract, hash, and byte-compare them. |

There is no new blocking finding. Three major and one minor finding prevent CONTROL integration.

## 5. Canonical evidence, root, comparison, and publication audit

### 5.1 Evidence receipts, bundles, and status

| Required attack | Result | Assessment |
|---|---|---|
| receipt bytes | **PASS** | Edge, producer role, artifact kind, artifact digest, and accepted result have one ASCII/LF grammar and one role-bound signature. |
| digest copy versus double hash | **PASS** | Digest-only payloads copy the authenticated 64-hex value into `artifact_sha256`; hashing its ASCII representation is expressly rejected. |
| E02 plurality | **PASS FOR BYTES AND ORDER** | Three simulation-builder receipts are fixed as benchmark, audit, and power in that order. One producer can possess all three. |
| E25 plurality | **PASS FOR BYTES; FAIL FOR CUSTODY** | The two builder roles and order are fixed, so bundle bytes are unique once both envelopes exist. No role or edge uniquely assembles and delivers that two-producer bundle. See V13-M03. |
| bundle framing | **PASS** | Fixed entry count plus per-envelope decimal byte length yields one parse; no separator, alternate container, omission, duplicate, or reorder is accepted. |
| status commitment | **PASS** | Each non-genesis status record commits to SHA-256 of its exact companion bundle, not an individual carried digest. |
| transition and masks | **PASS** | The 14 status edges, 15 prefix states through `A-3fff`, sequence, prior-record hash, mask, status, and increasing timestamp remain deterministic. |
| E51 atomicity | **FAIL AT GENESIS** | E51 and `registrar-store` allow pair writes only, while genesis expressly has no bundle. See V13-M02. |
| E52 public verification | **PASS CONDITIONALLY** | Given a valid genesis and later pairs, the reader has the anchor, registry, receipts, bundles, and status envelopes needed to recompute the public chain. V13-M02 prevents instantiation of that precondition. |

### 5.2 CONTROL root and registry

| Required attack | Result | Assessment |
|---|---|---|
| external anchor | **PASS AS A FUTURE GATE INPUT** | Trust starts from a later user-approved exact commit identity and anchor hash, not from a key found only inside the registry. |
| anchor bytes | **PASS** | Schema, root role, 32-byte public key, and raw-key SHA-256 key ID have one grammar without commit self-reference. |
| registry bytes and order | **PASS** | The version, anchor hash, count 22, numbered role/key/key-ID/active blocks, and ASCII role order are exact. Local inventory found 22 unique ordered roles. |
| registry signer | **PASS** | Only the anchored `control-root-authority` key may sign; the registry root entry must equal the anchor key. |
| substitution and rotation | **PASS** | Commit, anchor, signer, role, order, key, duplicate, status, and byte-form changes reject. Registry v1 has no silent rotation or revocation path. |
| external-root topology | **PASS WITH BOUNDED SCOPE** | The authority's only stated act is signing the public pre-run registry later bound by a user-approved integration commit. It has no experimental input or edge and is denied bank, label, package, output, map, and sealed material. Treating that user-approved trust decision as an external root does not add a hidden experimental transfer. It does not implement key custody. |

### 5.3 E42-E45 comparison verification

| Required attack | Result | Assessment |
|---|---|---|
| source envelope | **PASS** | E42/E44 outputs use the generic length-delimited envelope with fixed signer role and registry key. |
| payload extraction | **PASS** | `record_length` selects exact payload bytes; signer identity remains outside the record so independent payloads can be byte-identical while envelopes differ. |
| envelope versus record hash | **PASS** | Comparison records name both scopes separately for each side, and recipients recompute both. |
| left/right roles | **PASS** | Judge 1/2 and operator 1/2 are fixed and swaps reject. |
| equality | **PASS** | The custodian and every recipient compare the two extracted records byte-for-byte and require the agreed record and all three record hashes to match. |
| recipient delivery | **PASS** | E43 sends the full five-artifact set to both comparator operators; E45 sends its full set to analysis. These recipients no longer rely on a custodian-only attestation. |

### 5.4 Public decision publication

The v0.12 E53-E56 publisher, terminal reader, stores, byte-equality receipt, atomic publication, and digest return remain intact. V0.13 additionally gives E56 a publisher-signed canonical evidence receipt. Public readers can authenticate the root/registry and recompute the decision and receipt hashes. No decision bytes reach the registrar. Operational atomicity and durable delivery remain unimplemented feasibility questions.

## 6. New findings

### V13-M01 — Receipt additions delete mandatory payloads from E25, E35, and E48

- Severity: **major**
- Fact: the role matrix says each comparator builder writes its implementation/mutation table in its own comparator vault. The only corresponding edge is E25, whose artifact is only the implementation/mutation-table digest plus a signed receipt. Comparator operators later cite E25 as their comparator input.
- Fact: the role matrix says analysis-map comparison writes the agreed blinded map in `analysis-map-vault`. E35 carries only an agreed-map digest plus a signed receipt, while E47 must later deliver the actual blinded coefficient/stratum map to analysis.
- Fact: the analysis role's output is the frozen anonymous P2-P4 statistics/decision inputs/hash, and final decision requires the frozen anonymous analysis. E48 carries only a frozen-analysis digest plus a signed receipt to the registrar and final-decision custodian.
- Executable design counterexample: perform each edge literally. After E25, a comparator vault contains only a digest and receipt, so the operator cannot execute the assigned comparator. After E35, `analysis-map-vault` contains no map bytes, so E47 cannot deliver them. After E48, final decision has only a digest and cannot mechanically join anonymous statistics with the condition map. Supplying the omitted bytes instead uses an artifact not named by the edge and breaks the claimed matrix/ledger bijection.
- Consequence: three mandatory downstream consumers cannot operate under the written positive-input graph. This is not merely a status-receipt issue; the redesign has replaced protected payload transfer with evidence about the payload.
- Minimum correction proposal: restore each underlying payload and add the signed receipt alongside it. E25 must place the implementation/table bytes in each comparator vault while sending only the receipt/bundle to the registrar; E35 must place the agreed map bytes in `analysis-map-vault`; and E48 must deliver the frozen anonymous statistics/decision inputs to final decision while exposing only the canonical receipt/bundle to the registrar. Reflect each split recipient and artifact explicitly in matrix, store, edge, and index text.

### V13-M02 — The pair-only registrar store has no authorized genesis write

- Severity: **major**
- Fact: `registrar-store` has one writer, the registrar, through atomic E51 pair writes only.
- Fact: E51 writes one signed status envelope plus its exact companion evidence bundle; partial writes reject.
- Fact: genesis expressly has no evidence bundle. E52 nevertheless must deliver genesis followed by the stored envelope/bundle pairs.
- Executable design counterexample: start with the empty store. Writing genesis alone violates the pair-only E51/store rule. Pairing it with an empty or invented ROOT bundle violates the rule that genesis has no bundle and the 14-edge receipt table, which has no ROOT entry. No other writer or edge can create genesis.
- Consequence: the public status chain cannot be instantiated, so E52's verification precondition and the 15-record chain do not exist under the authorized topology.
- Minimum correction proposal: define one explicit atomic genesis-envelope-only E51 variant and store rule, or define an exact canonical zero-entry ROOT bundle and make genesis a normal committed pair. Update E51, E52, store, status, and P1 mutation text consistently.

### V13-M03 — E25's two-producer evidence bundle has no authorized assembler or transfer

- Severity: **major**
- Fact: E25 has two mutually isolated producers, each authorized to create only its own digest and signed receipt.
- Fact: the ledger says the registrar receives an already formed fixed-order two-entry bundle, and section 4.4 says a status-source bundle is sent to the registrar only after lower-bit pairs freeze.
- Fact: no builder may receive the other builder's output, no comparison/bundle custodian is named, and no row states that the registrar receives the two receipts separately and deterministically constructs the bundle.
- Executable design counterexample: builder 1 cannot create the bundle without builder 2's envelope, and builder 2 cannot create it without builder 1's. A transport aggregator or registrar-side assembler can make the bytes, but each is an extra role action or transfer not selected by the published graph. E02 does not have this problem because one simulation-builder role owns all three receipts.
- Consequence: although the bundle byte grammar and entry order are closed, the E25 custody path still requires an unlisted assembler or a different edge interpretation. The claimed role/store/edge bijection is incomplete at the exact plural case that motivated V12-M01.
- Minimum correction proposal: state that E25 delivers two separate fixed-role receipt envelopes to the registrar and authorize the registrar to construct the exact bundle after both verify, or add one deterministic bundle custodian with explicit input/output edges and denylist. Do not require isolated builders to jointly emit one artifact.

### V13-m01 — The inherited only freeze sequence still names the v0.10 package

- Severity: **minor**
- Fact: effective plan slot 7 is exact P7 section 5. Its first step says to obtain fresh independent review of the `v0.10` package, while the effective document is v0.13.
- Fact: P10 section 7 separately requires a future independent proposal-text pass before CONTROL consideration, so the stale token does not by itself authorize implementation or execution.
- Executable design counterexample: a schedule checker evaluating only the declared “only freeze sequence” can mark step 1 complete from the historical v0.10 review even though that step does not identify this v0.13 review.
- Consequence: the package version in the normative schedule is inaccurate and the current review is not represented at the schedule step where a reviewer would expect it.
- Minimum correction proposal: replace the retained schedule slice or apply an exact reviewed transform so step 1 names v0.13, while retaining the separate CONTROL-integration-only ceiling.

## 7. Complete topology and inventory audit

Independent parsing found eight E00 grants, exactly one row for every E01-E56 edge type, 26 unique store IDs, 32 role-matrix rows, and 32 role-index rows. It also found 22 registry roles, 14 status edges, and 17 total evidence receipts: E02 has three, E25 has two, and each remaining edge has one.

Those cardinalities are facts about the text, not proof of topology completeness. V13-M01 shows three matrix-output/edge-payload mismatches, V13-M02 shows a store writer state with no admissible genesis operation, and V13-M03 shows a plural artifact with no selected assembler. Apart from those findings, signer roles used by section 4 have registry entries, E43/E45 source envelopes use direct authorized forwarding rather than ambient stores, and the public publication roles remain present in matrix and index.

The external root authority does not create an unmodeled experimental role under the proposal's stated boundary: it is an explicit user-approved pre-run trust input with one public signing act and no experimental data. This conclusion is limited to proposal topology. The actual key-generation, private-key custody, Git publication, and integration decision remain future separately gated work.

## 8. Non-regression of predecessor proposal-text passes

| Area | Result | Assessment |
|---|---|---|
| 24 response rows and 64 predicate vectors | **PASS** | Direct operation remains only `authorized; none`; 48 H/G-compatible vectors map to 24 rows and 16 H=G=1 vectors reject. |
| response/answer/field consequences | **PASS** | Pre-parse invalidity, membership zeroing, answer-local zeroing, independent field availability, one block M5, and P3/P4 consequences are unchanged. |
| semantic atoms and T/F/U | **PASS** | U11 section 4 is byte-identical; availability, strength, permission, causes, selectors, reason judgment, consumption, and P3 Y remain closed at proposal level. |
| record-ID and cause ordering | **PASS** | Inner record-ID arrays use canonical scalar-JSON byte order and outer cause references use unsigned byte order. |
| target typing and C4 | **PASS** | Record/nonrecord targets and dependent/target/direct branches remain exact; unrelated missing IDs and extras remain M4. |
| catalog arithmetic | **PASS** | `20+4+4=28`, `7*256=1,792`, `4*10*3*3*5*4*128=921,600`, `1+28+C(28,2)=407`, and `720*2^12=2,949,120`. |
| bank construction | **PASS AS POLICY** | N remains 240-720; each gives exactly N/24 questions per row; development-example and duplicate-key exclusions remain pre-label stops. |
| P2 design | **PASS AS UNEXECUTED DESIGN** | Dependence sums, marginal mappings, Bonferroni allocation, fit/audit separation, and power rules remain unchanged and valid on the written grid. |
| P2 schedule | **PASS** | K=N/12 remains divisible by four for every candidate N. |
| P3 design | **PASS AS UNEXECUTED DESIGN** | Shifted-null probabilities remain in `[0.45,0.95]`; packet contrast, strict margins, calibration, and power rules remain fixed. |
| P3 schedule | **PASS** | K=N/8 is always 2 or 6 modulo 8; opposite rotations or their complement preserve the stated position/wave balance without redraw. |
| calls and tokens | **PASS AS ARITHMETIC** | At N=720 the plan still has 240 P2 calls plus 720 P3/P4 calls, 53,760,000 visible input tokens, and 3,194,880 visible output tokens. |
| human and resource stops | **PASS AS WRITTEN; UNVERIFIED** | The inherited ledger totals 240 hours and retains compute, storage, time, signing, and monetary pre-authoring stops. New key/receipt feasibility is unknown and current key generation is excluded. |
| equality, isolation, and blinding | **PASS EXCEPT FOR FINDINGS** | A-D equality, fresh roots, no ambient transfer, blinded analysis, map release after analysis, no retry, and drift invalidation remain. Missing payloads and E25 assembly break the custody graph. |
| publication and rollback | **PASS EXCEPT FOR GENESIS** | E53-E56 byte-identical publication, untouched-bank rollback, no waiver, and no post-map reanalysis remain. The public status chain cannot start under V13-M02. |
| claim ceiling | **PASS** | A future review pass authorizes at most CONTROL consideration; implementation, keys, bank/schema/fixture/oracle/runner/model/S0/sealed gates remain closed. |

Passed rows are construction, arithmetic, or proposal-text findings only. They are not implementations, measurements, cryptographic results, empirical effects, or validation.

## 9. Facts, inferences, proposals, and local construction tests

### 9.1 Facts established by this review

- The exact baseline and all eighteen input digests passed authentication.
- Both effective streams are independently reconstructable at the hashes and byte counts in section 3.
- The v0.13 receipt/bundle grammar removes the predecessor's digest-selection and ASCII-double-hash ambiguity.
- The root and registry construction has one noncircular proposal-text verification path.
- E43/E45 recipients now possess the source bytes needed for independent equality verification.
- E25, E35, and E48 omit mandatory underlying payloads from their only matching operational edges.
- No authorized write can place bundleless genesis in the pair-only registrar store.
- No selected role assembles E25's two-producer evidence bundle.
- No implementation or empirical result was inspected or created.

### 9.2 Review inferences

- Authenticating a digest does not deliver the artifact a downstream role must consume.
- A uniquely framed plural bundle can still have an incomplete custody path when no role may possess all inputs needed to form it.
- Atomic pair semantics need an explicit genesis exception or a canonical genesis companion.
- An out-of-band user-approved trust anchor is not circular merely because the anchored root key also appears in the registry it signs; the commit/anchor must actually be separately approved before use.

### 9.3 Correction proposals

- The minimum corrections under V13-M01-M03 and V13-m01 are proposals, not approved design choices.
- A successor can preserve both effective-construction grammars, the U11 semantic slice, ID/cause ordering, status receipt bytes, root registry, E43/E45 verification, statistical design, publication path, rollback, and claim ceiling while repairing only the payload, genesis, assembler, and stale schedule clauses.

### 9.4 Local construction-test results

- Strict UTF-8 reconstruction produced the contract and plan values in section 3.
- Slot 10 contained both required source strings exactly once and increased by two bytes after transformation.
- Inventory parsing found 64 unique edge rows: eight E00 grants and every E01-E56 row exactly once.
- Inventory parsing found 26 stores, 32 role-matrix rows, 32 role-index rows, 22 registry entries in ASCII order, and 14 status-edge rows totaling 17 receipts.
- Candidate arithmetic gives N/24 as 10, 14, 18, 22, 26, and 30; N/12 as 20, 28, 36, 44, 52, and 60; and N/8 modulo 8 as 6, 2, 6, 2, 6, and 2.
- No P0-P4 run, signature verification, key generation, mutation catalog, serializer comparison, generator execution, comparator execution, simulation, judge session, model session, or S0 run occurred.

## 10. Maximum justified claim

The maximum defensible claim is:

> At commit `b9b1a0edbd269a5c1c004220ca2a6029dfad47e7`, the authenticated URC-0.13 package is an unimplemented public redesign proposal. Its 31-slot contract and 25-slot plan are independently reconstructable; its inherited response semantics, ordering, C4, catalogs, bank balance, schedules, statistical design, resource stops, isolation, rollback, and claim ceiling remain coherent at the reviewed proposal level; its status receipts now bind plural/digest-only evidence deterministically; its key registry has a noncircular external-root construction; and E43/E45 comparison evidence is recipient-verifiable. It is not suitable for CONTROL integration because mandatory payload bytes disappear from E25/E35/E48, bundleless genesis has no authorized store write, E25 has no selected two-producer bundle assembler, and the normative freeze sequence retains a stale v0.10 review token.

No claim is authorized for key generation, executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 11. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions can meet metadata, target, alias, four-ID, balance, and duplicate constraints without distortion.
- Whether independent labelers, scanners, generators, comparators, judges, map builders, publishers, and custody implementations can agree exactly.
- Whether catalogs, signatures, receipts, bundles, comparisons, review, and confirmatory calls fit the human, compute, storage, calendar, and monetary ceilings.
- Whether the named ACL stores, write-only raw delivery, immutable model fingerprint, monotonic timing, Ed25519 key custody, atomic writes, and durable public delivery are operationally available.
- Whether calibration and power pass the frozen grids. No generalization outside those grids is authorized.

## 12. Exact next-gate recommendation

Do not open CONTROL integration, key generation, public bank authoring, schema or runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7-v0.13 artifacts and this review. The appropriate successor is a separately authorized public redesign that closes V13-M01 through V13-M03 and V13-m01, followed by another fresh public-only independent review. No later gate opens automatically.

## 13. Final verdict

**REVISE-AND-REVIEW**
