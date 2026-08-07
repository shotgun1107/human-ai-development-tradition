# CONTROL decision — URC-0.4 independent review v0.1

## Decision

- gate: `F0-PUBLIC QUESTION CONTRACT V0.4 INDEPENDENT REVIEW OPEN`
- independent-review verdict: `URC-0.4 requires question-contract redesign`
- CONTROL disposition: **ACCEPT REVIEW VERDICT**
- v0.4 status: **REJECTED FOR PUBLIC AUTHORING PROTOCOL DESIGN**
- gate state after this record: **CLOSED**
- public fixture authoring: **NOT AUTHORIZED**
- implementation, execution, sealed access, executors, and S0: **NOT AUTHORIZED**

URC-0.4 remains preserved at its existing hash as a failed candidate. It must not be edited in place, quietly relaxed, or treated as a passing baseline.

## Authenticated review evidence

| Artifact | SHA-256 |
|---|---|
| independent-review gate record v0.1 | `fa1f6082ac2d6555cef7180e4bf4d584a3acb3b3ad322485875b9cbb4e5eb04b` |
| independent-review brief v0.1 | `33d8d2856787f8b64152b2a0cf99d61f5a5c77ed634da046d5f119a8ba3302fa` |
| independent review v0.1 | `07e06f4735fc85438071a36522ac6f07d6b812bf3cbfee0e7f4b59044bfaaec9` |

The reviewer authenticated all allowed inputs, read no sealed material or outside source, performed no file writes, and found four Critical, three Major, and one Minor issue. The review score was 44/100, but the decision is governed by the noncompensatory failures rather than the total.

## CONTROL acceptance reasoning

CONTROL accepts the redesign verdict for four independent reasons:

1. **The six outcomes are not globally exclusive.** `prohibit`, `defer`, and `preserve` can all be supported by one ordinary combined record. Exact-one labeling therefore depends on an unstated priority or rejects realistic questions to hide ambiguity.
2. **The fixed error precedence loses information.** Counting one primary event prevents duplicate scoring, but the current order can suppress citation and affected-scope observations needed by predecessor M1, M4, or C4.
3. **The leakage gate is statistically incomplete.** The 33/180 calculation is correct, but four blocking original/neutral tests do not share a fully allocated familywise error budget, and the paired five-point rule is not a powered equivalence decision.
4. **The representation-alignment experiment is not reproducible.** The single-code control, estimator, covariance model, session unit, confidence algorithm, and deterministic sample escalation remain open.

These are not wording defects. They affect what the contract means and whether a later pass could be trusted. A bounded v0.4 wording revision is therefore insufficient.

## Elements that remain usable as design evidence

Rejection does not discard every idea. A successor may reuse these reviewed principles only after restating them under a new version:

- one response contract identical across all questions and conditions;
- no question-specific options, policies, examples, or enum narrowing;
- removing a redundant `state_effect` remains defensible when the prompt unambiguously names the operation;
- one envelope-level `response_contract_id`;
- exact structured observations separate from unscored prose;
- analytic compact-output budgeting below the 8,192-byte hard limit;
- hash equality, role separation, fresh-bank discipline, rollback, and bounded claims.

The following v0.4 elements must not be carried forward without redesign:

- the current six-row semantics;
- the generic field-order primary-error precedence;
- the current P2 multiplicity and paired rule;
- the under-specified single-code alignment control and sample escalation;
- ambiguous visibility of the answer-bearing serialization example;
- the unfixed session topology and cost ceiling.

## Required v0.5 redesign questions

A new design gate must answer, before any fixture or implementation work:

1. What globally exclusive outcome rule replaces or governs `prohibit`, `defer`, and `preserve`?
2. Can abstract combined-record countercases always produce one result without prompt hints, multiple accepted outputs, or prose interpretation?
3. How can one primary score per question preserve every essential predecessor C/M observable? If that is impossible, which invariant should change and why?
4. What universal decision tree maps atomic observations to C/M families without question-author discretion?
5. What is the full P2 hypothesis family, alpha allocation, paired estimand, equivalence interval, and prospective power rule?
6. What exact single-code control, estimator, resampling unit, session topology, covariance model, CI algorithm, and smallest-sufficient-sample algorithm define P3?
7. What model-call, token, human-time, elapsed-time, and monetary ceiling makes the public validation operationally acceptable?
8. What normative canonical JSON serialization and byte-measurement rule governs boundary checks?
9. How are all answer-bearing examples guaranteed CONTROL-only and absent from runner-visible artifacts?

## Next exact gate

If the user chooses to continue, the recommended next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.5 REDESIGN OPEN`

That gate should create a new v0.5 design path and may use only public design inputs. It must not edit v0.4 in place, create fixtures or executable schemas, run tests, access sealed material, or claim validation.

## Claims not made

This decision does not establish that any replacement grammar will work, that the public test is affordable, that the held source is compatible, or that S0 or any broader system has been implemented or validated.
