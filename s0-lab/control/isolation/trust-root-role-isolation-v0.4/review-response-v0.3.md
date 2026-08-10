# S0 v0.14 trust-root and role-isolation v0.4 review response v0.3

- `status`: author response candidate
- `responds_to_sha256`: `2146e197759d9d8b726ba1672ccc45028c8b233f2f0eac41b86dc3aa75f657d9`
- `gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION V0.4 BOUNDED DESIGN REVISION OPEN`
- `claim_kind`: proposed public-text repair only

## 1. Response limit

This response maps only `TRI2-M01` and `TRI2-m01` from the authenticated v0.3
independent rereview to the bounded v0.4 successor. It is author evidence, not
an independent finding closure, implementation result, cryptographic result,
or permission to advance a later gate.

The rereview's zero-blocking result and its conclusion that no third finding
exists are preserved as predecessor evidence. This response does not use that
conclusion as an answer key for a future reviewer.

## 2. `TRI2-M01` response

### Review finding

The v0.3 import schema retained the v0.2 grammar while adding a block beginning
with a second `result_media_id`. It did not fix insertion/replacement order or
the state fields for terminal records reached directly from `reserved` or
`admission-frozen`. Multiple bytes and hashes were possible.

### Bounded revision

The v0.4 design replaces v0.3 section 2.6 in full with one 31-line import-only
grammar. It has one schema value, one `result_media_id`, fixed field order,
strict ASCII/LF bytes, an exact event-hash preimage, separate global and route
chains, and a total lifecycle table.

The two formerly ambiguous records are now exact:

- terminal from `reserved`: completion ID, prior reserved ID, zero
  admission/media fields, zero frame hash, `outcome_class=none`, and
  `none -> none` state evidence;
- terminal from `admission-frozen`: completion ID, prior admission ID, exact
  frozen admission/media fields, zero frame hash, `outcome_class=none`, and
  `none -> none` state evidence.

Every post-pending classification also has an exact frame-hash and state tuple.
Signing-request and root-ceremony schemas remain unchanged.

### Author claim

Proposed closure of `TRI2-M01` at public-design-text level only. No parser,
ledger, witness, frame, medium, state transition, or hostile test was
implemented or executed.

## 3. `TRI2-m01` response

### Review finding

The v0.3 second literal pair did not follow its asserted `y1 = p - y0`
derivation. The failure appears before the sign bit and cannot be repaired by
changing that bit.

### Bounded revision

v0.4 does not guess which coordinate or literal was intended. It withdraws the
v0.3 coordinates, complement relation, and all four `TRI2-VEC-01` rows from
effective authority. RFC 9381 remains absent as a claimed source, and the full
inherited `S0-ED25519-STRICT-1` profile remains unchanged.

The acceptance plan now fails closed before key generation until a separately
opened public vector-authoring gate freezes a new `TRI2-VEC-02` package and
independent evidence proves exact derivation, canonical decode/re-encode,
nonidentity, `[8]`, `[4]`, `[L]`, and strict rejection for four distinct rows.
The old literals cannot be used as fallback evidence.

### Author claim

Proposed closure of the authoritative public-text inconsistency by withdrawal
and explicit blocking, not by claiming a corrected cryptographic vector. The
availability or order of any replacement point remains unvalidated and the
future vector requirement remains closed.

## 4. Non-regression and next boundary

The v0.4 package preserves every frozen topology count, signature scope,
ledger namespace, A-D opportunity, provider blocker, and implementation,
protected-material, E0, and S0 nonclaim.

After all v0.4 files and sidecars are frozen, a fresh reviewer must
independently reconstruct the complete import grammar and decide whether
withdrawal plus fail-closed deferral is a safe repair rather than trusting this
response. A zero-finding verdict may permit only separate CONTROL integration
consideration. No implementation, vector-authoring, key-generation, E0, S0,
or `main` gate opens from this response.
