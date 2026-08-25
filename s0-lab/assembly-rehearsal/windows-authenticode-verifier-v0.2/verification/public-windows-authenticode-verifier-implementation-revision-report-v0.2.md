# S0 PUBLIC Windows Authenticode verifier implementation revision report v0.2

## 1. Scope

This report records the bounded v0.2 code revision opened after preservation
of the v0.1 independent code and security review. It preserves the reviewed
v0.1 namespace unchanged and adds a separate v0.2 implementation candidate.

Revision base and preserved review commit:
`ade0e1636ba483b9f8e3f465421a2c47cf1f1e33`.

Preserved review SHA-256:
`e72fe7ce12e2182b5ca45e07f698083afb9672bf7b0c70ef6429d42dc55826f9`.

The preserved verdict is `REVISE-AND-REREVIEW` with six blocking findings.
This document records author-side responses, not independent closure.

## 2. Implemented revisions

### Acquisition provenance and immutable bytes

The entry requires an externally pinned canonical acquisition record and the
producer-manifest pin. The record binds fixed request/final URL, zero
redirects, transfer completion, same-process retained handle, a read-only
handle contract, file identity, length, and SHA-256.

The collector opens a verifier-owned `GENERIC_READ` lease with only
`FILE_SHARE_READ`. This conflicts with existing write/delete access and
writable mappings and denies later write/delete opens while the lease is
active. The collector compares acquisition, supplied handle, and lease
identity and hash. WinTrust and all subsequent measurements use the lease.
Hashing uses direct `ReadFile` calls and no shared-pointer duplicate.

These changes are the bounded responses to `BRM-AUTHV01-IR-001` and
`BRM-AUTHV01-IR-003`.

### Native resource lifecycle

The first VERIFY call is inside cleanup before its state handle is inspected.
Every VERIFY attempt therefore issues CLOSE, including null-state and later
failure paths. A nonzero CLOSE result rejects.

Every returned certificate-chain context is freed locally on parsing or call-
record failure. Only a fully built record transfers ownership to the outer
lifecycle, which frees it before WinTrust state close.

These changes respond to `BRM-AUTHV01-IR-002`.

### Observed trust inputs and explicit nonclaim

The mutation sentinel now enumerates local-machine Root, CA, My, Trust,
AuthRoot, and Disallowed certificates and CTLs. Enumeration accepts only
`CRYPT_E_NOT_FOUND` as the terminal status. Other errors, oversize inputs,
entry-count overflow, and store-close failure reject.

The sentinel is not represented as a complete effective trust namespace:
`effective_trust_authority_claimed=false`. Chain results, revocation,
explicit-disallow state, root trust, and all policy results remain separately
mandatory. A private authenticated chain-engine namespace remains future live-
authority work.

This is the bounded response to `BRM-AUTHV01-IR-004`.

### Executed-code authority nonclaim

Package import is inert. The revision also accepts that a mutable Python host
cannot establish its own already executing code authority from later disk
hashes. The result therefore fixes:

- `runtime_authority_scope=TRUSTED-HOST-DISK-CONSISTENCY-ONLY`;
- `executed_code_authority_established=false`;
- terminal pass to
  `PASS-BOUNDED-TRUSTED-HOST-CONSISTENCY-NO-LIVE-AUTHORITY`; and
- `process_authority_granted=false`.

This narrows the claim as permitted by the required correction for
`BRM-AUTHV01-IR-005`. A separately pinned pre-import loader, interpreter,
immutable source snapshot, and isolated process remain future work.

### Revocation time interval

The asserted exact reference time was removed. Each chain call records fixed-
hex FILETIME values for call start, return, certificate verification time, and
the exact cache-resync input. Intervals must be monotonic and at most 30
seconds. Every non-root Windows freshness age plus the full call interval must
remain within 86,400 seconds.

This conservatively covers any instant Windows could have used during the
call without claiming an undocumented exact returned time. It responds to
`BRM-AUTHV01-IR-006`.

## 3. Additional defect corrected

The revision found that actual 64-bit Windows FILETIME values exceed the
canonical codec's exact JSON integer range. Small v0.1 synthetic values hid
the issue. All v0.2 FILETIME values are fixed lowercase 16-hex text and are
converted to integers only for bounded arithmetic.

## 4. Source authority and bounds

The v0.2 outer implementation manifest has 14 canonical rows and SHA-256:
`6fe56c7fac527b0adfda02e32e0e4b5355ff4adfe8a499732dfb7a43d2df213a`.

It closes five subordinate manifests:

- acquisition validator: one source;
- policy contract: one source;
- native collector: one source;
- semantic validator: three sources; and
- runtime orchestrator: three sources.

Explicit bounds cover candidate bytes, certificate and CTL bytes, provider
and rebuilt chain counts, store entries, observation bytes, network retrieval
time, revocation age, and chain-call duration.

## 5. PUBLIC synthetic verification

Direct isolated execution with Python bytecode disabled passed 18 tests with
zero failure, error, or skip in `0.052s`.

The suite covers:

- outer and subordinate manifest closure;
- acquisition record pin, producer authority, process, handle, URL, identity,
  and SHA-256 substitution;
- private lease contract drift;
- canonical observation hashing and all 44 ordered relations;
- VERIFY/CLOSE and chain-cleanup source structure;
- provider-state event ordering and close failure;
- signer, timestamp, chain, and policy binding;
- conservative freshness under stale, reversed, and overlong intervals;
- provider-chain bounds;
- observed trust-snapshot and effective-authority nonclaims;
- inert package import and executed-code-authority nonclaim; and
- invalid-handle fail-close behavior.

The positive synthetic result still grants no live or process authority.

## 6. Status and nonclaims

Implementation status:
`PUBLIC-V0.2-REVISION-CANDIDATE-AWAITING-FRESH-INDEPENDENT-CODE-AND-SECURITY-REREVIEW`.

No actual acquisition record, bootstrapper, signature, certificate,
timestamp, revocation response, Windows store content, network response,
build, runtime materialization, live assembly, rehearsal, F0 role, S0, or E0
evidence was produced. No native trust API, certificate-store operation,
network call, download, installer, candidate process, or build was invoked by
the suite.

Fresh independent review is required. No live-artifact gate is authorized by
this revision.
