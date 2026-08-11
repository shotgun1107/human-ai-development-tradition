# TRI2-VEC-02 main integration decision v0.1

- `decision_date`: `2026-08-11 KST`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR MAIN INTEGRATION DECISION OPEN`
- `repository`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `target_ref`: `refs/heads/main`
- `audited_origin_main`: `5add6e5e1675793ad179e98e51ffa1515feb3db8`
- `audited_source`: `6a40c94750d6a6edc015caa75f0f79ff2b990339`
- `audited_source_tree`: `6751657ca139bf6a60cc60241b5ea93e1a8eb448`
- `decision`: `APPROVE-EXACT-FAST-FORWARD-AFTER-SEPARATE-MERGE-AUTHORIZATION`
- `claim_kind`: public Git integration eligibility only

## 1. Decision

CONTROL approves the exact source commit
`6a40c94750d6a6edc015caa75f0f79ff2b990339` for a later **fast-forward-only**
advance of remote `main`, subject to the preconditions and explicit scope
acknowledgement in this decision.

This decision does not itself move `main`. The actual push requires a separate
user authorization after this decision pair is validated, committed, and
published. That authorization must be requested with the exact repository,
source, destination, 90-file scope, and 53 default-deny file count visible.

No merge commit, rebase, squash, cherry-pick, force push, history rewrite, or
local dirty-worktree update is approved. If remote `main` or the source tip
changes, this decision expires and integration must be re-audited.

## 2. Git ancestry and fast-forward result

CONTROL fetched all current remote refs before the audit and observed:

```text
origin/main commit = 5add6e5e1675793ad179e98e51ffa1515feb3db8
origin/main tree = b949a345cc80283ab78c889fa3d1cbabeed04cba
source commit = 6a40c94750d6a6edc015caa75f0f79ff2b990339
source tree = 6751657ca139bf6a60cc60241b5ea93e1a8eb448
merge base = 5add6e5e1675793ad179e98e51ffa1515feb3db8
left/right count = 0 main-only / 11 source-only
```

`origin/main` is an exact ancestor of the source. Therefore the audited
integration is a conflict-free Git fast-forward and needs no content merge.
The reverse ancestry does not hold.

The eleven source-only commits, oldest to newest, are:

1. `56fb3301630a4cf51643f0fa4a1f3351e9be5cf2` — author public vectors;
2. `dbba47b47c5c82649acfc2d839e18119344cd514` — preserve the first invalid review;
3. `daba763e219f597197768769115c01e5ea929c8a` — first input-boundary repair;
4. `85ad19ba6703f43b1209a13164d1e28a4b62f6a4` — preserve default-deny material and handoff records;
5. `b857545113058321dd4d65f601c2d5ad8cceeec0` — synchronization handoff completion;
6. `6d21e61dada605763d808f623a754d8c598bd6fb` — company synchronization record;
7. `a92a1029061f725a7a587bee690f091db0d334b5` — second input-boundary repair;
8. `3c41b54895d105496aa748ffe367939fefd0bd9e` — preserve the v0.3 invalid review;
9. `bb19e6aaf6cdbd34908670876b5badeff27a6eec` — final v0.3 input-boundary repair;
10. `439020a20ff7781673f561355246ee9013180d1e` — passing independent verification; and
11. `6a40c94750d6a6edc015caa75f0f79ff2b990339` — CONTROL final vector freeze.

Invalid reviews remain immutable failure history and do not override the later
passing review or final-freeze decision.

## 3. Exact tree-difference inventory

The audited source differs from `origin/main` in exactly 90 paths:

| Classification | Count |
|---|---:|
| added paths | 89 |
| modified paths | 1 (`AGENTS.md`) |
| deleted or renamed paths | 0 |
| regular-file mode `100644` | 90 |
| total paths | 90 |

Of those 90 paths, 53 are tracked default-deny F0 artifacts:

| Default-deny prefix | Count |
|---|---:|
| `s0-lab/control/f0-sealed/**` | 32 |
| `s0-lab/f0-sealed-staging/**` | 11 |
| `s0-lab/reviews/f0-sealed/**` | 10 |
| total default-deny paths | 53 |

The remaining 37 paths are public CONTROL, handoff, vector, review, or policy
records. This audit compared Git path inventory, modes, ancestry, and counts;
it did not open, search within, quote, hash as task evidence, or summarize any
default-deny file content.

## 4. Default-deny publication consequence

Commit `85ad19ba6703f43b1209a13164d1e28a4b62f6a4` introduced the 53 default-deny
paths into this already published remote lineage. Advancing `main` would not be
their first appearance on the public Git remote, but it would make them part of
the repository's default branch and ordinary default clone.

The updated `AGENTS.md` forbids unauthorized AI access to those paths. That is
a process and role-control boundary, not encryption, access control, or
secrecy. It cannot prevent a person or external system with repository access
from reading public Git objects. The fast-forward therefore increases default
visibility even though the objects already exist remotely.

This tradeoff is accepted for integration consideration only because the
audited lineage intentionally preserves those materials for cross-PC and
cross-session continuity. The actual main advance still requires the user to
approve the visible 53-path default-deny scope. An ordinary approval that
mentions only the four vectors is insufficient.

## 5. Included and excluded lineages

The exact fast-forward includes only commits ancestral to source
`6a40c94750d6a6edc015caa75f0f79ff2b990339`.

It does **not** include these separate branch tips:

- the v0.4 invalid-review branch tip
  `b84fd09de62750725d2ec5afa706c5a26ba9da30`;
- the handoff-manifest record branch tip
  `e8a3a9527a215cf73aaa27e6d8af4515696165b9`; or
- the model-role ground-rules branch tip
  `6908591b2315d42930a326687e4952bddb605ec1`.

Their exclusion is not deletion or a negative judgment. They remain separate
remote histories and require separate integration decisions if later needed.

## 6. Local-worktree safety

The repository-root local `main` is not an integration vehicle. At audit time
it was at `d88097df450c7869ebf336e3e1089d952955ea3f`, with no local-only commits
but 52 remote-only commits relative to `origin/main`. Existing local and
historical worktrees must not be reset, cleaned, rebased, stashed, switched,
or overwritten to perform this integration.

If the actual main advance is authorized, use the exact remote refs directly
from a clean CONTROL context. Re-fetch first, require `origin/main` still equal
the audited commit, require the source remote ref still equal the audited
source, repeat the ancestry and 90/53 inventory checks, then perform one normal
non-force fast-forward push. A normal non-fast-forward rejection is terminal;
do not add force.

After the push, fetch again and require:

```text
origin/main = 6a40c94750d6a6edc015caa75f0f79ff2b990339
origin/main tree = 6751657ca139bf6a60cc60241b5ea93e1a8eb448
```

Do not update or clean the stale repository-root local `main` as part of that
remote integration. Local synchronization is a later, separately checked
operation.

## 7. Claim and closed gates

This decision establishes only that the exact audited source is eligible for
a guarded public fast-forward of `main`. It does not claim that every
historical document is successful or current, and it does not reopen an
invalid review as evidence.

The vector package remains public evidence only. Implementation,
machine-readable generation, key generation, private-key custody, protected
material, provider/model sessions, fixtures, oracle, executor work, E0, S0,
central-system implementation, Project Brain integration, operational safety,
economic value, production readiness, and model-to-model transfer remain
closed.

After this decision is frozen and published, the maximum next gate is a
separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR MAIN FAST-FORWARD OPEN`

That gate authorizes only the exact guarded remote ref movement described
above. It does not authorize any subsequent technical or experimental gate.
