# S0 v0.14 identity and authority matrix addendum v0.4

- `status`: bounded public-design revision candidate
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 BOUNDED DESIGN REVISION OPEN`
- `predecessor_matrix_sha256`: `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a`
- `responds_to_rereview_sha256`: `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9`
- `claim_kind`: public identity, authority, and scope design only

## 1. Effective composition and preserved inventory

This addendum changes only import-event serialization authority and the
authority status of the withdrawn v0.3 order-eight literals. Every unlisted
v0.3 matrix clause remains effective.

The effective counts remain 32 aggregated role rows, 40 positions, eight
paired rows, 21 experimental signers, 19 `none` positions, one non-row root,
22 registry IDs, 27 experimental stores, 46 reader entries, 64 edges, three
signature scopes, three ledger namespaces, 107 acceptance rows, eight future
executor units, and maximum concurrency three.

## 2. Import-event authority

| Object or decision | Producing authority | Verification authority | Authority limit |
|---|---|---|---|
| identifiers and reserved/admission/pending records | CONTROL host preflight | signer-media ledger and monotonic witness | identity and lifecycle only |
| unsigned outcome frame | pinned `S0-IMPORT-TRANSITION-TCB-1` | CONTROL post-run admission under exact media/admission bindings | target state evidence only |
| final classification | CONTROL post-run admission applies frozen precedence | ledger consumer and witness verify exact inputs | cannot create missing target evidence |
| consumed or terminal event | CONTROL proposes exact 31-line bytes; ledger/witness atomically accepts or rejects | independent replay of exact bytes, event hash, global chain, and route chain | no append means no completion claim |

The canonical import event is exactly
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` as completely defined by the v0.4
main revision. It is not the v0.2 record plus an appended block. The schema
contains exactly one `result_media_id`, exactly 31 ordered fields, and no
separate version field.

The event hash covers every emitted ASCII byte including the final LF. The
global `previous_event_sha256` chain and route-local `prior_route_event_id`
chain are separate and both mandatory. The frame binds the planned completion
ID, while the completion event binds the frame hash; neither binds the future
event hash, so no hash cycle is introduced.

## 3. State-evidence authority

| Lifecycle point | Permitted state evidence |
|---|---|
| reserved | `none -> none`, zero frame hash, `outcome_class=none` |
| admission frozen | `none -> none`, zero frame hash, `outcome_class=none` |
| pending | exact class source to `none`, zero frame hash, `outcome_class=none` |
| consumed | exact source to destination, one canonical frame hash, `accepted` |
| terminal from reserved or admission frozen | `none -> none`, zero frame hash, `outcome_class=none` |
| explicit parse or validation rejection | exact source to source and one canonical rejected-frame hash |
| state-commit failure | exact source to `indeterminate` and one canonical failure-frame hash |
| crash, missing, or duplicate | exact source to `indeterminate` and zero frame hash |
| disagreement | exact source to `indeterminate`; canonical frame hash only under the main revision's unique-frame rule |

No operator may substitute a known after-state for `indeterminate`, infer a
destination from shutdown, choose one duplicate frame, or construct a
completion after append conflict. Unused preallocated IDs are burned by an
early terminal and cannot authorize another route.

## 4. Vector authority withdrawal

The v0.3 `TRI2-VEC-01` coordinates, complement relation, and four literals have
no effective authority. They cannot be accepted as implementation input,
hostile-vector evidence, or grounds to pass `ISO-K28`.

The inherited `S0-ED25519-STRICT-1` profile remains authoritative and
unchanged. A future `TRI2-VEC-02` can become acceptance input only after the
separate public vector-authoring gate freezes exact literals and a fresh
independent verifier freezes construction, canonical decode/re-encode,
nonidentity, `[8]`, `[4]`, `[L]`, and strict-rejection evidence. Until then,
the affected pre-key-generation vector requirement is blocked, not waived.

## 5. Future machine-readable successor requirement

A later, separately approved implementation gate must derive exact machine-
readable schemas for `S0-SIGNER-IMPORT-ADMISSION-2`,
`S0-SIGNER-IMPORT-OUTCOME-1`, and the complete 31-line
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` from the authenticated effective
v0.3 plus v0.4 public text. It must reject the v0.3 additive-block
interpretation and preserve the inherited non-root signing, root-ceremony,
ledger, witness, signature-scope, topology, and A-D symmetry requirements.

The future implementation must also keep `TRI2-VEC-01` withdrawn and treat
`TRI2-VEC-02` as unavailable until the separate vector-authoring and
independent-verification evidence is frozen. This requirement authorizes no
schema file, generator, parser, vector, or implementation under the current
gate.

## 6. Topology and implementation boundary

The event record, outcome medium, TCB service, classification, and future
vector artifact are control objects only. They add no experimental role,
signer, store, reader, edge, signature scope, ledger namespace, or A-D
opportunity. This addendum authorizes no machine-readable schema, provider,
witness, vector, key, signature, implementation, acceptance test, E0 test, or
S0 execution.
