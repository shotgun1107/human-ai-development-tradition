# S0 v0.14 role-isolation acceptance-plan addendum v0.3

- `status`: design revision candidate
- `design_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION DESIGN REVISION OPEN`
- `predecessor_plan_sha256`: `534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1`
- `responds_to_review_sha256`: `67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990`
- `claim_kind`: public tabletop acceptance design only

## 1. Effective plan and row inventory

This addendum composes with the authenticated v0.1 acceptance plan and v0.2
addendum. It changes only the import-outcome evidence and the exact vector-
provenance requirement needed to answer `TRI2-M01` and `TRI2-m01`. It executes
no test and contains no key, VM, fixture, protected input, provider session,
model output, or acceptance result.

No row is added or removed. The effective inventory remains 107 rows:

- platform: ISO-P01 through ISO-P19, 19 rows;
- channels: ISO-C01 through ISO-C14, 14 rows;
- media/routes: ISO-R01 through ISO-R22, 22 rows;
- independence: ISO-I01 through ISO-I08, eight rows;
- trust/signer: ISO-K01 through ISO-K34, 34 rows; and
- lifecycle: ISO-L01 through ISO-L10, ten rows.

Every row remains noncompensatory. One failure, skip, waiver, ambiguous result,
missing record, substituted test, or unbounded operator judgment fails the
candidate. The row mutations below replace only their v0.2 meanings; all other
v0.2 rows remain exact.

## 2. Required import-outcome evidence

For each of the three import classes, future implementation evidence must bind
one exact route from admission through cleanup:

| Evidence group | Mandatory evidence |
|---|---|
| route identity | campaign, ceremony, signer, import class, exact from/to states, package SHA-256, package object ID, and one-use attachment capability |
| preallocated identity | nonzero `result_media_id` plus distinct reserved, admission-frozen, pending, and completion signer-media event IDs |
| admission | exact `S0-SIGNER-IMPORT-ADMISSION-2` bytes and SHA-256, `result_media_kind=import-outcome-v1`, immutable ISO identity/hash, fresh exactly 2,048-byte raw outcome-medium identity, zero-initial state, and powered-off attachment evidence |
| target decision | complete `S0-SIGNER-IMPORT-OUTCOME-1` frame bytes when one valid frame exists, body hash, complete-frame hash, before/after states and configuration-state hashes, decision, and reason |
| host observation | controlled stop evidence, both-media detachment before raw reading, full 2,048-byte observation, frame count, zero remainder, and the fixed final classification |
| ledger and witness | exact reserved, admission-frozen, pending, and consumed-or-terminal records; prior-event chain; capability use; outcome hash/class; before/after appliance states; ledger head; witness head |
| persistence and cleanup | durable completion evidence before destruction, retained bounded failure evidence, ISO/outcome-medium cleanup, and no cryptographic-erasure claim |

Evidence from one signer, import class, package, campaign, route attempt, event
chain, capability, or medium in another route is a failure. A normal shutdown,
detachment, zero medium, missing error, or target state observed without the
exact frame and ledger agreement is never accepted evidence.

The exact state mapping is:

| Import class | Before | Accepted after |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

## 3. Exact v0.2 row replacements

### 3.1 `ISO-K20`: route state and completion authority

| Existing ID | Effective v0.3 mutation or observation | Required result |
|---|---|---|
| ISO-K20 | A signing request crosses class/state; an import starts in the wrong state; an import has no fresh nonzero outcome medium; any admission, event, frame, state, capability, object, or host binding differs; a non-accepted outcome is treated as consumed; a pending/crashed route is retried; or ledger/witness evidence is unavailable, restored, or inconsistent | Reject without signature or authorized state advance. Only one exact state-consistent `accepted` frame plus agreeing host evidence may append `consumed/accepted`; every other post-pending import outcome requires `terminal/rejected` when the exact append remains possible, invalidates the candidate, spends the route, and forbids retry. An append conflict creates no substitute completion |

### 3.2 `ISO-K25`: medium lifecycle

| Existing ID | Effective v0.3 mutation or observation | Required result |
|---|---|---|
| ISO-K25 | Any non-root/root route uses non-finalized, shared, network, PowerShell-Direct, hot-attached, simultaneous, stale, prior, or wrong media; an import outcome medium is missing, reused, zero-ID, nonzero initially, not exactly 2,048 bytes, partitioned, formatted, mounted, read before shutdown/detachment, writable by the host after attachment, contains more than one frame or a nonzero tail, or is destroyed before completion evidence persists; or any request/result medium, shutdown, detachment, destruction, pagefile, hibernation, crash-dump, command-line, or payload-log constraint from v0.2 is violated | Reject appliance configuration or transition. If the attempt reached `pending`, append the one preallocated terminal event when possible, invalidate the candidate, and do not replace or retry the medium |

### 3.3 `ISO-K28`: exact negative-vector reproducibility

| Existing ID | Effective v0.3 mutation or observation | Required result |
|---|---|---|
| ISO-K28 | The implementation does not independently reproduce all four literal `TRI2-VEC-01` encodings from the stated `p`, `y0`, `p-y0`, little-endian rule, and sign bit; any byte is different; canonical decoding/re-encoding differs; `[8]P != I`; `[4]P = I`; `[L]P = I`; or the strict profile admits any of the four as `A` or `R` | Reject the implementation/profile before key generation. Require exact construction and order evidence and exact Boolean rejection for every literal encoding; a copied label or RFC 9381 attribution is not evidence |

### 3.4 `ISO-K31`: parser decision observability

| Existing ID | Effective v0.3 mutation or observation | Required result |
|---|---|---|
| ISO-K31 | A context, registry-binding, or activation ISO/package/record violates its exact file, grammar, manifest, capability, key, object, hash, admission, or state binding; the target reports acceptance; rejection changes state; a valid rejection frame is absent after a normal target rejection; or the host infers success or a particular rejection from shutdown alone | Exact valid package may continue. An internally detected parse failure must yield `rejected/parse-rejected` with unchanged state; a later semantic/hash/state failure must yield `rejected/validation-rejected` with unchanged state. Missing, malformed, conflicting, or noncanonical outcome evidence becomes host `missing` or `disagreement`, never success |

### 3.5 `ISO-K33`: transition and outcome agreement

| Existing ID | Effective v0.3 mutation or observation | Required result |
|---|---|---|
| ISO-K33 | Any inherited transcript, registry, strict-proof, root-package, registry-binding, activation-package, import-admission, or appliance-entry condition differs; an accepted frame lacks the exact durable destination state; a rejection frame follows a state advance; state-commit failure claims a known destination; host and appliance disagree; inert validation is treated as active authority; or activation is demanded before candidate validation | Reject registry-signed, registry-bound, active, or other intended transition. Classify exact state-commit uncertainty as `state-commit-failed`; every post-pending mismatch as `disagreement`; append terminal evidence when the exact completion remains possible and otherwise claim no completion; invalidate the candidate without retry or premature authority use |

## 4. Stage boundary and final-classification decision table

A defect detected before `pending` follows the inherited admission lifecycle,
has no import-outcome classification, and terminates from the last durable
event when the preallocated completion ID and ledger/witness are usable. A
preallocation collision or unavailable ledger/witness permits no new terminal
append and fails on the existing conflict evidence.

The eight-class table applies only after `pending`. Its `terminal/rejected`
cells state the required logical completion. The event is appended only when
the preallocated completion ID is unused and the ledger/witness accepts the
exact append. A completion-ID/event collision or append failure creates no
replacement event or completion claim; the already observed outcome
classification remains bounded failure evidence. The conflict independently
invalidates the candidate and forbids retry.

The host applies the main revision's precedence. Each future case must produce
one and only one result:

| Classification | Minimum observable condition | Completion and authority |
|---|---|---|
| `crash` | abnormal process, appliance, watchdog, or shutdown evidence, regardless of apparent frame bytes | `terminal/rejected`; ignore apparent frame; destination unavailable |
| `missing` | normal shutdown but no complete frame or an all-zero medium | `terminal/rejected`; destination unavailable |
| `duplicate` | more than one outcome medium, more than one frame/magic value, or any nonzero byte after the one canonical final LF | `terminal/rejected`; select neither frame |
| `disagreement` | malformed/oversized frame, bad body hash, wrong or replayed binding, invalid decision/state/hash combination, host/appliance conflict, or anti-replay conflict | `terminal/rejected`; prefer neither side |
| `parse-rejected` | one valid `rejected/parse-rejected` frame with unchanged source state and matching hashes | `terminal/rejected`; retain rejection evidence |
| `validation-rejected` | one valid `rejected/validation-rejected` frame with unchanged source state and matching hashes | `terminal/rejected`; retain rejection evidence |
| `state-commit-failed` | one valid failure frame with indeterminate after-state and zero after-configuration hash | `terminal/rejected`; invalidate candidate |
| `accepted` | one valid `accepted/none` frame, durable exact destination state, nonzero unequal configuration hashes, and full host/ledger/witness agreement | `consumed/accepted`; exact destination alone becomes available |

If the completion event or witness cannot be durably appended, no accepted
result exists even when the target may have changed state. Unknown, partial,
or multiply matching classification is `disagreement` and fails closed.

## 5. Mandatory future hostile traces

A fresh reviewer must trace the design on paper, and a later implementation
gate must exercise the effective rows, for at least:

1. one exact accepted outcome for each of the three import classes;
2. parse rejection, validation rejection, and state-commit failure for every
   applicable class;
3. crash before persistence, after persistence but before frame completion,
   after frame completion but before shutdown, and before host completion
   persistence;
4. empty, partial, truncated, oversized, reordered, extra-field, bad-hash,
   nonzero-tail, and two-frame outcome media;
5. wrong campaign, ceremony, signer, class, source/destination state, package,
   object, capability, admission hash, result-medium ID, or any event ID;
6. cross-signer, cross-class, cross-package, cross-campaign, replayed,
   duplicated, or selectively retried evidence;
7. accepted frame with unchanged/wrong state, rejection with advanced state,
   and host/appliance disagreement;
8. cleanup before evidence persistence, stale medium attached later, mounted or
   filesystem medium, and private/protected bytes in outcome evidence;
9. treating the unsigned frame or TCB service as a signature, signer, key,
   registry authority, experimental role, store, reader, edge, or fourth
   ledger namespace; and
10. all four exact `TRI2-VEC-01` bytes, swapped endianness/sign handling,
    noncanonical decoding, wrong point order, copied-label acceptance, and the
    removed RFC 9381 attribution.

Each mutation must map to one exact observable classification and row result.
An unobservable, ambiguous, waived, retried, or operator-selected result is a
failure.

## 6. Non-regression evidence

The future reviewer must independently confirm that the v0.3 replacements do
not alter:

- 32 aggregated role rows, 40 positions, eight paired rows, 21 experimental
  signers, 19 `none` positions, one non-row root, or 22 registry IDs;
- 27 stores, 46 explicit readers, or 64 edge rows;
- the three exclusive signature scopes or three ledger namespaces;
- A-D source information, authority, model condition, time, output, or scoring
  opportunity;
- the eight executor invocation/session units or concurrency maximum three;
  or
- any provider, implementation, protected-material, E0, or S0 blocker.

The outcome medium, service, frame, and events must remain TCB control objects
outside the experimental topology. Any count or authority drift fails the
candidate.

## 7. Acceptance and gate rule

At design-review time, the candidate can earn only a finding disposition about
whether these rules are complete and internally consistent. It cannot earn an
implementation pass.

A future implementation candidate passes isolation review only when all 107
effective rows return their exact outcomes on one frozen implementation and
configuration, every required record is authenticated, and a fresh independent
review reports zero findings. Even that result would permit only separate
CONTROL integration consideration.

This addendum does not open or authorize implementation, a helper or validator,
VM or media provisioning, key generation, vector execution, protected
material, fixture, oracle, executor, provider or model session, judge handoff,
scoring, E0, or S0 execution.
