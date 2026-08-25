# Windows Authenticode verifier v0.4 independent code and security rereview

## 1. Review result

Verdict:
`PASS-FOR-BOUNDED-WINDOWS-AUTHENTICODE-VERIFIER-V0.4-NO-LIVE-AUTHORITY`.

Blocking findings: none.

The authenticated PUBLIC v0.4 candidate passes the bounded independent code
and security rereview. `BRM-AUTHV03-IR-001` is closed within the reviewed
synthetic, static, and no-live boundary. This verdict does not establish live
signature, trust, runtime, process, or operational authority and does not open
a live-artifact gate.

## 2. Reviewer role and boundary

Preserved reviewer facts:

- role: fresh independent, read-only PUBLIC code and security rereviewer;
- local branch, HEAD, tree, sole parent, and live remote identity: PASS;
- repository bytes changed by the reviewer: none;
- final status, index, and worktree: clean; and
- F0 content access and F0 role: none.

The reviewer model and runtime metadata were not supplied to the documentation
role and are not asserted here. F0 was used only as aggregate inventory and
quiet-state evidence.

## 3. Authenticated inputs and completed verification

Authenticated artifact facts available to the documentation role:

- v0.4 README SHA-256:
  `f31315808f0dc3c33de7529da2ba0cf04500164f43a65ed1c95fec2daa27f20a`;
- v0.4 implementation-manifest SHA-256:
  `ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c`;
- v0.4 verification-manifest SHA-256:
  `c977c482fc1c7364941072327168d233d31d54f6a7301b4cf3392948294515c1`;
- v0.4 revision-report SHA-256:
  `4e92839569c39f91381a8f880c7508ea7387055cfa301920e574f744a3daa348`;
- v0.3 rereview-response SHA-256:
  `0a95c38d45bd48b834cc805346b8d5495d628239f3f07ac00c68f7b7fba22d02`;
  and
- preserved v0.3 independent-rereview SHA-256:
  `d90452a74a352c76b3b33fae7d4487f11007ab9004e903c5c5b53740d2f98d1d`.

Preserved reviewer-reported verification results:

- v0.4 namespace: exactly 24 files;
- top manifests: `14 / 5` canonical rows;
- subordinate manifests: `1 / 1 / 1 / 3 / 3` rows;
- subordinate union: all nine implementation sources exactly once;
- manifest, target, predecessor-tree, preservation-ancestry, predecessor-
  manifest, and predecessor-review pins: PASS;
- canonical validator SelfTest and four Markdown/sidecar pairs: PASS;
- isolated no-bytecode manifest-bound `verify_candidate.py`: `23 / 23 PASS`;
- authenticated snapshot and original-input swap sentinel: PASS; and
- candidate native, network, provider, and process calls during verification:
  zero.

The final reviewer audit reported a clean repository, index, and worktree.
F0 tracked inventory was `32 / 11 / 10`; F0 worktree, index, untracked,
ignored, skip-worktree, assume-unchanged, and other special-flag anomaly
aggregates were all zero.

## 4. Finding disposition

### BRM-AUTHV03-IR-001 — CLOSED

Ownership is protected before every post-return FILETIME and QPC sample and
before chain parsing, hashing, and validation. The `finally` path frees every
non-null context whose ownership has not transferred, while a null context is
not freed.

On success, ownership transfers immediately before return. The local cleanup
does not double-free the transferred context, and the outer lifecycle frees it
exactly once.

Five relevant synthetic tests passed: post-return QPC failure with one free,
API failure with a non-null context and one free, API failure with a null
context and no free, parsing failure with one free and no double-free, and
successful transfer followed by one outer cleanup. The ownership-guard static
assertion also passed.

## 5. Authority correction and bounded authority

Authority correction: PASS.

No stale v0.3 namespace remained. The pinned outer implementation manifest
authenticated five subordinate manifests and their exact nine-source union.
Package import remained inert.

The resulting authority is only trusted-host disk consistency. The review did
not establish loaded- or executed-code authority, atomic mutable-host
authority, effective-trust authority, process authority, or live authority.

## 6. Predecessor dispositions

| Finding | Disposition | Boundary |
|---|---|---|
| `BRM-AUTHV02-IR-001` | **CLOSED** | Bounded fake-API certificate and CTL ownership evidence only. |
| `BRM-AUTHV02-IR-002` | **CLOSED WITH EXPLICIT ASSUMPTION** | Producer-time truth remains external CONTROL authority. |
| `BRM-AUTHV02-IR-003` | **CLOSED** | QPC remains the conservative elapsed-time authority. |

The relevant v0.1 dispositions remain closed within their previously stated
bounded no-live and external-authority limitations.

## 7. Nonblocking findings and limitations

- Exact acquisition-record, supplied-handle, and lease comparisons do not
  prove when the external producer sampled the path.
- UTC/QPC endpoint comparison cannot observe a fully cancelling intermediate
  wall-clock excursion. QPC remains authoritative for monotonic duration and
  freshness.
- Disk manifests do not authenticate loaded or executed code and do not
  provide atomic authority against a hostile mutable host.
- Native cleanup behavior, UNC and network-volume behavior, and x86 ABI
  behavior were not exercised live.
- F0 tracked inventory was `32 / 11 / 10`; skip-worktree and
  assume-unchanged anomaly counts were zero.

## 8. Correction provenance

The reviewer's first final draft mistakenly described `32 / 11 / 10` as
assume-unchanged counts while also reporting special flags as zero. The
reviewer immediately corrected the record: `32 / 11 / 10` is tracked F0
inventory, while skip-worktree and assume-unchanged counts are both zero.

This preservation treats only the corrected final result as authoritative.
The correction did not change the verdict, finding dispositions, evidence, or
scope.

## 9. Skipped work and nonclaims

The reviewer skipped real Windows trust, certificate-store, and native API
operations; candidate network, download, installer, build, and process
actions; x86 execution; live runtime materialization; an F0 content or role
action; S0; and E0.

No live signature, certificate, timestamp, revocation, trust, runtime,
operational-safety, or economic-value claim is established.

## 10. CONTROL-authenticated preservation facts

The following were supplied by CONTROL for result preservation and are not
additional reviewer evidence:

- opened gate: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.4 INDEPENDENT CODE AND SECURITY REREVIEW RESULT PRESERVATION OPEN`;
- preservation branch:
  `codex/s0-windows-authenticode-verifier-v04-independent-rereview-preservation`;
- preservation base:
  `84f21ecf183b44f67dfab507f732c273d7b70d5a`;
- preservation-base tree:
  `7d2cf3ec835ba4c7a6956c6c641d6a51f1065f09`; and
- CODE, TEST/VERIFICATION, and INDEPENDENT REVIEW were not rerun in this
  preservation gate.

## 11. Scope and next action

The reviewer's next action is result preservation only. No live gate may open
from this result.

`PASS-FOR-BOUNDED-WINDOWS-AUTHENTICODE-VERIFIER-V0.4-NO-LIVE-AUTHORITY`
