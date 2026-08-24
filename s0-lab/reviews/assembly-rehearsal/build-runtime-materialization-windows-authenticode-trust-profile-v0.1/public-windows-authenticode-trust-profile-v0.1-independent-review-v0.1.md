# S0 v0.14 Windows Authenticode trust profile v0.1 independent review

## 1. Verdict

**Verdict:** `REVISE-AND-REREVIEW`.

Finding counts:

| Severity | Count |
|---|---:|
| BLOCKING | 3 |
| MAJOR | 1 |
| MINOR | 1 |

The candidate is candid that it is design-only and blocked on recovery v0.3,
and current Microsoft guidance does require certificate and algorithm agility.
However, the candidate cannot yet support the acceptance plan's sole passing
verdict. Its future accepted evidence can be internally inconsistent, its
selected WinVerifyTrust decision does not by itself authenticate Microsoft as
the supplier, and its mandatory timestamp and revocation rules are not fully
specified or evidenced.

## 2. Review identity and boundary

- gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE TRUST PROFILE V0.1 INDEPENDENT REVIEW OPEN`;
- role: fresh independent PUBLIC security reviewer;
- reviewed branch:
  `codex/s0-build-runtime-authenticode-trust-profile-v01-review`;
- reviewed/source commit:
  `2aaf014927b04816602b45513d1df6c7e4f83608`;
- reviewed tree: `c619bebb4624f45b6bb10b72edba9f5ab87187ad`;
- sole parent: `2cb57954c92199dd92af84b8b510b38e3444bebd`;
- parent tree: `0b325f0b54f2f2315cee167d05ceffc51f000f2c`;
- package-manifest SHA-256:
  `6105b0ec246318e69ae189fcf686fa0266d18ea06c58039c07c9bca100f49bee`;
- recovery v0.2 package-manifest SHA-256:
  `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`;
- recovery review-record SHA-256:
  `3cb76b0d2da2e303efb6f1a8353946180ca3c5d962ba9983747cfa67ad064f80`;
- official-document review date: `2026-08-24`; and
- F0 content access: none.

No executable, certificate, CRL, archive, signature-bearing candidate byte,
or trust-store content was downloaded or inspected. No native verification,
trust-store query or mutation, bootstrapper process, installation, build,
materialization, rehearsal, S0, or E0 action occurred.

## 3. Authentication and mechanical validation

Facts and test results:

- origin, branch, HEAD, source remote ref, tree, sole parent, and initially
  clean worktree/index/untracked state: PASS;
- F0 tracked aggregates: `32 / 11 / 10`; worktree, index, untracked, ignored,
  skip-worktree, and assume-unchanged anomalies: zero;
- canonical text validator read in full and SelfTest: PASS;
- candidate manifest: six canonical rows, every target hash matched, and the
  candidate namespace closed exactly at ten tracked files: PASS;
- recovery manifest: four rows and every target hash matched: PASS;
- all eight supplied Markdown/sidecar pairs: PASS;
- strict recursive duplicate-key parsing of the profile, both schemas, and
  recovery JSON: PASS; explicit top-level and nested duplicate mutations were
  rejected;
- both schemas passed Draft 2020-12 meta-schema checking, and the profile
  instance validated against its schema;
- every object-typed schema location was closed with
  `additionalProperties: false` (`11` profile-schema objects and `1`
  evidence-schema object);
- all `82` profile-schema constant mutations, `97` required-property
  omissions, and extra-property mutations at all `11` object locations were
  rejected; and
- all `11` evidence constants, all `18` required-property omissions, and an
  extra top-level property were rejected.

Those structural passes do not cure the relational and authority-binding
failures below.

## 4. Official Microsoft guidance reconstruction

The candidate is correct on the central agility question. Microsoft KB 5125813
says applications must not depend on fixed certificate names, thumbprints,
issuers, key sizes, or digest algorithms; its compatibility-risk list also
names serial numbers and intermediate CAs. It directs applications toward
WinVerifyTrust or appropriate CryptoAPI chain and policy interfaces. This
conflicts with recovery v0.2's exact signer-certificate, chain, and algorithm
pins.

The same documentation does not establish that a generic successful
Authenticode decision proves that the publisher is Microsoft. Microsoft's
WinVerifyTrust example describes generic policy as accepting a code signer
that chains to a trusted root and has a code-signing EKU or no EKU. The
CertVerifyCertificateChainPolicy documentation separately exposes Microsoft-
root and Authenticode timestamp policies. Those are documented building
blocks, not permission to reuse static certificate identities and not, by
themselves, a complete correction.

The reviewed official sources were:

- [KB 5125813: Preparing the Windows ecosystem for next-generation code signing](https://support.microsoft.com/en-us/servicing/os/windows/docs/2026/08/next-generation-code-signing);
- [WinVerifyTrust](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust);
- [WINTRUST_DATA](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_data);
- [WINTRUST_FILE_INFO](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_file_info);
- [Microsoft's embedded-signature WinVerifyTrust example](https://learn.microsoft.com/en-us/windows/win32/seccrypto/example-c-program--verifying-the-signature-of-a-pe-file);
- [CertGetCertificateChain](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain);
- [CertVerifyCertificateChainPolicy](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certverifycertificatechainpolicy);
- [Time Stamping Authenticode Signatures](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures);
- [Configure trusted roots and disallowed certificates in Windows](https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-trusted-roots-disallowed-certificates);
- [Certificates and trust management in Windows](https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/certificate-trust); and
- [Microsoft PKI repository and certificate policy](https://www.microsoft.com/pkiops/docs/repository.htm).

## 5. Findings

### BRM-AUTH01-IR-001 — BLOCKING — accepted evidence is not relationally sound or bound to the approved procedure

Fact: a schema-valid baseline evidence object remained valid after all three
artifact hashes were made different. It also remained valid when
`signer_leaf_sha256_observation` was absent from
`chain_certificate_sha256`, and when the chain array was replaced with
arbitrary unrelated hashes.

Fact: the closed evidence schema has no field for the approved profile or
implementation hash, retained file identity, WinTrust input flags, state-close
result, signer-chain policy status, timestamp signer/time/chain, per-chain
revocation status and freshness, network/cache provenance, trusted/disallowed
CTL identity, or trust-store source. Because it is closed, an implementation
cannot add those proofs while remaining schema-valid.

Inference: `decision: ACCEPTED-PREEXECUTION` and zero-valued status fields can
be self-consistent assertions rather than evidence of the required call and
byte/file-identity sequence. The schema therefore accepts the exact changed-
hash, file-swap, unbound-chain, untrusted-observation, and unsupported-success
classes that the acceptance plan requires it to reject.

Required correction: bind the record to authenticated profile and verifier
implementation bytes; represent the retained file identity; enforce equality
of download, post-signature, and preexecution hashes outside JSON Schema and
record that validator's result; bind signer and timestamp observations to the
actual retained WinTrust/chain state; record every required policy input and
status; and define an authenticated decision procedure that rejects any
cross-field inconsistency before it can emit `ACCEPTED-PREEXECUTION`.

### BRM-AUTH01-IR-002 — BLOCKING — generic Windows trust silently widens Microsoft supplier authority

Fact: recovery v0.2 requires Microsoft supplier authenticity before the first
process. The candidate replaces its exact signer pins with only
`WINTRUST_ACTION_GENERIC_VERIFY_V2`. Microsoft's documentation describes that
policy as authenticating a file under Authenticode through a trusted root and
code-signing usage; it does not say the leaf is Microsoft. The candidate has
no separate supported Microsoft-identity policy result.

Inference: a file signed by a different Windows-trusted code publisher can
satisfy the stated generic trust decision. The exact HTTPS URL is not a
substitute under the authenticated recovery threat model, which already held
that URL/TLS success alone was insufficient supplier authentication. The
proposed v0.3 resolution therefore drops a security property instead of
replacing its brittle pins with an agile supported policy.

Required correction: specify and independently review an approved Windows API
composition that preserves Microsoft supplier identity without static
certificate, CA, key, or algorithm pins. For example, the documented
`CERT_CHAIN_POLICY_MICROSOFT_ROOT` is a possible building block, but Microsoft
states that it performs no complete policy verification by itself; the final
composition must retain normal Authenticode policy, exclude test roots, bind
the observed chain to the verified signer, and fail closed.

### BRM-AUTH01-IR-003 — BLOCKING — timestamp and revocation claims exceed the specified Windows call contract

Fact: WinVerifyTrust can accept a currently valid signed file that has no time
stamp; zero means the selected trust action passed, not that a mandatory time
stamp was present. The candidate requires a timestamp and a zero timestamp
policy error but specifies neither provider-state extraction nor the
documented `CERT_CHAIN_POLICY_AUTHENTICODE_TS` path that would establish
presence, time, chain, usage, and policy status. Its evidence schema can only
self-assert `timestamp_kind` and `timestamp_policy_error`.

Fact: `fdwRevocationChecks` is set to `WTD_REVOKE_WHOLECHAIN`, while
`dwProvFlags` simultaneously requires
`WTD_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT`. Microsoft documents those as whole-
chain and chain-excluding-root scopes respectively; the candidate gives no
documented precedence or reconciliation. Omitting cache-only flags permits
network retrieval but does not prove that a retrieval occurred, so it cannot
establish `network_retrieval_required: true`. The record also lacks freshness,
per-element signer/timestamp disposition, and retrieval provenance.

Fact: the profile relies on the live Windows system trust and disallowed CTLs,
while asserting no automatic enrollment or store mutation. Microsoft
documents that trusted and untrusted CTLs can update automatically and daily.
The profile acknowledges the snapshot as unresolved, but the future accepted
record cannot identify or bracket the effective trust state.

Inference: missing timestamps, offline/unknown or stale status, a timestamp-
signer revocation gap, conflicting root scope, or an unaccounted live-store
change cannot be proven to fail closed by the stated procedure and evidence.

Required correction: choose one documented revocation-control path with exact
scope and precedence; define cache, retrieval, timeout, freshness, offline,
and per-element error handling; specify the supported timestamp presence and
policy-validation path; bind all results to retained provider/chain state; and
define the effective trusted/disallowed-store authority without claiming
unobserved mutation or retrieval.

### BRM-AUTH01-IR-004 — MAJOR — the recovery v0.2 conflict inventory is incomplete

Fact: recovery v0.2 also requires exact intermediate and root identities and
thumbprints, plus an exact timestamp authority. The profile's exact
`conflicting_requirements` constant lists only signer subject, issuer,
thumbprint, serial, and signature/timestamp algorithms. It has an
intermediate-CA prohibition but no explicit static-root or timestamp-authority
disposition.

Inference: the blocked status is honest, but its exact correction inventory is
not complete. A v0.3 author following only that list could preserve prohibited
root or timestamp-certificate pins or remove them without defining a supported
replacement.

Required correction: enumerate every recovery v0.2 identity and algorithm
constraint, classify each against KB 5125813 or another documented supported
contract, and state the exact agile replacement or preserved security
property.

### BRM-AUTH01-IR-005 — MINOR — base Git authority is format-checked rather than value-bound

Fact: `base_authority.handoff_commit` and `handoff_tree` use only a 40-hex
pattern. Replacing either with forty zeroes still validates, although the
reviewed instance correctly matches the candidate's authenticated parent and
parent tree. The recovery manifest and review hashes are constant-bound.

Inference: a downstream schema-only check can accept false provenance without
changing the security-policy constants.

Required correction: make the two reviewed Git identities constants in this
versioned schema, or remove them from normative validation and authenticate
them through an explicitly defined outer manifest rule.

## 6. Hostile-case reconstruction

The following results distinguish direct schema rejection from actual
evidence of the future Windows operation.

| Required hostile class | Result |
|---|---|
| Static subject, issuer, leaf, serial, intermediate, key-size, or algorithm pins | Direct field promotion/addition rejects, but recovery root and timestamp-authority conflicts are incomplete; see `IR-004`. |
| Nonzero WinVerifyTrust result or warning | Evidence constant rejects a nonzero value. Exact `LONG` zero is correctly required. |
| Omitted `WTD_STATEACTION_CLOSE` | Profile omission rejects, but the evidence record cannot establish the close call; see `IR-001`. |
| Interactive UI, callback, custom parser, or candidate-selected policy | Profile mutations reject, but accepted evidence is not bound to those inputs; see `IR-001`. |
| Cache-only, end-only, disabled, unknown, offline, stale, or soft-fail revocation | Direct profile mutations reject; actual scope, retrieval, freshness, and timestamp-chain proof remain insufficient; see `IR-003`. |
| Absent, untrusted, invalid, or revoked timestamp | A timestamp-kind string is required, but absence or a fabricated status can still produce schema-valid accepted evidence; see `IR-003`. |
| Candidate/new/test root, ignored error, or trust enrollment | Profile booleans reject direct promotion; generic trust plus an unidentified live store is not enough to prove the root was independently authorized; see `IR-002` and `IR-003`. |
| Redirect, final-URI drift, reused destination, changed file identity, or changed byte hash | Redirect/final-URI/reuse mutations reject. Unequal hashes validate and file identity is unrepresentable; see `IR-001`. |
| Evidence observation reused as future authority | Narrative forbids it, but no authenticated decision binding exists. Arbitrary observations validate; see `IR-001`. |
| Status promoted from blocked | Profile constant rejects. |
| Process, download, installation, build, runtime, rehearsal, S0, or E0 claim | All profile claim-bit promotions reject. |

The recovery v0.2 adversarial list was also reconstructed. Unsigned or invalid
signatures and nonzero policy results are rejected by the intended Windows
decision; a Windows-trusted but non-Microsoft signer is not rejected by the
selected generic policy (`IR-002`); alternate/candidate roots, timestamp and
revocation cases are not sufficiently evidenced (`IR-003`); post-verification
hash mutation and file swaps can yield schema-valid accepted records
(`IR-001`); and the fixed URI fields reject redirect drift. Layout cases 18–21
(unbound extra content, unsigned content absent from signed manifests,
layout verification failure, and the 24 GiB ceiling) remain later recovery
obligations and are neither implemented nor claimed by this package.

## 7. Preserved passes, nonclaims, and next action

The package truthfully identifies itself as a blocked, nonexecuting candidate;
its status and operational claim bits cannot be promoted by schema-valid
mutation; its package closure, canonical text, JSON syntax, Draft 2020-12
validity, and nested object closure pass; and its maximum claim does not claim
a real download, signature result, build, runtime, rehearsal, S0, or E0
result.

No recovery v0.3 design should adopt this profile until all five findings are
corrected in a new version and independently re-reviewed. This review opens no
acquisition, execution, build, runtime, rehearsal, S0, E0, Git publication, or
later experimental gate.
