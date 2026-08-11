# AI Development Tradition project instructions

## Current gate

- The active design baseline is `central-system-v2.1-s0-preparation`.
- This repository is still in S0 preparation. Do not claim that S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer has been implemented or validated.
- Do not implement code, create synthetic fixtures, create a hidden oracle, or run S0 unless the user explicitly opens that exact gate in the current thread.

## S0 role isolation

- Follow the role and allowed-input list in the current thread prompt. An allowlist is a maximum, not a suggestion to inspect the rest of the repository.
- Do not search the repository broadly when the assigned role has a narrow input list.
- The following tracked paths are **default-deny F0-SEALED material** even when
  they are present in a public clone or visible to filesystem tools:
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

## Model assignment and verification

- Choose a model for the assigned evidence role, not because a different model
  name is itself evidence of independence, correctness, or security.
- Use a strong general coding/reasoning model as the primary reviewer for
  functional correctness, architecture, ordinary code review, test design,
  formal reasoning, and mathematical or cryptographic derivation.
- Use a defensive-cybersecurity-specialized model, such as Daybreak Blue when
  available, for a separate hostile security lane: threat modeling,
  authorization and isolation failures, secret exposure, injection, path
  traversal, unsafe parsing or deserialization, dependency and supply-chain
  risk, and security regressions in a code diff.
- Do not use a cybersecurity-specialized model as the sole judge of formal
  mathematics, cryptographic-vector correctness, general functional
  correctness, or experiment validity. It may separately review attack
  surface, misuse resistance, implementation hazards, and bypass paths.
- For security-sensitive implementations, keep the functional/correctness
  review and hostile security review as distinct evidence lanes. If either is
  claimed as independent, use a fresh session with its own bounded input set
  and do not inherit the author's or the other reviewer's conclusions.
- Model specialization never relaxes a frozen-input check, role allowlist,
  sealed boundary, fresh-session rule, deterministic test, reproducible tool
  check, or required human approval. Agreement between models is correlated
  AI evidence, not multiple independent facts.
- Apply the specialist security lane based on risk: security gates,
  authentication or authority changes, protected-data paths, dependency
  changes, release candidates, and security-sensitive diffs. Do not add it to
  every low-risk unit test merely to increase reviewer count or cost.
- Record the model role, allowed inputs, checks performed, findings, and
  evidence limits. Do not infer unavailable model pricing, capability, or
  account access from an alias alone.

## Change and verification rules

- Preserve the SHA-256 records of frozen inputs. If a frozen input hash differs, stop the dependent task.
- For a public Markdown artifact with a same-basename SHA-256 sidecar, use `s0-lab/control/tools/verify-text-artifacts.ps1` after writing and before commit or transfer. Run its `-SelfTest` mode before relying on it in a new environment.
- Do not replace the canonical text-artifact validator with an ad hoc BOM, UTF-8, final-newline, trailing-whitespace, or sidecar check when the canonical tool applies. In particular, BOM detection must compare the leading bytes with `EF BB BF`, never a decoded-string `StartsWith` coercion.
- Keep text checks independently labeled. A BOM, UTF-8, final-LF, trailing-whitespace, sidecar-format, or sidecar-hash failure must identify its own failed check rather than a combined status label. The canonical tool does not replace task-specific branch, HEAD, exact-change-set, role-boundary, or frozen-input checks.
- Keep facts, inferences, proposals, and test results distinguishable.
- Do not use real customer, personal, secret, or past-project content in S0.
- When preserving, reviewing, transferring, or publishing completed work would materially benefit from a branch, commit, or push, the agent may identify that need independently and proactively request the user's approval. Before approval, state the exact repository, intended scope, branch, and whether the request covers commit, push, or both; do not perform the operation until the user approves it.
- For an ordinary commit or push approval request, make the request visually prominent with a clear heading, bold text, or an emoji, and state the repository, branch, scope, and requested Git action. Do not require or invent an all-caps approval token, security code, or gate-like passphrase. After such a clear request, an unambiguous response such as `ㄱㄱ`, `승인`, or `푸시해` is sufficient approval. Reserve exact gate phrases for work that genuinely changes an experimental gate, role-independence boundary, sealed boundary, or similarly sensitive authority.
- When the user explicitly requests a cross-PC or cross-session handoff package,
  that handoff request itself authorizes commit and push of the completed
  public handoff-only artifacts to a dedicated handoff branch after exact
  staged-scope and publication-eligibility verification. Do not wait for a
  second ordinary commit/push approval. This standing handoff authorization
  does not authorize publishing sealed, hidden-oracle, secret, personal, or
  otherwise non-public material, and it does not authorize a PR, release,
  `main` merge, history rewrite, or deletion.
- Never include sealed, hidden-oracle, secret, personal, or otherwise non-public material in a commit or push merely because Git publication was approved. Verify the staged scope separately, and request additional direction whenever publication eligibility is unclear.
- Do not change another repository unless the user explicitly approves the exact repository and operation.
- Keep new S0 setup material under `s0-lab/` unless a task's approved output path says otherwise.
