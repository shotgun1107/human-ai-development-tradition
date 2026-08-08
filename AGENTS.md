# AI Development Tradition project instructions

## Current gate

- The active design baseline is `central-system-v2.1-s0-preparation`.
- This repository is still in S0 preparation. Do not claim that S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer has been implemented or validated.
- Do not implement code, create synthetic fixtures, create a hidden oracle, or run S0 unless the user explicitly opens that exact gate in the current thread.

## S0 role isolation

- Follow the role and allowed-input list in the current thread prompt. An allowlist is a maximum, not a suggestion to inspect the rest of the repository.
- Do not search the repository broadly when the assigned role has a narrow input list.
- A fixture-authoring thread must never be forked into an executor thread.
- Executors A–D must be fresh threads, must not inherit another executor's conversation, and must not read another condition's output.
- The hidden oracle must not be stored in this repository or in an executor-visible worktree.
- Worktrees isolate edits, not secrets. Never describe worktree separation alone as independent information security.
- If role boundaries or allowed inputs are unclear, stop without reading more files and request direction.

## Change and verification rules

- Preserve the SHA-256 records of frozen inputs. If a frozen input hash differs, stop the dependent task.
- For a public Markdown artifact with a same-basename SHA-256 sidecar, use `s0-lab/control/tools/verify-text-artifacts.ps1` after writing and before commit or transfer. Run its `-SelfTest` mode before relying on it in a new environment.
- Do not replace the canonical text-artifact validator with an ad hoc BOM, UTF-8, final-newline, trailing-whitespace, or sidecar check when the canonical tool applies. In particular, BOM detection must compare the leading bytes with `EF BB BF`, never a decoded-string `StartsWith` coercion.
- Keep text checks independently labeled. A BOM, UTF-8, final-LF, trailing-whitespace, sidecar-format, or sidecar-hash failure must identify its own failed check rather than a combined status label. The canonical tool does not replace task-specific branch, HEAD, exact-change-set, role-boundary, or frozen-input checks.
- Keep facts, inferences, proposals, and test results distinguishable.
- Do not use real customer, personal, secret, or past-project content in S0.
- When preserving, reviewing, transferring, or publishing completed work would materially benefit from a branch, commit, or push, the agent may identify that need independently and proactively request the user's approval. Before approval, state the exact repository, intended scope, branch, and whether the request covers commit, push, or both; do not perform the operation until the user approves it.
- Never include sealed, hidden-oracle, secret, personal, or otherwise non-public material in a commit or push merely because Git publication was approved. Verify the staged scope separately, and request additional direction whenever publication eligibility is unclear.
- Do not change another repository unless the user explicitly approves the exact repository and operation.
- Keep new S0 setup material under `s0-lab/` unless a task's approved output path says otherwise.
