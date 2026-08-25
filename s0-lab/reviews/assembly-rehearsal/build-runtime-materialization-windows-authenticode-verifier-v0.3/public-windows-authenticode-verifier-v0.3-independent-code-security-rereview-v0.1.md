# Windows Authenticode verifier v0.3 independent code and security rereview

## 1. Review result

Verdict: `REVISE-AND-REREVIEW`.

The authenticated PUBLIC v0.3 candidate does not pass the bounded independent
code and security rereview. One native-resource finding remains blocking.

| Severity | Count | Finding IDs |
|---|---:|---|
| MEDIUM / BLOCKING | 1 | `BRM-AUTHV03-IR-001` |

The acquisition-path revision, certificate and CTL exceptional ownership,
monotonic duration and freshness revision, and fixed-hex time representation
were accepted within the stated boundaries. The chain-context regression
requires another revision and fresh independent rereview. No live-artifact
gate may open.

## 2. Role, identity, and boundary

Preserved reviewer facts:

- opened result-preservation gate: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.3 INDEPENDENT CODE AND SECURITY REREVIEW RESULT PRESERVATION OPEN`;
- role: fresh independent, read-only PUBLIC code and security rereviewer;
- reviewed candidate commit:
  `b441db0379f7bef4f24384a7001e2c82df2813d5`;
- reviewed candidate tree:
  `71319ee002dc99400669172f4b3d94335caae524`;
- candidate sole parent:
  `ad36069581816416dec5cc970962289701f51de7`;
- worktree and repository changes by the reviewer: none; and
- F0 content access: none.

The reviewer used F0 only as aggregate inventory and quiet-state evidence.
The reviewer model and runtime metadata were not supplied to the documentation
role and are not asserted by this preservation artifact.

## 3. Input authentication and bounded verification

Authenticated artifact facts available to the documentation role:

- implementation-manifest SHA-256:
  `f44e1d3f37cd122c0b619fa31080f1d759050d8932dc8e75cdc3861441e4dc1d`;
- verification-manifest SHA-256:
  `c32127e9db0d9f42a759274f790f223cedf98b701eee809bac9c39ae69fdaccc`;
- implementation-revision-report SHA-256:
  `5a75aae93c1f23057e73519480da60f95b5f01d4efd7a04f67516cf710bb631a`;
- v0.2 rereview-response SHA-256:
  `afce6a34020762f8721f5382906cf24abce36725021f705ebeea4c82952e53d8`;
- preserved v0.2 independent-rereview SHA-256:
  `c8fdb45ba2fde477e5a1662e28131a388ec1cce637313e2508b5e40c2d369eee`;
  and
- each supplied Markdown hash matched its canonical sidecar.

The following are preserved reviewer-reported verification results. This
documentation pass did not rerun them:

- pinned candidate commit, tree, and parent: PASS;
- worktree and index before and after review: clean;
- F0 aggregate inventory: `32 / 11 / 10`, with zero reported anomalies;
- v0.3 namespace: exactly 24 files;
- v0.3 top manifests: `14 / 5` canonical rows;
- subordinate manifests: `1 / 1 / 1 / 3 / 3` rows;
- subordinate union: exact coverage of all nine v0.3 sources;
- manifest and target hashes: PASS;
- supplied revision-report, response, and predecessor-rereview pins: PASS;
- canonical validator SelfTest and four Markdown/sidecar pairs: PASS; and
- predecessor manifests: `14 / 5` rows and all 19 exact targets matched.

The reviewer did not independently run the author-reported 18 tests, the x64
size script, an x86 runtime, or live APIs. The author-reported `18 / 18` result
is not independent closure evidence.

## 4. Blocking finding

### BRM-AUTHV03-IR-001 — MEDIUM — chain context can leak when return-time QPC sampling fails

Evidence:

- `win32.py:736-747` calls `CertGetCertificateChain`, which may return a
  non-null chain context.
- `call_returned` and `_qpc_now` are evaluated at `win32.py:748-749`, before
  the cleanup `try` begins at line 754.
- `_qpc_now` can raise at `win32.py:424-428`.
- That exception bypasses both the failure-path free at `win32.py:750-752`
  and the exception-path free at `win32.py:797-799`.

Failure path: after a successful chain call returns a non-null context, a
return-time QPC failure raises before cleanup ownership is protected. Each
such rejection leaks one chain context.

Affected claim: complete chain-context ownership and bounded native-resource
lifecycle.

Required correction: protect ownership immediately after
`CertGetCertificateChain` returns, free every non-null context on every later
exception, and add a fake-API test for chain success followed by return-time
QPC failure.

Microsoft documents the returned-context ownership requirement in
[CertGetCertificateChain](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain).

## 5. v0.2 finding dispositions

| Finding | Disposition | Reason |
|---|---|---|
| `BRM-AUTHV02-IR-001` | **CLOSED** | Certificate and CTL exceptional ownership is corrected in the bounded fake-API scope. |
| `BRM-AUTHV02-IR-002` | **CLOSED WITH EXPLICIT ASSUMPTION** | Exact record, supplied-handle, and lease path comparisons close the candidate-side binding only under external CONTROL producer truth. |
| `BRM-AUTHV02-IR-003` | **CLOSED** | QPC is the conservative elapsed-time authority for duration and freshness; the new chain leak is a separate regression. |

## 6. Regression and earlier-finding dispositions

| Finding | Disposition | Reason |
|---|---|---|
| `BRM-AUTHV01-IR-001` | **CLOSED WITH EXTERNAL-AUTHORITY LIMITATION** | Candidate-side binding is present, but producer-time path truth remains external to the verifier. |
| `BRM-AUTHV01-IR-002` | **REGRESSED / OPEN IN PART** | VERIFY and CLOSE remain closed; chain-context ownership is reopened by `BRM-AUTHV03-IR-001`. |
| `BRM-AUTHV01-IR-003` | **CLOSED IN BOUNDED NO-LIVE SCOPE** | The private read lease correction remains accepted. |
| `BRM-AUTHV01-IR-004` | **CLOSED IN BOUNDED NO-LIVE SCOPE** | Certificate and CTL exceptional ownership is correct within the reviewed boundary. |
| `BRM-AUTHV01-IR-005` | **CLOSED IN BOUNDED NO-LIVE SCOPE** | Executed-code, process, effective-trust, and live-authority nonclaims remain bounded. |
| `BRM-AUTHV01-IR-006` | **CLOSED IN BOUNDED NO-LIVE SCOPE** | Monotonic QPC duration and freshness behavior is accepted within the stated limitations. |

The fixed-hex FILETIME correction is **CLOSED**. The QPC correction is also
**CLOSED** for monotonic duration and freshness. Neither closure resolves the
separate chain-context leak.

## 7. Nonblocking findings and limitations

- The acquired path remains a producer-time fact asserted by external
  CONTROL. Exact acquisition-record, supplied-handle, and lease path
  comparisons do not prove when the producer sampled that path.
- `semantic.py:290-306` compares UTC and QPC endpoints only. A fully
  cancelling intermediate backward-then-recover excursion is unobservable,
  so `README.md:51-52` overstates detection of every such excursion. QPC
  remains the conservative elapsed-time authority, and the two-second
  tolerance was not deemed an additional freshness margin.
- Certificate and CTL exceptional ownership at `win32.py:584-636` is correct.
  Tests at `test_authenticode_verifier.py:490-540` cover the cleanup helper,
  not the full ownership-transfer path.
- UNC and network volume-GUID behavior and x86 ABI behavior remain untested
  live and fail closed.

## 8. Explicitly unverified and skipped work

The reviewer did not independently verify:

- the author-reported 18-test run;
- the x64 size script;
- an x86 runtime; or
- any live Windows API behavior.

The review skipped real trust and certificate-store operations, network and
download activity, installer and build activity, candidate-process execution,
runtime materialization, an F0 role, S0, and E0. These are unverified, not
implicitly passed.

## 9. Later CONTROL-authenticated preservation facts

The following facts were supplied by CONTROL after the reviewer completed the
read-only assessment. They are preservation facts, not reviewer evidence:

- preservation branch:
  `codex/s0-windows-authenticode-verifier-v03-independent-rereview-preservation`;
- preservation base:
  `3a77ed1c9de234116e15d5278465c4149547d9e6`; and
- the range from reviewed candidate
  `b441db0379f7bef4f24384a7001e2c82df2813d5` through preservation base
  `3a77ed1c9de234116e15d5278465c4149547d9e6` changes only root `AGENTS.md`
  and leaves the reviewed v0.3 namespace unchanged.

This section does not extend the review to the later policy commit or convert
CONTROL authentication into independent-review evidence.

## 10. Scope and next decision

This artifact preserves a read-only assessment of authenticated PUBLIC source
and bounded synthetic and static evidence. It establishes no live signature,
acquisition, trust state, runtime authority, operational safety, rehearsal,
F0 result, S0, or E0 result.

Another bounded code revision and fresh independent code and security
rereview are required. No live-artifact gate is authorized.

`REVISE-AND-REREVIEW`
