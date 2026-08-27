# CONTROL integration-readiness decision: external artifact authority acquisition v0.1

## Gate and role boundary

**FACT — exact current gate:** `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL ARTIFACT AUTHORITY ACQUISITION V0.1 CONTROL INTEGRATION READINESS DECISION OPEN`.

**FACT — role disposition:** CONTROL authenticated the inputs and made the decision recorded below. DOCUMENTATION writes this decision record from CONTROL-authenticated facts and existing public evidence; DOCUMENTATION supplies no approval or review verdict of its own. CODE IMPLEMENTATION, TEST/VERIFICATION, and INDEPENDENT REVIEW have no task-owned artifact or action in this decision gate and are explicitly not reabsorbed or rerun.

**NONCLAIM:** this record does not open an implementation, test, review, PR, merge, release, v0.4 correction, or downstream execution gate.

## Authenticated candidate identity

- **FACT:** branch `codex/s0-external-artifact-authority-acquisition-v01` was clean with stash count `0` at CONTROL authentication.
- **FACT:** candidate commit `38c67b3aed7e9caf18e950ee7d49b7b2c7c722d4` has tree `c7491099cefa28dd78fbe50e60b18be14d4a2ac7` and sole parent `b469b71f3e1dd23b39b9992532785c9d6a57363d`.
- **FACT:** at decision time, live `origin/codex/s0-external-artifact-authority-acquisition-v01` equaled the candidate commit and live `origin/main` equaled its sole parent. The candidate was therefore an exact one-commit linear fast-forward candidate at that time.
- **FACT:** the commit changes exactly `24` candidate files and `0` other paths; the worktree was clean. The three PUBLIC-GIT F0 inventories were `32 / 11 / 10`, and candidate-versus-parent F0 changes were `0 / 0 / 0`. No external runtime root is committed.
- **FACT:** the candidate reports and manifest record the result-preservation repository identity at parent `b469b71f3e1dd23b39b9992532785c9d6a57363d`; CONTROL authenticated the final 24-file candidate as its sole child. This decision is pinned to candidate commit `38c67b3aed7e9caf18e950ee7d49b7b2c7c722d4` and tree `c7491099cefa28dd78fbe50e60b18be14d4a2ac7`, not to a moving branch name.

**REAUTHENTICATION REQUIREMENT:** every moving branch or remote relation above is time-bound. Before any future PR, fast-forward, merge, publication, or other Git action, CONTROL must reauthenticate the exact commit, tree, parent, live tips, change set, worktree state, F0 invariants, and applicable authority.

## Authenticated evidence and results

**FACT — exact public result artifacts:**

- `ADVERSARIAL_CHECKLIST.md`: size `26210`, SHA-256 `783fb168748f3405f9b2fb48b2f32c38a25a43021e2c70cdd355b0f5664a3752`;
- `STATUS_REPORT.md`: size `16379`, SHA-256 `841a94fde093ae41d618a45606db1aeef85fd4ee956527513d81c3c7f70913fe`;
- `LIVE_BLOCKER_REPORT.md`: size `12308`, SHA-256 `bfdb01c7adbf1f49756f14a6bc250f74ed6e061ea63e497d49e9b5d8addbbd15`;
- `evidence-manifest.json`: size `37688`, SHA-256 `b7896b00ba187aa431ff8f81840259f91f58f4dff7c33f5589d9ea1b33b6f084`.

**FACT:** all four same-basename sidecars are exact and canonical. These artifacts preserve the bounded threat checklist, result and blocker state, hashes, sizes, commands, evidence pointers, role boundaries, and nonclaims. Their embedded candidate result is correction closure only.

**RESULT — supplied TEST/VERIFICATION evidence:** the offline suite passed `44/44`; the live-harness self-test passed with network use false and native trust false; the candidate verifier passed over `32` frozen inputs with stable pre/post bytes and both sentinels true; retained-root authentication passed `18/18` with final authority false. TEST/VERIFICATION was not rerun in this decision gate.

**RESULT — preserved independent review evidence:** the exact human verdict is `PASS — ACCEPT CORRECTION CLOSURE`, with finding counts `BLOCKING 0 / MAJOR 0 / MINOR 0`. CONTROL further authenticated that final-byte review of the one-LF, pin, and documentation cascade preserved that result with counts `0 / 0 / 0`. DOCUMENTATION preserves those supplied results and makes no independent finding or verdict.

## CONTROL decision

**CONTROL DECISION:** `CONTROL-INTEGRATION-READY-FOR-BOUNDED-EXTERNAL-ARTIFACT-AUTHORITY-ACQUISITION-V0.1-NO-BUILD-TOOLS-OR-FINAL-AUTHORITY`.

**DECISION MEANING:** the repository commit is fit to enter a separately authorized PR or fast-forward integration gate as bounded fail-closed acquisition, pin, and closure infrastructure only. It does not grant a Build Tools proposal or Build Tools authority, environment completion, execution authority, final authority, build or runtime authority, rehearsal completion, or S0.

**BOUNDED INFERENCE:** the exact one-commit relation, exact 24-file scope, preserved F0 tree, authenticated artifact set, supplied test results, and preserved independent correction-closure result support CONTROL's bounded integration-readiness decision. This inference does not remove any blocker or promote any unverified prerequisite into authority.

## Permanent blockers and required nonclaims

**BLOCKED OR UNVERIFIED:** `BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED`; `BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING`; the proposed Build Tools pin is not CONTROL-promoted; CPython Sigstore cryptographic verification is unavailable; host runtime authority, network producer authority, acquisition producer authority, effective trust, supplier assurance, offline toolchain layout, and runtime profile remain unverified.

**SEPARATE HISTORICAL DIAGNOSTIC:** the provider-owned `hAdditionalStore` condition remains a distinct historical diagnosis. It is not an artifact signature failure and does not close or replace the current transitive-closure blocker. Any v0.4 correction requires a separately opened future verifier candidate and gate; this record invents no future version or gate phrase.

**REQUIRED NONCLAIM:** no acquired byte was executed, imported, installed, compiled, or linked. No final or process authority, installation, offline toolchain layout, build, runtime, rehearsal, S0, E0, central system, Project Brain integration, operational safety, economic value, or model-to-model transfer was implemented or validated by this decision.

**AUTHORITY LIMIT:** this decision authorizes no PR, main merge, commit, push, release, v0.4 change, next gate, F0 content access, or external-runtime publication by itself.
