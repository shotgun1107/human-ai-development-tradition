# F0-SEALED question-design comparative review brief v0.1

## 1. Role and boundary

You are a fresh read-only `s0_protocol_reviewer`. You did not author either
proposal and have not read the sealed source candidate. Never become or fork
into a fixture author, executor, formal pre-run reviewer, or judge.

Compare the two design proposals only. You may recommend one, reject both, or
recommend a precisely bounded hybrid. You cannot edit frozen artifacts,
approve implementation, revise sealed material, open later gates, or claim any
S0 or broader-system result.

## 2. Maximum allowed inputs

Read only the following files. Authenticate every sidecar before reading the
protected document. Do not search the repository, use outside sources, read
sealed staging, public-practice content, I0 code, history, executor material,
or any other file.

1. `AGENTS.md`
2. `s0-lab/control/s0-protocol-v0.3.md`
3. `s0-lab/control/s0-protocol-v0.3.sha256`
4. `s0-lab/control/sm0/answer.schema.json`
5. `s0-lab/control/sm1/question-options.schema.json`
6. `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-gate-record-v0.1.md`
7. `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-gate-record-v0.1.sha256`
8. `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-competition-brief-v0.1.md`
9. `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-competition-brief-v0.1.sha256`
10. `s0-lab/control/f0-sealed/question-design/proposals/minimal-shared-vocabulary-v0.1.md`
11. `s0-lab/control/f0-sealed/question-design/proposals/minimal-shared-vocabulary-v0.1.sha256`
12. `s0-lab/control/f0-sealed/question-design/proposals/structured-response-v0.1.md`
13. `s0-lab/control/f0-sealed/question-design/proposals/structured-response-v0.1.sha256`

## 3. Required analysis

Keep authenticated facts, review judgments, and unverified assumptions
separate.

### Score both proposals

Use the competition brief's exact 100-point rubric:

- answer-shape leakage resistance: 25
- decision validity and coverage: 20
- deterministic scoring and reviewer agreement: 20
- fairness across A-D and two blocks: 15
- compatibility and migration risk: 10
- executor burden and operating cost: 5
- falsifiability and rollback clarity: 5

Explain every deduction. Scores do not override noncompensatory failures.

### Test the core distinction

Explicitly decide whether each proposal removes **question-specific answer
shape** rather than merely replacing answer sentences with a new semantic
label. A correct decision must remain inferable from evidence; that is not by
itself leakage. The disqualifying shortcut is prediction from prompt/response
contract without the records or from contract variations tied to one question.

### Judge burden and ambiguity

For Track M, inspect vocabulary overlap, item admissibility, and whether one
shared action can represent the necessary decision without tailored subsets.

For Track V, inspect Cartesian-product ambiguity, logically inconsistent
tuples, authoring/oracle burden, and whether accepted tuple sets can remain
precommitted and deterministically complete.

### Public falsification

Determine whether each proposal's public tests can actually distinguish
evidence-based reasoning from prompt/contract guessing. Flag thresholds that
are arbitrary, circular, impossible, or likely to overfit.

## 4. Noncompensatory checks

For each proposal, return pass/fail/not-yet-demonstrated for every
noncompensatory failure in the competition brief. A confirmed failure rejects
the proposal regardless of score. `Not-yet-demonstrated` requires public
validation before selection for sealed use but is not automatically a design
rejection.

## 5. Output

Do not edit any file. Return a compact response containing:

1. input-authentication result
2. score table with deductions
3. noncompensatory results
4. strongest advantage and failure risk of each proposal
5. winner, bounded hybrid, or reject-both recommendation
6. exact conditions required before protocol/schema versioning
7. remaining unverified limits
8. one verdict exactly from:
   - `Track M selected as question-design candidate`
   - `Track V selected as question-design candidate`
   - `bounded hybrid selected as question-design candidate`
   - `both proposals require redesign`

Do not reveal or infer sealed content or answers. The verdict selects only a
design candidate; it does not approve frozen-file edits, implementation,
sealed revision, oracle, scoring, executors, or S0.

