# S0 v0.14 Windows Authenticode trust profile acceptance plan v0.1

## 1. Review boundary

Review only authenticated PUBLIC profile, schemas, predecessor recovery bytes,
and official Microsoft documentation. Do not download the bootstrapper,
mutate trust stores, execute a process, or run a build, materialization,
rehearsal, S0, or E0 operation.

## 2. Authentication

Require exact package-manifest rows and hashes, canonical Markdown sidecars,
strict duplicate-key-free JSON, Draft 2020-12 schema validity, exact recovery
v0.2 package/review pins, and F0 aggregate 32 / 11 / 10 with zero change.

Independently verify Microsoft KB 5125813 and the WinVerifyTrust,
WINTRUST_DATA, CertGetCertificateChain, CertVerifyCertificateChainPolicy, and
Authenticode timestamp documentation from official Microsoft domains.

## 3. Required profile properties

The profile must:

1. delegate trust to supported Windows APIs;
2. require exact `LONG` zero from `WinVerifyTrust`;
3. use no interactive UI or candidate callbacks;
4. retain and close WinTrust state correctly;
5. require code-signing usage and a trusted timestamp;
6. hard-fail revoked, unknown, offline, unchecked, stale, or soft-fail states;
7. forbid trust-store mutation and candidate-provided roots;
8. require byte and file identity stability through first execution;
9. leave every execution and operational claim false; and
10. remain blocked until recovery v0.3 resolves the v0.2 conflict.

## 4. Required hostile mutations

Reject or remain blocked for:

- static subject, issuer, leaf thumbprint, leaf serial, intermediate, key-size,
  or algorithm pinning;
- any nonzero WinVerifyTrust result or warning;
- omitted `WTD_STATEACTION_CLOSE`;
- interactive UI, callback, custom parser, or candidate-selected policy;
- cache-only, end-certificate-only, disabled, unknown, offline, stale, or
  soft-fail revocation;
- absent, untrusted, invalid, or revoked timestamp;
- candidate root, newly enrolled root, ignored error, or test root;
- redirect, final-URI drift, reused destination, changed file ID, or changed
  byte hash;
- evidence observation reused as future authority;
- profile status changed from blocked to complete; and
- any process, download, installation, build, runtime, rehearsal, S0, or E0
  claim.

## 5. Verdict boundary

A passing review may support only:

`PASS-FOR-RECOVERY-V0.3-DESIGN-CONSIDERATION-ONLY`.

It must not authorize acquisition, signature verification of real bytes,
bootstrapper execution, installation, build, materialization, or S0/E0.
