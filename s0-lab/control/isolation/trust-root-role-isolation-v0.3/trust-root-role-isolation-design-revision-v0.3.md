# S0 v0.14 trust-root and role-isolation design revision v0.3

- `status`: design revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `continuation_base_commit`: `5a7181b2c4b62c912bb0c48daf2cd6e0783fb1af`
- `predecessor_design_commit`: `cb4198f4475881ba5b607517fdbb4f0db6b8ce5d`
- `predecessor_review_commit`: `7d251f04588babeb180b743c8f6860929997b17c`
- `claim_kind`: public design only

## 1. Decision and effective composition

This revision addresses only `TRI2-M01` and `TRI2-m01` from the authenticated
v0.2 independent review. It creates no implementation, validator, helper, VM,
account, network rule, key, anchor, registry, signature, executable
cryptographic-vector artifact, cryptographic computation or validation,
fixture, bank, label, oracle, condition map, executor, provider session, model
call, acceptance result, E0 result, or S0 result. Section 3 freezes public
literal specification text only.

The effective v0.3 candidate is a strict composition:

1. the authenticated v0.1 candidate remains the base design;
2. the authenticated v0.2 successor remains the first overlay;
3. this document replaces only the v0.2 clauses listed in section 1.1;
4. `identity-authority-matrix-addendum-v0.3.md` replaces or supplements only
   its listed v0.2 matrix clauses;
5. `isolation-acceptance-plan-addendum-v0.3.md` replaces only its listed v0.2
   evidence fields and hostile-row meanings, without adding a test-row ID;
6. `review-response-v0.2.md` is explanatory evidence and grants no authority;
   and
7. `trust-root-role-isolation-independent-review-brief-v0.3.md` replaces the
   v0.2 review brief for a future, separately opened review gate.

No unlisted v0.1 or v0.2 sentence changes meaning. A conflict inside a named
replacement is resolved in favor of v0.3. A conflict outside those
replacements is a candidate defect, not implicit v0.3 precedence.

### 1.1 Exact replacement map

| v0.2 source | Effective v0.3 treatment |
|---|---|
| design section 3.5 bullet beginning `all four canonical order-eight encodings` | replaced by section 3 of this revision |
| design section 4.3.5 import-admission grammar and the import-only zero-`result_media_id` rule | replaced for the three import classes by sections 2.2 and 2.3 |
| design section 4.3.6 phrases limiting a result disk to signing routes, import event grammar, and exact result/state evidence for imports | replaced for import routes by sections 2.4 through 2.7; signing and root-ceremony behavior otherwise survives |
| design section 4.4 state-transition evidence for the three imports | supplemented and, on conflict, replaced by sections 2.5 and 2.6 |
| v0.2 identity/authority addendum rows for the three imports, import admission, and signer-media evidence | supplemented by the v0.3 identity/authority addendum |
| v0.2 acceptance evidence; ISO-K20, ISO-K25, ISO-K31, and ISO-K33 meanings for import routes; and ISO-K28 negative-vector provenance | replaced only as stated by the v0.3 acceptance-plan addendum |
| v0.2 independent-review brief | replaced in full by the v0.3 brief |

### 1.2 Authenticated predecessor inputs

| Input | SHA-256 |
|---|---|
| v0.2 design revision | `e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4` |
| v0.2 identity/authority addendum | `3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1` |
| v0.2 acceptance-plan addendum | `534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1` |
| v0.2 review response | `5c961d3bba03e12e07d34aede1207448565bf3456d0bffb6cad1602f1bbd2494` |
| v0.2 independent-review brief | `610b4ca1b03d7539cdcaf526a03bf3877cfca24426fd9f58b816aa0012d6db27` |
| v0.2 independent review | `67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990` |

The same-basename sidecars remain the identity records. The v0.2 candidate and
its `REVISE-AND-REVIEW` review remain immutable failure evidence.

### 1.3 Unchanged frozen invariants

This revision does not change:

- 32 aggregated role rows, 40 role positions, or eight paired rows;
- 21 experimental section-4 signers, 19 `none` bindings, one non-row root, or
  the exact 22-entry registry order;
- 27 experimental stores, 46 explicit reader entries, or 64 edge rows;
- 107 noncompensatory acceptance rows;
- the three exclusive signature scopes or three existing ledger namespaces;
- the exact A-D source information, authority, model condition, time, output,
  and scoring opportunities;
- the eight future executor invocation/session units or maximum concurrency
  three; or
- any closed provider, implementation, protected-material, E0, or S0 gate.

The import-outcome medium below is a TCB temporary replica on an already
declared host-to-appliance administrative route. It is not an experimental
store, reader, edge, role, signer, signature scope, or fourth ledger namespace.

## 2. `TRI2-M01`: canonical import outcome route

### 2.1 One route for exactly three imports

The following state-changing imports use one common outcome contract:

| Import class | Required before state | Accepted after state |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

The common outcome route and raw-medium kind is exactly
`import-outcome-v1`. It is not a fourth import class.

No fourth import class is created. Shutdown, ISO detachment, elapsed time, or
absence of a host error is never success evidence. Only the exact accepted
frame and ledger agreement defined below can authorize `consumed/accepted`.

### 2.2 Preallocated noncircular event identities

Before the import-admission record freezes, CONTROL host preflight generates
five independent opaque 32-byte identifiers with the already required Windows
CNG system-preferred RNG:

1. one nonzero `result_media_id` for a fresh 2,048-byte raw outcome medium;
2. `reserved_media_event_id`;
3. `admission_frozen_media_event_id`;
4. `pending_media_event_id`; and
5. `completion_media_event_id`.

All five values are reserved once in the existing project-lifetime TCB
admission/signer-media ledger and cannot appear in another route. Their
preallocation lets the appliance bind the planned completion event without
depending on a later event hash or decision. Event hashes still form the v0.2
sequence chain; preallocating an event ID does not pre-authorize its state.

For an import, the v0.2 admission record is replaced by this exact ASCII/LF
record:

```text
import_admission_schema=S0-SIGNER-IMPORT-ADMISSION-2
authority_id=control-host-preflight
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
import_class=<preactivation-context-v1, registry-binding-v1, or activation-binding-v1>
from_state=<the exact class-mapped source state>
to_state=<the exact class-mapped destination state>
package_sha256=<64 lowercase hex>
package_object_id=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
result_media_kind=import-outcome-v1
result_media_id=<64 lowercase hex, nonzero>
reserved_media_event_id=<64 lowercase hex>
admission_frozen_media_event_id=<64 lowercase hex>
pending_media_event_id=<64 lowercase hex>
completion_media_event_id=<64 lowercase hex>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_max_bytes=2048
admission_event_id=<byte-equal to admission_frozen_media_event_id>
decision=approved
```

The record has one final LF, no BOM, no CR, no extra field, and no trailing
space. Its SHA-256 is the import `admission_record_sha256`. Every identifier,
class, state, package, capability, and event ID is frozen before either medium
is attached.

### 2.3 Raw outcome medium and canonical frame

Every import attaches exactly two media while the target is powered off:

- the exact immutable read-only import ISO from v0.2; and
- one fresh, zero-filled, fixed-capacity 2,048-byte raw medium identified by
  the admission record's nonzero `result_media_id`.

The raw medium has no filesystem and is never mounted. The appliance writes at
most one canonical ASCII/LF frame whose fields are in this exact order:

```text
import_outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
tcb_service_id=S0-IMPORT-TRANSITION-TCB-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
import_class=<exact import class>
from_state=<exact class-mapped source state>
to_state=<exact class-mapped destination state>
package_sha256=<64 lowercase hex>
package_object_id=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
admission_record_sha256=<64 lowercase hex>
result_media_kind=import-outcome-v1
result_media_id=<64 lowercase hex>
reserved_media_event_id=<64 lowercase hex>
admission_frozen_media_event_id=<64 lowercase hex>
pending_media_event_id=<64 lowercase hex>
completion_media_event_id=<64 lowercase hex>
before_state=<exact source state>
after_state=<exact destination, exact source, or indeterminate>
before_configuration_state_sha256=<64 lowercase hex>
after_configuration_state_sha256=<64 lowercase hex or 64 zeroes only when indeterminate>
decision=<accepted or rejected>
reason=<none, parse-rejected, validation-rejected, or state-commit-failed>
outcome_body_sha256=<SHA-256 of every preceding frame byte including the LF after reason>
```

The frame has one final LF, no BOM, no CR, no extra field, and no trailing
space. Its complete byte length must be at most 2,048. Every byte after that
final LF through the end of the medium remains zero. The host computes
`outcome_frame_sha256` over the complete canonical frame including the final
hash line and LF; this value is evidence in the completion ledger event.

The frame rules are total:

- `accepted/none` requires `before_state=from_state`,
  `after_state=to_state`, two nonzero and unequal configuration-state hashes,
  and atomic persistence of the destination state before frame emission;
- `rejected/parse-rejected` or `rejected/validation-rejected` requires
  `before_state=after_state=from_state` and byte-equal nonzero configuration-
  state hashes;
- `rejected/state-commit-failed` requires `before_state=from_state`,
  `after_state=indeterminate`, and an all-zero after-state hash; and
- every other decision/reason/state/hash combination is malformed and becomes
  host classification `disagreement`.

### 2.4 Authority and claim boundary

`S0-IMPORT-TRANSITION-TCB-1` is the exact frozen import parser and atomic
state-transition service inside the target appliance image. It emits the frame
only after its final import decision. The frame is deliberately unsigned. It
is TCB state evidence authenticated by all of these bindings together:

- the externally pinned appliance image and launch-admission identity;
- the one-use capability and exact immutable ISO/result-medium object handles;
- the exact admission record and signer-media event identities;
- exclusive powered-off attachment and one-shot boot; and
- the frame body hash, complete frame hash, and existing ledger/witness chain.

The frame is not an Ed25519 artifact, PoP, registry authority, section-4
signature, experimental role statement, or cryptographic proof against a
malicious host/hypervisor. If the exact TCB image, launch admission, exclusive
medium binding, ledger, or witness is unavailable, the result is not trusted
and the candidate fails closed.

### 2.5 Host classification and state transition

After a route reaches `pending` and then controlled stop, the host detaches
both media before reading the raw outcome medium without mounting it. It
assigns exactly one classification in this precedence order:

1. `crash`: watchdog, process, appliance, or shutdown evidence records an
   abnormal end; any apparent frame is ignored;
2. `missing`: normal shutdown occurred but the medium is all zero or contains
   no complete frame;
3. `duplicate`: more than one outcome medium was attached, more than one
   magic/frame exists, or any nonzero byte follows the one canonical final LF;
4. `disagreement`: the frame is malformed, exceeds 2,048 bytes, has a bad body
   hash, mismatches any admission/event/object/state binding, conflicts with
   host launch/shutdown evidence, or conflicts with appliance anti-replay
   state;
5. `parse-rejected`, `validation-rejected`, or `state-commit-failed`: the one
   valid rejected frame names that exact reason; or
6. `accepted`: the one valid accepted frame and every host-bound field agree.

Only classification `accepted` permits the exact import state to advance and
the completion signer-media event to be `consumed/accepted`. Every other
classification prevents the intended state from being treated as available,
invalidates the candidate, and forbids retry or selective replay. When the
preallocated completion event ID is unused and the ledger/witness can perform
the exact append, the host records one `terminal/rejected` event. If that ID
already conflicts, the ledger or witness is unavailable, or the append fails,
no completion event is invented: the conflicting or failed append evidence
itself invalidates the candidate, and no new ID, append, or route is attempted.
An explicit target rejection is therefore distinguishable from a crash or
missing output but is not recoverable inside the candidate.

A failure detected before `pending` is not an import-outcome classification.
It follows the inherited admission lifecycle and, when the preallocated
completion ID and ledger/witness remain usable, terminates from the last
durable `reserved` or `admission-frozen` event with `outcome_class=none` and a
zero frame hash. A preallocation collision or unavailable ledger/witness
admits no new terminal append and fails the candidate on the existing
conflict evidence.

### 2.6 Import signer-media event grammar

Import routes use the existing `signer-media` ledger namespace but replace the
v0.2 import-event grammar with
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1`. It retains every v0.2 field and adds:

```text
result_media_id=<the route's nonzero outcome-medium ID>
result_media_kind=import-outcome-v1
reserved_media_event_id=<the preallocated reserved event ID>
admission_frozen_media_event_id=<the preallocated admission-frozen event ID>
pending_media_event_id=<the preallocated pending event ID>
completion_media_event_id=<the preallocated consumed-or-terminal event ID>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_frame_sha256=<64 zeroes before completion; exact complete-frame hash when one valid frame exists>
outcome_class=<none, accepted, parse-rejected, validation-rejected, state-commit-failed, crash, missing, duplicate, or disagreement>
before_appliance_state=<exact source state or none before pending>
after_appliance_state=<exact destination, exact source, indeterminate, or none before completion>
```

The successful order remains
`reserved -> admission-frozen -> pending -> consumed`. The four event records
must use their corresponding preallocated IDs, and each `prior_route_event_id`
must name the immediately preceding event. Before completion,
`outcome_frame_sha256` is zero, `outcome_class=none`, and state evidence is
`none` except that pending records the exact expected source state. Completion
after `pending` is one of:

- `consumed/accepted` with `outcome_class=accepted`, the exact frame hash,
  source and destination states; or
- `terminal/rejected` from `pending` with one exact non-accepted classification,
  available frame hash or zero when no valid frame exists, and the applicable
  source/unchanged/indeterminate state evidence.

An inherited pre-pending terminal may instead follow the rule in section 2.5.
No post-pending completion event may be appended before both media are detached
and the host classification is final. A reused capability or event binding
found after `pending` is `disagreement`; an additional outcome medium or frame
is `duplicate`. A conflicting completion ID or event, inability to append the
exact event, ledger/witness rollback, partial persistence, or unknown pending
state invalidates the candidate without claiming a new completion and without
retry.

Signing-request and offline-root result frames retain their v0.2 grammar and
behavior. Their ledger records do not silently acquire import-outcome
authority.

### 2.7 Persistence and cleanup

For a valid frame, CONTROL may retain the exact frame bytes and frame hash only
inside the already declared named ceremony evidence governed by the existing
TCB signer-media ledger/witness provider. This is not a 28th experimental
store. Rejected valid frames are retained as failure evidence but grant no
state authority. For crash, missing, duplicate, or malformed output, the host
retains the bounded raw observation and terminal classification without
inventing appliance success.

The import ISO and raw outcome medium remain TCB temporary replicas. After
evidence is sealed, both are destroyed under the inherited temporary-replica
rule before any later route can attach. This is operational deletion, not a
claim of cryptographic erasure. The target persistent disk retains only the
bounded IDs, hashes, decision, configuration state, and anti-replay state
already allowed by v0.2.

## 3. `TRI2-m01`: exact order-eight encoding derivation

The v0.2 attribution to RFC 9381 section 5.4.5 is removed. That section is not
the source of `bad_y2` or the four encodings, and v0.3 makes no such claim.

Let:

```text
p = 2^255 - 19
y0 = 2707385501144840649318225287225658788936804267575313519463743609750303402022
y1 = p - y0
```

Ed25519 point encoding stores the canonical 255-bit `y` value as 32
little-endian bytes and uses bit 255, the high bit of byte 31, for the `x` sign.
Applying that rule gives `TRI2-VEC-01: frozen order-eight encoding table`:

| y value | x-sign | Exact 32-byte lowercase hexadecimal encoding |
|---|---:|---|
| `y0` | 0 | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` |
| `y0` | 1 | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` |
| `y1` | 0 | `c7176a703d4d4141d8ab75eb1c3d6eff76ff3248ddd5e501831fc9f80b2e037a` |
| `y1` | 1 | `c7176a703d4d4141d8ab75eb1c3d6eff76ff3248ddd5e501831fc9f80b2e03fa` |

The derivation is independently checkable without trusting a copied label:

1. decode each 64-hex string as 32 little-endian bytes;
2. clear the high bit of byte 31 and require the resulting integer to equal
   exactly `y0` for the first pair and `p - y0` for the second pair;
3. require the two members of each pair to differ only in that high sign bit;
4. under the RFC 8032 canonical point decoder, reconstruct the corresponding
   point and require re-encoding to reproduce the same 32 bytes;
5. independently require `[8]P = I`, `[4]P != I`, and therefore exact order
   eight for every point; and
6. independently confirm `[L]P != I`, so `S0-ED25519-STRICT-1` rejects it.

The future implementation gate must freeze and verify these literal bytes,
their derivation, construction, canonical decoding, and point orders before
key generation. This design does not execute that check, produce an executable
vector artifact, or claim a cryptographic test result; it freezes only the
public literal specification above. The v0.2 strict order-`L` predicate, all
other hostile constructions, and the requirement for an independent future
construction/order check remain unchanged.

## 4. Finding dispositions and next boundary

| Finding | v0.3 proposal-text disposition |
|---|---|
| `TRI2-M01` | every state-changing import receives one bounded raw outcome medium, an exact unsigned TCB frame, preallocated noncircular event binding, total host classification, and consumed-versus-terminal ledger rules |
| `TRI2-m01` | the false RFC attribution is removed and replaced by an independently checkable arithmetic encoding rule plus four literal 32-byte encodings |

These are author-side closure proposals, not independent findings. The v0.3
package may proceed only to a future fresh independent design review after its
files and sidecars are frozen and the user opens that exact review gate.

Even a zero-finding review would authorize CONTROL integration consideration
only. It would not authorize implementation, a helper or validator, appliance
configuration, key or signature generation, cryptographic vector execution,
acceptance testing, protected material, fixtures, oracle, executors, provider
or model calls, E0 work, S0 execution, or `main` integration.
