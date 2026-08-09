# S0 v0.14 trust-root and role-isolation design v0.1

- `status`: design candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN OPEN`
- `baseline_commit`: `93e353ac975c3cb5c948d61609fe4e43c57a0f37`
- `claim_kind`: public design only

## 1. Decision and scope

This candidate defines the security architecture that must exist before any S0
bank, label, oracle, executor, model call, or scoring work can begin. It does
not provision a virtual machine, create a key, create a vault, configure a
network, or open any later S0 gate.

This design has four distinct identity domains:

1. an actor VM is a full Hyper-V Generation 2 VM for one exact role position
   and one invocation, then quarantined and never reused;
2. a signer-custody appliance is a separate campaign-lifetime VM bound to one
   exact section-4 signer ID, retaining only that non-exportable key and a
   bounded anti-replay ledger across authorized signatures;
3. the offline root environment is a separate non-row authority used only for
   the exact registry-v1 signature; and
4. route, ingestion, store, and hypervisor services are trusted infrastructure,
   not experimental role positions.

A frozen actor base image may be reused as a source, but an instantiated actor
VM, its writable disk, output disk, invocation credential, and process state
may not be reused by another position or invocation. A signer appliance may
persist only for its one signer identity and may never execute the actor role,
hold a role vault, or become a general signing oracle. No fake role position is
assigned to root or infrastructure components.

An external AI service is outside that VM boundary. A future model role needs
both the local VM custody/transport controls and a separately gated fresh,
stateless external-session profile. The local VM does not prove provider-side
memory isolation. Future executors must receive only one frozen package through
the approved one-shot transport; future semantic judges remain the user's
manual two-Project Pro handoff with one fresh project/chat/first response each.
Neither external profile is created, contacted, or tested by this gate.

Both external profiles are therefore marked
`external-provider-isolation-unresolved`. An execution package cannot freeze
until a provider-specific profile independently closes model ID/revision,
memory/history, tools, browsing, MCP, retry, packet identity, response origin,
and first-response evidence limits.

For a future manual semantic judge, the returned first response is imported as
an immutable byte artifact into that judge position's actor VM. The actor may
verify the frozen packet/response identity and construct the unchanged E42
record, then request its separate signer appliance to sign only that canonical
preimage. The actor never receives the key and may not edit, retry, complete,
reinterpret, or regenerate the Pro response. The local signature proves only
which custody appliance sealed the supplied bytes; it does not prove provider
origin, first-response status, or provider-side statelessness. The two projects,
response artifacts, actor VMs, and signer appliances remain separate.

Windows Sandbox, Windows users, AppContainer, WSL, job objects, worktrees, and
fresh conversations are not substitutes for that VM boundary. They may later
be used as defense-in-depth or workflow controls only after an independent
review of the exact use. Windows Sandbox is not the primary evidence-producing
environment because it is disposable, permits only one instance at a time,
and starts with networking and clipboard sharing enabled unless explicitly
disabled.

The architecture protects against accidental cross-role contamination,
ambient repository access, ordinary guest-to-guest access, unauthorized
artifact routing, stale input substitution, and a buggy or hostile role
process attempting to use an ungranted channel. It does not claim secrecy or
integrity against the trusted Hyper-V host administrator, compromised
hypervisor or firmware, physical attacks, side channels, deliberate human
retyping or photography, or two nominally independent roles operated by a
person who already knows both results.

## 2. Frozen facts and design proposals

### 2.1 Frozen public facts

The candidate was derived from these public bytes at the baseline commit:

| Input | SHA-256 |
|---|---|
| `AGENTS.md` | `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| v0.14 universal response contract | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` |
| v0.14 public falsification plan | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` |
| v0.14 review response | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` |
| v0.14 independent review | `537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605` |
| v0.14 CONTROL integration decision | `f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65` |
| I1 `public-runtime-v0.14.json` | `fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08` |
| I1 public-spec manifest | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` |
| I1 implementation manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` |
| I1 CONTROL integration decision | `167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925` |

The same-basename sidecars and the I1 manifests remain the authentication
records; this table does not replace them.

The CONTROL-integrated v0.14 public topology contains:

- 32 aggregated role rows;
- 40 actor positions after expanding the eight paired rows;
- 22 canonical section-4 Ed25519 signer role IDs;
- one `control-root-authority` outside the 32 experimental role rows;
- 27 literal stores;
- 64 edge rows, E00A-E00H and E01-E56;
- 14 ordered status edges, 15 status states, 17 evidence receipts, and 15 E51
  envelope/bundle pairs.

An aggregated row, actor position, signer role ID, VM instance, and human or AI
operator are different identifiers. No 40-entry signing registry is inferred.
Only the frozen 22 signer IDs may appear in registry v1.

The accepted I1 runtime authenticates public bytes and enforces public
structure under a trusted caller. Its Python objects are API discipline, not a
hostile same-process security boundary. This design supplies the later OS
boundary; it does not reinterpret I1 as already secure against hostile code.

### 2.2 New design proposals

This candidate proposes:

- a single-host, trusted-administrator Hyper-V isolation profile for the
  synthetic S0 experiment;
- a one-role-position, one-invocation, one-new-VM rule;
- an offline input/output airlock using read-only input media and a unique
  output disk instead of shared folders or repository mounts;
- a fail-closed route controller that copies bytes only along frozen edges and
  never becomes a new semantic S0 role;
- an offline root ceremony and per-signer private-key custody profile;
- machine-verifiable launch, transfer, shutdown, and quarantine evidence; and
- mandatory negative tests before any protected input exists.

These remain proposals until fresh independent review and a later CONTROL
integration decision.

## 3. Trusted computing base and threat model

### 3.1 Trusted components

For this single-PC design, the trusted computing base is:

1. the user-approved exact Git commit used as the public root pin;
2. the Windows host, its firmware, Hyper-V hypervisor, storage, and patch
   state;
3. the host administrator acting as CONTROL;
4. the independently authenticated actor and ingestion VM bases, frozen
   bootstrap/extractor services, and provisioning policy;
5. four distinct least-privilege infrastructure principals: input route
   controller, ingestion/export verifier, trusted-staging verifier, and
   immutable-store committer;
6. every signer appliance's OS, domain-restricted signing service,
   non-exportable Ed25519 provider, and anti-replay ledger;
7. the signature and canonical-record verifier; and
8. the offline `control-root-authority` environment.

The four infrastructure principals do not share one wildcard credential. The
route controller can read only exact granted source objects and build input
media; ingestion can read only one detached output image and write one raw
export frame; staging can read the two raw frames for one invocation and emit
one verified unit; store commit can write only that verified unit to its exact
destinations. None may enumerate a parent namespace or assume another
principal's capability.

Compromise of any item above invalidates isolation evidence. Ordinary Hyper-V
on one client PC does not protect a role from that PC's administrator. If the
administrator is in the threat model, S0 must stop and move to separately
administered physical hosts or a separately reviewed guarded-fabric design.

### 3.2 Protected assets

The protected assets are private signing keys, future bank and prompt bytes,
future agreed labels or oracle material, the semantic condition map, raw and
anonymous outputs, comparator and judge internals, role-local state, frozen
public inputs, and the integrity and order of edge deliveries.

### 3.3 Fail-closed objectives

For every role invocation:

- the role sees exactly the inbound artifacts authorized for its position and
  phase, plus approved public runtime bytes;
- it cannot see another position's input, output, key, vault, prior state,
  conversation, Git metadata, or credentials;
- it has no ambient network, clipboard, drive redirection, host folder,
  PowerShell Direct, guest file-copy, or Git channel;
- it can emit only the artifacts allowed by its outbound edges to a unique
  output medium;
- CONTROL admits output only after byte, manifest, route, signature, freshness,
  and duplicate checks; and
- any mismatch stops the invocation before a later phase is prepared.

## 4. Normative Hyper-V role profile

### 4.1 Base and instance lifecycle

The implementation must independently authenticate one stopped Generation 2
base export. Every invocation imports it as a copy with a new VM identifier,
uses a new writable differencing disk, and binds exactly one
`role_position_id` and one globally unique `invocation_id`. The actor instance
is that exact binding; there is no second serialized `actor_instance_id`.
CONTROL generates the invocation ID as 32 random bytes from an approved CSPRNG
and renders it as 64 lowercase hex characters outside binary frames. A
duplicate invocation ID, conflicting position binding, or reused VM ID rejects.
No checkpoint or prior role disk is used as proof of integrity. Base export,
VM configuration, input media, output media, and approved executable hashes are
recorded before boot.

The base contains no role assignment, machine credential, cached user secret,
certificate/private key, browser/profile, provider token, Git material, prior
output, project/application-owned DRBG state, generated project secret, or
signer-key material. General operating-system entropy state is not claimed
absent. Each imported actor receives a new OS/machine identity and an invocation
secret derived after that identity exists by combining an approved OS CSPRNG
with the externally supplied unique invocation nonce, before protected input is
attached. Two clones must not produce the same invocation secret.

The only boot path is a frozen startup service in the authenticated base. It
reads the signed invocation descriptor from the read-only ISO, validates the
role/ID/media/executable binding, launches the one exact approved executable
under a restricted invocation-local principal, enforces the frozen executable,
child-process, token, privilege, and resource allowlists, seals output, and
shuts down. No interactive command is needed or permitted.

Only the small number of roles active in the current phase need instantiated
VMs. Forty simultaneously running or persistent VMs are neither required nor
permitted by this design.

After output ingestion, the actor VM is powered off and moved to
`quarantined`. Re-entry, resume, checkpoint rollback, reassignment, and reuse
reject. Input ISO, output VHDX, actor writable disk, ingestion staging, and
temporary copies are explicitly TCB-controlled temporary replicas, not extra
experimental stores. Their ACL, attach/detach events, retention deadline, and
logical destruction state freeze before protected work. No other actor or
signer may attach or enumerate them. Successful replicas are destroyed after
two independent ingest checks; failed replicas remain inaccessible only until
failure evidence is frozen and must be destroyed before a new invocation is
opened. Deletion is not described as cryptographic erasure and physical
residual protection remains a host/volume-encryption TCB assumption.

### 4.2 No ambient communication

The preflight must prove all of the following before boot:

- no virtual network adapter is attached;
- Enhanced Session Mode and all RDP resource redirection are disabled;
- clipboard, drive, USB, printer, audio-input, video-input, and smart-card
  redirection are disabled;
- host folder mapping and `\\tsclient` paths are unavailable;
- Hyper-V integration services are exact-allowlist: only heartbeat and orderly
  shutdown may remain enabled; data exchange/KVP, time synchronization, backup,
  Guest Service Interface, and guest file-copy are disabled;
- general-purpose host-to-guest data or command paths, including PowerShell
  Direct, are unavailable to the role operator during the measured interval;
  the fixed heartbeat and orderly-shutdown signals are the only exceptions,
  while the host administrator remains an explicit TCB capability;
- both virtual COM ports are disconnected and no host named pipe is bound;
- no Hyper-V socket service, `GuestCommunicationServices` endpoint, or custom
  VMBus endpoint is enabled for the role;
- no VMConnect, RDP, console, keyboard, mouse, or other interactive operator
  session is open during the measured role interval;
- no Git repository, `.git` directory, Git remote, SSH agent, Git Credential
  Manager material, provider token, browser profile, or host credential is on
  any attached medium; and
- the role VM has no device passthrough not explicitly included in the frozen
  profile.

`No network` means no virtual NIC, not merely a firewall rule or a private
virtual switch. A private switch still permits VM-to-VM communication.

A future dispatcher transport exception must be separately designed and
approved with the execution package. It may not silently weaken this default.
Only that transport component may receive an exact provider egress exception;
the role package never gains browser, MCP, Git, arbitrary network, conversation
history, retry, or cross-run access.

### 4.3 Input and output airlock

Roles never mount a live host repository or a logical vault. The route
controller creates a per-invocation input manifest containing exact artifact
IDs, source store IDs, edge IDs, byte lengths, SHA-256 values, and authenticated
envelope identities. It rejects any artifact not authorized by the frozen
role/store/edge topology.

Approved input bytes are placed on a finalized read-only ISO. The ISO contains
no `.git` data, secrets not assigned to the role, prior outputs, ambient
directory listing, or unlisted common resource. Its complete-file-set manifest
and image hash freeze before attachment.

The only writable exchange medium is a new, invocation-specific blank VHDX.
The role writes one canonical output manifest plus the allowed output files.
After shutdown, CONTROL detaches the disk but does not mount the guest-authored
filesystem on the host. The same VHDX is attached read-only, one at a time, to
two clean disposable no-network ingestion VMs using independently implemented
extractors. They have no vault, key, repository, host share, or common writable
disk. Each validates a bounded flat ASCII relative-path grammar and rejects any
path traversal, reserved/device name, case or Unicode collision, reparse point,
junction, symlink, mount point, alternate data stream, hard-link count above
one, sparse/compressed/encrypted/offline file, unlisted file, malformed
filesystem, or non-regular object. Normal path-following against a host path is
forbidden.

Each extractor writes one canonical non-filesystem export frame to its own new
raw output disk. The disk has no partition table or filesystem. The frame is:

```text
magic: exact ASCII `S0-INGEST-EXPORT-1\n`
invocation_id: 32 raw bytes
entry_count: unsigned 32-bit big-endian
total_frame_length: unsigned 64-bit big-endian
for each entry in ascending ASCII path-byte order:
  path_length: unsigned 16-bit big-endian, 1..255
  path: that many permitted ASCII bytes
  content_length: unsigned 64-bit big-endian within frozen ceiling
  content: exact bytes
  content_sha256: 32 raw bytes
frame_sha256: 32 raw bytes over every preceding frame byte
```

All bytes after `total_frame_length` to the raw disk's frozen capacity must be
zero. The host never mounts either export disk. The trusted-staging verifier
opens each as a raw read-only device through the frozen virtual-disk API, uses
an independently implemented bounded frame parser, recomputes every length and
hash, and requires both complete frames to be byte-identical. Any extractor,
frame, parser, or equality failure rejects with zero staging/store change.

Only the agreed raw frame becomes trusted staging and is authenticated as a
complete invocation unit. Existing
object IDs, extra files, missing files, invalid signatures, unexpected bytes,
wrong destinations, or a second ingest reject the entire invocation with zero
store changes. Only after every artifact passes may the future store backend
commit the whole invocation unit. E51 and E54 retain their stricter inherited
pair semantics.

The input route controller, ingestion/export verifier, trusted-staging
verifier, immutable-store committer, and host administrator are TCB byte-access
principals, not experimental semantic readers in the 27-store ACL. Their
physical ability to access bytes is a trust assumption, not a technical proof
that they cannot interpret content. Each service receives only its exact
stage-specific object capability; none receives a parent listing, wildcard,
cross-store search, discretionary read/write, recipient choice, or another
service's credential. They may copy, hash, compare, and enforce their frozen
stage but may not repair output, add an edge, or expose protected bytes to the
registrar. Their logs contain identifiers, sizes, hashes, decisions, and
ordered event IDs only; a protected-payload canary in any infrastructure log
rejects the campaign. Compromise or semantic inspection by a TCB principal
invalidates the evidence.

### 4.4 Vault realization constraints

The future backend must realize all 27 frozen stores as distinct immutable
namespaces. Each namespace has exactly the frozen writer and readers, with
edge- and phase-scoped grants. There is no ambient parent-directory listing,
administrator convenience share, synonym, mirror, or cross-vault search.

Those 27 writers and 46 reader entries are the exact experimental logical ACL.
They do not pretend the four TCB mediation principals or host administrator
lack physical byte access. Infrastructure access is separately constrained by
the TCB capability rules in section 4.3 and never grants semantic role
authority.

Store admission uses exclusive creation and content authentication. Replacing,
mutating, partially writing, or duplicating an accepted object rejects. E51 and
E54 paired writes need a separately reviewed atomic-commit implementation;
this design does not claim that NTFS directory writes alone provide it.

The registrar receives only the public receipt material assigned by the
frozen split edges and never the corresponding protected payload.

### 4.5 Paired-role independence

The eight paired rows expand to distinct positions. Both positions must have
different VM IDs, writable disks, input media, output media, operator sessions,
conversation roots, and—where the frozen registry assigns signer identities—
different private keys. They may originate from the same authenticated base
export because the base contains no role state or secret.

Paired positions may run concurrently or sequentially. Sequential execution is
acceptable only if the first position's VM, output disk, logs, and human-visible
result are unavailable to the second. Scheduling order is frozen before the
first invocation and may not be selected based on its result.

Agreement is evidence only when each position independently produced its
result under these boundaries. Common operators who have inspected both input
or output sets defeat cognitive independence even if the VM controls pass.

The one `public-executor:single` topology position is a template for exactly
eight future fresh actor/external-session pairs: four conditions times two
blocks. One pair handles exactly one condition/block unit, no pair is forked
from a fixture author or another executor, no pair sees another transcript or
output, and at most three pairs run concurrently.

## 5. Trust root and signer custody

### 5.1 Exact inherited public construction

The trust root follows the v0.14 section-4 construction without extension:

- the anchor record names `control-root-authority`, one Ed25519 public key, and
  `key_id = SHA-256(exact 32 raw public-key bytes)`;
- registry v1 contains exactly the frozen 22 role entries, once each in fixed
  order, all `active`, with unique public keys and recomputed key IDs;
- the root entry equals the anchor;
- only the anchor's root key signs the exact registry record through the
  inherited signed-envelope grammar; and
- verification begins from an exact Git commit and anchor hash approved by the
  user out of band, then authenticates anchor bytes, registry bytes, role/key
  bindings, and signature in that order.

Registry order is exactly:

1. `adjudication-comparison`
2. `analysis`
3. `analysis-map-comparison`
4. `catalog-comparison`
5. `comparator-builder-1`
6. `comparator-builder-2`
7. `comparator-operator-1`
8. `comparator-operator-2`
9. `content-intake`
10. `control-registrar`
11. `control-root-authority`
12. `final-decision-custodian`
13. `judgment-comparison`
14. `label-comparison`
15. `leakage-comparison`
16. `p1-review-comparison`
17. `public-record-publisher`
18. `representation-builder`
19. `scan-comparison`
20. `semantic-judge-1`
21. `semantic-judge-2`
22. `simulation-builder`

The approved commit pin cannot authenticate itself from bytes inside that same
commit. The implementation must require the exact commit SHA and anchor hash as
external CONTROL inputs. The commit contains the anchor, its sidecar, exact
registry envelope, and an integration record naming the artifact hashes; the
user's separate approval designates that commit as the root pin.

The external activation record is a separately trusted CONTROL input. For this
SHA-1 Git repository its exact ASCII/LF form is:

```text
activation_schema=URC-0.14-ROOT-ACTIVATION-1
repository_url=https://github.com/shotgun1107/human-ai-development-tradition
campaign_id=<64 lowercase hex>
git_object_format=sha1
git_commit_hex=<40 lowercase hex>
anchor_record_sha256=<64 lowercase hex>
registry_version=1
registry_envelope_sha256=<64 lowercase hex>
proof_transcript_sha256=<64 lowercase hex>
approval_state=approved
```

There is one final LF and no extra field. CONTROL generates the public 32-byte
campaign ID before the ceremony. The user approves and supplies the complete
record out of band; it is not discovered from the repository it authenticates.
A branch, tag, abbreviated object ID, `HEAD`, timestamp, adjacent sidecar, or
automatic “latest” discovery cannot substitute for any field.

Registry v1 has no mutation, rotation, revocation, expiry, or status transition.
Any key loss, suspected disclosure, changed key, duplicate assignment, root
change, or registry change stops S0 and requires a new registry version, fresh
independent review, and a newly user-approved root commit. A timestamp alone
cannot authorize a newer registry or prevent rollback.

### 5.2 Key generation and custody requirements

Actual key generation remains closed. A later implementation must satisfy:

- use an independently reviewed Ed25519 implementation and pass the applicable
  RFC 8032 test vectors before generating role keys;
- generate all private keys inside their final isolated custody environment;
- never print, log, place on a command line, commit, copy to input/output media,
  or expose a private key to another role;
- bind each of the 22 unique public keys to exactly one frozen signer role and
  verify possession before registry assembly;
- keep the root environment offline, without a virtual NIC, repository, role
  vault, bank, labels, oracle, model output, or experimental edge;
- permit the root key to sign only the exact registry candidate approved for
  the ceremony;
- make role signing interfaces accept only the exact role's canonical preimage
  domain and reject arbitrary bytes or another role ID; and
- record public ceremony evidence and verification results without recording
  secret material.

Each of the 21 non-root section-4 signer IDs has one dedicated
campaign-lifetime signer-custody appliance. The root has its separate offline
environment. A signer appliance is never cloned or shared, contains no role
vault, and receives no arbitrary interpreter or actor credential. It accepts a
canonical signing request only when campaign ID, registry digest, signer ID,
edge/artifact kind, signature domain, request ID, preimage bytes/hash, and
caller capability all match its frozen allowlist. It returns only the exact
signature result. Wrong-domain, wrong-role, duplicate, reordered, or replayed
requests reject. Request payloads are removed after signing; only bounded
request IDs, hashes, decisions, and anti-replay state persist with the key.

The actor VM never receives the private key. The appliance is the stable key
boundary that permits an authorized role identity such as the registrar to
sign at multiple phases while actor invocations remain disposable. Appliance
provisioning, storage, reboot persistence, retirement, and destruction have a
separate campaign state machine from section 6's actor invocation lifecycle.

For each request, the powered-off appliance receives one finalized read-only
request ISO and one new raw signature-output disk. Its persistent encrypted
disk contains only the non-exportable key, frozen service, configuration, and
bounded anti-replay state. On boot, the frozen service validates the request,
signs once if authorized, writes a fixed raw result frame containing request
ID, signer ID, preimage SHA-256, exact 64-byte signature, and result-frame
SHA-256, seals the output, and shuts down. CONTROL generates each request ID as
32 random bytes, rendered as 64 lowercase hex outside binary frames. The exact
successful result frame is ASCII magic `S0-SIGNATURE-RESULT-1\n`, 32 raw
request-ID bytes, unsigned 16-bit big-endian signer-ID length, permitted ASCII
signer-ID bytes, 32 raw preimage-hash bytes, 64 raw signature bytes, then 32 raw
SHA-256 bytes over every preceding frame byte. Remaining disk capacity is zero.
The host reads that result as a raw device without a filesystem.
Request/result media are TCB temporary replicas and follow the section-4.1
retention/destruction rule; they are not experimental edges or stores.

Paging, hibernation, crash-dump capture, command-line preimages, request-body
logging, and persistent request payloads are disabled. The persistent appliance
may retain only request IDs, preimage hashes, decisions, and anti-replay state.
An implementation that cannot demonstrate this separation may not generate a
key.

The concrete non-exportable Ed25519 provider is marked
`signer-custody-provider-unresolved`. Provider/API choice, attacker model,
memory/dump/export behavior, reboot persistence, role authentication, and
domain-restricted signing must pass a separate design decision and independent
implementation review before key generation.

The implementation must decide and independently review the concrete
non-exportable key provider, encrypted-at-rest mechanism, backup policy, and
operator authentication before generation. A vTPM or encrypted VHDX alone is
not accepted as proof that a key is non-exportable. If the selected Ed25519
provider cannot meet the custody test, the phase stops rather than exporting
software key files as a workaround.

The 22-entry registry governs only the inherited section-4 generic-envelope
scope. Other predecessor artifacts described as signed retain their inherited
signature specifications. The accepted public inputs do not yet provide a
total replacement preimage/key mechanism for all of those artifacts. This
candidate marks that separate scope `inherited-signature-unresolved`; it does
not add registry entries, declare those artifacts unsigned, or authorize their
implementation. That scope must be resolved and independently reviewed before
an execution package can freeze.

### 5.3 Pre-activation proof of possession

Before registry assembly, each of the 21 non-root signer appliances must prove
possession of its proposed private key. The root key does not sign a separate
proof: its one allowed registry-v1 signature is its possession evidence. None
of these signatures makes the root trusted; external activation does that.

The registrar first generates a public 32-byte ceremony ID and freezes a
commitment manifest containing the ceremony ID,
campaign ID, registry version, exact 22 role/public-key/key-ID proposals, and
their order. After that freeze, an approved cryptographic random generator
issues one independently generated 32-byte nonce to each non-root signer. A
nonce is used once. Each non-root role signs these exact ASCII/LF bytes with
plain Ed25519:

```text
URC-0.14-KEY-POSSESSION-PROOF-1
registry_version=1
ceremony_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
role_id=<exact frozen signer role ID>
registrar_role=control-registrar
public_key_hex=<64 lowercase hex>
key_id=<64 lowercase hex: SHA-256 of exact 32 raw public-key bytes>
nonce_hex=<64 lowercase hex>
```

There is one final LF, no BOM, no CR, and no extra field. The detached
signature is exactly 64 bytes, encoded as 128 lowercase hex characters in the
public ceremony transcript. A proof rejects if the role, key, key ID, nonce,
bytes, signature, or verifier result differs, or if a nonce repeats. All 21
proofs must verify, the registry entries must remain byte-identical to the
frozen commitments, and the proof transcript hash must freeze before the root
signs the registry candidate. That transcript hash is bound by the later
integration and external activation records.

Proof of possession demonstrates control of a private key for that public key;
it does not establish the person's identity, authorize the role, make the root
trusted, or prove key non-exportability. CONTROL supplies the role binding, and
the user's external anchor/commit pin supplies root trust. No wall-clock claim
is made; only the frozen order—commitments, challenges, proofs, registry
signature, user activation—is asserted. Verification rejects noncanonical
Ed25519 point encodings, invalid point decoding, signatures with `S` outside
the RFC 8032 range, wrong length, or use of Ed25519ctx, Ed25519ph, or an
application-defined prehash in place of plain Ed25519.

### 5.4 Root and role failure handling

The root VM is single-purpose and is never cloned after key generation. Its
private state is not used as an ordinary role base. Root-key loss before
activation discards the candidate. Loss after activation without evidence of
compromise leaves the already approved public registry and existing signatures
verifiable but prevents successor signing. Suspected compromise invalidates
the campaign and all signatures whose acceptance depends on that registry.
Recovery is a new, separately gated trust-root version on untouched
experimental material, not an in-place edit or majority vote among existing
role keys.

A role-key failure before protected work starts requires a new reviewed
registry version. A role-key failure after protected work starts invalidates
the affected bank/package/run according to the inherited stop rules. Existing
signed evidence remains historical evidence, not authority for a resumed run.

A non-root signer appliance follows the separate campaign order `proposed`,
`provisioned`, `key-generated`, `proof-verified`, `registry-bound`, `active`,
then exactly one of `retired`, `lost`, or `compromised`. It cannot sign ordinary
artifacts before `active`; `lost` and `compromised` are terminal. The root
environment follows `proposed`, `provisioned`, `key-generated`,
`registry-signed`, `externally-activated`, then the same terminal states. Actor
invocation states never advance or reset these signer states.

The default for this single synthetic campaign is no operational backup of
role private keys: loss causes re-bootstrap. Suspected root compromise
invalidates the campaign because a signature or timestamp cannot distinguish
pre-compromise from post-compromise use. A root recovery copy or dual-control
scheme would require its own exact design, review, and implementation gate.

## 6. Invocation state machine

The only accepted state order is:

1. `declared` — role position, invocation ID, frozen base, edges, stores, and
   expected outputs are fixed;
2. `provisioned` — a new VM ID, disk identities, and measured configuration
   exist;
3. `input-frozen` — the exact read-only input image and empty output medium are
   authenticated;
4. `preflight-passed` — all channel, credential, device, process, and canary
   tests pass;
5. `running` — the VM is booted once under the frozen profile;
6. `output-sealed` — the role stops, the VM powers off, and media hashes freeze;
7. `ingested` — complete output passes route and artifact validation exactly
   once; and
8. `quarantined` — the VM and writable media cannot be resumed or reassigned.

Every transition binds the invocation ID, a unique invocation nonce, and a
strictly increasing event sequence. Host and guest wall-clock values are
diagnostic only; equality between them is not required and no security order
depends on filesystem time, Git time, or a trusted wall clock.

Skipping, repeating, reversing, or repairing a state rejects. A failed
invocation transitions directly to `failed-quarantined`; its outputs are not
inputs to a retry. A new attempt requires the later gate and untouched material
required by the governing S0 stop rule.

## 7. Evidence that must be frozen

Before any protected S0 input is created, the implementation and its
independent review must freeze:

- host edition/build, firmware virtualization status, Hyper-V feature state,
  patch identity, and administrator/TCB declaration;
- base export complete-file-set manifest and hash;
- normative VM configuration schema and exact allowed device/service list;
- frozen bootstrap service, executable/process/token/privilege allowlists, and
  instance-identity creation rules;
- the 40-position deployment map and 22-signer assignment;
- all 27 store ACLs and all 64 route decisions;
- input ISO, hostile-output ingestion, trusted staging, output VHDX, temporary-
  replica retention/destruction, and complete-file-set rules;
- key-ceremony, anchor, registry, signature-verification, and external-pin
  procedures;
- signer-appliance provider, domain policy, state machine, and anti-replay
  behavior;
- launch, transfer, ingest, audit, quarantine, and failure state grammars;
- independent negative-test fixtures containing only synthetic canaries; and
- resource ceilings for disk, RAM, CPU, elapsed time, and concurrent VMs.

No actual role key, bank, label, oracle, protected package, executor, or model
credential is permitted in those public evidence files.

## 8. Rejection and stop conditions

The phase rejects on any unmeasured base/configuration byte, reused VM or disk,
attached NIC, enabled convenience channel, unauthorized device, missing log,
unlisted or hostile filesystem object, wrong route, stale root pin, registry or
commitment mismatch, signature or PoP mismatch, signer replay/domain escape,
duplicate object, partial invocation or pair, unauthorized reader, private-key
appearance, role canary crossing, prior-run residue, unresolved signer provider
or external-session profile, or inability to prove the negative tests in the
companion acceptance plan.

An ordinary implementation defect discovered before protected material exists
may be corrected only under the later implementation gate and reviewed again.
Once a bank, label, oracle, execution package, or run exists, the inherited
untouched-material stop rules control; this design does not authorize repair in
place.

## 9. Closed gates and claim limit

This candidate does not authorize or claim:

- VM, account, ACL, vault, airlock, or network implementation;
- actual Ed25519 keys, anchor, registry, signature, or root commit;
- cryptographic security against the host administrator;
- bank, prompt, label, oracle, fixture, projection, package, or comparator work;
- executor sessions, provider access, model calls, retries, judgments, scoring,
  statistics, or S0 conclusions;
- E0 work, sealed-material access, central-system implementation, Project Brain
  integration, operational safety, economic value, or model-to-model transfer.

A future independent design pass supports only CONTROL integration
consideration. Actual provisioning requires a separate exact implementation
gate.

The only natural next gate from this candidate is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`

## 10. Primary references

- Microsoft, [Windows security servicing criteria and security boundaries](https://www.microsoft.com/en-us/msrc/windows-security-servicing-criteria)
- Microsoft, [Hyper-V overview](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/overview)
- Microsoft, [Hyper-V host hardware requirements](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements)
- Microsoft, [Hyper-V networking planning](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-networking-in-windows-server)
- Microsoft, [Hyper-V enhanced session mode](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/enhanced-session-mode)
- Microsoft, [Manage Hyper-V integration services](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-integration-services)
- Microsoft, [PowerShell Direct](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/powershell-direct)
- Microsoft, [Export and import virtual machines](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/export-and-import-virtual-machines)
- Microsoft, [Windows Sandbox](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/)
- RFC Editor, [RFC 8032: Edwards-Curve Digital Signature Algorithm](https://www.rfc-editor.org/rfc/rfc8032)
- NIST, [Key-management project and lifecycle overview](https://csrc.nist.gov/Projects/Key-Management/faqs)
- NIST, [FIPS 186-5: Digital Signature Standard](https://csrc.nist.gov/pubs/fips/186-5/final)
- NIST, [SP 800-57 Part 1 Rev. 5: Key-management guidance](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- NIST, [SP 800-89: Assurance of key possession](https://csrc.nist.gov/pubs/sp/800/89/final)
- NIST, [SP 800-133 Rev. 2: Cryptographic key generation](https://csrc.nist.gov/pubs/sp/800/133/r2/final)
