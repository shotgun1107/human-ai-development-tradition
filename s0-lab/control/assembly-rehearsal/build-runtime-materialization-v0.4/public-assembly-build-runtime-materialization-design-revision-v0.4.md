# S0 v0.14 public assembly build and runtime materialization design revision v0.4

## 1. Status and claim boundary

This document is a PUBLIC design candidate only. It does not authorize or
report a compiler invocation, build, binary, runtime tree, native API call,
platform probe, provider/model call, rehearsal, S0 run, or E0 run.

The effective design is the exact authenticated v0.3 admission package plus
the mandatory v0.4 corrections in this package. Direct execution of either
the v0.3 profile or this v0.4 design is forbidden. A future implementation
must independently authenticate the complete package, schemas, semantic
validator, source, toolchain, and all retained predecessor inputs before any
import, process creation, or native call.

Exact predecessor bindings:

- v0.3 package manifest SHA-256:
  `1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277`;
- v0.3 independent review SHA-256:
  `e84775d2cb07ea5353192bd3c3cbe80dec487af5bafa4ea36a91ade8b74914cc`;
- v0.3 admission schema SHA-256:
  `b9f87936be3b4376e3b6cc5ede9aaab2cc66b853b249c4ecacbd6a6160f7efc7`;
- v0.3 prepublication schema SHA-256:
  `1c9c355cedf162b343b59cd08de8816fd8e6488b5d729b3e02470246c0cf1eec`;
- v0.3 final-record schema SHA-256:
  `f63fd9059404d75cd6f5333907313599eeba374bdf207d7056cfbd1ba438e43d`;
- v0.3 mutation-matrix SHA-256:
  `965606a860409dc6810ffd7b969d9eb77de0f23aae0dcc49130a8145767f5685`.

The v0.3 review left exactly two MAJOR findings. Sections 2 and 3 replace
only the affected v0.3 rules. Every other authenticated v0.3 relation,
resource ceiling, authority restriction, record rule, and failure rule stays
effective.

## 2. Windows directory identity closure

### 2.1 Canonical virtual-directory grammar

Every application-directory or DLL-map parent is first parsed as ASCII text.
It is valid only when all of the following are true:

1. the only separator is the single byte `/`;
2. the path has no leading separator, trailing separator, doubled separator,
   backslash, colon, control byte, DEL byte, or non-ASCII byte;
3. every segment is nonempty and is neither `.` nor `..`;
4. every segment consists only of `A-Z`, `a-z`, `0-9`, `.`, `_`, and `-`;
5. no segment ends in `.`;
6. the part of each segment before its first `.` is not, under ASCII
   case-insensitive comparison, `CON`, `PRN`, `AUX`, `NUL`, `COM1` through
   `COM9`, or `LPT1` through `LPT9`; and
7. the complete path is at most 1,024 ASCII bytes.

The parser does not repair a path. It does not replace `\\` with `/`, delete
an empty segment, trim a dot, normalize case, expand a short name, or consult
the host. A noncanonical input fails before directory hashing, candidate
import, or process creation with `BR-AUTH/0`.

### 2.2 Admitted comparison key

For one valid canonical virtual directory `D`, define
`ascii_lower(D)` byte by byte:

- bytes `0x41` through `0x5a` are replaced with the corresponding byte plus
  `0x20`;
- every other admitted byte is copied unchanged.

The result is `windows_directory_identity_key`. No locale, Unicode,
filesystem, environment, current-directory, registry, PATH, or host case
mapping participates.

Before hashing or assigning indices, all identity keys must be pairwise
distinct. Therefore `Lib`, `lib`, and `LIB` cannot coexist as separate search
directories. Separator variants never reach this comparison because the
canonical grammar rejects them. Two different canonical paths producing the
same key fail as `BR-AUTH/0`; the implementation may not select one.

The exact directory identity preimage is ASCII with one final LF:

```text
windows_directory_identity_key=<identity-key>
```

`directory_identity_sha256` is SHA-256 over exactly those bytes. Hashing the
original case-preserving path, omitting the final LF, adding another line, or
using a repaired path fails.

### 2.3 Order and physical identity

The application directory remains index zero. Its identity key is removed
from the DLL-parent set before sorting. Remaining unique keys are sorted in
strict ascending unsigned-ASCII byte order and assigned consecutive indices.
Raw case-preserving paths never determine order.

After a later materializer creates the runtime tree but before a runtime
candidate can be imported or started, every search directory must be opened
without following a reparse point and queried as `FILE_ID_INFO`. The recorded
physical identity is the exact pair:

```text
(VolumeSerialNumber, FileId)
```

All pairs must be distinct, and every directory must have
`reparse_point=false`. A missing identity, repeated pair, reparse point, or
identity change fails. This second check catches filesystem aliases that are
not expressible by the restricted ASCII virtual grammar. It does not grant
build or runtime authority; it is a future implementation acceptance
condition.

### 2.4 DLL resolution binding

Each DLL-map row binds exactly:

- DLL name;
- case-preserving canonical runtime virtual path;
- canonical parent virtual directory;
- parent `windows_directory_identity_key`;
- assigned directory index; and
- authenticated target SHA-256.

The binding set is bijective with the authenticated DLL map. A different
parent key, index, path, target hash, duplicate basename under the admitted
DLL-name comparison, host-filled directory, PATH/registry/current-directory
source, or physical-identity alias fails before import or process creation.

This closes `BRM-V03-IR-001`: byte-distinct case aliases cannot receive
separate indices, separator aliases are invalid input, and physical
directories must also be distinct by stable file identity.

## 3. No-replace atomic publication closure

### 3.1 Exact primitive

The only admitted runtime-A publication primitive is:

- DLL: `kernel32.dll`;
- API: `SetFileInformationByHandle`;
- `FILE_INFO_BY_HANDLE_CLASS`: `FileRenameInfoEx`;
- numeric information class: `22`;
- structure: `FILE_RENAME_INFO` using its `Flags` union member;
- exact numeric flags: `0`;
- `FILE_RENAME_FLAG_REPLACE_IF_EXISTS` bit: unset;
- `FILE_RENAME_FLAG_POSIX_SEMANTICS` bit: unset; and
- same-volume source and destination: required.

The source is the retained handle for runtime-A's unpublished staging root,
opened with `DELETE` and `SYNCHRONIZE`. `RootDirectory` is the same retained
destination-parent handle whose identity was frozen in the prepublication
record and used by the diagnostic absence recheck. `FileName` contains only
the same authenticated final leaf name. `FileNameLength` is its exact UTF-16LE
byte count without a terminating NUL. Absolute paths, current-directory
resolution, a reopened parent, a recomputed name, a different source handle,
or a fallback rename API are forbidden.

Because the admitted final leaf is ASCII, `file_name_length_bytes` is exactly
twice its character count. That value is frozen in both record packages and
must equal the byte length passed to the call.

`publication_no_replace_policy_sha256` is SHA-256 over the RFC 8785 JCS UTF-8
encoding of the exact `publication_no_replace_policy` object followed by one
LF byte. No BOM or other trailing byte is included.

The retained handles use two exact ASCII/LF identity preimages. The source
preimage is:

```text
schema_id=S0-BRM-PUBLICATION-SOURCE-HANDLE-1
transaction_id=<64 lowercase hexadecimal characters>
volume_serial_number=<16 lowercase hexadecimal characters>
file_id=<32 lowercase hexadecimal characters>
required_access=DELETE,SYNCHRONIZE
```

The destination-parent preimage is:

```text
schema_id=S0-BRM-PUBLICATION-PARENT-HANDLE-1
transaction_id=<64 lowercase hexadecimal characters>
volume_serial_number=<16 lowercase hexadecimal characters>
file_id=<32 lowercase hexadecimal characters>
intended_final_name_utf16le_sha256=<64 lowercase hexadecimal characters>
```

Every line, including the last, ends in one LF. The two record identity
fields are SHA-256 over these exact preimages. The parent handle used by the
absence observation and rename call must reproduce the same parent preimage;
the source handle used by the call must reproduce the source preimage.

Microsoft documents `SetFileInformationByHandle`, the `FileRenameInfoEx`
enumeration entry, and the `FILE_RENAME_INFO` `Flags`, `RootDirectory`, and
byte-length fields in the public Win32 contract:

- <https://learn.microsoft.com/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle>
- <https://learn.microsoft.com/windows/win32/api/minwinbase/ne-minwinbase-file_info_by_handle_class>
- <https://learn.microsoft.com/windows/win32/api/winbase/ns-winbase-file_rename_info>

The design pins the above API surface but does not call it in this gate.

### 3.2 Linearization and race handling

The destination-absence recheck remains required and is recorded, but it is
diagnostic only. It never authorizes replacement. The sole publication
linearization point is a successful call to the exact primitive with flags
zero.

The ordered success path is:

1. `RUNTIME-TREES-BYTE-IDENTICAL`;
2. `RUNTIME-B-QUARANTINED`;
3. `PREPUBLICATION-RECORD-BODY-FROZEN`;
4. `PREPUBLICATION-RECORD-CLOSE-READBACK-VERIFIED`;
5. `DESTINATION-ABSENT-RECHECK-PASSED`;
6. `NO-REPLACE-ATOMIC-RENAME-INVOKED`;
7. `RUNTIME-A-ATOMICALLY-PUBLISHED` only after the call returns success;
8. `POSTPUBLICATION-IDENTITY-VERIFIED`;
9. `FINAL-RECORD-BODY-FROZEN`;
10. `FINAL-RECORD-CLOSE-READBACK-VERIFIED`; and
11. `FINAL-DIAGNOSTIC-RECORDS-FROZEN`.

If another actor creates the final name after step 5 and before the rename
linearization point, the no-replace call must fail. The implementation must
not overwrite, delete, rename aside, or select a new destination. Every call
failure, regardless of the platform error code, freezes primary failure
`BR-MATERIALIZE/1`, leaves the preexisting destination untouched, grants no
live/rehearsal/S0 authority, and permits no retry or replacement-capable
fallback.

The runtime staging output already exists before this failure, so mutation
rows truthfully retain output bit `/1`; that bit does not mean the final
destination was created or authorized.

### 3.3 Closed records

The v0.4 prepublication record is frozen before the call and binds:

- the exact v0.4 profile and authority closure;
- source-handle and destination-parent identities;
- intended final name and diagnostic absence observation;
- the exact no-replace policy hash;
- primitive ID;
- information-class numeric value `22`;
- rename flags numeric value `0`;
- exact UTF-16LE filename byte length; and
- exact policy, source-handle, and destination-parent preimage hashes.

It cannot claim call success, publication, final identity, or PASS.

The v0.4 final record can exist only on the success path. It binds the same
transaction, source handle, parent handle, final name, filename byte length,
primitive, class, and flags; `no_replace_atomic_rename_result=success`; the exact linearization
point; reopened destination identity; runtime manifest; target rows;
canonical target-set hash; byte count; and postpublication identity result.
All body objects are closed. The canonical, closed-file, and readback hashes
must be byte-identical under the retained JCS/UTF-8/final-LF codec.

This closes `BRM-V03-IR-002`: a destination created during the race makes the
same exact call fail, and no schema-valid success record can be produced for
that failed transaction.

## 4. Failure matrix and nonregression

The effective matrix is the exact 97-row v0.3 effective matrix followed by
the published 14 v0.4 rows. Effective count is 111. All IDs are unique. Every
row has one primary failure and one Boolean output-created bit whose `/0` or
`/1` suffix agrees with that Boolean. Cleanup, quarantine, record, and retry
facts never replace the first primary failure.

The v0.4 interface map and profile schema publish the same ordered semantic
relations. The exact twelve v0.3 resource ceilings remain unchanged. The
v0.3 target-set grammar, binary-import ownership, full import allowlists,
runtime role map, record hash closure, A/B preselection, B quarantine,
authority pins, and all other nonreplaced behavior remain effective.

Neither JSON Schema validity nor a future semantic-validator PASS is a build,
runtime, rehearsal, or S0 result. The implementation candidate, compiler,
binary materialization, native publication probe, and real Windows behavior
remain closed behind later explicit gates.

## 5. Required independent review result

A fresh PUBLIC reviewer must independently authenticate the v0.3 base,
v0.3 review, this package, and the exact predecessor manifests named in the
review brief. It must reconstruct the Windows directory key and no-replace
transaction, attack all 111 effective rows, validate all three v0.4 schemas,
and confirm nonregression without building or calling a native API.

Only a verdict of
`PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
BLOCKING and zero MAJOR findings can support a later CONTROL integration
gate. This document does not open that gate.
