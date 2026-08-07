# Independent design review — URC-0.4 candidate

## 1. Authenticated-input statement

I used only the following CONTROL instructions and substantive allowlist. I did not search the repository, inspect Git history, read sealed staging or sealed content, use outside sources, or modify/create any file. The allowlisted predecessor decision under `f0-sealed/` is a public CONTROL record; it contains no sealed questions, facts, answers, or oracle material.

CONTROL instructions authenticated:

| Path | Computed SHA-256 |
|---|---|
| `s0-lab/control/f0-public/question-contract-v0.4/independent-review/independent-review-gate-record-v0.1.md` | `fa1f6082ac2d6555cef7180e4bf4d584a3acb3b3ad322485875b9cbb4e5eb04b` |
| `s0-lab/control/f0-public/question-contract-v0.4/independent-review/independent-review-brief-v0.1.md` | `33d8d2856787f8b64152b2a0cf99d61f5a5c77ed634da046d5f119a8ba3302fa` |

Both values exactly matched their `.sha256` sidecars.

Substantive allowlist authenticated:

| Path | Computed SHA-256 |
|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| `s0-lab/control/sm0/answer.schema.json` | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` |
| `s0-lab/control/sm1/question-options.schema.json` | `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` |
| `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-decision-v0.1.md` | `7230ac449d06a4eb4ea74887d1bf163bb3e6ed9808077f27e7d1e19dff154703` |
| `s0-lab/control/f0-public/question-contract-v0.4/f0-public-question-contract-v0.4-gate-record.md` | `d1f2a41a4cfccf1e8e3e6bb8ceee186648e6dc2c4ea540f71e4b25f57a7aa806` |
| `s0-lab/control/f0-public/question-contract-v0.4/universal-response-contract-v0.4-candidate.md` | `1a06737a8f7de90bdb8c0c467cf3bc0ccab236ced91e3fb364e91ea1dc1d4a82` |
| `s0-lab/control/f0-public/question-contract-v0.4/public-falsification-plan-v0.1.md` | `9649bcffa2b8d39a03077b7797e537912525ed664d57486fd28466b0ca0440a8` |
| `s0-lab/control/f0-public/question-contract-v0.4/control-design-assessment-v0.1.md` | `18be3f037ebed89f030dc3109f3b26566a2d5a39151980722009fe19cf69b1f7` |

The three frozen predecessor artifacts retain their frozen hashes. URC-0.4 proposes successor versions and does not edit those artifacts in place. This is a current-file integrity finding, not a Git-history claim.

## 2. Reproduced calculations and adversarial analyses

### Six-pair semantics

The matrix count is correct: four dispositions multiplied by four handling values gives 16 Cartesian pairs; six are admitted and ten rejected.

Abstract countercases:

- `prohibit + none`: a record expressly bars the named operation and authorizes no alternative handling.
- `prohibit + data_only`: a record bars the effectful operation but permits bounded local information handling.
- `defer + none`: the records do not justify a binding decision and identify no authority route.
- `defer + human_decision`: the records reserve the unresolved binding decision to an identified human authority.
- `preserve + none`: an established state is expressly to remain in force, with no new operation.

These meanings can be recovered from records when records cleanly contain only one basis. They are not globally exclusive when records contain ordinary combined statements. “Do not replace the active state; it remains active” supports both `prohibit + none` and `preserve + none`. “The decision remains pending; until then the current state remains” supports both `defer + none` and `preserve + none`. The contract supplies no global precedence rule for such overlaps. Requiring exactly one accepted pair therefore risks hiding semantic disagreement as question rejection.

Removing a separate `state_effect` output is defensible when the prompt unambiguously names the operation: repeating “start,” “limit,” “pause,” or “end” would often score prompt recognition rather than record reasoning. However, `preserve` reintroduces a state-effect proposition inside `disposition`, where it overlaps the negative and pending dispositions. The removal is therefore only partly successful.

### Determinism and scoring

For a schema-conforming answer with a wrong decision, wrong citation, and wrong affected set, the fixed precedence emits decision mismatch as the one primary event; citation and affected-set mismatches are diagnostic and unscored.

That prevents coordinate double-counting, but it is stricter than predecessor v0.3, which permits independently caused C/M errors while capping each code once per block. In particular, it can suppress M1, M4, or the affected-scope evidence needed for C4. A later question-specific C/M mapping cannot recover an observation that the universal precedence has already made unscored. Those future mappings are also not yet governed by a universal mapping rule.

### Leakage and alignment

The response fields and six rows are identical across questions, which removes the predecessor’s visible per-question option shape. No direct D relation-code vocabulary appears in the contract.

Nevertheless, `disposition`, `handling`, authority routing, and state preservation can map more naturally onto C’s state/scope fields or D’s explicit relations than onto A/B raw-record presentations. This is a semantic-alignment risk, not direct lexical D leakage.

The named operation does not deterministically fix the exact response pair, but it can strongly constrain likely classes. That is legitimate only if the no-record test treats such predictability as measured leakage.

The document also contains one concrete serialization using `defer + human_decision`. It is called unscored, but it is not explicitly classified as CONTROL-only and excluded from every runner-visible package. If shipped, it would give all conditions the same but asymmetric answer prior.

The proposed single-code control has the right high-level purpose, but its codebook, schema, lexical construction, nondecision fields, byte layout, mapping burden, and session unit are not specified. Consequently, a measured difference could combine grammar alignment with control-format artifacts.

### Statistics

For the leakage test, the balanced exact-tuple chance rate is correctly `1/6`.

Solving the one-sided 97.5% Clopper–Pearson upper-bound equation gives:

- 33 correct of 180: upper bound `0.2477193027`;
- 34 correct of 180: upper bound `0.2538212696`.

Thus “at most 33” and the stated approximate 24.77% bound are correct.

The original two observer streams receive a valid 2.5% one-sided allocation each for an overall 5% Bonferroni budget. The neutral-token variants create two additional blocking confidence tests, however, without reallocating that budget across all four tests. Four tests at 2.5% each can have familywise error as high as approximately 9.63% absent dependence assumptions.

The paired five-point rule is also not an equivalence test. Five percentage points is nine questions at `n=180`; the exact paired test has no specified null, alpha, rejection/pass direction, or power requirement. Its precision depends on discordant pairs. Under maximal discordance, the standard error of a paired accuracy difference can be about 7.45 percentage points, with a 95% half-width near 14.61 points. Therefore an observed difference within five points does not establish bounded lexical sensitivity.

The P3 ±10-point, two-sided 90% CI rule is a legitimate equivalence form, and the requirement for at least 80% prospective power at true zero is directionally correct. It is not operationally complete. “Paired randomization or bootstrap,” expected control accuracy, within-question covariance across eight observations, allocation, simulation model, and the exact sample-size escalation algorithm remain open. Expected control accuracy alone does not determine the variance of the difference-in-differences estimand. Increasing beyond 180 before data is not a post-result change, but the resulting sample size is not reproducible from the present plan.

### Resources and operating topology

The stated arithmetic is correct:

`8 × 896 + 512 = 7,680`, leaving 512 bytes under 8,192.

The field caps support an even smaller compact bound. With 40-byte question and record IDs, four cited IDs, four affected IDs, a 160-byte already-escaped reason, the longest valid disposition/handling text, and fixed ASCII keys, a compact answer object is at most about 701 bytes. Eight such objects plus the current fixed compact envelope are about 5,817 bytes. Thus a compact valid serialization exists well below both limits.

This does not imply a first model output will be compact or valid. Whitespace and other first-output behavior can still exceed 8,192 bytes; the candidate correctly separates that empirical burden test from the analytic bound. A normative canonical-serialization algorithm and exact “after escaping” measurement procedure still need freezing.

P3 entails 180 questions × four representations × two grammars = 1,440 question-level observations. If up to eight questions share each fresh one-turn block session, the minimum is `8 × ceil(180/8) = 184` P3 sessions; if freshness applies per question, it is 1,440. P2 explicitly requires 30 fresh sessions for the original prompts, and symmetry-preserving fresh neutral runs would add another 30, for at least 244 model sessions under the lower P3 interpretation. The plan does not resolve this topology.

Missing budget variables include model input/output token counts for each representation, codebook and schema overhead, enlarged-bank size, observer and executor pricing, invalid-bank replacement, human author/label/judge time, comparator implementation and 200 repeated suite executions, concurrency, elapsed time, and reserve-bank cost. No price can be estimated from the allowed inputs.

## 3. Rubric

| Dimension | Score | Written deduction |
|---|---:|---|
| Semantic coherence and intended-decision coverage | 7/20 | The six rows cover the predecessor decision families abstractly, but `preserve` overlaps `prohibit` and `defer`; exact-one acceptance lacks a global exclusivity rule. |
| Answer-shape leakage resistance | 9/20 | Universal fields and prompt restrictions are improvements. Deducted for the potentially runner-visible single-pair example, incomplete neutral-test multiplicity, and unresolved operation-word leakage. |
| Deterministic adjudication and no double-counting | 5/15 | Atomic booleans and fixed precedence are deterministic, but the precedence suppresses independently meaningful predecessor observables, while later C/M mappings remain unspecified. |
| A–D and two-block measurement fairness | 7/15 | Same sources, question hashes, authority, model settings, time, tools, limits, and scoring opportunity are specified. Delivery is unverified, and the C/D alignment control is not operationally complete. |
| Statistical validity and falsifiability | 6/15 | The 33/180 calculation and basic equivalence criterion are correct. Neutral multiplicity, paired-rule power, joint simulation model, estimator choice, and sample escalation remain defective or open. |
| Resource, operating-cost, and one-person feasibility | 5/10 | The serialization budget is analytically safe. Session topology, full cost, human workload, and a ceiling remain unspecified and potentially material. |
| Versioning, rollback, role isolation, and claim boundaries | 5/5 | Versioning, fresh-bank rules, no post-result threshold change, rollback, role isolation, and bounded claims are explicit. |
| **Total** | **44/100** | Noncompensatory failures control regardless of total. |

## 4. Noncompensatory checks

| # | Result | Reason |
|---:|---|---|
| 1 | **FAIL** | Individual pairs are interpretable, but `preserve` overlaps `prohibit` and `defer` without a global exclusivity rule. |
| 2 | **FAIL** | Predecessor families can be named, but common combined records can justify multiple pairs unless prose interpretation or question rejection supplies the missing priority. |
| 3 | **NOT YET DEMONSTRATED** | Static question-specific shapes are removed, but prompt-operation leakage and the status of the serialization example remain untested. |
| 4 | **FAIL** | The one-primary precedence can suppress citation/scope errors, including observables essential to predecessor C/M logic. |
| 5 | **FAIL** | Information, authority, model, time, and opportunity equality are specified, but grammar alignment is unresolved and the proposed noncompensatory P3 control is not fully specified. |
| 6 | **FAIL** | Chance, 33/180 ceiling, and the original two-stream correction are valid; the two neutral variants expand the blocking family without confidence-budget reallocation, and the paired rule lacks a reproducible inferential pass rule. |
| 7 | **FAIL** | The equivalence margin is sound in form, but the control, estimator, covariance model, session allocation, and sample-size escalation rule are not operationally fixed. |
| 8 | **PASS** | The field limits imply a compact object below 896 bytes and the formula remains below 8,192; first-output compliance is correctly left empirical. |
| 9 | **NOT YET DEMONSTRATED** | The plan is public-only and excludes pilot confirmation, but operational cost and role/session topology are unresolved. This status is acceptable only while the next gate remains limited to authoring-protocol and cost design, with no fixture creation. |
| 10 | **PASS** | The package makes no implementation, sealed-compatibility, S0, safety, economic, central-system, Project Brain, or transfer claim. |

## 5. Findings by severity

### C-01 — Critical: global decision rows are not mutually exclusive

- **Verified fact:** `prohibit`, `defer`, and `preserve` all prevent the named operation now; `preserve` additionally states that an existing state remains.
- **Reviewer inference:** Ordinary records can support two rows simultaneously, so exact-one acceptance is not recoverable from the grammar alone.
- **Falsification or correction needed:** Define and adversarially test a universal, record-derived exclusivity/precedence rule, or replace the overlapping value set. It must work without prompt hints, multiple accepted pairs, or prose interpretation.
- **Consequence if unresolved:** Public authors will hide grammar ambiguity as question rejection or discretionary labeling; noncompensatory checks 1 and 2 remain failed.

### C-02 — Critical: fixed field precedence suppresses predecessor observables

- **Verified fact:** A decision mismatch always precedes citation and affected-set mismatches, which become unscored.
- **Reviewer inference:** Independently caused M1/M4 errors, and potentially C4 evidence, can disappear from the scored record.
- **Falsification or correction needed:** Produce an abstract trace for every predecessor C/M family showing that one primary event still preserves every essential critical observable, with severity-aware and cause-aware rules frozen globally.
- **Consequence if unresolved:** URC results would not remain comparable to the predecessor C/M logic.

### C-03 — Critical: P2 multiplicity and paired sensitivity are incomplete

- **Verified fact:** Two original and two neutral blocking confidence tests are contemplated, while 97.5% bounds are justified only as a two-test Bonferroni allocation. The paired test is merely “reported.”
- **Reviewer inference:** P2 lacks a valid familywise confidence rule for its full blocking family and has no powered five-point equivalence decision.
- **Falsification or correction needed:** Freeze the full hypothesis family, alpha allocation, paired estimand, confidence interval or exact equivalence rule, multiplicity correction, and prospective power.
- **Consequence if unresolved:** A claimed leakage pass would exceed its stated error budget and would not substantiate neutral-token robustness.

### C-04 — Critical: the representation-alignment control is not reproducible

- **Verified fact:** The plan leaves “randomization or bootstrap,” control construction, covariance assumptions, simulation inputs, session allocation, and exact enlarged sample size open.
- **Reviewer inference:** The single-code comparison cannot yet isolate two-field grammar alignment, and two analysts need not obtain the same power or equivalence decision.
- **Falsification or correction needed:** Specify the complete control artifact, neutral code mapping, common fields, session unit, estimator, resampling unit, CI algorithm, joint simulation model, and deterministic smallest-sample rule before bank creation.
- **Consequence if unresolved:** A C/D-relative advantage could be missed, induced by the control, or decided through pre-analysis discretion.

### M-01 — Major: operating feasibility and cost are not bounded

- **Verified fact:** The design implies at least 1,440 P3 question-level observations, many fresh sessions, two full label sets, duplicate judging, and 200 comparator repetitions; no ceiling is supplied.
- **Reviewer inference:** One-person operation may be unaffordable or may pressure later reductions in separation or sample size.
- **Falsification or correction needed:** Freeze session topology, token and time estimates, human-work estimates, enlarged-sample contingency, and a stop-before-authoring monetary ceiling.
- **Consequence if unresolved:** The plan may be formally rigorous but operationally unusable, or vulnerable to convenience-driven threshold changes.

### M-02 — Major: the serialization example has ambiguous visibility

- **Verified fact:** The candidate shows only `defer + human_decision` in an executor response example and labels it unscored, but does not explicitly exclude it from runner-visible artifacts.
- **Reviewer inference:** If shipped, it supplies an asymmetric answer prior despite equal exposure across A–D.
- **Falsification or correction needed:** Mark the example CONTROL-only and require runner-manifest verification that no answer-bearing example appears in prompts, codebook, schema annotations, or package metadata.
- **Consequence if unresolved:** P2 can measure example priming rather than intrinsic contract leakage.

### M-03 — Major: later C/M mappings retain hidden discretion

- **Verified fact:** The candidate leaves each question’s primary observation-to-error-code mapping to a later scoring format.
- **Reviewer inference:** Pre-result freezing prevents post-result manipulation but does not establish that different authors will map the same abstract failure identically.
- **Falsification or correction needed:** Define a universal mapping decision tree or require independent exact mapping agreement on a frozen public mutation set before authoring.
- **Consequence if unresolved:** Deterministic field comparison can still yield discretionary scores.

### m-01 — Minor: canonical serialization needs a normative definition

- **Verified fact:** Field limits imply a safe compact size, but “canonical serialization” and “after escaping” are not fully defined.
- **Reviewer inference:** Independent serializers could disagree on the 160-, 896-, or 7,680-byte checks.
- **Falsification or correction needed:** Freeze UTF-8 encoding, whitespace, escape rules, property ordering if required, and byte-measurement timing.
- **Consequence if unresolved:** Boundary cases can fail inconsistently even though the analytic headroom is ample.

## 6. Severity-count summary

| Severity | Count |
|---|---:|
| Critical | 4 |
| Major | 3 |
| Minor | 1 |

## 7. Three most important findings

1. The six-row grammar is not exclusive: `preserve` overlaps both negative and pending dispositions.
2. The universal mismatch precedence can hide predecessor-critical observables rather than merely prevent double-counting.
3. The C/D alignment test is not yet a reproducible equivalence experiment because its control, estimator, covariance model, and sample rule remain open.

## 8. Bounded corrections required

Corrections should remain confined to this public question-contract package:

1. Redesign the six-row semantics into a globally exclusive decision rule and repeat the abstract countercase review.
2. Replace generic field-order precedence with a rule that preserves every essential predecessor C/M observable while still emitting at most one primary scored event per question.
3. Correct P2 across the complete four-test family and replace the observed five-point red flag with a powered paired equivalence rule.
4. Fully specify the single-code control, P3 estimator, session unit, joint simulation, and deterministic sample-size escalation.
5. Explicitly exclude answer-bearing examples from runner-visible artifacts.
6. Freeze public-test topology and cost ceilings before authoring.
7. Define canonical serialization exactly.

These changes do not authorize fixtures, schemas, code, runs, sealed access, executors, or S0.

## 9. Remaining unknowns and prohibited claims

Unknowns include whether a revised grammar can represent a varied public bank uniquely, whether no-record observers remain below the leakage ceiling, whether C/D receive a grammar advantage, whether first outputs satisfy format and byte limits, whether A–D delivery artifacts actually preserve equal sources/authority/model/time/opportunity, whether the full test is affordable, and whether any held sealed material fits the limits.

No conclusion may be drawn about sealed compatibility, S0 execution or success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, representation superiority, or model-to-model transfer. This review authorizes no subsequent work.

## 10. Verdict

**URC-0.4 requires question-contract redesign.**
