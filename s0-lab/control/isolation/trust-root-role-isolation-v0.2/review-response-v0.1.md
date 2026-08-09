# S0 v0.14 trust-root and role-isolation v0.2 review response v0.1

- `status`: author response candidate
- `responds_to_sha256`: `d99cf801719e2f524ca87fe3741b8a6776c4682df304d9448c245e5d3fee7404`
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `claim_kind`: proposed finding closure only

## 1. Response limit

This record maps the four authenticated v0.1 findings to proposed v0.2 text.
It is not independent evidence and cannot change a finding's status. Only a
fresh independent review may close a finding.

## 2. Finding-by-finding response

### 2.1 `TRI-B01`: Ed25519 public-key validity

**Review finding:** canonical identity/small-order values could satisfy the
cofactored verification equation without possession of a private key.

**Revision:** design revision section 3 defines
`S0-ED25519-STRICT-1`. It requires canonical decoding/re-encoding, nonidentity
order-`L` public key and `R`, `S < L`, plain Ed25519, and the uncofactored
equation. The profile is mandatory at anchor, every registry entry, every PoP,
the root registry signature, and every active section-4 artifact. Acceptance
rows ISO-K27 through ISO-K30 include the identity construction, small/mixed
order, cofactored-only, boundary-bypass, cache, and non-Boolean cases.

**Claim:** proposed blocking-finding closure; implementation/provider behavior
remains untested and closed.

### 2.2 `TRI-B02`: pre-activation PoP circularity

**Review finding:** PoP had to occur before registry assembly, while the only
signer request contract required a registry digest and active artifact scope.

**Revision:** design revision section 4 defines two disjoint non-root request
classes plus a separate root-only ceremony. A three-file context import binds
the complete commitment/challenge bytes before `preactivation-pop-v1` is
accepted at `pop-context-bound`; the two-file PoP request forbids a registry
digest and edge. The exact PoP preimage and raw result frame are republished.
The root receives one exact seven-file `root-registry-v1` package at
`key-generated`, signs without an activated-registry dependency, and cannot
sign a second candidate. Exact registry-binding and activation packages close
the one-way transition to `active`: a `pop-issued` appliance may validate the
inert candidate envelope, but only user activation grants ordinary authority.
Every import/request/ceremony also shares one powered-off, one-ISO lifecycle;
signing routes add exactly one new raw result medium, while imports add none.
All routes have mirrored anti-replay state. The bootstrap proof has its own
exclusive signature scope and grants no ordinary authority. ISO-K20/K25 and
ISO-K31 through ISO-K34 exercise package, media, state, replay, class, root, and
scope failures.

**Claim:** proposed blocking-finding closure; no PoP, key, media, registry, or
state transition was executed.

### 2.3 `TRI-M01`: signed invocation-descriptor authority

**Review finding:** no signer, key source, canonical preimage, domain, or
verification order existed for the claimed signed descriptor.

**Revision:** design revision section 5 removes the signature claim. The exact
`S0-INVOCATION-DESCRIPTOR-2` bytes are bound by the already declared TCB through
an exact host launch-admission record, complete ISO hash, content/route/policy
hashes, VM/media identities, and pre/post host/guest cross-checks. The
descriptor authority is `input-route-controller`, while the sole admission
authority is `control-host-preflight` under an exact pinned configuration and
capability. The route controller cannot approve launch. The
descriptor omits its own and whole-ISO digests to prevent self-reference. It is
not a signature-bearing artifact and does not add a registry signer or hidden
key. ISO-P16/P17, ISO-C14, ISO-R07/R22 cover substitution and authority errors.

**Claim:** proposed major-finding closure under the existing trusted-host
nonclaim; no launch path was implemented.

### 2.4 `TRI-M02`: invocation nonce uniqueness

**Review finding:** a second external nonce had no exact generation, encoding,
global duplicate rule, or relation to invocation ID.

**Revision:** design revision section 6 deletes the second nonce. The exact raw
32-byte `invocation_id` is the sole external uniqueness input and is atomically
reserved forever in a project-lifetime ledger before provisioning. Exact
reserved/bound/admission-frozen/boot-consumed/terminal event grammars bind
opaque event/object/authorization IDs, admission bytes, and the exact immutable
ISO object. An independently persisted monotonic witness detects restoration of
an older internally valid ledger; the concrete provider remains explicitly
unresolved and blocks implementation. Ceremony, signer-media, and invocation
ledgers are separate namespaces under that same witness-backed provider. The
invocation ID is
also the HKDF-SHA-256 salt for a precisely domain-separated 32-byte guest
invocation secret. Records containing a separate nonce or another external
value reject. ISO-P18/P19 and ISO-C13/C14 cover duplicate, derivation, and
cross-record mismatch cases.

**Claim:** proposed major-finding closure; the ledger, CSPRNG, and KDF remain
future implementation subjects.

## 3. Non-regression statement

The revision preserves the accepted v0.1 topology and claim boundaries:

- 32 rows, 40 positions, eight pairs, 21 experimental signer bindings plus one
  non-row root, and the exact 22-entry registry;
- 27 stores, 46 readers, 64 edges, split-edge and E49 ordering;
- disposable actor, persistent signer-appliance, offline-root, and
  stage-specific TCB identities;
- eight future executor units with concurrency at most three; and
- all external/signer/launch-ledger provider, inherited-signature,
  implementation, protected-material, E0, and S0 gates remain closed.

## 4. Exact next review target

A fresh reviewer must authenticate the v0.1 predecessor, its review, and all
v0.2 candidate files; reconstruct the effective composition; attack every
finding disposition and non-regression invariant; and return only an allowed
verdict.

No later gate opens from this author response. The next permissible gate after
the candidate is frozen is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN INDEPENDENT REVIEW OPEN`
