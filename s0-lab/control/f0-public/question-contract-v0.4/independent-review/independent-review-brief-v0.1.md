# URC-0.4 independent-review brief v0.1

## Assignment

Act as a hostile but symmetric design reviewer. Determine whether URC-0.4 is sufficiently coherent and falsifiable to justify designing a later public authoring protocol. Do not reward length, apparent rigor, or conservative wording. Look for a contract that cannot express its intended decisions, a test that cannot establish its stated gate, hidden discretion, false determinism, answer leakage, C/D alignment, unaffordable validation, and conflicts with frozen predecessor boundaries.

Facts, reviewer inferences, and recommended changes must be explicitly distinguished.

## Required verification

1. Authenticate every allowed input before relying on it.
2. Report the exact allowlist used and confirm no sealed or outside input was read.
3. Verify that the candidate changes no frozen predecessor artifact.
4. Reproduce rather than trust the six-of-sixteen matrix count, 7,680-byte formula, and the 180-trial leakage threshold claim.
5. Treat “specified,” “analytically bounded,” and “empirically demonstrated” as different evidence states.

## Scoring rubric

Score each candidate dimension with written deductions. Total score cannot override a noncompensatory failure.

| Dimension | Points |
|---|---:|
| semantic coherence and intended-decision coverage | 20 |
| answer-shape leakage resistance | 20 |
| deterministic adjudication and no double-counting | 15 |
| A–D and two-block measurement fairness | 15 |
| statistical validity and falsifiability of the public plan | 15 |
| resource, operating-cost, and one-person feasibility | 10 |
| versioning, rollback, role isolation, and claim boundaries | 5 |
| **Total** | **100** |

## Noncompensatory checks

For each, return `PASS`, `FAIL`, or `NOT YET DEMONSTRATED` with a concise reason:

1. The six-pair grammar is internally coherent without question-specific exceptions.
2. The intended predecessor decision families can be represented without multiple accepted decisions or prose interpretation.
3. Runner-visible prompt/schema/codebook cannot narrow the likely answer by question-specific shape.
4. A question produces at most one primary scored event without suppressing an error essential to the predecessor C/M logic.
5. No A–D condition receives more information, opportunity, or grammar alignment by design.
6. The public leakage test has a valid chance definition, multiplicity handling, numeric ceiling, and reproducible threshold.
7. The representation-alignment test can produce a genuine equivalence decision with pre-result sample-size control.
8. Resource bounds are derived from enforceable constraints rather than asserted caps.
9. The plan can be operated without sealed inputs and without using pilot results as confirmation.
10. The package makes no implementation, sealed-compatibility, S0, safety, economic, or transfer claim.

A confirmed failure in items 1–4, 6–8, or 10 prohibits the first verdict. Item 5 may be `NOT YET DEMONSTRATED` only if a sound noncompensatory public test is fully specified. Item 9 may be `NOT YET DEMONSTRATED` only if the next gate is limited to authoring-protocol and cost design, not fixture creation.

## Required adversarial analyses

### Six-pair semantics

- Construct abstract countercases for `prohibit + none`, `prohibit + data_only`, `defer + none`, `defer + human_decision`, and `preserve + none` without using any fixture content.
- Determine whether the differences can be recovered from records rather than prompt wording.
- Determine whether `state_effect` removal discards a scored decision or correctly removes a redundant prompt feature.
- Check whether exactly one accepted pair is realistic or merely forces disagreement to be hidden as question rejection.

### Determinism and scoring

- Trace a wrong decision plus wrong citation plus wrong affected set through the precedence rule.
- Check whether diagnostic-but-unscored mismatches preserve the predecessor's critical observables.
- Check whether later question-specific primary mappings reintroduce hidden discretion.

### Leakage and alignment

- Separate permitted inference from supplied records from forbidden prediction using only prompt/schema/codebook.
- Check whether the operation named in a prompt determines any response field.
- Examine whether the two-field grammar maps more directly to C/D than A/B.
- Assess whether the single-code control is semantically equivalent enough to isolate grammar alignment.

### Statistics and costs

- Recalculate the 33/180 one-sided 97.5% Clopper–Pearson claim.
- Assess the paired neutral-token five-point rule and its power.
- Check whether an unspecified increase above 180 preserves precommitment.
- Assess whether the ±10-point, 90% CI equivalence gate and ≥80% prospective power rule are operationally complete.
- Estimate minimum session topology and identify missing budget variables; do not invent prices.

### Resources

- Recalculate `8 × 896 + 512`.
- Determine whether the field-level limits actually imply the 896-byte object cap, including JSON escaping and whitespace.
- Separate the existence of a compact canonical serialization from the probability that a first model output satisfies the hard limit.

## Required findings format

List findings by severity:

- `Critical`: invalidates the candidate direction or a noncompensatory gate;
- `Major`: bounded design change required before another review;
- `Minor`: clarification that does not change the central design.

For each finding give:

- ID and severity;
- verified fact;
- reviewer inference;
- falsification or correction needed;
- consequence if unresolved.

## Required conclusion

Return:

1. authenticated-input statement;
2. 100-point rubric table;
3. noncompensatory table;
4. severity-count summary;
5. the three most important findings;
6. bounded corrections, if any;
7. remaining unknowns and prohibited claims;
8. exactly one verdict line from this list:

`URC-0.4 may proceed to public authoring protocol design`

`URC-0.4 requires bounded revision before another review`

`URC-0.4 requires question-contract redesign`

The first verdict does not authorize public fixtures, implementation, runs, sealed access, or S0.
