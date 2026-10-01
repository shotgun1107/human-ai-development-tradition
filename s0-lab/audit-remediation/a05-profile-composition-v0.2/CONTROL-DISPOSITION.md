# A05 v0.2 CONTROL disposition

Date: 2026-09-17. Candidate: `a05-profile-composition-v0.2`.

CONTROL (`/root`) decision: **FAILED-AT-TEST — NOT ACCEPTED. INDEPENDENT REVIEW NOT REACHED. USER DECISION REQUIRED BEFORE A THIRD CORRECTION CANDIDATE.** This DOCUMENTATION record attributes the decision to CONTROL and the verification results to TEST; it is not an independent review.

## Authenticated candidate and result

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`; branch: `codex/windows-build-toolchain-environment-v0.1`; HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. Root `AGENTS.md` SHA-256: `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.

CODE `/root/audit_a05_v02_code` changed only four sets in `source_audit.py`: admit `dataclasses.replace` and `.profile.ValidatedSuccessorProfileCandidate`; remove the profile's direct `copy` and module-attribute `copy.deepcopy` allowances. The other nine implementation files remain byte-identical to v0.1. Checker algorithms, other constants and native inventory remain unchanged; TEST's exact-delta cases pass.

TEST `/root/audit_a05_test_resumed` retained 36 cases and added 11 methods: **47 run, 46 PASS, 0 assertion failures, 1 ERROR**. The actual `RealSourceClosure.test_real_exact_ten_candidate_files_pass` calls `inspect_source_structure` on all ten exact candidate files without a checker double. It errors at `source_audit.py`:297 with `RuntimeProfileError: candidate source uses dynamic or ambient authority at #`. The [results](verification/test-results.json) and [stdout](verification/test-stdout.txt) preserve this failure.

The command recorded in JSON uses Python 3.12.10; TEST reported exit 1. DOCUMENTATION did not rerun it:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a05-profile-composition-v0.2/tests/test_profile_composition.py'
```

TEST separately reported a read-only per-file/AST diagnosis: nine source files pass; only `profile.py` fails. Its `SuccessorProfileMaterial.__post_init__` contains forbidden `getattr` Name loads at lines 299 (`type(getattr(self, name))`), 303 (`_snapshot_current_files(getattr(self, name), name)`) and 308 (`value = getattr(self, name)`). These sites are visible in the pinned source. This is an attributed diagnostic report, not an additional durable diagnostic artifact or a per-file matrix inside the 47-test JSON.

Passing data-flow positives retain explicitly labelled upstream historical, design, native and schema doubles. They establish neither a complete positive historical validation nor a native integration pass. JSON's 47 pre/post input hashes match; TEST also reported unchanged inputs after output, preservation of v0.1's original 17 artifacts plus three diagnostics and the ten v0.2 source files, and unchanged Git identity. DOCUMENTATION compares inventory metadata without admitting the contents of additional paths named there.

## Exact v0.2 input pins

Paths are relative to this candidate directory. The first ten filenames are under `implementation/s0_public_runtime_preloader/`. These 13 artifacts were hash-authenticated before this record; its Markdown and sidecar are separate outputs.

| Artifact | SHA-256 |
| --- | --- |
| `__init__.py` | `a2e40d7a44f79f3c0f96b790c2249fcb6efe7dba2abf821ea3ee96302f1570c3` |
| `canonical.py` | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` |
| `errors.py` | `20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86` |
| `evidence.py` | `e0f1d9de22eb8b7a727dbef146f808c59d44accbbb96fa3367ee2d0dfdbdd964` |
| `integration.py` | `7d40c5091c43354287fade09f8e11d2ca6a830492d390385d8b13cee361a3dfd` |
| `preloader.py` | `718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee` |
| `profile.py` | `0c0c451a0be41c5593fb3937192da61ae1728534d12e114e0fda9b7a4e297c14` |
| `schema.py` | `97b00ab0bb9417b63c5871332751e8c14dea80423414810e99aa2b443f9d6317` |
| `semantic.py` | `1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d` |
| `source_audit.py` | `50399a565232136736e041ea028b76ed8767d18327553ecf2ec6ec5b0bfe2d36` |
| `tests/test_profile_composition.py` | `c06c03bcef51ca143f078aab5f9fe0ca3d959e46abf250d0a77f6f53c56c0de1` |
| `verification/test-results.json` | `ea204f87902ea5accc53ee0188a2c3a90a1d3288a9a086475e07fd72dff56433` |
| `verification/test-stdout.txt` | `296546ef7fef781821d9060278a10ef1fdd214b774899f56a47343c357f5d518` |

The authenticated [v0.1 disposition](../a05-profile-composition-v0.1/CONTROL-DISPOSITION.md) remains at `3c1f38aba7962a9dfa34b317d9f84227f3266223de1532cd91ee53a0ce5d007b`; its original manifest remains at `b2505ce58732de16185f434f9e4ece1c8c2345aba80bc165f3a2df43cc217802`. Original hashes and failure evidence are preserved.

## Role status and continuation boundary

CODE and TEST completed their actions. DOCUMENTATION `/root/audit_a05_v02_docs` records the failure. INDEPENDENT REVIEW remains unreached because mandatory TEST did not pass; no v0.2 review verdict exists, CONTROL does not absorb that role, and the five-role gate is not successfully completed.

v0.1 received one independent P1 rejection. v0.2 failed mandatory real TEST; it did not receive a second independent-review rejection. CONTROL conservatively applies the repeat-correction boundary after these two candidate attempts and requests a user decision before any third candidate. No v0.3 correction is opened. This is not a 30-minute elapsed-time stop.

The proposed next step is auxiliary tooling/evidence work only: replace the three reflective access sites with explicit named attribute/value pairs, preserving order, exact type checks and immutable snapshots. Keep `getattr` forbidden and retain the existing audit policy. The isolated cause makes this a bounded proposed correction, not a guaranteed pass. Reuse the existing checker and 47 regressions, including actual all-ten-file closure, then DOCUMENTATION and a fresh independent review. Expected useful output is a candidate eligible for that review, with no new framework, native execution or artifact fixture. Estimated cost: 20–40 minutes. The cheapest fallback is to leave this failed candidate preserved and defer further correction; doing so leaves its self-source closure blocker unresolved. Any scope expansion or further unresolved rejection returns to CONTROL/user decision, not automatic additional corrections.

Complete historical material, current native-path mapping, executed/imported byte identity, full interpreter/stdlib/native closure, Windows path lifecycle and TOCTOU, external provenance and full integration remain unverified. F0 access, hidden-oracle or S0/E0 fixture creation, S0/E0 execution/scoring and real provider execution remain closed. The baseline remains `central-system-v2.1-s0-preparation`; no central-system or Project Brain integration, operational safety, economic value or model transfer is established. The prior unclassified Git-status blocker remains unresolved and unwaived, with no publication approval or Git mutation.
