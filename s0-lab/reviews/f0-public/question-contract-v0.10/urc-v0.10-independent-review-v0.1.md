# URC-0.10 independent hostile public-only review

- Review type: `fresh independent hostile public-only design review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `72ab5204646f9e088a828e88c9b604254edab50e`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.10 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch change, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** Before substantive reading, the required origin, branch, HEAD, and clean worktree matched exactly. All thirteen allowlisted Markdown files were read in full and no other substantive repository file was inspected. The twelve required same-basename sidecars used lowercase SHA-256, two spaces, and the same-basename filename, and each matched its Markdown bytes. `AGENTS.md` has no expected sidecar; its independently computed digest is recorded below.

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
| `s0-lab/control/f0-public/question-contract-v0.9/review-response-v0.4.md` | `8d243c4435fff25012b0ec416c5b09414654edf4e1c4ee9d7e8d1ab549419597` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.9/urc-v0.9-independent-review-v0.1.md` | `d88560ecad9642c743ea1cf9386623b1cc8e77cd34e12c7f5180c298acb52446` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/universal-response-contract-v0.10-candidate.md` | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/public-falsification-plan-v0.7.md` | `07edb8ec3044874f39ed60f1a6952eb64e369715fc1501fd309888c9b24d09dd` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/review-response-v0.5.md` | `a15484c1f55ee388b2f6b49c25f67f549af6560b620a9b1ae128a080eedfd1d1` | matching sidecar |

No repository-wide search, history inspection beyond the exact baseline checks, E0 work product, sealed/private/oracle material, fixture, question, answer, schema, runner, implementation, output, or external source was used. Worktree separation was treated as edit isolation only.

## 2. Review rubric

- **PASS**: the authenticated proposal text uniquely determines the reviewed result without a result-affecting author, builder, comparator, custodian, or analyst choice. This does not mean implemented or validated.
- **FAIL**: a contradiction, missing normative definition, non-unique mapping, unsatisfied construction precondition, missing authorized transfer, or executable counterexample remains.
- **UNCLEAR**: materially different implementations remain permitted and the allowlisted public text does not select one.

Finding severities are:

- **blocking**: prevents CONTROL integration because an effective document, mandatory comparator result, or P0/P1 artifact cannot be uniquely constructed;
- **major**: materially breaks custody, blinding, reproducibility, fairness, or feasibility; and
- **minor**: a localized precision defect that must be corrected before freeze.

## 3. Independent effective-document reconstruction

### 3.1 Thirty-one-slot contract

**PASS for byte construction.** All three source digests authenticate, every named heading resolves exactly once, the full and preamble slices satisfy the stated level and ordering rules, and all 31 successor slots are classified exactly once. Heading metadata is ASCII-safe because only lowercase SHA-256 digests of exact UTF-8 heading text enter records. The U10 sidecar supplies a nonrecursive source digest.

Independent strict-UTF-8, raw-LF-preserving reconstruction produced:

```text
effective_contract_sha256=b110eb844e81c53ffdd3103cfbd26e57365487d89d8b19b2452f142e1e56d8a8
effective_slots=31
raw_slice_bytes=28518
effective_stream_bytes=38051
```

### 3.2 Twenty-five-slot plan

**PASS for byte construction.** P4-P7 authenticate, all headings and preambles resolve, and the 25 slots are classified once. In the authenticated raw P5 section 8 slice, lowercase ASCII `v0.8` occurs exactly once and uppercase ASCII `URC-0.8` occurs exactly once. The two ordered transforms therefore execute under their respective count-one preconditions. The complete record grammar emits one `slice_mode`, one `transform_count`, exactly two transform blocks only for slot 10, and ASCII heading digests instead of literal U+2014 metadata.

Independent reconstruction produced:

```text
effective_plan_sha256=864a53f07c678ef26971f19d0338d23a8f8fff232902727aefaad01bee03ddb0
effective_slots=25
raw_slice_bytes=50307
transformed_slice_bytes=50309
effective_stream_bytes=58650
```

These are independent in-memory design-review computations. They are not implementations, frozen manifests, or execution results.

## 4. Required predecessor-finding dispositions

| Finding | Decision | Independent v0.10 assessment |
|---|---|---|
| V9-B01 — slot-10 transform cannot execute | **PASS** | The source inventory is correct at one lowercase and one uppercase occurrence, both count-one transforms execute sequentially, and the plan stream is computable. |
| V9-B02 — contradictory or non-unique plan record encoding | **PASS** | The contract and plan each publish one complete record grammar. Every field occurs once, heading text enters metadata by ASCII SHA-256, and the plan transform block location and count are unique. |
| V9-B03 — undefined inner record-ID order | **PASS** | `id_order_key` is canonical JSON scalar-string UTF-8; unsigned bytewise comparison is global over every listed record-ID collection before cause serialization. `R10`/`R2`, prefix, quote, backslash, punctuation, and presentation-order mutations are mandatory. |
| V9-M01 — lost balance and duplicate controls | **PASS AT PROPOSAL-TEXT LEVEL** | Every authorized N is divisible by 24, 12, and 8; each row must have exactly `N/24` questions; development examples and exact or skeleton-preserving swaps are prohibited; and a frozen duplicate-key specification and denylist must precede authoring. The future key implementation and authoring feasibility remain unverified. |
| Continuing V8-M02 — incomplete custody bijection | **FAIL** | Most previously missing paths are repaired, including transformation and simulation specifications and named-vault writes. The published claim that every only-output/store maps to an exact edge is still false; see V10-M01. |

## 5. New blocking finding

### V10-B01 — The effective contract omits the semantic-atom and strength definitions required by its comparator

- Severity: **blocking**
- Fact: effective slot 21 replaces U7 section 6 in full with U10 section 5. U7 section 6 therefore contributes no bytes to the effective contract.
- Fact: U10 section 5 defines cause references and selectors but does not define the semantic atoms, citation/obligation/correlation truth predicates, operational commitment strengths, `stronger(answer,truth)`, `permits_direct`, mechanical-reason truth, or semantic-reason truth that U7 section 6 had defined.
- Fact: retained U7 section 4.2 makes P3 `Y` depend on “every semantic atom,” retained U9 section 7.2 uses `stronger` and correlation/counterexample conditions in C2, C3, and C5, and retained U9 section 8.1 consumes citation, obligation, correlation, reason, and other false causes. The effective bytes do not supply the missing truth functions.
- Composition conflict: U10 says the replaced selectors “remain total,” while the effective map classifies U7 section 6 as replaced. Treating the omitted U7 definitions as silently inherited conflicts with the explicit slot construction; not treating them as inherited leaves required predicates undefined.
- Executable counterexample: let truth be `underdetermined; none`, submit `barred; none`, and supply a correlation violation. The omitted U7 strength table would classify the submitted row as stronger and make C2 true. An implementation using only the retained direct-permission rule can classify both rows as non-direct and make C2 false. Both choices are compatible with the effective bytes because no retained table defines strength. They yield different critical events, consumed causes, totals, and P3 `Y`.
- Consequence: two conforming builders cannot be required to agree on the comparator, mutation catalog, expected table, or P3 question outcomes. P0 and P1 are therefore not uniquely executable, despite the effective byte hash being unique.
- Minimum correction proposal: add a mapped normative slice that completely defines every semantic atom and availability dependency, the operational-strength function, `stronger`, `permits_direct`, reason predicates, and citation/obligation/correlation/affected truth functions. The successor map must state whether that slice is retained or replaced and then rerun exact reconstruction and hostile mutations.

## 6. New major finding and custody continuation

### V10-M01 — The matrix-ledger bijection still has unmatched declared outputs and store access

- Severity: **major**
- Fact: the registrar's matrix output includes signed status manifests in `registrar-store`, and the named-store table gives a public status reader access by signed digest. E00A-H and E01-E50 contain no write to or read from `registrar-store`; the role-to-edge index likewise lists no such edge.
- Fact: the judgment-comparison custodian's declared output is an equality digest plus an agreed semantic table. E43 transfers only the agreed semantic table.
- Fact: the adjudication-comparison custodian's declared output is an equality digest plus an agreed derived table. E45 transfers only the agreed derived table.
- Fact: section 4.2 claims every cross-role positive input and every `only output / store` maps to the exact edges. Ambient or implicit routing is forbidden.
- Consequence: the published edge set cannot satisfy its own zero-unmatched-output assertion. In particular, status and equality evidence may be silently discarded, stored ambiently, or transferred through an unlisted route, producing different custody records under the same plan.
- Minimum correction proposal: add literal store-write/read or recipient edges for `registrar-store` and the two comparison digests, then regenerate the role-to-edge index mechanically. If those outputs are intentionally unnecessary, remove them from the matrix/store declarations and explain how the downstream exact-pass gates are authenticated.

The added transformation specification in E00C, full statistical/catalog bytes in E01, explicit content/label/leakage/condition-map vault routes, and registrar authority over reviewed public specification grants otherwise close the exact V8-M02 examples recorded by the predecessor review.

## 7. Hostile checks and non-regression

| Required attack | Result | Assessment |
|---|---|---|
| source hashes, headings, slices, transforms, ordering, and stream lengths | **PASS** | Both effective streams are byte-unique and independently hashed in section 3. |
| transform occurrence inventory | **PASS** | Slot 10 has exactly one `v0.8` and one `URC-0.8`; both replacements increase content by one byte. |
| heading and metadata encoding | **PASS** | Exact heading lookup remains UTF-8; only fixed-length lowercase digests enter ASCII metadata. |
| global record-ID ordering | **PASS** | One canonical scalar-JSON byte key controls all listed inner arrays, unique unions, and citation witnesses; outer cause order uses the same unsigned-byte principle. |
| record-ID presentation-order divergence | **PASS AS WRITTEN** | Equal sets must sort before serialization; permutations, escapes, prefixes, and punctuation are required P1 mutations. |
| C4 dependent, target, extra, alias, and T/F/U behavior | **PASS; NO REGRESSION** | Exact branch-specific sources remain in retained U9 section 7.3, unrelated missing accepted IDs and extras remain M4, and identical dependent/target keys union once. |
| 28-cause and eight-availability bounds | **PASS AS ARITHMETIC** | `20+4+4=28`; `7*256=1,792`; all eight axes and their order remain named. |
| catalog arithmetic | **PASS AS ARITHMETIC** | `4*10*3*3*5*4*128=921,600`, `1+28+C(28,2)=407`, and `720*2^12=2,949,120`. Rejected abstract rows remain counted. |
| response/answer/field consequence levels | **PASS AS RETAINED TEXT** | Pre-parse invalidity, response-wide membership failure, answer-local failure, field availability, one-M5 behavior, and P3/P4 schema effects remain explicit. Semantic success itself fails under V10-B01. |
| exact 24-row bank balance | **PASS AS UNIMPLEMENTED REQUIREMENT** | Every selected N divides evenly and each row is fixed at `N/24`. |
| duplicate and development-example loopholes | **PASS AT POLICY LEVEL; IMPLEMENTATION UNVERIFIED** | Exact, development-example, and skeleton-preserving swap reuse are forbidden before labels; the future duplicate-key specification has not been authored or tested. |
| A-D source information and question opportunity | **PASS AS UNIMPLEMENTED REQUIREMENT** | Canonical fact IDs, record IDs, normalized content hashes, questions, grammar opportunities, and equality manifests remain common; only intended representation differs. |
| authority, tools, model, reasoning, time, and retry equality | **PASS AS UNIMPLEMENTED REQUIREMENT** | Exact revision/fingerprint, reasoning, tier, region, limits, authority, tools/network, one turn, first output, and no retry remain common. |
| P2 hypotheses, dependence grid, mappings, and alpha arithmetic | **PASS AS UNEXECUTED DESIGN** | Probabilities remain valid, all dependence sums are below one, and `4*0.00625+2*0.0125=0.05`. |
| P3 marginal grid, estimator, and schedule | **PASS AS UNEXECUTED DESIGN** | Null probabilities remain within `[0.45,0.95]`; all authorized K values have remainder 2 or 6 modulo 8, and the construction balances position and wave without seed redraw. |
| call and visible-token arithmetic at N=720 | **PASS AS ARITHMETIC** | P2 has 240 calls, P3/P4 has 720 first-output calls, total calls are 960, visible input is 53,760,000 tokens, and visible output is 3,194,880 tokens. |
| human, compute, storage, calendar, and monetary ceilings | **PASS AS WRITTEN STOPS; UNVERIFIED** | The ledger totals 240 hours and catalog projections are included in the pre-authoring benchmark; no feasibility run exists. |
| role, custody, and ACL completeness | **FAIL** | V10-M01 leaves unmatched declared outputs despite otherwise substantial repairs. |
| circularity and post-result discretion | **PASS** | Pre-bank seeds exclude the bank hash; expected generators freeze before comparator output; labels and analysis freeze before map release; threshold changes require a new reviewed version and untouched bank. |
| runner and answer leakage | **PASS AT THE LIMITED TEXTUAL CLAIM** | Neutral runner vocabulary, signed typed generation, paired scans, and semantic reviewers remain required; zero paraphrased leakage is not claimed. |
| rollback, sealed/oracle boundary, and S0-E0 separation | **PASS** | Failure preserves authenticated evidence, exposed banks are not reused, and no sealed, real, E0, or later-gate material is authorized. |
| claim ceiling | **PASS** | Even the future-pass sentence remains limited to one frozen synthetic public experiment and excludes S0, system, safety, economic, and transfer claims. |

Passed rows are design-text, arithmetic, or construction results only. They are not implementations, measurements, empirical effects, or validation results.

## 8. Facts, inferences, and correction proposals

### 8.1 Facts established by this review

- The exact baseline and thirteen input digests passed authentication.
- Both effective byte streams are mechanically reconstructable at the hashes and byte counts in section 3.
- V9-B01, V9-B02, V9-B03, and V9-M01 have written successor controls that pass at the stated proposal-text level.
- U7 section 6 is absent from the effective contract, while retained clauses still consume its former terms.
- The ledger has no exact route for `registrar-store` status manifests or the judgment/adjudication comparison digests.
- No implementation or empirical result was inspected or created.

### 8.2 Review inferences

- A unique document hash does not make its semantics executable when mandatory comparator functions are absent.
- Undefined `stronger` and semantic atoms can change critical events, M events, cause consumption, and P3 outcomes, so V10-B01 is result-affecting rather than editorial.
- Exact custody matters because the plan expressly denies ambient access and invalidates unlisted transfers.
- Correct construction, ordering, balance, arithmetic, and fairness controls cannot compensate for a blocking semantic contract or a major custody mismatch.

### 8.3 Correction proposals

- The minimum corrections in sections 5 and 6 are proposals, not approved design decisions.
- A successor can preserve the authenticated byte grammars, ID order, C4 repair, balance controls, statistical design, resource stops, and bounded claim while adding the missing semantic slice and closing the remaining ledger edges.

## 9. Maximum justified claim

The maximum defensible claim is:

> At commit `72ab5204646f9e088a828e88c9b604254edab50e`, the authenticated URC-0.10 package is an unimplemented public redesign proposal. Its 31-slot contract and 25-slot plan are independently reconstructable; its transform grammar, heading encoding, global record-ID order, bank balance, duplicate policy, C4 repair, catalog arithmetic, and many synthetic-test controls are coherent at proposal-text level. It is not suitable for CONTROL integration because the effective contract omits mandatory semantic-atom and strength definitions, and the custody matrix still has unmatched declared outputs.

No claim is authorized for an executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 10. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions can satisfy metadata, target, alias, four-ID, balance, and duplicate-key constraints without distortion.
- Whether independent labelers, scanners, generators, comparators, leakage reviewers, judges, and map builders can agree exactly.
- Whether catalogs, two generations, comparison, signatures, 200 comparator runs, and review fit the human, compute, storage, calendar, and monetary ceilings.
- Whether named ACL stores, write-only raw delivery, an immutable model fingerprint, and durable monotonic timestamps are operationally available.
- Whether calibration and power pass the frozen grids; no generalization outside those grids is authorized.

## 11. Exact next-gate recommendation

Do not open CONTROL integration, public bank authoring, schema or runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7-v0.10 artifacts and this review. The only appropriate successor action is a separately authorized `F0-PUBLIC QUESTION CONTRACT V0.11 REDESIGN OPEN`, followed by another fresh public-only independent review. No later gate opens automatically.

## 12. Final verdict

**REVISE-AND-REVIEW**
