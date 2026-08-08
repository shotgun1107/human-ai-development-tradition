# URC-0.11 independent hostile public-only review

- Review type: `fresh independent hostile public-only design review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `c578ffcb61a389160190f2636c8afd3fde568268`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.11 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch change, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** Before substantive reading, the required origin, branch, HEAD, and clean worktree matched exactly. All fifteen allowlisted Markdown files were read in full and no other substantive repository file was inspected. The fourteen required same-basename sidecars used lowercase SHA-256, two spaces, and the same-basename filename, and each matched its Markdown bytes. `AGENTS.md` has no expected sidecar; its independently computed digest is recorded below.

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
| `s0-lab/control/f0-public/question-contract-v0.10/review-response-v0.5.md` | `a15484c1f55ee388b2f6b49c25f67f549af6560b620a9b1ae128a080eedfd1d1` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.10/urc-v0.10-independent-review-v0.1.md` | `b20855eca2efb59fc51768d581a815ef26934ed524c3fbc2197db6407c621c8a` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/universal-response-contract-v0.11-candidate.md` | `ae4620c1b532906538252ed503cf39211c46371d4e1eebdbe9a5ef5136528807` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/public-falsification-plan-v0.8.md` | `a35ec31efd009684cf8c96400b48b87ef50a7692402f9793ee08ce883f8450c0` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/review-response-v0.6.md` | `6f5e2308ba33da97b231b76d621559f2b4153588a55acab698a6af4c65c2365e` | matching sidecar |

No repository-wide search, implementation inspection, history inspection beyond the exact baseline checks, E0 work product, sealed/private/oracle material, fixture, question, answer, schema, output, web source, or external source was used. The canonical validator was reserved for output validation and was not treated as substantive input. Worktree separation was treated as edit isolation only.

## 2. Review rubric

- **PASS**: the authenticated proposal text uniquely determines the reviewed result without a result-affecting author, builder, comparator, custodian, registrar, publisher, or analyst choice. This does not mean implemented or validated.
- **FAIL**: a contradiction, missing normative definition, non-unique mapping, unsatisfied construction precondition, missing authorized transfer, incomplete ACL route, or executable counterexample remains.
- **UNCLEAR**: materially different implementations remain permitted and the allowlisted public text does not select one.

Finding severities are:

- **blocking**: prevents CONTROL integration because an effective document, mandatory comparator result, or P0/P1 artifact cannot be uniquely constructed;
- **major**: materially breaks custody, blinding, reproducibility, fairness, or feasibility; and
- **minor**: a localized precision defect that must be corrected before freeze.

## 3. Independent effective-document reconstruction

### 3.1 Thirty-one-slot contract

**PASS for byte construction.** U7, U9, U10, and U11 authenticate. Every named heading resolves exactly once; every full and preamble slice satisfies the stated level, order, and range rules; and all 31 successor slots are classified exactly once. Heading metadata is ASCII-safe because exact heading text is located in strict UTF-8 while only its lowercase SHA-256 enters each record. The U11 sidecar supplies a nonrecursive source digest.

Independent strict-UTF-8, raw-LF-preserving reconstruction produced:

```text
effective_contract_sha256=45d9526b4c48d199acbcf3659befab18ba1cd55e08fdaac45ea11e02f95ef88c
effective_slots=31
raw_slice_bytes=34069
effective_stream_bytes=43602
```

### 3.2 Twenty-five-slot plan

**PASS for byte construction.** P4-P8 authenticate, all headings and preambles resolve, and the 25 slots are classified once. In the authenticated raw P5 section 8 slice, lowercase ASCII `v0.8` occurs exactly once and uppercase ASCII `URC-0.8` occurs exactly once. The two ordered count-one transforms to v0.11 therefore execute. The record grammar emits one `slice_mode`, one `transform_count`, exactly two transform blocks only for slot 10, and no literal non-ASCII heading bytes in metadata.

Independent reconstruction produced:

```text
effective_plan_sha256=2c7043400030506a6d19029139869f49ac8689e95c853e2a15dde3f60fd3dc8f
effective_slots=25
raw_slice_bytes=51897
transformed_slice_bytes=51899
effective_stream_bytes=60240
```

These are independent in-memory design-review computations. They are not implementations, frozen manifests, simulations, or execution results.

## 4. Required predecessor-finding dispositions

| Finding | Decision | Independent v0.11 assessment |
|---|---|---|
| V10-B01 — omitted semantic atoms and strength | **PASS AT PROPOSAL-TEXT LEVEL** | Effective slot 21 now contains one self-contained semantic slice. It defines response/field and judge availability, every answer semantic atom, T/F/U behavior, operational strength, `stronger`, direct permission, false-atom cause mapping, total selectors, source nonemptiness, and P3 Y. It expressly excludes silent inheritance from omitted U7 section 6. The retained Kleene tables and consequence table compose without a result-affecting contradiction. |
| V10-M01 — unmatched registrar and comparison outputs | **PASS FOR THE THREE CITED ROUTE DEFECTS; FAIL FOR COMPLETE CUSTODY CLOSURE** | E51 writes registrar status records, E52 supplies a terminal status reader, E43 carries both the judgment digest and table, and E45 carries both the adjudication digest and table. Those exact omissions are repaired. The broader zero-unmatched-route and custody claim remains false or underdefined for the reasons in V11-M01 and V11-M02. |

There is no new blocking finding in this review. Two new major custody findings prevent integration.

## 5. Hostile semantic-slice audit

| Required semantic attack | Result | Assessment |
|---|---|---|
| field availability | **PASS** | `response_ok` requires envelope and membership T; each field then depends only on its own format atom. `F-answer` is expressly not an extra dependency, preserving diagnosis of valid independent fields inside an invalid answer. |
| judge availability | **PASS AS DESIGN TEXT** | R-semantic additionally requires an available reason plus two fresh signed judgments and byte-identical comparison. Missing, malformed, or unequal judgments produce U and stop adjudication rather than becoming F. The future rubric, schema, signing, and ACL realization remain unimplemented. |
| semantic-atom domain | **PASS** | Decision, submitted citation, required, correlation, counterexample, affected-union, uncertainty, mechanical-reason, and semantic-reason atoms are all enumerated with exact availability and T conditions. |
| operational strength and `stronger` | **PASS** | `authorized; none` maps to 2, every barred row to 1, and every other row to 0. Submitted strength is U unless both submitted coordinates are available; every ordered available pair is numerically total. |
| direct permission | **PASS** | Truth and submitted direct permission are true only for `authorized; none`; submitted direct is U unless basis and responsibility are both available. |
| false-atom causes and aliases | **PASS** | Every available false atom maps to one slot-20 canonical cause family. Identical obligation arrays, dual-tag records, and repeated affected IDs have the already frozen aliases; unavailable atoms create no cause. |
| selectors | **PASS** | `wrong_direct` and `stronger_sources` return every unequal available basis/responsibility coordinate and cannot be empty when their T precondition holds. No primary/minimal/counterfactual choice remains. |
| C1-C7 inputs | **PASS** | The retained Kleene AND/OR tables, admitted metadata, field availability, strength/direct predicates, tagged citations, groups, closures, affected membership, reservation, and insufficient-basis values make every retained branch T, F, or U. A U code is diagnostic-only and cannot suppress a T sibling. |
| consumption | **PASS** | All T source sets freeze before ascending C1-C7 subtraction; each canonical root is consumed once; later aliases are shadowed or emit only their unique residual; remaining available roots map deterministically to M1-M4/M6 after the one-M5 format step. |
| P3 Y | **PASS** | Inherited format defects retain their response- or answer-level zero. After format handling, Y is 1 only when every enumerated semantic atom is T, 0 on an available F, and undefined because adjudication stops on any U. |
| retained format/three-valued composition | **PASS** | The new slice does not coerce U to F, does not reintroduce `F-answer` as a field dependency, and does not alter the retained raw/response/answer/field consequences. |

These results establish only that the written functions are closed enough for later independent implementation attempts. No comparator, expected generator, mutation catalog, judge, or P3 observation exists.

## 6. New major findings

### V11-M01 — E51 status records authenticate bytes but do not determine a valid status transition

- Severity: **major**
- Fact: E51 permits repeated append-only records containing a triggering evidence digest, prior-record digest or zero genesis, `new status`, signature, and monotonic timestamp.
- Fact: the effective plan supplies no closed status vocabulary, allowed-transition table, evidence-to-status function, canonical status-record byte grammar, digest preimage/order, signature identity rule, or frozen specification delivery that selects those values.
- Fact: E52 requires the public reader to check signature, chain, and requested digest, but does not authorize that reader to inspect the triggering evidence or verify that `new status` is the unique result required by it.
- Executable counterexample: for the same authenticated pass/reject digest and prior chain tip, the registrar can sign one syntactically complete record whose new status says pass and another whose new status says reject. Both contain every required field and can satisfy the stated signature, chain, and monotonic-time checks because no normative transition function rejects either content.
- Fact: E43 and E45 now route both declared digests, but their digest preimage grammar and ordering are likewise not defined. The text says each digest “covers” two signed inputs and an agreed table; different length-prefixing, ordering, or concatenation rules can therefore produce different evidence bytes while preserving the same tables.
- Consequence: status publication and comparison-evidence mutations cannot have one independently generated expected result. The registrar retains result-affecting status discretion, and P0/P1 cannot prove the advertised chain/digest exactness from the effective plan alone.
- Minimum correction proposal: freeze a closed status enum and transition table keyed by exact evidence types; define one canonical byte grammar, SHA-256 preimage, signature scope/key identity, timestamp order rule, and genesis/append rule; and define one ordered, length-delimited digest grammar for E43/E45. Add their exact specifications to a pre-use public grant and require independent expected mutations.

### V11-M02 — The final public-record publisher remains an unmodeled ACL reader

- Severity: **major**
- Fact: the `final-decision-vault` store row authorizes a `public record publisher` to read the decision record, and E50 additionally states that “public gets record.”
- Fact: neither the 30-row role matrix nor the 30-row role-to-edge index contains a public record publisher or a terminal public decision reader. There is no positive input, denylist, only-output rule, role conflict, signature check, or exact inbound edge for that reader.
- Fact: v0.11 added a fully modeled `public status reader` for E52, demonstrating that terminal public reading is represented as a role elsewhere in the same plan.
- Consequence: the claim that every store reader, role input/output, and operational route has a unique matrix/store/edge/index cell is false. An unspecified publisher account could receive other forbidden inputs or publish bytes not authenticated to the E50 record without violating any role row because no such role row exists.
- Minimum correction proposal: add one terminal public-decision reader/publisher role with a positive input, denylist, output rule, exact store-read edge, and index row, or remove the publisher reader and define a direct authenticated public-release operation whose bytes and digest are part of E50. Regenerate the matrix/store/edge/index bijection mechanically.

No minor finding is separately recorded; the localized digest-construction ambiguity is included in V11-M01 because it affects required P1 evidence.

## 7. Custody and ACL audit

| Required custody attack | Result | Assessment |
|---|---|---|
| E51 registrar-store write route | **PASS FOR ROUTE EXISTENCE; FAIL FOR STATUS DETERMINISM** | E51 is the only declared writer route and may repeat by edge type. V11-M01 prevents a unique transition result. |
| E52 public status reader | **PASS FOR ROLE/ACL ROUTING; UNCLEAR FOR SEMANTIC AUTHENTICATION** | The terminal role, denylist, store reader, and index cell exist. It can verify a byte chain but cannot prove the status/evidence relationship under the current text. |
| repeated append-only chain | **FAIL** | Prior digest, genesis, signature, evidence digest, and time are named, but record grammar and permitted transitions are not. |
| E43 judgment digest/table | **PASS FOR DELIVERY; UNCLEAR FOR DIGEST BYTES** | Both declared outputs reach comparator operators. Exact signed-input equality remains required, but the digest preimage grammar is absent. |
| E45 adjudication digest/table | **PASS FOR DELIVERY; UNCLEAR FOR DIGEST BYTES** | Both declared outputs reach analysis. The same preimage ambiguity remains. |
| E00A-H and E01-E52 inventory | **PASS AS ROW INVENTORY** | Independent parsing found exactly eight distinct E00 grants and exactly one row for every E01-E52 edge type: 60 unique edge rows and no missing or extra ID. |
| store table | **PASS AS ID INVENTORY** | All 25 literal store IDs are unique and each row names one writer plus readers. The final-decision reader is not modeled as a role; inventory uniqueness does not cure V11-M02. |
| matrix/index row inventory | **PASS AS COUNT; FAIL AS COMPLETE BIJECTION** | Both tables contain 30 role rows, including the new status reader. The unmodeled public decision publisher remains outside both. |
| E43/E45 declared-output closure | **PASS** | The exact two omissions identified in V10-M01 are repaired. |
| ACL and ambient-copy boundary | **FAIL** | V11-M02 leaves one authorized store reader without a role or indexed route; V11-M01 leaves status-signing discretion. |

## 8. Non-regression of authenticated v0.10 passes

| Required non-regression attack | Result | Assessment |
|---|---|---|
| construction, encoding, transforms, and ID order | **PASS** | Both streams are byte-unique at section 3 hashes. Slot 10 has exactly two count-one transforms. Global scalar-JSON byte order and outer cause order remain unchanged. |
| 24 response rows and 64 predicate vectors | **PASS** | The exact Cartesian rows, H/G rejection, typed owner identities, and direct-operation rule remain inherited without alteration. |
| target typing and C4 | **PASS** | Record/nonrecord target rules and dependent/target/direct branches remain exact; unrelated missing accepted IDs and extras remain M4, and equal dependent/target keys union once. |
| response, answer, and field consequences | **PASS** | Pre-parse invalidity, response-wide membership failure, answer-local failure, field-local diagnosis, one block-level M5, and P3/P4 schema effects are retained. |
| cause and catalog bounds | **PASS AS ARITHMETIC** | `20+4+4=28`; `7*256=1,792`; `4*10*3*3*5*4*128=921,600`; `1+28+C(28,2)=407`; and `720*2^12=2,949,120`. |
| bank balance | **PASS AS UNIMPLEMENTED REQUIREMENT** | N remains 240, 336, 432, 528, 624, and 720, giving exactly 10, 14, 18, 22, 26, and 30 questions per response row. |
| duplicate controls | **PASS AT POLICY LEVEL** | Development examples, exact duplicates, and noun/entity/identifier/number swaps preserving a relation/predicate/operation/answer skeleton remain pre-label rejection conditions. The future key specification is unimplemented. |
| A-D fact and opportunity equality | **PASS AS UNIMPLEMENTED REQUIREMENT** | Canonical facts, IDs, normalized content hashes, questions, grammar opportunities, model, authority, tools, limits, turns, first output, and no retry remain common. |
| P2 model and statistics | **PASS AS UNEXECUTED DESIGN** | All dependence sums are below one; the probability mappings are valid; alpha remains `4*0.00625+2*0.0125=0.05`; fit and audit streams remain separate and pre-bank. |
| P2 schedule | **PASS** | Every `K=N/12` is divisible by four, so the four-cell rotation balances every serial position and wave. |
| P3 grid and estimator | **PASS AS UNEXECUTED DESIGN** | Every null probability remains in `[0.45,0.95]`; all dependence sums are below one; the packet contrast and strict equivalence boundaries remain fixed. |
| P3 schedule | **PASS** | `K=N/8` is 30, 42, 54, 66, 78, or 90, hence remainder 6 or 2 modulo 8. Opposite residual rotations or their complement keep every position and wave within one without seed redraw. |
| calls and visible tokens at N=720 | **PASS AS ARITHMETIC** | P2 is 240 calls, P3/P4 is 720 first-output calls, total is 960; visible input is 53,760,000 tokens and visible output is 3,194,880 tokens. |
| resource rules | **PASS AS WRITTEN STOPS; UNVERIFIED** | The human rows total 240 hours; catalog generation/comparison, CPU, RAM, storage, calendar, and monetary projections remain pre-authoring stop conditions. |
| isolation, leakage, and rollback | **PASS EXCEPT FOR THE CUSTODY FINDINGS** | Fresh-root separation, no ambient transfers, blinded analysis, post-analysis map release, no reanalysis, no retry, drift invalidation, untouched-bank rollback, and public/sealed/E0 boundaries remain. V11-M01/M02 prevent complete custody closure. |
| claim ceiling | **PASS** | The future-pass sentence remains limited to one frozen synthetic public experiment and excludes S0, system implementation, safety, economic value, production, stability, and transfer claims. |

Passed rows are construction, arithmetic, or proposal-text results only. They are not implementations, measurements, empirical effects, or validation results.

## 9. Facts, inferences, proposals, and test results

### 9.1 Facts established by this review

- The exact baseline and fifteen input digests passed authentication.
- Both effective byte streams are mechanically reconstructable at the hashes and byte counts in section 3.
- V10-B01 is repaired at proposal-text level.
- E51/E52 and the two-output forms of E43/E45 repair the three exact missing routes named by V10-M01.
- The status transition/value and cryptographic record constructions are not closed.
- The `final-decision-vault` public publisher is absent from the role matrix and role index.
- No implementation or empirical result was inspected or created.

### 9.2 Review inferences

- The semantic slice is sufficiently total for later independent builder attempts, but this is not evidence that the builders or judges will agree.
- A signature authenticates a registrar's chosen status; without a transition function it does not prove that the status follows from the triggering evidence.
- A unique edge-ID inventory does not establish a bijection when one authorized reader is outside the role and index tables.
- Construction, semantic closure, balance, statistics, and resource stops cannot compensate for major custody gaps.

### 9.3 Correction proposals

- The minimum corrections in V11-M01 and V11-M02 are proposals, not approved design decisions.
- A successor can preserve the authenticated constructions, semantic slice, ID order, C4 repair, catalog arithmetic, schedules, balance controls, isolation rules, and bounded claim while closing the status/digest grammars and final public-reader route.

### 9.4 Test results

- The reconstruction and arithmetic results in sections 3, 7, and 8 are local design-review checks over authenticated public text.
- No P0-P4 test, mutation catalog, serializer comparison, generator run, comparator run, simulation, model session, judge session, or S0 run occurred.

## 10. Maximum justified claim

The maximum defensible claim is:

> At commit `c578ffcb61a389160190f2636c8afd3fde568268`, the authenticated URC-0.11 package is an unimplemented public redesign proposal. Its 31-slot contract and 25-slot plan are independently reconstructable, and its semantic-atom, strength, direct-permission, cause, selector, C1-C7, consumption, P3, ID-order, C4, balance, schedule, arithmetic, isolation, rollback, and claim-ceiling text is coherent at the reviewed proposal level. The three exact output-route omissions from v0.10 are repaired, but the package is not suitable for CONTROL integration because the registrar status transition/digest constructions remain non-unique and the final public decision publisher is absent from the role/edge ACL model.

No claim is authorized for an executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 11. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions can satisfy metadata, target, alias, four-ID, balance, and duplicate-key constraints without distortion.
- Whether independent labelers, scanners, generators, comparators, leakage reviewers, judges, map builders, and digest/status implementations can agree exactly.
- Whether catalogs, two generations, comparison, signatures, 200 comparator runs, and review fit the human, compute, storage, calendar, and monetary ceilings.
- Whether named ACL stores, write-only raw delivery, immutable model fingerprinting, monotonic timing, registrar signing, and terminal publication are operationally available.
- Whether calibration and power pass the frozen grids; no generalization outside those grids is authorized.

## 12. Exact next-gate recommendation

Do not open CONTROL integration, public bank authoring, schema or runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7-v0.11 artifacts and this review. The appropriate successor action is a separately authorized public redesign that closes V11-M01 and V11-M02, followed by another fresh public-only independent review. No later gate opens automatically.

## 13. Final verdict

**REVISE-AND-REVIEW**
