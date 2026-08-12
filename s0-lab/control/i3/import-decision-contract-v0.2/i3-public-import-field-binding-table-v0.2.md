# S0 v0.14 I3 public import field-and-binding table v0.2

- `status`: bounded public design revision candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 BOUNDED DESIGN REVISION OPEN`
- `responds_to_review_sha256`: `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c`
- `claim_kind`: exact field and binding design only
- `implementation_status`: not opened

## 1. Authority and conventions

This table indexes the complete v0.2 main contract. It creates no additional
record or authority. A contradiction between the documents fails the package;
an implementation cannot choose the more permissive text.

The unchanged I2 v0.4 event contract SHA-256 is
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

Conventions: `Z` is 64 ASCII zeroes; `HEX64` is 64 lowercase ASCII hex;
`NONZERO_HEX64` excludes `Z`; `R/A/P/C` are the distinct route event IDs;
`SRC/DST` are selected by import class; `H` hashes all 26 canonical outcome
lines including final LF.

## 2. Admission fields

The record has exactly 21 fields in this order.

| # | Field | Exact domain/source | Required binding |
|---:|---|---|---|
| 1 | `import_admission_schema` | literal `S0-SIGNER-IMPORT-ADMISSION-2` | selects this grammar only |
| 2 | `authority_id` | literal `control-host-preflight` | names existing public preflight; grants no new authority |
| 3 | `campaign_id` | `HEX64` | outcome and all route events |
| 4 | `ceremony_id` | `HEX64` | outcome and all route events |
| 5 | `signer_id` | exact non-root I1 registry role ID | outcome and all route events |
| 6 | `import_class` | one allowed class | selects one `SRC/DST`; outcome and events |
| 7 | `from_state` | mapped `SRC` | outcome and event lifecycle |
| 8 | `to_state` | mapped `DST` | outcome and accepted completion |
| 9 | `package_sha256` | `HEX64` | outcome and route events |
| 10 | `package_object_id` | `HEX64` | outcome and route events |
| 11 | `attachment_capability_id` | `HEX64` | outcome and route events |
| 12 | `result_media_kind` | literal `import-outcome-v1` | outcome and route events |
| 13 | `result_media_id` | `NONZERO_HEX64` | outcome/events; distinct from `R/A/P/C` |
| 14 | `reserved_media_event_id` | `NONZERO_HEX64` (`R`) | exact reserved event |
| 15 | `admission_frozen_media_event_id` | `NONZERO_HEX64` (`A`) | exact admission-frozen event; equals field 20 |
| 16 | `pending_media_event_id` | `NONZERO_HEX64` (`P`) | exact pending event |
| 17 | `completion_media_event_id` | `NONZERO_HEX64` (`C`) | exact one-use completion event |
| 18 | `outcome_schema` | literal `S0-SIGNER-IMPORT-OUTCOME-1` | outcome field 1 |
| 19 | `outcome_max_bytes` | literal `2048` | fixed raw-medium size |
| 20 | `admission_event_id` | exact bytes of `A` | no additional event identity |
| 21 | `decision` | literal `approved` | only admitted record under this schema |

The admission hash covers all 21 ordered lines including final LF. Every field
is required exactly once. `R/A/P/C/result_media_id` are pairwise distinct for
the supplied route.

## 3. Outcome fields

The frame has exactly 26 fields in this order.

| # | Field | Exact domain/source | Required binding |
|---:|---|---|---|
| 1 | `import_outcome_schema` | literal `S0-SIGNER-IMPORT-OUTCOME-1` | admission field 18 |
| 2 | `tcb_service_id` | literal `S0-IMPORT-TRANSITION-TCB-1` | existing unsigned TCB producer; not a signer |
| 3 | `campaign_id` | `HEX64` | admission field 3 and route events |
| 4 | `ceremony_id` | `HEX64` | admission field 4 and route events |
| 5 | `signer_id` | exact non-root I1 registry role ID | admission field 5 and route events |
| 6 | `import_class` | one allowed class | admission field 6; selects same route |
| 7 | `from_state` | mapped `SRC` | admission field 7 |
| 8 | `to_state` | mapped `DST` | admission field 8 |
| 9 | `package_sha256` | `HEX64` | admission field 9 and route events |
| 10 | `package_object_id` | `HEX64` | admission field 10 and route events |
| 11 | `attachment_capability_id` | `HEX64` | admission field 11 and route events |
| 12 | `admission_event_id` | `HEX64` | admission `A` and field 20 |
| 13 | `admission_record_sha256` | `HEX64` | SHA-256 of exact 21-line admission bytes |
| 14 | `result_media_kind` | literal `import-outcome-v1` | admission field 12 and route events |
| 15 | `result_media_id` | `NONZERO_HEX64` | admission field 13 and route events |
| 16 | `reserved_media_event_id` | `NONZERO_HEX64` (`R`) | admission field 14 and route events |
| 17 | `admission_frozen_media_event_id` | `NONZERO_HEX64` (`A`) | admission field 15 and route events |
| 18 | `pending_media_event_id` | `NONZERO_HEX64` (`P`) | admission field 16 and route events |
| 19 | `completion_media_event_id` | `NONZERO_HEX64` (`C`) | admission field 17 and completion event ID |
| 20 | `before_state` | exact `SRC` | tuple; I2 event before state |
| 21 | `after_state` | exact tuple value | tuple; I2 event after state |
| 22 | `before_configuration_state_sha256` | `NONZERO_HEX64` | internal outcome-tuple check; committed by `H`, no direct I2 field |
| 23 | `after_configuration_state_sha256` | `HEX64` | internal outcome-tuple check; committed by `H`, no direct I2 field |
| 24 | `decision` | `accepted` or `rejected` | one of four frozen tuples |
| 25 | `reason` | one frozen reason | one of four frozen tuples |
| 26 | `outcome_body_sha256` | `HEX64` | SHA-256 of lines 1-25 including LF after line 25 |

`H` covers all 26 lines including final LF. The frame begins at byte zero of
one 2,048-byte medium and has only zero padding after line 26.

## 4. Outcome tuples and I2 event values

| Class | Frame tuple | Outcome before/after | Configuration rule | I2 event before/after/hash |
|---|---|---|---|---|
| `accepted` | `accepted/none` | `SRC/DST` | nonzero and unequal | `SRC/DST/H` |
| `parse-rejected` | `rejected/parse-rejected` | `SRC/SRC` | equal and nonzero | `SRC/SRC/H` |
| `validation-rejected` | `rejected/validation-rejected` | `SRC/SRC` | equal and nonzero | `SRC/SRC/H` |
| `state-commit-failed` | `rejected/state-commit-failed` | `SRC/indeterminate` | before nonzero; after `Z` | `SRC/indeterminate/H` |
| `crash` | no selected frame | none | none | `SRC/indeterminate/Z` |
| `missing` | no selected frame | none | none | `SRC/indeterminate/Z` |
| `duplicate` | no selected frame | none | none | `SRC/indeterminate/Z` |
| `disagreement` | unique canonical frame or no selected frame | do not trust frame state | tuple checked only if frame canonical | `SRC/indeterminate/H` for one unique canonical frame; otherwise `SRC/indeterminate/Z` |

The configuration hashes never compare to nonexistent I2 fields. For an
H-bearing class, the I2 event's actual `outcome_frame_sha256=H` transitively
commits them as frame bytes.

## 5. Exact cross-object bindings

| ID | Objects | Exact rule | Failure after pending |
|---|---|---|---|
| `I3-B01` | admission bytes/hash | recompute over all 21 canonical lines | disagreement; `H` only if frame independently canonical/unique |
| `I3-B02` | admission/outcome | schema, route, identity, package, capability, medium, `R/A/P/C`, `A`, admission hash agree | disagreement |
| `I3-B03` | class/state | class selects only frozen `SRC/DST` | disagreement |
| `I3-B04` | outcome body/hash | recompute lines 1-25 including LF | disagreement with `Z` |
| `I3-B05` | frame/`H` | recompute all 26 lines including LF; never caller-selected | use recomputed `H` |
| `I3-B06` | media/frame | derived media sequence length; one 2,048-byte member; frame at zero; zero tail | missing, duplicate, or disagreement by ordered table |
| `I3-B07` | records/I2 events | compare only actual shared I2 fields: campaign, ceremony, signer, route, package/object, capability, media IDs, `R/A/P/C`, admission tuple, outcome class, frame hash, appliance states | disagreement or no-completion-claim |
| `I3-B08` | lifecycle | exact `R -> A -> P -> C`, I2 global chain, route-local chain | no substitute event or retry |
| `I3-B09` | frame/I2 completion | exact class, `H/Z`, and before/after state; `H` commits the full frame including configuration hashes | no-completion-claim if final event differs |
| `I3-B10` | accepted/authority | exact consumed event plus append `persisted` | destination unavailable otherwise |

## 6. Classification fact bindings

| Fact group | Exact representation | Use |
|---|---|---|
| lifecycle | one closed `last_durable_phase` enum | pre-pending versus pending |
| end | one closed `end_observation` enum | crash, normal result, or host-evidence disagreement |
| media | one immutable finite `outcome_media_observations` sequence of byte strings | count derived as length; empty/one/multiple classified |
| launch/media statuses | four closed `exact/conflict/unavailable` enums | external evidence consistency |
| route/state statuses | three closed `exact/conflict/unavailable` enums | external evidence consistency |
| persistence view | one closed `exact/conflict/unavailable` enum | classification evidence only; append handled later |
| admission | absent or exact bytes | parser and binding evidence |

There is no caller-supplied `outcome_media_count`. A malformed sequence or
non-byte member is `I3_INPUT_ERROR`; an empty, one-member, or multiple-member
byte sequence is well typed and reaches the classification table.

## 7. Completion binding

| Phase/class | Required exact I2 completion | Append | Disposition | Destination |
|---|---|---|---|---|
| pre-pending `none` | direct terminal from exact phase | `persisted` | `terminal-rejected` | unavailable |
| `accepted` | consumed/accepted using `C`, `H`, `SRC/DST` | `persisted` | `consumed-accepted` | `DST` available |
| other post-pending | terminal/rejected using `C`, tabled `H/Z`, `SRC` and tabled after-state | `persisted` | `terminal-rejected` | unavailable |
| any mismatch or append not persisted | no event accepted | any | `no-completion-claim` | unavailable |

No result redraws an ID, retries, invents append success, changes the class, or
creates a configuration-hash field in I2.

## 8. Closed boundary

This table is design only. It does not implement or validate real media,
platform observations, durable state, ledger/witness, atomic append, registry,
keys, signatures, VM/provider isolation, F0, fixture/oracle, E0, or S0.
