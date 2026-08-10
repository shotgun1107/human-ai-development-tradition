# S0 v0.14 identity and authority matrix addendum v0.3

- `status`: design revision candidate
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `predecessor_matrix_sha256`: `3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1`
- `claim_kind`: public identity, authority, and scope design only

## 1. Effective composition and count preservation

This addendum overlays only the import admission, outcome, and completion
authority of the authenticated v0.2 matrix. Every unlisted v0.2 matrix row
remains effective. It creates no implementation and no experimental identity,
role, position, signer, store, reader, edge, signature scope, or ledger
namespace.

| Inventory | Effective count |
|---|---:|
| aggregated role rows | 32 |
| role positions | 40 |
| paired rows | 8 |
| experimental section-4 signer bindings | 21 |
| positions with signer `none` | 19 |
| non-row root signer | 1 |
| registry IDs | 22 |
| experimental stores | 27 |
| explicit reader entries | 46 |
| experimental edge rows | 64 |
| exclusive signature scopes | 3 |
| existing ledger namespaces | 3 |
| noncompensatory acceptance rows | 107 |
| future executor invocation/session units | 8 |
| maximum executor concurrency | 3 |

`S0-IMPORT-TRANSITION-TCB-1`, its outcome frame, the raw outcome medium, and
the import signer-media events are TCB control objects on an existing
administrative route. They do not enter any count above.

## 2. Effective import authority classes

The following rows replace the v0.2 matrix rows for the three imports, import
admission, and import completion evidence. They do not replace signing-request
or offline-root result authority.

| Object or action | Producing authority | Verification authority | Signature scope | Experimental topology effect |
|---|---|---|---|---|
| `preactivation-context-v1` import admission | CONTROL host preflight under the pinned TCB configuration | exact target appliance, host signer-media ledger, and monotonic witness | deliberately unsigned | none |
| `registry-binding-v1` import admission | CONTROL host preflight under the pinned TCB configuration | exact target appliance, host signer-media ledger, and monotonic witness | deliberately unsigned | none |
| `activation-binding-v1` import admission | CONTROL host preflight under the pinned TCB configuration | exact target appliance, host signer-media ledger, and monotonic witness | deliberately unsigned | none |
| fresh `import-outcome-v1` raw medium | CONTROL host preflight creates and binds; target appliance may write once | CONTROL post-run admission reads raw bytes without mounting; ledger/witness binds identity | none | none |
| `S0-SIGNER-IMPORT-OUTCOME-1` frame | exact pinned `S0-IMPORT-TRANSITION-TCB-1` inside the target appliance | CONTROL post-run admission plus exact admission, host state, ledger, witness, and appliance-state agreement | deliberately unsigned TCB state evidence | none |
| import completion classification | CONTROL post-run admission applies the fixed precedence to host and frame evidence | signer-media ledger consumer plus monotonic witness | none | none |
| `consumed/accepted` import transition | exact accepted appliance frame and agreeing host evidence jointly satisfy the frozen rule | target anti-replay state plus signer-media ledger/witness | none | none |
| `terminal/rejected` import transition | fixed host classification for every non-accepted post-pending outcome | CONTROL host evidence plus signer-media ledger/witness; target anti-replay state is bound when observable and uncertainty invalidates the candidate | none | none |

The unsigned outcome frame is not proof against a malicious host or
hypervisor. It is usable only as bounded TCB state evidence when the pinned
appliance image, one-shot launch admission, exact ISO and outcome-medium
handles, one-use capability, frame hashes, host evidence, and ledger/witness
all agree. Removing any one of those bindings removes authority; it does not
fall back to shutdown, detachment, operator judgment, or a valid-looking
frame.

## 3. Import state and outcome matrix

| Import class | Admitted source | Intended destination | Exact accepted evidence | Every other outcome |
|---|---|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` | one valid `accepted/none` frame, matching durable destination state, host evidence, and completion event | terminal append when possible; otherwise no completion claim; destination unavailable; no retry |
| `registry-binding-v1` | `pop-issued` | `registry-bound` | one valid `accepted/none` frame, matching durable destination state, host evidence, and completion event | terminal append when possible; otherwise no completion claim; destination unavailable; no retry |
| `activation-binding-v1` | `registry-bound` | `active` | one valid `accepted/none` frame, matching durable destination state, host evidence, and completion event | terminal append when possible; otherwise no completion claim; destination unavailable; no retry |

The inherited signer-state/route matrix otherwise remains exact. A signing
request cannot perform an import transition, an import cannot produce a
signature, and an accepted state cannot be inferred from a normal shutdown.

## 4. Identifier and event authority

CONTROL host preflight generates the following independent opaque 32-byte
values with the inherited Windows CNG system-preferred RNG before admission is
frozen. All are unique over the project-lifetime signer-media ledger.

| Value | Persistence and single-use rule | May authorize |
|---|---|---|
| `result_media_id` | reserved before attachment; nonzero; never reused | identity of one fresh 2,048-byte raw outcome medium only |
| `reserved_media_event_id` | project-lifetime ledger; appended once | one route reservation event only |
| `admission_frozen_media_event_id` | project-lifetime ledger; appended once | one exact frozen admission event only |
| `pending_media_event_id` | project-lifetime ledger; appended once | one exact powered route attempt only |
| `completion_media_event_id` | project-lifetime ledger; appended once as consumed or terminal | one exact final classification only |
| `attachment_capability_id` | inherited one-use admission capability; spent by the attempt | attachment of the exact ISO and outcome medium to one signer only |

The four event IDs are preallocated, but their records remain chained by
`prior_route_event_id`. Preallocation conveys identity, not state or success.
The outcome frame binds the planned IDs, while the completion event binds the
frame hash and final classification. The frame never depends on the later
completion-event hash or ledger head, so there is no hash cycle.

The admission, outcome frame, and import ledger event each bind
`result_media_kind=import-outcome-v1` and the same `result_media_id`.

A duplicate ID, capability, or prior-event link found before `pending` rejects
admission under the inherited lifecycle and is not an outcome classification.
After `pending`, a reused binding is `disagreement`; more than one outcome
medium or frame is `duplicate`. A completion-ID conflict or failed ledger/
witness append cannot produce another terminal event: the conflict evidence
invalidates the candidate, and no new ID or repeated import is allowed.

## 5. Media, reader, and persistence boundaries

| Object | Writer | Permitted reader | Persistence | Forbidden interpretation |
|---|---|---|---|---|
| immutable import ISO | inherited CONTROL freeze route | exact target import service | temporary TCB replica until final evidence | experimental input store or mutable operator channel |
| raw outcome medium | zero-filled by CONTROL; written at most once by the target service | CONTROL post-run admission, raw and unmounted | temporary TCB replica until evidence is sealed | filesystem, payload store, signature medium, or experimental edge |
| canonical outcome frame | target import service | CONTROL post-run admission and future reviewer through retained evidence | exact bytes/hash in existing named ceremony evidence | cryptographic proof, signature, registry statement, or signer output |
| completion signer-media event | CONTROL post-run admission | existing signer-media ledger consumers and witness | project-lifetime existing ledger namespace | fourth ledger, experimental store, or permission to retry |

The raw medium is always detached before host reading. Cleanup happens only
after the completion event and bounded evidence are durably retained, or after
the bounded conflict/failure evidence is sealed when an exact append is
impossible. Deletion is an operational cleanup claim, not cryptographic
erasure. A frame containing protected content, private-key bytes, or any field
outside the exact schema is `disagreement` and invalidates the candidate.

## 6. Classification authority and precedence

For a route that reached `pending`, CONTROL post-run admission must choose
exactly one outcome in this order:

1. `crash`;
2. `missing`;
3. `duplicate`;
4. `disagreement`;
5. `parse-rejected`, `validation-rejected`, or `state-commit-failed`; or
6. `accepted`.

The earlier matching class wins. Only `accepted` may append
`consumed/accepted`. Every other class requires `terminal/rejected` when the
preallocated completion ID and ledger/witness remain usable, spends the route
identities and capability, withholds the destination state, and forbids retry
or selective replay. If exact classification or event persistence is
impossible, no completion is claimed and the candidate fails closed.

## 7. Strict-vector provenance boundary

The v0.3 design table `TRI2-VEC-01: frozen order-eight encoding table` is
public negative-vector specification text only. It grants no authority to a
copied label or to RFC 9381. A future implementation gate must independently
reproduce all four literal encodings from the stated Edwards25519 field and
encoding rules, decode them canonically, establish exact order eight, confirm
`[L]P != I`, and prove rejection by the inherited strict profile.

No vector construction, point decoding, scalar multiplication, key creation,
signature, or verification occurred under this design gate.

## 8. Machine-readable successor requirement

A later, separately approved implementation gate must derive exact schemas for
`S0-SIGNER-IMPORT-ADMISSION-2`, `S0-SIGNER-IMPORT-OUTCOME-1`, and
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` from authenticated v0.3 text. It must
also preserve the inherited signing-request and root-ceremony schemas, the
three exclusive signature scopes, the three ledger namespaces, every frozen
count, A-D source-information/authority/model/time/output/scoring symmetry,
and every provider or implementation blocker.

This requirement authorizes no machine-readable artifact or implementation
under the current gate.
