# S0 v0.14 Windows Authenticode trust profile revision v0.2

## 1. Scope and authority

This package is the bounded PUBLIC v0.2 successor to the authenticated v0.1
candidate and its independent review. It repairs only findings
`BRM-AUTH01-IR-001` through `BRM-AUTH01-IR-005`.

Authenticated predecessor facts:

- handoff commit:
  `2cb57954c92199dd92af84b8b510b38e3444bebd`;
- handoff tree:
  `0b325f0b54f2f2315cee167d05ceffc51f000f2c`;
- recovery v0.2 package-manifest SHA-256:
  `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`;
- recovery v0.2 review-record SHA-256:
  `3cb76b0d2da2e303efb6f1a8353946180ca3c5d962ba9983747cfa67ad064f80`;
- v0.1 trust-profile package-manifest SHA-256:
  `6105b0ec246318e69ae189fcf686fa0266d18ea06c58039c07c9bca100f49bee`;
  and
- v0.1 independent-review SHA-256:
  `a46c0cd2aa0e90aeaca7070577fbbb68a1982a9bfa6c6f1408f006bfe8508406`.

No F0 content, executable, certificate, trust store, CRL, OCSP response, or
signature-bearing candidate was opened. No download, native API, network,
process, installer, build, runtime, rehearsal, S0, or E0 action occurred.

## 2. Review response

| Finding | v0.2 disposition |
|---|---|
| `BRM-AUTH01-IR-001` | Replaces the accepting observation with a non-authoritative raw observation, a separately derived decision, exact profile/verifier/semantic bindings, retained file identity, ordered provider-state and rebuilt chains, effective trust-state observations, and 33 mandatory external semantic relations. |
| `BRM-AUTH01-IR-002` | Requires generic Authenticode success, normal Authenticode chain policy, code-signing EKU, and Microsoft-root policy on the same signer chain, with test roots disabled. The fixed Microsoft-operated URL remains a separate required input. |
| `BRM-AUTH01-IR-003` | Selects one revocation authority: separate `CertGetCertificateChain` calls for signer and timestamp chains. It also requires provider-state timestamp extraction and `CERT_CHAIN_POLICY_AUTHENTICODE_TS`. |
| `BRM-AUTH01-IR-004` | Enumerates signer, intermediate, root, timestamp authority/chain, algorithm, chain-time, revocation, and trusted/disallowed-authority constraints with an explicit agile replacement or preserved property. |
| `BRM-AUTH01-IR-005` | Binds the exact handoff commit and tree, v0.1 candidate/review identities, and predecessor manifest hashes in the exact-value profile schema. |

These are author dispositions pending independent review. They are not closed
findings.

## 3. Evidence and decision separation

The raw provider-observation schema intentionally has no acceptance field. It
can represent success or failure returns, absent timestamps, arbitrary chains,
and failed policy calls without turning those observations into authority.

The derived decision binds:

1. the independently authenticated profile package-manifest hash;
2. a separately approved verifier implementation-manifest hash;
3. the raw observation hash;
4. the exact semantic-contract hash;
5. the semantic-validator implementation-manifest hash; and
6. the semantic-validator output hash.

Its 33 relation results are ordered and complete. A positive trust-policy
result requires every relation to be true. A rejection requires at least one
false relation. Even the positive result is named
`PASS-TRUST-POLICY-FOR-LATER-GATE-CONSIDERATION`; the schema always keeps
`process_authority_granted` false.

Schema validity is therefore structural evidence only. The authenticated
semantic validator must compute every equality and policy relation from the
bound raw observation. Self-asserted relation booleans are not sufficient.

## 4. Same-file and same-state binding

The future verifier must use a fresh `CREATE_NEW` destination outside the
repository and retain one open file handle. It records volume serial, file ID,
reparse status, byte length, and SHA-256 at download close, after signature
verification, and immediately before the later execution boundary.

The semantic validator requires all three file identities, lengths, and hashes
to agree. It also requires the signer leaf to equal chain position zero and the
ordered chain extracted from retained WinTrust provider state to equal the
ordered chain rebuilt by the approved chain procedure. The same rules apply to
the timestamp countersigner and timestamp chain.

`WTD_STATEACTION_CLOSE` occurs only after extraction and policy inputs are
captured. Exact `LONG` zero is required for both the generic verify result and
the close result. Any inconsistency rejects before process count can change
from zero.

## 5. Microsoft supplier assurance composition

The v0.2 proposal uses all of the following on one bound signer chain:

- the exact fixed Microsoft-operated Build Tools URL and zero redirects;
- `WINTRUST_ACTION_GENERIC_VERIFY_V2` with exact `LONG` zero;
- `CERT_CHAIN_POLICY_AUTHENTICODE` with `dwError == 0`;
- code-signing EKU;
- `CERT_CHAIN_POLICY_MICROSOFT_ROOT` with `dwError == 0`; and
- Microsoft-root policy flags zero, so the test-root flag is never enabled.

`CERT_CHAIN_POLICY_MICROSOFT_ROOT` is not treated as complete validation. It is
only the supplier-specific component layered on normal Authenticode
validation, same-chain binding, exact source selection, timestamp validation,
revocation, and effective Windows trust/disallowed authority.

This composition replaces static subject, issuer, certificate, CA, key-size,
and algorithm pins. Independent review must decide whether the composition
preserves the recovery v0.2 Microsoft-supplier property without silently
widening authority.

## 6. One revocation path and mandatory timestamp

WinVerifyTrust uses `WTD_REVOKE_NONE`; its result is not the revocation
evidence. The sole authoritative revocation route is a separate
`CertGetCertificateChain` call for each of the signer and timestamp chains,
using:

- `HCCE_LOCAL_MACHINE`;
- `CERT_CHAIN_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT`;
- `CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT`;
- an accumulative URL-retrieval timeout of 10,000 ms;
- no cache-only flag;
- no candidate additional store; and
- no ignored, offline, unknown, unchecked, stale, or soft-fail disposition.

A fresh cached response may be used; the design does not falsely claim that a
network fetch occurred. The future observation records retrieval source,
freshness, update interval, trust status, and revocation disposition for every
non-root element. Each root must instead be trusted by the selected Windows
authority and absent from the effective Disallowed authority.

A timestamp is mandatory even when generic WinVerifyTrust succeeds. The
countersigner must come from the same retained provider state, its rebuilt
chain must match, and `CERT_CHAIN_POLICY_AUTHENTICODE_TS` must return
`dwError == 0`. Both RFC 3161 and legacy Authenticode countersignatures remain
algorithm-agile when Windows policy accepts them.

## 7. Effective trust authority

The selected scope is the local-machine chain engine, local-machine Root and
CA stores, chain-engine retrieval, and the effective Windows Disallowed
authority. The future verifier must canonically hash that authority before
verification and again immediately before emitting the derived decision, and
reject drift. The second value is the raw schema's post-verification snapshot.

The package does not claim that Windows automatic trust updates are disabled.
It forbids candidate or verifier mutation and requires observed pre/post
equality. The exact snapshot implementation and its binding to recovery v0.3
remain unresolved and block operational use.

## 8. Recovery v0.2 compatibility

The profile JSON contains the complete ordered conflict inventory. Identity,
certificate-chain, root, timestamp-authority, and digest-algorithm pins are
replaced by supported Windows trust-policy composition and observation-only
certificate evidence. Chain-time, revocation, and trusted/disallowed-authority
properties are preserved and made explicit rather than discarded.

Recovery v0.3 must adopt an independently reviewed form of these replacements.
It must also authenticate the verifier implementation and semantic validator
before any acquired file can be considered.

## 9. Status and maximum claim

Status:

`BLOCKED-REQUIRES-RECOVERY-V0.3-ALIGNMENT-AND-VERIFIER-IMPLEMENTATION`.

Maximum claim: v0.2 is a PUBLIC, nonexecuting revision candidate that specifies
an exact evidence/decision boundary and a reviewable Windows API composition.
It is not an implemented verifier, authenticated executable, trust-store
snapshot, external pin, installation, build, runtime, rehearsal, S0, or E0
result.

The next candidate gate after publication is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE TRUST PROFILE V0.2 INDEPENDENT REVIEW OPEN`
