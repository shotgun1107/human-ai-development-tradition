# S0 v0.14 I2 public implementation v0.2 independent review v0.1

- `review_date`: `2026-08-11 KST`
- `review_role`: fresh independent PUBLIC-ONLY implementation reviewer
- `candidate_branch`: `codex/s0-trust-root-role-isolation-public-implementation-v02-review`
- `candidate_head`: `5dc29a6fd1cfebb18c815afc67e34964233d5e58`
- `candidate_remote_tracking_ref`: `refs/remotes/origin/codex/s0-trust-root-role-isolation-public-implementation-v02`
- `candidate_remote_tracking_sha`: `5dc29a6fd1cfebb18c815afc67e34964233d5e58`
- `implementation_manifest_sha256`: `9bd5d96951344d7d431e905479a35f1dc5aa1856812847b59c42ff60ad2831d6`
- `contract_sha256`: `447b56c39f16c37272edd527d44e06328b5245a51dc8e83bc17a931cad26b2a8`
- `verdict`: `REVISE-AND-REVIEW`
- `claim_kind`: bounded public implementation-construction review only

## 1. Verdict and finding count

The candidate requires revision and a fresh independent review.

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 2 |
| minor | 0 |

The two major findings are confined to supplied-set structural validation. This
review does not claim that S0, E0, a trust root, role isolation, cryptographic
operations, a ledger or witness, provider or platform enforcement, the central
system, Project Brain, operational safety, economic value, production
readiness, or model-to-model transfer has been implemented or validated.

## 2. Review validity and authenticated boundary

Before substantive reading, the review independently established all of the
following:

- origin was exactly
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- the current branch, HEAD, and candidate remote-tracking ref matched the
  values in the header;
- the dedicated review worktree was clean;
- the external implementation-manifest pin matched the complete-file SHA-256
  of `implementation-files.sha256`;
- `implementation-manifest.sha256` canonically corroborated that external pin;
- the canonical text validator `-SelfTest` passed all eleven cases; and
- the contract complete-file SHA-256 matched the expected external pin.

The review then authenticated 16 payload-manifest rows with zero missing files,
zero duplicate paths, and zero hash mismatches. The exact I2 namespace contained
18 files: those 16 payloads, the payload manifest, and its canonical anchor,
with zero extra or missing files. The public-source manifest contained the exact
12-row allowlist with zero missing files, duplicates, syntax errors, or hash
mismatches.

The reviewer reconstructed requirements from the authenticated v0.4 design,
CONTROL decision, identity/authority matrix, acceptance addendum, final
`TRI2-VEC-02` freeze decision, and I1 public runtime inputs before relying on
candidate README, report, tests, or implementation assertions. All admitted I2
files were then read in full. No hidden material, F0 default-deny content,
fixture, oracle, protected material, key, provider/model session, curve
arithmetic, E0 work, or S0 work was read, created, or executed.

## 3. Public requirements used for judgment

The authenticated public requirements material to the findings are:

1. `R`, `A`, `P`, and `C` are distinct, never-reused event IDs; an early
   terminal burns unused later IDs.
2. A route has exactly one permitted `R/A/P/C` path. There is no record after
   consumed or terminal, no replacement completion, and no retry.
3. Global event chaining and route-local event chaining are distinct and both
   mandatory at their declared validation boundaries.
4. Every supplied event must retain the route's immutable identity and
   preallocated bindings.
5. Invalid or ambiguous structural evidence fails closed; visibly reused IDs
   cannot be waived merely because project-lifetime durable authority remains a
   separately blocked boundary.
6. The machine-readable successor must preserve exact source/hash bindings and
   state its unsupported ledger, witness, provider, cryptographic, and complete
   outcome-classification boundaries accurately.

## 4. Findings

### I2-V02-M01 — major — repeated identical route identity admits contradictory terminal histories and reused completion IDs

`validate_supplied_route_set` keys ownership by `_route_identity`, but it rejects
an overlapping preallocated ID only when the prior identity is different. It
therefore deliberately permits the same route binding more than once. The
candidate test suite even treats a complete accepted route followed by an
early-terminal version of the same route as valid.

Relevant candidate evidence:

- `s0-lab/i2/implementation/s0_i2/lifecycle.py` lines 531-563 define the route
  identity and say identical binding repetition is permitted;
- lines 573-600 reject an ID only when `prior_identity != identity`; and
- `s0-lab/i2/tests/test_i2.py` lines 933-942 expect an accepted route and an
  early-terminal route with the same context to pass as two groups.

A fresh bounded counterexample supplied one valid accepted `R/A/P/C` history
and one valid `R/C` early-terminal history under the same immutable context.
The API returned both groups. Their completion event IDs were equal while one
completion claimed `state=consumed` and the other claimed `state=terminal`.

Observed result:

```text
COUNTEREXAMPLE_SAME_ROUTE_CONTRADICTORY_TERMINALS=ACCEPTED
GROUP_COUNT=2
COMPLETION_EVENT_ID_REUSE=true
TERMINAL_CLASSES=consumed,terminal
```

This is not an unavailable project-lifetime observation. Both conflicting
histories and the reused completion ID are already present in the supplied set.
Accepting them contradicts the public no-record-after-terminal, no replacement
completion, no retry, and never-reuse rules. It also makes the supplied-set API
return a structural pass for mutually impossible route histories.

Exact repair:

1. Reject a second occurrence of an immutable route identity in
   `validate_supplied_route_set`; do not treat a second history as a valid
   repeated binding.
2. Maintain one emitted-event-ID set across every group in the supplied set,
   in addition to the preallocated-ID ownership set.
3. Add hostile tests for identical duplicate histories, accepted-versus-early
   terminal histories, two different post-pending completions, and a second
   history after either consumed or terminal.
4. Update the contract, README, and verification report so the repaired
   supplied-set rule and the still-blocked project-lifetime boundary are stated
   separately.

### I2-V02-M02 — major — result-media collisions are checked only inside one route and escape supplied-set validation

The candidate rejects `result_media_id` when it equals one of the same route's
four preallocated event IDs. The aggregate supplied-set validator, however,
tracks only the four event IDs. It neither registers result-media IDs nor checks
them against identifiers owned by other supplied routes.

Relevant candidate evidence:

- `s0-lab/i2/implementation/s0_i2/lifecycle.py` lines 99-105 implement the
  same-route result-media/event-ID collision rule; and
- lines 588-600 add only `R/A/P/C` values to the supplied-set ownership map.

Two fresh bounded counterexamples passed:

```text
COUNTEREXAMPLE_RESULT_MEDIA_TO_OTHER_ROUTE_EVENT_ID=ACCEPTED
COLLISION=true
GROUP_COUNT=2
COUNTEREXAMPLE_DISTINCT_ROUTES_SAME_RESULT_MEDIA_ID=ACCEPTED
COLLISION=true
GROUP_COUNT=2
```

The first made route 1's `result_media_id` byte-equal route 2's reserved event
ID. The second assigned one result-media ID to two distinct route identities.
Each individual route remained canonical and the aggregate API accepted both
groups. Thus the candidate's collision rule changes according to which group
contains the same bytes, and the advertised supplied-scope collision checking
does not cover result-media ownership.

Exact repair:

1. Freeze the supplied-set identifier ownership rule in the public contract:
   each route owns one nonzero result-media ID and four nonzero preallocated
   event IDs.
2. In `validate_supplied_route_set`, register all five identifiers in one
   supplied-set ownership map and reject result/result and result/event
   collisions across distinct route identities, while M01 rejects repeated
   identities.
3. Add both counterexamples above, their reversed group order, and early-
   terminal variants to the hostile suite.
4. Update README/report scope language to name result-media collision handling
   explicitly and retain `project-lifetime-uniqueness` as blocked beyond the
   supplied set.

## 5. Tests and hostile review summary

### 5.1 Candidate verifier evidence

The shipped verifier was run from the dedicated review worktree with the
external manifest pin. It reported:

- 16 authenticated payload rows and the exact namespace;
- exact 12-row public-source authentication;
- authenticated temporary snapshot creation and rehash;
- Python `>=3.12,<4.0` with `-B -S -P` and the declared environment controls;
- 34 unit tests run, zero failures, errors, skips, expected failures, or
  unexpected successes;
- contract CLI pass and stdlib/snapshot-only implementation import audit pass;
- original/snapshot/public-source post-execution stability pass; and
- closed admission/outcome/classification, durable ledger/witness, and
  forbidden operational capabilities remaining `BLOCKED_NOT_EXECUTED`.

This output was treated as candidate evidence, not as the independent verdict.

### 5.2 Independent structural probes

The reviewer independently exercised:

- 39 valid single-event cases: three route classes times all 13 lifecycle
  variants;
- 30 complete route paths: three route classes times two early-terminal and
  eight post-pending completion paths;
- an interleaved eight-event global chain containing two independently valid
  route-local chains;
- exact 31-line ASCII/LF serialization, final-LF hashing, canonical and
  arbitrary-length decimal handling, and hostile byte-format rejections;
- source/destination, admission tuple, frame-hash sentinel, early-terminal,
  terminal, predecessor, and immutable-binding mutations;
- emitted and preallocated ID reuse in the candidate's declared supplied
  scopes;
- exact I1 manifest/JSON hashes, 22 registry roles, 21 non-root event signers,
  and root exclusion;
- exact four-row `TRI2-VEC-02` byte/order/hash binding without performing curve
  arithmetic;
- forged and corrupt public handles; and
- fail-closed admission, outcome, classification, ledger, witness, registry,
  provider/platform, cryptographic, model, E0, and S0 boundaries.

The module-private provenance marker was reachable by hostile same-process
introspection and could be used to construct an accepted handle. This is not an
additional finding because README and report explicitly and accurately state
that the handle is trusted same-process API discipline, not a security boundary.

### 5.3 Verifier construction review

Line-by-line review covered verifier bootstrap disclosure, exact-set logic,
the exact source allowlist, startup-hook exclusion, reparse/device rejection,
byte snapshotting, source and payload rehash, candidate execution from the
snapshot, post-checks, environment restoration, and cleanup. The verifier
accurately discloses that its own already-executing bootstrap cannot authenticate
itself. The observed run left zero residual `s0-i2-public-verify-*` snapshot
directories. No separate verifier finding was established for this exact
candidate.

The canonical validator also passed all seven admitted Markdown/sidecar pairs
to which it applied: the four v0.4 control/design/matrix/acceptance pairs, the
final vector-freeze pair, candidate README, and candidate verification report.

## 6. Claim audit and next boundary

The contract, README, and report correctly keep complete outcome semantics,
durable ledger/witness authority, project-lifetime authority, cryptographic
operations, process/VM isolation, provider/model work, E0, and S0 blocked. Their
same-process handle limitation and verifier bootstrap limitation are also
accurately disclosed.

Those accurate limitations do not close M01 or M02: both counterexamples are
fully visible in the exact caller-supplied set that the candidate does validate.

The maximum supported result of this review is therefore
`REVISE-AND-REVIEW` for the bounded public implementation-construction
candidate. Repairing these findings permits only a fresh public-only independent
implementation review. It does not open any operational, cryptographic,
provider/model, protected-material, E0, S0, central-system, Project Brain,
production, economic, transfer, merge, or release gate.

## 7. Authorized review outputs

This review owns only:

- `s0-lab/reviews/i2/i2-public-implementation-v02-independent-review-v0.1.md`
- `s0-lab/reviews/i2/i2-public-implementation-v02-independent-review-v0.1.sha256`
