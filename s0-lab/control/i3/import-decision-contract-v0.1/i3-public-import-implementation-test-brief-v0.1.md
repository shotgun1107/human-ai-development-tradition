# S0 v0.14 I3 public import implementation and test brief v0.1

- `status`: future implementation brief candidate
- `design_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT DESIGN OPEN`
- `design_base_commit`: `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7`
- `claim_kind`: bounded public implementation/test requirements only
- `implementation_status`: closed

## 1. Gate boundary

This brief defines what a later, separately opened I3 implementation candidate
would have to build and test. It authorizes no code, fixture, hidden oracle,
platform operation, import attempt, provider/model call, E0, or S0 now.

The later implementation must consume, without weakening:

1. the exact 21-line admission grammar;
2. the exact 26-line outcome grammar and 2,048-byte medium rule;
3. the total ordered classification table;
4. the separate completion finalizer; and
5. the existing I2 v0.4 public event contract identified by SHA-256
   `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da`.

It must reuse the authenticated I2 v0.4 event parser, serializer, hash,
lifecycle, chain, and supplied-set validators. A duplicate I3 copy of the
31-field event grammar is forbidden unless a later explicit revision replaces
this decision after independent review.

## 2. Minimum public implementation surface

A candidate may expose only pure, model-free operations equivalent to:

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

Equivalent naming is allowed only if one public contract maps every operation
and parameter unambiguously. Hidden default values, permissive modes, operator
overrides, network calls, filesystem discovery, ambient Git state, process-
global configuration changes, and model judgment are forbidden.

## 3. Required data models

| Model | Required property |
|---|---|
| `ImportAdmission` | exactly the 21 named fields; no extension map or unknown-field retention |
| `ImportOutcome` | exactly the 26 named fields; body hash and full-frame hash independently reproducible |
| `ClassificationFactSet` | closed enums and typed media/admission inputs from the classification table; not serialized as new authority |
| `ImportClassification` | selected row/class, `H/Z`, public states, required completion kind, destination unavailable |
| `ImportDecision` | exactly `consumed-accepted`, `terminal-rejected`, or `no-completion-claim`, plus destination availability |

Objects must be immutable after validated construction or otherwise prevent a
caller from mutating fields behind a cached hash. Equality for identifiers and
hashes is exact byte equality. There is no case folding, trimming, Unicode
normalization, or decimal reinterpretation.

## 4. Stable failure surface

Direct parser/serializer/hash operations must distinguish at least these
public error categories without leaking raw runtime exceptions:

| Error ID | Meaning |
|---|---|
| `I3_BYTE_ERROR` | non-bytes where bytes are required, non-ASCII, BOM, CR, NUL, invalid LF/final-LF, trailing whitespace, or raw-size violation |
| `I3_FIELD_ERROR` | missing, extra, duplicate, reordered, unknown, or malformed `name=value` field |
| `I3_VALUE_ERROR` | value outside its closed lexical domain |
| `I3_ROUTE_ERROR` | class does not select the supplied `SRC/DST` mapping |
| `I3_TUPLE_ERROR` | outcome decision/reason/state/configuration combination is not one of four valid tuples |
| `I3_HASH_ERROR` | body, admission, or full-frame hash mismatch where that operation requires validation |
| `I3_BINDING_ERROR` | two otherwise valid records disagree on an exact cross-binding |
| `I3_INPUT_ERROR` | malformed classification fact set or finalizer argument |
| `I3_EVENT_ERROR` | supplied I2 event is noncanonical or mismatches the selected classification/finalization binding |

For a well-typed `ClassificationFactSet`, absent or malformed admission/outcome
evidence follows the classification table and must not escape as one of these
direct-call errors. The implementation may attach a bounded diagnostic code to
the public result, but that code cannot alter the selected class.

The implementation must not change a process-global integer digit limit,
encoding, locale, warning filter, exception hook, parser mode, hash provider,
or security setting.

## 5. Required unit-test groups

All tests use synthetic public values created only after the implementation
and public-fixture gate is separately opened. They must not read or derive from
F0, a hidden oracle, real credentials, personal data, customer data, or prior
project content.

### 5.1 Admission grammar

Test:

- one canonical record for every import class;
- serialize/parse/serialize byte identity;
- exact 21-field count and order;
- recomputed admission hash over all bytes including final LF;
- each field individually missing, duplicated, reordered, renamed, or given an
  out-of-domain value;
- BOM, CRLF, CR, missing final LF, blank line, NUL, non-ASCII, trailing space,
  trailing tab, extra line, and extra byte;
- each wrong class/state combination;
- `R/A/P/C/result_media_id` zero, collision, and `admission_event_id != A`;
  and
- root, unknown, malformed, or wrongly normalized signer identifiers.

### 5.2 Outcome grammar and medium

Test:

- one canonical frame for each of the four valid tuples;
- serialize/parse/serialize byte identity;
- exact 26-field order and final LF;
- independent line-1-through-25 body hash and whole-frame `H`;
- each field missing, duplicated, reordered, renamed, or invalid;
- every decision/reason pairing outside the four valid tuples;
- wrong before/after state, zero/nonzero/equal/unequal configuration hashes at
  every tuple boundary;
- complete frame lengths exactly below, at, and above 2,048 bytes;
- all-zero padding, one nonzero tail byte at each boundary class, a 27th line,
  embedded second prefix, and two complete candidates; and
- wrong admission hash and every individual cross-record binding mismatch.

### 5.3 Ordered classification

Test every row in the complete table and every adjacent precedence overlap,
including:

- abnormal end with valid, invalid, duplicate, and absent-looking bytes always
  selects crash;
- normal one-medium all-zero and partial frames select missing;
- two media, two prefixes, two candidates, and nonzero tail select duplicate;
- zero physical media, wrong length, unknown/not-started pending end,
  noncanonical complete frame, nonzero-offset candidate, bad body hash, and
  illegal tuple select disagreement with `Z`;
- each external binding or status conflict with an internally canonical frame
  selects disagreement with `H`;
- each exact rejection tuple selects only its named rejection;
- exact accepted tuple selects accepted but destination remains unavailable;
- every class produces the exact unchanged I2 before/after state pair; and
- every pre-pending fact set selects `none` and the correct direct-terminal
  requirement.

The suite must demonstrate that missing and duplicate are mutually exclusive,
that a complete malformed frame cannot become missing, and that no explicit
frame result suppresses a prior crash/missing/duplicate/disagreement result.

### 5.4 Finalization

Test:

- each pre-pending direct-terminal variant with persisted append;
- accepted plus the exact consumed event and persisted append;
- every other post-pending class plus its exact terminal event and persisted
  append;
- missing, malformed, wrong-schema, wrong-ID, wrong-class, wrong-`H/Z`, wrong-
  state, wrong-chain, or duplicate completion evidence;
- append `conflict`, `unavailable`, and `failed`; and
- attempts to redraw `C`, substitute another route, append twice, finalize
  after consumed/terminal, or convert `no-completion-claim` into success.

Only exact accepted/consumed/persisted may make `DST` available.

## 6. Exhaustive and mutation checks

The implementation candidate must provide deterministic public checks for:

1. all closed enum Cartesian combinations after excluding malformed API
   objects into `I3_INPUT_ERROR`;
2. all 21 admission field positions and all 26 outcome field positions under
   missing/duplicate/order/name mutation;
3. all four outcome tuples crossed with each state/hash boundary;
4. every pairwise collision among `R/A/P/C/result_media_id`;
5. every admission-to-outcome binding changed one at a time;
6. every classification status changed from `exact` to `conflict` and
   `unavailable` on a canonical frame;
7. every required `H` versus `Z` branch; and
8. every I2 completion variant admitted or rejected against every I3 class.

If full enumeration of byte strings is impossible, byte mutation must be
position-bounded around a canonical seed and supplemented by the exact parser
structural cases above. Coverage counts and the generator domain must be
printed without using F0.

## 7. Non-regression obligations

The candidate fails if it:

- changes any byte or interpretation in the I2 v0.4 contract;
- duplicates the I2 31-field grammar as a competing authority;
- changes the route mapping or the frozen class precedence;
- lets missing suppress duplicate evidence;
- treats a complete malformed frame as missing;
- calculates `H` from padding or omits the final LF;
- accepts an outcome body hash without independent recomputation;
- grants destination authority before exact finalization;
- adds a retry, replacement ID, inferred append, or operator override;
- adds an experimental role, signer, store, reader, edge, signature scope, or
  ledger namespace; or
- reads any F0 or other closed input.

The candidate must bind the exact predecessor contract hash and publish a
machine-readable implementation manifest plus public source manifest in the
same style as I2. Manifest format selection is deferred to the implementation
gate; this brief does not create those files.

## 8. Candidate verification command requirements

A future verifier must be one deterministic public command with an external
expected-manifest SHA-256 argument. It must:

- authenticate all candidate files and normative public source pins before
  tests;
- run its own synthetic-only self-test before relying on generated cases;
- print separate grammar, hash, binding, classification, finalization,
  mutation, import, CLI, and final-stability results;
- rerun integrity checks after tests;
- prove closed boundaries were `BLOCKED_NOT_EXECUTED`; and
- return nonzero on a skipped test, input mismatch, unexpected file, raw
  exception, nondeterminism, or changed input.

The command must never fetch a network source, enumerate denied F0 paths, or
turn a platform/ledger claim into a unit-test result.

## 9. Independent review package

Before implementation can open, a fresh design reviewer should receive only:

- repository instructions and the I3 boundary;
- these four I3 design documents and sidecars;
- exact authenticated v0.3/v0.4 public authority inputs named by the main
  contract;
- the I2 v0.4 public JSON contract and public verification evidence; and
- the canonical text validator.

The reviewer must independently reconstruct both grammars, the full ordered
classification, `H/Z`, pre-pending/finalization separation, and the unchanged
I2 binding. A zero-finding design review may permit only a separate CONTROL
integration decision; it does not open implementation automatically.

## 10. Bounded review loop

Review findings are limited to concrete contradictions, non-total or
non-deterministic rows, ambiguous bytes/bindings, a weakened I2 boundary, an
authority escalation, or an untestable requirement inside I3 scope.

VM hardening, Git publication mechanics, credential security, provider/model
behavior, project-lifetime ledger durability, same-process hostility, F0,
hidden-oracle design, E0, S0, central-system integration, and Project Brain
are not I3 design blockers. They may not be introduced merely because a more
defensive system is imaginable.

## 11. Maximum claim

This brief defines a future public implementation and test target. No code,
fixture, test, platform, import transition, provider/model call, E0, or S0 was
created or run under the present gate.
