# Public end-to-end assembly rehearsal workstream

- `workstream_id`: `public-end-to-end-assembly-rehearsal`
- `evidence_baseline_main_commit`: `00491ddb9b656a901e62b31dc4a87d910dda2888`
- `evidence_baseline_main_tree`: `654285f032b30c389a97a6ee36c32dc98519376b`
- `evidence_baseline_role`: pre-integration `main` base
- `design_v0.5_integration_identity`: resolve the Git commit containing this map and the design-only integration record
- `live_main_inclusion_rule`: established only when authenticated live `main` contains that containing commit
- `publication_identity`: resolve the Git commit containing this map
- `current_outcome`: real PUBLIC end-to-end assembly rehearsal path on the admitted Windows host
- `routing_state`: `DESIGN-V0.5-DESIGN-ONLY-INTEGRATION-BY-CONTAINING-COMMIT`
- `F0_content_access`: none

## Ordered stages

| Order | Stage | Local version | State | Exact evidence path | Depends on |
|---:|---|---|---|---|---|
| 10 | Public assembly design | v0.5 | complete, reviewed, integrated | `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-acceptance-plan-v0.5.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/control-integration-decision-v0.1.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/main-integration-decision-v0.1.md` | none |
| 20 | Controller, verifier-parent observer, live consumer | v0.1 | offline implemented; reuse | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md` | 10 |
| 25 | Bounded assembly/runtime-preloader adapter | v0.1 | offline integrated; reuse | `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/public-end-to-end-runtime-preloader-bounded-integration-implementation-candidate-report-v0.1.md`; `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-control-integration-and-main-merge-decision-v0.1.md` | 20, runtime/preloader v0.3 |
| 30 | CPython and jsonschema runtime materialization | v0.7 | complete, reviewed, present at evidence baseline | `s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/STATUS_REPORT.md`; current presence from Git commit `2d7bb4f6b84b1b04c2b054d64edad7feaaeb3664` | exact external pins |
| 35 | Windows build-toolchain environment | v0.1 | bounded post-reboot compile/run PASS; reuse | `s0-lab/assembly-rehearsal/windows-build-toolchain-environment-v0.1/STATUS_REPORT.md` | none |
| 40 | Runtime-profile and neutral-preloader design | v0.5 | terminal `PASS`; design-only integration identity is the containing Git commit; live-main inclusion requires authenticated containment | `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/design-package-files.sha256`; `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/v0.5-independent-rereview2-result-preservation-record-v0.1.md`; `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/v0.5-control-integration-readiness-decision-v0.1.md`; `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/v0.5-design-only-main-integration-record-v0.1.md` | 10, 20 |
| 50 | Runtime-profile and neutral-preloader implementation | candidate v0.4; future corrected candidate | v0.4 remains rejected historical evidence; its 19 source files are excluded from design-only integration and a corrected candidate is separately gated after authenticated live-main inclusion | `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/verification/implementation-files.sha256`; `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/verification/public-assembly-runtime-profile-neutral-preloader-implementation-candidate-report-v0.4.md`; `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-implementation-control-integration-readiness-decision-v0.1.md`; excluded source rows remain at commit `440f4342bb27398c6f2a4131d5518f2b55722f4c` | 25, 30, 35, live-main-included 40 |
| 60 | Runtime-profile/preloader implementation review | v0.4 historical; future fresh review | v0.4 rereview was `CORRECT/RETEST` with three MAJOR findings; corrected implementation requires fresh TEST and independent review | `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-implementation-independent-rereview-result-preservation-record-v0.1.md` | corrected 50 |
| 70 | Bounded real-Windows runtime/preloader platform probe | future | blocked | `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.5.md` | fresh accepted 60 |
| 80 | Live assembly connection and same-process decision | implementation v0.1 downstream gate | pending | no live artifact | 20, 30, 70 |
| 90 | Official public assembly rehearsal consideration | future | closed | no result artifact | 80 |

## Dependency edges

```text
10 -> 20
20 -> 25
10 -> 40
20 -> 40
25 + 30 + 35 + 40 -> 50 -> 60
60 -- CORRECT/RETEST --> revised 40 v0.5 -- PASS --> design-only containing commit
authenticated live-main containment of 40 -> separately gated corrected 50 -> fresh TEST/review 60 -> 70
20 + 30 + 70 -> 80 -> 90
```

Stage 20 already contains the controller, observer, Windows publication
adapter, witness, and same-process consumer. It must be reused rather than
implemented again. Stage 25 already connects the offline assembly and
runtime/preloader APIs and must also be reused. Stage 30 supplies authenticated
Python and package bytes, and stage 35 supplies a bounded native build
environment, but neither performs stage 50 process creation, handle-list
construction, or pre-import admission. The v0.4 stage-50 candidate exercised
those mechanisms, but stage-60 rereview found three MAJOR contract gaps. The
successor v0.5 design closes those gaps at the design-contract level and has a
terminal CONTROL integration-ready decision. Its design-only integration
identity is the containing Git commit; live-main inclusion exists only after
authenticated containment. The selective integration excludes all 19 v0.4
implementation source files while retaining their manifest and report as
historical rejection evidence. It does not validate or change the rejected
implementation. Stage 80 cannot start from the completed components or that
rejected candidate.

## Next eligible work package

Once authenticated live `main` contains the Git commit carrying this map and
the design-only integration record, the next technical work package is a
separately opened corrected stage-50 implementation candidate based on v0.5.
No candidate or version is selected here, and no literal gate phrase is
established. The future candidate must receive fresh TEST/verification and
fresh independent review before stage 70. Before authenticated live-main
containment, the technical package remains ineligible. Stage 70, stage 80,
and official rehearsal consideration remain downstream and separately gated.

The already opened stage-80 gate remains pending. It does not authorize stage
50 or stage 70 and must not absorb them.

## Authority and updates

Git objects, the latest root `AGENTS.md`, and the current user message override
this derived map. Candidate-time fields in the v0.7 status file remain
historical; the evidence-baseline Git commit proves its current presence.
CONTROL must update this map and
`s0-lab/control/CURRENT-WORK-LEDGER.md` together after any stage acceptance,
rejection, discard, prerequisite completion, main integration, or routing
correction. The containing commit is the map's publication identity, so a
second self-referential hash update is neither required nor allowed.
