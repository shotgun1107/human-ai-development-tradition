# E0 measurement and analysis plan v0.4

- Status: `revision proposal — awaiting fresh independent review, pre-result design only`
- Applies only to a future separately approved A/D pilot, A/B/D confirmation or separately designed C/D diagnostic.
- Current output: definitions and future freeze requirements; no sample, oracle, score, calculation, simulation or result
- Currently prohibited: materials, tasks, answers, oracle, rubric, prompt, schema, code, model calls, scoring, statistical execution and effect claims

## 1. Facts, inference and proposal

### 1.1 Facts

1. E0 has no results.
2. The v0.3 review passed the alignment of the family-weighted estimands, `δ ≤ Δ` nulls, lower-bound pass rules, endpoint-specific counts and vector power structure.
3. The review found that the vector stopped before family-dependent human time and cash, allowing a future scalar operational total to hide a deficient relevant, harm or reserve set.

### 1.2 Inference

A total number of families is not an inferential sample size when endpoints use different family sets. Likewise, a total number of human hours or total human cash is not a set-feasibility demonstration when marginal work depends on `F_R`, `F_H` and their reserves. Every confirmatory endpoint and every family-dependent resource must retain named membership until its own requirement and ceiling pass.

### 1.3 Proposal

v0.4 preserves two disjoint confirmatory family populations, all eight endpoint rows and power over `(N_relevant, N_harm)`. It adds a nonoptional operating propagation contract for `F_R`, `F_H`, `F_R_reserve` and `F_H_reserve`, separately for human active, waiting and calendar time, compensation and replacement cash. Shared fixed overhead stays explicit and uses a frozen allocation rule before totals. A scalar union or total remains reporting-only.

## 2. Frozen family populations and allocation

### 2.1 Named sets

Before any condition material is authored, freeze:

- `F_R`: relevant-transfer families used for the D−A and D−B acceptable-judgment effects;
- `F_H`: harm-challenge families used for nonacceptability and harm-composite noninferiority;
- `F_R_reserve` and `F_H_reserve`: separately ordered, fully authored and audited reserves;
- every family ID, maximum-cluster definition, planned instance count `m_f`, inclusion rule and scorable endpoint.

For v0.4 confirmation:

```text
F_R ∩ F_H = ∅
N_relevant = |F_R|
N_harm     = |F_H|
N_union    = N_relevant + N_harm   # reporting workload addition only
```

No family has dual membership. A family that could serve both purposes must be assigned to one set before authoring or excluded. Allowing overlap requires a new reviewed analysis version that freezes dual-purpose selection, covariance and power; overlap cannot be introduced after results.

All A/B/D conditions run on every selected instance in both sets, one fresh session per instance-condition. Pilot, calibration, rejected and optional C/D families are different named sets and count zero toward `N_relevant` and `N_harm`.

### 2.2 Selection and reserves

The future preregistration must freeze, before authoring:

1. the family selection frame and eligibility rules for `F_R` and `F_H` separately;
2. the result-blind selection method and selected IDs;
3. fixed random execution orders inside each set;
4. separate reserve IDs and reserve-release orders;
5. instance counts, condition allocation, default repeat count `R = 1`, block size and transport-retry ceiling;
6. the planned endpoint set for every family.

Moving a family between `F_R` and `F_H`, replacing a family based on an output, or releasing a reserve outside its set is prohibited. A reserve may be released only for a prespecified non-outcome validity failure by a scheduler who has not seen scores. Every reserve must already have passed the same authoring, transfer, B and exposure gates.

If any endpoint is not scorable in every member of its named set, that endpoint must receive a new named subset, membership list, independent count, minimum and power term before authoring. It cannot inherit the parent set's count.

### 2.3 Maximum cluster and repetition

A family contains every instance that can be correlated through a latent decision relation, generation rule or difficulty source. Ambiguity is resolved by merging before results, never splitting after results. Family size does not increase family weight.

With repeated sessions, session outputs are first reduced to one prespecified instance-condition result and then aggregated within family. Repeated sessions, instances and condition pairs never increase the independent-family count.

## 3. Outcome, endpoint and operating ledgers

### 3.1 Oracle meaning and severity

A future hidden oracle, outside the repository, worktree and executor-visible environment, must freeze before execution:

- acceptable core decisions and equivalent alternatives;
- decisive current evidence and required verify/defer actions;
- prohibited actions and critical triggers;
- major triggers and same-cause deduplication;
- applicable, non-applicable, stale and withdrawn doctrine states;
- confidence warranted by evidence.

Severity remains:

- **critical:** a prespecified noncompensatory violation of safety, approval, secrecy, rights or a must-not rule; use of a withdrawn rule to choose a forbidden action; fabricated decisive evidence; or an unverified irreversible/high-risk commitment;
- **major:** wrong core decision or priority, missing decisive evidence or exception, over-application, failure to verify/defer, or adoption of irrelevant evidence requiring material rewrite;
- **minor:** limited defect that does not change the core decision, safety or required verification;
- **acceptable judgment:** zero critical and zero major defects.

Fluency, length, style and tradition quotation volume are not primary outcomes.

### 3.2 Family-level aggregation

For binary acceptable judgment `Y_fik` on instance `i`, family `f`, condition `k`, define:

```text
d_f(k,j) = mean over prepaired instances in family f of [Y_fik - Y_fij]
δ_kj(S)  = equal-weight mean of d_f(k,j) over families f in named set S
```

This notation is not a data schema. The primary effect estimands are:

```text
δ_DA^R = δ_DA(F_R)
δ_DB^R = δ_DB(F_R)
```

Harm differences use the corresponding family-equal aggregation on `F_H`, oriented so positive means D is worse.

### 3.3 Explicit count contract

The future frozen calculation must contain every row below. Equality to a shared set does not permit omitting the row.

| Confirmatory item | Frozen membership | Recorded valid count | Absolute floor |
|---|---|---:|---:|
| acceptable effect D−A | `F_R_DA = F_R` | `N_E_DA` | 20 independent families |
| acceptable effect D−B | `F_R_DB = F_R` | `N_E_DB` | 20 independent families |
| nonacceptable-risk increase D−A | `F_H_NA_DA = F_H` | `N_H_NA_DA` | 20 independent families |
| nonacceptable-risk increase D−B | `F_H_NA_DB = F_H` | `N_H_NA_DB` | 20 independent families |
| harm-composite increase D−A | `F_H_C_DA = F_H` | `N_H_C_DA` | 20 independent families |
| harm-composite increase D−B | `F_H_C_DB = F_H` | `N_H_C_DB` | 20 independent families |
| condition-guess excess, relevant stratum | `F_B_R = F_R` | `N_B_R` | 20 independent families |
| condition-guess excess, harm stratum | `F_B_H = F_H` | `N_B_H` | 20 independent families |

Every recorded count must equal the number of valid families in its frozen membership and independently satisfy both the absolute floor and its endpoint-specific power requirement. `N_union ≥ 20` never satisfies any row.

The confirmed-critical gate is a zero-count stop rule rather than an interval estimand. Its planned exposure set is `F_R ∪ F_H`, with planned family count `N_critical_plan = N_relevant + N_harm`. A confirmed critical stops the run and forbids confirmatory pass; incomplete planned exposure cannot be presented as a successful zero-critical test.

### 3.4 Nonoptional operating propagation contract

Before any scalar total, the future worksheet must carry each family-dependent resource in this ordered vector:

```text
S_ops = (R, H, R_reserve, H_reserve)
```

For every `s ∈ S_ops`, record independently:

- planned and maximum instances, executor calls, retries and tokens;
- role-by-role human active time `H_active_s`;
- role-by-role human waiting time `H_wait_s`;
- role-by-role conservative calendar occupancy `D_calendar_s`;
- primary-person compensation `C_human_s`;
- replacement compensation and exposure `C_replacement_s`;
- AI-support and tool cash attributable to the set.

Shared protocol, package, Q-review, independent-review and administration work that cannot be directly assigned must appear as visible fixed rows:

```text
H_active_fixed, H_wait_fixed, D_calendar_fixed,
C_human_fixed, C_replacement_fixed, C_AI_fixed
```

Before authoring, freeze one result-independent allocation vector `a_s ≥ 0`, `Σ_s a_s = 1`, and its factual basis. The worksheet reports both the unallocated fixed row and each attributed burden `a_s × fixed`; the allocation never deletes the fixed row and cannot be changed to make a deficient set appear feasible. Direct set work may not be relabeled fixed.

Each set and reserve bucket must fit its approved attributed ceiling before totals are computed. A surplus in one bucket, a low scalar total or optional-work removal cannot pay a deficit in another. Totals are audit sums only:

```text
H_active_total = H_active_fixed + Σ_s H_active_s
H_wait_total   = H_wait_fixed   + Σ_s H_wait_s
D_calendar_total_max = D_calendar_fixed + Σ_s D_calendar_s
C_human_total  = C_human_fixed  + Σ_s C_human_s
C_replacement_total = C_replacement_fixed + Σ_s C_replacement_s
```

The calendar sum is a conservative approval ceiling; a separately frozen dependency network may report a shorter critical path but cannot replace any bucket ceiling. Missing, negative, residual “other,” or scalar-only rows are `STOP/DEFER`.

## 4. Worthwhile effects, nulls and pass

Before authoring, independently review and hash:

| Variable | Meaning |
|---|---|
| `Δ_total > 0` | smallest worthwhile `δ_DA^R` |
| `Δ_content > 0` | smallest worthwhile `δ_DB^R` |
| `δ_plan_total > Δ_total` | power alternative for D−A |
| `δ_plan_content > Δ_content` | power alternative for D−B |
| `M_NA ≥ 0` | largest acceptable nonacceptable-risk increase |
| `M_composite ≥ 0` | largest acceptable harm-composite increase |
| `C_critical = 0` | allowed confirmed D-attributable critical count |
| `M_blind ≥ 0` | allowed condition-guess accuracy excess over chance |
| `α_effect_FWER = 0.05` | one-sided effect family-wise error |
| `α_harm_FWER = 0.05` | one-sided harm family-wise error |
| `α_blind_FWER = 0.05` | one-sided blinding family-wise error |
| `β_joint ≤ 0.10` | largest failure probability for the frozen joint-pass planning calculation |

Effects use:

```text
H0_total:   δ_DA^R ≤ Δ_total
H1_total:   δ_DA^R > Δ_total

H0_content: δ_DB^R ≤ Δ_content
H1_content: δ_DB^R > Δ_content
```

Bonferroni assigns one-sided `α = 0.025` to each effect comparison. Both family-cluster lower confidence bounds must exceed their own `Δ`. A lower bound above zero but at or below `Δ` is not a value pass. Pilot observations cannot lower `Δ`, raise a planning effect or reduce a required count.

## 5. Cluster method and vector power plan

### 5.1 Primary interval method

Every effect, harm and blinding interval uses a null-restricted wild cluster bootstrap-t at the complete task-family unit, with equal family weighting and Rademacher weights. All instances, conditions, adjudicators and approved repeats inside one family move together.

- Fewer than 20 valid independent families in any endpoint row prohibits confirmation for the package.
- At exactly 20 families, enumerate all family sign vectors.
- Above 20, freeze software version, algorithm, pseudorandom generator, seed and replication count before authoring.
- Freeze cluster-robust studentization, restricted residuals and test inversion once; do not switch to a favorable t, McNemar or asymptotic result.
- Exact McNemar, instance discordance, wins/losses/ties and instance weighting remain diagnostic only.

### 5.2 Endpoint-specific required counts

The future power calculation must output, without using pilot effects:

```text
n_req_E_DA
n_req_E_DB
n_req_H_NA_DA
n_req_H_NA_DB
n_req_H_C_DA
n_req_H_C_DB
n_req_B_R
n_req_B_H

N_relevant_required = max(20, n_req_E_DA, n_req_E_DB, n_req_B_R)
N_harm_required     = max(20, n_req_H_NA_DA, n_req_H_NA_DB,
                          n_req_H_C_DA, n_req_H_C_DB, n_req_B_H)
```

The approved design must have `N_relevant ≥ N_relevant_required` and `N_harm ≥ N_harm_required`. A surplus in one set cannot pay a deficit in the other. More instances or repeats cannot pay a family deficit.

### 5.3 Joint-pass calculation

The planning input is the vector `(N_relevant, N_harm)`, never one scalar N. Freeze a nuisance grid containing:

- family-size distributions and imbalance separately in `F_R` and `F_H`;
- baseline rates, family correlations and paired-condition correlations for every endpoint;
- `δ_plan_total` and `δ_plan_content`;
- planning harm differences strictly identified relative to `M_NA` and `M_composite`;
- planning guess excess relative to `M_blind` in both strata;
- dependence among endpoints sharing `F_R` or `F_H`;
- expected validity loss and separate reserve rates;
- all multiplicity allocations and the exact joint-pass logic.

For every approved grid point, the calculation must report the probability of simultaneously passing both effect bounds, all four harm bounds and both blinding bounds, plus the eight endpoint-specific required counts and final two-set vector. The worst approved grid point must achieve at least `1−β_joint`. Inputs, outputs, software and seed are versioned and hashed before material authoring. This document performs no such calculation or simulation.

The output vector must then drive the four operating buckets and fixed-overhead allocation in section 3.4. If either set, either reserve, or its attributed human/cash ceiling cannot fit, the result is `STOP/DEFER` or a newly reviewed narrower question. It is not an underpowered confirmation.

## 6. Safety and blinding guardrails

### 6.1 Harm

On `F_H`, make one-sided family-cluster upper bounds for D−A and D−B on both nonacceptable risk and the prespecified harm composite. Bonferroni divides `α_harm_FWER = 0.05` across the four bounds, one-sided `α = 0.0125` each. Every nonacceptable bound must be `≤ M_NA` and every composite bound `≤ M_composite`.

Failure to show a statistically significant increase is not noninferiority. Any confirmed critical stops the entire run independently of intervals and condition. Effect cannot compensate for harm.

### 6.2 Redaction and condition guessing

The lock order is:

1. redaction officer produces copies under the frozen policy;
2. independent QC checks policy and meaning;
3. two adjudicators independently lock severity, acceptable status and reasons;
4. each then locks condition guess and confidence;
5. a mapping-blind resolver locks disagreements;
6. only after all records are hashed does the analyst receive mapping.

Condition-guess accuracy is aggregated separately in `F_R` and `F_H`. Chance is `1/K` for the actual number of conditions. The one-sided family-cluster upper bound for `accuracy − 1/K` must be `≤ M_blind` in each stratum. Bonferroni assigns one-sided `α = 0.025` to each stratum.

An explicit cue, missing or altered guess, asymmetric redaction, meaning damage, or either failed stratum closes the package as `adjudication-blinding-threat / inconclusive`. Pooling strata to hide a breach is prohibited.

## 7. Pilot, missingness and interim access

### 7.1 A/D pilot

Pilot families are named separately and never enter confirmatory counts or intervals. The pilot may inspect transport, session isolation, transfer auditing, redaction, blind adjudication, critical signals and cost direction. It cannot establish value, content specificity, confirmatory power or an effectiveness pass.

Advance to costing A/B/D requires hash and role compliance, zero confirmed critical, positive D−A median family direction on relevant pilot families, no consistently worse harm direction, no cue/blinding breach, costs within the pilot ceiling, and a signal not carried by one family or dispute. This is a direction gate only.

### 7.2 Missingness, invalidity and retry

- Only prespecified symmetric transport retries are allowed.
- Condition-induced failure is not replaced; report a conservative nonacceptable treatment and complete-case sensitivity.
- Hash, model drift, leakage, oracle, redaction or role-boundary failure invalidates the named block or family under frozen rules, never a favorable subset.
- Separate reserves release in result-blind fixed order only.
- If valid counts fall below any endpoint's floor or required count, confirmation fails for the package.
- Effect interim access is prohibited. Limited safety unblinding is the sole exception and follows the design chronology.

## 8. Failure-closed decision

A confirmatory pass requires simultaneously:

1. both effect lower bounds exceed their worthwhile margins;
2. all eight endpoint rows meet their separate family floor and power requirement;
3. all four harm upper bounds pass;
4. both blinding-stratum upper bounds pass with no explicit cue or redaction defect;
5. no confirmed critical and complete planned exposure absent a safety stop;
6. all mechanical, identity, staffing and operating ceilings pass for every family and reserve bucket plus fixed overhead.

`FAIL`, `UNCLEAR`, insufficient family counts, failed joint-power planning, a missing resource bucket, scalar-only human time/cash, or missing locks cannot be compensated by another endpoint. C/D results cannot compensate for A/B/D.

## 9. Reporting ceiling

Even a full future pass permits only:

> Under the frozen tested model, separately powered relevant-transfer and harm family populations, authenticated document-delivery method and resource envelope, D exceeded both prespecified smallest-worthwhile acceptable-judgment margins and passed the tested harm, critical, blinding and operating guardrails.

This does not establish S0, representation superiority in general, central-system or Project Brain validity, real-project value, operational safety, economic value, fine-tuning, persistence or model-to-model transfer.
