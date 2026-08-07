# URC-0.6 independent hostile public-only review

- Review type: `fresh public-only hostile read-only review`
- Commit: `0d0bdfc7ce994de6d50ce5aa883dc1ff0f2e99cf`
- Branch: `codex/s0-question-contract-v06`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.6 INDEPENDENT REVIEW OPEN`
- Authority: review and CONTROL-integration suitability only
- No files changed; no code, fixtures, questions, answers, oracle, simulation, model calls, scoring, or S0 execution occurred.

## 1. Input boundary and authentication

HEAD, branch, all seven allowlisted inputs, and all six assigned same-basename sidecars were present and matched.

| Authenticated input | Verified SHA-256 |
|---|---|
| S0–E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| Protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| v0.5 independent review | `cffe6b6d9910b1a43b5fa07aa0152583e10429cdc94971d8dc27ccd79adda359` |
| URC-0.6 candidate | `2223defe3a01c7bd85feaac32951a01b3f7661901230743598136bf62472fb67` |
| Falsification plan v0.3 | `66e0c07fe7137a322f016f71aac7ee2cee1953129196af1eff1279c967a0434b` |
| Review response v0.1 | `d177fd893b9a5b8b44848608d839ea778b1e74317029f96f3814945a0d4cfa1b` |

No repository history, sibling output, E0 material, sealed/private/oracle material, web source, or non-allowlisted file was used.

## 2. Decision rubric

- **PASS**: the authenticated finding is closed at the public proposal-text level with no remaining counterexample or hidden choice in the reviewed scope. It does not mean implemented or validated.
- **FAIL**: a concrete contradiction, incomplete branch, arithmetic error, or non-executable rule still defeats the claim.
- **UNCLEAR**: the text admits incompatible implementations or lacks enough semantics for an author-independent decision.

Severity for new findings:

- **blocking**: prevents CONTROL integration.
- **major**: materially breaks reproducibility, isolation, feasibility, or a gate result.
- **minor**: localized precision defect that still must be corrected before freeze.

## 3. Authenticated v0.5 finding decisions

| Finding | Decision | Hostile assessment |
|---|---|---|
| B-01 | **FAIL** | The 32 rows mechanically preserve H/D bits, but the mapping is not truth-consistent. Candidate §3.1 defines H as assignment of the “exact unresolved binding decision” to a human, while §§3.2–3.4 permit `authorized; H1` and derive direct operation as allowed. V03/V04 and vectors `C=0,A=1,B=0,H=1,D=*` therefore permit direct operation while the exact binding decision is still assigned and unresolved. |
| B-02 | **FAIL** | Field-local unavailability fixes the original invalid-decision-pair M5+M3 cascade, but metadata aliases can still turn one omission into C3 plus M1, and the response-level/raw-class versus question-level P3 consequence is not exact. |
| B-03 | **FAIL** | Metadata and formulas remain incomplete. C4 uses an untyped “applicable” closure, C6 does not fully cover the declared responsibility states, group-set invariants are incomplete, and the 128-mask table enumerates code presence rather than source-level overlap behavior. |
| B-04 | **PASS** | Plan §§8.1–8.2 removes the bank hash from prospective seeds and confines bank-hash seeds to post-bank confirmatory artifacts. The freeze order is non-circular as written. |
| B-05 | **FAIL** | The plan appropriately narrows error-control claims to audited grids and separates fit/audit streams, but the P3 null grid includes an impossible probability and therefore cannot execute for every required point. P2 simulation details also remain underdetermined. |
| B-06 | **PASS** | Candidate §10 confines fixed runner prose to typed generation, requires independent semantic review for unavoidable prompt prose, and expressly narrows the mechanical claim to enumerated syntactic/provenance predicates. This is a truthful limited claim, not proof of zero leakage. |
| M-01 | **FAIL** | The nested trillion-scale bootstrap is removed and a benchmark stop gate exists, but the human ceiling arithmetic is internally inconsistent: the listed work totals 320 hours against an aggregate ceiling of 240 hours. |
| M-02 | **FAIL** | P2 rotation is balanced, but the seeded P3 rotation algorithm does not guarantee its asserted per-wave difference of at most one. The exact elapsed-time metric used by P4 is also undefined. |
| M-03 | **UNCLEAR** | The six raw classes and broad P3/P4 outcomes are now named, but it is unclear whether one schema defect in a multi-answer response sets every question-level `Y` to zero or only the affected question. Those choices produce different P3 estimands. |
| M-04 | **FAIL** | The matrix is much more detailed but not mutually executable: no authorized role can perform several required transfers, including raw-output custody/anonymization and label-bundle comparison, without violating an allowlist or CONTROL denylist. |
| m-01 | **PASS** | Candidate §9 rejects rather than normalizes non-NFC raw strings and explicitly prohibits U+000A, U+000B, U+000C, U+000D, U+0085, U+2028, and U+2029 in `short_reason`. A separate canonical-JSON edge remains below. |

## 4. New findings

### N-B01 — Human-route vectors authorize an unresolved human decision

- Severity: **blocking**
- Failed claim: all 32 predicate vectors return a truthful, authorized disposition without a route-induced contradiction.
- Evidence: candidate §§3.1–3.4. H means the exact unresolved binding decision is assigned to an identified human now. V03/V04 and vectors `0/1/0/1/*` nevertheless return `authorized`, for which direct operation is allowed.
- Consequence: enumeration preserves the positive H flag but permits the operation to bypass the authority to whom the unresolved decision is assigned.
- Minimum correction direction: make the H/A/direct-operation relationship semantically consistent, add the required metadata identity, and repeat an exhaustive truth-entailment review of all 32 vectors—not merely a row-enumeration check.

### N-B02 — Admissible metadata can describe an impossible valid answer

- Severity: **blocking**
- Failed claim: every bank item passing metadata consistency has at least one schema-valid, semantically correct response.
- Evidence:
  - Candidate §4.1 requires one to four citations and at most four affected IDs.
  - §5.1 permits `allowed_record_ids` to contain zero IDs, permits arbitrarily many required groups, and places no four-ID bound on accepted affected truth.
  - §5.2 contains no satisfiability check tying those sets to the response bounds.
- Consequence: two labelers can agree byte-for-byte on an item for which no conforming correct answer exists—for example, zero allowed citations, more than four mutually disjoint required groups, or more than four accepted affected IDs.
- Minimum correction direction: add deterministic pre-admission satisfiability and cardinality validation across citation obligations, affected truth, and runner limits.

### N-B03 — Source aliases reintroduce cascade double-counting

- Severity: **blocking**
- Failed claim: one semantic mismatch is consumed once while independent failures remain available.
- Evidence:
  - Candidate §§5.1–5.2 do not forbid a required citation group and a counterexample group from representing the same omitted record set.
  - Under §§6.1, 7, and 8.1, a stronger wrong answer omitting that set produces false `E-counter:G` and false `E-required:R`. C3 consumes `D-basis` and `E-counter:G`; the unconsumed `E-required:R` then emits M1.
- Consequence: one omitted counterexample is scored as both C3 and M1 solely because the metadata names it through two atom families. Conversely, correlation member/basis overlap can suppress C2: the same ID may be both a derivative and an “independent” basis because disjointness is not required.
- Minimum correction direction: freeze cross-component alias/disjointness invariants and a root-cause consumption rule covering every permitted overlap.

### N-B04 — The 128-mask table does not test source-level overlap

- Severity: **blocking**
- Failed claim: exhaustive hazard treatment proves deterministic behavior for fully shared, partially shared, and disjoint sources.
- Evidence: candidate §8.2 partitions integers `0..127` by true code bits. It does not enumerate source atoms, realizable metadata, shared-source graphs, expected residual source sets, or expected scored-versus-shadowed results. Some masks are not realizable under the operation-class and formula constraints.
- Consequence: two comparators can agree on true-code masks yet disagree on atom construction and consumption. Plan §6 promises later mutations, but the public design does not provide the frozen expected source-level truth cases needed to judge them independently.
- Minimum correction direction: replace code-presence enumeration as closure evidence with exhaustive realizable source-overlap cases and precommitted expected source, consumed, residual, emitted, and shadowed results.

### N-B05 — C4/C6 are not complete over their declared metadata

- Severity: **blocking**
- Failed claim: exact C1–C7 formulas have executable truth conditions for every metadata branch.
- Evidence:
  - Candidate §7 defines C4 using an “applicable withdrawal closure,” but §5.1 has no applicability field or universal rule declaring every listed closure applicable.
  - §5.2 requires `reservation=human → H=true`, but not `H=true → reservation=human`. Thus H may be true with reservation `none`, and a wrong absent human route becomes only M3 rather than C6.
  - `reservation=brain` has no runner-visible responsibility coordinate; C6 observes it only through one unauthorized-basis branch.
- Consequence: bank authors or comparator implementers must supply unstated interpretations, and declared responsibility/withdrawal hazards can be underclassified.
- Minimum correction direction: close the metadata identities and define every C4/C6 branch solely over typed, observable atoms.

### N-B06 — Required P3 null calibration contains an invalid probability

- Severity: **blocking**
- Failed claim: every P3 null-grid point can be directly simulated before deterministic N selection.
- Evidence: plan §9.3 permits `p_low=0.75` and common C/D gap `0.20`, giving base C/D probability `0.95`. The `theta=+0.10` null shifts both URC C/D marginals to `1.05`. Only base probabilities are said to be excluded outside `[0.05,0.95]`; no rule excludes invalid shifted-null points.
- Consequence: the inverse-normal threshold is undefined, while §§9.3 and 10.1 require every null audit to run and pass. No N can be selected by the stated algorithm.
- Minimum correction direction: freeze a valid, explicit null-grid construction before calibration and re-review any grid change.

### N-M01 — Raw-output classes lack a question-level consequence rule

- Severity: **major**
- Failed claim: raw classes, field-local semantic availability, P3 `Y`, and P4 schema outcomes are globally consistent.
- Evidence: candidate §4.2 classifies the complete raw response; §4.3 preserves valid independent per-question fields. Plan §9.2 defines `Y[q,g,r]`, while §12.1 assigns P3 zero to a “parseable schema-invalid” first output.
- Consequence: for a packet response containing several questions and one invalid field, the text supports both “all packet Y values are zero” and “only the affected question is zero.” The former discards valid decisions; the latter is not derivable from the response-level class table.
- Minimum correction direction: freeze class consequences separately at transport, response, answer, and field levels.

### N-M02 — P3 seeded rotations do not guarantee asserted wave balance

- Severity: **major**
- Failed claim: the deterministic schedule ensures every P3 cell’s serial-position and wave counts differ by at most one.
- Evidence: plan §10.2 repeats a bank-hash-seeded permutation of rotations. For `N=336`, `K=42`: five full eight-rotation cycles leave two rotations. If the seeded prefix is rotations 0 and 1, a base-position-3 cell receives two extra wave-1 placements, while a base-position-5 cell receives none, producing a wave-1 count difference of two.
- Consequence: a valid bank hash can deterministically generate a schedule that contradicts the plan’s claimed balance. The checker then stops, but no deterministic construction guaranteeing a valid schedule exists.
- Minimum correction direction: use a construction whose balance property is proven for every authorized K and seed outcome.

### N-M03 — Human-resource ceilings contain a 240-versus-320-hour contradiction

- Severity: **major**
- Failed claim: all human and monetary ceilings are internally achievable under the stated scope.
- Evidence: plan §11.3 sets aggregate labor to 240 hours, then lists CONTROL 80, authoring 60, labels 80, review/judging 40, and implementation/scan/analysis/reserve 60: total 320 hours. The independent role constraints prevent treating CONTROL coordination as the same labor event as the other incompatible roles.
- Consequence: the resource preflight has no valid passing interpretation.
- Minimum correction direction: reconcile the aggregate with a non-overlapping role/task accounting ledger before any benchmark or authoring gate.

### N-M04 — The role matrix has required but unauthorized transfer operations

- Severity: **major**
- Failed claim: the per-role matrix is complete, mutually compatible, ancestry-safe, and keeps labels and outputs outside executor-visible state.
- Evidence:
  - Plan §3.2 restricts CONTROL registrar inputs to public design artifacts, attestations, and nonsemantic metadata, and denies unblinded semantic output before judge freeze.
  - The executor’s only transfer is a raw response to a CONTROL drop box.
  - No output custodian/router is authorized to hash, anonymize, and transfer raw semantic responses to judges.
  - No role is authorized to compare label bundles before the leakage reviewers receive both.
- Consequence: the freeze and judging sequence cannot run without an unlisted role or a listed role exceeding its allowlist. Such an informal repair would invalidate the bank under §3.1.
- Minimum correction direction: enumerate every custody, comparison, anonymization, signing, and transfer operation and assign it to a compatible isolated role with exact inputs and outputs.

### N-M05 — Statistical and P4 metric definitions remain partly non-executable

- Severity: **major**
- Failed claim: independent implementations can reproduce calibration and burden analysis from the frozen public specification.
- Evidence:
  - Plan §7.3 does not fully state component distributions and independence indexing, or the exact conversion of equivalence midpoint and delta into the original/neutral marginal probabilities.
  - Plan §12.3 uses “pooled median elapsed time,” while §10.3 records queue, provider start, first-token, and finish times without selecting the interval used by the threshold and bootstrap.
- Consequence: conforming implementations can generate different latent datasets and different P4 pass/fail results.
- Minimum correction direction: freeze the missing stochastic mappings and exact timestamp-derived metric before implementation hashes are accepted.

### N-m01 — Canonical JSON leaves escaped-surrogate and property-order edges open

- Severity: **minor**
- Failed claim: two independent serializers have a complete normative byte rule.
- Evidence: candidate §9.1 validates strict UTF-8 bytes, but JSON can contain escaped unpaired surrogates such as `"\ud800"` without malformed UTF-8 bytes. The subsequent NFC/scalar behavior is not classified. Section 4.1 explicitly fixes answer-member order but does not explicitly fix every top-level and nested decision-object member order relied on by §9.3.
- Consequence: parsers and serializers may reject, preserve, or encode the same parseable input differently.
- Minimum correction direction: classify non-scalar JSON escape sequences and explicitly enumerate every object’s canonical member order.

## 5. Overall rubric

| Review dimension | Result |
|---|---|
| Frozen input and SHA-256 integrity | **PASS** |
| Exact 16-row Cartesian enumeration | **PASS, syntactic only** |
| Truth-consistent 32-vector mapping | **FAIL** |
| No route-induced unauthorized direct operation | **FAIL** |
| Raw-output class exhaustiveness | **UNCLEAR** |
| Field-local availability and M5 boundary | **PASS in the original malformed-decision trace; FAIL globally** |
| No cascade double-counting | **FAIL** |
| Preservation of independent valid failures | **UNCLEAR** |
| Closed metadata satisfiability | **FAIL** |
| Exact C1–C7 truth conditions | **FAIL** |
| Missing/extra citation handling | **FAIL under permitted metadata aliases** |
| Withdrawal and responsibility coverage | **FAIL** |
| 128-mask code enumeration | **PASS** |
| 128-mask source-overlap proof | **FAIL** |
| Prospective seed non-circularity | **PASS** |
| Fit/audit stream separation | **PASS** |
| P2 direct-statistic and grid-limited framing | **UNCLEAR** |
| P3 boundary-grid executability | **FAIL** |
| Alpha/power/N selection without post-bank tuning | **UNCLEAR** |
| Removal of nested bootstrap | **PASS** |
| Simulation benchmark stop gate | **PASS AS AN UNEXECUTED REQUIREMENT** |
| Call/token arithmetic at N=720 | **PASS** |
| Human-hour arithmetic | **FAIL** |
| Monetary/compute/storage feasibility | **UNVALIDATED** |
| P2 wave balance | **PASS** |
| P3 wave balance | **FAIL** |
| Exact revision and drift stop rules | **PASS AS DESIGN REQUIREMENTS; UNVALIDATED** |
| P3/P4 invalid-output compatibility | **UNCLEAR** |
| P4 interval reproducibility | **UNCLEAR** |
| Typed fixed-prose generation | **PASS AS DESIGN REQUIREMENT** |
| Narrow semantic-leakage claim | **PASS** |
| Executor visibility and ancestry rules | **PASS in principle** |
| Complete executable role/transfer matrix | **FAIL** |
| NFC and one-line rules | **PASS** |
| Complete canonical JSON bytes | **FAIL** |
| Rollback and untouched-bank rule | **PASS** |
| Sealed/private/oracle boundary | **PASS** |
| S0–E0 boundary | **PASS** |
| Claim ceiling | **PASS** |
| CONTROL-integration suitability | **FAIL** |

## 6. Maximum allowed claim

The maximum defensible claim is:

> At the authenticated commit, URC-0.6 and public falsification plan v0.3 are unimplemented public redesign proposals. They textually remove the prospective bank-hash seed dependency, replace the nested prospective bootstrap with direct statistics and a benchmark stop gate, narrow the mechanical leakage claim, and resolve the predecessor’s NFC/line-break ambiguity. They do not establish a truth-consistent universal decision contract, nonduplicative deterministic scoring, executable calibrated sample selection, internally coherent resource envelope, complete role isolation, public validation, or CONTROL-integration suitability.

No executable schema, fixture, question, answer, oracle, implementation, simulation, executor work, public validation, sealed migration, S0 result, representation superiority, central-system result, Project Brain integration, operational-safety result, economic-value result, or model-transfer claim is authorized.

## 7. Exact next-gate recommendation

Do not open CONTROL integration, public authoring, implementation, simulation, executor work, sealed access, or S0 execution.

Preserve the authenticated v0.6 artifacts at their present hashes. The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.7 REDESIGN OPEN`

That successor must correct the blocking and major findings above and then receive another fresh public-only independent read-only review.

## 8. Final verdict

**REVISE-AND-REVIEW**
