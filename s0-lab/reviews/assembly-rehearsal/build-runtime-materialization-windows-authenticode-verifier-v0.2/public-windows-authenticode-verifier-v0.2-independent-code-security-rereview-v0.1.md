# S0 v0.14 Windows Authenticode verifier v0.2 independent code and security rereview

## 1. Review result

Verdict: `REVISE-AND-REREVIEW`.

The authenticated PUBLIC v0.2 revision does not pass the bounded independent
code and security rereview. Three security and native-resource findings remain
blocking.

| Severity | Count | Finding IDs |
|---|---:|---|
| HIGH / BLOCKING | 1 | `BRM-AUTHV02-IR-002` |
| MEDIUM / BLOCKING | 2 | `BRM-AUTHV02-IR-001`, `BRM-AUTHV02-IR-003` |

The v0.2 private read lease, WinTrust and chain lifecycle corrections,
executed-code-authority claim narrowing, and fixed-hex FILETIME representation
were accepted within their bounded non-live scope. The new findings still
require revision and fresh rereview. No live-artifact gate may open.

## 2. Role, identity, and boundary

Facts:

- rereview gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.2 INDEPENDENT CODE AND SECURITY REREVIEW OPEN`;
- role: fresh independent PUBLIC code and security rereviewer;
- reviewer runtime: `gpt-5.6-sol`, reasoning level `ultra`;
- reviewed branch tip:
  `67ed5f55b3883c1b3d897fe26bb3cc27c98ef14d`;
- tip tree:
  `614837a93524ca2f2f0ad76c139e5f4c274aebb5`;
- implementation candidate commit and tip sole parent:
  `808d08e876e60f9c0fbe2d81b5e5c1682928b026`;
- implementation candidate tree:
  `2acfe3c7f42bb92328f10aeb537f701c372fe41c`;
- candidate sole parent and v0.1 review-preservation commit:
  `ade0e1636ba483b9f8e3f465421a2c47cf1f1e33`;
- implementation-manifest SHA-256:
  `6fe56c7fac527b0adfda02e32e0e4b5355ff4adfe8a499732dfb7a43d2df213a`;
- verification-manifest SHA-256:
  `f8f2516ad00d06e257954b3b82e67446f7b3920656626eb026530062c7da9b02`;
- revision-report SHA-256:
  `d06cc9a9712ba95b0830d38481a757a838ca2ee76cfa5ee0e607d98365f82b47`;
- v0.1 review-response SHA-256:
  `91713bf5d7824a069292d3416f9c64c907682fb253d7e58e244770bef23e436c`;
- preserved v0.1 independent-review SHA-256:
  `e72fe7ce12e2182b5ca45e07f698083afb9672bf7b0c70ef6429d42dc55826f9`;
- rereview date: `2026-08-25`; and
- F0 content access: none.

The rereviewer inherited no author or prior-review conversation, called no
other agent, used only the frozen PUBLIC allowlist, and made no repository
change. F0 was used only as aggregate inventory and quiet-state evidence.

## 3. Input authentication and bounded verification

Facts and test results:

- live remote tip, local tip, branch, trees, sole parents, and ancestry: PASS;
- the tip-only policy change from the implementation commit changed exactly
  root `AGENTS.md`; the v0.2 namespace and F0 were quiet;
- worktree and index: clean before and after review;
- F0 aggregate inventory: `32 / 11 / 10`;
- every F0 worktree/index quiet query and untracked, ignored, skip-worktree,
  and assume-unchanged anomaly count: zero;
- v0.2 namespace: exactly 24 files;
- v0.2 top manifests: `14 / 5` canonical rows, all target hashes matched;
- subordinate manifests: `1 / 1 / 1 / 3 / 3`, all target hashes matched;
- subordinate union covered all nine v0.2 sources exactly once;
- v0.1 predecessor manifests: `12 / 4` rows and all 16 exact targets matched;
- canonical validator SelfTest: PASS;
- v0.2 README, revision report, review response, and preserved v0.1 review
  Markdown/sidecar pairs: PASS;
- authenticated temporary-snapshot tests: `18 / 18 PASS` in `0.052s`;
- original-input swap sentinel: PASS; and
- static x64 ctypes sizes and checked offsets: PASS.

No candidate native API, certificate store, network, download, installer,
build, runtime materialization, candidate process, F0 role, S0, or E0 action
occurred. No x86 Python runtime was available.

## 4. Blocking findings

### BRM-AUTHV02-IR-002 — HIGH — the acquisition record does not bind the acquired path

Evidence:

- `acquisition.py:84-100` defines the exact canonical record fields with no
  acquired-path field.
- The record file identity at `acquisition.py:42-61` contains only volume
  serial, file ID, reparse status, and byte length.
- `win32.py:772-800` compares the independently supplied `full_path` with the
  current supplied-handle and lease paths, but compares the acquisition record
  only by file identity.
- `README.md:33-35` and the review response at lines 47-49 incorrectly state
  that acquisition, handle, and lease are compared by path.

Failure path: an externally pinned acquisition record for file identity and
bytes `F` cannot distinguish the acquired path from a later caller-selected
alias or hard-link path that currently resolves to `F`. The runtime proves
only that the caller path matches the current handle and lease, not that the
acquisition authority recorded that path.

Affected claim: fixed-URL acquisition provenance, acquisition/handle/path
binding, and the supplier composite.

Required correction: add one canonical externally pinned acquired-path
representation to the acquisition schema and bind it to the producer and
verifier handles. Define NT, DOS, UNC, case, ADS, hard-link, rename, and
reparse semantics. If path is intentionally outside the criterion, remove all
path-binding claims instead.

### BRM-AUTHV02-IR-001 — MEDIUM — certificate and CTL contexts leak on exceptional enumeration exits

Evidence:

- `win32.py:535-565` can raise after receiving a current certificate or CTL
  context but before passing it to the next enumeration call. Oversize or
  absent encoding and the entry bound are direct paths.
- The adapter defines neither `CertFreeCertificateContext` nor
  `CertFreeCTLContext`.
- Its `finally` calls `CertCloseStore(store, 0)`, which does not check
  outstanding contexts.

Microsoft requires a returned enumeration context that is not passed back to
be explicitly freed:
[CertEnumCertificatesInStore](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certenumcertificatesinstore),
[CertEnumCTLsInStore](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certenumctlsinstore),
[CertCloseStore](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certclosestore).

Failure path: a malformed or oversize store entry, or the first entry beyond
the configured bound, raises while the current context remains owned.
Repeated rejected snapshots can exhaust process memory even when store close
returns success.

Affected claim: bounded native resource lifecycle and complete closure of
`BRM-AUTHV01-IR-004`.

Required correction: define the two context-free APIs and explicitly free the
current context on every exceptional exit before normal ownership transfer.
Prevent double-free after normal enumeration and add mocked exceptional-path
allocation/free-count tests.

### BRM-AUTHV02-IR-003 — MEDIUM — adjustable UTC timestamps do not detect clock discontinuity

Evidence:

- `win32.py:647-680` and `685-692` bracket each chain call only with
  `GetSystemTimeAsFileTime` and accept any nonnegative net UTC difference up
  to 30 seconds.
- `semantic.py:238-260` uses that net difference as the complete freshness
  margin.
- `test_authenticode_verifier.py:502-518` tests only a net reversal and a net
  overrun.

Microsoft describes `GetSystemTimeAsFileTime` as current UTC and QPC as an
interval clock independent of system-time changes:
[GetSystemTimeAsFileTime](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getsystemtimeasfiletime),
[QPC guidance](https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps).

Inferred failure path: a backward adjustment followed by partial recovery can
leave `returned >= started` with a net interval below 30 seconds even when the
actual elapsed interval is longer. Near the 86,400-second threshold, the
underestimated margin can accept stale revocation material.

Affected claim: conservative freshness and complete closure of
`BRM-AUTHV01-IR-006`.

Required correction: bracket each chain call with QPC or another documented
monotonic counter. Use the ceiling of monotonic elapsed time for freshness and
duration bounds, and cross-check UTC movement against monotonic elapsed time
under an explicit tolerance. Serialize large counters without reintroducing
the JSON exact-integer defect.

## 5. Predecessor finding dispositions

| Finding | Disposition | Reason |
|---|---|---|
| `BRM-AUTHV01-IR-001` | **PARTIALLY CLOSED** | Canonical external pins, fixed URL, producer label, PID/handle value, file identity, length, hash, and lease cross-binding exist; the acquired path is absent and producer truth remains an external assumption. |
| `BRM-AUTHV01-IR-002` | **CLOSED** | VERIFY enters cleanup before state inspection; CLOSE covers every VERIFY path. Chain contexts have correct local-to-outer ownership transfer and no double-free or use-after-free was found. |
| `BRM-AUTHV01-IR-003` | **CLOSED** | The verifier-owned `GENERIC_READ`/`FILE_SHARE_READ` lease has the documented conflict behavior, remains open, and supplies every WinTrust and hash operation. |
| `BRM-AUTHV01-IR-004` | **PARTIALLY CLOSED** | Store coverage, terminal-status checks, bounds, close-result checks, and the effective-trust nonclaim exist; exceptional current-context ownership remains broken. |
| `BRM-AUTHV01-IR-005` | **CLOSED** | Closure is by the permitted claim narrowing: inert import, trusted-host disk-consistency scope, false executed/process authority, and no-live-authority terminal result. |
| `BRM-AUTHV01-IR-006` | **PARTIALLY CLOSED** | The exact-instant overclaim was removed and a freshness margin added, but the interval is not monotonic or discontinuity-safe. |

## 6. FILETIME JSON-range disposition

The fixed-hex FILETIME correction is **CLOSED**.

All reviewed FILETIME values use fixed lowercase 16-hex strings. Semantic
parsing enforces that grammar and converts values only for bounded arithmetic.
The positive fixture uses a real Windows-range value above JSON's exact
integer range and serializes successfully.

This closure does not resolve `BRM-AUTHV02-IR-003`, which concerns the clock
source and elapsed-time measurement rather than representation.

## 7. Nonblocking findings and limitations

- Acquisition-record and producer-manifest hashes remain external CONTROL
  authorities. The package does not authenticate or execute the producer.
  Numeric same-process handle continuity is not protected against a hostile
  trusted host that deliberately recycles handles. This is acceptable only
  under the explicit no-live-authority boundary.
- The six-store snapshot is consistently represented as an observed mutation
  sentinel with `effective_trust_authority_claimed=false`; it does not cover
  every cache, policy source, or transient effective-chain input.
- `process_count_before_decision` is caller supplied and must not be promoted
  beyond the process-authority nonclaim.
- No code or documentation path was found that promotes
  `TRUSTED-HOST-DISK-CONSISTENCY-ONLY` into executed-code, process, effective-
  trust, or live authority.
- Explicit `restype=None` declarations for void Win32 APIs would improve ABI
  exactness. No current blocking ABI failure was demonstrated.

## 8. Scope and next decision

This rereview establishes only a read-only assessment of authenticated PUBLIC
source and bounded synthetic/static evidence. It establishes no live
signature, acquisition, trust state, runtime authority, operational safety,
rehearsal, F0 result, S0, or E0 result.

Result preservation may proceed under its separate CONTROL gate. Another
bounded revision and fresh independent rereview are required. Any live-
artifact gate remains closed.

`REVISE-AND-REREVIEW`
