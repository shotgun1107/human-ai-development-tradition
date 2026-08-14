# Public end-to-end assembly runtime profile and neutral preloader bounded integration acceptance plan v0.2

Status: design-level acceptance obligations; no implementation or execution

## 1. Purpose and threshold

This plan defines the evidence required to accept or reject the v0.2 bounded
integration design revision. It does not accept an implementation and does not
authorize runtime materialization, native execution, a platform probe, or a
public assembly rehearsal.

Design PASS requires exact package authentication, zero unresolved BLOCKING,
zero unresolved MAJOR, explicit disposition of any MINOR, preservation of the
current live fail-close, and independent closure of both v0.1 MAJOR findings.

## 2. Package authentication

The independent reviewer must reject before semantic judgment if:

- the CONTROL-supplied exact branch, commit, tree, sole parent, upstream, or
  live remote tip does not reproduce;
- the package manifest is not canonical, ASCII-sorted, unique, and exactly six
  logical rows;
- any logical artifact hash differs from its manifest row or sidecar;
- any Markdown pair fails the canonical validator after validator SelfTest;
- either JSON artifact fails strict duplicate-key-rejecting parsing;
- the interface map fails its exact Draft 2020-12 schema;
- any predecessor pin fails;
- the worktree, index, or admitted status is not clean; or
- the reviewer reads outside the exact allowlist or accesses F0 content.

F0 checking is aggregate-only and must reproduce `32 / 11 / 10` with zero
worktree, index, untracked, ignored, skip-worktree, or assume-unchanged
anomalies.

## 3. Required reconstruction

The reviewer must independently establish:

1. the current assembly implementation remains diagnostic and path-based;
2. the current live entry remains unconditionally fail-closed;
3. the offline assembly bridge remains candidate-only and native-unreachable;
4. effective runtime/preloader v0.3 assigns sole root creation and continuous
   original-handle retention to the authenticated native preloader;
5. v0.4 retains that atomic-root design and exact five-handle policy;
6. assembly child `COMPLETE` remains diagnostic-only under effective assembly
   v0.5; and
7. runtime-admission `SPENT`/`REJECTED` and the private live consumer remain
   the terminal authority boundary.

Any contrary fact is at least MAJOR.

## 4. `ARPNP-INT-RR-001` closure matrix

| Proposition | Required v0.2 rule | Reject if |
|---|---|---|
| One root creator | Authenticated native preloader only | CONTROL, verifier parent, candidate, callback, or fallback can create/open the leaf |
| Path is nonauthority | CONTROL supplies authenticated parent/leaf intent only | A path or serialized identity substitutes for a retained live handle |
| Correct order | `PRELOADER-STARTED` precedes `ROOT-CREATED-HELD` | Root reservation or creation is claimed before preloader start |
| Sole transaction | One direct authenticated `NtCreateFile` with effective ABI and `FILE_CREATE` | Reopen, second create, alternate API, alias retry, or cleanup-and-retry exists |
| Original continuity | Returned original remains open through verifier termination and final recheck | Close/reopen or path rediscovery replaces it |
| Exact verifier authority | Only the reduced same-object duplicate occupies handle position four | Wrong access, role, identity, object, order, or original-handle inheritance is admitted |
| Post-create routing | Any later failure preserves quarantined-root semantics | Later absence or cleanup relabels the run as clean or successful |

The reviewer must reject any purported parent-to-preloader root-handle handoff:
v0.2 intentionally has none.

## 5. `ARPNP-INT-RR-002` closure matrix

The reviewer must confirm that the outer machine:

- has no generic `TERMINAL`;
- names `LIVE-CONSUMED` and `REJECTED` as its only live terminals;
- binds root creation to preloader `ROOT-CREATED-HELD`;
- binds verifier resume to preloader `VERIFIER-LAUNCHED`;
- binds guard success to runtime admission `ROOT-CREATED-BOUND` before Python
  import;
- requires the exact ten-state child traversal;
- distinguishes private witness issuance from child `COMPLETE`;
- requires child `COMPLETE` and the unused witness before `COMMITTING`;
- requires exact preloader recheck and reply before `COMMIT-ACKED`;
- permits `LIVE-CONSUMED` only when the same-process consumer advances the
  admission to `SPENT` and consumes the witness; and
- maps every nested failure, invalid transition, timeout, interruption, or
  consumer rejection to immutable outer `REJECTED`.

The schema and map must reject a skipped state, a reordered predicate, a
premature terminal, or a positive terminal lacking any required nested state.

## 6. Terminal authority review

The following must each remain insufficient for live acceptance:

- outer nonterminal or terminal state text;
- child `COMPLETE` or a controller result;
- publication files, record, receipt, hashes, or observer trace;
- private witness without current files and `COMMIT-ACKED` admission;
- preloader `OK`, `COMMIT-REPLIED`, process exit, or job accounting;
- admission `COMMIT-ACKED` without the consumer's first terminal attempt;
- copied, serialized, prior-run, or reconstructed evidence; and
- any offline diagnostic or offline plan.

`LIVE-CONSUMED` requires the exact current-process conjunction frozen by the
design. Even then it is bounded live-consumer acceptance only, not official
rehearsal PASS or S0.

## 7. Required later implementation mutations

A later implementation candidate must deterministically reject at least:

1. CONTROL, verifier parent, or candidate root creation;
2. root create before preloader start or before complete authentication;
3. path reopen, second create, alternate API, case alias, reparse, or
   post-check root substitution;
4. original handle early close or original inheritance;
5. verifier duplicate wrong access, role, order, identity, or object;
6. admission bind before resume or after Python import;
7. any child-state skip, repeat, reorder, or fabricated `COMPLETE`;
8. missing, early, copied, reused, or misbound publication witness;
9. commit before witness plus authenticated child completion;
10. malformed, missing, duplicate, early, or authority-upgraded preloader
    reply;
11. missing, rejected, retried, stale, or copied consumer input;
12. premature `LIVE-CONSUMED`, generic terminal, or success from process exit;
13. offline-to-live promotion; and
14. retry reuse of any nonce, root, process, pipe, handle, admission, witness,
    snapshot, or authority.

Each mutation must fail before the affected action or authority consumption.
Passing only the happy path is insufficient.

## 8. Nonregression review

The reviewer must also confirm that v0.2 does not weaken:

- the exact offline bridge and forbidden authority surfaces;
- the two deferred RPNP MINOR dispositions;
- closed manifest, build, runtime, binary, import, and platform evidence
  ownership;
- the exact five-handle `CreateProcessW` contract and process-wide absence
  nonclaim;
- assembly publication, witness, receipt, and same-process consumer rules;
- failure routing and quarantine precedence; or
- the required later gate order.

## 9. Required independent verdict

The fresh reviewer must return exactly one of:

- `PASS-FOR-BOUNDED-ASSEMBLY-RUNTIME-PRELOADER-INTEGRATION-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `RETURN-TO-INTEGRATION-DESIGN-REVISION`; or
- `INVALID-REVIEW` after an authentication or role-boundary failure.

PASS requires zero BLOCKING and zero MAJOR findings. It permits only separate
implementation consideration. It does not open that gate, authorize Git
publication, materialize a runtime, call a native API, run a platform probe or
rehearsal, access F0 or an oracle, or establish S0 or production acceptance.
