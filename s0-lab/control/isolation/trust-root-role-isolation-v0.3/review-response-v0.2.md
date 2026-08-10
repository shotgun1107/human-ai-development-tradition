# S0 v0.14 trust-root and role-isolation v0.3 review response v0.2

- `status`: author response candidate
- `responds_to_sha256`: `67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990`
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `claim_kind`: proposed finding closure only

## 1. Response limit

This record maps only `TRI2-M01` and `TRI2-m01` from the authenticated v0.2
independent review to the proposed v0.3 successor text. It is explanatory
author evidence, not an independent review, implementation result, or finding
closure. Only a fresh independent reviewer may close either finding.

The v0.2 review's proposal-text closure of `TRI-B01`, `TRI-B02`, `TRI-M01`, and
`TRI-M02` is preserved as predecessor evidence. This response neither reopens
those findings nor expands the v0.3 revision beyond the two new findings.

## 2. Finding-by-finding response

### 2.1 `TRI2-M01`: observable import outcomes

**Review finding:** the three state-changing import routes had no canonical
host-observable result. Shutdown and detachment could not distinguish an
accepted transition from an internal parse or validation rejection, so the
host could not justify `consumed/accepted` in the mirrored signer-media
ledger.

**Revision:** the v0.3 design and authority/acceptance addenda define one
outcome route whose raw-medium kind is `import-outcome-v1` for each of
`preactivation-context-v1`, `registry-binding-v1`, and
`activation-binding-v1`.

- Every import receives one fresh nonzero `result_media_id` and one raw,
  zero-initialized outcome medium whose capacity is exactly 2,048 bytes; its
  one complete frame may be at most 2,048 bytes.
- The existing import-transition service is named
  `S0-IMPORT-TRANSITION-TCB-1`. It emits at most one canonical
  `S0-SIGNER-IMPORT-OUTCOME-1` frame and no protected or private-key byte.
- The frame binds campaign, ceremony, signer, import class, exact from/to
  states, package hash and object ID, admission hash, the one-use capability,
  before/after appliance state, decision, outcome-medium kind and identity, and
  the preallocated
  reserved, admission-frozen, pending, and completion signer-media event IDs.
- The appliance durably records its transition decision and after-state before
  finalizing the frame. The host reads the raw medium without mounting it,
  verifies the exact frame and zero remainder, and binds the frame hash in the
  preallocated completion event before cleanup.
- The complete outcome classification is `accepted`, `parse-rejected`,
  `validation-rejected`, `state-commit-failed`, `crash`, `missing`,
  `duplicate`, or `disagreement`. Only one exact `accepted` frame whose state
  and host evidence agree permits `consumed`; every other class requires a
  terminal result when the exact ledger append remains possible and otherwise
  permits no completion claim. Both paths fail closed.
- Missing, partial, oversized, malformed, duplicate, replayed, cross-signer,
  cross-class, wrong-event, or host/appliance-disagreeing evidence cannot be
  inferred from shutdown or repaired by selective retry. The candidate is
  rejected, the capability and event IDs remain spent, and the temporary
  medium is detached and destroyed under the inherited cleanup rule.

The outcome is an unsigned TCB control record. Its authority is the already
declared pinned host/appliance TCB and exact one-shot admission, not a new key,
registry signer, signature scope, experimental role, store, reader, or edge.
The acceptance addendum traces success and every failure class for all three
imports and makes the effective ledger transition noncompensatory.

**Claim:** proposed major-finding closure at public design-text level only. No
appliance, medium, frame, state transition, ledger, or hostile case was
implemented or executed.

### 2.2 `TRI2-m01`: order-eight vector provenance

**Review finding:** RFC 9381 section 5.4.5 does not provide the stated
`bad_y2` decimal coordinate or the four claimed order-eight encodings.

**Revision:** the v0.3 design removes that false attribution. It supplies an
independently checkable Edwards-curve derivation and four literal exact
32-byte encodings: the two derived canonical y encodings, each with both
permitted x-sign bits. The derivation states the field and encoding steps
needed to reproduce the bytes instead of treating a copied name or label as
evidence.

The mandatory nonidentity order-`L` predicate for admitted public keys and
`R` values is unchanged. The four values remain future negative vectors, and
a later independent implementation review must still reproduce their
construction, canonical decoding, and point orders before relying on them.

**Claim:** proposed minor-finding closure at public design-text level only. The
four public literal specifications are frozen, but no executable vector
artifact was generated and no vector was decoded, multiplied, signed, or
verified.

## 3. Non-regression and closed gates

The v0.3 successor must preserve:

- 32 aggregated role rows, 40 role positions, eight paired rows;
- 21 experimental section-4 signers, 19 `none` positions, one non-row root,
  and 22 registry IDs;
- 27 stores, 46 explicit readers, and 64 edge rows;
- 107 noncompensatory acceptance rows, three ledger namespaces, eight future
  executor invocation/session units, and maximum concurrency three;
- equal A-D source information, authority, model condition, time, output, and
  scoring opportunity;
- the three exclusive signature scopes; and
- every inherited provider, implementation, protected-material, E0, and S0
  blocker or nonclaim.

The new outcome medium and records are TCB temporary/control objects only.
They do not alter the frozen experimental topology or authorize an
implementation.

Still closed are VM, sandbox, account, network, clipboard, Git, ACL, vault,
store, signer, ledger, witness, or provider implementation; key generation,
anchor, registry, Ed25519, HKDF, or vector execution; protected material,
fixture, bank, label, oracle, condition map, package, executor, model call,
judge handoff, scoring, statistics, E0, S0, central-system implementation, and
Project Brain integration.

## 4. Exact next review target

After the complete v0.3 candidate and its authentication records are frozen,
a fresh reviewer must authenticate and reconstruct the v0.1 plus v0.2 plus
v0.3 composition without trusting this response. The review must attack both
proposed repairs, verify every frozen invariant and closed gate, and return
only an allowed verdict from the v0.3 independent-review brief.

No later gate opens from this author response. The next permissible gate is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`
