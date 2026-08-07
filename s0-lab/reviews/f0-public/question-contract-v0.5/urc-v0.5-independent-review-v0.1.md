# URC-0.5 independent hostile review v0.1

- review type: `fresh public-only hostile read-only review`
- reviewed candidate: `URC-0.5-CANDIDATE`
- reviewed plan: `URC-0.5 public falsification plan v0.2`
- final verdict: **REVISE-AND-REVIEW**
- authority: review and CONTROL-integration suitability only
- not authorized: schema, fixture, question, answer, oracle, implementation, simulation, executor work, S0 run, sealed access, or downstream gate

## 1. Input boundary and authentication

The reviewer read only the authorized public inputs. Repository history, E0 material, sealed/private/oracle material, sibling output, and external sources were excluded. No file changes, implementation, fixture authoring, simulation, or S0 execution occurred in the review session.

| Input | Verified SHA-256 |
|---|---|
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| Protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.4 candidate | `1a06737a8f7de90bdb8c0c467cf3bc0ccab236ced91e3fb364e91ea1dc1d4a82` |
| Falsification plan v0.1 | `9649bcffa2b8d39a03077b7797e537912525ed664d57486fd28466b0ca0440a8` |
| v0.4 independent review | `07e06f4735fc85438071a36522ac6f07d6b812bf3cbfee0e7f4b59044bfaaec9` |
| v0.4 CONTROL decision | `27a6513dea6ed7dc7bbfe3ea8c04c4ad7cab775bd7846594bc0166ef76a6ae6c` |
| URC-0.5 candidate | `d081f67861447616aa961ef75920c4f0c317fd13e3273bf1ef5bf36edb31d52f` |
| Falsification plan v0.2 | `e6288cdf9275644223ba65a418c029dd0878c157847a4ea426f029cc7c40a0ef` |

The two predecessor paths that differed from the review prompt were resolved only by narrow basename lookup:

- `s0-lab/reviews/f0-public/question-contract-v0.4/urc-v0.4-independent-review-v0.1.md`
- `s0-lab/control/f0-public/question-contract-v0.4/independent-review/independent-review-decision-v0.1.md`

`AGENTS.md` was read fully as the governing instruction file. No `AGENTS.sha256` was listed or present.

## 2. v0.4 rejection-reason closure

| v0.4 rejection reason | Result | Assessment |
|---|---|---|
| Globally exclusive combined-record outcomes | **FAIL** | The ordered predicate function is single-valued, but some rows contradict positive route predicates suppressed by precedence. |
| Preserve C1-C7/M1-M6 without cascade double-counting | **FAIL** | An invalid decision pair can make both `F` and `D` false and score M5 plus M3 for one defect. Coarse token consumption can also suppress independent failures. |
| Author-independent observation-to-error mapping | **FAIL** | Hazard predicates and source-token selection remain qualitative rather than complete Boolean algorithms. |
| Complete P2 family, alpha, paired equivalence, and power | **FAIL** | The family and nominal allocation are explicit, but the power seed is circular and percentile-bootstrap bounds do not establish the declared finite-sample error control. |
| Exact P3 control, estimator, unit, covariance, resampling, CI, and sample rule | **UNCLEAR** | The components are substantially specified, but covariance sensitivity is narrow, scheduling is open, and the combined sample selector cannot run as written. |
| Model, token, human, elapsed, and monetary ceilings | **PASS** | All requested ceiling categories are stated; feasibility fails separately. |
| Normative canonical JSON bytes | **PASS WITH MINOR DEFECT** | Serialization is substantially normative; raw-NFC handling and the meaning of one line need final precision. |
| Mechanical exclusion of answer-bearing examples | **FAIL** | Provenance and exact-token scanners cannot exclude paraphrased free-text worked traces before an artifact is signed. |

Not every v0.4 rejection reason is closed.

## 3. Blocking findings

### B-01 — Total function can return a semantically false handling value

- Failed claim: combined-record predicate vectors produce one truthful disposition-and-route result.
- Evidence: candidate sections 3.2-3.3 define `human_decision` as an identified authorized human route and R03 as no authorized alternative. Section 4.1 makes `human_route=true` when that route exists. Section 4.2 nevertheless maps every `operation_barred=true` case without `data_only_route` to R03 even when `human_route=true`.
- Adversarial trace: `binding_conflict=false`, `operation_barred=true`, `human_route=true`, `data_only_route=false` returns R03, contradicting the positive human route. A conflict with a valid data-only route can likewise suppress that route.
- Minimum correction: perform an exhaustive truth-condition review over all 32 predicate vectors. Every selected row must be entailed by every positive predicate it claims to report. Resolve barrier-plus-route cases structurally instead of discarding route facts by precedence.

### B-02 — Consumption tree permits cascade double-counting

- Failed claim: one mismatch cannot be scored twice while disjoint failures remain observable.
- Evidence: candidate section 6.2 includes allowed decision row in `F`, while `D` tests equality with the accepted row. A parseable invalid pair produces `F=false` and `D=false`; section 6.4 then emits M5 and later M3.
- Additional inconsistency: protocol v0.3 distinguishes unparsable or missing output as suite-invalid rather than M5. Candidate section 6 appears to emit M5 without preserving or explicitly replacing that boundary.
- Minimum correction: define dependency-aware token availability and consumption. A format defect that invalidates semantic comparison must not independently create a semantic mismatch. Explicitly retain or version the suite-invalid versus M5 boundary.

### B-03 — Critical mapping is not author-independent

- Failed claim: standardized metadata and the universal tree eliminate local judgment in C1-C7 assignment.
- Evidence: section 6.3 relies on qualitative predicates such as treated as independent support, strengthened, failed to reach, treated as authority, and displaced. Section 6.4 requires a documented source-token set but supplies no exact Boolean or source-selection algorithm. Section 6.5 lists possible tokens rather than executable truth conditions.
- Consequence: overlapping critical predicates can be selected by numeric order, and a coarse source set can consume an unrelated citation failure.
- Minimum correction: freeze exact metadata schemas, decision-strength ordering, Boolean formulas, and source-token consumption sets for every critical predicate, including an exhaustive overlapping-hazard truth table.

### B-04 — P2 power selection has an impossible seed dependency

- Failed claim: the plan deterministically selects the smallest sufficient `N` before bank authoring.
- Evidence: the freeze order requires `N` and simulation seeds before fact authoring, but P2 power inherits a seed containing `<frozen-bank-hash>`.
- Consequence: the bank hash does not exist until after selecting the sample size that governs bank authoring.
- Minimum correction: derive prospective-power seeds only from immutable pre-bank artifacts, candidate `N`, grid ID, and simulation-version identifiers. Define confirmatory-analysis bank-hash seeds separately.

### B-05 — Nominal bootstrap quantiles do not establish declared alpha control

- Failed claim: P2 controls familywise type-I error at 0.05 and P3 supplies a valid 90% equivalence interval.
- Evidence: Bonferroni arithmetic is explicit, but percentile cluster-bootstrap quantiles are treated as confidence bounds without finite-sample coverage justification. P2 can have only 20-60 clusters. Power is simulated under alternatives rather than false-pass behavior at the null boundaries. P3 similarly tests power at `theta=0`, not interval size at `theta=±0.10`.
- Minimum correction: add frozen boundary-null size calibration over the authorized dependence grid or adopt a justified conservative cluster method, with calibration applied before power and sample selection.

### B-06 — Answer-bearing prose is not mechanically excluded

- Failed claim: every answer-bearing runner example is mechanically blocked.
- Evidence: exact tokens, populated envelopes, identifier-row co-occurrence, provenance, and known mutations are scanned, while free-text `instruction` and `codebook` artifacts remain allowed.
- Counterexample: a paraphrased worked trace can omit exact enum tokens, row labels, IDs, and response envelopes while teaching which semantic outcome to choose.
- Minimum correction: generate instructions and codebooks from a closed typed representation with exact allowed fields and strings. If semantic free text is unavoidable, require separate pre-signing semantic leakage review and narrow the claim.

## 4. Major findings

### M-01 — Prospective power procedure is not operationally feasible

- The plan nests 200,000 bootstrap replicates inside 100,000 simulated datasets.
- P2 has 18 grid points and P3 has 81 grid points per candidate `N`; all five candidate sizes can approach 9.9 trillion inner bootstrap analyses.
- No compute-hour or storage ceiling, benchmark, or evidence connects this procedure to the 30-day and USD 3,000 ceilings.
- Minimum correction: benchmark a frozen implementation before authoring, add compute/storage ceilings, and replace nested simulation with a validated cheaper procedure where possible. Re-review numerical changes.

### M-02 — Run scheduling can confound grammar and representation

- Eight P3 cells per packet are fixed, but three concurrent sessions can span 30 days without seeded run order, balanced waves, grammar/representation rotation, or drift invalidation.
- Provider revision, load, and time effects can align with grammar or A-D and contaminate elapsed-time comparisons.
- Minimum correction: freeze a deterministic balanced schedule and concurrency-wave allocation, record revision/load evidence, and define pre-result drift invalidation rules.

### M-03 — P3 invalid-cell handling conflicts with P4 burden threshold

- P3 invalidates any missing or invalid cell, while P4 permits URC first-output schema conformity as low as 95%.
- If schema-invalid output invalidates P3, P3 implicitly requires 100%; if it counts as `Y=0`, the plan does not say so.
- Minimum correction: distinguish technical absence, unparsable output, schema-invalid output, and semantically wrong output, with exact P3 consequences aligned to P4.

### M-04 — Exact role isolation contracts are deferred

- Roles are named, but exact allowed inputs, forbidden inputs, outputs, fork ancestry, and storage boundaries are left for later gates.
- Minimum correction: freeze a per-role allowlist/denylist and ancestry/output-transfer matrix before public authoring. Worktree separation must not be treated as secret isolation.

## 5. Minor finding

### m-01 — Canonical-text boundary rules remain ambiguous

- Candidate section 7.1 does not say whether a non-NFC raw response is rejected or normalized before semantic comparison and limits.
- One line is not defined for Unicode separators such as U+0085, U+2028, and U+2029.
- Minimum correction: freeze raw-input normalization or rejection order and the complete prohibited line-break set.

## 6. Rubric

| Item | Result |
|---|---|
| Frozen-input integrity | **PASS** |
| Globally exclusive and truth-consistent combined-record outcomes | **FAIL** |
| C1-C7/M1-M6 observable preservation | **FAIL** |
| No cascade double-counting | **FAIL** |
| Author-independent observation-to-error mapping | **FAIL** |
| Complete P2 family and nominal alpha allocation | **PASS** |
| P2 paired estimand/equivalence specification | **PASS** |
| P2 executable power and valid error-control rule | **FAIL** |
| P3 control artifact and semantic equivalence | **PASS** |
| P3 estimator, session unit, resampling, and CI algorithm | **PASS** |
| P3 covariance adequacy and deterministic sample selection | **UNCLEAR** |
| Complete model/token/human/elapsed/monetary ceilings | **PASS** |
| Resource feasibility within those ceilings | **FAIL** |
| Normative canonical JSON byte serialization | **PASS** |
| Mechanical answer-example exclusion | **FAIL** |
| Internal consistency | **FAIL** |
| Public falsifiability and noncompensatory stopping | **PASS** |
| Implementability without hidden discretion | **FAIL** |
| A-D equality requirements | **PASS AS DESIGN REQUIREMENT; UNVALIDATED** |
| Role isolation | **UNCLEAR** |
| Sealed/private/oracle boundary | **PASS** |
| Prevention of CONTROL design traces becoming runner input | **UNCLEAR** |
| Claim and rollback limits | **PASS** |

## 7. Maximum claim and next gate

The maximum defensible claim is:

> URC-0.5 and public falsification plan v0.2 are authenticated public design proposals that substantially specify a candidate total-function grammar, canonical JSON format, P3 control experiment, and operating ceilings, but independent review has identified unresolved blocking semantic, scoring, P2, visibility, and implementability defects.

No fixture authoring, executable schema, implementation, public validation, sealed access, executor work, S0 result, representation superiority, central-system result, Project Brain integration, safety, economic, or transfer claim is authorized.

Do not open CONTROL integration, public authoring, implementation, or execution. Preserve the reviewed v0.5 artifacts at their current hashes and open only:

`F0-PUBLIC QUESTION CONTRACT V0.6 REDESIGN OPEN`

A versioned successor must address the blocking findings and then receive a fresh independent public-only review.

## 8. Final verdict

**REVISE-AND-REVIEW**
