# E0 effect-test design v0.3

- Status: `revision proposal — awaiting fresh independent review, design only`
- Proposal label: `E0` is not a frozen official phase.
- Baseline: `central-system-v2.1-s0-preparation`
- Scope: causal structure and information boundaries for a possible future effect test
- Currently prohibited: source, tradition, comparator, task, answer, hidden oracle, prompt, schema, code or runner creation; model calls; scoring; execution; effect findings; later gates

## 1. Facts, inferences and proposal

### 1.1 Authenticated facts

1. S0, E0, the central system, Project Brain integration, operational safety, economic value, real-project value and model-to-model transfer have not been implemented or validated.
2. The authenticated v0.2 independent review returned `REVISE-AND-REVIEW`.
3. That review passed the single authenticated representation rule, estimand/null/lower-bound alignment, transfer chronology, limited safety unblinding, redaction and score-before-guess controls, S0/E0 separation, hidden-oracle boundary, rollback and claim ceiling.
4. It found one blocking defect in B-quality reviewer blindness, one major ambiguity in family-set counts and one minor package-entry defect.

### 1.2 Design inferences

1. Replacing D/B labels with X/Y cannot make a person blind after that person has seen labeled D/B, task or oracle meaning, condition identity, or relevance identity.
2. Semantic parity must be decided before relevance evidence is released, and relevance must be audited by different fresh people.
3. A family count used by one estimand cannot prove that a different family set has enough independent clusters.
4. Independence and safety requirements are stop conditions. They are not adjustable conveniences for meeting a staffing or cost target.

### 1.3 v0.3 proposal

This revision:

- gives B-quality review its own two people and a frozen exposure chronology;
- assigns relevance review to two different fresh people after all quality and condition-guess records are locked;
- rejects the package on any missing record, `FAIL`, `UNCLEAR`, disagreement, exposure breach or forbidden cue;
- carries distinct relevant-transfer and harm family counts through measurement, power, calls, tokens, staffing time and cost;
- adds a versioned v0.3 package entry point while leaving the frozen README unchanged.

## 2. Causal question, conditions and units

### 2.1 Narrow question

> Under one frozen model snapshot, common instructions, tools, task information, timing and output envelope, does a fresh session given an authenticated refined tradition from a separate synthetic experience make acceptable judgments more often than both a fresh session given no tradition and a fresh session given a quality-matched but irrelevant synthetic document, on self-contained tasks whose surface and decision relations differ from the source, without worsening prespecified harm challenges?

The intervention is external document delivery. It is not a model-weight update or evidence that a model learned.

### 2.2 Conditions

| ID | Condition | Status | Maximum question |
|---|---|---|---|
| A | no tradition | required in pilot and confirmation | no-tradition reference |
| B | independently quality-matched, irrelevant synthetic document | required for content-specific confirmation | whether relevant content exceeds format, token and general-advice effects |
| C | raw record from the same synthetic source | optional separate diagnostic | whether refinement adds value over raw access |
| D | refined tradition under the authenticated representation contract | intervention | limited external-tradition delivery effect |

- A/D remains pilot-only and cannot produce an effect pass.
- A/B/D is required for content-specific confirmation.
- C cannot replace or compensate for A/B/D.
- A four-condition run is closed by default and requires a separate reviewed question, family-set vector, power plan, staffing plan and budget.

### 2.3 Units

- Intervention unit: one task instance × one condition × one fresh session.
- Confirmatory default: one session per task-instance condition.
- Instances are nested in a pre-frozen maximum task family.
- Independent inferential unit: task family, never an instance or repeated session.
- A session sees one task and one condition only. No A-to-D crossover is allowed.

## 3. Exactly one authenticated representation reference

Before any future material authoring, the active protocol must contain exactly one `selected_representation_ref`. It must identify one versioned artifact with owner, SHA-256, approval basis and time, scope, known limitations, representation rules for A wrapper and B/C/D, and replacement or withdrawal relation.

A CONTROL-approved simple public fallback is not an exception. It must first become an independently reviewed, versioned and hashed artifact and then be installed as the protocol's only active reference.

Authoring stops if the reference is empty, plural, expressed as “candidate or fallback,” replaced by inline discretion, missing a required field, hash-mismatched, or applied differently to B. Changing the reference terminates the validity of dependent materials, audits and results; it requires a new protocol version and pre-result review.

The same stop-before-authoring rule applies to `runner_visibility_contract_ref`, `evidence_citation_contract_ref`, `resource_envelope_ref` and `known_limitations`. These links freeze representation and resources; they do not convey S0 scores or a claim that tradition works.

## 4. Transfer rather than near-copy

### 4.1 Frozen authoring chronology

1. Freeze a latent-pattern contract describing the abstract decision relation and its application and non-application boundary before D or downstream tasks are authored.
2. The tradition curator sees only the approved separate synthetic source and latent-pattern contract, never downstream tasks or oracle.
3. The task/oracle author sees only the latent-pattern contract and independent synthetic-world rules, never final D, B or condition outputs.
4. Close and hash both authoring lines before cross-audit.
5. Two pre-result leakage auditors work in controlled environments; neither may be an author, B-quality reviewer, relevance reviewer, executor, redactor, adjudicator, resolver, safety monitor or analyst.
6. A failed family is discarded. It is not repaired after cross-audit; a new unseen authoring version is required.

### 4.2 Mechanical rejection and acceptance rules

Normalization is limited to frozen Unicode normalization, case, whitespace and punctuation normalization, and simple name placeholders. One tokenizer from `resource_envelope_ref` is used. Only a pre-authoring public terminology allowlist may exclude unavoidable terms.

Automatic family rejection occurs for any of the following:

- reuse of a decision-relevant proper name, identifier, numeric tuple or option order;
- an allowlist-external run of eight content tokens shared by decision-relevant source and task passages;
- recovery of the downstream conclusion, required evidence, exception and action by name substitution or surface rearrangement;
- one-to-one correspondence of decisive evidence, priority, exception trigger and required action;
- any D change after task authoring or oracle change after D authoring;
- a task whose permitted answer cannot be determined from its current information.

Acceptance additionally requires all of the following:

- only the frozen latent pattern is shared;
- at least four of six axes differ: action context, deliverable type, evidence form, constraint placement, exception mechanism and correct-action form;
- the task contains at least two decisive relations absent from the source;
- at least one salient source relation cannot be directly reused in the task;
- A remains solvable from the task and D supplies no exclusive answer fact.

The surface/provenance auditor sees source, D, B, tasks and lineage without hidden oracle. The structural auditor sees source, D, tasks and only the oracle meaning needed for structural judgment in a repository- and executor-external read-only environment; oracle content is not copied, summarized or exported. A `FAIL`, `UNCLEAR`, missing record or conflict between the two scopes rejects the family. No adjudicator or analyst can reverse it.

## 5. B semantic quality and blindness

### 5.1 Frozen parity contract

B is a useful, internally coherent synthetic document that is irrelevant to every test latent pattern. Under the same `selected_representation_ref`, B and D must satisfy:

- equal document count and top-level section count, with total context tokens within 5%;
- active, superseded and withdrawn item counts, sourced-claim counts and citation counts each within ±1;
- one-to-one claims at every authority/evidence tier, with no unmatched claim; undefined tier meaning stops authoring;
- modal strength, application-condition count, prohibition count and required-verification count for each actionable rule each within ±1;
- counterexample, limitation and version-replacement counts each within ±1;
- comparable completeness, internal consistency and practical actionability;
- an identical semantic list of general guidance such as verify, defer and check evidence.

Any universal guidance appearing only in D moves to the common wrapper or receives a semantically equivalent B counterpart. Filler, empty generic advice and surface-only parity fail.

### 5.2 Frozen exposure classes

The protocol records append-only person IDs, timestamps, artifact hashes and one or more exposure flags:

- `L_DB`: labeled or readily identifiable D/B;
- `T_ORACLE`: task, latent-pattern or oracle meaning;
- `COND_ID`: condition identity or X/Y mapping;
- `REL_ID`: which material is relevant, irrelevant, applicable or non-applicable.

The two B-quality reviewers, `Q1` and `Q2`, must be different natural people from each other and from every leakage auditor and every other role with any earlier flag above. They may hold no other E0 role. A declaration is not enough: the append-only exposure ledger and access log must both show no prior exposure. Another account, session, agent or worktree does not create a new person.

`Q1` and `Q2` never receive task, latent-pattern, oracle, relevance, condition mapping, labeled D/B, leakage findings or each other's records. They remain excluded from that information until the B package is finally accepted or rejected, and receive none of it later for reuse in E0.

### 5.3 Non-reorderable preapproval chronology

1. **Roster lock:** freeze identities, forbidden combinations, exposure-ledger state, compensation and availability. Any earlier prohibited exposure makes a proposed Q reviewer ineligible.
2. **Authoring close:** D and B are independently closed and hashed. Authors do not contact Q reviewers.
3. **Leakage close:** the two leakage auditors complete their separate transfer audits. Their inputs, identities and findings remain hidden from Q reviewers.
4. **Blind package:** a mapping holder produces randomized X/Y copies and topic-stripped X/Y copies under one frozen stripping rule. The holder records hashes and mapping but gives Q reviewers only X/Y materials and the parity rubric.
5. **Quality lock:** Q1 and Q2 independently lock every parity item, each document's internal usefulness, coherence and actionability, and explicit authority, specificity, completeness and general-guidance judgments as `PASS/FAIL/UNCLEAR` with reasons.
6. **Guess lock:** without any new information, each Q reviewer examines the topic-stripped copies and locks a forced X/Y guess for D, confidence category and reasons. Quality and guess records are timestamped and hashed before any relevance audit begins.
7. **Quality exit:** access is closed. Missing locks, contact, cross-review or prohibited information exposure rejects the package.
8. **Fresh relevance audit:** two new natural people, `R1` and `R2`, distinct from Q1/Q2, both leakage auditors and every authoring, mapping, execution, adjudication and analysis role, independently receive only the minimum frozen task/latent/oracle meaning and mapped X/Y needed to judge relevance. They do not see Q records or each other's records.
9. **Relevance lock:** R1 and R2 independently decide for every family whether B is irrelevant and whether D has the prespecified relevant, non-applicable, stale or withdrawn relationship. Every item must be `PASS` from both.
10. **Cue check and package verdict:** a predesignated mapping-aware verifier compares the locked topic-stripped guesses and reasons with the mapping. A correct D guess whose reason identifies an authority, specificity, actionability, completeness, general-guidance or representation imbalance is a condition-cue failure.

No relevance information may be released, and no relevance audit may begin, before both complete quality and guess locks exist. Chronology is verified by timestamps and hashes, not recollection.

### 5.4 Noncompensatory rejection

The complete B package is rejected for any quality, cue or relevance `FAIL`, `UNCLEAR`, missing item, disagreement, chronology violation, exposure-ledger inconsistency, unauthorized contact or access, or mapping/hashed-copy mismatch. There is no resolver and majority vote. A strong effect estimate cannot compensate. Repair requires a new B package version, new blinded copies and reviewers whose eligibility still passes; old results are not reused.

## 6. Safety unblinding

Primary adjudicators remain condition-blind and never attribute a critical event to D. Execution is released in frozen small blocks. A blind critical candidate stops all new calls. Two blind adjudicators or the blind resolver first lock severity and reasons. Only then may the separate safety monitor open the condition label of that single output ID once.

A confirmed critical event stops the whole run regardless of condition. A D label is used only for attribution and D-package isolation; a non-D label does not permit restart. The monitor sees no other output, score, aggregate trend or unexecuted allocation. Every access, time, reason, field and action is logged. A stopped run cannot contribute a favorable subset to a success analysis.

The safety monitor cannot be an author, auditor, Q or R reviewer, mapping holder, scheduler, executor, redactor, adjudicator, resolver or analyst.

## 7. Redaction, score-before-guess and blinding

Raw outputs stay outside the adjudication view. A mapping- and oracle-blind redaction officer applies a frozen policy to remove condition/package identifiers, wrapper echoes, order/timestamps, model/tool metadata, paths, formatting fingerprints and source labels on long quotations without removing decision, evidence, uncertainty, error or over-application meaning. An independent QC checks policy compliance and meaning preservation.

Each adjudicator independently locks severity, acceptable judgment and reasons before locking a condition guess and confidence category. A blind resolver handles score disagreements. Mapping is released to the analyst only after every score, reason, guess, resolver result and redaction record is locked.

Explicit cues, missing guesses, asymmetric redaction, meaning damage or a failed family-cluster condition-guess guardrail prohibit confirmatory pass and close the result as `adjudication-blinding-threat / inconclusive`. Objective machine-checkable items may be sensitivity results only.

## 8. Sessions, resources and role boundaries

- Every task-condition uses a fresh executor session without other conditions, source, oracle or prior outputs.
- Author, auditor, Q/R reviewer, redactor and adjudicator sessions are never forked into executors.
- Cache, agent memory, retrieval state and local files are condition-isolated. A worktree is not a secret boundary.
- Provider, exact model snapshot, settings, service tier, region, wrappers, tools, network/files, time, output and retry ceiling are frozen within a block.
- Only prespecified symmetric transport retries are allowed. Drift, asymmetric resources or shared state invalidate the block.
- The hidden oracle remains outside the repository, worktree and executor-visible environment.

The operating plan owns the complete person table. An allowlist is a maximum; each role receives only the minimum needed input. Any forbidden exposure is a package or block failure, not a documentation note.

## 9. Mechanical eligibility and claim ceiling

Hashes, the single representation reference, authoring chronology, transfer and B audits, exposure locks, fresh sessions, resource symmetry, redaction, score-before-guess, limited unblinding, all planned calls and all costs are analysis eligibility checks, not performance.

At most:

| Stage | Maximum claim |
|---|---|
| fresh v0.3 review pass | eligible for CONTROL integration review only |
| mechanical preflight | planned comparison is mechanically ready |
| A/D pilot advance | A/B/D confirmation may be worth costing; no effect pass |
| A/B/D confirmation pass | limited evidence at the tested model, family populations, document delivery and resource envelope for an effect exceeding both prespecified worthwhile margins while passing tested guardrails |
| optional C/D pass | limited separate evidence about refinement versus raw access |
| independent repetitions in multiple models | separate within-model replications only |

No stage establishes S0, representation superiority in general, a central system, Project Brain, real-customer or operational value, operational safety, economic value, fine-tuning, persistence or model-to-model transfer.

## 10. Current closed state

Actual references, people, compensation, schedules, models, prices, family counts, materials, oracle, prompts, schemas, code, calls, scores and results remain unknown and closed. v0.3 is a proposal to correct v0.2 review findings. It awaits a new fresh independent read-only review.
