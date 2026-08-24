# S0 PUBLIC Windows Authenticode verifier implementation candidate report v0.1

## 1. Scope

This report records the bounded PUBLIC implementation opened by the user's
instruction to proceed with Authenticode defect correction and verifier
implementation. It is a code implementation result, not another design
baseline.

The implementation branch is based on v0.2 independent-review preservation
commit `2709a46faf5502e96c24bc7731e201398042b6b6`. The reviewed v0.2 package
manifest has SHA-256
`315f89b1b13151ab9abe2aaff7ae64d23afa959ace8bd37f52ec4e872cc807c0`.
The independent review has SHA-256
`f3e738c3d1bee80014b033e16681cadfdb1847087aa84ac855ee089bc26c7a45`
and verdict `REVISE-AND-REREVIEW` with three blocking findings.

## 2. Implemented corrections

### `BRM-AUTH02-IR-001`

The runtime entry now authenticates one externally supplied outer
implementation-manifest pin before native collection. Four subordinate
manifests independently close policy, native collector, semantic validator,
and orchestrator sources.

The native observation carries all four authenticated manifest hashes. The
semantic validator recomputes the observation SHA-256 from canonical input
bytes, cross-checks every observation authority copy, computes all relation
booleans itself, serializes the exact semantic trace, and binds that trace hash
into the decision. The caller cannot inject an acceptance field or relation
array into the raw observation.

### `BRM-AUTH02-IR-002`

The collector records a 13-event sequence at the actual call sites. Events
from WinTrust return through state close share one provider-state identifier.
Signer and timestamp signer use fixed signer/countersigner indexes.

Every chain call records and hashes the exact leaf, chain engine, flags,
requested EKU, 10-second cumulative retrieval timeout, no-additional-store
setting, timestamp `pTime`, reference time, and rebuilt output chain. Every
policy call binds its exact policy ID, chain-context digest, verification time,
flags, and extra-policy input.

The chain builder enables Windows freshness checking with a project maximum
age of 86,400 seconds. Every non-root element must carry Windows
`fHasFreshnessTime`, an age within that maximum, the exact recorded reference
time, zero trust error, and good revocation result. Roots must have zero trust
error and no explicit-disallow observation.

### `BRM-AUTH02-IR-003`

The user-authorized implementation criterion is the exact Microsoft-operated
URL plus generic Authenticode, same-chain Authenticode policy, same-chain
Microsoft-root policy with test roots disabled, code-signing EKU, mandatory
timestamp policy, hard-fail revocation, and stable effective trust authority.

The source contains the exact negative claim
`official_leaf_guarantee_claimed=false`. It does not reinterpret the Microsoft
root policy as an official Microsoft leaf-publisher guarantee and introduces
no static certificate or algorithm pin.

## 3. Native implementation

The Windows adapter defines and uses the documented `WINTRUST_DATA`,
`WINTRUST_FILE_INFO`, `CRYPT_PROVIDER_SGNR`, `CRYPT_PROVIDER_CERT`,
`CERT_CHAIN_PARA`, `CERT_CHAIN_CONTEXT`, `CERT_SIMPLE_CHAIN`,
`CERT_CHAIN_ELEMENT`, `CERT_REVOCATION_INFO`, and chain-policy structures.

Its live path uses:

- `GetFinalPathNameByHandleW`, `GetFileInformationByHandleEx`,
  `GetFileSizeEx`, and a same-object duplicate for hashing;
- `WinVerifyTrust`, `WTHelperProvDataFromStateData`, and
  `WTHelperGetProvSignerFromChain`;
- `CertGetCertificateChain` for signer and timestamp chains;
- `CertVerifyCertificateChainPolicy` for Authenticode, Microsoft root, and
  Authenticode timestamp policies; and
- read-only local-machine certificate and CTL enumeration for before/after
  trust-state snapshots.

The live entry never executes the candidate file. Native ambiguity is
converted to a malformed non-authoritative observation and a deterministic
`REJECTED-BEFORE-PROCESS` decision.

## 4. PUBLIC synthetic verification

Direct focused execution passed 13 tests with zero failure, error, or skip.
The tests cover the three preserved findings and hostile mutations across
authority hashes, canonical bytes, state chronology, chain/policy inputs,
timestamp indexes, time and freshness, supplier criterion, file identity,
URI, trust snapshots, and process authority.

The 12-row outer implementation manifest has SHA-256
`11e2f27fc4993f8b60bca17852f2112fb1d20c901b7044572deb325147cafc6f`.
The authenticated-snapshot verifier passed the outer manifest, all four
submanifests, the exact v0.2 trust-profile and recovery manifests, both
preserved reviews, static authority separation, all 13 focused tests, and the
original-input swap sentinel.

No test called a Windows trust API, opened a certificate store, accessed a
network, downloaded a file, or invoked a candidate process.

## 5. Status and nonclaims

Implementation status:
`PUBLIC-CANDIDATE-IMPLEMENTED-AWAITING-INDEPENDENT-CODE-AND-SECURITY-REVIEW`.

No actual bootstrapper, signature, certificate, timestamp, revocation
response, Windows trust state, build, runtime, live assembly, rehearsal, F0,
S0, or E0 evidence was produced. `process_authority_granted` remains false for
every result in this gate.
