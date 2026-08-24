# S0 v0.14 public build/runtime external-pin recovery acceptance plan v0.2

## 1. Review boundary

This acceptance plan reviews only the authenticated v0.1 basis and exact v0.2
revision bytes. It performs no download, signature verification against a new
artifact, trust-store mutation, process invocation, installation, source
authoring, build, materialization, platform probe, rehearsal, S0, or E0.

## 2. Authority checks

Reject unless:

1. the v0.1 package manifest and independent-review preservation record match
   their exact supplied hashes;
2. the v0.2 package manifest is canonical, complete, ordered, and exact;
3. all Markdown/sidecar pairs pass the canonical validator after SelfTest;
4. the v0.2 JSON rejects duplicate keys and preserves the exact ten-class
   order and bindings;
5. all execution and operational claim bits remain false; and
6. F0 remains aggregate-only at 32 / 11 / 10 with zero applicable changes.

## 3. Fixed-target checks

Independently obtain the official release-history row for 17.14.39 and require
the selected Build Tools link target to equal, byte for byte:

`https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe`

Reject an evergreen URL, alternate row, mirror, redirect, URL normalization,
query addition, case change, decoded alias, or candidate-provided target.

The path component that resembles a digest must not be treated as downloaded
artifact authentication.

## 4. Preexecution trust-contract checks

The contract must make process count zero unless every required item is
already authenticated from an authority independent of the downloaded file:

- verifier procedure bytes and semantic contract;
- Microsoft signer identity;
- signer certificate identity;
- full intermediate/root chain identity;
- timestamp authority and time policy;
- signature and timestamp digest algorithms;
- revocation evidence, mode, scope, and freshness;
- trust/disallowed-store snapshot or equivalent exact authority; and
- canonical evidence record schema.

`Get-AuthenticodeSignature` status text, Product Version, file hash, TLS
success, URL origin, certificate display name, or candidate-created chain
alone is insufficient.

The later procedure must require a valid embedded signature, valid
`WinVerifyTrust` result or approved equivalent, exact approved Microsoft
signer, exact chain/root, valid timestamp, good non-soft-fail revocation, and
stable bytes through the first-execution boundary.

## 5. Required adversarial mutations

The independent reviewer must prove rejection before process invocation for at
least:

1. correct Product Version on substituted unsigned bytes;
2. self-consistent attacker layout and newly generated hashes;
3. signed bytes from a non-Microsoft signer;
4. Microsoft-looking subject text with a different certificate;
5. untrusted, alternate, or candidate-added root;
6. missing or changed intermediate;
7. absent, malformed, untrusted, or invalid timestamp;
8. signing time outside applicable certificate validity;
9. revoked signer, timestamp signer, intermediate, or root;
10. revocation `unknown`, offline soft-fail, unchecked, or stale evidence;
11. ignored chain or policy error;
12. wrong signature or timestamp digest algorithm;
13. exact URL followed by a redirect or different final URI;
14. file mutation after signature verification;
15. file-identity substitution between verification and execution;
16. missing Windows Authenticode trust profile;
17. trust-store enrollment from the untrusted new layout;
18. signed layout package with an unbound extra file;
19. unsigned content absent from every authenticated signed manifest/catalog;
20. layout signature/catalog verification failure; and
21. layout size above 24 GiB.

Every mutation must terminate before first bootstrapper execution or later
layout/install/build action. A rejected attempt cannot retry with the same
file or evidence.

## 6. Finding closure rule

`BRM-EPR-V01-IR-001` closes only if the reviewer independently establishes all
of the following:

- exact fixed link target binding;
- no bootstrapper execution before supplier authenticity;
- trust values cannot be learned from and approved by the candidate itself;
- signature, chain, signer, timestamp, and revocation requirements are
  complete and fail closed;
- byte and file identity remain stable through first execution; and
- signed layout-content verification remains mandatory after bootstrapper
  authentication.

Any ambiguity is at least MAJOR because it can admit attacker-controlled code
before layout hashes become evidence.

## 7. Verdict boundary

A passing review may support only:

`PASS-FOR-PUBLIC-EXTERNAL-PIN-RECOVERY-TRUST-PROFILE-CONSIDERATION-ONLY`.

It must not authorize acquisition, download, trust-store mutation,
bootstrapper execution, source authoring, installation, build, runtime
materialization, platform testing, rehearsal, S0, or E0.
