# S0 v0.14 public assembly runtime/preloader bounded integration implementation v0.1 CONTROL integration and main merge decision

- `status`: CONTROL integration and main fast-forward decision
- `decided_at`: `2026-08-14T21:27:33.2119584+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL RUNTIME PROFILE + NEUTRAL PRELOADER BOUNDED INTEGRATION IMPLEMENTATION V0.1 CONTROL INTEGRATION AND MAIN MERGE OPEN`
- `decision_worktree_branch`: `codex/s0-assembly-rpnp-integration-v01-control`
- `decision_input_branch`: `codex/s0-assembly-rpnp-integration-implementation-v01-minor-rereview`
- `decision_input_commit`: `eff8ed57107e93721a0b9b1342f408f42a316501`
- `decision_input_tree`: `dce58dc299f5907ef57313ab4274cb9e2df3c249`
- `observed_origin_main`: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- `observed_origin_main_tree`: `a14e8b9c9bc8905060cd8811e8934643e2aa4aa3`
- `decision`: `APPROVE-AND-EXECUTE-MAIN-FAST-FORWARD-ONLY`
- `main_merge_mode`: `fast-forward-only`
- `main_merge_status_at_record_creation`: `pending exact Git operation in this gate`
- `F0_content_access`: none

## 1. CONTROL decision

CONTROL accepts the authenticated bounded PUBLIC offline integration
implementation candidate, its independent review, the exact-byte minor
revision, and its zero-finding fresh minor rereview for main integration.

This gate authorizes exactly this sequence:

1. commit this decision Markdown and its same-basename SHA-256 sidecar as the
   sole direct-child change of the authenticated decision input;
2. reauthenticate the resulting source tip, live `origin/main`, complete
   ancestry, exact path scope, clean state, and F0 preservation;
3. publish the decision source branch; and
4. advance `main` to that exact source tip by fast-forward only.

No merge commit, rebase, force push, reset, selective cherry-pick, history
rewrite, PR, release, tag, branch deletion, or source-file modification is
authorized.

## 2. Authenticated implementation and review evidence

| Artifact | SHA-256 | Result used by CONTROL |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current publication, F0 access, and claim boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | SelfTest PASS and exact public Markdown validation |
| bounded implementation manifest | `7469f62d67c9d5f416f38db7e4a14b5f3819e739cf38a71f1fec452421a7fabe` | exact three-row implementation/test closure |
| bounded verification manifest | `8f8140d678e5846639ff382b32035c342dc8b2dd7d929da5ff37a759f8aa9d7b` | exact four-row report/verifier closure |
| implementation candidate report | `945832688fc5ec043a8c8ec4902fe85f101efeb2a5aa3af40a46e7f2b2ecbddd` | bounded offline result and explicit nonclaims |
| first independent implementation review | `ddf5d4ade01c4d87a2e027d8487a9c5a34e317a3df3aee1e19d624492849dbc0` | one MINOR finding; no blocking or major finding |
| fresh minor rereview | `3adbdbb3a30457c7b9baae319e7e31b4def993c454e24182d4b3596a573d99aa` | `ARPNP-INT-IR-001` CLOSED; zero remaining findings |
| effective integration v0.2 design manifest | `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c` | exact bounded integration design authority |
| integration v0.2 design rereview preservation record | `947b2713a04291357be88be86f96d1a2d805058b0ec602c3b5f4812b00db308c` | predecessor design eligible for bounded implementation |

The bounded implementation and verification manifests contained exactly
three and four unique rows, respectively, and every listed target hash
matched. The candidate report, first independent review, and minor rereview
Markdown/sidecar pairs passed every canonical validator check.

The fresh minor rereview independently reproduced:

- exact candidate and predecessor manifest closure authentication;
- `6 / 6` focused tests;
- 24 hostile nonexact or mutated closure cases rejected before bridge use;
- exactly one bridge call on the authenticated happy path;
- snapshot-only verifier execution and pre/post source sentinel behavior;
- zero candidate native, process, network, or provider calls; and
- `candidate_only=true`, `native_api_reachable=false`, and
  `rehearsal_pass=false`.

CONTROL did not reinterpret those bounded results as live or rehearsal
evidence.

## 3. Exact accepted lineage

The implementation-specific lineage is linear:

```text
f16c68dbc6e28b2483eff7b940ebf890a1d26402
  -> e774cc04034c2c8f43b6357ac738fd7d86d2e18e
  -> edcebb6434cd1a86736fb612ee26b1b0ec7b1311
  -> eff8ed57107e93721a0b9b1342f408f42a316501
```

- `f16c68d` adds the bounded offline candidate;
- `e774cc0` adds the first independent review;
- `edcebb6` applies the exact-byte private-snapshot minor repair; and
- `eff8ed5` adds the zero-finding fresh minor rereview.

The live remote main is also a direct ancestor of the decision input. The
exact `origin/main...decision_input` left/right commit count is `0 / 22`.
There is no main-only commit and no omitted commit between the observed main
and accepted input.

## 4. Full main-to-input path disclosure

Fast-forward integrates the complete linear public preparation lineage, not
only the newest eight candidate files. Before this decision pair, the exact
main-to-input diff is 187 paths:

| Public path family | Paths |
|---|---:|
| assembly candidate/runtime v0.1 | 35 |
| bounded assembly integration candidate v0.2 | 8 |
| runtime/profile neutral-preloader implementations v0.1/v0.2/v0.3 | 14 / 14 / 14 |
| integration designs v0.1/v0.2 | 11 / 13 |
| runtime/profile neutral-preloader design/control v0.1/v0.2/v0.3/v0.4-input/v0.4 | 13 / 13 / 13 / 2 / 13 |
| dated public handoff records | 6 |
| assembly integration implementation reviews | 4 |
| runtime/preloader and integration design/implementation reviews | 14 |
| unexpected or unclassified paths | 0 |

The decision pair raises the expected final main diff to exactly 189 paths.
The dated handoff records remain historical public evidence and do not
override current `AGENTS.md`, current Git state, or the authenticated design,
implementation, and review records.

## 5. Finding disposition

The first independent review reported:

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 1 |

Its sole finding, `ARPNP-INT-IR-001`, showed that mutable target values could
pass the public input closure despite the exact-byte claim. The minor revision
requires exact `str` keys, exact `bytes` values, and a private immutable
mapping snapshot before hashing. The fresh minor rereview independently
rejected `bytearray`, `memoryview`, bytes subclasses, string subclasses,
changed/missing/extra values, and nonexact mapping containers across all three
closures before bridge use.

The final fresh rereview reported zero blocking, zero major, and zero minor
findings with verdict `PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`.

## 6. Accepted implementation status

Main integration establishes only that:

1. one bounded PUBLIC offline adapter calls the already authenticated
   `prepare_assembly_runtime_launch` bridge;
2. public implementation, design, and integration closures are authenticated
   before that bridge can produce a diagnostic;
3. verifier execution occurs from an authenticated temporary snapshot with a
   post-run original-input sentinel;
4. exact offline success and rejection traces are mechanically constrained;
5. no returned diagnostic grants live, native, rehearsal, provider, model,
   executor, judge, or S0 authority; and
6. the exact-byte closure defect found by the first review is closed in the
   fresh rereview.

This is a bounded public implementation candidate integrated as preparation
evidence. It is not a materialized runtime, trusted build, native preloader,
Windows platform result, official assembly rehearsal, or S0 result.

## 7. F0 preservation

The observed `origin/main` and decision input each contain exactly 32, 11,
and 10 tracked entries in the three PUBLIC-GIT F0 path families. Their quiet
main-to-input diff is zero. The accepted lineage and this decision pair do not
modify those path families.

No F0 filename or content was opened, searched, quoted, summarized, derived,
or used as an implementation or decision input. Their unchanged Git presence
is repository synchronization, not AI content authority.

## 8. Mandatory final fast-forward checks

Immediately before any branch publication or `main` update, CONTROL must
reproduce all of the following:

1. live `origin/main` is still exactly
   `41e0b684a7cca387be6d264c4a5b63de2561fd7c`;
2. the decision commit is the sole direct child of
   `eff8ed57107e93721a0b9b1342f408f42a316501` and adds only this Markdown and
   sidecar;
3. `origin/main` remains an ancestor of the final decision commit with zero
   main-only commits;
4. the final main diff is exactly 189 paths in the disclosed families with
   zero unexpected paths;
5. the implementation, review, and design hashes in section 2 remain exact;
6. both trees retain F0 counts `32 / 11 / 10` and their quiet F0 diff is zero;
7. the integration worktree and index are clean, the repository stash count is
   zero, and no unclassified local path participates; and
8. publication uses normal fast-forward pushes only, without force or history
   rewriting.

Any mismatch stops the main update. The current gate does not authorize
adapting this decision to another live main or another source tip.

## 9. Gates and claims that remain closed

This decision and main fast-forward do not authorize or establish:

- source/build/binary/import materialization or a trusted runtime package;
- native preloader, Windows API, handle, filesystem, process, VM, sandbox, or
  platform-probe behavior;
- output-root creation, live admission, witness consumption, or official
  assembly rehearsal PASS;
- F0 content access, hidden oracle, fixture, executor, judge, scoring,
  provider/model, S0, or E0 work;
- central-system or Project Brain implementation;
- operational safety, economic value, production readiness, or
  model-to-model transfer; or
- PR, release, tag, branch deletion, or any later technical gate.

Build-and-runtime materialization remains a separately gated future stage.
It is not opened by this document or by moving `main`.

## 10. Maximum claim

**Decision: `APPROVE-AND-EXECUTE-MAIN-FAST-FORWARD-ONLY`.**

After the exact fast-forward succeeds, main may claim only that the complete
authenticated public preparation lineage through the bounded offline
integration implementation v0.1 and its zero-finding minor rereview is
integrated. No live system, rehearsal, S0, operational, economic, production,
or transfer result follows.
