# S0 v0.14 Windows Authenticode trust profile acceptance plan v0.2

## 1. Review boundary

Review only the authenticated PUBLIC v0.2 package, its named predecessors, and
the official Microsoft documentation listed below. Do not download or inspect
the bootstrapper, query or mutate a trust store, call a native API, invoke a
process, or perform installation, build, runtime, rehearsal, S0, or E0 work.

## 2. Package authentication

Require all of the following:

1. canonical package-manifest ordering, paths, hashes, and exact closure;
2. canonical Markdown/sidecar validation after validator SelfTest;
3. strict duplicate-key-free parsing of every JSON target;
4. Draft 2020-12 meta-schema validity for all three schemas;
5. exact profile-instance validation;
6. exact v0.1 package/review and recovery v0.2 package/review hashes;
7. exact handoff commit and tree constants; and
8. F0 aggregate `32 / 11 / 10` with zero applicable change and no content
   access.

Any manifest mismatch or extra file in the package namespace rejects the
candidate.

## 3. Official-policy reconstruction

Independently reconstruct the design from current official Microsoft pages:

- `https://support.microsoft.com/en-us/servicing/os/windows/docs/2026/08/next-generation-code-signing`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_data`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain`;
- `https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certverifycertificatechainpolicy`;
- `https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures`;
- `https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-trusted-roots-disallowed-certificates`;
  and
- `https://www.microsoft.com/pkiops/docs/repository.htm`.

Confirm that Microsoft-root policy is only one building block, performs no
complete Authenticode policy evaluation by itself, must not use the test-root
flag, and does not itself perform revocation checking.

## 4. Structural and relational tests

Use reviewer-created fake PUBLIC JSON only. Prove that:

- raw observations contain no acceptance or execution authority;
- raw success and failure observations remain representable;
- the decision schema accepts a rejection only with at least one false
  relation;
- the decision schema accepts a positive trust-policy result only with all 33
  ordered relations true;
- missing, duplicate, reordered, or unknown relation IDs reject;
- a positive result still has `process_authority_granted == false`;
- profile, verifier, observation, semantic-contract, semantic-validator, and
  validator-output hashes are all mandatory; and
- schema-valid assertions are never described as proof without the
  authenticated semantic-validator implementation.

## 5. Hostile same-file and evidence cases

The semantic contract must reject or keep blocked for:

1. unequal download, post-signature, or preexecution hashes;
2. changed volume serial, file ID, reparse status, byte length, or retained
   handle;
3. a redirect or final-URI change;
4. signer leaf unequal to provider-state chain position zero;
5. arbitrary or reordered signer chain elements;
6. provider-state signer chain unequal to rebuilt signer chain;
7. arbitrary or reordered timestamp chain elements;
8. a timestamp leaf unequal to timestamp chain position zero;
9. provider state closed before required extraction;
10. omitted close, nonzero close result, or nonzero WinVerifyTrust result;
11. substituted profile, verifier, observation, semantic contract, or semantic
    validator bytes; and
12. reused observations or certificate identities promoted into future
    authority.

## 6. Supplier, timestamp, revocation, and trust-state cases

Reject or keep blocked for:

- a Windows-trusted non-Microsoft signer;
- generic Authenticode success without normal Authenticode chain-policy pass;
- Microsoft-root policy applied to a different chain;
- Microsoft-root policy used alone;
- nonzero Microsoft-root policy error, nonzero Authenticode policy error, test
  root, absent code-signing EKU, or candidate-provided store;
- absent timestamp, invented countersigner, wrong timestamp chain, nonzero
  Authenticode timestamp-policy error, or invalid signing time;
- `WTD_REVOKE_WHOLECHAIN` or another second claimed revocation authority;
- end-certificate-only, cache-only, disabled, unknown, offline, unchecked,
  stale, soft-fail, or ignored revocation;
- missing per-element evidence for any non-root signer or timestamp-chain
  element;
- a root that is untrusted or effectively disallowed;
- changed pre/post trusted/disallowed-authority snapshot;
- candidate or verifier trust-store mutation; and
- an unimplemented or unauthenticated authority snapshot algorithm.

Fresh cache is not itself a rejection when its freshness is established and
the chain call remains network-capable. Do not require or claim an unobserved
network fetch.

## 7. Recovery conflict completeness

Compare the ordered conflict inventory with every recovery v0.2 requirement.
Require explicit coverage of signer, intermediate, root, timestamp authority,
timestamp chain/root, signature and timestamp algorithms, verification time,
revocation scope/freshness, and trusted/disallowed authority.

Reject a replacement that merely removes supplier authenticity, timestamp,
revocation, chain, or trust-state security properties.

## 8. Claim and verdict boundary

All package operational claim bits must remain false. The only passing review
verdict is:

`PASS-FOR-RECOVERY-V0.3-AND-VERIFIER-DESIGN-CONSIDERATION-ONLY`.

A pass must not authorize download, native verification, trust-store access or
mutation, bootstrapper execution, installation, build, materialization,
rehearsal, S0, or E0.
