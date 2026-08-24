# S0 v0.14 Windows Authenticode trust profile authoring v0.1

## 1. Scope

This package authors a PUBLIC, nonexecuting Windows Authenticode trust-profile
candidate for the selected Visual Studio Build Tools 17.14.39 bootstrapper.
It downloads no executable, invokes no process or native API, changes no trust
store, and supplies no build, runtime, rehearsal, S0, or E0 authority.

The authenticated recovery v0.2 package and review are the predecessor
authority:

- recovery package manifest SHA-256:
  `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`;
- recovery review record SHA-256:
  `3cb76b0d2da2e303efb6f1a8353946180ca3c5d962ba9983747cfa67ad064f80`.

## 2. New official Microsoft constraint

Microsoft support article KB 5125813, published 2026-08-20, requires
certificate and algorithm agility for Windows code-signature validation:

`https://support.microsoft.com/en-us/servicing/os/windows/docs/2026/08/next-generation-code-signing`

It warns applications not to pin certificate subject, issuer, thumbprint,
serial number, intermediate CA, key size, or digest algorithm. It directs
applications to use `WinVerifyTrust` or approved CryptoAPI chain and policy
interfaces because Microsoft is rotating signing CAs and algorithms and is
preparing for post-quantum signatures.

This current Microsoft requirement conflicts with recovery v0.2, which
requires exact signer subject, issuer, thumbprint, serial, and signature and
timestamp algorithms. The trust profile must not silently choose one
interpretation. Its status is therefore:

`BLOCKED-REQUIRES-RECOVERY-V0.3-ALIGNMENT`.

## 3. Trust decision

The permitted future trust decision is Windows trust-policy validation, not
candidate-selected certificate identity.

The procedure uses `WinVerifyTrust` with
`WINTRUST_ACTION_GENERIC_VERIFY_V2`, a noninteractive window handle,
`WTD_UI_NONE`, `WTD_CHOICE_FILE`, a retained file handle,
`WTD_STATEACTION_VERIFY`, whole-chain revocation, and an exact `LONG` return
value of zero. Every verify state is closed with `WTD_STATEACTION_CLOSE`.

The procedure must reject every warning, nonzero return, policy error,
untrusted or test root, wrong usage, expired untrusted signature, missing
timestamp, revoked certificate, unknown/offline/stale revocation result,
redirect, file-identity change, or byte-hash change.

Observed certificate hashes and chain elements are evidence outputs only.
They cannot become authority for the same file. Trust-store enrollment,
candidate-provided roots, ignored policy flags, cache-only revocation, and
soft fail are forbidden.

## 4. Timestamp and revocation

A trusted timestamp is mandatory. Windows may accept RFC 3161 or legacy
Authenticode countersignature timestamps when its Authenticode policy accepts
the signature. The profile does not hard-code a digest algorithm. Timestamp
chain policy and revocation must succeed, and the signing time must be valid
under Windows Authenticode policy.

Revocation checks cover the entire applicable chain except the root. Online
retrieval is required; `unknown`, `offline`, `unchecked`, `stale`, and
soft-fail results reject. The future evidence record preserves the observed
chain and revocation disposition without making those observations future
trust anchors.

## 5. Byte and file identity

The future acquisition role must create a fresh exclusive destination outside
the repository, follow zero redirects, close and hash the download, retain the
same file identity, verify the signature, hash again, and reauthenticate the
same file immediately before any first execution. All three hashes must be
identical. A rejected file, destination, or evidence set is burned and cannot
be retried.

## 6. Required recovery v0.3 correction

Recovery v0.3 must replace its static certificate and algorithm pins with the
exact Windows trust-API policy in this package. It must preserve:

- independent authority for the procedure bytes and policy;
- no execution before trust succeeds;
- exact fixed URL and zero redirects;
- stable file identity and SHA-256 through the first-execution boundary;
- timestamp and hard-fail revocation requirements;
- no trust-store mutation or candidate-provided root; and
- signed layout-content authentication after bootstrapper verification.

Until that revision passes independent review, bootstrapper process count
remains zero.

## 7. Maximum claim

Maximum claim: this package identifies the Microsoft-supported, algorithm-
agile Windows trust-policy contract and exposes an incompatibility in recovery
v0.2. It is not a completed external pin, authenticated executable, download,
signature result, installation, build, runtime, Windows-behavior, rehearsal,
S0, or E0 result.
