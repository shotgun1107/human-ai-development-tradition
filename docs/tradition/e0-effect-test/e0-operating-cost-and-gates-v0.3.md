# E0 operating cost and gates plan v0.3

- Status: `revision proposal — awaiting fresh independent review, design only`
- Proposal label: E0 is not a frozen official phase.
- Current authority: read-only review of the v0.3 design packet only
- Currently prohibited: material, oracle, prompt, schema or code creation; model calls; price lookup; staffing commitment; budget approval; scoring; statistical execution; effect, safety or economic claims; later gates
- Cost principle: future approval must use numeric worst-case people, compensation, time, call, token, tool and cash ceilings. This document supplies formulas, not values or commitments.

## 1. Facts, inference and proposal

### 1.1 Facts

1. No E0 model, price, person, compensation, schedule, family count or result is fixed.
2. The v0.2 review passed the compensation, time, absence and all-AI-call scope in principle.
3. It rejected the 14-person confirmatory minimum because the same two people were both leakage auditors and B-quality reviewers.

### 1.2 Inference

B-quality blindness requires two dedicated people with no earlier prohibited exposure, followed by two different fresh relevance reviewers. Those four roles cannot be recovered by renaming the two leakage auditors.

### 1.3 Proposal

- Keep the A/D pilot minimum at 13 distinct natural people.
- Raise the A/B/D confirmatory lifecycle minimum to 18 distinct natural people.
- Freeze an append-only exposure chronology before assigning Q reviewers.
- Budget relevant and harm family sets separately, including reserves, before adding totals.
- Stop rather than merge roles, family sets or unbudgeted AI calls.

## 2. Stage path

| Stage | Conditions | Purpose | Maximum result |
|---|---|---|---|
| 0 | v0.3 read-only review | F-01/F-02/F-03 and preserved-correction review | CONTROL-integration suitability only |
| 1 | dependencies, endpoint vector, staffing and ceiling | prove future feasibility on paper | none |
| 2 | separately authorized material authoring | role-isolated synthetic material work | none |
| 3 | preflight and calibration | hashes, transfer, B, redaction and adjudication eligibility | none |
| 4 | A/D pilot | feasibility, direction, harm and cost screen | pilot-only |
| 5 | A/B/D confirmation | limited content-specific question | only after every joint criterion passes |
| 6 | optional C/D diagnostic | refinement versus raw access | separate diagnostic only |
| 7 | optional extension | new model, family population or delivery method | separate preregistration and gate |

Pilot families never become confirmatory families. Stage 6 or 7 does not open automatically after Stage 5.

## 3. Distinct-person and exposure contract

### 3.1 Common rule

- A distinct person is a distinct natural person. Accounts, sessions, agents, models and worktrees are not people.
- The minima cover the complete stage lifecycle, not simultaneous attendance.
- An activated replacement is an additional person and never reduces the minimum.
- Only combinations explicitly listed below are allowed. Independence is not waived for cost or availability.
- AI assistance does not replace a human reviewer and is charged to the relevant role's call and verification ceilings.

The exposure ledger uses the design's `L_DB`, `T_ORACLE`, `COND_ID` and `REL_ID` flags with person ID, artifact hash and timestamp. Access logs and declarations must agree. An inconsistency is a stop.

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

### 3.3 A/B/D confirmation: minimum 18 distinct people

Confirmation requires all 13 roles above plus five additional people:

| Person | Role | Mandatory boundary |
|---:|---|---|
| 14 | B author | separate from curator; no task, oracle or output access |
| 15 | B-quality reviewer Q1 | no other E0 role; no prior or later prohibited exposure |
| 16 | B-quality reviewer Q2 | separate from Q1; identical isolation |
| 17 | relevance reviewer R1 | fresh, separate from every prior role; minimum mapped semantic input only after Q locks |
| 18 | relevance reviewer R2 | fresh and separate from R1 and every prior role; same boundary |

Q1 and Q2 must be distinct from every leakage auditor and every role previously exposed to labeled D/B, task or oracle meaning, condition identity, or relevance identity. They receive neither leakage findings nor relevance material. Their complete semantic parity, authority/specificity judgments and topic-stripped guess/reasons must be hashed before R1 or R2 receives relevance information.

R1 and R2 may not be Q reviewers, leakage auditors, authors, mapping holders, executors, redactors, adjudicators, resolvers, safety monitors, analysts or the independent package reviewer. They do not see Q records or each other's judgments.

Any `FAIL`, `UNCLEAR`, missing record, disagreement, exposure breach or chronology violation rejects the package. There is no reconciliation role. Optional C, another model or a new family population can only add people; it cannot reduce these minima.

### 3.4 Ineligibility and absence stop

A stage does not open or continue if:

- the stage minimum is unmet;
- a prohibited exposure or role combination exists;
- Q or R eligibility cannot be proven from append-only logs;
- the oracle's external custody boundary is not approved;
- either adjudicator, resolver, redaction officer/QC, safety monitor or required pre-result reviewer is absent;
- any required person's compensation, time or availability is unapproved.

For every role, the staffing record must identify either one prequalified replacement or `no replacement`. Replacement eligibility, exposure history, compensation and time are reviewed before access. All replacement maxima are included in ceilings. If no eligible replacement is available, new calls stop. The safety monitor is not replaced after any unblinding; the run ends. Q replacement after blind-package access requires a new blinded package version and new quality chronology. R replacement must be fresh and must not see the departed reviewer's record.

## 4. Compensation, time and calendar freeze

Before material authoring, record and obtain user approval for every primary and replacement person:

- natural-person identifier, role, conflict declaration and exposure-ledger status;
- compensation type (`hourly`, `fixed` or explicit `volunteer`), rate, currency, taxes/fees and maximum payment;
- minimum and maximum active time and waiting time;
- maximum time by protocol, authoring, leakage, B quality, relevance, packaging, calibration, block operation, redaction, safety, adjudication, resolution, analysis and review;
- calendar availability, response deadline and maximum block turnaround;
- absence plan and replacement;
- allowed AI support, allowed information and human verification time.

Volunteer or user time is recorded as unpaid active and waiting time with an explicit opportunity-cost treatment; it does not disappear because cash payment is zero.

The active-time ceiling must expose the formerly combined roles:

```text
H_total_active_max = H_protocol
                   + H_source + H_tradition + H_B_authoring + H_task_oracle
                   + H_leakage_surface + H_leakage_structural
                   + H_B_quality_Q1 + H_B_quality_Q2
                   + H_relevance_R1 + H_relevance_R2
                   + H_mapping_packaging + H_run_ops
                   + H_redaction + H_redaction_QC + H_safety
                   + H_adjudication_1 + H_adjudication_2 + H_resolution
                   + H_analysis + H_independent_review
                   + H_replacements_max
```

Waiting-time and calendar ceilings list the same roles separately. Each term records planned minimum, planned maximum and later actual. AI drafting plus human verification appears in both the AI-call ledger and human time ledger.

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

### 5.2 All AI-support calls

Every model or model-backed-tool call connected to E0 is counted, including failed, cached, subscription, bundled-credit and discarded calls:

```text
Q_total_max = Q_protocol_support
            + Q_source_tradition_support + Q_B_authoring_support
            + Q_task_oracle_support
            + Q_leakage_surface_support + Q_leakage_structural_support
            + Q_B_quality_Q1_support + Q_B_quality_Q2_support
            + Q_relevance_R1_support + Q_relevance_R2_support
            + Q_mapping_packaging_support
            + Q_calibration
            + Q_executor_R_max + Q_executor_H_max
            + Q_executor_R_res_max + Q_executor_H_res_max
            + Q_retry_R_max + Q_retry_H_max
            + Q_redaction_QC_support + Q_adjudication_support
            + Q_safety_support + Q_analysis_support
            + Q_independent_review_support + Q_model_backed_tools
```

Every category is explicitly frozen as zero or a numeric maximum. If AI support is permitted for Q or R review, the model receives no more information than that human role, its output cannot replace the human judgment, and human verification time is budgeted. Shared AI outputs cannot be used to make Q1/Q2 or R1/R2 independent of each other.

Each call record must later include role, purpose, provider, exact model/version, service tier, input/cached/output/tool tokens, start/end, retry reason, cash-price basis and exposure class. This is a future record requirement, not a schema created now.

### 5.3 Token and resource ceilings

Freeze per condition and family set:

```text
T_executor_R_max = sum of wrapper + task + condition + tool + output ceilings over F_R
T_executor_H_max = corresponding sum over F_H
T_reserve_max    = separate F_R_reserve and F_H_reserve sums
T_support_max    = sum of every non-executor support category
T_total_max      = T_executor_R_max + T_executor_H_max
                 + T_reserve_max + T_support_max + T_retry_max
```

B and D context resources remain within the parity tolerance. Bundling tasks in one prompt cannot evade fresh sessions or call counts.

## 6. Cash ceiling

Only at a future approved pricing gate may official provider information supply model, tier, date checked, currency, taxes, exchange-rate assumption, input/cached/output/tool/storage price, and subscription/credit allocation.

Use maximum output, all permitted transport retries, reserve release, model-backed tools, dispute handling and replacement coverage:

```text
C_cash_max = C_AI_R_max + C_AI_H_max + C_AI_reserve_max
           + C_AI_support_max
           + C_human_compensation_18_roles_max
           + C_replacement_compensation_max
           + C_tools_storage_max + C_other_approved_max
```

Incremental cash of zero is recorded as zero without deleting use, tokens, subscription allocation, human time or opportunity cost.

## 7. Stop-before-authoring sequence

1. Freeze A/D pilot or A/B/D confirmatory question and condition count.
2. Freeze `F_R` and `F_H` as disjoint selection frames, selected IDs, reserves, instances and allocations.
3. Freeze both effect margins, four harm comparisons, two blinding strata, multiplicity and the eight endpoint count rows.
4. Run the future pre-result power calculation and freeze `N_relevant_required`, `N_harm_required` and joint-pass output. This plan performs no calculation now.
5. Assign at least 13 pilot or 18 confirmatory people and audit role and exposure histories.
6. Freeze compensation, active/wait/calendar time, availability and replacement coverage for every person.
7. Freeze every AI call and token category, including distinct Q and R support and both family sets.
8. Confirm exact model/tier and official prices at that future time.
9. Calculate worst-case cash, people time, calendar, calls and tokens.
10. Obtain explicit user approval of `B_cash`, `B_active_time`, `B_wait_time`, `B_calendar`, `B_calls` and `B_tokens`.
11. Version and hash the calculation, roster, exposure ledger state, assumptions and approvals.
12. Only then may the exact separate material-authoring gate be requested.

Keep authoring at zero if either family set is under its required vector count; staffing or replacement coverage is missing; Q/R isolation fails; an AI-call category is absent; the single representation reference is unavailable; or B, harm challenges, fresh sessions, redaction, blinding or safety would need removal to fit the ceiling.

Cost reduction order is: remove optional C, remove optional AI judge, remove nonessential AI support, reduce result-independent repetitions, or propose a newly reviewed narrower question. Do not reduce independent-family counts, merge `F_R` and `F_H`, combine Q with leakage or relevance, remove B, or weaken a guardrail.

## 8. Gates

### V3-G0 — `E0 EFFECT TEST DESIGN V0.3 REVIEW`

Requires matching v0.3 Markdown sidecars, frozen earlier files, versioned package index, and a fresh hostile read-only review with F-01/F-02/F-03 plus preserved-correction verdicts. Passing allows CONTROL integration review only.

### V3-G1 — `E0 SINGLE REPRESENTATION INTERFACE READY`

Requires exactly one authenticated `selected_representation_ref` and the visibility, citation, resource and limitation links. A fallback must have identical artifact status. Failure keeps authoring closed.

### V3-G2 — `E0 ENDPOINT STAFFING AND CEILING APPROVED`

Requires:

- disjoint `F_R`/`F_H`, all eight count rows, two-set power vector and joint-pass output;
- at least 13 or 18 eligible people as applicable, exposure chronology, compensation, time, availability and absence coverage;
- separate relevant, harm and reserve call/token/workload maxima;
- all-AI-support and worst-case cash ceilings;
- explicit user approval.

A combined family count or the former 14-person path fails this gate.

### V3-G3 — `E0 MATERIAL AUTHORING OPEN`

Requires V3-G0 through G2 and the user's explicit opening of this exact gate in the current thread, plus role input allowlists, output ownership and external oracle custody. It opens synthetic material authoring only, not code, calls, execution or scoring.

### V3-G4 — `E0 PREFLIGHT AND CALIBRATION OPEN`

Requires all material hashes; two leakage passes; both Q quality and guess locks before relevance release; both fresh R relevance passes; exposure and chronology audit; redaction/guess and adjudication calibration plans; safety-block plan; and recalculated ceilings. It does not open effect execution.

### V3-G5 — `E0 A-D PILOT EXECUTION OPEN`

Requires separate pilot preregistration, 13-person availability, no reuse of confirmatory families, current model/price/resource confirmation, blind adjudication, redaction/QC and safety monitoring. Its output can only decide whether A/B/D costing is worth review.

### V3-G6 — `E0 A-B-D CONFIRMATORY EXECUTION OPEN`

Requires pilot advance without treating it as effect evidence; V3-G4 B-package acceptance; 18-person eligibility and availability; all eight endpoint counts and both required set sizes; frozen margins, multiplicity and joint-pass calculation; refreshed worst-case ceiling and user approval; and another result-blind independent review.

### V3-G7 — `E0 OPTIONAL C OR EXTENSION OPEN`

C/D, four conditions, another model, another task population, retrieval comparison or any overlapping family design requires its own question, set memberships, endpoint counts, power, staffing, budget, preregistration and approval. Earlier results do not open it.

## 9. Block release and rollback

- Release only frozen-size blocks after transport checks, blind critical clearance and staff availability.
- A critical candidate stops new calls; confirmed critical stops the full run regardless of condition.
- A missing Q/R lock, exposure breach or review disagreement rejects the whole B package.
- A family-count shortfall in either set prohibits confirmation; do not add instances or borrow families.
- Hash mismatch, unledgered AI call, price/resource drift, shared state, raw cue, redaction asymmetry, adjudication ambiguity or ceiling overrun stops the affected work under the preregistered rollback.
- Invalid or contaminated outputs are never joined to clean samples. Results cannot justify changing thresholds, sets, counts, retries, conditions, redaction or staffing.

## 10. Unresolved feasibility and bounded status

It is unknown whether 18 eligible people and compensation can be obtained, Q and R exposure isolation can be maintained, both independently powered family sets can fit a ceiling, a useful but irrelevant B can pass both review layers, redaction can preserve meaning while passing both blinding strata, or a single representation artifact will be approved.

These are future stop conditions, not implicit commitments. v0.3 remains design-only and awaits a new independent read-only review.
