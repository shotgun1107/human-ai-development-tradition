# Company-local CONTROL resume prompt — 2026-08-13

You are the existing CONTROL session continuing the
`human-ai-development-tradition` project on the company PC.

Do not reconstruct project truth from prior conversation memory. Use current
Git state, the latest root `AGENTS.md`, the externally supplied exact final
handoff commit/tree, and authenticated repository records.

## Repository and fixed public payload

- repository:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`
- handoff branch: `codex/home-to-company-handoff-20260813`
- required public design payload commit:
  `a44e68d2994168a87bbf63d1b9f016496b82908b`
- payload tree: `ccc418fa7ce415718f3facf39cacf62df4872263`
- payload parent: `f336995da41d201a9132246d7fffd0506f9a5a01`
- recorded `origin/main` at home handoff preparation:
  `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`

The CONTROL chat that delivers this prompt must also provide the exact final
handoff commit and tree. Treat those out-of-band values as required pins. Do
not trust the moving branch name by itself.

## First task: synchronize and authenticate only

Use the existing company repository if it exists. Do not create a new clone
unless no repository exists.

First inspect, without changing state:

- repository path and origin;
- current branch, HEAD, upstream, worktrees, and stash count;
- tracked/staged/unstaged state;
- untracked and ignored state reduced according to the current root
  `AGENTS.md`; and
- local-only commits.

Preserve dirty work, stashes, local-only commits, and worktrees. If any are
present, do not reset, clean, stash, rebase, merge, switch over them, or
overwrite them. Fetch the handoff ref and materialize the exact pinned final
handoff commit in a separate clean worktree. If the existing company worktree
is completely clean and current instructions allow it, fetch and advance only
to the exact pinned commit. Do not use an unpinned `git pull` as the authority.

Verify:

- live remote handoff tip equals the externally supplied final commit;
- final tree equals the externally supplied final tree;
- the final commit's sole parent is
  `a44e68d2994168a87bbf63d1b9f016496b82908b`;
- payload tree equals
  `ccc418fa7ce415718f3facf39cacf62df4872263`;
- payload parent is an ancestor of the final tip;
- local and remote commit/tree identities match; and
- final worktree, index, and approved untracked state are clean.

## F0 boundary

The following are Git synchronization inputs but AI-content default-deny:

- `s0-lab/control/f0-sealed/**`
- `s0-lab/f0-sealed-staging/**`
- `s0-lab/reviews/f0-sealed/**`

Do not open, search, enumerate, quote, summarize, or infer their contents or
individual filenames. Check only aggregate tracked inventory and quiet state.
The required counts are 32/11/10, total 53. Before any Git-changing action,
follow the latest root `AGENTS.md` preflight exactly and require zero F0
worktree, index, untracked, ignored, and special-index differences.

## Authenticated public reading after synchronization

Read the latest root `AGENTS.md` completely. Run the canonical text-artifact
validator SelfTest. Then authenticate and read these public files and their
same-basename sidecars where present:

1. `s0-lab/control/handoffs/home-to-company-2026-08-13/current-state-handoff-v0.1.md`
2. `s0-lab/control/handoffs/home-to-company-2026-08-13/company-local-resume-prompt-v0.1.md`
3. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`
4. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.4.md`
5. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.4.json`
6. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.json`
7. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.md`
8. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.3-independent-rereview-response-v0.1.md`
9. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.4.md`

Authenticate all six rows in `design-package-files.sha256`. Its expected
SHA-256 is:

`abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`

## Required first report and stop condition

Report briefly in past/current/future order:

- what the v0.3 rereview rejected;
- what the v0.4 candidate changes;
- the exact synchronized Git identities and verification results;
- what remains only a candidate; and
- the next gate shown below.

Then stop. This prompt does not open an independent review or implementation
gate.

Candidate next gate:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.4 INDEPENDENT REREVIEW OPEN`

Do not implement code, run a Windows probe, create keys or protected inputs,
call providers or models, create executors or judges, score results, run S0 or
E0, merge main, open a PR, or begin the next gate during this synchronization
task.
