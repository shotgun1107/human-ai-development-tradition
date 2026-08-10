# S0 v0.14 role-isolation acceptance-plan addendum v0.4

- `status`: bounded public tabletop revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 BOUNDED DESIGN REVISION OPEN`
- `predecessor_plan_sha256`: `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3`
- `responds_to_rereview_sha256`: `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9`
- `claim_kind`: public tabletop acceptance design only

## 1. Effective plan and row inventory

This addendum replaces only the v0.3 interpretation of `ISO-K20`, `ISO-K28`,
the import-event serialization evidence, and the directly related hostile
traces. No row is added or removed. The effective inventory remains 107
noncompensatory rows: 19 platform, 14 channel, 22 media/route, eight
independence, 34 trust/signer, and ten lifecycle rows.

One failure, skip, waiver, ambiguous result, missing record, substituted test,
or operator-selected interpretation fails the candidate. This document runs
no acceptance test.

## 2. Exact import-event evidence

For each of the three import classes, future evidence must contain all 31
ordered fields of `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` and prove:

1. one occurrence of every field and no other field;
2. strict ASCII/LF encoding with final LF and no BOM, CR, NUL, blank line, or
   trailing whitespace;
3. exact event hash over all 31 lines including final LF;
4. exact namespace sequence and global predecessor hash;
5. exact route predecessor event ID;
6. byte-equal route identity, capability, nonzero result-medium ID, and four
   preallocated event IDs across the route;
7. the exact admission/media zero-to-frozen transition;
8. one and only one lifecycle tuple from the v0.4 main revision;
9. the deterministic complete-frame hash rule; and
10. no event after consumed or terminal and no ID reuse, redraw, or retry.

The direct terminal-from-reserved and terminal-from-admission-frozen records
must both use completion ID `C`, `outcome_class=none`, zero frame hash, and
`none -> none` appliance state. The first retains zero admission/media fields;
the second retains the exact frozen admission/media tuple. Any other value is
not an alternative interpretation; it is a failed record.

## 3. Exact row replacements

### 3.1 `ISO-K20`: import lifecycle and record serialization

| Existing ID | Effective v0.4 mutation or observation | Required result |
|---|---|---|
| ISO-K20 | An import uses the v0.2 schema, the v0.3 additive-block interpretation, duplicate `result_media_id`, another field count/order/schema value, an illegal state tuple, wrong class source/destination, wrong event ID or chain, a known state where `none` or `indeterminate` is required, a nonzero frame hash where zero is required, or success without the exact durable consumed append | Reject without authorized state advance. Preserve bounded failure evidence, spend the preallocated route identities, and forbid replacement completion, waiver, or retry |

All other v0.3 `ISO-K20` route/state/capability and append-failure obligations
remain effective.

### 3.2 `ISO-K28`: withdrawn and future order-eight literals

| Existing ID | Effective v0.4 mutation or observation | Required result |
|---|---|---|
| ISO-K28 | Any v0.3 `TRI2-VEC-01` coordinate, relation, or literal is used; a future row is copied without an explicit derivation; any of four rows is absent or duplicated; canonical decode/re-encode, `P != I`, `[8]P = I`, `[4]P != I`, `[L]P != I`, or strict-profile rejection is missing, ambiguous, or fails; evidence is not independently frozen before use | Block key generation and reject the vector package. No old literal, copied label, substitution, waiver, or retry may satisfy the row. Only a separately authorized and independently verified `TRI2-VEC-02` package can become evidence |

The strict profile itself remains unchanged. This replacement withdraws bad
test data; it does not relax public-key or signature validation.

## 4. Mandatory hostile tabletop traces

A fresh design reviewer must trace at least:

1. the exact 31-line reserved, admission-frozen, pending, consumed, and each
   terminal variant for all three import classes;
2. a duplicate `result_media_id`, old schema literal, additive-block order,
   extra version field, missing/reordered field, CR, BOM, and missing final LF;
3. terminal from reserved with nonzero admission fields or appliance-state
   claims, and terminal from admission freeze with zero/changed admission
   fields or appliance-state claims;
4. pending with wrong source, known after-state, outcome class, or frame hash;
5. accepted without exact source-to-destination, canonical frame hash, or
   durable consumed append;
6. parse/validation rejection without source-to-source and state-commit
   failure without source-to-indeterminate;
7. crash, missing, or duplicate with a claimed frame hash or known after-state;
8. disagreement with a known after-state, a hash for noncanonical or
   non-unique bytes, or no hash for one uniquely selectable canonical but
   conflicting frame;
9. global predecessor mismatch, route predecessor mismatch, cross-route field
   substitution, early-terminal reuse of an unused ID, append conflict followed
   by redraw, and any retry; and
10. any attempt to use old `TRI2-VEC-01`, treat absence of `TRI2-VEC-02` as a
    pass, skip independent point-order evidence, or claim this design executed
    a vector.

Each mutation must have one fail-closed result. A multiply interpreted,
unobservable, or operator-selected result is a finding.

## 5. Non-regression and gate rule

The future reviewer must confirm no change to the frozen topology, counts,
signature scopes, ledger namespaces, A-D opportunity, provider blockers, or
closed implementation, protected-material, E0, and S0 gates.

At this gate the candidate can earn only an independent public-design finding
disposition. It cannot earn an implementation or acceptance pass. The missing
future `TRI2-VEC-02` evidence is an explicit pre-key-generation blocker. This
addendum does not open the vector-authoring gate, implementation, provider or
model sessions, protected material, fixture/oracle work, E0, or S0.
