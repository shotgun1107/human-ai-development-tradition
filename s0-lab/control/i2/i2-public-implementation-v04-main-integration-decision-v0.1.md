# S0 v0.14 I2 public implementation v0.4 MAIN integration decision v0.1

- `decided_at`: `2026-08-12T11:05:54.0565701+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 MAIN INTEGRATION DECISION OPEN`
- `source_branch`: `codex/s0-trust-root-role-isolation-public-implementation-v04-main-integration-decision`
- `observed_origin_main`: `aa68f797ff4be1175048d8329f98d3c469dfb904`
- `observed_origin_main_tree`: `0525d314a37a2b6eaab1a9f4c22d37d87bc35abb`
- `approved_lineage_tip`: `72b75d05927638a6c473235e898b2de7285bf778`
- `approved_lineage_tree`: `08da416ea2405cb94f8f96389bbf305b8822a102`
- `reviewed_candidate_commit`: `cfb532f72a1434095e2a7af754e9f7c414e3b888`
- `reviewed_candidate_tree`: `1aadf50b88c7c6fa1de56f6582739dc65e6f1a43`
- `decision`: `APPROVE-MAIN-INTEGRATION-BY-EXACT-FAST-FORWARD-ONLY`
- `claim_kind`: Git lineage integration authorization only

## 1. Decision

CONTROL approves the authenticated I2 public implementation v0.4 lineage for
later integration into `main` by one exact fast-forward operation only.

This is a main-integration decision, not the main-changing operation. It does
not alter `main`, create a merge commit, rebase history, force-push, open a PR,
or start implementation, provider/model, E0, or S0 work.

The approved content lineage ends at CONTROL integration commit
`72b75d05927638a6c473235e898b2de7285bf778`. This decision Markdown and its
sidecar must first be frozen as the only two changes in a direct child commit
of that tip. Only that future exact decision child may be considered as the
fast-forward target under a separately opened execution gate.

## 2. Live main and ancestry evidence

Immediately before this decision, CONTROL fetched `origin/main` directly and
observed:

| Item | Exact value |
|---|---|
| `origin/main` | `aa68f797ff4be1175048d8329f98d3c469dfb904` |
| `origin/main` tree | `0525d314a37a2b6eaab1a9f4c22d37d87bc35abb` |
| approved lineage tip | `72b75d05927638a6c473235e898b2de7285bf778` |
| approved lineage tree | `08da416ea2405cb94f8f96389bbf305b8822a102` |
| merge base | `aa68f797ff4be1175048d8329f98d3c469dfb904` |
| main-only commits | `0` |
| lineage-only commits | `7` |
| merge commits in lineage | `0` |
| changed paths | `26` |
| changed paths outside approved public prefixes | `0` |

`origin/main` is therefore the exact ancestor of the approved lineage tip.
No merge, conflict resolution, cherry-pick, or rebase is required to integrate
the current lineage. The only permitted topology is a fast-forward from the
still-exact observed main to the future exact decision-child tip.

If `origin/main` changes before execution, this decision does not authorize
an automatic merge or reinterpretation. CONTROL must fetch the new live ref,
recompute ancestry and scope, and obtain a new decision or explicit amendment.

## 3. Exact seven-commit content lineage

The current fast-forward candidate is the following linear sequence after the
observed `origin/main`:

1. `5dc29a6fd1cfebb18c815afc67e34964233d5e58` — public I2 v0.2 candidate;
2. `01a1430d29d3c87e9448d9370a404e60371f721d` — v0.2 independent review;
3. `be1d56c0f98dba97919f294c253fc1d8368ef623` — bounded v0.3 revision;
4. `5e374933a80fd89afb85649c83353317d40581ec` — v0.3 independent review;
5. `cfb532f72a1434095e2a7af754e9f7c414e3b888` — bounded v0.4 revision;
6. `66afb460cc6a166872bf3936a459cd4b9ab05ee4` — zero-finding v0.4 independent review;
7. `72b75d05927638a6c473235e898b2de7285bf778` — v0.4 CONTROL integration decision.

The failed or revised predecessor candidates and their reviews remain visible
as history. Integrating the lineage does not rewrite them as successful
versions. The effective approved public implementation candidate is v0.4 at
`cfb532f72a1434095e2a7af754e9f7c414e3b888`, interpreted with its independent
review and CONTROL integration decision.

## 4. Authenticated implementation and review evidence

| Evidence | SHA-256 |
|---|---|
| implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` |
| implementation-manifest anchor file | `82d0167eaa8bde75b58f5c3bf116de1a91e555f16e7de85444f3eaf6736df00c` |
| v0.4 public contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |
| v0.4 independent review | `2a7dec6bbbece90ce8da151ead4ce19a64e857e33530729b6983646b68b9693f` |
| v0.4 independent-review sidecar file | `0451ea3300dd8f074ced192e351bd37d54dcd7594f1b5308f673d29dac2cf0df` |
| v0.4 CONTROL integration decision | `7c150fd516a019dc040f2ea83197ae76f4d17db9af23bb9f4dd00a0823f25919` |
| CONTROL-decision sidecar file | `75b604fd5a235fdc491f7ce2c141b7d418bf64caf6e8cfe016c4e0ba16bf152e` |

The canonical validator SelfTest passed all 11 cases in this decision
worktree. The v0.4 independent-review pair and CONTROL-integration-decision
pair passed every independently labelled text and sidecar check.

The accepted independent implementation verdict remains
`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY` with zero blocking, zero
major, and zero minor findings. The CONTROL integration decision remains
`APPROVE-PUBLIC-IMPLEMENTATION-INTEGRATION-ONLY`.

## 5. Integrated change scope and F0 preservation

The 26 paths changed between the observed main and approved lineage tip are
all confined to these explicit public prefixes:

- `s0-lab/i2/**`;
- `s0-lab/reviews/i2/**`; and
- `s0-lab/control/i2/**`.

There are zero changed paths outside those prefixes. The future decision-child
commit may add only this Markdown and its same-basename sidecar under
`s0-lab/control/i2/**`.

At both the observed main and approved lineage tip, the three PUBLIC-GIT / AI-
CONTENT-DEFAULT-DENY F0 aggregate inventories are exactly 32, 11, and 10. The
three main-to-tip quiet-diff exit codes are all zero. No F0 filename, content,
answer, oracle information, or internal structure was used in this decision.

The later fast-forward gate must recheck the exact target tree's 32/11/10
counts and require a quiet F0 diff from its direct parent before any push.

## 6. Required fail-closed execution conditions

A later main-changing action is allowed only if every condition below holds:

1. this decision pair is canonical, committed, and published as the only two
   changes in one direct child of
   `72b75d05927638a6c473235e898b2de7285bf778`;
2. the exact child commit and tree are pinned before any main-changing action;
3. a fresh fetch shows `origin/main` is still exactly
   `aa68f797ff4be1175048d8329f98d3c469dfb904`;
4. `origin/main` is an ancestor of the exact pinned target and has zero
   main-only commits;
5. the target contains no merge commit, unapproved path, or worktree change;
6. target F0 counts are 32/11/10 and its direct-parent F0 diff is quiet;
7. local and remote control-decision tips agree;
8. the user separately opens the exact fast-forward execution gate; and
9. the push uses ordinary fast-forward semantics, never force or lease-based
   history replacement.

Any mismatch, moving ref, dirty state, unexpected path, failed query, nonzero
F0 diff, or ancestry change cancels this authorization. Do not repair it with
reset, rebase, cherry-pick, merge, force-push, or filename-bearing diagnosis.

## 7. Closed gates and claim limits

Main integration changes only repository lineage. It does not validate or
open:

- actual trust-root or operational role isolation;
- key generation, private-key custody, signature or curve operations, anchor,
  registry activation, rotation, or revocation;
- exact admission or outcome grammars absent from the public source set,
  complete outcome classification, project-lifetime uniqueness, atomic
  append, durable ledger, or witness;
- VM, sandbox, account, ACL, network, clipboard, Git, vault, appliance,
  provider, or platform enforcement;
- protected material, hidden oracle, fixture, executor, judge, scoring, or
  statistics;
- provider or model sessions, E0, S0, central-system implementation, Project
  Brain integration, operational safety, economic value, production
  readiness, or model-to-model transfer.

No such work was executed for this decision.

## 8. Exact next gate

This decision does not alter `main` and does not open another gate
automatically. After this decision pair is frozen and published on its exact
child commit, the maximum next gate the user may separately open is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 MAIN FAST-FORWARD OPEN`

That gate may perform only the exact fast-forward authorized above and must
report the final remote main commit, tree, ancestry, clean state, and preserved
F0 aggregates.

## 9. Maximum claim

The maximum supported claim is that the authenticated public I2 v0.4
implementation, review, and CONTROL-decision lineage is currently a clean
linear descendant of the observed `origin/main`, has no identified scope or
F0-preservation conflict, and is approved for a later exact fast-forward after
this decision pair is frozen and the execution gate is separately opened.

No operational, cryptographic, provider/model, E0, S0, central-system,
Project Brain, safety, economic, production, or transfer result follows.
