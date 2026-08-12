# S0 v0.14 I3 public import-decision contract v0.1

- `status`: public design candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT DESIGN OPEN`
- `design_base_commit`: `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7`
- `design_base_tree`: `3b2663fed848728ae5ebdb730f79fe6137d03862`
- `claim_kind`: model-free public contract design only
- `implementation_status`: not opened

## 1. Decision and scope

I3 defines one deterministic public contract for the relationship among:

1. `S0-SIGNER-IMPORT-ADMISSION-2`;
2. `S0-SIGNER-IMPORT-OUTCOME-1`; and
3. the already implemented
   `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` v0.4 record.

The admission and outcome grammars are exact materializations of authenticated
v0.3 public text. The import-event grammar is not copied or revised here. It
remains exactly the machine-readable I2 v0.4 contract with SHA-256
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.
Any event implementation or interpretation that differs from that byte-
identified contract is an I2 regression and fails I3.

I3 separates three noncompensatory layers:

- canonical byte validity;
- cross-record and host-fact structural consistency; and
- deterministic classification plus completion disposition.

Success at one layer cannot repair failure at another. I3 creates no actual
authority. Its host, state, ledger, witness, and append inputs are caller-
supplied public facts for a pure classifier; this design does not prove that a
real platform reported those facts honestly or persisted them durably.

## 2. Authenticated normative sources

| Source | SHA-256 | I3 use |
|---|---|---|
| I3 boundary v0.1 | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` | scope, deliverables, review-loop limit |
| I2 public contract v0.4 | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` | unchanged 31-line event and supplied-set semantics |
| v0.3 design revision | `a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b` | ordered admission block, 26-line outcome, raw-medium and precedence rules |
| v0.3 authority matrix | `5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a` | producer, verifier, ID, media, state, and authority limits |
| v0.3 acceptance addendum | `bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3` | failure classes and hostile evidence |
| v0.4 design revision | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` | complete 31-line event and exact hash/lifecycle interpretation |
| v0.4 authority matrix | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` | event authority and future machine-readable requirement |
| v0.4 acceptance addendum | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` | exact event non-regression and hostile traces |

Each Markdown source was authenticated through its same-basename sidecar and
passed the canonical public-text validator before use. No F0 or nonpublic
source was read.

## 3. Common lexical rules

Let:

- `Z` be exactly 64 ASCII `0` bytes;
- `HEX64` be exactly 64 lowercase ASCII hexadecimal characters;
- `NONZERO_HEX64` be `HEX64` except `Z`;
- `LF` be byte `0A`;
- `R`, `A`, `P`, and `C` be the distinct nonzero reserved, admission-frozen,
  pending, and completion event IDs; and
- `H` be the SHA-256 of one complete internally canonical outcome frame,
  including its final hash line and final LF.

Every admission and outcome record is strict ASCII. Each field is emitted as
one `name=value` line in the declared order and ends in LF, including the last
line. BOM, CR, NUL, blank line, trailing space or tab, missing or duplicate
field, reordered field, unknown field, extra field, non-ASCII byte, or missing
final LF rejects canonical parsing.

The three allowed route classes and state mapping are:

| Import class | `SRC` | `DST` |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

The values `campaign_id`, `ceremony_id`, package hashes and object IDs,
capability, result-media ID, and the four event IDs are compared byte-for-byte.
Case folding, Unicode normalization, trimming, numeric reinterpretation, and
operator-selected aliases are forbidden.

## 4. Exact admission grammar

`S0-SIGNER-IMPORT-ADMISSION-2` is exactly 21 lines:

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
separate numeric count. I3 makes the derived count explicit: all 21 displayed
fields are required, including both `admission_event_id` and `decision` after
`outcome_max_bytes`. No separate version field exists.

The admission hash is:

```text
admission_record_sha256 = SHA-256(all 21 canonical lines including final LF)
```

`R`, `A`, `P`, `C`, and `result_media_id` are pairwise distinct. This design
checks distinctness within the supplied route. Project-lifetime uniqueness
remains outside I3. `admission_event_id` is exactly `A`; it is not a sixth
event identity. The exact signer identifier must be one of the 21 non-root I1
public registry roles bound by I2 v0.4.

## 5. Exact outcome grammar

`S0-SIGNER-IMPORT-OUTCOME-1` is exactly 26 lines in one raw medium:

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

The body hash covers every preceding outcome byte through and including the LF
after `reason`:

```text
outcome_body_sha256 = SHA-256(lines 1 through 25 including each LF)
```

The complete-frame hash is:

```text
H = SHA-256(all 26 canonical lines including final LF)
```

The complete frame must end within a fixed 2,048-byte raw medium. Every medium
byte after the final LF is zero. The medium has no filesystem and is not a
record field. I3 validates supplied bytes only; it does not mount, attach,
detach, persist, or destroy a real medium.

Exactly four decision tuples are internally canonical:

| Decision/reason | Before | After | Configuration hashes |
|---|---|---|---|
| `accepted/none` | `SRC` | `DST` | before and after are nonzero and unequal |
| `rejected/parse-rejected` | `SRC` | `SRC` | before and after are byte-equal and nonzero |
| `rejected/validation-rejected` | `SRC` | `SRC` | before and after are byte-equal and nonzero |
| `rejected/state-commit-failed` | `SRC` | `indeterminate` | before is nonzero; after is `Z` |

Every other decision, reason, state, or configuration-hash tuple is
internally malformed. It cannot be repaired through external host evidence.

## 6. Unchanged import-event contract

The canonical import event remains the exact I2 v0.4 schema
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` with 31 fields and contract hash
`713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

I3 does not emit a second event schema or restate all 31 lines as new
authority. The field-and-binding table names the required event relationships,
but an implementation must call or reuse the authenticated I2 parser,
serializer, hash, lifecycle, chain, and supplied-set validators. Reimplementing
that grammar inside a separate I3 module is a reviewable regression risk.

The I2 rules remain exact, including:

- `request_id=Z` and `route_kind=import`;
- the distinct `R/A/P/C` lifecycle;
- the separate global hash chain and route-local event-ID chain;
- the zero-to-frozen admission/media tuple;
- the accepted, rejected, early-terminal, crash, missing, duplicate, and
  disagreement event variants;
- `H` versus `Z` frame-hash selection; and
- no event after consumed or terminal, ID redraw, replacement completion, or
  retry.

## 7. Pure classification fact set

I3 classification accepts a caller-supplied typed fact set. It is not a fourth
canonical record and has no signature or authority of its own.

| Fact | Exact value domain |
|---|---|
| `last_durable_phase` | `reserved`, `admission-frozen`, or `pending` |
| `end_observation` | `not-started`, `normal`, `abnormal`, or `unknown` |
| `outcome_media_count` | canonical nonnegative integer |
| `outcome_media_bytes` | absent unless count is one; otherwise exact bytes |
| `launch_admission_status` | `exact`, `conflict`, or `unavailable` |
| `iso_attachment_status` | `exact`, `conflict`, or `unavailable` |
| `outcome_medium_status` | `exact`, `conflict`, or `unavailable` |
| `detachment_and_raw_read_status` | `exact`, `conflict`, or `unavailable` |
| `route_event_binding_status` | `exact`, `conflict`, or `unavailable` |
| `anti_replay_status` | `exact`, `conflict`, or `unavailable` |
| `host_state_status` | `exact`, `conflict`, or `unavailable` |
| `ledger_witness_snapshot_status` | `exact`, `conflict`, or `unavailable` |

The status value `exact` means only that the caller supplies an exact-match
fact to the pure function. I3 does not prove the observation, implement its
provider, or convert an unavailable external system into success.

A well-typed fact set always produces one classification result. A malformed
fact-set object is an API input error, not an experimental classification.

## 8. Raw-medium scan and classification predicates

For `last_durable_phase=pending`, the classifier applies these predicates in
the frozen order below.

### 8.1 Crash

`crash` matches exactly when `end_observation=abnormal`. Apparent frame bytes
are ignored and frame hash is `Z`.

### 8.2 Missing

`missing` matches only when all are true:

- end observation is `normal`;
- exactly one outcome medium is supplied;
- its length is exactly 2,048 bytes;
- there is no duplicate evidence; and
- the medium is all zero, or it has neither a structurally complete 26-line
  block beginning at byte zero nor a complete outcome candidate elsewhere.

Requiring exactly one medium and no duplicate evidence makes `missing` and
`duplicate` mutually exclusive while preserving the inherited precedence.
A partial or truncated candidate with fewer than 26 LF-terminated lines is
missing; no target decision is inferred.

### 8.3 Duplicate

`duplicate` matches when crash and missing do not match and any is true:

- more than one outcome medium is supplied;
- the exact outcome-schema prefix occurs more than once in the one medium;
- more than one frame candidate exists; or
- any nonzero byte follows the LF ending one complete 26-line frame.

No frame is selected and frame hash is `Z`. An extra 27th line is a nonzero
tail and therefore duplicate, not an alternate grammar.

### 8.4 Disagreement

`disagreement` matches every remaining non-explicit case, including:

- zero media, a media count/bytes contradiction, or a medium not exactly
  2,048 bytes;
- `end_observation=unknown` or an impossible phase/end combination;
- a structurally complete 26-line block at byte zero with noncanonical syntax,
  a complete candidate at a nonzero offset, a bad body hash, or an illegal
  decision tuple;
- any admission parse failure after pending;
- any cross-record identity, hash, class, state, object, capability, medium,
  or event-ID mismatch;
- any host fact status other than `exact`; or
- any conflict or unavailable anti-replay, state, ledger, or witness fact.

Frame hash is `H` only when exactly one internally canonical frame is uniquely
selectable but an external admission, host, state, event, anti-replay, ledger,
or witness fact is not exact. It is `Z` for malformed, incomplete, oversized,
bad-hash, invalid-tuple, or non-unique bytes.

### 8.5 Explicit frame result

If none of the four earlier predicates matches, exactly one internally
canonical frame exists, every cross-record binding matches, every required
host fact is `exact`, and the frame tuple decides the class:

- `parse-rejected`;
- `validation-rejected`;
- `state-commit-failed`; or
- `accepted`.

All four use `H`. Classification `accepted` is a proposed public class only;
it does not make `DST` available before an exact consumed event is durably
accepted by the external ledger/witness provider.

The classification result uses the unchanged I2 event-state mapping:

- pre-pending `none` uses `none/none`;
- `accepted` uses `SRC/DST`;
- `parse-rejected` and `validation-rejected` use `SRC/SRC`; and
- `state-commit-failed`, `crash`, `missing`, `duplicate`, and `disagreement`
  use `SRC/indeterminate`.

These event fields are bounded public evidence values. `indeterminate` does
not assert a known real state, and no classification grants destination
authority before finalization.

## 9. Pre-pending and completion finalization

A route whose last durable phase is `reserved` or `admission-frozen` has no
post-pending outcome classification:

- `outcome_class=none`;
- `outcome_frame_sha256=Z`;
- required event is the exact I2 direct-terminal variant from that phase; and
- destination is unavailable and retry is forbidden.

After post-pending classification, a separate pure finalizer receives the
classification, one supplied I2 completion event when present, and
`append_status` in `persisted`, `conflict`, `unavailable`, or `failed`.

It returns exactly one completion disposition:

| Condition | Disposition | Destination |
|---|---|---|
| `accepted`, exact matching consumed event, append `persisted` | `consumed-accepted` | available as `DST` |
| non-accepted class, exact matching terminal event, append `persisted` | `terminal-rejected` | unavailable |
| pre-pending `none`, exact matching direct terminal, append `persisted` | `terminal-rejected` | unavailable |
| every event mismatch, missing event, conflict, unavailable, or failed append | `no-completion-claim` | unavailable |

The finalizer never redraws `C`, invents persistence, changes the outcome
class, or retries the route. An apparently accepted frame plus failed append
is `no-completion-claim`, not accepted authority.

## 10. Pure interface contract

A future implementation candidate may expose these model-free operations:

```text
parse_import_admission(bytes) -> ImportAdmission
serialize_import_admission(ImportAdmission) -> bytes
hash_import_admission(ImportAdmission or canonical bytes) -> HEX64

parse_import_outcome_frame(bytes) -> ImportOutcome
serialize_import_outcome(ImportOutcome) -> bytes
hash_import_outcome_frame(ImportOutcome or canonical bytes) -> HEX64

classify_import_attempt(
  optional admission bytes,
  classification fact set
) -> ImportClassification

finalize_import_attempt(
  ImportClassification,
  optional canonical I2 event bytes,
  append_status
) -> ImportDecision
```

Direct parser calls report stable, separately named byte, field, enum, tuple,
hash, and binding errors. For a well-typed classification fact set, malformed
or absent evidence maps through the total classification table rather than
leaking parser or runtime exceptions. The implementation must not change a
process-global parser, encoding, integer, locale, or safety setting.

## 11. Nonclaims and closed boundaries

I3 does not implement or validate durable ledger/witness behavior, project-
lifetime uniqueness, atomic append, actual registry authority, keys,
signatures, hostile same-process security, process/VM isolation, provider or
platform enforcement, protected material, F0, fixture/oracle, executor,
judge, scoring, E0, S0, the central system, or Project Brain.

The outcome medium, TCB service, records, fact set, classification, and event
remain public control objects. They add no experimental role, signer, store,
reader, edge, signature scope, ledger namespace, or A-D opportunity.

## 12. Maximum claim and next gate

The maximum claim is that this candidate specifies two exact canonical public
record grammars, preserves the exact I2 v0.4 event contract, and defines a
total pure classification and finalization boundary for later independent
design review.

No parser, serializer, classifier, validator, live platform, or experiment has
been implemented or run. After this four-document package is frozen, the
maximum next gate is a separately opened fresh independent I3 design review.
