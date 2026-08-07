# URC-0.4 public falsification plan v0.1

- status: **test-design proposal only**
- governed candidate: `URC-0.4-CANDIDATE`
- permitted data: newly authored synthetic public material only
- prohibited data: sealed source, eventual S0 oracle, real/customer/personal/secret/past-project material
- current gate authorization: design only; no bank, labels, implementation, sessions, or measurements may be created or run

## 1. Purpose and decision rule

This plan tries to reject URC-0.4 before it can influence sealed authoring. It does not try to demonstrate that S0 or a representation effect works.

URC-0.4 may advance beyond public validation only if every noncompensatory gate in section 9 passes under thresholds frozen before results. A high total score cannot compensate for one failed gate. Any contract, threshold, sample, label, or analysis change after results requires a new version and a fresh unaffected bank.

## 2. Required role separation

Later exact gates must create fresh roles with these boundaries:

| Role | May see | Must not see |
|---|---|---|
| public fact author | public synthetic scenario requirements and URC codebook | sealed material, later executor outputs |
| independent label author A | frozen public facts and URC codebook | author B's labels, outputs |
| independent label author B | same as A | author A's labels, outputs |
| prompt-leakage reviewer | runner prompts, schema, codebook; no records | labels, record bodies, sealed material |
| public representation builder | frozen public canonical facts and representation rules | labels, outputs |
| comparator builder 1 | public adjudication format and mutation specification | comparator 2 implementation |
| comparator builder 2 | same public specifications | comparator 1 implementation |
| public executors | one assigned public representation, common questions, common response contract | labels, other conditions, other outputs |
| public judge | anonymous outputs, condition-neutral public facts, precommitted public adjudication bundle | condition identity, timing, cost, other unjudged outputs |
| CONTROL | hashes, role records, final frozen findings | must not change thresholds after results |

Public test labels are not the S0 hidden oracle. Nevertheless, they must remain outside executor-visible worktrees and prompts. Worktree separation alone is not treated as secret isolation.

## 3. Bank topology and freeze order

### 3.1 Confirmatory public bank

The planned confirmatory bank contains 180 independent synthetic questions, balanced exactly across the six URC decisions: 30 questions per decision. Questions are grouped into blocks of at most eight only after labels are frozen. No block may contain a duplicate scenario template with changed nouns only.

The exact sample size of 180, tuple balance, scenario-family allocation, prompt text, facts, labels, analysis code, randomization seed, model ID, reasoning level, and thresholds must be frozen and hashed before any confirmatory observer or executor sees the bank.

If prospective power analysis performed before bank freeze shows that 180 is insufficient for the representation-alignment equivalence test in section 7, CONTROL may increase the sample once, before data, using the written power rule. It may not reduce the bank or alter the ±10 percentage-point margin. The increased size and allocation then become the frozen sample size.

### 3.2 Holdout discipline

- Contract development examples cannot enter the confirmatory bank.
- Any question seen while clarifying URC wording is development material and cannot be restored as holdout.
- Label-author disagreement on a confirmatory question fails the bank version; the item is not silently dropped or rewritten after other labels are inspected.
- A revised contract requires a newly authored confirmatory bank or a previously frozen, untouched reserve whose prompts, facts, and labels were never opened during revision.

### 3.3 Freeze order

1. URC candidate and this plan independently reviewed.
2. Public authoring protocol, bank topology, and role allowlists frozen.
3. Canonical public facts and questions authored.
4. Label authors work independently.
5. Agreement and admissibility checked without executor results.
6. Representation forms, public adjudication bundle, and run manifests frozen.
7. Comparator mutation set and implementations frozen.
8. No-record leakage tests run.
9. Representation-alignment and burden runs conducted only if earlier blocking gates pass.
10. Anonymous judging and CONTROL result decision.

## 4. Gate P0 — static contract coherence

### Inputs

Only the reviewed URC specification and later executable schema candidates.

### Required checks

- exactly six and only six decision pairs are accepted;
- all other 10 combinations from the four-by-four Cartesian space are rejected identically for every question;
- `response_contract_id` appears once at the envelope level and cannot vary by question;
- runner questions contain only `question_id` and `runner_prompt`;
- there is no per-question enum, policy, example, or accepted-answer field;
- all codebook tokens and definitions are byte-identical across A–D and both blocks;
- one decision mismatch produces one boolean observation, not coordinate-level events;
- a maximal canonical block serialization is at most 7,680 bytes and a final output above 8,192 bytes is rejected.

### Pass threshold

100% of the checks must pass in two independent reviews. Any disagreement or accepted seventh combination fails P0.

## 5. Gate P1 — independent public labeling and judge determinism

### Independent labeling

Label authors A and B independently produce, for all 180 questions:

- exactly one of the six structured decisions;
- normalized citation clauses and the complete allowed-citation set;
- exactly one affected-ID set;
- exactly one uncertainty value;
- the primary observation category that a mismatch would test.

They use the public facts and written contract only. Neither sees the other's work until both label bundles are hashed.

### Pass threshold

Exact normalized agreement is required on every discrete field for all 180 questions. Cohen's kappa or another chance-corrected statistic may be reported, but it cannot replace 180/180 exact agreement. One disagreement fails the bank version and requires contract clarification plus a new untouched bank.

### Judge repeatability

Two fresh reviewers independently apply the public adjudication contract to a frozen mutation set. Required result: 100% agreement on validation layer, all five atomic observations, and the single primary outcome. Free interpretation of `short_reason` is prohibited.

## 6. Gate P2 — no-record answer-shape leakage

### Test input

Each leakage observer receives the complete runner-visible prompt, full URC codebook, question projection, and answer schema, but no record bodies, record metadata, labels, bank-balance or frequency information, other batches, or examples with answers. Balance is known only to the frozen analysis plan.

Two independently prompted observer streams each predict one of the six exact decisions for all 180 questions. Each stream uses 15 independently fresh sessions of 12 questions, with no memory or output sharing between batches. This prevents a session from enforcing a bank-wide class quota. Batch allocation and order are set by a frozen seed.

### Chance and ceiling

- Balanced exact-tuple chance rate: `1/6 = 16.67%`.
- Material leakage ceiling: `25%` exact-tuple accuracy.
- Multiple-observer confidence: for each observer separately, the one-sided 97.5% Clopper–Pearson upper confidence bound must be at most 25%.
- With `n = 180`, this is satisfied only when that observer predicts at most 33 questions correctly; the design calculation gives an upper bound of approximately 24.77% at 33/180.

The two observer tests use the 97.5% bound as a Bonferroni allocation of an overall one-sided 5% error budget. Results are not pooled to hide one leaking observer.

### Neutral-token sensitivity

Each observer also receives a separately frozen version in which scenario names, target names, and record identifiers in the prompts are replaced consistently with neutral tokens while grammar and named operation remain intact.

For each observer:

- both original and neutral-token versions must independently satisfy the 25% upper-bound rule;
- the absolute paired accuracy difference must be at most 5 percentage points;
- an exact paired test is reported with Holm correction across the two observers.

The five-point comparison is a red-flag margin, not proof that lexical effects are absent.

### Blocking result

One observer above the ceiling, a prompt containing a decisive qualification, a codebook token echo, or a frequency imbalance fails P2. Passing means only that this public bank did not reveal a large answer-shape shortcut under the tested observers.

## 7. Gate P3 — representation alignment

### Question

Does the two-field URC grammar itself increase the relative advantage of structured C/D-style public representations compared with an option-free single-code control carrying the same six meanings?

### Design

- Use the same frozen canonical public facts in four neutral presentation forms modeled only on the structural differences A–D intend to test.
- Use fresh, one-turn sessions with identical model ID, revision, reasoning level, authority, tools, time, and output limits.
- Cross URC with a global single-code control whose six semantic meanings are identical and whose code list is also unchanged for every question.
- Use every confirmatory question unless prospective power analysis requires a larger frozen bank.
- Randomize grammar, presentation, block, and run order with a frozen seed.
- Do not provide correctness feedback or repairs.

The single-code control is a measurement control only. It is not selected as the successor contract and cannot be used for sealed authoring without a separate decision.

### Primary estimand

For grammar `g`, define:

`structured_gap(g) = mean_accuracy(C,D) - mean_accuracy(A,B)`.

The alignment effect is:

`structured_gap(URC) - structured_gap(single-code control)`.

The independent unit is the public question. Analysis uses a precommitted paired case-level randomization or bootstrap procedure that preserves all eight observations for each question.

### Equivalence threshold and power

- Material alignment margin: `±10 percentage points`.
- Pass only if the complete two-sided 90% confidence interval for the alignment effect lies inside `[-0.10, +0.10]`.
- Before bank freeze, simulation under the frozen allocation and expected control accuracy must show at least 80% power to declare equivalence when the true alignment effect is zero.
- If 180 questions is insufficient, increase the sample before data until the 80% power rule is met. Do not widen the margin or change the estimator.

Any interval crossing either margin fails P3. A null-hypothesis non-significant result is not an equivalence pass.

## 8. Gate P4 — comparator reliability, executor burden, and resources

### Comparator mutation set

A later authorized author creates public cases covering:

- every one of the six valid combinations;
- every one of the 10 invalid combinations;
- one controlled mismatch in each of the five atomic observation fields;
- malformed JSON, wrong hashes, missing and duplicate questions, extra fields, unsorted/duplicate IDs, unknown IDs, byte-limit boundaries, and prohibited reason content;
- multi-coordinate decision mismatches that must still produce only one primary decision event.

Two independently implemented comparators run the entire frozen set 100 times each.

Pass requires byte-identical normalized comparator output across all repeats and exact agreement between comparators on every case. One disagreement or nondeterministic result fails the gate.

### Executor burden

Compare URC with the single-code control from P3 using first outputs only.

All of these must pass:

- at least 95% of URC outputs are schema-conforming on the first attempt;
- URC first-pass schema success is no more than 3 percentage points below the control;
- maximum minus minimum URC schema-success rate across A–D is at most 5 percentage points;
- median elapsed time is no more than 20% above the control;
- median output bytes are no more than 20% above the control;
- no valid canonical response exceeds 7,680 bytes;
- no executor output exceeds the hard 8,192-byte limit;
- no question needs more than four cited or affected IDs or more than eight questions per block.

Elapsed time and output bytes are secondary to accuracy and cannot rescue a failed semantic or fairness gate.

## 9. Noncompensatory decision table

| Gate | Pass requirement | Failure action |
|---|---|---|
| P0 coherence | all static invariants, two-reviewer agreement | reject or version contract |
| P1 labels/judging | 180/180 exact label agreement; 100% judge agreement | discard bank version; clarify contract; use fresh bank |
| P2 leakage | both observers' 97.5% upper bounds ≤25%; neutral-token conditions pass | reject prompts or contract; new version and bank |
| P3 alignment | 90% CI wholly within ±10 points; ≥80% prospective equivalence power | reject or redesign grammar |
| P4 comparator | 100% deterministic agreement | reject implementation/contract ambiguity |
| P4 burden/resources | every listed threshold passes | reject or redesign within a new version |
| A–D equality | exact hash/resource/opportunity equality except representation | invalidate public suite |

There is no weighted total. All rows must pass.

## 10. Cost and stop rules

Before authoring or running the public bank, CONTROL must publish a token, elapsed-time, and monetary ceiling. If the estimated full confirmatory cost exceeds the approved ceiling, the test does not start and no scientific claim is made.

A cheap development pilot may be authorized later to debug mechanics, but:

- pilot cases and results cannot count toward confirmatory thresholds;
- pilot material cannot enter the confirmatory bank;
- contract changes after a pilot require a new candidate hash;
- a pilot pass cannot authorize sealed access.

Stop immediately if sealed content is encountered, labels leak to an observer or executor, a frozen hash changes, a role sees a forbidden input, or a threshold is altered after results. Preserve the incident record but do not reuse the affected bank.

## 11. Interpretation limits

Even a full pass would support only this bounded statement:

> Under the frozen synthetic public bank, observers, model revision, resource limits, and analysis rules, URC-0.4 did not trigger the precommitted large-leakage, adjudication, alignment, burden, or resource rejection thresholds.

It would not prove zero leakage, universal fairness, sealed-question compatibility, model stability, representation superiority, S0 success, production readiness, safety, economic value, central-system effectiveness, Project Brain integration, or model-to-model transfer.
