# S0 v0.14 trust-root and role-isolation v0.4 CONTROL integration decision

- `decided_at`: `2026-08-10T15:52:14.6810379+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 CONTROL INTEGRATION DECISION OPEN`
- `source_branch`: `codex/s0-isolation-v04-independent-review`
- `review_evidence_tip`: `8dbb0f504edb9ee21f29e49c88a8aca9e8bf1c66`
- `reviewed_candidate_commit`: `d55c642d688fea847b469e8221ef63dfcb159052`
- `reviewed_candidate_tree`: `1867dd953f072a189c3f57df22f317ba2f98d609`
- `decision`: `APPROVE-PUBLIC-DESIGN-INTEGRATION-ONLY`
- `claim_kind`: authenticated public design baseline only

## 1. Decision

The S0 v0.14 trust-root and role-isolation v0.4 bounded revision is
**APPROVED FOR CONTROL INTEGRATION** as the current public trust-root and
role-isolation design overlay within `central-system-v2.1-s0-preparation`.

The effective public design is the authenticated predecessor composition
through v0.3, with only the explicit v0.4 replacements applied. V0.1 through
v0.3 and their reviews remain immutable construction, failure, correction,
and review evidence. They are not rewritten as successful versions.

CONTROL accepts the independently reviewed public text and its fail-closed
boundaries. This decision does not claim that any schema, parser, appliance,
ledger, witness, isolation mechanism, cryptographic operation, provider/model
session, E0 test, or S0 test exists or works.

## 2. Authenticated decision evidence

| Artifact | SHA-256 |
|---|---|
| `s0-protocol-v0.3-canonical-r1.md` | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` |
| `trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| `identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| `isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| `review-response-v0.3.md` | `6ddb194426353a42a907d8b7ba9b5fe5feac5b29c20d6a59daa09cbcfc853478` |
| `trust-root-role-isolation-independent-review-brief-v0.4.md` | `d6d80771a4793a3153ae35cb4cbcc6177eb8f72ac4c779daaebb8adb6e797a96` |
| `trust-root-role-isolation-design-v0.4-independent-review.md` | `82746f7c1b59fd162c1f54dc9e0e3d6d3c86b8ef7dc391fb5a10401e88157344` |

The canonical validator SelfTest passed all eleven cases. The five v0.4
candidate pairs and the independent-review pair each passed every canonical
text and same-basename sidecar check with `OVERALL=PASS`. The independent
review authenticated all 34 admitted inputs before review and again after
writing, with zero hash mismatches.

## 3. Independent result accepted by CONTROL

The final independent verdict is:

`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |

CONTROL accepts the review's bounded conclusions:

- `TRI2-M01` is closed at public-design-text level because the import event
  has one exact 31-field serialization, total lifecycle rows, deterministic
  frame-hash selection, separate mandatory global and route chains, complete
  pre-pending terminals, and no replacement-completion or retry path.
- `TRI2-m01` is closed at public-design-text level because every unsupported
  v0.3 coordinate, complement relation, and literal is withdrawn from
  effective authority while the inherited strict Ed25519 predicate remains
  unchanged and key generation is blocked before any missing future vector
  could be treated as evidence.
- No new topology, fairness, signature-scope, ledger-namespace, provider,
  implementation, protected-material, E0, or S0 regression was found.

## 4. Effective public baseline adopted

The integrated public design adopts the following exact boundaries:

1. `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` has exactly 31 ordered ASCII
   `name=value` lines, each ending in LF including the final line. A duplicate,
   missing, reordered, unknown, malformed, or extra field rejects.
2. Global `previous_event_sha256` chaining and route-local
   `prior_route_event_id` chaining are distinct and both mandatory.
3. The fixed `R`, `A`, `P`, and `C` lifecycle permits only the declared
   reserved, admission-frozen, pending, consumed, and terminal tuples. Early
   terminalization burns later IDs; conflict or append failure grants no new
   completion and no retry.
4. Only a unique, canonical, state-consistent accepted outcome plus durable
   consumed `C` makes the destination state available. Every other class is
   terminal and fail-closed.
5. Host preflight, target TCB outcome emission, CONTROL post-run
   classification, and ledger/witness append retain separate authorities.
   Unsigned TCB evidence creates no signature, signer, registry authority,
   experimental topology object, or fourth ledger namespace.
6. The v0.3 `TRI2-VEC-01` values have no effective authority. No replacement
   vector or point-order result is accepted by this decision.
7. A future `TRI2-VEC-02` can exist only after the user separately opens
   `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR AUTHORING OPEN` and the required
   construction, decoding, re-encoding, order, and strict-rejection evidence
   is independently frozen before key generation.

The frozen public inventories remain 32 aggregated role rows, 40 role
positions, eight paired rows, 21 experimental signers plus one non-row root,
22 registry IDs, 27 stores, 46 explicit readers, 64 edges, 107
noncompensatory acceptance rows, three signature scopes, three ledger
namespaces, eight future invocation/session units, and maximum concurrency
three. A-D source information, authority, model condition, time, output, and
scoring opportunity remain equal.

## 5. Decision limits and closed gates

This is public design integration only. It does not automatically authorize or
open any of the following:

- a machine-readable schema, parser, generator, validator, or implementation;
- a host, VM, sandbox, account, network, clipboard, Git restriction, ACL,
  vault, store, ledger, witness, appliance, or provider setup;
- key generation, private-key custody, anchor, registry, rotation,
  revocation, signature, HKDF, vector construction, or point operation;
- protected material, bank, label, fixture, projection, package, condition
  map, hidden oracle, or executor authoring;
- provider/model sessions, judge handoff, scoring, statistics, E0, or S0;
- central-system implementation, Project Brain integration, operational
  safety, economic value, production readiness, or model-to-model transfer;
  or
- `main` integration.

The independent-review branch and this decision lineage may be preserved by
ordinary commit and push approval. Merging any lineage into `main` requires a
separate explicit user authorization after the decision pair is frozen and
published. This decision itself supplies no merge authority.

## 6. Maximum claim

The maximum supported claim is that the authenticated v0.4 public design
repairs the two reviewed predecessor defects without an identified public
design regression and is adopted by CONTROL as the current public
trust-root/role-isolation design overlay for later, separately gated work.

No implementation, cryptographic, platform, provider/model, acceptance, E0,
S0, central-system, Project Brain, operational, economic, production, or
transfer result follows from this decision.
