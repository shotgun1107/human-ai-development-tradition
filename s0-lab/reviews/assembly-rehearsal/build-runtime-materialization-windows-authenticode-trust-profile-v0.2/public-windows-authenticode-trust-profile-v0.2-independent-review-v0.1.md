# S0 v0.14 Windows Authenticode trust profile v0.2 independent review

## 1. Review result

The v0.2 package does not pass the bounded design-consideration gate. Its
mechanical package, JSON Schema, exact-value, relation-order, and nonclaim
controls pass, but three security-authority gaps remain.

Finding counts:

| Severity | Count | Finding IDs |
|---|---:|---|
| BLOCKING | 3 | `BRM-AUTH02-IR-001`, `BRM-AUTH02-IR-002`, `BRM-AUTH02-IR-003` |
| MAJOR | 0 | none |
| MINOR | 0 | none |

This result does not authorize download, native verification, trust-store
access or mutation, bootstrapper execution, installation, build,
materialization, rehearsal, S0, or E0.

## 2. Role, identity, and boundary

Facts:

- review gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE TRUST PROFILE V0.2 INDEPENDENT REVIEW OPEN`;
- role: fresh independent PUBLIC security reviewer who did not author v0.2;
- reviewed branch:
  `codex/s0-build-runtime-authenticode-trust-profile-v02-review`;
- reviewed/source commit:
  `7798a714b88dee92c5d1682e23a0018f78179780`;
- reviewed tree: `49344ce13146019a23d1b426b9b65a84c8e85533`;
- sole parent: `bb97d9eec2ee24ced3b153959a957576b2a3889d`;
- package-manifest SHA-256:
  `315f89b1b13151ab9abe2aaff7ae64d23afa959ace8bd37f52ec4e872cc807c0`;
- official-document review date: `2026-08-24`; and
- F0 content access: none.

Only the gate's exact allowlist was used. No executable, certificate, CRL,
OCSP response, candidate byte, or trust-store content was downloaded or
inspected. No native API, trust-store query or mutation, bootstrapper,
installer, build, runtime, rehearsal, S0, or E0 operation occurred. Local
execution was limited to the required canonical text validator and in-memory
PUBLIC JSON/schema tests.

## 3. Input authentication and mechanical results

Facts and test results:

- branch, HEAD, tree, and sole-parent identity: PASS;
- handoff commit `2cb57954c92199dd92af84b8b510b38e3444bebd`
  resolves to tree `0b325f0b54f2f2315cee167d05ceffc51f000f2c`:
  PASS;
- v0.1 candidate commit
  `2aaf014927b04816602b45513d1df6c7e4f83608` resolves to tree
  `c619bebb4624f45b6bb10b72edba9f5ab87187ad` and has the handoff commit as
  its sole parent: PASS;
- v0.1 review commit
  `bb97d9eec2ee24ced3b153959a957576b2a3889d`: present and exact;
- recovery review commit
  `fd9415dd8e8bfc2eabda515398844097cd9cae1d` resolves to tree
  `acefe36c123f525da995e248dd2ff9396a922d7a`: PASS;
- F0 tracked aggregates: `32 / 11 / 10`; working-tree quiet-diff codes and
  parent-to-v0.2 quiet-diff codes: `0 / 0 / 0`;
- canonical validator SHA-256:
  `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`;
  validator equals HEAD and SelfTest passed every case;
- v0.2 manifest: eight canonical rows; all target hashes matched; all three
  Markdown/sidecar pairs passed; namespace closure was exactly 12 files;
- v0.1 manifest SHA-256:
  `6105b0ec246318e69ae189fcf686fa0266d18ea06c58039c07c9bca100f49bee`;
  all six targets and three target sidecars matched and validated;
- v0.1 independent-review SHA-256:
  `a46c0cd2aa0e90aeaca7070577fbbb68a1982a9bfa6c6f1408f006bfe8508406`;
  its sidecar validated;
- recovery v0.2 manifest SHA-256:
  `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`;
  all four targets and three target sidecars matched and validated;
- recovery v0.2 review-record SHA-256:
  `3cb76b0d2da2e303efb6f1a8353946180ca3c5d962ba9983747cfa67ad064f80`;
  its sidecar validated; and
- one additional current file exists in the recovery directory outside this
  review's allowlist. It was neither named nor opened and was not treated as
  part of the authenticated four-target recovery package.

Strict JSON and schema test results using fake PUBLIC in-memory objects:

- all nine allowlisted JSON targets parsed with recursive duplicate-key
  rejection: PASS;
- top-level and nested duplicate-key counterexamples rejected: PASS;
- all three v0.2 schemas passed Draft 2020-12 meta-schema validation: PASS;
- the profile instance validated against the exact-value profile schema:
  PASS;
- the profile schema's `const` equals the complete profile object: PASS;
- raw success and raw failure observations are both representable: PASS;
- adding acceptance, terminal-decision, or process-authority fields to a raw
  observation rejects: PASS;
- an all-true ordered 33-result positive decision validates: PASS;
- a positive decision containing a false relation rejects: PASS;
- a rejection with at least one false relation validates, while an all-true
  rejection rejects: PASS;
- missing, duplicate, reordered, and unknown relation IDs reject: PASS;
- all six decision hash fields are structurally mandatory: PASS; and
- even a positive decision is constrained to
  `process_authority_granted == false`: PASS.

These are structural results. They do not authenticate the referenced bytes
or prove that a relation result was computed from a native observation.

## 4. Official Microsoft-policy reconstruction

Facts confirmed from the exact official pages named by the acceptance plan:

- [KB 5125813](https://support.microsoft.com/en-us/servicing/os/windows/docs/2026/08/next-generation-code-signing)
  requires certificate and algorithm agility. It warns against static subject,
  issuer, thumbprint, serial, intermediate-CA, key-size, and digest-algorithm
  assumptions and directs applications to supported Windows trust APIs.
- [WinVerifyTrust](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust)
  describes `WINTRUST_ACTION_GENERIC_VERIFY_V2` as Authenticode-policy
  verification and requires exact `LONG` zero; no other return is success.
- [WINTRUST_DATA](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_data)
  requires every `WTD_STATEACTION_VERIFY` state handle to be freed by a later
  `WTD_STATEACTION_CLOSE`. It separately documents WinTrust revocation flags.
- [WTHelperProvDataFromStateData](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata)
  retrieves provider data from a state handle, and
  [WTHelperGetProvSignerFromChain](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain)
  retrieves a signer or countersigner by explicit indexes from that provider
  data.
- [CertGetCertificateChain](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain)
  permits `HCCE_LOCAL_MACHINE`, defines chain-excluding-root revocation, and
  makes the URL timeout cumulative when the selected flag is present. It also
  states that `pTime` controls certificate validity while root-store, trust-
  list, and revocation-material validity use current state/time.
- [CertVerifyCertificateChainPolicy](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certverifycertificatechainpolicy)
  defines normal Authenticode and Authenticode timestamp policies. Its
  Microsoft-root policy checks the last element of the first simple chain for
  a Microsoft root public key; the test-root flag widens that check, and the
  Microsoft-root policy performs no complete policy verification by itself.
- [Authenticode timestamp guidance](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures)
  explains that a timestamp preserves verifiability after the signing
  certificate expires and recommends always timestamping.
- [Windows trusted-root and Disallowed guidance](https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-trusted-roots-disallowed-certificates)
  documents live Trusted and Untrusted CTLs, their update mechanism, and
  separate last-sync state.
- [Microsoft's PKI repository](https://www.microsoft.com/pkiops/docs/repository.htm)
  publishes multiple Microsoft-operated roots, timestamp roots, issuing CAs,
  and revocation endpoints. This supports agility, not a static certificate
  pin.

Inference: the v0.2 choice to layer normal Authenticode policy and
Microsoft-root policy with test roots disabled is directionally correct. It
does not cure the supplier-identity gap described in
`BRM-AUTH02-IR-003`, because the official contract cited for the latter policy
is a root-key test, not a documented leaf-publisher identity guarantee.

## 5. Disposition of every v0.1 finding

| v0.1 finding | Independent v0.2 result |
|---|---|
| `BRM-AUTH01-IR-001` | **Not corrected.** Raw and derived records are separated, and 33 relations were added, but raw-observation and semantic-validator bytes are not independently bound by the relation contract (`BRM-AUTH02-IR-001`). Several relations also require facts absent from the raw record (`BRM-AUTH02-IR-002`). |
| `BRM-AUTH01-IR-002` | **Not corrected.** Normal Authenticode plus Microsoft-root policy is stronger than v0.1 generic trust, but the cited Microsoft policy guarantees only a Microsoft root at the end of the first simple chain, not that the signer leaf is a Microsoft publisher (`BRM-AUTH02-IR-003`). |
| `BRM-AUTH01-IR-003` | **Not corrected.** v0.2 selects one revocation route and adds timestamp policy, but retained-state chronology, policy-input chain identity, verification-time inputs, and freshness computation remain unrecorded (`BRM-AUTH02-IR-002`). |
| `BRM-AUTH01-IR-004` | **Structurally corrected, security disposition still dependent.** The ordered 15-item inventory now covers signer, intermediate, root, timestamp, algorithms, verification time, revocation, and trust/disallowed authority. The supplier and verification-time replacements remain blocked by the new findings. |
| `BRM-AUTH01-IR-005` | **Corrected.** The complete v0.2 profile is one exact schema `const`; mutation of either Git identity rejects, and the reviewed values match the authenticated commits and trees. |

## 6. Findings

### BRM-AUTH02-IR-001 — BLOCKING — referenced observation and semantic-validator bytes are not authenticated by the 33-relation contract

Facts:

- The decision schema requires
  `observation_record_sha256`, `semantic_validator_manifest_sha256`, and
  `semantic_validator_output_sha256`, but JSON Schema checks only their 64-hex
  shape.
- No relation requires `observation_record_sha256` to equal the canonical
  bytes of the raw observation being evaluated.
- No relation requires `semantic_validator_manifest_sha256` to equal a
  separately approved semantic-validator implementation manifest.
- No relation requires `semantic_validator_output_sha256` to equal the actual
  output that supplied the 33 booleans.
- `AUTH02-R01` and `AUTH02-R02` use singular field names but do not state that
  the raw-observation and decision copies must equal each other as well as the
  external authorities.
- The profile's required-external-authority object names the verifier manifest
  but omits a semantic-validator implementation manifest.
- A fake PUBLIC decision with arbitrary observation, validator-manifest, and
  validator-output hashes and 33 self-asserted true results is schema-valid.
  This is expected at the schema layer, but the semantic contract contains no
  missing outer authentication relations that could make it authoritative.

Inference: substituting the raw observation, semantic validator, or validator
output is not ruled out by an implementation that follows all 33 written
requirements. The narrative claim that the decision binds these bytes is
therefore stronger than the normative relation contract. This leaves the core
v0.1 relational-authority finding open.

Required correction:

1. define canonical bytes for the observation, decision input, validator
   output, and each implementation manifest;
2. add explicit relations binding the actual observation hash, both copies of
   the profile/verifier hashes, an independently approved semantic-validator
   manifest, and the actual validator output;
3. identify the outer authority that approves both implementation manifests;
   and
4. version the relation contract and schemas because the exact ordered
   relation set must change.

### BRM-AUTH02-IR-002 — BLOCKING — same-state, same-policy-chain, verification-time, and freshness relations cannot be derived from the raw record

Facts:

- `AUTH02-R13` requires provider state to remain open through extraction and
  policy checks and to close afterward. The raw record has extraction status,
  a free-form binding hash, close-attempt/result fields, but no event order,
  state-handle identity at each use, or retained-through-policy observation.
- `AUTH02-R16` and `AUTH02-R17` require two policy results on the same signer
  chain. The raw record stores two error integers next to chain arrays but no
  policy-call input chain-context binding.
- `AUTH02-R20` requires the timestamp to be extracted from the same retained
  provider state. The timestamp object has no provider-state binding or signer
  and countersigner indexes.
- `AUTH02-R23` requires Authenticode acceptance of signing time, but neither
  chain call records `pTime`, `CERT_CHAIN_TIMESTAMP_TIME`, or exact extra
  policy inputs. The profile uses the label `WINDOWS-AUTHENTICODE-POLICY`
  instead of an exact verification-time procedure.
- `AUTH02-R24` and `AUTH02-R25` require per-element freshness. The record has
  asserted freshness labels plus `this_update`/`next_update`, but no
  observation/reference time and no normative freshness computation. It also
  does not bind each element's revocation data to the result of the one
  selected chain call.
- Arbitrary but equal provider-state and rebuilt arrays, asserted zero policy
  errors, asserted `FRESH`, and asserted close ordering can therefore support
  all-true booleans without giving the semantic validator enough raw data to
  recompute those facts.

Official fact: Microsoft's chain API makes `pTime`, current revocation-data
validity, and current root/trust-list state distinct. Consequently,
verification time and freshness cannot be recovered from the existing fields
by treating a policy-error integer as a complete transcript.

Inference: the future semantic validator would have to trust verifier
assertions or consume undeclared live/native inputs. That contradicts the
package's claim that every equality and policy relation is computed from the
bound raw observation. Early provider-state close, a policy result from a
different chain, an invented countersigner, or stale evidence is not yet
proven to fail closed.

Required correction: extend the raw schema and semantic contract with an
exact event sequence and state-handle binding, signer/countersigner indexes,
policy-call input chain-context hashes, exact chain `pTime` and policy-extra
inputs, verification/reference time, per-element revocation-source binding,
and a deterministic freshness rule. The authenticated verifier and semantic
validator responsibilities must be nonoverlapping and explicit.

### BRM-AUTH02-IR-003 — BLOCKING — Microsoft-root success is not a documented Microsoft leaf-publisher guarantee

Facts:

- Generic WinVerifyTrust and normal Authenticode policy establish a trusted
  Authenticode publisher, not specifically Microsoft.
- The cited Microsoft documentation says
  `CERT_CHAIN_POLICY_MICROSOFT_ROOT` checks the last certificate of the first
  simple chain for a Microsoft root public key. It expressly says this policy
  performs no complete policy verification by itself.
- v0.2 correctly layers generic verification, normal Authenticode policy,
  code-signing EKU, the Microsoft-root test, flags zero, same-chain relations,
  and fixed Microsoft-operated URL selection.
- None of the cited official contracts says that every code-signing leaf that
  can terminate at a Microsoft root is itself a Microsoft software-publisher
  identity. The exact URL authenticates source selection but does not turn a
  root-key test into a leaf-publisher guarantee.
- Recovery v0.2 requires Microsoft signer/supplier authenticity before the
  first process, and the v0.1 review already held that the URL alone is not a
  substitute for that property.

Inference: the composition is a strong candidate, but its final step from
Microsoft-operated root to Microsoft signer is unsupported by the official
guarantees supplied to this review. This is a security-authority ambiguity,
not a request to restore prohibited static certificate pins.

Required correction: cite and encode a supported Windows contract whose
documented semantics establish the required Microsoft publisher/supplier
property while remaining certificate- and algorithm-agile, or narrow and
reauthorize the recovery supplier property in recovery v0.3. Continue to
require normal Authenticode, same-chain binding, test roots disabled,
timestamp, revocation, and effective trust/disallowed checks.

## 7. All 33 semantic relations

Every ordered relation was reviewed. `Defined` means the relation is
structurally present and has sufficient design inputs subject to a future
authenticated implementation. `Blocked` identifies a current finding.

| Relation | Result | Review note |
|---|---|---|
| `AUTH02-R01` | Blocked by IR-001 | External profile-manifest comparison exists, but the raw and decision copies are not explicitly cross-bound. |
| `AUTH02-R02` | Blocked by IR-001 | Verifier authority is named; semantic-validator authority is not. |
| `AUTH02-R03` | Defined | Authenticated observation-schema validation is required. |
| `AUTH02-R04` | Defined with IR-001 caveat | Decision/schema/contract validation is required, but it cannot authenticate the validator producing the results. |
| `AUTH02-R05` | Defined | Requested and final URI ordinal equality is expressible. |
| `AUTH02-R06` | Defined | Zero redirects is expressible. |
| `AUTH02-R07` | Defined | Three file identities and one-retained-handle assertion exist; native provenance remains a verifier obligation. |
| `AUTH02-R08` | Defined | CREATE_NEW/out-of-repository and no-reparse requirements exist. |
| `AUTH02-R09` | Defined | Positive, equal byte lengths are computable. |
| `AUTH02-R10` | Defined | Three-way SHA-256 equality is computable. |
| `AUTH02-R11` | Defined | Exact WinTrust constants and forbidden extensions are represented. |
| `AUTH02-R12` | Defined | Exact `LONG` zero is computable. |
| `AUTH02-R13` | Blocked by IR-002 | Required retained-state chronology is absent. |
| `AUTH02-R14` | Defined | Signer leaf to provider-chain position-zero equality is computable. |
| `AUTH02-R15` | Blocked in part by IR-002 | Array equality is computable; provenance from provider state and the approved rebuild is not bound. |
| `AUTH02-R16` | Blocked by IR-002 | Zero error exists; policy-call input chain identity does not. |
| `AUTH02-R17` | Blocked by IR-002 and IR-003 | Same issue as R16 plus the supplier-guarantee gap. |
| `AUTH02-R18` | Defined | Flags zero and test-root false are expressible. |
| `AUTH02-R19` | Blocked in part by IR-002 | EKU assertion exists; the chain-usage-call result/input is not separately bound. |
| `AUTH02-R20` | Blocked by IR-002 | Presence/kind are present; same-provider-state countersigner identity is not. |
| `AUTH02-R21` | Defined | Timestamp leaf to position-zero equality is computable. |
| `AUTH02-R22` | Blocked in part by IR-002 | Array equality is computable; approved timestamp rebuild provenance is not. |
| `AUTH02-R23` | Blocked by IR-002 | Error/time fields exist; exact verification-time and policy inputs do not. |
| `AUTH02-R24` | Blocked by IR-002 | Per-element labels exist; deterministic freshness and chain-call binding do not. |
| `AUTH02-R25` | Blocked by IR-002 | Same timestamp-chain gap as R24. |
| `AUTH02-R26` | Defined but intentionally unresolved | Root trust/disallowed result is required; exact snapshot implementation remains a declared later obligation. |
| `AUTH02-R27` | Blocked in part by IR-002 | Exact flags and forbidden labels cover modes; ignored-error and evidence provenance still rely on missing call bindings. |
| `AUTH02-R28` | Defined but intentionally unresolved | Scope constants and pre/post equality exist; canonical snapshot implementation is expressly missing. |
| `AUTH02-R29` | Defined | Raw mutation observations and zero counts can reject mutation. |
| `AUTH02-R30` | Defined | Callback, candidate store, custom parser, and candidate policy are forbidden. |
| `AUTH02-R31` | Defined | Process count is fixed at zero in raw and decision records. |
| `AUTH02-R32` | Defined | Exact profile schema fixes every operational claim bit false. |
| `AUTH02-R33` | Defined with dependent gaps | The ordered 15-item inventory is complete, but supplier/time replacements remain affected by IR-002/003. |

## 8. Hostile-case coverage

### 8.1 Structural decision cases

| Required case | Result |
|---|---|
| Raw record contains acceptance or execution authority | Direct extra-property rejection: PASS. |
| Raw success and failure remain representable | PASS. |
| Rejection lacks a false relation | Rejected: PASS. |
| Positive decision contains any false relation | Rejected: PASS. |
| Missing, duplicate, reordered, or unknown relation ID | Rejected: PASS. |
| Positive result grants process authority | Rejected by exact `false`: PASS. |
| Any of six decision hash fields omitted | Rejected structurally: PASS. Authentication/equality remains failed under IR-001. |
| Schema-valid booleans presented as proof | Narrative denies this, but the absent byte-authentication relations leave IR-001. |

### 8.2 Same-file and evidence cases

| Required hostile class | Result |
|---|---|
| Unequal download/post-signature/preexecution hashes | R10 defines rejection. |
| Changed volume serial, file ID, reparse status, byte length, or retained handle | R07-R09 define rejection; authenticated native provenance remains a verifier obligation. |
| Redirect or final-URI change | R05-R06 define rejection. |
| Signer leaf differs from provider-chain position zero | R14 defines rejection. |
| Arbitrary or reordered signer elements | A provider/rebuild mismatch rejects, but identically invented arrays are not bound to provider/policy calls; IR-002. |
| Provider signer chain differs from rebuilt chain | R15 defines rejection. |
| Arbitrary or reordered timestamp elements | Same provenance gap as signer arrays; IR-002. |
| Timestamp leaf differs from position zero | R21 defines rejection. |
| Provider state closed before extraction/policies | Not derivable from the raw record; IR-002. |
| Close omitted/nonzero or WinVerifyTrust nonzero | R12-R13 define rejection for asserted fields; chronology remains IR-002. |
| Profile/verifier/observation/contract/validator bytes substituted | Profile and contract pins are strong; observation and validator bindings fail under IR-001. |
| Reused observation or certificate identity promoted to future authority | Profile narrative and claim bits forbid promotion; authoritative enforcement awaits corrected bindings and implementations. |

### 8.3 Supplier, timestamp, revocation, and trust-state cases

| Required hostile class | Result |
|---|---|
| Windows-trusted non-Microsoft signer | Normal non-Microsoft roots reject under R17, but Microsoft-root-to-Microsoft-leaf assurance remains IR-003. |
| Generic success without normal Authenticode policy | R16 defines rejection. |
| Microsoft-root policy applied to another chain | Intended to reject, but policy-call input chain is unbound; IR-002. |
| Microsoft-root policy used alone | Ordered all-true R12/R16/R17 prevents this structurally. |
| Nonzero policy errors, test root, absent EKU, candidate store | R16-R19 and R30 define rejection. |
| Absent/invented/wrong-chain/invalid-time timestamp | R20-R23 intend rejection; same-state and time-policy inputs remain IR-002. |
| A second claimed WinTrust revocation authority | Exact profile selects `WTD_REVOKE_NONE` and one separate chain path: PASS at design level. |
| End-only, cache-only, disabled, unknown, offline, unchecked, stale, soft-fail, or ignored revocation | Mode labels and R24-R27 intend rejection; freshness/provenance remains IR-002. |
| Missing evidence for a non-root element | Intended R24/R25 coverage cannot prove an omitted actual chain element without corrected chain-call binding; IR-002. |
| Untrusted or effectively disallowed root | R26 defines rejection, subject to the declared snapshot implementation obligation. |
| Changed pre/post trust/disallowed snapshot | R28 defines rejection. |
| Candidate/verifier trust-store mutation | R29-R30 define rejection. |
| Unimplemented or unauthenticated snapshot algorithm | Package status remains blocked and authority status is unresolved: correctly kept blocked. |
| Fresh cache with established freshness and network-capable call | Correctly allowed in principle; what establishes freshness is incomplete under IR-002. |

## 9. Recovery conflict inventory and nonclaims

Test result: the recovery conflict inventory has exactly 15 ordered entries
covering signer subject/issuer/thumbprint/serial, intermediate identity/hash,
root identity/hash, timestamp authority and chain/root, both digest algorithms,
verification time, revocation scope/freshness, and trusted/disallowed
authority. This corrects the v0.1 inventory omission.

Inference: inventory completeness is not semantic adequacy. The Microsoft
supplier replacement and verification-time/freshness replacement remain
unapproved because of `BRM-AUTH02-IR-002` and `BRM-AUTH02-IR-003`.

The package truthfully remains
`BLOCKED-REQUIRES-RECOVERY-V0.3-ALIGNMENT-AND-VERIFIER-IMPLEMENTATION`.
Its effective-authority snapshot, verifier implementation, semantic validator,
and recovery v0.3 alignment are not implemented or authenticated. All
operational claim bits remain false. This review establishes no real
signature, certificate, revocation, trust-store, acquisition, execution,
installation, build, runtime, rehearsal, S0, E0, central-system, Project Brain,
economic-value, safety, or transfer result.

## 10. Required next revision

A successor must correct all three findings in versioned profile,
observation, decision, and semantic-contract bytes, then undergo another fresh
independent PUBLIC review. The current package must not be adopted by recovery
v0.3 or a verifier design as an approved trust authority.

REVISE-AND-REREVIEW
