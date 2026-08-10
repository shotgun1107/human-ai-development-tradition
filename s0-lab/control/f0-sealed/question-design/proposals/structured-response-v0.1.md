# F0-SEALED Track V structured-response proposal v0.1

- track: `V — measurement validity`
- design label: `Universal Decision Vector (UDV)`
- status: **proposal only — not approved, implemented, frozen, or validated**
- scope: question/answer-format design only

## 1. Outcome summary

Replace runner-visible, question-specific multiple-choice options with one
precommitted structured response used unchanged for every question. Each
answer carries a three-axis `decision` vector, record citations, affected
scope, uncertainty, and a short reason. The runner never receives candidate
answer sentences.

The universal decision vector is:

| Axis | Precommitted values |
|---|---|
| `disposition` | `permit`, `prohibit`, `defer`, `preserve` |
| `state_effect` | `start`, `continue`, `constrain`, `pause`, `end`, `none` |
| `route` | `automated_action`, `data_only`, `human_decision`, `not_applicable` |

These values and their definitions must be frozen before any sealed-source
access. Every Cartesian-product combination is structurally valid. The runner
schema must not narrow the values per question, because a question-specific
subset would itself become an answer-shape cue. Semantic correctness is a
separate, pre-run comparison against a sealed adjudication contract.

This design requires new protocol and schema versions. It does not alter the
frozen v0.3, SM0, or SM1 files and does not approve the held source candidate.

## 2. Facts / inferences / proposal boundary

### Verified facts from the authenticated allowlist

- Protocol v0.3 defines a comparison of four representations of the same
  facts, repeated across two independent blocks and fresh single-turn
  sessions.
- The frozen answer schema uses a question-specific `decision_option_id`.
- The frozen question/options schema exposes each question's `OPT-*` IDs and
  `runner_text` while keeping evaluation and scoring metadata sealed.
- The source-authoring decision is `COMPLETED WITH HOLD`; the candidate is not
  approved or frozen.
- The remaining review finding is that some option sets contain a uniquely
  qualifying or source-echoing choice, allowing likely selection from answer
  shape. Three wording-level revisions did not close that finding.
- No implementation, sealed fixture approval, oracle, execution, judging, or
  S0 result is established by the authenticated inputs.

### Design inferences

- Equalizing option length does not remove a uniquely specific semantic cue.
- Removing question-specific answer sentences closes that cue more directly
  than another wording pass.
- A finite, shared decision vector can preserve objective comparison without
  asking a judge to freely reinterpret prose.
- Orthogonal fields expose whether an error concerns authorization, state
  effect, or routing. That is a more diagnostic measurement than recognizing
  one compound option sentence, but its clarity and burden remain empirical
  questions for public-only testing.

### Proposals, not facts

Everything below—including the UDV vocabulary, prompt restrictions,
adjudication rules, schema deltas, thresholds, migration order, and
recommendation—is a proposal. It creates no expected answers, oracle entries,
scoring entries, fixtures, code, or execution authority.

## 3. Runner-visible contract

### 3.1 Exactly what the executor sees

For one opaque block, every executor sees only the same categories already
permitted by the common execution design:

1. the common neutral instruction;
2. that executor's one opaque `input.json` representation;
3. one runner question projection for the block;
4. the proposed versioned answer schema; and
5. an opaque output path.

The runner question projection contains only:

```json
{
  "contract_version": "UDV-0.1",
  "block_id": "BLK-OPAQUE000001",
  "questions": [
    {
      "question_id": "Q-GENERIC-01",
      "runner_prompt": "Decide the named target and return one UDV response."
    }
  ]
}
```

The real prompt may identify the decision target and the operation being
decided, but it must not quote or paraphrase the decisive qualification, state
an expected direction, offer examples, list candidate answers, or vary the
response fields. It must be byte-identical across the four conditions for the
same block. All questions expose the same response contract; there are no
question-specific citation policies, affected-scope policies, permitted
tuples, or option lists.

Runner-visible material must not contain condition identity, representation
names, structure ranking, target preference, evaluation role, risk or error
codes, oracle or scoring references, or answer markers. The UDV codebook is a
global response grammar, not a question-specific answer set.

The global meanings are fixed as follows:

- `disposition`: whether the named operation is permitted, prohibited,
  deferred without a terminal decision, or governed by the present state
  without a new determination.
- `state_effect`: whether the answer starts, continues, constrains, pauses,
  ends, or makes no transition to the named target's state.
- `route`: whether any next handling is an automated action, data-only
  treatment, a human decision, or not applicable.

These definitions must be published and frozen before sealed-source access.
No sealed question may add synonyms, explanations, special cases, or a reduced
value set.

### 3.2 Exactly what the executor writes

The executor writes exactly one UTF-8 JSON object:

```json
{
  "protocol_version": "0.4-proposed",
  "block_id": "BLK-OPAQUE000001",
  "input_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "answers": [
    {
      "question_id": "Q-GENERIC-01",
      "decision": {
        "disposition": "permit",
        "state_effect": "none",
        "route": "human_decision"
      },
      "cited_record_ids": ["R-EXAMPLE-01"],
      "affected_record_ids": [],
      "uncertainty": "bounded",
      "short_reason": "The cited record assigns the decision to the named reviewer."
    }
  ]
}
```

All three decision fields are required for every question. The schema accepts
the full shared vocabulary for every question. `cited_record_ids` is always
nonempty, sorted, and unique; `affected_record_ids` is always present, sorted,
and unique and may be empty. `uncertainty` retains
`none|bounded|material`. `short_reason` is one line and at most 240 Unicode
code points. The existing total output ceiling remains 8,192 UTF-8 bytes.

`short_reason` is retained for concise auditability and prohibited-information
checking. It does not select or repair the structured semantic result and is
not freely interpreted to decide correctness.

## 4. Judge-visible contract

### 4.1 Inputs and isolation

After outputs are frozen, the independent judge receives only:

- the anonymous answer;
- the exact runner question projection and answer schema used in that run;
- a condition-neutral block fact projection;
- a sealed, pre-run adjudication contract for that block; and
- the already-frozen error-counting rules needed for the authorized review.

The judge does not receive condition identity, representation metadata,
structure names, target preference, cost, timing, or another condition's
answer before the anonymous semantic result is frozen.

### 4.2 Deterministic adjudication data

For each question, the sealed adjudication contract precommits only machine-
comparable rules:

- one or more accepted UDV tuples;
- citation clauses, each satisfied by citing at least one member of a listed
  record-ID set;
- the complete set of record IDs allowed as relevant citations, preventing
  citation dumping;
- one or more accepted affected-record-ID sets; and
- the accepted uncertainty value set.

This proposal defines the rule shape only. It supplies no question-specific
values, expected tuple, record mapping, rationale, error assignment, or score.
Those remain closed and require a later exact gate.

### 4.3 Deterministic comparison order

1. Check output existence, UTF-8, JSON parsing, input hash, and byte ceiling.
   Failures at this layer retain the protocol's suite-invalid boundary.
2. For parseable output, check the answer schema, exact question set,
   one-answer-per-question rule, sorted unique IDs, and required fields.
   Failures at this layer are format errors, not semantic decisions.
3. For schema-conforming answers, compare the UDV tuple by exact equality
   against the accepted tuple set.
4. Evaluate citation clauses by set membership and reject citations outside
   the precommitted allowed set.
5. Compare `affected_record_ids` by exact set equality against the accepted
   set list and compare `uncertainty` by enum membership.
6. Validate `short_reason` only for length, one-line form, and prohibited
   runner-visible vocabulary. Do not use free-form interpretation to change
   steps 3–5.

Thus malformed JSON, schema/format errors, and semantic decision errors remain
distinct. A structurally valid but wrong combination is a semantic error; it
is not relabeled as a schema error. Multiple accepted tuples or affected sets
are allowed only if frozen before execution and confirmed by pre-run review.

## 5. Schema and protocol delta

No frozen file should be edited in place. Selection would require new files,
new hashes, independent review, and a later implementation gate.

### 5.1 Protocol v0.3

A new protocol version is required; `protocol_version: 0.3` must not be reused.
The proposed delta is:

| Location | Required new-version change |
|---|---|
| §5 sealed files | Replace runner `question/options` projection with an option-free question projection plus a separately sealed adjudication contract. Freeze the UDV codebook before sealed-source access. |
| §6.1 output | Replace the single question-specific decision option with the required three-field `decision` object. Retain citations, affected IDs, uncertainty, reason, envelope IDs, and hashes. |
| §6.2 validation | Apply the full UDV value set and identical field requirements to every question. Prohibit per-question enum narrowing. Require at least one citation and cap the reason at 240 code points. |
| §8 observables | Observe exact UDV coordinates and record-ID sets. Preserve the existing suite-invalid versus parseable-format-error distinction. Re-review any mapping from semantic mismatches to existing error categories under the new coordinates. |
| §8.4 judging | Require the deterministic comparison order in §4 and state that prose cannot repair or overturn structured fields. |
| §11 release order | Freeze and publicly falsify the response grammar and option-free question format before any sealed-source question is authored or revised. |

The two-block/four-condition design, fresh-session isolation, common question
opportunity, resource ceilings, condition blinding, and accuracy-before-cost
order need no conceptual change. Their references and hashes would still need
version updates in any new protocol package.

### 5.2 `answer.schema.json`

A new schema version and `$id` are required. Exact structural changes:

- change the protocol const to the new protocol version;
- remove `decision_option_id`;
- add required object `decision` with `additionalProperties: false`;
- require `disposition`, `state_effect`, and `route` with exactly the global
  enums in §1;
- do not encode question-specific combinations or conditional enum subsets;
- split the current shared ID-array definition so cited IDs have `minItems: 1`
  while affected IDs may remain empty;
- retain record-ID syntax, uniqueness, and the envelope fields;
- reduce `short_reason` maximum from 500 to 240 code points while retaining
  the one-line requirement; and
- retain `additionalProperties: false` throughout.

Question-set equality, sorting, citation-clause comparison, affected-set
comparison, and prohibited vocabulary remain cross-file validation duties; a
JSON Schema must not be claimed to prove them.

### 5.3 `question-options.schema.json`

The frozen v0.2 schema cannot represent this design without a new version.
Prefer renaming its successor to `question-response-contract.schema.json` so a
file named “options” does not survive after options are removed. If path
compatibility requires the old family name, version it to a new manifest
version and make the same content changes:

- remove `options`, the `option` definition, `option_id`, and `runner_text`;
- remove runner-visible `citation_policy` and `affected_ids_policy`; the
  response obligations are global and identical;
- make each runner question contain only `question_id`, `runner_prompt`, and a
  constant `response_contract_id: UDV-0.1`;
- change `runner_projection.included_fields` accordingly;
- continue excluding evaluation role, oracle/scoring references, condition
  mapping, and target preference;
- add invariants that every question uses the same response contract, no
  prompt contains an answer example or expected-direction statement, and the
  projection is identical across conditions; and
- retain evaluation role only in sealed metadata if the later protocol still
  needs it, never in the runner projection.

JSON Schema can enforce the field shape and constants but cannot prove that a
prompt paraphrases no decisive qualification. That semantic check remains a
mandatory pre-run review and public leakage test.

### 5.4 Consequent format impact

The neutral answer-validation and judging/scoring format families would need
new versions or explicitly reviewed compatibility records for UDV tuples and
citation clauses. No change to their frozen files is proposed here, and this
document supplies no scoring content. Reusing an old format merely because it
parses would be a rejection condition.

## 6. Abstract example

The following is an invented serialization example only. It is unrelated to
any public or sealed fixture and asserts no expected answer or correctness.

Abstract records:

- `R-EXAMPLE-01`: a generic item is awaiting a named reviewer's disposition.
- `R-EXAMPLE-02`: the current state remains in force until that review occurs.

Abstract runner prompt:

> For the pending disposition of Item K, return one UDV response.

Illustrative output:

```json
{
  "protocol_version": "0.4-proposed",
  "block_id": "BLK-EXAMPLE00001",
  "input_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "answers": [
    {
      "question_id": "Q-EXAMPLE-01",
      "decision": {
        "disposition": "defer",
        "state_effect": "none",
        "route": "human_decision"
      },
      "cited_record_ids": ["R-EXAMPLE-01", "R-EXAMPLE-02"],
      "affected_record_ids": [],
      "uncertainty": "bounded",
      "short_reason": "The current state remains while the named reviewer decides."
    }
  ]
}
```

No adjudication contract is shown, so the example contains no answer marker,
expected tuple, rationale key, or score.

## 7. Leakage and fairness analysis

### Answer-shape leakage resistance

- There are no question-specific answer sentences or distractors to echo a
  decisive source qualification.
- The same finite axis names, values, order, definitions, and schema appear for
  every question before sealed-source access.
- All Cartesian-product combinations are schema-valid; the runner cannot infer
  a likely answer from per-question enum narrowing or schema branches.
- Citations, affected scope, uncertainty, and reason are present for every
  question under the same rules, so policy presence does not reveal question
  type or likely result.
- Semantic judging uses sealed exact-match data rather than prose similarity
  to a source sentence.

This design does not prove zero leakage. A prompt can still reveal direction,
outcome frequencies can create priors, and axis terminology can prime a style
of reasoning. Those risks are falsified publicly and reviewed before any
sealed use.

### Fairness across conditions and blocks

- Within a block, all four conditions receive the identical question
  projection hash and answer schema hash.
- No condition receives extra values, examples, instructions, retry
  opportunity, fields, or byte allowance.
- Each condition answers every question once with the same contract.
- The same frozen UDV codebook applies to both independent blocks; neither
  block may introduce vocabulary.
- Judge-visible comparison rules are keyed to question IDs and anonymous
  answers, not representation identity.
- Any accepted-alternative rule is shared across all four conditions for that
  question and frozen before execution.

## 8. Public-only validation plan

All tests in this section require a later exact gate. They must use only newly
authored, clearly synthetic public material, never the held candidate, sealed
content, real customer or personal data, past-project content, or an eventual
hidden oracle. Test design, samples, labels, thresholds, and hashes must be
frozen before collecting the measurements they govern.

### 8.1 Answer-leakage falsification

1. Build a public set balanced across the UDV tuples selected for coverage;
   do not let frequency reveal a majority answer.
2. Give fresh reviewers only the response schema and question projection, with
   source records withheld, and ask them to predict the public labels.
3. Run a precommitted exact permutation test against the balanced chance rate.
   Reject UDV if prediction is above chance at two-sided `alpha = 0.05`.
4. Repeat with prompt nouns and IDs replaced by neutral tokens. A material
   accuracy difference indicates lexical leakage and rejects the prompt form.
5. Have a separate reviewer inspect every prompt for decisive qualification
   echoes. Any uniquely directional prompt is a blocking failure.

### 8.2 Scoring reliability

1. Prepare public answers containing one controlled mutation at a time in each
   UDV coordinate, citation clause, affected set, uncertainty field, and format
   boundary.
2. Run two independently produced comparators against the same public
   adjudication data.
3. Require identical classification for every answer and byte-identical output
   across 100 repeated runs per comparator.
4. Require 100% separation of suite-invalid, parseable-format-error, and
   schema-valid-semantic-error cases. Any collision or nondeterministic result
   rejects the contract or comparator.

### 8.3 Inter-reviewer agreement

Two fresh reviewers independently apply only the written contract to blinded
public answers. Require exact agreement on every discrete mismatch and error
layer. If a chance-corrected coefficient is defined for the public sample, its
precommitted target is `1.00`; an undefined coefficient due to no category
variation does not substitute for the exact-agreement check. Any disagreement
forces rule clarification and a new version before sealed use.

### 8.4 Executor burden and condition fairness

Use a randomized public crossover with the same model settings and one-turn
limits. Compare UDV with an option-free public control that asks for the same
decision content. Record schema-valid completion rate, elapsed time, output
bytes, omitted fields, and repair attempts without using self-reported effort.

Reject UDV if any of the following precommitted thresholds is crossed:

- fewer than 95% of public runs are schema-conforming on the first output;
- median elapsed time or output bytes exceed the public control by more than
  20%;
- any public presentation receives a different prompt/schema/question set;
- the maximum-minus-minimum first-pass schema success rate across public
  presentations exceeds 5 percentage points; or
- any run needs more than the existing 15-minute or 8,192-byte ceiling.

These thresholds test usability only. Passing them would not validate S0 or a
representation effect.

## 9. Migration and rollback

### Migration

1. CONTROL decides whether to select this proposal; completion alone is not
   approval.
2. Assign new protocol, answer-schema, question-contract, validation, and
   adjudication-format versions. Never overwrite frozen files.
3. Freeze the UDV vocabulary, definitions, prompt constraints, and public test
   plan before any sealed-source access.
4. Run the public-only falsification plan and obtain independent design review.
5. If and only if all gates pass, authorize a separate sealed-source revision
   that removes options without importing public wording or labels.
6. Conduct a new pre-run review of prompt neutrality, exact projection equality,
   schema compatibility, and deterministic adjudication before any executor is
   created.

Existing question-specific options cannot be mechanically converted by
choosing the “closest” UDV tuple; that would import the very option semantics
under review. Any later mapping must be authored from authorized source facts
and independently reviewed under a new gate.

### Rollback

Because this proposal changes no frozen artifact, rollback is to reject the
new candidate versions, retain protocol v0.3/SM0/SM1 at their recorded hashes,
keep the held source candidate unapproved, and return to the question-design
gate. Do not silently restore or run the old question-specific options. A
future alternative design requires its own version and review.

## 10. Failure modes and unverified limits

### Rejection criteria

Reject this design if any of the following occurs:

- any question-specific answer sentence, option list, enum restriction,
  response example, or accepted-tuple hint reaches a runner;
- UDV vocabulary must be extended after sealed-source access to express a
  sealed answer;
- a correct output depends on a condition-specific field or term;
- the judge must interpret `short_reason` freely to resolve correctness;
- deterministic comparators or independent reviewers disagree;
- public leakage or burden tests fail their frozen thresholds;
- one condition or block receives more decision information or opportunity;
- a new format cannot keep semantic and JSON/format failures distinct; or
- migration would reuse unreviewed old option semantics as expected UDV data.

### Unverified limits

- The UDV axes may be ambiguous, correlated, overly burdensome, or too coarse
  for some decision targets.
- Requiring a citation for every question may be infeasible for a future
  authorized case; this has not been tested.
- The 240-code-point reason limit, public thresholds, and exact-match citation
  clauses have not been empirically validated.
- This proposal has not examined the held source candidate and does not show
  that its questions can be migrated without information loss.
- Prompt neutrality, outcome balance, accepted-alternative completeness,
  transformation equality, byte ceilings, oracle consistency, scoring
  coverage, model stability, isolation, and judge reliability remain
  unverified.
- No implementation exists, and no schema engine, validator, runner, fixture,
  executor, or judge has been tested here.

### Prohibited claims

This proposal must not be cited as evidence that F0, I0, S0, the central
system, Project Brain integration, operational safety, economic value,
representation superiority, model-to-model transfer, or any real-world effect
has been implemented or validated. It makes no customer, privacy, security,
safety, economic, or production-readiness claim.

## 11. Recommendation

Advance UDV to an independent, read-only comparative review as the Track V
candidate. Its main validity advantage is structural: it removes
question-specific distractor prose and prevents question-level schema
narrowing while preserving finite, exact-match decisions and the existing
evidence/scope/uncertainty fields.

Do not approve sealed-source revision or implementation on this proposal
alone. Selection should be conditional on a new-version design package passing
the public leakage, deterministic-adjudication, inter-reviewer, and executor-
burden falsification tests above.
