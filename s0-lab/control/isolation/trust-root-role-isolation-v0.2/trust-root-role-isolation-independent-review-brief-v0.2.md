# S0 v0.14 trust-root and role-isolation independent-review brief v0.2

- `status`: design revision candidate
- `review_kind`: fresh public-only hostile design rereview
- `claim_kind`: CONTROL integration consideration only

## 1. Reviewer independence

The reviewer must be a fresh session that did not author v0.1, v0.2, an
implementation derived from either, or an advisory QA result about v0.2. The
reviewer must not have read sealed material, oracle, bank, labels, condition
map, executor output, E0, or another v0.2 reviewer conclusion.

The authenticated v0.1 independent review is a required finding source, not an
answer key. The reviewer must independently reconstruct each alleged repair and
may retain, change, or add findings based only on authenticated public inputs.

The reviewer uses a separate clean worktree at the exact candidate commit.
Worktree separation is edit isolation, not a secrecy claim.

## 2. Maximum input set

CONTROL must supply exact path and SHA-256 values. The maximum substantive set
is:

1. repository-root `AGENTS.md` at the candidate commit;
2. `s0-lab/control/s0-protocol-v0.3.md` and sidecar;
3. the v0.14 universal response contract, public falsification plan, review
   response, independent review, and CONTROL integration decision with their
   sidecars;
4. the I1 public runtime v0.2 CONTROL integration decision and sidecar;
5. the authenticated I1 public topology JSON, public-spec manifest,
   implementation-files manifest, and implementation binding manifest;
6. all four v0.1 isolation candidate Markdown files and sidecars;
7. the v0.1 isolation independent review and sidecar;
8. `trust-root-role-isolation-design-revision-v0.2.md` and sidecar;
9. `identity-authority-matrix-addendum-v0.2.md` and sidecar;
10. `isolation-acceptance-plan-addendum-v0.2.md` and sidecar;
11. `review-response-v0.1.md` and sidecar; and
12. this brief and sidecar.

The reviewer may open only official primary references linked by the candidate
to validate cryptographic or platform facts. No broad repository search,
advisory-agent output, implementation code beyond the explicitly authenticated
I1 topology inputs, or unlisted source is authorized.

## 3. Design-only boundary

This is a tabletop review. The reviewer must not provision a VM, change host
configuration, create a key, execute Ed25519 or HKDF, create a canary, fixture,
script, validator, account, vault, provider session, or model call, or run any
acceptance test. No implementation result may be inferred from prose.

The reviewer writes only the authorized review Markdown and same-basename
`.sha256` sidecar. It does not modify candidate files, commit, push,
merge, open a PR, or prepare a later implementation.

## 4. Required independent reconstruction

The reviewer must reconstruct without trusting the author response:

1. the exact v0.1 plus v0.2 composition and replacement map;
2. unchanged counts: 32 rows, 40 positions, eight pairs, 21 experimental
   signers plus one non-row root, 22 registry IDs, 27 stores, 46 readers, and
   64 edges;
3. all three exclusive signature scopes and every new unsigned TCB object;
4. strict key/signature validation at anchor, commitment, registry, PoP, root
   signature, and active artifact boundaries;
5. the two non-root request classes, separate root ceremony, three import
   packages, exact fields/files/states/media admissions, caller capabilities,
   powered-off one-shot lifecycle, host/appliance anti-replay order, transcript,
   inert candidate validation, registry binding, and activation;
6. descriptor/admission canonical bytes, absence of digest self-reference,
   authority source, host/guest responsibility, and post-run rejection;
7. the single invocation-ID construction, project-lifetime global reservation,
   separate ceremony/signer-media/invocation ledger namespaces, exact event
   chains, independent monotonic witnesses, boot authorization, absence of a
   second actor nonce, HKDF context, and evidence binding;
8. the effective 107 acceptance rows and noncompensatory rule; and
9. every inherited provider, signature, implementation, protected-material,
   E0, and S0 blocker/nonclaim.

## 5. Mandatory hostile tabletop cases

At minimum, independently trace these mutations:

- `A = R = identity`, `S = 0` for PoP, root registry, and ordinary artifact;
- every defined small-order class, one mixed-order public key, one mixed-order
  `R`, and one cofactored-only signature;
- strict key check skipped or cached across anchor/registry/profile/campaign/
  verifier-process contexts;
- pre-activation request with active fields or registry digest;
- active request before activation or with bootstrap fields;
- root ceremony that requires its not-yet-created activated envelope, lacks one
  of seven files, appears in the wrong root state, or repeats;
- context, registry-binding, or activation package with a missing/extra file,
  wrong capability/object admission, cross-signer replay, or state mismatch;
- hot/simultaneous/prior signer media, missing shutdown/detachment, reused raw
  result medium, active-request replay/crash, or restored signer-media ledger;
- repeat, crash-at-pending, cross-signer, changed commitment/challenge,
  transcript reorder, registry mismatch, and proof reused as ordinary authority;
- descriptor signed by an arbitrary key, edited after freeze, made digest-
  circular, or paired with a different ISO/VM/policy/ledger event;
- distinct VM IDs that try to share a separate nonce, duplicate invocation ID,
  conflicting role reservation, concurrent reservation race, failed-run reuse,
  restored ledger behind the monotonic witness, and boot-authorization reuse;
- any topology/count/edge/store/signer or closed-gate regression.

Agreement with prose is not evidence. Every handled mutation must trace to one
exact reject rule; an unhandled or multiply interpreted mutation is a finding.

## 6. Finding-specific closure criteria

### 6.1 `TRI-B01`

Pass only if no identity, small-order, mixed-order, noncanonical, out-of-range,
cofactored-only, wrong-profile, wrong-cache, or non-Boolean path can admit a key
or signature at any required boundary.

### 6.2 `TRI-B02`

Pass only if a non-root appliance can issue exactly one PoP before registry
assembly without an undefined registry digest/edge/scope, while that path
cannot authorize an active artifact or bypass later activation; and the root
can create exactly one registry signature without depending on that signature's
future activation. The inert candidate envelope must be verifiable for the
`pop-issued -> registry-bound` check without becoming authoritative until the
separate user activation record verifies.

### 6.3 `TRI-M01`

Pass only if the descriptor has one exact, noncircular TCB authority and
verification order, adds no hidden signer or topology object, and makes no
cryptographic claim against the trusted host.

### 6.4 `TRI-M02`

Pass only if exactly one external actor uniqueness value exists, its generation
and global lifetime are exact, duplicate/replay/rollback races reject, and
every derivation/evidence path binds the same bytes.

## 7. Severity and verdict

- `blocking`: protected-asset exposure, lost independence, circular or
  forgeable trust root, impossible bootstrap, frozen-topology contradiction, or
  required implementation of a still-closed gate.
- `major`: required route, authority, validation, state, lifecycle, evidence,
  failure, or nonclaim remains ambiguous or incomplete.
- `minor`: bounded exactness defect that cannot grant authority, weaken
  isolation, alter experimental meaning, or hide failure.

Allowed verdicts:

- `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any finding exists; or
- `INVALID-REVIEW`: baseline, hash, boundary, independence, or evidence failed.

No verdict opens implementation, key generation, protected material, provider
sessions, model calls, scoring, E0, or S0 execution.

## 8. Required output

Write exactly one Markdown review and one same-basename `.sha256` sidecar under
the CONTROL-approved v0.2 isolation-review path. State baseline/authentication,
all input hashes, independent reconstruction, mutation trace, predecessor-
finding disposition, new findings, counts, verdict, maximum claim, and exact
next gate. State explicitly that no implementation test was run.

Run the canonical public text-artifact validator SelfTest before relying on it,
validate the output pair, and preserve candidate inputs unchanged.
