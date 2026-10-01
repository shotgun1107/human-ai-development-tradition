# A05 v0.3 scope and pre-CODE checklist transcription

This DOCUMENTATION file was written **after CODE and TEST**. It transcribes CONTROL's earlier pre-CODE freeze supplied in the role handoff; it does not claim that this file existed before implementation. Checklist rows are bounded requirements and review criteria, not claims that every row received a new test. Actual TEST evidence and its doubles are reported in `README.md`. **INDEPENDENT REVIEW PENDING; no CONTROL acceptance at this freeze.**

## Purpose, authority and ownership

The one-sentence purpose is to remove the three reflective constructor reads that prevent the actual ten-file source inventory from passing its unchanged checker, while preserving the inherited historical/current-profile contract. This is **auxiliary tooling/evidence work** in the authorized F01-F08 remediation, not core system implementation. It reuses the existing checker, constructors and regressions; no new verification framework or environment redesign is proposed.

CONTROL reported user assent to one additional v0.3 correction, regression and fresh review after explaining the 20-40 minute estimate and the cheaper fallback of preserving the failure and deferring correction. This is contextual authorization of that exact non-Git proposal, not generic Git approval. Prior v0.1 rejection and v0.2 TEST failure remain preserved. Further unresolved failure or expansion requires a CONTROL/user decision; no automatic fourth candidate is authorized. Thirty minutes is a progress/value checkpoint, not an automatic stop or extension request.

No F0 exception, security/independence weakening, new experiment gate, S0/E0 fixture or oracle creation, native/provider/network call, installation/deletion, integration, or Git publication is opened. The 2026-09-16 bounded authorization permits the existing root to continue as CONTROL, not to become independent.

| Role | Agent | Exact ownership and boundary |
| --- | --- | --- |
| CONTROL | `/root` | Scope, pre-CODE freeze, pins, allowlists, handoffs, evidence integration and later decision; no candidate code/test/document authoring or independent verdict |
| CODE IMPLEMENTATION | `/root/audit_a05_v03_code` | Ten `C3/implementation/s0_public_runtime_preloader/` modules enumerated below; only `SuccessorProfileMaterial.__post_init__` in `profile.py` changes relative to C2; no test/document edits |
| TEST/VERIFICATION | `/root/audit_a05_test_resumed` | `C3/tests/test_profile_composition.py`, `C3/verification/test-results.json`, `C3/verification/test-stdout.txt`; substantive verification only, no implementation fixes or independent verdict |
| DOCUMENTATION | `/root/audit_a05_v03_docs` | `C3/README.md`, `C3/README.sha256`, `C3/SCOPE-AND-CHECKLIST.md`, `C3/SCOPE-AND-CHECKLIST.sha256`, `C3/candidate-files.sha256`; no candidate/test execution or code/test edits |
| INDEPENDENT REVIEW | Fresh `/root/audit_a05_v03_review`, planned | Read-only primary assessment under its separately frozen exact inputs/exposure order, using `gpt-5.6-sol` at ultra reasoning; no prior role for v0.3 or artifact edits |

Sequence: CONTROL freeze -> CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW -> CONTROL decision. No role is absorbed by another. A future disposition is excluded from these five DOCUMENTATION outputs. This file does not itself grant another role access to historical verdicts or every path named in a hash inventory.

## Exact pins and DOCUMENTATION allowlist

Prefixes are exact abbreviations, never recursive discovery grants:

- `P = C:/Users/SSAFY/Documents/ai-development-tradition`
- `C1 = P/s0-lab/audit-remediation/a05-profile-composition-v0.1`
- `C2 = P/s0-lab/audit-remediation/a05-profile-composition-v0.2`
- `C3 = P/s0-lab/audit-remediation/a05-profile-composition-v0.3`

Authenticated branch: `codex/windows-build-toolchain-environment-v0.1`; HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. `P/AGENTS.md` was authenticated at `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e` and read completely before task action.

The first ten entries are exact filenames under `C3/implementation/s0_public_runtime_preloader/`; the last three are relative to `C3/`. Nine implementation pins are identical to C2; only `profile.py` changes from C2's `0c0c451a0be41c5593fb3937192da61ae1728534d12e114e0fda9b7a4e297c14`.

| Artifact | v0.3 SHA-256 |
| --- | --- |
| `__init__.py` | `a2e40d7a44f79f3c0f96b790c2249fcb6efe7dba2abf821ea3ee96302f1570c3` |
| `canonical.py` | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` |
| `errors.py` | `20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86` |
| `evidence.py` | `e0f1d9de22eb8b7a727dbef146f808c59d44accbbb96fa3367ee2d0dfdbdd964` |
| `integration.py` | `7d40c5091c43354287fade09f8e11d2ca6a830492d390385d8b13cee361a3dfd` |
| `preloader.py` | `718ba925b7f31bec04ac5d90efe6e6fb4dd7c098a9afdb61d58ffa572ebb38ee` |
| `profile.py` | `efae38b6a99763c0dca61efe2813c11672cf784a28ea1f0747937f80e260501a` |
| `schema.py` | `97b00ab0bb9417b63c5871332751e8c14dea80423414810e99aa2b443f9d6317` |
| `semantic.py` | `1bea3a04282c7d5b6f930ed51b95dbcea87f14f417b04bdee4fb4fbe93c0037d` |
| `source_audit.py` | `50399a565232136736e041ea028b76ed8767d18327553ecf2ec6ec5b0bfe2d36` |
| `tests/test_profile_composition.py` | `b43f60b24999571d8654e3d1de337fc58ec47cf23b00b3483cbb77218f111631` |
| `verification/test-results.json` | `8bce9f03218f3070ab456704d183a8f9b2f7ce10591031735598825394ee414b` |
| `verification/test-stdout.txt` | `a1f0500882178e9750d5a9d174abdb391b315f1875ebae9eeb0722443a56166f` |

Additional content inputs admitted to this DOCUMENTATION role only:

| Exact path | SHA-256 / use |
| --- | --- |
| `C2/CONTROL-DISPOSITION.md` | `4f0b974351baae72118e592d9319d4aefb01e90ff9b0da65bbf35d65b9d362b9`; historical status and exact C2 module pins |
| `C1/SCOPE-AND-CHECKLIST.md` | `113cddf9b5acb76281f8d1a34fffa0be5f5ec0f978f898adbb0486a0f8323d63`; inherited bounded contract, not a current verdict |
| `C1/candidate-files.sha256` | `b2505ce58732de16185f434f9e4ece1c8c2345aba80bc165f3a2df43cc217802`; inventory/preservation metadata only |
| `P/s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`; canonical DOCUMENTATION checks only |

The authenticated v0.3 TEST JSON releases its 60 `pre_input_sha256` paths to DOCUMENTATION for **hash-only preservation**, not content. The exact union is C1's 17 manifest entries, that manifest itself and its three named diagnostic artifacts; ten C2 modules and its three TEST artifacts; ten C3 modules; ten original recovered modules; AGENTS; Python executable identity; historical P4; v0.5 schema/interface map; and v0.4 schema. Each path and expected digest must match the supplied frozen inventory; any unexpected path or mismatch blocks the affected action. C2 disposition and C1 scope do not admit the content of their other links. Python executable identity is `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe`, SHA-256 `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`, with no DOCUMENTATION execution permission.

DOCUMENTATION may read its own outputs after writing. It uses `apply_patch` for the five exact outputs and the canonical validator with `-SelfTest`, followed by `-Path` for each Markdown, checking each exit immediately. Both sidecars contain lowercase SHA-256, two spaces, Markdown basename and LF. The candidate manifest has exactly 17 ASCII-sorted repository-relative entries: ten CODE, three TEST, and four Markdown/sidecar files. It excludes itself and any later disposition. No broad search, review/history/log/index/conversation retrieval, F0 content, native/provider/network action, installation/deletion, or Git mutation is admitted.

## Earlier pre-CODE adversarial freeze

An attacker may supply arbitrary bytes, maps and digest strings and mutate caller maps before or after snapshot construction. Expected hashes supplied as candidate data are not trusted authority. Maintenance-frozen pins are trusted for this bounded task; hostile concurrent interpreter/global/OS control is **UNVERIFIED**. Every unverified prerequisite blocks a stronger dependent claim. These rows cover the candidate's bounded surface and do not claim every possible attack is covered.

| Row / surface | CODE defense owner and action | TEST case and expected fail-closed result | DOCUMENTATION claim / required nonclaim | INDEPENDENT REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| 1. Explicit constructor fields | CODE uses explicit pairs for six raw fields, two current maps and six other maps, preserving order, exact types, errors and snapshots. | Malformed values for each field, order, snapshots and absence of `getattr`; inconsistent material rejects or preserves the copied state. | Constructor unit result only; hostile concurrent getter behavior is unverified. | No omitted check or field; tested ordering and snapshot behavior preserved. |
| 2. Historical and authority prerequisites | CODE preserves historical-first validation, four predecessor pins and design/schema/map/native gates. | Real negative gates and labelled order spies; failed prerequisites stop composition. | No full historical/native positive pass. | Required gates, order and pins remain in force. |
| 3. Complete bounded data flow | CODE preserves historical P4 -> current manifest/files -> six-row package -> effective bytes/hash/snapshot -> preloader -> evidence/admission. | Retain the prior 47 cases; mixed/missing/extra/tampered inputs fail and contrasting historical/current consumers use intended material. | Bounded Python flow only; full integration is unverified. | Trace each consumer to its intended source. |
| 4. Mutability, mintability and rebinding | CODE preserves immutable copies and raw/object/digest bindings, with no execution capability. | Before/after mutation and inconsistent construction reject or leave a stable snapshot. | Caller-mintable coherent data is not authority; hostile concurrency is unverified. | No silent rebinding or authority promotion. |
| 5. Verified versus consumed bytes | CODE leaves downstream consumer bytes unchanged. | Real downstream consumers with labelled missing-upstream doubles consume the validated snapshot. | Native executed/imported identity and binary-path mapping are unverified. | Same Python snapshot reaches consumers without stronger native claims. |
| 6. Source/import closure and inventory | CODE keeps `source_audit.py` byte-identical to C2; only the profile constructor method changes. | Actual ten-file checker pass without doubles; missing/extra/nonbyte/import-alias/dynamic injections reject; nine other modules and bytes outside the method are preserved. | Bounded AST result, not complete interpreter/stdlib/native closure. | No checker-policy relaxation or hidden source delta. |
| 7. Windows paths and concurrent replacement | CODE adds no OS feature or lifecycle change. | Virtual traversal/dot/case-alias/resource rejects and ordinary output non-reparse observations only. | ACLs, volume/root identity, symlinks/junctions/reparse, rename/replacement, retained identities/handles, repository exclusion and TOCTOU through writes remain unverified. | No stronger OS, output-root or filesystem-concurrency guarantee. |
| 8. External artifacts | CODE adds no download or provenance change. | No network/process/native execution; digest tamper rejects within admitted material. | External URL, redirects, digest, size and provenance verification are unverified. | No inferred authenticity from local digest consistency. |
| 9. Evidence producer, outputs and failure | CODE remains source-only. | Frozen pins before/after, executable/flags, exact outputs and command, error preservation, no secrets/deletion. | Canonical DOC SelfTest/Path and manifest pins only; observations do not prove hostile trace or isolation. | Producer identity, bytes and declared result agree; no trace-proof claim. |
| 10. Bounds, cleanup and close paths | CODE preserves 512 files / 512 MiB limits and existing cleanup/failure paths. | Actual file-count bound, labelled reduced byte-bound test and errors preventing consumption. | No native handle-close or execution-safety claim. | Only the required bounded cases support acceptance. |

These are the earlier freeze's requirements. TEST's 56 passing cases include the actual ten-source check, three isolated reflective-read reintroductions and old-C2 rejection under the unchanged checker, constructor types/order/snapshots, and preservation of the 47 earlier cases with their explicit adaptation. Upstream positive doubles remain disclosed. Canonical document checks do not execute or validate the candidate.

## Preservation and unresolved claims

The 60 frozen TEST inputs match pre/post hashes and were independently hash-authenticated by DOCUMENTATION without reading hash-only content. Historical frozen bytes and original hashes remain attached to their original evidence. Recovery archives remain recovery-only. This manifest is a documentation/source handoff, not a runnable historical package, execution authority, full integration proof or publication permission.

Complete positive historical/P4/runtime/native integration, native path mapping, executed/imported identity, installed import closure, external provenance and Windows race/lifecycle proof remain unverified. S0/E0, F0 content, hidden oracle, real provider execution, operational safety, economic value and model transfer remain closed or unestablished. The baseline remains `central-system-v2.1-s0-preparation`; central-system and Project Brain integration are not established. F03 is not fully closed.

CONTROL plans to give the fresh reviewer pinned C3/C2 source and neutral frozen requirements first, with a primary assessment before TEST counts/results, README or scope. CONTROL then explicitly releases the final packet for evidence/document consistency review. This sequence is planned, not completed or proof of enforced isolation; each phase requires a separately frozen exact allowlist and exposure history. Shared folders, worktrees, logs, indexes and replacement sessions do not prove enforced read isolation. Prior procedural failures are not retroactively cured. The unclassified Git-status blocker remains unchanged; no Git publication or integration approval is supplied.
