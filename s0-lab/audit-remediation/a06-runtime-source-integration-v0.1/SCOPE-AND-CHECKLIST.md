# A06 scope and bounded adversarial checklist

Candidate: `a06-runtime-source-integration-v0.1`. Status at this documentation freeze: **independent review PENDING**.

This is DOCUMENTATION's transcription of CONTROL's pre-CODE freeze and later authenticated TEST evidence. It was physically authored after CODE and TEST. It does not backdate a document, create a new gate, grant another role broader input access, or supply a review verdict.

## Purpose, authority, and immutable base

The one-sentence purpose is to combine the already approved F01/F03/F08 source corrections into one coherent 20-file development input without losing either overlapping patch. This is core development-preparation integration. Standard pinned file copying and exact-diff union are sufficient: A05 alone lacks the F08 correction and A02 alone lacks the F03 composition correction. The estimate for the complete role sequence is 40-90 minutes; roughly 30-minute value checkpoints are progress reports, not automatic extension requests.

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition` (abbreviated `P` below). Candidate root `C` is `P/s0-lab/audit-remediation/a06-runtime-source-integration-v0.1`. Branch is `codex/windows-build-toolchain-environment-v0.1`; HEAD is `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; base tree is `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. Current `P/AGENTS.md` SHA-256 is `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.

Existing bounded F01-F08 remediation authority covers this integration and its ordinary role handoffs. It does not cover F0 content, oracle/fixture creation, S0/E0 execution or scoring, real providers, weaker security/independence contracts, other repositories, installation/deletion, or publication. The base design remains S0 preparation. Recovery-only artifacts remain distinct from a runnable candidate.

The fallback is to retain the existing frozen corrections separately and defer their source union. Stop only affected work if a required pinned input cannot be recovered, progress has no evidence-backed next step, the purpose expands, architectural redesign is needed, or two independent reject/correct cycles have occurred. Continue independent authorized work where possible. A third correction cycle requires a new explicit decision. Missing proof outside the required bounded source claim is a nonclaim, not automatic justification for another gate.

## Roles and exact allowed artifacts

| Role | Session | Owned actions and output |
| --- | --- | --- |
| CONTROL | `/root` | Freeze exact base, pins, allowed paths, checks and assignments; integrate evidence; later decision and separately approved Git operations |
| CODE IMPLEMENTATION | `/root/audit_a06_code` | Author only `C/implementation/`'s exact 20 released files; no tests, docs, or independent review |
| TEST/VERIFICATION | `/root/audit_a06_test` | Two exact tests and four exact verification outputs listed below; substantive checks; no candidate fixes or verdict |
| DOCUMENTATION | `/root/audit_a06_docs` | Only `C/README.md`, `C/README.sha256`, `C/SCOPE-AND-CHECKLIST.md`, `C/SCOPE-AND-CHECKLIST.sha256`, `C/artifact-files.sha256`; input authentication and canonical documentation checks only |
| INDEPENDENT REVIEW | `/root/audit_a06_review` planned | Fresh read-only `gpt-5.6-sol` at ultra; source and requirements first, then separately released evidence/docs; no prior role contribution or edits |

Required order: CONTROL freeze -> CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW -> CONTROL decision. This document reports no completed review or publication. Role-specific prompts may narrow the following inputs; this document does not release everything to every role.

### Content-admitted source inputs

| Input | Exact authentication and content limit |
| --- | --- |
| `O = P/docs/maintenance/audit-2026-09-09/f03-source-recovery-2026-09-16` | `O/verification/implementation-source-files-v0.5.sha256` SHA-256 `498a7190238f927817010b9506f53130af93f14271252ed19e785faa6a2f0467`; exactly 20 rows with `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/` prefix map to `O/implementation/`; authenticate each pin before content |
| `A2 = P/s0-lab/audit-remediation/a02-native-source-corrections-v0.1` | `A2/artifact-files.sha256` SHA-256 `97a86c931b9662fb52492c34abe7120b94dab305f62e8dda115b56d4cb9fac25`; only corrected native preloader, `canonical.py`, and `source_audit.py` content admitted; other entries hash-only |
| `A5 = P/s0-lab/audit-remediation/a05-profile-composition-v0.3` | `A5/candidate-files.sha256` SHA-256 `a0fb92b746d399b4fe0e079187828ff21c1312b875681be7f8e8aea1804cc287`; only its exact ten Python source files content-admitted after pins; other entries hash-only |
| Current `C/implementation/` | Original 20-file inventory; 15 original byte strings and exactly five prescribed replacements, each pinned below and in `artifact-files.sha256` |

The exact five replacement paths relative to `C/implementation/` and hashes are:

```text
88e2a05bbb643c18247844b9aa38b0b327215730f8cf0fd44925e077df5c6e53  native/s0_neutral_preloader_v0_5.cpp
14b30ef5688f3340b78215632fba4f0f4360b2d394ca56730979ac5e6f5c1ff0  s0_public_runtime_preloader/canonical.py
718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee  s0_public_runtime_preloader/preloader.py
efae38b6a99763c0dca61efe2813c11672cf784a28ea1f0747937f80e260501a  s0_public_runtime_preloader/profile.py
663c281460139f9a847bddfd29f27f7ccee553e649887912bd1c9d4faed8fa60  s0_public_runtime_preloader/source_audit.py
```

The native preloader and canonical helper are exact A02 bytes. The profile and preloader Python modules are exact A05 bytes. The source audit module combines A05's policy with A02's MoveFile-family delta. The admitted A02 audit-module source SHA-256 is `7b65cfec819544a258ecb0cb9f25346b0c9c6606c52f12448d0a8d6954f57e6c`; the A05 audit-module source SHA-256 is `50399a565232136736e041ea028b76ed8767d18327553ecf2ec6ec5b0bfe2d36`. Original frozen artifacts, including original expected hashes, remain unchanged.

### Exact TEST evidence and hash-only dependencies

The six content-admitted current TEST artifacts, relative to `C`, are:

```text
7b551aeb5a89a59857bab17fc705fa9af35d01644bdd216bf2bddc21dde915da  tests/test_source_corrections.py
991668fc4255a79ec4dce533c9c0f72cea5f959b49918242534ea130aad7a170  tests/test_profile_composition.py
1c68764eda95f810f1012988ff490e8c7bd4e97793b14873fde7883f63fa734a  verification/source-corrections-results.json
1bc44112e0f0e91aab38d8ab18b2d0dc062d821a90fb7c370d08f8fec015b642  verification/source-corrections-stdout.txt
110ad1d29ceb6214ce6ca1c971c0779b53d9d467ee75b3b0a320944380a12f52  verification/profile-composition-results.json
df242fa081388d48915fe8f40d9056d41be2f2f67b98dc496887aaae13383b6a  verification/profile-composition-stdout.txt
```

The authenticated source result's `pre.pins`/`post.pins` and profile result's `pre_input_sha256`/`post_input_sha256` release 113 deduplicated exact paths for hash-only preservation. They include current/original source inventories, prior A02/A05 source/tests/snapshots, and A05's legacy 60 supports: earlier C1/C2 source/test/evidence/manifests/docs, P4 and v0.4/v0.5 schema/map material, `AGENTS.md`, and Python metadata. They do not release additional linked content, histories, prior verdicts, search indexes, or recursive discovery. Unexpected paths are not admitted. Documentation authenticated 75 source and 78 profile pins, all 113 distinct paths matching.

Base Python metadata only: `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe`, CPython 3.12.10, SHA-256 `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`. Documentation must not invoke Python, candidate code, tests, native tools, or project execution. Its sole permitted verification execution is the canonical documentation validator, `P/s0-lab/control/tools/verify-text-artifacts.ps1`, SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`, first `-SelfTest`, then `-Path` for each owned Markdown file via native `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`, capturing each exit immediately.

## Bounded threat and evidence model

The adversarial cases may supply malformed in-memory source, manifests, maps, types, byte strings, path strings, digests and package rows; omit/add/reorder/duplicate entries; substitute bindings; and mutate caller-owned data before or after snapshots. They do not grant hostile authority over the developer host, interpreter, native libraries, output root, or concurrent filesystem. Trusted prerequisites are the pinned public inputs, CPython and standard library, OS, Git identity tooling, and permitted evidence producer/output paths. Hostile concurrency and compromised prerequisites are **unverified** and cannot support broader authority claims.

The bounded flow is pinned original/A02/A05 source -> exact source union -> current test import/parameter checks -> separate pre/post evidence -> documented manifest/sidecars -> later independent assessment. The runtime data flow preserves historical-first validation, pinned predecessors, current manifest/files/package and effective-profile bytes/hash, historical P4 identity, snapshots, and current consumers. Verified Python source bytes are not automatically the native bytes executed or imported by a future runtime. Caller-provided data does not mint acceptance authority.

No external artifact is fetched: external URL/redirect/digest/size/provenance checks and native execution closure remain unverified. There is no permission to repair these limitations by expanding this candidate. Native compilation/materialization, full positive historical acceptance, actual binary identity, and current runtime-authority integration remain outside the required source claim.

## CONTROL's pre-CODE checklist, transcribed

Every row assigns the CODE defense, TEST discrimination and expected rejection, DOCUMENTATION claim boundary, and later REVIEW closure criterion. These are bounded falsifiable checks, not a claim to cover every possible attack. Unknown prerequisites remain **unverified** and block only a claim that depends on them.

| # / surface | CODE IMPLEMENTATION defense/action | TEST/VERIFICATION discrimination and expected fail-closed result | DOCUMENTATION allowed claim and required nonclaim | INDEPENDENT REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| 1. Inventory, source union and shadows | Preserve the original exact 20-file inventory and full initializer; keep 15 files unchanged and only five prescribed replacements; retain both overlapping patches. | Exact pins/inventory/full exports; missing, extra, shadow and each changed-pin cases reject; exact union accepts. | Complete original source inventory and retained source fixes only; no complete runtime closure. | Verify 20 paths, original exports, exact union and no lost patch or unapproved byte delta. |
| 2. F01 native physical lists | Carry the exact A02 one-entry P5 change; both physical lists contain the same seven entries with P5 once; no other native edit. | Static lists and consuming comparison/directory-check call sites; missing/extra/duplicate mutations reject; baseline missing P5 is discriminated. | Source-level F01 correction only; native build/lifecycle/close behavior unverified. | Confirm exact one-entry patch and static discrimination without interpreting it as native execution. |
| 3. F08 lexical path lifecycle | Carry the exact A02 raw-segment guard before normalization; bind F03 snapshots to the corrected canonical helper. | Direct, manifest and snapshot invalid paths reject; real wrapping helper spy proves the call; normal paths accept. | Raw lexical aliases are rejected in the tested flows; OS containment and hostile path races unverified. | Confirm the actual corrected helper is called, ordering is preserved, and no fake positive helper replaces it. |
| 4. F03 gates, composition and consumers | Retain historical-first validation, four predecessor pins, design/schema/map/native gates, current six-row package, effective bytes/hash, historical P4 identity, snapshots and consumers. | Retain all 56 A05 purposes with named merge-preservation adaptations; malformed/mixed bindings and missing gate material reject; current inputs cannot silently fall back to history. | Bounded composition/data-flow observations; disclose positive historical/design/schema/native/P1-P3 doubles and no complete positive historical pass. | Confirm prior gates and bindings remain, changes are exact, and evidence distinguishes real logic from prerequisite doubles. |
| 5. Mutable/caller-minted authority | Introduce no authority or capability; preserve object/raw/hash consistency checks and immutable snapshots. | Inconsistent objects reject; caller mutation is rejected or yields stable validated snapshots; relation promotion cannot mint authority. | Bounded input consistency and snapshots only; caller data is not authority, and hostile concurrency/introspection remains unverified. | No authority rebinding or widened trust claim; tested caller mutations preserve intended failure/stability. |
| 6. Import/AST and native API families | Preserve A05's four-set import/getattr/constructor policy and A02 MoveFile-family diagnostic/comment in the same audit module. | Run the real merged ten-source checker without doubles; exact source accepts; import/reflective/inventory negatives and all three getattr reinjections reject; MoveFile rejects. | Bounded AST/import and named API-family diagnostics; no full interpreter/stdlib/native-library closure or complete Windows API classifier. | Confirm both policies survive together, no allowlist weakening or fake checker, and exact current-source pass. |
| 7. Verified bytes versus execution and old pins | Preserve source/configuration/build/authority originals except declared patches; do not invent new historical hashes or repair unavailable native inputs. | Pin and imported-module observations; preserve exact source/config bytes; mark build/authority and actual native path/binary identity unverified. | Verified Python source/import observations only; rebuilt executable package and native acceptance remain unverified. | Exact source evidence supports only source claims; unchanged historical pins are not represented as current binary acceptance. |
| 8. Windows full path lifecycle | No new ACL/volume/root/reparse/symlink/junction/rename/replacement/retained-handle/repository-exclusion/TOCTOU mechanism; preserve existing code. | Lexical tests and ordinary path/output ancestry observations only; invalid lexical inputs reject. Hostile lifecycle and concurrent output/evidence replacement remain unverified. | No stronger OS isolation, containment or hostile-filesystem evidence-production claim. | Each Windows lifecycle prerequisite through final evidence writes is explicit and does not silently become an assumption of security. |
| 9. Producer, execution, downloads and evidence | No downloads/provider/native project calls; retain pinned sources and configuration. | Isolated/no-site/no-bytecode Python (`-I -S -B -X utf8`); exact commands, imports, pre/post pins and output checks; mismatch fails closed; preserve failed attempts and diagnostics. DOC uses canonical text checks. | Reproducible bounded developer-host evidence, trusted producer/output root; external artifact URL/redirect/digest/size/provenance and secure evidence production unverified. | Trace source/evidence/output identity and failure history; no unjustified native/network result or producer-security claim. |
| 10. Bounds, failure, cleanup, cost and gates | Keep existing 512-file/512 MiB bounds and failure/cleanup paths; no prior-output overwrite or speculative architectural changes. | Exercise real 512-file bound and explicitly reduced byte bound; preserve previous outputs and pre/post identities. Diagnose an unresolved failure before another speculative correction. | Report actual tested bounds and test-only failure repair; no native close, operational safety, value, S0/E0 or transfer claim. Two independent reject/correct cycles require a new decision. | Bounds/failure evidence and preserved history support the bounded claim; no hidden third correction cycle, native cleanup claim, or gate expansion. |

## Evidence integration after TEST

The source result reports 24 passing tests, 205 subtests, zero failures/errors/skips, 21 retained purposes and three additions. The profile result reports 59 passing tests, zero failures/errors, 56 retained purposes, eight named preservation adaptations and three additions; all 59 records are PASS. TEST's handoff reports both final exits 0 and zero skips. The profile JSON itself does not have a skip-count or process-exit key.

Current real-source checker evidence comprises 19 observations: one PASS and 18 REJECT, including all three getattr reinjections. A separate preserved historical rejection record is not counted as a current execution. The F03 snapshot helper spy invokes the real corrected F08 helper; the native-family checks retain the MoveFile diagnostic in the same module. The real 512-file bound is exercised, while the byte bound is temporarily reduced to 3 and explicitly labeled.

Positive historical/design/native/schema gates and P1-P3 pins use the doubles listed in `profile-composition-results.json`; actual P4 bytes and current source checker are not replaced with positive doubles. These unit outcomes do not establish complete positive historical/native acceptance. The build scripts and runtime authority retain old toolchain/artifact pins. No executed binary, runtime materialization, native-path identity, or runtime-authority integration is newly accepted.

The first source run exited 1 after candidate checks, in post-run Git authentication before output generation. The TEST-only audit hook expected argv-list representation; the diagnostic recorded Windows string representation for the exact three Git identity queries. TEST made one exact-string correction and reran, leaving candidate source unchanged. The final source JSON preserves initial test SHA-256 `8fe50fd178bea5d6cc1e62e1a6464305b072a3e19d75625edcb7725184ec3368`, cause, phase, exit and diagnostic; the full original traceback remains in the TEST tool transcript. It is not a candidate implementation failure, a native run, or an erased prior report.

## Preservation and next decision

The 20 CODE and six TEST artifact pins are fixed before documentation. DOCUMENTATION is limited to five output paths and authenticates inputs without running substantive tests. Its manifest has exactly 30 ASCII-sorted candidate-relative entries (20 CODE, six TEST, four Markdown/sidecar files), excluding itself and future disposition. Both Markdown sidecars are checked by the canonical validator with independently labeled text checks. Validation output and final hashes are handed to CONTROL.

Original frozen artifacts, current root policy, and concurrent A07 work must remain unchanged. Prior verdicts/interpretations are not primary evidence for the fresh reviewer. Repository links, public presence, shared files, and this document do not broaden any role's input allowlist. Worktree separation is not proof of information isolation.

The remaining authorized sequence is fresh source-first independent review and CONTROL's bounded disposition. Publication still requires its own applicable approval and clean classified status. This candidate neither completes the broader audit/maintenance objective nor opens S0/E0, F0, real providers, feature development, or any other technical gate.
