# S0 v0.14 public assembly runtime profile and neutral preloader design revision v0.2

- `status`: public design revision candidate; fresh independent rereview required
- `gate`: `PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN v0.2`
- `scope`: close exactly `RPNP-RR-001`, `RPNP-RR-002`, and `RPNP-RR-003`
- `effective_predecessor`: v0.1 plus the replacements in this document
- `base_commit`: `da4ad3af483652bd755deff9d024a9833c177d39`
- `base_tree`: `e5ad06934a9864b4c5665852e0097f3885d2d277`
- `v0_1_design_package_manifest_sha256`: `13b69bfd8614ea57e49d317902e9563bd8a47eaa13a06be22065f81177b29cad`
- `v0_1_review_result_record_sha256`: `e1423b6d61c95407eeb34f03ba5dacdd372fb4fbbd500c4734af8f3df424eb29`
- `implementation_status`: not implemented by this gate
- `platform_probe_status`: not executed
- `official_rehearsal_status`: not executed
- `F0_content_access`: none

## 1. Replacement boundary

This revision replaces only:

- v0.1 design §7 pipe construction and §10 admission-commit transport;
- the portions of v0.1 §§7 and 10 that prematurely bind an output-root object
  identity before the output leaf exists;
- v0.1 runtime-profile schema field `resource_limits.maximum_processes`; and
- corresponding interface-map and acceptance-plan clauses.

Every other v0.1 clause remains authoritative. The effective assembly design
remains v0.3 plus v0.4 replacements plus v0.5 replacements plus v0.1 plus
these v0.2 replacements. No predecessor invariant is weakened.

## 2. Exact unidirectional channel topology

The preloader creates exactly three anonymous pipe objects before verifier
creation:

| Channel | Direction | Preloader end | Verifier end |
|---|---|---|---|
| admission | preloader to verifier | write | read |
| commit request | verifier to preloader | read | write |
| commit reply | preloader to verifier | write | read |

The verifier's explicit `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` contains exactly:

1. admission-read;
2. commit-request-write;
3. commit-reply-read; and
4. one synchronize-only preloader process handle.

No authentication-file, job, verifier-process, pipe-opposite-end, output-root,
network, console, ambient standard handle, or unrelated handle is inherited.
All preloader ends and all nonchild duplicates are noninheritable. Immediately
after successful suspended creation, the preloader closes its duplicates of
the three verifier ends before assigning the process to the job and resuming
it. The verifier closes each endpoint at the frozen transition below.

The runtime admission binds the actual private process-local handle wrappers
for the three inherited endpoints and preloader process handle. Serialized
numeric handle values, copied wrappers, or structurally equal objects have no
authority.

## 3. Exact frame, close, and EOF protocol

### 3.1 Admission

The preloader writes exactly one canonical ASCII JSON admission line of at
most 8,192 bytes to admission-write, then closes admission-write. The verifier
reads exactly one final-LF frame, requires immediate EOF, and closes
admission-read. EOF before final LF, no EOF after the line, extra byte, second
line, timeout, or broken channel rejects before verifier-package import.

### 3.2 Commit request

Only a runtime admission in `ROOT-CREATED-BOUND` may enter `COMMITTING`. The
verifier writes exactly:

`RUNTIME_ADMISSION_COMMIT\n`

to commit-request-write, then closes that write end. The preloader reads the
exact bytes followed by immediate EOF and closes commit-request-read. Short,
extra, reordered, repeated, missing-EOF, timeout, or broken input is terminal.

### 3.3 Commit reply

After the exact request and EOF, the preloader performs every frozen identity,
file-set, job-accounting, verifier-liveness, pipe, root, and external-pin
recheck. If and only if they all pass, it writes exactly:

`OK\n`

to commit-reply-write and closes the write end. The verifier requires the
exact bytes followed by immediate EOF and closes commit-reply-read. Any other
condition rejects and permanently spends the admission attempt.

No retry, reconnection, alternate pipe, named-pipe fallback, duplex emulation,
self-read route, handle duplication after launch, or second commit exists.

## 4. Staged runtime-admission state machine

The private runtime admission has exactly these states:

1. `ROOT-ABSENT-BOUND`;
2. `ROOT-CREATED-BOUND`;
3. `COMMITTING`; and
4. `COMMIT-ACKED`; and
5. terminal `SPENT` or terminal `REJECTED`.

All transitions are one-way, lock-protected, identity-based, and attempted at
most once. Any invalid transition sets `REJECTED` before returning failure.

### 4.1 ROOT-ABSENT-BOUND

The verifier bootstrap creates the private admission before verifier-package
import only after binding:

- the existing output-parent retained handle and object identity;
- one canonical absent ASCII output leaf;
- workspace, runtime, and system-root identities;
- all external pins;
- admission, commit-request, and commit-reply endpoint wrappers;
- live preloader process handle and image identity;
- verifier PID and job membership;
- nonce; and
- retained runtime-file inventory digest.

The state contains no output-root identity and makes no claim about a
nonexistent object.

### 4.2 ROOT-CREATED-BOUND

After verifier-package authentication and import, but before candidate creation
or output-file reservation, the exact verifier-owned root binder:

1. rechecks the retained parent identity and leaf absence;
2. performs exactly one exclusive directory creation for that parent/leaf;
3. opens the created directory without following reparse points and without
   share-write or share-delete;
4. verifies local fixed NTFS, exact case, containment, non-reparse status,
   expected directory kind, emptiness, and parent/leaf continuity;
5. records volume serial and file index from the retained root handle; and
6. atomically advances the admission to `ROOT-CREATED-BOUND`.

The root handle remains open through verifier termination. Candidate launch,
output reservation, observer creation, and publication are forbidden before
this transition. A second root creation or binding, preexisting leaf, identity
change, replacement, unexpected entry, or binding failure sets `REJECTED`.

The sensitive-event policy admits only this exact verifier-owned root creation
and authentication sequence. It grants no candidate directory-creation or
general filesystem authority.

### 4.3 Witness and commit binding

The publication observer is constructed only from the retained bound-root
handle. Its private v0.5 witness records the same volume serial and file index.
After publication completes, the verifier atomically advances the admission
from `ROOT-CREATED-BOUND` to `COMMITTING` before writing the commit request.
An exact reply plus EOF advances it to `COMMIT-ACKED`; every commit failure
advances it to `REJECTED`.

The live consumer accepts only an admission in `COMMIT-ACKED`. On its first
terminal attempt it atomically spends both the admission and witness while
checking that:

- the admission is the exact live object in `COMMIT-ACKED`;
- the witness is the exact live v0.5 object;
- both reference the same retained root object identity;
- all final files and receipt bytes match; and
- neither authority has any prior terminal attempt.

The preloader's commit recheck independently verifies the output-parent and
root retained identities and exact root containment before replying `OK`.
Live-consumer acceptance advances the admission to `SPENT`; rejection advances
it to `REJECTED`. The witness is consumed in either case. No state can be
reused, and preloader `OK` alone is never success authority.

## 5. Exact process and job accounting

The preloader remains outside the job and owns the job handle. The job has both:

- `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`; and
- `JOB_OBJECT_LIMIT_ACTIVE_PROCESS` with `ActiveProcessLimit=2`.

Breakaway and silent breakaway are disabled. The verifier is assigned before
its first thread resumes.

The complete process topology is:

| Phase | Preloader outside job | Active job members | Job total created |
|---|---:|---:|---:|
| verifier bootstrap | 1 | 1 verifier | 1 |
| candidate execution | 1 | verifier + candidate = 2 | 2 |
| candidate exited, before commit | 1 | 1 verifier | 2 |

Exactly one verifier and exactly one authenticated candidate are created for
the run. No other descendant, helper, retry, replacement candidate, shell,
launcher, worker, crash reporter, or breakaway process is allowed. Candidate
runtime policy denies every process-creation capability. While the candidate
is active, the job limit independently prevents a third active member.

Immediately before commit reply, the preloader queries job accounting and
requires:

- total processes created: 2;
- active processes: 1, the exact verifier;
- total terminated processes: 1; and
- no breakaway or unclassified descendant evidence.

The verifier separately retains and authenticates the sole candidate process
handle and image and binds that identity into the run trace and live-consumer
checks. Job accounting proves that exactly one nonverifier job process was ever
created; the verifier evidence proves that this sole process was the admitted
candidate. Neither evidence substitutes for the other.

The future v0.2 runtime-profile package retains the complete v0.1 profile as a
separately hashed predecessor object and adds one v0.2 supplemental profile
conforming to the supplied v0.2 schema. The supplement pins the exact v0.1
profile SHA-256, records that its legacy `maximum_processes` value was one, and
marks that value `superseded-no-authority-do-not-enforce`. The v0.2
`process_job_policy` is the sole effective process-count authority and freezes
separate values for each counting domain. A consumer that enforces or derives
authority from the legacy value rejects.

The v0.2 runtime-profile package contains exactly these logical artifacts:

1. `runtime-profile-v0.1.json`;
2. `runtime-profile-v0.2.json`;
3. `runtime-files.sha256`; and
4. `runtime-profile-package-files-v0.2.sha256`, an exact three-row sorted
   manifest over items 1 through 3 whose own hash is externally supplied.

The v0.1 package manifest is predecessor evidence only and is not the v0.2
package authority. The runtime-file inventory must equal the v0.1 profile
inventory; the v0.2 supplement may replace only process/channel/root-binding
policy and may not add, delete, or reinterpret a runtime file, module, or PE
edge.

## 6. Failure routing replacements

- Admission-channel failure before verifier-package import remains
  `AR-AUTH/0` and occurs before output-root creation.
- Root creation, root binding, commit-channel, preloader-liveness, job-accounting,
  or retained-root failure after verifier launch is terminal
  `AR-BOUNDARY/observed-0-or-1`.
- Publication, observer, move, witness, receipt, or live-consumer defects remain
  `AR-RECORD/1` unless a denied boundary or preloader failure overrides them.
- Unauthenticated process death or diagnostic output is never success.

If an output root was created before any failure, no authority-bearing process
removes or renames it. It is reported as quarantined residue and remains
not-success. Any later post-process cleanup occurs outside the rehearsal
authority, is diagnostic only, and cannot upgrade or retroactively repair the
run. This preserves the retained no-share-delete handle and avoids a
close-then-path-delete substitution window.

## 7. Preserved nonregression requirements

Unchanged v0.1 authority includes:

- externally authenticated CONTROL launcher and Windows-kernel trust base;
- locked preloader binary handle, suspended creation, child-image equality,
  and resume-after-equality only;
- full Python, module, package, extension, PE, API-set, KnownDLL, and system-DLL
  closure;
- no SxS, redirection, registry, ambient path, repair, retry, download, or
  fallback;
- retained file handles and final exact-set recheck;
- exact flags, environment, `sys.path`, module origins, loaded-PE inventory,
  and denial latch;
- nonforgeable process-local authority and unchanged receipt-v2 wire form; and
- all claim limits and closed experimental boundaries.

## 8. Closed boundaries and next gate

This design revision does not implement or validate a preloader, runtime
profile, verifier revision, pipe, job, process, root binder, platform behavior,
or rehearsal. It opens no implementation, compilation, dependency-install,
runtime-materialization, platform-probe, real-`MoveFileExW`, official-rehearsal,
F0-content, hidden-oracle, provider/model/network, S0/E0, central-system,
Project Brain, commit, push, PR, release, or main-integration authority.

The exact next gate is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.2 INDEPENDENT REREVIEW OPEN`
