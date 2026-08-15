# S0 v0.14 public assembly build and runtime materialization acceptance plan v0.4

## 1. Scope

This plan tests only the public v0.4 design package as data. It does not build
or load a binary, materialize a runtime tree, call a native API, run a
platform probe, or open any S0 execution gate.

The effective candidate is the authenticated v0.3 package plus the mandatory
v0.4 overlay. Direct v0.3 execution is forbidden. Every test uses clearly
fake PUBLIC in-memory objects and exact authenticated public schemas.

## 2. Integrity preflight

Before substantive review:

1. pin origin, review branch, HEAD, tree, sole parent, and candidate remote
   ref;
2. run the canonical text validator SelfTest;
3. authenticate the v0.3 package manifest, v0.3 review, v0.4 package manifest,
   all logical targets, and every sidecar before reading targets;
4. authenticate every predecessor manifest named by the review brief before
   reading its literal target paths;
5. reject duplicate JSON keys and validate UTF-8, BOM absence, CR absence,
   final LF, trailing whitespace, sidecar format, and exact hashes;
6. validate the v0.1, v0.2, v0.3, v0.4, v0.4 prepublication, and v0.4 final schemas
   against Draft 2020-12;
7. resolve the v0.4 absolute base reference to the exact authenticated v0.3
   schema and the nested v0.3 reference to v0.2; and
8. retain all hashes for one final recheck.

Any real mismatch makes the review `INVALID-REVIEW`; an ordinary reviewer
command or quoting error is corrected and rerun.

## 3. Windows directory identity tests

### 3.1 Positive construction

Independently construct an inventory containing:

- one application directory at index zero;
- at least three DLL parents whose raw case-preserving paths sort differently
  from their ASCII-lowercase identity keys;
- exact identity-key preimages and SHA-256 values;
- pairwise-distinct synthetic `FILE_ID_INFO` identities;
- exact DLL bindings for every DLL-map row; and
- no reparse point.

Two independently written serializers must produce identical identity keys,
preimages, hashes, order, indices, and binding rows.

### 3.2 Required rejection cases

Reject before import or process creation:

- empty, leading, trailing, or doubled separator;
- backslash, colon, control, DEL, non-ASCII, `.` or `..` segment;
- trailing-dot segment;
- `CON`, `PRN`, `AUX`, `NUL`, `COM1`-`COM9`, or `LPT1`-`LPT9` segment,
  including an extension;
- incorrect ASCII lowercase transform;
- `Lib`/`lib` or another duplicate identity key;
- original-case rather than identity-key hashing;
- missing or extra final LF in the identity preimage;
- raw-path order instead of identity-key order;
- application directory not at index zero;
- repeated or malformed `FILE_ID_INFO` identity;
- a reparse point;
- binding path, parent key, index, or target-hash mismatch; and
- host, PATH, registry, current-directory, user-site, or environment fill.

Each case has primary failure `BR-AUTH/0`, creates no build output, and cannot
be repaired by selecting one alias.

## 4. No-replace publication tests

### 4.1 Static contract reconstruction

Independently reconstruct exactly:

- `kernel32.dll!SetFileInformationByHandle`;
- `FileRenameInfoEx` numeric class `22`;
- `FILE_RENAME_INFO.Flags=0`;
- replace-if-exists and POSIX-semantics bits unset;
- retained runtime-A source handle with `DELETE` and `SYNCHRONIZE`;
- the same retained parent handle and final leaf name used by the recheck;
- UTF-16LE byte length excluding terminal NUL;
- exact source-handle and parent-handle ASCII/LF identity preimages;
- RFC 8785 JCS policy-object hash with one final LF;
- same-volume requirement; and
- successful call as the sole publication linearization point.

The v0.4 prepublication and final record schemas must expose one closed field
inventory for these facts. Missing, unknown, reordered cross-boundary, or
changed primitive fields reject.

### 4.2 Hostile race table

Model, without calling Windows, these deterministic traces:

1. destination absent at recheck and still absent at call: success may advance
   through publication and postpublication identity checks;
2. destination exists at recheck: stop before the call with
   `BR-MATERIALIZE/1`;
3. destination is created after recheck but before the call: the exact
   no-replace call fails, the intervening object is unchanged, and the trace
   stops with `BR-MATERIALIZE/1`;
4. flags set replace-if-exists or POSIX semantics: reject before call;
5. different API, information class, source handle, parent handle, final name,
   access rights, name length, handle-identity preimage, policy hash, or
   volume: reject before call;
6. call failure followed by another name, retry, delete, overwrite, or
   replacement-capable fallback: reject; and
7. failed call followed by final record, PASS, live, rehearsal, or S0 claim:
   reject.

Publication-stage rows retain output bit `/1` only because the staging runtime
already exists. A `/1` bit never means the destination was successfully
published.

## 5. Schema and cross-file tests

Use one clearly fake PUBLIC in-memory nested admission package to validate:

- exact v0.3 base-profile reference and hash binding;
- v0.4 authority extension;
- directory grammar, inventory, physical identities, and DLL bindings;
- no-replace policy and transaction;
- v0.4 prepublication and final record packages;
- exact twelve resource values; and
- semantic-validator fail-closed fields.

At every new object depth, delete every required property and add one unknown
property. All must reject. Mutate every digest to uppercase, wrong length,
all zero when a meaningful evidence hash is required, or a different
authenticated object. All must reject or fail the semantic relation.

The interface map and schema semantic-relation arrays must be byte-for-byte
equal in order and content. The effective mutation inventory must reconstruct
as 97 authenticated v0.3 rows plus 14 published v0.4 rows, for 111 unique IDs.
Every expected-primary suffix must agree with its Boolean output bit.

## 6. Nonregression and resources

Confirm that all nonreplaced v0.3 authority, target-set, binary-import,
runtime-map, record, failure, publication-owner, quarantine, and claim rules
remain effective. Confirm exact equality of these twelve resource values:

| Resource | Value |
|---|---:|
| `source_bytes` | 268435456 |
| `toolchain_bundle_bytes` | 25769803776 |
| `cpython_dependency_bundle_bytes` | 4294967296 |
| `build_root_bytes_each` | 34359738368 |
| `runtime_tree_bytes` | 2147483648 |
| `materialization_staging_bytes_each` | 4294967296 |
| `private_bytes_aggregate` | 17179869184 |
| `captured_output_bytes_per_command` | 16777216 |
| `runtime_file_count` | 20000 |
| `wall_seconds_per_build` | 3600 |
| `materialization_seconds` | 1800 |
| `concurrent_build_processes` | 1 |

## 7. Verdict limit

Return `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY`
only with zero BLOCKING and zero MAJOR findings. Any design finding returns
`REVISE-AND-REVIEW`. Integrity, input-boundary, independence, or F0 failure
returns `INVALID-REVIEW`.

Even a PASS is design evidence only. It does not authorize source creation,
compiler execution, binary loading, native calls, runtime materialization,
rehearsal, or S0.
