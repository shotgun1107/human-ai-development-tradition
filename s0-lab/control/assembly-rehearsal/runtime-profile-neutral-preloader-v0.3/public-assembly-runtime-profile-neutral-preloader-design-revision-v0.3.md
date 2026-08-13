# Public Assembly Runtime Profile + Neutral Preloader Design Revision v0.3

Status: CONTROL design candidate for fresh independent rereview

## 1. Scope, authority, and replacement rule

This revision answers only the three findings preserved in the v0.2
independent-rereview result record:

1. inherited-handle discovery was not defined;
2. output-root creation and later opening left a substitution window; and
3. terminal retry wording conflicted with terminal-state immutability.

It replaces:

- v0.2 §§2 and 4 insofar as they define the inherited handle set, private
  wrapper binding, and output-root state construction;
- v0.2 §6 failure routing insofar as root creation now occurs in the
  preloader before verifier launch; and
- v0.2 interface-map, schema, and acceptance clauses corresponding to those
  subjects.

Every other v0.1 and v0.2 clause remains authoritative. The effective public
assembly design remains the frozen assembly v0.3 plus v0.4 replacements plus
v0.5 replacements, together with runtime/preloader v0.1, v0.2, and this v0.3
replacement. A consumer must apply the replacements in that order and reject
any attempt to select a convenient predecessor clause.

This is a design artifact. It does not authorize or establish an
implementation, compiler invocation, runtime capture, native binary, platform
probe, fixture, oracle, S0 run, official rehearsal, or public success result.

## 2. Authority graph and trust closure

The externally authenticated CONTROL launcher and the Windows kernel remain
the only external roots of trust. The launcher authenticates the exact
preloader image, runtime-profile package, workspace and runtime roots, public
assembly inputs, and platform closure before creating the preloader. No caller
path, environment value, serialized handle number, Python object, or child
self-report is an authority root.

The preloader's effective direct-import surface is exactly:

- the already admitted `kernel32.dll` imports;
- the already admitted `bcrypt.dll` imports; and
- the v0.3 `ntdll.dll!NtCreateFile` import.

The exact loaded `ntdll.dll` path, file identity, SHA-256, PE machine, image
identity, and `NtCreateFile` import binding are members of the authenticated
platform closure. The preloader must finish those checks before its first
`NtCreateFile` call. No delay-load, `LoadLibrary*`, caller-selected DLL,
alternate export, syscall stub, direct system call, fallback, or retry is
admitted.

The verifier bootstrap closure adds exactly one purpose-built native extension
named `s0_runtime_handle_guard_v0_3`. Its source, build recipe, compiler and
linker identity, binary, imports, origin, hash, and loaded-image identity are
profiled. It is not a general FFI surface. `ctypes`, `_ctypes`, generic native
loading, Python-level handle construction, and caller-provided extension
origins remain forbidden.

Its semantic Windows call surface is exactly `GetHandleInformation`,
`GetFileType`, `GetNamedPipeInfo`, `GetFileInformationByHandleEx`,
`GetProcessId`, `GetCurrentProcessId`, `QueryFullProcessImageNameW`,
`NtQueryObject`, `NtQueryInformationProcess`, `ReadFile`, and `CloseHandle`.
The normal Python-extension initialization imports and CRT support must be
enumerated separately in the platform profile. Any other semantic Windows API,
dynamic resolution, or syscall route rejects at binary review.

## 3. Atomic parent-relative output-root construction

### 3.1 Pre-root binding

Before any output mutation, the preloader binds:

- the retained authenticated output-parent directory handle and its volume
  serial and file identifier;
- one canonical ASCII output leaf containing no separator, colon, dot segment,
  alternate-data-stream syntax, trailing dot, trailing space, or case alias;
- local fixed NTFS, exact parent case, non-reparse parent ancestry, and the
  parent directory's per-directory case-sensitive flag equal to zero;
- the absence of every case-folding alias of that leaf relative to the retained
  parent handle; and
- a fresh 256-bit CNG nonce and the exact external pins.

This private preloader state is `PRE-ROOT-ABSENT`. It records an intended
parent/leaf relation and does not pretend that the absent leaf has an object
identity. If the leaf appears before the create call, `FILE_CREATE` must fail
with collision and the run rejects.

### 3.2 Sole admitted create call

The preloader creates the output root with exactly one direct
`ntdll.dll!NtCreateFile` call. Its frozen ABI is the Windows x64 ABI with the
following eleven arguments and no variadic or alternate prototype:

1. `PHANDLE FileHandle` points to preloader-owned zero-initialized storage;
2. `ACCESS_MASK DesiredAccess` is
   `FILE_LIST_DIRECTORY | FILE_READ_ATTRIBUTES | SYNCHRONIZE`;
3. `POBJECT_ATTRIBUTES ObjectAttributes` points to the exact structure below;
4. `PIO_STATUS_BLOCK IoStatusBlock` points to zero-initialized storage;
5. `PLARGE_INTEGER AllocationSize` is null;
6. `ULONG FileAttributes` is `FILE_ATTRIBUTE_DIRECTORY`;
7. `ULONG ShareAccess` is `FILE_SHARE_READ`;
8. `ULONG CreateDisposition` is `FILE_CREATE`;
9. `ULONG CreateOptions` is
   `FILE_DIRECTORY_FILE | FILE_SYNCHRONOUS_IO_NONALERT |
   FILE_OPEN_REPARSE_POINT`;
10. `PVOID EaBuffer` is null; and
11. `ULONG EaLength` is zero.

The exact `OBJECT_ATTRIBUTES` has:

- `Length = sizeof(OBJECT_ATTRIBUTES)` for the admitted x64 ABI;
- `RootDirectory` equal by live-handle identity to the retained output-parent
  handle;
- `ObjectName` pointing to one exact `UNICODE_STRING` containing only the
  canonical leaf, with a correct byte length and no terminating NUL counted;
- `Attributes = OBJ_CASE_INSENSITIVE | OBJ_DONT_REPARSE`;
- `SecurityDescriptor = NULL`; and
- `SecurityQualityOfService = NULL`.

Success requires a success `NTSTATUS`, a nonzero non-`INVALID_HANDLE_VALUE`
returned handle, `IoStatusBlock.Status` equal to the return status, and
`IoStatusBlock.Information = FILE_CREATED`. Any warning, collision, open of an
existing object, supersede, overwrite, reparse result, inconsistent status, or
unexpected information value rejects.

The required case-insensitive lookup is a collision defense, not permission to
accept an alias. Because the retained parent has case sensitivity disabled,
any concurrently inserted case-folding alias collides with `FILE_CREATE`; a
newly created object still must preserve and validate the exact supplied case.

There is no `CreateDirectory*`, pathname reopen, `OpenFile`, `CreateFile*`,
second `NtCreateFile`, alternate native API, case-insensitive retry, cleanup
and retry, or lock-after-create route.

### 3.3 Returned-handle validation and retention

Without closing or reopening the returned handle, the preloader validates:

- disk object and directory kind;
- local fixed NTFS volume;
- no reparse-point attribute or tag;
- exact canonical leaf case and containment under the retained parent object;
- volume serial and file identifier distinct from the parent and stable across
  two reads;
- one link, no alternate stream, and empty newly created directory state; and
- granted access, share disposition, and no delete-pending state consistent
  with the frozen call.

The same returned handle becomes the preloader's retained root authority and
remains open until verifier termination and the final preloader recheck. A
post-create pathname is evidence only; it can never replace handle identity.

The preloader creates one inheritable reduced-access duplicate of that exact
root object for the verifier. The duplicate has only directory-list,
read-attribute, and synchronize access. The preloader proves object equality
between original and duplicate before launch, places only the duplicate in the
explicit inherited-handle list, and closes its local duplicate immediately
after successful suspended verifier creation. The original retained handle is
never inherited.

## 4. Exact inherited-handle set and command-line locators

### 4.1 Five inherited handles

The verifier's `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` contains exactly, in this
semantic order:

1. admission-read pipe endpoint;
2. commit-request-write pipe endpoint;
3. commit-reply-read pipe endpoint;
4. reduced-access output-root directory handle; and
5. synchronize plus query-limited-information preloader process handle.

No authentication-file, parent-directory, preloader-retained-root, job,
verifier-process, candidate-process, opposite pipe end, network, console,
ambient standard, registry, token, section, or unrelated handle is inherited.
The exact three unidirectional pipe objects and all close/EOF rules from v0.2
remain authoritative.

### 4.2 Canonical non-authoritative locators

The preloader appends exactly these five arguments, in this order, after the
frozen Python flags and exact bootstrap path:

1. `--s0-admission-read=0xhhhhhhhhhhhhhhhh`
2. `--s0-commit-request-write=0xhhhhhhhhhhhhhhhh`
3. `--s0-commit-reply-read=0xhhhhhhhhhhhhhhhh`
4. `--s0-output-root=0xhhhhhhhhhhhhhhhh`
5. `--s0-preloader-process=0xhhhhhhhhhhhhhhhh`

Each `h` is one lowercase hexadecimal digit. The representation is exactly
`0x` plus sixteen digits, including leading zeroes. No uppercase, sign,
whitespace, decimal form, abbreviation, duplicate key, reordered key, extra
argument, response file, environment substitute, standard-handle mapping, or
alias is admitted. Each value must fit `uintptr_t`, be nonzero, differ from
`INVALID_HANDLE_VALUE`, and be distinct from every other value.

The arguments are generated only from the handles in the explicit handle list.
They are locators, not credentials. Their equality to a live integer or their
presence in `sys.argv` conveys no authority.

### 4.3 One-use native bind transaction

The minimal authenticated bootstrap parses the five strings without opening a
generic FFI surface and passes the five integers as one ordered tuple to
`s0_runtime_handle_guard_v0_3.bind_once_v3`. The extension has a
process-global first-call latch. The first call consumes the latch before any
validation; success and failure both make every later call fail. A failed call
closes all five located handles and returns no partial wrapper.

Inside one native transaction, before any Python-level endpoint, directory,
process wrapper, admission object, or candidate-visible object exists, the
guard validates:

- all five values are exact, distinct live handles carrying the expected
  inheritance flag, and the admission frame's ordered handle-list digest equals
  the authenticated preloader's exact five-entry construction;
- the first three objects are pipe objects, with the first and third admitting
  read but not write-data access and the second admitting write but not
  read-data access;
- all opposite ends are absent from the verifier, the pipe mode is the frozen
  byte-stream mode, and the endpoint close/EOF state is initial;
- the fourth object is the exact reduced-access directory object named in the
  admission frame, with stable volume/file identity, no write/delete access,
  no reparse state, and equality to the preloader's retained-root identity;
- the fifth object is a live process handle with synchronize and
  query-limited-information but no terminate, VM, duplicate, token, create, or
  write authority;
- the fifth handle's PID and queried image path equal the preloader PID and
  path carried by the exact admission frame;
- that same frame and nonce bind the CONTROL-authenticated preloader image file
  identity and hash from the runtime profile; the guard neither reopens nor
  self-hashes a pathname;
- `NtQueryInformationProcess(ProcessBasicInformation)` reports that the
  verifier's inherited parent PID equals the fifth handle's live PID, while the
  preserved v0.2 job evidence proves verifier membership and preloader
  nonmembership;
- the admission channel's sole writer and the commit channels' sole opposite
  owner are bound to that preloader launch by explicit-list construction,
  closed duplicate counts, the fresh nonce, exact PIDs, and the one-frame EOF
  protocol; and
- the current process PID and image equal the admitted verifier identity.

The guard natively reads and closes the admission-read endpoint, validates the
single admission frame and EOF, and only then returns one private,
nonconstructible `HandleBindingsV3` object containing private endpoint,
root-identity, preloader-process, and parsed-admission capsules. The type has no
public constructor, subclassing, copying, pickling, integer conversion,
attribute dictionary, or capsule export. Structural equality is irrelevant.

Before verifier-package import, the bootstrap replaces `sys.argv` with the
single exact bootstrap-path element, removes the guard module's public binding,
and verifies that the raw locator strings and integers are unreachable from
candidate inputs. The loaded extension remains pinned in `sys.modules` only
under its exact name; its consumed latch makes re-entry fail.

### 4.4 Exact admission-frame delta

The v0.1 canonical ASCII JSON, one-line final-LF, maximum-8,192-byte framing
remains authoritative, with schema ID
`S0-PUBLIC-ASSEMBLY-RUNTIME-ADMISSION-FRAME-3`. Relative to the effective v0.2
frame, v0.3 requires these additional or replaced bindings:

- preloader state exactly `ROOT-CREATED-HELD`;
- root volume serial and 128-bit file identifier from the sole returned
  `NtCreateFile` handle;
- output-parent volume serial and 128-bit file identifier;
- ordered semantic handle-list digest over the five role, object-kind, and
  access-policy descriptors;
- exact preloader and verifier PIDs and image identities;
- v0.1, v0.2, and v0.3 profile hashes and effective four-row package hash; and
- the existing fresh nonce and external-pin digest.

Keys are ASCII-sorted and unique; integers use canonical unsigned decimal;
hashes and identifiers use fixed-width lowercase hexadecimal; no pathname
replaces an object identifier. Numeric handle values and locator strings are
forbidden in the frame. The frame remains non-authoritative by value and is
accepted only through the exact endpoint/process/nonce transaction.

## 5. Admission, root, and commit state machines

### 5.1 Preloader state

The preloader root/launch states are:

1. `PRE-ROOT-ABSENT`;
2. `ROOT-CREATED-HELD`;
3. `VERIFIER-LAUNCHED`;
4. `COMMIT-REQUESTED`;
5. terminal `COMMIT-REPLIED` or terminal `FAILED`.

Only a successful sole `NtCreateFile` transaction advances
`PRE-ROOT-ABSENT` to `ROOT-CREATED-HELD`. Only successful suspended creation,
exact inherited-list verification, job assignment, and resume advance to
`VERIFIER-LAUNCHED`. The exact v0.2 commit request and reply protocol governs
the final two transitions.

### 5.2 Verifier runtime admission

The verifier receives no authority for an absent root. A successful native
bind transaction constructs the private runtime admission directly in
`ROOT-CREATED-BOUND`, binding the exact inherited root handle to the
preloader-retained root identity and admission frame.

The verifier admission states are exactly:

1. `ROOT-CREATED-BOUND`;
2. `COMMITTING`;
3. `COMMIT-ACKED`;
4. terminal `SPENT`; and
5. terminal `REJECTED`.

The v0.2 publication, commit, and live-consumer transition requirements remain
authoritative. An invalid transition attempted from any nonterminal state
atomically advances the admission to `REJECTED` before returning failure. An
attempt against `SPENT` or `REJECTED` rejects without changing that terminal
state. No terminal state may transition to itself as a successful operation,
to the other terminal state, or back to a nonterminal state.

The live witness and admission are both consumed on their first terminal
attempt. A terminal retry cannot create a second diagnostic authority, second
commit, second consumer result, or success upgrade.

## 6. Runtime-profile v0.3 supplement and package

The future platform-specific runtime package contains exactly four logical
rows, ASCII-sorted by virtual path:

1. `runtime-files.sha256`;
2. `runtime-profile-v0.1.json`;
3. `runtime-profile-v0.2.json`; and
4. `runtime-profile-v0.3.json`.

The v0.3 supplemental profile conforms to the supplied v0.3 schema and pins
the exact SHA-256 of both predecessor profile objects. It freezes:

- the five command-line locator names, order, representation, and scrub rule;
- the exact bootstrap-guard source and binary identities and one-use API;
- the five-handle inheritance policy and per-handle access predicates;
- the `NtCreateFile` direct import, ABI, constants, structure sizes, and call
  policy;
- exact `ntdll.dll` and relevant platform identities;
- root validation and duplicate-handle policy;
- terminal-state mutation policy; and
- the unchanged effective v0.2 process/job policy.

The runtime-files manifest includes every new source, object, library, PDB if
retained, extension, generated header, import library, build metadata, and
system image needed to reproduce or load the guard and preloader. Omission,
extra file, alias, duplicate virtual path, mutable external build input, or
predecessor hash mismatch rejects.

## 7. Failure routing and residue

Failure before the sole root-create call remains pre-output `AR-AUTH/0` when it
is an authentication failure and `AR-BOUNDARY/0` when it is a platform or
boundary failure.

Once `NtCreateFile` returns `FILE_CREATED`, the output root exists. Any later
preloader failure before verifier launch, handle binding, admission delivery,
verifier startup, or ordinary diagnostic routing is therefore
`AR-BOUNDARY/0` with a quarantined root. It must not be relabeled as clean
pre-output `AR-AUTH/0`.

After verifier admission, the frozen v0.5 diagnostic and routing precedence
applies. Any native guard failure is pre-import `AR-BOUNDARY/0`; no Python
exception may downgrade it. A root identity mismatch, locator mismatch,
unexpected handle, second bind, terminal retry, native status mismatch, or
fallback attempt is rejection, never success.

The preloader retains its root handle through verifier termination and final
recheck. Cleanup after handle release is diagnostic only and cannot upgrade
the run. No close-then-path-delete operation is rehearsal authority.

## 8. Required evidence before implementation consideration

A fresh independent design rereview must authenticate this exact package and
return no BLOCKING or MAJOR finding before implementation consideration may
reopen. That rereview must specifically challenge:

- locator discovery circularity and numeric-handle forgery;
- native guard origin, import surface, partial-return, and second-call routes;
- inherited-handle count, object type, access direction, and process binding;
- `NtCreateFile` ABI, status, relative-name, and reparse semantics;
- root replacement between absence observation, creation, validation, and
  verifier launch;
- root-handle duplication and retained-object equality;
- terminal retries from both terminal states; and
- every predecessor nonregression claim.

If design rereview passes, implementation still requires a separately opened
gate. A future implementation candidate must then receive source review,
binary/import review, mutation testing, and a bounded real-Windows platform
probe. In particular, the platform probe must prove that the retained root
handle permits the frozen assembly writes while preventing root substitution;
the design does not assume that result without evidence.

## 9. Closed claims

This revision establishes only a public design candidate. It does not claim
that the preloader, native guard, runtime package, handle protocol, atomic root
construction, assembly candidate, S0, central system, Project Brain
integration, operational safety, economic value, or model-to-model transfer
has been implemented or validated.
