# S0 v0.14 public assembly rehearsal acceptance plan v0.5

- `status`: bounded public design acceptance candidate
- `implementation_status`: not implemented
- `execution_status`: not executed
- `scope`: M-07A, M-06B, and N-01 only, with v0.4 non-regression

## 1. Required future authority split

A later implementation candidate must retain the v0.4 separation:

- candidate child: public I0/I1 flow, exact run-record-v3 and receipt-v2
  construction, and the two fixed IPC requests;
- verifier parent observer: exact ABI, real calls, immutable events, capability,
  and witness issuance; and
- verifier parent live consumer: exact witness/current-file/receipt validation
  and the sole rehearsal PASS decision.

The child receives no FFI, observer, trace, capability, witness, or consumer
authority. Nothing in v0.5 widens those interfaces.

## 2. N-01 last-error tests

The event builder must have two disjoint paths:

1. zero return: `get_last_error()` is the immediately next operation and the
   captured unsigned 32-bit value is stored; and
2. nonzero return: `get_last_error()` is not called and literal integer `0` is
   stored as the not-sampled sentinel.

Future source and runtime tests must reject:

- reading last error after a successful call;
- preserving a value other than integer zero on the success path;
- delaying the failure read behind formatting, logging, cleanup, another FFI
  call, or any other action;
- using a signed, string, null, omitted, inherited, or candidate-supplied event
  value; and
- treating either event field as independent success authority.

The exact nonzero-return predicate and all other v0.4 ABI mutations remain
unchanged.

## 3. Exact run-record-v3 reconstruction

Before candidate execution, independently canonicalize the interface map's
`run_record_v3.exact_object`. Require exactly:

- 38 unique fields;
- strict UTF-8, no BOM, sorted keys, compact separators, `ensure_ascii=true`,
  and one final LF;
- 2,224 bytes; and
- SHA-256
  `73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6`.

Mutate every one of these fields independently and require rejection:

- `schema_id`;
- `design_revision`;
- `claim_kind`;
- `result`;
- `offline_status`; and
- `rehearsal_pass_authority`.

Also reject the predecessor 36-field object, its 2,046-byte encoding, its
SHA-256
`bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`,
and any record or documentation branch that treats
`COMPLETE` or retained bytes as rehearsal PASS.

## 4. Receipt-v2 freeze and provenance

The future implementation gate must receive the three pins externally before
candidate import:

- assembly implementation manifest SHA-256;
- exact v0.5 `design-package-files.sha256` file SHA-256; and
- fresh approving v0.5 independent-rereview Markdown SHA-256.

Each is exactly 64 lowercase hexadecimal characters and is authenticated by
the verifier, not selected by candidate code. With those values, independently
construct the 21-field receipt and require exactly 1,173 canonical bytes.
Freeze the complete bytes and their SHA-256 before any execution.

Reject before reservation on any missing, placeholder, uppercase, malformed,
self-selected, predecessor-package, predecessor-review, or unauthenticated
pin. The old v0.3 consumer/profile IDs, old receipt schema, old record hash,
and every single-field mutation must also reject.

Treat the record's retained `design_base_commit` only as a historical
public-flow lineage anchor. A verifier must reject any implementation that
uses it instead of the exact receipt-v2 design-package and fresh-review pins.

The future implementation report must publish the three input pins, exact
receipt length and hash, and a field-by-field mutation table. It must not
publish a capability or witness representation.

## 5. Live-consumer claim matrix

The sole positive row remains:

- exact v0.4 observer, child, endpoint, root, capability, and ordered two-event
  trace;
- exact private unconsumed witness;
- exact current final files with event identity continuity;
- exact run-record-v3 and frozen receipt-v2;
- exact current external pins and fixed authority IDs;
- pending names absent and root nonquarantined; and
- same-process live-consumer-2 atomic acceptance.

Mandatory negative rows include:

- candidate `COMPLETE` without consumer acceptance;
- exact v3 record and v2 receipt without witness;
- predecessor record or receipt, even with a valid witness;
- correct v2 receipt with any old authority or provenance pin;
- correct files and trace after verifier restart;
- fabricated, foreign, copied, stale, or consumed witness;
- current final file identity changed after valid moves; and
- consumer unavailable, exception, rejection, or skipped call.

Each negative row is `not-success`; the overall run is `AR-RECORD/1` unless an
earlier inherited failure or the denied-boundary override applies.

## 6. Retained-file and report claims

Static text and source inspection must require:

- controller `COMPLETE` means only child completion;
- `candidate-controller-complete-awaiting-live-consumer` is not PASS;
- `offline-not-success-diagnostic-only` applies after process exit;
- only the same-process live consumer can issue the in-memory PASS decision;
- serialized files, event traces, and reports cannot recreate witness
  authority; and
- no power-loss, kernel-crash, directory-durability, hostile-process,
  cross-process-attestation, S0, or E0 claim exists.

Reject any old `public-assembly-rehearsal-pass-not-s0` value or API that
derives PASS from files, hashes, receipt fields, `COMPLETE`, or process exit.

## 7. Inherited hostile non-regression

Fresh review must recheck without redesigning:

- the literal ABI and all v0.4 source mutations;
- exact copied files without a witness;
- post-witness byte-for-byte file replacement;
- capability/witness fabrication, replay, and cross-run substitution;
- zero, one, reordered, duplicate, failed, or mismatched move events;
- M-04 failure routing and exact call counts;
- fixed 90-row bundle, B2/P01 case, request, grant, stub, five counters,
  deterministic repeat, and I2/I3 no-import dispositions;
- four output names and quarantine behavior; and
- every F0, provider/model, executor/judge, S0/E0, central-system, and Project
  Brain boundary.

No new implementation subsystem, durable witness, cross-process authority,
cryptographic signer, or platform claim is required by this revision.

## 8. Author-side design checks

Before transfer to a fresh reviewer, the author must:

1. reproduce the predecessor 36-field/2,046-byte/hash tuple;
2. reproduce the successor 38-field/2,224-byte/hash tuple independently;
3. confirm the receipt has exactly 21 fields and a fixed 1,173-byte length for
   every admissible three-digest tuple;
4. verify every v0.5 Markdown/sidecar and JSON/sidecar pair with the canonical
   validator after its SelfTest;
5. authenticate the five-row design-package manifest;
6. confirm no file outside the v0.5 package changed; and
7. confirm no implementation or rehearsal action occurred.

These checks are author evidence only and cannot close a finding.

## 9. Fresh independent verdict vocabulary

The fresh v0.5 rereviewer may return only:

- `PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY` with zero findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, boundary, or independence failure.

No result automatically opens implementation, platform execution, rehearsal,
provider/model use, F0, S0/E0, commit, push, PR, or main integration.
