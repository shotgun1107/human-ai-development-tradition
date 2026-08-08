# URC-0.5 public falsification plan v0.2

- status: **public test-design proposal awaiting independent review**
- governed candidate: `URC-0.5-CANDIDATE`
- permitted future data: newly authored synthetic public material only
- prohibited: sealed or hidden-oracle material, real/customer/personal/secret/past-project material
- current gate: design only; no bank, labels, schemas, implementation, sessions, measurements, or validation claims

## 1. Purpose and noncompensatory rule

This plan is designed to reject URC-0.5 before it can influence any sealed work. It does not test whether A-D differs in S0 and does not validate a central or tradition system.

URC-0.5 may advance beyond public validation only if every P0-P4 and equality gate passes under artifacts, thresholds, analysis algorithms, and ceilings frozen before confirmatory data. Results cannot compensate across gates. Any post-result change creates a new contract or test version and requires an untouched bank.

## 2. Facts, inferences, and proposals

### Verified predecessor facts

- v0.4 proposed 180 balanced questions, two original observer streams, neutral-token variants, a single-code P3 control, and a noncompensatory decision table.
- Independent review verified the v0.4 33-of-180 calculation for the original two-stream 97.5% Clopper-Pearson rule.
- The review rejected the full P2 design because four blocking ceiling streams did not share a complete familywise allocation and the paired five-point rule was not an equivalence test.
- The review rejected P3 because the control, estimator, session unit, covariance assumptions, resampling, confidence interval, and sample escalation were open.
- No public bank or result exists.

### CONTROL inferences

- Grouping questions in matched packets can reduce calls while keeping the packet/session dependency explicit.
- A packet-cluster analysis is more defensible than treating questions in one model session as independent.
- A deterministic maximum sample and stop-before-authoring ceiling are necessary because power-driven expansion otherwise creates open-ended cost.

### Proposals

All hypotheses, allocations, algorithms, topology, simulation assumptions, and ceilings below are pre-review proposals. Numerical ceilings state when not to start; they do not show that the design is affordable or powered.

## 3. Roles, bank, and freeze order

Later exact gates must create mutually isolated public fact authors, independent label authors A and B, prompt-leakage observers, representation builders, two comparator builders, public executors, public judges, and CONTROL. Labels remain outside executor-visible workspaces. Worktrees alone are not secret isolation.

The confirmatory bank size `N` must:

- be balanced equally over the five response rows;
- contain no development or worked-example material;
- have no duplicated scenario template with nouns changed;
- be chosen by section 8 before fact authoring;
- be a multiple of 120, so five-row balance, 12-question P2 packets, and 8-question P3 packets are exact;
- be no smaller than 240 and no larger than 720.

Freeze order:

1. Independently review URC-0.5 and this plan.
2. Freeze authoring protocol, role allowlists, canonical serializer, runner visibility checks, analysis algorithms, simulation implementation, seeds, ceilings, and selected `N`.
3. Author canonical public facts and prompts.
4. Label authors work independently; both bundles are hashed before comparison.
5. Reject the whole bank version unless every predicate, row, citation clause, affected set, uncertainty value, and standardized hazard relation agrees exactly.
6. Freeze A-D public representations, the single-code control, runner manifests, and anonymization map.
7. Freeze the comparator mutation specification and two implementations.
8. Run P0-P2; run P3-P4 only if earlier blocking gates pass.
9. Freeze anonymous findings before CONTROL receives condition identity, timing, or cost.

An item is never silently dropped or edited after either label bundle or confirmatory output is visible.

## 4. P0 — static coherence and visibility

Two independent reviewers and, where specified, two independent scanners must agree exactly that:

- exactly the five URC rows and no other pairs are accepted for every question;
- the ordered rule maps every boolean predicate vector to one row;
- the combined-record traces and a frozen adversarial mutation set have one result without prompt hints or prose repair;
- response contract, codebook, question hashes, schema, model opportunity, and limits are equal across A-D;
- one wrong decision object yields one false `D` token, not coordinate events;
- every C1-C7 and M1-M6 source observation in the v0.5 preservation table is emitted;
- the observation-consumption tree never consumes one false token twice and never suppresses a disjoint false token;
- no author-selected primary error code exists;
- both canonical serializers produce identical bytes and hashes at every boundary case;
- both runner-package scanners pass every valid package and reject every answer-bearing mutation required by the v0.5 visibility predicates;
- maximally populated authorized canonical responses remain at most 7,680 bytes and raw responses over 8,192 bytes are rejected.

P0 requires 100% agreement. One ambiguity, seventh result, lost predecessor observable, scanner difference, or serializer difference fails the contract version.

## 5. P1 — independent labels and adjudication determinism

For all `N` questions, label authors independently produce the record-derived predicate vector and supporting IDs, the resulting row, citation clauses and complete allowed set, affected set, uncertainty, and all standardized hazard relations. They do not select C/M codes.

Pass requires exact normalized agreement on every discrete value for all `N` questions. A chance-corrected statistic may be reported but cannot replace exact agreement.

Two fresh public judges then apply the frozen adjudication specification to a frozen mutation set containing, at minimum:

- every valid and invalid decision pair;
- every combined-record predicate combination;
- every single false F/D/E/A/U/R token;
- every C1-C7 predicate with each permitted source-token pattern;
- overlapping critical predicates that share a token;
- disjoint critical and major failures;
- repeated same-code events within a block;
- malformed and raw-byte-boundary responses.

Pass requires byte-identical tokens, consumed-token sets, events, diagnostics, and block totals between judges. One difference fails P1.

## 6. P2 — no-record leakage and neutral-token equivalence

### 6.1 Topology and observations

There are two independently prompted observer identities `O1` and `O2` and two prompt variants `original` and `neutral`. Each of the four streams receives the complete runner-visible prompt, codebook, question projection, and structural contract but no records, record metadata, labels, row frequencies, other batches, outputs, or answer-bearing examples.

Each stream uses `N/12` fresh, one-turn sessions. A session predicts the exact response row for one frozen packet of 12 questions. The original and neutral versions use matched packets and order but separate fresh sessions; no output or memory is shared. Observers never see the full-bank balance.

For stream `(o,v)`, `p[o,v]` is exact-row accuracy. For observer `o`, the paired neutral sensitivity is:

`delta[o] = p[o,original] - p[o,neutral]`.

The resampling unit is the matched 12-question packet. All 24 binary correctness values for an observer's original/neutral packet remain together.

### 6.2 Complete blocking hypothesis family and alpha allocation

The overall familywise type-I budget is `0.05` across six blocking claims.

Four leakage-ceiling claims use:

- `H0-L[o,v]: p[o,v] >= 0.25`;
- `H1-L[o,v]: p[o,v] < 0.25`;
- one-sided alpha `0.00625` for each of four streams.

Two paired-equivalence claims use:

- `H0-E[o]: delta[o] <= -0.05 or delta[o] >= +0.05`;
- `H1-E[o]: -0.05 < delta[o] < +0.05`;
- TOST claim-level alpha `0.0125` for each observer.

Bonferroni control is `4 * 0.00625 + 2 * 0.0125 = 0.05`. Each equivalence claim is one union-null test; its two one-sided tests both use the claim-level alpha.

### 6.3 Deterministic cluster-bootstrap intervals

For each analysis, resample the `K=N/12` matched packet indices with replacement, retaining every question and applicable stream in a selected packet. Use 200,000 replicates from `PCG64-DXSM`. The seed is the unsigned 128-bit integer represented by the first 32 hexadecimal digits of SHA-256 over the ASCII string:

`URC-0.5|P2|<frozen-bank-hash>|<analysis-id>`.

Sort replicate estimates ascending. Quantile `q` is the value at one-based rank `ceil(q * 200000)`, clamped to ranks 1 through 200000.

- For each leakage stream, the one-sided upper bound is quantile `0.99375`; pass only if it is strictly below `0.25`.
- For each observer's `delta`, the two-sided 97.5% percentile interval uses quantiles `0.0125` and `0.9875`; pass only if the complete interval is strictly inside `[-0.05,+0.05]`.

The strict rule makes a boundary value fail. Original and neutral results are never pooled to rescue a stream.

### 6.4 P2 prospective power model

Power is simulated jointly for all six claims. For observer `o`, variant `v`, packet `k`, and question `q`, generate latent correctness:

`Z[o,v,q] = mu + sqrt(rho_q)*Q[o,q] + sqrt(rho_s)*S[o,v,k] + sqrt(1-rho_q-rho_s)*E[o,v,q]`;

`Y[o,v,q] = 1` when `Z[o,v,q] > 0`.

All latent variables are independent standard normal except that `Q[o,q]` is shared by the two variants for the same observer/question. `mu = Phi_inverse(p)`, so each marginal accuracy is `p` and true `delta` is zero. O1 and O2 are independent.

The required grid is the Cartesian product:

- `p` in `{0.18, 0.20}`;
- `rho_q` in `{0.20, 0.40, 0.60}`;
- `rho_s` in `{0.00, 0.10, 0.20}`;

excluding combinations where `rho_q + rho_s >= 1`. For every grid point, 100,000 simulated full P2 datasets are analyzed by the exact section 6.3 algorithm. Power is the fraction in which all six claims pass. The P2 power requirement is at least 80% at every grid point.

The simulation seed follows section 6.3 with analysis ID `power-<N>-<grid-id>`. These assumptions are proposals about public-test operating behavior, not measurements; failure of sensitivity-grid power prevents the test from starting.

### 6.5 P2 blocking conditions

P2 fails if any one confidence rule fails, any prompt contains decisive qualification or asymmetric answer material, row frequency is exposed, or any stream/session boundary is violated. A pass would reject only the precommitted large-leakage and neutral-sensitivity nulls for this bank and observer design.

## 7. P3 — representation-alignment equivalence

### 7.1 Exact single-code control

The control carries exactly the same five semantic rows as URC-0.5. Its only decision field is `outcome_code`, accepting the opaque equal-length strings `K01` through `K05`. Before bank authoring, a seed-derived permutation maps those five codes one-to-one to R01-R05. The control codebook presents all five codes in code order with the complete row meanings; it contains no scenarios, frequency, recommendation, or condition language.

The control and URC envelopes are otherwise identical: same contract/version placement, block and input hashes, question order, citations, affected IDs, uncertainty, reason obligation, ID limits, canonicalization, raw byte limit, authority, model, tools, and one-turn/no-repair policy. The control replaces only the two-field `decision` object with `outcome_code`. Its schema may not use defaults, examples, per-question narrowing, or annotations selecting a code.

The mapping permutation is the Fisher-Yates result using `PCG64-DXSM` seeded by the first 128 bits of SHA-256 over:

`URC-0.5|P3-control-map|<contract-hash>|<plan-hash>`.

This control is a measurement artifact only. It is not a successor candidate and cannot be used for sealed authoring without a separate gate.

### 7.2 Session and allocation unit

Each grammar is crossed with all four neutral public representation forms A-D. Questions are grouped into `N/8` frozen matched packets of eight. For each packet, eight fresh one-turn sessions are created: two grammars times four representations. A session answers only its assigned eight-question packet and receives no feedback, other grammar, representation, packet, or output.

The session unit is `grammar x representation x packet`. The analysis/resampling unit is the matched packet containing all 64 correctness observations: eight questions times eight cells. This explicitly preserves within-session dependence and the paired question structure.

### 7.3 Estimator

Let `Y[q,g,r]` be exact structured-decision correctness for question `q`, grammar `g`, and representation `r`. Define:

`gap[g] = mean_q((Y[q,g,C]+Y[q,g,D]-Y[q,g,A]-Y[q,g,B])/2)`;

`theta = gap[URC] - gap[CONTROL]`.

Every bank question has equal weight. First outputs only are used. Missing or invalid cell results invalidate P3; they are not imputed.

### 7.4 CI and equivalence decision

Use a paired packet-cluster percentile bootstrap with 200,000 replicates. Resample the `N/8` packet indices with replacement and keep each selected packet's 64 observations together. Compute `theta` in every replicate.

Use `PCG64-DXSM`, the quantile rule in section 6.3, and seed string:

`URC-0.5|P3|<frozen-bank-hash>|alignment-ci`.

The two-sided 90% interval uses quantiles `0.05` and `0.95`. P3 passes only if its lower endpoint is strictly greater than `-0.10` and its upper endpoint is strictly less than `+0.10`. A nonsignificant difference is not a pass.

### 7.5 Joint covariance and prospective power model

For question `q` in packet `k` and cell `c=(g,r)`, simulate:

`Z[q,c] = mu[c] + sqrt(rho_q)*Q[q] + sqrt(rho_s)*S[k,c] + sqrt(1-rho_q-rho_s)*E[q,c]`;

`Y[q,c] = 1` when `Z[q,c] > 0`.

`Q`, `S`, and `E` are mutually independent standard normal variables. `Q[q]` is shared over all eight cells for a question; `S[k,c]` is shared by the eight questions in one model session; residuals are cell-specific. Set `mu[c]=Phi_inverse(p[c])`. Under the simulated equivalence truth, both grammars use identical cell marginals and therefore `theta=0`.

Power must be checked over the full Cartesian grid:

- A/B marginal accuracy `p_low` in `{0.55,0.65,0.75}`;
- common structured gap `p_high-p_low` in `{0.00,0.10,0.20}`, excluding `p_high > 0.95`;
- `rho_q` in `{0.10,0.30,0.50}`;
- `rho_s` in `{0.00,0.10,0.20}`;

excluding `rho_q+rho_s >= 1`. Set A and B to `p_low`, C and D to `p_high` for both grammars. For each grid point, simulate 100,000 full datasets and apply the exact section 7.4 algorithm. Power is the proportion whose 90% interval lies strictly within the equivalence margins. Required power is at least 80% at every grid point.

Seeds follow `URC-0.5|P3-power|<N>|<grid-id>`. Expected accuracy alone is explicitly insufficient; the full marginal/covariance grid controls sample selection.

## 8. Deterministic smallest-sufficient sample rule

The authorized sample selector evaluates candidate sizes `N = 240, 360, 480, 600, 720` in ascending order. For each `N`, it runs every P2 and P3 power grid exactly as specified, using the frozen simulation implementation and seeds.

Select the first `N` for which:

1. every P2 grid point has joint six-claim power at least 80%; and
2. every P3 grid point has equivalence power at least 80%.

Monte Carlo uncertainty is handled non-discretionarily: for each reported power, the one-sided 99% Clopper-Pearson lower confidence bound over the 100,000 simulation results must be at least 0.80. The raw proportion alone is insufficient.

If no candidate through 720 satisfies both requirements, the public confirmatory test does not start. The margin, covariance grid, CI, estimator, or power threshold may be changed only in a newly reviewed plan version, never to force a fit under the ceiling. `N` cannot be reduced after selection.

## 9. P4 — comparator reliability and executor burden

Two independently implemented comparators must run the frozen mutation set 100 times each. Pass requires byte-identical normalized tokens, events, consumed-token sets, diagnostics, and final results over all 200 runs.

Executor burden uses the first P3 outputs and compares URC with the single-code control. Every condition must pass:

- at least 95% of URC responses are schema-conforming first outputs;
- URC success is no more than 3 percentage points below control;
- maximum minus minimum URC schema-success across A-D is at most 5 points;
- median elapsed time is no more than 20% above control;
- median raw output bytes are no more than 20% above control;
- every valid canonical response is at most 7,680 bytes;
- every raw response is at most 8,192 bytes;
- no answer requires more than four cited or affected IDs.

Use the matched P3 packet as the resampling unit and the section 6.3 bootstrap/quantile algorithm with 200,000 replicates. The seed string is `URC-0.5|P4|<frozen-bank-hash>|<metric-id>`. Use two-sided 95% percentile intervals for all five threshold statistics. Pass only when: the URC schema-success lower endpoint is at least 0.95; the URC-minus-control success-difference lower endpoint is at least -0.03; the A-D URC success-range upper endpoint is at most 0.05; the URC/control pooled-median elapsed-time ratio upper endpoint is at most 1.20; and the corresponding raw-byte ratio upper endpoint is at most 1.20. A boundary is allowed only where this sentence says `at least` or `at most`. Resource outcomes cannot rescue P0-P3.

## 10. Explicit operating ceilings

These are stop-before-authoring ceilings for one complete confirmatory suite at the maximum `N=720`. There is no individual-call retry and no automatic whole-suite retry.

### 10.1 Calls and sessions

| Component | Formula | Maximum calls |
|---|---:|---:|
| P2 | `2 observers * 2 variants * (N/12)` | 240 |
| P3/P4 first outputs | `2 grammars * 4 representations * (N/8)` | 720 |
| **Total** | `4N/12 + 8N/8` | **960** |

Comparator runs, serialization checks, and simulations are local deterministic computations and are not model calls. A technical failure after a confirmatory input is revealed invalidates the affected suite and requires a new user gate and new cost approval; it does not enlarge 960.

### 10.2 Token ceilings

| Component | Per-call input | Per-call output | Maximum aggregate input | Maximum aggregate output |
|---|---:|---:|---:|---:|
| P2 | 32,000 tokens | 1,024 tokens | 7,680,000 | 245,760 |
| P3/P4 | 64,000 tokens | 4,096 tokens | 46,080,000 | 2,949,120 |
| **Total** | — | — | **53,760,000** | **3,194,880** |

Any provider-side cached or reasoning tokens must be reported separately and included in monetary preflight. They do not allow the visible input/output ceilings to increase.

### 10.3 Human and elapsed time

- aggregate human labor ceiling: 240 hours;
- single CONTROL operator coordination ceiling: 80 of those hours;
- public fact authoring and cleanup: 60 hours;
- two label streams combined: 80 hours;
- two review/judge streams combined: 40 hours;
- implementation, scan, analysis, and incident reserve: 60 hours;
- wall-clock ceiling from authoring start through frozen decision: 30 calendar days;
- each model session: 15 minutes maximum;
- maximum concurrent model sessions: 3.

Role separation may require several people or isolated agents; the 240-hour ceiling is aggregate and does not imply one person may occupy incompatible roles.

### 10.4 Monetary ceiling

Before authoring, CONTROL must price the selected model revision, all input/output/cached/reasoning tokens, required compute, storage, and paid reviewer labor at then-current rates. The signed preflight estimate must include a 20% contingency and be no more than **USD 3,000 equivalent**. Any later price change that makes the frozen estimate exceed the ceiling stops the test before the next paid action. Internal uncompensated human time is still reported under section 10.3 and cannot be hidden as zero cost.

Exceeding any call, token, human-time, elapsed-time, or monetary ceiling stops the suite without a scientific pass claim. A cheaper pilot cannot contribute questions, labels, thresholds, power, or results to the confirmatory suite.

## 11. Equality, stopping, and interpretation

Before execution, A-D must have exact equality of canonical facts, question projection and order, response contract, grammar assignment opportunity, model ID and fixed revision, reasoning level, authority, tools/network state, turn count, retry opportunity, time and output limits, and anonymous adjudication fields. Only the intended representation differs.

Stop immediately for a changed frozen hash, sealed or forbidden material, label/example leakage, forbidden role input, undeclared runner file, threshold change, missing P3 cell, or ceiling breach. Preserve a public incident record but do not reuse the affected bank.

Even a complete pass would support only this bounded statement:

> Under the frozen synthetic public bank, model revision, observers, representations, control, packet topology, resource ceilings, and analysis algorithms, URC-0.5 did not cross the precommitted public rejection thresholds.

It would not prove zero leakage, universal semantic coverage, sealed compatibility, representation superiority, S0 success, production readiness, operational safety, economic value, central-system effectiveness, Project Brain integration, model stability, or model-to-model transfer.
