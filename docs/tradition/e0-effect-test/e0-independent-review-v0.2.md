# E0 effect-test design v0.2 independent hostile review

- review type: `fresh hostile read-only revision review`
- reviewed commit: `7799324f8f82544e764624fce1bde87162a16a9b`
- reviewed branch: `codex/e0-effect-test-design-v02`
- final verdict: **REVISE-AND-REVIEW**
- authority: CONTROL-integration suitability only
- not authorized: material authoring, implementation, model execution, scoring, effectiveness claims, staffing/budget approval, or downstream gate

## 1. Input boundary and integrity

The reviewer read all 15 allowlisted Markdown files. The 12 files with assigned same-basename SHA-256 sidecars matched. Repository history, S0 material, sealed or oracle material, web sources, and other reviews or outputs were not read. No file was created or changed by the reviewer, and no execution or scoring occurred.

| Input | SHA-256 |
|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` |
| `s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| `purpose-and-philosophy.md` | `c62966864428392d7a70bd23996d461c53e600e540c4737ade52523f22cafef0` |
| `central-system-v2-common-baseline.md` | `f40bd01f2957d508f55fbfc683503afbe649dfb080608d03fff2f45902f09667` |
| `roadmap-and-evaluation.md` | `4d3b15e509d4ac278c23ee0a4d43900d630e3b421afcae7b160527401f689892` |
| E0 package `README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` |
| design v0.1 | `96de9cc3bdb695e32f98daa5b1d81585669a7c42c7bc90fc98efbcbf65f60986` |
| measurement v0.1 | `bc0baf919863de6901026cc7ba6a756f00ce04c1e5ad67ae365e283f17d6545f` |
| operating v0.1 | `5a847ce5c95e970c1163cbfa19bc903312bfa104ad01c5b88b0c8481b4753ab8` |
| review brief v0.1 | `6bada32d807dd066ece8f971a1adc8d4039c945567e7ee345bc4be8114bd1ffa` |
| design v0.2 | `cc5da83ebe3fa19ed9d1b31c3798be35bfa4b4969282907788f64b94cad8761a` |
| measurement v0.2 | `ba23ac34a814940c164be37dae2d4f7eeb75725baaf2bb3237eb288541f17a86` |
| operating v0.2 | `93d79a15fa2085d6675bc31b03e7be5a5a22a072af116d97e82996f483bb45d3` |
| revision response v0.2 | `687f3b1776e3216762e2c8825fd98b0be169d24d8978699586ba7443e59970af` |
| review brief v0.2 | `c148241e3f7605fa3dfa2a347d44f2ff36b9e06d64ed705c03d5877b6677fe62` |

`AGENTS.md`, purpose and philosophy, and roadmap had no sidecars assigned by the review packet; their calculated hashes are recorded without claiming sidecar authentication.

## 2. Findings

### F-01 — B-quality review blindness is structurally broken

- Severity: **blocking**
- Failed claim: two independent reviewers approve B/D semantic quality, authority, specificity parity, and condition cues while condition-blind under X/Y labels.
- Evidence:
  - Design v0.2 section 4.3 allows a leakage auditor to see labeled source, D, B, task, or D/task/oracle semantics.
  - Design section 5.2 permits the same auditor to act as B-quality reviewer.
  - The same reviewer separately determines which document contains the latent pattern during relevance review.
  - Operating plan section 3 combines each person as `leakage/B-quality reviewer` in the minimum staffing count.
- Consequence: replacing labels with X/Y cannot restore blindness after a reviewer has already seen labeled D/B or has identified D through relevance. A topic-stripped condition guess can be answered from memory. B preapproval and the stated 14-person staffing path are therefore invalid.
- Minimum correction direction:
  - separate B-quality reviewers from every person exposed to labeled D/B, task/oracle meaning, or leakage-review condition identity;
  - lock semantic parity and topic-stripped guess with reasons before relevance information is disclosed, or assign relevance to separate people;
  - recalculate distinct-person minimums, forbidden role combinations, compensation, absence coverage, and AI-call ceilings.
- Required rereview scope: design sections 4.3 and 5.2; operating sections 3, 6, V2-G2, V2-G4, and V2-G6; revision-response M-04 and M-07 claims.

### F-02 — Cluster minimum and power allocation are ambiguous across family sets

- Severity: **major**
- Failed claim: primary effect, safety interval, and joint power all use the same explicit independent-family unit and sufficient minimum cluster count.
- Evidence:
  - Measurement v0.2 separates relevant-transfer families from harm families.
  - The effect estimand uses relevant families while safety uses harm families.
  - The prohibition on fewer than 20 independent families does not state whether it applies separately to each participating estimand set or only to the combined total.
  - Power and cost gates refer to one minimum independent-family count or cluster-aware N.
- Consequence: a design with 20 total families split into 10 relevant and 10 harm families could be read as passing the minimum even though each confirmatory statistic has only 10 clusters.
- Minimum correction direction:
  - state the cluster minimum separately for every family set entering a confirmatory estimand or guardrail;
  - freeze pre-result allocation of relevant and harm family counts and identify their separate joint-power inputs and outputs;
  - carry each required count into staffing and cost ceilings.
- Required rereview scope: measurement sections 2, 3.3, and 5; operating section 6 and gates V2-G2/V2-G6.

### F-03 — Package README remains a v0.1-only entry point

- Severity: **minor**
- Failed claim: the public package entry point clearly identifies the current proposal under review.
- Evidence: the existing package README maps and labels only v0.1, while the revision response intentionally leaves it unchanged.
- Consequence: without a strict packet prompt, a reader may treat v0.1 as the active proposal. This does not change the causal review verdict.
- Minimum correction direction: preserve v0.1 while adding an explicit versioned v0.2-or-later entry point and current status to the package index.
- Required rereview scope: README and revision-response document map only.

## 3. Review of v0.1 findings

| Prior finding | Verdict | Assessment |
|---|---|---|
| **B-01** | **PASS** | Exactly one versioned, owned, hashed representation reference is required. Fallback receives identical authentication; empty, multiple, or inline bypasses stop authoring; A and B/C/D share the representation contract; changes require re-authoring. |
| **M-01** | **PASS** | Family-weighted estimand, `H0: delta <= Delta`, lower bound `> Delta`, planning alternative, Bonferroni allocation, joint power, and claim limit are aligned. Pilot observations cannot reduce Delta, the planning effect, or N. |
| **M-02** | **UNCLEAR** | Family is the primary resampling unit, repeated sessions do not increase N, and McNemar is diagnostic. F-02 leaves per-estimand family minimums and power allocation ambiguous. |
| **M-03** | **PASS** | Latent pattern freezes first; author paths are separated; token overlap, decision skeleton, chronology, and change-axis rules fail closed; two pre-result auditors must agree; oracle access stays outside repository and executor-visible environments. |
| **M-04** | **FAIL** | Surface and semantic rules are stronger, but the F-01 role-combination path prevents condition-blind X/Y quality approval. |
| **M-05** | **PASS** | Primary adjudicators do not attribute conditions. Only the safety monitor opens one output label after blind critical lock, and a confirmed critical event stops the complete run regardless of label. |
| **M-06** | **PASS** | Independent redaction and QC, score-before-guess, mapping lock, family-cluster guess guardrail, and noncompensatory cue or redaction failures are explicit. |
| **M-07** | **FAIL** | Compensation, time, absence, and all-AI-call accounting are materially improved, but the claimed 14-person minimum relies on the invalid combined auditor/B-reviewer role. |

## 4. Condition verdicts

- **A/D — PASS, pilot only:** sufficient for total-package feasibility and directional pilot work; value or effect pass remains forbidden; pilot families cannot enter confirmatory analysis.
- **B — FAIL:** B remains required for content confirmation, but current preapproval roles and sequence are not condition-blind. A/B/D execution cannot open.
- **C — PASS, optional diagnostic:** C cannot compensate for or replace A/B/D failure.
- **Four-condition simultaneous — PASS as closed-by-default design:** it remains unjustified by default and requires separate value, cluster-power, staffing, budget, preregistration, and gate approval.

## 5. System-level verdicts

| Area | Verdict |
|---|---|
| Primary outcome, critical/major rules, deterministic oracle requirements | **PASS** |
| Estimand, null, lower-bound, and power alignment | **PASS** |
| Family/session clustering | **UNCLEAR — F-02** |
| Transfer/near-copy chronology | **PASS** |
| B semantic quality and preapproval | **FAIL — F-01** |
| Limited safety unblinding | **PASS** |
| Redaction, score-before-guess, and blinding guardrail | **PASS** |
| Staffing minimum | **FAIL — F-01** |
| Compensation, time, and absence rules | **PASS** |
| All-AI-call ledger and worst-case cost scope | **PASS** |
| Power, staffing, and cost coexistence | **UNCLEAR/DEFER** |
| S0/E0 separation and single connection point | **PASS** |
| Hidden-oracle repository/worktree/executor boundary | **PASS** |
| Rollback, stopping, and noncombination of contaminated results | **PASS** |
| Claim ceiling | **PASS** |

## 6. Maximum claim

The maximum defensible claim is:

> E0 v0.2 is a revision proposal that mechanically addresses a substantial part of the v0.1 review, but independent review requires further revision of B-preapproval blindness and the family-cluster count contract. It does not establish S0 or E0 success, material or implementation readiness, execution, effectiveness, safety, economic value, real-project value, or model-to-model transfer.

## 7. Next gate recommendation

- Do not pass V2-G0.
- Create a new version of the design, measurement, operating, revision-response, package index, and sidecars that addresses F-01 through F-03.
- Submit that version to a fresh independent review under the same public-only boundary.
- Keep V2-G1 and every later staffing, budget, authoring, preflight, pilot, and confirmatory gate closed.
- The next review packet may add only the new versioned documents, sidecars, and an authenticated CONTROL record of this review to the current v0.2 brief packet.

Recommended exact next design gate:

`E0 EFFECT TEST DESIGN V0.3 REVISION OPEN`

## 8. Final verdict

**REVISE-AND-REVIEW**
