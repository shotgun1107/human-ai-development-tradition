# F-03 source recovery — 2026-09-16

This is a CONTROL/maintenance preservation archive, not a runnable candidate or an independent-review input. Links and public presence do not expand a role allowlist. Do not import these modules, place this directory on an execution/search path, or invoke its build/materialization scripts as part of this recovery.

## Authenticated result

- Recovered original v0.5 implementation: **20 files, 324,283 bytes**, each matching its historical SHA-256.
- Recovered original inventory: `verification/implementation-source-files-v0.5.sha256`, **3,632 bytes**, SHA-256 `498a7190238f927817010b9506f53130af93f14271252ed19e785faa6a2f0467`.
- The inventory keeps its original repository-relative paths. For this archive's integrity check only, its prefix `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/` maps to this directory's `implementation/`. It was not rewritten to point to this archive.
- Missing JSON inputs were restored: `control-envelope-v0.5.schema.json` (5,761 bytes, `b9e7d6131202f47522e4f3055199df71f5e5ff8737362b7c97337350646d1dc1`) and `runtime-authority-v0.5.json` (10,815 bytes, `664f0950e903ef508082fcd9465f895e16c08418bee94f3cd3e86e85dd248642`).
- No expected historical hash was changed to obtain a match. No recovered code was imported, compiled, or executed.

## Public provenance

Metadata-only discovery was limited to the 2026-09-08 session directory and the known project parent `01a03b3b-8bf3-74d0-9833-a89d29ce487f`. Other-project conversation bodies, private reasoning, guardian content, and F0 content were not recovery inputs. Only exact approved public source records were selected; whole conversations are not copied here.

| Route | Exact material / evidence |
| --- | --- |
| Twelve original files from public file changes | Source author `/root/rpnp_impl_v05_code_current_gate`, session `01a07ea0-d557-7023-87a2-11c1cc0c2efb`, local log `C:/Users/SSAFY/.codex/sessions/2026/09/08/rollout-2026-09-08T10-27-44-01a07ea0-d557-7023-87a2-11c1cc0c2efb.jsonl`. Only completed public `FileChange` records for exact implementation paths were used. Initial contents and textual changes were reconstructed as data, never by executing historical commands. |
| Six existing authenticated snapshots | Exact copies from `../source-snapshot-2026-09-16/`: `build.ps1`, `s0_neutral_preloader_v0_5.cpp`, `canonical.py`, `profile.py`, `semantic.py`, and `source_audit.py`, mapped into their original native/package subdirectories. Originals remain unchanged because prior evidence references them. |
| Two numbered public source reads | `s0_public_runtime_preloader/__init__.py`: all 71 lines from public output at audit-log row 1351. `s0_public_runtime_preloader/evidence.py`: all 509 lines from public outputs at rows 787 and 795. Audit log: `C:/Users/SSAFY/.codex/sessions/2026/09/09/rollout-2026-09-09T11-05-28-01a083e9-bc25-7d40-a70f-a794100e24c7.jsonl`. Matching path, SHA-256 and byte-count headers were required before accepting numbered lines. |
| Original inventory | Reassembled from the final exact 20 path/digest rows in ordinal path order, then authenticated against the already known original inventory hash and byte count. |

Public author-log change rows: envelope JSON 93/299; authority JSON 93/283/347; build contract 93/220/347; materialize script 93/220; guard C++ 93/182/318; materializer C++ 206/318/794/840; header 93/182; errors 93; integration 93/283; preloader 93/241/283/318; schema 93; bootstrap 93/347.

The earlier author summary carried an intermediate materializer (49,685 bytes, hash beginning `72007307`), not the final file. The final source is **49,712 bytes**, SHA-256 `2ec252ed9d15d12e0447244f1bbd138f922edcc27a53d626c5c71ac60d64d691`, recovered through the later public change at row 840 and independently corroborated by public audit-read headers at rows 718/725/732. The final original inventory authenticates this selection.

Direct change replay did not resolve every Python file's intermediate context. Unmatched intermediate reconstructions were not saved or labeled recovered; already authenticated snapshots and exact numbered public reads supplied the remaining files. Final acceptance here is byte identity, not a claim that the recovery transformation is a new security verifier.

## Limits and remaining work

F-03 remains unresolved. This archive does not restore the complete historical R/B runtime/static input material, binary/environment evidence, or demonstrate historical P4 validation. The profile-composition contradiction is not corrected merely by recovering these sources. Do not remove an equality, rebind current runtime bytes to a historical pin, or claim implementation/native lifecycle PASS from this archive.

The separate accepted audit-remediation candidates remain distinct and unchanged; these original sources intentionally retain their historical behavior. No S0/E0 fixture, oracle, scoring, provider call, installation, full native run, or broader security/value claim was opened.

Read-only Git identity remained branch `codex/windows-build-toolchain-environment-v0.1`, HEAD `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`, tree `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. The opaque unclassified status item was not inspected or waived. No staging, commit, push, history change, or deletion was performed.

This recovery was performed directly by CONTROL as ordinary preservation/authentication, not as candidate CODE, TEST, or INDEPENDENT REVIEW. Any technical correction must separately freeze the exact required inputs, ownership, checks and permitted claims under root `AGENTS.md`.
