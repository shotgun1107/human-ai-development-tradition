# S0 v0.14 public end-to-end assembly rehearsal design revision v0.5

- `status`: bounded public successor candidate; fresh independent rereview required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`
- `predecessor_design_commit`: `d85cb891a598e54c581c80ebc6c677dd779ceefa`
- `predecessor_review_commit`: `78d95cf9a82c40ac33a6b0b3c54979765c96474f`
- `predecessor_review_sha256`: `b501acacfb04ce62d8c831b303d2c20e1e0cee5f60290a2aa8e287ca7cdd3942`
- `implementation_status`: not implemented
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Replacement boundary

This v0.5 package changes only the v0.4 rules implicated by `M-07A`,
`M-06B`, and `N-01`. The effective design is v0.3 plus the v0.4 replacements
plus these v0.5 replacements.

Unchanged and retained:

- the v0.2 public bundle, case, request, grant, stub, I0/I1 flow, I2/I3
  no-import dispositions, deterministic repeat, and denied boundaries;
- the v0.3 M-04 routing, four output names, five counters, quarantine rule,
  and determinism-before-record order;
- the v0.4 literal `MoveFileExW` ABI, verifier-parent observer, child IPC,
  private capability, exact two-event trace, file-identity continuity,
  private one-use witness, live consumer, and copied-pair rejection; and
- all implementation, platform-execution, provider/model, F0, S0, E0,
  central-system, and Project Brain blockers and nonclaims.

This gate changes public design text only. It does not implement or execute
the controller, FFI, observer, witness, consumer, or rehearsal.

## 2. Positive-call last-error rule

The v0.4 ABI rules remain exact. The following rule replaces only the
positive-event meaning of `last_error_uint32`.

Before either real call, the observer executes `ctypes.set_last_error(0)` as
already required. It then performs exactly one `MoveFileExW` call.

- If the signed 32-bit return is zero, the observer must call
  `ctypes.get_last_error()` as the immediately following operation and record
  that captured unsigned 32-bit value in `last_error_uint32`.
- If the signed 32-bit return is nonzero, the observer must not call
  `ctypes.get_last_error()` for the event. It assigns the literal integer `0`
  to `last_error_uint32` as the frozen not-sampled-on-success sentinel.

`ffi_return_signed_int32` and `terminal_status` distinguish the sentinel from
a captured failure code of zero. Reading, preserving, or reporting another
thread-local last-error value after a successful return is forbidden. This
rule does not change the nonzero success predicate and grants no new authority.

## 3. Run record v3

The inherited 36-field run record is replaced by
`S0-PUBLIC-ASSEMBLY-RUN-RECORD-3`. It retains every operational fact and adds
two explicit claim-boundary fields. Its canonicalization remains strict UTF-8,
no BOM, keys sorted by Unicode code point, compact JSON separators,
`ensure_ascii=true`, and one final LF.

The exact positive controller record has:

- 38 fields;
- 2,224 bytes; and
- SHA-256
  `73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6`.

The changed or added values are exactly:

| Field | Exact value |
|---|---|
| `schema_id` | `S0-PUBLIC-ASSEMBLY-RUN-RECORD-3` |
| `design_revision` | `0.5` |
| `claim_kind` | `candidate-controller-completion-diagnostic-only-not-rehearsal-pass-not-s0` |
| `result` | `candidate-controller-complete-awaiting-live-consumer` |
| `offline_status` | `offline-not-success-diagnostic-only` |
| `rehearsal_pass_authority` | `same-process-verifier-live-consumer-2-acceptance-only` |

All other fields and values are inherited byte-for-byte from the v0.2 exact
positive record. The complete object is frozen in the v0.5 interface map.

The retained `design_base_commit` is only the historical public-flow lineage
anchor from which the request and record were first defined. It is not the
current design authority and cannot substitute for either receipt-v2 external
design/review pin. Current design authorization is expressed only by
`design_package_manifest_sha256` and `design_independent_review_sha256` in the
receipt.

`state=COMPLETE` means only that the candidate child finished its controller
sequence. Neither `state`, `result`, the record bytes, nor their hash is a
rehearsal PASS. After the verifier process exits, the record is diagnostic and
has status `offline-not-success-diagnostic-only`.

The old 2,046-byte record, old schema ID, old hash, or any result containing
`public-assembly-rehearsal-pass-not-s0` is inadmissible under v0.5.

## 4. Publication receipt v2

The v0.3 receipt is replaced by
`S0-PUBLIC-ASSEMBLY-PUBLICATION-RECEIPT-2`. It has exactly 21 fields and the
same strict canonical JSON rules as the run record.

The receipt binds these current authorities:

| Field | Required authority or exact value |
|---|---|
| `evidence_consumer_id` | `S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2` |
| `observer_id` | `S0-PUBLIC-ASSEMBLY-PUBLICATION-OBSERVER-2` |
| `platform_profile_id` | `S0-WIN64-NTFS-MOVEFILEEXW-CTYPES-ABI-2` |
| `record_sha256` | `73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6` |
| `schema_id` | `S0-PUBLIC-ASSEMBLY-PUBLICATION-RECEIPT-2` |
| `publication_outcome` | `controller-files-published-awaiting-live-consumer` |
| `offline_status` | `offline-not-success-diagnostic-only` |
| `rehearsal_pass_authority` | `same-process-verifier-live-consumer-2-acceptance-only` |

The three 64-character lowercase SHA-256 fields have these exact meanings:

1. `assembly_implementation_manifest_sha256` authenticates the future public
   assembly implementation manifest supplied outside candidate code.
2. `design_package_manifest_sha256` authenticates the exact v0.5
   `design-package-files.sha256` bytes.
3. `design_independent_review_sha256` authenticates the fresh v0.5 independent
   rereview Markdown bytes that approve this effective design.

No predecessor v0.3/v0.4 design or review hash may substitute. Candidate code
cannot select any of the three pins. Missing, placeholder, uppercase,
noncanonical, self-selected, old-package, or old-review values fail
`AR-AUTH/0` before output reservation.

Because each external digest has a fixed 64-byte lowercase representation,
every admissible canonical v2 receipt is exactly 1,173 bytes. Its exact bytes
and SHA-256 remain intentionally unavailable until all three external pins
exist. A later implementation candidate must publish and authenticate those
actual bytes, length, and hash before any execution. A template digest is not
an admissible receipt.

## 5. Receipt and live-consumer binding

The candidate constructs the receipt only from the three externally supplied
pins and the fixed v0.5 values. The verifier-owned live consumer must reject
unless the receipt equals the frozen v2 bytes and each authority agrees with
the current observer, ABI profile, record, root, trace, witness, and verifier
configuration.

The following each reject independently:

- either old consumer or old platform-profile ID;
- either predecessor design-package or review pin;
- the old record hash or old receipt schema;
- any mutation of `observer_id`, `offline_status`,
  `rehearsal_pass_authority`, or `publication_outcome`; and
- a receipt with correct bytes presented without the exact private witness.

The receipt remains descriptive evidence. It does not prove either move and
cannot recreate witness authority after process exit.

## 6. PASS authority and retained artifacts

The future candidate controller may reach `COMPLETE`. The verifier may report
rehearsal PASS only in the same process after
`S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2` atomically consumes the exact private
witness and accepts the current files and all receipt bindings.

Before that decision, the overall result is not PASS. If the consumer rejects,
is not called, crashes, or becomes unavailable, the overall result is
`AR-RECORD/1`. After process exit, the files and any serialized report are
diagnostic evidence only and cannot be re-presented as success authority.

No record, receipt, file pair, controller return, event serialization, copied
object, or report can substitute for the live consumer decision.

## 7. Failure routing and non-regression

All inherited routing remains unchanged:

- platform or ABI authentication failure: `AR-AUTH/0`;
- initial collision: `AR-RESERVE/0`;
- I1 or stub-integrity failure: `AR-INVOKE/0-or-1`;
- semantic determinism failure: `AR-DETERMINISM/1`; and
- record/receipt, observer, move, witness, or consumer failure:
  `AR-RECORD/1`.

Denied access remains the only override. Cleanup failure preserves the first
primary class and marks the root `QUARANTINED-FAILED`. The fixed bundle,
request, grant, five counters, two deterministic runs, I2/I3 dispositions,
and every closed boundary remain unchanged.

## 8. Proposed closure

- `M-07A`: proposed closed by receipt v2, current consumer/observer/ABI IDs,
  exact v0.5 design and fresh-review pin meanings, and single-field rejection.
- `M-06B`: proposed closed by run record v3, non-PASS result text, explicit
  offline status, and exact live-consumer PASS authority.
- `N-01`: proposed closed by constant zero without a successful-call
  `get_last_error()` read and immediate capture only after a zero return.

These are author proposals, not independent closure. The v0.4 closures of
`M-05A` and core `M-06A`, plus inherited `M-04`, remain subject to fresh
non-regression review.

## 9. Maximum claim and next gate

Maximum claim: v0.5 defines a bounded public design successor for the three
v0.4 findings. It provides no implementation, Windows, observer, witness,
consumer, rehearsal, F0, provider/model, S0, or E0 evidence.

After the package is authenticated and committed, the exact next candidate
gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.5 INDEPENDENT REREVIEW OPEN`
