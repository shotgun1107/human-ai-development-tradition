# A07 scope and CONTROL checklist transcription

Candidate: `a07-public-cli-readiness-v0.1`.

Status: **TEST PASS / REVIEW PENDING**. DOCUMENTATION authored this artifact after CODE and TEST on 2026-09-29. The matrix below transcribes the earlier pre-CODE CONTROL handoff supplied to this role; this file was not physically present before CODE, and it is not independent evidence of that earlier timing.

## Purpose, value, and stop conditions

This is **core project preparation**: remove the concrete missing-dependency blocker and run the already-approved A04 public CLI against real jsonschema and existing public inputs. The expected useful output is one reusable local environment plus a bounded recorded result for `integrity`, `schema-check`, and `verify`.

The cheapest standard alternative is Python `venv` plus pip. That alternative was selected; there is no demonstrated need for a custom downloader, trust engine, verifier, or launcher. The approved estimate was 20-40 minutes for setup, bounded checks, documentation, and review. Thirty minutes is a progress/value checkpoint, not automatic permission expiry. Stop the affected work for a required pin mismatch, unavailable required role/input, repeated failure without discriminating evidence, scope expansion or redesign, or two independent reject/correct cycles. Continue unrelated authorized work. No new installation, dependency upgrade, cleanup, or third correction cycle is implied by this document.

## Identity and role ownership

The authenticated repository is `C:/Users/SSAFY/Documents/ai-development-tradition` (abbreviated `P` below). `C` means `P/s0-lab/audit-remediation/a07-public-cli-readiness-v0.1`; `A4` means `P/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1`; `E` means `P/.venv-public`.

| Identity | Value |
| --- | --- |
| Branch | `codex/windows-build-toolchain-environment-v0.1` |
| HEAD | `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` |
| HEAD tree | `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` |
| Active baseline | `central-system-v2.1-s0-preparation` |

| Role | Assigned session and bounded responsibility |
| --- | --- |
| CONTROL | `/root`: freeze scope, inputs and role assignments; integrate evidence and decide disposition. Publication requires separate authority. |
| CODE IMPLEMENTATION | `/root/audit_a07_code`: standard local environment setup, lock and one ignore entry; no A04 source or test/document authorship. |
| TEST/VERIFICATION | `/root/audit_a07_test`: test producer and one bounded verification run; no candidate source fixes or review verdict. |
| DOCUMENTATION | `/root/audit_a07_docs`: this document, README, their sidecars, and the candidate manifest from authenticated evidence; no CLI/test execution or independent verdict. |
| INDEPENDENT REVIEW | `/root/audit_a07_review`, planned fresh read-only `gpt-5.6-sol` at ultra reasoning: primary source/configuration assessment before results/docs, then evidence assessment. Not completed at this artifact's freeze. |

Required order: CONTROL freeze -> CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW -> CONTROL decision. Concurrent A06/A08 work is outside this role's input and write scope and must be preserved. No role gets additional access through links, logs, shared storage, or prior summaries. Worktree or agent separation does not establish enforced information isolation.

## Frozen input authorities

Authenticate these exact paths before using their content. The original full A04 manifest does not authorize reading its prior verdicts or other entries as content. Its release to DOCUMENTATION is limited to the eleven `implementation/s0_i0/*.py` sources and `requirements.txt`; all other A04 entries remain hash-only.

| Path | SHA-256 | DOCUMENTATION use |
| --- | --- | --- |
| `P/AGENTS.md` | `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` | Complete current operating policy |
| `C/requirements.lock.txt` | `58a76393ebeb1d098c09bd74713704673d4b2c768162bb903145e7d2acbd9c71` | Dependency specification |
| `P/.gitignore` | `93b0ba1fee168778488b7839f3094b9f2c137399aafea117a3dc417a6ddd718a` | External configuration prerequisite |
| `E/Scripts/python.exe` | `0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14` | Metadata/hash only |
| `E/pyvenv.cfg` | `6d7ac85012ab1132ed60a62b8ead1d23b2a29f658e90b443babbe9e6464feb68` | Environment configuration |
| `E/install-report.json` | `3df056b8d8c3ba50349cd3b8fe8d379f60280af55e6c408153a930607458767c` | Standard pip provenance |
| `A4/artifact-files.sha256` | `3188bfb5d5745b83a0f07f8134e2021d63285c8591db1698eca02e6086fc3f68` | Exact released source pins; no prior verdict content |
| `A4/requirements.txt` | `d0bc9baee84543883a0a966d477620161876536b552742ab6409d1da50251405` | Original top-level requirement |
| `P/s0-lab/public-practice/v0.1/bundle-files.sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` | Manifest metadata; its 90 entries are hash-only to DOCUMENTATION |
| `C/tests/verify_public_cli.py` | `b29360f0844a405dbc72bbeece4d98552eb21ade006efee064fbd638bd7b5625` | Read-only test provenance |
| `C/verification/test-results.json` | `011fb8de441c82ac975e649648495e752cf7afa581bfd9df4131a5f764f6a1ea` | Structured evidence and exact pre/post input map |
| `C/verification/test-stdout.txt` | `0f3beb4f388b518c7fc34bfa3a0b9762b412c106e8530a9826ba36045f6d6607` | Recorded command outputs |
| `P/s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | Canonical document validation only |
| `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe` | `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` | Base interpreter metadata/hash only |

The `.gitignore` prior pin was `d3ac3c115fb311b06ba7ff0e4abdb53f1f4ca68ee3f7db2da75773a72bd4b595`. TEST compared it with the pinned HEAD version and recorded only the appended `.venv-public/` line. It is not an entry inside the candidate manifest.

The exact eleven A04 source names are `__init__.py`, `answer_validation.py`, `authentication.py`, `cli.py`, `error_reporting.py`, `integrity.py`, `json_validation.py`, `paths.py`, `schema_suite.py`, `transform.py`, and `verification.py`, beneath `A4/implementation/s0_i0/`; their individual pins come from the authenticated A04 manifest. The eleven schema paths and hashes are exactly the `FROZEN_SCHEMA_HASHES` keys in admitted `schema_suite.py`, relative to `P/s0-lab/control`; schema bytes are hash-only to DOCUMENTATION.

The JSON's 122-entry before/after maps release only preservation metadata for the exact combination of 10 directly pinned inputs, 11 A04 modules, 11 schemas, and 90 existing public bundle files. DOCUMENTATION reconstructed this allowlist from the pinned authorities, rejected unexpected entries, and authenticated every current hash and size against both recorded maps. It did not open schema or public bundle contents. These releases authorize no broad repository discovery, history/log inspection, unrelated review documents, F0 content, oracle, or other-condition outputs.

## Pre-CODE bounded checklist, transcribed after CODE/TEST

The required claim is ordinary dependency and public CLI readiness on a trusted developer host. The lock, source, input manifests, schemas, installation receipt, interpreter, and evidence producer are explicit authority inputs. Source bytes on disk and observed import origins are connected by TEST's pre/post authentication and same-child observations. They are mutable filesystem objects; these observations do not establish resistance to a malicious host, concurrent writer, caller-minted/rebound authority, or loaded-image substitution.

| Row / surface | CODE owner and frozen action | TEST diagnostic and expected stop/fail behavior | DOCUMENTATION permitted claim and required limit | REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| 1. Dependency authority | CODE pins exactly 18 names, versions and wheel hashes, retaining the jsonschema format extra. | Compare lock, receipt and installed metadata; reject a changed version/hash and stop on a mismatch or substitution. | Exact standard dependency setup; no publisher or supply-chain proof. | No silent version, digest, name, or extra change. |
| 2. Environment ownership | CODE uses the exact previously absent project-local environment with ordinary no-reparse observations; append one ignore entry only. | Check interpreter, prefix/base identity, exact ignore change and ordinary path observations; unexpected identity or ownership stops the run. | Local environment setup; no global install or enforced isolation claim. | Correct local ownership and no broader setup action. |
| 3. External artifacts | CODE uses official PyPI HTTPS, pinned wheels, pip hash enforcement, binary-only mode, normal TLS, timeout 20 and one retry. | Compare all 18 receipt URLs, hashes and versions; unexpected host/scheme/hash/version rejects. | Standard pip provenance; redirects, publisher signatures and hostile-index behavior unverified. | Receipt evidence is not promoted into independent authority. |
| 4. Transitive dependencies | CODE installs the frozen transitive set only. | Real `pip check`, real jsonschema metadata and exact installed versions; no doubles; incompatibility or unexpected package fails. | Real dependency consistency; whole interpreter/stdlib/native closure unverified. | Real handlers and correct dependency versions, with closure limits retained. |
| 5. Public input and source flow | CODE changes no I0 source or existing public inputs. | Authenticate 11 A04 sources, 90 public entries and 11 schemas; execute three actual commands; mismatch or unexpected source/bundle inventory stops. | Existing public offline checks only; no F0 access or new fixture. | Admitted sources and inputs preserved; no scope expansion. |
| 6. Executed/imported bytes | CODE performs setup only; TEST owns interpreter and dependency execution. | Observe module origins in the same CLI child and compare them with admitted paths; unexpected origins fail. | Observed real imports and versions; no hostile loaded-image proof. | Exact tested runtime identified without claiming native/preloader validation. |
| 7. Windows lifecycle/concurrency | CODE adds no ACL, root/volume, reparse, rename, retained-handle, repository-exclusion or TOCTOU redesign. | Ordinary path and reparse observations only; observed reparse/identity anomaly stops. Hostile concurrency and replacement remain unverified, not a completed adversarial test. | No OS-safety, secure authority, retained-identity or race-resistance claim. | Every lifecycle gap remains explicit and blocks a stronger security claim. |
| 8. Evidence flow/output | CODE produces exact config and standard receipt; TEST owns new exclusive result outputs, pinned producer and pre/post inputs; DOCUMENTATION owns sidecars/manifest. | Capture arguments/stdout/stderr/exit; reject existing result outputs; stop for input drift or evidence errors. Canonical document checks validate text/sidecars. | Trusted-host evidence only; no secure attestation or permission to overwrite historical evidence/fix code. | Source-to-command-to-record relationship and document hashes are coherent. |
| 9. Resource/failure/cleanup | CODE bounds setup to 18 wheels, about 1.4 MB; no arbitrary upgrades or cleanup. | Exact packages plus bootstrap pip; 45-second subprocess timeouts; source/bundle inventory preservation; errors stop affected work. | Ordinary pip temporary cleanup and bounded observations; no OS cleanup/close-path proof or claim that every host directory was audited. | No unapproved artifacts/packages or retry/repair expansion hidden by a passing result. |
| 10. Claim boundary | CODE supplies readiness only; TEST performs actual 90-file/11-schema/8-package checks. | Never create S0/E0 fixtures, oracle or scoring outputs, call providers, or execute the project-native preloader; prohibited work stops the affected role. | Bounded public CLI readiness only; no central/Brain/safety/value/transfer, historical native or overall audit closure. | Required public result is supported; all broader claims remain excluded. |

The complete permitted flow is CONTROL-pinned inputs -> standard CODE venv/pip setup -> TEST's pinned base producer -> three real environment CLI children -> captured outputs/import observations -> before/after preservation measurements -> DOCUMENTATION's two reports/sidecars and eight-entry manifest -> planned fresh read-only review -> CONTROL decision. Remote artifacts enter only through CODE's standard installer. No remote access is part of TEST or DOCUMENTATION.

The checklist is bounded, not a universal threat model. Unknown interpreter/native closure, authority mutability/rebinding, hostile index/redirect behavior, Windows lifecycle defenses, concurrency and secure output production remain **unverified**. Neither positive command results nor a future review may silently turn them into verified prerequisites. If an unexplained failure needs a second speculative correction, TEST must first provide a discriminating diagnostic matrix; repeated hypothesis-only edits are not authorized.

## Evidence interpretation and output contract

The authenticated JSON reports one producer run with exit `0`, all four substantive subprocesses returning `0`, 631 recorded assertions and zero failed assertions. The assertions include repeated integrity authentication; there are not 631 independent tests. Existing public byte equality and all 122 before/after file measurements passed, and DOCUMENTATION's later hash-only authentication found the same inputs. Existing public-bundle inventory has 91 files including its manifest; the public payload manifest itself contains 90 entries. The source inventory contains 11 files. Both recorded inventories had zero extra, missing, reparse or root-chain reparse entries.

`rpds.cp312-win_amd64.pyd` was an ordinary installed dependency import. There was no project-native preloader/Win32 rehearsal, historical full 36-test rerun, schema/bundle edit, new fixture, model/provider call, or historical expected-pin update. Documentation records CODE/CONTROL setup and preflight statements as attributed handoff evidence; it does not present them as independently rerun checks.

DOCUMENTATION writes only these five files in `C`: `README.md`, `README.sha256`, `SCOPE-AND-CHECKLIST.md`, `SCOPE-AND-CHECKLIST.sha256`, and `artifact-files.sha256`. Each Markdown sidecar is lowercase SHA-256, two spaces, its Markdown basename, and LF. The manifest is ASCII path-sorted and contains exactly these eight candidate-relative entries: `README.md`, `README.sha256`, `SCOPE-AND-CHECKLIST.md`, `SCOPE-AND-CHECKLIST.sha256`, `requirements.lock.txt`, `tests/verify_public_cli.py`, `verification/test-results.json`, and `verification/test-stdout.txt`. It excludes itself, any later disposition, external `.gitignore`, and local generated environment files. Never copy interpreter or dependency binaries into these records.

Document validation uses the pinned native `verify-text-artifacts.ps1` with `-SelfTest`, then `-Path` for each Markdown file, checking each immediate native exit code. This verifies text encoding/format and sidecar integrity, not the substantive CLI result or an independent review. The final five output pins are handed to CONTROL after validation.

The next authorized role is a fresh independent reviewer. Its planned staged input sequence must be frozen separately; it is not fulfilled by reading this document. Overall audit/maintenance closure still needs the remaining work and a separate completion audit. No Git mutation or publication was performed by DOCUMENTATION, no publication approval is implied, and the existing unclassified-status blocker remains unchanged.
