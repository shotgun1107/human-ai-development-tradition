# F0-SEALED source candidate limited review v0.1

- review_role: fresh read-only `s0_protocol_reviewer`
- candidate: `s0-lab/f0-sealed-staging/v0.1-source-candidate/`
- review_scope: limited source-authoring decision only

## Input authentication

**PASS**. The review brief and all four sidecar-protected prerequisites matched
SHA-256. Embedded AGENTS and schema hashes matched. The candidate ledger had
exactly ten safe, unique, non-self entries with no missing, extra, or
mismatched file.

## Findings

### Critical

None.

### Major

#### FSR-M-01 — insufficient block independence

The blocks are near-isomorphic in record-role and relation topology and in
their one-to-one question families. Renaming, paraphrasing, and reordering do
not establish material independence.

Evidence locations:

- `blocks/*/canonical-input.json:item_index`
- `blocks/*/canonical-input.json:records[*].record_kind`
- `blocks/*/canonical-input.json:records[*].explicit_relations`
- `blocks/*/question-options.json:questions[*]`

#### FSR-M-02 — semantic answer cues

Some prompts and options provide strong answer cues. Decisive relations are
sometimes restated, while narrowly qualified options are conspicuously longer
and contrasted with categorical or manifestly unauthorized distractors.

Evidence locations:

- `blocks/*/runner-question-options.json:questions[*].runner_prompt`
- `blocks/*/runner-question-options.json:questions[*].options[*].runner_text`

### Minor

None.

## A-E result

| Area | Result |
|---|---|
| A. Scope and provenance | pass |
| B. Protocol item coverage | pass |
| C. Independence and leakage | fail |
| D. Question fairness and sufficiency | fail |
| E. Honest limits | pass |

## Verdict

`source candidate requires revision before CONTROL decision`

This verdict is not complete F0 approval, pre-run approval, an oracle or
scoring gate, transformation approval, executor approval, or an S0 result.

## Remaining unverified limits

- oracle and scoring consistency
- actual A-D equality of source information, authority, model/reasoning
  conditions, time, limits, and scoring opportunities
- four-condition transformation equivalence and the 15% byte ceiling
- provenance reports and oracle-derived relation checks
- formal pre-run approval, executor isolation, or any S0 outcome

