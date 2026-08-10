# F0-SEALED source revision 1 limited rereview v0.1

- rereview_role: fresh read-only `s0_protocol_reviewer`
- reviewed_candidate: revision 1
- decision_scope: source-authoring decision only

## Input authentication

**PASS**. The rereview brief and four protected prerequisites matched
SHA-256. The schema matched its freeze record. The candidate ledger had
exactly ten unique, safe, self-excluding entries with no missing, extra, or
mismatched file.

## Finding resolution

### FSR-M-01 — resolved

Material differences now exist in project roles, derivative direction,
withdrawal placement, responsibility allocation, evidence paths, and question
grouping.

Evidence locations:

- `blocks/*/canonical-input.json:projects`
- `blocks/*/canonical-input.json:records[*].explicit_relations`
- `blocks/*/question-options.json:questions[*]`

### FSR-M-02 — unresolved (Major)

Length and order improved, but runner-visible evidence options still contain a
condition-structural grouping concept prohibited by protocol §6.1 and may
favor a relationship-rich representation. Several sets retain one uniquely
bounded or status-preserving option against categorical, expansive, or
manifestly unauthorized alternatives.

Evidence location:

- `blocks/*/runner-question-options.json:questions[*].options[*].runner_text`

## Regression check

- Critical: none
- Major: FSR-M-02
- Minor: none
- scope and synthetic-data boundary: pass
- protocol §4.1 counts and explicit source support: pass
- prohibited-material boundary: pass
- honest limits: pass

## Verdict

`revision 1 requires further revision before CONTROL decision`

## Remaining unverified limits

- actual A-D equality of source information, authority, model/reasoning
  conditions, time, limits, and scoring opportunities
- transformation equivalence and byte ceiling
- oracle/scoring and provenance checks
- formal pre-run approval, executor isolation, judging, and any S0 or
  broader-system outcome

