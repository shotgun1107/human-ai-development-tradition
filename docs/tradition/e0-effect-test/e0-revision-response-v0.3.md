# E0 effect-test v0.3 revision response

- Status: `revision proposal — awaiting fresh independent read-only review`
- Baseline: `central-system-v2.1-s0-preparation`
- Exact authorized gate: `E0 EFFECT TEST DESIGN V0.3 REVISION OPEN`
- Target: authenticated v0.2 independent review verdict `REVISE-AND-REVIEW`
- Authority: traceability entry for v0.3; it does not pass the review or open a later gate.

## 1. Input boundary and integrity

This revision was authored only in the designated worktree on branch `codex/e0-effect-test-v02-review` at commit `de587b60c03dc70c24696f6525f52ccf05b185ab`.

All twelve allowed Markdown inputs were read in full. Every available same-basename sidecar matched before use:

| Authenticated input | Verified SHA-256 |
|---|---|
| `s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| `central-system-v2-common-baseline.md` | `f40bd01f2957d508f55fbfc683503afbe649dfb080608d03fff2f45902f09667` |
| `e0-effect-test/README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` |
| `e0-effect-test-design-v0.2.md` | `cc5da83ebe3fa19ed9d1b31c3798be35bfa4b4969282907788f64b94cad8761a` |
| `e0-measurement-and-analysis-plan-v0.2.md` | `ba23ac34a814940c164be37dae2d4f7eeb75725baaf2bb3237eb288541f17a86` |
| `e0-operating-cost-and-gates-v0.2.md` | `93d79a15fa2085d6675bc31b03e7be5a5a22a072af116d97e82996f483bb45d3` |
| `e0-revision-response-v0.2.md` | `687f3b1776e3216762e2c8825fd98b0be169d24d8978699586ba7443e59970af` |
| `e0-independent-review-brief-v0.2.md` | `c148241e3f7605fa3dfa2a347d44f2ff36b9e06d64ed705c03d5877b6677fe62` |
| `e0-independent-review-v0.2.md` | `35389afb32f17f62b9ff8223d7baf1e6329d0625dc55eccc8a88c81d70fc8de7` |

`AGENTS.md`, `purpose-and-philosophy.md` and `roadmap-and-evaluation.md` had no available same-basename sidecar in the allowed packet. No repository history, `s0-lab/**`, sealed/private/oracle material, other proposal or review, web source, actual project material or file outside the allowlist was read.

## 2. Authenticated v0.2 review result

The v0.2 review found:

- **F-01 blocking:** combined leakage/B-quality roles had already seen identity or relevance information, so X/Y labels could not restore blindness.
- **F-02 major:** one ambiguous family minimum could hide insufficient relevant or harm clusters.
- **F-03 minor:** the frozen README remained a v0.1-only entry point.

It passed the single authenticated representation rule, worthwhile-effect alignment, transfer chronology, limited safety unblinding, redaction and blinding guardrail, S0/E0 separation, oracle boundary, rollback and claim ceiling. v0.3 preserves those corrections and does not claim review success.

## 3. v0.3 document map

| Document | Main responsibility |
|---|---|
| `e0-package-index-v0.3.md` | current v0.3 status and versioned entry point |
| `e0-effect-test-design-v0.3.md` | causal design, transfer boundary, B-quality/relevance chronology, safety and blinding |
| `e0-measurement-and-analysis-plan-v0.3.md` | disjoint family populations, endpoint ledger, estimands, vector power and analysis |
| `e0-operating-cost-and-gates-v0.3.md` | 13/18-person staffing, exposure/absence controls, separate workload and all-call ceilings |
| `e0-independent-review-brief-v0.3.md` | maximum packet and new noncompensatory review rubric |
| `e0-revision-response-v0.3.md` | this closure and preservation map |

All six Markdown files require same-basename `.sha256` sidecars. Earlier files and the README remain unchanged.

## 4. Finding closure map

“Proposed closure” identifies the author's intended mechanical correction, not a reviewer PASS.

### F-01 — proposed closure of B-quality blindness

Design sections 5.2 through 5.4 now require:

1. append-only exposure flags for labeled D/B, task/oracle meaning, condition identity and relevance identity;
2. two dedicated natural-person Q reviewers, distinct from both leakage auditors and every previously exposed role, with no other E0 role;
3. all semantic parity, authority/specificity/actionability/completeness judgments and topic-stripped condition guesses with reasons locked and hashed before any relevance audit begins;
4. no relevance information ever released to Q reviewers;
5. two different fresh natural-person R reviewers who receive minimum relevance semantics only after Q locks and never see Q records;
6. package rejection for any `FAIL`, `UNCLEAR`, disagreement, missing item, cue, exposure breach, contact or chronology violation, with no resolver.

Operating sections 3 through 7 recalculate:

- pilot minimum: 13 distinct people, unchanged because B is absent;
- confirmation minimum: **18 distinct people**, adding a B author, Q1, Q2, R1 and R2 to the 13-role path;
- forbidden combinations and replacement eligibility;
- separate compensation, active/wait/calendar time and absence coverage for Q1, Q2, R1 and R2;
- separate AI-support call categories, verification time and cost ceilings for both Q and both R roles;
- V3-G2, G4 and G6 requirements.

### F-02 — proposed closure of family-set ambiguity

Measurement sections 2 through 6 now require:

- disjoint pre-result `F_R` relevant-transfer and `F_H` harm-challenge sets;
- explicit `N_relevant` and `N_harm`; `N_union` is workload-only;
- eight separately recorded valid-family count rows: two effect, four harm and two blinding-stratum rows;
- a 20-independent-family absolute floor and endpoint-specific power requirement for every row;
- a new named set, count and power term for any endpoint not scorable on its parent set;
- separately ordered relevant and harm reserves, no cross-set borrowing and no pilot/calibration reuse;
- endpoint-specific required counts, then `N_relevant_required` and `N_harm_required` as separate maxima;
- a joint-pass calculation over the vector `(N_relevant, N_harm)`, with frozen inputs and outputs before authoring;
- no overlap in v0.3; any future overlap requires a new reviewed plan and covariance treatment.

Operating sections 5 through 8 carry both sets into instance allocation, executor and retry calls, token maxima, people time, reserve work, cash and V3-G2/G6. A scalar total cannot open either gate.

### F-03 — proposed closure of entry ambiguity

`e0-package-index-v0.3.md` is an explicit versioned entry point stating the current v0.3 review status, reading order, historical status of the unchanged v0.1 README, required sidecars and claim ceiling. No existing file was overwritten.

## 5. Preserved v0.2 corrections

### Single authenticated representation

Exactly one active, versioned, owned, hashed and approved `selected_representation_ref` remains mandatory. A public fallback has identical authentication requirements; empty, multiple, inline or asymmetric use stops authoring. A reference change invalidates dependent materials and audits.

### Worthwhile-effect alignment

The effect estimands remain equal-family-weighted acceptable-judgment differences. The nulls remain `δ ≤ Δ`; a pass requires one-sided family-cluster lower bounds above their respective `Δ`. Planning alternatives remain strictly above `Δ`, and pilot results cannot lower margins or counts.

### Transfer and near-copy

The latent pattern freezes before both authoring lines. Curator and task/oracle author remain separated. Eight-token overlap, one-to-one decision skeleton, chronology breach and non-self-contained tasks reject automatically; four-of-six changed axes, two new decisive relations and one unusable source relation remain required. Two leakage scopes fail closed, and the oracle stays outside repository and executor-visible environments.

### Safety and blinding

Primary adjudicators remain condition-blind. Only the safety monitor opens one locked critical output label; a confirmed critical stops the whole run regardless of label. Raw outputs are independently redacted and QC'd. Scores lock before guesses; explicit cues, asymmetric or meaning-damaging redaction and failed family-cluster guessing prohibit pass.

### Boundaries, rollback and claims

S0 and E0 manipulate different causes; E0 receives only the authenticated representation interface, not S0 winning narratives. Worktrees are not secret boundaries. Invalid or contaminated results are not combined. Cost, harm and blinding never compensate one another. No wording asserts central-system, Project Brain, operational, economic, real-project, fine-tuning or model-transfer validity.

## 6. Unresolved feasibility

The following remain unknown, not promises:

- availability, independence, compensation and calendar feasibility of at least 18 people plus any replacements;
- whether no-prior-exposure Q reviewers and fresh R reviewers can be recruited and kept isolated;
- the eventual endpoint-specific family counts and whether both required sets fit approved ceilings;
- whether the future joint-pass power calculation is feasible;
- whether a useful quality-matched B can remain irrelevant and cue-free;
- whether transfer auditors and relevance reviewers will agree on future synthetic materials;
- whether meaning-preserving redaction can pass both relevant and harm blinding strata;
- whether exactly one representation artifact will be approved;
- future model, price, token, time and cash values.

Failure of any required future gate means `STOP/DEFER` or a newly reviewed narrower design. It does not justify weakening independence, family counts or guardrails.

## 7. Bounded status

> E0 v0.3 is a design-only revision proposal that mechanically addresses F-01 through F-03 while preserving the v0.2 corrections that passed. It awaits a new fresh independent read-only review.

No materials, oracle, prompts, schema, code, runner, model call, simulation, score, result, staffing commitment, budget approval or later gate has been created or opened.
