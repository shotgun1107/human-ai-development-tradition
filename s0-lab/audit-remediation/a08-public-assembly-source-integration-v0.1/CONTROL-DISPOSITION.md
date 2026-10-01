# A08 CONTROL disposition

**CONTROL decision: ACCEPT the bounded 27-source developmental integration only.** Candidate `a08-public-assembly-source-integration-v0.1` is retained as a complete public source baseline for later authorized development. It is not live execution authority. This records CONTROL `/root`'s decision; DOCUMENTATION does not issue an independent verdict.

The accepted packet is the exact 39-entry [artifact manifest](artifact-files.sha256), SHA-256 `459399ba34b856601ebaa16bee52c996179e72c44a743393661da928688e5503`. CONTROL reauthenticated every entry after the final review, and DOCUMENTATION confirmed them unchanged before this disposition. Branch `codex/windows-build-toolchain-environment-v0.1`, HEAD `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`, and tree `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` remain pinned. The original [README](README.md), [scope/checklist](SCOPE-AND-CHECKLIST.md), their pending-at-freeze statements, and the manifest remain unchanged. This disposition and its sidecar are separate later records, excluded from that frozen manifest.

## Basis of acceptance

CONTROL relays the fresh read-only review by `/root/audit_a08_review`, created with `fork_turns=none`, `gpt-5.6-sol`, ultra reasoning. It completed a primary source assessment followed by Phase 2 evidence/document assessment and returned **PASS, zero findings at every severity**. Its reported basis was:

- Exact 27-source inventory without shadow/reparse entries, byte comparison of 25 unchanged originals plus two A01 corrections, and both full original initializers.
- F-02 source handling of `None` mode and third-position flags, matched to 18 actual own-file `O_TEMPORARY` denials with preserved bytes, normal reads, pending writes, and denial latch observations.
- F-04 EOF-38-only termination, last-error capture, `FindClose` handling, and alternate-stream rejection, matched to 36 API-double observations.
- Twenty-five candidate module origins, two compile-only sentinel-installing modules, 47 retained original unit purposes, unchanged original authority roots, and retained live refusal. The diagnostic `'a' * 64` implementation pin confers no authority.
- Authenticated TEST evidence of 77 tests and 485 subtests, zero failures/errors/skips, 34 children, 250 equal pre/post/current input hashes, zero unit temporary residue, and identical retained `attempt-001` result duplicates. Actual TEST process exit 0 is attributed execution evidence, not a reviewer rerun. Canonical SelfTest and both frozen Markdown/sidecar checks passed.

## Review process and limitations

The reviewer first assessed source, then received the released evidence and documentation. This is source-first review followed by evidence exposure, not an outcome-blind final review or proof of enforced filesystem isolation. Review chronology, other role actions, and execution facts are authenticated or attributed handoff evidence; the reviewer did not reconstruct other agents' transcripts. CONTROL relays that the reviewer accessed no denied/F0 inputs and performed no network/provider calls, candidate/test/native execution, edits, or Git actions.

The reviewer reported one malformed initial combined-path validator invocation that validated nothing. Subsequent separate per-file invocations passed without writes. This is a review tool-invocation limitation, not a candidate failure or another correction cycle. The earlier stopped DOCUMENTATION role incident remains attributed in the README; replacing that role prospectively did not excuse or retroactively validate the earlier handoff.

## Continuing boundaries

Acceptance establishes only the frozen source integration and bounded diagnostics. Historical/native Windows execution, live authentication, OS sandboxing, actual ADS exploitation, full interpreter/stdlib/native/import closure, hostile globals or arbitrary caller minting, concurrency, and complete ACL/volume/root/symlink/junction/reparse/rename/replacement/retained-handle/repository-exclusion/TOCTOU behavior remain unverified. This includes final output/evidence writes and evidence-producer security. No runtime preload or native/live rehearsal is authorized by acceptance.

No S0/E0 creation, execution or scoring, central-system implementation, Project Brain integration, operational safety, economic value, or model-to-model transfer claim follows. The baseline remains `central-system-v2.1-s0-preparation`. This decision opens no F0, provider/model, broader implementation, Git publication, installation, deletion, or new gate. The overall maintenance closeout remains a separate pending final record/check.

DOCUMENTATION's final action is limited to this file and `CONTROL-DISPOSITION.sha256`, using the pinned canonical text validator for SelfTest and individual-file validation. The 39 frozen artifacts and their manifest are preserved; no candidate/test rerun or other file modification accompanies this disposition.
