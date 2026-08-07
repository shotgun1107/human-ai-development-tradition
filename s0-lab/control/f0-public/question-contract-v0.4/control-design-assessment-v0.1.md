# CONTROL assessment — URC-0.4 public design v0.1

## 1. Decision

- gate: `F0-PUBLIC QUESTION CONTRACT V0.4 DESIGN OPEN`
- design package status: **COMPLETE FOR INDEPENDENT DESIGN REVIEW**
- current gate after this record: **CLOSED**
- freeze status: **NOT FROZEN**
- public authoring status: **NOT AUTHORIZED**
- implementation and execution status: **NOT AUTHORIZED**
- sealed source status: **UNCHANGED AND ON HOLD**

URC-0.4 is ready to be challenged by a fresh independent reviewer. It is not ready to become a protocol, schema, public fixture contract, or sealed-source migration rule.

## 2. Protected design package

| Artifact | SHA-256 |
|---|---|
| gate record | `d1f2a41a4cfccf1e8e3e6bb8ceee186648e6dc2c4ea540f71e4b25f57a7aa806` |
| URC-0.4 candidate | `1a06737a8f7de90bdb8c0c467cf3bc0ccab236ced91e3fb364e91ea1dc1d4a82` |
| public falsification plan | `9649bcffa2b8d39a03077b7797e537912525ed664d57486fd28466b0ca0440a8` |

The predecessor protocol and schema hashes remained unchanged during the design task. No sealed staging path was read or modified.

## 3. Principal design change

Track V required three coordinates and allowed 96 combinations. URC-0.4 removes `state_effect` because the question already identifies the operation being decided. The new contract uses two fields and exactly six global combinations that are identical for every question.

This is not merely a smaller vocabulary. It changes the measured object:

- the prompt names the operation;
- the response states whether that operation is permitted, prohibited, deferred, or superseded by preservation of the current state;
- the response separately states whether direct action, data-only handling, human decision, or no handling follows;
- the operation's start/limit/pause/end type is not redundantly scored in the answer.

## 4. Predecessor-condition coverage

| Required condition from the prior CONTROL decision | URC-0.4 response | Current evidence state |
|---|---|---|
| define the object governed by each axis | one named operation; fixed `disposition` and `handling` meanings | specified, not tested |
| eliminate incoherent Cartesian tuples or use one global matrix | six global pairs; all other 10 pairs invalid for every question | specified, not implemented |
| show expressibility without sealed terms | public question-admissibility rule and future 180-question bank | planned, not demonstrated |
| prevent coordinate double-counting | one `decision_exact` boolean and one primary outcome by precedence | specified, not implemented |
| reconcile `response_contract_id` | one envelope-level ID only | resolved in design |
| prove resource compatibility | eight-answer, 896-byte-per-answer, 7,680-byte canonical budget | analytic bound specified; actual burden unmeasured |
| define A–D equality checks | exact hash, model, authority, opportunity, time, and limit list | specified, delivery unverified |
| precommit numeric public tests | 180-item leakage bank, 25% ceiling, ±10-point alignment margin, exact comparator and burden thresholds | designed, not frozen or run |
| reject grammar advantage for C/D | powered equivalence test against a single-code control | designed, not run |
| preserve rollback and prohibit result-dependent changes | versioned rejection, fresh-bank, and unchanged v0.3/SM0/SM1 rules | specified |

No table row is empirical evidence. “Specified” means the design contains a falsifiable rule.

## 5. Internal challenge findings

### Finding A — data-only semantics corrected

The first draft paired `permit + data_only`. That could falsely imply that an effectful named operation partly proceeded. Before hashing, CONTROL changed the global pair to `prohibit + data_only`: the named operation is rejected and only a non-effectful alternative is allowed.

This correction improves coherence but still requires independent review across varied public question types.

### Finding B — six combinations may collapse meaningful distinctions

The design intentionally maps multiple named operations to `permit + direct_action`. This is valid only because the operation itself is already in the question. A reviewer must test whether `prohibit`, `preserve`, and the two forms of `defer` remain uniquely distinguishable without relying on tailored prompts.

If reviewers need multiple accepted pairs, a seventh pair, or prose interpretation, the candidate fails rather than expanding after sealed access.

### Finding C — resource compatibility is conditional

The arithmetic guarantees that eight canonical answer objects capped at 896 bytes plus a 512-byte envelope fit within 7,680 bytes. It does not show that the held sealed candidate has at most eight questions per block, uses at most four relevant IDs, or can use 40-byte IDs. Those facts were deliberately not inspected.

If later authorized material exceeds these limits, URC-0.4 is incompatible and must be versioned before use.

### Finding D — validation cost is material

The confirmatory plan requires 180 independently labeled public questions and multiple no-record, representation, comparator, and burden runs. This is substantially larger than a mechanical schema check. Reducing it after results would undermine the leakage and equivalence claims.

Before public authoring, CONTROL must estimate token and monetary cost and obtain the user's approval for the fixed ceiling. A cheaper pilot may debug mechanics but cannot authorize sealed access.

### Finding E — representation alignment remains the central risk

Two structured answer fields may fit C/D representations more naturally than A/B. Identical prompts do not rule this out. The candidate therefore cannot advance based only on no-record leakage; the paired response-grammar equivalence test is noncompensatory.

### Finding F — current review is not independent

CONTROL authored and assessed the package in the same active context. This assessment can find contradictions but cannot supply the required independent challenge. No reviewer has yet authenticated the package, reproduced the statistical design calculations, or attempted to reject its semantics.

## 6. Independent review questions

A fresh reviewer should answer at least:

1. Are all six pairs coherent, mutually distinguishable, and sufficient for the stated public decision family?
2. Does removing `state_effect` improve validity, or does it hide a decision dimension required by the predecessor protocol?
3. Can prompt authors distinguish `prohibit`, `preserve`, `defer + none`, and `defer + human_decision` without encoding the answer in the prompt?
4. Does `prohibit + data_only` express a bounded alternative without becoming a compound option?
5. Is exactly one accepted pair per question realistic and independently reproducible?
6. Does the fixed precedence prevent double-counting without suppressing a critical error that the original C/M system must observe?
7. Are the 7,680-byte analytic bound and field caps internally sound?
8. Is the 180-question leakage calculation correct, including the “at most 33” threshold and multiple-observer correction?
9. Is the ±10-point representation-alignment margin defensible, and can the prospective power rule be executed without post-result discretion?
10. Can the public plan be operated by one person at acceptable cost without compromising role separation?
11. Do any fields, definitions, tests, or control grammars leak condition identity or favor C/D?
12. Are rollback, fresh-bank, and no-threshold-change rules strong enough to prevent a failed design from being rescued post hoc?

## 7. Required independent verdict

The next reviewer should return exactly one:

- `URC-0.4 may proceed to public authoring protocol design`
- `URC-0.4 requires bounded revision before another review`
- `URC-0.4 requires question-contract redesign`

Even the first verdict must not authorize fixture creation, implementation, public execution, sealed access, or S0. It permits only the next separately gated public authoring-protocol design.

## 8. Next exact gate

Recommended next gate:

`F0-PUBLIC QUESTION CONTRACT V0.4 INDEPENDENT REVIEW OPEN`

That gate should provide a fresh read-only reviewer only the current `AGENTS.md`, this protected design package, the selected Track V decision, and the frozen predecessor protocol/schema files. It must not provide sealed staging or allow file edits.

## 9. Claims not made

This assessment does not claim that the response contract is correct, that public validation passed, that the test plan is affordable, that the held source can migrate, that A–D are fair in execution, or that S0 or any broader system has been implemented or validated.
