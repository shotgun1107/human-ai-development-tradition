# A01 v0.1 CONTROL disposition

Date: 2026-09-16. Candidate: `a01-public-boundaries-v0.1`. Classification: auxiliary tooling/evidence work.

CONTROL decision: **REJECT-COMBINED-CANDIDATE**. The F-02 acceptance blocker remains open; the combined package is not approved for integration or publication. Further correction is stopped at the 30-minute auxiliary-work limit pending an explicit user cost decision.

## Frozen identity

- Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.
- Branch: `codex/windows-build-toolchain-environment-v0.1`.
- HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
- `artifact-files.sha256`: `d583db794052e751a03200bee65a278fa06c2dc943011482e58d9c34f48e654a`.
- `REMEDIATION-REPORT.md`: `bbb14419ae246d541190496cab2966d528717f5ae950b0c22429dd46746b765f`.
- Root `AGENTS.md`: `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065`.

The commit/tree identify the repository baseline; the manifest pins the separate candidate working files. This record and its sidecar are outside the original 17-file manifest. The manifest and all 17 entries remain unchanged; their historical PENDING statements describe the packet before this disposition.

## Supplied independent assessment

CONTROL supplied the primary **REJECT/CORRECT** assessment from fresh read-only reviewer `/root/audit_a01_review_resumed`. The earlier paused review issued no verdict and was replaced. The reviewer reported authenticating the 27-file packet, including the 17 manifest entries, seven original implementation inputs, manifest, root policy and validator, plus Git identity. This replacement does not establish enforced information isolation through session reset.

The high-severity acceptance blocker concerns `implementation/s0_public_assembly_candidate/runtime_guard.py`, lines 213-218 and 239-240: mode `None` accepts nonnegative integer flags, while the mutating mask covers only `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_TRUNC` and `O_APPEND`. Windows `O_TEMPORARY` has delete-on-close behavior outside that mask, so an approved-input open can be classified as a read, contrary to the existing write/allowlist contract. The reviewer identified the missing discriminator in `tests/test_runtime_guard.py`, lines 235-248. This is static reasoning, not an executed deletion diagnostic.

If continuation is explicitly authorized, TEST/VERIFICATION should discriminate this behavior using owned benign approved scratch, expecting `BoundaryViolation`, a latched denial and intact bytes. This record authorizes neither that diagnostic nor a CODE correction.

The reviewer reported no actionable finding for the F-04 stream correction in `implementation/s0_public_assembly_verifier/win32.py` around line 307: EOF 38, error capture, close failure, call counts and AR failure classes matched the bounded contract/evidence. CONTROL preserves that bounded evidence without approving the combined package or integration.

## Retained evidence and stop condition

Authenticated TEST evidence remains 23 tests and 88 subtests, zero failures/errors/skips, 13 isolated child observations, 36 stream API-double scenarios, recorded import paths and zero scratch remaining. These counts overlap. Existing cases remain valid bounded observations; they did not cover the newly identified flag.

Evidence pins: `verification/test-results.json` = `b10e144c25110ed7880975e62295ac722939e14b1f441e687c6b0b1ac7c32d1e`; `verification/test-stdout.txt` = `3f519ec90d3c65326190976611392dc972016c2cdb199776dc80e174738f0235`.

CONTROL reported that the auxiliary limit was reached and offered a 10-20 minute extension; no user decision had been received at this record's handoff. The current fallback is to retain the rejected candidate and bounded evidence without further diagnostics, correction or integration. The opaque unclassified-status count of one remains a CONTROL-reported publication blocker, not a new inspection by DOCUMENTATION.

Replacement DOCUMENTATION role `/root/audit_a01_disposition_docs` records the supplied review and CONTROL decision after the prior documentation session became unavailable following the user pause. It authenticated only its allowed inputs and the manifest entries' hashes, authored only this record and sidecar, and makes no independent approval or review claim. It did not inspect source/test contents or rerun substantive tests. Canonical text/sidecar validation outcomes are returned separately to CONTROL.

No full native/controller/security, complete-system, operational-safety, economic-value, model-transfer or S0/E0 claim follows. F0 content, hidden oracles, fixtures, S0/E0 execution/scoring, real providers, system installation/deletion and Git mutation remain outside this record's authority. The project remains in `central-system-v2.1-s0-preparation`.
