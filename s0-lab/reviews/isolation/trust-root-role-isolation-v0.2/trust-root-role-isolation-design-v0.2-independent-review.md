# S0 v0.14 trust-root and role-isolation design independent review v0.2

- review kind: fresh independent public-only hostile design rereview
- review date: 2026-08-09 KST
- gate: S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN
- repository: C:\Users\kimsiyeol\.codex\visualizations\2026\08\06\019fd6bc-5977-7de1-8efa-c030a2a29cad\hadt-s0-isolation-v02-review
- origin: https://github.com/shotgun1107/human-ai-development-tradition.git
- branch: codex/s0-trust-root-role-isolation-review-v02
- reviewed commit: cb4198f4475881ba5b607517fdbb4f0db6b8ce5d
- verdict: REVISE-AND-REVIEW
- finding count: zero blocking, one major, one minor
- claim kind: public design review only

No implementation test was run. No VM was provisioned or configured; no host
setting, key, Ed25519 or HKDF operation, account, vault, canary, fixture,
script, provider/model session, acceptance test, I1 verifier, protected
material, E0, or S0 execution was created or run.

## 1. Review authority, independence, and boundary

This reviewer did not author v0.1 or v0.2, did not participate in author-side
QA, did not use another v0.2 reviewer conclusion, and did not read sealed,
oracle, bank, label, condition-map, executor-output, or E0 material. No
subagent was used. Worktree separation was treated only as edit isolation.

Before substantive reading, the exact local state was:

| Check | Required and observed value | Result |
|---|---|---|
| origin | https://github.com/shotgun1107/human-ai-development-tradition.git | pass |
| branch | codex/s0-trust-root-role-isolation-review-v02 | pass |
| HEAD | cb4198f4475881ba5b607517fdbb4f0db6b8ce5d | pass |
| worktree | no tracked or untracked porcelain entries | pass |

The candidate source branch need not have a local remote-tracking ref under
the stated fetch-refspec rule. Its absence was not used as evidence.

The review then hashed all 39 allowlisted files before relying on their
contents. All values matched the handoff. All 17 same-basename Markdown
sidecars contained exactly one canonical lowercase digest plus two spaces plus
the exact Markdown basename and one final LF; every recorded digest matched
the Markdown bytes. AGENTS.md has no sidecar. The four I1 topology/manifest
inputs were read only as the explicitly allowed files; no manifest row was
followed into implementation code.

## 2. Authenticated inputs

| Exact input | Verified SHA-256 |
|---|---|
| AGENTS.md | ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844 |
| s0-lab/control/s0-protocol-v0.3.md | b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c |
| s0-lab/control/s0-protocol-v0.3.sha256 | ffcd795bb94f78f69b404cb49955130c3bf4ae4fff12b026a1b3584cbd391963 |
| s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.md | 49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0 |
| s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.sha256 | ff71deea0b0aaac3a6f46d703376b22f677baa4d0e20be22a42f98a449706766 |
| s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md | a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee |
| s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.sha256 | 7f30298de0667cd01991e72704b963a20ebb558e1e76474eb212d8a67842d888 |
| s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.md | b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9 |
| s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.sha256 | 24ce405c3987410cd2a2f6cba0ce4ec83a235f8b23b013d908675797432e8310 |
| s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.md | 537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605 |
| s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.sha256 | e73f0bb18e65f39b6ebb8ac0fda00ef4f756a3a01000f97db9fb9a41ac0eaf6c |
| s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md | f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65 |
| s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.sha256 | 8c90eda5c1557c1f31e977f94ec6985e8799a692e56141a830e6cc8ff7f685b4 |
| s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.md | 167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925 |
| s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.sha256 | 36a1565b93df98f2d18f8447280458df66a0d38dacf2aa4bb56cc4b7a7564c40 |
| s0-lab/i1/spec/public-runtime-v0.14.json | fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08 |
| s0-lab/i1/spec/public-runtime-files.sha256 | 9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e |
| s0-lab/i1/verification/implementation-files.sha256 | 668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c |
| s0-lab/i1/verification/implementation-manifest.sha256 | 1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.md | 6a062383742e90409f5dac9c443de90b93773c266525ba00f3802b60d40ff6fc |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.sha256 | 7a0bc9043ae8ac2e59d4ef0aa1a8723835865717f0054e818711cc7809df8601 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.md | ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.sha256 | 08fef8b7e5c31f94983b5f24cdfae44aeb5f7137cbcf81854130f589ea6ac61d |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.md | 71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.sha256 | 6caf7c1ca42e5ed1c81f45d481cc4403d637156068d8a9f48d61d98a9349dc3a |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.md | 88ca9ae00ee8a76f1f01865be7ffc106afede4a8207c86fab1bb72c9099e8d7a |
| s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.sha256 | 5553c4fa3698186ad1eae160143e4a97b30aba651e033db38f4c3d654352224a |
| s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.md | d99cf801719e2f524ca87fe3741b8a6776c4682df304d9448c245e5d3fee7404 |
| s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.sha256 | e6c8497753878df8407dd23cfa606927e09909a8486b398206bb237a75f76e7d |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md | e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256 | 41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md | 3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.sha256 | 566bba9b81d4ed5216f9c49c01448154f0a2a53ee6d9cfa13e0d9993475df70c |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md | 534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.sha256 | 29ec3013bab28aa1265653ad4badc034381fa91cbd40a0aa44443359a9d70060 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.md | 5c961d3bba03e12e07d34aede1207448565bf3456d0bffb6cad1602f1bbd2494 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.sha256 | ac64d54c204d17e4d541e08ab1e1ab487c2f2a43542aa317958130250383cc90 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.md | 610b4ca1b03d7539cdcaf526a03bf3877cfca24426fd9f58b816aa0012d6db27 |
| s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.sha256 | 964b09d8c42ee5680f15eda27659aded87571ce6b77a734affe9253473114da4 |

The permitted primary-reference check reproduced RFC 8032's Ed25519 decoding,
scalar range, cofactored verification equation, and permitted uncofactored
alternative; RFC 5869's salt and info roles; and Microsoft's exact
BCRYPT_USE_SYSTEM_PREFERRED_RNG/NULL-handle contract. The check also produced
the bounded citation defect in TRI2-m01 below.

## 3. Independent effective-composition reconstruction

The effective candidate is not v0.2 alone. It is the authenticated v0.1 design,
matrix, and acceptance plan plus the following exact overlay:

1. Revision section 6 replaces the two v0.1 invocation-ID sentences, every
   separate invocation-nonce reference, and the old invocation-secret clause.
2. The v0.1 signed-descriptor phrase alone becomes unsigned TCB-bound
   invocation descriptor; revision section 5 supplies the replacement
   authority, bytes, admission, and verification order.
3. Revision sections 4.1-4.5 replace the two named v0.1 signer-request/media
   paragraphs and all of v0.1 section 5.3.
4. Revision section 4.4 replaces the named non-root signer-state paragraph.
5. Matrix section 1 is supplemented, and conflicts are replaced, by revision
   section 6.
6. Matrix section 3 is replaced by revision section 4.5 plus authority-addendum
   sections 2-3.
7. Matrix section 7 is supplemented by revision sections 3.5, 4.5, 5.4, and
   6.4 plus authority-addendum section 7.
8. Acceptance-plan section 2 actor/signer fields and only the rows named by
   addendum section 2 are replaced; all other v0.1 rows survive.
9. The v0.2 review response is explanation only and grants no authority.
10. The v0.2 brief entirely replaces the v0.1 brief for this review.

Within a named replacement, unrepeated v0.1 text does not survive. Outside the
map, v0.1 remains authoritative, and an unlisted conflict would be a defect.
No such unlisted topology, split-edge, E49, executor-count, provider-blocker,
or gate conflict was found.

## 4. Fixed topology and A-D fairness

Targeted reconstruction of the authenticated public topology and the
row-position map produced:

| Inventory | Exact count |
|---|---:|
| aggregated role rows | 32 |
| role positions | 40 |
| paired rows | 8 |
| experimental section-4 signer bindings | 21 |
| positions with signer none | 19 |
| non-row root signer | 1 |
| registry IDs | 22 |
| stores | 27 |
| explicit reader entries | 46 |
| edge rows | 64 |

The paired rows remain label authors, leakage reviewers, comparator builders,
expected-catalog generators, P1 reviewers, blinded-map builders, semantic
judges, and comparator operators. The registry remains the exact 22-ID order
from adjudication-comparison through simulation-builder. The 21 experimental
signers plus the separate root account for all 22 IDs exactly once. No
ceremony coordinator, descriptor, admission record, ledger namespace,
witness, media, or TCB service is promoted into a role, signer, store, reader,
or edge.

### 4.1 Equal experimental opportunity

| Dimension | Reconstruction |
|---|---|
| source information | A-D retain identical fact-ID, record-ID, normalized fact text, question, and error-opportunity sets. Only the already frozen representation structure differs. |
| authority | Every run uses the same public-executor:single template, no section-4 signer identity, one exact assigned package, the same common resources, and the same denylist. No condition receives another store, edge, tool, credential, or retry right. |
| model conditions | Exact model identity and reasoning setting must freeze once in the common manifest; all eight units are fresh, unforked one-turn sessions with no subagent, internet, MCP, browser, or external transfer. |
| time and output | Each run has the same 15-minute wall-clock limit, 8,192-byte UTF-8 answer limit, one output file, human content intervention zero, and suite-wide technical-retry rule. At most three runs are concurrent, with order fixed before results. |
| scoring opportunity | Each condition receives the same questions and precommitted primary/ancillary opportunities. Accuracy is anonymously frozen before condition identity, timing, bytes, or cost are revealed. One cause cannot be double counted, and no result-time threshold, question, error code, or limit change is allowed. |
| selection rule | D can survive only if eligible and strictly lower in major errors in both blocks against every eligible simple condition. Tie, one-block advantage, crossed advantage, or mixed result cannot select D over the precommitted simple fallback. |
| leakage and vocabulary | Runner paths and fields may not expose A-D, structure rank, the D hypothesis, chronological/common/lineage labels, scores, oracle, or condition map. Neutral relationship codes alone are permitted. The isolation overlay adds no runner-facing D-favoring vocabulary. |

The trust-root revision changes no fact, question, model, time, byte, error,
threshold, or selection rule. It therefore creates no D-specific information
or scoring advantage. This is a design-level equality result, not evidence
about any executor or model.

## 5. Strict Ed25519 profile reconstruction

S0-ED25519-STRICT-1 admits an exact 32-byte public key only after RFC decoding,
byte-identical re-encoding, identity rejection, and [L]A = I. Because L is
prime, the admitted nonidentity point has exact order L; identity,
nonidentity small-order, and mixed-order keys reject.

A signature must be exactly 64 bytes. R receives the same
decode/re-encode, identity, and order-L checks; S is little-endian with
0 <= S < L; k is SHA-512(Renc || Aenc || M) mod L; and only the exact
Boolean result of the uncofactored equation [S]B = R + [k]A is accepted.
Ed25519ctx, Ed25519ph, custom prehash/context, cofactored-only acceptance,
truthy non-Boolean values, batch-only results, provider fallback, and algorithm
substitution reject.

The profile applies before anchor acceptance, all commitment and registry
entries, all PoPs, root registry signature acceptance, registry binding, and
every active generic-envelope signature. A cache binds exact key bytes,
profile, campaign, process-local verifier instance, and the applicable
authenticated anchor or registry digest; it cannot cross profile, campaign,
anchor/registry, verifier instance, or process. Commitment-stage keys have no
activated registry context, so their stated pre-commit strict check must be
performed rather than imported from an active-registry cache.

## 6. Bootstrap, authority, and signature-scope reconstruction

### 6.1 Classes, states, and files

There are exactly two non-root request classes:

- preactivation-pop-v1 is accepted only at pop-context-bound, forbids registry,
  edge, active-artifact, and active-caller fields, and can produce one own-key
  PoP.
- active-section4-v1 is accepted only at active, requires the activated
  registry digest and exact owner/edge/phase/artifact/domain/caller tuple, and
  rejects every bootstrap field.

The root accepts neither. Its disjoint one-use root-registry-v1 ceremony is
accepted only at root key-generated and signs the one exact registry-v1
generic-envelope preimage after 22 strict key checks, 21 proofs, commitment
equality, and transcript freeze. It does not require its not-yet-created
activated envelope. One success moves it to registry-signed and a second
signature is impossible.

The exact import/signing packages are:

| Route | Exact file set | State effect |
|---|---|---|
| preactivation context import | context-binding.txt, commitment-manifest.txt, challenge-manifest.txt | key-generated to pop-context-bound |
| PoP request | request.txt, preimage.bin | pop-context-bound to pop-issued after one successful signature |
| offline root ceremony | request.txt, preimage.bin, anchor-record.txt, commitment-manifest.txt, challenge-manifest.txt, proof-transcript.txt, registry-record.txt | root key-generated to registry-signed |
| registry-binding import | binding-control.txt, anchor-record.txt, commitment-manifest.txt, challenge-manifest.txt, proof-transcript.txt, registry-envelope.bin | pop-issued to registry-bound after inert validation |
| activation-binding import | activation-record.txt, activation-binding.txt | registry-bound to active |
| active request | request.txt, preimage.bin | active remains active after one admitted request |

Every route is host-admitted against an immutable package object/hash, exact
target/state, and a one-use capability. Preactivation context and request
capabilities freeze in the challenge manifest; registry and activation import
capabilities freeze after their source artifacts; root IDs/capability freeze
after the transcript. Active request capability and caller authentication
remain subject to the frozen owner tuple and the explicitly unresolved signer-
provider decision, so no active implementation or key generation is
authorized here.

The physical order is powered-off clean target, admission and ledger/witness
check, capability pending/consume, one read-only ISO attachment, one new raw
result disk only for a signing route, frozen parser/service boot, shutdown,
full detachment, then terminal consumed evidence. Hot, simultaneous, stale,
shared, writable, reused, prior, or unresolved media reject. The appliance
independently maintains unused to pending to consumed or terminal anti-replay
state. The missing observable outcome for the three no-result-media import
routes is TRI2-M01.

### 6.2 Transcript, registry binding, and activation

CONTROL freezes a strict 22-entry commitment, then a 21-entry challenge
manifest with four independent values per non-root signer. The 84 values are
atomically reserved before challenge freeze and never freed. The transcript
contains exactly 21 proofs in non-root registry order and binds role, request,
preimage hash, and signature. The root revalidates the complete chain.

A pop-issued appliance may cryptographically validate the root-signed registry
envelope as an inert candidate against commitment, challenge, transcript,
anchor, commit, strict-key, and strict-signature bindings. That validation
grants no ordinary verification/signing authority. A separate exact user
activation record and two-file activation import alone move registry-bound to
active.

### 6.3 Three exclusive signature scopes

1. preactivation-pop-v1 contains only the 21 detached bootstrap proofs and
   grants no ordinary authority.
2. section4-generic-envelope-v1 contains the root registry signature and
   ordinary active section-4 envelopes. The registry envelope is only inert
   before activation.
3. inherited-signature-unresolved contains predecessor signatures outside the
   generic-envelope system and remains forbidden to implement.

The transcript and TCB control records are unsigned containers or records, not
new scopes. Scope overlap, scope absence for a signature-bearing object,
request-class/scope confusion, or PoP reuse as ordinary authority rejects.

## 7. Descriptor and invocation reconstruction

The descriptor is deliberately unsigned. The input route controller constructs
one canonical S0-INVOCATION-DESCRIPTOR-2 from the frozen declaration; only the
pinned control-host-preflight TCB function may approve launch. The descriptor
omits both its own digest and the whole ISO digest. The external admission
record binds descriptor hash, complete ISO hash and immutable object handle,
content and route manifests, VM/base/configuration, executable and policy
hashes, blank output medium, reservation/bound events, and one boot
authorization. The route controller cannot approve. The host attaches the same
already-hashed object handle without path re-resolution and consumes the boot
authorization before power-on.

The guest verifies canonical descriptor bytes, attached payload and policy
hashes, executable self-measurement, and its declared invocation binding. It is
not credited with observing host-only VM, VHDX, ISO-handle, base, or
configuration facts. Post-run admission cross-checks host and guest evidence.
No cryptographic claim is made against the trusted host administrator.

There is no actor invocation nonce. Exactly 32 raw bytes from one successful
BCryptGenRandom(NULL, 32, BCRYPT_USE_SYSTEM_PREFERRED_RNG) call form the sole
external invocation_id. Before VM, ISO, descriptor, or output-medium creation,
the ID is atomically reserve-if-absent in the project-lifetime ledger and is
never freed across campaign, failure, quarantine, cancellation, candidate
rejection, or successor version.

After machine identity exists, the guest obtains 32 fresh CSPRNG bytes and
derives 32 bytes with HKDF-SHA-256: IKM is guest_random, salt is the exact raw
invocation ID, and info binds campaign, invocation, role position, VM ID, and
descriptor digest. The host, guest, ingest frames, admission, and state
evidence bind the same invocation bytes.

## 8. Three ledger namespaces and witnesses

| Namespace | Exact success chain | Terminal rule | Independent witness purpose |
|---|---|---|---|
| ceremony | values-reserved to challenge-frozen to terminal/accepted | either preterminal state may move once to terminal/rejected; 84 values never free | detect restored or forked ceremony/value-reservation history |
| signer-media | reserved to admission-frozen to pending to consumed | any pre-consumed state may move once to terminal/rejected; crash or uncertainty at pending is terminal | bind exact package/object/capability/admission/result route and prevent host/appliance replay |
| invocation | reserved to bound to admission-frozen to boot-consumed to terminal | one terminal from any reached state; completed only from boot-consumed; ID never frees | prevent duplicate/racing reservation, stale binding, rollback, and second boot |

Each event is exact ASCII/LF, carries a global sequence and previous-event
hash in its namespace, uses a fresh opaque CNG event ID, and binds its exact
kind payload. Each namespace has its own monotonic head in a rollback domain
independent of the ledger filesystem. Every append must advance ledger and
witness atomically. Restoring an internally valid older ledger, head mismatch,
unavailability, partial append, or capability/authorization resurrection
invalidates the candidate. The concrete provider remains
launch-ledger-provider-unresolved and blocks provisioning.

## 9. Effective acceptance inventory and nonclaims

The 92 predecessor IDs plus 15 added IDs, with the named v0.1 rows replaced
rather than duplicated, produce:

| Family | Effective rows |
|---|---:|
| ISO-P01-P19 | 19 |
| ISO-C01-C14 | 14 |
| ISO-R01-R22 | 22 |
| ISO-I01-I08 | 8 |
| ISO-K01-K34 | 34 |
| ISO-L01-L10 | 10 |
| total | 107 |

Every row is noncompensatory. No skip, waiver, provider-default acceptance
set, operator substitution, or passing row compensates for a failure. These
are unexecuted future requirements.

The following remain explicit blockers/nonclaims: inherited signatures outside
section 4, signer-custody provider and role authentication, launch-ledger and
witness provider, external provider/model isolation, VM/base/network/ACL/vault
implementation, atomic stores, keys, anchor, registry, ceremony, protected
material, bank, labels, oracle, condition map, packages, model calls, judge
handoff, scoring, statistics, E0, and S0. Nothing here establishes central-
system implementation, Project Brain integration, operational safety,
economic value, production readiness, model stability, representation
superiority, or model-to-model transfer.

## 10. Mandatory hostile tabletop trace

These are paper traces, not executed tests. Each handled mutation names its
primary fail-closed rule. The one import-observability ambiguity is a finding.

| Mutation | Primary rule and disposition |
|---|---|
| PoP with A = identity, R = identity, S = 0 | A is rejected first by strict-key step 4 before commitment/PoP. With a valid A used to reach the signature path, R is rejected by strict-signature step 3. ISO-K27. |
| root registry signature with identity anchor/key or identity R and zero S | Anchor/key is rejected before root admission by strict-key step 4; with a valid root key, identity R is rejected by strict-signature step 3. ISO-K27/K30. |
| ordinary artifact with identity registry key or identity R and zero S | Registry entry fails strict-key admission; with a valid entry, identity R fails strict-signature step 3 before artifact/state acceptance. ISO-K27/K30. |
| zero32, sign-bit zero32, order-two encoding, and four stated order-eight encodings as A | Identity uses step 4; every nonidentity low-order point has [L]P != I and fails strict-key step 5. ISO-K28. The source attribution for the order-eight coordinates is TRI2-m01. |
| each small-order class as R | Identity fails strict-signature step 3 identity clause; every other small-order R fails its [L]R = I clause. ISO-K28. |
| mixed-order A made from the order-two point plus RFC test-vector-1 key | [L]A != I, so strict-key step 5 rejects. ISO-K28. |
| analogous mixed-order R | [L]R != I, so strict-signature step 3 rejects. ISO-K28. |
| cofactored-only signature | The required uncofactored equation fails and no provider/cofactored fallback exists. ISO-K29. |
| strict check skipped or cache reused across key/profile/campaign/anchor/registry/verifier/process | The exact cache tuple and process-local verifier ID fail to match; ISO-K30 rejects the affected anchor, registry, proof, or artifact. |
| preactivation request carries registry digest, edge, active kind, or active caller field | The disjoint preactivation schema forbids the field before signature processing. ISO-K16/K20. |
| active request before activation or with bootstrap fields | Signer-state matrix permits active-section4-v1 only at active, and its exact parser rejects cross-class fields. ISO-K20/K32. |
| root request depends on its not-yet-activated envelope | Root-registry-v1 has no activated-registry field and accepts only the seven-file candidate package at root key-generated. ISO-K15. |
| root package misses one of seven files | Exact root file-set admission fails. ISO-K10/K33. |
| root package at wrong state or repeated | Root key-generated is the only allowed state; successful request ID and root state are consumed once. ISO-K32. |
| context, registry-binding, or activation package has missing/extra file, wrong capability/object, cross-signer target, or wrong state | Appliance parser and import admission reject under ISO-K31/K33. The missing exact host-observable import outcome after this internal decision is TRI2-M01. |
| hot, simultaneous, stale, prior, shared, writable, or reused signer media; missing shutdown/detachment | Common one-shot order and ISO-K25 reject before the next route/state. |
| active request replay or crash at host/appliance pending | Host signer-media and appliance anti-replay machines make pending uncertainty terminal; ISO-K20. |
| signer-media ledger restored behind its witness | Independent head mismatch invalidates the candidate under ISO-K20/P18. |
| repeat PoP or cross-signer request/capability | One own proof at pop-context-bound and exact signer/capability/object admission reject. ISO-K16/K32. |
| changed commitment or challenge after context binding | Exact manifest hashes and bound context mismatch; ISO-K16/K31. |
| transcript reorder/count/hash change | Exact 21-entry registry order and transcript hash fail; ISO-K33. |
| registry differs from commitments or signer entry | Byte-equality, strict registry, and own-entry checks fail; ISO-K33. |
| PoP reused as ordinary authority | Exclusive scope and active-request rules reject. ISO-K34. |
| descriptor signed by an arbitrary key | Descriptor signature/signer fields are forbidden; TCB admission is the sole authority. ISO-R22. |
| descriptor edited after freeze | Descriptor hash, immutable ISO object/hash, admission, and bound ledger event mismatch. ISO-P17/R07. |
| descriptor made self/ISO-digest circular | Canonical schema omits both values; extra/circular field rejects. ISO-P16. |
| descriptor paired with another ISO, VM, policy, medium, or ledger event | Exact host admission and post-run cross-check fail. ISO-P17/R07. |
| two VM records try to share a second actor nonce | Any second invocation_nonce or alternate external uniqueness value is forbidden. ISO-C13. |
| duplicate invocation ID or conflicting role/VM reservation | Atomic project-lifetime reserve/binding rejects before provisioning. ISO-P15/P18. |
| concurrent reservation race | Exactly one reserve-if-absent may succeed; the frozen losing attempt rejects without redraw. ISO-P18. |
| failed-run or successor-version ID reuse | Terminal never frees an ID; ISO-P15. |
| invocation ledger restored behind witness | Ledger/witness head mismatch invalidates the candidate. ISO-P18. |
| boot authorization reused | One atomic boot-consumed transition rejects second consume. ISO-P17/P18. |
| topology/count/edge/store/signer regression | Exact 32/40/8/21+1/22/27/46/64 reconstruction and machine-readable successor rule reject the changed inventory. |
| provider, implementation, protected-material, E0, scoring, S0, or central-system claim opened by this review | Closed-gate and claim-limit rules reject; no such action occurred. |

## 11. Predecessor-finding dispositions

| Finding | Disposition |
|---|---|
| TRI-B01 | Original blocking defect is repaired at proposal-text level. Exact-order-L A/R checks and the uncofactored Boolean equation reject identity, small-order, mixed-order, and cofactored-only paths at every required boundary. TRI2-m01 is a separate vector-source citation defect, not a reopening of the predicate. |
| TRI-B02 | Original registry-digest/signature-scope circularity is repaired at proposal-text level. Two non-root classes, a separate root ceremony, inert registry validation, external activation, exact packages, and anti-replay states form a noncircular path. TRI2-M01 is a new import-outcome evidence defect in that successor lifecycle. |
| TRI-M01 | Repaired at proposal-text level. The unsupported signature is removed; descriptor and admission bytes have one explicit TCB authority, noncircular hash order, host/guest responsibility split, and post-run rejection. |
| TRI-M02 | Repaired at proposal-text level. The second actor nonce is deleted; one CNG invocation ID is reserved forever, binds all lifecycle/evidence paths, salts HKDF, and is protected by atomic reservation, boot consumption, and rollback witnesses. |

## 12. New findings

### TRI2-M01 — no exact observable outcome for the three state-changing import routes

Severity: major.

Counterexample: attach a registry-binding-v1 ISO to a pop-issued appliance.
Compare two executions: in the first, every file verifies and the appliance
records registry-bound; in the second, registry-envelope.bin is changed and
the appliance correctly refuses the transition. Both routes use no result
medium, both shut down, and both detach the ISO. The host-visible design gives
no canonical result/status frame, attestation, readback, or other exact channel
that distinguishes those outcomes.

Revision section 4.3.6 nevertheless permits signer-media
consumed/accepted only after exact result/state evidence. Section 4.3.5 fixes
result_media_id to zero for imports, while sections 4.3.1 and 4.4 define no
replacement outcome artifact. The same gap affects preactivation-context,
registry-binding, and activation-binding imports. ISO-K31/K33 specify the
target's internal rejection but do not supply the host evidence needed to
append accepted versus terminal in the mirrored ledger.

The host must therefore either deadlock without a consumed transition or infer
success from shutdown/detachment, which is identical for a failed parse. This
leaves a required state, lifecycle, and evidence route materially incomplete.
It does not by itself grant experimental authority, so major rather than
blocking is appropriate.

Exact required repair: define one bounded, canonical, host-observable outcome
route for every import class. It must bind campaign, ceremony, signer, import
class, from/to state, exact package and admission hashes, capability,
before/after appliance state, decision, and the corresponding signer-media
events; define success, parse rejection, crash, missing outcome, duplicate,
and host/appliance disagreement; and update the zero-result-media rule,
evidence fields, ledger transition, and hostile acceptance rows consistently.
The repair must state its TCB/signature authority and preserve the frozen
experimental topology unless a separately reviewed change is intended.

### TRI2-m01 — RFC 9381 section 5.4.5 is not the stated source of bad_y2 or four order-eight encodings

Severity: minor.

The strict-profile future-evidence section says the decimal bad_y2 value and
its four sign/y encodings are specified by RFC 9381 section 5.4.5. The exact
official section defines ECVRF key validation as multiplying the supplied key
by the cofactor and rejecting identity. It contains neither that decimal
coordinate nor those four encodings, and the decimal does not occur elsewhere
in the official RFC text. See
https://www.rfc-editor.org/rfc/rfc9381.html#section-5.4.5.

The order-L acceptance predicate remains exact, and the candidate already
requires a later independent implementation reviewer to verify vector
construction and point order. The wrong attribution therefore does not grant
authority or weaken isolation, but it is a reproducibility/exactness defect.

Exact required repair: remove the false section attribution and either provide
an independently checkable derivation plus exact 32-byte encodings or cite an
official primary source that actually contains them. Retain the independent
order/construction check and do not treat a copied label as evidence.

## 13. Finding counts and verdict

| Severity | Count | IDs |
|---|---:|---|
| blocking | 0 | none |
| major | 1 | TRI2-M01 |
| minor | 1 | TRI2-m01 |

REVISE-AND-REVIEW

Any finding requires this verdict. The zero-finding pass verdict is therefore
unavailable.

## 14. Facts, inferences, proposals, and test-result boundary

Facts established by this review are the exact authenticated baseline, the
composition map, the 32/40/8/21+1/22/27/46/64 counts, the 107-row inventory,
the written request/package/state/ledger grammars, the two findings, and the
fact that no implementation test was run.

Review inferences are that the original four defects are repaired at
proposal-text level, A-D retain equal public source/authority/model/time/
scoring opportunity, and the remaining import-outcome gap prevents a
zero-finding disposition.

Proposals remain proposals: strict cryptography, keys, appliances, VMs,
descriptors, admission, ledgers, witnesses, stores, providers, and all 107
tests remain unimplemented and unvalidated.

No cryptographic, platform, provider, model, acceptance, E0, or S0 test result
was produced. Hash/sidecar authentication, text construction counts, and
primary-reference reading are document-review checks only.

## 15. Maximum justified claim and exact next gate

The maximum justified claim is:

At commit cb4198f4475881ba5b607517fdbb4f0db6b8ce5d, the authenticated public
v0.2 composition preserves the frozen topology and A-D experimental
opportunities and repairs TRI-B01, TRI-B02, TRI-M01, and TRI-M02 at
proposal-text level. It still has one major import-state evidence defect and
one minor cryptographic-vector citation defect. It is not suitable for CONTROL
integration consideration in this version.

No verdict here opens implementation, provisioning, key generation, protected
material, provider/model sessions, judge handoff, scoring, E0, or S0, and no
conclusion extends beyond the frozen synthetic logic design.

The exact next permissible gate is:

S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN
