# A05 profile composition v0.3

Date: 2026-09-17. Status at this documentation handoff: **TEST PASS; INDEPENDENT REVIEW PENDING; no CONTROL acceptance or integration.** This is an auxiliary public-source correction within the F01-F08 remediation. It does not close F03 as a whole.

## Change and bounded result

CODE changed only `SuccessorProfileMaterial.__post_init__` in `implementation/s0_public_runtime_preloader/profile.py` relative to v0.2. Three reflective `getattr` read sites became explicit `(name, self.field)` tuples for six raw-byte fields, two current-file maps, and six other maps. The bounded checks retain their field order, exact-type requirements, errors, digest check, and immutable snapshots. The other nine modules, including `source_audit.py`, remain byte-identical to v0.2; the checker policy was not relaxed.

TEST `/root/audit_a05_test_resumed` completed one run with reported exit 0: **56 PASS, 0 failures, 0 errors**. The authenticated [JSON results](verification/test-results.json) and [stdout](verification/test-stdout.txt) record 47 retained cases and nine new cases. The new cases cover constructor field completeness/order, each field's rejected types, distinct values and nested snapshots, failure order, method-only preservation, and discriminating source checks.

`RealSourceClosure.test_real_exact_ten_candidate_files_pass` passes the ten actual v0.3 source files to the actual checker. JSON records `source_closure_uses_doubles: false`. Each of the three separately reintroduced `getattr` sites is rejected by the same checker, as is the full v0.2 source inventory. Existing missing/extra/nonbyte inventory, import-alias/wildcard/nontoplevel import, disallowed symbol and import checks also pass. The source result is a bounded AST-policy check, not proof of full interpreter, standard-library, native-library, or imported/executed-byte closure.

Retained tests cover historical-first ordering, predecessor/design/schema/map/native failure gates, current manifest and six-row package consistency, immutable Python data flow, and the intended current-versus-historical identities at downstream consumers. These results establish only the branches actually tested below.

## Positive-branch doubles and remaining limits

The JSON's `mocked_prerequisites` explicitly records these substitutions:

- Positive composition uses a coherent data-only P4 wrapper in place of a successful full historical validator. P1-P3 pin constants use harmless unit-parameter hashes; P4 remains the actual pinned raw input.
- Positive design and native gates are no-op call spies. Overlay schema validation is a no-op for the minimal overlay; actual v0.5 schema and interface-map byte pins remain checked.
- Downstream launch parsing, identity, evidence, precreation and admission are real on that isolated positive branch, with the same unavailable upstream gates doubled. Negative diagnostics may replace preceding gates solely to isolate the target gate.
- The 512-file bound is tested without replacement. The byte-limit test temporarily sets `_MAX_RUNTIME_BYTES` to 3, so it does not demonstrate a full 512 MiB allocation test.

No double establishes a complete positive historical/P4, native, runtime, or assembly integration result. Caller-supplied coherent data and expected hashes are not trusted execution authority. Tests do not establish hostile concurrent getter/global/interpreter safety. Native binary virtual-path mapping to the current runtime manifest, actual executed/imported identity, installed interpreter/stdlib/native closure, and complete historical prerequisites remain **UNVERIFIED**.

Windows ACLs, root/volume identity, symlink/junction/reparse behavior, rename/replacement, retained handles, repository exclusion, and TOCTOU through final output/evidence writes remain **UNVERIFIED**. Ordinary output ancestry observations are not hostile-filesystem isolation. External URL, redirects, digest, size and provenance verification, native handle-close behavior, cleanup safety and full execution safety are also unverified. No native/provider/network execution was authorized by this candidate.

## Authenticated evidence and command

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`. Branch: `codex/windows-build-toolchain-environment-v0.1`. HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`. Tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. Root `AGENTS.md`: `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.

The exact command in JSON used Python 3.12.10; executable SHA-256 is `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a05-profile-composition-v0.3/tests/test_profile_composition.py'
```

This records the completed invocation; DOCUMENTATION did not rerun it. The test script refuses to overwrite existing results. Any future authorized rerun needs its own exact output arrangement and must preserve these frozen artifacts.

| TEST artifact | SHA-256 |
| --- | --- |
| `tests/test_profile_composition.py` | `b43f60b24999571d8654e3d1de337fc58ec47cf23b00b3483cbb77218f111631` |
| `verification/test-results.json` | `8bce9f03218f3070ab456704d183a8f9b2f7ce10591031735598825394ee414b` |
| `verification/test-stdout.txt` | `a1f0500882178e9750d5a9d174abdb391b315f1875ebae9eeb0722443a56166f` |

JSON's `pre_input_sha256` and `post_input_sha256` contain the same 60 exact input hashes. TEST reported those inputs unchanged after output production; DOCUMENTATION separately authenticated their current hashes using only the permitted hash-only inventory. The JSON records imported repository-module paths and ordinary non-reparse output ancestry observations; these are evidence-producer observations, not a hostile trace or enforced isolation proof. All 13 v0.3 CODE/TEST input pins are frozen in [SCOPE-AND-CHECKLIST.md](SCOPE-AND-CHECKLIST.md); [candidate-files.sha256](candidate-files.sha256) freezes the 17-artifact handoff and excludes itself and any later disposition.

## Authorization, preservation and next role

CONTROL reported that the user approved one additional bounded correction, regression run and fresh review after the 20-40 minute auxiliary-work estimate and the cheaper fallback of preserving the failure and deferring correction. Commit and push were expressly excluded. That contextual assent opens v0.3 only. A further unresolved candidate failure or scope expansion returns to CONTROL/user decision. Thirty minutes remains a progress/value checkpoint, not an automatic stop.

The preserved v0.2 disposition records 47 tests, 46 passes and one error before independent review. v0.1's prior rejection and frozen evidence remain historical; their hashes were not rewritten to create a pass. Recovery-only snapshots are not runnable candidates or automatically admitted role inputs. This document includes historical status for CONTROL/DOCUMENTATION; a fresh reviewer's primary input/exposure order must be separately frozen before release.

CODE, TEST and DOCUMENTATION are separate roles. CONTROL plans a fresh read-only `gpt-5.6-sol` reviewer at ultra reasoning: first, pinned C3/C2 source and neutral frozen requirements only, with a primary assessment before TEST counts/results, README or scope; then explicit release of the final packet for evidence/document consistency review. This is planned, not completed or proof of enforced isolation. No verdict is inferred from the test count. CONTROL `/root` continues under the bounded 2026-09-16 remediation authorization and is not an independent reviewer. Shared files, logs, indexes and session replacement do not establish enforced read isolation.

The baseline remains `central-system-v2.1-s0-preparation`. F0 content, hidden oracle and S0/E0 fixture creation, execution/scoring and real provider calls remain closed. Central-system/Project Brain integration, operational safety, economic value and model-to-model transfer are not implemented or validated by this work. No Git mutation or publication is authorized here; the opaque unclassified-status blocker remains unresolved and unwaived.
