# URC-0.7 redesign response to authenticated v0.6 review v0.2

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.6-independent-review-v0.1.md`
- proposed successors: `universal-response-contract-v0.7-candidate.md` and `public-falsification-plan-v0.4.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.7 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, sealed work, and S0 conclusions

## 1. Authenticated input record

Before redesign, CONTROL verified the assigned clean branch and HEAD, read every allowlisted Markdown input in full, and verified all six available same-basename sidecars. `AGENTS.sha256` was not present.

| Input | Verified SHA-256 |
|---|---|
| `AGENTS.md` | `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` |
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.6 candidate | `2223defe3a01c7bd85feaac32951a01b3f7661901230743598136bf62472fb67` |
| public falsification plan v0.3 | `66e0c07fe7137a322f016f71aac7ee2cee1953129196af1eff1279c967a0434b` |
| review response v0.1 | `d177fd893b9a5b8b44848608d839ea778b1e74317029f96f3814945a0d4cfa1b` |
| v0.6 independent review v0.1 | `e0c4408f820f1c11da7989998910aac633887524ff649a7296ee652aea96ac81` |

No repository history, E0 workstream result, sealed/private/oracle material, fixture, code, output, web source, or unlisted file was used.

## 2. Finding-response map

“Proposed closure” means only that v0.7 contains a written rule addressing the finding. It does not mean the rule is correct, feasible, implemented, or tested.

| Authenticated finding | v0.7 response | Author assessment |
|---|---|---|
| B-01 / N-B01: H/A/direct-operation contradiction | Candidate §§3.1-3.5 redefine A as record basis, add typed `responsibility_route`, and allow direct operation only for `authorized; none`. Every H-positive predecessor vector is human-routed and direct=no. A typed G predicate covers Brain. Human/Brain reservations require exactly one owner ID and support. All 64 raw vectors have a row or deterministic H/G rejection. | proposed closure; truth-entailment requires hostile review |
| N-B02: unsatisfiable metadata | Candidate §4.4 requires a finite 1-4 citation hitting-set witness, nonempty allowed IDs, accepted affected size <=4, per-answer witness <=896 bytes, and per-packet witness <=7,680/8,192 bytes. §5.2 makes these admission conditions. | proposed closure; future varied-bank feasibility unknown |
| B-02 / N-B03: alias cascade | Candidate §§5.3, 6, and 8 assign surface templates to one typed cause, require identical required/counterexample sets to share an obligation, reject partial overlap, make derivative/basis sets disjoint, and consume causes so an alias cannot later emit M1. | proposed closure; mutation proof required |
| B-03 / N-B04: masks do not prove overlap | Candidate §8.2 demotes masks to diagnostics and defines the exhaustive realizable normal form, permitted B and C1/C5 X sharing only, overlap cases O0-O6, and exact prior/residual/emitted/shadowed/consumed equations. Plan §6 requires every finite instantiation with typed preconditions. | proposed closure; catalog size and reviewer agreement unvalidated |
| N-B05: incomplete C4/C6 | Candidate §§5.1-5.2 type closure applicability and make C4 quantify only explicit applicable closures. C6 uses the visible responsibility coordinate for both human and Brain, with bidirectional H/G identities and typed owners. | proposed closure |
| B-05 / N-B06: invalid P3 null grid | Plan §9.3 explicitly lists six base pairs and both theta boundaries; every resulting marginal is in `[0.45,0.95]` and no exclusion branch remains. | proposed closure; calibration unrun |
| M-03 / N-M01: response/answer/field consequences | Candidate §§4.2-4.3 separately fix suite, response, answer, and field consequences. Response envelope/membership defects zero all response questions; answer-local defects zero only that question; field-local C/M availability remains exact. Plan §§9.2 and 12.1 reuse those rules. | proposed closure; needs independent mutation review |
| M-02 / N-M02: P3 rotation not guaranteed | Plan §10.3 uses full eight-rotation cycles plus a residual antipodal pair or its complement. The written wave/position proof holds for every authorized K and seed; the checker cannot redraw a seed. | proposed closure; construction unimplemented |
| M-01 / N-M03: 240-versus-320 hours | Plan §11.3 gives five nonoverlapping task-ledger rows summing exactly to the 240-hour aggregate. Each labor event belongs to one row and an overestimate stops the gate. | arithmetic proposed closure; practical sufficiency unvalidated |
| M-04 / N-M04: unauthorized transfers | Plan §§3.2-3.3 add label comparison, output custody/anonymization, judge comparison, comparator operation/comparison, condition-map custody, and a 21-step producer-artifact-recipient ledger. Executors write to a vault not readable by CONTROL; the map releases only after analysis freeze. | proposed closure; ACL enforcement unimplemented |
| N-M05: incomplete stochastic and elapsed metrics | Plan §§7.2 and 9.3 define standard-normal components, all indices, sharing/independence, probit thresholds, and midpoint/delta mappings. §12.3 defines elapsed as monotonic pre-send to durable final-byte receipt, pooling, median, ratios, bootstrap unit, and interval directions. | proposed closure; two-implementation reproduction required |
| N-m01: surrogate and property order | Candidate §9 rejects unpaired/reversed surrogate escapes, decodes valid pairs to one scalar, and enumerates complete response, answer, and decision member order plus mutations. | proposed closure |

## 3. Preserved authenticated passes and controls

- The prospective seed remains pre-bank and contains no bank hash; bank-hash seeds remain post-freeze only.
- Fit and audit streams remain separate, alpha and N selection remain precommitted, and statistical claims remain limited to audited grids.
- The nested prospective bootstrap remains removed; direct statistics, benchmark, CPU/RAM/storage/elapsed/cost stops, and no-inner-bootstrap rules remain.
- P2 rotation balance, immutable exact revision evidence, drift invalidation, concurrency three, first-output-only behavior, and no automatic retry remain.
- Call and visible-token arithmetic at N=720 remains 960 calls, 53,760,000 input tokens, and 3,194,880 output tokens.
- Fixed runner prose remains typed; semantic prose retains two independent reviewers; the mechanical leakage claim remains limited to enumerated syntax and provenance.
- NFC rejection, the full seven line-separator prohibition, raw-before-canonical validation, and no normalization rescue remain.
- P0-P4 remain noncompensatory. Changed hashes, forbidden material, role leakage, schedule/revision drift, invalid raw output, threshold changes, and post-result tuning stop the bank.
- Public, blinded adjudication, and sealed/private domains remain separate. Worktrees are not described as secret boundaries.
- Failure preserves authenticated protocol and review evidence, requires untouched material, and opens no later gate automatically.
- The maximum possible future-pass claim remains limited to the frozen synthetic bank, exact revision, audited grids, schedule, custody, ceilings, and algorithms.

The v0.6 16-row syntactic product is not silently retained as the complete semantic surface because doing so would leave Brain responsibility unobservable. Its exhaustive Cartesian/no-question-local-row principle is preserved in the explicit 24-row product, and every one of its 32 G=0 predicate vectors remains classified.

## 4. Unresolved feasibility and review risks

- The 24-row grammar may be harder for executors than v0.6's 16-row grammar.
- The restriction that relation groups are disjoint or exact aliases may make varied synthetic authoring impractical or distort realistic evidence relations.
- The finite overlap catalog may be large even with cardinality bounds; affordability has not been benchmarked.
- Exact independent agreement on owners, predicates, causes, closures, and relations may fail often.
- The C formulas and operational-strength function may still misclassify a hazard or overstate a bar.
- The explicit P2/P3 latent-normal families do not guarantee error control outside their audited grids.
- The direct simulation program may breach compute or seven-day ceilings.
- The 240-hour ledger and USD 3,000 total may be insufficient for the expanded isolated roles.
- Required ACLs, write-only vaults, exact model fingerprints, monotonic timestamp capture, and durable custody may be unavailable.
- Semantic-leakage reviewers or reason judges may disagree; disagreement remains failure.
- P4 percentile intervals are a bounded burden analysis, not the grid-calibrated P2/P3 error-control claim.

## 5. Bounded status

The three v0.7 files are public design proposals responding to authenticated v0.6 findings. They have not received independent review and do not establish defect closure as a fact.

No executable schema, synthetic bank, question, answer, fixture, oracle, code, comparator, runner, simulation, model call, measurement, sealed artifact, or S0 result was created or authorized. No result from E0 was requested or used. The only appropriate next action is a fresh public-only read-only independent review under a separate exact gate.
