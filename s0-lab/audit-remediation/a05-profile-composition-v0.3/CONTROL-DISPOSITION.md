# A05 v0.3 CONTROL disposition

Date: 2026-09-17. CONTROL `/root` decision: **ACCEPT-BOUNDED-SOURCE-REMEDIATION**. The explicit-field constructor correction and matching regression evidence are accepted for this bounded source claim. **F03 is not fully closed; integration, historical/native execution and Git publication are not accepted or authorized.**

Fresh INDEPENDENT REVIEW `/root/audit_a05_v03_review` reported **PASS - bounded source remediation only**, with no Critical, High, Medium or Low in-scope findings. This DOCUMENTATION record attributes the verdict to that reviewer and the decision to CONTROL; it is not a new review or test run.

## Accepted change and evidence

The implementation delta from v0.2 is confined to `profile.py` lines 294-321, `SuccessorProfileMaterial.__post_init__`: three reflective reads become explicit field/value pairs. The six byte checks, digest check, two current-map snapshots and six other-map checks retain their tested order, exact types and errors. The other nine modules, including the source checker, remain byte-identical to v0.2.

TEST recorded 56/56 PASS: 47 retained cases plus nine new cases. The reviewer confirmed actual ten-source checker acceptance without doubles; rejection of each of three separate `getattr` reintroductions and the exact v0.2 inventory; field-type/order/distinct-value/recursive-snapshot/caller-mutation checks; and preservation of bytes outside the method. JSON/stdout agree, the stdout digest matches, and recorded repository imports are limited to the test and ten C3 modules. Positive upstream historical/design/native/schema/P1-P3 doubles remain explicitly disclosed and establish no complete positive integration result.

The reviewer authenticated all 60 frozen input paths/hashes against pre/post/current values, the sorted 17-entry manifest, canonical SelfTest 11/11 PASS and both frozen Markdown/sidecar checks. The reviewer ran no candidate or tests, wrote no files and made no Git mutation; its executable checks were documentation checks only. CONTROL separately reauthenticated all 60 input hashes and 17 packet hashes at **2026-09-17 03:25:39 UTC**, with HEAD/tree unchanged. These are integrity observations, not another test run or verdict.

## Review exposure and completed roles

The reviewer was a fresh `gpt-5.6-sol` session at ultra reasoning, `fork none`, read-only, with no prior v0.3 role. Phase 1 admitted only AGENTS and 20 pinned C2/C3 source files with neutral frozen requirements. Its primary assessment reached CONTROL before tests, results, README or scope were released and found no material in-scope source defect. It noted that eager tuple evaluation can differ for manually malformed missing-attribute objects, hostile `__getattribute__`/subclasses or concurrent mutation; those cases are outside the frozen normal exact-class constructor claim.

Phase 2 explicitly released the current 17-file packet and manifest, C2/C1 comparison test source, canonical validator and exact 60-input hash-only inventory. Historical comparison facts in current documentation were exposed only after the primary assessment; prior verdicts/reports were not directly read. The supported independence claim is a fresh source-first assessment followed by evidence review, not an outcome-blind review of the whole final packet or enforced read isolation.

CONTROL `/root`, CODE `/root/audit_a05_v03_code`, TEST `/root/audit_a05_test_resumed`, DOCUMENTATION `/root/audit_a05_v03_docs` and the fresh reviewer completed the required sequence without dual-role absorption. The existing root remains CONTROL under the prior bounded-remediation exception. Shared files, logs, indexes or new sessions do not enforce isolation or retroactively cure earlier procedural failures.

## Exact identity and preservation

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`. Branch: `codex/windows-build-toolchain-environment-v0.1`. HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`. Tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.

| Artifact | SHA-256 |
| --- | --- |
| Root `AGENTS.md` | `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` |
| `candidate-files.sha256` | `a0fb92b746d399b4fe0e079187828ff21c1312b875681be7f8e8aea1804cc287` |
| `implementation/s0_public_runtime_preloader/profile.py` | `efae38b6a99763c0dca61efe2813c11672cf784a28ea1f0747937f80e260501a` |
| `implementation/s0_public_runtime_preloader/source_audit.py` | `50399a565232136736e041ea028b76ed8767d18327553ecf2ec6ec5b0bfe2d36` |
| `tests/test_profile_composition.py` | `b43f60b24999571d8654e3d1de337fc58ec47cf23b00b3483cbb77218f111631` |
| `verification/test-results.json` | `8bce9f03218f3070ab456704d183a8f9b2f7ce10591031735598825394ee414b` |
| `verification/test-stdout.txt` | `a1f0500882178e9750d5a9d174abdb391b315f1875ebae9eeb0722443a56166f` |

All 17 packet files and their manifest retain their original bytes. README/scope intentionally retain PENDING-at-freeze wording; this later record supplies the completed disposition. These two new disposition files are excluded from the original manifest by design. v0.1's rejection and v0.2's TEST failure retain their original hashes/outcomes; neither receives a retroactive pass. The authorized one-additional-correction has completed; no fourth candidate is needed or opened.

## Limits and remaining gates

Full positive historical P4/native/assembly execution, current native-path mapping, actual executed/imported identity, installed interpreter/stdlib/native closure, hostile concurrency/OS behavior, Windows lifecycle/TOCTOU, external provenance and native cleanup/close remain **UNVERIFIED**. Complete missing historical/runtime prerequisites are still required for broader claims.

The baseline remains `central-system-v2.1-s0-preparation`. No F0 content/access exception, security weakening or research gate is opened. S0/E0, hidden oracle and provider execution remain closed; central-system/Project Brain integration, operational safety, economic value and model transfer remain unestablished. No integration, staging, commit, push or other Git mutation occurred or is authorized by this disposition. The opaque unclassified-status blocker remains unresolved and unwaived.
