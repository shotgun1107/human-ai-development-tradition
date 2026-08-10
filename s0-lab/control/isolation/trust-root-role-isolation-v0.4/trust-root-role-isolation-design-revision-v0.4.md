# S0 v0.14 trust-root and role-isolation design revision v0.4

- `status`: bounded public-design revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 BOUNDED DESIGN REVISION OPEN`
- `continuation_base_commit`: `81a32c97dc9f1e50d742dd009034ac678ff66494`
- `predecessor_design_sha256`: `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b`
- `predecessor_rereview_sha256`: `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9`
- `claim_kind`: public design text only

## 1. Decision and effective composition

This revision addresses only the open `TRI2-M01` major finding and
`TRI2-m01` minor finding in the authenticated v0.3 independent rereview. It
does not implement or execute a schema, ledger, witness, appliance, vector,
point operation, key, signature, acceptance test, E0 test, or S0 test.

The effective candidate is the authenticated v0.1 base, the v0.2 overlay, the
v0.3 overlay, and this bounded v0.4 overlay in that order. A conflict inside
one of the exact replacements below is resolved in favor of v0.4. A conflict
outside those replacements is a candidate defect, not implicit v0.4
precedence.

### 1.1 Exact replacement map

| Predecessor clause | Effective v0.4 treatment |
|---|---|
| v0.3 design section 2.6, including “retains every v0.2 field and adds” and its partial field block | replaced in full by section 2 of this revision |
| v0.3 design section 2.5 pre-pending terminal state-field meaning | replaced only where section 2 fixes the exact direct-terminal records |
| v0.2 common signer-media grammar and zero import `result_media_id` | remains effective for non-root signing and root ceremony; replaced for `route_kind=import` only by section 2 |
| v0.3 design section 3 and `TRI2-VEC-01` | replaced in full by section 3; the old coordinates, relation, and four literals are withdrawn |
| v0.3 matrix sections 7 and 8 and import-event serialization implications | replaced only as stated by `identity-authority-matrix-addendum-v0.4.md` |
| v0.3 acceptance meanings for `ISO-K20`, `ISO-K28`, pre-pending terminal records, and related hostile traces | replaced only as stated by `isolation-acceptance-plan-addendum-v0.4.md` |
| v0.3 review brief | historical only after the v0.4 review brief is frozen; it does not govern a v0.4 review |

No other v0.1, v0.2, or v0.3 clause changes meaning.

### 1.2 Authenticated repair inputs

| Input | SHA-256 |
|---|---|
| v0.3 design revision | `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b` |
| v0.3 identity/authority addendum | `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a` |
| v0.3 acceptance-plan addendum | `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3` |
| v0.3 independent rereview | `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9` |
| canonical public protocol r1 | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` |

The same-basename sidecars remain the byte-identity records. All predecessor
files remain immutable evidence.

### 1.3 Frozen non-regression boundary

This revision does not change 32 aggregated role rows, 40 positions, eight
paired rows, 21 experimental section-4 signers, 19 `none` bindings, one
non-row root, 22 registry IDs, 27 experimental stores, 46 explicit readers,
64 edges, 107 noncompensatory acceptance rows, three signature scopes, three
ledger namespaces, eight future executor units, or maximum concurrency three.
It does not change A-D source information, authority, model condition, time,
output, or scoring opportunity. Every provider, implementation, protected-
material, vector-execution, E0, and S0 gate remains closed.

## 2. `TRI2-M01`: complete import-event grammar

### 2.1 Exact 31-line record

Import routes use one complete schema. They do not compose the v0.2 common
grammar with the v0.3 partial block.

```text
signer_media_event_schema=S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1
namespace=signer-media
sequence=<canonical unsigned decimal, beginning at 0>
previous_event_sha256=<64 lowercase hex; 64 zeroes exactly at namespace sequence 0>
event_id=<64 lowercase hex>
prior_route_event_id=<64 lowercase hex>
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact non-root registry role ID>
route_kind=import
route_class=<preactivation-context-v1, registry-binding-v1, or activation-binding-v1>
request_id=<64 zeroes>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
admission_record_sha256=<64 lowercase hex>
media_object_sha256=<64 lowercase hex>
media_object_id=<64 lowercase hex>
result_media_id=<64 lowercase hex, nonzero>
result_media_kind=import-outcome-v1
reserved_media_event_id=<64 lowercase hex, nonzero>
admission_frozen_media_event_id=<64 lowercase hex, nonzero>
pending_media_event_id=<64 lowercase hex, nonzero>
completion_media_event_id=<64 lowercase hex, nonzero>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_frame_sha256=<64 lowercase hex>
outcome_class=<none, accepted, parse-rejected, validation-rejected, state-commit-failed, crash, missing, duplicate, or disagreement>
before_appliance_state=<none, key-generated, pop-issued, or registry-bound>
after_appliance_state=<none, key-generated, pop-context-bound, pop-issued, registry-bound, active, or indeterminate>
state=<reserved, admission-frozen, pending, consumed, or terminal>
terminal_from=<none, reserved, admission-frozen, or pending>
decision=<reserved, approved, executing, accepted, or rejected>
```

The first line is the sole schema/version field; terminal `-1` is the schema
version. A separate version field is forbidden. Every record is exactly these
31 ASCII `name=value` lines in this order, each followed by byte `0A`, including
the LF after `decision`. A BOM, CR, NUL, blank line, duplicate, missing,
reordered, unknown, or extra field rejects. Placeholders above are constraints,
not emitted text.

The event contains no self-hash field. Its hash is:

```text
event_bytes = ASCII(line_01) || 0A || ... || ASCII(line_31) || 0A
event_sha256 = SHA-256(event_bytes)
```

`previous_event_sha256` is zero only for sequence zero; otherwise it is the
exact hash of the immediately preceding event in the global `signer-media`
namespace, including another route if events interleave. `prior_route_event_id`
separately names the immediately preceding event of this import route.

### 2.2 Constants and route bindings

Let `Z` be exactly 64 ASCII zeroes. Let `R`, `A`, `P`, and `C` be the distinct
preallocated reserved, admission-frozen, pending, and completion event IDs.
They are nonzero, mutually distinct, project-lifetime unique, and never reused.
An early terminal burns unused later IDs.

| `route_class` | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

Every event retains byte-equal campaign, ceremony, signer, route class,
capability, nonzero `result_media_id`, result-media kind, four event IDs, and
outcome schema. `request_id=Z` and `route_kind=import` in every event.

Before admission freeze, `admission_event_id`, `admission_record_sha256`,
`media_object_sha256`, and `media_object_id` are all `Z`. From admission freeze
onward they are respectively `A`, the hash of the exact admission bytes
including final LF, the admission-bound package hash, and the admission-bound
package object ID, and never change.

### 2.3 Exact lifecycle records

`ADM0` means the four admission/media fields are all `Z`. `ADM1` means the
exact frozen tuple `(A, admission hash, package hash, package object ID)`. `H`
is defined in section 2.4.

| Variant | `event_id` | `prior_route_event_id` | Admission | Frame hash | Outcome | Before | After | `state` | `terminal_from` | `decision` |
|---|---|---|---|---|---|---|---|---|---|---|
| reserved | `R` | `Z` | `ADM0` | `Z` | `none` | `none` | `none` | `reserved` | `none` | `reserved` |
| admission frozen | `A` | `R` | `ADM1` | `Z` | `none` | `none` | `none` | `admission-frozen` | `none` | `approved` |
| pending | `P` | `A` | `ADM1` | `Z` | `none` | `SRC` | `none` | `pending` | `none` | `executing` |
| accepted completion | `C` | `P` | `ADM1` | `H` | `accepted` | `SRC` | `DST` | `consumed` | `none` | `accepted` |
| direct terminal from reserved | `C` | `R` | `ADM0` | `Z` | `none` | `none` | `none` | `terminal` | `reserved` | `rejected` |
| direct terminal from admission frozen | `C` | `A` | `ADM1` | `Z` | `none` | `none` | `none` | `terminal` | `admission-frozen` | `rejected` |
| parse rejection | `C` | `P` | `ADM1` | `H` | `parse-rejected` | `SRC` | `SRC` | `terminal` | `pending` | `rejected` |
| validation rejection | `C` | `P` | `ADM1` | `H` | `validation-rejected` | `SRC` | `SRC` | `terminal` | `pending` | `rejected` |
| state-commit failure | `C` | `P` | `ADM1` | `H` | `state-commit-failed` | `SRC` | `indeterminate` | `terminal` | `pending` | `rejected` |
| crash | `C` | `P` | `ADM1` | `Z` | `crash` | `SRC` | `indeterminate` | `terminal` | `pending` | `rejected` |
| missing | `C` | `P` | `ADM1` | `Z` | `missing` | `SRC` | `indeterminate` | `terminal` | `pending` | `rejected` |
| duplicate | `C` | `P` | `ADM1` | `Z` | `duplicate` | `SRC` | `indeterminate` | `terminal` | `pending` | `rejected` |
| disagreement | `C` | `P` | `ADM1` | section 2.4 | `disagreement` | `SRC` | `indeterminate` | `terminal` | `pending` | `rejected` |

No other tuple parses. There is no terminal from `consumed`, no record after
`consumed` or `terminal`, and no direct `reserved -> pending`,
`reserved -> consumed`, or `admission-frozen -> consumed` transition.

### 2.4 Complete-frame hash rule

`H` is SHA-256 of the one complete canonical outcome frame, including its
`outcome_body_sha256` line and final LF. It is available only when the frame is
uniquely selectable, at most 2,048 bytes, followed only by zeroes, and has
canonical syntax, a correct body hash, and an allowed decision/reason/state
tuple.

- `accepted`, `parse-rejected`, `validation-rejected`, and
  `state-commit-failed` require `H`.
- `crash` records `Z`; classification precedence ignores apparent frame bytes.
- `missing` and `duplicate` record `Z`; duplicate evidence never selects one
  frame.
- `disagreement` records `H` only when exactly one internally canonical frame
  exists but conflicts with admission, host, ledger, witness, or anti-replay
  evidence. It records `Z` for malformed, oversized, bad-body-hash,
  invalid-tuple, or non-uniquely-selectable bytes.

Raw observations remain separate bounded failure evidence. A ledger event
hash never chooses a frame from duplicates.

### 2.5 Authority and order

CONTROL host preflight alone reserves identities, freezes admission, and
authorizes attachment. The target `S0-IMPORT-TRANSITION-TCB-1` alone emits the
unsigned outcome frame. CONTROL post-run admission alone applies the fixed
classification. The ledger/witness provider alone enforces uniqueness,
transition legality, global chaining, and append durability; it does not create
a success classification.

The exact logical order is reservation `R`, admission freeze `A`, powered-off
attachment and pending `P`, one boot, controlled stop, detachment of both
media, final classification, then exactly one consumed or terminal `C`. A
pre-pending failure may append terminal `C` from the last durable `R` or `A`.
If `C` conflicts or the ledger/witness cannot append, no replacement ID or
completion is invented. The candidate fails and the route cannot retry. An
accepted target frame does not make `DST` available unless consumed `C`
persists.

This schema remains unsigned TCB evidence in the existing `signer-media`
namespace. It creates no signer, signature scope, experimental role, store,
reader, edge, or fourth ledger namespace. The unresolved provider and witness
implementation remains outside this gate.

## 3. `TRI2-m01`: withdraw unsupported literals and fail closed

The v0.2 attribution to RFC 9381 section 5.4.5 remains removed. The v0.3
definitions of `y0` and `y1`, the relation `y1 = p - y0`, and all four rows of
`TRI2-VEC-01` are withdrawn in full. They remain immutable failure evidence
but have no effective vector, implementation, or acceptance authority.

[RFC 8032 sections 5.1.2 and
5.1.3](https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1.2) remain
authoritative only for the general Ed25519 encoding and decoding rule. The complete inherited
`S0-ED25519-STRICT-1` profile remains byte-for-byte unchanged, including exact
decode and re-encode, nonidentity, order-`L`, scalar-range, and uncofactored-
equation requirements at their existing application points.

This revision freezes no replacement coordinate or literal and makes no point-
order claim. Before key generation, a separately opened
`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR AUTHORING OPEN` gate must freeze a new
public `TRI2-VEC-02` artifact containing exactly four pairwise-distinct
candidate encodings for the nonidentity exact-order-eight hostile class. For
every row, separately frozen construction and independent verification
evidence must establish:

1. an explicit public derivation produces the exact 32-byte literal;
2. RFC 8032 canonical decoding succeeds;
3. re-encoding reproduces identical bytes;
4. `P != I`;
5. `[8]P = I`;
6. `[4]P != I`;
7. `[L]P != I`; and
8. `S0-ED25519-STRICT-1` rejects the encoding as both `A` and `R` where
   applicable.

A copied label, unauthenticated coordinate, relation, or byte string is not
evidence. The new vector artifact, derivation, and independent verification
must all be frozen before use. Missing, inconsistent, or failed evidence blocks
key generation without substitution, waiver, or retry. No vector artifact is
created and no curve operation is executed by this design revision.

## 4. Finding dispositions and next boundary

| Finding | v0.4 author proposal |
|---|---|
| `TRI2-M01` | replace the ambiguous overlay with one complete 31-line schema, exact hashes, and a total lifecycle table including both pre-pending terminals |
| `TRI2-m01` | remove every unsupported coordinate and literal from effective authority and convert future hostile-vector use into an explicit fail-closed gate |

These are author proposals, not independent finding closures. The maximum next
step is a fresh public-only independent review after all v0.4 files and
sidecars are authenticated in a frozen candidate commit. Even a zero-finding
review permits only separate CONTROL integration consideration. It does not
open implementation, the vector-authoring gate, key generation, protected
material, provider/model sessions, E0, S0, or `main` integration.
