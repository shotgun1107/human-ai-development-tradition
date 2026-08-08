# E0 operating cost and gates plan v0.4

- Status: `revision proposal — awaiting fresh independent review, design only`
- Proposal label: E0 is not a frozen official phase.
- Current authority: fresh read-only review of the v0.4 design packet only
- Currently prohibited: material, oracle, prompt, schema or code creation; model calls; price lookup; staffing commitment; budget approval; simulation; scoring; statistical execution; effect, safety or economic claims; later gates
- Cost principle: future approval must use numeric worst-case people, identity, compensation, time, call, token, tool and cash ceilings by family bucket before totals. This document supplies formulas, not values or commitments.

## 1. Facts, inference and proposal

### 1.1 Facts

1. No E0 model, price, person, compensation, schedule, family count, material or result is fixed.
2. The v0.3 review passed the 13/18 first-cycle role separation, per-role compensation/time/absence fields, all-AI-call scope, executor call/token family separation and the statistical family vector.
3. It found that prior unmapped candidate exposure did not permanently bar a Q reviewer from a later package version and that a repair path did not budget a mandatory new Q pair.
4. It also found that human active/wait/calendar time and human compensation/cash were scalar by role rather than propagated through relevant, harm and reserve family buckets.

### 1.2 Inference

Candidate semantics, not labels alone, create durable Q exposure. After access, replacing one Q means retiring both and starting a new package cycle with two new natural people. Separately, a scalar human total cannot demonstrate that both family populations and both reserves are operationally feasible.

### 1.3 Proposal

- Keep the A/D pilot minimum at 13 distinct natural people.
- Keep the first untouched A/B/D cycle minimum at 18 distinct natural people.
- Freeze `J_Q_restart_max`, the maximum allowed number of post-access Q-cycle restarts; prequalify two additional fresh natural people per permitted restart.
- Use lifetime `CAND_DB` exposure and fail-closed natural-person identity resolution across all versions.
- Budget calls, tokens, human active/wait/calendar time, compensation and cash separately for `F_R`, `F_H`, `F_R_reserve` and `F_H_reserve`, plus visible fixed overhead and a frozen allocation.
- Stop rather than reuse Q reviewers, merge family buckets, approve a scalar-only total or omit an AI-support category.

## 2. Stage path

| Stage | Conditions | Purpose | Maximum result |
|---|---|---|---|
| 0 | v0.4 read-only review | v0.3 F-01/F-02/F-03 and preserved-correction review | CONTROL-integration suitability only |
| 1 | dependencies, endpoint vector, lifecycle staffing and bucket ceilings | establish future feasibility on paper | none |
| 2 | separately authorized material authoring | role-isolated synthetic material work | none |
| 3 | preflight and calibration | hashes, transfer, B, redaction and adjudication eligibility | none |
| 4 | A/D pilot | feasibility, direction, harm and cost screen | pilot-only |
| 5 | A/B/D confirmation | limited content-specific question | only after every joint criterion passes |
| 6 | optional C/D diagnostic | refinement versus raw access | separate diagnostic only |
| 7 | optional extension | new model, family population or delivery method | separate preregistration and gate |

Pilot families never become confirmatory families. Stage 6 or 7 does not open automatically after Stage 5.

## 3. Distinct-person, identity and lifetime-exposure contract

### 3.1 Common rule

- A distinct person is a distinct natural person. Accounts, aliases, sessions, agents, models and worktrees are not people.
- The minima cover the complete first package cycle, not simultaneous attendance.
- An activated replacement or restart pair adds natural people and never reduces a minimum.
- Only combinations explicitly listed below are allowed. Independence is not waived for cost or availability.
- AI assistance does not replace a human reviewer and is charged to the relevant role's call, token, human-verification and cash ceilings.

The lifetime exposure ledger uses stable natural-person IDs, known aliases, identity-resolution evidence, artifact and derivative hashes, package version, access time and the design's `CAND_DB`, `L_DB`, `T_ORACLE`, `COND_ID` and `REL_ID` flags. `CAND_DB` covers full and topic-stripped D/B-derived candidates whether mapped or unmapped. It is append-only across every E0 version, repair and replacement.

Before assignment, an identity custodian must positively resolve each proposed person and reconcile the ledger with access logs. Unresolved identity, a possible alias collision, missing historic access, inability to prove a clean pre-access history or ledger/access disagreement is a stop. Declarations, deleted files or new accounts cannot clear exposure.

### 3.2 A/D pilot: minimum 13 distinct people

| Person | Role | Allowed combination and prohibition |
|---:|---|---|
| 1 | CONTROL + protocol owner + analyst only after all result locks | no material/output authoring or adjudication |
| 2 | tradition curator | no task, oracle, B or output access |
| 3 | task/oracle author + external oracle custodian | no D, B or output access; oracle remains external |
| 4 | surface/provenance leakage auditor | no authoring, Q/R review, execution, adjudication or analysis |
| 5 | structural leakage auditor | separate from 4; same role prohibitions |
| 6 | mapping holder + blind-package packager + cue verifier + scheduler + run operator | compares locked Q reasons only after quality exit; no oracle, scores or effect result access |
| 7 | redaction officer | no mapping, oracle or score access |
| 8 | redaction QC | separate from 7; no adjudication |
| 9 | safety monitor | only one locked critical ID's minimum mapping |
| 10 | adjudicator 1 | no condition package or mapping access |
| 11 | adjudicator 2 | separate from 10; same prohibitions |
| 12 | blind disagreement resolver | no mapping or earlier other score access |
| 13 | independent read-only reviewer | no authoring, gate approval, execution or adjudication |

The pilot has no B. People 4 and 5 perform only the two leakage scopes. They do not gain later eligibility as B-quality reviewers.

### 3.3 A/B/D first untouched cycle: minimum 18 distinct people

Confirmation requires all 13 roles above plus five additional people:

| Person | Role | Mandatory boundary |
|---:|---|---|
| 14 | B author | separate from curator; no task, oracle or output access |
| 15 | B-quality reviewer Q1 | no other E0 role; no earlier `CAND_DB` or other prohibited exposure |
| 16 | B-quality reviewer Q2 | separate from Q1; identical isolation |
| 17 | relevance reviewer R1 | fresh, separate from every prior role; minimum mapped semantic input only after Q locks |
| 18 | relevance reviewer R2 | fresh and separate from R1 and every prior role; same boundary |

Q1 and Q2 receive neither leakage findings nor relevance material. Candidate access adds `CAND_DB` and permanently prevents either natural person from Q service on a later package version. Their complete semantic parity, authority/specificity/actionability/completeness judgments and topic-stripped guesses/reasons must be hashed before R1 or R2 receives relevance information.

R1 and R2 may not be Q reviewers, leakage auditors, authors, mapping holders, executors, redactors, adjudicators, resolvers, safety monitors, analysts or the independent package reviewer. They do not see Q records or each other's judgments.

Any `FAIL`, `UNCLEAR`, missing record, disagreement, identity uncertainty, exposure breach or chronology violation rejects the package. There is no reconciliation role. Optional C, another model or a new family population can only add people; it cannot reduce these minima.

### 3.4 Post-access Q restart: mandatory fresh pair

Before any candidate access, freeze a nonnegative integer `J_Q_restart_max`. For each permitted restart `j`, roster and prequalify two additional natural people `Q1_j` and `Q2_j` with clean lifetime histories, compensation, availability, absence coverage and resource maxima.

If either Q in a cycle has accessed full or topic-stripped candidate bytes, any package rejection, amendment, candidate change, access failure, missing or corrupted lock, Q withdrawal or attempted Q replacement triggers all of the following:

1. retire both current Q reviewers permanently from later Q service;
2. close their access and record lifetime `CAND_DB` exposure;
3. prohibit either retired reviewer from seeing or comparing a later candidate version;
4. create a new versioned package, randomized copies, topic-stripped copies, mapping and locks;
5. activate one complete prequalified fresh pair and restart quality review from zero;
6. reuse no prior Q judgment, guess, reason or partial record.

A stable D, B or stripped candidate is not an exception because semantic recognition itself is the risk. If logs prove that neither Q received candidate bytes, roster correction may occur before access; uncertainty invokes the full-pair rule.

The minimum possible first cycle remains 18. The planned lifecycle roster must additionally expose:

```text
N_Q_restart_people_max = 2 × J_Q_restart_max
N_lifecycle_people_max = 18
                       + N_Q_restart_people_max
                       + N_other_activated_replacements_max
```

This is a staffing ceiling, not a commitment or current fact. If an unbudgeted restart is needed, `J_Q_restart_max` is exhausted, or a fresh pair is unavailable, the stage is `STOP/DEFER`.

### 3.5 Other absence and replacement stops

A stage does not open or continue if:

- the stage minimum or lifecycle maximum coverage is unmet;
- a prohibited exposure or role combination exists;
- identity, Q or R eligibility cannot be proven from append-only logs;
- the oracle's external custody boundary is not approved;
- either adjudicator, resolver, redaction officer/QC, safety monitor or required pre-result reviewer is absent;
- any required person's compensation, time or availability is unapproved.

For every non-Q role, the staffing record must identify one prequalified replacement or `no replacement`. Replacement eligibility, exposure history, compensation and time are reviewed before access. All replacement maxima are included in the correct family or fixed bucket. If no eligible replacement is available, new calls stop. The safety monitor is not replaced after any unblinding; the run ends. R replacement must be fresh and must not see the departed reviewer's record. If an R-stage rejection causes a new or amended B package, section 3.4 also requires a fresh Q pair.

## 4. Four-bucket human time, compensation and calendar freeze

### 4.1 Mandatory resource buckets

Before material authoring, freeze the ordered operating set:

```text
S_ops = { R, H, R_reserve, H_reserve }
```

For every primary, prequalified replacement and Q-restart person, the worksheet must include four explicit family-dependent columns and one shared-fixed column for:

- minimum and maximum active time;
- minimum and maximum waiting time;
- conservative calendar occupancy and response deadline;
- compensation type (`hourly`, `fixed` or explicit `volunteer`), rate, currency, taxes/fees and maximum payment;
- replacement or restart exposure and maximum payment;
- allowed AI support and human verification time.

An inapplicable cell is an authenticated zero, not a blank. Volunteer or user time is recorded as unpaid active/waiting time with an explicit opportunity-cost treatment; it does not disappear because cash payment is zero.

The roles remain separately visible: protocol/CONTROL, source, tradition, B authoring, task/oracle, both leakage auditors, Q1/Q2 for every allowed cycle, R1/R2, mapping/packaging, run operations, redaction, redaction QC, safety, both adjudicators, resolver, analysis and fresh independent review.

### 4.2 Direct family-dependent rows

For every `s ∈ S_ops`, calculate role-by-role and then bucket totals:

```text
H_active_s_max = Σ_role H_active_role,s_max
H_wait_s_max   = Σ_role H_wait_role,s_max
D_calendar_s_max = conservative sequential ceiling for role,s dependencies

C_human_s_max = Σ_role C_primary_role,s_max
C_replacement_s_max = Σ_role C_replacement_role,s_max
```

Direct work caused by a selected or reserve family—including task-specific audit, execution, redaction, adjudication, safety review, analysis and result handling—must stay in that family's bucket. It cannot be relabeled as shared fixed overhead.

### 4.3 Visible fixed overhead and frozen allocation

One-time protocol, package-level B/Q review, independent-review and administration work that genuinely cannot be assigned to one family bucket is recorded separately:

```text
H_active_fixed_max
H_wait_fixed_max
D_calendar_fixed_max
C_human_fixed_max
C_replacement_fixed_max
```

Q-restart identity review, candidate packaging, both fresh reviewers' active/wait/calendar time, compensation, absence coverage and human verification are included in explicit `Q_restart_fixed` subrows. They are never hidden in a generic contingency.

Before authoring, freeze a result-independent allocation vector:

```text
a_R, a_H, a_R_reserve, a_H_reserve ≥ 0
a_R + a_H + a_R_reserve + a_H_reserve = 1
```

Record the factual basis, such as planned direct hours or planned instances, and a rounding rule. Report both the original fixed row and each attributed burden `a_s × fixed`. The vector cannot change after outputs, cannot assign negative overhead and cannot be chosen to cure a deficient bucket. A future review may require a conservative sensitivity allocation; a favorable allocation alone cannot open a gate.

### 4.4 Bucket tests and totals

Each family and reserve bucket must pass its own approved ceiling after attributed fixed overhead:

```text
H_active_s_attributed_max = H_active_s_max + a_s × H_active_fixed_max
H_wait_s_attributed_max   = H_wait_s_max   + a_s × H_wait_fixed_max
D_calendar_s_attributed_max = D_calendar_s_max + a_s × D_calendar_fixed_max
C_human_s_attributed_max  = C_human_s_max  + a_s × C_human_fixed_max
C_replacement_s_attributed_max
  = C_replacement_s_max + a_s × C_replacement_fixed_max
```

Only after all four bucket tests pass may totals be shown:

```text
H_total_active_max = H_active_fixed_max + Σ_s H_active_s_max
H_total_wait_max   = H_wait_fixed_max   + Σ_s H_wait_s_max
D_total_calendar_max = D_calendar_fixed_max + Σ_s D_calendar_s_max
C_total_human_max  = C_human_fixed_max  + Σ_s C_human_s_max
C_total_replacement_max
  = C_replacement_fixed_max + Σ_s C_replacement_s_max
```

The calendar sum is a conservative approval ceiling. A separately frozen dependency graph may report a shorter critical path but cannot replace bucket rows. No scalar total, low average or surplus in another bucket compensates for a missing or excessive relevant, harm or reserve row.

## 5. Family-specific workload, calls and tokens

### 5.1 Frozen workload vector

Let:

```text
I_R      = sum of planned instances over f in F_R
I_H      = sum of planned instances over f in F_H
I_R_res  = sum over F_R_reserve
I_H_res  = sum over F_H_reserve
K_confirm = 3  # A, B, D
R_session = 1  # confirmatory default
```

The worksheet must show `N_relevant`, `N_harm`, all eight endpoint-specific required counts, `I_R`, `I_H`, both reserve sizes and each block allocation. It may show `N_union` only after those rows. No `N_total` can replace a missing relevant or harm count.

Maximum executor calls are separate:

```text
Q_executor_R_max     = K_confirm × R_session × I_R
Q_executor_H_max     = K_confirm × R_session × I_H
Q_executor_R_res_max = K_confirm × R_session × I_R_res
Q_executor_H_res_max = K_confirm × R_session × I_H_res
```

Pilot and calibration calls have separate terms and cannot be hidden inside confirmation.

### 5.2 All AI-support calls, including restarts

Every model or model-backed-tool call connected to E0 is counted, including failed, cached, subscription, bundled-credit and discarded calls. Each support category is assigned to one of the four family buckets or the visible fixed bucket before totals.

```text
Q_total_max = Q_protocol_support_fixed
            + Q_source_tradition_support_fixed + Q_B_authoring_support_fixed
            + Q_task_oracle_support_R + Q_task_oracle_support_H
            + Q_task_oracle_support_R_res + Q_task_oracle_support_H_res
            + Q_leakage_support_R + Q_leakage_support_H
            + Q_leakage_support_R_res + Q_leakage_support_H_res
            + Q_B_quality_initial_support_fixed
            + Q_Q_restart_support_fixed_max
            + Q_relevance_support_R + Q_relevance_support_H
            + Q_relevance_support_R_res + Q_relevance_support_H_res
            + Q_mapping_packaging_support_fixed
            + Q_calibration
            + Q_executor_R_max + Q_executor_H_max
            + Q_executor_R_res_max + Q_executor_H_res_max
            + Q_retry_R_max + Q_retry_H_max
            + Q_retry_R_res_max + Q_retry_H_res_max
            + Q_redaction_QC_support_R + Q_redaction_QC_support_H
            + Q_redaction_QC_support_R_res + Q_redaction_QC_support_H_res
            + Q_adjudication_support_R + Q_adjudication_support_H
            + Q_adjudication_support_R_res + Q_adjudication_support_H_res
            + Q_safety_support + Q_analysis_support
            + Q_independent_review_support_fixed + Q_model_backed_tools
```

Every category is explicitly frozen as zero or a numeric maximum. `Q_Q_restart_support_fixed_max` covers all `J_Q_restart_max` fresh pairs, new copies, new locks and human verification. If AI support is permitted for Q or R review, the model receives no more information than that human role, its output cannot replace human judgment, and human verification time is budgeted. Shared AI outputs cannot make Q1/Q2 or R1/R2 independent.

Each future call record includes role, purpose, family bucket or fixed allocation, provider, exact model/version, service tier, input/cached/output/tool tokens, start/end, retry reason, cash-price basis and exposure class. This is a future record requirement, not a schema created now.

### 5.3 Token and resource ceilings

Freeze:

```text
T_executor_R_max, T_executor_H_max,
T_executor_R_res_max, T_executor_H_res_max

T_support_R_max, T_support_H_max,
T_support_R_res_max, T_support_H_res_max,
T_support_fixed_max,
T_Q_restart_fixed_max
```

`T_Q_restart_fixed_max` covers all permitted fresh-pair cycles and derivative packages. For every bucket, wrapper, task, condition, tool, output and retry ceilings are explicit. B and D context resources remain within the parity tolerance. Bundling tasks in one prompt cannot evade fresh sessions or call counts.

Only after each bucket passes may:

```text
T_total_max = T_executor_R_max + T_executor_H_max
            + T_executor_R_res_max + T_executor_H_res_max
            + T_support_R_max + T_support_H_max
            + T_support_R_res_max + T_support_H_res_max
            + T_support_fixed_max + T_Q_restart_fixed_max
            + T_retry_total_max
```

be reported.

## 6. Cash ceiling

Only at a future approved pricing gate may official provider information supply model, tier, date checked, currency, taxes, exchange-rate assumption, input/cached/output/tool/storage price, and subscription/credit allocation.

For every `s ∈ S_ops`, calculate before totals:

```text
C_AI_s_max
C_human_s_max
C_replacement_s_max
C_tools_storage_s_max
C_other_approved_s_max
```

Fixed rows include initial and restart Q review, shared protocol/packaging, independent review and genuinely common tools:

```text
C_AI_fixed_max
C_AI_Q_restart_fixed_max
C_human_fixed_max
C_human_Q_restart_fixed_max
C_replacement_fixed_max
C_tools_storage_fixed_max
C_other_approved_fixed_max
```

Apply the frozen section 4.3 allocation for bucket approval while retaining every fixed row. Then, and only then, calculate:

```text
C_cash_max = Σ_s (C_AI_s_max + C_human_s_max
                + C_replacement_s_max + C_tools_storage_s_max
                + C_other_approved_s_max)
           + C_AI_fixed_max + C_AI_Q_restart_fixed_max
           + C_human_fixed_max + C_human_Q_restart_fixed_max
           + C_replacement_fixed_max
           + C_tools_storage_fixed_max + C_other_approved_fixed_max
```

Maximum output, all permitted transport retries, reserve release, model-backed tools, dispute handling and every allowed fresh Q pair are included. Incremental cash of zero is recorded as zero without deleting use, tokens, subscription allocation, human time or opportunity cost. A scalar `C_cash_max` cannot open a gate unless all source rows and four attributed bucket tests pass.

## 7. Stop-before-authoring sequence

1. Freeze A/D pilot or A/B/D confirmatory question and condition count.
2. Freeze `F_R` and `F_H` as disjoint selection frames, selected IDs, reserves, instances and allocations.
3. Freeze both effect margins, four harm comparisons, two blinding strata, multiplicity and all eight endpoint count rows.
4. Run the future pre-result power calculation and freeze `N_relevant_required`, `N_harm_required` and joint-pass output. This plan performs no calculation now.
5. Assign at least 13 pilot or 18 first-cycle confirmatory people and resolve lifetime identities and exposure histories.
6. Freeze `J_Q_restart_max`; prequalify two fresh Q people per allowed restart or set the value to zero.
7. Freeze role-by-role compensation, active/wait/calendar time, availability, absence and replacement coverage in all four family buckets plus fixed overhead.
8. Freeze and justify the fixed-overhead allocation vector.
9. Freeze every AI call and token category, including Q restarts and all family/reserve buckets.
10. Confirm exact model/tier and official prices at that future time.
11. Calculate four attributed bucket ceilings, then worst-case total cash, people time, calendar, calls and tokens.
12. Obtain explicit user approval of each bucket and `B_cash`, `B_active_time`, `B_wait_time`, `B_calendar`, `B_calls` and `B_tokens` totals.
13. Version and hash the calculation, roster, identity/exposure ledger state, assumptions and approvals.
14. Only then may the exact separate material-authoring gate be requested.

Keep authoring at zero if either family set is under its required vector count; a reserve bucket is missing; staffing, fresh-pair or replacement coverage is missing; identity or Q/R isolation fails; an AI-call category is absent; a family-dependent human/cash row is blank; the single representation reference is unavailable; or B, harm challenges, fresh sessions, redaction, blinding or safety would need removal to fit a ceiling.

Cost reduction order is: remove optional C, remove optional AI judge, remove nonessential AI support, reduce result-independent repetitions, reduce `J_Q_restart_max` only before any candidate access with the consequence that an additional restart becomes `STOP/DEFER`, or propose a newly reviewed narrower question. Do not reduce independent-family counts, merge buckets, reuse Q reviewers, combine Q with leakage/relevance, remove B or weaken a guardrail.

## 8. Gates

### V4-G0 — `E0 EFFECT TEST DESIGN V0.4 REVIEW`

Requires matching v0.4 Markdown sidecars, unchanged earlier files, versioned package index, direct current-byte review of README and all four v0.1 design files, and a fresh hostile read-only review of v0.3 F-01/F-02/F-03 plus every preserved correction. Passing allows CONTROL integration review only.

### V4-G1 — `E0 SINGLE REPRESENTATION INTERFACE READY`

Requires exactly one authenticated `selected_representation_ref` and the visibility, citation, resource and limitation links. A fallback must have identical artifact status. Failure keeps authoring closed.

### V4-G2 — `E0 ENDPOINT LIFECYCLE STAFFING AND VECTOR CEILING APPROVED`

Requires:

- disjoint `F_R`/`F_H`, all eight count rows, two-set power vector and joint-pass output;
- at least 13 or 18 eligible people as applicable, positive identity resolution, lifetime exposure chronology, compensation, availability and absence coverage;
- frozen `J_Q_restart_max`, two prequalified fresh Q people per permitted restart, and complete restart call/token/time/cash ceilings;
- separate relevant, harm, relevant-reserve and harm-reserve call, token, role-by-role human active/wait/calendar time, compensation, replacement and cash maxima;
- visible shared fixed overhead, frozen allocation, four attributed bucket passes and only then totals;
- all-AI-support and worst-case cash ceilings;
- explicit user approval of every bucket and total.

A combined family count, former 14-person path, cross-version Q reuse, single-Q replacement, blank resource bucket or scalar-only human/cash approval fails this gate.

### V4-G3 — `E0 MATERIAL AUTHORING OPEN`

Requires V4-G0 through G2 and the user's explicit opening of this exact gate in the current thread, plus role input allowlists, output ownership and external oracle custody. It opens synthetic material authoring only, not code, calls, execution or scoring.

### V4-G4 — `E0 PREFLIGHT AND CALIBRATION OPEN`

Requires all material hashes; two leakage passes; both Q quality and guess locks before relevance release; both fresh R relevance passes; identity/exposure and chronology audit; no cross-version comparison; sufficient unused fresh-pair coverage for the approved restart maximum; redaction/guess and adjudication calibration plans; safety-block plan; and recalculated four-bucket ceilings. It does not open effect execution.

### V4-G5 — `E0 A-D PILOT EXECUTION OPEN`

Requires separate pilot preregistration, 13-person availability, no reuse of confirmatory families, current model/price/resource confirmation, blind adjudication, redaction/QC and safety monitoring. Its output can only decide whether A/B/D costing is worth review.

### V4-G6 — `E0 A-B-D CONFIRMATORY EXECUTION OPEN`

Requires pilot advance without treating it as effect evidence; V4-G4 B-package acceptance; 18-person first-cycle eligibility plus approved fresh-pair coverage; all eight endpoint counts and both required set sizes; frozen margins, multiplicity and joint-pass calculation; refreshed relevant, harm and both reserve human-time/cash rows, fixed allocation, four bucket passes and totals; explicit user approval; and another result-blind independent review.

### V4-G7 — `E0 OPTIONAL C OR EXTENSION OPEN`

C/D, four conditions, another model, another task population, retrieval comparison or any overlapping family design requires its own question, set memberships, endpoint counts, power, staffing, budget, preregistration and approval. Earlier results do not open it.

## 9. Block release and rollback

- Release only frozen-size blocks after transport checks, blind critical clearance and staff availability.
- A critical candidate stops new calls; confirmed critical stops the full run regardless of condition.
- A missing Q/R lock, identity uncertainty, exposure breach or review disagreement rejects the whole B package.
- After candidate access, package rejection, amendment, access failure or Q replacement retires both Qs and consumes one approved fresh-pair restart; otherwise stop.
- A family-count or resource-bucket shortfall prohibits confirmation; do not add instances, borrow families or rely on scalar totals.
- Hash mismatch, unledgered AI call, price/resource drift, shared state, raw cue, redaction asymmetry, adjudication ambiguity or ceiling overrun stops the affected work under the preregistered rollback.
- Invalid or contaminated outputs are never joined to clean samples. Results cannot justify changing thresholds, sets, counts, retries, conditions, fixed-overhead allocation, redaction or staffing.

## 10. Unresolved feasibility and bounded status

It is unknown whether 18 eligible first-cycle people plus any approved fresh Q pairs and other replacements can be recruited, compensated and kept available; lifetime identity and exposure isolation can be maintained; both independently powered family sets and reserves fit their attributed human/cash ceilings; a useful but irrelevant B can pass both review layers; redaction can preserve meaning while passing both blinding strata; or a single representation artifact will be approved.

The endpoint-specific counts, restart maximum, allocation vector, model, price, token, human-time, calendar and cash values are also unknown. These are future stop conditions, not implicit commitments. v0.4 remains design-only and awaits a fresh independent read-only review.
