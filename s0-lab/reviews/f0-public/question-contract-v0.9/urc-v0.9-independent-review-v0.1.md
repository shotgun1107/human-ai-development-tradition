# URC-0.9 independent hostile public-only review

- Review type: `fresh independent hostile public-only read-only review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `4fe66224122169dd23e64c92a1a4bed40ae0d518`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.9 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, code, generator, comparator, runner, simulation, model call, scoring, executor work, sealed access, S0 execution, branch creation, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** The worktree was clean at the required branch, commit, and origin before substantive review. All twelve allowlisted Markdown inputs were read in full. Eleven same-basename sidecars, formed by replacing `.md` with `.sha256`, had the required lowercase digest plus two spaces plus same-basename filename form and matched the Markdown bytes. `AGENTS.md` has no sidecar; its computed digest is recorded as a governing-input fact.

| Exact input | Verified SHA-256 | Authentication |
|---|---|---|
| `AGENTS.md` | `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d` | no sidecar; governing instruction only |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matching sidecar |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/universal-response-contract-v0.8-candidate.md` | `ee9f9dd02030a79b7f28a475f18402906c0425de97eab677d50316d41676677c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/review-response-v0.3.md` | `b2ab90bb3862fa9b74bf656c87d92cc809b2dfa5990a555731b6c52175b6adcf` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.8/urc-v0.8-independent-review-v0.1.md` | `9bca8b3b2ba9e43d00e17f89ad4e5eec9c329bb8d49fccd5137e01b27034d511` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/public-falsification-plan-v0.6.md` | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/review-response-v0.4.md` | `8d243c4435fff25012b0ec416c5b09414654edf4e1c4ee9d7e8d1ab549419597` | matching sidecar |

No repository-wide search, history inspection beyond the exact baseline checks, E0 work product, other S0 version, sealed/private/oracle path, fixture, problem, answer, schema, runner, code, output, or web source was read. Worktree separation was treated as edit isolation only.

## 2. Rubric

- **PASS**: the authenticated proposal text uniquely closes the finding in scope without a result-affecting author, builder, comparator, custodian, or analyst choice. This never means implemented or validated.
- **FAIL**: a contradiction, incomplete construction, non-unique mapping, unsatisfied precondition, missing authorized transfer, or executable counterexample remains.
- **UNCLEAR**: the public text permits materially different implementations and the allowlisted inputs do not choose one.

New-finding severity:

- **blocking**: prevents CONTROL integration because an effective document, mandatory adjudication result, or P0/P1 artifact cannot be uniquely constructed.
- **major**: materially breaks custody, blinding, reproducibility, fairness, or feasibility.
- **minor**: a localized precision defect requiring correction before freeze.

## 3. Effective-document reconstruction

### 3.1 Thirty-one-slot contract

**PASS for byte construction.** `U7` and `U9` authenticate to the declared hashes, each named heading resolves uniquely, the parent preambles and full ranges are consecutive at the stated levels, and all 31 predecessor slots are classified exactly once. The `U9` source digest comes from its authenticated sidecar; the effective hash is not embedded in `U9`, so no self-reference occurs.

Using strict UTF-8, raw LF-preserving slices, the stated ASCII record fields, and no inserted separators, this review independently obtained:

```text
effective_contract_sha256=54e731edd895db001c3e89da25e06e7c86f1563c297184be3e6cb570fff83f01
effective_slots=31
raw_slice_bytes=27267
effective_stream_bytes=34289
```

This is an in-memory review computation, not a frozen implementation or later manifest.

### 3.2 Twenty-five-slot transitive plan

**FAIL.** The P4/P5/P6 source hashes and named slices authenticate, but the mandatory slot-10 transform precondition is false. The exact authenticated P5 section 8 slice contains one ASCII occurrence of `URC-0.8`, not the required two. It separately contains one lowercase `v0.8` occurrence. The construction therefore rejects at slot 10 under its own rule and no conforming effective-plan hash exists.

Even after repairing that count, the record grammar is not byte-unique:

1. The companion record already contains `slice_mode`; P6 then says to insert both `slice_mode` and `transform` immediately before `length`. A literal insertion produces two `slice_mode` lines, while an intended replacement produces one.
2. The companion says record metadata is ASCII, but plan slot headings 9, 11, and 21 contain U+2014 EM DASH and must also be copied as exact heading text into `slice_start` or `slice_end`. UTF-8 preservation and ASCII replacement yield different bytes; strict satisfaction of both requirements is impossible.

The P6 sidecar itself is nonrecursive and authentic. The failure is in effective-record construction, not source authentication.

## 4. Finding-by-finding disposition of V8-B01 through V8-M02

| Authenticated finding | Decision | v0.9 assessment |
|---|---|---|
| V8-B01 — incomplete exact-hash contract composition | **PASS FOR THE 31-SLOT CONTRACT ONLY** | The predecessor section map is total and the contract stream is computable. The companion 25-slot plan fails independently under new V9-B01 and V9-B02. |
| V8-B02 — cause ordering not canonical | **FAIL** | Outer `cause_ref` ordering now fixes unsigned UTF-8 bytes, prefix behavior, and `R10` before `R2`, and removes ordinal IDs. However, multi-member obligation and correlation keys still require `ascending member_ids` without defining the record-ID order used before serialization; see V9-B03. |
| V8-B03 — C4 branch/source mismatch | **PASS** | Dependent-missing, target-record-missing, and direct-mismatch branches are separate. Each T branch names only its own sources; unrelated missing accepted IDs and extra submitted IDs remain M4. |
| V8-B04 — impossible catalog arithmetic | **PASS AS ARITHMETIC** | The unquotiented product is correctly `921,600`; rejected tuples remain rows. The `1,792`, `407`, and `2,949,120` counts are also arithmetically correct. Feasibility remains untested. |
| V8-M01 — incomplete cause/availability bounds | **PASS AT THE DECLARED BOUND LEVEL** | The absolute maximum is 28 causes, dynamic extra-affected causes are included, and all eight availability axes and their bit order are listed. Later exact generator specifications and slot instantiations remain unverified future artifacts. |
| V8-M02 — unmatched operational edges | **FAIL** | The package and constants/formula paths are added, but the published matrix/index still contains unauthorized producer duties and unmatched inputs/stores; see section 6.4. |

## 5. New blocking findings

### V9-B01 — The slot-10 transform cannot execute

- Severity: **blocking**
- Fact: P6 requires exactly two nonoverlapping ASCII occurrences of `URC-0.8` in the authenticated P5 section 8 slice.
- Fact: that slice has exactly one `URC-0.8` and one distinct lowercase `v0.8`.
- Executable counterexample: authenticate and slice P5 section 8, count case-sensitive ASCII `URC-0.8`, and obtain `1`; the rule requires rejection before replacement.
- Consequence: the 25-record stream and `effective_plan_sha256` cannot exist, so P0 cannot agree on the required plan hash.
- Minimum correction proposal: specify the two intended old byte strings and their separate replacements, or require the actual one-occurrence transform; then publish and hostile-check the resulting exact count and transformed slice.

### V9-B02 — The plan record encoding is contradictory and non-unique

- Severity: **blocking**
- Fact: the reused companion record already includes one `slice_mode` field.
- Fact: P6 instructs insertion of `slice_mode` and `transform` before `length` without saying that the inherited `slice_mode` is replaced.
- Fact: three P4 level-2 headings used in record metadata contain U+2014, while the companion requires ASCII metadata and exact heading text.
- Executable counterexample: builder A retains the inherited `slice_mode` and inserts another; builder B emits it once. Separately, builder C encodes the exact U+2014 heading in UTF-8 while an ASCII encoder emits `?` or rejects. The byte streams differ before content semantics.
- Consequence: correcting V9-B01 alone still would not yield one plan hash.
- Minimum correction proposal: publish the complete plan-record grammar once, with each field occurring exactly once, and define all metadata as UTF-8 or use ASCII-safe heading digests/indices rather than contradictory exact non-ASCII values.

### V9-B03 — Multi-member cause identity still depends on an undefined record-ID order

- Severity: **blocking**
- Fact: section 6 fully orders already-serialized cause references by unsigned canonical UTF-8 bytes.
- Fact: obligation and correlation constructors first require arrays of `ascending member_ids`, `ascending derivative_ids`, and `ascending independent_basis_ids`, but no record-ID comparator is defined. The cause-reference order does not state that it orders elements inside those arrays.
- Executable counterexample: for obligation members `{R2,R10}`, natural-numeric ascending produces `['R2','R10']`; unsigned bytewise ascending produces `['R10','R2']`. Both satisfy an unstated interpretation of “ascending,” but serialize to different canonical key bytes. Prefix, quote/backslash escape, and ASCII-punctuation IDs create the same unresolved pre-serialization choice.
- Consequence: equal typed member sets can receive different `cause_ref` identities, breaking biconditional equality, the 407-row catalog, expected tables, and comparator agreement.
- Minimum correction proposal: apply one explicit unsigned-canonical-byte comparator to every ID array before key construction, including prefix, escape, and punctuation cases, and freeze mutations for multi-member obligation and correlation keys.

## 6. New major findings and custody continuation

### V9-M01 — The transitive plan drops predecessor bank-balance and duplicate controls

- Severity: **major**
- Fact: P4 section 4 requires N to be exactly balanced across all 24 rows and forbids development examples and noun-swapped duplicates.
- Fact: P5 section 6 expressly preserved the divisibility and no-duplicate rules.
- Fact: effective slot 7 replaces P5 section 6 with P6 section 5, which republishes the candidate N sequence and freeze schedule but not exact 24-row balance, the development-example ban, or the noun-swapped-duplicate ban.
- Executable counterexample: author N=240 with 239 questions in one row and one in another, including noun-swapped duplicates. The effective P6 section 5 sequence and later freeze steps can still be followed; no retained effective clause expressly rejects this bank.
- Consequence: row-frequency leakage, independence, and bank coverage can differ while the nominal N and schedules remain valid.
- Minimum correction proposal: put the exact balance, divisibility, development-example, and duplicate rules into a retained effective slice or republish them verbatim in P6.

### Continuation of V8-M02 — The claimed matrix/ledger bijection is false

- Severity: **major**
- The representation builder requires a transformation specification, but no E00A-H or E01-E50 edge delivers one.
- The simulation builder requires frozen statistical/catalog specifications, while E01 carries reviewed hashes and a pre-bank manifest; no edge authorizes the specification bytes.
- E00A-H make the CONTROL registrar the producer of authoring, label, scanner, leakage, metadata, catalog, schedule, formula, rubric, resource, transport, anonymization, and decision-table artifacts. The registrar matrix cell allows only reviewed hashes as relevant inputs and only signed status manifests as output. It neither receives nor is authorized to emit those specification bytes.
- The registrar's positive `role/store attestations` input has no producer or edge.
- Several named-store outputs are bypassed by direct edges: `content-vault`, `label-vault-A`, `label-vault-B`, `leakage-vault-1`, `leakage-vault-2`, and `condition-map-vault` lack exact write/read ledger rows matching their matrix/store declarations.
- Executable counterexample: execute grants and transfers literally. The representation builder reaches its turn with content via E06 but no transformation specification. Supplying it through the repository or conversation violates the explicit ambient-access ban; omitting it prevents A-D construction. The same contradiction occurs earlier if the registrar attempts E00A-H using only its positive inputs.
- Consequence: the bank cannot reach representation construction or later roles under its own allowlists, and the promised zero-unmatched-edge P0 check must fail.
- Minimum correction proposal: make each specification owner and byte source explicit; authorize the registrar only to sign/route artifacts it receives, or assign public-specification custody elsewhere; add exact missing store writes/reads and publish a mechanically checkable edge-to-matrix table with zero unmatched cells.

## 7. Focused hostile checks

| Required attack | Result | Assessment |
|---|---|---|
| 31-slot headings, preambles, source hashes, record construction | **PASS** | All contract slices resolve and the in-memory hash is reported in section 3.1. |
| 25-slot P4/P5/P6 construction | **FAIL** | Slot-10 transform rejects at count one; record encoding has independent defects. |
| self-sidecar handling | **PASS** | U9/P6 source hashes come from authenticated external sidecars; no effective hash is embedded recursively. |
| `R10`/`R2` outer cause order | **PASS** | Canonical bytes put `R10` before `R2`. |
| prefix and escape order for serialized cause references | **PASS** | First differing unsigned byte and shorter-prefix-first are explicit after inherited canonical escaping. |
| multi-member key construction | **FAIL** | Inner record-ID ordering remains undefined before serialization. |
| C4 dependent missing | **PASS** | Only the missing dependent key sources the branch. |
| C4 target missing | **PASS** | Only the typed target-record value sources the branch. |
| C4 extra submitted affected ID | **PASS** | It remains M4 and cannot source C4. |
| C4 dependent=target alias | **PASS** | Identical canonical key is unioned once. |
| C4 T/F/U independence | **PASS AS WRITTEN** | Applicable/inapplicable and dependency guards are explicit; unrelated U cannot hide a decisive branch. |
| 28-cause maximum | **PASS AS ARITHMETIC** | `20+4+4=28`; extra affected causes are not omitted. |
| eight availability axes | **PASS** | Bit order is explicit and `7*256=1,792`. |
| abstract catalog | **PASS AS ARITHMETIC** | `4*10*3*3*5*4*128=921,600`; no pre-rejection quotient. |
| cause-key catalog count | **PASS AS ARITHMETIC** | `1+28+C(28,2)=407`. |
| bank-instance maximum | **PASS AS ARITHMETIC** | `720*2^12=2,949,120`. |
| every named store and E00A-H/E01-E50 | **FAIL** | The ledger repairs earlier package/constants paths but still contradicts matrix authority and omits required inputs/store edges. |
| role-to-edge index | **FAIL** | Index repetition cannot create transfers absent from the ledger or authorize registrar outputs forbidden by its matrix cell. |
| D-favoring runner vocabulary | **PASS AT THE TEXTUAL LEVEL** | A-D names, target-candidate narrative, semantic condition map, and relation ranking remain outside executor packages; neutral codes and common grammar remain required. |
| answer leakage | **PASS AT ITS LIMITED CLAIM** | Typed package generation, two scans, two semantic reviewers, and the narrow scanner claim remain; zero paraphrased leakage is not claimed. |
| post-result threshold changes | **PASS** | Threshold or formula changes require a new reviewed version and untouched bank; the final join cannot reanalyze. |
| conclusion beyond synthetic logic | **PASS** | The future claim remains bounded to one frozen synthetic public experiment and excludes S0, system, safety, economic, and transfer claims. |

## 8. A-D fairness and predecessor non-regression

### 8.1 Same source information, authority, model conditions, time, and scoring opportunities

| Dimension | Decision | Evidence and limit |
|---|---|---|
| canonical source facts | **PASS AS UNIMPLEMENTED REQUIREMENT** | The inherited protocol and plan require the same canonical fact IDs, record IDs, normalized content hashes, question order, and equality manifest; only intended representation differs. D relations require explicit supporting facts available in every condition. |
| runner authority and tools | **PASS AS UNIMPLEMENTED REQUIREMENT** | Authority, tools/network, external transfer, turn, retry, and output limits remain common. Custody failure prevents execution but does not introduce a D-specific grant. |
| model and reasoning | **PASS AS UNIMPLEMENTED REQUIREMENT** | Exact revision/fingerprint, reasoning, tier, region, token limits, and timeout are shared across every cell; drift invalidates the suite. |
| time and load | **PASS AS UNIMPLEMENTED REQUIREMENT** | P2 rotations and the every-seed P3 construction balance serial positions and waves; concurrency is three and the window is seven days. |
| question and scoring opportunity | **PASS AS UNIMPLEMENTED REQUIREMENT** | Every grammar crosses A-D on matched packets, with the same question, response contract, anonymous comparator rules, and frozen thresholds. No D-specific retry, threshold, or extra question is authorized. |

### 8.2 Recorded non-regressions

| Control | Decision |
|---|---|
| 24 rows and all 64 C/A/B/H/G/D vectors | **PASS** |
| typed human/Brain owners and direct operation only for `authorized; none` | **PASS** |
| citation hitting-set, affected, answer, packet, and raw-byte satisfiability | **PASS** |
| strong T/F/U tables and decisive T/F/U branch behavior | **PASS** |
| C1-C7 truth/source definitions other than inner multi-member key order | **PASS; C4 REPAIRED** |
| target typing and record-only affected arrays | **PASS** |
| canonical JSON, duplicate rejection, NFC, seven line scalars, surrogates, member order | **PASS; NO REGRESSION** |
| response-, answer-, field-, P3-, and P4-level consequences | **PASS BY EXPLICIT INHERITED REFERENCE; UNIMPLEMENTED** |
| P2 stochastic mapping, hypotheses, alpha allocation, and schedules | **PASS AS UNEXECUTED DESIGN** |
| P3 valid marginal grid, estimator, mappings, and every-seed schedule | **PASS AS UNEXECUTED DESIGN** |
| non-circular seed and fit/audit separation | **PASS** |
| independent labels, generators, comparators, scans, judges, and blinded analysis | **PASS IN ROLE INTENT; FAIL IN COMPLETE CUSTODY** |
| transport recorder, first-output interval, no retry, load/drift invalidation | **PASS** |
| 960 calls at N=720 | **PASS AS ARITHMETIC** |
| visible input tokens `53,760,000` | **PASS AS ARITHMETIC** |
| visible output tokens `3,194,880` | **PASS AS ARITHMETIC** |
| 240-hour ledger | **PASS AS ARITHMETIC; FEASIBILITY UNVERIFIED** |
| benchmark, CPU/RAM/storage/calendar/USD stops | **PASS AS WRITTEN STOPS; UNRUN** |
| rollback and untouched-bank rule | **PASS** |
| sealed/oracle and S0-E0 boundaries | **PASS** |
| noncompensatory P0-P4 | **PASS** |
| claim ceiling | **PASS** |
| exact bank balance and duplicate controls | **FAIL; V9-M01** |

The passed clauses establish only textual non-regression or arithmetic. They are not implementations, measurements, feasibility results, or validation results.

## 9. Facts, inferences, correction proposals, and unverified requirements

### 9.1 Facts established by this review

- The baseline and twelve input digests are recorded in section 1; all eleven available sidecars match.
- The 31-slot contract byte stream is computable and has the in-memory digest in section 3.1.
- The authenticated plan slot-10 slice has one exact `URC-0.8`, so the required count-two transform rejects.
- P4 headings used by plan slots 9, 11, and 21 contain U+2014 and cannot be both exact and ASCII metadata.
- The ledger does not deliver the transformation specification to the representation builder, while E00A-H exceed the registrar's matrix authority.
- No implementation or empirical result was available or created.

### 9.2 Review inferences

- A plan that cannot produce one effective hash cannot satisfy its own noncompensatory P0 gate.
- Undefined ordering inside multi-member cause keys permits different mandatory expected bytes from the same set-valued metadata.
- Custody mismatches are substantive because the plan forbids ambient access and treats any unlisted transfer as bank-invalidating.
- Correct C4 branches, repaired arithmetic, and symmetric A-D requirements cannot compensate for these failures.

### 9.3 Correction proposals

- The minimum correction directions in sections 5 and 6 are proposals, not approved design choices.
- A successor can retain the authenticated passing clauses while changing only the plan transform/record grammar, inner ID ordering, bank-balance clauses, and custody matrix/edges.

### 9.4 Unverified future requirements

- Two implementations still must reproduce section slicing, serializers, scanners, generators, comparators, schedules, simulations, and burden calculations.
- Exact 28-slot catalog instantiation, labels, package scans, semantic reviews, reason judgments, ACL enforcement, and P0-P4 remain unperformed.
- The 921,600-row abstract catalog and maximum projection have not been benchmarked against 240 human hours or compute, storage, calendar, and USD ceilings.
- Calibration, power, immutable revision availability, varied-bank feasibility, and executor behavior remain unknown and unauthorized.

## 10. Maximum allowed claim

The maximum defensible claim is:

> At commit `4fe66224122169dd23e64c92a1a4bed40ae0d518`, the authenticated URC-0.9 package is an unimplemented public redesign proposal. It provides a total, mechanically reconstructable 31-slot contract map; repairs C4 source scope; corrects the catalog arithmetic and cause bound; and preserves many public synthetic-test controls. Its transitive plan cannot produce the required effective hash, multi-member cause identity is not fully canonical, exact bank-balance controls regress, and the published custody bijection remains incomplete.

No claim is authorized for CONTROL integration, an executable schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation result, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 11. Unresolved feasibility

- Whether the 24-row grammar is usable by fresh first-output executors.
- Whether varied synthetic questions can satisfy the metadata, target, alias, and four-ID bounds without distortion.
- Whether independent labelers, semantic reviewers, judges, generators, scanners, and map builders can agree exactly.
- Whether corrected catalogs and 200 comparator runs fit the stated human, compute, storage, calendar, and monetary ceilings.
- Whether required ACL stores, write-only raw delivery, immutable model fingerprint, and durable monotonic timestamps are available.
- Whether calibrated conclusions would hold outside the frozen latent-normal grids; no such claim is permitted.

## 12. Minimum rereview scope

A fresh successor review must authenticate this record and unchanged governing inputs, then read the successor candidate, plan, and author response in full. At minimum it must re-evaluate:

1. a satisfiable slot-10 transform with the exact case-sensitive occurrence inventory;
2. one complete plan-record encoding with no duplicate fields and an encoding that can represent every exact heading;
3. the 31-slot contract and corrected 25-slot plan hashes from independent reconstruction;
4. byte-exact ordering inside every record-ID array used by obligation and correlation cause keys, including `R10`/`R2`, prefix, escape, and punctuation cases;
5. C4 dependent, target, extra, alias, and T/F/U non-regression;
6. all 28 causes, eight availability axes, and `921,600`, `1,792`, `407`, and `2,949,120` counts;
7. exact 24-row bank balance, divisibility, development-example, and duplicate prohibitions;
8. every named store and E00A-H/E01-E50 edge, including registrar authority, transformation/statistical specification delivery, attestations, and exact store writes/reads;
9. A-D source, authority, model, time, question, and scoring equality; and
10. every other PASS in sections 7-9 without claim inflation.

No bank, labels, implementation, simulation, model call, executor output, sealed input, or result is required or permitted for that rereview.

## 13. Exact next-gate recommendation

Do not open CONTROL integration, public bank authoring, schema/runner implementation, simulation, model calls, executor work, sealed access, S0 execution, or E0-dependent work.

Preserve the authenticated v0.7-v0.9 artifacts and this review. The only appropriate next gate is:

`F0-PUBLIC QUESTION CONTRACT V0.10 REDESIGN OPEN`

The successor must correct every blocking and major finding above and receive a fresh public-only independent read-only review.

## 14. Final verdict

**REVISE-AND-REVIEW**
