# A07 CONTROL disposition

Decision date: 2026-09-29 (Asia/Seoul).

**CONTROL decision: ACCEPT the bounded current-host public CLI readiness of `a07-public-cli-readiness-v0.1`.** The existing A04 public CLI successfully ran with real jsonschema in the prepared local environment, and the assigned fresh reviewer returned PASS with P0/P1/P2/P3 finding counts all zero.

This records CONTROL's decision, authored by DOCUMENTATION from the final CONTROL handoff. The review findings and review sequence below are attributed to that handoff, not a direct reviewer transcript inspected by DOCUMENTATION. DOCUMENTATION does not issue an independent verdict.

The accepted result applies to the existing public-input scope and the recorded source/environment on this host. The source and environment remain usable under that unchanged authorization. This disposition does not itself grant new execution, installation, experimental, or publication permission, and does not complete the wider audit/maintenance goal.

## Identity and roles

Repository `P`: `C:/Users/SSAFY/Documents/ai-development-tradition`.

Candidate `C`: `P/s0-lab/audit-remediation/a07-public-cli-readiness-v0.1`.

A04 source `A4`: `P/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1`.

Environment `E`: `P/.venv-public`.

| Identity | Frozen value |
| --- | --- |
| Branch | `codex/windows-build-toolchain-environment-v0.1` |
| HEAD | `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` |
| HEAD tree | `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` |
| Active baseline | `central-system-v2.1-s0-preparation` |

| Role | Assigned session and contribution |
| --- | --- |
| CONTROL | `/root`: freeze, evidence integration, final ACCEPT decision |
| CODE IMPLEMENTATION | `/root/audit_a07_code`: standard local venv/pip setup, locked requirements, one ignore entry |
| TEST/VERIFICATION | `/root/audit_a07_test`: producer and one bounded verification run |
| DOCUMENTATION | `/root/audit_a07_docs`: frozen reports/sidecars/manifest and this separate disposition pair |
| INDEPENDENT REVIEW | `/root/audit_a07_review`: fresh read-only `gpt-5.6-sol`, ultra reasoning, `fork none`; source/configuration-first primary assessment, followed by evidence review and final PASS |

CONTROL reports that the reviewer's primary source/configuration assessment completed before test counts, results and documentation were released. The final review then examined those outcomes. This is a procedural staged source-first review, not an outcome-blind final review or proof of enforced filesystem isolation.

## Frozen packet and prerequisites

The eight-entry candidate manifest SHA-256 is `109d3a954fc5685b65f9642c5fc03270cd4f4ec4277f0cbda9d64be53f988b2f`. CONTROL reports authenticating it and every entry unchanged after review. DOCUMENTATION independently authenticated that same frozen packet before authoring this disposition.

| Candidate-relative artifact | SHA-256 |
| --- | --- |
| `README.md` | `9d94b2b9dc1e11083b36ced15bce5c5337af8b69416b831d82e8f8070591ff74` |
| `README.sha256` | `db4ae5b4b171d02b4733f9df3103c48d0c0bc02193cc7049a857d2482859d513` |
| `SCOPE-AND-CHECKLIST.md` | `79aa9f55034e36f20e1819035319651f922cd837a7dbd19810f589caf497d4a3` |
| `SCOPE-AND-CHECKLIST.sha256` | `54b346ff415943eba0a5292f83b7390c528a7dd4c7b35ba5cf53d3d8f32e8fc8` |
| `requirements.lock.txt` | `58a76393ebeb1d098c09bd74713704673d4b2c768162bb903145e7d2acbd9c71` |
| `tests/verify_public_cli.py` | `b29360f0844a405dbc72bbeece4d98552eb21ade006efee064fbd638bd7b5625` |
| `verification/test-results.json` | `011fb8de441c82ac975e649648495e752cf7afa581bfd9df4131a5f764f6a1ea` |
| `verification/test-stdout.txt` | `0f3beb4f388b518c7fc34bfa3a0b9762b412c106e8530a9826ba36045f6d6607` |

The following external authorities and host prerequisites retain the recorded pins. Generated environment files remain local; they are not candidate-manifest entries.

| Exact prerequisite | SHA-256 |
| --- | --- |
| `P/AGENTS.md` | `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` |
| `P/.gitignore` | `93b0ba1fee168778488b7839f3094b9f2c137399aafea117a3dc417a6ddd718a` |
| `E/Scripts/python.exe` | `0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14` |
| `E/pyvenv.cfg` | `6d7ac85012ab1132ed60a62b8ead1d23b2a29f658e90b443babbe9e6464feb68` |
| `E/install-report.json` | `3df056b8d8c3ba50349cd3b8fe8d379f60280af55e6c408153a930607458767c` |
| `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe` | `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` |
| `A4/artifact-files.sha256` | `3188bfb5d5745b83a0f07f8134e2021d63285c8591db1698eca02e6086fc3f68` |
| `A4/requirements.txt` | `d0bc9baee84543883a0a966d477620161876536b552742ab6409d1da50251405` |
| `P/s0-lab/public-practice/v0.1/bundle-files.sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` |
| `P/s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

The exact existing implementation pins, relative to `A4/implementation/s0_i0/`, are:

| Source | SHA-256 |
| --- | --- |
| `__init__.py` | `b49749dd2446520cb9e640dd33934ced9267f33ccc9c911fe93f9ed2afb439ed` |
| `answer_validation.py` | `ed8026ac8497e5571e957903b9de43d3007698d2d95fcae20f7556974f138928` |
| `authentication.py` | `d970660ac960020df64f1a31cfc5e5d452796ca8095b301d36684403b25c1a6e` |
| `cli.py` | `819edaf785558b620aa7b79036560d4fb895d7ce513a5cc4173fad04df8e43f9` |
| `error_reporting.py` | `4ac26d811b3842c95be513136d765e5e0abf62498e12227812be5bd277a7206e` |
| `integrity.py` | `6e6e6093f5cf8fe81a58e6bb67f85477db0abe97e4b68a4d04bd2d0e574ba7f4` |
| `json_validation.py` | `3298aa7fbee3d4744d9370d34c1c67fb028ca8bda4b49907eeeea488c7b1ef89` |
| `paths.py` | `3884c3372ee72df7807d0c65f3b192d11e53a50e1da0c65ef9d0cdfe71e86111` |
| `schema_suite.py` | `efabf23d7d60a5527b0ea6815d1cd9b51ba57891641d7db134be58b5ca171295` |
| `transform.py` | `80ffaf4d0eeed1d8a8071972dd40339f18eb63cb4cbe9af76b2c015fbffc53d2` |
| `verification.py` | `4857c2b8776bd23d1a84c7e64094440dce561ba00c845c152052c89cbdd9e7f6` |

The public bundle's exact 90 paths/hashes remain defined by its pinned manifest. The exact eleven schemas and hashes remain defined by `FROZEN_SCHEMA_HASHES` in the pinned `schema_suite.py`, relative to `P/s0-lab/control`. The JSON's before/after maps retain the full 122-input preservation record. These references do not broaden any role's content allowlist.

## Review evidence closure, as reported by CONTROL

CONTROL's final handoff reports that the reviewer authenticated the eight artifacts, repository identity, policy and validator pins, and reached these conclusions:

- The JSON is coherent with a passing producer, exit `0`, 631 assertion records and zero failures. Most assertions are repeated authentication checks, not 631 independent tests. The transcript exactly reproduces all nine command records, including the five Git identity/configuration checks.
- The four substantive subprocesses were `pip check`, `integrity`, `schema-check` and `verify`, each executed once with exit `0`. Actual origins for all eleven A04 modules and real jsonschema 4.26.0 from the project venv were observed. Installed metadata showed the exact eighteen locked packages plus bootstrap pip 25.0.1.
- The reviewer independently derived the 122 admitted inputs and found their current, pre-run and post-run hashes/sizes equal. Source and public-bundle inventories had zero extra, missing or reparse entries.
- Public integrity covered 90 entries, including 56 JSON files and eight packages. Schema checks covered eleven designated schemas with zero designated or broader-impact errors. Eight package byte sequences generated in memory matched the existing public packages.
- All eighteen lock and receipt entries agreed. The canonical validator SelfTest and both frozen Markdown/sidecar checks passed.

The reviewer resolved the primary-assessment questions with these limits intact. Wheel sizes and setup-index provenance are supported by the attributed CONTROL/CODE handoffs; they are not supplied by the pip receipt and are not independent supply-chain proof. Complete base/global/documentation-environment package trees were not measured, and that stronger preservation claim is not made.

The published read-only commands were assessed as statically equivalent calls to the tested handler arguments without the observation wrapper. The reviewer did not rerun the CLI. Full interpreter/stdlib/native closure and hostile Windows lifecycle, replacement, TOCTOU and concurrency defenses remain unverified.

## Decision boundaries and preservation

The acceptance establishes the existing A04 public CLI's bounded readiness with the recorded Python 3.12.10 environment and jsonschema 4.26.0 on the current host. It does not establish portability or future unchanged state. A changed source, dependency, interpreter or input must not inherit this recorded result without appropriate authentication and already-authorized verification. Historical frozen expected hashes remain attached to their original evidence.

There was no S0/E0 execution or scoring, fixture/oracle creation, F0-content access, real model/provider call, project-native preloader/Win32 rehearsal, or historical full 36-test rerun. The ordinary imported `rpds.cp312-win_amd64.pyd` dependency is not project-native validation. The central system, Project Brain, operational safety, economic value and model-to-model transfer remain unimplemented/unvalidated by this work. Broader audit completion and Git publication are not established; the unclassified-status blocker remains unchanged.

The frozen README and scope document retain their historical `TEST PASS / REVIEW PENDING` status because that was their status at review freeze. This disposition supplies the subsequent CONTROL decision without rewriting those bytes. The original eight entries and `artifact-files.sha256` remain unchanged. This document and its same-basename sidecar are deliberately outside that frozen manifest.

DOCUMENTATION's extension authorizes only `CONTROL-DISPOSITION.md` and `CONTROL-DISPOSITION.sha256`. It includes canonical native document validation (`-SelfTest`, then `-Path` for this file, with immediate exit capture), not CLI/test execution, installation, source/configuration edits, or Git mutation. The pair's final hashes are returned to CONTROL after validation. Concurrent A06/A08 work and all other repository artifacts remain outside this extension's write scope.
