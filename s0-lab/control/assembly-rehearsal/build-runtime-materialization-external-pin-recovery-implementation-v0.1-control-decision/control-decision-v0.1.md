# External-pin recovery implementation v0.1 CONTROL decision

## 1. Purpose and authority

This public artifact records the exact CONTROL decision for external-pin
recovery implementation v0.1. CONTROL froze the candidate identity, integrated
the authenticated CODE IMPLEMENTATION, TEST/VERIFICATION, DOCUMENTATION, and
fresh INDEPENDENT REVIEW handoffs, and made the decision recorded here.
DOCUMENTATION transcribed that decision from the authenticated evidence; it did
not modify candidate or review bytes, rerun substantive verification, perform
independent review, or make a different decision.

This decision authorizes no commit, push, pull request, release, or `main`
merge. Git publication remains subject to separate approval.

## 2. Gate and pinned identity

- Opened candidate gate: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.1 ACTUAL EXTERNAL ARTIFACT ACQUISITION AND BUILD RUNTIME ENVIRONMENT CONSTRUCTION OPEN`
- Branch: `codex/s0-build-runtime-external-pin-recovery-implementation-v01`
- HEAD/base commit: `defec54dd0f6bf9896bc22beab2732f4ae660e48`
- Tree: `3f6711d5d6491a250bde7c36b769051229fe7e43`
- Parent commit: `dfa31376f11a7e2267f9ac1aaea38f99c194f846`
- Candidate status: `LIVE-ACQUISITION-COMPLETED-CANDIDATE-BLOCKED`
- Independent verdict: `REVISE-AND-REREVIEW`
- Finding count: `0 BLOCKING / 4 MAJOR / 0 MINOR`
- Integration readiness: `NOT READY`

## 3. Authenticated evidence identity

CONTROL authenticated the evidence used for this decision against these exact
records:

- implementation manifest SHA-256: `0f011bbc469d77f4fe06591abe769963a3eca1ae36d964a21e18d4cfd531de13`
- verification manifest SHA-256: `f347e8ceb2934179f5e065a55787a792295bb85332e167e2c9c7e0e90110c330`
- candidate-package manifest SHA-256: `35a6f82d938e05b2d3e33f02c74d3ddc86858e2e6048cd24a75dd0eef2c355a6`
- independent-review preservation Markdown SHA-256: `408c16c3b0e6e0249c2ae3313f096e15111be5332f4e216611802e7c2a27b063`
- independent-review preservation sidecar-file SHA-256: `fa6e60e5d3e0603989ad6af63e68f0eb54e0ef3b22baaa69e26129c51b1b6e34`

The fresh independent reviewer was read-only, used `gpt-5.6-sol` with `ultra`
reasoning, and had not served as CONTROL, CODE IMPLEMENTATION,
TEST/VERIFICATION, or DOCUMENTATION for this candidate/version. The reviewer
reported manifest closure PASS, 24 of 24 tests passing with zero failures,
errors, skips, expected failures, unexpected successes, or nonzero child or
verifier exits, while still issuing the `REVISE-AND-REREVIEW` verdict.

These preserved observations are evidence inputs to CONTROL's decision. They
are not a new substantive test run or an independent conclusion by
DOCUMENTATION.

## 4. Bounded live-acquisition evidence accepted by CONTROL

CONTROL accepts only the following bounded factual evidence from v0.1:

- The CPython 3.12.10 embeddable ZIP was actually acquired with zero redirects.
  Its observed 11,133,606-byte archive matched the frozen SHA-256
  `4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3`.
- The authenticated CPython archive was staged inertly as 35 regular files,
  zero explicit directories, and 22,501,299 aggregate regular-file bytes. The
  recorded target-set SHA-256 was
  `6fc8da66db95821ca8692de9d224d63673b11c0a47593cfa86fced2fb32549df`.
  The archive and staged content were not executed or imported.
- The Visual Studio Build Tools bootstrapper was acquired with zero redirects,
  but its expected size and expected SHA-256 were absent. Its status remains
  `ACQUIRED-UNAUTHENTICATED`; resemblance between a URL segment and the
  observed digest is not authentication authority. The acquired bytes were
  never executed.
- `jsonschema` and its complete transitive dependency closure were not
  acquired. The unresolved pins and associated trust blockers remain blocked.

The retained external root's exact local path is classified
`NONPUBLIC-OUT-OF-REPO` and is represented here only as
`<OUT-OF-REPOSITORY-ROOT>`. The existing external root and its acquired
artifacts must be preserved and must not be reused for a new acquisition
attempt.

This bounded acceptance does not overcome the independent findings, make the
candidate eligible, or grant execution or integration authority.

## 5. Independent findings integrated by CONTROL

CONTROL integrates all four MAJOR findings without downgrading or accepting
them:

1. `BRM-EPRI01-IR-001` — Windows path validation and creation are not bound to
   retained handles and a no-reparse creation chain. A concurrent parent
   junction or reparse-point swap can redirect writes after validation.
2. `BRM-EPRI01-IR-002` — Archive and output identities are not held stable
   across use, and final outputs are not reauthenticated through retained
   identities. Concurrent mutation can separate the recorded evidence from the
   archive or final tree actually used.
3. `BRM-EPRI01-IR-003` — Authentication authority is caller-mintable through
   mutable or duck-typed pins and naked digests rather than a closed,
   authenticated, immutable allowlist.
4. `BRM-EPRI01-IR-004` — The verifier does not bind itself to the exact test
   file and full manifest, and its pass predicate permits skipped or
   expected-failure tests. The outer manifest authenticated the observed
   24-test suite, but the verifier is not fail-closed against substitution.

## 6. CONTROL decision

The v0.1 candidate is blocked and must be revised and independently reviewed
again. Its integration readiness is `NOT READY`. It must not integrate to
`main`, and it grants no authority to execute a process, install software,
construct or run a build, construct or run a runtime, conduct a rehearsal, run
S0, or run E0.

The exact authority state remains:

- process executed: false
- process authority granted: false
- installation claimed: false
- installation validated: false
- build claimed: false
- build validated: false
- runtime claimed: false
- runtime validated: false
- rehearsal claimed: false
- rehearsal validated: false
- S0 claimed: false
- S0 validated: false
- E0 claimed: false
- E0 validated: false

## 7. Required v0.2 revisions

Before a new candidate may be handed to fresh independent review, the next
revision must provide all of the following:

1. Handle-bound Windows no-reparse creation, retained parent identity, and
   explicit detection of parent swaps.
2. Stable archive and output identities throughout acquisition and
   materialization, followed by final reauthentication of the archive and
   produced output through those retained identities.
3. A closed allowlist of authenticated pins and digests using exact immutable
   pin objects; callers must not be able to mint or mutate authentication
   authority.
4. Verifier binding to the exact test file and the complete authenticated
   manifest, with zero skipped tests and zero expected failures required by the
   verifier's own pass predicate.
5. Negative tests for parent-swap and reparse races, mutable authentication
   authority, archive or output mutation, and test or manifest substitution.
6. New, sequential TEST/VERIFICATION and DOCUMENTATION handoffs followed by a
   fresh, read-only INDEPENDENT REVIEW. CONTROL must then make a new decision.

The next revision must not reuse the existing external acquisition root. Any
new acquisition attempt requires a fresh, separately controlled external root
and the exact gate authority applicable to that attempt.

## 8. Nonclaims and closed authority

This decision does not claim or validate live trust, supplier assurance,
process execution, installation, build construction or success, runtime
construction or success, rehearsal, S0, E0, the central system, Project Brain
integration, operational safety, economic value, or model-to-model transfer.
It does not authenticate Build Tools, resolve `jsonschema`, close the
transitive dependency set, or approve any remaining external pin.

The candidate artifacts, review artifacts, and retained external bytes remain
evidence only within their stated boundaries. Worktree separation, repository
presence, and successful bounded tests do not expand those boundaries.

## 9. Next gate recorded but not opened

The exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.2 REVISION OPEN`

That gate is recorded for a possible future CONTROL freeze. It is **not open**
by this decision, this documentation artifact, or the prior v0.1 gate. No v0.2
implementation, test, acquisition, documentation, review, integration, Git
publication, or execution authority is granted here.
