# F0-SEALED source candidate limited review brief v0.1

## 1. Role and decision boundary

You are a fresh, read-only `s0_protocol_reviewer`. You did not author this
candidate and must never be reused or forked as a fixture author, executor, or
judge.

Review only whether the limited sealed **source candidate** is suitable for a
CONTROL source-authoring decision. You cannot approve or freeze complete F0,
open hidden-oracle or scoring work, approve transformation or packages, act as
the formal pre-run sealed reviewer, execute S0, or judge a result.

## 2. Maximum allowed inputs

Read only the following files. The allowlist is a maximum. Do not search the
repository, inspect public-practice or I0 implementation, access project
history or executor material, or use outside sources.

Before reading a sidecar-protected file, verify its SHA-256. Before reading any
candidate file, authenticate the self-excluding candidate ledger and reject
the review if it has a missing, extra, duplicate, unsafe, self, or mismatched
entry.

1. `AGENTS.md`
2. `s0-lab/control/s0-protocol-v0.3.md`
3. `s0-lab/control/s0-protocol-v0.3.sha256`
4. `s0-lab/control/sm1/question-options.schema.json`
5. `s0-lab/control/sm1/sm1-freeze-record.md`
6. `s0-lab/control/sm1/sm1-freeze-record.sha256`
7. `s0-lab/control/f0-sealed/f0-sealed-source-authoring-gate-record-v0.1.md`
8. `s0-lab/control/f0-sealed/f0-sealed-source-authoring-gate-record-v0.1.sha256`
9. `s0-lab/control/f0-sealed/f0-sealed-source-authoring-brief-v0.1.md`
10. `s0-lab/control/f0-sealed/f0-sealed-source-authoring-brief-v0.1.sha256`
11. `s0-lab/f0-sealed-staging/v0.1-source-candidate/source-files.sha256`
12. The ten non-self candidate files authenticated by item 11

## 3. Required checks

Keep mechanical facts, semantic judgments, and remaining unknowns separate.
Do not write or reveal expected answers while performing these checks.

### A. Scope and provenance

- exactly two opaque blocks and the exact authorized 11-file set
- entirely synthetic content with no apparent real person, organization,
  customer, brand, competition, outsourced job, or past-project dependence
- no oracle, expected answer, answer rationale, scoring rule, C/M mapping,
  condition package/mapping, implementation, execution, or judge material

### B. Protocol item coverage

For each block, verify the exact §4.1 counts and identify any missing,
duplicated, or conflated item. Confirm every fact has a direct record,
ownership boundary, and explicit text needed for later state, scope, approval,
withdrawal, derivation, counterexample, malicious-data, and responsibility
relations.

Reject relationships that a future transformer could create only by guessing
or by using an answer key.

### C. Independence and leakage

- block names, fictional names, sentences, ordering, question wording, and
  apparent option placement are materially independent
- runner-visible files contain no condition identity, structure rank,
  preferred structure, evaluation role, scoring contract, answer marker,
  expected result, risk code, or hidden field name
- malicious imperative text is unambiguously data/evidence, not a reviewer or
  executor instruction

### D. Question fairness and sufficiency

- questions and options are understandable from source facts without hidden
  context
- all future conditions would receive the same questions and neutral options
- every C1-C7 and M1-M6 failure type has at least one observable opportunity
  per block, assessed internally without copying those mappings or answers into
  the report
- at least one supported no-change opportunity exists in each block
- options are balanced and do not signal the likely answer through wording,
  length, order, or moral framing

### E. Honest limits

Explicitly state that no judgment is possible yet about:

- oracle and scoring consistency
- four-condition transformation equivalence and the 15% byte ceiling
- provenance reports and oracle-derived relation checks
- formal pre-run approval, executor isolation, or any S0 outcome

## 4. Output

Do not edit the repository or candidate. Return a compact review to CONTROL in
your response only, without pasting sealed source text, fictional names,
questions, options, or inferred answers.

Required output:

1. input-authentication result
2. Critical, Major, and Minor findings with opaque IDs and concise evidence
   locations only
3. pass/partial/fail for A-E
4. one verdict exactly from:
   - `source candidate acceptable for CONTROL source-authoring decision`
   - `source candidate requires revision before CONTROL decision`
5. remaining unverified limits

Any confirmed Critical or Major finding requires the revision verdict. This
review is never complete F0 approval or freeze.

