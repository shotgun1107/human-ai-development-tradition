# E0 effect-test design v0.4 independent hostile review

- Review type: `fresh hostile read-only revision review`
- Repository: `C:/Users/kimsiyeol/.codex/worktrees/e5fd/human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Reviewed HEAD: `e22e1c08ca12e5b485921d1f4ed03591e3f47701`
- Ref state: detached HEAD at the exact expected commit; `codex/e0-effect-test-design-v04` was verified at the same commit in its separate worktree
- Initial worktree state: clean
- Review date: `2026-08-08` (KST)
- Final verdict: **PASS-FOR-CONTROL-INTEGRATION-ONLY**
- Authority: CONTROL-integration suitability only
- Not authorized: representation selection, staffing or budget approval, material/oracle/prompt/schema/code creation, model calls, simulation, scoring, execution, effect or safety findings, or any later gate

## 1. Input boundary and integrity

**Input-boundary verdict: PASS.** The exact repository, origin, supplied HEAD, detached ref state, clean worktree and worktree registration were verified without repository-history exploration. All 29 allowlisted Markdown files were read in full. Every one of the 26 available exact same-basename sidecars matched before reliance. The three files without an available sidecar are identified below; their calculated hashes are recorded without claiming sidecar authentication.

| Input | Calculated SHA-256 | Sidecar verdict |
|---|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | not available |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | match |
| `docs/tradition/purpose-and-philosophy.md` | `c62966864428392d7a70bd23996d461c53e600e540c4737ade52523f22cafef0` | not available |
| `docs/tradition/central-system-v2-common-baseline.md` | `f40bd01f2957d508f55fbfc683503afbe649dfb080608d03fff2f45902f09667` | match |
| `docs/tradition/roadmap-and-evaluation.md` | `4d3b15e509d4ac278c23ee0a4d43900d630e3b421afcae7b160527401f689892` | not available |
| `docs/tradition/e0-effect-test/README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` | match |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.1.md` | `96de9cc3bdb695e32f98daa5b1d81585669a7c42c7bc90fc98efbcbf65f60986` | match |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.1.md` | `bc0baf919863de6901026cc7ba6a756f00ce04c1e5ad67ae365e283f17d6545f` | match |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.1.md` | `5a847ce5c95e970c1163cbfa19bc903312bfa104ad01c5b88b0c8481b4753ab8` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.1.md` | `6bada32d807dd066ece8f971a1adc8d4039c945567e7ee345bc4be8114bd1ffa` | match |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.2.md` | `cc5da83ebe3fa19ed9d1b31c3798be35bfa4b4969282907788f64b94cad8761a` | match |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.2.md` | `ba23ac34a814940c164be37dae2d4f7eeb75725baaf2bb3237eb288541f17a86` | match |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.2.md` | `93d79a15fa2085d6675bc31b03e7be5a5a22a072af116d97e82996f483bb45d3` | match |
| `docs/tradition/e0-effect-test/e0-revision-response-v0.2.md` | `687f3b1776e3216762e2c8825fd98b0be169d24d8978699586ba7443e59970af` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.2.md` | `c148241e3f7605fa3dfa2a347d44f2ff36b9e06d64ed705c03d5877b6677fe62` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-v0.2.md` | `35389afb32f17f62b9ff8223d7baf1e6329d0625dc55eccc8a88c81d70fc8de7` | match |
| `docs/tradition/e0-effect-test/e0-package-index-v0.3.md` | `86cdd2021019737f574ce3f8678b03484821abe43ef0deea04a12612fdd083fd` | match |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.3.md` | `a3802b7c682388059ad718270fb36307160e462fa84fe35330de2078532f8fd9` | match |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.3.md` | `8eab2dcd19953dfcc75a56ee3cf0046023aa8605dc493ff16eb2d0a520bfc32a` | match |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.3.md` | `3aa178e45c00a16550afc036c313093adc95650c1339d4e2b54e4220971ceb0c` | match |
| `docs/tradition/e0-effect-test/e0-revision-response-v0.3.md` | `1bd9d67bd9c0094a16ef564cf888f7095d8456e916560d3f2971cf40ec4b4c16` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.3.md` | `d2d64c593e6c381069366745e709f4dea9be731ee8a533d4df0df369d3361f97` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-v0.3.md` | `995ca5d6ff24e5b6ad2268992b72caa99f1e39934656e52038263d7942ca4ff4` | match |
| `docs/tradition/e0-effect-test/e0-package-index-v0.4.md` | `6c88892323ca5361d644d231b0518804441772bdac9442d3f00383fcc91e6270` | match |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.4.md` | `39b761d5e00f156c1c01b1670980d22e5232241c71a5f103e1efa88f52a312dd` | match |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.4.md` | `9e972de90ca2a861079dc629193cc95e9fc788f5999df2075cb0c5e422d4a4d9` | match |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md` | `9124990ebfd328a8628728317cbce62385a2a059e888e30c300eb55627409057` | match |
| `docs/tradition/e0-effect-test/e0-revision-response-v0.4.md` | `ec70f33e3faa656b10d0ef564d19bfb335ed849d12f27ce6546785343e348fb0` | match |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.4.md` | `e8880b81500ab60967dd4fc087de14df9775cd32fc857b10ecacb7eb3bded5a7` | match |

No repository history, broad search, `s0-lab/**`, S0 candidate or output, sealed/private/oracle material, fixture, condition package, prompt, schema, code, experiment output, simulation/result, customer/personal/secret/past-project content, another unlisted proposal or review, or web source was read. Worktree separation is treated only as edit isolation.

### 1.1 Required current-byte identity record

| Exact current file | Exact sidecar expected value | Independently calculated current value | Verdict |
|---|---|---|---|
| `docs/tradition/e0-effect-test/README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` | **MATCH** |
| `docs/tradition/e0-effect-test/e0-effect-test-design-v0.1.md` | `96de9cc3bdb695e32f98daa5b1d81585669a7c42c7bc90fc98efbcbf65f60986` | `96de9cc3bdb695e32f98daa5b1d81585669a7c42c7bc90fc98efbcbf65f60986` | **MATCH** |
| `docs/tradition/e0-effect-test/e0-measurement-and-analysis-plan-v0.1.md` | `bc0baf919863de6901026cc7ba6a756f00ce04c1e5ad67ae365e283f17d6545f` | `bc0baf919863de6901026cc7ba6a756f00ce04c1e5ad67ae365e283f17d6545f` | **MATCH** |
| `docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.1.md` | `5a847ce5c95e970c1163cbfa19bc903312bfa104ad01c5b88b0c8481b4753ab8` | `5a847ce5c95e970c1163cbfa19bc903312bfa104ad01c5b88b0c8481b4753ab8` | **MATCH** |
| `docs/tradition/e0-effect-test/e0-independent-review-brief-v0.1.md` | `6bada32d807dd066ece8f971a1adc8d4039c945567e7ee345bc4be8114bd1ffa` | `6bada32d807dd066ece8f971a1adc8d4039c945567e7ee345bc4be8114bd1ffa` | **MATCH** |

The current README and v0.1 values also equal the authenticated values recorded in the allowlisted earlier review records. Current v0.2 and v0.3 hashes equal their sidecars and the allowlisted authenticated review records. This is a current-packet byte comparison, not repository-history inspection.

## 2. Finding inventory

- Blocking findings: **none**
- Major findings: **none**
- Minor findings: **none**
- Claim-relevant `UNCLEAR`: **none**

## 3. F-01 — durable Q blindness across versions

**Verdict: PASS.**

### 3.1 Lifetime semantic exposure — PASS

Design v0.4 section 5.2 defines one append-only lifetime E0 ledger and records `CAND_DB` at access start for every full or topic-stripped D/B-derived candidate, including mapped or unmapped X/Y, current, rejected and superseded versions. It retains the independent `L_DB`, `T_ORACLE`, `COND_ID` and `REL_ID` flags. Candidate access permanently bars that natural person from Q1/Q2 on every later package version, repair, amendment or restart. Deletion, relabeling, topic stripping, a new account, session, agent, employer, worktree or declaration cannot clear exposure.

### 3.2 Fail-closed natural-person identity — PASS

Design section 5.2 and operating section 3.1 require one stable natural-person ID, all known aliases, positive identity evidence, lifetime-ledger and access-log reconciliation before roster lock. Unresolved identity, possible duplication, unlinked aliases, missing access history, inability to prove a clean history or any ledger/log disagreement makes the person ineligible. A declaration alone is insufficient.

### 3.3 First-cycle lock chronology — PASS

Design section 5.3 closes and hashes D/B before review, creates randomized and topic-stripped X/Y copies under one frozen rule, withholds mapping from Q reviewers, and requires each Q to lock all semantic parity and internal-quality items before a forced topic-stripped guess, confidence and reasons. All records are timestamped and hashed before relevance release. Missing locks, contact, cross-review, access or chronology failure rejects the package. R1 and R2 are two different fresh people used only after complete Q locks and receive neither Q records nor each other's records.

### 3.4 Pair retirement and restart — PASS

Design section 5.4 and operating section 3.4 retire both Q reviewers after either one accesses candidate bytes and a rejection, amendment, candidate change, access failure, missing/corrupt lock, withdrawal or attempted replacement occurs. Every allowed next attempt requires a new versioned package, new randomized and stripped copies, a new mapping and chronology, two new positively resolved clean natural people, new locks and a new package verdict. Old judgments, guesses, reasons and partial records are prohibited from reuse; retired reviewers cannot see or compare later candidates. Stable D, B or stripped content is explicitly not an exception. Zero-access correction is allowed only when logs positively prove neither Q received candidate bytes.

### 3.5 Staffing and resource consequences — PASS

Operating sections 3 through 8 preserve the first untouched A/B/D minimum of at least 18 distinct natural people, freeze `J_Q_restart_max` before access and prequalify two additional fresh people for each permitted restart. Identity review, availability, absence, compensation, active/wait/calendar time, allowed AI support, human verification, tokens and cash are represented for every pair. V4-G2, G4 and G6 enforce the same lifecycle requirements. Exhausted, unavailable or unbudgeted fresh-pair coverage yields `STOP/DEFER`, never reviewer reuse.

No claim is made that the required people or lifecycle coverage are actually available.

## 4. F-02 — endpoint and operating-vector propagation

**Verdict: PASS.**

### 4.1 Preserved endpoint vector — PASS

Measurement v0.4 sections 2 through 5 keep `F_R` and `F_H` disjoint, reserves set-specific and `N_union` reporting/workload-only. All A/B/D instances use fresh sessions; instances and repeats never increase family N; no result can move a family or reserve across sets.

The future frozen calculation must separately record membership, valid count, the 20-family floor and endpoint-specific power for all eight required rows:

1. D−A acceptable effect;
2. D−B acceptable effect;
3. D−A nonacceptable-risk harm;
4. D−B nonacceptable-risk harm;
5. D−A harm composite;
6. D−B harm composite;
7. relevant-stratum condition guessing;
8. harm-stratum condition guessing.

It must output all eight requirements, then separate `N_relevant_required` and `N_harm_required`, and jointly plan on `(N_relevant, N_harm)`. A surplus in one set cannot cover the other.

### 4.2 Four human-resource buckets — PASS

Measurement section 3.4 and operating section 4 require role-by-role rows for `F_R`, `F_H`, `F_R_reserve` and `F_H_reserve`, separately covering active time, waiting time, conservative calendar occupancy/deadline, primary compensation, replacement compensation/cash, allowed AI support and human verification. Every inapplicable cell is an authenticated zero. Direct family work cannot move to fixed overhead. Missing, blank or excessive buckets stop the gate.

### 4.3 Fixed overhead allocation — PASS

Operating sections 4.1 through 4.4 keep protocol/CONTROL, package-level B/Q review, independent review and administration roles visible in fixed rows. Q-restart identity, packaging, both fresh reviewers, verification, time and compensation appear in explicit `Q_restart_fixed` subrows rather than generic contingency. One nonnegative, sum-to-one, result-independent allocation vector, its factual basis and rounding rule freeze before authoring. Both the original fixed rows and attributed bucket burdens remain visible; results cannot change the vector; direct work cannot be relabeled fixed. Every attributed family/reserve bucket must pass before totals.

### 4.4 Calls, tokens and cash — PASS

Operating sections 5 through 8 retain executor, retry, reserve, support-call and token terms by all four buckets or an explicit fixed row, including every permitted Q restart. Human cash retains primary and replacement terms in every bucket plus fixed rows. Section 6 requires every fixed row, including Q-restart rows, to receive the frozen allocation for bucket approval while remaining visible. Totals form only after the source rows and four attributed bucket tests pass. V4-G2 and V4-G6 reject scalar-only human time or cash approval. Failure to fit either family set, either reserve or fixed overhead yields `STOP/DEFER` or a newly reviewed narrower question, not fewer clusters or weaker guardrails.

No endpoint count, power output, price, staffing value, time or cash feasibility is inferred.

## 5. F-03 — current README and v0.1 byte identity

**Verdict: PASS.**

Package index v0.4 identifies v0.4 as the current design-only proposal awaiting fresh review, maps all six v0.4 documents, requires exact same-basename sidecars, identifies README as the frozen historical v0.1 entry point and records its authenticated current hash. Review brief v0.4 directly includes README and all four v0.1 design Markdown files and their sidecars. The five-file table in section 1.1 records complete expected and independently calculated hashes; every pair matches at the supplied HEAD.

The current hashes of README, v0.1, v0.2 and v0.3 equal their authenticated packet records, while v0.4 exists as new versioned files. The index claims neither review success nor a later gate.

## 6. Preserved correction verdicts

| Correction | Verdict | Evidence-backed assessment |
|---|---|---|
| Single authenticated representation | **PASS** | Design section 3 requires exactly one active, versioned, owned, hashed and approved `selected_representation_ref`; fallback has identical status; empty, plural, inline, asymmetric or changed references stop or invalidate dependent work. |
| Estimand and worthwhile-effect alignment | **PASS** | Measurement sections 3 through 5 retain equal-family weighting, `δ ≤ Δ` nulls, lower-bound pass only above the same `Δ`, planning alternatives above `Δ`, and no pilot-driven reduction of margins or counts. |
| Family/session noninflation | **PASS** | Measurement sections 2.3 and 5 use complete task families as inferential/resampling units; instances and repeats do not increase N; McNemar and instance discordance remain diagnostic. |
| Transfer rather than near-copy | **PASS** | Design section 4 freezes the latent pattern first, separates curator and task/oracle author, rejects token overlap, one-to-one skeleton, chronology and non-self-containment, requires four changed axes, two new decisive relations and one unusable source relation, uses both leakage scopes and keeps oracle meaning outside repository/executor-visible environments. |
| Limited safety unblinding | **PASS** | Design section 6 keeps primary adjudicators blind; only the safety monitor opens one label after a blind critical lock; any confirmed critical stops the whole run regardless of label, with no favorable subset or automatic non-D restart. |
| Redaction and adjudication blinding | **PASS** | Design section 7 and measurement section 6.2 require independent redaction/QC, severity-before-guess, mapping after all locks, and noncompensatory failure for explicit cue, missing guess, asymmetric or meaning-damaging redaction, or either failed family stratum. |
| Conditions and system boundary | **PASS** | A/D is pilot-only; B remains mandatory for content confirmation; C is optional and noncompensatory; four-condition execution is closed by default. S0/E0 separation, authenticated interface without winner narrative, external oracle, worktree limitation, rollback, noncombination and the restricted claim ladder remain explicit. |

## 7. Required condition and system verdicts

| Area | Verdict |
|---|---|
| Lifetime candidate exposure | **PASS** |
| Natural-person identity resolution | **PASS** |
| First-cycle Q lock chronology | **PASS** |
| Cross-version pair retirement/restart | **PASS** |
| 13-person A/D minimum | **PASS as a design minimum; feasibility unknown** |
| 18-person first-cycle A/B/D minimum | **PASS as a design minimum; feasibility unknown** |
| `J_Q_restart_max` and two-person coverage | **PASS as a freeze/stop contract; value unknown** |
| Compensation, active/wait/calendar time and absence | **PASS as a four-bucket contract** |
| All-AI-call and human-verification coverage | **PASS** |
| Eight endpoint counts and 20-family floors | **PASS as a future calculation contract** |
| Disjoint sets, reserves and vector joint power | **PASS as a future calculation contract; no power result exists** |
| Four-bucket human time and cash | **PASS** |
| Fixed-overhead visibility and allocation | **PASS** |
| Relevant/harm/reserve call, token and cash propagation | **PASS** |
| A/D | **PASS, pilot only; no effect pass** |
| B | **PASS as mandatory for content confirmation, subject to future quality/relevance gates** |
| C | **PASS, optional diagnostic only** |
| Four-condition execution | **PASS as closed by default; separate reviewed gate required** |
| S0/E0 separation and authenticated interface | **PASS** |
| Hidden-oracle boundary and worktree limitation | **PASS** |
| Rollback and noncombination of contaminated results | **PASS** |
| Claim ceiling | **PASS** |

## 8. Unresolved feasibility risks

These remain unknown and are not defects because the design closes them with explicit future `STOP/DEFER` rules:

- approval of exactly one authenticated representation artifact;
- positive identity resolution, recruitment, independence, compensation and calendar availability of the first-cycle people, every fresh Q pair and other replacements;
- practical maintenance of the lifetime exposure and access records;
- the eight endpoint-specific required counts and the `(N_relevant, N_harm)` joint-power result;
- fit of both family sets, both reserves, attributed fixed overhead, calls, tokens, human time and cash within an approvable envelope;
- authoring a useful, quality-matched, irrelevant and cue-free B;
- agreement of future leakage, quality and relevance reviewers;
- meaning-preserving redaction that passes both blinding strata;
- future model, price, service-tier, token, time, calendar and cash values.

No feasibility fact, effect, safety result, economic value or model-transfer claim is inferred.

## 9. Rereview scope and next maximum packet

No corrective revision or v0.4 design rereview is required for V4-G0. Any change to the lifetime exposure/identity contract, Q restart rule, family vector, four-bucket propagation, fixed allocation, preserved causal/safety controls or claim ceiling requires a new version, hashes and fresh review of the affected contract and dependencies.

For CONTROL design-integration review, the recommended maximum packet is the 29 authenticated Markdown inputs and available sidecars listed in section 1, plus this review and its exact sidecar. No S0 result, fixture, oracle, prompt, schema, code, simulation, execution output, web source or other repository material is needed. Any future V4-G1, G2, G4 or G6 review must use a separately bounded result-blind packet containing only the exact newly frozen artifacts required by that gate.

## 10. Final verdict

**PASS-FOR-CONTROL-INTEGRATION-ONLY**

> E0 v0.4 may be sent to CONTROL for design-integration review only.

This verdict does not approve a representation, identity record, person, budget, authoring, implementation, pilot, confirmation, result, operational safety, economic value, central system, Project Brain integration or model-to-model transfer, and it opens no later gate.
