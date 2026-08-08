# URC-0.12 independent hostile public-only review

- Review type: `fresh independent hostile public-only design review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `7a1b2037cf8abfaac389ddd4ac684cf23f47847a`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.12 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch change, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** Before substantive reading, the required origin, branch, HEAD, and clean worktree matched exactly. All seventeen allowlisted Markdown files were read in full and no other substantive repository file was inspected. The sixteen required same-basename sidecars contained lowercase SHA-256, two spaces, and the same-basename filename, and each matched its Markdown bytes. `AGENTS.md` has no expected sidecar; its independently computed digest is recorded below.

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
| `s0-lab/control/f0-public/question-contract-v0.11/public-falsification-plan-v0.8.md` | `a35ec31efd009684cf8c96400b48b87ef50a7692402f9793ee08ce883f8450c0` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/review-response-v0.6.md` | `6f5e2308ba33da97b231b76d621559f2b4153588a55acab698a6af4c65c2365e` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.11/urc-v0.11-independent-review-v0.1.md` | `f797dfe55781fb9b8c9b325a9945757076596968c8e4f9dc3e449099e8754fe1` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/universal-response-contract-v0.12-candidate.md` | `c536e0d8316c432cdc14d70c8de7c7505f4ad7e675652246c78658720c6c5de4` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/public-falsification-plan-v0.9.md` | `c651de01e2f7420fe54692e6c69862a7224ff08bd517a96a800bf48cab77a5f8` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.12/review-response-v0.7.md` | `447b37d6d2266286ceea28f1abc173254edfd5bdca7cb72cce10da49c6b02c2e` | matching sidecar |

No repository-wide search, implementation inspection, E0 work product, sealed/private/oracle material, fixture, question, answer, schema, output, web source, or external source was used. The canonical validator was reserved for output validation and was not treated as substantive input. Worktree separation was treated as edit isolation only.

## 2. Review rubric

- **PASS**: the authenticated proposal text uniquely determines the reviewed result without a result-affecting author, builder, comparator, custodian, registrar, publisher, reader, or analyst choice. This does not mean implemented or validated.
- **FAIL**: a contradiction, missing normative definition, non-unique mapping, unsatisfied precondition, missing authorized transfer, unverifiable required check, incomplete ACL route, or executable counterexample remains.
- **UNCLEAR**: materially different implementations remain permitted and the allowlisted public text does not select one.

Finding severities are:

- **blocking**: prevents CONTROL integration because an effective document or mandatory P0/P1 result cannot be uniquely constructed;
- **major**: materially breaks custody, cryptographic trust, blinding, reproducibility, fairness, or feasibility; and
- **minor**: a localized precision defect that must be corrected before freeze.

## 3. Independent effective-document reconstruction

### 3.1 Thirty-one-slot contract

**PASS for byte construction.** U7, U9, U10, U11, and U12 authenticate. Every named heading resolves exactly once; every full and preamble slice satisfies the stated level, order, and range rules; and all 31 successor slots are classified once. The U11 semantic slice enters unchanged as slot 21. Heading metadata is ASCII-safe because exact heading text is located in strict UTF-8 while only its lowercase SHA-256 enters the record.

Independent strict-UTF-8, raw-LF-preserving reconstruction produced:

```text
effective_contract_sha256=d44a73a6cd494d1e081be434ebed3d8d52f22fe49f3eed4009ed75c169a753a2
effective_slots=31
raw_slice_bytes=33758
effective_stream_bytes=43291
```

### 3.2 Twenty-five-slot plan

**PASS for byte construction.** P4, P5, P6, P7, and P9 authenticate. P8 is evidence only and contributes no normative byte. All 25 slots resolve and are classified once. In the authenticated raw P5 section 8 slice, lowercase ASCII `v0.8` occurs exactly once and uppercase ASCII `URC-0.8` occurs exactly once. The ordered count-one transforms to v0.12 therefore execute. Every record has one `slice_mode`, one `transform_count`, and exactly two transform blocks only for slot 10.

Independent reconstruction produced:

```text
effective_plan_sha256=d6796b581822deb9e8dedfa21d59adeb16331418a71342cf5fa2ad81955fdfc8
effective_slots=25
raw_slice_bytes=60656
transformed_slice_bytes=60658
effective_stream_bytes=68999
```

These are independent in-memory design-review computations. They are not implementations, frozen manifests, simulations, or execution results.

## 4. Required predecessor-finding dispositions

| Finding | Decision | Independent v0.12 assessment |
|---|---|---|
| V11-M01 — status transition and digest/signature constructions are non-unique | **PARTIAL PASS; OVERALL FAIL** | The closed status vocabulary, edge/bit order, genesis, prefix transition, previous-record hash, maximum chain, timestamp ordering, record/envelope grammar, fixed E43/E45 roles, comparison record, digest, and unequal-input stop are now explicit. Three remaining gaps prevent complete closure: the singular status event digest does not have a unique binding to plural or digest-only edge artifacts (V12-M01), the key registry is not itself canonically authenticated (V12-M02), and E43/E45 recipients lack the input bytes they are required to recompute and compare (V12-M03). |
| V11-M02 — final public publisher is outside the role/ACL model | **PASS AT PROPOSAL-TEXT LEVEL** | The public record publisher and terminal public record reader now have positive inputs, deny lists, outputs, E00G grants, E53-E55 index cells, and a literal `public-decision-store`. E56 returns only the receipt-envelope digest to the registrar. E50 and E53-E56 form one closed publication path, subject to the shared key-registry finding. |

There is no new blocking or minor finding. Three major findings prevent CONTROL integration.

## 5. Status-machine and E51/E52 audit

| Required attack | Result | Assessment |
|---|---|---|
| status vocabulary | **PASS** | The only values are `A-0000` and the fourteen successive lowercase four-hex prefix masks through `A-3fff`. `A` is expressly a custody-receipt state, not an empirical or S0 pass. |
| bit and edge order | **PASS** | Bits 0-13 map once to E02, E05, E08, E14, E21, E24, E25, E27, E29, E31, E35, E48, E50, and E56. |
| genesis | **PASS AS DESIGN TEXT** | Sequence 0, zero previous digest, `ROOT`, CONTROL-integration-manifest digest, mask `0000`, and status `A-0000` are fixed. The manifest remains a future artifact. |
| prefix transition | **PASS** | Sequence n fixes edge n-1, bits 0 through n-1, and the identical status suffix. Repeats, skips, clears, and alternate status selection reject. |
| previous-record hash | **PASS** | The link is SHA-256 of the immediately preceding exact unsigned status `record_bytes`, and every envelope is separately verified. |
| timestamp | **PASS FOR ORDERING** | Canonical decimal syntax and strict increase are fixed. Timestamp values remain observations and do not choose status or evidence meaning. |
| maximum chain | **PASS** | Exactly genesis plus at most fourteen evidence transitions are admitted. Local enumeration reproduced all 15 listed states and ended at `A-3fff`. |
| failure meaning | **PASS** | An artifact that fails its edge check creates no status record and stops dependent work. The chain never encodes a free pass/reject narrative. |
| status-source delivery order | **PASS AS WRITTEN** | A source does not send its registrar-facing receipt until all lower-bit receipts freeze. An already produced artifact remains in its declared store, not in an implicit registrar buffer. |
| event-evidence binding | **FAIL** | The singular `event_artifact_sha256` is not uniquely derived for edges that deliver multiple hashes or a digest rather than one canonically enveloped artifact. See V12-M01. |
| E52 reader verification | **PASS FOR STRUCTURE; FAIL FOR COMPLETE EVIDENCE IDENTITY** | The reader can verify envelope signatures, record hashes, sequence, edge, mask, status, and time ordering. It cannot resolve the ambiguous event-artifact binding in V12-M01. The text appropriately does not claim that the reader sees protected evidence bytes. |

## 6. Signed-artifact and comparison audit

| Required attack | Result | Assessment |
|---|---|---|
| generic preimage and envelope | **PASS EXCEPT FOR REGISTRY BOOTSTRAP** | The prefix, signer role, key ID, decimal byte length, exact record bytes, record hash, algorithm, and signature field have one order. The registry needed to validate them is underdefined in V12-M02. |
| record-length boundary | **PASS** | The decimal byte count delimits exact `record_bytes`; the next field follows the record's required final LF without an inserted separator. |
| LF, BOM, CR, and field order | **PASS** | Custody grammars require ASCII, LF, no BOM, no CR, one final LF, and exact field order. |
| SHA-256 scope | **PASS** | `record_sha256` and comparison digests are SHA-256 of exact unsigned `record_bytes`; the signed preimage repeats the recomputed value. |
| Ed25519 scope | **PASS CONDITIONALLY** | The 32-byte public key, 64-byte signature, key hash, signer-role field, record length, record bytes, and record hash are all in the check. Acceptance still depends on a uniquely authenticated registry. |
| key ID and role binding | **PASS IN EACH ENVELOPE; FAIL AT REGISTRY ROOT** | A role-mismatched key rejects, but the registry's own bytes, signer, and trust anchor are not fixed. |
| domain separation | **PASS** | The signed-artifact prefix plus the first-line status/comparison/publication schema and the byte length prevent cross-record boundary or type substitution under the written grammars. |
| E43/E45 fixed roles and fields | **PASS** | Both records fix edge, left/right role, source hashes, agreed hash, result, comparison digest, comparison-custodian signer, and field order. |
| unequal-input handling | **PASS** | Unequal inputs produce neither an agreed table nor an E43/E45 artifact and stop the workflow. |
| recipient verification | **FAIL** | Recipients are told to recompute both source hashes and byte equality but receive neither source artifact. See V12-M03. |

## 7. New major findings

### V12-M01 — A status transition does not uniquely bind plural or digest-only edge evidence

- Severity: **major**
- Fact: each status record has exactly one `event_artifact_sha256`.
- Fact: E25 delivers two fixed-role comparator hashes to the registrar. E02 similarly names multiple benchmark/audit/power summary hashes, while E05, E08, E14, E21, E24, E27, E29, E31, E35, E50, and E56 often deliver an already-computed digest rather than one canonical evidence-envelope byte string.
- Fact: section 4.1 says the event digest equals the exact artifact accepted on the edge, but it supplies no edge-specific receipt grammar, role order, count, or rule selecting whether a carried digest is copied as the event value or hashed again as the bytes of a digest artifact.
- Executable design counterexample: for E25 the registrar can place the comparator-1 hash, the comparator-2 hash, or SHA-256 of an unstated concatenation/container into the one event field. Each candidate is 64 lowercase hex and can coexist with the required sequence, previous digest, edge, mask, status, increasing timestamp, and valid registrar signature. The plan provides no byte rule that selects one.
- Consequence: the status record remains non-unique for the same two E25 inputs. E52 can authenticate whichever record the registrar signed but cannot determine which exact pair of comparator artifacts that record commits to. Status-expected mutations and evidence-to-status binding therefore lack one independent answer.
- Minimum correction proposal: define one canonical status-source receipt for every bit. It should contain the edge, fixed artifact count, fixed artifact roles, ordered artifact digests, and required-check result; set `event_artifact_sha256` only to SHA-256 of those exact receipt bytes. Alternatively split plural evidence into separately ordered bits. State explicitly whether digest-only edge payloads are copied values or hashed transport artifacts.

### V12-M02 — The public key registry has no canonical bytes, designated signer, or noncircular trust anchor

- Severity: **major**
- Fact: before any signed-artifact use, E00G delivers a “signed public key registry” containing four role-bound Ed25519 keys and their IDs.
- Fact: the plan defines no registry record grammar, role-row order, registry digest, registry signature envelope, designated registry signer, or external trust anchor. The generic envelope permits a `<closed role ID>` but no rule selects which role signs this registry.
- Fact: `control-registrar` is one key inside the registry and the registrar produces E00G. A registrar-signed registry is therefore self-authenticating unless an independently authenticated expected registry hash or external root is fixed. The genesis manifest is named only as a digest inside the later registrar status record; it is not stated to bind the registry bytes or verification key.
- Executable design counterexample: two registries can contain the same four role/key/key-ID associations in different byte formats or orders and be signed by different listed signing roles. Both satisfy the stated content condition, while their bytes, signature preimages, and trust assumptions differ.
- Consequence: “no alternate bytes or signer” is true for a custody envelope only after a registry is trusted, but the text does not uniquely establish that trust root. Status, comparison, and publication signatures therefore lack one public acceptance procedure.
- Minimum correction proposal: publish an exact canonical registry `record_bytes` grammar and role order; name exactly one registry signer and signature preimage; and bind the exact registry-envelope digest in a separately authenticated CONTROL-integration root whose verification key is not obtained from the registry being verified. Add registry substitution, signer substitution, reordering, revocation, and bootstrap mutations.

### V12-M03 — E43/E45 require recipient checks that their authorized deliveries cannot perform

- Severity: **major**
- Fact: E43 delivers only the signed comparison envelope, comparison digest, and agreed semantic table to comparator operators. E45 delivers the analogous three artifacts to analysis.
- Fact: the left and right judge tables are readable only by the judgment-comparison custodian, and the left and right comparator tables are readable only by the adjudication-comparison custodian. No E43/E45 recipient receives those source bytes or has a store-read grant for them.
- Fact: section 4.2 nevertheless requires each recipient to recompute both fixed-role input hashes and byte equality in addition to the agreed-table hash, record hash, key, and signature.
- Executable design counterexample: a comparison custodian can sign a well-formed record containing two invented source hashes and the true hash of the delivered agreed table. The recipient can verify the comparison-custodian signature, record digest, and agreed-table hash, but cannot recompute either source hash or establish source equality from the delivered artifacts.
- Fact: E43 calls the source artifacts “signed table” bytes while the comparison result is `equal`. If independently signed envelopes are meant, role/signature differences normally make the bytes unequal; if only table payloads are meant, no extraction grammar or payload-hash field selects those bytes. The same payload/envelope distinction is unstated for E45.
- Consequence: recipient verification is an impossible precondition under the current ACL graph, and the comparison record can only be treated as a custodian attestation rather than the independently recomputable evidence the text requires.
- Minimum correction proposal: choose one model. Either deliver the exact left/right source bytes through explicit ACL-safe edges so recipients can hash and compare them, or state that recipients verify only a role-bound custodian attestation and remove the recomputation claim. In either model, define whether each source hash covers a signed envelope or a canonical table payload, and provide an exact payload extraction/hash grammar.

No minor finding is separately recorded.

## 8. Public decision publication and ACL audit

| Required attack | Result | Assessment |
|---|---|---|
| publisher role | **PASS** | The publisher has E00G/E53 inputs, a narrow deny list, and only E54 output. It has no read grant to raw, label, condition-map, or analysis stores. |
| terminal public reader | **PASS** | The reader has only E00G/E55, denies nonpublic experimental and sealed material, and emits nothing. |
| final-decision-vault | **PASS** | E50 is its only writer; E53 is the publisher's only full-record read; the registrar receives only the E50 record digest. |
| public-decision-store | **PASS** | E54 is its only write, E55 its terminal full-record read, and E56 its digest-only registrar route. |
| exact byte equality | **PASS** | Source and published record hashes must be equal, the receipt states byte identity, and changed bytes reject. |
| atomic receipt write | **PASS AS DESIGN TEXT** | E54 must atomically store the exact record and signed receipt; partial or second publication yields no E56. No implementation exists to establish operational atomicity. |
| receipt digest return | **PASS AS A ROUTE** | E56 returns only SHA-256 of the exact signed receipt envelope. Its use in the status chain is subject to V12-M01's general status-source receipt ambiguity. |
| reader verification | **PASS CONDITIONALLY** | E55 supplies the record and receipt needed to recompute both record hashes and the publisher signature. Public-key trust remains conditional on V12-M02. |
| matrix/store/edge/index closure | **PASS AS INVENTORY** | Independent parsing found eight E00 grants, exactly one row for every E01-E56 type, 26 unique store IDs, 32 role-matrix rows, and 32 role-index rows. The four public terminal/publication roles are present in both role and edge topology. |
| unmatched output or reader | **PASS** | No v0.11-style unmodeled public publisher remains. The E43/E45 problem is an insufficient input for a declared recipient check, not an absent recipient row. |

## 9. Non-regression of authenticated v0.11 passes

| Required non-regression attack | Result | Assessment |
|---|---|---|
| contract semantics and 24 rows | **PASS** | Slots 6-30 retain the reviewed decision, response, semantic, cause, C1-C7, consumption, canonicalization, and runner-package slices. Direct operation remains exactly `authorized; none`; H/G dual truth rejects. |
| 64 predicate vectors | **PASS** | The 48 H/G-compatible vectors map to the 24 rows and the 16 H=G=1 vectors reject before admission. |
| construction, encoding, and transforms | **PASS** | Both effective streams are unique at section 3 hashes; contract records have no transforms; plan slot 10 has exactly the two count-one transforms. |
| record-ID and cause order | **PASS** | Inner record-ID arrays use canonical scalar-JSON UTF-8 byte order; complete cause references use unsigned bytewise order, including `R10` before `R2`. |
| response/answer/field consequences | **PASS** | Pre-parse invalidity, response membership zeroing, answer-local zeroing, independent field availability, one block-level M5, and P3/P4 effects remain unchanged. |
| target typing and C4 | **PASS** | Record/nonrecord targets and dependent/target/direct branches remain exact; unrelated missing accepted IDs and extras remain M4; identical dependent/target keys union once. |
| cause and catalog bounds | **PASS AS ARITHMETIC** | `20+4+4=28`; `7*256=1,792`; `4*10*3*3*5*4*128=921,600`; `1+28+C(28,2)=407`; and `720*2^12=2,949,120`. |
| bank balance | **PASS AS AN UNIMPLEMENTED REQUIREMENT** | N remains 240, 336, 432, 528, 624, and 720, giving 10, 14, 18, 22, 26, and 30 questions per response row. |
| duplicate controls | **PASS AT POLICY LEVEL** | Development examples, exact duplicates, and noun/entity/identifier/number swaps preserving the relation/predicate/operation/answer skeleton remain pre-label rejection conditions. The future duplicate-key implementation does not exist. |
| A-D equality and opportunity | **PASS AS AN UNIMPLEMENTED REQUIREMENT** | Canonical facts, IDs, normalized hashes, question order, grammar opportunity, model, authority, tools, limits, turns, first output, and no retry remain common. |
| P2 stochastic model | **PASS AS UNEXECUTED DESIGN** | Every dependence sum is below one; probability mappings remain valid; alpha is `4*0.00625+2*0.0125=0.05`; fit and audit streams remain independent and pre-bank. |
| P2 schedule | **PASS** | Every `K=N/12` is divisible by four, so all four cells occupy each serial position and wave equally. |
| P3 stochastic model | **PASS AS UNEXECUTED DESIGN** | Dependence sums are below one and every shifted-null probability lies in `[0.45,0.95]`; the packet contrast and strict boundaries remain fixed. |
| P3 schedule | **PASS** | `K=N/8` is 30, 42, 54, 66, 78, or 90 and therefore 6 or 2 modulo 8. Opposite residual rotations or their complement keep position and wave counts within one without seed redraw. |
| calls and tokens at N=720 | **PASS AS ARITHMETIC** | P2 has 240 calls and P3/P4 has 720 first-output calls, for 960 total; visible input is 53,760,000 tokens and visible output is 3,194,880 tokens. |
| human and resource rules | **PASS AS WRITTEN STOPS; UNVERIFIED** | Human rows total 240 hours. Catalog generation/comparison, CPU, RAM, storage, calendar, signing, and monetary projections remain pre-authoring stops. |
| isolation, leakage, and rollback | **PASS EXCEPT FOR FINDINGS** | Fresh-root separation, no ambient transfer, blinded analysis, map release after analysis, no reanalysis, no retry, drift invalidation, untouched-bank rollback, and public/sealed/E0 boundaries remain. V12-M01-M03 prevent complete custody closure. |
| bounded claim | **PASS** | The future-pass sentence remains confined to one frozen synthetic public experiment and excludes S0, system implementation, safety, economic value, production readiness, stability, and model transfer. |

Passed rows are construction, arithmetic, or proposal-text results only. They are not implementations, measurements, empirical effects, or validation results.

## 10. Facts, inferences, proposals, and local review tests

### 10.1 Facts established by this review

- The exact baseline and all seventeen input digests passed authentication.
- Both effective byte streams are independently reconstructable at the hashes and byte counts in section 3.
- The status enum, transition function, sequence, previous-record hash, time ordering, and fixed E43/E45/publication record grammars are materially more closed than v0.11.
- The singular status evidence field does not uniquely bind E25's two fixed-role hashes.
- The signed key registry lacks exact bytes, one signer, and a noncircular anchor.
- E43/E45 recipients do not receive the source bytes they are required to hash and compare.
- The public publisher and public decision reader are now represented in the matrix, stores, ledger, and index.
- No implementation or empirical result was inspected or created.

### 10.2 Review inferences

- A deterministic prefix-mask state does not by itself make its triggering evidence digest deterministic.
- A valid signature proves that one key signed one preimage; it does not establish which key should be trusted when the key registry's own authentication is circular or unspecified.
- A signed comparison record is a custodian attestation unless the verifier receives, or has an authorized way to retrieve, the source bytes needed to reproduce the claimed hashes and equality.
- The E53-E56 publication topology is closed at proposal-text level, but deployable key custody and atomic storage remain feasibility questions.

### 10.3 Correction proposals

- The minimum corrections under V12-M01-M03 are proposals, not approved design choices.
- A successor can preserve both effective constructions, the complete semantic slice, global ID order, C4 repair, catalogs, balance, schedules, public publication roles, isolation, rollback, and bounded claim while replacing only the incomplete evidence-receipt, registry-bootstrap, and comparison-verification clauses.

### 10.4 Local review-test results

- Strict UTF-8 reconstruction independently produced the contract and plan hashes in section 3.
- Status enumeration independently produced 15 states, exactly matched the published sequence, and ended at `A-3fff`.
- Inventory parsing found 64 unique edge rows: eight E00 grants and every E01-E56 row exactly once, with no missing, extra, or duplicate ID.
- Inventory parsing found 26 unique store rows, 32 role-matrix rows, and 32 role-index rows.
- Independent arithmetic produced 921,600 abstract rows, 1,792 availability rows, 407 cause-key rows, and a 2,949,120-row maximum bank-instance projection.
- No P0-P4 test, signature verification, key generation, mutation catalog, serializer comparison, generator run, comparator run, simulation, judge session, model session, or S0 run occurred.

## 11. Maximum justified claim

The maximum defensible claim is:

> At commit `7a1b2037cf8abfaac389ddd4ac684cf23f47847a`, the authenticated URC-0.12 package is an unimplemented public redesign proposal. Its 31-slot contract and 25-slot plan are independently reconstructable; its inherited semantic, ordering, C4, catalog, bank-balance, schedule, statistical, resource, isolation, rollback, and claim-ceiling text remains coherent at the reviewed proposal level; and its final public publisher/reader path is now represented in the ACL topology. It is not suitable for CONTROL integration because status evidence is not uniquely bound on plural/digest-only edges, the signing-key registry lacks a canonical noncircular trust root, and E43/E45 recipients cannot perform the source-hash and equality verification the plan requires.

No claim is authorized for an executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 12. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions can satisfy metadata, target, alias, four-ID, balance, and duplicate-key constraints without distortion.
- Whether independent labelers, scanners, generators, comparators, leakage reviewers, judges, map builders, publishers, and custody implementations can agree exactly.
- Whether catalogs, two generations, comparisons, signatures, 200 comparator runs, and review fit the human, compute, storage, calendar, and monetary ceilings.
- Whether named ACL stores, write-only raw delivery, immutable model fingerprinting, monotonic timing, Ed25519 key custody, revocation, atomic publication, and durable public delivery are operationally available.
- Whether calibration and power pass the frozen grids; no generalization outside those grids is authorized.

## 13. Exact next-gate recommendation

Do not open CONTROL integration, public bank authoring, schema or runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7-v0.12 artifacts and this review. The appropriate successor action is a separately authorized public redesign that closes V12-M01, V12-M02, and V12-M03, followed by another fresh public-only independent review. No later gate opens automatically.

## 14. Final verdict

**REVISE-AND-REVIEW**
