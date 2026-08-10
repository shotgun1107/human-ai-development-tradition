# CONTROL decision — F0-SEALED question design v0.1

## Decision status

- Gate: `F0-SEALED QUESTION DESIGN REOPEN`
- Outcome: **Track V selected conditionally as the successor question-design candidate**
- Gate state after this record: **closed**
- Authorization granted: selection of a design direction only
- Authorization not granted: protocol or schema modification, sealed-source access or revision, fixture creation, oracle creation, scoring implementation, package creation, executor launch, or S0 execution

This is not an approval of Track V as written, and it is not an S0 pass. It selects the response-contract family that the next separately opened design gate may refine and attempt to falsify.

## Protected evidence considered

| Artifact | SHA-256 |
|---|---|
| Question-design gate record v0.1 | `364b4d712c9c17b16325c859d7248668af1c171884704a43f120ffd2c0d1a7f3` |
| Question-design competition brief v0.1 | `908777a514d25bd9707e7c0b94d3160f758b1c70ac1d311f65ef604677a4d2a7` |
| Track M proposal v0.1 | `10416179fa97eaa7dcc692f78fa2d289443b6b0e4d9be9c6d665940602ce4b55` |
| Track V proposal v0.1 | `5f55208f5b0a2c41d0b723cdf92aa53ce3b77a700fa424da3d5b434dd08bd032` |
| Comparative-review brief v0.1 | `5bc66dcde88631ce132ef51efb7efe85d6fd2a61f4c317a98a5da07964a826a2` |
| Independent comparative review v0.1 | `4d62506c941c2695eb7861db825a58f4814637ffa846dd27e792b17177f29795` |

The independent reviewer authenticated its maximum allowlist, did not read sealed staging, made no file writes, and scored Track M 68/100 and Track V 70/100. The two-point total difference alone is not the basis of this decision.

## CONTROL reasoning

### Why Track M was not selected

Track M is simpler to operate and easier to score, but it does not fully remove the defect that reopened this gate. Its local answer sentences disappear, yet question-varying citation and affected-ID policies remain visible. Its ten semantic labels can also overlap, so making exactly one label correct may recreate question-specific tailoring. It therefore offers the safer migration but the weaker correction of FSR-M-02.

### Why Track V was selected

Track V gives every question the same response axes, values, and obligations. It removes question-local option lists and visible per-question contract changes. This most directly attacks the ability to predict an answer shape from the question contract instead of reading the supplied records.

The selection is conditional because the draft’s 96 possible tuples create a different threat: incoherent combinations, incomplete accepted-answer sets, coordinate double-counting, added executor burden, and possible alignment with the more structured C/D representations. Selection means “develop and test this family,” not “freeze these exact axes and values.”

## Mandatory successor-design conditions

Before any successor protocol or schema can be frozen, a separately authorized design task must satisfy all of the following without reading sealed questions:

1. Define the exact object governed by each axis.
2. Either show that every tuple is coherent or precommit one global admissibility matrix that is identical for all questions. Per-question narrowing is forbidden.
3. Demonstrate, using only public synthetic examples, that the response contract can express the intended decision families without new sealed-specific terms.
4. Map every structured mismatch to a precommitted observation event without double-counting one answer.
5. Reconcile the `response_contract_id` inconsistency noted by the reviewer.
6. Prove worst-case serialized output fits the 8,192-byte limit.
7. Define exact equality checks for A–D question/schema hashes, model, reasoning level, authority, time, output limit, retries, and judge-visible inputs.
8. Precommit numeric leakage, reviewer-agreement, representation-alignment, and executor-burden tests before observing their results.
9. Give the next independent reviewer an explicit rejection rule if the response grammar itself advantages C or D.
10. Preserve the ability to roll back to the last frozen public baseline; no result-dependent threshold changes are allowed.

## Public falsification required before sealed reuse

The next candidate must fail closed if any of these occur in a precommitted public test:

- a no-record observer predicts structured answers above the frozen leakage limit from the full runner-visible prompt, schema, and codebook;
- independent comparators disagree on exact accepted outputs beyond the frozen limit;
- an incompatible tuple is accepted or a coherent tuple cannot be represented;
- the contract creates a material relative advantage for a neutral C/D-style representation over an option-free control;
- the worst-case valid response exceeds the resource limit;
- any A–D condition receives different questions, rules, opportunities, or judge-visible information other than the intended representation treatment.

The numeric thresholds, sample size, power or equivalence margin, chance definition, and multiple-comparison handling must be frozen before the tests. This decision does not invent those values after the fact.

## Boundary and next gate

The sealed source candidate remains on HOLD. No sealed question, answer, oracle, or scoring content was examined or changed under this gate.

If the user wants to continue, the recommended exact next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.4 DESIGN OPEN`

That gate should be limited to a public, non-sealed successor contract design and its falsification plan. It must not authorize sealed rewriting, implementation, executors, or S0 execution. After that design is independently reviewed and its public checks pass, CONTROL may decide whether a separate sealed-source revision gate is justified.

## Claims explicitly not made

This decision does not establish that Track V works, that its 96-tuple draft is valid, that A–D are fair in execution, that the sealed source is usable, or that S0 or any broader system has been implemented or validated. It establishes only a protected, review-backed direction for the next design step.
