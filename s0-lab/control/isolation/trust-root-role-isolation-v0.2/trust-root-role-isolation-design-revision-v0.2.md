# S0 v0.14 trust-root and role-isolation design revision v0.2

- `status`: design revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `revision_baseline_commit`: `2fc328700124d6b874ddad4c82ca718a7c561d6a`
- `predecessor_design_commit`: `ccedcbc3a6a029df76d4d612b2978370558c87fb`
- `claim_kind`: public design only

## 1. Decision and effective composition

This revision addresses only the four findings in the authenticated v0.1
independent review. It creates no VM, key, anchor, registry, vault, account,
canary, fixture, provider session, model call, protected material, or S0 result.

The effective v0.2 candidate is a strict composition:

1. the four authenticated v0.1 candidate documents remain the predecessor;
2. this document replaces only the clauses named in section 1.1;
3. `identity-authority-matrix-addendum-v0.2.md` replaces and supplements only
   the matrix clauses named in section 1.1;
4. `isolation-acceptance-plan-addendum-v0.2.md` replaces the listed v0.1 test
   fields and adds exact hostile cases;
5. `review-response-v0.1.md` is explanatory evidence and adds no authority;
6. the v0.2 independent-review brief entirely replaces the v0.1 brief for the
   next review.

No unlisted v0.1 sentence changes meaning. Within a replaced clause, no v0.1
sentence survives unless this revision repeats it. A conflict between a named
replacement and v0.1 is resolved only in favor of this revision. A conflict
outside the named replacements is a defect, not implicit precedence.

### 1.1 Exact replacement map

| v0.1 source | Effective v0.2 treatment |
|---|---|
| design section 4.1 sentences beginning `CONTROL generates the invocation ID` and `A duplicate invocation ID` | replaced by section 6 of this revision |
| design section 4.1 clause beginning `an invocation secret derived` and ending `Two clones must not produce the same invocation secret` | replaced by section 6.3 of this revision |
| design section 4.1 phrase `signed invocation descriptor` | replaced by `unsigned TCB-bound invocation descriptor`; section 5 supplies its exact contract while the rest of that paragraph survives |
| design section 5.2 paragraphs beginning `Each of the 21 non-root` and `For each request` | replaced by sections 4.1 through 4.5 |
| design section 5.3 in full | replaced by sections 3 and 4 |
| design section 5.4 paragraph beginning `A non-root signer appliance follows` | replaced by section 4.4 |
| design section 6 references to a separate `invocation nonce` | replaced by section 6; the only external uniqueness value is `invocation_id` |
| matrix section 1 definition of invocation identity | supplemented and, on conflict, replaced by section 6 |
| matrix section 3 two-scope partition and signer-state table | replaced by section 4.5 and `identity-authority-matrix-addendum-v0.2.md` sections 2 through 3 |
| matrix section 7 implementation inventory | supplemented by sections 3.5, 4.5, 5.4, and 6.4 plus `identity-authority-matrix-addendum-v0.2.md` section 7 |
| acceptance-plan section 2 actor/signer evidence fields and rows named by the v0.2 addendum, including ISO-L10 | replaced by the addendum |
| v0.1 independent-review brief | replaced in full by the v0.2 brief |

### 1.2 Authenticated revision inputs

| Input | SHA-256 |
|---|---|
| v0.1 trust-root/role-isolation design | `6a062383742e90409f5dac9c443de90b93773c266525ba00f3802b60d40ff6fc` |
| v0.1 role-position matrix | `ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0` |
| v0.1 acceptance plan | `71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937` |
| v0.1 review brief | `88ca9ae00ee8a76f1f01865be7ffc106afede4a8207c86fab1bb72c9099e8d7a` |
| v0.1 independent review | `d99cf801719e2f524ca87fe3741b8a6776c4682df304d9448c245e5d3fee7404` |

The same-basename sidecars remain the authentication records. The v0.1
candidate and its `REVISE-AND-REVIEW` record remain immutable failure evidence.

### 1.3 Unchanged frozen invariants

This revision does not change:

- 32 aggregated role rows, 40 role positions, or eight paired rows;
- 21 experimental section-4 signer bindings, 19 `none` bindings, one non-row
  root, or the exact 22-entry registry order;
- 27 experimental stores, 46 explicit reader entries, or 64 edge rows;
- the six split edges, E49 ordering, E51/E54 pair requirements, or registrar
  payload exclusions;
- disposable actor VMs, campaign-lifetime signer appliances, the offline root,
  or the four stage-specific TCB mediation principals;
- exactly eight future executor invocation/session pairs with maximum
  concurrency three; or
- any closed implementation, provider, protected-material, E0, or S0 gate.

## 2. Finding dispositions

| Finding | Revision disposition |
|---|---|
| `TRI-B01` | define one strict Ed25519 public-key/signature profile and require it at every section-4 trust boundary |
| `TRI-B02` | define a pre-activation request class, state path, public ceremony media route, and third signature scope with no registry-digest dependency |
| `TRI-M01` | remove the unsupported signed-descriptor claim and replace it with an exact TCB-bound launch descriptor/admission contract |
| `TRI-M02` | eliminate the separate invocation nonce and make the one globally reserved 32-byte invocation ID the sole external uniqueness input |

Closure is a proposal until a fresh independent review reaches the allowed
zero-finding pass verdict.

## 3. `S0-ED25519-STRICT-1`

### 3.1 Scope and constants

Every Ed25519 public key or signature admitted by the section-4 system must be
validated under the exact profile `S0-ED25519-STRICT-1`. This is deliberately
stricter than accepting every signature that satisfies RFC 8032's cofactored
verification equation.

Let:

- `p = 2^255 - 19`;
- `L = 2^252 + 27742317777372353535851937790883648493`;
- `B` be the RFC 8032 Ed25519 base point; and
- `I` be the Edwards identity point `(0, 1)`.

Only plain Ed25519 with SHA-512 is permitted. Ed25519ctx, Ed25519ph, a custom
prehash, a provider-specific context, and algorithm substitution reject.

### 3.2 Strict public-key validation

For exact 32-byte public-key encoding `Aenc`, the verifier must perform these
steps in order:

1. require exact length 32;
2. decode under RFC 8032 section 5.1.3 and reject any decoding failure;
3. re-encode the decoded point and require byte equality with `Aenc`, including
   rejection of a noncanonical field encoding or negative-zero encoding;
4. reject `A = I`;
5. require `[L]A = I`; and
6. admit the key only when every prior step returned exact Boolean `True`.

Because `L` is prime, steps 4 and 5 require exact order `L`. Identity,
nonidentity small-order, and mixed-order public keys reject. A library's
ordinary signature-verification success cannot substitute for this separate
public-key-validity result.

The strict key check occurs before:

- anchor acceptance;
- commitment-manifest acceptance;
- any of the 22 registry entries is admitted;
- any PoP is evaluated;
- a signer appliance becomes registry-bound; and
- a cached verifier/key handle is used.

A cache key must bind exact public-key bytes, exact profile ID, campaign ID,
one process-local verifier-instance ID, and either the externally authenticated
anchor-record digest or the authenticated registry-envelope digest, as
applicable. The cache is destroyed when that verifier process exits. A result
from another key, profile, anchor, registry, campaign, verifier instance, or
process cannot be reused.
The verifier-instance ID is 32 fresh bytes from one successful Windows CNG
system-preferred RNG call at verifier-process startup. It is never serialized
as authority and is used only to prevent cross-process cache identity.

### 3.3 Strict signature validation

For message bytes `M`, validated `Aenc`, and exact 64-byte signature
`Renc || Senc`, the verifier must:

1. require exact signature length 64;
2. decode and re-encode `Renc` exactly as for `Aenc`;
3. reject `R = I` and require `[L]R = I`;
4. parse `Senc` as a 32-byte little-endian integer and require `0 <= S < L`;
5. compute `k = SHA-512(Renc || Aenc || M) mod L`; and
6. require the uncofactored equation `[S]B = R + [k]A` to return exact Boolean
   `True`.

The cofactored equation alone is insufficient. No fallback, alternate provider
acceptance set, truthy non-Boolean result, batch-only result, or skipped point
check is accepted.

### 3.4 Mandatory application points

The same strict profile applies to:

- the externally pinned root anchor key;
- all 22 registry public keys;
- all 21 pre-activation PoP signatures;
- the root registry signature; and
- every active section-4 generic-envelope signature.

An inherited signature remains forbidden while
`inherited-signature-unresolved` is open. This revision does not silently apply
the section-4 registry to that separate scope.

### 3.5 Required future evidence

Before key generation, the implementation must freeze exact positive and
negative vectors and independently reproduce:

- every applicable RFC 8032 valid vector;
- `identity32 = 0x01 || 31 * 0x00` as `Aenc`;
- `identity32` as `Renc` with `Senc = 32 * 0x00`;
- each canonical small-order point available to the reviewed implementation as
  `A` and as `R`;
- a canonical mixed-order point satisfying `[L]P != I`;
- a signature accepted only by a cofactored equation but not by the required
  uncofactored equation;
- noncanonical point encodings, negative zero, `S = L`, wrong lengths, and each
  forbidden Ed25519 variant; and
- the same hostile key/signature classes at anchor, registry, PoP, root
  signature, and ordinary artifact boundaries.

At minimum, the frozen hostile corpus must include these exact constructions:

- `identity32 = 0x01 || 31 * 0x00`;
- `zero32 = 32 * 0x00` and `0x00 || 30 * 0x00 || 0x80` as canonical
  nonidentity low-order encodings;
- `0xec || 30 * 0xff || 0x7f` as the canonical order-two encoding;
- all four canonical order-eight encodings obtained by encoding
  `bad_y2 = 2707385501144840649318225287225658788936804267575313519463743609750303402022`
  and `p - bad_y2`, each with both x-sign bits, as specified by RFC 9381
  section 5.4.5; and
- one canonical mixed-order point formed by adding the order-two point
  `(0, -1)` to the RFC 8032 test-vector-1 public point.

The independent implementation review must verify the construction and point
orders rather than trust a copied label.

The vector bytes, generator, implementation, and results belong to the later
implementation gate. This design executes none of them.

## 4. Noncircular pre-activation PoP ceremony

### 4.1 Non-root request classes and the separate root ceremony

There are exactly two non-root signer-appliance request classes:

| Request class | Allowed signer state | Registry digest | Allowed artifact |
|---|---|---|---|
| `preactivation-pop-v1` | `pop-context-bound` only | forbidden | one exact PoP for the appliance's own committed key |
| `active-section4-v1` | `active` only | required | the exact owner/domain/edge/artifact allowlist inherited from section 4 |

An appliance parser selects one exact schema from `request_class`; common-field
parsing followed by optional fields is forbidden. A pre-activation request that
contains a registry digest, edge ID, active artifact kind, or active caller
capability rejects. An active request that contains ceremony, commitment,
challenge, proposed-key, or PoP fields rejects. The root environment rejects
`preactivation-pop-v1` entirely.

The offline root is not a non-root signer appliance. It has one separate,
single-use ceremony class, `root-registry-v1`, accepted only by the exact root
environment in `key-generated`. It requires no activated registry digest and
may sign only the exact frozen registry-v1 generic-envelope preimage after all
21 proofs and the transcript have verified. It transitions the offline root
environment
to `registry-signed`. External activation gates acceptance and use of the
completed envelope; it does not gate creation of the root signature. Sections
4.3 and 4.4 define this route completely.

### 4.2 Commitment and challenge records

CONTROL, acting as the public ceremony coordinator within the declared host
TCB, generates one 32-byte campaign ID before the ceremony and one independent
32-byte ceremony ID. Both are rendered as 64 lowercase hexadecimal characters.

The commitment manifest is exact ASCII with LF, one final LF, no BOM, no CR,
and no extra field:

```text
commitment_schema=S0-POP-COMMITMENT-MANIFEST-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
registry_version=1
entry_count=22
entry_01_role_id=<first frozen registry role ID>
entry_01_public_key_hex=<64 lowercase hex>
entry_01_key_id=<64 lowercase hex>
...
entry_22_role_id=<last frozen registry role ID>
entry_22_public_key_hex=<64 lowercase hex>
entry_22_key_id=<64 lowercase hex>
```

The ellipsis denotes the same three literal line forms for every two-digit
index `01` through `22`; it is not a record byte. Registry order is the exact
inherited 22-ID order. Every key must already pass
`S0-ED25519-STRICT-1`, every key ID is SHA-256 of the exact 32 raw public-key
bytes, and all keys and key IDs are unique before this manifest freezes.

After that freeze, CONTROL obtains, for each of the 21 non-root entries, four
independent 32-byte values from successful Windows CNG system-preferred RNG
calls: one challenge nonce, one request ID, one preactivation-context attachment
capability ID, and one PoP-request caller-capability ID. The challenge manifest
uses the same encoding rules:

```text
challenge_schema=S0-POP-CHALLENGE-MANIFEST-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
entry_count=21
entry_01_role_id=<first non-root role in frozen registry order>
entry_01_request_id=<64 lowercase hex>
entry_01_challenge_nonce=<64 lowercase hex>
entry_01_context_capability_id=<64 lowercase hex>
entry_01_request_capability_id=<64 lowercase hex>
...
entry_21_role_id=<last non-root role in frozen registry order>
entry_21_request_id=<64 lowercase hex>
entry_21_challenge_nonce=<64 lowercase hex>
entry_21_context_capability_id=<64 lowercase hex>
entry_21_request_capability_id=<64 lowercase hex>
```

All 84 generated values are unique within the ceremony, and no value is reused
across any ceremony known to the project-lifetime ceremony ledger. A duplicate
rejects the ceremony without redraw or selective repair.
CONTROL atomically reserves the complete 84-value set in that public TCB
ceremony ledger before the challenge manifest freezes. An unavailable ledger,
partial reservation, or value already present rejects the whole candidate; the
ledger is not an experimental store and contains no private key or protected
experimental payload. It uses the same future rollback-resistant provider
profile and independent witness required by section 6.2, in a separate public
ceremony namespace, so `launch-ledger-provider-unresolved` also blocks this
reservation from implementation.

Before reservation, CONTROL serializes the 84 values in exact non-root registry
order as ASCII/LF:

```text
value_set_schema=S0-POP-UNIQUE-VALUE-SET-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
entry_count=21
entry_01_role_id=<first non-root role in frozen registry order>
entry_01_request_id=<64 lowercase hex>
entry_01_challenge_nonce=<64 lowercase hex>
entry_01_context_capability_id=<64 lowercase hex>
entry_01_request_capability_id=<64 lowercase hex>
...
entry_21_role_id=<last non-root role in frozen registry order>
entry_21_request_id=<64 lowercase hex>
entry_21_challenge_nonce=<64 lowercase hex>
entry_21_context_capability_id=<64 lowercase hex>
entry_21_request_capability_id=<64 lowercase hex>
```

The ellipsis is not emitted; the five exact entry lines repeat for indexes
`01` through `21`. The value set has one final LF. Its SHA-256 is the
`value_set_sha256` below, and the later challenge manifest must contain the
byte-identical ordered entries.

Every ceremony-ledger event has this exact ASCII/LF grammar:

```text
ceremony_event_schema=S0-POP-CEREMONY-LEDGER-EVENT-1
namespace=ceremony
sequence=<canonical unsigned decimal, beginning at 0>
previous_event_sha256=<64 lowercase hex; 64 zeroes only at sequence 0>
event_id=<64 lowercase hex>
event_kind=<values-reserved, challenge-frozen, or terminal>
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
value_set_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
values_reserved_event_id=<64 lowercase hex>
challenge_frozen_event_id=<64 lowercase hex>
terminal_from=<none, values-reserved, or challenge-frozen>
terminal_event_id=<64 lowercase hex>
decision=<reserved, frozen, accepted, or rejected>
```

There is one final LF. At `values-reserved`, the event ID equals
`values_reserved_event_id`; challenge hash, challenge-frozen event ID, and
terminal event ID are 64 zeroes; `terminal_from=none`; and
`decision=reserved`. At `challenge-frozen`, the reserved event ID is retained,
the event ID equals `challenge_frozen_event_id`, challenge hash is nonzero and
matches the exact manifest, terminal event ID is zero,
`terminal_from=none`, and `decision=frozen`. A terminal event names the exact
immediately prior ceremony event: from `values-reserved` it retains zero
challenge fields and is only `rejected`; from `challenge-frozen` it retains all
frozen fields and is `accepted` or `rejected`; its event ID equals
`terminal_event_id`. No other field/state combination parses.

Ceremony event IDs are independent 32-byte Windows CNG values. Event hashes
cover all exact bytes. The only success order is
`values-reserved -> challenge-frozen -> terminal/accepted`; either preterminal
state may instead move once to `terminal/rejected`. Every append atomically
advances the ceremony namespace's independent monotonic witness, and terminal
never frees any of the 84 reserved values.

### 4.3 Exact import and signing media

All textual control records and manifests in this section are exact ASCII with
LF, one final LF, no BOM, CR, leading/trailing space, omitted or reordered
field, extra field, or leading zero in a decimal. Binary `.bin` artifacts and
the raw result frame follow their separately stated byte grammars. Every named
ISO is finalized read-only and has exactly the listed regular-file entries
beneath its mandatory filesystem root, with no subdirectory or additional
filesystem object.

#### 4.3.1 Preactivation context import

At `key-generated`, each non-root appliance first receives a context ISO with
exactly `context-binding.txt`, `commitment-manifest.txt`, and
`challenge-manifest.txt`. The last two files are byte-identical to the frozen
manifests in section 4.2. `context-binding.txt` is:

```text
context_schema=S0-POP-CONTEXT-BINDING-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
registry_version=1
signer_id=<exact non-root registry role ID>
public_key_hex=<64 lowercase hex>
key_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
challenge_nonce=<64 lowercase hex>
request_id=<64 lowercase hex>
context_capability_id=<64 lowercase hex>
request_capability_id=<64 lowercase hex>
```

The appliance recomputes both file hashes, parses the complete manifests,
requires exact 22/21 order and its own unique entries, recomputes its key ID,
and compares every control field to its provisioned key and manifest entries.
Only then may it enter `pop-context-bound`. Thus a later two-file signing ISO
does not ask the appliance to verify bytes it never received.

#### 4.3.2 PoP request and exact preimage

At `pop-context-bound`, the PoP request ISO contains exactly `request.txt` and
`preimage.bin`. `request.txt` is:

```text
request_schema=S0-SIGNING-REQUEST-1
request_class=preactivation-pop-v1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
registry_version=1
signer_id=<exact non-root registry role ID>
public_key_hex=<64 lowercase hex>
key_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
challenge_nonce=<64 lowercase hex>
request_id=<64 lowercase hex>
artifact_kind=bootstrap-key-possession-proof-v1
signature_domain=URC-0.14-KEY-POSSESSION-PROOF-1
caller_capability_id=<the entry's request_capability_id>
preimage_length=<canonical unsigned decimal>
preimage_sha256=<64 lowercase hex>
```

`preimage.bin` is exactly these ASCII/LF bytes:

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

Every value must equal the previously bound context. No registry digest, edge,
phase, or active-artifact field is permitted.

#### 4.3.3 Active non-root request

An active non-root request ISO also contains exactly `request.txt` and
`preimage.bin`. Its exact `request.txt` field order is:

```text
request_schema=S0-SIGNING-REQUEST-1
request_class=active-section4-v1
campaign_id=<64 lowercase hex>
registry_version=1
registry_envelope_sha256=<externally activated registry-envelope digest>
signer_id=<exact active registry role ID>
edge_id=<exact inherited allowlisted edge ID>
phase_id=<exact inherited allowlisted phase ID>
artifact_kind=<exact inherited allowlisted section-4 artifact kind>
signature_domain=<exact inherited allowlisted section-4 domain>
request_id=<64 lowercase hex>
caller_capability_id=<64 lowercase hex>
preimage_length=<canonical unsigned decimal>
preimage_sha256=<64 lowercase hex>
```

`preimage.bin` is byte-identical to the canonical generic-envelope signature
preimage in
`s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md`,
section 4.2, authenticated SHA-256
`a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee`:

```text
URC-0.14-SIGNED-ARTIFACT
signer_role=<one exact active registry role ID>
signer_key_sha256=<that role's registry key ID>
record_length=<canonical decimal byte length>
<exact record_bytes>
record_sha256=<SHA-256 of exact record_bytes>
```

The exact `record_bytes` end in LF, so `record_sha256` begins immediately after
that LF with no added separator. The named v0.14 section remains byte-
authoritative and is not replaced by this overlay. The allowed signer/edge/
phase/artifact/domain/caller tuple also comes only from that authenticated
predecessor; this revision creates no tuple. An active record containing any
bootstrap field rejects.

#### 4.3.4 Separate offline-root registry request

After all proofs verify and the transcript freezes, CONTROL generates one
independent 32-byte root request ID and one independent 32-byte root attachment
capability ID with Windows CNG. The offline-root ISO contains exactly:

- `request.txt`;
- `preimage.bin`;
- `anchor-record.txt`;
- `commitment-manifest.txt`;
- `challenge-manifest.txt`;
- `proof-transcript.txt`; and
- `registry-record.txt`.

The five supporting public artifact files (`anchor-record.txt` through
`registry-record.txt`) are byte-identical to their frozen forms; `preimage.bin`
is reconstructed from the exact registry record as specified below.
`request.txt` is:

```text
request_schema=S0-ROOT-REGISTRY-SIGNING-REQUEST-1
ceremony_class=root-registry-v1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
registry_version=1
signer_id=control-root-authority
public_key_hex=<64 lowercase hex>
key_id=<64 lowercase hex>
anchor_record_sha256=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
proof_transcript_sha256=<64 lowercase hex>
registry_record_sha256=<64 lowercase hex>
request_id=<64 lowercase hex>
caller_capability_id=<64 lowercase hex>
artifact_kind=registry-v1-envelope
signature_scope=section4-generic-envelope-v1
preimage_length=<canonical unsigned decimal>
preimage_sha256=<64 lowercase hex>
```

`preimage.bin` is the exact v0.14 generic-envelope signature preimage over the
byte-identical `registry-record.txt`:

```text
URC-0.14-SIGNED-ARTIFACT
signer_role=control-root-authority
signer_key_sha256=<root key ID>
record_length=<canonical decimal byte length of registry-record.txt>
<exact registry-record.txt bytes>
record_sha256=<SHA-256 of exact registry-record.txt bytes>
```

The root independently authenticates the pinned anchor, applies
`S0-ED25519-STRICT-1` to all 22 keys and all 21 proofs, checks manifest and
transcript order/hashes, requires registry entries byte-equal to commitments,
and signs only this preimage. It rejects every other file set or ceremony class.

#### 4.3.5 Host media admission and raw result frame

Before attaching any signer import package, host preflight freezes:

```text
import_admission_schema=S0-SIGNER-IMPORT-ADMISSION-1
authority_id=control-host-preflight
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
import_class=<preactivation-context-v1, registry-binding-v1, or activation-binding-v1>
from_state=<exact allowed source state>
to_state=<exact allowed destination state>
package_sha256=<64 lowercase hex>
package_object_id=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
decision=approved
```

The import class/state mapping is exact:
`preactivation-context-v1` maps `key-generated -> pop-context-bound`,
`registry-binding-v1` maps `pop-issued -> registry-bound`, and
`activation-binding-v1` maps `registry-bound -> active`. No other source or
destination literal parses.

Before attaching either non-root signing-request ISO, host preflight freezes:

```text
request_admission_schema=S0-SIGNING-REQUEST-ADMISSION-1
authority_id=control-host-preflight
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
request_class=<preactivation-pop-v1 or active-section4-v1>
request_id=<64 lowercase hex>
caller_capability_id=<64 lowercase hex>
authority_context_kind=<challenge-manifest or registry-envelope>
authority_context_sha256=<64 lowercase hex>
request_iso_sha256=<64 lowercase hex>
request_iso_object_id=<64 lowercase hex>
result_media_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
decision=approved
```

The context mapping is exact: PoP uses `challenge-manifest` and active section-4
uses `registry-envelope`. Before attaching the separate offline-root ISO, host
preflight instead freezes this disjoint record:

```text
root_ceremony_admission_schema=S0-ROOT-CEREMONY-ADMISSION-1
authority_id=control-host-preflight
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=control-root-authority
ceremony_class=root-registry-v1
request_id=<64 lowercase hex>
caller_capability_id=<64 lowercase hex>
proof_transcript_sha256=<64 lowercase hex>
request_iso_sha256=<64 lowercase hex>
request_iso_object_id=<64 lowercase hex>
result_media_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
decision=approved
```

The root ceremony context is exactly `proof-transcript`. Every
object/event/result-media ID is an independently generated opaque 32-byte value,
not a content hash, and is unique in the project-lifetime TCB admission ledger.
The appropriate one-use capability is atomically consumed against the exact
immutable ISO object handle before attachment. Same capability with another
hash, object, signer, state, or request rejects. Registry- and activation-import
capabilities are generated after their respective source artifacts freeze but
before the control record and complete import package freeze; context and PoP-
request capabilities are the exact challenge-manifest values.

Every successful signer output uses this exact raw frame:

```text
magic: exact ASCII `S0-SIGNATURE-RESULT-1\n`
request_id: 32 raw bytes
signer_id_length: unsigned 16-bit big-endian
signer_id: that many permitted ASCII role-ID bytes
preimage_sha256: 32 raw bytes
signature: 64 raw bytes
frame_sha256: 32 raw bytes over every preceding frame byte
```

All remaining raw-disk capacity is zero. The host reads it without mounting a
filesystem. Request/import media and raw result disks are TCB temporary replicas,
not E00A-E56 or any of the 27 stores. No private key or protected experimental
byte crosses these routes.

#### 4.3.6 Common one-shot appliance lifecycle and admission ledger

Every non-root import, non-root signing request, and offline-root ceremony uses
the same fail-closed physical order:

1. require the target environment powered off, with no prior exchange ISO or
   result medium attached and no unresolved prior media event;
2. authenticate the exact admission record, ledger/witness head, immutable ISO
   object handle/hash, target identity/state, and one-use capability;
3. atomically consume the capability to `pending`, attach exactly that one
   read-only ISO and, for a signing route only, exactly one new raw result disk;
4. boot only the frozen parser/service, perform one import or one signing
   decision, write at most the one raw result frame, seal it, and shut down;
5. detach every attached exchange medium—the ISO and, for a signing route only,
   the result disk—before any next state transition or attachment; and
6. atomically record `consumed` only after shutdown, detachment, and exact
   result/state evidence. A failure or uncertain `pending` becomes terminal.

Prior request/import bytes and result media remain inaccessible to the target
and are destroyed under the inherited temporary-replica rule before another
request or import may attach. No simultaneous, stale, shared, reused, writable,
or hot-attached exchange media is permitted. The persistent signer disk may
retain only key/configuration bytes plus bounded request/capability IDs,
preimage/package hashes, decisions, and anti-replay state; request/preimage/
package bodies and result signatures are removed after detachment.
This removal rule applies to the isolated target's persistent storage; CONTROL
may retain the separately admitted public result frame or derived public
envelope/transcript under its named ceremony record.

The host mirrors every media transition in a project-lifetime signer-media
ledger whose exact event grammar is:

```text
signer_media_event_schema=S0-SIGNER-MEDIA-LEDGER-EVENT-1
namespace=signer-media
sequence=<canonical unsigned decimal, beginning at 0>
previous_event_sha256=<64 lowercase hex; 64 zeroes only at sequence 0>
event_id=<64 lowercase hex>
prior_route_event_id=<64 lowercase hex; 64 zeroes only at the route's reserved event>
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
route_kind=<import, nonroot-request, or root-ceremony>
route_class=<exact import_class, request_class, or ceremony_class literal>
request_id=<64 lowercase hex, or 64 zeroes only for an import>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex; zero only before admission freeze>
admission_record_sha256=<64 lowercase hex; zero only before admission freeze>
media_object_sha256=<64 lowercase hex, or 64 zeroes before admission freeze>
media_object_id=<64 lowercase hex, or 64 zeroes before admission freeze>
result_media_id=<64 lowercase hex, or 64 zeroes only for an import>
state=<reserved, admission-frozen, pending, consumed, or terminal>
terminal_from=<none, reserved, admission-frozen, or pending>
decision=<reserved, approved, executing, accepted, or rejected>
```

The only successful order is
`reserved -> admission-frozen -> pending -> consumed`; any pre-consumed state
may move once to `terminal/rejected`. Field/state combinations
outside these exact rules reject:

- `reserved` has zero `prior_route_event_id`, `admission_event_id`,
  `admission_record_sha256`, `media_object_sha256`, and `media_object_id`, and
  has `terminal_from=none`;
- `admission-frozen` has `prior_route_event_id` equal to the reserved event,
  `admission_event_id` equal to its own `event_id`, the SHA-256 of the exact
  admission record, and the now-nonzero immutable media hash/object ID;
- `pending` and `consumed` retain those exact admission/media fields and name
  the immediately prior route event;
- `terminal` names the exact immediately prior route event and sets
  `terminal_from` to that prior state; only `terminal_from=reserved` retains
  zero `admission_event_id`, `admission_record_sha256`,
  `media_object_sha256`, and `media_object_id`, while later terminal events
  retain the exact nonzero values already frozen;
- `result_media_id` is zero for imports and nonzero for non-root signing and
  offline-root ceremony routes in every state, and all other route-identity
  fields are retained byte-for-byte across that route's events; and
- no nonterminal record has a non-`none` `terminal_from`.

The only nonterminal state/decision pairs are `reserved/reserved`,
`admission-frozen/approved`, `pending/executing`, and `consumed/accepted`;
terminal is always `terminal/rejected`. Event IDs are independent 32-byte
Windows CNG values. Event hashes cover all exact bytes. The appliance's own
persistent anti-replay ledger independently enforces
`unused -> pending -> consumed|terminal` for every request ID and capability,
including ordinary `active-section4-v1` requests. Crash at either host or
appliance `pending`, duplicate request/capability, or disagreement between the
two ledgers aborts the candidate without retry.

The ceremony, signer-media, and invocation ledgers are separate namespaces of
the same future atomic, witness-backed provider profile. Each has an independent
monotonic head in a rollback domain outside the ledger filesystem. Therefore
`launch-ledger-provider-unresolved` blocks every namespace from implementation.
Ledger/witness unavailability, rollback, head mismatch, partial transition, or
restoration of a consumed capability invalidates the candidate.

### 4.4 State, transcript, registry binding, and activation

The effective non-root appliance state order is:

`proposed -> provisioned -> key-generated -> pop-context-bound -> pop-issued -> registry-bound -> active -> retired|lost|compromised`

At `key-generated`, exactly one matching context import may atomically advance
to `pop-context-bound`. At `pop-context-bound`, exactly one matching PoP request
may be consumed. Before key invocation, the persistent anti-replay ledger moves
the request ID `unused -> pending`; after signing it moves
`pending -> consumed` with exact result hash and decision before `pop-issued`.
A crash or uncertain `pending` state aborts the whole ceremony. No replay,
selective retry, active request, or second transition is permitted.

CONTROL independently applies `S0-ED25519-STRICT-1` to every key and proof.
The public ceremony verdict `proof-verified` is external evidence, not a signer-
appliance state. All 21 proofs must verify before this transcript freezes:

```text
transcript_schema=S0-POP-TRANSCRIPT-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
proof_count=21
proof_01_role_id=<first non-root role in frozen registry order>
proof_01_request_id=<64 lowercase hex>
proof_01_preimage_sha256=<64 lowercase hex>
proof_01_signature_hex=<128 lowercase hex>
...
proof_21_role_id=<last non-root role in frozen registry order>
proof_21_request_id=<64 lowercase hex>
proof_21_preimage_sha256=<64 lowercase hex>
proof_21_signature_hex=<128 lowercase hex>
```

The ellipsis is not a record byte. The root may accept exactly one
`root-registry-v1` package only at `key-generated`. Its request ID advances
atomically through the same `unused -> pending -> consumed` anti-replay order;
uncertain `pending` aborts the candidate. One successful signature advances the
offline root environment to `registry-signed`; no second registry signature is
possible.
CONTROL assembles the generic signed registry envelope from the exact preimage
and returned signature. The public root-candidate state becomes
`externally-activated` only after the exact user activation record verifies;
that public transition is not another offline-root ceremony request.

At `pop-issued`, a non-root appliance may receive one registry-binding ISO with
exactly `binding-control.txt`, `anchor-record.txt`,
`commitment-manifest.txt`, `challenge-manifest.txt`, `proof-transcript.txt`, and
`registry-envelope.bin`. `binding-control.txt` is:

```text
binding_schema=S0-SIGNER-REGISTRY-BINDING-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
registry_version=1
signer_id=<exact non-root registry role ID>
public_key_hex=<64 lowercase hex>
key_id=<64 lowercase hex>
git_object_format=sha1
git_commit_hex=<40 lowercase hex>
anchor_record_sha256=<64 lowercase hex>
commitment_manifest_sha256=<64 lowercase hex>
challenge_manifest_sha256=<64 lowercase hex>
proof_transcript_sha256=<64 lowercase hex>
registry_envelope_sha256=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
```

The appliance recomputes every file hash, verifies exact external commit/anchor
pins, strict root key/signature, registry bytes, commitment/challenge/transcript,
campaign, and its own entry before entering `registry-bound`.
This is cryptographic validation of an inert candidate envelope and is expressly
permitted before activation. It grants no ordinary signing permission, no
authority to accept another section-4 signature, no experimental edge/store
access, and no `active` state. Only the later user-approved activation record
makes that already-validated registry authoritative for section-4 use.

At `registry-bound`, the activation ISO contains exactly
`activation-record.txt` and `activation-binding.txt`. The first file is the
byte-identical v0.1 `URC-0.14-ROOT-ACTIVATION-1` record.
`activation-binding.txt` is:

```text
activation_binding_schema=S0-SIGNER-ACTIVATION-BINDING-1
campaign_id=<64 lowercase hex>
registry_version=1
signer_id=<exact non-root registry role ID>
registry_envelope_sha256=<64 lowercase hex>
proof_transcript_sha256=<64 lowercase hex>
activation_record_sha256=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
approval_state=approved
```

The import must match the appliance's registry-bound state and the exact user-
approved activation record before the one-way transition to `active`. Every
package uses the exact import-admission record in section 4.3.5. A missing or
extra file/object, wrong filename/order/bytes/hash, changed capability, replay,
cross-appliance attachment, crash during a pending import, or second transition
is terminal for the candidate. None of these imports signs anything.

### 4.5 Three exclusive signature scopes

Every signature-bearing public artifact belongs to exactly one scope:

1. `preactivation-pop-v1`: the 21 detached PoP signatures; it grants no
   ordinary signing authority;
2. `section4-generic-envelope-v1`: the root registry signature created by the
   offline root ceremony and all ordinary section-4 generic envelopes; the root
   envelope may be cryptographically validated as an inert candidate before
   activation but is usable as authority for ordinary signature verification
   only after external activation, and ordinary role signing requires an
   `active` appliance; or
3. `inherited-signature-unresolved`: predecessor signatures outside the
   generic-envelope scope, still forbidden to implement.

Non-root request class, offline-root ceremony class, and signature scope are
distinct fields. The `root-registry-v1` ceremony and `active-section4-v1`
request both produce `section4-generic-envelope-v1` signatures but have disjoint
states, schemas, and allowlists. The transcript container records signatures
but is not itself signed. The TCB launch descriptor in section 5 is deliberately
unsigned and belongs to none of these scopes. Scope overlap, absence for a
signature-bearing object, or use of a PoP as active authority rejects.

## 5. TCB-bound invocation descriptor

### 5.1 Authority decision

The phrase `signed invocation descriptor` is removed from the effective design.
No new experimental signer, registry entry, ceremony key, or hidden trust root
is introduced.

The descriptor is authenticated by the already declared TCB: CONTROL freezes
the invocation declaration, the input route controller constructs exact input
bytes, and host preflight binds descriptor, media, VM, and policy hashes before
boot. The guest validates canonical bytes and content bindings; post-run
admission cross-checks host and guest evidence. This does not protect against a
malicious host administrator, which remains an explicit nonclaim.

### 5.2 Canonical descriptor

The ISO contains `invocation-descriptor.txt` with exact ASCII/LF bytes:

```text
descriptor_schema=S0-INVOCATION-DESCRIPTOR-2
descriptor_authority_id=input-route-controller
campaign_id=<64 lowercase hex>
invocation_id=<64 lowercase hex>
role_position_id=<one exact frozen role-position ID>
vm_id=<lowercase 8-4-4-4-12 hexadecimal UUID>
base_export_sha256=<64 lowercase hex>
vm_configuration_sha256=<64 lowercase hex>
startup_service_sha256=<64 lowercase hex>
actor_executable_sha256=<64 lowercase hex>
execution_policy_sha256=<64 lowercase hex>
topology_policy_sha256=<64 lowercase hex>
resource_policy_sha256=<64 lowercase hex>
input_content_manifest_sha256=<64 lowercase hex>
route_manifest_sha256=<64 lowercase hex>
expected_output_policy_sha256=<64 lowercase hex>
output_media_id=<64 lowercase hex>
output_capacity_bytes=<canonical unsigned decimal>
allowed_boot_count=1
```

There is one final LF and no extra field. The descriptor deliberately omits
its own hash and the whole ISO hash, preventing a self-referential digest.
`input-content-manifest` lists every payload file except the descriptor and the
manifest itself in ascending ASCII path order. It binds exact paths, lengths,
hashes, source stores, edge IDs, and recipients. The host's external admission
record binds the descriptor and the complete ISO.

### 5.3 Host launch-admission record

Before attachment, host preflight freezes exact ASCII/LF bytes:

```text
admission_schema=S0-LAUNCH-ADMISSION-2
admission_authority_id=control-host-preflight
preflight_configuration_sha256=<64 lowercase hex>
preflight_capability_id=<64 lowercase hex>
campaign_id=<64 lowercase hex>
invocation_id=<64 lowercase hex>
role_position_id=<exact frozen role-position ID>
vm_id=<lowercase 8-4-4-4-12 hexadecimal UUID>
descriptor_sha256=<64 lowercase hex>
input_content_manifest_sha256=<64 lowercase hex>
input_iso_sha256=<64 lowercase hex>
input_iso_object_id=<64 lowercase hex>
output_media_id=<64 lowercase hex>
initial_output_media_sha256=<64 lowercase hex>
base_export_sha256=<64 lowercase hex>
vm_configuration_sha256=<64 lowercase hex>
startup_service_sha256=<64 lowercase hex>
actor_executable_sha256=<64 lowercase hex>
execution_policy_sha256=<64 lowercase hex>
topology_policy_sha256=<64 lowercase hex>
resource_policy_sha256=<64 lowercase hex>
route_manifest_sha256=<64 lowercase hex>
expected_output_policy_sha256=<64 lowercase hex>
reservation_event_id=<64 lowercase hex>
bound_event_id=<64 lowercase hex>
boot_authorization_id=<64 lowercase hex>
allowed_boot_count=1
decision=approved
```

The admission record has one final LF, no BOM or CR, no leading/trailing
whitespace, no leading zero in a decimal, and no omitted, reordered, or extra
field.

The admission record is a TCB audit object, not an experimental store artifact
or a signature-bearing object. Its authority is the exact externally pinned
CONTROL host-preflight configuration and exact preflight capability. Only the
`control-host-preflight` service ACL may create an `approved` admission record,
append its admission event, or consume its boot authorization. The input route
controller may construct the descriptor but can never approve launch. A branch,
ambient file, operator-entered override, unsigned alternate record, wildcard
source, or after-freeze edit is not an authority source.
`control-host-preflight` names a frozen least-privilege function of the existing
host-administrator/CONTROL TCB, not a fifth section-3.1 infrastructure principal,
experimental role, signer, store, reader, or edge.
Its hash, exact immutable ISO object identity, and referenced ledger/boot events
are appended to the project-lifetime `invocation-id-ledger` before boot.
Preflight opens and
hashes that exact object through a non-path-reusable handle, attaches the same
object without resolving a mutable path again, and atomically consumes the one
boot authorization before power-on. Path swap, handle substitution, second
consume, unavailable ledger, or partial append rejects before boot.

### 5.4 Verification order

The exact order is:

1. CONTROL reserves the invocation ID and freezes the `reserved` event in the
   project-lifetime ledger before the invocation enters `declared`;
2. the route controller constructs content manifest, route manifest,
   descriptor, and finalized ISO;
3. host preflight independently rehashes all named bytes, binds the exact
   immutable ISO object in the `bound` event, and requires every
   descriptor/admission field to match VM, media, base, policy, and ledger;
4. host preflight freezes the admission record, appends its exact hash and the
   unique boot authorization in `admission-frozen`, and advances the external
   monotonic witness;
5. only that exact `approved` record permits read-only ISO and blank output-
   media attachment, and the one boot authorization is atomically consumed in
   `boot-consumed` before power-on;
6. the frozen guest startup service parses the descriptor, rejects any encoding
   or file-set mismatch, verifies content/route/executable/output-policy hashes,
   and launches only the declared role executable;
7. host and guest evidence must contain the same descriptor hash and invocation
   ID; and
8. output admission rejects the whole invocation if any preflight, guest, or
   post-run value differs.

The guest does not claim to independently authenticate the trusted host or to
observe host-only VM ID, base, configuration, VHDX identity, or ISO object-
handle facts. It repeats only canonical parsing, payload/policy hashes,
executable self-measurement, and its declared invocation binding. The host/
route controller's ability to substitute both ISO and evidence remains a TCB
assumption stated by v0.1. The descriptor is an unsigned TCB control record and
temporary replica; it makes no cryptographic-origin claim.

## 6. Single invocation uniqueness value

### 6.1 Elimination of the second nonce

There is no separate invocation nonce in the effective v0.2 design. The exact
32 raw bytes represented by `invocation_id` are the sole external uniqueness
input for declaration, VM binding, state transitions, guest secret derivation,
input/output frames, and evidence.

Any record or implementation that adds a second `invocation_nonce`, uses a
different external value for secret derivation, or permits host and guest to
bind different values rejects. This replacement removes the v0.1 ambiguity; it
does not rename two separately generated values to the same label.

### 6.2 Generation and global reservation

CONTROL obtains exactly 32 bytes by a successful Windows CNG
`BCryptGenRandom(NULL, buffer, 32, BCRYPT_USE_SYSTEM_PREFERRED_RNG)` call before
that invocation is provisioned. Any non-success status or wrong output length
rejects. It renders the value as 64 lowercase hex only in text records.
Independent reservations may coexist only within the inherited maximum-
concurrency and phase schedule.

Before a VM, descriptor, ISO, or output disk is created, the host performs an
atomic reserve-if-absent operation in a project-lifetime append-only
`invocation-id-ledger`. It is a TCB security-control component, not a 28th
experimental store. Reserved IDs are never deleted or reused across campaigns,
including after failure, quarantine, cancellation, candidate rejection, or a
successor-version transition.

Every ledger event is exact ASCII/LF and has this common envelope:

```text
ledger_event_schema=S0-INVOCATION-LEDGER-EVENT-1
project_id=human-ai-development-tradition
sequence=<canonical unsigned decimal, beginning at 0>
previous_event_sha256=<64 lowercase hex; 64 zeroes only at sequence 0>
event_id=<64 lowercase hex>
event_kind=<reserved, bound, admission-frozen, boot-consumed, or terminal>
campaign_id=<64 lowercase hex>
invocation_id=<64 lowercase hex>
role_position_id=<exact frozen role-position ID>
payload_length=<canonical unsigned decimal>
<exact event-kind payload bytes>
payload_sha256=<64 lowercase hex>
```

There is one final LF. `payload_length` counts the exact payload bytes, which
also end in LF. Optional fields are forbidden; the parser selects one of these
five exact payload grammars from `event_kind`:

```text
reservation_event_id=<same event_id>
state=reserved
```

```text
reservation_event_id=<prior reserved event ID>
bound_event_id=<same event_id>
vm_id=<lowercase 8-4-4-4-12 hexadecimal UUID>
descriptor_sha256=<64 lowercase hex>
input_iso_sha256=<64 lowercase hex>
input_iso_object_id=<64 lowercase hex>
output_media_id=<64 lowercase hex>
initial_output_media_sha256=<64 lowercase hex>
state=bound
```

```text
reservation_event_id=<prior reserved event ID>
bound_event_id=<prior bound event ID>
admission_event_id=<same event_id>
admission_sha256=<64 lowercase hex>
preflight_configuration_sha256=<64 lowercase hex>
preflight_capability_id=<64 lowercase hex>
boot_authorization_id=<64 lowercase hex>
state=admission-frozen
```

```text
reservation_event_id=<prior reserved event ID>
bound_event_id=<prior bound event ID>
admission_event_id=<prior admission-frozen event ID>
boot_consumed_event_id=<same event_id>
admission_sha256=<64 lowercase hex>
boot_authorization_id=<64 lowercase hex>
state=boot-consumed
```

```text
reservation_event_id=<prior reserved event ID>
terminal_from=<reserved, bound, admission-frozen, or boot-consumed>
bound_event_id=<prior bound event ID or 64 zeroes>
admission_event_id=<prior admission-frozen event ID or 64 zeroes>
boot_consumed_event_id=<prior boot-consumed event ID or 64 zeroes>
terminal_event_id=<same event_id>
terminal_reason=<completed, failed, quarantined, cancelled, candidate-rejected, or successor-closed>
state=terminal
```

In a terminal payload, every event ID through `terminal_from` is required and
every later-stage ID is exactly 64 zeroes; a skipped, nonzero future, or zeroed
past ID rejects. `completed` is permitted only from `boot-consumed`.

The event envelope hash is SHA-256 of all exact envelope bytes. CONTROL obtains
every event ID, `input_iso_object_id`, `preflight_capability_id`, and
`boot_authorization_id` from separate successful 32-byte Windows CNG calls.
They are opaque identifiers, not content hashes, and each is unique across the
project lifetime. The output-media ID keeps its inherited generation rule.
The bound event ID is allocated before the admission record freezes, so the
record may refer to that completed event without a self-hash cycle. The
admission-frozen event then commits the completed admission hash.

The logical provider must atomically enforce forward transitions
`reserved -> bound -> admission-frozen -> boot-consumed`, allow one terminal
transition from any reached state, enforce uniqueness of invocation and
authorization IDs, and permit one boot consume. After every append,
it must atomically advance an independently persisted monotonic witness holding
the exact tuple `(project_id, sequence, event_sha256)`. That witness must be in
a rollback domain independent of restoration of the ledger host filesystem.
Every reservation, preflight, boot, and later audit compares the ledger head to
the witness before acting. Restoring an older internally valid ledger therefore
produces a sequence/head mismatch and rejects.

The concrete atomic ledger and rollback-resistant witness mechanism is
`launch-ledger-provider-unresolved`. It must be chosen, separately designed,
implemented, and independently reviewed before any VM provisioning. A local
append-only file, ACL, hash chain, timestamp, or restorable host snapshot alone
does not close this gate. Witness or ledger unavailability, rollback, mismatch,
or compromise invalidates the candidate.

The logical ledger and witness are TCB security-control components. This text
does not add an experimental identity, role, signer, store, reader, or edge and
does not select a new operator principal. If the eventual provider requires a
new infrastructure credential or external service, that exact authority and
threat-model change belongs to the separately reviewed provider decision.

A duplicate draw, concurrent/conflicting role binding, absent reservation,
second reservation, stale object binding, already-consumed authorization, or
non-atomic transition rejects before provisioning or boot. Terminal state never
frees an ID. A failed frozen attempt is not selectively redrawn or resumed.

### 6.3 Invocation-secret derivation

After the new machine identity exists and the startup service has read the
descriptor from the attached ISO, but before the actor principal receives any
protected payload access, the guest obtains exactly 32 fresh bytes
`guest_random` from the approved guest OS CSPRNG. The future implementation
derives exactly 32 bytes using RFC 5869 HKDF-SHA-256:

```text
IKM = guest_random
salt = the 32 raw invocation_id bytes
L = 32 bytes
```

The `info` value is exactly these ASCII/LF bytes:

```text
S0-ACTOR-INVOCATION-SECRET-1
campaign_id=<64 lowercase hex>
invocation_id=<64 lowercase hex>
role_position_id=<exact frozen role-position ID>
vm_id=<lowercase 8-4-4-4-12 hexadecimal UUID>
descriptor_sha256=<64 lowercase hex>
```

The info value has one final LF. `guest_random` and the derived secret never
enter a command line, public log, ISO, output disk, checkpoint, crash dump, or
persistent actor state. No secure-erasure claim is made. The implementation
must prove that different reserved invocation IDs bind different derivation
contexts and that two fresh guests do not reuse a derived secret.

### 6.4 Lifecycle and evidence

The `reserved` transition binds campaign ID, invocation ID, role-position ID,
reservation event ID, and sequence. Every transition from `bound` onward binds
VM ID and descriptor hash either directly or through its exact `bound_event_id`
chain. Diagnostic clocks do not authorize ordering. The host, guest, ingestion
frames, and immutable admission record must agree on the same invocation ID.

The machine-readable realization must add the invocation ledger and descriptor
schemas, all three signer import-package schemas, the two non-root request and
offline-root ceremony
schemas, all three media-admission schemas, and rollback-witness binding as TCB-
control inventories without changing the frozen role, signer, store, reader,
or edge counts.
It must additionally include `S0-POP-UNIQUE-VALUE-SET-1`,
`S0-POP-CEREMONY-LEDGER-EVENT-1`, and
`S0-SIGNER-MEDIA-LEDGER-EVENT-1`, with the ceremony, signer-media, and invocation
namespace/witness bindings.

## 7. Rejection and stop conditions added by v0.2

The candidate rejects on any:

- public key or signature point outside the exact nonidentity order-`L`
  subgroup;
- cofactored-only acceptance, skipped strict validation, or non-Boolean result;
- bootstrap request with a registry digest or active field;
- active request without the externally activated registry digest;
- root ceremony with an activated-registry dependency, wrong root state, missing
  ceremony bytes, or a second registry signature;
- activation required merely to validate the inert registry candidate, or the
  inert candidate used as ordinary signing/verification authority before the
  exact user activation record;
- cross-class field, wrong state, missing/extra import file, repeated PoP,
  changed commitment/challenge, or PoP used as ordinary authority;
- signature-bearing artifact in zero or multiple effective scopes;
- descriptor signature claim, unlisted descriptor authority, circular digest,
  noncanonical descriptor, or descriptor/admission/media mismatch;
- separate invocation nonce, duplicate/reserved invocation ID, ledger/witness
  rollback or mismatch, reused boot authorization, mismatched derivation
  context, or host/guest ID disagreement; or
- inability of the later implementation to expose the strict point/subgroup
  checks and exact acceptance evidence for independent review.

Before protected material exists, an implementation defect may be corrected
only under its later gate and reviewed again. This design revision itself does
not open that gate.

## 8. Closed gates and maximum claim

The maximum claim is that v0.2 proposes exact public repairs for the four v0.1
review findings while preserving the accepted topology and isolation design.
It does not establish that any repair has been implemented or independently
accepted.

Still closed are VM/account/ACL/vault implementation, actual Ed25519 or HKDF
execution, key generation, signer-provider and launch-ledger-provider selection,
root ceremony, protected
content, bank, label, oracle, condition map, package, executor, external
provider session, model call, judge handoff, scoring, statistics, S0 execution,
E0, central-system implementation, Project Brain integration, operational
safety, economic value, and model-to-model transfer.

The only natural next gate after this revision is frozen and transferred is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`

## 9. Primary references

- RFC Editor, [RFC 8032: Edwards-Curve Digital Signature Algorithm](https://www.rfc-editor.org/rfc/rfc8032)
- RFC Editor, [RFC 9381: Verifiable Random Functions](https://www.rfc-editor.org/rfc/rfc9381)
- NIST, [SP 800-89: Recommendation for Obtaining Assurances for Digital Signature Applications](https://csrc.nist.gov/pubs/sp/800/89/final)
- RFC Editor, [RFC 5869: HMAC-based Extract-and-Expand Key Derivation Function](https://www.rfc-editor.org/rfc/rfc5869)
- Microsoft, [BCryptGenRandom function](https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptgenrandom)
