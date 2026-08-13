# S0 v0.14 public end-to-end assembly rehearsal design revision v0.4

- `status`: bounded public successor candidate; fresh independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`
- `predecessor_design_commit`: `24f1130c35aa3ddd4015f7ed0abae58c1eae8cc1`
- `predecessor_review_commit`: `3705571a1762f4e9d37738624b2c9f7b27afc9d6`
- `predecessor_review_sha256`: `e71c1312be10312bdc767910b3bcb18abdca6883797278e148e19fc812982c22`
- `implementation_status`: not implemented
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Replacement boundary

This v0.4 package replaces only the v0.3 rules implicated by `M-05A` and
`M-06A`. The effective design is v0.3 plus these replacements.

Unchanged and retained:

- every v0.2 public case, bundle, request, grant, I0/I1, I2/I3, record,
  deterministic-repeat, denied-boundary, and nonclaim rule;
- v0.3 initial-versus-race routing and call counts;
- v0.3 `STUB_INTEGRITY` and all five counters;
- v0.3 determinism-before-record validation order;
- v0.3 four output names, receipt fields, external provenance pins,
  quarantine rule, and exact failure classes; and
- the process-interruption/API-failure-only scope, with no power-loss,
  kernel-crash, or directory-metadata durability claim.

This gate changes public design text only. It does not authorize an
implementation, platform probe, rehearsal, provider/model, F0 content,
executor, judge, S0, E0, central system, or Project Brain action.

## 2. Exact supported process and ABI profile

The only supported future process is:

- 64-bit CPython 3.12.x on 64-bit Windows 10 or Windows 11;
- native pointer width 64 bits;
- local NTFS source and destination in one authenticated output directory and
  one volume; and
- the system `kernel32.dll` export named exactly `MoveFileExW`.

The normative Win32 declaration is:

```c
BOOL WINAPI MoveFileExW(
    LPCWSTR lpExistingFileName,
    LPCWSTR lpNewFileName,
    DWORD   dwFlags
);
```

The exact ABI meanings are:

- `LPCWSTR`: non-null pointer to a NUL-terminated array of 16-bit UTF-16 code
  units; Python binding `ctypes.c_wchar_p` on the supported Windows process;
- `DWORD`: unsigned 32-bit integer; Python binding `ctypes.c_uint32`;
- `BOOL`: signed 32-bit integer; Python binding `ctypes.c_int32`;
- `WINAPI`: Microsoft x64 Windows calling convention for the supported
  64-bit-only process; the Python loader must be
  `ctypes.WinDLL("kernel32", use_last_error=True)`;
- `argtypes`: exactly
  `[ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]`;
- `restype`: exactly `ctypes.c_int32`;
- both path arguments: absolute extended-length Win32 paths beginning with
  `\\?\`, constructed from the previously authenticated canonical output
  paths, with embedded NUL rejected before the call; and
- `dwFlags`: exactly numeric zero.

Before each call, `ctypes.set_last_error(0)` is executed. A nonzero return is
success. On a zero return, `ctypes.get_last_error()` is captured immediately
as the next operation before formatting, logging, cleanup, another FFI call,
or any other action can overwrite it. The captured unsigned 32-bit code is a
diagnostic; it grants no success.

Any different DLL resolution, export, architecture, loader, calling
convention, parameter type, return type, flag type/value, relative path,
nonextended path, embedded NUL, replace/copy flag, fallback, or retry is
`AR-AUTH/0` before output reservation.

## 3. Claim correction: files are not standalone success evidence

v0.3 claimed that an authenticated consumer could distinguish the required
publication moves from copied exact files. That claim is withdrawn.

The four filesystem objects are retained diagnostics. No file, pair of files,
receipt field, pathname, hash, controller return value, or later offline
consumer can by itself prove that either `MoveFileExW` call occurred.

The only success claim is a same-process verifier observation made while the
future candidate is running. After that verifier process exits, the files may
support reproduction and diagnosis but are explicitly `offline-not-success`.

## 4. Verifier-owned publication observer

The future implementation verifier parent process owns
`S0-PUBLIC-ASSEMBLY-PUBLICATION-OBSERVER-2`. It is outside the candidate
controller package and process and is authenticated by the verifier's
externally pinned implementation manifest. The candidate controller runs in a
separate child process created by that verifier.

The parent creates one private process-local `run_capability` object for one
fresh output-root identity and binds it to the exact child process handle and
one parent-owned IPC endpoint. The object:

- has no public constructor, serializer, byte representation, equality by
  value, copy operation, or candidate-visible secret;
- is accepted only by object identity in the observer instance that created
  it;
- is never passed to the child or written to the repository, output root,
  environment, command line, IPC bytes, log, or receipt; and
- is spent on the first terminal observer result.

The child receives only the other end of one verifier-created anonymous pipe.
It may send exactly these ASCII messages, each with one LF and no other byte:

- `PUBLISH_RECORD\n`; and
- `PUBLISH_RECEIPT\n`.

The parent accepts them only from the bound child endpoint and only in that
order. It replies `OK\n` after a successful event or closes the pipe after any
failure; no authority-bearing object or trace is returned. Extra, partial,
duplicate, reordered, non-ASCII, or post-terminal bytes fail.

The child cannot call `MoveFileExW` directly, obtain the parent FFI function
object, create an observer result, read the parent trace, obtain the run
capability or witness, or invoke either operation more than once. Static source
review, process-boundary inspection, and runtime import/open/call sentinels
must enforce those restrictions.

## 5. Independently observed move event

For each callback, the observer—not the candidate—performs these ordered
operations:

1. authenticate the exact root and expected source/destination path pair;
2. open the source without following reparse points and capture its immutable
   pre-call identity as `(volume_serial_number, file_index_high,
   file_index_low)` plus exact byte length and SHA-256;
3. require the destination absent immediately before the call;
4. invoke the exact section-2 ABI once with flags zero;
5. capture the return and last-error result as specified in section 2;
6. on success, require source absent, open destination without following
   reparse points, and require its volume/file-index identity, length, and
   SHA-256 equal the pre-call source values; and
7. append one immutable event to the observer-owned in-memory trace.

The record event must precede the receipt event. Their exact path pairs are:

- `run-record.pending -> run-record.json`; and
- `publication-receipt.pending -> publication-receipt.json`.

The trace event contains the observer instance identity, run capability
identity, ordinal `1` or `2`, authenticated output-root identity, source and
destination canonical paths, pre/post file identity, length, hash, ABI profile
ID, flags, return value, last-error result, and an observer-assigned terminal
status. It is process-local and is not candidate-authored receipt data.

Any mismatch, duplicate, reordering, copy-created file identity, source
replacement, destination collision, callback misuse, or observer failure is
terminal `AR-RECORD/1`, spends the capability, and prevents a success witness.

## 6. Live success witness and consumer

After the second event, the observer creates one private parent-process-local
`PublicationWitness` object only if the two immutable trace events are exact,
ordered, successful, and bound to the same child/capability/root.

`S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2`, also owned by the verifier parent,
returns success only when called in that same parent process with:

1. the exact witness object by identity;
2. the same observer instance, bound child process, pipe endpoint, and spent
   run capability;
3. the observer's exact two-event trace;
4. the exact final record/receipt pair and no pending names;
5. all v0.3 receipt and external provenance bindings;
6. matching pre/post file identities, lengths, and hashes from both events;
7. a nonquarantined root; and
8. a previously unconsumed witness.

Consumption atomically marks the witness used. A second attempt rejects.
The child controller never receives the witness and cannot call the live
consumer.

The verifier records only the aggregate result and externally authenticated
candidate/verifier identities in its future report. It must not serialize the
witness or claim that the report or output files recreate its authority.

## 7. Copied-pair rule

The exact hostile case from `M-06A` is mandatory:

1. construct exact pending record and receipt bytes;
2. copy them to both final names;
3. remove both pending names; and
4. present the exact final pair to the live consumer without an observer
   witness.

The result is `not-success` because no exact process-local witness exists.
Supplying a fabricated object, an object from another observer/run/root, a
replayed consumed witness, or a trace with no matching file identity also
rejects.

If a real two-event witness exists but a final object is later replaced by a
copy, its file identity no longer matches the observed destination identity
and the live consumer rejects. No offline or restarted-process consumer is
authorized to accept the pair.

## 8. Receipt and commit semantics

The v0.3 receipt remains a deterministic candidate-produced object binding
implementation, design, review, counters, primitive profile, paths, and record
hash. Its `publication_outcome` field is descriptive, not proof of the API
events.

The candidate controller reaches its internal `COMPLETE` state after the
observer reports the second move successful. The rehearsal itself is reported
PASS only after the separate verifier-owned live consumer accepts the witness
and current files. Thus controller completion without live-consumer acceptance
is not rehearsal success.

No fallible candidate success check follows the second move. The verifier's
consumer evaluation is outside candidate state and may downgrade the overall
rehearsal result to failure.

## 9. Failure routing and residue

All v0.3 routing remains unchanged. Specifically:

- ABI/platform authentication failure: `AR-AUTH/0`;
- initial output collision: `AR-RESERVE/0`;
- I1/stub-integrity failure: `AR-INVOKE/0-or-1`;
- semantic determinism failure: `AR-DETERMINISM/1`;
- observer callback, FFI, file-identity, publication, witness, or live-consumer
  failure: `AR-RECORD/1`.

Denied access remains the only override. Cleanup failure retains the first
primary class and marks the root `QUARANTINED-FAILED`. Residual or copied files
never substitute for the missing live witness.

## 10. Proposed closure

- `M-05A`: proposed closed by the literal Win32 declaration, fixed 64-bit
  process, exact ctypes loader/argtypes/restype, path representation, flags,
  and last-error order.
- `M-06A`: proposed closed by withdrawing standalone-file success and requiring
  a verifier-owned, process-local, identity-checked two-event witness plus
  destination file-identity continuity.

These are author proposals only. M-04 and M-07 remain inherited closed
subject to fresh non-regression review.

## 11. Maximum claim and next gate

Maximum claim: v0.4 proposes design-level closure of the two v0.3 major
findings. No FFI call, file identity, observer, witness, consumer, controller,
rehearsal, platform behavior, provider/model, F0, S0, or E0 result exists.

After this package is authenticated and committed, the exact next candidate
gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.4 INDEPENDENT REREVIEW OPEN`
