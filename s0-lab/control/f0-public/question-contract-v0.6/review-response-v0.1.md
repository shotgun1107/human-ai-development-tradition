# URC-0.6 redesign response to authenticated v0.5 review v0.1

- status: **CONTROL author response; not an independent review or validation**
- source review: `urc-v0.5-independent-review-v0.1.md`
- proposed successors: `universal-response-contract-v0.6-candidate.md` and `public-falsification-plan-v0.3.md`
- gate: `F0-PUBLIC QUESTION CONTRACT V0.6 REDESIGN OPEN`
- excluded: implementation, public authoring, simulation, execution, sealed work, and S0 conclusions

## 1. Authenticated input record

Before redesign, CONTROL verified the assigned commit and branch and recomputed every available allowlisted sidecar:

| Input | Verified SHA-256 |
|---|---|
| S0-E0 boundary | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` |
| protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| URC-0.5 candidate | `d081f67861447616aa961ef75920c4f0c317fd13e3273bf1ef5bf36edb31d52f` |
| public falsification plan v0.2 | `e6288cdf9275644223ba65a418c029dd0878c157847a4ea426f029cc7c40a0ef` |
| v0.5 independent review v0.1 | `cffe6b6d9910b1a43b5fa07aa0152583e10429cdc94971d8dc27ccd79adda359` |

This response relies only on those public inputs and `AGENTS.md`. It does not rely on repository history, E0 content, sealed/private/oracle material, other reviews, web sources, fixtures, or results.

## 2. Defect-closure map

“Proposed closure” means the successor text contains a mechanical rule addressing the finding. It does not mean the correction has passed review, implementation, or a test.

| Review finding | Proposed closure in v0.6 | Author assessment |
|---|---|---|
| B-01 total function contradicts positive routes | Candidate §§3.2-3.5 replace the exclusive handling enum with two independent route flags, define sixteen rows, and enumerate all 32 C/A/B/H/D vectors. Every positive H/D bit remains present. `A and B` resolves to explicit conflict rather than arbitrary precedence. | proposed closure; needs hostile review |
| B-02 format/semantic cascade | Candidate §§4.2-4.3 version classes 1-3 as suite-invalid, class 4 as M5, and make semantic atoms field-locally available. An invalid decision field has no false D atom. Plan §12.1 fixes P3/P4 consequences. | proposed closure; mutation verification required |
| B-03 qualitative C mapping | Candidate §§5-8 freeze closed metadata components, consistency identities, strength ordering, C1-C7 Boolean formulas, source selectors, consumption, and all 128 hazard masks. No author-selected primary code or source set exists. | proposed closure; metadata sufficiency and formulas remain reviewable |
| B-04 circular power seed | Plan §§4 and 8 create an immutable pre-bank manifest and use only its hash, N, grid, phase, and simulation version for prospective seeds. Bank-hash seeds begin only after bank freeze. | proposed closure |
| B-05 uncalibrated nominal intervals | Plan §§7.4 and 9.3 fit and independently audit boundary-null critical constants at every authorized dependence-grid point before power and N selection, with Clopper-Pearson Monte Carlo safeguards. Claims are explicitly grid-limited. | proposed closure; not a distribution-free guarantee |
| B-06 semantic prose called mechanical | Candidate §10 uses closed typed generation for codebook/common instructions, requires two independent pre-signing semantic reviewers for question prose, and narrows scanners to syntactic/provenance claims. | proposed closure; semantic review remains human/model judgment |
| M-01 infeasible nested simulation | Plan §§7.5, 9.3, and 11.1 use direct studentized dataset statistics with no inner bootstrap, require a frozen benchmark, and impose CPU, RAM, storage, elapsed, and compute-cost ceilings before authoring. | proposed closure; feasibility intentionally unknown until a later gated benchmark |
| M-02 unbalanced schedule and drift | Plan §10.2 defines P2 rotations and P3 grammar/representation rotations in bounded concurrency waves; §10.3 requires immutable revision evidence, load records, a seven-day window, and pre-semantic invalidation for drift events. | proposed closure |
| M-03 invalid-cell conflict | Candidate §4.2 and plan §§9.2 and 12.1 distinguish technical absence, transport invalidity, unparsable, parseable schema-invalid, semantic-wrong, and correct outputs. Parseable schema-invalid yields P3 Y=0/P4 schema=0; the first three invalidate the suite. | proposed closure |
| M-04 role contracts deferred | Plan §3 freezes per-role allowlists, explicit denylists, ancestry, outputs/transfers, and ACL storage boundaries; it expressly rejects worktrees as secret boundaries. | proposed closure; later operational enforcement still required |
| m-01 NFC/line ambiguity | Candidate §9 fixes raw size/BOM/UTF-8/parse/NFC/schema/canonicalization order, rejects rather than normalizes non-NFC input, and enumerates U+000A, U+000B, U+000C, U+000D, U+0085, U+2028, and U+2029. | proposed closure |

## 3. Preserved constraints

- Facts, CONTROL inferences, and proposals remain separately labeled.
- Public design, blinded public adjudication, and sealed/private material remain separate. No sealed input or hidden oracle is authorized or created.
- P0-P4 are noncompensatory; post-result tuning requires a new version and untouched bank.
- Changed hashes, leakage, role violations, schedule/model drift, technical invalidity, and resource breaches stop the suite.
- Call, visible token, human, elapsed, storage, simulation-compute, and monetary ceilings are explicit.
- Failure rolls back to the unchanged authenticated protocol and review evidence; it does not revive v0.5 or open another gate.
- The maximum future-pass statement is limited to the frozen synthetic public bank, revision, grids, schedule, ceilings, and algorithms.

## 4. Unresolved risks requiring fresh review

- The sixteen-row grammar may be cognitively harder than the rejected five-row grammar even though it is semantically total.
- The exact critical formulas may still omit a relevant record relation or encode an undesirable decision-strength concept.
- Exact independent metadata agreement may be impractical on varied synthetic questions.
- Finite-grid null calibration does not establish coverage outside the authorized latent-dependence families.
- The proposed direct simulation count may still fail the benchmark and resource ceilings.
- An immutable provider revision/fingerprint may be unavailable, which would prevent the confirmatory test from starting.
- Independent semantic-leakage and reason judges may disagree; the design treats disagreement as failure rather than resolving it.
- P4 percentile intervals remain a bounded burden analysis, not the P2/P3 grid-calibrated error-control claim.

## 5. Bounded status

The v0.6 files are public design proposals authored in response to the authenticated v0.5 findings. They have not received independent review and do not establish defect closure as a fact.

No executable schema, fixture, public bank, question, answer, oracle, code, comparator, runner, simulation, model call, measurement, sealed artifact, or S0 result was created or authorized. The only appropriate next action is a fresh public-only read-only independent review under a separate exact gate.
