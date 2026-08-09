# S0 v0.14 role-isolation acceptance-plan addendum v0.2

- `status`: design revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `predecessor_plan_sha256`: `71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937`
- `claim_kind`: public tabletop acceptance design only

## 1. Effective plan

This addendum composes with the authenticated v0.1 acceptance plan. It executes
no test and contains no key, VM, canary, fixture, protected input, provider
session, or model output.

The v0.1 plan's 92 rows remain effective except for the exact replacements in
section 2. Sections 3 through 6 add 15 rows, producing 107 effective rows:

- platform: ISO-P01 through ISO-P19, 19 rows;
- channels: ISO-C01 through ISO-C14, 14 rows;
- media/routes: ISO-R01 through ISO-R22, 22 rows;
- independence: ISO-I01 through ISO-I08, eight rows;
- trust/signer: ISO-K01 through ISO-K34, 34 rows; and
- lifecycle: ISO-L01 through ISO-L10, ten rows.

Every row is noncompensatory. A skip, waiver, unbounded operator judgment,
provider-default acceptance set, or test-result substitution is a failure.

## 2. Exact v0.1 replacements

### 2.1 Required evidence

The v0.1 section 2 common evidence field `invocation nonce` is deleted. Actor
evidence binds one exact `invocation_id`, its project-lifetime ledger
reservation event, descriptor hash, launch-admission hash, and ordered state
events. No second nonce field is permitted.

Signer evidence is signing-route specific:

- `preactivation-pop-v1`: appliance ID, campaign, ceremony, signer, public key,
  key ID, complete context-import file hashes, commitment/challenge hashes,
  request ID, challenge, context/request capabilities, import/request admission
  hashes/event IDs, request/preimage/result-media hashes, strict-profile result,
  and state;
- `active-section4-v1`: appliance ID, campaign, activated registry-envelope
  digest, signer, exact edge/phase/artifact/domain, registry-binding and
  activation package/admission hashes, request ID, caller capability, request-
  admission hash/event ID, request-ISO/preimage/result-media hashes, strict-
  profile result, and state; and
- `root-registry-v1`: offline root ID, campaign, ceremony, anchor/commitment/
  challenge/transcript/registry hashes, exact seven-file request-ISO hash,
  request and capability IDs, root-ceremony-admission hash/event ID, preimage/
  result-media hashes, strict-profile result, and
  `key-generated -> registry-signed` state.

Fields from one request/import/ceremony class in another are a failure, not
optional metadata.

### 2.2 Replaced platform/channel/route/lifecycle rows

| Existing ID | Effective v0.2 mutation or observation | Required result |
|---|---|---|
| ISO-P14 | Startup path lacks the exact frozen service/policy or accepts an absent, noncanonical, circular, after-freeze, or unbound `S0-INVOCATION-DESCRIPTOR-2`/launch-admission pair | Reject before protected input attachment |
| ISO-P15 | Invocation ID is absent from the project-lifetime ledger/witness chain, duplicated across any campaign, rebound to another VM/role, deleted after failure, or accepted after ledger/witness rollback or unavailability | Reject before import/boot and invalidate the candidate on rollback |
| ISO-C10 | Host and guest evidence disagree on campaign, invocation ID, descriptor hash, VM ID, process set, or ordered event sequence; wall clocks alone differ | Reject on identity/hash/order/process mismatch; clock difference alone is diagnostic |
| ISO-R07 | Change descriptor, admission, content-manifest, route-manifest, source store, edge, recipient, role, VM, media, policy, phase, hash, or authenticated envelope while retaining another declared identifier | Reject the whole invocation |
| ISO-L10 | Execution package freezes while `external-provider-isolation-unresolved`, `signer-custody-provider-unresolved`, `inherited-signature-unresolved`, or `launch-ledger-provider-unresolved` remains | Reject |

### 2.3 Replaced signer rows

| Existing ID | Effective v0.2 mutation or observation | Required result |
|---|---|---|
| ISO-K01 | Applicable RFC 8032 valid vector also passes `S0-ED25519-STRICT-1` key, point, scalar, and uncofactored-equation checks | Exact Boolean `True` |
| ISO-K02 | Alter message, public key, signature byte, length, algorithm/profile label, or subgroup result | Exact Boolean `False`/reject |
| ISO-K10 | Request/import/ceremony parser sees arbitrary bytes, wrong role/domain/class/state/capability, cross-class field, extra package object, or record outside the exact allowlist | Reject without signature or state advancement |
| ISO-K11 | Any of 21 non-root keys fails strict validity or its one pre-activation PoP; root fails strict validity or exact registry signature | Reject registry candidate |
| ISO-K15 | Root signature occurs outside the exact `root-registry-v1` package/state, or before strict validation of 22 keys, 21 unique challenges/proofs, commitment equality, and transcript freeze | Reject registry candidate |
| ISO-K16 | PoP request/preimage/commitment/challenge/capability/state changes, repeats, crosses signer, or contains active-class fields | Reject proof, appliance transition, and registry candidate |
| ISO-K19 | `A` or `R` is noncanonical, identity, small-order, or mixed-order; `[L]P != I`; `S >= L`; uncofactored equation fails; result is non-Boolean; or variant/prehash differs | Reject before signature acceptance |
| ISO-K20 | Pre-activation request includes registry/edge/active fields, active request lacks exact activated registry/edge/artifact fields, root ceremony depends on an activated registry, any route crosses class/state, signer-media ledger/witness is restored, or request/capability replays or crashes at `pending` | Reject without signature; only exact owner/class/state signing routes may sign; invalidate on ledger/witness failure |
| ISO-K24 | Signature-bearing object belongs to zero or multiple scopes among `preactivation-pop-v1`, `section4-generic-envelope-v1`, and `inherited-signature-unresolved`; or request/ceremony class is treated as signature scope | Reject inventory |
| ISO-K25 | Any non-root/root route uses non-finalized/shared/network/PowerShell-Direct media, a wrong file set, hot attachment, simultaneous/stale/prior exchange media, reused result medium, missing shutdown/detachment/destruction gate, writable request media, persistent request body, filesystem result disk, command-line preimage, pagefile, hibernation, crash dump, or payload log | Reject appliance configuration/transition |

## 3. Added platform and channel rows

| ID | Mutation or observation | Required result |
|---|---|---|
| ISO-P16 | Descriptor or launch-admission record has wrong schema/order/encoding/final LF, extra/missing field, unknown role, wrong UUID/hex/decimal form, or an internally circular descriptor/ISO digest | Reject before ISO attachment |
| ISO-P17 | Host admission authority/configuration/capability, descriptor, exact ISO object handle/identity, ISO bytes, content manifest, route manifest, executable policy, blank output medium, base, configuration, reservation/bound/admission event, or boot authorization differs by one byte/value; route controller attempts approval; or a path is resolved again after hashing | Reject before boot |
| ISO-P18 | CSPRNG emits an invocation/event/object/boot ID already used, concurrent reserve races, any ceremony/signer-media/invocation ledger or independent witness is unavailable, a ledger is restored behind its witness, witness/head differs, or consumed capability/boot authorization is reused | Reject the frozen attempt without redraw; preserve the original ledger/witness entry; exactly one concurrent reservation may succeed |
| ISO-P19 | Guest derivation uses a separate nonce, wrong HKDF-SHA-256 salt/info/length, omits campaign/invocation/role/VM context, uses pre-machine-identity randomness, retains random/secret bytes, or equal forced guest randomness plus distinct IDs yields equal secrets | Reject before protected input; candidate fails on retention/context/reuse |
| ISO-C13 | Any record, process, CLI, API, or log adds a separately generated `invocation_nonce` or binds an external uniqueness value different from raw `invocation_id` | Reject configuration/invocation |
| ISO-C14 | Guest launches with descriptor bytes/hash or invocation ID different from host admission, or post-run evidence omits either value | Reject output with zero store change |

## 4. Added media/route row

| ID | Mutation or observation | Required result |
|---|---|---|
| ISO-R22 | A signature, arbitrary operator file, branch/tag/latest value, ambient directory, or unlisted principal is treated as descriptor authority instead of exact TCB admission/hash binding | Reject authority source and invocation |

## 5. Added strict-key and bootstrap rows

These remain future implementation tests. The design reviewer traces them on
paper only.

| ID | Mutation or observation | Required result |
|---|---|---|
| ISO-K27 | `Aenc = identity32` where `identity32 = 0x01 || 31 * 0x00`; or signature is `Renc = identity32`, `Senc = 32 * 0x00` | Reject public key/signature before PoP or artifact acceptance |
| ISO-K28 | Canonical decoded `A` or `R` satisfies `[L]P != I`, including nonidentity small-order or mixed-order point | Reject even if a provider's ordinary verify call succeeds |
| ISO-K29 | Signature satisfies only RFC 8032's cofactored equation but not `[S]B = R + [k]A` | Reject |
| ISO-K30 | Anchor, registry entry, PoP, root registry signature, or active artifact bypasses strict validation, uses another profile/cache/registry result, or accepts truthy non-Boolean output | Reject the applicable anchor, registry, proof, or artifact |
| ISO-K31 | Preactivation context ISO lacks its exact three files, PoP ISO lacks exactly `request.txt`/`preimage.bin`, either has wrong manifest/capability/key/object/admission binding, or PoP bytes do not reconstruct the republished grammar | Reject without signature or state advancement except a logged failed decision |
| ISO-K32 | Context import is accepted outside `key-generated`, PoP outside `pop-context-bound`, a second proof is issued, active request is accepted before `active`, root ceremony is accepted outside root `key-generated`, root accepts PoP, or a second root signature is attempted | Reject route and candidate state transition |
| ISO-K33 | Transcript order/count/hash, registry commitment equality, strict proof result, root seven-file package/signature order, six-file registry-binding package, two-file activation package, import admission, or appliance entry differs; inert candidate validation is treated as active authority, or activation is demanded before candidate validation | Reject registry-signed/registry-bound/active transition or premature authority use |
| ISO-K34 | PoP signature authorizes an ordinary artifact, unsigned transcript is described as signed, TCB descriptor enters a signature scope, or inherited unresolved artifact is assigned an active registry signer | Reject scope inventory and package freeze |

## 6. Tabletop trace required of the next reviewer

The next fresh reviewer must independently construct at least these five
counterexamples and trace a unique rejection:

1. the identity-key/identity-`R`/zero-`S` construction from `TRI-B01`;
2. a context import at `key-generated`, a PoP request at `pop-context-bound`
   without a registry digest, then cross-class injection and proof reuse;
3. an arbitrary or after-freeze descriptor substituted while every payload
   file remains unchanged;
4. a root ceremony that circularly demands its own activated envelope, a package
   missing one required file, and a second root-signature attempt; and
5. two distinct VM IDs whose records try to share a second nonce, one duplicate
   invocation ID, and restoration of an older valid ledger behind the monotonic
   witness.

The reviewer must also independently verify that the replacements do not alter
32/40/8/22, 27/46/64, split-edge, E49, executor-count, provider-blocker, or
closed-gate invariants.

## 7. Acceptance rule

The effective candidate passes implementation review only when all 107 rows
return their exact outcomes on one frozen implementation/configuration and a
fresh reviewer reports zero findings. This design-stage document cannot supply
that evidence.

Passing a later implementation review would support only CONTROL consideration
of the public isolation implementation. It would not open key generation,
protected material, provider sessions, model execution, judge handoff, scoring,
or S0 execution.
