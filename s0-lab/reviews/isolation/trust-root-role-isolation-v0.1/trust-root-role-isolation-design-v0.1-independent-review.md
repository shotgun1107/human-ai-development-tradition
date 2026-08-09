# S0 v0.14 trust-root and role-isolation design independent review v0.1

- `review_kind`: fresh independent public-only hostile design review
- `review_date`: `2026-08-09` KST
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`
- `reviewed_commit`: `ccedcbc3a6a029df76d4d612b2978370558c87fb`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_count`: two blocking, two major, zero minor
- `claim_kind`: public design review only

No implementation test was run. No VM was provisioned, no host setting was
changed, no key, account, vault, canary, fixture, script, validator, model
session, or provider session was created, and no implementation acceptance test
was executed. No sealed, oracle, bank, label, condition-map, executor-output,
E0, or non-allowlisted repository material was read.

## 1. Review authority, independence, and baseline

The reviewer did not author the candidate, did not call a subagent, did not
read another reviewer conclusion about this candidate, and used only the exact
public allowlist and permitted primary references. The authenticated v0.14
predecessor review was treated as predecessor evidence, not as an answer key.
Worktree separation was treated as edit isolation, not secret isolation.

The first metadata check found the required local candidate remote-tracking ref
absent and stopped before substantive reading. CONTROL alone fetched that ref
and explicitly superseded the provisional stop. The reviewer deleted the
provisional invalid-output pair, restarted authentication from zero, and
obtained this exact result before opening any substantive input:

| Check | Required and observed value | Result |
|---|---|---|
| review worktree | `C:\Users\kimsiyeol\.codex\worktrees\s0-isolation-design-review` | pass |
| origin | `https://github.com/shotgun1107/human-ai-development-tradition.git` | pass |
| branch | `codex/s0-trust-root-role-isolation-design-v01-review` | pass |
| HEAD | `ccedcbc3a6a029df76d4d612b2978370558c87fb` | pass |
| candidate remote ref | `origin/codex/s0-trust-root-role-isolation-design-v01` = `ccedcbc3a6a029df76d4d612b2978370558c87fb` | pass |
| worktree state | no porcelain entries | pass |

## 2. Input authentication

All 16 exact substantive files were hashed before their text was relied upon
and were then read in full. The repository's same-basename convention replaces
`.md` with `.sha256`; it does not append `.md.sha256`. Eleven such sidecars were
available and all eleven contained the exact Markdown digest and canonical
Markdown filename. `AGENTS.md` had no same-basename sidecar. The three I1
`.sha256` manifests below were substantive inputs in their own right.

| Exact input | Verified SHA-256 | Sidecar authentication |
|---|---|---|
| `AGENTS.md` | `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` | `AGENTS.sha256` absent |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | pass; sidecar SHA-256 `ffcd795bb94f78f69b404cb49955130c3bf4ae4fff12b026a1b3584cbd391963` |
| `s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.md` | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` | pass; sidecar SHA-256 `ff71deea0b0aaac3a6f46d703376b22f677baa4d0e20be22a42f98a449706766` |
| `s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md` | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` | pass; sidecar SHA-256 `7f30298de0667cd01991e72704b963a20ebb558e1e76474eb212d8a67842d888` |
| `s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.md` | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` | pass; sidecar SHA-256 `24ce405c3987410cd2a2f6cba0ce4ec83a235f8b23b013d908675797432e8310` |
| `s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.md` | `537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605` | pass; sidecar SHA-256 `e73f0bb18e65f39b6ebb8ac0fda00ef4f756a3a01000f97db9fb9a41ac0eaf6c` |
| `s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md` | `f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65` | pass; sidecar SHA-256 `8c90eda5c1557c1f31e977f94ec6985e8799a692e56141a830e6cc8ff7f685b4` |
| `s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.md` | `167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925` | pass; sidecar SHA-256 `36a1565b93df98f2d18f8447280458df66a0d38dacf2aa4bb56cc4b7a7564c40` |
| `s0-lab/i1/spec/public-runtime-v0.14.json` | `fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08` | authenticated directly and by the listed public-spec manifest |
| `s0-lab/i1/spec/public-runtime-files.sha256` | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` | substantive manifest input |
| `s0-lab/i1/verification/implementation-files.sha256` | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | substantive manifest input |
| `s0-lab/i1/verification/implementation-manifest.sha256` | `1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6` | substantive binding input |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.md` | `6a062383742e90409f5dac9c443de90b93773c266525ba00f3802b60d40ff6fc` | pass; sidecar SHA-256 `7a0bc9043ae8ac2e59d4ef0aa1a8723835865717f0054e818711cc7809df8601` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.md` | `ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0` | pass; sidecar SHA-256 `08fef8b7e5c31f94983b5f24cdfae44aeb5f7137cbcf81854130f589ea6ac61d` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.md` | `71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937` | pass; sidecar SHA-256 `6caf7c1ca42e5ed1c81f45d481cc4403d637156068d8a9f48d61d98a9349dc3a` |
| `s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.md` | `88ca9ae00ee8a76f1f01865be7ffc106afede4a8207c86fab1bb72c9099e8d7a` | pass; sidecar SHA-256 `5553c4fa3698186ad1eae160143e4a97b30aba651e033db38f4c3d654352224a` |

The candidate-linked Microsoft references reproduce the relevant platform
facts: a private Hyper-V switch still connects guests to each other; PowerShell
Direct does not require guest networking; Enhanced Session Mode exposes RDP
device and clipboard channels; integration services are host/guest
communication channels; and importing a VM as a copy creates a new VM ID.
[RFC 8032](https://www.rfc-editor.org/rfc/rfc8032) supplies the exact Ed25519
point decoding and cofactored verification equation used in finding TRI-B01.
[NIST SP 800-89](https://csrc.nist.gov/pubs/sp/800/89/final) separately names
public-key-validity assurance and private-key-possession assurance; one does not
replace the other.

## 3. Independent topology reconstruction

Targeted parsing of the authenticated I1 topology, followed by an independent
position/signing reconstruction from the plan responsibilities, produced:

| Inventory | Reconstructed result |
|---|---:|
| aggregated role rows | 32 |
| role positions | 40 |
| paired rows | 8 |
| experimental section-4 signer bindings | 21 |
| `none` signer bindings | 19 |
| non-row root signer | 1 |
| unique registry signer IDs | 22 |
| stores | 27 |
| explicit reader entries | 46 |
| edge rows | 64 |

The eight paired rows are `label-authors`, `leakage-reviewers`,
`comparator-builders`, `expected-catalog-generators`, `p1-reviewers`,
`blinded-map-builders`, `semantic-judges`, and `comparator-operators`.

### 3.1 Exact row-position-signer total map

| Role position | Section-4 signer ID |
|---|---|
| `registrar:single` | `control-registrar` |
| `public-status-reader:single` | `none` |
| `public-record-publisher:single` | `public-record-publisher` |
| `public-record-reader:single` | `none` |
| `content-intake:single` | `content-intake` |
| `simulation-builder:single` | `simulation-builder` |
| `fact-author:single` | `none` |
| `label-authors:A` | `none` |
| `label-authors:B` | `none` |
| `label-comparison:single` | `label-comparison` |
| `representation-builder:single` | `representation-builder` |
| `package-builder-scanner-1:single` | `none` |
| `scanner-2:single` | `none` |
| `scan-comparison:single` | `scan-comparison` |
| `leakage-reviewers:1` | `none` |
| `leakage-reviewers:2` | `none` |
| `leakage-comparison:single` | `leakage-comparison` |
| `comparator-builders:1` | `comparator-builder-1` |
| `comparator-builders:2` | `comparator-builder-2` |
| `expected-catalog-generators:1` | `none` |
| `expected-catalog-generators:2` | `none` |
| `catalog-comparison:single` | `catalog-comparison` |
| `p1-reviewers:1` | `none` |
| `p1-reviewers:2` | `none` |
| `p1-review-comparison:single` | `p1-review-comparison` |
| `condition-map-schedule-custodian:single` | `none` |
| `blinded-map-builders:1` | `none` |
| `blinded-map-builders:2` | `none` |
| `analysis-map-comparison:single` | `analysis-map-comparison` |
| `dispatcher-transport-recorder:single` | `none` |
| `public-executor:single` | `none` |
| `raw-output-custodian-anonymizer:single` | `none` |
| `semantic-judges:1` | `semantic-judge-1` |
| `semantic-judges:2` | `semantic-judge-2` |
| `judgment-comparison:single` | `judgment-comparison` |
| `comparator-operators:1` | `comparator-operator-1` |
| `comparator-operators:2` | `comparator-operator-2` |
| `adjudication-comparison:single` | `adjudication-comparison` |
| `analysis:single` | `analysis` |
| `final-decision-custodian:single` | `final-decision-custodian` |
| non-row `control-root-authority` | `control-root-authority` |

The 21 experimental signer bindings are unique. Adding the one non-row root
produces the authenticated 22-ID registry set with no missing or extra ID.

### 3.2 Stores, readers, and edges

The 27 store IDs are:

`registrar-receipt-vault`, `registrar-store`, `public-decision-store`,
`content-vault`, `label-vault-A`, `label-vault-B`, `agreed-label-vault`,
`representation-vault`, `signed-package-vault`, `scan-vault-1`,
`scan-vault-2`, `leakage-vault-1`, `leakage-vault-2`,
`comparator-vault-1`, `comparator-vault-2`, `generator-vault-1`,
`generator-vault-2`, `analysis-input-vault`, `catalog-vault`,
`p1-review-vault-1`, `p1-review-vault-2`, `condition-map-vault`,
`analysis-map-vault`, `raw-output-vault`, `judgment-vault-1`,
`judgment-vault-2`, and `final-decision-vault`.

In that order their explicit reader-entry counts are
`1,1,2,3,1,1,8,2,4,1,1,1,1,1,1,1,1,1,4,1,1,3,1,1,1,1,1`, totaling 46.
The edge list is exactly E00A-E00H followed by every E01-E56 once, in order:
64 unique rows with no gap or extra ID.

The logical ACL does not claim that the four infrastructure mediators or the
host administrator lack physical byte access. Input routing, ingestion/export,
trusted staging, and immutable commit are TCB principals with stage-specific
object capabilities, while the 27-store reader list is experimental semantic
authority. Registrar payload exclusions remain exact: on E25, E27, E29, E35,
E48, and E50 the registrar receives only the receipt leg.

### 3.3 Identity, VM, channel, and route reconstruction

The four identity domains are: disposable one-position/one-invocation actor
VMs; 21 campaign-lifetime non-root signer appliances; one separate offline
non-row root environment; and TCB route/ingestion/store/hypervisor
infrastructure. A signer appliance never acts as its row's actor and an actor
never receives a private key.

The single `public-executor:single` position is a template for exactly eight
future actor/external-session pairs: four conditions times two blocks. Each
pair handles one unit, none inherits from a fixture author or another executor,
none sees another output, and maximum concurrency is three.

The actor profile requires no virtual NIC, no Enhanced Session or RDP resource
redirection, no clipboard/drive/USB/printer/audio/video/smart-card channel, no
host share, no KVP/data exchange/time sync/backup/Guest Service Interface/file
copy, no PowerShell Direct, no COM named pipe, no Hyper-V socket or custom
VMBus endpoint, no interactive console, no Git material, and no unlisted
device. Heartbeat and orderly shutdown are the only residual guest signals;
the host administrator remains a declared TCB capability.

Input flows from exact source object capabilities into a finalized read-only
ISO. Output flows to one blank invocation VHDX, is attached read-only to two
clean ingestion VMs, and is extracted by two independent extractors into two
filesystem-free raw frames. The trusted-staging parser requires complete
byte-identical frames, exact hashes and lengths, and a zero tail before one
invocation unit can reach immutable commit. Hostile path, reparse, ADS,
hard-link, sparse/compressed/encrypted/offline, malformed-filesystem,
non-regular-object, second-ingest, and partial-unit cases reject with zero store
change. Temporary replicas have frozen ACLs, attachment events, deadlines, and
logical-destruction state; deletion is expressly not claimed as cryptographic
erasure.

E49 is stricter than receipt arrival alone. The E48 protected payload/hash,
the analysis producer receipt, and the corresponding committed E51
status-envelope/bundle pair at `A-0fff` must all authenticate before the
semantic map may be released.

## 4. Trust-root and signer reconstruction

The external root is noncircular at proposal level: verification starts from a
user-supplied exact SHA-1 Git commit and anchor hash, not from a branch, tag,
`HEAD`, timestamp, or repository-discovered latest value. The activation record
also fixes repository, 32-byte campaign ID, registry v1, registry-envelope hash,
proof-transcript hash, and approved state. Anchor bytes are verified before the
root-signed registry.

Registry v1 has exactly 22 active entries in the inherited fixed order. Keys
and key IDs are unique, every key ID is SHA-256 of exactly 32 raw public-key
bytes, the root entry equals the anchor, and only the root signs the registry.
Twenty-one non-root signer appliances must prove possession after a commitment
manifest and per-role random challenges freeze; the root's registry signature
is its possession evidence. The transcript freezes before the root signature,
and external activation binds that transcript hash. PoP is correctly limited in
claim: it does not prove human identity, role authorization, root trust,
non-exportability, or wall-clock freshness.

The candidate also correctly states that registry v1 has no in-place rotation,
revocation, expiry, or mutation. Loss and suspected compromise follow distinct
stop rules, temporary signing media are replicas, signer appliances persist on
a separate campaign state machine, and existing signatures cannot authorize a
resumed run after the applicable stop.

The section-4 registry scope is the inherited generic-envelope scope. Other
predecessor artifacts called signed remain
`inherited-signature-unresolved`; the candidate does not silently add registry
roles or silently treat them as unsigned. Findings TRI-B02 and TRI-M01 show
that the candidate's own new signature-bearing objects are not closed by that
two-scope statement.

The two implementation blockers are preserved as blockers, not claims:
`external-provider-isolation-unresolved` prevents an execution-package freeze
until provider-specific session/revision/history/tool/origin constraints pass,
and `signer-custody-provider-unresolved` prevents key generation until a
concrete non-exportable provider and custody profile pass separate design and
implementation review. `inherited-signature-unresolved` also blocks package
freeze.

## 5. Hostile tabletop mutation trace

These were paper constructions only. “Exact reject text” below names the
candidate acceptance-plan result or, for an unhandled case, identifies the
absence that creates a finding.

| Class | Concrete mutation | Exact candidate disposition | Assessment |
|---|---|---|---|
| platform | Attach a NIC to a private switch, then attempt guest-to-guest traffic. | ISO-P05/P06: `Reject before boot`; ISO-C01: every attempt fails because no role interface exists. | handled |
| residual Hyper-V channels | Enable Enhanced Session clipboard, KVP, Guest Service Interface, PowerShell Direct, COM named pipe, or a Hyper-V socket. | ISO-P07-P12 and ISO-C11/C12: reject before boot/execution or fail and log. | handled |
| ambient repository | Put `.git`, a remote, credential helper material, or a provider token on the input ISO. | ISO-R02: `Reject before attachment`; ISO-C02: fails with no metadata/credential/remote. | handled |
| base/instance identity | Import without a new VM ID, reuse a writable disk, or bind an existing invocation ID to another position. | ISO-P03/P15: reject before import, boot, or both. | handled |
| hostile filesystem | Emit `..`, a device name, ADS, symlink, junction, hard link, and malformed filesystem in one VHDX. | ISO-R13/R14: disposable ingestion rejects or quarantines before host path following or store change. | handled |
| dual ingestion/frame | Make extractor 2 change one content byte, leave a nonzero raw-disk tail, or add a filesystem to the export disk. | ISO-R20: `Reject with zero staging/store change`. | handled |
| route | Change one source store, edge, recipient, phase, hash, or signature while retaining the declared object ID. | ISO-R07: `Reject`. | handled except descriptor authority in TRI-M01 |
| registrar split | Send E48 protected analysis bytes, rather than only its receipt, to registrar. | ISO-R08: `Reject and quarantine`. | handled |
| immutable admission | Re-ingest an invocation, replace an object, or fail the last artifact of a multi-output unit. | ISO-R06/R11/R15: reject with original state unchanged and zero accepted changes. | handled |
| pair atomicity | Crash after writing only one E51 or E54 member. | ISO-R10: neither member accepted; no partial visible state. | handled as a future implementation requirement |
| logical ACL versus TCB | Give a mediator a parent listing/wildcard or put a payload canary in a mediator log. | ISO-R18/R19/R21: reject, invalidate candidate/campaign, or both. | handled |
| pair independence | Give paired position 2 position 1's disk, receipt, key, log, or visible result. | ISO-I01-I05/I07: reject the pair, registry candidate, or independence claim. | handled |
| executor multiplicity | Create seven executors, reuse one for two units, or run four concurrently. | ISO-L07: `Reject`. | handled |
| signer custody | Export/dump a key, use a shared folder/network/PowerShell Direct, or mount a signature-result filesystem. | ISO-K09/K21/K25/K26: reject and, where applicable, invoke compromise stop. | handled at requirement level; provider remains unresolved |
| registry | Reorder two entries, duplicate one key, change the root entry, or use a non-root registry signature. | ISO-K05/K06: `Reject`. | handled |
| external activation | Supply a branch, tag, abbreviated commit, wrong campaign, or omit the transcript digest. | ISO-K22: `Reject without fallback`. | handled |
| PoP transcript | Repeat a challenge nonce or change role/key/commitment bytes after commitment. | ISO-K15/K16/K18: reject proof and registry candidate. | handled |
| public-key validity | Use canonical Ed25519 identity encoding for A and R and `S=0`. | No candidate reject applies; detailed in TRI-B01. | **unhandled blocking mutation** |
| pre-activation PoP route | Ask a key-generated but not registry-bound appliance to sign its required PoP before registry assembly. | The appliance rule requires a registry digest and frozen edge/artifact kind, while K10 rejects an unlisted kind; no admissible request class exists. | **unhandled blocking mutation** |
| signature inventory | Classify the new PoP transcript or the new signed invocation descriptor under the stated section-4/inherited partition. | ISO-K24 rejects an artifact in neither scope; neither object is assigned a permitted scope. | finding TRI-B02/TRI-M01 |
| invocation descriptor | Substitute a descriptor signed by an arbitrary key while preserving media hashes. | The startup service says it validates a signed descriptor, but no signer, preimage, key, or domain is specified. | **unhandled major mutation** |
| invocation nonce | Reuse one external nonce across two fresh VMs with distinct invocation IDs and internally consistent host/guest logs. | No ISO-P/I/L test rejects nonce reuse and no nonce format/generator is defined. | **unhandled major mutation** |
| E48/E49 order | Release E49 after receipt arrival but before the E51 `A-0fff` pair commits. | ISO-R17: reject without semantic-map release. | handled |
| replica lifecycle | Open a new invocation while a failed prior output/staging replica still exists or request a quarantined replica from another role. | Design section 4.1 requires destruction before a new invocation; ISO-R16 denies access and section 8 rejects prior-run residue. | handled as a design requirement |
| v1 loss/compromise | Replace a lost role key in-place or select a new root by timestamp/majority vote. | ISO-K13/K23: reject and require the stated new-version/user-root path. | handled |
| unresolved providers | Freeze an execution package while either provider blocker or inherited signature blocker remains. | ISO-L10: `Reject`. | handled |
| claim limit | Claim protection from host admin, hypervisor compromise, physical attack, side channel, cognitive crossover, or secure erasure. | ISO-L06: `Review rejects the claim`. | handled |
| gate limit | Treat this paper review as implementation evidence or provision a VM during it. | ISO-L09: invalid review and stop; candidate section 9 keeps implementation/S0 gates closed. | handled; no such action occurred |

## 6. Acceptance-plan falsifiability coverage

All 92 expected-result rows were traced on paper; none was executed.

| Test family | Rows reviewed | Tabletop result |
|---|---:|---|
| ISO-P01-P15 | 15 | Platform prerequisites, base identity, VM/device configuration, and channel checks have observable pass/reject results. The separate nonce gap is TRI-M02. |
| ISO-C01-C12 | 12 | Network, Git, host-share, cross-role canary, process, resource, audit, KVP, socket, and COM results are observable and fail closed. |
| ISO-R01-R21 | 21 | Media, route, hostile-filesystem, dual-ingest, immutable admission, TCB capability, logging, E49, and pair-atomicity results are observable. R07 cannot supply the missing descriptor authority in TRI-M01. |
| ISO-I01-I08 | 8 | Pair/co-location/cognitive-independence mutations have exact rejection results. Distinct IDs with a repeated nonce remain outside the table. |
| ISO-K01-K26 | 26 | Canonical encoding, registry, activation, custody, replay, PoP transcript, lifecycle, and result-frame mutations are specified. TRI-B01 is a canonical small-order key/signature that K19 does not reject; TRI-B02 is the missing pre-activation request/scope needed for K11/K15/K24 to coexist. |
| ISO-L01-L10 | 10 | State, retry, claim, executor-count, provider, and review-gate outcomes are exact. |

The noncompensatory acceptance rule is otherwise clear: no skip, waiver,
compensation, or operator substitution can turn a failed row into a pass.

## 7. Findings

### TRI-B01 — Ed25519 public-key validity is not enforced before PoP or registry admission

**Severity: blocking.**

The candidate rejects noncanonical encodings, decoding failure, out-of-range
`S`, wrong lengths, and wrong Ed25519 variants, but never rejects a canonical
small-order public key or requires a non-identity prime-order public key.

A concrete counterexample uses the canonical encoding of the Edwards identity
point for both proposed public key `A` and signature point `R` (`01` followed
by 31 zero bytes) and encodes `S=0` in 32 bytes. The candidate's listed K19
checks all pass: both points decode canonically, lengths are exact, and
`0 <= S < L`. RFC 8032 verification then accepts because both sides of
`[8][S]B = [8]R + [8][k]A` are the identity for every message and every `k`.
The RFC's permitted alternative equation also reduces to identity equals
identity.

Therefore the PoP can verify without possession of any private key. If that
key enters registry v1, the same construction can forge that role's
section-4 signatures on arbitrary records. NIST SP 800-89's separate
public-key-validity and possession assurances make the missing check material;
successful signature verification is not itself public-key validation.

This can admit a forgeable signer binding and undermine every protected route
that trusts that role. The trust root/signature system is not verifiable under
the candidate's own acceptance set. A revision needs exact Ed25519 public-key
validation, including rejection of identity/small-order/mixed-order keys as
appropriate to the selected strict verification profile, plus explicit hostile
vectors for PoP, root, registry, and ordinary artifact verification.

### TRI-B02 — the mandatory pre-activation PoP has no admissible signer-appliance request or signature-scope path

**Severity: blocking.**

Section 5.2 says an appliance accepts a signing request only when campaign ID,
**registry digest**, signer ID, **edge/artifact kind**, domain, request ID,
preimage, and caller capability match the frozen allowlist. Section 5.3 requires
all 21 non-root PoPs **before registry assembly**, and the signer state machine
places `proof-verified` before `registry-bound` and `active`.

At that point there is no defined registry digest to supply, no E00A-E56 edge
or inherited artifact kind for the new PoP, and no defined pre-active request
exception. ISO-K10 requires an out-of-allowlist artifact request to reject;
ISO-K15 requires all PoPs before the root registry signature; and ISO-K24
requires every signature-bearing artifact to belong to exactly one of the
section-4 or inherited scopes. The candidate's plain-Ed25519 public PoP
transcript is new, is not a section-4 envelope, and is not a predecessor
artifact in `inherited-signature-unresolved`.

Thus an appliance following section 5.2 must reject the proof needed to reach
`proof-verified`, while accepting it requires an unlisted request class,
artifact kind, and signature scope. The 21-proof precondition and registry
bootstrap cannot be completed without a revised, independently reviewed
pre-activation ceremony request grammar, state transition, allowlist, media
route, and scope classification.

### TRI-M01 — the signed invocation descriptor has no authentication authority or canonical signature definition

**Severity: major.**

Section 4.1 requires the frozen startup service to read and validate a **signed
invocation descriptor** from the ISO, and output admission later rejects invalid
signatures. The candidate never names the descriptor signer, public key, key
source, canonical preimage, signature domain, exact descriptor grammar, or
verification order. It is not one of the listed section-4 artifacts and is not
a predecessor artifact covered by `inherited-signature-unresolved`.

Consequently ISO-R07 can say that a changed route-manifest signature rejects,
but an implementation cannot distinguish an authorized descriptor signature
from an arbitrary one without inventing a new trust decision. This is a
required launch/route-authentication rule, not a cosmetic implementation
choice. The revision must either define and classify the exact authority and
preimage or remove the unsupported signature claim and replace it with an
equally exact authenticated TCB binding.

### TRI-M02 — invocation nonce generation, uniqueness admission, and reuse testing are unspecified

**Severity: major.**

The candidate precisely defines a 32-byte CSPRNG `invocation_id`, but separately
requires an externally supplied **unique invocation nonce** for invocation-
secret derivation, every state transition, and acceptance evidence. It never
defines that nonce's length, generator, encoding, registry, relation to the
invocation ID, or duplicate-admission rule.

The acceptance plan rejects invocation-ID reuse and host/guest nonce mismatch,
but not reuse of the same nonce across two distinct, internally consistent
invocations. Such a candidate can pass ISO-P15, ISO-C10, and ISO-I01. If cloned
OS entropy state also repeats—the base expressly makes no claim that general OS
entropy state is absent—the repeated external nonce defeats the stated
two-source uniqueness safeguard and can repeat the invocation secret.

The revision needs one exact nonce construction and identity relation, a global
duplicate/replay rejection rule, and a hostile cross-invocation reuse test.

## 8. Finding counts and verdict

| Severity | Count |
|---|---:|
| blocking | 2 |
| major | 2 |
| minor | 0 |

`REVISE-AND-REVIEW`

The allowed pass verdict requires zero findings. The two blocking and two major
findings above therefore prohibit
`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`.

## 9. Maximum justified claim

At commit `ccedcbc3a6a029df76d4d612b2978370558c87fb`, the authenticated
public candidate reconstructs the frozen 32-row/40-position/8-pair/22-signer/
27-store/46-reader/64-edge topology and supplies many explicit fail-closed
platform, route, ACL, lifecycle, provider-limit, and nonclaim rules. It does
not, however, close public-key validity, the pre-activation PoP request/scope,
the signed invocation-descriptor trust path, or invocation-nonce uniqueness.
It is not suitable for CONTROL integration consideration in this version.

This review does not establish implementation, key custody, VM isolation,
external-provider isolation, atomic storage, public validation, sealed
compatibility, representation superiority, S0 success, central-system
implementation, Project Brain integration, operational safety, economic value,
production readiness, model stability, or model-to-model transfer.

## 10. Exact next gate

No later gate opens automatically. The next permissible gate is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`

That revision must address TRI-B01, TRI-B02, TRI-M01, and TRI-M02 on public
untouched material and freeze new hashes. Only after that revision is complete
may CONTROL separately open a fresh
`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`.
Implementation, key generation, provider sessions, protected material, and S0
execution remain closed.
