# A06 runtime source integration v0.1

Status at documentation freeze: **SOURCE INTEGRATION VERIFIED BY TEST; INDEPENDENT REVIEW PENDING**. This is a complete 20-file source development input combining the bounded F01, F03, and F08 corrections. It is not a rebuilt or accepted native executable package. CONTROL must record any later review and disposition separately; this frozen README does not anticipate that decision.

The active design baseline remains `central-system-v2.1-s0-preparation`. Completion of this candidate does not complete the broader audit/maintenance goal, open feature development, or validate S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer.

## Purpose and value

This is **core development-preparation integration**: provide one coherent source input for later authorized development without losing either overlapping correction. A05 alone retained the old F08 path helper; A02 alone lacked the F03 profile composition changes. The selected standard file-copy and exact-diff union preserves both, including their changes to the same `source_audit.py` module. It introduces no downloader, verifier product, trust service, or architectural redesign.

The expected reusable output is the 20-file source tree and bounded public regression evidence. CONTROL estimated 40-90 minutes for the complete role sequence, with progress/value checkpoints around 30 minutes. Elapsed time alone is not a stop condition. Missing historical native runtime inputs constrain stronger native claims; they do not block every unrelated development task. The cheapest fallback is to retain the already frozen source corrections separately and postpone their integration. Stop the affected work on an input-pin mismatch, a scope/authority expansion, lack of an evidence-backed next step, or two independent reject/correct cycles; do not enter a third cycle autonomously.

## Frozen identity and ownership

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.

- Branch: `codex/windows-build-toolchain-environment-v0.1`.
- Base HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`.
- Base tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
- Root `AGENTS.md` SHA-256: `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.
- Candidate root: `s0-lab/audit-remediation/a06-runtime-source-integration-v0.1`.

These identify the authenticated repository base; candidate files are pinned separately in `artifact-files.sha256`. No commit, push, PR, merge, or publication is claimed here.

| Role | Assigned session | Responsibility |
| --- | --- | --- |
| CONTROL | `/root` | Freeze, exact allowlists and pins, handoffs, evidence integration, later decision |
| CODE IMPLEMENTATION | `/root/audit_a06_code` | The 20 implementation files only |
| TEST/VERIFICATION | `/root/audit_a06_test` | Two tests, four verification outputs, bounded verification |
| DOCUMENTATION | `/root/audit_a06_docs` | This README, scope/checklist, their sidecars, artifact manifest |
| INDEPENDENT REVIEW | `/root/audit_a06_review` planned | Fresh read-only `gpt-5.6-sol`, ultra reasoning; not completed at this freeze |

The sequence is CONTROL pre-CODE freeze, CODE, TEST, DOCUMENTATION, fresh REVIEW, then CONTROL decision. `SCOPE-AND-CHECKLIST.md` transcribes CONTROL's earlier freeze after CODE and TEST; it does not claim that the physical document existed before implementation. A fresh reviewer must assess the source and pinned requirements before receiving tests/results/documentation. Neither TEST nor DOCUMENTATION supplies an independent verdict.

## Exact source union

The recovered original is `docs/maintenance/audit-2026-09-09/f03-source-recovery-2026-09-16/implementation/`. Its 20-file inventory is pinned by `verification/implementation-source-files-v0.5.sha256`, SHA-256 `498a7190238f927817010b9506f53130af93f14271252ed19e785faa6a2f0467`. Each manifest row's original `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/` prefix maps to that recovery directory. Recovery source is not evidence of a newly validated runtime.

A02 input manifest: `s0-lab/audit-remediation/a02-native-source-corrections-v0.1/artifact-files.sha256`, SHA-256 `97a86c931b9662fb52492c34abe7120b94dab305f62e8dda115b56d4cb9fac25`.

A05 input manifest: `s0-lab/audit-remediation/a05-profile-composition-v0.3/candidate-files.sha256`, SHA-256 `a0fb92b746d399b4fe0e079187828ff21c1312b875681be7f8e8aea1804cc287`.

Exactly five current files differ from the recovered original:

| Candidate path under `implementation/` | Origin and bounded change | Current SHA-256 |
| --- | --- | --- |
| `native/s0_neutral_preloader_v0_5.cpp` | Exact A02: add P5 once to the re-verification physical list, retaining the same seven entries as the initial list | `88e2a05bbb643c18247844b9aa38b0b327215730f8cf0fd44925e077df5c6e53` |
| `s0_public_runtime_preloader/canonical.py` | Exact A02: reject invalid raw path segments before normalization | `14b30ef5688f3340b78215632fba4f0f4360b2d394ca56730979ac5e6f5c1ff0` |
| `s0_public_runtime_preloader/profile.py` | Exact A05: historical-first gates, current composition/bindings and snapshots | `efae38b6a99763c0dca61efe2813c11672cf784a28ea1f0747937f80e260501a` |
| `s0_public_runtime_preloader/preloader.py` | Exact A05: consume current composition while retaining historical P4 identity | `718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee` |
| `s0_public_runtime_preloader/source_audit.py` | A05 import/constructor policy plus the exact A02 MoveFile-family diagnostic and explanatory comment | `663c281460139f9a847bddfd29f27f7ccee553e649887912bd1c9d4faed8fa60` |

The other 15 files retain their original bytes. These include the full package initializer, build scripts, contracts, runtime authority, native guard/materializer/header, schemas, and supporting Python modules. TEST checked the full original export set, comprising 28 names, and its resolution. This completeness claim concerns the original source inventory only.

The copied build script and runtime-authority material retain their old toolchain and artifact pins. A06 does not replace old expected hashes with current build outputs or establish that the integrated source satisfies those historical runtime pins.

## Authenticated verification evidence

DOCUMENTATION authenticated the following six TEST artifacts before reading them. It did not execute the candidate or rerun the tests.

| Candidate-relative artifact | SHA-256 |
| --- | --- |
| `tests/test_source_corrections.py` | `7b551aeb5a89a59857bab17fc705fa9af35d01644bdd216bf2bddc21dde915da` |
| `tests/test_profile_composition.py` | `991668fc4255a79ec4dce533c9c0f72cea5f959b49918242534ea130aad7a170` |
| `verification/source-corrections-results.json` | `1c68764eda95f810f1012988ff490e8c7bd4e97793b14873fde7883f63fa734a` |
| `verification/source-corrections-stdout.txt` | `1bc44112e0f0e91aab38d8ab18b2d0dc062d821a90fb7c370d08f8fec015b642` |
| `verification/profile-composition-results.json` | `110ad1d29ceb6214ce6ca1c971c0779b53d9d467ee75b3b0a320944380a12f52` |
| `verification/profile-composition-stdout.txt` | `df242fa081388d48915fe8f40d9056d41be2f2f67b98dc496887aaae13383b6a` |

The source JSON reports `outcome: pass`, 24 tests, 205 subtests, zero failures/errors/skips, and equal pre/post inputs. The profile JSON reports `passed: true`, 59 tests, zero failures/errors, and 59 PASS records. It has no standalone skip-count or process-exit field; all 59 records are PASS, and TEST's handoff reports zero skips and exit 0 for both final runs. These are bounded TEST results, not native execution or independent acceptance.

The source suite retains 21 earlier case purposes and adds three integration cases. The profile suite retains all 56 A05 case purposes, adapts eight named preservation assertions to account for the exact source union, and adds three integration cases. The added source cases check the 15 unchanged files, full original exports, and inventory/pin rejection. The added profile cases check retained purposes, the exact union, and F03 snapshots invoking the real corrected F08 helper. The wrapping spy returns the real helper result; it supplies no positive replacement result.

The merged ten-file source checker has 19 current real-checker observations: one exact-source PASS and 18 REJECT outcomes, including rejection at all three reintroduced `getattr` sites. A separate historical rejection record is preserved and is not a twentieth current checker execution. No source-checker double is used. The MoveFile diagnostic survives in this same merged audit module; these bounded AST and name-family checks do not establish complete interpreter or Windows API closure.

The source evidence records 75 pre/post pins; the profile evidence records 78. They reduce to 113 distinct prerequisite paths after path normalization. DOCUMENTATION re-authenticated all 113 as hash-only preservation inputs with no mismatch. Hash-only access does not release the contents of prior reports, verdicts, schemas, or support artifacts. TEST also reports exact 20-file implementation inventory, no extra/shadow or missing file, and unchanged original inputs. These checks do not constitute hostile concurrent-filesystem isolation.

### Preserved initial TEST failure

The first source-suite invocation used test SHA-256 `8fe50fd178bea5d6cc1e62e1a6464305b072a3e19d75625edcb7725184ec3368` and exited 1 during post-run Git identity authentication, before result output. The TEST audit hook expected an argv list, while Windows supplied a command-line string. The recorded diagnostic isolated exactly three queries: `git branch --show-current`, `git rev-parse HEAD`, and `git rev-parse HEAD^{tree}`; each had executable `None`, a string equal to standard `subprocess.list2cmdline`, and exit 0.

TEST made one test-only correction admitting those exact diagnosed strings and reran successfully. Candidate source did not change. The final source JSON preserves the initial test hash, phase, exit, cause, and diagnostic; it locates the original traceback in the TEST tool transcript, not in a separate frozen traceback file. This event is not a candidate implementation failure or native execution result and is not hidden by the final PASS.

### Commands and execution limits

TEST recorded the following commands from the repository working directory. The interpreter was CPython 3.12.10 at `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe`, SHA-256 `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`.

```powershell
& "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe" -I -S -B -X utf8 "C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/tests/test_source_corrections.py"
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a06-runtime-source-integration-v0.1/tests/test_profile_composition.py'
```

These are evidence of the authorized TEST invocations, not permission to overwrite frozen outputs. A later run requires its own authorized output handling and must preserve this frozen evidence.

Positive composition and consumer cases use disclosed upstream doubles: historical validation returns a coherent data-only P4 wrapper; P1-P3 pins use benign unit hashes; successor design/native gates use no-op call spies; minimal-overlay schema validation is replaced while actual schema/map byte pins are checked. Negative diagnostics may replace preceding gates to isolate the target. Actual historical/design/schema/native rejection checks do not establish a complete positive historical pass. P4 is the actual pinned raw input. Current-byte checks and downstream parsing, identity, evidence, precreation and admission logic remain real within these unit cases.

The real 512-file count bound is exercised. The byte-bound test temporarily reduces `_MAX_RUNTIME_BYTES` to 3; it does not allocate or test a 512 MiB payload. The production 512-file/512 MiB constants and existing failure/cleanup paths are unchanged.

## Remaining limits and closed scope

- Native compilation, materialization, current binary identity, actual executed/imported native-byte closure, complete historical positive acceptance, and runtime-authority integration remain **unverified**. The native `ArtifactMaterial.virtual_path` to current runtime-manifest mapping is not inferred or repaired here.
- Windows ACLs, volume/root identity, symlink/junction/reparse behavior, rename/replacement, retained handles, repository exclusion, and TOCTOU through output/evidence writes remain **unverified**. Lexical path checks and observed ordinary non-reparse output ancestry do not prove containment.
- Interpreter, standard-library and native-library closure, hostile introspection/global compromise, hostile concurrency, and secure evidence production remain **unverified**. The developer host, interpreter, Git identity tool, and output root are trusted prerequisites of these bounded results.
- No external download occurs. URL, redirect, digest, size, and provenance verification for a newly fetched artifact remains **unverified**. No network or provider call is evidence in this candidate.
- F0 content, hidden oracles, S0/E0 fixtures, execution/scoring, real model/provider calls, system installation/deletion, security-contract weakening, and Git publication remain outside this gate. No claim of operational safety, value, or model transfer follows from these tests.

These nonclaims restrict the conclusions above; they do not by themselves recommend another technical gate. Concurrent A07 environment work is a separate candidate and is not incorporated or validated by this document.

## Document and manifest integrity

`README.sha256` and `SCOPE-AND-CHECKLIST.sha256` each contain a lowercase SHA-256, two spaces, the Markdown basename, and LF. `artifact-files.sha256` contains exactly 30 ASCII-sorted candidate-relative entries: 20 CODE files, six TEST files, and the two Markdown files plus two sidecars. It excludes itself and any future disposition so that a later CONTROL decision cannot silently rewrite this freeze.

DOCUMENTATION must authenticate and use the canonical `s0-lab/control/tools/verify-text-artifacts.ps1` (SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`) with native `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`, first `-SelfTest` and then `-Path` for each Markdown document, capturing each native exit immediately. Its separately labeled BOM, UTF-8, final-LF, trailing-whitespace, sidecar-format, and sidecar-hash results are reported in the documentation handoff. They do not substitute for TEST evidence, role boundaries, input pins, or independent review.
