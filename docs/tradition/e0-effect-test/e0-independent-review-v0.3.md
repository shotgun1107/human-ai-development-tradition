# E0 effect-test design v0.3 independent hostile review

- Review type: `fresh hostile read-only revision review`
- Reviewed branch: `codex/e0-effect-test-design-v03`
- Reviewed HEAD: `c1c3b7ec5b5dd508c1e1d5cd0408ba0be331b46e`
- Review date: `2026-08-08` (KST)
- Final verdict: **REVISE-AND-REVIEW**
- Authority: CONTROL-integration suitability only
- Not authorized: representation selection, staffing or budget approval, material/oracle/prompt/schema/code creation, model calls, simulation, scoring, execution, effect or safety findings, or any later gate

## 1. Input boundary and integrity

**Input-boundary verdict: PASS.** The designated worktree initially had the exact supplied branch and HEAD and was clean. All 18 allowlisted Markdown files were read in full. Every one of the 15 available same-basename sidecars matched before reliance. The three files without an available sidecar are identified below; their calculated hashes are recorded without claiming sidecar authentication.

| Input | Verified SHA-256 | Sidecar |
|---|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | not available |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matched |
| `docs/tradition/purpose-and-philosophy.md` | `c62966864428392d7a70bd23996d461c53e600e540c4737ade52523f22cafef0` | not available |
| `docs/tradition/central-system-v2-common-baseline.md` | `f40bd01f2957d508f55fbfc683503afbe649dfb080608d03fff2f45902f09667` | matched |
| `docs/tradition/roadmap-and-evaluation.md` | `4d3b15e509d4ac278c23ee0a4d43900d630e3b421afcae7b160527401f689892` | not available |
| `docs/tradition/e0-effect-test/README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` | matched |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.2.md` | `cc5da83ebe3fa19ed9d1b31c3798be35bfa4b4969282907788f64b94cad8761a` | matched |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.2.md` | `ba23ac34a814940c164be37dae2d4f7eeb75725baaf2bb3237eb288541f17a86` | matched |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.2.md` | `93d79a15fa2085d6675bc31b03e7be5a5a22a072af116d97e82996f483bb45d3` | matched |
| `docs/tradition/e0-effect-test/e0-revision-response-v0.2.md` | `687f3b1776e3216762e2c8825fd98b0be169d24d8978699586ba7443e59970af` | matched |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.2.md` | `c148241e3f7605fa3dfa2a347d44f2ff36b9e06d64ed705c03d5877b6677fe62` | matched |
| `docs/tradition/e0-effect-test/e0-independent-review-v0.2.md` | `35389afb32f17f62b9ff8223d7baf1e6329d0625dc55eccc8a88c81d70fc8de7` | matched |
| `docs/tradition/e0-effect-test/e0-package-index-v0.3.md` | `86cdd2021019737f574ce3f8678b03484821abe43ef0deea04a12612fdd083fd` | matched |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.3.md` | `a3802b7c682388059ad718270fb36307160e462fa84fe35330de2078532f8fd9` | matched |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.3.md` | `8eab2dcd19953dfcc75a56ee3cf0046023aa8605dc493ff16eb2d0a520bfc32a` | matched |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.3.md` | `3aa178e45c00a16550afc036c313093adc95650c1339d4e2b54e4220971ceb0c` | matched |
| `docs/tradition/e0-effect-test/e0-revision-response-v0.3.md` | `1bd9d67bd9c0094a16ef564cf888f7095d8456e916560d3f2971cf40ec4b4c16` | matched |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.3.md` | `d2d64c593e6c381069366745e709f4dea9be731ee8a533d4df0df369d3361f97` | matched |

No repository history, broad search, `s0-lab/**`, S0 result, sealed/private/oracle material, fixture, condition package, prompt, schema, code, tool or simulation result, customer/personal/secret/past-project content, another review, or web source was read. Worktree separation is treated only as edit isolation.

## 2. Findings

### F-01 — FAIL: cross-version Q-reviewer re-entry defeats durable blindness

- Severity: **blocking**
- Failed claim: Q1 and Q2 remain genuinely unexposed throughout B-package repair or reviewer replacement, and a new blinded package version is enough to restore quality-review blindness.
- Evidence:
  - Design v0.3 section 5.2 makes prior `L_DB`, `T_ORACLE`, `COND_ID` or `REL_ID` exposure disqualifying, but does not record exposure to an earlier **unmapped X/Y or topic-stripped candidate** as a permanent Q-review exclusion.
  - Design section 5.4 permits repair with a “new B package version, new blinded copies and reviewers whose eligibility still passes”; it does not require two new Q reviewers after either Q has seen the rejected version.
  - Operating section 3.4 requires a new blinded package and chronology after Q replacement, but does not retire the other Q reviewer who already saw the prior X/Y pair.
  - The repair language changes the B package, while D may remain byte- or content-stable. A reused reviewer can recognize the stable candidate across randomized mappings and infer D identity even though no mapping was disclosed in the first round.
- Consequence: the first-cycle 18-person separation is sound, but a rejected/repaired B package or mid-review Q replacement can legally reuse a person whose earlier unlabeled exposure becomes identifying when compared with the new pair. Label randomization cannot restore blindness. The exposure ledger does not currently close this path, and replacement staffing/time/cost maxima can undercount the fresh pair actually required.
- Minimum correction direction:
  1. add an append-only exposure class covering any full or topic-stripped D/B candidate, even when unmapped;
  2. make any such exposure permanently ineligible for Q1/Q2 on every later package version;
  3. after package rejection, amendment, Q access failure or Q replacement after access, retire both Q reviewers and restart with two new natural people, new copies, new locks and revised replacement ceilings;
  4. prohibit cross-version candidate comparison and carry the fresh-pair consequence through compensation, availability, absence, AI-support, token and cash ceilings.
- Rereview scope: design v0.3 sections 5.2–5.4; operating v0.3 sections 3.3–3.4, 4–7 and V3-G2/G4/G6; revision-response F-01; the next review brief's exposure and restart rubric.

The initial one-version chronology otherwise passes: D/B close and hash before Q review; Q1/Q2 are dedicated and separated from leakage and relevance roles; complete quality and forced-guess records lock before relevance release; R1/R2 are different fresh people; and any first-cycle disagreement or missing record rejects without a resolver. That does not compensate for the lifecycle loophole.

### F-02 — FAIL: the family vector stops before human time and cash

- Severity: **major**
- Failed claim: every relevant/harm family requirement propagates separately through workload, calls, tokens, people time and cash before totals, so a scalar operational estimate cannot open a gate.
- Evidence:
  - Measurement v0.3 sections 3.3 and 5 correctly specify eight endpoint rows, separate `N_relevant`/`N_harm` requirements and vector joint-power planning.
  - Operating section 5 keeps relevant, harm and reserve executor calls and tokens separate.
  - Operating section 4 defines `H_total_active_max` only as a sum by role. Waiting and calendar ceilings likewise list roles, not `F_R`, `F_H`, `F_R_reserve` and `F_H_reserve` components.
  - Operating section 6 separates AI cash into `C_AI_R_max`, `C_AI_H_max` and reserve terms, but aggregates all human compensation into `C_human_compensation_18_roles_max` and `C_replacement_compensation_max` without relevant/harm/reserve terms.
  - V3-G2 requires separate relevant/harm/reserve call, token and workload maxima, but does not require set-specific human active/wait/calendar time or human cash. This conflicts with review brief v0.3 section 6.4 and revision-response v0.3 section 4's claim that people time and cash carry both sets.
- Consequence: a future worksheet can satisfy the literal gate with scalar human-time and human-cash totals even though changing or releasing one family set has no auditable marginal human resource propagation. The endpoint vector therefore does not fully reach the stop-before-authoring feasibility decision.
- Minimum correction direction:
  1. split every family-dependent human active, waiting and calendar-time term into relevant, harm, relevant-reserve and harm-reserve components;
  2. split corresponding human compensation and replacement exposure the same way;
  3. keep genuinely fixed/common overhead in an explicit separate term;
  4. require these rows, both set requirements and all reserve maxima in V3-G2 and V3-G6 before totals and user approval.
- Rereview scope: measurement v0.3 section 3.3's operating propagation contract; operating v0.3 sections 4–7 and V3-G2/G6; revision-response F-02; the next review brief's cost-propagation rubric.

The set and statistical core passes: `F_R` and `F_H` are pre-result and disjoint; pilot/calibration/optional families do not count; cross-set movement and borrowing are prohibited; all A/B/D instances use fresh sessions; repeats and instances do not inflate family N; all eight rows have an absolute 20-family floor and endpoint-specific requirement; and joint planning uses `(N_relevant, N_harm)` with no cross-set surplus substitution.

### F-03 — UNCLEAR: the entry point is fixed, but v0.1 immutability is unverifiable in the authorized packet

- Severity: **minor**
- Failed claim: the reviewer can independently confirm that README, v0.1 and v0.2 were all left unchanged while remaining inside the maximum packet.
- Evidence:
  - Package index v0.3 clearly identifies v0.3 as the current revision proposal, maps all six current documents, requires sidecars, labels README as the frozen historical v0.1 entry point, and opens no gate.
  - Current README and all allowlisted v0.2 files match their sidecars.
  - Review brief v0.3 section 7 asks whether v0.1 files were left unchanged, and section 9 treats silent overwrite as noncompensatory, but section 2 omits the four v0.1 Markdown files from the maximum packet.
  - The authenticated v0.2 review records earlier v0.1 hashes only at its reviewed commit; it does not authenticate the current HEAD bytes. Repository-history inspection and unlisted-file hashing are prohibited.
- Consequence: navigation is repaired, but the complete immutability assertion cannot receive an independent `PASS` without violating the review boundary. Author statements are not byte verification.
- Minimum correction direction: add the four current v0.1 Markdown files and their available same-basename sidecars to the next maximum packet, or add a CONTROL-authenticated current-HEAD immutability manifest that binds each current v0.1 path and hash and is itself allowlisted.
- Rereview scope: current v0.1 byte identities, package-index relationship section and the next input-boundary rubric only.

## 3. Preserved v0.2 correction verdicts

| Correction | Verdict | Assessment |
|---|---|---|
| **B-01 — single authenticated representation** | **PASS** | Exactly one versioned, owned, hashed and approved reference is required; fallback has identical status; empty, plural, inline, asymmetric or changed references stop or invalidate dependent work. |
| **M-01 — worthwhile-effect alignment** | **PASS** | Equal-family estimands, `δ ≤ Δ` nulls, lower bounds `> Δ`, planning alternatives above the same margins and the reporting ceiling remain aligned; pilot results cannot lower margins or counts. |
| **M-02 — family/session clustering** | **PASS** | Complete task family is the inferential/resampling unit; every endpoint row has its own valid count and requirement; instances and repeated sessions cannot increase N; McNemar remains diagnostic. The separate operating propagation failure is F-02. |
| **M-03 — transfer/near-copy** | **PASS** | Latent pattern freezes first; author paths remain separated; token, skeleton, chronology and self-containment rules fail closed; four-of-six axes, two new relations and one unusable source relation remain mandatory; both leakage scopes must pass. |
| **M-04 — B semantic quality/preapproval** | **FAIL** | First-cycle Q/R separation is corrected, but F-01 permits cross-version Q re-entry after prior candidate exposure, so blindness is not durable across the allowed repair path. |
| **M-05 — limited safety unblinding** | **PASS** | Primary adjudicators remain blind; only one locked output label may be opened by the safety monitor; any confirmed critical stops the whole run regardless of condition; no favorable subset or non-D restart is allowed. |
| **M-06 — redaction/adjudication blinding** | **PASS** | Independent redaction/QC, score-before-guess, post-lock mapping, separate relevant/harm guess bounds and failure-closed cue or meaning-damage rules remain explicit. |
| **M-07 — staffing/cost** | **FAIL** | The 13/18 base-person counts and per-role compensation/absence/all-call categories are improved, but F-01's repair path lacks a mandatory fresh Q pair and F-02 leaves human time and cash scalar by family set. |

## 4. Required system and condition verdicts

| Area | Verdict |
|---|---|
| B-quality initial exposure chronology | **PASS for one untouched package only** |
| B-quality repair/replacement chronology | **FAIL — F-01** |
| Separate fresh relevance review | **PASS** |
| 13-person A/D base minimum | **PASS as a design minimum; feasibility unknown** |
| 18-person A/B/D base minimum | **PASS for the first cycle; replacement/restart coverage FAIL — F-01** |
| Per-person compensation, time, availability and absence fields | **PASS** |
| All-AI-call category coverage | **PASS** |
| Eight endpoint memberships, valid counts and floors | **PASS** |
| Disjoint relevant/harm allocation and reserve rules | **PASS** |
| Endpoint-specific and vector joint-power contract | **PASS as a future calculation contract; no power result exists** |
| Relevant/harm executor, retry, reserve-call and token propagation | **PASS** |
| Relevant/harm human time and human cash propagation | **FAIL — F-02** |
| Single representation and fallback boundary | **PASS** |
| Estimand/null/lower-bound/power alignment | **PASS** |
| Transfer chronology and external oracle boundary | **PASS** |
| Limited safety unblinding | **PASS** |
| Redaction, score-before-guess and two-stratum blinding | **PASS** |
| S0/E0 separation, rollback and noncombination | **PASS** |
| Claim ceiling | **PASS** |

Condition verdicts:

- **A/D — PASS, pilot only:** feasibility and direction only; no effect pass or confirmatory-family reuse.
- **B — FAIL for confirmation:** B remains required, but the allowed repair/replacement lifecycle does not preserve Q blindness.
- **C — PASS, optional diagnostic:** it cannot replace or compensate for A/B/D.
- **Four-condition simultaneous — PASS as closed by default:** a separate reviewed question, family vector, power, staffing and budget remain mandatory.

## 5. Finding inventory and passed closures

- Blocking findings: **1** (`F-01`)
- Major findings: **1** (`F-02`)
- Minor/unclear findings: **1** (`F-03`)

Passed closures are the single authenticated representation, worthwhile-effect alignment, endpoint-specific family counts and vector power structure, family/session noninflation, transfer/near-copy chronology, separate first-cycle Q and R roles, limited safety unblinding, redaction/adjudication blinding, A/D pilot-only status, optional C, closed-by-default four-condition execution, external oracle boundary, rollback and restricted claim ladder.

## 6. Unresolved feasibility

No feasibility fact is inferred. It remains unknown whether:

- 18 eligible people plus the fresh replacement pairs required by a corrected restart rule can be recruited, compensated and kept available;
- Q and R exposure isolation can be maintained in practice;
- the eight endpoint-specific counts and `(N_relevant, N_harm)` joint-power vector fit an approvable ceiling;
- a useful, quality-matched, cue-free and irrelevant B can be authored;
- leakage and relevance reviewers agree on future synthetic materials;
- meaning-preserving redaction passes both blinding strata;
- exactly one representation artifact is approved;
- future model, price, call, token, human-time, calendar and cash ceilings coexist.

Any failure remains `STOP/DEFER` or requires a newly reviewed narrower design. It does not authorize weaker independence, fewer families, merged sets or reduced guardrails.

## 7. Maximum allowed claim

> E0 v0.3 is a design-only revision that closes the first-cycle separation of B-quality and relevance review and makes endpoint-specific family counts and vector power explicit, but independent review found a blocking cross-version Q-blindness loophole, incomplete relevant/harm propagation of human time and cash, and an input-boundary gap for verifying v0.1 immutability. It does not establish material readiness, implementation, execution, effectiveness, safety, economic or real-project value, central-system or Project Brain validity, model learning, persistence or model-to-model transfer.

## 8. Minimum correction, rereview packet and exact next gate

Do not pass V3-G0. Keep V3-G1 and every staffing, budget, authoring, preflight, pilot, confirmation and extension gate closed.

Minimum correction scope is limited to the F-01 lifecycle exposure/restart rules, their replacement-resource consequences, F-02 set-specific human time/cash propagation, and F-03 current-byte verification. Preserve every passed correction unchanged except where a cross-reference must be updated.

The next maximum input packet should be exactly the current 18 Markdown inputs and available sidecars, plus:

1. `docs/tradition/e0-effect-test/e0-effect-test-design-v0.1.md`
2. `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.1.md`
3. `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.1.md`
4. `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.1.md`
5. `docs/tradition/e0-effect-test/e0-independent-review-v0.3.md`
6. `docs/tradition/e0-effect-test/e0-package-index-v0.4.md`
7. `docs/tradition/e0-effect-test/e0-effect-test-design-v0.4.md`
8. `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.4.md`
9. `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md`
10. `docs/tradition/e0-effect-test/e0-revision-response-v0.4.md`
11. `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.4.md`

and every available same-basename sidecar for those additions. No S0 result, fixture, oracle, prompt, schema, code, simulation, execution output, web source or other repository material is needed.

Recommended exact next design gate:

`E0 EFFECT TEST DESIGN V0.4 REVISION OPEN`

## 9. Final verdict

**REVISE-AND-REVIEW**
