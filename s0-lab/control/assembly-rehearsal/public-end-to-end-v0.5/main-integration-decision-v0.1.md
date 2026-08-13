# S0 v0.14 public end-to-end assembly rehearsal design v0.5 main integration decision v0.1

- `status`: main integration decision
- `decision_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.5 MAIN INTEGRATION DECISION OPEN`
- `decided_at`: `2026-08-13T11:24:28.2154950+09:00`
- `decision_worktree_branch`: `codex/s0-public-assembly-rehearsal-design-v05-main-integration-decision`
- `decision_base`: `92b747cb314340dfc872b660aece5ed5c71896d4`
- `decision_base_tree`: `2cfe5966c3ee78bacbf2516177fff9a10e7d5705`
- `observed_origin_main`: `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`
- `observed_origin_main_tree`: `d1ed10e2e8e5e21a510322c002b69b9cf89de848`
- `decision`: `APPROVE-SEPARATE-MAIN-FAST-FORWARD-ONLY`
- `implementation_status`: closed
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Decision

The authenticated public assembly rehearsal design v0.5 lineage is approved
for a separately opened main fast-forward operation.

This decision does not move `main`. It establishes only that, at the observed
remote state, `origin/main` can advance linearly from
`402a4a0ef6ff60c00ddf84b5ea46fdc766f28984` to the future direct child of
`92b747cb314340dfc872b660aece5ed5c71896d4` that adds only this decision pair.
The later operation must use a fast-forward only, without a merge commit,
rebase, force, reset, deletion, or history rewrite.

## 2. Fast-forward proof at decision time

| Check | Result |
|---|---|
| `origin/main` | `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984` |
| reviewed CONTROL tip | `92b747cb314340dfc872b660aece5ed5c71896d4` |
| `origin/main...tip` left/right count | `0 / 15` |
| main is an ancestor of tip | yes |
| tip is already an ancestor of main | no |
| main-only commit | zero |
| changed paths before this decision pair | 77 |
| assembly control lineage | 53 |
| assembly review lineage | 10 |
| readiness historical record | 2 |
| dated handoff historical records | 12 |
| every other path | 0 |

The source branch published at the reviewed CONTROL tip resolves to the same
commit. No commit is omitted between the observed main and proposed tip.

The 12 dated handoff files and two readiness files are preserved explicitly
as historical public project records. Under current root policy they do not
override the v0.5 design, review, or CONTROL decision, and they are not
treated as implementation or runtime evidence. Their presence is disclosed
here because a fast-forward integrates the complete linear tree rather than
only the newest v0.5 files.

After this decision pair is committed as the sole direct-child change, the
expected final source diff is exactly 79 paths: 55 assembly-control, 10
assembly-review, two readiness, 12 dated handoff, and zero other paths.

## 3. Authenticated design and decision evidence

| Artifact | SHA-256 |
|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| v0.5 design-package manifest | `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802` |
| v0.5 design revision | `849e0655e7f73b78eeb039b09357c48f150c637f8cf527dec2a9990b9d240f5b` |
| v0.5 independent rereview | `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137` |
| v0.5 CONTROL integration decision | `957ccf01f2d9abe0e4c5d3c417f143c1106122a47f0942fcc5a598373ef69645` |

The canonical validator SelfTest passed before use. The decision-critical
Markdown pairs passed every canonical text and sidecar check. The five-row
v0.5 design manifest and every listed hash were authenticated in the prior
review and CONTROL gates.

The independent rereview reported zero blocking, zero major, and zero minor
findings with verdict
`PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY`. CONTROL then accepted
the design only for main integration consideration with decision
`ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`.

## 4. Accepted design disposition

Main integration may establish only the following public design baseline:

1. the effective design is v0.3 plus the bounded v0.4 and v0.5 replacements;
2. `M-07A`, `M-06B`, and `N-01` are closed at public design-text level;
3. the v0.4 closures of `M-05A` and core `M-06A`, plus inherited `M-04`,
   remain effective;
4. run-record-v3 is exactly 38 fields, 2,224 bytes, and SHA-256
   `73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6`;
5. receipt-v2 is exactly 21 fields and 1,173 bytes for every admissible three-
   digest tuple, while its actual bytes and SHA-256 remain unavailable until
   the three true external pins exist;
6. controller `COMPLETE` is not rehearsal PASS, retained files are
   `offline-not-success-diagnostic-only`, and only same-process live-consumer
   acceptance may issue PASS; and
7. the last-error failure-read and success-sentinel paths remain disjoint.

V0.1 through v0.4 and their reviews remain immutable historical design,
failure, and correction evidence. They are not competing current design
authorities.

## 5. F0 preservation

The observed `origin/main` and reviewed CONTROL tip both contain exactly:

- 32 tracked entries under the CONTROL F0 family;
- 11 tracked entries under the staging F0 family; and
- 10 tracked entries under the review F0 family.

The quiet diff from observed main to reviewed tip is zero for all three
families. No F0 filename or content was used as a decision input. Their
tracked presence is required repository synchronization, not AI content
authority.

## 6. Exact conditions on the later fast-forward

A later `MAIN FAST-FORWARD OPEN` operation may proceed only if it independently
rechecks all of the following immediately before changing Git state:

1. live `origin/main` is still exactly
   `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`;
2. the pushed source tip is the commit containing this decision pair as the
   sole direct-child change of
   `92b747cb314340dfc872b660aece5ed5c71896d4`;
3. main remains an ancestor of that final source tip and the left count is
   zero;
4. the final source diff is exactly 79 paths in the 55/10/2/12 categories in
   section 2, with zero other path;
5. every design, review, and CONTROL hash in section 3 remains exact;
6. both trees retain F0 counts 32/11/10 and their F0 quiet diff is zero;
7. the worktree, index, stash, local-only commits, ignored/untracked
   aggregates, and special index flags satisfy current repository Git rules;
   and
8. the operation is a fast-forward only, with no merge commit, rebase, force,
   reset, deletion, branch rewrite, or selective cherry-pick.

If live main moved, an input changed, the scope differs, the relationship is
not a fast-forward, or any query fails, the later gate must stop. This
decision cannot be stretched to a different main or source tip.

## 7. What main integration will and will not mean

After the separately authorized fast-forward, main may claim only that the
authenticated public assembly rehearsal v0.5 **design**, its correction and
review lineage, and the disclosed historical project records are integrated.

It will not mean that a controller, FFI wrapper, observer, capability,
witness, live consumer, receipt instance, verifier, test harness, Windows or
NTFS behavior, or rehearsal exists or works. It will not establish rehearsal
PASS, F0 isolation, provider/model behavior, S0/E0, central-system or Project
Brain behavior, operational safety, economic value, production readiness, or
model-to-model transfer.

Implementation remains a separate user-opened gate. Main integration cannot
open it automatically.

## 8. Closed actions

This decision does not authorize:

- changing or pushing `main`;
- creating a merge commit, PR, release, tag, or branch deletion;
- implementation, tests, Windows/VM/platform provisioning, or rehearsal;
- F0 content access or modification;
- fixture, oracle, executor, judge, scoring, provider/model, E0, or S0 work;
  or
- central-system or Project Brain implementation.

## 9. Decision and next gate

**Decision: `APPROVE-SEPARATE-MAIN-FAST-FORWARD-ONLY`.**

The exact next permissible gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.5 MAIN FAST-FORWARD OPEN`

That gate authorizes only the bounded Git fast-forward after every section 6
condition is freshly reproduced. It does not authorize implementation.

## 10. Maximum claim

At the observed Git state, the complete authenticated public assembly
rehearsal design v0.5 lineage is eligible for a separate exact main
fast-forward. Main has not been changed by this decision.
