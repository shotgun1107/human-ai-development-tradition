# S0 v0.14 I3 public import-decision contract v0.2

- `status`: bounded public design revision candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 BOUNDED DESIGN REVISION OPEN`
- `revision_base_commit`: `d2167aebe6b295b99982bed15f5a0d79720c899d`
- `responds_to_review_sha256`: `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c`
- `claim_kind`: model-free public contract design only
- `implementation_status`: not opened

## 1. Revision decision and replacement map

This package completely replaces the four v0.1 I3 design artifacts for future
I3 interpretation. The v0.1 package and its independent review remain
historical evidence and are not edited.

The revision is limited to the three authenticated findings:

| Finding | v0.2 resolution |
|---|---|
| `I3-IR-B01` | one uniquely selectable internally canonical frame always contributes full-frame hash `H`, including when end evidence is `unknown` or `not-started`; `Z` is reserved for no such frame, crash, missing, duplicate, or internally invalid/non-unique bytes |
| `I3-IR-M01` | the caller supplies one `outcome_media_observations` sequence; its length is the only media count, so no count/bytes contradiction exists in the typed domain |
| `I3-IR-M02` | configuration-state hashes are validated inside the outcome frame and committed transitively by event field `outcome_frame_sha256=H`; no nonexistent I2 configuration-hash field or direct equality is required |

No other I3 scope is added. This revision does not modify the authenticated I2
v0.4 event contract with SHA-256
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

## 2. Contract layers and common lexical rules

I3 defines the relationship among:

1. exact 21-line `S0-SIGNER-IMPORT-ADMISSION-2` bytes;
2. exact 26-line `S0-SIGNER-IMPORT-OUTCOME-1` bytes;
3. the unchanged I2 v0.4 31-line
   `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1`; and
4. pure classification and finalization results that are not new canonical
   records or authorities.

The noncompensatory layers are canonical byte validity, cross-record
structural consistency, ordered classification, and completion finalization.
Passing one cannot repair failure at another.

Let:

- `Z` be exactly 64 ASCII `0` bytes;
- `HEX64` be exactly 64 lowercase ASCII hexadecimal characters;
- `NONZERO_HEX64` be `HEX64` other than `Z`;
- `LF` be byte `0A`;
- `R/A/P/C` be distinct nonzero reserved, admission-frozen, pending, and
  completion event IDs; and
- `H` be SHA-256 of all 26 canonical outcome lines including final LF.

Admission and outcome records are strict ASCII `name=value` lines in declared
order, each followed by LF including the last line. BOM, CR, NUL, blank line,
trailing space/tab, non-ASCII, missing/duplicate/reordered/unknown/extra field,
or missing final LF rejects canonical parsing.

The exact route mapping is:

| Import class | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

Identifiers, object IDs, hashes, capability, media ID, and event IDs compare
byte-for-byte. Trimming, case folding, Unicode normalization, numeric
reinterpretation, and aliases are forbidden.

## 3. Exact admission grammar

`S0-SIGNER-IMPORT-ADMISSION-2` is exactly these 21 lines:

```text
import_admission_schema=S0-SIGNER-IMPORT-ADMISSION-2
authority_id=control-host-preflight
campaign_id=<HEX64>
ceremony_id=<HEX64>
signer_id=<exact non-root I1 registry role ID>
import_class=<one allowed import class>
from_state=<exact class-mapped SRC>
to_state=<exact class-mapped DST>
package_sha256=<HEX64>
package_object_id=<HEX64>
attachment_capability_id=<HEX64>
result_media_kind=import-outcome-v1
result_media_id=<NONZERO_HEX64>
reserved_media_event_id=<NONZERO_HEX64 R>
admission_frozen_media_event_id=<NONZERO_HEX64 A>
pending_media_event_id=<NONZERO_HEX64 P>
completion_media_event_id=<NONZERO_HEX64 C>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_max_bytes=2048
admission_event_id=<byte-equal to A>
decision=approved
```

The authenticated v0.3 source freezes this complete ordered block without a
numeric count; I3 freezes the derived count as 21. No version field exists.

```text
admission_record_sha256 = SHA-256(all 21 canonical lines including final LF)
```

`R`, `A`, `P`, `C`, and `result_media_id` are pairwise distinct within the
supplied route. Project-lifetime uniqueness remains outside I3.
`admission_event_id` is exactly `A`, not another event ID.

## 4. Exact outcome grammar

`S0-SIGNER-IMPORT-OUTCOME-1` is exactly these 26 lines:

```text
import_outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
tcb_service_id=S0-IMPORT-TRANSITION-TCB-1
campaign_id=<HEX64>
ceremony_id=<HEX64>
signer_id=<exact non-root I1 registry role ID>
import_class=<one allowed import class>
from_state=<exact class-mapped SRC>
to_state=<exact class-mapped DST>
package_sha256=<HEX64>
package_object_id=<HEX64>
attachment_capability_id=<HEX64>
admission_event_id=<HEX64>
admission_record_sha256=<HEX64>
result_media_kind=import-outcome-v1
result_media_id=<NONZERO_HEX64>
reserved_media_event_id=<NONZERO_HEX64 R>
admission_frozen_media_event_id=<NONZERO_HEX64 A>
pending_media_event_id=<NONZERO_HEX64 P>
completion_media_event_id=<NONZERO_HEX64 C>
before_state=<exact SRC>
after_state=<DST, SRC, or indeterminate as allowed below>
before_configuration_state_sha256=<NONZERO_HEX64>
after_configuration_state_sha256=<HEX64>
decision=<accepted or rejected>
reason=<none, parse-rejected, validation-rejected, or state-commit-failed>
outcome_body_sha256=<HEX64>
```

The body hash covers lines 1-25 including LF after `reason`:

```text
outcome_body_sha256 = SHA-256(lines 1 through 25 including every LF)
```

The full-frame hash covers all 26 lines including final LF:

```text
H = SHA-256(all 26 canonical lines including final LF)
```

The frame begins at raw-medium byte zero, ends within exactly one 2,048-byte
raw medium, and is followed only by zero bytes. Padding is not part of `H`.

Exactly four tuples are internally canonical:

| Public class | Decision/reason | Before/after | Configuration hashes |
|---|---|---|---|
| `accepted` | `accepted/none` | `SRC/DST` | both nonzero and unequal |
| `parse-rejected` | `rejected/parse-rejected` | `SRC/SRC` | byte-equal and nonzero |
| `validation-rejected` | `rejected/validation-rejected` | `SRC/SRC` | byte-equal and nonzero |
| `state-commit-failed` | `rejected/state-commit-failed` | `SRC/indeterminate` | before nonzero; after `Z` |

Every other decision/reason/state/configuration-hash tuple is internally
invalid and cannot be repaired by host evidence.

## 5. Unchanged I2 event and exact configuration-hash boundary

The event remains exactly the I2 v0.4 31-field schema. I3 does not copy,
extend, or reinterpret it. A later implementation must reuse its authenticated
parser, serializer, hash, lifecycle, chain, and supplied-set validators.

The I2 event contains no direct before/after configuration-state hash fields.
Therefore I3 requires no nonexistent field equality. Instead:

1. the two configuration hashes are validated against the exact outcome tuple;
2. for a uniquely selectable canonical frame, `H` commits every frame byte,
   including both configuration hashes; and
3. the matching I2 completion event carries exactly
   `outcome_frame_sha256=H`.

This is a transitive byte commitment, not a claim that I2 has configuration-
hash fields. For `crash`, `missing`, and `duplicate`, no canonical frame is
selected and the I2 event uses `Z`. For disagreement, the event uses `H` only
when exactly one internally canonical frame is uniquely selectable; otherwise
it uses `Z`.

The unchanged I2 event-state mapping is:

| Classification | Before | After | Frame hash |
|---|---|---|---|
| pre-pending `none` | `none` | `none` | `Z` |
| `accepted` | `SRC` | `DST` | `H` |
| `parse-rejected` | `SRC` | `SRC` | `H` |
| `validation-rejected` | `SRC` | `SRC` | `H` |
| `state-commit-failed` | `SRC` | `indeterminate` | `H` |
| `crash` | `SRC` | `indeterminate` | `Z` |
| `missing` | `SRC` | `indeterminate` | `Z` |
| `duplicate` | `SRC` | `indeterminate` | `Z` |
| `disagreement` | `SRC` | `indeterminate` | `H` for one unique canonical frame; otherwise `Z` |

## 6. Typed classification fact set

The fact set is a pure function argument, not a canonical record or authority.

| Fact | Exact typed domain |
|---|---|
| `last_durable_phase` | `reserved`, `admission-frozen`, or `pending` |
| `end_observation` | `not-started`, `normal`, `abnormal`, or `unknown` |
| `outcome_media_observations` | one immutable finite sequence of byte strings; empty means zero observed media |
| `launch_admission_status` | `exact`, `conflict`, or `unavailable` |
| `iso_attachment_status` | `exact`, `conflict`, or `unavailable` |
| `outcome_medium_status` | `exact`, `conflict`, or `unavailable` |
| `detachment_and_raw_read_status` | `exact`, `conflict`, or `unavailable` |
| `route_event_binding_status` | `exact`, `conflict`, or `unavailable` |
| `anti_replay_status` | `exact`, `conflict`, or `unavailable` |
| `host_state_status` | `exact`, `conflict`, or `unavailable` |
| `ledger_witness_snapshot_status` | `exact`, `conflict`, or `unavailable` |

`observed_media_count` is derived only as the sequence length. It is never a
caller-supplied field. When the sequence has one member, that member is the
only candidate medium bytes. Empty, one-member, and multiple-member sequences
are all well typed and classified. A non-sequence container, non-byte member,
unbounded/lazy producer, or value outside a closed enum is `I3_INPUT_ERROR`
before classification.

Optional admission evidence is absent or exact bytes. Noncanonical admission
bytes remain well-typed evidence and participate in disagreement; a non-byte
admission argument is `I3_INPUT_ERROR`.

The status `exact` means only that the caller supplied an exact-match fact. I3
does not prove the real observation or provider. Every well-typed fact set maps
to exactly one result.

## 7. Derived raw-medium facts

For pending routes derive:

| Name | Exact derivation |
|---|---|
| `observed_media_count` | sequence length |
| `medium_exact` | count one and sole member length exactly 2,048 bytes |
| `schema_prefix_count` | literal outcome-schema-prefix occurrences in the sole medium; zero unless count one |
| `complete_at_zero` | byte zero begins one structurally complete 26-LF-line block |
| `complete_candidate_count` | structurally complete outcome candidates beginning at schema prefixes |
| `candidate_end` | byte immediately after LF ending line 26 when one candidate begins at zero |
| `nonzero_tail` | any nonzero byte from `candidate_end` through byte 2047 |
| `canonical_frame` | the unique candidate passes exact grammar, body hash, route, and tuple rules |

A structurally complete block can still be noncanonical. Such a block is not
missing. A candidate beginning after byte zero is not selectable.

## 8. Total ordered classification

For `last_durable_phase=reserved` or `admission-frozen`, result is
`outcome_class=none`, frame hash `Z`, before/after `none/none`, and the exact I2
direct-terminal variant from that phase. No outcome bytes are interpreted.

For `pending`, apply exactly this order:

### 8.1 Crash

If `end_observation=abnormal`, class is `crash`, frame hash `Z`, and state pair
is `SRC/indeterminate`. Apparent frame bytes are ignored.

### 8.2 Missing

Class is `missing`, hash `Z`, state pair `SRC/indeterminate` only when:

- end is `normal`;
- the media sequence has exactly one member of exactly 2,048 bytes;
- no duplicate predicate below is true; and
- the medium is all zero, or has neither a structurally complete 26-line block
  at byte zero nor a complete outcome candidate elsewhere.

### 8.3 Duplicate

Class is `duplicate`, hash `Z`, state pair `SRC/indeterminate` when crash and
missing did not match and any is true:

- the sequence has more than one member;
- the sole medium contains more than one exact schema prefix;
- it contains more than one complete candidate; or
- a complete candidate begins at zero and a nonzero tail follows line 26.

No frame is selected.

### 8.4 Disagreement with `H`

Class is `disagreement`, hash `H`, state pair `SRC/indeterminate` when exactly
one internally canonical frame begins at byte zero with zero tail, but any
external condition is not exact, including:

- end is `unknown` or `not-started` rather than `normal`;
- admission is absent, noncanonical, or does not hash/bind exactly;
- any identity, route, object, capability, medium, event, state, or admission
  binding differs; or
- any of the eight supplied statuses is `conflict` or `unavailable`.

The canonical frame remains uniquely identifiable evidence, so uncertain or
conflicting host evidence cannot replace `H` with `Z`.

### 8.5 Disagreement with `Z`

Class is `disagreement`, hash `Z`, state pair `SRC/indeterminate` when no
uniquely selectable internally canonical frame exists after the earlier crash,
missing, and duplicate rows failed. This includes:

- an empty media sequence;
- one medium with length other than 2,048;
- unknown or not-started end without one unique canonical frame;
- a complete block at byte zero with noncanonical syntax, bad body hash, or
  illegal tuple;
- one complete candidate only at a nonzero offset; or
- any malformed, incomplete, oversized, or non-uniquely-selectable bytes not
  already classified missing or duplicate.

### 8.6 Explicit frame result

If no prior row matches, end is `normal`, exactly one canonical frame begins at
zero with zero tail, admission and every binding/status are exact, and the
frame tuple selects exactly one:

- `parse-rejected`, `H`, `SRC/SRC`;
- `validation-rejected`, `H`, `SRC/SRC`;
- `state-commit-failed`, `H`, `SRC/indeterminate`; or
- `accepted`, `H`, `SRC/DST`.

Classification `accepted` does not make `DST` available.

## 9. Completion finalization

The pure finalizer receives a completed classification, an optional canonical
I2 event, and append status in `persisted`, `conflict`, `unavailable`, or
`failed`. It does not reclassify.

| Condition | Disposition | Destination |
|---|---|---|
| pre-pending `none`, exact phase-matching direct terminal, append `persisted` | `terminal-rejected` | unavailable |
| `accepted`, exact matching consumed event with `H`, append `persisted` | `consumed-accepted` | exact `DST` available |
| any non-accepted post-pending class, exact matching terminal event with required `H/Z`, append `persisted` | `terminal-rejected` | unavailable |
| missing/malformed/mismatching event, wrong `H/Z`, or append not `persisted` | `no-completion-claim` | unavailable |

The finalizer compares only fields that exist in the exact I2 event. For
H-bearing classes, matching `outcome_frame_sha256=H` transitively commits the
configuration hashes inside the frame; it does not compare nonexistent event
fields. The finalizer never redraws `C`, invents persistence, replaces an
event, changes class, or retries.

## 10. Future pure interfaces and stable errors

A later separately opened implementation may expose:

```text
parse_import_admission(bytes) -> ImportAdmission
serialize_import_admission(ImportAdmission) -> bytes
hash_import_admission(ImportAdmission or canonical bytes) -> HEX64

parse_import_outcome_frame(bytes) -> ImportOutcome
serialize_import_outcome(ImportOutcome) -> bytes
hash_import_outcome_frame(ImportOutcome or canonical bytes) -> HEX64

classify_import_attempt(optional admission bytes, ClassificationFactSet)
  -> ImportClassification

finalize_import_attempt(ImportClassification, optional I2 event bytes,
  append_status) -> ImportDecision
```

Direct operations use stable byte, field, value, route, tuple, hash, binding,
input, and event errors. A well-typed fact set returns a classification rather
than a leaked parser/runtime exception. No operation changes process-global
parser, encoding, locale, integer, warning, exception, or security settings.

## 11. Nonclaims and closed boundaries

I3 does not implement or validate durable ledger/witness behavior, project-
lifetime uniqueness, atomic append, actual registry authority, keys,
signatures, same-process hostility, process/VM isolation, provider/platform
enforcement, protected material, F0, fixture/oracle, executor, judge, scoring,
E0, S0, the central system, or Project Brain.

No experimental role, signer, store, reader, edge, signature scope, ledger
namespace, or A-D opportunity is added.

## 12. Maximum claim and next gate

This candidate proposes design-level closure of exactly `I3-IR-B01`,
`I3-IR-M01`, and `I3-IR-M02`. It is not independent closure and implements
nothing. After all four v0.2 artifacts and sidecars are authenticated and
frozen, the maximum next gate is a separately opened fresh independent I3 v0.2
design rereview.
