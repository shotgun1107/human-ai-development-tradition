# URC-0.7 independent hostile public-only review

- Review type: `fresh public-only hostile read-only review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\.codex\worktrees\88d0\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Baseline: detached HEAD accepted by the CONTROL correction; source ref/ancestry `codex/s0-question-contract-v06-review`
- Commit: `d2e024a6c95213ccaf54bf996063c267a6d10ae6`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.7 INDEPENDENT REVIEW OPEN`
- Authority: review record and CONTROL-integration suitability only
- Final verdict: **REVISE-AND-REVIEW**

No schema, fixture, question, answer, oracle, code, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch operation, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** The corrected baseline authorizes the already observed detached clean worktree at the expected commit. All ten allowlisted Markdown inputs were read in full. Every available same-basename sidecar matched before the corresponding Markdown was relied upon. `AGENTS.sha256` was absent; `AGENTS.md` was used only as the governing instruction and its computed hash is recorded below.

| Exact input | Verified SHA-256 | Authentication |
|---|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | no sidecar; governing instruction only |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matching sidecar |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.6/universal-response-contract-v0.6-candidate.md` | `2223defe3a01c7bd85feaac32951a01b3f7661901230743598136bf62472fb67` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.6/public-falsification-plan-v0.3.md` | `66e0c07fe7137a322f016f71aac7ee2cee1953129196af1eff1279c967a0434b` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.6/review-response-v0.1.md` | `d177fd893b9a5b8b44848608d839ea778b1e74317029f96f3814945a0d4cfa1b` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.6/urc-v0.6-independent-review-v0.1.md` | `e0c4408f820f1c11da7989998910aac633887524ff649a7296ee652aea96ac81` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/review-response-v0.2.md` | `ee1d62662f73ac14c814ac287b23c42f92505b2c9f4db9b0c055bf3d494b75a0` | matching sidecar |

No repository history, E0 work product, other S0 version or review, sealed/private/oracle material, fixture, problem, answer, schema, runner, code, output, web source, or non-allowlisted file was read or searched. Worktree separation was treated as edit isolation only, never as a secrecy boundary.

## 2. Review rubric

- **PASS**: the authenticated finding is closed at proposal-text level with no remaining counterexample or author/implementer choice in that finding's scope. It does not mean implementation or validation.
- **FAIL**: a concrete contradiction, incomplete branch, non-unique mapping, unauthorized transfer, or non-executable rule remains.
- **UNCLEAR**: the text admits incompatible implementations but the reviewed public inputs cannot determine which is intended.

New-finding severity:

- **blocking**: prevents CONTROL integration because a required semantic or adjudication result is not uniquely determined.
- **major**: materially breaks role isolation, reproducibility, feasibility, or a gate result.
- **minor**: a localized precision defect that must be corrected before freeze.

## 3. Every authenticated v0.6 finding: v0.7 closure decision

The first table preserves every predecessor finding decision carried by the v0.6 review. The second table decides every new blocking, major, and minor finding authored by that review. Repeated IDs are not merged even when they share one v0.7 cause.

### 3.1 Findings carried into the v0.6 review

| Finding | Decision | v0.7 assessment |
|---|---|---|
| B-01 | **PASS** | Candidate §§3.1-3.5 makes A a record-basis fact, exposes `responsibility_route`, requires typed human/Brain owners, and permits direct operation only for `authorized; none`. No reserved vector directly operates. |
| B-02 | **FAIL** | Response/answer/field zeroing and the original required/counterexample alias are repaired, but candidate §7 does not define branch-local truth under partial atom availability. A valid independent critical failure can still be either scored or hidden by an unrelated malformed decision field. See V7-B02. |
| B-03 | **FAIL** | C4 applicability and human/Brain C6 coordinates are typed, but source-cause selection and the claimed normal form remain non-unique and internally inconsistent. See V7-B01. |
| B-04 | **PASS** | Plan §8 retains the immutable pre-bank seed and confines bank-hash seeds to post-bank artifacts. No circular prospective seed remains. |
| B-05 | **PASS** | Plan §§7.2-7.3 and 9.3 state the latent mappings, fit/audit split, valid null probabilities, grid-limited claim, and pre-power calibration without an invalid required point. No calibration result is claimed. |
| B-06 | **PASS** | Candidate §10 preserves closed typed fixed prose, independent semantic review for unavoidable prose, and the truthful narrow syntactic/provenance scanner claim. |
| M-01 | **PASS** | Direct non-nested simulation, the benchmark stop, and resource contingencies remain; the human ledger now sums to 240. Feasibility is still unvalidated, as it should be. |
| M-02 | **PASS** | Plan §§10.2-10.4 gives exact P2 balance, a P3 construction valid for every authorized K and seed, and a monotonic request-to-durable-final-byte elapsed metric. Custody of that metric still fails under M-04/N-M04, not its mathematical definition. |
| M-03 | **PASS** | Candidate §4.2 and plan §§9.2/12.1 uniquely state suite-, response-, answer-, and question-level P3/P4 consequences for every raw class. |
| M-04 | **FAIL** | The expanded matrix still contradicts its positive allowlists and omits required operational transfers. See V7-M01 and V7-M02. |
| m-01 | **PASS** | NFC rejection, non-normalizing validation order, and all seven prohibited line scalars remain exact. |

### 3.2 Blocking, major, and minor findings created by the v0.6 review

| Finding | Decision | v0.7 assessment |
|---|---|---|
| N-B01 | **PASS** | `authorized; human|brain` now means affirmative record basis with direct operation forbidden; all 64 raw predicate vectors yield a unique row or H/G rejection, and every reservation has an identified typed owner. |
| N-B02 | **PASS** | Candidate §4.4 adds a finite 1-4 citation hitting-set witness, nonempty allowed set, affected cardinality at most four, answer/packet byte witnesses, and pre-admission rejection. A separate target-ID type edge remains as V7-m01. |
| N-B03 | **FAIL** | Exact required/counterexample equality now shares an obligation and correlation members are disjoint, but the cause registry still permits non-unique same-family equivalence classes and decision sources are not uniquely selected. See V7-B01. |
| N-B04 | **FAIL** | Masks are correctly demoted, but the proposed realizable-source normal form cannot represent all source sets allowed by the formulas and lacks declared finite group-count bounds. See V7-B01 and V7-M03. |
| N-B05 | **PASS** | Withdrawal applicability is typed; H/G identities are bidirectional; owner presence is required; C6 observes human and Brain symmetrically through `responsibility_route`. |
| N-B06 | **PASS** | The six explicit P3 base pairs and both theta boundaries remain within `[0.45,0.95]`; every stated null point is executable as a probability. |
| N-M01 | **FAIL** | Level-specific Y/schema consequences are exact, but C/M consequences under a true independent disjunct plus an unavailable unrelated disjunct are not. See V7-B02. |
| N-M02 | **PASS** | Full cycles plus an antipodal residual pair or its complement guarantee per-position and per-wave differences at most one for r=2 or r=6; seed choice cannot invalidate balance. |
| N-M03 | **PASS** | The five nonoverlapping task rows sum exactly to 240 hours and double-booking is explicitly forbidden. Practical sufficiency remains unvalidated. |
| N-M04 | **FAIL** | Label/output roles were added, but registrar, scan, timestamp, P1-review, and analysis-map transfers are still missing or unauthorized. See V7-M01 and V7-M02. |
| N-M05 | **PASS** | Plan §§7.2 and 9.3 specify normal components, indices, sharing, independence, probit thresholds, midpoint/delta mapping, and valid marginals; §12.3 fixes the elapsed interval, pooling, median, ratios, resampling unit, and interval directions. |
| N-m01 | **PASS** | Candidate §9 rejects unpaired/reversed surrogate escapes, treats a valid pair as one scalar, and enumerates every runner-object member order. |

## 4. New v0.7 findings

### V7-B01 — Decision-source and cause-equivalence rules are not a unique normal form

- Severity: **blocking**
- Failed claims: exact root-cause selection, complete realizable overlap normal form, and author-independent consumption.
- Evidence:
  - Candidate §6 says `wrong_direct` returns whichever false basis/responsibility causes are “necessary” to explain a direct-permission difference, but gives no unique counterfactual rule when both coordinates are wrong.
  - With truth `barred; human` and submission `authorized; none`, both `D-basis` and `D-responsibility` are false. Correcting either coordinate alone removes direct permission. A comparator may therefore return basis, responsibility, or both from `wrong_direct`.
  - Candidate §7 makes C6 source `wrong_responsibility` plus `wrong_direct`; C2/C3/C5 use the plural “decision causes contributing to stronger.” Candidate §8.2 nevertheless restricts each `B_i` to empty or **one** decision cause. The permitted formula source and the claimed normal form contradict each other.
  - Candidate §5.3 makes identical sets share a cause and different submitted fields not share one, but does not state the converse within one field family. Distinct disjoint required groups, correlation groups, counterexample groups, or prohibited records are not expressly forbidden from sharing one author-entered `cause_id`/`obligation_id`. Such sharing changes residuals and diagnostics without changing the typed facts.
- Consequence: two conforming label/comparator implementations can produce different critical source sets, earlier consumption, later residuals, and scored-versus-shadowed results. P0/P1 cannot adjudicate which output is correct.
- Minimum correction direction: mechanically derive one cause-equivalence class from typed component keys; make the mapping biconditional and forbid all undeclared many-to-one cause aliases. Define `wrong_direct` and `stronger` source contribution coordinate by coordinate, permit the actual bounded number of decision causes in the normal form, and republish every affected source/prior/residual/emitted/shadowed equation and mutation obligation.

### V7-B02 — Partial-availability Boolean semantics are unspecified

- Severity: **blocking**
- Failed claims: field-local availability preserves valid independent failures, and every C1-C7 branch has one result.
- Evidence: candidate §4.3 says valid independent fields in a schema-invalid answer remain available. Candidate §7, however, defines formulas only “when all required atoms are available” and supplies no branch-local or three-valued evaluation rule.
- Executable counterexample: an applicable C4 closure has a valid affected set that omits a required dependent ID, while `basis_status` is malformed. The missing-affected disjunct is true and its cause is available; the operation-dependency disjunct cannot evaluate. One comparator can apply `true OR unknown = true` and emit C4, while another can mark the entire formula `diagnostic-unknown` because not all atoms are available. The same ambiguity occurs in C6 when responsibility is valid and wrong but basis is unavailable.
- Consequence: an unrelated format defect can hide an independently observable critical hazard, or the same output can receive C versus M/diagnostic treatment across implementations.
- Minimum correction direction: freeze branch-specific dependencies and a complete partial-availability truth algebra for AND/OR/quantifiers, including exact source sets when one disjunct is decisive and another is unavailable. Add all decisive-true, decisive-false, and unresolved mutations for C1-C7.

### V7-M01 — The custody matrix and ledger still contain unauthorized or impossible transfers

- Severity: **major**
- Failed claim: every required custody, comparison, signing, and transfer operation is assigned to a compatible positive allowlist.
- Evidence:
  - The CONTROL registrar allowlist omits canonical bank/prompt contents and representations, yet ledger steps 3-4 make the registrar receive and reproduce the frozen author artifact, and step 7 sends representations to the registrar.
  - The registrar allowlist also omits the condition map, yet step 20 transfers that map to the registrar for step 21.
  - Scanner 2 is allowed only the scanner specification and completed package and denies scanner-1 internals, yet step 8 transfers “packages and scan 1” to scanner 2. Scan 1 has no separate authorized delivery to the registrar even though two-scan agreement is required.
  - Plan §10.4 says the dispatcher records request-send and final-byte receipt timestamps. The dispatcher role only delivers a package and emits a dispatch log; it does not receive the model response. The executor's only output is the raw response, and the transfer ledger contains no producer-to-custodian run-log transfer. The raw custodian is allowed to read “run logs” that no listed role is authorized to produce and send.
  - Plan §6 requires two read-only reviewers to sign expected overlap results, but the role matrix and 21-step ledger assign no such bank/mutation input, output, or transfer to a compatible pair.
- Consequence: following the allowlists literally prevents package approval, timing construction, overlap adjudication, map release, or final decision; repairing the sequence informally would itself invalidate the bank.
- Minimum correction direction: split content-blind registrar intake/routing from registrar bookkeeping or explicitly authorize exact content/hash operations; name producers and recipients for scan 1, run logs, P1 expected results, and the final map; align every matrix cell with one ledger row and remove each denylist conflict.

### V7-M02 — The blinded analysis role lacks the mapping needed to compute P2-P4

- Severity: **major**
- Failed claim: anonymous analysis can freeze P2-P4 statistics before condition-map release.
- Evidence: the analysis role receives an agreed derived table, anonymous timing/byte data, constants, and anonymous packet/cell IDs, while the condition map is withheld until after the analysis hash (steps 18-20). P2 requires observer/variant grouping; P3 requires URC/control and A-D signed coefficients; P4 requires URC/control pooling and the A-D range. No coefficient/stratum map is an allowed input or ledger artifact.
- Consequence: if the cell IDs are truly opaque, the analysis cannot compute the precommitted contrasts. If they encode those identities, the withheld-map and positive-allowlist claims are false. Releasing the map only after the analysis hash cannot repair a missing computation because step 21 forbids reanalysis.
- Minimum correction direction: freeze and transfer a blinded analysis-design map that assigns opaque cells to all required coefficients, pools, and strata without revealing prohibited semantic condition identities; specify who derives, signs, receives, and verifies it, and prove it is sufficient for every P2-P4 statistic before calls.

### V7-M03 — The mandatory overlap catalog has no closed finite size or single freeze point

- Severity: **major**
- Failed claim: every permitted normal-form instance can be frozen, reviewed, and run within a precommitted catalog.
- Evidence: candidate §5.1 bounds members within a correlation/counterexample group but does not bound the number of correlation groups, counterexample groups, prohibited-citation entries, withdrawal closures, or cause-registry entries per question. Candidate §8.2 nevertheless says multiplicity is bounded by §5.1 and requires every active-code/B-sharing/X-tag/unique-slot instance through its cardinality bound. Plan §4 step 2 freezes “overlap catalog, mutations” before bank authoring, while step 8 again freezes “overlap mutations” after labels.
- Consequence: there is no public maximum from which two reviewers can derive the required catalog or preflight its computation and human review, and two freeze points admit incompatible choices about whether bank-specific cases may alter the catalog.
- Minimum correction direction: add explicit per-question maxima for every repeated metadata component and cause class; distinguish a pre-bank generator/specification from post-label generated instances; freeze their hashes and permitted inputs at one unambiguous stage; include their worst-case time/storage/human cost in the benchmark ledger.

### V7-m01 — Operation target and affected-record ID types are not tied

- Severity: **minor**
- Failed claim: affected-ID truth is type-correct as well as cardinality-satisfiable.
- Evidence: candidate §3 names a general target ID, §4 requires `affected_record_ids`, and §5.2 adds the named operation target to the accepted affected set when an applicable closure has `operation_dependency=present`. It never requires the target ID itself to be a supplied record ID or defines a target-to-record mapping.
- Consequence: otherwise consistent metadata can place a non-record target ID into a field whose declared members are record IDs; independent schemas may accept or reject it differently.
- Minimum correction direction: require `target_id` to belong to the affected-record ID universe when it can be emitted, or add a typed `target_record_id` relation and validate it before satisfiability.

## 5. Overall rubric

| Review dimension | Result |
|---|---|
| Input boundary and SHA-256 integrity | **PASS** |
| Record-basis authorization versus responsibility | **PASS** |
| Direct-operation truth consistency | **PASS** |
| Identified human/Brain owner and all basis×responsibility rows | **PASS** |
| Citation/answer/packet cardinality satisfiability | **PASS** |
| Affected-ID cardinality satisfiability | **PASS; target type MINOR FAIL** |
| Cross-component alias/disjointness | **FAIL at cause-equivalence closure** |
| Root-cause source selection and consumption | **FAIL** |
| Realizable source-overlap normal form | **FAIL** |
| Residual/emitted/shadowed determinism | **FAIL** |
| Typed C4 applicability | **PASS** |
| C6 human/Brain coverage | **PASS** |
| Partial-availability C1-C7 consequences | **FAIL** |
| Raw/response/answer/field P3-P4 consequence levels | **PASS** |
| P3 null grid validity | **PASS AS UNEXECUTED DESIGN** |
| P2 stochastic mapping | **PASS AS UNEXECUTED DESIGN** |
| P3 stochastic mapping | **PASS AS UNEXECUTED DESIGN** |
| P2 balance for every authorized N | **PASS** |
| P3 balance for every authorized N and seed | **PASS** |
| 240-hour nonoverlapping ledger arithmetic | **PASS** |
| Monetary/compute/storage feasibility | **UNVALIDATED** |
| Custody/anonymization/comparison/signing/transfer matrix | **FAIL** |
| Blinded P2-P4 analysis executability | **FAIL** |
| P4 elapsed-time metric definition | **PASS** |
| P4 elapsed-time capture custody | **FAIL** |
| Escaped surrogate rejection | **PASS** |
| Complete runner canonical member order | **PASS** |
| Prospective pre-bank seed | **PASS; NO REGRESSION** |
| Fit/audit separation | **PASS; NO REGRESSION** |
| Direct non-nested simulation | **PASS AS UNEXECUTED REQUIREMENT** |
| Benchmark stop | **PASS AS UNEXECUTED REQUIREMENT** |
| Exact revision/model drift stops | **PASS AS UNVALIDATED REQUIREMENTS** |
| Limited mechanical-leakage claim | **PASS; NO REGRESSION** |
| NFC/line rules | **PASS; NO REGRESSION** |
| Rollback and untouched-bank rule | **PASS; NO REGRESSION** |
| Sealed/oracle boundary | **PASS; NO REGRESSION** |
| S0-E0 boundary | **PASS; NO REGRESSION** |
| Noncompensatory P0-P4 | **PASS; NO REGRESSION** |
| Claim ceiling | **PASS; NO REGRESSION** |
| CONTROL-integration suitability | **FAIL** |

## 6. Facts, inferences, proposals, and unverified requirements

### 6.1 Facts established by this review

- The ten public inputs had the exact hashes in section 1; nine available sidecars matched and `AGENTS.md` had no sidecar.
- v0.7 text fixes the prior direct-operation contradiction, invalid shifted-null probability, P3 seed-balance construction, 240-versus-320 arithmetic, explicit stochastic mapping, elapsed metric wording, and surrogate/member-order gaps at proposal-text level.
- The counterexamples in V7-B01/V7-B02 and allowlist/ledger contradictions in V7-M01/V7-M02 arise directly from the authenticated public text.
- No implementation or empirical result was available or created.

### 6.2 Review inferences

- The two blocking source/evaluation defects permit different scores from conforming implementations and therefore prevent CONTROL integration.
- The role and analysis gaps cannot be treated as harmless operational details because plan §§3 and 13 make an unlisted transfer or allowlist breach bank-invalidating.
- The passed arithmetic and written stop gates bound a future attempt; they do not show that the attempt will fit those bounds.

### 6.3 Correction proposals

- The minimum correction directions in section 4 are proposals, not approved designs.
- A successor may preserve every passed v0.7 rule while changing only cause derivation, partial-availability evaluation, repeated-component bounds, custody/analysis transfers, and affected-target typing.

### 6.4 Unverified future requirements

- Two independent implementations must still reproduce serializers, scanners, stochastic generators, comparators, schedules, and burden calculations.
- Independent labels, semantic-leakage review, reason judgment, mutation coverage, and ACL enforcement remain unperformed.
- Benchmark, null calibration, power, cost preflight, bank authoring, model availability, and all P0-P4 measurements remain unperformed and unauthorized.

## 7. Maximum allowed claim

The maximum defensible claim is:

> At commit `d2e024a6c95213ccaf54bf996063c267a6d10ae6`, URC-0.7 and public falsification plan v0.4 are unimplemented public redesign proposals. They textually establish a truth-consistent record-basis/responsibility split with identified human/Brain owners, bounded citation/affected/packet witnesses, a valid stated P3 null grid, exact P2/P3 latent mappings, a seed-safe balanced schedule, a 240-hour arithmetic ledger, fixed raw-level consequences, and complete runner surrogate/member order rules. They do not establish author-independent root-cause adjudication, exhaustive realizable overlap consumption, partial-availability C1-C7 determinism, an executable custody/blinded-analysis pipeline, resource feasibility, public validation, or CONTROL-integration suitability.

No claim is authorized for an executable schema, fixture, question, answer, oracle, implementation, simulation result, executor work, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 8. Unresolved feasibility

- Whether the 24-row grammar is usable by first-output executors.
- Whether varied synthetic questions can satisfy the cause, alias, owner, closure, citation, affected, and packet constraints without distortion.
- Whether two independent labelers can agree exactly on every typed relation and owner.
- Whether a corrected finite overlap catalog can fit the 240-hour, compute, and storage ledgers.
- Whether direct calibration/power runs fit 1,000 CPU-hours, 64 GiB RAM, 200 GiB temporary storage, 10 GiB persistent simulation output, seven days, and USD 500 compute.
- Whether calls, storage, paid isolated roles, and contingency fit the USD 3,000 total and 100 GiB confirmatory storage ceiling.
- Whether 240 human hours are practically sufficient for the expanded isolated role set despite correct arithmetic.
- Whether required ACL vaults, write-only delivery, exact model fingerprint, monotonic/durable timestamps, and blinded coefficient routing are available.
- Whether semantic reviewers and judges agree; disagreement remains failure.
- Whether any calibrated conclusion holds outside the expressly audited latent-normal grids; no such claim is permitted.

## 9. Minimum rereview scope

A fresh successor review must, at minimum, authenticate the unchanged governing boundary/protocol and predecessor hashes plus this review, then read the successor candidate, falsification plan, and author response in full. It must re-evaluate:

1. a mechanically unique cause-equivalence relation and multi-coordinate decision-source selector;
2. complete branch-local partial-availability truth/source tables for C1-C7;
3. finite repeated-component bounds and one unambiguous overlap-catalog freeze/generation sequence;
4. a matrix/ledger bijection for registrar content, both scans, timing/run logs, P1 expected results, condition-map release, and every signature;
5. a blinded coefficient/stratum map sufficient for every P2-P4 statistic before condition identity release;
6. target/affected-record typing; and
7. non-regression of every PASS in sections 3 and 5.

No bank, label, implementation, simulation, executor output, sealed input, or result is needed or allowed for that rereview.

## 10. Exact next-gate recommendation

Do not open CONTROL integration, public authoring, schema/runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or any E0-dependent work.

Preserve the authenticated v0.6/v0.7 artifacts and this review at their hashes. The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.8 REDESIGN OPEN`

The successor must correct every blocking and major finding above, the minor type defect, and then receive another fresh public-only independent read-only review.

## 11. Final verdict

**REVISE-AND-REVIEW**
