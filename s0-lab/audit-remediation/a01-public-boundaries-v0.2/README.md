# A01 public boundaries v0.2

Status at documentation freeze: bounded verification passed; fresh independent review and CONTROL disposition pending. This packet contains no earlier review verdict. Later decisions must be recorded separately without rewriting this freeze.

This is auxiliary tooling/evidence work: the sole new correction rejects Windows delete-on-close flags in the F-02 file-open sentinel. It preserves the F-04 stream-enumeration correction from v0.1. It does not establish S0/E0, central-system implementation, Project Brain integration, operational safety, economic value, or model transfer.

## Authority and identity

- CONTROL records the user's 2026-09-16 `진행` authorization for a 10–20 minute continuation, approximately 07:18–07:38 UTC. This extends only the auxiliary time limit for this correction; no F0, isolation, Git-publication, or experiment exception is granted.
- Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`; branch: `codex/windows-build-toolchain-environment-v0.1`.
- Base HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. Candidate files are working-tree artifacts, not a committed candidate tree.
- Root `AGENTS.md` SHA-256: `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065`.
- Roles: CONTROL `/root`; CODE `audit_a01_v02_code`; TEST `audit_a01_v02_test`; DOCUMENTATION `audit_a01_v02_docs`; fresh read-only INDEPENDENT REVIEW assigned next by CONTROL. No role absorbs another role's actions.
- Sequence: CONTROL freeze → TEST-owned v0.1 failure-isolation diagnostic → CODE → final TEST → DOCUMENTATION → fresh INDEPENDENT REVIEW → CONTROL decision. The pre-CODE diagnostic is failure isolation, not a replacement for the final TEST handoff.
- One opaque unclassified Git-status blocker remains. No staging, commit, push, PR, merge, F0 content access, model/provider call, installation, or S0/E0 execution is authorized here.

## Exact packet and preserved inputs

`artifact-files.sha256` pins 18 files relative to this directory: nine implementation files, three test files, four evidence files, this README, and its sidecar. The manifest excludes itself; its hash is supplied in the CONTROL handoff. Only the exact manifest entries are candidate inputs; the manifest does not authorize directory discovery or adjacent files.

The preserved v0.1 manifest is `../a01-public-boundaries-v0.1/artifact-files.sha256`, SHA-256 `d583db794052e751a03200bee65a278fa06c2dc943011482e58d9c34f48e654a`. Its metadata releases only its nine implementation files and `tests/test_runtime_guard.py` / `tests/test_stream_inventory.py` for this packet; its earlier documents, results, and disposition are excluded. Those tests are pinned respectively to `9b6795262f8fa8fb6b1b0a2e98d17e78ee4d199041918acae37ccca20b326bfa` and `4733df59dc05a30c2a8ec2c7e35b9a90d8e6f8f30f5d3be79632a735e64d3496`.

The additional baseline release is exactly seven files under `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/`: candidate `runtime_guard.py`, `errors.py`, `storage.py`, `constants.py`; verifier `win32.py`, `errors.py`, `models.py`, each in its corresponding `s0_public_assembly_candidate` or `s0_public_assembly_verifier` package. Pins are recorded in the final JSON `before.baseline_sha256` and `after.baseline_sha256`; no package-init or other baseline file is released.

The nine v0.2 implementation files match v0.1 except `s0_public_assembly_candidate/runtime_guard.py`, now SHA-256 `811f1df27a44d70948f3e37fedcba976189fd5b58ff61a6e029c14d74c768f7a`. The change checks integer legacy flags and the third flags argument independently and invokes the existing latched denial for `O_TEMPORARY` before either read or pending-write allowance. Existing `None` validation and ordinary flag classification remain in place. File-descriptor authority is outside this bounded path-based claim.

## Frozen adversarial checklist

The following records CONTROL's pre-CODE freeze, not a post hoc expansion. Each row assigns CODE action, TEST expectation, documentation boundary, and fresh-review closure.

| Row | CODE owner/action | TEST expected discrimination | DOCUMENTATION limit | REVIEW closure |
| --- | --- | --- | --- | --- |
| A | CODE preserves the exact nine-file inventory and pins except the owned correction. | Authenticate candidate, old candidate, baseline, and actual imported byte paths before/after. | Python, stdlib, native libraries and OS are trusted; secure import closure is unverified. | Pins, inventory and import paths agree; no stronger closure claim. |
| B | CODE denies delete-on-close unconditionally within path-open classification before read/write allowances. | Reject `None`, legacy integer, string-plus-third-flags, conflicting dual representations, benign/write-bit mixes and both pending paths; preserve bytes and latch denial. | Claim only the frozen flag/path cases; no pending or approved-read escape in those cases. | Both integer representations are checked independently; measured calls reject before OS open. |
| C | CODE preserves invalid-`None` rejection and ordinary semantics. | Missing/bool/noninteger/negative flags reject; ordinary reads, pathlib, os.open, storage and pending writes retain expected behavior. | All-platform and unknown/future-flag completeness remain unverified. | Source and regression cases support preservation without broadening authority. |
| D | CODE preserves inherited F-04 bytes. | API doubles cover EOF 38, enumeration/close failure, error capture and rejection classes. | This is regression evidence, not native ADS/publication validation. | Unchanged source/test pins and bounded observations support only that claim. |
| E | CODE retains argument → classification → rejection or lexical allowlist flow. | Controlled OS scratch → parent byte observations and child latch/health observations; no newly minted authority. | FD authority, mutable globals, introspection, caller-mintability/rebinding attacks and hostile concurrency remain unverified; no URL/download flow is introduced. | No new authority source or execution path; no claim that the in-process sentinel is an OS sandbox. |
| F | CODE makes no Windows path-lifecycle redesign. | Existing bounded benign checks only; no hostile lifecycle case is promoted to proof. | ACLs, volume/root identity, symlink/junction/reparse behavior, rename/replacement, retained handles, repository exclusion and TOCTOU through output/evidence writes remain unverified. | Those prerequisites block broader security claims and remain explicit. |
| G | CODE preserves owner-specific sources; TEST owns scripts/results; DOC owns manifest/sidecar. | Exact command, producer/source pins, pre/post measurements, failure/close behavior and zero scratch residue. Preserve diagnostic evidence separately. | Evidence producer and output root are trusted, not security-proven. | Frozen diagnostic is distinct from final evidence; command provenance, resource bounds and cleanup are consistent. |
| H | CODE corrects only the isolated delete-flag defect; no architecture change. | TEST supplies diagnosis before correction and never fixes CODE. | One-purpose 10–20 minute extension, no additional Git/F0/experiment gate. | Separate roles, bounded scope and time limit; further speculative correction returns to CONTROL. |

## Recorded measurements

The frozen pre-CODE diagnostic consists of `tests/test_delete_on_close.py`, `verification/delete-on-close-diagnostic.json`, and `verification/diagnostic-stdout.txt`. It made four actual installed-sentinel v0.1 child observations on disposable Windows files: ordinary approved reading retained the file; approved and pending `O_TEMPORARY` opens were allowed and removed their files on close; the forbidden path was denied, latched, and retained. `O_TEMPORARY` was 64. These original script/evidence bytes are preserved and must not be rerun or overwritten.

Final evidence is `verification/test-results.json` and `verification/test-stdout.txt`. TEST records 26 tests, 332 subtests, zero failures/errors/skips, 31 child observations and 36 F-04 API-double observations. Eighteen actual `O_TEMPORARY` combinations (approved file and both pending names × read-only and five write bits) rejected before open, with parent-side byte equality and child-side latched read/health checks. The stream test is byte-identical to v0.1. The harness elapsed time was 2.766 seconds; unittest reports 2.473 seconds. Scratch residue was zero. Pre/post pins and identity agreed for v0.2 nine files, v0.1 nine files, baseline seven files, and the frozen three diagnostic files.

Interpreter: `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe`; `3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]`; isolated mode 1, no-site 1, bytecode writing disabled. Final JSON records imports under the exact v0.2 `implementation/` directory: candidate `__init__.py`, `constants.py`, `errors.py`, `runtime_guard.py`, `storage.py`; verifier `__init__.py`, `errors.py`, `models.py`, `win32.py`. The earlier diagnostic records v0.1 imports separately.

Recorded reproduction command, from the repository root:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B 's0-lab/audit-remediation/a01-public-boundaries-v0.2/tests/test_runtime_guard.py'
```

This command writes final evidence. Fresh review is read-only and MUST NOT run it or the diagnostic. Any later authorized reproduction must preserve these frozen bytes and obtain a separately assigned output/version. DOCUMENTATION authenticated evidence and did not rerun substantive tests.

No full native publication/controller lifecycle, actual ADS exploitation, hostile OS isolation, hostile interpreter/import closure, arbitrary same-process tampering, race/concurrency safety, or exhaustive platform compatibility is established. The active project baseline remains `central-system-v2.1-s0-preparation`.

Canonical documentation validation uses `s0-lab/control/tools/verify-text-artifacts.ps1`, SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`, first `-SelfTest`, then `-Path` for this README in native Windows PowerShell. Actual outcomes and the three final document hashes are supplied in the documentation handoff, avoiding a self-referential hash claim.
