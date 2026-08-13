# S0 v0.14 public assembly rehearsal acceptance plan v0.4

- `status`: bounded public design acceptance candidate
- `implementation_status`: not implemented
- `execution_status`: not executed
- `scope`: M-05A and M-06A only, with v0.3 non-regression

## 1. Future implementation split

A later implementation candidate must keep these authorities separate:

- candidate controller child process: public I0/I1 flow, deterministic record
  and receipt construction, and exactly two fixed IPC requests only;
- verifier parent-owned observer: exact ABI binding, two real publication calls,
  immutable event trace, run capability, and witness issuance; and
- verifier-owned live consumer: same-process witness and current-file
  validation plus one-use success decision.

The observer and consumer must be authenticated independently from the
candidate controller. Candidate code runs in a verifier-created child process
and may not import the FFI, instantiate or inspect the observer/witness, or
call the consumer.

## 2. Exact ABI source audit

Before any candidate import or filesystem mutation, source inspection and a
synthetic no-call binding test must require literally:

- supported process: 64-bit CPython 3.12.x on 64-bit Windows 10/11;
- loader: `ctypes.WinDLL("kernel32", use_last_error=True)`;
- export: `MoveFileExW`;
- `argtypes=[ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]`;
- `restype=ctypes.c_int32`;
- Microsoft x64 Windows `WINAPI` convention;
- two absolute `\\?\` UTF-16 NUL-terminated paths with embedded NUL rejected;
- `ctypes.set_last_error(0)` immediately before the call;
- numeric flags exactly zero; and
- after zero return, `ctypes.get_last_error()` as the immediately following
  operation.

Mutate each element independently. Every mutation must fail `AR-AUTH/0`
before output reservation. This includes `CDLL`, `c_char_p`, `c_void_p`,
signed flags, 64-bit flags, unsigned return, Python `bool`, default restype,
another DLL/export, relative/nonextended path, nonzero flags, delayed error
capture, fallback, and retry.

## 3. Observer construction tests

The verifier parent creates one observer, one run capability, one child
process, and one anonymous-pipe pair for one fresh root.
Require:

- capability identity, not value equality;
- capability bound to exact child process handle and parent pipe endpoint;
- capability and witness never cross the pipe or enter child-visible state;
- child messages exactly `PUBLISH_RECORD\n` then `PUBLISH_RECEIPT\n`;
- parent reply exactly `OK\n` only after each successful observed event;
- partial, extra, duplicate, reordered, non-ASCII, or post-terminal bytes
  reject;
- no public capability or witness constructor;
- copy, deepcopy, pickle, JSON, repr-derived reconstruction, and foreign
  observer objects cannot create accepted authority;
- candidate receives only the child pipe endpoint;
- candidate direct FFI/import/trace/consumer/witness access is rejected by
  static and runtime sentinels;
- either callback accepts one exact capability and one exact ordinal only;
- replay, reorder, duplicate, wrong observer, wrong root, and spent capability
  terminate without witness.

These are future implementation tests. No such object is created in this
design gate.

## 4. Real move-event tests

On the supported real Windows/NTFS profile, for each path pair the observer
must capture and compare:

- exact canonical source/destination and authenticated root identity;
- destination absence immediately before call;
- source pre-call volume serial, file-index high/low, length, and SHA-256;
- ABI profile, flags, signed return, and immediate last-error result;
- source absence after success; and
- destination post-call volume serial, file-index high/low, length, and
  SHA-256.

Positive success requires pre/post file identity, length, and hash equality.
Tests must cover source disappearance/replacement, destination race,
cross-volume, reparse, alternate stream, copied destination, changed bytes,
wrong path, wrong root, wrong ordinal, API failure, and interruption before
and after each call.

No mock result may satisfy the real-profile acceptance row.

## 5. Live witness and consumer matrix

The sole positive row is:

- same observer and capability;
- exact ordered record and receipt events;
- exact private witness by identity;
- exact current record/receipt final files matching event identities and
  hashes;
- pending names absent;
- v0.3 provenance/receipt bindings valid;
- root nonquarantined; and
- witness not previously consumed.

Mandatory negative rows:

- no witness;
- fabricated, copied, serialized, foreign-observer, foreign-root, stale, or
  consumed witness;
- zero, one, reordered, duplicated, mismatched, or failed observer events;
- exact record alone or receipt alone;
- either pending name present;
- final object identity differs from its successful observer event;
- receipt/provenance/counter/path/hash mismatch;
- quarantined root; and
- consumer call after verifier process restart.

Every negative row returns `not-success`; observer/consumer failures use
`AR-RECORD/1` for the overall run.

## 6. Exact copied-pair hostile test

This test is noncompensatory:

1. build the exact pending record and receipt;
2. copy their bytes to the exact two final names;
3. remove both pending names;
4. confirm final bytes and v0.3 receipt fields are exact; and
5. call the live consumer without the verifier-issued witness.

Required result: `not-success`.

Repeat with a fabricated witness-like object, a witness from another successful
run, and a consumed witness. All reject. Then perform two real observed moves,
replace either final by an exact byte-for-byte copy, and require rejection by
file-identity mismatch.

## 7. Claim-boundary tests

The candidate report and retained files must say:

- controller `COMPLETE` is not rehearsal PASS;
- only same-process verifier live-consumer acceptance is PASS;
- final files after process exit are diagnostic and `offline-not-success`;
- no serialized witness or report recreates witness authority; and
- no power-loss, kernel-crash, directory-durability, security-boundary, or
  cross-process attestation claim exists.

Any offline/pass-from-files API, documentation statement, or code branch is a
major regression.

## 8. Inherited non-regression

Fresh review must retain all v0.3 closure and v0.2 public flow, including:

- M-04 unique routing and call counts;
- M-07 external implementation/design/review and five-counter provenance;
- four output names and quarantine semantics;
- fixed public bundle/case/request/grant/stub/record;
- I2/I3 no-import dispositions;
- two fresh deterministic executions; and
- every F0, provider/model, executor/judge, S0/E0, central-system, and Project
  Brain boundary.

## 9. Required future evidence

An implementation review must publish public evidence for exact source hashes,
ABI declaration and mutations, real platform/volume checks, two event traces
with identifiers reduced to non-sensitive test values, witness negative
matrix, copied-pair rejection, file-identity continuity, routing, deterministic
runs, closed-boundary nonexecution, and final Git stability.

It must not serialize an authority-bearing capability or witness.

## 10. Verdict vocabulary

The fresh v0.4 design rereview may return only:

- `PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY` with zero findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, boundary, or independence failure.

No test described here has been implemented or executed under the current
gate.
