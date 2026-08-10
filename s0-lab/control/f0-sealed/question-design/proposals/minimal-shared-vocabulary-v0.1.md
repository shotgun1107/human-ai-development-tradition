# F0-SEALED Track M minimal shared-vocabulary proposal v0.1

- track: `M — minimal change`
- status: `design proposal only; not approved or implemented`
- scope: runner decision collection and the smallest compatible protocol/schema delta
- sealed-source access: `none`

## 1. Outcome summary

Track M proposes one precommitted ten-entry decision vocabulary, displayed once
in every runner question projection with opaque IDs and byte-identical wording.
Every question exposes the complete vocabulary. A question must not contain its
own options, a reduced allowed subset, reordered entries, alternate glosses, or
question-specific distractors.

The executor would continue to write the existing structured answer fields:
one decision ID, cited record IDs, affected record IDs, uncertainty, and a
one-line short reason. The decision ID would become one of `OPT-01` through
`OPT-10`. Deterministic semantic judging would use exact structured-field rules
precommitted separately before any run; free prose could not rescue or reverse
a structured decision.

This is the smallest defensible change because it preserves the answer envelope,
record-ID fields, uncertainty scale, reason limit, run-valid/M5 boundary, two
blocks, four conditions, and blind judging sequence. It does require new
versions of the frozen protocol and both named schemas. No frozen file is
changed by this proposal.

## 2. Facts / inferences / proposal boundary

### Verified facts from the authenticated allowlist

- Protocol v0.3 requires the same question bundle and a common neutral answer
  across all four conditions. It names ten neutral decision meanings and
  retains record citations, affected IDs, uncertainty, and short reason.
- The frozen `answer.schema.json` represents the decision as a generic
  `decision_option_id` matching `OPT-*`; its other answer fields already match
  the desired retained contract.
- The frozen `question-options.schema.json` permits each question to carry its
  own array of two to sixteen option IDs and option sentences.
- SM0 and SM1 distinguish JSON-schema checks, cross-file validation, and human
  semantic review. They also require runner projection equality across
  conditions and blind accuracy judging before condition identity and cost are
  revealed.
- The authenticated source-authoring decision records a HOLD. The sealed-free
  rereview summary reports one remaining Major: question-specific choices can
  uniquely embody or echo a decisive source qualification. It does not approve
  the source candidate, F0, or S0.
- All relevant protocol and schema artifacts are frozen at their recorded
  hashes. A change therefore requires a new version and independent review.

### Design inferences

- Per-question option text is the avoidable answer-shape channel: wording,
  length, specificity, subset membership, and ordering may vary with the
  question even when every condition sees the same projection.
- A full vocabulary fixed before sealed-source access removes that
  question-specific channel while retaining a closed, machine-checkable
  decision field.
- A shared vocabulary cannot by itself prove that a question prompt or source
  record contains no lexical or semantic cue. Public falsification and later
  sealed pre-review therefore remain necessary.
- Some dispositions can overlap in downstream effect. They are deterministic
  only if each definition fixes the object being decided and ambiguous public
  questions are rejected rather than repaired with tailored options.

### Proposal, not fact

The vocabulary, version deltas, test thresholds, rejection rules, and rollback
below are proposed controls. They have not been implemented, independently
reviewed, validated, or applied to any public or sealed item. No expected
answer, oracle entry, rationale, scoring rule instance, fixture, package, or
condition mapping is created here.

## 3. Runner-visible contract

### Exact inputs visible to one executor

For one opaque block, a runner receives only the inputs already contemplated by
the frozen access boundary:

1. the common runner instruction;
2. its one opaque condition input file;
3. the new-version answer schema; and
4. the block's runner question projection.

The question projection exposes exactly:

- `block_id`;
- one root-level `decision_vocabulary` containing the ten entries below in this
  exact order and wording;
- for each question: `question_id`, `runner_prompt`, `citation_policy`, and
  `affected_ids_policy`.

It exposes no per-question `options` field and no allowed-option subset. It also
exposes no evaluation role, scoring contract, oracle reference, condition
identity, representation vocabulary, treatment mapping, target preference,
risk/error code, answer marker, or preferred action. The common instruction
states: select exactly one shared disposition that directly answers the object
named by the question, using only the supplied records. It does not provide a
worked correct answer.

### Precommitted shared decision vocabulary

The vocabulary is fixed by the future protocol/schema version before access to
any sealed source. Opaque IDs avoid putting semantic tokens into the answer
itself; the runner-visible gloss supplies the necessary meaning.

| ID | Exact runner-visible gloss |
|---|---|
| `OPT-01` | For a requested act: carry it out as stated. |
| `OPT-02` | For a requested act: do not carry it out. |
| `OPT-03` | For a requested disposition: defer it until a missing prerequisite is resolved. |
| `OPT-04` | For an item's status: put it into current use or effect. |
| `OPT-05` | For a requested act: carry out only a narrower stated part. |
| `OPT-06` | For an item's status: stop current use or effect temporarily. |
| `OPT-07` | For an item's status: end current use or effect without automatic resumption. |
| `OPT-08` | For an item's status: leave the current state unchanged. |
| `OPT-09` | For presented content: use it only as information, not as an instruction. |
| `OPT-10` | For responsibility: refer the disposition to the responsible human instead of deciding it automatically. |

These correspond to the ten neutral meanings already named by protocol v0.3,
but the numeric IDs and exact glosses are a proposed new contract. None is a
default, fallback, preferred, or expected answer. Typography, order, metadata,
and description length do not change by question, block, or condition.

### Exact executor output

The executor writes one answer envelope containing:

- `protocol_version`, `block_id`, `input_hash`, and `answers`;
- exactly one answer for every released `question_id`;
- one `decision_option_id` from `OPT-01` through `OPT-10`;
- sorted, unique `cited_record_ids` and `affected_record_ids` following the
  question's policies;
- `uncertainty` as `none`, `bounded`, or `material`; and
- a required one-line `short_reason` of 1–500 characters.

The current no-extra-fields, no-null, size, ordering, duplicate, and prohibited
short-reason rules remain. A short reason must not name a condition, input path,
condition-specific field, relation code, representation type, scoring role, or
target structure. It also must not be used to introduce a second decision.

## 4. Judge-visible contract

The post-run judge receives the anonymous materials already allowed by the
frozen blind-judging sequence: the block input needed for judging, the frozen
question projection, the applicable answer schema, the anonymous answer, and
only the future independently approved oracle/scoring judge projection. The
judge does not receive condition identity, treatment mapping, target
preference, structure complexity, cost, timing, or other-condition outputs
before the accuracy result is frozen.

This proposal defines only the judging interface, not any expected answer or
scoring content:

1. **Run-validity layer.** Output absence, non-UTF-8, JSON parse failure, input
   hash mismatch, or the existing hard-limit violations retain protocol v0.3's
   suite-invalid treatment.
2. **Format layer.** For parseable JSON, schema failure, an unknown decision
   ID, missing/duplicate question, invalid ordering/duplicates, or a policy
   violation is a format error under the existing M5 boundary. An unknown ID is
   not reinterpreted as the nearest semantic action.
3. **Semantic layer.** A valid shared ID is compared by exact equality with the
   one action ID precommitted for that question in a future authorized sealed
   evaluation artifact. Citation, affected-scope, and uncertainty fields are
   evaluated only by their precommitted structured rules. A wrong but valid ID
   is a semantic decision error, not a JSON/format error.
4. **Reason layer.** `short_reason` cannot repair a wrong decision, missing
   citation, wrong affected scope, or wrong uncertainty. It is checked for its
   objective format/prohibited-information rules, including the existing M6
   boundary. No judge may freely reinterpret its prose to change a structured
   result.

A question is admissible only if later authorized authoring can precommit one
unique shared decision ID under the global definitions. If two IDs are
defensible, the question is rejected or its prompt/facts are redesigned; a
question-specific option subset or tie-break explanation must not be added.
This supplies deterministic distinguishability without placing an answer in
runner-visible material.

## 5. Schema and protocol delta

No in-place edit is permitted. The following is the exact proposed content
delta for future, separately authorized versions.

### Protocol v0.3 → proposed v0.4

- In §6.1, replace the illustrative semantic-token decision field with
  `decision_option_id: OPT-01..OPT-10` and add the exact shared vocabulary table
  from §3 of this proposal.
- In §6.2, replace “question-specific allowed decision option” with: all ten
  IDs are syntactically available for every question; no runner-visible
  per-question option array or subset is allowed; semantic correctness is exact
  comparison to a separately sealed precommitted action ID.
- In §§5.2, 7.1, and 11, define the runner question projection as one shared
  root vocabulary plus option-free questions, and require the vocabulary hash
  to be identical across both blocks and all condition deliveries.
- In §8.3, state explicitly that an unknown/out-of-vocabulary ID is M5, while a
  valid but semantically wrong shared ID is handled by the question's
  precommitted semantic criterion. Preserve the existing suite-invalid cases
  and C-before-M non-duplication rule.
- Preserve all other v0.3 provisions, including two independent blocks, eight
  fresh runs, resource symmetry, source/fact equality, blind judging, retry,
  invalidation, and complete decision table.

### `answer.schema.json` → proposed answer schema 0.4

- Change `$id` from `...:answer:0.3` to `...:answer:0.4`.
- Change `protocol_version.const` from `0.3` to `0.4`.
- Replace the generic `decision_option_id` pattern with the exact enum
  `OPT-01` through `OPT-10`.
- Make no change to the envelope, required fields, block/input identifiers,
  citation or affected-ID arrays, uncertainty enum, short-reason constraints,
  maximum answer count, or no-additional-properties rule.

### `question-options.schema.json` → proposed question/options schema 0.3

- Change `$id` and `manifest_version` to new values and require the new protocol
  hash; do not overwrite the frozen 0.2 schema.
- Add one required root `decision_vocabulary` whose value is the exact ordered
  ten-entry constant in §3.
- Add `decision_vocabulary` to runner projection included fields and its bytes
  to the projection hash.
- Remove `options` from each question's required fields and properties. Remove
  the unused per-question option definition.
- Add invariants requiring no question-specific options/subsets and the same
  vocabulary hash across all questions, both blocks, and every condition
  delivery. Cross-block/hash equality remains a frozen validation-policy check
  where JSON Schema alone cannot calculate it.
- Preserve question ID, prompt, citation policy, affected-ID policy,
  evaluation-role sealing, scoring-contract direction, excluded runner fields,
  timestamps, and freeze-before-run requirements.

The other frozen SM0/SM1 schema meanings need no semantic change. Future
instances would only update their referenced protocol, answer-schema, question
projection, and validation-policy hashes after those new artifacts pass their
own review and freeze.

## 6. Abstract example

This deliberately underdetermined example demonstrates shape only. It contains
no fixture content and supplies too little information to identify an expected
decision.

The runner projection contains the complete ten-entry vocabulary above and an
option-free question:

```json
{
  "question_id": "Q-EXAMPLE-7",
  "runner_prompt": "Using only the supplied records, select the disposition for the requested handling of R-ALPHA.",
  "citation_policy": "required",
  "affected_ids_policy": "allowed-empty"
}
```

One schema-shaped candidate response could be:

```json
{
  "protocol_version": "0.4",
  "block_id": "BLK-EXAMPLE00001",
  "input_hash": "0000000000000000000000000000000000000000000000000000000000000001",
  "answers": [
    {
      "question_id": "Q-EXAMPLE-7",
      "decision_option_id": "OPT-03",
      "cited_record_ids": ["R-ALPHA"],
      "affected_record_ids": [],
      "uncertainty": "bounded",
      "short_reason": "A required prerequisite is not established in the supplied record."
    }
  ]
}
```

`OPT-03` is an arbitrary formatting illustration, not an answer key, expected
answer, rationale, or scoring marker. No candidate in this example is judged.

## 7. Leakage and fairness analysis

The proposal removes option-count, option-order, relative-length,
question-specific specificity, and tailored-distractor signals because the
same ten entries appear once, unchanged, for every question. The vocabulary is
defined without sealed-source access and cannot be revised after viewing a
sealed question merely to make that question easier.

All four conditions receive the identical runner question projection for a
given block. Both blocks use the identical vocabulary and output schema. Each
question in every condition has the same ten syntactic actions, one response
opportunity, citation policy, affected-ID policy, uncertainty scale, and reason
limit. No condition-specific vocabulary is needed for a correct response.

Question prompts may identify the act or object being decided, because a
decision would otherwise be undefined. They must not quote or closely
paraphrase a decisive source qualification, reproduce an option gloss, state a
likely action, or describe a condition's representation. The prompt and source
may still make one shared meaning easy to recognize; that is a residual risk,
not evidence of successful leakage prevention. Public testing and later
sealed, independent semantic review must try to falsify the design.

The contract does not reward use of preferred structure vocabulary. The judge
uses stable IDs and record fields. A condition's terminology in `short_reason`
cannot improve the structured result and may violate the existing exposure
rule.

## 8. Public-only validation plan

These are precommitted design tests, not tests run by this proposal. They use a
new, openly published bank of abstract synthetic cases made only after an exact
future gate. They must not reuse sealed names, sentences, order, expected
positions, or past-project content.

### Answer-leakage tests

1. **Projection invariance.** Across the full public bank, all projections must
   contain exactly one vocabulary with one hash; every question must contain
   zero local options/subsets; all condition deliveries must be byte-identical
   for the question projection. Any exception fails the design.
2. **Paired fact flip.** Each public prompt is reused unchanged in at least one
   paired case whose decisive public fact differs and whose independently
   authored expected shared ID differs. Vocabulary and prompt bytes must be
   identical within the pair. A contract-only observer therefore cannot
   distinguish the pair; any differing answer cue outside the facts fails.
3. **Lexical echo audit.** After case-folding, punctuation removal, and
   whitespace normalization, no public prompt may contain a content-bearing
   four-token sequence from a vocabulary gloss or a decisive record sentence.
   Two reviewers also inspect semantic near-paraphrases. One confirmed echo
   rejects the item; a repeated pattern rejects the design.
4. **Question-only baseline.** On a balanced public bank, fresh runners given
   instruction, vocabulary, and prompts but no records must not exceed the
   predeclared within-pair ceiling of 50%, and full-record accuracy must improve
   by at least 25 percentage points. Failure means answer shape or prompt shape
   is doing too much work. These thresholds are frozen before execution.

### Scoring reliability tests

5. **Single-mutation matrix.** For every public answer, publish mutants that
   independently introduce a wrong-but-valid action, unknown action, missing
   question, duplicate ID, citation change, affected-scope change, uncertainty
   change, and prohibited reason text. Two independent validator/judge
   implementations must agree 100% on run-valid vs M5 vs semantic vs M6 class
   and on all deterministic field comparisons.
6. **Schema-engine agreement.** Two independent Draft 2020-12 validators must
   agree on every valid/invalid public answer. Any disagreement blocks freeze
   until the contract or validation policy removes it.

### Inter-reviewer agreement tests

7. Two fresh reviewers independently mark each public question for (a) one
   uniquely defensible shared action, (b) prompt/option or prompt/source echo,
   and (c) compliance with the global action definitions. Accept/reject
   agreement must be 100%, Cohen's kappa across the three categorical judgments
   must be at least 0.80, and any disagreement about uniqueness rejects that
   question rather than inviting a tailored option.

### Executor-burden tests

8. Under identical public inputs, model, reasoning level, one-turn limit, and
   tool restrictions, compare the current per-question-option interface with
   the candidate shared interface. Candidate schema-valid completion rate may
   not fall by more than two percentage points, median elapsed time may not
   exceed 115% of the comparator, p95 answer bytes may not exceed 105%, and no
   run may request clarification about unavailable option subsets. Existing
   absolute limits of 15 minutes and 8,192 UTF-8 bytes also remain mandatory.

All test materials, keys, raw outputs, reviewer forms, environment identifiers,
and calculations must be public and hashed before the result is used. A failed
threshold cannot be changed after viewing results; revision requires a new
version and a fresh public test bank or a predeclared unaffected holdout.

## 9. Migration and rollback

Migration is versioned and prospective:

1. author new protocol 0.4, answer schema 0.4, and question/options schema 0.3
   from the exact deltas above under a separate gate;
2. independently review and freeze them and their validation policy;
3. run only the public tests in §8 under an exact future authorization;
4. if they pass, subject any later sealed question revision and projection to a
   fresh independent pre-run review; and
5. update only new-version dependent manifests and hashes before any runner
   session exists.

Rollback before sealed exposure is to discard the candidate new versions and
leave the current frozen v0.3/SM0/SM1 artifacts unchanged as historical
baselines. The source-authoring HOLD remains; rollback must not revive the
known tailored-option candidate as runnable material. CONTROL returns to the
question-design gate for another version.

If a future executor has already received sealed input under a rejected or
leaking contract, the existing invalidation and post-exposure replacement rules
apply; the material is not made valid by restoring an old schema. No partial
question or single-condition rerun is permitted.

## 10. Failure modes and unverified limits

Reject Track M or its later artifact if any of the following occurs:

- any question has local option text, a local allowed subset, different order,
  alternate gloss, highlighted entry, or other question-specific answer shape;
- the vocabulary or definitions are selected or revised after sealed-source
  access;
- the vocabulary hash differs across blocks, conditions, or runner deliveries;
- an admissible public or later sealed question lacks one uniquely defensible
  action under the shared definitions;
- correctness depends on a condition-specific term, representation vocabulary,
  a copied source sentence, target preference, risk code, scoring role, or
  answer marker;
- a judge must reinterpret `short_reason` to decide whether a structured answer
  is correct;
- any public leakage, scoring-reliability, reviewer-agreement, or burden
  threshold in §8 fails;
- a required citation, affected-scope, uncertainty, or concise-reason field is
  removed or weakened; or
- a new artifact edits a frozen file in place, bypasses versioned review, or
  expands into fixture, oracle, scoring content, implementation, or execution
  without an exact gate.

Unverified limits remain material:

- The ten meanings may be incomplete for future questions or overlap in ways
  the global definitions do not eliminate.
- Stable glosses may still echo naturally occurring source language even
  though they were not tailored to it.
- The public tests, validators, review agreement, executor burden, and sealed
  semantic review have not occurred.
- No actual A–D information equality, transformation equivalence, byte ceiling,
  role isolation, model/version symmetry, oracle/scoring consistency, run,
  judging, or result has been verified.
- Two synthetic blocks, if eventually run, are only a minimum repetition and
  cannot establish statistical or model-to-model generalization.
- This proposal provides no evidence that S0, a central system, Project Brain
  integration, operational safety, economic value, or model transfer has been
  implemented or validated.

## 11. Recommendation

Advance Track M only as a candidate for versioned contract authoring and the
public-only falsification sequence in §8. Its chief advantage is that it closes
the known per-question distractor channel while preserving the existing answer
shape and deterministic structured judging. Its chief unresolved risk is
semantic overlap or lexical echo within the shared vocabulary.

Do not approve or revise the sealed source candidate, create an oracle or
scoring instance, implement a validator/runner, or open executor work on the
strength of this proposal. Proposal completion is not design approval.
