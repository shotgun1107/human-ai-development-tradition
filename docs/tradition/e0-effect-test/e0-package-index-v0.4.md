# E0 effect-test package index v0.4

- Status: `revision proposal — awaiting fresh independent read-only review`
- Baseline: `central-system-v2.1-s0-preparation`
- Exact open gate for this revision: `E0 EFFECT TEST DESIGN V0.4 REVISION OPEN`
- Source ancestry: `codex/e0-effect-test-design-v03` at `d172bc723d35978d322caef718e5bdaa78ef1445`
- Authority: this is the versioned entry point for the v0.4 review packet only.
- No authority: representation selection, material or oracle creation, staffing commitment, budget approval, prompt, schema, runner or code creation, model calls, simulation, scoring, execution, effectiveness or safety findings, economic claims, or any later gate

## Current package

Read the v0.4 proposal in this order.

| Document | Role |
|---|---|
| [e0-effect-test-design-v0.4.md](./e0-effect-test-design-v0.4.md) | Causal design, single representation reference, transfer boundary, lifetime Q-exposure and full-pair restart rules, safety and blinding |
| [e0-measurement-and-analysis-plan-v0.4.md](./e0-measurement-and-analysis-plan-v0.4.md) | Endpoint-specific family sets and counts, estimands, nulls, vector power, adjudication and failure-closed analysis |
| [e0-operating-cost-and-gates-v0.4.md](./e0-operating-cost-and-gates-v0.4.md) | Lifecycle staffing, four-bucket human-resource propagation, fixed-overhead allocation, all-call ceilings, gates and rollback |
| [e0-revision-response-v0.4.md](./e0-revision-response-v0.4.md) | v0.3 F-01/F-02/F-03 closure map, preserved corrections and unresolved feasibility |
| [e0-independent-review-brief-v0.4.md](./e0-independent-review-brief-v0.4.md) | Maximum input packet and noncompensatory rubric for a new fresh review |
| `e0-package-index-v0.4.md` | This status and package entry point |

Every Markdown file above requires a same-basename `.sha256` sidecar. A sidecar authenticates bytes only; it does not approve the design.

## Relationship to frozen earlier versions

The unversioned [README.md](./README.md) is the frozen historical v0.1 entry point and remains unchanged. Its current authenticated byte identity for the v0.4 review packet is:

| Current-HEAD file | SHA-256 |
|---|---|
| `README.md` | `22d2297b429ebe1ee8d62526c573ed836df5a0a8cffb9bf274fe760b4e68fd29` |

The four v0.1 design Markdown files, all v0.2 files and all v0.3 files also remain frozen and unchanged. The v0.4 independent-review brief explicitly allowlists the four current v0.1 Markdown files, `README.md`, and every available same-basename sidecar so the fresh reviewer can bind each current byte sequence to the supplied reviewed branch and HEAD and record its exact SHA-256 without repository-history access. Author assertions alone do not establish immutability.

The authenticated v0.3 independent review ended in `REVISE-AND-REVIEW`. This package proposes mechanical corrections for its F-01 through F-03. The existence of these files is not a review pass.

## Bounded status

The only current claim is:

> E0 v0.4 is a design-only revision proposal that awaits a new fresh hostile read-only review.

It does not establish S0 or E0 success, a selected representation, material readiness, staffing or budget feasibility, implementation or execution, safety, economic or real-project value, central-system or Project Brain validity, model learning, persistence, or model-to-model transfer.
