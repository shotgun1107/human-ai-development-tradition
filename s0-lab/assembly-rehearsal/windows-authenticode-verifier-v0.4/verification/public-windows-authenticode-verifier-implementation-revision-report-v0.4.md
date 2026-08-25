# S0 PUBLIC Windows Authenticode verifier implementation revision report v0.4

## 1. Scope and authenticated pins

Opened gate:
`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.4 REVISION OPEN`.

This report records the bounded v0.4 code revision after preservation of the
v0.3 independent code and security rereview. It preserves v0.3 unchanged and
adds a separate v0.4 candidate.

- revision base: `2b62f1b6cc0b6da6e25e7bc14931252eb56829e8`;
- reviewed v0.3 candidate commit:
  `b441db0379f7bef4f24384a7001e2c82df2813d5`;
- reviewed v0.3 candidate tree:
  `71319ee002dc99400669172f4b3d94335caae524`;
- preserved v0.3 rereview Markdown SHA-256:
  `d90452a74a352c76b3b33fae7d4487f11007ab9004e903c5c5b53740d2f98d1d`;
  and
- preserved v0.3 rereview sidecar SHA-256:
  `0eb0ca4ea9867f397d376e5b6ec7cab3b4df78d42999d501f40ec1ed7189eac8`.

The preserved verdict is `REVISE-AND-REREVIEW` with one blocking finding,
`BRM-AUTHV03-IR-001`. This report records author-side revision evidence, not
independent closure.

## 2. Role separation

CONTROL froze the gate, pins, allowlists, role assignments, and authenticated
handoff facts. CODE IMPLEMENTATION changed only the v0.4 implementation
candidate. TEST/VERIFICATION authored and ran the focused tests and prepared
the manifest-bound verifier. DOCUMENTATION owns this report, response, README,
manifests, and sidecars. A fresh INDEPENDENT REVIEW and the final CONTROL
decision remain pending.

## 3. Implemented revision

### Immediate chain-context ownership

The candidate establishes `context_transferred = False` before the chain API
call and enters a `try` immediately after `CertGetCertificateChain` returns.
No return-time sampling or processing call occurs outside that protection.

The `finally` condition frees the context only when it is non-null and has not
been transferred. API failure with a non-null context, return-time QPC failure,
and later parsing or serialization exceptions therefore free exactly once.
API failure with a null context performs no free. A successful return marks
the context transferred, and the caller performs the one normal cleanup.

This is the v0.4 response to `BRM-AUTHV03-IR-001`.

## 4. Preserved boundaries and narrowed clock claim

The acquisition record, supplied handle, and private lease retain exact
volume-GUID path comparison. Producer-time path truth remains an external
CONTROL assertion; the package neither authenticates nor executes that
producer.

QPC remains the monotonic authority for duration and freshness. UTC and QPC
endpoint divergence beyond the two-second tolerance rejects. A fully
cancelling intermediate wall-clock excursion is not observable from endpoint
samples, and this revision does not claim otherwise.

The private read lease, mandatory WinTrust CLOSE, exceptional certificate and
CTL ownership, inert import, trusted-host-only disk scope, and executed-code,
effective-trust, process, and live-authority nonclaims remain in place.

## 5. Source authority

The v0.4 outer implementation manifest has 14 canonical rows and SHA-256:
`ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c`.

It closes five subordinate manifests with row counts `1 / 1 / 1 / 3 / 3`
and covers each of the nine implementation sources exactly once. Seven source
files are byte-identical to v0.3. Corrected v0.4 `authority.py` has SHA-256
`8e0bb2f2bc8b4bc9741ba8ebd94fdb3292fef9723e72be533e8e98167b7ea430`,
and v0.4 `win32.py` has SHA-256
`2bcfff0b3fffe9785de1e8574e7bf6eb0bbb81a776d00974e274ea0bf3a4856a`.

The initial manifest-bound checkpoint found that `authority.py` still used the
v0.3 namespace for its base and six derived manifest or package paths. CODE
moved that base to v0.4; an exact search across the nine implementation files
then reported zero stale v0.3 namespace literals. This is authenticated CODE
handoff evidence. The final manifest-bound TEST rerun remains pending.

## 6. Focused TEST evidence

The TEST role directly ran:

`python -I -B -m unittest discover -s s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.4/tests -v`

Result: 23 tests run, 21 passed, 2 skipped, and zero failures or errors. Test
SHA-256 is
`dd566feef30f3f6db7eb5aa123472d1a413f69c80e37cb5123d676b2569100e0`.

The focused evidence covers post-return QPC failure free-once, API failure
with non-null free-once, null no-free, parsing failure free-once without
double-free, successful transfer followed by caller cleanup once, and the AST
ownership-guard assertion.

The run produced no bytecode and invoked no live native, certificate-store,
network, build, or candidate-process operation. This direct result predates
the `authority.py` namespace correction, and no tests have been rerun after
that CODE change. The final manifest-bound verifier remains explicitly
pending for the TEST role after documentation completion.

## 7. Status and nonclaims

Implementation status:
`PUBLIC-V0.4-REVISION-CANDIDATE-AWAITING-MANIFEST-BOUND-VERIFICATION-AND-FRESH-INDEPENDENT-CODE-AND-SECURITY-REREVIEW`.

No real acquisition record, signature, certificate, timestamp, revocation
response, Windows trust state, network response, installer, build, candidate
process, runtime materialization, live assembly, rehearsal, F0 role, S0, or E0
evidence was produced. No live-artifact gate is authorized.
