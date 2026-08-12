# S0 v0.14 I3 public import classification table v0.1

- `status`: public design candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT DESIGN OPEN`
- `design_base_commit`: `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7`
- `claim_kind`: total deterministic classification design only
- `implementation_status`: not opened

## 1. Purpose

This document makes the I3 import decision total and mechanically testable.
It is subordinate to the exact 21-line admission and 26-line outcome grammars
in `i3-public-import-decision-contract-v0.1.md` and to the unchanged I2 v0.4
event contract whose SHA-256 is
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

The table classifies supplied public facts. It does not observe a real host,
prove a caller truthful, append an event, or grant authority.

## 2. Typed-input gate

The classifier first checks only the type and closed value domain of the fact
set. A malformed object produces one stable `I3_INPUT_ERROR`; it is not called
`crash`, `missing`, `duplicate`, `disagreement`, or a target rejection.

A well-typed fact set has:

- one `last_durable_phase` in `reserved`, `admission-frozen`, `pending`;
- one `end_observation` in `not-started`, `normal`, `abnormal`, `unknown`;
- one nonnegative integer `outcome_media_count`;
- exact byte content only when the count is one and no byte content otherwise;
- exactly eight status fields, each in `exact`, `conflict`, `unavailable`; and
- optional admission bytes represented only as absent or exact bytes.

The eight statuses are launch admission, ISO attachment, outcome medium,
detachment/raw read, route-event binding, anti-replay, host state, and
ledger/witness snapshot.

After this gate, every input follows exactly one row below. Earlier rows have
strict precedence. A later row cannot replace an earlier result merely because
its evidence also appears true.

## 3. Pre-pending decision

| Row | Predicate | Outcome class | Frame hash | Required completion |
|---|---|---|---|---|
| `PRE-R` | `last_durable_phase=reserved` | `none` | `Z` | exact I2 direct terminal from reserved |
| `PRE-A` | `last_durable_phase=admission-frozen` | `none` | `Z` | exact I2 direct terminal from admission-frozen |

These rows represent a route that did not reach pending. No outcome-frame
class is inferred from any apparent bytes. The finalizer grants
`terminal-rejected` only if the matching direct-terminal event is supplied
and its append status is `persisted`; otherwise it returns
`no-completion-claim`. There is no destination authority or retry.

## 4. Derived scan facts for pending routes

For `last_durable_phase=pending`, the raw scan derives values without choosing
the most favorable frame:

| Derived fact | Definition |
|---|---|
| `medium_exact` | count is one and supplied bytes are exactly 2,048 bytes |
| `schema_prefix_count` | literal byte occurrences of `import_outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1` in the one medium; zero if no one medium |
| `complete_at_zero` | byte zero begins a block of exactly 26 LF-terminated nonempty lines ending at a candidate line 26; syntax may still be invalid |
| `complete_candidate_count` | number of structurally complete 26-line candidates beginning at an outcome-schema prefix |
| `candidate_end` | byte immediately after LF terminating candidate line 26, when exactly one candidate at byte zero exists |
| `nonzero_tail` | at least one nonzero byte from `candidate_end` through byte 2047 |
| `canonical_frame` | the unique candidate passes strict bytes, field order/domains, route tuple, and body-hash checks |
| `H` | SHA-256 of all bytes of that canonical 26-line frame including final LF |
| `all_bindings_exact` | admission is canonical and every admission/outcome/event/object/state/status binding is exact |

`complete_at_zero` is only a structural delimiter test. A 26-line block with a
wrong name, value, order, body hash, or tuple is complete but noncanonical and
therefore reaches disagreement rather than missing.

## 5. Complete ordered pending table

| Order | Row ID | Exact predicate after earlier rows failed | Class | Frame hash | Before/after public state |
|---:|---|---|---|---|---|
| 1 | `P-CRASH` | `end_observation=abnormal` | `crash` | `Z` | `SRC` to `indeterminate`; apparent result ignored |
| 2 | `P-MISSING` | end is `normal`; count is one; medium is exactly 2,048 bytes; no duplicate predicate is true; and the medium is all zero or both `complete_at_zero=false` and `complete_candidate_count=0` | `missing` | `Z` | `SRC` to `indeterminate`; destination unavailable |
| 3 | `P-DUPLICATE` | count is greater than one, or one medium has `schema_prefix_count>1`, `complete_candidate_count>1`, or `nonzero_tail=true` | `duplicate` | `Z` | `SRC` to `indeterminate`; select no frame |
| 4 | `P-DISAGREE-BYTES` | count is zero; count/bytes contradict; one medium is not 2,048 bytes; end is `unknown` or `not-started`; a complete block at byte zero is noncanonical; or one complete candidate appears only at a nonzero offset | `disagreement` | `Z` | `SRC` to `indeterminate`; no destination authority |
| 5 | `P-DISAGREE-BINDING` | exactly one internally canonical frame exists but admission is absent/noncanonical, a cross-binding differs, or any required status is not `exact` | `disagreement` | `H` | `SRC` to `indeterminate`; prefer neither side |
| 6 | `P-PARSE-REJECTED` | canonical frame, all bindings exact, tuple `rejected/parse-rejected` | `parse-rejected` | `H` | `SRC` to `SRC` |
| 7 | `P-VALIDATION-REJECTED` | canonical frame, all bindings exact, tuple `rejected/validation-rejected` | `validation-rejected` | `H` | `SRC` to `SRC` |
| 8 | `P-STATE-COMMIT-FAILED` | canonical frame, all bindings exact, tuple `rejected/state-commit-failed` | `state-commit-failed` | `H` | `SRC` to `indeterminate` |
| 9 | `P-ACCEPTED` | canonical frame, all bindings exact, tuple `accepted/none` | `accepted` | `H` | proposed `SRC` to `DST`; no authority yet |

The `P-MISSING` row explicitly requires one medium. Consequently, a missing
physical medium is not confused with an empty outcome written to the one
preallocated medium. It reaches `P-DISAGREE-BYTES`; both results fail closed.

The duplicate predicate is evaluated as part of the missing exclusion as well
as at row 3. Thus multiple media or frames cannot be hidden by a missing first
candidate even though inherited class names retain crash-before-missing-
before-duplicate precedence.

## 6. Representative overlap resolution

| Observation | Potential overlap | Required result and reason |
|---|---|---|
| abnormal end plus a valid-looking frame | crash versus explicit result | `crash`; abnormal end is first and apparent bytes are ignored |
| normal end, two zero media | missing versus duplicate | `duplicate`; missing requires exactly one medium |
| normal end, one partial 12-line write | missing versus disagreement | `missing`; no structurally complete 26-line candidate exists |
| normal end, one complete 26-line block with a bad body hash | missing versus disagreement | `disagreement` with `Z`; complete candidate exists but is internally malformed |
| normal end, one complete candidate beginning after byte zero | missing versus disagreement | `disagreement` with `Z`; frames must begin at byte zero |
| normal end, canonical frame plus nonzero byte after final LF | explicit result versus duplicate | `duplicate`; nonzero tail precedes frame interpretation |
| normal end, canonical accepted frame with wrong campaign | accepted versus disagreement | `disagreement` with `H`; frame is internally valid but external binding differs |
| normal end, canonical rejection frame with unavailable witness snapshot | rejection versus disagreement | `disagreement` with `H`; all required statuses must be exact |
| pending plus no physical medium | missing versus disagreement | `disagreement` with `Z`; the expected medium observation itself is absent |

These rows are classification rules, not statements that all failure classes
are operationally equally useful. They exist so two implementations cannot
silently label the same supplied facts differently.

## 7. Exact class outputs

For every well-typed fact set, `ImportClassification` contains at least:

| Output | Exact domain |
|---|---|
| `last_durable_phase` | copied closed enum |
| `outcome_class` | `none`, `accepted`, `parse-rejected`, `validation-rejected`, `state-commit-failed`, `crash`, `missing`, `duplicate`, or `disagreement` |
| `outcome_frame_sha256` | exactly `H` or `Z` as tabled |
| `before_appliance_state` | `none` before pending; exact `SRC` after pending |
| `after_appliance_state` | `none` before pending; `DST` for accepted; `SRC` for parse/validation rejection; `indeterminate` for every other post-pending class |
| `required_completion_kind` | `direct-terminal-reserved`, `direct-terminal-admission-frozen`, `terminal-rejected`, or `consumed-accepted` |
| `destination_authority` | always `unavailable` at classification time |

This is an in-memory public result contract, not a canonical serialized record.
I3 does not add it to the experimental topology or ledger namespace.

## 8. Completion finalizer table

The finalizer does not rerun or change classification.

| Order | Classification | Supplied event and append | Disposition | Destination authority |
|---:|---|---|---|---|
| 1 | pre-pending `none` | exact phase-matching I2 direct terminal; `persisted` | `terminal-rejected` | unavailable |
| 2 | pending `accepted` | exact I2 `consumed/accepted` event using `C`, `H`, and matching states/hashes; `persisted` | `consumed-accepted` | exact `DST` available |
| 3 | pending non-accepted | exact I2 `terminal/rejected` event using `C` and table-required `H/Z`; `persisted` | `terminal-rejected` | unavailable |
| 4 | any | missing, malformed, wrong-variant, wrong-ID, wrong-hash, conflicting, unavailable, failed, or unpersisted completion | `no-completion-claim` | unavailable |

An `accepted` classification alone never authorizes `DST`. A failed or unknown
append cannot be repaired by a second event, new ID, replay, inferred success,
or retry.

## 9. Totality proof obligation

A later implementation test must show, for the full well-typed public input
domain or an independently justified exhaustive partition, that:

1. every input selects one and only one pre-pending or pending row;
2. the same input always selects the same row;
3. missing and duplicate never both match;
4. a complete malformed frame never becomes missing;
5. no explicit rejection or acceptance precedes crash, missing, duplicate, or
   disagreement;
6. only a canonical unique frame can produce `H`;
7. only row 2 of the finalizer can make `DST` available; and
8. invalid typed input yields only stable `I3_INPUT_ERROR`, never a partially
   populated experimental class.

No test is executed under this design gate.

## 10. Closed boundary

This table does not implement platform observations, durable storage, ledger
or witness truth, atomic append, registry or cryptographic authority,
project-lifetime replay protection, same-process hostility, VM/provider
isolation, F0, fixture/oracle, E0, or S0.
