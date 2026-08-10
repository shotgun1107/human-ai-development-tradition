# S0 v0.14 trust-root and role-isolation v0.4 independent-review brief

- `status`: bounded public-design review candidate
- `review_kind`: fresh public-only hostile limited review
- `review_scope`: v0.4 repairs for `TRI2-M01` and `TRI2-m01` plus non-regression
- `review_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 INDEPENDENT REVIEW OPEN`
- `claim_kind`: CONTROL integration consideration only

## 1. Reviewer independence

The reviewer must be a fresh session that did not author or advise on the v0.4
candidate, did not run author-side QA, and does not inherit another v0.4
reviewer conclusion. The reviewer must not use a subagent.

The authenticated v0.3 full rereview establishes the predecessor finding
boundary but is not an answer key. The reviewer must independently reconstruct
the v0.4 composition and may report any regression introduced by v0.4. No
sealed material, oracle, fixture, condition map, executor output, E0 material,
or unlisted repository source may be read.

Use a separate clean worktree at the exact candidate commit. Worktree
separation is edit isolation, not secrecy or independent information security.

## 2. Authenticated handoff contract

CONTROL must supply outside this self-referential brief:

- exact repository and worktree path;
- branch, candidate commit, tree, sole parent, and parent tree;
- an exact path/SHA-256 manifest for every allowed input, including this brief
  and its sidecar; and
- the exact output directory.

The review may start only after the user separately opens the exact
`review_gate` above.

The candidate must be one direct child of
`81a32c97dc9f1e50d742dd009034ac678ff66494`. The parent is the authenticated
v0.3 rereview-result commit. Parent-to-candidate tracked diff must add exactly
the five v0.4 Markdown files below and their five same-basename sidecars, with
no modification or deletion:

1. `trust-root-role-isolation-design-revision-v0.4.md`;
2. `identity-authority-matrix-addendum-v0.4.md`;
3. `isolation-acceptance-plan-addendum-v0.4.md`;
4. `review-response-v0.3.md`; and
5. this brief.

Any other parent, merge, changed predecessor, extra tracked path, missing
sidecar, hash mismatch, dirty initial state, or manifest ambiguity makes the
review `INVALID-REVIEW` before substantive analysis.

## 3. Maximum input set

CONTROL may supply only the exact current versions of these public files and
their same-basename sidecars where present:

1. repository-root `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. `s0-lab/control/s0-protocol-v0.3-canonical-r1.md`;
4. `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md`;
5. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md`;
6. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md`;
7. `s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md`;
8. `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.md`;
9. `s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.md`;
10. `s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.md`;
11. `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/trust-root-role-isolation-design-v0.3-independent-rereview.md`;
12. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md`;
13. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md`;
14. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md`;
15. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/review-response-v0.3.md`;
16. `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-independent-review-brief-v0.4.md`;
17. `s0-lab/i1/spec/public-runtime-v0.14.json`;
18. `s0-lab/i1/spec/public-runtime-files.sha256`;
19. `s0-lab/i1/verification/implementation-files.sha256`; and
20. `s0-lab/i1/verification/implementation-manifest.sha256`.

With same-basename sidecars for the 14 Markdown pairs, this maximum set is
exactly 34 paths: 28 pair paths plus six file-specific inputs.

Authenticate every supplied byte before relying on it. The official validator
must pass SelfTest before validating every admitted Markdown/sidecar pair.
The four file-specific I1 inputs may be parsed or checked read-only only to
reproduce public counts and cross-bindings. Broad search, sealed paths,
implementation code outside those four inputs, old invalid-review output,
advisory notes, and any unlisted file are forbidden.

Official primary references directly linked by an admitted candidate may be
opened only to check the general encoding statement actually attributed to
that reference. They cannot supply or validate a replacement vector under this
gate.

## 4. Read-only review boundary

This is a public tabletop document review. Do not provision a host, VM,
sandbox, account, network, ACL, vault, store, signer, ledger, witness, medium,
or provider. Do not create or execute a schema, parser, vector, key, anchor,
registry, signature, fixture, oracle, model call, acceptance harness, E0 test,
or S0 test. Do not perform point decoding, scalar multiplication, order
checking, or cryptographic-vector construction.

Canonical text validation, hashing, Git inspection, JSON parsing, manifest
checks, and manual paper traces are integrity or design-review evidence only.
The reviewer may write only the authorized review Markdown and sidecar. Do not
modify candidate files, commit, push, merge, open a PR, or prepare
implementation.

## 5. Required independent reconstruction

Without trusting the author response, reconstruct:

1. the exact v0.4 overlay against the authenticated effective-v0.3 baseline
   and its replacement map, proving that v0.4 claims no change outside the two
   open findings;
2. all 31 import-event fields in exact order, with one occurrence each, the
   sole schema/version value, exact ASCII/LF byte contract, and event-hash
   preimage;
3. the distinction between global namespace chaining and route-local event-ID
   chaining;
4. immutable route bindings, admission/media zero-to-frozen values, and the
   exact event-ID mapping for `R`, `A`, `P`, and `C`;
5. every class-specific `SRC` and `DST` and all lifecycle rows, especially
   direct terminal from reserved and admission-frozen;
6. the complete-frame hash rule for accepted, explicit rejection,
   state-commit failure, crash, missing, duplicate, and both disagreement
   subcases;
7. authority separation among host preflight, target TCB service, post-run
   classification, and atomic ledger/witness append;
8. absence of a frame/event hash cycle, replacement completion, or retry;
9. full withdrawal of v0.3 `TRI2-VEC-01` coordinates, relation, and literals
   from effective authority;
10. byte-for-byte preservation of the inherited `S0-ED25519-STRICT-1` profile;
11. the future `TRI2-VEC-02` fail-closed prerequisites and the fact that no
    vector or point-order claim exists now; and
12. every frozen count, topology, A-D opportunity, signature-scope,
    ledger-namespace, provider, implementation, protected-material, E0, and S0
    invariant.

## 6. Mandatory hostile tabletop cases

At minimum, trace:

- old common-schema or additive-block parsing, duplicate `result_media_id`, a
  second version field, 30 or 32 fields, reordering, extra/missing line, CR,
  BOM, NUL, trailing whitespace, or missing final LF;
- a wrong global predecessor hash with a correct route predecessor and the
  converse;
- each lifecycle record with the wrong event ID, prior route ID,
  admission/media tuple, frame hash, outcome, before/after state, terminal
  source, or decision;
- both pre-pending terminal variants with invented appliance-state evidence;
- pending with `before=none` or a known after-state;
- consumed without exact accepted frame and durable append;
- explicit rejection with changed state, state-commit failure with a known
  after-state, or crash/missing/duplicate with a claimed frame hash;
- disagreement with a hash for malformed or non-unique bytes, or zero hash for
  one uniquely selectable canonical but conflicting frame;
- cross-signer, cross-class, cross-package, cross-campaign, capability, medium,
  event-ID, or route-field substitution;
- early terminal followed by reuse of unused IDs, completion conflict followed
  by redraw, append failure followed by reconstructed success, and any retry;
- treating the unsigned frame/event as a signature, signer, registry authority,
  experimental topology object, or fourth ledger;
- any attempt to keep one old coordinate or literal authoritative, use the
  withdrawn table as evidence, treat missing future vectors as a pass, weaken
  the strict predicate, or claim point-order validation; and
- any count, fairness, signature-scope, closed-gate, or claim-limit regression.

Every mutation must map to one exact fail-closed rule. An unhandled or multiply
interpreted mutation is a finding.

## 7. Finding-specific closure criteria

### 7.1 `TRI2-M01`

Pass only if one and only one byte serialization exists for every import-event
state, all 31 fields and the hash preimage are exact, the two pre-pending
terminal records are complete, frame-hash selection is deterministic, both
chains are enforced, and no new authority or retry path appears. The
non-root-request and root-ceremony schemas must remain unchanged.

### 7.2 `TRI2-m01`

Pass only if no v0.3 coordinate, complement relation, or literal retains
effective authority; the false RFC 9381 attribution remains absent; the full
strict profile remains unchanged; key generation fails closed until four new
distinct literals and all construction/decode/re-encode/order/rejection
evidence are independently frozen; and the candidate makes no vector or point-
order result claim. The reviewer must decide whether withdrawal plus blocking
is a safe closure; the author response cannot decide it.

## 8. Severity and verdict

- `blocking`: protected-asset exposure, lost reviewer/A-D independence,
  forgeable or circular authority, frozen-topology contradiction, or a repair
  requiring a closed implementation gate to be treated as complete;
- `major`: required bytes, state, event, hash, authority, failure, blocker, or
  nonclaim remains ambiguous or incomplete; and
- `minor`: bounded public-text exactness defect that cannot grant authority,
  weaken isolation, alter experimental meaning, or hide failure.

Allowed verdicts are exactly:

- `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any finding exists; or
- `INVALID-REVIEW`: baseline, input, hash, validator, boundary, independence,
  or evidence validity failed.

No verdict automatically opens CONTROL integration or any later gate.

## 9. Required output and next authority

Write exactly one review Markdown and same-basename `.sha256` under:

`s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/`

The Markdown basename is:

`trust-root-role-isolation-design-v0.4-independent-review.md`

State independence, Git baseline, every authenticated input, validation
results, effective composition, both finding reconstructions, hostile traces,
non-regression, finding counts, exact verdict, maximum claim, and evidence
limits. Rehash every input after writing and confirm Git status contains only
the two authorized output files.

A valid zero-finding verdict permits CONTROL to decide separately whether to
open the following exact gate:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 CONTROL INTEGRATION DECISION OPEN`

The verdict does not open that gate itself and never opens implementation,
vector authoring, key generation, E0, S0, or `main` integration.
