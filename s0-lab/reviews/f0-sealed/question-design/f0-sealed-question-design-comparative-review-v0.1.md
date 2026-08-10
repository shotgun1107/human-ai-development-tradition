# F0-SEALED question-design comparative review v0.1

## Input authentication and boundary

All allowed inputs authenticated successfully:

- Comparative brief: `5bc66d…26a2`
- Protocol v0.3: `b1a721…0b8c`
- Gate record: `364b4d…a7f3`
- Competition brief: `908777…d2a7`
- Track M: `104161…4b55`
- Track V: `5f5520…d032`
- `AGENTS.md`, `answer.schema.json`, and `question-options.schema.json` also matched the hashes embedded in the authenticated competition brief.

The reviewer read only the comparative brief’s maximum allowlist. The reviewer did not inspect sealed staging, public-practice material, I0 code, history, executor material, or other repository files. The reviewer made no file writes.

## Scores

| Criterion | Track M | Track V | Principal deductions |
|---|---:|---:|---|
| Answer-shape leakage resistance | 11/25 | 22/25 | M removes local option lists but retains question-varying `citation_policy` and `affected_ids_policy`, allowing contract-based clues. Its ten glosses also closely mirror question families. V exposes the same complete contract everywhere; residual risks are prompt wording and axis priming. |
| Decision validity and coverage | 13/20 | 12/20 | M’s single actions overlap: deny/defer/no-change, defer/human-decision, deny/data-only, and act/start can all collide. V covers compound decisions but creates 96 tuples, including apparently inconsistent or correlated combinations, and requires complete accepted-tuple sets. Neither demonstrates sealed-question coverage. |
| Deterministic scoring and reviewer agreement | 17/20 | 15/20 | M’s one-ID equality is simpler, but unique-answer admissibility and mapping semantic errors to C/M codes remain unfinished. V supports exact comparison, but multiple accepted tuples/affected sets increase completeness risk; coordinate-to-C/M counting is unresolved. Its example contract also omits the per-question `response_contract_id` later required by its schema delta. |
| Fairness across A–D and two blocks | 13/15 | 12/15 | Both preserve identical questions, model settings, authority, time, output limits, and one response opportunity across conditions. Actual manifests do not yet exist. M’s status/responsibility labels and especially V’s `state_effect`/`route` axes may align more naturally with C/D’s explicit structures; this is a possible measurement interaction, not proven information inequality. |
| Compatibility and migration risk | 8/10 | 4/10 | M preserves most of the answer envelope. V requires coordinated protocol, answer-schema, question-contract, validation, adjudication, and scoring-format changes. |
| Executor burden and operating cost | 4/5 | 2/5 | M requires one choice from ten. V requires three coordinates, navigation among 96 combinations, a citation for every answer, and more field-level completion under the same limits. |
| Falsifiability and rollback clarity | 2/5 | 3/5 | Both have clear rollback and prohibit threshold changes after results. M’s paired 50% ceiling is largely guaranteed by pair construction and does not clearly include its policy fields. V’s permutation test lacks a frozen power/equivalence margin, and “material accuracy difference” is undefined. Both burden thresholds are currently unvalidated. |
| **Total** | **68/100** | **70/100** | Scores do not override noncompensatory failures. |

## Core distinction and fairness judgment

**Track M does not fully remove question-specific answer shape.** It replaces tailored answer sentences with a common semantic-label list, which is useful, but keeps response-contract fields that vary by question. Those policies can narrow the likely answer without consulting records. Its public test does not clearly expose an observer to the complete runner-visible contract, so it would not reliably detect this shortcut.

**Track V removes question-specific answer shape at the design level.** Every question exposes the same axes, values, and field obligations, with no accepted tuple or policy variation visible to the executor. Correctness must still be inferred from evidence. Its principal weakness is no longer leakage shape but whether the universal tuple space is coherent and deterministically complete.

Under either proposal, A–D are specified to receive the same canonical fact set, questions, authority, model/reasoning level, turn count, 15-minute limit, 8,192-byte limit, and retry opportunity. Representation structure intentionally differs. None of that equality has been demonstrated with actual manifests or fixtures.

Neither proposal contains literal D-only terminology. However, M’s lifecycle/responsibility categories and V’s state/route decomposition could preferentially align with structured C/D inputs. V presents the greater alignment risk because it turns that structure into three required scored coordinates.

No post-result threshold change has occurred. The remaining hazard is undefined language—M’s “repeated pattern” and V’s “material difference”—which could permit discretionary interpretation unless quantified before any measurements.

## Noncompensatory checks

| Failure | Track M | Track V |
|---|---|---|
| Tailored question-specific distractors remain | **Pass** — local options and subsets are prohibited, although other question-specific contract cues remain | **Pass** |
| Correct output depends on condition-specific vocabulary | **Pass at design level** | **Pass at design level** |
| Sealed/oracle access is required to define the answer contract | **Pass** — vocabulary is precommitted | **Pass** — axes are precommitted |
| Judge must freely reinterpret unrestricted prose | **Pass** — prose cannot repair structured fields | **Pass** — prose cannot repair structured fields |
| One condition receives more information or opportunity | **Not yet demonstrated** — equality is specified but no delivery artifacts exist | **Not yet demonstrated** — equality is specified but no delivery artifacts exist |
| Claims S0 or broader-system validation | **Pass** | **Pass** |

There is no confirmed literal noncompensatory failure in either document. The not-yet-demonstrated symmetry check blocks sealed use, not design-level candidacy.

## Decisive comparison

Track M has the strongest compatibility and adjudication simplicity. Its decisive weakness is that it leaves question-specific policy shape visible and relies on overlapping compound labels whose uniqueness may require question tailoring.

Track V more directly addresses the reopened gate by eliminating all question-local response-contract variation. Its decisive risk is Cartesian-product ambiguity: globally valid but logically inconsistent tuples, correlated axes, incomplete accepted-alternative sets, added executor burden, and possible alignment with C/D structure.

The narrow two-point preference for V is therefore conditional and design-only. It does not approve implementation, sealed revision, an oracle, scoring, executors, or S0.

## Conditions before successor protocol/schema versions may be frozen

1. Define the object governed by each V axis and either prove coherent semantics for all 96 tuples or freeze one global admissibility matrix used identically for every question. No question-local narrowing is permitted.
2. Freeze a question-admissibility rule showing that required decisions can be represented without sealed-source vocabulary extensions.
3. Define how each tuple-coordinate mismatch maps to exactly one precommitted C/M observation event. Prevent coordinate-level double counting and preserve equal scoring opportunities across A–D.
4. Reconcile the runner-projection inconsistency concerning `response_contract_id`.
5. Prove the maximum authorized question set and serialized answers fit the 8,192-byte ceiling; do not rely only on median output size.
6. Freeze exact A–D equality checks for question/schema hashes, model ID, reasoning level, authority, time, output limit, retries, and judge-visible materials.
7. Add a public test for representation alignment: under identical model conditions, determine whether the UDV grammar changes relative performance across neutral A–D-style public presentations compared with an option-free single-decision control.
8. Complete independent design review before sealed-source access. Any revision after public results requires a new version, hashes, and unaffected holdout or fresh public bank.

Public leakage testing must expose the entire runner-visible prompt, schema, and codebook while withholding records; precommit tuple coverage, sample size, power, chance definition, equivalence margin, multiple-alternative handling, and a numeric definition of “material.” Public adjudication testing must cover every coordinate and incompatible tuple, use independently produced comparators, and require exact deterministic agreement. Burden testing must precommit the control, randomization, thresholds, and first-output treatment.

## Remaining limits

No proposal has been implemented or publicly validated. Sealed-question coverage, actual A–D information equality, model stability, prompt neutrality, tuple completeness, scoring coverage, resource compliance, isolation, and judge reliability remain unverified. Claims in the proposals derived from source-authoring or rereview documents outside this reviewer’s allowlist were not independently verified. At most, this review selects a candidate response design for a two-block synthetic one-turn logic comparison; it establishes nothing about S0 performance, a central system, Project Brain integration, operational safety, economic value, real-world effectiveness, or model-to-model transfer.

## Verdict

**Track V selected as question-design candidate.**
