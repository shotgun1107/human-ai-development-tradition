# Public Assembly Runtime Profile + Neutral Preloader Design Revision v0.5

Status: successor DESIGN candidate for fresh independent rereview

## 1. Authority, scope, and composition

This is a non-destructive successor to immutable v0.4. It closes only
`RPNP4-IRR-001`, `RPNP4-IRR-002`, and `RPNP4-IRR-003`. The effective contract
is the complete authenticated v0.4 package followed by this complete v0.5
overlay. Consumers MUST authenticate and validate all of v0.4 before applying
all of v0.5; selective, mixed, reordered, or partially validated predecessor
use rejects.

Authority pins are:

- base commit `440f4342bb27398c6f2a4131d5518f2b55722f4c` and tree
  `c77b078ac934ab7a8b31142bad337cf86ee16ca1`;
- v0.4 design manifest
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- v0.4 interface map
  `63b36e5b7a6f1aad8027b5794cf21221a05d8eb057f4c0c1d0350b67a12ec2a7`
  and schema
  `3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd`;
- v0.4 implementation manifest
  `670803a185e6968f97acb8bdc4acd99932e4dc7722157816a28d684b9e9989f5`;
- actual current v0.4 implementation-rereview record
  `1edea02f498a47839ae9575df41d4f75d4e949b98d6ca87521af2c02dca7c8ab`;
  and
- v0.4 CONTROL decision
  `4342c64a012f6bc9fe9d2550d3879fbef89b592ef08ade1940a3344d9d1c2920`.

The immutable CONTROL decision body contains the older rereview-record value
beginning `89fbac`. That value is stale historical metadata, not current hash
authority. The v0.5 package binds the current Git bytes and canonical sidecar
value beginning `1edea0`; the v0.4 artifact is not rewritten. The preserved
verdict and finding counts are semantically consistent.

Every v0.1 through v0.4 obligation not expressly replaced below remains
authoritative, including process creation, five-handle inheritance, admission,
one-use guard, atomic-root, terminal-state, import/environment, package,
resource, and closed-claim rules. The profile order is exactly v0.1, v0.2,
v0.3, v0.4, then v0.5.

This design revision authorizes no source or binary implementation, build,
runtime execution, stage-70 probe, stage-80 connection, live assembly,
official rehearsal, S0, F0 access, Git publication, or generalized security
claim.

## 2. RPNP4-IRR-001: exact native API contract

The v0.5 schema and interface map bind authenticated source hashes, declared
call inventories, direct-import families, binary imports, loaded images, and
the effective profile as one equality relation. An omitted or unknown relied
call, an alternate route, a reordered inventory, or an unmatched import
rejects. Decision-semantic calls affect an admission, identity, policy, or
state decision. Supporting calls implement cleanup, error retrieval, timing,
memory clearing, or attribute-list lifecycle and cannot become an undeclared
alternate decision route.

### 2.1 Guard source-derived inventory

Authenticated source:
`implementation/native/s0_runtime_handle_guard_v0_4.cpp`, SHA-256
`ed22d812d873a03e5d0f21a46a8c3a5e8eba47eb29744cf4e7e2341d814e599f`.

- Decision-semantic, exact 18:
  `CompareStringOrdinal`, `GetCurrentProcessId`,
  `GetFileInformationByHandleEx`, `GetFileType`, `GetHandleInformation`,
  `GetNamedPipeInfo`, `GetProcessId`, `InterlockedCompareExchange`,
  `InterlockedExchange`, `IsProcessInJob`, `MultiByteToWideChar`,
  `NtQueryInformationProcess`, `NtQueryObject`, `PeekNamedPipe`,
  `QueryFullProcessImageNameW`, `ReadFile`, `WaitForSingleObject`, and
  `WriteFile`.
- Supporting, exact 4: `CloseHandle`, `GetCurrentProcess`, `GetLastError`, and
  `SecureZeroMemory`.
- Direct-import families, exact:
  `kernel32.dll`, `ntdll.dll`, `python312.dll`, and `static-crt-support`.

This expressly brings `PeekNamedPipe`, `IsProcessInJob`,
`WaitForSingleObject`, `GetLastError`, and `GetCurrentProcess` into the frozen
contract.

### 2.2 Preloader source-derived inventory

Authenticated source:
`implementation/native/s0_neutral_preloader_v0_4.cpp`, SHA-256
`a32fb997638607e3577ac44382b29c015685920655ee1c2499aa975131250cae`.

- Decision-semantic, exact 44: `AssignProcessToJobObject`,
  `BCryptCloseAlgorithmProvider`, `BCryptCreateHash`, `BCryptDestroyHash`,
  `BCryptFinishHash`, `BCryptGetProperty`, `BCryptHashData`,
  `BCryptOpenAlgorithmProvider`, `CompareStringOrdinal`, `CreateFileW`,
  `CreateJobObjectW`, `CreatePipe`, `CreateProcessW`, `DuplicateHandle`,
  `FindFirstFileW`, `FindNextFileW`, `GetCurrentProcessId`, `GetDriveTypeW`,
  `GetExitCodeProcess`, `GetFileAttributesExW`, `GetFileAttributesW`,
  `GetFileInformationByHandleEx`, `GetFileSizeEx`, `GetFileType`,
  `GetFinalPathNameByHandleW`, `GetFullPathNameW`, `GetHandleInformation`,
  `GetVolumeInformationByHandleW`, `GetVolumePathNameW`,
  `InitializeProcThreadAttributeList`, `MultiByteToWideChar`, `NtCreateFile`,
  `NtQueryObject`, `OpenProcess`, `PeekNamedPipe`, `ReadFile`, `ResumeThread`,
  `SetFilePointerEx`, `SetHandleInformation`, `SetInformationJobObject`,
  `UpdateProcThreadAttribute`, `WaitForSingleObject`,
  `WideCharToMultiByte`, and `WriteFile`.
- Supporting, exact 7: `CloseHandle`, `DeleteProcThreadAttributeList`,
  `GetCurrentProcess`, `GetLastError`, `GetTickCount`, `Sleep`, and
  `TerminateProcess`.
- Direct-import families, exact: `bcrypt.dll`, `kernel32.dll`, `ntdll.dll`,
  and `static-crt-support`.

### 2.3 Materializer contract

The authenticated v0.4 materializer source
`implementation/native/materialize-runtime.ps1`, SHA-256
`26d5bcda6117742317ea6a7fc8a21d7bb8bf8e338b89e8a7cd93a87957028bd8`,
has no direct Win32/NT call and therefore has empty source-derived decision and
supporting call sets. That current fact is not implementation of section 4.

A future physical-isolation implementation MUST expose this exact
ASCII-sorted unique 29-call inventory: `AccessCheck`, `BCryptCloseAlgorithmProvider`,
`BCryptCreateHash`, `BCryptDestroyHash`, `BCryptFinishHash`,
`BCryptGetProperty`, `BCryptHashData`, `BCryptOpenAlgorithmProvider`,
`CloseHandle`, `DuplicateHandle`, `FindClose`, `FindFirstFileW`,
`FindFirstStreamW`, `FindNextFileW`, `FindNextStreamW`, `FlushFileBuffers`,
`GetDriveTypeW`, `GetFileInformationByHandleEx`,
`GetFinalPathNameByHandleW`, `GetLastError`, `GetSecurityInfo`,
`GetTokenInformation`, `GetVolumeInformationByHandleW`, `LocalFree`, `NtCreateFile`,
`NtQueryObject`, `ReadFile`, `SetFilePointerEx`, and `WriteFile`; and exact
families `advapi32.dll`, `bcrypt.dll`, `kernel32.dll`, `ntdll.dll`, and
`static-crt-support`. Source review must classify the eventual occurrences as
decision-semantic or supporting and prove that their union, imports, profile,
binary, and loaded routes equal this required set. This document does not
claim those calls exist or execute now. `LocalFree` is the sole explicitly
classified supporting cleanup call in this future set. The materializer owns
every security-descriptor buffer returned by a successful `GetSecurityInfo`
call and MUST call `LocalFree` exactly once on every success, failure, timeout,
cleanup, and close terminal path. Omitting `LocalFree`, substituting another
cleanup call, adding an unknown call, or violating source/map/schema/import
inventory equality rejects.

## 3. RPNP4-IRR-002: canonical launch evidence v2

The sole new grammar is `S0-LAUNCH-HANDLE-SET-EVIDENCE-2`. Encoding is
US-ASCII, no BOM, no CR, with lines exactly `field-name=field-value\n` and
one exact final LF. The header is field 1:
`schema_id=S0-LAUNCH-HANDLE-SET-EVIDENCE-2` (`schema_id`: width 31,
exact ASCII). The following eight semantic groups contain fields 2 through 45
in the listed order. Group boundaries are semantic; no extra delimiter line is
serialized.

| Group | Ordered fields with exact width and normalization |
|---|---|
| `run-authority` | `run_nonce` (64, lowercase hex); `external_pin_digest` (64, lowercase hex); `workspace_root` (3..32766, uppercase-drive absolute backslash path, no dot segment or delimiter, no trailing separator except drive root) |
| `runtime-profile-and-package-hashes` | `preloader_image_sha256`, `runtime_package_sha256`, `launch_control_sha256`, `runtime_profile_v0_1_sha256`, `runtime_profile_v0_2_sha256`, `runtime_profile_v0_3_sha256`, `runtime_profile_v0_4_sha256` (each 64, lowercase hex) |
| `application-bootstrap-verifier-identities` | `application_virtual_path` (1..1024, canonical POSIX virtual path with no dot segment, delimiter, or case alias); `application_sha256` (64, lowercase hex); `bootstrap_virtual_path` (same path rule); `bootstrap_sha256` (64, lowercase hex); `verifier_virtual_path` (same path rule); `verifier_sha256` (64, lowercase hex) |
| `creation-flags` | `creation_flags_numeric` (10, exact lowercase `0x` plus eight hex, constant `0x08080404`); `startupinfoex_dwflags` (1, canonical unsigned decimal, constant `0`) |
| `inheritance-switch` | `b_inherit_handles` (4, lowercase ASCII Boolean, constant `true`) |
| `attribute-list-shape` | `attribute_count` (1, unsigned decimal, constant `1`); `attribute_id_numeric` (10, lowercase `0x` plus eight hex, constant `0x00020002`); `handle_array_bytes_x64` (2, unsigned decimal, constant `40`); `handle_count` (1, unsigned decimal, constant `5`) |
| `five-ordered-handle-records` | `handle_0_role` (14, `admission-read`); `handle_0_kind` (25, `byte-stream-pipe-endpoint`); `handle_0_access` (19, `read-not-write-data`); `handle_0_locator` (18, lowercase `0x` plus sixteen hex, nonzero and nonsentinel); `handle_1_role` (20, `commit-request-write`); `handle_1_kind` (25, `byte-stream-pipe-endpoint`); `handle_1_access` (19, `write-not-read-data`); `handle_1_locator` (18, same locator rule); `handle_2_role` (17, `commit-reply-read`); `handle_2_kind` (25, `byte-stream-pipe-endpoint`); `handle_2_access` (19, `read-not-write-data`); `handle_2_locator` (18, same locator rule); `handle_3_role` (11, `output-root`); `handle_3_kind` (9, `directory`); `handle_3_access` (52, `file-list-directory-read-attributes-synchronize-only`); `handle_3_locator` (18, same locator rule); `handle_4_role` (17, `preloader-process`); `handle_4_kind` (7, `process`); `handle_4_access` (50, `process-query-limited-information-synchronize-only`); `handle_4_locator` (18, same locator rule) |
| `precreation-verifier` | `precreation_verifier_pid` (1, unsigned decimal, constant `0`) |

Field names, group names, group order, field order, constants, widths,
normalization, count, hash algorithm `sha256`, and final LF are all normative.
`external_pin_digest` and `workspace_root` are now inside the first named
semantic group. Raw handle values remain forbidden in the admission frame.
The producer, consumer, schema, interface map, admission, and tests MUST all
bind exactly v2. Any v1 component in a v2 transaction, any v2 component paired
with a v1 producer/consumer/schema/interface, or any implicit migration
rejects before authority.

## 4. RPNP4-IRR-003: physical output and evidence isolation

Lexical overlap is diagnostic only. Authority comes from retained kernel
handles and stable object identities:

1. Bind and retain base-root, repository-root, volume-root, every output
   ancestor, output-root, evidence-root, and every created output/evidence
   file through terminal measurement.
2. Open each existing ancestor component relative to the retained parent via
   direct `NtCreateFile`, with `OBJ_DONT_REPARSE`,
   `FILE_OPEN_REPARSE_POINT`, directory/synchronous policy, and no
   `FILE_SHARE_WRITE` or `FILE_SHARE_DELETE`.
3. Measure each component twice: `FileIdInfo` stable volume serial plus
   128-bit file ID; `FileAttributeTagInfo` non-reparse directory;
   `FileStandardInfo` one link and not delete-pending; local fixed NTFS volume;
   and security-descriptor SHA-256 plus effective-token binding. Any change,
   unsupported API/filesystem, symlink, junction, any reparse point, or volume
   mount rejects before output authority.
4. Compare every output ancestor and root identity with the retained base
   identity. Equality, containment, aliasing, or rebinding rejects.
5. Exclude the repository physically: bind its retained volume/file identity
   before the ancestry walk; compare the complete output ancestor chain,
   output root, and evidence root for identity equality, physical containment,
   physical alias, and reparse rebinding. Output or evidence under the
   repository rejects before any authoritative write. A string-prefix check is
   never sufficient.
6. Create the output leaf once, relative to the retained output parent, with
   direct `NtCreateFile`, `FILE_CREATE`, `OBJ_DONT_REPARSE`, and
   `FILE_OPEN_REPARSE_POINT`. Preexistence or pathname reopen rejects.
7. Perform every create, write, flush, readback, hash, inventory, sidecar,
   pre/post measurement, cleanup, and terminal operation relative to the
   retained output identity. Retain exclusive created-file handles until the
   final manifest/sidecar readback, pre/post identity equality, terminal state,
   and cleanup record are complete; then close exactly once.

This contract blocks the known alias-parent gap at the design level. It does
not establish that Windows, NTFS, a future implementation, or post-close state
actually satisfies it.

## 5. End-to-end preservation and bounds

The preserved end-to-end chain is: exact external URL/redirect/digest/size/
provenance pins; retained-handle runtime materialization; complete profile
composition; authenticated preloader; evidence v2; exact `CreateProcessW`
handle-list launch; postcreation nonce/PID/version/object binding; one-use
guard before import; verified bytes equal executed/imported bytes; exact
interpreter, standard-library, native-library, and import closure; and
retained-root output/evidence production.

Exact bounded constants are admission maximum 8,192 bytes, evidence maximum
65,536 bytes, five handles, runtime maximum 512 files, and runtime maximum
536,870,912 bytes. Exact manifests reject unlisted files, alternate data
streams, case aliases, shadow artifacts, duplicate logical paths, and
unexpected import routes. Every acquire path needs a single terminal owner;
failure terminates any suspended child, quarantines partial output, records a
bounded cause, and closes retained resources without retrying into new
authority.

## 6. Design evidence and nonclaims

TEST4 ran the published Python 3.12.10/jsonschema 4.26.0 command in 323 ms and
reported PASS 23 / FAIL 0 / UNVERIFIED 3, candidate failures 0, and harness
failures 0. It rejected all 595 mutations: 5 overlay, 11 `LocalFree` cleanup,
208 evidence, 349 schema, 5 v1/v2 mixing, 11 physical, and 6 cross-cutting.
This is design-level synthetic/static evidence only.

Unverified items are predecessor profile bytes outside the TEST allowlist;
OS, filesystem, API, and runtime behavior; PE/import/loaded-image closure;
stage 70; stage 80; and live assembly. There is no claim of runtime source or
binary implementation, post-handle-close same-user or administrator
resistance, all-Windows/filesystem correctness, full loader closure, new
downloader or supplier/TLS/provenance assurance, official rehearsal, S0,
central-system or Project Brain implementation, operational safety, economic
value, or model-to-model transfer.
