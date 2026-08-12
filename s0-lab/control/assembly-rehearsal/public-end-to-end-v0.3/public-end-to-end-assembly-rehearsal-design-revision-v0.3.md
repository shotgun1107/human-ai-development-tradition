# S0 v0.14 public end-to-end assembly rehearsal design revision v0.3

- `status`: bounded public design successor candidate; independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`
- `predecessor_design_commit`: `18a9562a9da48ce5743fc183c8c68c15d00cf249`
- `predecessor_review_commit`: `179dd6f76f2709881900a42dc32cbde8c33c33b0`
- `predecessor_review_sha256`: `c7b31be05274bb87442550c8a5790e4737d5da7d937d3d7e2f22f6d743bde6fd`
- `active_baseline`: `central-system-v2.1-s0-preparation`
- `implementation_status`: not implemented
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Replacement boundary

This document, the v0.3 interface map, and the v0.3 acceptance plan replace
the v0.2 logical design package for future implementation. The authenticated
v0.2 package remains predecessor evidence.

The following v0.2 rules are retained byte-for-meaning unless this successor
explicitly replaces them:

- the fixed public `BLK-PRACTICE0002 / P01` case;
- the complete public-bundle manifest plus 90-row I0 boundary;
- the 7,917-byte request and 135-byte one-row request manifest;
- the exact I1 manifest grant and candidate-owned one-frame stub;
- I2/I3 contract authentication with no-import dispositions;
- the ten success states through `TEMP_RECORD_VERIFIED`;
- the 36-field, 2,046-byte run record and SHA-256
  `bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`;
- two fresh deterministic executions; and
- every denied boundary and nonclaim.

This successor changes only failure routing, Windows publication semantics,
evidence consumption, and implementation/design/close provenance. It does not
modify I0, I1, I2, I3, their manifests, public contracts, or public-practice
data.

## 2. Fixed target and nonclaims

The only positive flow remains:

`I0 public authentication/transform -> I1 authenticated one-shot stub -> I0 answer validation -> public run record -> publication receipt`.

I2 and I3 remain exact contract preflights. No signer-media route, event,
admission, outcome, classification, completion, destination authority, ledger,
witness, or protected material is created.

This gate writes public design text only. It does not authorize a controller,
request artifact, stub, verifier, rehearsal execution, provider/model call,
F0 content access, executor, judge, scoring, S0, E0, central system, or Project
Brain work.

## 3. Exact output names and initial reservation

Each run receives one newly created, controller-owned, empty output directory
on the same local NTFS volume as all four output objects:

1. `run-record.pending`
2. `run-record.json`
3. `publication-receipt.pending`
4. `publication-receipt.json`

Before `OUTPUT_RESERVED`, the controller performs one ordered reservation
operation:

1. reject a symlink, junction, reparse point, alternate data stream, or
   nonempty output directory;
2. check that all four exact names are absent;
3. exclusively create `run-record.pending`; and
4. keep its already opened handle as the reservation authority.

Any failure in these four steps is `AR-RESERVE` with observed transport calls
equal to zero. No later absence check is allowed to relabel an initial
collision.

After `OUTPUT_RESERVED`, a destination created by another actor is a race.
Any such collision is `AR-RECORD` with the then-observed call count. The
preexisting or racing destination is never replaced, truncated, removed, or
treated as evidence from this run.

## 4. Fixed stub-integrity operation

I1's generic first-final behavior remains unchanged. The candidate-owned stub
remains the only transport and owns an eager immutable frame tuple.

Immediately after I1 returns and before `INVOKED_ONCE`, the controller performs
one `STUB_INTEGRITY` operation. It requires exactly:

- `transport_calls=1`;
- `script_frame_count=1`;
- `yielded_frame_count=1`;
- `close_count=1`; and
- `unconsumed_frame_count_on_close=0`.

A missing or non-callable close, a close exception, a second close, or any
counter mismatch is `AR-INVOKE` with observed transport calls equal to one.
Only successful `STUB_INTEGRITY` permits `RUNNER_ENTERED -> INVOKED_ONCE`.

## 5. Determinism and record-check order

After answer validation, the controller constructs an in-memory record from
the exact 36-field schema. It then performs these operations in fixed order:

1. `DETERMINISM_AUDIT`: reject an unknown/missing field, nondeterministic
   source, noncanonical value, `retry_count != 0`, or a value different from
   the interface map as `AR-DETERMINISM`;
2. `CANONICAL_SERIALIZE`: serialize the already accepted object by the frozen
   ASCII JSON rule;
3. `RECORD_EXPECTATION`: require exact length 2,046, exact bytes, and exact
   frozen hash; a mismatch here is `AR-RECORD` because the semantic audit has
   already passed; and
4. write, flush, close, reopen, and byte/hash verify `run-record.pending`;
   failure is `AR-RECORD`.

This order prevents one mutation from being classified as both
`AR-DETERMINISM` and `AR-RECORD`.

## 6. Supported Windows publication primitive

The first implementation candidate is supported only on Windows 10 or 11 on
one local NTFS volume. Network, removable, ReFS, FAT, exFAT, overlay, virtual,
cross-volume, and unknown filesystems are unsupported and fail `AR-AUTH`
before output reservation.

The only publication primitive is direct Win32 `MoveFileExW` with:

- source and destination resolved in the same already authenticated output
  directory and verified to have the same volume serial number;
- flags exactly `0`;
- no `MOVEFILE_REPLACE_EXISTING`;
- no `MOVEFILE_COPY_ALLOWED`;
- no copy/delete, delete/rename, temporary fallback, retry, or overwrite path;
- success only when the API returns nonzero; and
- failure preserving the captured Win32 error code as diagnostic evidence.

The claimed failure model is process interruption and ordinary API failure
only. Power loss, storage-controller loss, kernel failure, and post-return
directory-metadata durability are explicitly outside the rehearsal claim.
The words `durable` and `crash-safe` are not used for this publication result.

Within the declared model, a successful same-volume no-replace rename makes
the destination visible as one namespace operation. A failed call grants no
success. The future implementation review must verify the actual Windows/NTFS
preflight, imported function signature, exact flags, source/destination volume
identity, collision behavior, and absence of fallbacks.

## 7. Two-object success evidence

The 2,046-byte run record alone is never success evidence. Successful evidence
is the ordered pair:

- `run-record.json`; and
- `publication-receipt.json`.

The controller first uses the fixed primitive to move the verified
`run-record.pending` to `run-record.json`. This is an intermediate publication,
not the success commit point.

It then constructs the receipt defined in the interface map. The receipt binds:

- the run-record path and frozen hash;
- the externally pinned assembly implementation-manifest SHA-256;
- the authenticated v0.3 `design-package-files.sha256` manifest SHA-256;
- the fresh independent-review artifact SHA-256 that approved that exact
  design package;
- all five stub counters, including `stub_close_count=1`;
- the exact Windows primitive identifier and flags;
- the record-publication result; and
- the exact evidence-consumer rule identifier.

The future implementation gate must freeze those three provenance hashes,
canonical receipt bytes, length, and SHA-256 before any rehearsal execution.
Unknown placeholder, zero, self-asserted, missing, or non-externally-pinned
values fail preflight.

The v0.3 design-package manifest is part of this candidate and lists the five
logical v0.3 artifacts, excluding their sidecars and excluding the manifest
itself. Its own SHA-256 is supplied externally by CONTROL to both the design
review and every future implementation review; it is never learned from the
candidate at runtime.

The controller exclusively creates `publication-receipt.pending`, writes,
flushes, closes, reopens, and verifies the frozen receipt, then moves it with
the same fixed primitive to `publication-receipt.json`. Successful receipt
publication is the sole transition to `COMPLETE` and the sole success commit
point. No fallible success check follows it.

## 8. Consumer and residue rule

The only authorized consumer is `S0-PUBLIC-ASSEMBLY-EVIDENCE-CONSUMER-1`.
It receives the authenticated output-root identity, not arbitrary bytes. It
fails closed unless all of the following are true:

1. both exact final pathnames exist as regular non-reparse files in that root;
2. both pending pathnames are absent;
3. neither final has an alternate data stream or link alias accepted by the
   consumer;
4. run-record bytes/hash equal the frozen record;
5. receipt bytes/hash equal the implementation-frozen receipt;
6. every receipt binding equals the externally supplied implementation,
   design-package, review, primitive, counter, path, and record pins; and
7. the pair has not already been consumed under that output-root identity.

Raw bytes, a renamed or copied pending object, a final record without the
receipt, a receipt without the record, or either object at another pathname is
`not-success`.

If cleanup after a failed pre-commit operation cannot remove a pending or
intermediate final object, the output root becomes `QUARANTINED-FAILED`. The
controller records only an out-of-band test diagnostic; it does not publish a
success-shaped failure record. The consumer always rejects a quarantined root.
Cleanup never changes the already selected primary failure class.

## 9. Exact failure routing

Denied access is the only override. Otherwise the first failed ordered
operation selects exactly one primary class:

| Ordered failure | Calls | Primary class |
|---|---:|---|
| denied capability/path or fabricated I2/I3 operation | observed | `AR-BOUNDARY` |
| platform, component, bundle, contract, request, grant, or provenance authentication | 0 | `AR-AUTH` |
| I0 transformed bytes differ | 0 | `AR-TRANSFORM` |
| initial four-name/output-root reservation fails | 0 | `AR-RESERVE` |
| I1 or `STUB_INTEGRITY` fails | 0 before stub entry; otherwise 1 | `AR-INVOKE` |
| successful I1 return but response bytes/hash differ | 1 | `AR-RESPONSE` |
| I0 answer errors are nonempty | 1 | `AR-ANSWER` |
| semantic determinism audit fails | 1 | `AR-DETERMINISM` |
| serialization, pending I/O, either rename, receipt construction/verification, race collision, or consumer pre-commit validation fails | 1 | `AR-RECORD` |

An initial final collision is `AR-RESERVE/0`. A final destination that appears
after reservation is `AR-RECORD/1`. The latter may leave the other actor's
destination present; “no final file” is not claimed. Instead, no valid two-file
success evidence may result.

## 10. Repeat and acceptance boundary

Two executions use fresh empty output roots and independently constructed
stubs. Each must produce the exact frozen record/receipt pair. The second run
is not a retry. Equality is required against the externally frozen bytes and
hashes, not merely between runs.

The verifier may report success only through the exact consumer. Direct file
existence, record JSON contents, controller return value, or pending bytes are
insufficient.

## 11. Finding closures proposed

- `M-04`: closed by exact initial-versus-race collision routing,
  `STUB_INTEGRITY`, and determinism-before-record ordering.
- `M-05`: closed by one Windows 10/11 local-NTFS `MoveFileExW(flags=0)`
  profile and an explicit process-failure-only claim.
- `M-06`: closed by the mandatory two-object consumer and quarantined residue
  rule.
- `M-07`: closed by the receipt's implementation manifest, design-package,
  independent-review, five-counter, primitive, and run-record bindings.

These are author proposals, not independent closure.

## 12. Maximum claim and next gate

Maximum claim: v0.3 proposes bounded public design repairs for M-04 through
M-07. No implementation, publication primitive, receipt, consumer, rehearsal,
platform behavior, model call, F0 boundary, S0, or E0 result has been tested.

After this package is authenticated and committed, the exact next candidate
gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.3 INDEPENDENT REVIEW OPEN`
