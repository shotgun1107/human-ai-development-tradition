# S0 PUBLIC Windows Authenticode verifier implementation candidate v0.1

This directory contains the first runnable PUBLIC verifier implementation for
the selected Visual Studio Build Tools bootstrapper. It replaces the
design-only v0.2 trust-profile path with authenticated Python source,
deterministic semantic evaluation, and a Windows ctypes collector.

## Implemented flow

The public entry point authenticates an externally pinned 12-row outer
implementation manifest. That manifest closes four separate source
authorities:

- one policy-contract source;
- one native Windows collector source;
- three semantic-validator sources; and
- three runtime-orchestrator sources.

Only after those bytes authenticate may the collector receive an already open
file handle. The collector:

1. confirms that the handle resolves to the requested absolute path outside
   the repository;
2. records file ID, volume serial, reparse status, length, and SHA-256 from the
   retained handle;
3. snapshots local-machine Root, CA, and Disallowed certificates and CTLs;
4. calls `WinVerifyTrust` with retained state and no WinTrust revocation
   authority;
5. extracts signer and timestamp signer by fixed zero indexes;
6. rebuilds both chains with one exact `CertGetCertificateChain` path;
7. applies Authenticode, Microsoft-root, and Authenticode timestamp policies;
8. records verification/reference times and per-element Windows revocation
   freshness ages;
9. repeats the trust snapshot, closes WinTrust state, and rehashes the same
   handle; and
10. emits one canonical non-authoritative observation.

The semantic validator then computes 39 ordered relations from those exact
bytes. It does not accept relation booleans from the native collector. Its
trace hash is bound into the derived decision. Every decision keeps
`process_authority_granted=false`; a pass means only
`PASS-TRUST-POLICY-FOR-LATER-GATE-CONSIDERATION`.

## Microsoft supplier criterion

The implementation uses the user-authorized project criterion
`PROJECT-APPROVED-MICROSOFT-DISTRIBUTION-COMPOSITE-1`:

- exact fixed Microsoft-operated URL;
- generic Authenticode success;
- normal Authenticode policy on the rebuilt signer chain;
- Microsoft-root policy on that same chain with flags zero;
- code-signing EKU;
- mandatory timestamp policy;
- hard-fail revocation and effective trust/disallowed state.

This is explicitly a project acceptance criterion. The implementation does
not claim that Microsoft documents `CERT_CHAIN_POLICY_MICROSOFT_ROOT` as a
Microsoft leaf-publisher identity guarantee. No static subject, issuer,
certificate, CA, key-size, or digest-algorithm pin is used.

## Evidence boundary

The PUBLIC synthetic suite exercises byte authentication, canonical parsing,
all-positive evaluation, manifest substitution, observation substitution,
event reordering, provider-state substitution, chain-context substitution,
timestamp-index and time substitution, stale/unknown revocation, supplier
criterion mutation, file/URI drift, trust-state drift, process-count drift,
and deterministic fail-close behavior.

The suite intentionally supplies an invalid handle to the live entry point so
no Windows native verification, trust-store query, network retrieval, file
download, or candidate execution occurs during this gate.

No real executable signature, Microsoft publisher identity, CRL/OCSP result,
trust-store state, external pin closure, build, runtime materialization,
platform behavior, rehearsal, S0, or E0 result is claimed.

