# S0 v0.14 role-isolation acceptance plan v0.1

- `status`: design candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN OPEN`
- `claim_kind`: public, synthetic-canary acceptance design only

## 1. Purpose

This plan defines the tests that a later implementation must pass before any
bank, label, oracle, condition map, model credential, or executor exists. It
contains no such material and authorizes no provisioning.

Every test is noncompensatory. A single failure rejects the candidate
environment. Re-running a test is allowed during implementation development
before protected material exists, but the final candidate must be frozen and
reviewed as one exact configuration. After protected material exists, the
governing untouched-material stop rule applies.

## 2. Required test evidence

Each test record must bind:

- test ID and exact test implementation hash;
- host build and Hyper-V feature identity;
- identity-domain kind and the exact common configuration/policy hashes;
- invocation nonce, ordered event sequence, and diagnostic host/guest times;
- expected result, observed result, and exact Boolean pass/reject;
- stdout, stderr, exit status, and relevant event-log digest; and
- the identity and hash of the independent verifier.

Domain-specific identity fields are mandatory only for their domain:

- actor: base-export hash, VM ID, `role_position_id`, `invocation_id`,
  invocation nonce, VM configuration, and media hashes;
- signer: signer ID, appliance/VM ID, campaign ID, registry digest, request ID,
  signing-policy hash, and request/result-media hashes;
- root: root-environment ID, campaign ID, ceremony ID, candidate registry hash,
  activation-record hash, and media hashes; and
- TCB service: component ID, service-principal ID, implementation/configuration
  hash, exact input capability, and exact output capability.

Test logs must not place secrets or protected payload bytes on command lines or
in public logs.

## 3. Platform and configuration tests

| ID | Mutation or observation | Required result |
|---|---|---|
| ISO-P01 | Required firmware virtualization, SLAT, DEP, Hyper-V, host edition, RAM, and storage preflight | Exact frozen prerequisites pass; unknown is reject |
| ISO-P02 | Base export or any enumerated file changed by one byte | Reject before import |
| ISO-P03 | Import without a new VM ID or reuse prior writable disk | Reject before boot |
| ISO-P04 | Generation 1 VM, Secure Boot off, unexpected device, checkpoint, saved state, or non-frozen configuration | Reject before boot |
| ISO-P05 | Attach External, Internal, Private, Default, NAT, or any other virtual switch | Reject before boot |
| ISO-P06 | Attach a virtual NIC with no switch | Reject before boot |
| ISO-P07 | Enable Enhanced Session or any clipboard, drive, USB, printer, smart-card, microphone, camera, or audio redirection | Reject before boot |
| ISO-P08 | Enable data exchange/KVP, time sync, backup, Guest Service Interface, guest file copy, custom Hyper-V socket, or any integration service other than exact heartbeat/shutdown allowlist | Reject before boot |
| ISO-P09 | Make PowerShell Direct usable during the measured role interval | Reject before role execution |
| ISO-P10 | Add a mapped host folder, physical disk, pass-through device, or unlisted ISO/VHDX | Reject before boot |
| ISO-P11 | Open VMConnect, RDP, console, keyboard/mouse, or another interactive operator session during the measured interval | Reject invocation |
| ISO-P12 | Connect virtual COM1/COM2 to a host named pipe | Reject before boot |
| ISO-P13 | Base contains a role assignment, cached credential, certificate/private key, browser/profile, token, Git material, prior output, project/application DRBG state, generated project secret, or signer material; or two clones reuse machine identity/invocation secret | Reject base image |
| ISO-P14 | Startup path is not the exact frozen bootstrap service, executable, restricted principal, process tree, token, privilege, and resource policy | Reject before protected input attachment |
| ISO-P15 | Existing invocation ID is bound to a new VM or reused for the same or a different role position | Reject before import/boot |

## 4. Runtime channel tests

Use unique public random canaries, never real protected data.

| ID | Attempt | Required result |
|---|---|---|
| ISO-C01 | Resolve DNS and reach host, gateway, LAN peer, public fixed IP, SMB, HTTP, or HTTPS | Every attempt fails; no packets leave an attached role interface because none exists |
| ISO-C02 | `git ls-remote`, Git credential discovery, SSH agent use, or repository remote discovery | Fails; no credential, agent, remote, or `.git` metadata exists |
| ISO-C03 | Guest reads host path, `\\tsclient`, redirected drive, clipboard, or host environment variable | Fails |
| ISO-C04 | Host sends clipboard/file canary to guest and guest sends one to host | Both directions fail |
| ISO-C05 | Role A input/output/key canary searched from role B VM | No occurrence or accessible namespace |
| ISO-C06 | Prior invocation canary searched from a fresh VM of the same role | No occurrence |
| ISO-C07 | Unlisted process, child-process escape, or executable not in the approved image policy | Blocked and logged |
| ISO-C08 | Exceed CPU, memory, process, output-byte, file-count, or elapsed-time ceiling | Invocation terminates and output is rejected |
| ISO-C09 | Put a secret-shaped canary on a command line | Test design rejects; command is never launched |
| ISO-C10 | Guest and host audit streams disagree on invocation ID/nonce, ordered event sequence, VM ID, process set, or shutdown; wall-clock values alone differ | Reject on bound identity/order/process mismatch; wall-clock difference alone is diagnostic |
| ISO-C11 | Transfer a canary through KVP/Data Exchange in either direction | Both directions fail |
| ISO-C12 | Connect through an unapproved Hyper-V socket, `GuestCommunicationServices` endpoint, VMBus service, or COM named pipe | Fails and is logged |

## 5. Media and route tests

| ID | Mutation or attempt | Required result |
|---|---|---|
| ISO-R01 | Write to finalized input ISO | Fails |
| ISO-R02 | Input image contains an extra file, missing file, wrong byte length/hash, `.git`, credential, or artifact from an ungranted edge | Reject before attachment |
| ISO-R03 | Output medium is reused, nonempty, or attached to another VM | Reject before boot |
| ISO-R04 | Output contains an extra, missing, duplicate, renamed, malformed, or wrong-destination artifact | Reject entire invocation |
| ISO-R05 | Import output before VM power-off or while disk is still guest-writable | Reject |
| ISO-R06 | Attempt second ingest of the same invocation/object ID | Reject without changing accepted store state |
| ISO-R07 | Change source store, edge, recipient, role position, phase, hash, or signature in the route manifest | Reject |
| ISO-R08 | Registrar route includes any protected payload on E25, E27, E29, E35, E48, or E50 | Reject and quarantine |
| ISO-R09 | Unauthorized role requests store enumeration, parent-directory listing, or an unlisted object | Deny and log without revealing existence metadata |
| ISO-R10 | Crash or power loss between members of E51 or E54 pair | Neither member becomes accepted; no partial visible state |
| ISO-R11 | Existing immutable object is replaced or changed | Reject; original bytes and digest remain unchanged |
| ISO-R12 | Route-controller output differs from input bytes although its declared hash was retained | Independent rehash detects and rejects |
| ISO-R13 | Guest output uses path traversal, reserved/device name, case/Unicode collision, junction, reparse point, symlink, mount point, ADS, hardlink, sparse/compressed/encrypted/offline file, or non-regular object | Disposable ingestion rejects before host path following or store access |
| ISO-R14 | Output filesystem is malformed or triggers parser failure | Quarantine without host mount or store change |
| ISO-R15 | Last artifact of a multi-output invocation fails or crash occurs before complete commit | Accepted store change count remains zero |
| ISO-R16 | Another invocation/role requests a quarantined ISO, VHDX, writable disk, or staging replica | Deny without existence metadata and record the violation |
| ISO-R17 | E49 is delivered before E48 payload/hash, signed producer receipt, and E51 `A-0fff` status pair all authenticate and commit, or a stale/wrong pair is supplied | Reject without semantic-map release |
| ISO-R18 | TCB mediator requests parent listing, wildcard, cross-store search, discretionary object access, or recipient override | Reject and invalidate candidate |
| ISO-R19 | Protected-payload canary appears in route, ingestion, host, stdout/stderr, event, or store-service log | Reject campaign |
| ISO-R20 | Either ingestion extractor emits a malformed/different raw frame, export disk has a partition/filesystem/nonzero tail, host attempts to mount it, or independent frame parser disagrees | Reject with zero staging/store change |
| ISO-R21 | Route, ingestion, staging, and store-commit principals share a wildcard credential or one principal exercises another's capability | Reject configuration |

## 6. Paired-role independence tests

Apply to label A/B, leakage reviewers 1/2, comparator builders 1/2,
expected-catalog generators 1/2, P1 reviewers 1/2, blinded-map builders 1/2,
semantic judges 1/2, and comparator operators 1/2.

| ID | Mutation or observation | Required result |
|---|---|---|
| ISO-I01 | Same VM ID, writable disk, output disk, invocation ID, operator session, or conversation root assigned to both positions | Reject |
| ISO-I02 | First position's result becomes accessible before the second freezes its output | Reject the pair |
| ISO-I03 | Schedule/order selected after inspecting first result | Reject the pair |
| ISO-I04 | One position receives the other's key, vault, receipt, log, or nonpublic input | Reject the pair |
| ISO-I05 | Paired signer positions share one public key or key ID | Reject registry candidate |
| ISO-I06 | Two clean instances from the same base reveal a base-baked role or prior-run canary | Reject base image |
| ISO-I07 | Human/operator had access to both results before independent freeze | Independence claim rejects even if technical tests pass |
| ISO-I08 | Any two distinct role positions, paired or not, share an actor VM, process, interpreter, session, credential, writable root, or output disk | Reject |

## 7. Trust-root and signer tests

These tests use only RFC test vectors and synthetic candidate keys until a
later key-generation gate opens.

| ID | Mutation or attempt | Required result |
|---|---|---|
| ISO-K01 | RFC 8032 valid Ed25519 vector | Exact `True` |
| ISO-K02 | Alter message, public key, signature byte, signature length, or algorithm label | Exact `False`/reject |
| ISO-K03 | Uppercase hex, invalid hex, wrong key/signature length, alternate newline, BOM, CRLF, extra field, reordered field, or missing final LF | Reject before signature acceptance |
| ISO-K04 | Compute key ID over hex text, envelope, or any bytes other than exact 32 raw public-key bytes | Reject |
| ISO-K05 | Registry has not exactly 22 entries in frozen order, contains duplicate role/key/key ID, wrong root entry, or non-`active` status | Reject |
| ISO-K06 | Registry signed by non-root role, unpinned root, wrong anchor, or wrong canonical preimage | Reject |
| ISO-K07 | Registry or anchor loaded before exact external Git commit and anchor-hash pins are supplied | Reject without fallback discovery |
| ISO-K08 | Older but otherwise valid registry supplied after another version was approved | Reject because exact externally approved commit/version does not match |
| ISO-K09 | Any private-key byte appears in Git, log, command line, ISO, output VHDX, route manifest, crash dump, or another role | Reject and invoke compromise stop |
| ISO-K10 | Signer asked to sign arbitrary bytes, another role's domain, or a record outside its frozen artifact kinds | Reject without signature |
| ISO-K11 | Any of the 21 non-root role public keys cannot prove possession during the future ceremony, or the root cannot produce the exact registry signature | Reject registry candidate |
| ISO-K12 | Root environment has NIC, repository, experimental edge, bank, label, oracle, model output, or ordinary role state | Reject ceremony |
| ISO-K13 | Root or role key loss/compromise is handled by in-place v1 edit, timestamp choice, majority vote, or silent replacement | Reject; require new reviewed version and user-approved root |
| ISO-K14 | A predecessor artifact outside section-4 generic-envelope scope is silently assigned a registry-v1 signer or silently treated as unsigned | Reject; keep `inherited-signature-unresolved` until separately designed |
| ISO-K15 | Registry root signature occurs before all 21 unique non-root PoP challenges and proofs verify or before the transcript hash freezes | Reject registry candidate |
| ISO-K16 | PoP domain, version, ceremony ID, commitment hash, role, registrar, public key, key ID, or nonce changes; nonce repeats or proof is replayed for another ceremony/role/key | Reject proof and registry candidate |
| ISO-K17 | PoP is treated as proof of human identity, role authorization, root trust, non-exportability, or wall-clock freshness | Reject the claim |
| ISO-K18 | Commitment manifest and registry candidate differ in any role, key, key ID, order, campaign, or version | Reject before root signature |
| ISO-K19 | Ed25519 public key/signature has noncanonical or invalid point encoding, `S` outside the RFC 8032 range, or uses Ed25519ctx/Ed25519ph/custom prehash | Reject |
| ISO-K20 | Signing request is replayed, uses another role/domain/artifact/campaign/registry, or connects a stable key to another appliance; valid repeated phase use stays in the exact owner/domain | Reject every invalid request; exact authorized owner/domain requests alone may sign |
| ISO-K21 | Private-key export/read/dump is attempted, reboot changes the bound public key, or another role reaches the signer appliance | Reject and invoke compromise stop |
| ISO-K22 | External activation uses branch/tag/`HEAD`, abbreviated commit, auto-latest discovery, wrong repository/campaign, or missing anchor/registry/transcript digest | Reject without fallback |
| ISO-K23 | Root loss before activation, loss after activation without compromise, or suspected compromise is handled contrary to the three distinct rules | Reject; respectively discard candidate, retain verification only, or invalidate campaign |
| ISO-K24 | A signature-bearing artifact belongs to both section-4 and inherited scope or to neither scope | Reject inventory |
| ISO-K25 | Signer request uses any filesystem other than the exact finalized read-only request ISO, or signer request/result uses a shared folder, network, PowerShell Direct, persistent request payload, pagefile, hibernation, crash dump, command-line preimage, or request-body log; or result uses any filesystem | Reject appliance configuration |
| ISO-K26 | Signature raw result frame has wrong magic/request/signer/hash/signature, nonzero tail, filesystem, replayed request ID, or host mount | Reject without artifact acceptance |

## 8. Lifecycle and failure tests

| ID | Mutation or attempt | Required result |
|---|---|---|
| ISO-L01 | Skip, repeat, or reverse an invocation state | Reject |
| ISO-L02 | Resume or reassign a quarantined VM | Reject |
| ISO-L03 | Retry after role output or protected input exists | Reject under untouched-material rule |
| ISO-L04 | Continue after missing host/guest evidence, unknown configuration, failed canary, or verifier disagreement | Reject |
| ISO-L05 | Treat checkpoint, VM export, worktree, fresh chat, or hash alone as a secret boundary | Review rejects the claim |
| ISO-L06 | Claim host-admin, hypervisor-escape, physical, side-channel, cognitive, or cryptographic-erasure protection from this design | Review rejects the claim |
| ISO-L07 | Future executor count is not exactly eight for four conditions × two blocks, one actor handles two units, more than three run concurrently, or one executor is forked from another/fixture author | Reject |
| ISO-L08 | Treat a local Hyper-V boundary as proof of external provider/session memory isolation, or automate the future manual Pro judge handoff | Reject |
| ISO-L09 | Design reviewer provisions a VM, changes host settings, creates keys/canaries/scripts, or executes this implementation test plan under the design-review gate | Invalid review and stop |
| ISO-L10 | Execution package freezes while `external-provider-isolation-unresolved`, `signer-custody-provider-unresolved`, or `inherited-signature-unresolved` remains | Reject |

## 9. Acceptance rule

The implementation candidate passes only when:

1. every applicable test above returns its exact expected outcome;
2. no test is skipped, waived, compensated, or replaced by operator judgment;
3. the exact implementation, base, configuration, test code, and evidence set
   are frozen before independent review;
4. a fresh reviewer reconstructs the 32-row/40-position/22-signer/27-store/
   64-edge topology and independently repeats hostile tests; and
5. the review reports no blocking, major, or minor finding.

Passing supports only CONTROL consideration of the isolation implementation.
It does not open key generation, protected content, executor, model, scoring,
or S0-run gates.
