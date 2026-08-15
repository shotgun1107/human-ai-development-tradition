# S0 v0.14 public assembly build and runtime materialization design revision v0.3

- `status`: design candidate; fresh independent review required
- `base_package_manifest_sha256`: `47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`
- `base_review_sha256`: `d5066d11172cdc33441e39087898a33ab14b5371533a0f4f529de92eb80be051`
- `implementation_status`: not implemented
- `build_or_runtime_status`: not executed

## 1. Purpose and composition

v0.3 is a bounded successor to the authenticated v0.2 package. It changes
only the four MAJOR findings in the v0.2 independent review. The embedded
v0.2 admission package remains immutable historical input and must validate
against the exact authenticated v0.2 schema. Direct use of that embedded
package as an executable build profile is forbidden.

The effective v0.3 contract is the embedded v0.2 package plus every mandatory
v0.3 correction in the interface map, profile schema, two record schemas, and
mutation matrix. An implementation may not select only some corrections or
fall back to a v0.2 interpretation.

## 2. Canonical target-set digest

Every `target_set_sha256` uses the exact preimage schema
`S0-BRM-TARGET-SET-PREIMAGE-1`. The preimage is ASCII, contains no BOM or CR,
uses one LF after every line including the last line, and has this exact
order:

```text
schema_id=S0-BRM-TARGET-SET-PREIMAGE-1
target_count=<canonical unsigned decimal>
total_target_bytes=<canonical unsigned decimal>
path_byte_length=<canonical unsigned decimal>
path=<canonical path>
target_byte_length=<canonical unsigned decimal>
target_sha256=<64 lowercase hexadecimal characters>
```

The four row lines repeat once for each target. Canonical unsigned decimal is
`0` or a nonzero decimal without a leading zero. `target_count` must be at
least one and equal the number of rows. `total_target_bytes` is the exact sum
of all `target_byte_length` values.

Paths are nonempty repository-relative ASCII byte strings with `/` separators.
Every segment matches `[A-Za-z0-9._-]+`; the path may not start with `/` and
no segment may be empty, `.` or `..`. Case is preserved and compared by raw byte.
Rows are in strict ascending unsigned ASCII path-byte order. Duplicate paths
are rejected before hashing, including duplicates whose content hashes differ.
Each path length is the ASCII byte length; each target length and hash comes
from the exact authenticated target bytes. No Unicode, locale, filesystem,
Git ordering, or manifest iteration order participates.

`target_set_sha256` is SHA-256 over exactly the complete preimage bytes. A
missing, extra, reordered, duplicate, malformed, empty, count-mismatched,
length-mismatched, or hash-mismatched row fails as `BR-AUTH/0` before candidate
import or process creation.

## 3. Effective binary import roles

The exact security-relevant direct-import list for the native preloader is:

1. `kernel32.dll!CreateProcessW`;
2. `ntdll.dll!NtCreateFile`.

The exact effective RPNP v0.4 observation-call direct-import list for the
runtime guard, in order, is:

1. `kernel32.dll!GetHandleInformation`;
2. `kernel32.dll!GetFileType`;
3. `kernel32.dll!GetNamedPipeInfo`;
4. `kernel32.dll!GetFileInformationByHandleEx`;
5. `kernel32.dll!GetProcessId`;
6. `kernel32.dll!GetCurrentProcessId`;
7. `kernel32.dll!QueryFullProcessImageNameW`;
8. `ntdll.dll!NtQueryObject`;
9. `ntdll.dll!NtQueryInformationProcess`;
10. `kernel32.dll!ReadFile`;
11. `kernel32.dll!CloseHandle`.

The guard's required export is exactly
`PyInit_s0_runtime_handle_guard_v0_4`. It may not import `NtCreateFile`.
The lists above are not substitutes for the complete role import allowlist:
the complete import set, including admitted CRT imports, must equal the
separately authenticated role import-allowlist manifest. Any import outside
that manifest fails. Inspection remains byte-bound and must not load either
image.

## 4. Ordered DLL search closure

The v0.3 admission package carries both
`ordered_dll_search_directories` and `dll_resolution_bindings`.

The application directory is the parent virtual directory of the exact
`verifier_application` runtime-role row and is directory index zero. Collect
the parent virtual directory of every authenticated `dll_map` row, remove the
application directory and byte-identical duplicates, sort the remaining
ASCII paths by unsigned byte order, and append them. This is the only valid
directory inventory and order.

For each directory row,
`directory_identity_sha256` is SHA-256 of the exact ASCII bytes
`directory=<virtual_directory>\n`. Indices are contiguous from zero. A host
path, PATH, registry, current directory, user site, environment value, or
filesystem enumeration may not add, remove, or reorder a directory.

There is exactly one resolution binding per `dll_map` row, in the exact map
order. It repeats the DLL name, exact runtime virtual path, SHA-256, parent
directory, and derived directory index. DLL names are unique under ASCII
lowercase comparison. The resolved bytes must come from that exact virtual
path and match that exact hash; directory search may not select another file
with the same basename. Missing, extra, duplicate, reordered, host-filled,
or mismatched directory or binding data fails before import or process.

This is a design closure. It does not claim that Windows loader behavior has
been observed; that remains a later separately gated platform test.

## 5. Closed record packages

The prepublication and final diagnostic records validate against the two
separate authenticated v0.3 schemas. Every object uses
`additionalProperties: false`; the published required lists and
`body_field_order` are exact.

The package codec is RFC 8785 JCS over UTF-8 without BOM followed by exactly
one LF. `body_field_order` is the normative semantic field inventory and
construction traversal; JCS, not insertion order, fixes the final JSON key
order. `body_canonical_sha256` hashes the canonical body bytes before write.
`body_closed_file_sha256` hashes the exact body file after close.
`body_readback_sha256` hashes bytes reopened through the retained parent.
All three must be byte-identical. They do not hash the enclosing package, so
there is no self-reference. After those fields exist, the complete record
package can be canonically encoded and externally hashed.

The prepublication body contains only already observed admission, staging,
equality, ownership, quarantine, retained-parent, intended-name, initial
destination-absence, and state facts. Its closed schema makes rename success,
final identity, postpublication rehash, or PASS an unknown forbidden field.

After prepublication body close/read-back succeeds, CONTROL must make a fresh
destination-absence observation through the same retained parent and exact
intended final name. The recheck phase is
`DESTINATION-ABSENT-RECHECK-PASSED`. No callback, path recomputation,
filesystem enumeration, or other candidate operation may occur between that
recheck and the one same-volume atomic A rename. A missing, stale, false, or
parent/name-mismatched recheck freezes `BR-MATERIALIZE/1` before rename.

The final body is created only after rename, retained-parent reopen, final
object identity comparison, runtime-manifest verification, exact file count,
total-byte count, every row hash, and canonical target-set rehash. It binds
the frozen prepublication package hash and the exact destination-recheck
observation hash. Its package uses the same body close/read-back equality.
Failure quarantines the candidate and grants no authority.

## 6. Failure matrix

All 63 authenticated v0.2 effective rows remain in exact order and keep their
original primary failure and output-created bit. v0.3 appends exactly 34 rows:

- 8 canonical target-set rows;
- 6 binary-role/import rows;
- 8 DLL-directory/resolution rows; and
- 12 record/publication rows.

The effective total is 97. Every added row has one action boundary, one
primary failure, and one Boolean output-created value. The immutable-first-
failure and no-retry rules remain unchanged.

## 7. Machine-contract precedence and nonregression

The v0.3 interface map and profile schema contain the same 42 semantic
relations in the same order. The semantic validator must execute those
relations and every nonreplaced v0.2 relation. Schema string presence is not
execution evidence, and schema or semantic validation never authorizes a
build.

The v0.3 authority extension also binds the exact v0.2 package and review,
the independently pinned v0.3 package and approving review, and both record
schema hashes. The record-schema hashes in authority and publication objects
must equal each other and the exact authenticated schema bytes.

All v0.2 authority pins, source/toolchain closure, reproducible A/B build,
static inspection, runtime roles, module mapping, resource limits, claim
limits, diagnostic-only publication, and later platform-test boundaries
remain effective except for the four exact v0.3 replacements.

## 8. Closed boundaries and maximum claim

No source, compiler, build, binary, runtime tree, native API, loaded image,
Windows behavior, platform probe, live assembly, rehearsal, F0 content,
provider/model call, S0, E0, central system, or Project Brain result was
created or observed.

Maximum claim: v0.3 is a bounded public design successor that defines one
constructible target-set digest, corrects binary role imports, closes the DLL
directory inventory, and provides closed publication record packages and an
explicit destination recheck. Fresh independent review is still required.
