# S0 v0.14 I3 public import implementation and test brief v0.2

- `status`: future implementation brief revision candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 BOUNDED DESIGN REVISION OPEN`
- `responds_to_review_sha256`: `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c`
- `claim_kind`: bounded public implementation/test requirements only
- `implementation_status`: closed

## 1. Present gate and future target

This brief does not open implementation. It defines what a later separately
opened candidate must implement and test after a zero-finding v0.2 design
rereview and separate CONTROL decision.

The future candidate must consume without weakening:

1. the exact 21-line admission grammar;
2. the exact 26-line outcome grammar, body hash, full `H`, and 2,048-byte
   zero-tail rule;
3. the v0.2 typed fact set and nine ordered pending rows;
4. the separate completion finalizer; and
5. the unchanged I2 v0.4 contract identified by SHA-256
   `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

It must reuse authenticated I2 event parsing, serialization, hashing,
lifecycle, chains, and supplied-set validation. It must not duplicate or
extend the 31-field event grammar.

## 2. Minimum pure interface

Equivalent public operations may be named differently only when an exact
machine-readable mapping is supplied:

```text
parse_import_admission(bytes) -> ImportAdmission
serialize_import_admission(ImportAdmission) -> bytes
hash_import_admission(ImportAdmission or canonical bytes) -> HEX64

parse_import_outcome_frame(bytes) -> ImportOutcome
serialize_import_outcome(ImportOutcome) -> bytes
hash_import_outcome_frame(ImportOutcome or canonical bytes) -> HEX64

classify_import_attempt(
  optional admission bytes,
  ClassificationFactSet
) -> ImportClassification

finalize_import_attempt(
  ImportClassification,
  optional canonical I2 event bytes,
  append_status
) -> ImportDecision
```

There is no separate media-count argument. `ClassificationFactSet` contains
one immutable finite `outcome_media_observations` sequence of byte strings;
the implementation derives the count from its length exactly once.

No interface may use hidden defaults, permissive modes, filesystem discovery,
network calls, ambient Git state, model judgment, or operator override.

## 3. Required public models

| Model | Requirement |
|---|---|
| `ImportAdmission` | exactly 21 named fields; no extension map |
| `ImportOutcome` | exactly 26 named fields; body hash and `H` reproducible |
| `ClassificationFactSet` | closed phase/end/status enums, optional admission bytes, one finite sequence of media byte strings |
| `ImportClassification` | exact selected row/class, `H/Z`, I2 state pair, required completion, destination unavailable |
| `ImportDecision` | exactly consumed-accepted, terminal-rejected, or no-completion-claim plus destination availability |

Validated objects must be immutable or otherwise prevent mutation behind a
cached hash. Exact byte equality controls identifiers and hashes.

## 4. Stable error surface

Direct operations distinguish at least:

| Error | Meaning |
|---|---|
| `I3_BYTE_ERROR` | wrong byte type, non-ASCII/BOM/CR/NUL/LF/trailing-whitespace/raw-size defect |
| `I3_FIELD_ERROR` | missing/extra/duplicate/reordered/unknown/malformed field |
| `I3_VALUE_ERROR` | value outside closed lexical domain |
| `I3_ROUTE_ERROR` | class and `SRC/DST` disagree |
| `I3_TUPLE_ERROR` | outcome tuple is not one of four valid tuples |
| `I3_HASH_ERROR` | admission/body/full-frame hash mismatch |
| `I3_BINDING_ERROR` | canonical records disagree on a required binding |
| `I3_INPUT_ERROR` | malformed fact-set/finalizer API object |
| `I3_EVENT_ERROR` | noncanonical or classification-incompatible I2 event |

An empty, one-member, or multiple-member byte-string media sequence is not an
input error. It reaches classification. A non-sequence, lazy/unbounded
producer, non-byte member, invalid enum, or non-byte admission argument is
`I3_INPUT_ERROR`. Noncanonical admission/media bytes are classified evidence,
not type errors.

No operation changes process-global parser, encoding, integer limit, locale,
warning filter, exception hook, hash provider, or security setting.

## 5. Admission conformance tests

After a later public-fixture gate opens, test only synthetic public data:

- canonical records for all three routes;
- serialize/parse/serialize byte identity;
- exact 21-field count/order and full admission hash including final LF;
- every field individually missing, duplicated, reordered, renamed, and out
  of domain;
- BOM, CRLF, CR, NUL, non-ASCII, blank line, missing final LF, trailing
  space/tab, extra line/byte;
- every wrong class/state combination;
- zero and every pairwise collision among `R/A/P/C/result_media_id`;
- `admission_event_id != A`; and
- root, unknown, malformed, or normalized signer IDs.

## 6. Outcome and medium conformance tests

Test:

- one canonical frame for each of four valid tuples;
- exact 26-field order and serialize/parse/serialize identity;
- independently recomputed body hash over lines 1-25 and `H` over all 26,
  always including the required LF;
- every field mutation and every invalid decision/reason/state/hash tuple;
- frame sizes around 2,048 bytes;
- all-zero padding, nonzero tail at boundary positions, 27th line, second
  prefix, two complete candidates, and candidate only at nonzero offset;
- wrong admission hash and each cross-record binding changed alone; and
- confirmation that configuration hashes are checked against the frame tuple
  and committed through `H`, never compared to nonexistent I2 fields.

## 7. Finding-closure tests

### 7.1 `I3-IR-B01`

For each of the four canonical frame tuples, hold frame/admission/bindings
constant and cross end observation with `normal`, `unknown`, `not-started`,
and `abnormal`:

- normal plus all external evidence exact selects the explicit frame class and
  `H`;
- unknown/not-started selects disagreement and the same recomputed `H`;
- abnormal selects crash and `Z` by explicit first precedence; and
- replacing the frame with a bad-body-hash or illegal-tuple block under
  unknown/not-started selects disagreement and `Z`.

The I2 terminal event for disagreement must accept exactly the tabled `H/Z`
and reject the other value.

### 7.2 `I3-IR-M01`

Test the single media-sequence representation:

- empty sequence derives zero and selects disagreement/`Z`;
- one all-zero 2,048-byte member under normal end selects missing/`Z`;
- one canonical member reaches its exact later row;
- two or more byte-string members select duplicate/`Z`;
- tuple/list implementation choices, if more than one is accepted, normalize
  to one immutable sequence without changing member bytes/order;
- non-byte member, lazy/unbounded iterable, scalar bytes used as the outer
  sequence, and any attempted separate count parameter reject as
  `I3_INPUT_ERROR`.

There must be no executable path in which count and bytes disagree because
count is not caller supplied.

### 7.3 `I3-IR-M02`

Test:

- configuration hashes against every valid/invalid outcome tuple;
- changing either configuration hash changes recomputed body hash and `H`;
- an H-bearing I2 completion accepts only exact
  `outcome_frame_sha256=H`;
- no I2 parser, serializer, event object, or test invents a configuration-hash
  field; and
- Z-bearing classes make no configuration-hash claim.

## 8. Ordered classification tests

Exercise every row and every adjacent overlap:

- abnormal end with absent, valid, invalid, or duplicate-looking bytes always
  selects crash/`Z`;
- normal one-medium all-zero or partial frame selects missing/`Z`;
- multiple media, multiple prefixes/candidates, or nonzero tail selects
  duplicate/`Z`;
- one canonical frame with any external conflict/unavailable status or
  unknown/not-started end selects disagreement/`H`;
- empty media, wrong length, complete malformed frame, sole nonzero-offset
  candidate, bad body hash, illegal tuple, or no canonical frame under
  uncertain end selects disagreement/`Z`;
- each exact rejection selects only its named class/`H`;
- exact accepted selects accepted/`H` while destination remains unavailable;
- each class emits the unchanged I2 before/after pair; and
- pre-pending phases select none/`Z` and the correct direct terminal.

The suite must demonstrate row exclusivity and totality over the declared
typed domain. A complete malformed frame cannot become missing; a unique
canonical frame cannot become `Z` merely because external evidence is
uncertain.

## 9. Finalization tests

Test:

- both exact pre-pending direct terminals with persisted append;
- accepted plus exact consumed event and persisted append;
- every non-accepted pending class plus exact terminal event and persisted
  append;
- every wrong class, ID, route, `H/Z`, state, chain, missing/duplicate event;
- append conflict, unavailable, failed, and unknown/malformed input; and
- redraw, replay, second completion, post-consumed/terminal event, and retry.

Only accepted plus exact consumed event plus persisted append makes `DST`
available. Event comparison uses only actual I2 fields. Configuration hashes
are committed transitively through `H`.

## 10. Exhaustive and mutation obligations

Provide deterministic public checks for:

1. all closed enum Cartesian combinations;
2. all 21 admission and 26 outcome positions under name/order/presence/value
   mutations;
3. all four tuples crossed with state/configuration-hash boundaries;
4. all pairwise `R/A/P/C/result_media_id` collisions;
5. each admission/outcome binding changed separately;
6. each of eight statuses changed from exact to conflict/unavailable on a
   canonical frame;
7. every `H/Z` branch, especially unique canonical frame plus uncertain end;
8. sequence lengths zero, one, two, and a bounded value greater than two; and
9. every I2 completion variant crossed with every I3 class.

Coverage counts and generator domains must be public. No test may use F0,
hidden oracle, real credentials, personal/customer data, or past-project
content.

## 11. Non-regression and verifier requirements

The candidate fails if it changes I2 bytes/meaning, duplicates its event
grammar, changes route mapping/precedence, lets missing hide duplicates,
treats a complete malformed frame as missing, emits `Z` for a uniquely
canonical frame under external uncertainty, hashes padding or omits final LF,
directly compares nonexistent I2 configuration-hash fields, grants authority
before finalization, adds retry/replacement/operator override, changes
experimental topology, or reads a closed input.

A future verifier must authenticate an external expected manifest, self-test
its synthetic generator, report grammar/hash/binding/classification/
finalization/mutation/import/CLI/final-stability results separately, rehash
inputs afterward, and print closed boundaries as `BLOCKED_NOT_EXECUTED`.

Manifest and verifier files are deferred to the implementation gate and are
not created now.

## 12. Independent rereview and bounded scope

A fresh v0.2 design rereviewer must independently reconstruct both grammars,
the media-sequence type, all pending rows, `H/Z`, configuration-hash commitment
through `H`, unchanged I2 states/events, and finalization. It must specifically
retest the three predecessor findings.

Review may block only for a concrete ambiguity, contradiction, non-total row,
wrong byte/hash/binding, authority escalation, I2 regression, or untestable I3
requirement. VM/Git/security/provider/F0/E0/S0 expansion is not an I3 closure
condition.

## 13. Maximum claim

This brief defines a future implementation/test target only. No code, fixture,
test, platform operation, import, provider/model call, E0, or S0 was created or
run under the present gate.
