# S0 v0.14 public assembly runtime profile and neutral preloader acceptance plan v0.1

## 1. Status and claim boundary

This is a public, design-only acceptance plan. It defines evidence that a future runtime-profile package, native neutral preloader, verifier bootstrap, and revised assembly candidate would have to produce before CONTROL could consider a public end-to-end rehearsal.

This document is not evidence that any such implementation exists or works. No runtime profile is materialized, no preloader is compiled, no platform probe is performed, and no official rehearsal is opened by this package.

The effective predecessor remains v0.3 plus the v0.4 replacements plus the v0.5 replacements. The runtime-profile and neutral-preloader design is conjunctive authority: it does not weaken any predecessor invariant.

## 2. Evidence order

Acceptance is fail-closed and ordered. Evidence from a later stage cannot repair a failure in an earlier stage.

1. Authenticate the approved design package and its independent rereview.
2. Authenticate the neutral-preloader source/binary package and its independent review.
3. Authenticate the runtime-profile package and its independent review.
4. Authenticate the revised public assembly implementation package and its independent review.
5. Run static and synthetic rejection tests without invoking the real publication primitive.
6. Run the separately authorized real-platform probe.
7. Only under a later explicit gate, run exactly the bounded public rehearsal specified by the then-approved protocol.

Passing this plan may support implementation or rehearsal consideration only. It cannot establish S0, E0, central-system, Project Brain, operational-safety, economic-value, or model-transfer claims.

## 3. Design-package acceptance

The design package passes its author-side integrity check only if all of the following hold:

- each logical artifact is UTF-8 without BOM, has a final LF, and has no trailing whitespace;
- every same-basename SHA-256 sidecar is exact and names only its basename;
- `design-package-files.sha256` contains exactly the six logical artifacts named by this package, sorted by ASCII basename, with no self-row and no sidecar rows;
- both JSON Schemas pass Draft 2020-12 metaschema validation;
- the interface map parses with duplicate-key rejection;
- the design, interface map, and acceptance plan agree on the exact next gate and closed boundaries; the schemas open no gate, and the rereview brief is limited to that exact review gate;
- the predecessor pins equal the authenticated public artifacts used by CONTROL.

An author-side check is not an independent review verdict.

## 4. External preloader authentication

The future implementation cannot execute the neutral preloader until an external CONTROL mechanism has authenticated its exact binary package. Acceptance evidence must identify that mechanism and demonstrate that it does not execute the candidate binary, load candidate-controlled code, or trust a self-reported hash before authentication completes.

The CONTROL launcher is the declared external trust base. It must authenticate from a no-reparse file handle held without share-write or share-delete, create the preloader suspended while retaining that handle, compare the child image identity with the retained file identity, and resume only after equality. A hash-then-close-then-path-launch sequence fails this requirement.

Required rejection cases include:

- binary bit mutation;
- source-to-binary manifest mutation;
- substituted binary with the expected filename;
- a binary that prints its own expected hash;
- an unreviewed rebuild with identical version metadata;
- an alternate launcher, interpreter, PowerShell, CLR, shell, script host, or DLL search path;
- any caller-provided executable override.

The future review must inspect the compiled PE import table, delay imports, embedded resources, signatures if present, compiler and linker settings, and source-to-binary correspondence. Version strings and Authenticode status may be supplemental evidence only.

## 5. Runtime-profile package acceptance

The future runtime profile must conform to `runtime-profile-v0.1.schema.json` and to the stricter semantic rules in the design. Schema validity alone is insufficient.

CONTROL must demonstrate all of the following:

- the package manifest authenticates exactly `runtime-profile-v0.1.json` and `runtime-files.sha256`;
- the JSON file inventory and text manifest are equal after canonical parsing;
- the private `runtime/` tree has an exact file set with no extra, missing, ignored, or alternate-stream objects;
- each admitted `system32/` dependency is explicitly named and hashed;
- all Python, extension-module, third-party, package-metadata, and dependent-DLL bytes needed by the admitted execution are represented;
- module names, loaders, origins, preload phases, and hashes are mutually consistent;
- every PE dependency has an unambiguous resolution root and an authenticated target;
- every PE edge freezes its resolution kind, static/delay/profiled-dynamic origin, load phase, API-set contract-to-host mapping where applicable, and target hash;
- DLL redirection, SxS redirection, packaged graphs, registry app paths, unprofiled dynamic loads, Windows-directory fallback, current-directory fallback, and `PATH` resolution are absent;
- no package discovery, version-only check, online resolution, repair, download, or dependency fallback is possible.

Required mutations include one-at-a-time changes to every scalar field, deletion and duplication of rows, row reordering where order is authoritative, extra files, hard links, alternate streams, reparse points, case aliases, reserved device names, traversal segments, drive substitutions, and System32 dependency substitutions.

## 6. Path and file-object acceptance

Path acceptance must be tested against object identity, not only string normalization.

Positive evidence must show:

- all virtual paths are canonical ASCII forward-slash paths;
- all physical roots are absolute local drive-letter paths on a fixed NTFS volume;
- exact component case is checked against directory entries;
- each admitted file is opened without following reparse points and without share-write or share-delete;
- the opened object is a regular single-link file with only the unnamed data stream;
- SHA-256 is computed from the retained handle;
- pre/post identity and length are equal;
- retained handles survive until verifier exit;
- the private runtime exact set is rechecked immediately before admission commit.

Mandatory negative cases include UNC, device paths, volume GUID paths, alternate streams, junctions, symbolic links, mount points, hard links, case-only aliases, trailing dot or space, `.` or `..`, empty segments, absolute manifest rows, backslashes, colons, NUL, and path replacement after initial authentication.

## 7. Native preloader behavior acceptance

The neutral preloader must have one deterministic path and no repair path. Static inspection and instrumented tests must establish:

- native Win64 PE execution only;
- no Python, PowerShell, CLR, shell, network, package manager, registry discovery, dynamic code loading, or child fallback;
- only the approved direct and delay-loaded imports;
- CNG SHA-256 is the only hash primitive used for authority decisions;
- exactly one profile/package authentication path;
- exactly one suspended verifier creation path;
- job assignment and handle-list construction occur before resume;
- no retry after any authentication, creation, assignment, resume, pipe, or commit failure;
- no success return can bypass the final identity and exact-set rechecks.

Mutation testing must remove or invert each failure branch, replace each exact comparison with a prefix or case-insensitive comparison, alter each Win32 flag, add an inherited handle, permit breakaway, add a fallback executable, and bypass the retained-handle inventory. Each mutant must be killed by a precommitted test.

PE-resolution mutations must substitute an API-set host, treat a KnownDLL as an arbitrary path file, introduce a redirection or SxS edge, move a dependency between application and System32 roots, alter a load phase, add `LoadLibrary`/`GetProcAddress`, and exploit current-directory, Windows-directory, or `PATH` fallback. Each mutation must reject before candidate import.

## 8. Launch, process, and lifetime acceptance

The launch envelope must conform to `neutral-preloader-launch-envelope-v0.1.schema.json` and the semantic design. The envelope is input, not authority; every pin and path is independently authenticated.

Required evidence includes:

- exact CPython 3.12.x, 64-bit, Windows 10/11, fixed local NTFS profile;
- exact argument order `-I -S -B -X utf8` followed by the authenticated verifier-bootstrap path;
- `lpCurrentDirectory` exactly equals the authenticated runtime root;
- an explicit environment containing only `SYSTEMDRIVE`, `SYSTEMROOT`, and `WINDIR` in the frozen order;
- no caller environment inheritance, Python override, dependency root, current-directory discovery, or user-site influence;
- `CREATE_SUSPENDED`, an explicit inherited-handle list, and assignment to a kill-on-close job before resume;
- no breakaway and no inheritable authentication-file handles;
- authenticated admission and liveness pipes;
- verifier termination and no success if the preloader dies, its process handle changes, a liveness pipe closes, or job membership changes.

The test suite must distinguish verifier failure, preloader failure, timeout, IPC truncation, extra IPC, child stdout/stderr, process-tree escape, and unclassified process death.

## 9. Verifier-bootstrap acceptance

The verifier bootstrap must be a separately authenticated source file and must not import the verifier package before runtime admission is established.

Before the verifier import, tests must prove exact checks for:

- canonical admission-frame bytes and maximum size;
- live preloader identity and expected image;
- exact parent/verifier process identities and job membership;
- every external lowercase SHA-256 pin;
- workspace, runtime, system, and output-root identities;
- `sys.executable`, CPython version, pointer width, launch flags, environment, and `sys.path`;
- every already-loaded Python module origin, loader, and hash;
- every loaded PE module origin and hash;
- successful installation of the sensitive-event audit policy.

Then, and only then, the authenticated verifier package may be imported through source-only file-backed loading. Bytecode, zip import, namespace packages, editable installs, `.pth`, site, user site, ambient package metadata, and import-origin drift must be rejected.

## 10. Sensitive-event policy acceptance

The audit policy must be tested at both the Python audit-hook layer and the lower-level capability layer exposed by the admitted runtime closure. Merely registering an audit hook is insufficient.

For each sensitive family in the interface map, tests must cover:

- one allowed event with exact normalized arguments;
- near-match path and argument rejection;
- direct low-level invocation;
- cached or preloaded capability invocation;
- import-hook replacement attempts;
- caught exceptions followed by continued execution;
- first-denial latching across every later stage boundary.

Cleanup exceptions are limited to the exact four owned output names and exact output-root enumeration. They must not authorize broader delete, rename, link, stream, metadata, or directory traversal operations.

## 11. Runtime admission and commit acceptance

`RuntimeAdmission` is process-local authority and must not be forgeable by constructing a value with matching fields.

Required positive evidence:

- a private constructor issues exactly one admission for the live process;
- identity equality, not structural equality, controls acceptance;
- the admission binds both pipes, the preloader handle and image, verifier process and job, nonce, roots, external pins, and retained-handle digest;
- the verifier sends exactly `RUNTIME_ADMISSION_COMMIT\n` once;
- the preloader performs all frozen rechecks and replies exactly `OK\n` once;
- the admission is spent on the first terminal attempt.

Required rejection cases include copied fields, JSON replay, pickle/copy/deepcopy, subclassing, public constructor, monkeypatching, stale nonce, wrong pipe, wrong process, wrong job, wrong image, wrong roots, wrong pin, wrong digest, second commit, extra bytes, reordered messages, early preloader reply, preloader death, and caught commit failure followed by retry.

## 12. Assembly integration acceptance

The existing v0.5 publication witness remains necessary but becomes insufficient by itself. The live consumer must atomically validate and spend both the exact v0.5 witness and exact live `RuntimeAdmission` on the first terminal attempt.

Tests must reject:

- witness without runtime admission;
- runtime admission without witness;
- authorities from different runs;
- a fabricated `LiveDecision` or equivalent return value;
- either authority reused after a rejected attempt;
- post-process status treated as success authority;
- a second invoke, second publication, second consumer call, or second commit.

The 21-field receipt-v2 wire form remains unchanged. The future revised implementation package and its exact receipt bytes/hash must nevertheless be newly pinned because runtime authority and implementation bytes change.

## 13. Failure-routing acceptance

Every injected single fault must produce one terminal, canonical result:

- runtime/preloader authentication defect before output mutation: `AR-AUTH/0`;
- preloader, retained lock, job, pipe, or runtime-origin loss after launch: `AR-BOUNDARY/observed-0-or-1`;
- publication, observer, move, witness, or consumer defect: `AR-RECORD/1`;
- process death without an authenticated canonical diagnostic: not success.

No test may infer PASS from exit code, a public dataclass, output-file presence alone, stdout, stderr, or a self-authored report. Cleanup status and quarantine status remain diagnostic and cannot upgrade a failure.

## 14. Real-platform probe separation

The real-platform probe is a later, separately authorized activity. It must use the exact reviewed binary and profile package on the admitted Windows/NTFS platform, with network disabled and without provider/model/F0 inputs.

Probe evidence must cover actual file identity, stream enumeration, link count, reparse rejection, CNG hashing, PE/DLL resolution, suspended creation, explicit handle inheritance, job kill-on-close, liveness, and the exact commit handshake. Probe evidence cannot substitute for source review, mutation testing, or independent review.

## 15. Verdicts and next gate

Author-side validation may report only `AUTHOR-CHECK-COMPLETE` or `AUTHOR-CHECK-FAILED`.

The independent design reviewer may report only the verdict vocabulary frozen in the rereview brief. A passing design review opens consideration of a bounded public implementation gate; it does not itself open implementation.

The exact next gate is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.1 INDEPENDENT REREVIEW OPEN`
