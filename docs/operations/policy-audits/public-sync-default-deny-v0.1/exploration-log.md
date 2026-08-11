# Public-sync/default-deny policy audit — exploration log

## 2026-08-11T15:44:50+09:00 — Phase 0: boundary and repository identity

### Exact public inputs

- Repository-root `AGENTS.md` (read completely).
- Git metadata only: current branch, `HEAD`, and object type of the supplied base commit.

### Query classes

- Full read of the repository-root instruction file.
- Exact Git identity checks (`branch --show-current`, `rev-parse HEAD`, `cat-file -t <base>`).
- Exact existence check for the approved output directory.

### Facts and findings

- Current branch is `codex/public-sync-default-deny-policy-audit-v01`.
- Current `HEAD` is the supplied base `6a40c94750d6a6edc015caa75f0f79ff2b990339`; the object is a commit.
- Root instructions explicitly call the three denied path families **tracked** and acknowledge that they can be present in a **public clone**.
- Root instructions clearly deny AI content access absent an exact gate, and expressly allow a synchronization/integrity role to compare metadata without treating contents as task input.
- A later publication clause says never to include “sealed, hidden-oracle, secret, personal, or otherwise non-public material” in a commit or push. Its unqualified use of `sealed` conflicts lexically with the earlier definition of the F0 paths as tracked/public-clone material and can be read as a prohibition on publishing those same files.
- The cross-PC handoff clause authorizes only “public handoff-only artifacts” and then excludes “sealed” material, creating a second likely route from the label `F0-SEALED` to “must not be synchronized.”

### Working hypotheses

- H1: Git itself still tracks and synchronizes the 53 files; the principal defect is policy-language conflation between AI read authority and Git publication eligibility.
- H2: Stale handoff/workflow documents repeat stronger “do not commit/push sealed” language and amplify the root ambiguity.
- H3: `.gitignore`, sparse checkout, LFS, skip-worktree/assume-unchanged flags, or synchronization scripts may create an actual sync defect; these require exact metadata checks without inspecting denied filenames or contents.

### Rejected hypotheses

- None yet. The filename token `sealed` is treated only as a label and is not evidence of Git privacy.

### Remaining checks

- Reproduce 32/11/10 = 53 using path-level tracked counts without listing filenames or reading contents.
- Check Git inclusion, ignore behavior, index flags, sparse-checkout configuration, attributes, and public sync scripts.
- Inventory and inspect relevant public policy, harness, workflow, operations, and stale handoff text outside the denied path families.
- Establish exact line references, causal chain, hostile scenarios, and the smallest coherent wording patch.

### Boundary compliance

- No denied file was opened, searched, quoted, summarized, hashed, or named.
- No filenames beneath any denied path were enumerated.
- No hidden oracle, fixture, secret, personal data, or provider/model session was accessed.
- Writes are confined to the user-approved audit output directory.
- No source, Git configuration, commit, push, merge, or PR operation was performed.

## 2026-08-11T15:50:33+09:00 — Phase 1: aggregate Git mechanics and public-text discovery

### Exact public inputs

- `.gitignore`, `.gitattributes`, `README.md`, `HOME-CODEX-START.md`, and repository-root `AGENTS.md`.
- The six tracked Markdown handoff/resume documents beneath:
  - `s0-lab/control/handoffs/company-to-home-2026-08-10/`
  - `s0-lab/control/handoffs/home-to-company-2026-08-09/`
  - `s0-lab/control/handoffs/home-to-company-2026-08-10/`
- Public protocol/status texts identified by public-only keyword search, including `s0-lab/README.md` and `s0-lab/control/s0-protocol-v0.1.md` through `v0.3-canonical-r1.md`.
- Git metadata: index/tree aggregate counts, local `origin/main`, ancestry, ignore/tracked aggregates, worktree-delta aggregates, sparse-checkout flags, shallow state, and submodule counts.

### Query classes

- `git ls-files` public inventory with all three denied path families excluded before output; denied-leak count asserted zero.
- Public-only `Select-String` searches over tracked `.md`, `.txt`, `.ps1`, `.sh`, `.yml/.yaml`, `.json`, and `.toml` files for the approved terminology classes and publication/action combinations.
- Path-scoped aggregate `git ls-files`, `git ls-tree`, `git status`, and ignored/tracked counts with output reduced to counts; no denied filename output.
- Exact line-range reads of public policy and handoff documents.

### Facts and findings

- Public-only tracked inventory: 554 paths after the three denied families were excluded; the filter reported zero denied-path leaks.
- Public text corpus searched: 341 tracked text/config files after exclusions.
- The denied families are present as regular tracked files in both the index and `HEAD`: 32, 11, and 10, totaling 53.
- `refs/remotes/origin/main` equals `HEAD` (`6a40c94750d6a6edc015caa75f0f79ff2b990339`) and has the same 32/11/10 aggregate tree counts. Both ancestry checks return success.
- For each denied family: ignored-but-tracked count is zero, worktree-delta count is zero, and submodule-entry count is zero.
- Sparse checkout and sparse-cone mode are unset; the repository is not shallow; no tracked `.gitmodules` exists.
- `.gitignore` contains only virtualenv, generated site, Python cache, and bytecode patterns. `.gitattributes` contains only general LF normalization and ZIP binary treatment. Neither excludes or filters the denied families.
- Therefore ordinary Git mechanics at the recorded `origin/main` do not block synchronization. A clone/pull of that tree carries all 53 entries. The dominant risk is an agent acting on contradictory policy and intentionally omitting, pruning, refusing, or misreporting them.
- `README.md:9` actively routes every new-PC/session operator to stale `HOME-CODEX-START.md`.
- `HOME-CODEX-START.md:35,41-46` says F0-sealed paths were untracked, are not transferred by Git, and may be absent on another PC. It has no supersession warning and directly contradicts the current index/tree state.
- `AGENTS.md:13-24` correctly separates public Git presence from AI read authority, but `AGENTS.md:46-54` later groups `sealed` with hidden-oracle/secret/personal/non-public material and prohibits its publication. There is no exception or precedence rule for the three tracked F0 families.
- The 2026-08-10 company-to-home handoff is internally self-contradictory: lines 18-20, 145, and 159-180 say all 53 are tracked, published, and physically present in public clones, while lines 102-104 say sealed material must be excluded from public worktrees and Git publication; lines 268-269 say not to copy sealed material into a new public worktree.
- The 2026-08-09 home-to-company handoff/resume pair is stale and more directly exclusionary: the current-state document lines 22-27 says company sealed material must not enter public Git, and lines 225-230 say not to copy it into a new worktree; the resume prompt lines 138-141 and 172-175 say Git does not synchronize company-only sealed material and absence can be normal.
- The 2026-08-10 home-to-company current-state handoff lines 75-84 says automatic handoff commit/push excludes `sealed`, while lines 86-110 says the three families are tracked 32/11/10. This repeats the publication-vs-read ambiguity even in the corrected handoff generation.
- Canonical protocol text uses `sealed/canonical input` for a genuinely non-public, outside-repository execution artifact (`s0-protocol-v0.3-canonical-r1.md:359`), while current path policy uses `F0-SEALED` for publicly tracked but AI-content-restricted files. The same adjective denotes two different publication classes.
- Several handoff commands violate their own metadata-only boundary: bare `git ls-tree -r --name-only` on the denied paths (`company-to-home current-state:317-319`) enumerates names rather than counts; broad `git ls-files -t` and `git status` commands can also print denied filenames if entries or changes exist. Corrected resume prompts sometimes wrap tree/list output in `.Count`, but not consistently.

### Working hypotheses

- H1 is supported: Git sync is currently intact; policy interpretation is the primary defect.
- H2 is supported: stale, actively routed handoffs and an internally contradictory current handoff amplify the defect.
- H3 is rejected for the recorded checkout/ref: no ignore, sparse, submodule, LFS attribute, or worktree-delta evidence explains missing synchronization.
- H4: the primary causal chain is overloaded `sealed` terminology → later blanket publication ban → conservative agent interpretation → refusal to stage/push or assertion that files are private → cross-PC mismatch despite a correct Git tree.

### Rejected hypotheses

- Path names containing `sealed` do not create Git privacy or exclusion.
- `.gitignore` does not affect the 53 current tracked entries and contains no relevant pattern.
- Worktree separation is not a secrecy or synchronization boundary.
- The 2026-08-10 handoffs are not uniformly correct; one contains both the intended rule and its negation.

### Remaining checks

- Complete public clause inventory and distinguish direct blockers, semantic amplifiers, correct counterevidence, and historical nonproblems.
- Inspect I0/current-gate prompts for generic “sealed may not enter repo/worktree” wording and determine whether it is task-scoped or globally misleading.
- Obtain the two independent sub-audit reports and reconcile duplicates.
- Build severity-ranked causal chain, precedence table, at least ten hostile scenarios, and minimal coherent wording patch.
- Validate final outputs and exact write scope.

### Boundary compliance

- Counts were computed without displaying or recording denied filenames.
- No denied file contents, hashes, semantics, or filename inventory were accessed.
- Public text searches excluded all three denied families before `Select-String` received its file list.
- No source or Git configuration was changed; no network fetch, commit, push, merge, PR, or hidden-oracle/provider/model action occurred.

## 2026-08-11T16:01:15+09:00 — Phase 2: hostile synthesis and minimum repair design

### Exact public inputs

- All Phase 0/1 public inputs.
- Additional exact public line ranges from:
  - `docs/tradition/s0-e0-boundary-and-parallel-work.md`
  - `docs/tradition/s0-isolated-design-execution-and-judgment-plan.md`
  - `s0-lab/control/i0/i0-gate-record.md`
  - `s0-lab/control/i0/home-local-resume-prompt.md`
  - `s0-lab/control/i0/i0-refreeze-next-control-prompt-v0.1.md`
  - `s0-lab/control/s0-protocol-v0.3-canonical-r1.md`
  - `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md`
- Two independent read-only sub-audits: Git mechanics and public-text conflicts.

### Query classes

- Public-only cross-line regex scan for `sealed/봉인` near publication, sync, outside-repository, untracked, exclusion, copy, and private-area actions.
- Public-only search for broad/name-producing Git recipes (`git diff`, `git status`, `git ls-files -t/-v`, `git ls-tree --name-only`).
- Exact public line-range inspection around every direct conflict cluster.
- Safe recipe proof: `git ls-tree --format='%(objectmode)'` and `git ls-files --format='%(objectmode)'` reproduced aggregate counts without filename output; path-scoped `git diff --quiet` returned success without content output.

### Facts and findings

- Final severity model: 2 Critical, 5 Major, 2 Minor findings (9 total).
- Root publication/read self-conflict and active stale onboarding are Critical.
- Handoff self-conflict, terminology collision with the authoritative canonical protocol, unsafe sync commands, missing precedence/supersession, and non-orthogonal approvals are Major.
- Old state claims and absence of one canonical count-only invariant are Minor amplifiers.
- Public command search found 21 risky Git command occurrences. Broad `git diff --exit-code` can print denied content on drift; `git ls-files -t` and bare `ls-tree --name-only` enumerate filenames; broad status reveals changed filenames.
- Fourteen hostile scenarios were constructed, covering deletion/untracking, refusal to push, orphan/pruned branches, sparse checkout, staged-scope fallacy, read/publication gate inversion, diff leakage, filename enumeration, gate-vs-inventory confusion, worktree secrecy error, and no-upstream misdiagnosis.
- The smallest coherent repair does not touch the 53 files or frozen protocol. It defines two independent axes at root, replaces the bare `sealed` publication ban, adds repository-document precedence, marks old onboarding/handoffs superseded, corrects current handoff contradictions, and replaces sync recipes with root-tree identity plus quiet/count-only checks.
- `audit-report.md` and `minimal-rule-revision-proposal.md` were written in the approved output directory.

### Supported causal chain

1. Some F0 paths were historically untracked/local-only.
2. A later user decision made all 53 Git-tracked preservation artifacts.
3. Correct tracked/public-clone wording was added without removing generic sealed publication bans.
4. README continued to route new sessions to the pre-transition HOME document.
5. Current handoffs copied both old exclusion language and new public-sync language.
6. Conservative agents collapse the overloaded label into `sealed = private = do not push`.
7. Agent behavior, not Git mechanics, causes refusal, omission, or incorrect reporting.

### Rejected hypotheses

- There is no demonstrated Git-level path exclusion at the recorded default-branch ref.
- Renaming or deleting the 53 files is not required to fix the policy.
- Editing the frozen canonical protocol is not the minimum repair and would require a separate semantic gate.
- Merely saying “sealed is public” is insufficient because it could authorize the inverse error of publishing truly non-public canonical/oracle material.
- Staged-scope verification alone cannot solve publication classification because Git commits retain inherited full-tree ancestry.

### Remaining checks

- Verify the approved output directory contains exactly the three authorized files.
- Verify public-only Git status shows no other change and denied path delta aggregates remain zero.
- Verify UTF-8/no-BOM/final-LF/trailing-whitespace status for the three outputs; no sidecars exist, so the canonical same-basename-sidecar validator is not applicable.
- Record final verification and report to the parent agent.

### Boundary compliance

- Both sub-audits read root `AGENTS.md` first and used explicit denied-path exclusions.
- No denied internal filename or content was included in either sub-audit result or final artifacts.
- All writes remain confined to the three authorized audit files.
- No repository source, frozen protocol, handoff, rule, harness, Git config, branch, commit, push, PR, or gate was changed.

## 2026-08-11T16:02:06+09:00 — Phase 3: final verification

### Exact inputs

- The three authorized output files only.
- Public-only Git status with all denied families excluded.
- Denied-family status reduced directly to aggregate counts.
- Branch, `HEAD`, and local `origin/main` Git identities.

### Verification results

- Approved output directory contains exactly three files:
  - `audit-report.md`
  - `exploration-log.md`
  - `minimal-rule-revision-proposal.md`
- Unexpected output files: 0.
- Public-only Git status contains exactly those three untracked audit artifacts and no other public change.
- Denied path status delta aggregates remain 0 / 0 / 0.
- Branch remains `codex/public-sync-default-deny-policy-audit-v01`.
- `HEAD` remains the supplied base `6a40c94750d6a6edc015caa75f0f79ff2b990339`.
- Local `origin/main` remains the same commit.
- All three outputs are strict-valid UTF-8, have no UTF-8 BOM, end in LF, contain zero CRLF sequences, and contain zero trailing-whitespace lines.
- Markdown fence counts are balanced and no `TODO`, `TBD`, or `FIXME` placeholder remains.
- No same-basename SHA-256 sidecars exist for these new artifacts; the canonical sidecar validator is therefore not applicable and no sidecars were created.
- The proposed quiet/count-only denied-path commands were executed in read-only form: worktree and staged diff exit codes were both 0, and object-mode-only tree/index counts reproduced the expected aggregate without filename output.

### Final conclusion

- Git state supports full synchronization of all 53 tracked entries.
- The primary defect is policy-language conflation and missing precedence, not a Git exclusion mechanism.
- The audit found 9 issues: 2 Critical, 5 Major, 2 Minor.
- The minimum repair is a public rule/onboarding/handoff/harness wording patch; no rename/delete of the 53 and no frozen-protocol semantic edit is required.

### Boundary compliance

- No denied filename or content was displayed during final verification.
- No source file or Git state was mutated beyond the three authorized untracked audit files.
- No commit, push, merge, PR, configuration change, network fetch, hidden-oracle action, or experimental gate action occurred.

## 2026-08-11 — Remediation and hostile rereview cycle

### Policy remediation

- Root policy now separates `PUBLIC-GIT` transport classification from
  `AI-CONTENT-DEFAULT-DENY` access authority.
- The existing 32/11/10 inventory is required in authoritative synchronization
  trees; hidden oracle, credentials, keys, personal/real/secret material, and
  future protocol-designated canonical execution input are classified as
  `NONPUBLIC-OUT-OF-REPO`.
- README now routes new sessions to root `AGENTS.md`; the old HOME document and
  2026-08-09 handoffs are visibly superseded.
- Current 2026-08-10 handoffs no longer tell agents to omit the inherited 53
  files or use name/content-producing F0 checks.

### First rereview result and correction

- A fresh Daybreak Blue rereview was attempted repeatedly but could not finish
  because the model service returned an organization TPM limit before a result.
  This was an availability failure, not a pass or a policy finding.
- A fresh Sol Ultra fallback rereview returned `REVISE-AND-REREVIEW` with one
  Critical and three Major findings:
  - a supersession warning disappeared when the embedded 2026-08-09 prompt was
    copied;
  - quiet-diff exit codes were overwritten by later Git commands and aggregate
    counts were not enforced;
  - target-tree 32/11/10 verification occurred too late and `git pull` could
    refetch after verification;
  - status commands could reveal filenames outside the three F0 paths.
- The candidate was revised so both current resume prompts use the same
  fail-closed PowerShell preflight. It emits aggregate values only, captures
  each exit immediately, distinguishes untracked from ignored entries, checks
  skip-worktree/assume-unchanged state, and throws before Git-changing actions.
- Local-only commits are evaluated only after a clean fetch refreshes remote
  refs. Exact remote tips are pinned; 32/11/10 is checked before materializing
  them; existing branches fast-forward to the pinned commit without `git pull`.
- Root policy and both current handoff directions require exact pushed-tip
  inventory plus an approved-parent quiet F0 diff before any separately
  approved push.

### Post-revision verification

- Canonical validator SelfTest: PASS.
- All seven changed Markdown/sidecar pairs: PASS.
- `git diff --check`: PASS.
- The two current executable preflight function blocks are byte-identical.
- Executing the documented functions against this dirty policy worktree
  produced F0 tree counts 32/11/10, zero F0 worktree/staged/local-only/ignored/
  special-index conditions, and correctly failed closed on the nonzero overall
  repository status without printing affected filenames.
- No protected F0 file content, internal filename, or per-file hash was read or
  emitted during remediation or validation.

### Remaining gate

- A fresh zero-finding hostile rereview of this revised candidate remains
  required before commit/push integration consideration. The prior fallback
  `REVISE-AND-REREVIEW` is not silently converted into a pass by author QA.
