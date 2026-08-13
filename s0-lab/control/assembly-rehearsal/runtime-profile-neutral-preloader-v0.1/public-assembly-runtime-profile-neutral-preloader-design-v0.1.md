# S0 v0.14 public assembly runtime profile and neutral preloader design v0.1

- `status`: public design candidate; fresh independent rereview required
- `gate`: `PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN v0.1`
- `scope`: close the runtime-closure and pre-import-authentication blockers only
- `effective_predecessor`: v0.3 plus v0.4 replacements plus v0.5 replacements
- `predecessor_base_commit`: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- `predecessor_base_tree`: `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- `predecessor_implementation_manifest_sha256`: `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623`
- `predecessor_implementation_report_sha256`: `520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005`
- `v0_5_design_package_manifest_sha256`: `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802`
- `v0_5_independent_rereview_sha256`: `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137`
- `implementation_status`: not implemented by this gate
- `platform_probe_status`: not executed
- `official_rehearsal_status`: not executed
- `F0_content_access`: none

## 1. Decision and replacement boundary

This design adds one conjunctive launch authority to the effective v0.5
assembly design. It does not replace or weaken any v0.3, v0.4, or v0.5
controller, observer, receipt, witness, live-consumer, failure-routing, or
nonclaim rule.

The predecessor implementation candidate correctly fails closed because the
effective design does not yet authenticate:

- the exact Python executable and `python312.dll`;
- standard-library source, frozen, built-in, and extension-module origins;
- `jsonschema` and every transitive dependency;
- private dependency DLLs and admitted system DLLs;
- the verifier bootstrap before verifier import;
- launch flags, environment, `sys.path`, module origins, and audit-event
  normalization; or
- the executable that performs those checks before Python starts.

This v0.1 design closes those omissions at design-text and schema level. It
does not claim that a runtime profile, preloader, executable, runtime
admission, platform probe, or rehearsal has been implemented or validated.

## 2. Threat model and maximum claim

The design must reject all of the following before output-root creation:

- a caller-selected or substituted Python executable;
- a version-only `jsonschema` check or caller-controlled dependency path;
- an unpinned `.py`, `.pyc`, `.pyd`, DLL, package metadata file, bootstrap, or
  verifier source;
- an extra, missing, duplicated, path-escaping, reparse-backed,
  alternate-stream, multiply linked, or hash-mismatched admitted file;
- mutation or replacement of an admitted file after authentication;
- environment, current-directory, `PATH`, `PYTHONPATH`, `PYTHONHOME`, site,
  user-site, bytecode-cache, or DLL-search injection;
- copied admission bytes without the live preloader process, exact inherited
  handles, job binding, and one-use verifier object;
- preloader death followed by continued verifier or candidate execution; and
- self-selected pins or self-hashing after the authority-bearing code already
  executed.

The claim remains bounded to ordinary process interruption and API failure on
the supported Windows profile. It excludes a malicious kernel, administrator,
firmware, hardware, debugger with equivalent privilege, power-loss durability,
kernel-crash durability, directory-metadata durability, and protection against
an actor that can replace the running preloader process or modify its memory.

The authenticated Windows kernel and CONTROL launcher are the external trust
base for this design. Their own implementation integrity is not established by
the assembly result. CONTROL must authenticate the preloader from an open
no-reparse file handle held without share-write or share-delete, create the
preloader suspended from that locked path, compare the child image identity to
the retained file identity, and resume only after equality. Hashing a path,
closing it, and later launching the same path is not sufficient.

## 3. Authority graph and bootstrap rule

The authority chain is strictly ordered:

1. CONTROL independently authenticates the neutral-preloader implementation
   manifest, exact native executable, and approving independent implementation
   review from externally supplied lowercase SHA-256 pins.
2. Only after step 1 may CONTROL execute the preloader and provide the exact
   canonical launch envelope.
3. The preloader authenticates and retains locks on the runtime-profile
   package, complete runtime file closure, assembly implementation manifest and
   rows, current runtime-design package and approving review, current assembly
   design authorities, and required public assembly inputs.
4. The preloader completes platform, path, file-identity, PE-import,
   environment, output-parent, and process-construction preflight.
5. Only then may it create the exact Python verifier process suspended, assign
   it to the kill-on-close job, restrict inherited handles, and resume it.
6. The verifier bootstrap validates the inherited admission channel, parent
   process handle, job membership, exact config, runtime module origins,
   `sys.path`, launch flags, environment, and audit policy before importing the
   verifier package.
7. Only an exact private runtime-admission object created by that bootstrap may
   accompany the existing observer witness into the same-process live
   consumer.

The preloader cannot authenticate itself by hashing itself after entry. Such a
self-hash is diagnostic only. The external step-1 authentication is mandatory
and cannot be replaced by a command-line value, environment value, profile
field, report, or preloader assertion.

The external CONTROL launcher is a declared trust root rather than another
artifact recursively authenticated by the preloader. A future implementation
review must observe or reproduce its locked-handle, suspended-creation, child-
image-identity, and resume sequence. If CONTROL cannot supply that exact
sequence from its trusted host, the run stops before preloader entry.

## 4. Neutral-preloader implementation profile

The future preloader is one 64-bit native Windows PE executable. It must not
depend on Python, PowerShell, the CLR, WSH, a shell, a package manager, a
network client, or an ambient scripting runtime. Its implementation manifest
must include the exact executable, source, build instructions, static and
binary audits, and tests. A fresh reviewer must reproduce or otherwise
independently establish the source-to-binary correspondence before approving
the executable pin.

The executable must:

- use fixed Win32 wide-character APIs and CNG SHA-256;
- statically link non-OS runtime support;
- have a frozen PE machine type, subsystem, import table, section inventory,
  and entry point;
- resolve no DLL through `PATH`, the current directory, user directories,
  registry app paths, plugins, or delay-loaded fallbacks;
- perform no network access, download, package discovery, update, repair,
  retry, or fallback;
- accept exactly one canonical ASCII JSON launch envelope over one
  CONTROL-owned inherited pipe or an equivalently authenticated handle, never
  from ambient stdin, a file selected from the workspace, or environment; and
- emit only bounded canonical status frames without input contents, secrets,
  paths outside the public envelope, or authority-bearing objects.

The default maximum PE import set is `kernel32.dll` and `bcrypt.dll`. Any
additional direct import requires a design revision and a new independent
review. OS transitive dependencies remain part of the runtime profile and are
not trusted merely because they reside under `System32`.

## 5. Runtime-profile package

The future public runtime-profile package contains exactly:

1. `runtime-profile-v0.1.json`, conforming to the supplied schema;
2. `runtime-files.sha256`, the exact private-runtime and admitted-system-file
   closure; and
3. `runtime-profile-package-files.sha256`, a two-row manifest over items 1 and
   2 whose SHA-256 is supplied externally.

The package manifest and runtime-file manifest use lowercase SHA-256, two
ASCII spaces, one safe virtual path, and LF. They are UTF-8 without BOM or CR,
sorted by path, unique, final-LF terminated, and bounded. The package manifest
has exactly two rows. The runtime-file manifest permits only the virtual roots
`runtime/` and `system32/`.

The profile JSON independently records, for every runtime file, the virtual
root, exact logical path, SHA-256, byte length, and class. Its file inventory
must equal the manifest row set and hashes exactly. It also freezes:

- exact CPython `3.12.x` patch version and 64-bit executable;
- Python DLL, standard library, extension modules, package metadata,
  `jsonschema`, transitive dependencies, private dependency DLLs, and admitted
  OS dependencies;
- every module name, origin kind, loader, path or built-in/frozen identity,
  hash when file-backed, and preload phase;
- every PE dependency name, source image, resolution root, resolution kind,
  load phase, destination file, and hash;
- exact `sys.path`, launch flags, environment names, audit-policy ID, and
  fixed resource limits; and
- exact runtime-root and system-root interpretation.

Each PE edge is classified as one of `application-directory-file`,
`system32-file`, `api-set-to-system32-host`, or `known-dll-system32`, and as a
static import, delay import, or profiled dynamic load. API-set contract names
and their expected host images are both recorded. DLL redirection files, SxS
dependency redirection, packaged dependency graphs, registry app paths,
unprofiled `LoadLibrary`/`GetProcAddress`, Windows-directory fallback,
current-directory fallback, and `PATH` resolution reject. The complete
transitive graph is authenticated before launch, and the loaded-PE inventory is
rechecked after each frozen preload phase.

An installed version string, wheel metadata, package-record file, executable
version resource, Authenticode signature, or directory name is never a
substitute for the complete file closure and external package-manifest pin.

## 6. Canonical path and file authentication

Manifest logical paths are ASCII forward-slash paths. Empty segments, `.` or
`..`, backslash, colon, NUL, absolute paths, UNC paths, device paths, volume
GUID paths, reserved DOS device segments, and segments ending in dot or space
reject. Every on-disk component must reproduce the manifest component's exact
ASCII case.

Externally supplied roots must be absolute local drive-letter paths. The
preloader converts them to extended-length form only after validation. It
walks every component without following reparse points, rejects junctions,
symlinks and all reparse tags, and compares the handle-derived final path,
volume serial, file index, and expected root containment.

Every admitted file must be a regular single-link file with exactly one
unnamed `::$DATA` stream. The preloader opens it without following reparse
points, with no share-write or share-delete permission, hashes the already
opened handle, verifies byte length and identity before and after hashing, and
retains the handle until the verifier process exits. A changed identity,
short read, extra stream, link count other than one, or sharing failure is
`AR-AUTH/0`.

The preloader enumerates the private runtime root before launch and again at
runtime-admission commit. Its exact regular-file set must equal the
`runtime/` manifest rows; no bytecode cache, unlisted DLL, package metadata,
temporary file, or other extra file is allowed. System32 is not treated as an
exact-set root; only the explicitly admitted `system32/` rows are opened,
hashed, identity-bound, and locked.

## 7. Launch construction and lifetime

After all authentication succeeds, the preloader:

1. validates one existing non-reparse local fixed-NTFS output parent and one
   exact absent ASCII run leaf without creating the leaf;
2. creates one job object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` and no
   breakaway permission;
3. creates separate admission and liveness anonymous-pipe pairs;
4. constructs an explicit three-key environment containing only
   `SYSTEMDRIVE`, `SYSTEMROOT`, and `WINDIR`, with values derived from the
   authenticated system root;
5. uses the exact runtime-profile Python executable, exact verifier-bootstrap
   source, the authenticated runtime root as `lpCurrentDirectory`, and arguments
   `-I -S -B -X utf8` in that exact order;
6. creates the verifier with `CREATE_SUSPENDED` and an explicit
   `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` containing only the verifier ends of the
   two pipes and one synchronize-only preloader process handle;
7. assigns the verifier to the job before resuming its first thread; and
8. retains every authentication handle, pipe, job, and verifier process handle
   until verifier termination.

The environment contains no `PATH`, `PYTHONPATH`, `PYTHONHOME`, `PYTHONUSERBASE`,
`PYTHONSTARTUP`, `PYTHONINSPECT`, `PYTHONDONTWRITEBYTECODE`, temp variable, proxy,
provider credential, or inherited caller entry. `-I` does not excuse an
incorrect environment; both predicates are required.

If the preloader exits or its job handle closes, the verifier and every
descendant candidate process terminate. The verifier must not be able to use
breakaway creation flags. A verifier that is not in the exact job, has an
unexpected parent/image/process identity, or inherits an extra handle rejects
before verifier import.

## 8. Verifier bootstrap and module closure

The exact verifier bootstrap is a separately named assembly-implementation
file and is not the verifier package initializer. Python startup may execute
only the runtime-profile startup closure before it. The bootstrap then:

- reads exactly one bounded canonical admission frame from the inherited pipe;
- binds the frame to the live preloader process handle, exact verifier PID,
  job, pipe identities, external pins, roots, output leaf, and a fresh
  CNG-generated 32-byte nonce;
- verifies `sys.executable`, implementation name and version, pointer width,
  flags, `sys.path`, environment, bytecode-disabled state, and absence of site
  and user-site activation;
- preloads the exact profile module closure with source-only loading for
  file-backed Python modules and exact extension loading for admitted `.pyd`
  origins;
- requires every `sys.modules` entry to equal one admitted built-in, frozen,
  source, or extension origin and rejects every extra or changed origin;
- verifies the loaded PE/DLL origin and hash inventory against the profile;
- rejects any loaded PE edge whose resolution kind, contract-to-host mapping,
  load phase, or target differs from the preauthenticated transitive graph;
- installs the exact sensitive-event audit policy and source/open sentinel;
  and
- creates one private process-local `RuntimeAdmission` by identity before
  importing the verifier package.

The bootstrap cannot accept an arbitrary dependency root, executable,
`sys.path` entry, loader, module origin, package version, `.pyc`, zip import,
namespace package, editable install, `.pth`, site customization, or user
customization.

The verifier launches the candidate child only with the executable, profile,
environment, flags, and bootstrap supplied by the private admission. Public
API parameters cannot override them.

## 9. Exact sensitive-event policy

The runtime profile includes an exact audit-policy ID and policy object.
Candidate execution applies explicit allowlists to sensitive event families
and denies unknown events under those families by default.

At minimum, the policy treats these as sensitive:

- `open`, `import`, `os.*`, `socket.*`, `subprocess.*`, `ctypes.*`,
  `winreg.*`, `marshal.*`, and dynamic-code events;
- process, network, provider, FFI, registry, DLL-directory, environment,
  rename, replace, link, symlink, permission, truncate, and start-file
  operations; and
- verifier, observer, witness, runtime-admission, `_winapi`, `_ctypes`, socket,
  subprocess, multiprocessing, provider SDK, and network-library imports.

Reads are allowed only for the exact authenticated public file set and exact
owned pending outputs. Directory metadata traversal is limited to the exact
public-bundle root and exact output root. Writes are limited to the two pending
files. Cleanup may remove only the four exact owned output names and may
enumerate only the exact output root. Publication moves remain verifier-parent
owned. A first denial latches; later substantive operations cannot recover by
catching the exception.

Every event path uses the same ASCII-rooted normalization and output-root
identity supplied by the runtime admission. File descriptors, relative paths,
unrecognized path-like objects, alternate path spellings, and unnormalized
arguments reject unless an exact policy row expressly admits the descriptor.

## 10. Runtime-admission protocol

Admission bytes are public diagnostics and do not create authority by value.
The preloader-to-verifier frame is one canonical ASCII JSON line of at most
8,192 bytes. It contains the exact public pins, preloader and verifier PIDs,
runtime and workspace root identities, output-parent identity, run leaf,
nonce, profile ID, launch-policy ID, job-policy ID, and schema ID.

The verifier's private `RuntimeAdmission` has no public constructor,
serializer, byte representation, copy operation, value equality, or
candidate-visible token. It binds by object identity to:

- the exact admission and liveness pipe endpoints;
- the live preloader process handle and image identity;
- the exact verifier process, job, nonce, and roots;
- every external pin and retained-handle inventory digest; and
- one unspent terminal state protected by a lock.

Immediately before live-consumer evaluation, the verifier writes exactly
`RUNTIME_ADMISSION_COMMIT\n` to the private liveness pipe. The preloader
rechecks that it still owns the exact job, verifier, roots, and all locked file
identities, repeats the private-runtime exact-set enumeration, and replies
exactly `OK\n`. Any EOF, timeout, extra byte, changed identity, changed set,
wrong process, wrong job, or second commit is terminal failure.

The live consumer atomically spends both the runtime admission and existing
publication witness on the first terminal attempt. Repairing files, restarting
a preloader, copying the admission frame, or changing arguments cannot turn a
rejection into acceptance.

## 11. Receipt compatibility and success authority

The candidate-produced receipt-v2 remains exactly the v0.5 21-field object.
This supplement does not add a candidate-visible runtime pin, serialize the
runtime admission, or make the receipt a proof of process ancestry.

The future assembly implementation-manifest pin will change when the verifier
bootstrap and runtime-admission integration are implemented. Before any live
execution, CONTROL must externally freeze that new pin and reconstruct the
exact 1,173-byte receipt-v2 and its SHA-256. The current predecessor pin and
receipt hash are not live-execution authorities.

Rehearsal PASS requires one same-process atomic decision satisfying both:

1. the complete existing v0.5 publication witness and current-file predicate;
   and
2. the complete live runtime-admission predicate defined here.

Neither object alone is sufficient. After verifier exit, the admission,
witness, and PASS authority cease to exist. Files, manifests, receipt, trace
summaries, and reports remain `offline-not-success-diagnostic-only`.

## 12. Failure routing

Manifest, pin, preloader, platform, path, runtime-file, PE, environment,
profile, executable, job, handle, config, module-origin, or verifier-bootstrap
defects found before output-leaf creation are `AR-AUTH/0` and cannot launch the
candidate.

Loss of the preloader, retained locks, job, admission pipe, liveness pipe,
runtime set, or module-origin invariant after verifier launch is terminal
`AR-BOUNDARY` with the actual observed transport call count `0` or `1`. If the
output leaf was created, it is non-success and cleaned or quarantined under the
retained v0.3 rule. Process termination without an authenticated diagnostic is
still not success.

Publication observer, move, witness, or live-consumer failures remain
`AR-RECORD/1`. No runtime failure may be relabeled as a record success, and no
cleanup outcome may replace the first primary class.

## 13. Independence and review order

The runtime-profile author, neutral-preloader implementer, independent design
reviewer, independent implementation reviewer, and platform-probe operator are
separate roles. A fresh independent design rereviewer receives only the exact
public allowlist in the accompanying brief. Passing this design review opens
only implementation consideration.

Before a platform probe, a fresh implementation reviewer must authenticate:

- this design-package manifest and approving design-review hash;
- the actual runtime-profile package and approving profile review;
- the neutral-preloader implementation manifest, exact executable, and
  approving implementation review;
- the updated assembly implementation manifest and approving implementation
  review; and
- every retained v0.5 authority.

No author review, self-hash, prior conversation, report assertion, mock,
in-memory substitute, or worktree separation satisfies independence.

## 14. Closed boundaries and exact next gate

This gate does not authorize implementation, compilation, runtime-profile
materialization, dependency installation, neutral-preloader execution,
platform probe, real `MoveFileExW`, official rehearsal, F0 content, hidden
oracle, provider/model/network, executor, judge, scoring, S0, E0, central
system, Project Brain, commit, push, PR, release, or `main` integration.

The exact next gate is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.1 INDEPENDENT REREVIEW OPEN`

Only a fresh `PASS-FOR-PUBLIC-RUNTIME-PROFILE-AND-PRELOADER-IMPLEMENTATION-CONSIDERATION-ONLY`
verdict may permit CONTROL to consider a later implementation gate.
