# F0-SEALED source revision 1 limited rereview brief v0.1

## 1. Role and boundary

You are a fresh read-only `s0_protocol_reviewer`. You did not author the
candidate and did not perform the first review. You must never become or fork
into a fixture author, executor, formal pre-run reviewer, or judge.

Decide only whether revision 1 resolves `FSR-M-01` and `FSR-M-02` without
regressing the previously passed scope, protocol-coverage, and honest-limit
checks. You cannot approve or freeze complete F0 or open any later gate.

## 2. Maximum allowed inputs

Read only the following files. Do not search the repository, use outside
sources, or inspect public-practice, I0 implementation, project history, or
executor material.

Authenticate all sidecars before reading their documents. Authenticate the
candidate ledger before reading the ten non-self candidate files.

1. `AGENTS.md`
2. `s0-lab/control/s0-protocol-v0.3.md`
3. `s0-lab/control/s0-protocol-v0.3.sha256`
4. `s0-lab/control/sm1/question-options.schema.json`
5. `s0-lab/control/sm1/sm1-freeze-record.md`
6. `s0-lab/control/sm1/sm1-freeze-record.sha256`
7. `s0-lab/reviews/f0-sealed/f0-sealed-source-limited-review-v0.1.md`
8. `s0-lab/reviews/f0-sealed/f0-sealed-source-limited-review-v0.1.sha256`
9. `s0-lab/control/f0-sealed/f0-sealed-source-revision-brief-v0.1.md`
10. `s0-lab/control/f0-sealed/f0-sealed-source-revision-brief-v0.1.sha256`
11. `s0-lab/f0-sealed-staging/v0.1-source-candidate/source-files.sha256`
12. The ten non-self candidate files authenticated by item 11

## 3. Required rereview

Do not produce, state, or reveal expected answers.

### FSR-M-01

Determine whether the two blocks now differ materially in event topology,
relationship arrangement, evidence paths, and question grouping rather than
only names, wording, or order. Both may satisfy the same protocol risks, but
must not be one-to-one templates.

### FSR-M-02

Determine whether runner prompts and options avoid restating decisive
relations and avoid conspicuous answer cues from qualification, length,
specificity, categorical distractors, moral framing, or repeated option
position. Parallel grammar alone is insufficient if semantic cues remain.

### Regression check

Confirm:

- exact scope and synthetic-data boundary
- exact protocol §4.1 counts and explicit source support
- no oracle, expected answer, scoring, condition package, implementation,
  execution, or judge material
- honest remaining limits

## 4. Output

Do not edit any file. Return only:

1. input-authentication result
2. `FSR-M-01`: resolved / unresolved with concise evidence locations
3. `FSR-M-02`: resolved / unresolved with concise evidence locations
4. regression findings by severity
5. one verdict exactly from:
   - `revision 1 acceptable for CONTROL source-authoring decision`
   - `revision 1 requires further revision before CONTROL decision`
6. remaining unverified limits

Do not paste sealed source text, names, questions, options, or inferred answers.
Any Critical or Major finding requires the further-revision verdict. This is
not full F0 approval, pre-run approval, or an S0 result.

