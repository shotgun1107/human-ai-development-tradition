# S0 v0.14 identity and authority matrix addendum v0.2

- `status`: design revision candidate
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `predecessor_matrix_sha256`: `ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0`
- `claim_kind`: public identity, authority, and scope design only

## 1. Count preservation

The authenticated v0.1 row-position-signer table remains byte-authoritative for
all 40 role positions. This addendum creates no role row, position, signer,
store, reader, or experimental edge.

| Inventory | Effective count |
|---|---:|
| aggregated role rows | 32 |
| role positions | 40 |
| paired rows | 8 |
| experimental section-4 signer bindings | 21 |
| positions with signer `none` | 19 |
| non-row root signer | 1 |
| registry IDs | 22 |
| experimental stores | 27 |
| explicit reader entries | 46 |
| experimental edge rows | 64 |

The public ceremony coordinator, invocation-ID ledger, launch-admission record,
input route controller, signer media, and descriptor are TCB controls. They are
not experimental identities or topology objects.

## 2. Effective authority classes

| Object or action | Producing authority | Verification authority | Signature scope | Experimental topology effect |
|---|---|---|---|---|
| root anchor key | externally pinned CONTROL root input | strict verifier before anchor admission | none; public key input | none |
| registry v1 envelope | non-row `control-root-authority` through one `root-registry-v1` ceremony | strict verifier from external root pin | `section4-generic-envelope-v1` | existing 22 IDs only |
| PoP commitment manifest | CONTROL ceremony coordinator | strict public ceremony verifier | none | none |
| PoP challenge manifest | CONTROL ceremony coordinator | strict public ceremony verifier | none | none |
| preactivation-context import | CONTROL ceremony coordinator plus one-use host attachment capability | exact signer appliance at `key-generated` | unsigned state-binding input | none |
| non-root PoP request | one-use host attachment capability for exact signer | signer appliance at `pop-context-bound` | request is unsigned | none |
| non-root PoP signature | exact non-root signer appliance at `pop-context-bound` | `S0-ED25519-STRICT-1` verifier | `preactivation-pop-v1` | none |
| PoP transcript | CONTROL deterministic assembly of 21 verified proofs | root ceremony and external activation verifiers | container unsigned; embedded proofs retain bootstrap scope | none |
| offline-root registry ceremony | CONTROL root ceremony plus one-use host attachment capability | exact offline root parser at `key-generated` | ceremony record is unsigned | none |
| root registry signature | exact non-row offline root environment at `key-generated` | strict verifier from external root pin | `section4-generic-envelope-v1` | none |
| registry-binding import | externally pinned CONTROL configuration import | exact signer appliance | unsigned state-binding input | none |
| activation-binding import | externally pinned CONTROL configuration import of the exact user-approved activation record | exact registry-bound signer appliance | unsigned state-binding input | none |
| ordinary section-4 signature | exact active signer appliance | strict registry-bound verifier | `section4-generic-envelope-v1` | existing edge/artifact only |
| inherited predecessor signature | unresolved predecessor authority | unresolved | `inherited-signature-unresolved` | implementation forbidden |
| invocation descriptor | input route controller from frozen declaration | host preflight, guest parser, post-run admission | deliberately unsigned | none |
| launch-admission record | CONTROL host preflight under pinned TCB configuration | host/post-run admission | deliberately unsigned | none |
| signer import-admission record | CONTROL host preflight | target environment plus signer-media ledger/witness | deliberately unsigned | none |
| non-root signing-request-admission record | CONTROL host preflight | exact non-root signer environment plus signer-media ledger/witness | deliberately unsigned | none |
| offline-root ceremony-admission record | CONTROL host preflight | exact offline root environment plus signer-media ledger/witness | deliberately unsigned | none |
| invocation-ID reservation and events | project-lifetime atomic TCB ledger provider | provisioning/preflight/admission plus monotonic witness | none | none |
| launch-ledger monotonic witness | independently persisted rollback domain | every ledger consumer | none | none |
| public ceremony-ledger namespace | same unresolved atomic witness-backed provider | ceremony coordinator and reviewer | none | none |
| signer-media admission-ledger namespace | same unresolved atomic witness-backed provider | host preflight and target anti-replay check | none | none |
| `preflight_capability_id` | CONTROL CNG under pinned host-preflight configuration | launch admission and invocation ledger | none | none |

No unsigned TCB object may be represented as cryptographic proof against the
host administrator. No ceremony object may be used to authorize an
experimental data transfer.
The admission records, three ledger namespaces, witness, and preflight
capability are TCB controls only. None is an experimental role, signer, store,
reader, or edge, and none changes the frozen counts.

## 3. Signer state/route matrix

| Signer kind and state | Context import | `preactivation-pop-v1` | Root ceremony (`root-registry-v1`) | `active-section4-v1` | Registry-binding import | Activation-binding import | Other input |
|---|---|---|---|---|---|---|---|
| non-root `key-generated` | exact own context allowed once | reject | reject | reject | reject | reject | reject |
| non-root `pop-context-bound` | reject replay/mutation | exactly one own-key request allowed | reject | reject | reject | reject | reject |
| non-root `pop-issued` | reject | reject | reject | reject | exact matching root-signed registry import allowed once | reject | reject |
| non-root `registry-bound` | reject | reject | reject | reject | reject replay/mutation | exact matching user-approved activation import allowed once | reject |
| non-root `active` | reject | reject | reject | exact owner/domain/edge/artifact request allowed | reject | reject replay/mutation | reject |
| non-root terminal | reject | reject | reject | reject | reject | reject | reject |
| root `key-generated` | not applicable | reject | exact registry candidate allowed once | reject | not applicable | not applicable | reject |
| root `registry-signed` | not applicable | reject | reject second ceremony/signature | reject | not applicable | not applicable | no input; external CONTROL activation changes only the public candidate state |
| root terminal | not applicable | reject | reject | reject | not applicable | not applicable | reject |

`registry-bound` is reached only after the appliance verifies the exact root-
signed registry package against the external root/commit and anchor pins. The
transition from `registry-bound` to `active` requires a separate exact user-
approved activation import and is one-way. It binds campaign, registry digest,
signer entry, transcript, and activation-record hash. A signing request cannot
cause either transition.

The public ceremony label `proof-verified` and public root-candidate label
`externally-activated` are CONTROL evidence states, not signer-appliance states.
Non-root request class, root ceremony class, and signature scope are separate:
the root ceremony and active non-root request both produce only
`section4-generic-envelope-v1` signatures under their disjoint schemas and
states.

## 4. Strict-validation matrix

| Boundary | Public key check | Signature point/scalar check | Equation | Failure effect |
|---|---|---|---|---|
| root anchor | canonical, nonidentity, exact order `L` | not applicable | not applicable | reject root candidate |
| 22 commitment/registry entries | canonical, nonidentity, exact order `L` | not applicable | not applicable | reject commitment/registry |
| 21 PoPs | same check on committed key | canonical nonidentity order-`L` `R`, `S < L` | uncofactored only | reject proof and registry |
| root registry signature | same check on pinned root | same | uncofactored only | reject registry |
| active section-4 artifact | same check on exact registry entry | same | uncofactored only | reject artifact/state advance |
| inherited unresolved artifact | no implementation authorized | no implementation authorized | no implementation authorized | reject package freeze |

A provider that cannot expose or prove these exact checks is incompatible with
the candidate, even if its ordinary `verify` API accepts RFC-compatible
cofactored signatures.

## 5. Invocation identity matrix

| Identifier or value | Generation | Uniqueness domain | Persistence | May authorize |
|---|---|---|---|---|
| `campaign_id` | CONTROL CSPRNG, 32 bytes | project/campaign control | external activation and TCB records | campaign binding only |
| `invocation_id` | Windows CNG system-preferred RNG, 32 bytes | all project S0 invocations across campaigns | append-only invocation ledger forever | one role-position/VM invocation |
| `vm_id` | Hyper-V copy import | host VM inventory | invocation evidence | exact VM binding only |
| `output_media_id` | CONTROL CSPRNG, 32 bytes | campaign media inventory | replica evidence until terminal retention action | exact blank/output medium only |
| `request_id` | CONTROL CSPRNG, 32 bytes | signer campaign ledger | signer anti-replay ledger | one exact non-root request or root ceremony |
| PoP `challenge_nonce` | CONTROL CSPRNG, 32 bytes | all known campaign ceremonies | public transcript/challenge ledger | one PoP freshness challenge only |
| signer attachment capability | Windows CNG system-preferred RNG, 32 bytes | all project signer-media admissions | TCB admission ledger; consumed once | one exact signer/import ISO object only |
| ledger event ID | Windows CNG system-preferred RNG, 32 bytes | all project ledger events | project-lifetime ledger forever | identify one exact event; never content authority |
| `input_iso_object_id` | Windows CNG system-preferred RNG, 32 bytes at immutable-object freeze | all project launch objects | ledger and launch admission | identify one exact object handle/bytes binding only |
| `boot_authorization_id` | Windows CNG system-preferred RNG, 32 bytes after `bound` | all project boot admissions | ledger forever; consumed once | one exact admission/ISO/VM boot only |

There is no independent actor `invocation_nonce`. The PoP challenge nonce is a
different, ceremony-only object and cannot enter actor invocation-secret
derivation or lifecycle evidence.

## 6. Descriptor responsibility split

| Check | Input route controller | Host preflight | Guest startup | Post-run admission |
|---|---:|---:|---:|---:|
| construct descriptor from frozen declaration | yes | no | no | no |
| canonical descriptor grammar | yes | independently verify | independently verify | independently verify hash |
| whole ISO hash | construct/freeze | independently verify | not claimed | compare frozen value |
| content/route/policy hashes | construct | independently verify | independently verify attached bytes | compare evidence |
| VM/base/config/output-medium binding | record | independently verify against host state | retain declared values only | cross-check host/guest evidence |
| invocation ledger reservation | no write | require prior atomic reservation | observe invocation ID only | require same reservation/event |
| authorize launch | never alone | only exact approved admission record | launch only after local parsing | not applicable |

The descriptor has no signature field, signer ID, public key, signature domain,
or section-4 envelope. Adding any of them is an unauthorized authority change.
Host preflight must bind and consume the one ledger boot authorization against
the exact immutable ISO object handle it hashes and attaches; guest code is not
credited with observing host-only VM, VHDX, configuration, or object-handle
facts.

## 7. Machine-readable successor requirement

A later implementation gate must derive exact schemas and inventories for the
three signature scopes, two non-root request classes, the separate root ceremony,
three signer import packages, three media-admission records, strict validation
profile, descriptor/admission pair, invocation ledger, and monotonic witness
binding from authenticated v0.2 text.
The inventory must explicitly include `S0-POP-UNIQUE-VALUE-SET-1`,
`S0-POP-CEREMONY-LEDGER-EVENT-1`, and
`S0-SIGNER-MEDIA-LEDGER-EVENT-1`, with the ceremony, signer-media, and invocation
namespace/witness bindings.
Those files may not alter the v0.1 32/40/22, 27/46/64 inventories or silently
resolve the signer provider, inherited-signature, external-provider, key, VM,
storage, or launch-ledger-provider gates.
