# Universal Response Contract v0.4 candidate

- design_id: `URC-0.4-CANDIDATE`
- status: **public design proposal only**
- predecessor: Track V `UDV-0.1`
- scope: runner-visible question/answer contract and judge-visible comparison shape
- not included: executable schemas, fixtures, questions, expected answers, oracle, scoring instances, code, runs, or validation results

## 1. Outcome

Replace question-specific options with one response contract that is identical for every question. Reduce Track V from three axes and 96 structurally valid combinations to two fields and six globally admissible combinations.

The candidate removes `state_effect`. A question already names the operation being decided, such as starting, limiting, pausing, or ending something. Asking the executor to classify that operation again does not measure the evidence-based decision; it mostly repeats information in the prompt and may favor representations that already expose state transitions explicitly.

The candidate keeps only:

1. `disposition`: what the records justify doing about the named operation now;
2. `handling`: how the decision may be carried forward, if at all.

No question may alter the fields, values, definitions, admissible combinations, citation obligation, affected-ID obligation, uncertainty obligation, or reason obligation.

## 2. Facts, inferences, and proposals

### Verified predecessor facts

- Protocol v0.3 compares four representations of the same facts across two independent blocks and fresh one-turn sessions.
- The frozen predecessor answer contract uses one question-specific decision option plus citations, affected IDs, uncertainty, and a short reason.
- The frozen question contract exposes question-specific options and question-specific citation and affected-ID policies.
- Track V was selected as the question-design direction because one universal structured response better addresses answer-shape leakage.
- Independent review found Track V's 96 combinations, possible inconsistent tuples, accepted-set completeness, coordinate double-counting, output burden, and possible C/D alignment unresolved.
- No public test, sealed migration, implementation, executor run, or S0 result has validated a successor contract.

### CONTROL inferences

- `state_effect` is redundant when the prompt already identifies the named operation.
- Removing that axis reduces both lexical leakage and response burden without returning to question-specific options.
- A global admissibility matrix can reject incoherent field combinations while remaining identical for every question.
- Requiring exactly one accepted structured combination per admissible question is more deterministic than allowing an open set of accepted tuples.

### Proposals

All vocabulary, definitions, limits, comparison order, resource budgets, rejection rules, and successor-version impacts below are proposals. They are neither implemented nor empirically validated.

## 3. Normative decision grammar

### 3.1 The object being decided

Every question must name exactly one operation on exactly one target at one decision time: **may this named operation proceed now under the supplied records?**

`disposition` governs that named operation, not the general worth of the target, not a future project strategy, and not an implied secondary operation.

`handling` governs what may happen next as a consequence of that disposition. It does not describe the input representation and does not reveal which condition produced the answer.

### 3.2 Global values

| Field | Value | Fixed meaning |
|---|---|---|
| `disposition` | `permit` | The supplied records authorize the named operation now. |
| `disposition` | `prohibit` | The supplied records rule out the named operation now. |
| `disposition` | `defer` | No binding yes/no decision is justified now; the matter remains pending. |
| `disposition` | `preserve` | No new operation should occur; the already established state remains in force. |
| `handling` | `direct_action` | The named operation may be carried out under the authority already present; no further binding decision is required. This does not necessarily mean software automation. |
| `handling` | `data_only` | Only local information handling is permitted; no project-state or external-world action is authorized. |
| `handling` | `human_decision` | No action is authorized until the named human authority makes the binding decision. |
| `handling` | `none` | The response authorizes no further handling route. |

### 3.3 One global admissibility matrix

The same six combinations are structurally valid for every question. The runner contract must expose all six and must never narrow or reorder them by question.

| Design-only row | `disposition` | `handling` | Generic interpretation |
|---|---|---|---|
| G01 | `permit` | `direct_action` | The named operation may proceed under existing authority. |
| G02 | `prohibit` | `data_only` | The named operation may not proceed; only non-effectful information handling is allowed as the bounded alternative. |
| G03 | `prohibit` | `none` | The named operation may not proceed. |
| G04 | `defer` | `none` | The evidence is insufficient for a binding decision and supplies no separate authority route. |
| G05 | `defer` | `human_decision` | The operation remains pending because a human authority must decide. |
| G06 | `preserve` | `none` | The existing state remains; no new operation is taken. |

`G01` through `G06` are design-document row labels only. They are not runner output values, question options, scores, or answer markers.

Every other Cartesian combination is structurally invalid for every question. Examples include `prohibit + direct_action`, `preserve + data_only`, and `permit + human_decision`. `data_only` never means that the prohibited named operation partly proceeded; it is a separately bounded, non-effectful alternative. If a future public or sealed question appears to require another combination, the question is inadmissible under URC-0.4; the matrix must not be changed after seeing that question.

## 4. Runner-visible contract

### 4.1 Common instruction

Every condition and both blocks receive one byte-identical codebook containing the definitions in section 3, the six admissible combinations, and the same field obligations. No condition receives examples tailored to its representation.

The common instruction states:

- decide only the one named operation in each prompt;
- use only one globally admissible combination;
- cite at least one supplied record ID;
- always return `affected_record_ids`, using an empty array when no record is affected;
- always state `uncertainty` as `none`, `bounded`, or `material`;
- provide one short reason, which is retained for audit only and cannot repair the structured decision;
- do not reveal or guess condition identity.

### 4.2 Question projection

The response contract is declared once at the top level, resolving Track V's inconsistent per-question `response_contract_id` treatment.

```json
{
  "contract_version": "0.4-candidate",
  "response_contract_id": "URC-0.4-CANDIDATE",
  "block_id": "BLK-OPAQUE000001",
  "questions": [
    {
      "question_id": "Q-ABSTRACT-01",
      "runner_prompt": "For the named target, decide whether the named operation may proceed now under the supplied records."
    }
  ]
}
```

Each question contains exactly `question_id` and `runner_prompt`. There are no options, response examples, per-question policies, per-question contract IDs, accepted combinations, evaluation roles, or scoring fields.

Within a block, the question projection must be byte-identical across A–D. Both blocks use the same contract and codebook hashes.

### 4.3 Prompt restrictions

A runner prompt may identify the target, named operation, and decision time. It must not:

- quote or paraphrase the decisive record qualification;
- contain `permit`, `prohibit`, `defer`, `preserve`, `direct_action`, `data_only`, `human_decision`, or an equivalent answer instruction;
- state which field is likely to vary;
- state a preferred outcome, risk code, evaluation role, target ranking, condition identity, representation name, or scoring consequence;
- combine two independently decidable operations;
- change citation, affected-scope, uncertainty, or reason obligations.

Exact codebook-token exclusion is mechanically checkable. Decisive-paraphrase exclusion requires independent semantic review and public leakage testing.

## 5. Executor response

The executor writes one UTF-8 JSON object:

```json
{
  "protocol_version": "0.4-candidate",
  "response_contract_id": "URC-0.4-CANDIDATE",
  "block_id": "BLK-OPAQUE000001",
  "input_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "answers": [
    {
      "question_id": "Q-ABSTRACT-01",
      "decision": {
        "disposition": "defer",
        "handling": "human_decision"
      },
      "cited_record_ids": ["R-ABSTRACT-01"],
      "affected_record_ids": [],
      "uncertainty": "bounded",
      "short_reason": "The cited record assigns the binding decision to a named authority."
    }
  ]
}
```

This is an unscored serialization example. It is not tied to any fixture and does not assert an expected answer.

### 5.1 Required answer rules

- exactly one answer for every question and no extra question;
- exactly one of the six globally admissible decision combinations;
- `cited_record_ids`: nonempty, sorted, unique, maximum four;
- `affected_record_ids`: present, sorted, unique, maximum four, possibly empty;
- IDs must refer to records actually present in that condition's input and must use the same canonical record IDs across A–D;
- `uncertainty`: exactly `none`, `bounded`, or `material`;
- `short_reason`: one line, nonempty, at most 160 UTF-8 bytes after JSON-string escaping;
- no extra fields and no `null` values;
- the short reason is never interpreted to override the structured fields.

## 6. Public question-admissibility rule

A question is eligible for a future URC-0.4 public bank only when two independent authors, without sealed access, can establish all of the following before any run:

1. It names exactly one operation, one target, and one decision time.
2. All information needed to decide is located in the supplied records rather than the prompt wording.
3. Exactly one of G01–G06 is justified by the complete public record set.
4. Ambiguous or insufficient records map deliberately to G04, or to G05 when a human authority route is explicitly established; they do not create multiple accepted tuples.
5. Exactly one accepted affected-ID set and exactly one accepted uncertainty value can be frozen.
6. Citation correctness can be expressed as one or more precommitted evidence clauses without revealing them to the runner.
7. The prompt contains no codebook token, decisive qualification, response example, or condition-specific wording.
8. The question can be represented with the same canonical facts and record IDs in all four public presentation forms.
9. The complete authorized block satisfies the resource budget in section 10.

Disagreement on items 1–6 rejects the question; it is not resolved by adding multiple accepted decisions, by interpreting `short_reason`, or by tailoring a runner prompt.

This rule is designed for new public synthetic material. It makes no claim that the held sealed questions are admissible or migratable.

## 7. Judge-visible adjudication shape

No adjudication instance is created under this gate. A later approved public authoring gate may create, for each question:

- exactly one accepted structured decision;
- one or more citation clauses, with each clause listing interchangeable supporting record IDs;
- one complete allowed-citation set to prevent citation dumping;
- exactly one accepted affected-record-ID set;
- exactly one accepted uncertainty value;
- one precommitted primary observation-to-error-code mapping;
- a freeze timestamp and hashes made before any executor output.

The independent judge must receive anonymous responses and condition-neutral facts. It must not receive condition identity, structure names, timing, cost, another condition's output, or any post-run explanation before its discrete findings are frozen.

## 8. Deterministic validation and observation order

### 8.1 Validation layers

1. **Suite validity:** required files exist; output is at most 8,192 bytes; UTF-8 and JSON parse; envelope IDs and `input_hash` match.
2. **Answer-format validity:** exact question set, one answer per question, allowed fields only, sorted unique arrays, per-answer byte bound, and one of the six global combinations.
3. **Semantic comparison:** exact equality with the single accepted decision.
4. **Evidence comparison:** citation clauses satisfied and no citation outside the allowed set.
5. **Scope comparison:** exact set equality for affected IDs.
6. **Uncertainty comparison:** exact value equality.
7. **Reason policy:** length, one-line form, and prohibited-term checks only.

Prose meaning cannot change layers 3–6.

### 8.2 Atomic observations

For each schema-conforming answer, a comparator emits exactly these booleans:

- `decision_exact`;
- `citation_valid`;
- `affected_set_exact`;
- `uncertainty_exact`;
- `reason_policy_valid`.

It does not emit one error per decision coordinate. A wrong two-field combination is one `decision_exact = false` observation regardless of whether one or both fields differ.

### 8.3 One primary scored event per question

To prevent cascaded double-counting, the question outcome is selected by fixed precedence:

1. answer-format failure;
2. decision mismatch;
3. citation mismatch;
4. affected-set mismatch;
5. uncertainty mismatch;
6. reason-policy mismatch;
7. pass.

Only the first applicable outcome may produce the question's one primary scored event. Later mismatches remain diagnostic and unscored for that question. A later scoring format must precommit how each question's primary outcome maps to one existing or successor C/M code. This document creates no scoring instance and assigns no question-specific code.

## 9. Protocol and schema successor impact

No frozen file is edited in place. If this candidate later passes review and public validation, separately versioned artifacts would need these changes:

### Protocol successor

- declare one top-level `response_contract_id` shared by all questions and outputs;
- replace question-specific decision options with the two-field URC decision;
- preserve the two blocks, four conditions, fresh one-turn sessions, equal questions, equal model settings, 15-minute limit, 8,192-byte output limit, and accuracy-before-cost decision order;
- insert the validation and single-primary-event order in section 8;
- require public falsification before any sealed-source revision.

### Answer-schema successor

- new version and `$id`;
- remove `decision_option_id`;
- add required `response_contract_id` at the envelope level;
- add required `decision` with `disposition` and `handling`;
- use a global `oneOf` or equivalent constraint accepting exactly G01–G06 for every answer;
- split cited and affected arrays so citations require at least one ID;
- enforce maximum four IDs per array, no extra fields, and the fixed uncertainty enum;
- leave byte-length, sorting, question equality, and cross-file record membership to explicit validators rather than falsely claiming JSON Schema proves them.

### Question-contract successor

- replace the options schema family with a separately versioned question-response-contract family;
- top level contains `contract_version`, `response_contract_id`, `block_id`, and `questions`;
- each runner question contains only `question_id` and `runner_prompt`;
- remove options, per-question citation policy, per-question affected-ID policy, and per-question response-contract IDs;
- maintain sealed evaluation metadata outside the runner projection.

Any validator, comparator, or schema implementation requires a later exact implementation gate.

## 10. Resource budget

The existing hard output ceiling remains 8,192 UTF-8 bytes. URC-0.4 adds a stricter design budget so a compliant canonical response has headroom:

- maximum questions per block: 8;
- maximum canonical serialized bytes per answer object: 896;
- maximum envelope, answer separators, and closing syntax: 512 bytes;
- maximum canonical response: `8 × 896 + 512 = 7,680` bytes;
- mandatory remaining headroom: 512 bytes;
- maximum four cited IDs and four affected IDs per answer;
- question and record IDs used by a candidate bank must each be at most 40 ASCII bytes;
- `short_reason` JSON-string content after escaping must be at most 160 bytes.

Before any bank is frozen, a deterministic dry serialization of the maximally populated authorized answer envelope must be at most 7,680 bytes. The actual executor output remains invalid above 8,192 bytes. A schema-conforming but excessively spaced response can still exceed the hard limit; the public burden test must measure whether ordinary first outputs stay below it.

If an intended bank requires more than eight questions, more than four evidence or affected IDs for any answer, longer IDs, or a larger reason, it is not compatible with this candidate. CONTROL must revise and re-review the contract before sealed access rather than relaxing limits after observing results.

This is an analytic budget, not an empirical result. No actual response has been generated or measured under this gate.

## 11. A–D and block equality contract

Before any public run, a manifest must demonstrate that A–D receive identical values for:

- question-projection SHA-256;
- response-codebook SHA-256;
- answer-schema SHA-256;
- question count and order;
- model ID and fixed revision;
- reasoning level;
- system and user authority;
- turn count and retry opportunity;
- 15-minute time limit;
- 8,192-byte hard limit;
- allowed tools and network state;
- judge-visible adjudication data after anonymization.

The only intended difference is the representation of the same canonical facts. Equality specified in a document is not evidence that later delivery artifacts satisfy it.

## 12. Migration and rollback

### Migration sequence

1. Independently review this candidate without sealed access.
2. If review permits, separately authorize creation of a synthetic public bank and test harness.
3. Freeze the public bank, answer labels, codebook, thresholds, manifests, and hashes before collecting results.
4. Run the public falsification plan.
5. If every noncompensatory gate passes, conduct a new independent review of results and residual risk.
6. Only then may CONTROL consider asking the user to open a sealed-source revision gate.

Existing sealed options must not be mechanically mapped to G01–G06. Any later sealed adjudication must be authored from authorized source facts in an isolated role and independently reviewed.

### Rollback

Rejecting URC-0.4 leaves protocol v0.3, SM0, and SM1 at their frozen hashes and leaves the held sealed source untouched. A rejected candidate is retained as evidence with its hash and must not be silently edited or reused under the same version.

## 13. Fail-closed conditions

Reject or revise the candidate if:

- a public question needs a seventh combination or multiple accepted decisions;
- `state_effect` or question-specific policies must be restored to express a decision;
- a prompt or schema exposes a likely answer without its records;
- two comparators or reviewers disagree under the written rules;
- a structured mismatch can create more than one primary scored event for one question;
- the response grammar materially advantages a C/D-style representation in the precommitted alignment test;
- the maximum authorized response cannot satisfy the resource budget;
- any A–D condition receives different decision information or opportunity;
- thresholds or admissibility rules are changed after results are visible;
- sealed content is needed to complete the public design.

## 14. Unverified limits and prohibited claims

Unverified:

- six combinations may be too coarse for some future question;
- the distinction between `defer + none` and `defer + human_decision` may still confuse executors;
- the two-field grammar may align more naturally with structured C/D inputs;
- the eight-question and four-ID limits may not fit the held sealed candidate;
- the one-primary-event precedence may hide useful secondary failures;
- reason, citation, and affected-ID burdens may still cause format errors;
- public test sample size, cost, model stability, and judge reliability remain unmeasured.

This candidate does not establish that the held source is usable, that public validation passed, that A–D delivery is equal, or that S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer has been implemented or validated.
