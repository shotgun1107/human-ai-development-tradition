# A05 v0.1 CONTROL disposition

Date: 2026-09-17. Candidate: `a05-profile-composition-v0.1`.

CONTROL (`/root`) decision: **REJECT-CURRENT-FREEZE-SOURCE-CLOSURE-INCONSISTENCY**. One P1 source-closure inconsistency prevents acceptance; the supplied fresh review reports no P0, P2, or P3 finding. This DOCUMENTATION record transcribes CONTROL's decision and attributed review/TEST evidence; it is not an independent judgment.

## Fixed candidate and review finding

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`; branch: `codex/windows-build-toolchain-environment-v0.1`; HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. Root `AGENTS.md` SHA-256: `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.

The authenticated [original 17-file manifest](candidate-files.sha256) remains fixed at SHA-256 `b2505ce58732de16185f434f9e4ece1c8c2345aba80bc165f3a2df43cc217802`. All 17 exact files matched before this record was written. This disposition and its sidecar are later, separately pinned artifacts excluded from that manifest, as are the separate diagnostic addenda below. The [README](README.md), [scope/checklist](SCOPE-AND-CHECKLIST.md), original results, and their pending-at-freeze wording remain unchanged.

Fresh INDEPENDENT REVIEW `/root/audit_a05_review_resumed` (`gpt-5.6-sol`, ultra) reported:

- [profile.py](implementation/s0_public_runtime_preloader/profile.py):10 imports `dataclasses.replace`, but [source_audit.py](implementation/s0_public_runtime_preloader/source_audit.py):76 admits only `dataclass` from that module.
- [preloader.py](implementation/s0_public_runtime_preloader/preloader.py):17 imports `ValidatedSuccessorProfileCandidate`, which `source_audit.py`:117 omits. Both imports are rejected by its checks at lines 283-295.
- [The original test](tests/test_profile_composition.py):245-248 checks `source_audit.py` byte identity, not closure of the real candidate source. The reviewer recommended synchronizing the closed lists, removing the obsolete `copy` allowance, and adding an exact-candidate regression.

The review otherwise found the bounded historical/current data flow, canonical effective identity, and original P4 evidence/admission separation consistent with the frozen scope. It found no fabricated evidence or full-native overclaim in the README/results. Those observations do not accept the candidate or prove unavailable prerequisites.

## Separate TEST diagnostic

After the source finding, TEST/VERIFICATION `/root/audit_a05_test_resumed` ran the real candidate `inspect_source_structure` on four in-memory dictionaries of exact source bytes:

| Dictionary | Recorded result |
| --- | --- |
| All original source | PASS |
| All candidate source | REJECT |
| Originals with candidate `profile.py` | REJECT |
| Originals with candidate `preloader.py` | REJECT |

Each rejection is `RuntimeProfileError: candidate from-import is outside positive closure at #`. AST differences independently isolate missing `dataclasses.replace` and `.profile.ValidatedSuccessorProfileCandidate`; new `canonical_json_bytes` and `safe_virtual_path` imports are already admitted. The old profile `copy` import was removed.

The command recorded in [diagnostic results](diagnostics/source-closure-results.json), run by TEST and not rerun by DOCUMENTATION, is:

```powershell
& "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe" -I -S -B -X utf8 "C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a05-profile-composition-v0.1/diagnostics/test_source_closure.py"
```

| Separately authenticated TEST artifact | SHA-256 |
| --- | --- |
| [Diagnostic script](diagnostics/test_source_closure.py) | `97cc7c13dcbce10a2d6785cd1e00f7f3c46255c07397be282ae0d6ce17d59279` |
| [Diagnostic results](diagnostics/source-closure-results.json) | `0788ea1856080b729f8e6a6d3fa1c99cc95d216dadd9b825a9e0d25af98039c3` |
| [Diagnostic stdout](diagnostics/source-closure-stdout.txt) | `94fdf5acb546fbc2d86c77e6f391dfef6092331db61e1f2329488becb57e5573` |

TEST records all 30 pinned inputs unchanged pre/post, with the original 17 files and manifest checked again after output. Only candidate `errors.py` and `source_audit.py` executed; original source was data only. No native/P4 validation, S0/E0 execution, or provider call occurred. DOCUMENTATION authenticated the three addenda and the original manifest/files; it did not read additional inputs merely because the JSON names them.

This diagnostic confirms rejection of the current freeze. The [original 36-test result](verification/test-results.json) and [stdout](verification/test-stdout.txt) remain valid for their stated cases and limitations, but insufficient for acceptance. They are neither erased nor retroactively broadened. No corrected-version pass exists at this decision.

## Role continuity and remaining boundaries

Original CODE `/root/audit_a05_code`, TEST `/root/audit_a05_test`, and DOCUMENTATION `/root/audit_a05_docs` completed their handoffs. Initial reviewer `/root/audit_a05_review` became unavailable before CONTROL received a primary assessment or verdict; none was inferred. CONTROL reauthenticated the unchanged branch, HEAD, tree, manifest, and 17 files before assigning the fresh replacement review with only the frozen packet and a source-first sequence. No prior review conclusion or maintenance conversation was supplied. The reviewer assessed primary source, checklist, and test source before opening README/results/stdout, executed no candidate/tests, and wrote no artifacts.

The diagnostic role remained TEST only. `/root/audit_a05_disposition_docs` is the replacement DOCUMENTATION role for these two decision files, not a reviewer. Separate sessions or worktrees do not prove enforced read isolation.

The v0.1 source and original frozen inputs/results remain preserved. A separately versioned minimal v0.2 may correct import closure through its own CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW sequence; this record asserts no v0.2 change or pass and authorizes no integration, execution, or Git publication.

Complete historical material, native current-path mapping, executed/imported byte identity, full interpreter/stdlib/native closure, Windows path lifecycle and TOCTOU, external provenance, and full integration remain unverified. F0 access, hidden-oracle creation, S0/E0 and real provider execution remain closed. The baseline remains `central-system-v2.1-s0-preparation`; this work establishes no central-system/Project Brain integration, operational safety, economic value, or model transfer. The prior opaque unclassified-status blocker remains unresolved and unwaived; no new Git approval is granted.
