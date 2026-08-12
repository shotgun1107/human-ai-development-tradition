# S0 v0.14 I3 public import-decision implementation v0.2 main integration decision v0.1

- `status`: main integration decision
- `decision_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION V0.2 MAIN INTEGRATION DECISION OPEN`
- `recorded_origin_main`: `1472cd191b5c8a84dcab41a6107386997c75fd3c`
- `recorded_origin_main_tree`: `b5427511c54fd861847240a2df27aeae6717903c`
- `decision_input_tip`: `1e29ff7941e1fd2dc1baa6cf620b6b853d6c2014`
- `decision_input_tree`: `81e97379382354dc0802a1c02b8db01bb7765570`
- `implementation_candidate_commit`: `4dad07167dbd1c14168c41d78f11fccbe0d07b09`
- `decision`: `APPROVE-MAIN-FAST-FORWARD-CONSIDERATION-ONLY`
- `main_mutated`: false
- `operational_execution_status`: closed

## 1. Decision

The authenticated I3 v0.2 bounded public model-free implementation lineage is
eligible for a separately opened main fast-forward gate.

This decision establishes only that:

1. the recorded `origin/main` is an ancestor of the authenticated decision
   input tip;
2. main has no main-only commit relative to that tip;
3. the implementation candidate, independent rereview, and CONTROL acceptance
   form one linear public lineage;
4. the PUBLIC-GIT F0 inventory is unchanged across the proposed integration;
   and
5. a later exact pinned fast-forward may be considered after this decision
   pair is preserved as the sole child of the decision input tip.

This decision does not update main, push main, merge, open a PR, execute I3,
or open any E0 or S0 gate.

## 2. Authenticated public evidence

| Artifact | SHA-256 | Use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current Git, publication, and F0 policy |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | public artifact validation |
| I3 v0.2 accepted design | `f04dae684b7373a4c613c3f0e357ef8266f0bf307e78e78d105cb04168f61594` | implementation design authority |
| I3 v0.2 implementation/test brief | `182df459eee2877d5c4710794ad7a7c86a56a44abe7ce14d09e629fc1c29ac62` | candidate and test requirements |
| I3 v0.2 implementation contract JSON | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` | machine-readable public implementation contract |
| I3 v0.2 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | exact public implementation payload |
| I3 v0.2 independent rereview | `164a5e0d0ec99a503b17ebaee7d8778f2b840c672b3f74760fdee6320f6ddc48` | zero-finding independent result |
| independent rereview sidecar file | `b8ebc5a1a7e8558172e6370a7e19f3c0e3791d83407edca7959cbee1778b88d2` | review-byte authentication |
| v0.2 CONTROL integration decision | `5ad38bda2bd0253d597d4e19db3e8bd1ca62c60adfa1d454fa9b247771d9ed6c` | CONTROL acceptance for main consideration |
| CONTROL decision sidecar file | `5084f1ddbf812934632434d1c33ea791673a35931668c51bcff47318ace2e300` | decision-byte authentication |

The authenticated validator SelfTest passed all 11 named cases. The committed
independent rereview pair and CONTROL decision pair each passed strict UTF-8,
BOM absence, final LF, trailing-whitespace absence, exact sidecar record, and
artifact hash validation with `OVERALL=PASS`.

## 3. Exact Git topology

At this decision gate, the authenticated topology was:

```text
1472cd191b5c8a84dcab41a6107386997c75fd3c  origin/main
  -> c67a1610af28688108dc1b033c9b68a5554cb21c
  -> d1b79cb8a032c285202aef7d72b80121065e217d
  -> 4dad07167dbd1c14168c41d78f11fccbe0d07b09
  -> 1e29ff7941e1fd2dc1baa6cf620b6b853d6c2014  decision input tip
```

The four target-only commits have these roles:

| Commit | Role |
|---|---|
| `c67a161` | initial bounded public I3 implementation candidate |
| `d1b79cb` | v0.1 independent review recording blocking `I3-IIR-B01` |
| `4dad071` | bounded v0.2 global-link validation repair |
| `1e29ff7` | zero-finding v0.2 rereview and CONTROL acceptance |

The independently observed relation was:

- main-only commits: `0`;
- target-only commits: `4`;
- merge-base ancestry check: `origin/main` is an ancestor of the target;
- local target tip equals remote target tip; and
- decision-entry worktree status count: `0`.

No rebase, merge, reset, checkout, main update, or history rewrite was used to
obtain this relation.

## 4. F0 and publication preservation

Only aggregate information was used. No F0 filename or content was opened,
searched, quoted, or derived.

| Tree | control F0 | staging F0 | review F0 | Total |
|---|---:|---:|---:|---:|
| recorded `origin/main` | 32 | 11 | 10 | 53 |
| decision input tip | 32 | 11 | 10 | 53 |

The three quiet F0 diffs from recorded `origin/main` to the decision input tip
all returned zero. The F0 inventory therefore remains synchronized while its
contents remain outside this role's AI input authority.

## 5. Technical and review disposition

The accepted implementation remains a bounded deterministic public contract
implementation. Its verified public properties include the exact 21/26/31
grammars, route and state mappings, media classification, stable error
surface, explicit expected I2 sequence and predecessor inputs, and unchanged
I2 global-link validation before destination-authority availability.

The fresh independent rereview reported zero blocking, zero major, and zero
minor findings. It independently confirmed that the exact matching link case
is the sole authority-granting structural path and that mutated, missing,
partial, contradictory, or unpersisted evidence fails closed.

The CONTROL integration decision accepted that zero-finding candidate only
for main integration consideration. No later evidence has contradicted or
replaced those authenticated bytes.

## 6. Required exact fast-forward preconditions

A future main fast-forward gate may proceed only if every condition below is
re-authenticated immediately before mutation:

1. this main decision pair is committed as the sole two-path child of
   `1e29ff7941e1fd2dc1baa6cf620b6b853d6c2014`;
2. the pushed decision branch tip equals that exact decision commit and tree;
3. live `origin/main` still equals
   `1472cd191b5c8a84dcab41a6107386997c75fd3c`, or a new explicit integration
   decision accounts for any movement;
4. live main-only count relative to the pinned decision tip remains zero;
5. the exact pinned decision tip has F0 aggregate counts 32/11/10;
6. each quiet F0 diff from the approved parent to the exact pushed tip is
   zero;
7. there is no tracked, staged, untracked, unclassified ignored,
   skip-worktree, or assume-unchanged state in the mutation worktree; and
8. the fast-forward uses the exact pinned commit, not a moving branch name.

Any mismatch stops the later gate without merge, reset, rebase, clean,
overwrite, or retry-based inference.

## 7. Gates and claims that remain closed

This decision does not authorize or establish:

- actual main mutation or publication;
- a real appliance, raw medium, durable ledger, witness, registry, vault, key,
  signature, VM, sandbox, network, or provider;
- real persistence, atomic append, project-lifetime uniqueness, or destination
  authority;
- F0 content access, fixture or oracle authoring, executor or judge work;
- model sessions, E0, S0, central-system implementation, or Project Brain
  integration; or
- operational safety, production readiness, economic value, or
  model-to-model transfer.

`append_status=persisted` and the expected global-link values remain
caller-supplied public structural evidence. They are not proof of a real
external durable ledger.

## 8. Decision and next gate

**Decision: `APPROVE-MAIN-FAST-FORWARD-CONSIDERATION-ONLY`.**

After this decision pair is canonically validated, committed as the exact
child described above, and pushed, the next permissible experimental gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT IMPLEMENTATION V0.2 MAIN FAST-FORWARD OPEN`

That gate may perform only the exact pinned fast-forward after repeating all
noncompensatory checks. It does not open I3 execution, E0, or S0.

## 9. Maximum claim

The authenticated I3 v0.2 bounded public implementation lineage is currently
linear and eligible for a separately authorized exact main fast-forward. Main
has not been changed by this decision, and no operational import or authority
claim has been validated.
