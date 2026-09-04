# Current project work ledger

- `ledger_kind`: derived CONTROL routing index
- `snapshot_date`: 2026-09-04 Asia/Seoul
- `evidence_baseline_main_commit`: `00491ddb9b656a901e62b31dc4a87d910dda2888`
- `evidence_baseline_main_tree`: `654285f032b30c389a97a6ee36c32dc98519376b`
- `publication_identity`: resolve the Git commit containing this ledger; do not self-record a future commit
- `authority_rule`: Git objects, root `AGENTS.md`, and the current user message override this ledger
- `structural_map`: `s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md`
- `F0_content_access`: none

## Global current-status namespaces

Version numbers belong to separate work packages and are not a global
sequence.

| Namespace | Current authenticated status | Exact current evidence | Claim boundary |
|---|---|---|---|
| Central-system product | Active design baseline `central-system-v2.1-s0-preparation` | `docs/tradition/central-system-v2-1-s0-preparation-baseline.md` | product, Project Brain integration, effect, safety, value, and transfer remain unimplemented or unvalidated |
| S0 public protocol | semantic v0.3, canonical document revision r1, final refreeze approved | `s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md` | no S0 execution or result |
| F0-PUBLIC question contract | v0.14 adopted as the current public design baseline after zero-finding review | `s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md` | no schema/runner, fixture, oracle, executor, scoring, or S0 execution |
| I0 and F0-PUBLIC public practice | bounded refreeze/content-freeze approved | `s0-lab/control/i0/i0-refreeze-gate-decision-v0.1.md` | no F0-SEALED access, executor run, scoring, or S0 result |
| E0 effect-test | v0.4 design review verdict `PASS-FOR-CONTROL-INTEGRATION-ONLY` | `docs/tradition/e0-effect-test/e0-independent-review-v0.4.md` | no CONTROL integration decision, implementation, execution, effect, safety, value, or transfer result |
| Public assembly rehearsal | see the structural map linked above | `s0-lab/control/workstreams/public-end-to-end-assembly-rehearsal.md` | preparation only; no official rehearsal or S0 result |

The candidate-era `commit_or_push_authorized: false` in the v0.7 status report
describes that historical candidate gate; Git at the evidence baseline contains
the accepted v0.7 directory. `s0-lab/setup-files.sha256`,
`s0-lab/session-registry.md`, and `s0-lab/i0/README.md` are initial setup or
candidate snapshots, not live status authorities.

## Documentation freshness audit disposition

On 2026-09-04, three isolated read-only audits compared the allowed general,
S0/control, and public-review document areas. No public review verdict-chain
conflict was found and no F0 content was accessed. Versioned designs,
candidates, reviews, decisions, handoffs, status reports, manifests, and
sidecars remain immutable historical evidence. Only mutable entry points and
this routing layer were selected for current-state correction. The temporary
audit reports are out-of-repository working material and are not authority.

## Current requested outcome

The requested outcome is a real PUBLIC end-to-end assembly rehearsal path on
the admitted Windows host. The latest opened prerequisite gate was:

```text
S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL LIVE IMPLEMENTATION PREREQUISITE PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.4 IMPLEMENTATION V0.4 OPEN
```

That gate reached the terminal CONTROL decision
`NOT-INTEGRATION-READY-DESIGN-V0.4-REVISION-REQUIRED`. Implementation and
bounded TEST evidence exist, but fresh independent rereview returned
`CORRECT/RETEST` with three MAJOR findings. No commit, push, main integration,
stage-70 probe, live assembly, official rehearsal, or S0 run occurred.

The previously opened downstream live-controller gate remains pending and
blocked. Its parked branch is historical local state and grants no authority
to bypass the prerequisite chain.

## Authenticated completion map

| Work package | Authenticated current state | Evidence | Routing result |
|---|---|---|---|
| Public assembly design | Effective design v0.5 accepted and integrated | `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-acceptance-plan-v0.5.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/control-integration-decision-v0.1.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/main-integration-decision-v0.1.md` | complete design prerequisite |
| Controller, verifier-parent observer, and same-process live consumer | Implementation v0.1 exists; 47 offline tests passed; live launch failed closed before output mutation | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md` | reuse; do not reimplement |
| Bounded assembly/runtime-preloader adapter | Implementation v0.1 integrated; `candidate_only=true`, `native_api_reachable=false`, `rehearsal_pass=false` | `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/public-end-to-end-runtime-preloader-bounded-integration-implementation-candidate-report-v0.1.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-control-integration-and-main-merge-decision-v0.1.md` | reuse as offline adapter only |
| Windows build-toolchain environment | v0.1 post-reboot x64 smoke compile/run passed on the named host | `s0-lab/assembly-rehearsal/windows-build-toolchain-environment-v0.1/STATUS_REPORT.md` | reuse environment; no general compiler, provenance, security, or production claim |
| Runtime-profile and neutral-preloader design | Design v0.4 received zero-finding design rereview, but implementation rereview exposed three contract gaps: the exact guard API list, evidence-schema binding/versioning, and physical ancestor/alias isolation | `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md`; `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-implementation-independent-rereview-result-preservation-record-v0.1.md` | design revision required before another implementation acceptance attempt |
| Runtime-profile and neutral-preloader implementation | v0.4 candidate implemented, compiled, materialized and bounded-tested; final TEST passed its stated scope, but fresh rereview returned `CORRECT/RETEST` with three MAJOR findings and CONTROL found it not integration-ready | `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/verification/public-assembly-runtime-profile-neutral-preloader-implementation-candidate-report-v0.4.md`; `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-implementation-control-integration-readiness-decision-v0.1.md` | rejected for integration; diagnostic evidence may inform the required design revision |
| CPython and jsonschema runtime materialization | v0.7 accepted, independently reviewed with 0/0/0 findings, and present at the evidence baseline | `s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/STATUS_REPORT.md` plus containing Git commit `2d7bb4f6b84b1b04c2b054d64edad7feaaeb3664` | complete; reuse exact pins and implementation |
| Real-Windows runtime/preloader platform probe | Not executed | `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.md` | blocked until v0.4 implementation and review complete |
| Live assembly connection and execution | Not executed | assembly v0.1 report plus runtime/preloader v0.4 acceptance plan | downstream gate remains pending |
| Official public assembly rehearsal decision | Not opened or executed | assembly v0.5 acceptance plan | closed |

## Required dependency order

```text
runtime materialization v0.7                         COMPLETE
assembly controller/observer/consumer v0.1          OFFLINE IMPLEMENTED
bounded assembly/runtime-preloader adapter v0.1      OFFLINE INTEGRATED
Windows build-toolchain environment v0.1             BOUNDED PASS
runtime-profile/neutral-preloader design v0.4        REVIEWED, CONTRACT GAPS FOUND IN IMPLEMENTATION REREVIEW
                  \          |          /
                   \         |         /
                    v        v        v
runtime-profile/neutral-preloader implementation v0.4   BUILT + BOUNDED-TESTED, NOT INTEGRATION READY
                |
                v
fresh implementation rereview                           CORRECT/RETEST, 3 MAJOR
                |
                v
runtime-profile/neutral-preloader design revision       REQUIRED
                |
                v
corrected implementation + fresh review                 REQUIRED
                |
                v
bounded real-Windows runtime/preloader platform probe  REQUIRED
                |
                v
live assembly connection and same-process decision     PENDING
                |
                v
official public assembly rehearsal consideration       CLOSED
```

The existing controller must be reused. Runtime materialization does not
replace the neutral preloader: v0.7 supplies authenticated Python and package
bytes, while the preloader must authenticate the executable/runtime/profile
before import and construct the exact Windows process and handle-list launch.

## Structurally eligible next work package

Revision of the runtime-profile and neutral-preloader design contract is the
only structurally eligible next work package. The revision must close the
exact guard semantic-call inventory, version and fully freeze every evidence
serialization binding, and define physical ancestor/reparse/volume identity
rules for materializer isolation. Its candidate/version is not yet frozen;
this ledger does not invent one or open a gate.

Before presenting a gate phrase, CONTROL must redo the value-first assessment
in ordinary language: core purpose, concrete blocker, cheapest standard
alternative, why that alternative is insufficient, useful output and reuse,
realistic best/worst time, and stop/discard condition. It must then freeze role
capacity, exact pins and allowlists, and the complete pre-CODE adversarial
checklist for the revised design and any later implementation.

The already opened downstream live-controller gate remains blocked and cannot
absorb the preloader implementation or Windows platform probe.

## Local preservation incident

One task-owned temporary worktree developed 1,393 tracked unstaged deletions,
including aggregate deletions of all 32/11/10 F0 preservation-path entries.
The cause is unverified. No restore, reset, clean, prune, or deletion was
performed on that worktree; it remains quarantined and is not evidence for the
candidate decision. A new clone from live `origin/main` was authenticated at
the exact baseline commit/tree and 32/11/10 F0 inventory before checkout. The
25 approved task files were transferred byte-for-byte into that clean clone,
and four final rereview/decision files were authored there by DOCUMENTATION.
With this ledger and workstream update, the clean clone has 31 task-owned
status entries. Its F0 paths are quiet with zero untracked, ignored,
skip-worktree, or assume-unchanged anomalies, and it has zero outside-task
status entries.

## Update triggers

CONTROL must update this ledger before recommending another technical gate
after any of the following: candidate acceptance or rejection, prerequisite
completion, main integration, discard decision, gate blockage, or
project-wide operating-policy correction. Every update must pin the exact
evidence-baseline main commit/tree and reauthenticate the evidence paths used
by changed rows. The containing Git commit supplies this ledger's publication
identity; do not create a second self-referential update merely to record it.
The matching workstream map must be updated in the same change whenever a
stage, dependency edge, canonical path, or next eligible work package changes.
