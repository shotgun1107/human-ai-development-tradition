# URC-0.8 independent hostile public-only review

- Review type: `fresh independent hostile public-only read-only review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `255fe7bbe1db404000611f560d4b9ab7696d24f5`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.8 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only
- Final verdict: **REVISE-AND-REVIEW**

No schema, bank, question, answer, fixture, oracle, code, generator, comparator, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch creation, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** The official worktree was clean at the required branch and commit. All ten allowlisted Markdown inputs were read in full. Nine same-basename sidecars, formed by replacing `.md` with `.sha256`, matched before substantive reliance. `AGENTS.md` has no sidecar; its computed hash is recorded as a governing-input fact.

| Exact input | Verified SHA-256 | Authentication |
|---|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | no sidecar; governing instruction only |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matching sidecar |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/review-response-v0.2.md` | `ee1d62662f73ac14c814ac287b23c42f92505b2c9f4db9b0c055bf3d494b75a0` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.7/urc-v0.7-independent-review-v0.1.md` | `2ed742dd90d8219f0c926a835e159b747f2fd899b8966d389503bfbba53fd276` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/universal-response-contract-v0.8-candidate.md` | `ee9f9dd02030a79b7f28a475f18402906c0425de97eab677d50316d41676677c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/review-response-v0.3.md` | `b2ab90bb3862fa9b74bf656c87d92cc809b2dfa5990a555731b6c52175b6adcf` | matching sidecar |

No repository history beyond the exact baseline checks, E0 work product, other S0 version, sealed/private/oracle path, fixture, problem, answer, schema, runner, code, output, or web source was read or searched. Worktree separation was treated as edit isolation only.

## 2. Rubric

- **PASS**: the proposal text uniquely closes the finding in scope without leaving a result-affecting author, builder, comparator, custodian, or analyst choice. This never means implemented or validated.
- **FAIL**: a contradiction, incomplete branch, non-unique mapping, unsatisfiable requirement, missing authorized transfer, or executable counterexample remains.
- **UNCLEAR**: the public text admits materially different implementations and the allowlisted inputs do not select one.

New-finding severity:

- **blocking**: prevents CONTROL integration because the effective contract, required adjudication result, or mandatory P0/P1 artifact is not uniquely satisfiable.
- **major**: materially breaks custody, blinding, reproducibility, or feasibility.
- **minor**: localized precision defect requiring correction before freeze.

## 3. Exact-hash composition audit

### 3.1 Plan composition

**PASS at section-routing level.** Plan v0.5 names the exact v0.4 hash and classifies every v0.4 section or subsection as inherited or replaced. Its runtime-token substitution is narrow and expressly leaves thresholds, formulas, grids, N candidates, schedules, and ceilings unchanged.

### 3.2 Contract composition

**FAIL.** Candidate v0.8 does not provide a complete, contradiction-free section routing:

- it expressly inherits v0.7 sections 3, 4.1-4.2, 9, and 10, and expressly replaces 4.3, 5.1-5.3, 6, 7, 8, and only the “claim text” in section 11;
- it does not classify v0.7 sections 1 or 2;
- it does not say whether the non-claim admissibility and rollback text in v0.7 section 11 is inherited, replaced, or merely summarized; and
- it says the section-11 claim text is replaced by new sections 3-8 even though the successor claim ceiling is in new section 9.

The general sentence “effective contract is the predecessor composed with the replacements” supports retention of unspecified text, while the enumerated inheritance list supports exclusion. The single conflict rule cannot resolve an omission.

**Executable counterexample:** Composer X retains v0.7 section 11 except its final claim paragraph and uses v0.8 section 9 for the new claim. Composer Y includes only the expressly inherited sections and therefore drops the non-claim v0.7 section-11 admission/rollback clauses. Both follow a literal part of v0.8 section 1, but their effective contracts have different admission and rollback requirements. A third literal composer replaces the old claim with sections 3-8 and never installs section 9 as its replacement. Their effective-document hashes differ before any bank exists.

## 4. Every v0.7 FAIL and new finding

Repeated predecessor IDs remain separate even where one counterexample defeats several.

| Finding | Decision | v0.8 evidence and executable counterexample when failing |
|---|---|---|
| B-02 | **PASS** | Candidate v0.8 §§5-6 supplies T/F/U atoms, complete AND/OR folds, exact branch dependencies, and decisive-T/F/U consequences. A true C4 dependent-missing branch survives unavailable basis; a true C6 wrong-responsibility branch does too. |
| B-03 | **FAIL** | Canonical-key equality is biconditional, but local cause-ID sorting and C4 source scope remain non-unique. In the sort trace `R2` versus `R10`, natural-numeric and canonical-byte lexicographic order produce opposite local IDs because no inherited scalar comparator is defined. In the C4 trace below, the table admits two source sets. |
| M-04 | **FAIL** | The role matrix and ledger still lack a bijection. Step 11 delivers the package to scanner 2, the leakage vault, and the condition-map custodian; step 29 gives the dispatcher only a schedule/routing map, yet step 30 requires the dispatcher to possess the package. No row transfers calibrated constants or the public formula manifest to the analysis role. Obtaining either off-ledger invalidates the bank; omitting either prevents execution. |
| N-B03 | **FAIL** | Authors can no longer merge/split equal keys, but the undefined key-sorting comparator permits different local cause IDs and therefore different expected-table bytes for identical typed facts. The `R2`/`R10` trace is executable without an author cause field. |
| N-B04 | **FAIL** | The normal-form set representation is an improvement, but its mandatory exhaustive catalog is internally contradictory: `4*10*3*3*5*4*128` equals `921,600`, not `276,480`. A generator enumerating the written product violates the declared bound; one enforcing 276,480 must omit 645,120 product rows. P0 requires both complete rows and the bound, so no artifact can satisfy both. |
| N-M01 | **PASS** | Response-, answer-, field-, and code-level consequences are now distinct. A field-local U does not hide a different T code; a schema-valid U is a comparator defect rather than a score. |
| N-M04 | **FAIL** | Registrar/content/map roles are separated and the two scans and run-log producer are repaired, but package-to-dispatch and constants/formulas-to-analysis transfers are unlisted. The exact ledger also names `adjudication-label vault` at step 8 and a different `agreed-label vault` as producer at step 21 without a linking row. |
| V7-B01 | **FAIL** | `wrong_direct` and `stronger_sources` now return all unequal coordinates, and key equality is deterministic, but `cause_id` remains order-dependent on an undefined “inherited canonical scalar order.” Different cause IDs change signed expected-table bytes and P1 equality. The C4 source-domain mismatch independently changes consumption. |
| V7-B02 | **PASS** | The strong three-valued tables and exact branch dependencies decide true-or-unknown, false-and-unknown, and unresolved cases for every listed branch. A U code consumes nothing and cannot suppress a T sibling code. |
| V7-M01 | **FAIL** | Content-blind registrar, scan comparison, transport recorder, and catalog roles are present, but the package and analysis-input traces above remain impossible under the positive allowlists. The asserted zero-unmatched-edge checker would reject the written matrix/ledger. |
| V7-M02 | **FAIL** | The coefficient/stratum map contains the necessary P2 pair weights, P3 coefficients, and P4 pool/stratum/burden roles. However, the analysis role's positive inputs omit the frozen public formula manifest, and no ledger row delivers the selected calibrated constants. With the allowlist enforced it cannot compute; reading them informally violates the plan. |
| V7-M03 | **FAIL** | Repeated metadata maxima and two distinct freeze artifacts are written, but the abstract-catalog row bound is arithmetically false, the eight availability-mask axes are never named or ordered, and the absolute cause bound omits dynamic extra-affected causes. Independent generators therefore lack one exact required catalog. |
| V7-m01 | **PASS** | `target_kind`, `target_record_id`, the supplied-record constraint, and the target-to-operation relation prevent a non-record target from entering `affected_record_ids`. Missing or unsupported mappings reject before satisfiability. |

### 4.1 C4 source trace used above

Use one applicable closure with dependent record `D1`, `operation_dependency=present`, and target-record value `T1`. Let the accepted affected set be `{D1,T1}`. Submit an empty, format-valid affected array and the correct direct-permission coordinates.

- The closed C4 hazard branch is true because dependent `D1` is missing.
- The operation/direct branch is false.
- Candidate §6 describes the true branch as “dependent record missing.”
- Its source cell says “every missing affected-record cause,” while §4 creates a key for each missing accepted affected record.

A branch-local implementation sources `{affected:D1}` and leaves `affected:T1` for M4. A literal all-missing implementation sources `{affected:D1, affected:T1}` and consumes both under C4. The text does not choose between “dependent records that made this branch true” and “all missing accepted affected records.” Critical sources, later M4, residuals, and signed expected tables differ.

## 5. New v0.8 findings

### V8-B01 — The exact-hash contract composition is incomplete

- Severity: **blocking**
- Evidence: section 3.2 of this review.
- Consequence: the effective normative document is not unique before implementation.
- Minimum correction: publish a total predecessor-section/subsection map; name the exact successor replacement for each replaced range; explicitly classify v0.7 sections 1, 2, and all of 11; and state one effective-document hash construction.

### V8-B02 — Cause equality is biconditional, but cause ordering is not canonical

- Severity: **blocking**
- Evidence: v0.8 derives local IDs from one-based sorted positions under an “inherited canonical scalar order.” The inherited serialization section fixes bytes and member order but does not define a comparator for JSON-array keys or even resolve lexical versus natural ordering of ASCII IDs.
- Executable counterexample: keys `['affected','R2']` and `['affected','R10']` sort as R10,R2 by canonical-byte lexicography and R2,R10 by natural numeric ordering. Both keys are canonical and distinct; their one-based IDs reverse.
- Consequence: expected catalogs and comparator tables can differ byte-for-byte without any difference in typed metadata.
- Minimum correction: freeze an explicit total comparison over canonical key bytes, including prefix, escape, and ASCII-ID cases, or use the canonical key bytes directly and remove ordinal IDs.

### V8-B03 — C4's true branch and declared source domain do not coincide

- Severity: **blocking**
- Evidence and executable trace: section 4.1.
- Consequence: one true formula has two defensible critical source sets and two downstream M4/consumption results.
- Minimum correction: state separately whether the missing branch sources only missing dependent IDs or every missing accepted affected ID, add the target-record case to the hazard formula if intended, and freeze both positive and negative mutations.

### V8-B04 — The mandatory catalog bound is arithmetically impossible

- Severity: **blocking**
- Evidence: the displayed seven-factor product is 921,600, while the declared result is 276,480. P0 separately requires complete abstract rows and the declared bound.
- Executable counterexample: nested loops over cardinalities 4,10,3,3,5,4,128 emit 921,600 tuples before any invariant rejection; retaining rejected rows is mandatory, so filtering cannot justify the smaller number.
- Consequence: no pre-bank abstract catalog can satisfy all written requirements, and the stated benchmark undercounts the required product by more than threefold.
- Minimum correction: correct the factors or the declared count, specify whether duplicates are quotiented before or after mandatory rejection rows, and rereview the resulting resource envelope.

### V8-M01 — The cause and availability catalog bounds are incomplete

- Severity: **major**
- Evidence:
  - the claimed absolute 24-cause maximum counts four dynamic invalid-citation causes but not up to four dynamic affected causes created by submitted extra affected IDs;
  - inherited `A:<id>` ranges over the union of submitted and accepted affected IDs, and the new key constructor assigns every such ID an affected cause; and
  - `7*2^8=1,792` is arithmetically correct, but the eight availability axes and their order are not enumerated.
- Executable counterexample: instantiate all 20 metadata-derived cause slots, submit four disallowed non-prohibited citations, and submit four extra affected record IDs disjoint from the four accepted IDs. The answer has 28 distinct canonical causes, not 24. Two availability generators can also choose different eight-bit axis lists while meeting the stated row count.
- Consequence: P1 completeness, row hashes, and worst-case storage/preflight are not fixed.
- Minimum correction: include dynamic affected causes in the absolute bound and catalogs; enumerate every availability bit and canonical bit order.

### V8-M02 — The matrix/ledger still has unmatched operational edges

- Severity: **major**
- Evidence:
  - no ledger row transfers an assigned package to the dispatcher/transport recorder before step 30;
  - no row transfers calibrated constants or the public formula manifest to the analysis role;
  - step 8's `adjudication-label vault` and step 21's `agreed-label vault` are not linked as the same signed store; and
  - the matrix promises a positive-input/ledger bijection, so these cannot be repaired by ambient public access or an informal store alias.
- Executable counterexample: execute rows 1-29 literally. At row 30 the dispatcher has a routing map but no package. If a hidden copy is supplied, the unlisted-transfer stop fires; otherwise no request can be sent. Later, the analysis role can possess derived/timing tables and a coefficient map but no authorized selected constants or formula manifest.
- Consequence: the bank cannot reach execution or frozen analysis under its own custody rules.
- Minimum correction: add exact producer-artifact-recipient rows and store identities for these edges, then publish the promised matrix/ledger bijection table rather than only requiring a future checker.

## 6. Focused hostile checks

| Required attack | Result | Assessment |
|---|---|---|
| canonical cause-key biconditionality | **PASS** | Equal canonical key bytes are iff-equal causes; authored cause IDs are forbidden. |
| canonical cause-key sorting | **FAIL** | No exact total comparator is defined; see V8-B02. |
| multi-coordinate `wrong_direct` | **PASS** | Returns all available unequal basis/responsibility coordinates and never a minimal explanation. |
| multi-coordinate `stronger_sources` | **PASS AS WRITTEN DESIGN** | Returns all unequal available coordinates whenever the frozen strength comparison is strictly greater. This is deterministic, though unvalidated as hazard semantics. |
| complete T/F/U algebra | **PASS** | Negation, AND, OR, finite any/all, guards, decisive T/F, U, and schema-valid-U failure are stated. |
| exact C1-C7 branch dependencies | **PASS EXCEPT C4 SOURCE** | Formula truth is complete; C4 source scope fails under target-record composition. |
| finite overlap catalog | **FAIL** | The product bound is false and the availability axes/cause maximum are incomplete. |
| pre-bank versus post-label freeze | **PASS** | Generator/spec/abstract catalogs freeze pre-bank; one non-discretionary instance projection freezes post-label. |
| target-record typing | **PASS** | Record/non-record forms and applicable-operation dependency are mechanically constrained. |
| registrar/content/map separation | **PASS** | The three authorities are separated and content-blind registrar claims are narrow. |
| both scans | **PASS** | Scan 1 and scan 2 have distinct inputs, outputs, and a comparison custodian. |
| run-log/timestamp producer | **PASS** | Transport recorder owns request-send through durable-final-byte endpoints and signs one log. |
| P1 generator/reviewer custody | **FAIL AT STORE/EDGE LEVEL** | Roles and tables exist, but the agreed-label vault name changes without a transfer/link. |
| blinded P2-P4 coefficient/stratum map | **PASS FOR COLUMNS; FAIL FOR AUTHORIZED EXECUTION** | Coefficients and strata suffice, but formula/constants delivery is absent. |
| release-after-analysis/no reanalysis | **PASS** | Map release follows authenticated analysis hash; final custodian may only join under the frozen table. |
| catalog workflow in ceilings | **PASS IN SCOPE; FAIL QUANTITATIVELY** | Time/storage/reviewer/signing work is expressly included, but the benchmark uses a false abstract-row bound. |
| D-favoring runner vocabulary | **PASS** | A-D names, target-candidate narrative, relation semantics, and condition map remain outside executor packages; neutral codes are required. |
| answer leakage | **PASS AS LIMITED PROPOSAL** | Typed generation, two package scans, and two semantic reviewers remain. Scanners still make only the narrow enumerated syntax/provenance claim. |
| A-D source facts | **PASS AS UNIMPLEMENTED REQUIREMENT** | Canonical facts, question order, and equality manifest are fixed; only intended representation may differ. |
| A-D authority/model/time/opportunity | **PASS AS UNIMPLEMENTED REQUIREMENT** | Exact revision, reasoning, tier, region, authority, tools, turns, retry, limits, and balanced schedule remain common. |
| A-D scoring opportunity | **PASS AS UNIMPLEMENTED REQUIREMENT** | Same grammar opportunities and anonymous comparator rules apply across A-D; no condition-specific threshold is authorized. |
| post-result threshold change | **PASS** | Any change creates a new reviewed version/untouched bank; final join cannot recompute or tune. |
| claim beyond synthetic logic | **PASS** | The stated future claim is bounded to one frozen synthetic public experiment and excludes S0/system/product claims. |

## 7. Non-regression of every v0.7 PASS

| v0.7 PASS | Decision | Evidence in effective v0.8 text |
|---|---|---|
| B-01 | **PASS** | All 24 rows and direct operation only for `authorized; none` are inherited. |
| B-04 | **PASS** | Pre-bank seed excludes bank hash; post-bank seed uses remain limited. |
| B-05 | **PASS** | Valid P3 null grid, latent mappings, fit/audit separation, and grid-limited claims are inherited. |
| B-06 | **PASS** | Typed runner prose and narrow mechanical-leakage claim are inherited. |
| M-01 | **PASS AS ARITHMETIC; FEASIBILITY UNVERIFIED** | Revised rows sum `50+40+50+45+55=240`; direct non-nested simulation and benchmark stop remain. |
| M-02 | **PASS** | P2 balance, every-seed P3 balance, and monotonic elapsed definition are unchanged. |
| M-03 | **PASS** | Raw/response/answer/field P3-P4 consequences are inherited exactly. |
| m-01 | **PASS** | NFC rejection and all seven prohibited line scalars remain. |
| N-B01 | **PASS** | All 64 vectors map to one of 24 rows or H/G rejection; typed owners remain required. |
| N-B02 | **PASS** | Citation hitting-set, affected, answer, packet, and raw-byte satisfiability remain; target typing is now explicit. |
| N-B05 | **PASS** | C4 applicability is typed and C6 covers identified human/Brain reservations symmetrically. |
| N-B06 | **PASS AS UNEXECUTED DESIGN** | Every stated P3 null marginal remains within `[0.45,0.95]`. |
| N-M02 | **PASS** | P3 rotation construction still guarantees per-position/per-wave imbalance at most one for every authorized N and seed. |
| N-M03 | **PASS AS ARITHMETIC** | The nonoverlapping aggregate remains exactly 240 hours with no double-booking. |
| N-M05 | **PASS AS UNEXECUTED DESIGN** | P2/P3 random variables, mappings, dependence grids, and P4 elapsed/pooling/bootstrap definitions remain complete. |
| N-m01 | **PASS** | Lone/reversed surrogate rejection, valid-pair treatment, canonical serialization, and complete runner member order are inherited. |

Additional recorded non-regressions:

- 960-call and 53,760,000-input/3,194,880-output visible-token arithmetic at N=720 remains exact.
- Direct statistics, no inner bootstrap, fit/audit separation, benchmark stops, immutable revision, drift invalidation, concurrency three, first-output only, and no automatic retry remain.
- Rollback, untouched-bank, sealed/oracle separation, the S0-E0 boundary, and noncompensatory P0-P4 remain stated.
- None of these textual passes is an implementation, feasibility result, or validation result.

## 8. Overall rubric

| Review dimension | Result |
|---|---|
| Input boundary and SHA-256 integrity | **PASS** |
| Exact-hash plan composition | **PASS** |
| Exact-hash contract composition | **FAIL** |
| 24 rows / 64 predicate vectors | **PASS; NO REGRESSION** |
| Owner/direct-operation rules | **PASS; NO REGRESSION** |
| Cardinality and satisfiability | **PASS; NO REGRESSION** |
| Target/affected-record typing | **PASS** |
| Canonical cause equivalence | **PASS** |
| Canonical cause ordering | **FAIL** |
| Multi-coordinate selectors | **PASS** |
| T/F/U formula truth | **PASS** |
| Exact C1-C7 source sets | **FAIL AT C4** |
| Consumption equations | **PASS IF SOURCES ARE FIXED** |
| Finite catalog satisfiability and row arithmetic | **FAIL** |
| Pre-bank/post-label freeze separation | **PASS** |
| Response/answer/field consequences | **PASS; NO REGRESSION** |
| P2/P3 mappings and schedules | **PASS AS UNEXECUTED DESIGN** |
| Valid P3 null grid | **PASS AS UNEXECUTED DESIGN** |
| Matrix/ledger bijection | **FAIL** |
| Registrar/content/map separation | **PASS** |
| Scan and transport-log custody | **PASS** |
| P1 generator/reviewer custody | **FAIL AT ONE STORE EDGE** |
| Blinded coefficient/stratum-map columns | **PASS** |
| Blinded analysis authorized inputs | **FAIL** |
| Release-after-analysis/no reanalysis | **PASS** |
| 240-hour arithmetic | **PASS; FEASIBILITY UNVERIFIED** |
| Catalog resource preflight | **FAIL FROM WRONG BOUND** |
| Exact revision/no retry | **PASS; NO REGRESSION** |
| Leakage claim | **PASS AT ITS NARROW STATED LEVEL** |
| Rollback/sealed/S0-E0 boundaries | **PASS; NO REGRESSION** |
| Noncompensatory P0-P4 | **PASS; NO REGRESSION** |
| Claim ceiling | **PASS; NO REGRESSION** |
| CONTROL-integration suitability | **FAIL** |

## 9. Facts, inferences, proposals, and unverified requirements

### 9.1 Facts established by this review

- The branch, commit, origin, clean baseline, and ten input hashes are those in section 1; all nine available sidecars matched.
- The v0.8 contract composition leaves predecessor ranges unclassified and points the section-11 claim replacement to the wrong successor range.
- The displayed abstract-catalog multiplication equals 921,600, not 276,480.
- The written matrix/ledger has no package transfer to the dispatcher and no calibrated-constant/formula transfer to analysis.
- No implementation or empirical result was available or created.

### 9.2 Review inferences

- Composition, cause-order, C4-source, and catalog contradictions permit different mandatory artifacts or make P0 impossible, so CONTROL integration is not suitable.
- The custody gaps are not harmless implementation details because the plan itself makes any unlisted transfer or positive-input mismatch bank-invalidating.
- The corrected T/F/U algebra, target typing, and blinded coefficient columns are genuine proposal-text improvements but cannot compensate for a failing noncompensatory gate.

### 9.3 Correction proposals

- The minimum correction directions in section 5 are proposals, not approved designs.
- A successor can preserve the authenticated PASS clauses while changing only composition routing, key order, C4 source scope, catalog bounds/axes, and the unmatched custody inputs.

### 9.4 Unverified future requirements

- Two implementations still must reproduce serializers, scanners, generators, comparators, schedules, stochastic simulations, and burden calculations.
- Labels, package scans, semantic reviews, reason judgments, catalog generation, ACL enforcement, and P0-P4 are unperformed.
- Benchmark, calibration, power, cost preflight, exact revision availability, bank feasibility, and executor behavior remain unknown and unauthorized.

## 10. Maximum allowed claim

The maximum defensible claim is:

> At commit `255fe7bbe1db404000611f560d4b9ab7696d24f5`, the authenticated URC-0.8 package is an unimplemented public redesign proposal. It textually improves three-valued evaluation, multi-coordinate selectors, target-record typing, repeated-component maxima, split custody roles, and blinded coefficient columns while preserving numerous authenticated v0.7 proposal-text controls. It does not yet define one complete effective contract, one canonical cause-ID order, one exact C4 source result, a satisfiable exhaustive catalog bound, or a complete matrix/ledger path to execution and blinded analysis.

No claim is authorized for CONTROL integration, an executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 11. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions fit the tightened metadata and target rules without distortion.
- Whether independent labelers, semantic reviewers, judges, generators, and map builders can agree exactly.
- Whether the corrected catalog size and 200 comparator runs fit 240 human hours, storage, calendar, compute, and USD ceilings.
- Whether required ACL stores, write-only delivery, immutable model fingerprint, and durable monotonic transport timestamps are available.
- Whether any calibrated conclusion holds outside the stated latent-normal grids; no such claim is permitted.

## 12. Minimum rereview scope

A fresh successor review must authenticate this review and unchanged governing inputs, then read the successor candidate, plan, and author response in full. It must re-evaluate:

1. a total exact-hash section/subsection composition map and effective-document construction;
2. a byte-exact total order for canonical cause keys;
3. C4 target/dependent source scope and downstream M4 consumption;
4. corrected abstract/availability/dynamic-cause bounds and arithmetic;
5. one matrix/ledger bijection including package delivery, exact label-vault identity, formula manifest, calibrated constants, every signature, and every store grant;
6. blinded P2-P4 sufficiency and release-after-analysis without post-map reanalysis; and
7. non-regression of every PASS in sections 6-8.

No bank, labels, implementation, simulation, model call, executor output, sealed input, or result is required or permitted for that rereview.

## 13. Exact next-gate recommendation

Do not open CONTROL integration, public bank authoring, schema/runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7/v0.8 artifacts and this review. The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.9 REDESIGN OPEN`

The successor must correct every blocking and major finding above and receive a fresh public-only independent read-only review.

## 14. Final verdict

**REVISE-AND-REVIEW**
