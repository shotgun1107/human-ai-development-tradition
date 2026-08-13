# S0 v0.14 public assembly runtime profile and neutral preloader acceptance plan v0.2

## 1. Status and replacement boundary

This is a public design-only acceptance revision. It replaces only the v0.1
criteria affected by `RPNP-RR-001`, `RPNP-RR-002`, and `RPNP-RR-003`. Every
other v0.1 acceptance requirement remains conjunctively necessary.

No implementation, runtime profile, executable, pipe, job, output root,
platform behavior, or rehearsal evidence is produced by this document.

## 2. Design-package acceptance

The v0.2 package passes author-side integrity validation only if:

- each logical artifact is strict UTF-8 without BOM, final-LF terminated, and
  free of trailing whitespace;
- every same-basename sidecar is canonical and hash-correct;
- `design-package-files.sha256` contains exactly six sorted unique logical rows
  and no self or sidecar row;
- both JSON files parse with duplicate-key rejection;
- `runtime-profile-v0.2.schema.json` passes Draft 2020-12 validation;
- the response, revision, interface map, schema, acceptance plan, and rereview
  brief agree on all three finding dispositions; and
- the v0.1 package and review-result-record pins reproduce exactly.

Author-side validation is not an independent verdict.

## 3. RPNP-RR-001 channel acceptance

Future static inspection and tests must establish exactly three Windows
anonymous unidirectional pipes and four verifier-inherited handles in the
frozen order. Each pipe must have one sender and one receiver after the
preloader closes all post-launch duplicate child ends.

For admission, request, and reply independently, tests must cover:

- exact frame followed by sender close and immediate receiver EOF;
- EOF before final LF;
- missing EOF;
- extra byte or line;
- duplicate frame;
- short read and fragmented read;
- wrong endpoint, direction, or order;
- inherited opposite end or extra handle;
- copied numeric handle or wrapper;
- sender or receiver death;
- timeout, broken pipe, and caught failure followed by retry; and
- a second commit, reconnect, alternate channel, named pipe, duplex pipe, or
  self-read attempt.

The only positive sequence is admission frame/EOF, commit request/EOF, frozen
preloader rechecks, and commit reply/EOF. `OK` alone is not PASS.

Mutation tests must change every handle-list row, direction, close, EOF check,
frame byte, count, timeout branch, and one-use transition. Every mutant must be
killed by a precommitted test.

## 4. RPNP-RR-002 staged-root acceptance

Before root creation, tests must prove that `RuntimeAdmission` binds exactly
the retained output-parent object identity and canonical absent leaf and
contains no fabricated output-root identity.

The sole positive root transition must prove:

1. parent identity remains unchanged and the leaf is absent;
2. the verifier executes one exclusive create;
3. the created directory is opened and retained without reparse traversal or
   share-write/share-delete;
4. fixed local NTFS, exact case, containment, directory kind, emptiness,
   nonreparse status, volume serial, and file index all match;
5. state advances once from `ROOT-ABSENT-BOUND` to `ROOT-CREATED-BOUND`; and
6. candidate creation is impossible before that transition.

Required negative cases include preexisting leaf, competing create, parent
replacement, leaf alias, reparse, hardlink-equivalent alias where applicable,
wrong volume, wrong case, unexpected entry, root replacement, second bind,
second creation, candidate-before-bind, and general candidate directory-create
authority.

The observer must be built from the same retained root handle. Tests must
reject a witness carrying another root identity, pathname-only equality,
reopened-copy identity, root replacement after publication, and preloader
commit recheck against a different root.

State tests must cover every invalid transition and require terminal
`REJECTED`. Exact preloader reply moves `COMMITTING` to `COMMIT-ACKED`; only the
first live-consumer attempt may atomically spend both the exact witness and
admission into `SPENT` or `REJECTED`.

## 5. RPNP-RR-003 process-accounting acceptance

Static source and binary review must establish:

- the preloader remains outside the job;
- the job flags include exactly kill-on-close and active-process limit;
- `ActiveProcessLimit` equals two;
- verifier assignment occurs before its first thread resumes;
- breakaway and silent breakaway are absent;
- exactly one candidate creation path exists; and
- candidate code has no process-creation capability.

Instrumented tests must observe exact phase accounting:

| Phase | Active job members | Total job processes created | Terminated |
|---|---:|---:|---:|
| verifier bootstrap | 1 | 1 | 0 |
| candidate execution | 2 | 2 | 0 |
| pre-commit | 1 | 2 | 1 |

The verifier must separately retain and authenticate the sole candidate
process/image/PID evidence. The preloader must independently verify the job
totals. Acceptance requires both bodies of evidence.

The future v0.2 supplemental profile must pin the complete v0.1 profile hash,
record the observed legacy value one, and mark it
`superseded-no-authority-do-not-enforce`. Tests must reject a changed v0.1
profile pin, any other disposition, enforcement of the legacy value, or a
process decision that consults it instead of `process_job_policy`.

The future runtime-profile package manifest must have exactly three sorted
rows: `runtime-files.sha256`, `runtime-profile-v0.1.json`, and
`runtime-profile-v0.2.json`. Its hash must be externally supplied. Tests must
reject the v0.1 two-row package manifest as v0.2 authority, any fourth row, a
missing or reordered row, supplement/profile pin disagreement, or any attempt
by the supplement to change the runtime-file/module/PE inventory.

Mandatory rejection cases include active limit one or greater than two, a
second candidate, helper, retry, replacement candidate, child-of-candidate,
shell, worker, crash reporter, detached process, breakaway, silent breakaway,
candidate exit before the authenticated run trace completes, wrong active PID,
and any job-accounting mismatch before reply.

Mutation tests must change each job flag, numeric limit, phase total, candidate
creation counter, PID/image binding, and failure branch. Every mutant must be
killed.

## 6. Cross-finding integration acceptance

A future implementation passes the combined diagnostic path only when:

1. admission authenticates and closes before verifier-package import;
2. root binding completes before candidate creation;
3. exactly one candidate executes as the second job member;
4. the candidate exits and publication evidence is complete;
5. commit request and EOF arrive exactly once;
6. the preloader rechecks runtime files, root identities, job totals, verifier
   identity, pins, and one-use state;
7. exact reply and EOF produce `COMMIT-ACKED`; and
8. the live consumer atomically spends the same-root witness and admission.

No isolated PASS of a pipe test, root test, process test, output hash, exit
code, or report can substitute for the combined chain.

## 7. Failure routing

- Admission authentication/channel failure before verifier-package import is
  `AR-AUTH/0` before output-root creation.
- Root creation/binding, commit channel, preloader, retained root, or job
  accounting failure after launch is `AR-BOUNDARY/observed-0-or-1`.
- Publication, move, observer, witness, receipt, or live-consumer failure is
  `AR-RECORD/1`, subject to denied-boundary override.
- Unauthenticated death, output presence, exit status, stdout, stderr, or
  `COMMIT-ACKED` without live-consumer acceptance is not success.

A created root is never deleted or renamed by an authority-bearing process
after failure. It remains quarantined not-success. Any later post-process
cleanup is diagnostic only and cannot upgrade or repair the run. Tests must
reject close-then-path-delete, in-run root removal, reused leaf, or cleanup
reported as success.

## 8. Independent rereview acceptance

The reviewer must independently authenticate the exact v0.1 package, review
result record, v0.2 package, schemas, sidecars, manifests, and predecessor pins.
The reviewer must then attempt to falsify each correction and every preserved
v0.1 nonregression predicate.

A passing v0.2 rereview requires zero unresolved `BLOCKING` or `MAJOR`
findings. It opens only consideration of a separate bounded implementation
gate and is not implementation authorization.

## 9. Closed boundaries and next gate

Implementation, compilation, dependency installation, runtime-profile
materialization, platform probe, real `MoveFileExW`, official rehearsal, F0
content, hidden oracle, provider/model/network, S0/E0, central system, Project
Brain, operational safety, economic value, model transfer, commit, push, PR,
release, and main integration remain closed.

The exact next gate is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.2 INDEPENDENT REREVIEW OPEN`
