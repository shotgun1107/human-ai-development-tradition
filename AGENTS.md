# AI Development Tradition project instructions

## Current gate

- The active design baseline is `central-system-v2.1-s0-preparation`.
- This repository is still in S0 preparation. Do not claim that S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer has been implemented or validated.
- Do not implement code, create synthetic fixtures, create a hidden oracle, or run S0 unless the user explicitly opens that exact gate in the current thread.

## S0 role isolation

- Follow the role and allowed-input list in the current thread prompt. An allowlist is a maximum, not a suggestion to inspect the rest of the repository.
- Do not search the repository broadly when the assigned role has a narrow input list.
- The following tracked paths are **PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY F0
  artifacts** even when they are present in a public clone or visible to
  filesystem tools:
  - `s0-lab/control/f0-sealed/**`
  - `s0-lab/f0-sealed-staging/**`
  - `s0-lab/reviews/f0-sealed/**`
- Public Git presence, a branch name, a path mention, repository-wide search
  convenience, or synchronization work does not add those paths to an agent's
  allowed inputs. Do not open, search within, quote, summarize, derive from, or
  pass their contents to another agent unless the current user message opens
  the exact F0-SEALED gate and the role prompt explicitly names the required
  paths. A synchronization or integrity role may compare path inventory,
  tracked state, file size, and supplied SHA-256 without treating content as a
  task input.
- An executor, judge, public reviewer, or unrelated CONTROL task must not read
  F0-SEALED material merely because the repository contains it. An accidental
  unauthorized read invalidates that role/session for dependent evidence; stop
  and report the boundary failure.
- A fixture-authoring thread must never be forked into an executor thread.
- Executors A–D must be fresh threads, must not inherit another executor's conversation, and must not read another condition's output.
- The hidden oracle must not be stored in this repository or in an executor-visible worktree.
- Worktrees isolate edits, not secrets. Never describe worktree separation alone as independent information security.
- If role boundaries or allowed inputs are unclear, stop without reading more files and request direction.

### Git publication and AI content access are independent

- The `SEALED` token in the three path names above is an experimental
  role-access label, not a Git privacy or publication label.
- The existing tracked inventory must remain in every authoritative tree used
  to synchronize this repository: 32 files under `s0-lab/control/f0-sealed/`,
  11 under `s0-lab/f0-sealed-staging/`, and 10 under
  `s0-lab/reviews/f0-sealed/` (53 total).
- Clone, fetch, checkout, pull, push, branch ancestry, worktree
  materialization, and unchanged tree preservation do not grant AI authority
  to read those files.
- An exact F0 role/read gate grants only the content access and role actions
  explicitly named by the current user message and allowlist. It does not by
  itself authorize commit or push.
- Git publication or handoff approval grants only the stated Git action. It
  does not by itself authorize content access.
- Before any cross-PC switch, pull, reset, clean, merge, or worktree
  replacement, check the three F0 path families without printing filenames:
  immediately capture every quiet-diff exit code; separately reduce untracked,
  ignored, skip-worktree, and assume-unchanged entries to aggregate counts;
  print only named aggregate values; and fail closed before another Git command
  can overwrite an exit code. Any nonzero or query failure blocks the
  Git-changing action and is reported only as a path-family/count condition.
- Native Git stdout that may contain filenames must remain captured and reduced
  to approved aggregates; native Git stderr must be suppressed at the command
  boundary and replaced by a generic condition label plus exit code. A failed
  command must never print a protected or unclassified filename before the
  fail-closed report.
- Excluding the three F0 families does not classify every remaining path as
  public. Enumerate filenames only within the current task's exact approved
  public allowlist. Reduce the repository's otherwise unclassified status to
  an aggregate count; any nonzero count blocks Git-changing or publication
  actions without printing filenames or content.
- For cross-PC preflight only, the repository's current explicitly disposable
  local-environment ignored classes are `.venv-docs/**`, `.mkdocs-site/**`,
  `**/__pycache__/**`, and `**/*.py[cod]`. Count them only as an approved local
  environment aggregate. Every other ignored path is unclassified and blocks
  Git-changing or publication actions without printing its filename.
- After fetch and before switch, checkout, rebase, merge, worktree
  materialization/replacement, or push, verify that the exact pinned target
  commit tree has aggregate F0 counts 32/11/10. Do not use `git pull` to fetch
  again after verification; advance only to the pinned commit. Before push,
  recheck the exact pushed tip counts and require a quiet F0 diff against its
  approved parent.
- `NONPUBLIC-OUT-OF-REPO` means hidden oracle, credentials, private keys,
  personal, real-customer, or secret material, and any future canonical
  execution input that the frozen protocol explicitly requires outside the
  repository. Never commit or push that class. Do not use the bare word
  `sealed` to decide publication eligibility.

### Current-policy precedence

- Platform instructions and the current user task remain authoritative.
- For repository-local interpretation, this root `AGENTS.md` controls current
  Git publication and synchronization classification.
- A current role prompt may narrow allowed inputs and actions, but it may not
  silently reclassify the three PUBLIC-GIT F0 path families as Git-private.
- Frozen protocol text controls experimental protocol semantics, including
  storage of future canonical execution input. It does not reclassify the
  existing three PUBLIC-GIT preservation path families.
- Dated README, HOME, handoff, resume, work-report, and review documents are
  historical evidence unless the current user message explicitly designates
  one. Historical text never overrides current tracked state or this
  publication/access mapping.
- If two current documents still conflict, stop before reading denied content
  or changing Git state and report the exact public clauses.

## Change and verification rules

- Preserve the SHA-256 records of frozen inputs. If a frozen input hash differs, stop the dependent task.
- For a public Markdown artifact with a same-basename SHA-256 sidecar, use `s0-lab/control/tools/verify-text-artifacts.ps1` after writing and before commit or transfer. Run its `-SelfTest` mode before relying on it in a new environment.
- Do not replace the canonical text-artifact validator with an ad hoc BOM, UTF-8, final-newline, trailing-whitespace, or sidecar check when the canonical tool applies. In particular, BOM detection must compare the leading bytes with `EF BB BF`, never a decoded-string `StartsWith` coercion.
- Keep text checks independently labeled. A BOM, UTF-8, final-LF, trailing-whitespace, sidecar-format, or sidecar-hash failure must identify its own failed check rather than a combined status label. The canonical tool does not replace task-specific branch, HEAD, exact-change-set, role-boundary, or frozen-input checks.
- Keep facts, inferences, proposals, and test results distinguishable.
- Do not use real customer, personal, secret, or past-project content in S0.
- When preserving, reviewing, transferring, or publishing completed work would materially benefit from a branch, commit, or push, the agent may identify that need independently and proactively request the user's approval. Before approval, state the exact repository, intended scope, branch, and whether the request covers commit, push, or both; do not perform the operation until the user approves it.
- For an ordinary commit or push approval request, make the request visually prominent with a clear heading, bold text, or an emoji, and state the repository, branch, scope, and requested Git action. Do not require or invent an all-caps approval token, security code, or gate-like passphrase. After such a clear request, an unambiguous response such as `ㄱㄱ`, `승인`, or `푸시해` is sufficient approval. Reserve exact gate phrases for work that genuinely changes an experimental gate, role-independence boundary, sealed boundary, or similarly sensitive authority.
- When the user explicitly requests a cross-PC or cross-session handoff
  package, that request authorizes commit and push of the completed public
  handoff-only **changes** to a dedicated handoff branch after exact staged-
  scope and publication-eligibility verification. The branch must preserve
  the inherited PUBLIC-GIT tree, including the unchanged 32/11/10 F0
  inventory. That inherited presence is required synchronization, not a
  forbidden content read or an extra handoff change. Do not wait for a second
  ordinary commit/push approval.
- Never commit or push `NONPUBLIC-OUT-OF-REPO` material. Existing or future
  user-approved bytes under the three PUBLIC-GIT F0 path families are not
  excluded merely because their path label contains `sealed`; modifying their
  contents still requires the exact role gate and separate applicable Git
  approval.
- No ordinary or handoff Git approval authorizes a PR, release, `main` merge,
  history rewrite, deletion, or AI content read unless those actions are
  separately explicit.
- Do not change another repository unless the user explicitly approves the exact repository and operation.
- Keep new S0 setup material under `s0-lab/` unless a task's approved output path says otherwise.
