# S0 PUBLIC Windows Authenticode verifier implementation revision report v0.3

## 1. Scope

This report records the bounded v0.3 code revision opened after preservation
of the v0.2 independent code and security rereview. It preserves the reviewed
v0.2 namespace unchanged and adds a separate v0.3 candidate.

Revision base and v0.2 rereview-preservation commit:
`ad36069581816416dec5cc970962289701f51de7`.

Preserved v0.2 rereview SHA-256:
`c8fdb45ba2fde477e5a1662e28131a388ec1cce637313e2508b5e40c2d369eee`.

The preserved verdict is `REVISE-AND-REREVIEW` with three blocking findings.
This report records author-side corrections, not independent closure.

## 2. Implemented revisions

### Acquisition path binding

The acquisition schema now binds the exact volume-GUID final path produced by
`GetFinalPathNameByHandleW(FILE_NAME_NORMALIZED | VOLUME_NAME_GUID)` and a
versioned path-semantics identifier.

The grammar rejects non-volume-GUID form, ADS, slash ambiguity, nulls,
wildcards, empty and dot segments, and trailing-space/dot normalization. The
collector obtains the same final path from the retained handle and private
lease. Acquisition, handle, and lease paths must be exact equal, so caller-
selected aliases cannot replace the acquisition authority path.

This responds to `BRM-AUTHV02-IR-002`.

### Exceptional certificate and CTL context cleanup

The native adapter now declares `CertFreeCertificateContext` and
`CertFreeCTLContext`. Store enumeration keeps the current returned context
under explicit ownership. Any processing exception frees that context before
store close.

Cleanup attempts certificate free, CTL free, and store close even if one
operation reports failure, then rejects. Fake-API tests count all cleanup
calls on successful and failed context-free paths.

This responds to `BRM-AUTHV02-IR-001`.

### QPC monotonic freshness interval

Every chain call now records fixed-hex QPC frequency, start, and return values
alongside UTC FILETIME values. Duration and freshness margin use the ceiling
of QPC elapsed time.

The semantic validator cross-checks UTC and QPC elapsed time with exact
integer arithmetic and a two-second tolerance. UTC or QPC reversal, duration
overrun, and a backward-then-recovering UTC discontinuity reject.

This responds to `BRM-AUTHV02-IR-003` while preserving fixed-hex serialization
outside the JSON exact-integer range.

## 3. Preserved security boundaries

The v0.2 corrections remain present:

- externally pinned acquisition record and producer manifest;
- verifier-owned `GENERIC_READ`/`FILE_SHARE_READ` lease;
- mandatory WinTrust CLOSE and bounded chain ownership;
- bounded store, chain, certificate, CTL, candidate, and observation inputs;
- inert package import;
- `TRUSTED-HOST-DISK-CONSISTENCY-ONLY` runtime scope;
- `effective_trust_authority_claimed=false`;
- `executed_code_authority_established=false`; and
- `process_authority_granted=false`.

A positive result remains bounded no-live-authority evidence only.

## 4. Source authority

The v0.3 outer implementation manifest has 14 canonical rows and SHA-256:
`f44e1d3f37cd122c0b619fa31080f1d759050d8932dc8e75cdc3861441e4dc1d`.

It closes five subordinate manifests:

- acquisition validator: one source;
- policy contract: one source;
- native collector: one source;
- semantic validator: three sources; and
- runtime orchestrator: three sources.

## 5. PUBLIC synthetic verification

Direct isolated execution with Python bytecode disabled passed 18 tests with
zero failure, error, or skip in `0.061s`.

The suite covers all 44 semantic relations and includes:

- volume-GUID acquisition path grammar and path substitution;
- acquisition, handle, lease, file identity, and SHA-256 binding;
- explicit exceptional certificate/CTL context cleanup counts;
- UTC and QPC reversal, overrun, and hidden-discontinuity cases;
- conservative freshness arithmetic;
- manifest closure and original v0.2 hostile-case regression; and
- runtime, effective-trust, executed-code, and process-authority nonclaims.

No test called a live Windows trust API or real certificate store.

## 6. Status and nonclaims

Implementation status:
`PUBLIC-V0.3-REVISION-CANDIDATE-AWAITING-FRESH-INDEPENDENT-CODE-AND-SECURITY-REREVIEW`.

No real acquisition record, bootstrapper, signature, certificate, timestamp,
revocation response, Windows trust state, network response, build, runtime
materialization, live assembly, rehearsal, F0 role, S0, or E0 evidence was
produced. No native trust API, real certificate-store operation, network call,
download, installer, candidate process, or build was invoked by the suite.

Fresh independent rereview is required. No live-artifact gate is authorized
by this revision.
