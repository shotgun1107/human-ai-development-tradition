# A08 public assembly source integration v0.1

Status at this documentation freeze: **TEST PASS / REVIEW PENDING**. This packet provides the complete 27-file public assembly source namespace for later development, with the two A01 v0.2 corrections integrated. It is a bounded source-integration result; CONTROL has not issued a final disposition.

## Purpose and composition

This is core project preparation: the partial correction packet lacked the complete assembly namespace. Standard exact file copying and existing public unit regressions were sufficient; no new verification framework was needed. CODE copied 25 original sources unchanged and substituted only `runtime_guard.py` (F-02) and `win32.py` (F-04) from A01 v0.2. Both full original package initializers are retained, including the verifier's consumer and observer exports. The original authority and implementation-manifest paths remain unchanged. Relocation, presence, import, and the diagnostic `IMPLEMENTATION_PIN = 'a' * 64` confer no live authority.

`artifact-files.sha256` inventories exactly 39 candidate-relative paths in ASCII ordinal order: 27 implementation sources, six test/runner sources, two canonical TEST outputs, and the two Markdown documents with their two sidecars. It excludes itself, any future disposition, and the preserved first-attempt JSON/stdout duplicates under `verification/scratch/attempt-001/`. It is an authoritative released-artifact inventory, not an inventory of every file below this directory. No scratch cleanup is authorized by this document.

## Authenticated identity and inputs

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`. Candidate root: `s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1`.

| Input | Frozen value |
| --- | --- |
| Branch | `codex/windows-build-toolchain-environment-v0.1` |
| HEAD | `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` |
| HEAD tree | `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` |
| Root `AGENTS.md` SHA-256 | `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` |
| Original `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256` | `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623` |
| A01 `s0-lab/audit-remediation/a01-public-boundaries-v0.2/artifact-files.sha256` | `c26f8a02c4dc306e9639dfefd26ee8e41793ffb45998b84c7c2841490772f972` |
| Candidate `runtime_guard.py` | `811f1df27a44d70948f3e37fedcba976189fd5b58ff61a6e029c14d74c768f7a` |
| Candidate `win32.py` | `dd250e352431390885adfb4a95244d96622bc9546bd003f585b1afb579143f68` |
| Full candidate package initializer | `e3d5d04f3b66673145aaf03646d78c644095e6f2e8fdbaab7ac0ffd8352015ff` |
| Full verifier package initializer | `55d0fa7ba416b6cabe8f28a934f4123b6a6ad59ebdf344239e6c72e1c989db0e` |
| Base Python executable | `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe` |
| Base Python SHA-256 | `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` |
| Canonical text validator `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

The original 32-entry manifest releases only its 27 implementation entries for source content in this DOCUMENTATION role. The A01 manifest releases only the two replacement sources for content. The authenticated TEST JSON supplies 250 exact paths and hashes for preservation comparison only; it does not release historical schemas, contracts, reviews, or other old artifacts for content reading. Unsafe or protected inventory paths must be rejected without printing their names. Existing frozen inputs and historical expected hashes are preserved.

## Bounded TEST evidence

`verification/test-results.json` has SHA-256 `bbe7fbeb52f87b8519e7ff92657f52c2f4dd53fe6cc849075e13349db2f0df46`; `verification/test-stdout.txt` has SHA-256 `1afbf1dec83434649f066c0a507e604a0a36624bffe9bb0ef50b2f98da1f0d5c`. TEST reported first-run process exit 0 and `BOUNDED-PUBLIC-UNIT-INTEGRATION-PASS`. The authenticated files record attempt 1, 77 tests, 485 subtests, zero failures, zero errors, and zero skips. There was no TEST failure/correction cycle.

| Evidence group | Recorded result and limit |
| --- | --- |
| Retained original unit purposes | 47: candidate 22, harness 8, verifier 17; FakeBackend and public unit parameters remain diagnostic. |
| Added regression and integration coverage | Runtime guard 17, stream inventory 9, integration 4. |
| Source integration | Exact 27-file implementation inventory, 25 original hashes plus two substitutions, full initializers, and unchanged authority roots. |
| Compilation/imports | All 27 sources compiled; 25 safe modules actually imported from the candidate. Candidate `child.py` and `__main__.py` were compiled only. |
| Child observations | 34 processes: 31 runtime checks, two sentinel checks, and one bootstrap refusal. Thirty-three exited 0; bootstrap exited the expected 2 with `BOOTSTRAP_FAILURE`. Timeouts were 10 or 15 seconds. |
| F-02 Windows own-file checks | All 18 actual `O_TEMPORARY` child attempts were denied and their tracked own-file bytes remained unchanged; ordinary reads and permitted pending writes also passed. This is not an OS sandbox result. |
| F-04 stream checks | 36 API-double observations covering EOF, error capture, alternate/multiple entries, and close failures; no native backend construction or actual ADS exploit was tested. |
| Preservation and scratch | 250 admitted input hashes matched before/after, and DOCUMENTATION authenticated their current hashes. Unit-test temporary residue count was zero; preserved attempt evidence remains. |

The recorded command, run by TEST from the repository root, was:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a08-public-assembly-source-integration-v0.1/tests/verify_integration.py'
```

Python reported 3.12.10 with isolated mode, no site initialization, UTF-8 mode, and bytecode writes disabled. The runner requires the frozen branch, HEAD, tree, interpreter, and input pins. Do not alter expected hashes to run it after an environment or policy change. A later authorized run creates the next `verification/scratch/attempt-NNN/` directory. It writes the top-level canonical JSON/stdout only for a successful run when `verification/test-results.json` does not already exist; those writes use exclusive creation. Therefore a rerun does not refresh this frozen result. Preserve existing evidence and identify any separately authorized result explicitly.

## Role and procedural record

CONTROL `/root` froze the scope and bounded checklist in the CODE handoff. CODE `/root/audit_a08_code` performed exact copying; TEST `/root/audit_a08_test` authored and ran the released verification. DOCUMENTATION `/root/audit_a08_docs_fresh` authenticated inputs and authored only this README, `SCOPE-AND-CHECKLIST.md`, their sidecars, and `artifact-files.sha256`. Fresh read-only INDEPENDENT REVIEW is planned as `/root/audit_a08_review`, `gpt-5.6-sol` at ultra reasoning, with primary source assessment before TEST evidence and documentation. It remains pending. No role here issues its own independent approval.

CONTROL reports that the initial CODE filename filter omitted digits and rejected `win32.py` before any writes; the copy filter was corrected and the released source bytes required no further edits. This was a copy-preflight correction, not a test failure or independent review cycle.

CONTROL also reports a DOCUMENTATION handoff incident: the previous role `/root/audit_a08_docs` authenticated identity/input pins, then read the first 130 lines of the pinned public canonical validator under a handoff ambiguously narrowed to execution only. It reported the possible action-allowlist overrun and stopped before writing any of the five outputs. No F0 content, old verdict content, candidate execution, or writes were reported. CONTROL stopped that role and assigned this fresh role explicit validator source-read and canonical validation permission. This prospective replacement does not retroactively validate the earlier order. Source and TEST bytes are unchanged; this role did not inspect the earlier agent transcript. These are attributed procedural reports, not independently reconstructed events.

## Limits and next decision

See `SCOPE-AND-CHECKLIST.md` for the bounded threat and claim mapping. Live entry refusal is retained. Native publication, runtime preload, historical runtime equivalence, hostile interpreter/stdlib/native/import closure, hostile process-global mutation, arbitrary caller minting, concurrency, and the full Windows path lifecycle remain unverified. Hash comparison and ordinary scratch containment do not prove those properties or a trusted evidence producer.

No S0/E0 fixture or hidden oracle was created, and this gate did not run or score S0/E0, call a model/provider, or establish central-system implementation, Project Brain integration, operational safety, economic value, or model-to-model transfer. The repository remains at `central-system-v2.1-s0-preparation`. No Git staging, commit, push, PR, merge, installation, deletion, or new access gate is authorized by this packet. The next action is the separately assigned fresh review, followed by CONTROL's decision within the existing scope.
