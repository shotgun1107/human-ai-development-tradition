# S0 v0.14 public build/runtime external-pin recovery plan revision v0.2

## 1. Revision authority and scope

This package is the bounded PUBLIC v0.2 revision of the authenticated v0.1
external-pin recovery selection. It responds only to preserved finding
`BRM-EPR-V01-IR-001`.

The revision base is:

- v0.1 package-manifest SHA-256:
  `2be3d8428502a5aeb92cbf4253ce3ec6dc39071aacc35f36b12f707ab5d8dc8e`;
  and
- v0.1 independent-review preservation-record SHA-256:
  `69be977790a8ed3d7288d6fe03655a94997770f6fe70b9b6a60c8880fcaaf070`.

All v0.1 selections and nonclaims remain effective except where this revision
explicitly strengthens the Build Tools bootstrapper authentication and
preexecution order.

No artifact was downloaded, installed, opened as a candidate executable,
compiled, linked, inspected, materialized, loaded, or executed while producing
this revision.

## 2. Preserved finding

The v0.1 review returned `REVISE-AND-REREVIEW` with one MAJOR finding. The
selection identified Build Tools by release labels and recorded a newly
downloaded executable's hash, but it did not authenticate Microsoft origin
before invoking that executable to create the layout.

A substituted executable could therefore self-report the selected version,
create attacker-chosen layout bytes, and receive internally consistent new
hashes. Hashing supplied identity without supplier authenticity.

## 3. Exact fixed bootstrapper target

The v0.2 selection binds the Build Tools link target from the official
Microsoft Visual Studio 2022 release-history row for fixed release 17.14.39,
build `17.14.37614.0`, dated 2026-08-18:

`https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe`

An evergreen link, alternate release-history row, URL shortener, mirror,
redirect, query variation, case variation, normalization-equivalent string,
or another final URI is not the selected target.

The URL path's digest-looking component is not treated as an authenticated
file hash. The downloaded byte hash remains unavailable until acquisition.

## 4. Approved trust-profile prerequisite

Bootstrapper authenticity depends on a separately authenticated Windows
platform trust profile. That profile is part of the existing
`external_pin_closure.windows_platform` authority and must bind exact:

- permitted Authenticode verification procedure and implementation bytes;
- Microsoft code-signing signer subject, issuer, thumbprint, and serial;
- every permitted intermediate and root certificate identity and thumbprint;
- permitted Authenticode and timestamp digest algorithms;
- permitted RFC 3161 or Authenticode countersignature timestamp authority;
- chain policy, verification time policy, revocation mode and scope;
- trusted and disallowed certificate-store snapshots or equivalent exact
  inputs; and
- required evidence-record schema and canonical serialization.

The acquisition role cannot discover these values from the downloaded
bootstrapper and then approve them. A candidate-selected signer, chain, root,
timestamp authority, verification flag, or trust-store state is rejected.

The current trust-profile status remains
`BLOCKED-MISSING-EXTERNAL-PIN`. Consequently, bootstrapper process count must
remain zero in v0.2.

## 5. Mandatory preexecution sequence

The only permitted future acquisition sequence is:

1. authenticate the complete v0.2 recovery package and the separately pinned
   Windows Authenticode trust profile;
2. require a fresh absent out-of-repository destination and create the
   bootstrapper file exclusively;
3. request only the exact fixed HTTPS URL and reject every redirect or final
   URI difference;
4. close the download, record byte length and SHA-256, and reopen only through
   the originally retained acquisition identity permitted by the later
   acquisition design;
5. verify an embedded Authenticode signature without executing the file;
6. require `WinVerifyTrust` or the separately approved equivalent procedure to
   return valid with no ignored verification error;
7. require signer identity, full chain, trusted root, timestamp signer,
   timestamp value, signature algorithms, and policy to equal the approved
   trust profile;
8. require good revocation disposition for the signer, timestamp signer, and
   entire applicable chain; `unknown`, `offline`, `unchecked`, `stale`, and
   soft-fail dispositions reject;
9. hash the file again and require exact byte identity with the closed download;
10. immediately before first execution, reauthenticate the same file identity,
    signature evidence, chain evidence, revocation evidence, timestamp evidence,
    and SHA-256; and
11. only then permit one bounded bootstrapper invocation to create the selected
    offline layout.

Any failure produces `REJECT-BEFORE-PROCESS`. No retry may reuse the file,
destination, trust evidence, or output layout.

## 6. Layout-content authenticity

An authenticated bootstrapper is necessary but not sufficient. A later
acquisition gate must record and verify:

- the exact fixed channel and catalog manifests selected by the bootstrapper;
- every signed package, executable, archive, cabinet, manifest, and catalog;
- Authenticode or catalog signature evidence where applicable;
- signer and chain equality with the approved layout-content trust profile;
- exact target paths, byte lengths, hashes, count, aggregate bytes, and
  target-set hash;
- the component- and language-limited closure;
- the bootstrapper's authenticated `--verify` result after layout completion;
  and
- the inherited 24 GiB hard ceiling.

Unsigned content is accepted only when an authenticated Microsoft-signed
manifest or catalog binds that exact content hash and path. Unbound, extra,
mutable, stale, or unverifiable content rejects.

Certificates obtained from the newly created layout cannot retroactively
authenticate the bootstrapper that created that layout. Automatic trust-store
enrollment or mutation is forbidden in the acquisition gate.

## 7. Finding disposition

The v0.2 author disposition is:

`BRM-EPR-V01-IR-001: CLAIMED-CLOSED-BY-V0.2-REVISION-PENDING-INDEPENDENT-REVIEW`.

The disposition rests on three changes:

1. the exact fixed Microsoft link target is now frozen;
2. supplier authenticity and trust evidence are mandatory before any process;
   and
3. absent or unverifiable trust authority stops with process count zero.

Only a fresh independent review may close the finding.

## 8. Remaining unavailable work

The following remain unavailable and are not repaired or opened here:

- all eight complete external manifest identities;
- the Authenticode trust profile itself;
- native source and materializer/inspector source;
- full Python dependency closure;
- runtime-tree profile;
- artifact download and offline layout creation;
- installation, compiler, linker, inspector, materializer, or build execution;
- native binary, platform behavior, runtime materialization, rehearsal, S0,
  and E0.

## 9. Maximum claim and next gate

Maximum claim: v0.2 is a PUBLIC, nonexecuting recovery-plan revision that
freezes an exact Build Tools target and makes preexecution Authenticode trust
evidence mandatory. It is not an authenticated bootstrapper, trust profile,
external pin bundle, build, runtime, or platform result.

The next permissible gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.2 INDEPENDENT REVIEW OPEN`

That review must not download, install, execute, build, materialize, or access
F0 content.
