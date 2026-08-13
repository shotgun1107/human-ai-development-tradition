# Public Assembly Runtime Profile + Neutral Preloader Acceptance Plan v0.3

Status: design-level acceptance obligations; not executed evidence

## 1. Purpose and gate order

This plan defines the evidence required to accept the v0.3 design corrections.
It does not authorize the implementation or execution of any item.

The gate order is:

1. authenticate the exact v0.3 design package;
2. complete a fresh independent design rereview;
3. only after a no-BLOCKING/no-MAJOR verdict, obtain a separate implementation
   gate;
4. authenticate source and build closure before compilation;
5. complete source, binary/import, and mutation review;
6. obtain a separate bounded platform-probe gate; and
7. only after the probe passes, reconsider an official public assembly
   rehearsal.

No later gate may be inferred from an earlier one.

## 2. Design-package acceptance

The design package passes authentication only if:

- every permitted Markdown file passes the canonical text-artifact validator
  and its exact sidecar;
- all JSON parses with duplicate-key rejection;
- the v0.3 schema passes direct Draft 2020-12 schema validation;
- every package-manifest row is ASCII-sorted, unique, hash-correct, and names
  exactly one logical artifact;
- the v0.2 design, interface map, package-manifest, and normalized independent
  rereview record pins reproduce exactly; and
- the reviewer reads no path outside the exact public allowlist.

A pin mismatch, unclassified file, boundary breach, parse ambiguity, or
validator failure makes the rereview invalid before semantic judgment.

## 3. Finding-closure matrix

| Finding | Required v0.3 evidence | Failure condition |
|---|---|---|
| `RPNP2-RR-001` | Exact five locator arguments, authenticated one-use guard, object/access/process/root validation, argv scrub, private wrappers | Any circular discovery, numeric authority, unvalidated wrapper, generic FFI, partial return, or retry |
| `RPNP2-RR-002` | One parent-relative `NtCreateFile` call returns the retained root handle; exact ABI and status; no reopen; targeted race mutation | Any create/open split, pathname rebound, alternate call, collision accepted, or different retained object |
| `RPNP2-RR-003` | Nonterminal invalid transition becomes `REJECTED`; terminal attempts fail without mutation | `SPENT` changes, `REJECTED` revives, or any terminal retry yields authority |

## 4. Future authenticated-build prerequisites

Before a future implementation is compiled, CONTROL must freeze and hash:

- complete preloader and bootstrap-guard source;
- all headers, generated headers, import libraries, compiler runtime inputs,
  build files, command lines, response files, environment, locale, and working
  directory;
- compiler, assembler, linker, signer disposition, and post-link tools;
- exact Windows SDK and WDK declarations used for `NtCreateFile`,
  `OBJECT_ATTRIBUTES`, `UNICODE_STRING`, and `IO_STATUS_BLOCK`;
- expected x64 structure sizes, field offsets, alignments, constants, and
  calling convention;
- exact PE direct and delay-import graph; and
- every produced binary, PDB if retained, manifest, and runtime dependency.

No network resolution, package repair, registry-derived tool selection,
ambient include/library path, or unmanifested generated input is permitted.

## 5. Handle-locator and native-guard evidence

### 5.1 Positive case

One positive probe must show that the preloader-generated exact command line
contains the frozen Python prefix followed by exactly five fixed-width
locators in order. The explicit handle list must contain the same five live
handles and no standard or opposite endpoint. The guard must consume the first
call, validate the five objects, read the single admission frame and EOF, and
return one exact private `HandleBindingsV3`. `sys.argv` must then contain only
the bootstrap path before verifier-package import.

### 5.2 Required locator mutations

Each of the following must reject before verifier-package import and return no
partial wrapper:

- one missing locator;
- one extra argument;
- reordered locators;
- duplicate key or duplicate numeric value;
- uppercase hexadecimal, decimal, signed, short, long, or whitespace form;
- zero or `INVALID_HANDLE_VALUE`;
- a closed, stale, pseudo, or noninherited handle;
- admission and reply handles swapped;
- wrong object type for any role;
- read/write direction reversed or both directions granted;
- a root file handle instead of a directory handle;
- a directory with write, delete, or reparse authority;
- a process handle with terminate, VM, duplicate, token, or write authority;
- a process handle for any process other than the exact preloader;
- mismatched preloader PID, image identity, or runtime-profile pin;
- a verifier parent PID different from the live preloader PID, wrong job
  membership, or preloader job membership;
- mismatched root volume/file identity;
- altered nonce, frame, length prefix, extra byte, missing EOF, or second frame;
- a fake, copied, subclassed, pickled, integer-derived, or structurally equal
  binding object;
- a second guard call after success; and
- a second guard call after first-call failure.

Every failure must consume the latch, close all located handles owned by the
failed transaction, emit no authority-bearing Python object, and route as
pre-import `AR-BOUNDARY/0` with quarantined-root residue.

### 5.3 Binary/import review

Static and loaded-image review must prove:

- one exported Python initialization symbol for the exact module name;
- one admitted callable API, `bind_once_v3`;
- no generic FFI, dynamic loader, shell, process creation, network, registry,
  environment lookup, alternate IPC, or arbitrary file-open surface;
- exactly the frozen semantic Windows call surface and no alternate query,
  wrapper, dynamic-resolution, or direct-syscall route;
- no unexpected delay import, forwarded import, API-set host, side-by-side
  activation, or writable executable mapping;
- exact native validation branches precede private-wrapper publication; and
- every failure path consumes the latch and closes without partial return.

## 6. Atomic root-construction evidence

### 6.1 Call and ABI audit

Source and disassembly review must prove exactly one reachable direct
`ntdll.dll!NtCreateFile` call for root creation and exact correspondence to the
interface-map ABI. The call must use the retained parent handle as
`RootDirectory`, a one-leaf case-sensitive `UNICODE_STRING`,
`OBJ_CASE_INSENSITIVE | OBJ_DONT_REPARSE`, a parent whose case-sensitive flag
is disabled, `FILE_CREATE`, the frozen desired access, share access,
attributes, create options, null allocation and EA arguments, and exact x64
structure sizes and offsets.

Any `CreateDirectory*`, `CreateFile*`, pathname reopen, second native call,
direct syscall, `GetProcAddress`, loader fallback, collision retry, or
close-and-reopen branch fails acceptance.

### 6.2 Status and object mutations

The following must reject:

- `NTSTATUS` warning, error, or success with inconsistent
  `IO_STATUS_BLOCK.Status`;
- information other than `FILE_CREATED`;
- null, zero, sentinel, closed, or wrong-type return handle;
- a preexisting leaf, case alias, reparse leaf, symlink, mount point, junction,
  ADS syntax, separator, trailing dot, or trailing space;
- remote, mapped, removable, non-NTFS, or wrong-volume parent;
- parent or root identity change;
- wrong exact leaf case or containment;
- a nonzero parent case-sensitive flag or a case-folding alias that does not
  cause collision;
- unstable file identity, link count other than one, alternate stream,
  delete-pending state, or nonempty returned directory;
- unexpected access/share mask; and
- returned-handle/duplicate-handle object inequality.

### 6.3 Targeted replacement-race mutation

An adversarial process with ordinary competing parent-directory rights must be
scheduled at every observable boundary between absent-leaf observation,
`NtCreateFile` entry, `NtCreateFile` return, post-call validation, suspended
verifier creation, guard binding, and verifier resume.

Acceptance requires one of only two results:

- the preloader retains the exact object it atomically created and every later
  identity check agrees; or
- the run rejects and never binds an attacker-created or replacement object.

No schedule may produce success with a different volume/file identity. The
test must explicitly demonstrate that there is no pathname reopen to target.

### 6.4 Usability and anti-substitution platform probe

On each admitted Windows build and exact runtime profile, a bounded probe must
show both:

- the retained no-share-write/no-share-delete root handle and its inherited
  reduced-access duplicate permit the frozen candidate/verifier output writes,
  reservations, observations, and publications; and
- the same retained identity prevents deletion, rename, reparse substitution,
  or root replacement for the full verifier lifetime.

If both properties cannot coexist with the frozen share/access policy, the
design returns to revision. The probe may not silently relax flags.

## 7. State-machine mutations

For each verifier admission state, test every named valid transition and every
other attempted transition. Required outcomes are:

- invalid transition from `ROOT-CREATED-BOUND`, `COMMITTING`, or
  `COMMIT-ACKED`: atomically enter `REJECTED`, consume applicable witness on a
  terminal attempt, and fail;
- any attempt from `SPENT`: remain `SPENT` and fail;
- any attempt from `REJECTED`: remain `REJECTED` and fail; and
- no concurrent pair of attempts produces two commits, two consumer results,
  two diagnostics with authority, or any terminal-to-nonterminal state.

The same immutability rule must be checked for preloader terminal states
`COMMIT-REPLIED` and `FAILED`.

## 8. Nonregression evidence

The future evidence set must also reproduce every applicable v0.1 and v0.2
test, including:

- three one-way channels and exact frame/EOF ordering;
- `COMMIT-ACKED` before live-consumer evaluation;
- exact process/job counting domains and two job members;
- runtime package exact-set and predecessor pins;
- retained runtime, workspace, parent, root, preloader, verifier, and candidate
  identities;
- exact environment, flags, `sys.path`, import origins, loaded-PE set, and
  denial latch;
- candidate transport count of zero or one and no provider/network/model call;
- receipt-v2 byte identity and exact publication semantics; and
- closed claims and failure-routing precedence.

## 9. Acceptance threshold

Design acceptance requires a valid fresh independent rereview with:

- BLOCKING: 0;
- MAJOR: 0; and
- an explicit statement that all three v0.2 findings are closed without
  regression.

MINOR findings require an explicit CONTROL disposition before implementation
consideration. A design PASS is only permission to consider opening the next
gate; it is not implementation or rehearsal evidence.
