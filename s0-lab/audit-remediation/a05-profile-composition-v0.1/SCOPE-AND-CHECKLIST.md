# A05 scope and pre-CODE checklist transcription

This file was authored by DOCUMENTATION **after** CODE and TEST handoff. It faithfully transcribes CONTROL's earlier pre-CODE role handoff and subsequent native-path clarification. It does not assert that this file existed before CODE. The checklist states bounded requirements and review closure criteria; the actual completed tests and their doubles are reported in `README.md` and the authenticated TEST evidence. Independent review is **PENDING**, with no CONTROL acceptance at this freeze.

## Gate, purpose, and role sequence

The user authorized minimal F01-F08 audit corrections and instructed CONTROL to proceed and fix them autonomously. This candidate's one-sentence purpose is to resolve the source data-flow contradiction between historical P4 validation and a current six-row package while preserving the existing historical/native contract. It is **auxiliary tooling/evidence work**, limited to public source remediation and related units. The cheapest implementation reuses the existing JSON, manifest, and hashing primitives; no verifier framework, downloader, trust service, or environment redesign is introduced.

This authorization does not waive missing full-material prerequisites, weaken native/research requirements, permit edits to original frozen bytes, authorize S0/E0 execution/scoring or F0 access, or supply Git publication approval. The candidate is not integrated into a live path. An unresolved exact-input, architecture, or scope issue stops only affected work. Thirty minutes is a progress/value checkpoint, not an automatic stop or renewed-approval boundary. A non-isolated failure requires discriminating TEST diagnostics before speculative CODE correction; two independent reject/correct cycles require an explicit decision before a third.

| Role | Assigned agent | Owned action/artifacts |
| --- | --- | --- |
| CONTROL | `/root` | Earlier scope/adversarial freeze, pins and allowlists, role handoffs, later disposition and separately authorized Git actions |
| CODE IMPLEMENTATION | `/root/audit_a05_code` | Exact ten candidate implementation modules below; only `profile.py` and `preloader.py` changed |
| TEST/VERIFICATION | `/root/audit_a05_test` | `tests/test_profile_composition.py`, `verification/test-results.json`, `verification/test-stdout.txt`; substantive candidate verification |
| DOCUMENTATION | `/root/audit_a05_docs` | `README.md`, `README.sha256`, `SCOPE-AND-CHECKLIST.md`, `SCOPE-AND-CHECKLIST.sha256`, `candidate-files.sha256` |
| INDEPENDENT REVIEW | Fresh read-only `/root/audit_a05_review`, planned | Primary assessment after documentation handoff; no artifact edits or prior candidate role |

The required sequence is CONTROL freeze -> CODE handoff -> TEST handoff -> DOCUMENTATION handoff -> fresh INDEPENDENT REVIEW -> CONTROL decision. No role is silently absorbed by another. DOCUMENTATION did not run candidate/tests, edit implementation/tests, or produce an independent verdict. CONTROL disposition is not an output of this freeze.

## Exact input and output scope

All paths below are exact compositions of these fixed prefixes and explicitly enumerated names; no prefix or suffix authorizes discovery or a wildcard read:

- `P = C:/Users/SSAFY/Documents/ai-development-tradition`
- `C = P/s0-lab/audit-remediation/a05-profile-composition-v0.1`
- `O = P/docs/maintenance/audit-2026-09-09/f03-source-recovery-2026-09-16/implementation/s0_public_runtime_preloader`
- `B = P/docs/maintenance/audit-2026-09-09/f03-input-recovery-2026-09-17`
- `I = C/implementation/s0_public_runtime_preloader`

The authenticated baseline is branch `codex/windows-build-toolchain-environment-v0.1`, HEAD `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`, tree `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. `P/AGENTS.md` is pinned to `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` and was read completely.

The ten modules below are admitted at `I/<name>` and `O/<name>` only. DOCUMENTATION authenticated every file against the TEST inventory before content use. Equal hashes indicate preserved bytes, not execution validation.

| Exact name | Candidate SHA-256 | Original SHA-256 |
| --- | --- | --- |
| `__init__.py` | `a2e40d7a44f79f3c0f96b790c2249fcb6efe7dba2abf821ea3ee96302f1570c3` | `a2e40d7a44f79f3c0f96b790c2249fcb6efe7dba2abf821ea3ee96302f1570c3` |
| `canonical.py` | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` |
| `errors.py` | `20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86` | `20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86` |
| `evidence.py` | `e0f1d9de22eb8b7a727dbef146f808c59d44accbbb96fa3367ee2d0dfdbdd964` | `e0f1d9de22eb8b7a727dbef146f808c59d44accbbb96fa3367ee2d0dfdbdd964` |
| `integration.py` | `7d40c5091c43354287fade09f8e11d2ca6a830492d390385d8b13cee361a3dfd` | `7d40c5091c43354287fade09f8e11d2ca6a830492d390385d8b13cee361a3dfd` |
| `preloader.py` | `718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee` | `b6f343c7a0a0c3ebe075eed386ff53d08abda507116ca19d1e7b7985aabd1c59` |
| `profile.py` | `0c0c451a0be41c5593fb3937192da61ae1728534d12e114e0fda9b7a4e297c14` | `c5c1f6c6c937e45b9da246b24783134570a48923501757ab4683173a5367fe89` |
| `schema.py` | `97b00ab0bb9417b63c5871332751e8c14dea80423414810e99aa2b443f9d6317` | `97b00ab0bb9417b63c5871332751e8c14dea80423414810e99aa2b443f9d6317` |
| `semantic.py` | `1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d` | `1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d` |
| `source_audit.py` | `c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99` | `c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99` |

Other exact admitted inputs are:

| Exact path | SHA-256 |
| --- | --- |
| `C/tests/test_profile_composition.py` | `a1a20ede2c99ebb6e0fa8b8196d6e809f63d13f22418fd7ad193806830fc6812` |
| `C/verification/test-results.json` | `03277de88f8c3353c72aefcc7fbb3723fb633bd385b89027b8cf9cc92a71af77` |
| `C/verification/test-stdout.txt` | `c15324516b0fc1685c0ee9884dc65da1f7788f4ed7236bdfc3198a0c406ba1ab` |
| `B/historical/runtime-profile-v0.4.json` | `266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e` |
| `B/design/findclose-amendment-v0.1/runtime-profile-v0.5.schema.json` | `04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e` |
| `B/design/findclose-amendment-v0.1/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json` | `f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623` |
| `P/s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.json` | `3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd` |
| `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe` (identity/hash metadata only for DOCUMENTATION) | `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` |
| `P/s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

The TEST JSON's `pre_input_sha256` inventory is admitted only for the 26 exact sources/supporting inputs above: ten candidate modules, ten originals, AGENTS, Python executable metadata, historical P4, both schemas, and the interface map. Unexpected entries do not broaden this scope. The three TEST artifact pins were authenticated before reading that inventory.

DOCUMENTATION may write only its five exact `C/` outputs from the role table using `apply_patch`. Both Markdown sidecars use a lowercase SHA-256, two spaces, the Markdown basename, and LF. `candidate-files.sha256` has 17 ASCII-sorted repository-relative entries covering ten CODE files, three TEST files, and four Markdown/sidecar files, excluding itself and any future CONTROL disposition. The canonical validator must run with `-SelfTest`, then `-Path` for each owned Markdown; every exit code is checked immediately.

No broad search, history/log access, recovery README, audit report, mutable index, prior review/verdict, session-conversation retrieval, F0 content, original recovery-recipe execution, candidate/test execution by DOCUMENTATION, native/provider/network action, installation, or Git write/publication is allowed. No hidden oracle or S0/E0 fixture/execution is allowed. Shared files and worktree placement do not prove enforced read isolation.

## Bounded pre-CODE adversarial checklist

The attacker model permits arbitrary supplied bytes, digest strings, maps, and caller mutation before/after snapshot construction. These are untrusted inputs. Frozen source pins are trusted for this bounded maintenance task; complete historical material and platform/native properties remain unverified. The rows cover the current candidate's complete bounded data-flow surface, not every imaginable attack. Concurrency and OS behavior are named explicitly where their stronger claims are unverified.

| Row / surface | CODE owner action | TEST case and expected result | DOCUMENTATION claim and required nonclaim | INDEPENDENT REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| 1. Caller bytes, pins, maps, mutable state | CODE copies and freezes supplied current state; accepts exact bounded types. | Malformed/missing types and mutations before/after snapshots must reject inconsistent material or preserve an already copied snapshot. | Claim bounded data consistency only; caller-mintable data is not authority. Concurrent hostile execution is unverified. | No rebinding path or promotion of unverified authority within the bounded Python flow. |
| 2. Trusted pins and unverified full historical prerequisites | CODE keeps full historical validation first, four predecessor pins/order, and design/schema/map/native gates. | Real historical negative plus labelled gate/order spies and tamper failures; failures prevent successor composition. | No mocked prerequisite is promoted to a completed historical/native prerequisite. | Preserved gate path, order, and frozen constants remain required. |
| 3. Complete Python data flow | CODE traces historical P4 check -> current manifest/files -> current six-row package -> effective snapshot -> preloader -> evidence/admission. | Contrasting historical/current data succeeds only on the isolated doubled-prerequisite branch; mixed manifest/package/P1-P5 material fails. | Source/unit result only; no complete integration success. | Trace every consumer to its intended current or original historical source. |
| 4. Mintability, consistency, and mutation | CODE binds raw/object/hash and explicit original/effective identities; issues no reusable capability. | Digest/object mismatches and mutation reject or leave immutable snapshots intact. | Candidate data only, including directly constructed coherent objects. | No removed equality check lacks a replacement binding check; identities cannot be silently exchanged. |
| 5. Verified bytes versus consumed bytes | CODE uses validated current control/artifacts/package and original P4 identity in evidence/admission. | Capture real downstream evidence/admission with contrasting inputs and mutation after validation; hashes must use the current snapshot and original P4 digest. | Python consumer binding only. Native executed/imported identity and native-binary-to-runtime path mapping are UNVERIFIED. | Same validated snapshot reaches all Python consumers; no native mapping or execution claim is inferred. |
| 6. Inventory, shadow paths, and resource bounds | CODE rejects nonbytes, missing/extra/duplicate/reordered/case-alias/dot/traversal entries; bounds runtime material to 512 files and 512 MiB. | Discriminating actual closure/path checks and labelled small byte-limit doubles where used; malformed/inconsistent material fails closed. | Virtual in-memory namespace and bounded limits only; no Windows path-security proof. | Exact bounded rejects and resource behavior supported by disclosed tests. |
| 7. Interpreter, stdlib, native/import closure and external artifacts | CODE adds no downloader/native call and does not weaken provenance gates; uses stdlib/existing imports. | Isolated authenticated source/interpreter; distinguish mocks from actual gates and ensure no newly authorized external/native action. | Full installed closure and external URL/redirect/digest/size/provenance proof are UNVERIFIED. | No broadened native, external, or interpreter claims; original requirements preserved. |
| 8. Windows path lifecycle and concurrency | CODE remains data-only with no OS writes; native contract unchanged. | No native lifecycle test; exact owned TEST outputs and path/integrity observations only. | ACL/root/volume/symlink/junction/reparse/rename/replacement/retained-handle/repository-exclusion/TOCTOU through output/evidence remain UNVERIFIED; trusted maintenance checks are not adversarial isolation. | No OS or concurrent-filesystem guarantee appears in results or prose. |
| 9. Evidence producer/output, sidecars, measurements, failure/cleanup/close | CODE introduces no filesystem evidence writer or native close changes. | Deterministic exact results, input integrity before/after, bounded resources, exact outputs, no scratch artifacts; failed prerequisites do not produce candidate success. | Publish commands, producer identities, and nonclaims; canonical text checks cover DOC artifacts only, not runtime safety. | Evidence supports only bounded source/unit scope, with no implied native close or output-root guarantee. |
| 10. Compatibility and failure | CODE requires new current material and refuses historical fallback. | Missing new arguments, wrong types, missing current controls/artifacts, and static/deferred scope checks fail or remain restricted as specified. | Caller migration is required; integration is absent and complete integration remains blocked. | Source correction only; no silent legacy fallback or complete-integration acceptance. |

CONTROL later clarified that native binary virtual-path mapping is unknown in the exact allowed inputs. Existing checks must remain; guessed aliases and claims of full current-native/runtime acceptance are prohibited. This is the row 5/7 nonclaim, not added implementation scope. A stronger claim stays blocked on its missing prerequisite; it does not automatically justify another auxiliary gate.

## Evidence and final handoff boundaries

The authenticated final TEST report records 36 tests with zero failures/errors and matching pre/post hashes for all 26 pinned inputs. The full-positive upstream doubles, the real historical semantic negative, resource-test substitution, interpreter pin, reproducible command, and unresolved native/path closure are disclosed in `README.md`; no independent verdict is inferred from the pass count.

Original frozen artifacts remain attached to their original bytes. The candidate manifest freezes this source/unit handoff; it is not a runnable historical package, an authority manifest, a publication approval, or a replacement for missing historical/native inputs. A fresh read-only reviewer assesses this frozen scope before CONTROL issues any later disposition.
