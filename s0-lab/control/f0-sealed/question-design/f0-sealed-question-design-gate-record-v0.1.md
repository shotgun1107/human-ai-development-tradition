# F0-SEALED question-design gate record v0.1

- opened_at: `2026-08-07` (KST)
- opening_signal: `F0-SEALED QUESTION DESIGN REOPEN`
- decision_role: `USER`
- control_role: `CONTROL`

## Opened scope

The user opened a design-only reconsideration of how S0 questions collect a
decision without leaking the likely answer through question-specific option
wording.

This gate permits:

- two independent question/answer-format proposals
- abstract, non-fixture examples
- explicit schema/protocol impact analysis
- a fresh read-only comparative review
- a CONTROL design decision

## Closed inputs and outputs

The sealed source candidate and all of its content remain closed to designers
and the comparative reviewer. They may use only the source-authoring HOLD
record and sealed-content-free review summary.

This gate does not authorize:

- edits to the sealed source candidate
- edits to frozen protocol or schema files
- new schema instances or implementation code
- hidden oracle, expected answers, rationale, or scoring content
- condition representations, transformation, packages, or mappings
- executor, pre-run reviewer, judge, S0 run, or scoring
- real, customer, personal, secret, brand, competition, outsourced, or
  past-project content
- commit, push, merge, branch creation, or publication

Any selected design must receive a new version, independent review, and a later
exact gate before it may alter frozen artifacts or the sealed candidate.

