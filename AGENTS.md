# AI Development Tradition project instructions

## Current gate

- The active design baseline is `central-system-v2.1-s0-preparation`.
- This repository is still in S0 preparation. Do not claim that S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer has been implemented or validated.
- Do not implement code, create synthetic fixtures, create a hidden oracle, or run S0 unless the user explicitly opens that exact gate in the current thread.

## Value-first gate selection and auxiliary-work limits

- CONTROL must optimize for the user's actual project outcome, not for technical completeness, security theater, evidence volume, or closing every historical nonclaim. A nonclaim, reviewer suggestion, theoretical attack, missing proof, or prior verdict suffix is not automatically a blocker or a reason to propose another gate.
- Before proposing any technical gate, CONTROL must explain in plain language: the exact core task it enables; what concrete failure or blocker exists without it; the cheapest standard or built-in alternative; why that alternative is insufficient; the expected useful output and realistic reuse; a rough best-case and worst-case time cost; and the stop or discard condition. If no current core task is blocked, label the work optional and do not recommend opening it.
- CONTROL must explicitly label proposed work as either **core project work** or **auxiliary tooling/evidence work**. Auxiliary work must not displace core implementation or environment construction merely because it can be made more rigorous.
- Prefer established operating-system, vendor, package-manager, and ecosystem verification tools for ordinary official artifacts. Do not propose a custom verifier, downloader, trust engine, evidence framework, or security subsystem unless the user explicitly requests that product or a frozen project requirement demonstrates that the standard tool cannot satisfy a concrete blocker. For example, an official Microsoft artifact normally needs its fixed source, digest, and standard Windows signature check—not a new research-grade verifier.
- Before asking the user to type a gate phrase that CONTROL itself suggested, CONTROL must repeat the purpose, expected result, non-result, likely cost, and cheaper alternative in ordinary language. The user's entry of the suggested phrase opens the stated scope, but it does not retroactively justify a poor recommendation.
- Time-box auxiliary candidates. If auxiliary work exceeds 30 minutes, expands beyond its original one-sentence purpose, requires an architectural redesign, or reaches two independent reject/correct cycles, stop before another correction. Report what was learned, the remaining benefit, the new estimated cost, and the cheapest fallback, then require an explicit user decision to continue. Do not autonomously enter a third correction cycle.
- Independent review is a backstop for an already justified bounded candidate, not a mechanism for continually expanding the threat model. Fix findings that violate the frozen required claim; preserve out-of-scope items as nonclaims instead of converting every hypothetical concern into new implementation work.
- Sunk cost creates no preservation duty. Before commit or integration, if auxiliary work no longer has concrete near-term value, CONTROL must recommend discarding it. Do not request result-preservation, commit, push, PR, or integration merely because substantial time was already spent.
- These value and time limits do not weaken F0 boundaries, Git approval requirements, destructive-action safeguards, or mandatory role separation inside a technical gate that the user knowingly chooses to continue.

## Delegation boundary for ordinary work

- Outside an explicitly opened technical gate and candidate/version, and unless the user explicitly requests delegation, root/CONTROL MUST perform the work directly. It MUST NOT spawn subagents merely for explanations, status reports, read-only repository authentication, ordinary approved Git operations, routine repository maintenance, or non-candidate operating-policy and documentation edits.
- The mandatory multi-role split below applies to substantive technical candidate work and candidate-owned implementation, tests, verification, documentation, and independent-review artifacts. Repository involvement alone does not make an ordinary task a multi-role technical gate.
- CONTROL MAY directly edit root `AGENTS.md` when the user explicitly requests a project-wide operating-policy correction. Candidate-specific reports, manifests, sidecars, preservation records, and technical claims remain owned by the DOCUMENTATION role inside the applicable technical gate.
- Ordinary non-technical work does not require a fresh independent reviewer unless the user explicitly requests one. CONTROL MUST still perform proportionate direct validation and MUST preserve every existing gate, role, F0, and Git-approval boundary.

## Mandatory technical role separation

- For every technical gate and every candidate/version, CONTROL must assign separate agents/sessions to exactly these roles: CONTROL, CODE IMPLEMENTATION, TEST/VERIFICATION, DOCUMENTATION, and INDEPENDENT REVIEW.
- One agent/session must not hold more than one of those roles for the same candidate/version or claim independence after contributing to another role for it.
- CONTROL freezes the gate, inputs and allowlists, pins and hashes, role assignments, evidence integration, decisions, and approved Git staging, commit, and push. CONTROL must not author or modify candidate code, tests, documentation artifacts, manifests or sidecars, or perform the independent review. Read-only Git and integrity authentication is allowed and is not substantive testing.
- The CODE IMPLEMENTATION agent alone edits implementation, source, and configuration within its allowed scope. It must not author tests or documentation or review its own work.
- The TEST/VERIFICATION agent alone authors or edits test and verification harnesses and runs substantive verification. It must not fix candidate code or author review verdicts, and it reports reproducible commands and results to CONTROL and the DOCUMENTATION agent.
- The DOCUMENTATION agent alone authors or edits public reports, design, revision, response, and preservation documents, manifests, sidecars, and handoff or resume artifacts from authenticated evidence. It must not edit code or tests or independently approve its own claims.
- The INDEPENDENT REVIEW agent must be fresh and read-only for the candidate, must not have served as CONTROL, CODE IMPLEMENTATION, TEST/VERIFICATION, or DOCUMENTATION for that same candidate/version, and must not edit artifacts. For code, security, adversarial, or unusually high-reasoning review, use a fresh `gpt-5.6-sol` agent at ultra reasoning when available, following the current user preference.
- The required sequence is CONTROL freeze -> CODE handoff -> TEST handoff -> DOCUMENTATION handoff -> fresh INDEPENDENT REVIEW -> CONTROL decision and publication. A role may be skipped only when the opened gate explicitly proves that it has no task-owned artifact or action; a skipped role must not be silently absorbed by another role.
- Every handoff must identify the exact pinned commit/tree, exact allowlist, applicable manifests and hashes, and explicit unverified items. No role may broaden its inputs.
- If a required role agent is unavailable, ambiguous, contaminated, or has crossed roles, stop and fail closed, then assign a fresh agent; CONTROL must not fill in for that role.
- Ordinary Git approval such as `ㄱㄱ` authorizes only the named commit and push; it does not open or combine technical roles or gates.
- Apply this policy prospectively to all new work after its adoption. Existing historical artifacts remain evidence and are not retroactively invalidated solely because this policy did not previously exist.

## Mandatory pre-CODE adversarial freeze

- Before every CODE handoff for every technical gate and candidate/version, CONTROL MUST freeze an end-to-end bounded and falsifiable adversarial checklist. It MUST cover the current candidate's complete attack surface and MUST NOT merely replay findings from an earlier version or review.
- At minimum, the checklist MUST map attacker capabilities and concurrency; trusted and untrusted prerequisites and authority sources; the complete data, execution, and evidence flow; authority mutability, caller-mintability, and rebinding; verified bytes versus the bytes actually executed or imported; interpreter, standard-library, native-library, and import closure; full inventory and shadow artifacts; and external-artifact URL, redirects, digest, size, and provenance.
- Where Windows paths are in scope, the checklist MUST cover the complete path lifecycle: ACLs, volume and root identity, symlink, junction, and reparse behavior, rename and replacement, retained identities and handles, repository exclusion, and TOCTOU through final output and evidence writes. It MUST also cover the evidence producer, output root, sidecars, pre/post measurements, published-command reproducibility, failure, cleanup, and close paths, resource bounds, and every permitted claim, nonclaim, and blocker.
- Every checklist row MUST freeze the CODE defense owner and action, the TEST/VERIFICATION adversarial or discriminating diagnostic case and expected fail-closed result, the DOCUMENTATION allowed claim and required nonclaim, and the INDEPENDENT REVIEW closure criterion. Every unverified prerequisite MUST remain explicit and MUST block any authority or claim broader than the verified evidence.
- The checklist is a bounded testable threat model, not a claim to cover every possible attack. Unknowns MUST be marked `unverified` and MUST NOT be silently promoted to assumptions.
- After an initial failure whose cause is not isolated, and always before a second speculative correction for the same blocker, TEST/VERIFICATION MUST produce a discriminating diagnostic matrix and evidence. CONTROL MUST stop repeated hypothesis-only CODE edits until that evidence isolates the next correction.
- Fresh INDEPENDENT REVIEW remains a backstop and MUST NOT substitute for CONTROL's precommitted threat freeze. The freeze itself MUST NOT open a gate, broaden an allowlist, combine roles, grant F0 access, or authorize staging, commit, push, or any other Git mutation.

## Session continuity, capacity, and fail-fast operation

- Chat promises and compressed conversation summaries are not authoritative. At every new, resumed, or compacted session, read the latest root `AGENTS.md` completely and reconstruct operational state from authenticated Git artifacts before acting. A user correction that must survive compaction must be written into root `AGENTS.md` before any role relies on it: CONTROL writes project-wide non-candidate operating policy directly, while the DOCUMENTATION role writes candidate-owned technical documentation and evidence within its opened gate.
- When F0 is not explicitly allowed, never run broad recursive path discovery under `s0-lab/reviews/`, including `rg --files`, recursive Git tree listing, or operating-system glob exclusion schemes. Use only exact supplied public paths and allowlists or authenticated manifests. Never rely on slash- or backslash-sensitive exclusions to protect F0. An exclusion mismatch or any protected filename exposure is a boundary failure: stop immediately, report it, and assign a fresh uncontaminated role agent.
- Before opening a multi-role gate, CONTROL must check available agent and thread capacity and plan the sequential role handoffs. Reuse an existing agent only when it remains in the same role for the candidate and every prior input is within the current allowlist; otherwise assign a fresh agent. Do not start a role sequence unless every required role can be allocated, and never let CONTROL absorb a blocked role.
- After direct ordinary commit or push approval such as `ㄱㄱ` or `rr`, the approval-bearing CONTROL or root session must execute the exact path in **Commit and push approval fast path** itself. Do not delegate the Git mutation to a child without the direct approval transcript. Subagents may prepare and authenticate staged scope but must not become an extra approval hop.
- Fail fast on latency: do not silently poll an unchanged agent or tool repeatedly. If the same blocker repeats, a required role cannot start, or completion will exceed 60 seconds, immediately give the user a concise blocker or status update and reroute or stop. Do not spend minutes retrying the same capacity, approval, or path failure.
- These rules persist through context compaction and apply prospectively. `ㄱㄱ` and `rr` authorize commit or push only; they never authorize implementation, review, another gate, a pull request, or a `main` merge.

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

### Commit and push approval fast path

- Treat an unambiguous response such as `ㄱㄱ` to a clear ordinary Git
  approval request as authorization for the named commit and push only. It
  does not authorize implementation, document revision, test expansion,
  independent review, another technical gate, PR creation, or main merge.
- Finish every task-owned byte change before requesting commit or push
  approval. Before the approval request, stage only the exact proposed scope
  unless the user explicitly requires it to remain unstaged, then require:
  exact branch and base identity, exact staged path set, zero unrelated
  staged/unstaged/untracked paths, `git diff --cached --check`, every required
  canonical text/sidecar check, final manifest and report hashes, applicable
  bounded tests, clean F0 aggregates and anomaly counts, and a quiet F0 diff
  against the proposed commit parent. Do not request approval while a known
  hash cascade, sidecar update, whitespace correction, or generated artifact
  remains unfinished.
- After approval, use the fast path: recheck only branch/HEAD, the already
  approved staged path set, unchanged staged bytes or hashes, F0 pre-push
  invariants, and then commit, push, and verify the live remote tip. Do not
  rerun a full test suite, regenerate artifacts, rewrite documentation, or
  reopen completed analysis merely because approval was granted.
- If an unexpected post-approval failure requires any byte change, stop the
  fast path and report the exact condition immediately. Apply only the
  smallest correction inside the already approved scope, rerun only checks
  invalidated by those changed bytes, and state why any hash cascade or
  bounded test rerun is unavoidable. A change outside the approved scope
  requires a new approval request.
- Keep the post-approval path short and continuously visible. If commit and
  push cannot complete promptly, report the blocker before beginning a long
  repair or validation sequence.
- The post-approval Git fast path has a hard 60-second wall-clock target. Before requesting approval, finish fetch/authentication, branch selection, exact staging, tests, hashes, F0 checks, and the intended publication route. After approval, perform only the minimal unchanged-byte recheck, commit, push, any explicitly requested fast-forward `main` integration, and live remote-tip verification. Do not stop after a feature-branch push when the same approval explicitly requested `main` integration.
- If the approved commit, push, requested `main` integration, and remote-tip verification cannot finish within 60 seconds, report the exact delay within 10 seconds and continue through the fastest safe in-scope path until completion. Do not turn the 60-second target into a blocker or stop condition. Never spend the post-approval interval fetching, designing, reanalyzing, rerunning full tests, changing branches unnecessarily, regenerating artifacts, or discovering the intended Git route.

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
