# External-pin recovery implementation v0.1 independent review result preservation

## Purpose and authority

This public artifact preserves the authenticated result handed off by the fresh independent code-security reviewer for external-pin recovery implementation v0.1. It does not replace the review, rerun candidate verification, modify candidate bytes, or make the CONTROL decision. Facts, review findings, required revisions, and claim boundaries are labeled separately below.

## Candidate and reviewer identity

- Branch: `codex/s0-build-runtime-external-pin-recovery-implementation-v01`
- HEAD/base commit: `defec54dd0f6bf9896bc22beab2732f4ae660e48`
- Tree: `3f6711d5d6491a250bde7c36b769051229fe7e43`
- Parent commit: `dfa31376f11a7e2267f9ac1aaea38f99c194f846`
- Reviewer model: `gpt-5.6-sol`
- Reviewer reasoning: `ultra`
- Reviewer status: fresh, read-only, and not previously assigned CONTROL, CODE IMPLEMENTATION, TEST/VERIFICATION, or DOCUMENTATION for this candidate/version
- Reviewer boundary: no repository or external edit, no F0 access, and no live rerun

The reviewer authenticated exactly 19 allowlisted untracked candidate files and zero untracked files outside that allowlist, with no staged or tracked modification.

## Authenticated evidence facts

### Manifest closure

Manifest closure: PASS.

- Implementation manifest: 7 rows; SHA-256 `0f011bbc469d77f4fe06591abe769963a3eca1ae36d964a21e18d4cfd531de13`
- Verification manifest: 7 rows; SHA-256 `f347e8ceb2934179f5e065a55787a792295bb85332e167e2c9c7e0e90110c330`
- Package manifest: 8 rows; SHA-256 `35a6f82d938e05b2d3e33f02c74d3ddc86858e2e6048cd24a75dd0eef2c355a6`
- Same-basename sidecars, JSON evidence, and canonical-validator pairs: PASS

### Independent verifier rerun

- Result: 24/24 PASS
- Failure, error, skip, expected, and unexpected counts: all zero
- Child and verifier exit codes: 0 and 0
- Mutation and swap sentinels: PASS
- Authenticated hashes before and after the rerun: stable
- Test-file SHA-256: `7804817aaf66b74e010bc3f1c2e7763593a15bf24e2b7c8a9785478e013107b9`

These are preserved test results, not a claim by the DOCUMENTATION role that it performed the tests.

### Live-evidence consistency

- The frozen CPython hash matched, and CPython staging remained inert.
- BuildTools remained `ACQUIRED-UNAUTHENTICATED`.
- `jsonschema` remained unacquired.
- All 13 blockers/false claims were retained.

The reviewer found the live evidence internally consistent. These facts do not establish process, installation, build, runtime, or S0 success.

## Independent review findings

Finding count: **0 BLOCKING / 4 MAJOR / 0 MINOR**.

### BRM-EPRI01-IR-001 — MAJOR

Locations: `acquisition.py:113-177,207-211`; `materialize.py:163-195,416-451`.

The path-check/path-use sequence has a time-of-check/time-of-use race. It retains neither directory identity nor a handle-relative, no-reparse creation chain. A concurrent parent junction or reparse-point swap can redirect writes or staging after validation.

### BRM-EPRI01-IR-002 — MAJOR

Locations: `materialize.py:376-403,425-484`; additionally `acquisition.py:135-190`.

Archive and output identity are unstable across use. There is no locked archive identity or final digest, and outputs are not reauthenticated through retained identities. Concurrent mutation can therefore make the evidence and final tree diverge.

### BRM-EPRI01-IR-003 — MAJOR

Locations: `pins.py:6-14`; `acquisition.py:92-115,183-205,252-282`; `materialize.py:406-432,487-527`.

Authentication authority is caller-mintable. A duck-typed mutable pin or naked digest can authenticate self-consistent attacker-controlled bytes, although the process flags remain false.

### BRM-EPRI01-IR-004 — MAJOR

Locations: `verify_candidate.py:20-42,156-177,223-246`.

The verifier does not internally pin the test file, and its pass predicate permits skipped or expected-failure tests. The current outer manifest authenticates the actual 24-test suite, but the verifier itself is not fail-closed against test substitution.

## Required revisions from the reviewer

Before another independent review, the reviewer requires:

1. Handle-bound Windows no-reparse creation and parent-swap detection.
2. Stable archive and output identity with final reauthentication.
3. A closed authenticated pin/digest allowlist with exact immutable pin objects.
4. Exact test-hash and full-manifest binding, with zero skipped or expected-failure tests permitted by the verifier's pass predicate.
5. Race, mutable-authority, and test-substitution negative cases, followed by repeated TEST/VERIFICATION, DOCUMENTATION, and fresh INDEPENDENT REVIEW handoffs.

## Adversarial conclusion and verdict

The existing URI, hash, and traversal controls are substantial, but they do not close the race, mutable-authority, or test-substitution attacks described above. Process, install, build, runtime, and S0 remain false.

The independent review verdict is **REVISE-AND-REREVIEW**.

## Claim boundary

This preservation artifact does not claim implementation or validation of S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer. It contains no CONTROL acceptance decision and grants no publication, commit, push, or gate-opening authority.
