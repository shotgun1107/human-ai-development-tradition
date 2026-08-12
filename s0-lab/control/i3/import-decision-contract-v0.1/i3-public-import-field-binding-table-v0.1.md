# S0 v0.14 I3 public import field-and-binding table v0.1

- `status`: public design candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT DESIGN OPEN`
- `design_base_commit`: `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7`
- `claim_kind`: exact field and binding design only
- `implementation_status`: not opened

## 1. Purpose and authority

This table is a readable index for the exact grammars in
`i3-public-import-decision-contract-v0.1.md`. It does not create another
record, loosen a grammar, or override the byte-identified I2 v0.4 contract.
If this table and the main contract differ, the candidate fails independent
review; an implementer must not choose the more permissive text.

The unchanged I2 event authority is the public JSON contract with SHA-256
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.
The I3 boundary and every source hash are recorded in the main contract.

Conventions:

- `Z`: exactly 64 ASCII zeroes;
- `HEX64`: exactly 64 lowercase ASCII hexadecimal characters;
- `NONZERO_HEX64`: `HEX64` other than `Z`;
- `R/A/P/C`: distinct reserved, admission-frozen, pending, and completion
  event IDs;
- `SRC/DST`: the source/destination states selected by the import class; and
- `H`: SHA-256 of all 26 canonical outcome lines including final LF.

## 2. Admission record fields

The admission record has exactly 21 fields in this order.

| # | Field | Exact domain or source | Required binding |
|---:|---|---|---|
| 1 | `import_admission_schema` | literal `S0-SIGNER-IMPORT-ADMISSION-2` | selects this grammar only |
| 2 | `authority_id` | literal `control-host-preflight` | names the existing public preflight authority; grants no new authority |
| 3 | `campaign_id` | `HEX64` | byte-equal in outcome and all four I2 route events |
| 4 | `ceremony_id` | `HEX64` | byte-equal in outcome and all four I2 route events |
| 5 | `signer_id` | exact non-root I1 registry role ID | byte-equal in outcome and all route events |
| 6 | `import_class` | one of three allowed classes | selects exactly one `SRC/DST` mapping; byte-equal in outcome and events |
| 7 | `from_state` | exact mapped `SRC` | byte-equal in outcome; binds event before-state rules |
| 8 | `to_state` | exact mapped `DST` | byte-equal in outcome; binds accepted event after-state |
| 9 | `package_sha256` | `HEX64` | byte-equal in outcome and route events |
| 10 | `package_object_id` | `HEX64` | byte-equal in outcome and route events |
| 11 | `attachment_capability_id` | `HEX64` | byte-equal in outcome and route events; one supplied route only |
| 12 | `result_media_kind` | literal `import-outcome-v1` | byte-equal in outcome and route events |
| 13 | `result_media_id` | `NONZERO_HEX64` | byte-equal in outcome and route events; distinct from `R/A/P/C` |
| 14 | `reserved_media_event_id` | `NONZERO_HEX64` (`R`) | exact reserved event ID and first route-chain position |
| 15 | `admission_frozen_media_event_id` | `NONZERO_HEX64` (`A`) | exact admission-frozen event ID; equals field 20 |
| 16 | `pending_media_event_id` | `NONZERO_HEX64` (`P`) | exact pending event ID |
| 17 | `completion_media_event_id` | `NONZERO_HEX64` (`C`) | exact one-use completion event ID |
| 18 | `outcome_schema` | literal `S0-SIGNER-IMPORT-OUTCOME-1` | byte-equal to outcome field 1 |
| 19 | `outcome_max_bytes` | canonical literal `2048` | binds fixed raw-medium capacity |
| 20 | `admission_event_id` | exact bytes of `A` | no additional event identity |
| 21 | `decision` | literal `approved` | no denied alternative is serialized under this schema |

The admission record hash is SHA-256 of all 21 ordered lines, including LF
after line 21. Any missing, extra, duplicate, reordered, or noncanonical field
is a parse failure. `R`, `A`, `P`, `C`, and `result_media_id` are pairwise
distinct within the supplied route; project-lifetime uniqueness is outside I3.

## 3. Outcome record fields

The outcome frame has exactly 26 fields in this order.

| # | Field | Exact domain or source | Required binding |
|---:|---|---|---|
| 1 | `import_outcome_schema` | literal `S0-SIGNER-IMPORT-OUTCOME-1` | equals admission field 18 |
| 2 | `tcb_service_id` | literal `S0-IMPORT-TRANSITION-TCB-1` | names existing unsigned TCB producer; is not a signer |
| 3 | `campaign_id` | `HEX64` | equals admission field 3 and route events |
| 4 | `ceremony_id` | `HEX64` | equals admission field 4 and route events |
| 5 | `signer_id` | exact non-root I1 registry role ID | equals admission field 5 and route events |
| 6 | `import_class` | one allowed class | equals admission field 6 and selects the same route |
| 7 | `from_state` | mapped `SRC` | equals admission field 7 |
| 8 | `to_state` | mapped `DST` | equals admission field 8 |
| 9 | `package_sha256` | `HEX64` | equals admission field 9 and route events |
| 10 | `package_object_id` | `HEX64` | equals admission field 10 and route events |
| 11 | `attachment_capability_id` | `HEX64` | equals admission field 11 and route events |
| 12 | `admission_event_id` | `HEX64` | equals admission `A` and admission field 20 |
| 13 | `admission_record_sha256` | `HEX64` | equals SHA-256 of the exact 21-line admission bytes |
| 14 | `result_media_kind` | literal `import-outcome-v1` | equals admission field 12 and route events |
| 15 | `result_media_id` | `NONZERO_HEX64` | equals admission field 13 and route events |
| 16 | `reserved_media_event_id` | `NONZERO_HEX64` (`R`) | equals admission field 14 and route events |
| 17 | `admission_frozen_media_event_id` | `NONZERO_HEX64` (`A`) | equals admission field 15 and route events |
| 18 | `pending_media_event_id` | `NONZERO_HEX64` (`P`) | equals admission field 16 and route events |
| 19 | `completion_media_event_id` | `NONZERO_HEX64` (`C`) | equals admission field 17 and completion event ID |
| 20 | `before_state` | exact `SRC` | equals admission field 7 and event before-state when post-pending |
| 21 | `after_state` | allowed tuple value | binds the exact outcome class and event after-state |
| 22 | `before_configuration_state_sha256` | `NONZERO_HEX64` | binds tuple and post-pending event before-configuration hash |
| 23 | `after_configuration_state_sha256` | `HEX64` | binds tuple and post-pending event after-configuration hash |
| 24 | `decision` | `accepted` or `rejected` | valid only in one of the four frozen tuples |
| 25 | `reason` | `none`, `parse-rejected`, `validation-rejected`, or `state-commit-failed` | valid only in its matching tuple |
| 26 | `outcome_body_sha256` | `HEX64` | equals SHA-256 of lines 1-25 including LF after line 25 |

The full frame hash `H` covers all 26 ordered lines including LF after line
26. The complete frame starts at raw-medium byte zero, ends within 2,048
bytes, and is followed only by zero bytes. The padding is not part of `H`.

## 4. Valid outcome tuples

| Public outcome class | Frame tuple | State requirement | Configuration-hash requirement | Frame hash |
|---|---|---|---|---|
| `accepted` | `accepted/none` | `SRC` to `DST` | both nonzero and unequal | `H` |
| `parse-rejected` | `rejected/parse-rejected` | `SRC` to `SRC` | byte-equal and nonzero | `H` |
| `validation-rejected` | `rejected/validation-rejected` | `SRC` to `SRC` | byte-equal and nonzero | `H` |
| `state-commit-failed` | `rejected/state-commit-failed` | `SRC` to `indeterminate` | before nonzero; after `Z` | `H` |

No other tuple is canonical. A syntactically complete frame with another tuple
is classified `disagreement`, not converted into the nearest valid class.

## 5. Cross-object bindings

| Binding ID | Objects | Exact rule | Failure result after pending |
|---|---|---|---|
| `I3-B01` | admission bytes to admission hash | recompute over all 21 canonical lines | `disagreement`; frame hash `H` only if frame itself is canonical and unique |
| `I3-B02` | admission to outcome | schema, route, identities, package, capability, medium, `R/A/P/C`, `A`, and admission hash all agree | `disagreement` |
| `I3-B03` | class to state | class selects only its frozen `SRC/DST` pair | `disagreement` |
| `I3-B04` | outcome body to body hash | recompute over outcome lines 1-25 with final LF | `disagreement`; frame hash `Z` because frame is internally malformed |
| `I3-B05` | frame to `H` | recompute over all 26 canonical lines with final LF | use recomputed `H`; never caller-selected |
| `I3-B06` | medium to frame | one 2,048-byte medium, frame at byte zero, zero tail | `missing`, `duplicate`, or `disagreement` by ordered table |
| `I3-B07` | admission/outcome to I2 events | exact campaign, ceremony, signer, route, object, capability, medium and event identities | `disagreement` or `no-completion-claim` |
| `I3-B08` | event lifecycle | exact `R -> A -> P -> C` route-local IDs and I2 global/route chain rules | no substitute event; no retry |
| `I3-B09` | outcome to completion event | outcome class, `H/Z`, before/after state and configuration hashes match the exact I2 variant | `no-completion-claim` if finalization event differs |
| `I3-B10` | accepted to authority | exact consumed event exists and append status is `persisted` | destination unavailable otherwise |

The classification stage and finalization stage are separate. A frame may be
classified `accepted` while finalization still returns
`no-completion-claim`; such a result grants no destination-state authority.

## 6. Caller-supplied classification facts

The fact set is a typed function argument, not canonical evidence and not a
new record.

| Fact group | Members | Allowed values | Use |
|---|---|---|---|
| lifecycle | `last_durable_phase` | `reserved`, `admission-frozen`, `pending` | chooses pre-pending or post-pending path |
| end | `end_observation` | `not-started`, `normal`, `abnormal`, `unknown` | first post-pending precedence decision |
| raw medium | `outcome_media_count`, optional `outcome_media_bytes` | nonnegative integer; bytes only when count is one | missing/duplicate/frame scan |
| launch/media | launch, ISO, outcome-medium, detach/raw-read statuses | `exact`, `conflict`, `unavailable` | cross-evidence consistency |
| route/state | route-event, anti-replay, host-state statuses | `exact`, `conflict`, `unavailable` | cross-evidence consistency |
| persistence view | ledger/witness snapshot status | `exact`, `conflict`, `unavailable` | classification consistency only; final append is separate |

`exact` is a supplied fact value, not an I3 proof of real-world truth. A
malformed fact-set object raises a stable API input error. Every well-typed
fact set maps to exactly one public classification or pre-pending `none`.

## 7. Finalization bindings

| Classification phase | Required exact I2 completion | Required append | Public disposition | Destination |
|---|---|---|---|---|
| pre-pending `none` | direct terminal from exact last durable phase | `persisted` | `terminal-rejected` | unavailable |
| post-pending `accepted` | `consumed/accepted` using `C` and `H` | `persisted` | `consumed-accepted` | exact `DST` available |
| other post-pending class | `terminal/rejected` using `C` and required `H/Z` | `persisted` | `terminal-rejected` | unavailable |
| any phase with absent, malformed, mismatching, conflicting, unavailable, or unpersisted completion | none accepted | any non-`persisted` or mismatch | `no-completion-claim` | unavailable |

The finalizer does not reclassify the attempt, repair evidence, redraw an ID,
append a replacement, or authorize retry.

## 8. Closed boundary

This table is not implementation or execution evidence. It neither proves nor
implements a host, appliance, raw medium, registry, signer, ledger, witness,
atomic append, durable state, key, signature, VM, provider, protected input,
F0, fixture, oracle, executor, judge, E0, or S0.
