# A06 CONTROL disposition

**CONTROL decision: ACCEPT the bounded complete 20-source development integration only.** Candidate `a06-runtime-source-integration-v0.1` combines the prescribed F01/F03/F08 source corrections without losing either overlapping patch. This decision does not close full F03, establish native/runtime acceptance, or complete the broader audit/maintenance goal.

This document is authored by DOCUMENTATION from CONTROL's decision handoff, the attributed fresh review result, and the authenticated frozen packet. DOCUMENTATION does not supply an independent verdict or rerun candidate tests. The original README's review-PENDING status describes its earlier documentation freeze and remains unchanged as historical evidence.

## Exact decision target

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.

- Candidate root: `s0-lab/audit-remediation/a06-runtime-source-integration-v0.1`.
- Branch: `codex/windows-build-toolchain-environment-v0.1`.
- Base HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`.
- Base tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
- Current root `AGENTS.md` SHA-256: `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`.
- Reviewed `artifact-files.sha256` SHA-256: `396958cf1283abc53cfa8de8248ba45e70ecdce08808b1172d0a263d2475f593`.

The reviewed manifest freezes exactly 30 candidate-relative entries: 20 implementation files, two tests, four verification outputs, two Markdown documents, and their two sidecars. CONTROL re-authenticated the manifest and all 30 entries unchanged after review. DOCUMENTATION re-authenticated the same packet before writing this disposition. The manifest excludes itself and this later disposition pair. Neither the 30 frozen files nor their manifest is modified to reflect the later decision.

| Frozen evidence path relative to candidate root | SHA-256 |
| --- | --- |
| `tests/test_source_corrections.py` | `7b551aeb5a89a59857bab17fc705fa9af35d01644bdd216bf2bddc21dde915da` |
| `tests/test_profile_composition.py` | `991668fc4255a79ec4dce533c9c0f72cea5f959b49918242534ea130aad7a170` |
| `verification/source-corrections-results.json` | `1c68764eda95f810f1012988ff490e8c7bd4e97793b14873fde7883f63fa734a` |
| `verification/source-corrections-stdout.txt` | `1bc44112e0f0e91aab38d8ab18b2d0dc062d821a90fb7c370d08f8fec015b642` |
| `verification/profile-composition-results.json` | `110ad1d29ceb6214ce6ca1c971c0779b53d9d467ee75b3b0a320944380a12f52` |
| `verification/profile-composition-stdout.txt` | `df242fa081388d48915fe8f40d9056d41be2f2f67b98dc496887aaae13383b6a` |
| `README.md` | `c3f371b49b758b701ea663400783188b01bc64cbb3828aa9d8812589067c0039` |
| `README.sha256` | `984718cf5654acf99b9f25a158c578a489ff8c028679fd9127b6253a3f917a8b` |
| `SCOPE-AND-CHECKLIST.md` | `fac63299f03740d0c7a2032118ad2890ef1e462aa69f6c53a048a92a242a529e` |
| `SCOPE-AND-CHECKLIST.sha256` | `b5eb46bb9175f4982c6bd20f0f129974704067fd76d6aafead812e5e96ef79f1` |

The original recovery, A02 and A05 source manifests and the five exact replacement source hashes remain recorded in the frozen README and scope/checklist. Their presence here does not expand any role's content allowlist.

## Role sequence and attributed independent review

| Role | Session | Contribution |
| --- | --- | --- |
| CONTROL | `/root` | Earlier pre-CODE freeze and handoffs; authentication; this bounded acceptance decision |
| CODE IMPLEMENTATION | `/root/audit_a06_code` | Exact 20-file source union |
| TEST/VERIFICATION | `/root/audit_a06_test` | Bounded tests and evidence, including preserved initial harness failure |
| DOCUMENTATION | `/root/audit_a06_docs` | Frozen documentation/manifest, then this separately authorized disposition pair |
| INDEPENDENT REVIEW | `/root/audit_a06_review` | Fresh read-only `gpt-5.6-sol`, ultra reasoning, `fork_turns: none`; source-first primary assessment followed by evidence assessment |

CONTROL reports that the fresh reviewer completed its primary source assessment before phase-two evidence release, then returned final **PASS with zero findings at every severity**. The review upheld the bounded source-integration claim and its stated limitations. This is the reviewer's reported verdict, recorded by DOCUMENTATION; it is not a new DOCUMENTATION review.

The reviewer first received the exact allowed source inputs and pinned requirements. The subsequent release comprised the 30-file packet, two prior test sources, the canonical validator, and 113 exact hash-only prerequisite paths. The two prior test sources were `s0-lab/audit-remediation/a02-native-source-corrections-v0.1/tests/test_source_corrections.py` (SHA-256 `8b4987b3853a91076edee3b595ab8cf8171f0ec72e48b82b090b1f2af26f9a84`) and `s0-lab/audit-remediation/a05-profile-composition-v0.3/tests/test_profile_composition.py` (SHA-256 `b43f60b24999571d8654e3d1de337fc58ec47cf23b00b3483cbb77218f111631`). Hash-only access did not release the contents of other prior reports or verdicts.

CONTROL's review handoff records no prior verdict/report-content exposure, F0 access, network use, candidate/test/native execution, edits, or Git mutation by the reviewer. The final review was a procedural source-first review with later evidence exposure. It was not an outcome-blind final review, and the shared filesystem does not establish enforced read isolation.

## Accepted source and bounded test evidence

The attributed review found the source union to be exactly 15 original files, the A02 native-preloader and canonical-helper files, the A05 profile and preloader Python files, and the merged source-audit module carrying the exact MoveFile delta. The complete original initializer and all 28 exports were preserved.

- F01: the two physical lists contain the same seven entries, with P5 once; the native patch is the exact prescribed list-entry correction.
- F08: invalid raw path segments are rejected before normalization, including through F03 snapshots using the real corrected helper.
- F03: historical-first validation, four predecessor pins, current six-row package, snapshots, effective-profile bindings, current consumers and historical P4 identity remain preserved.
- The real merged checker retains the bounded import/getattr, binding/rebinding and MoveFile checks; the integration does not widen the policy or substitute a positive fake checker.

The authenticated source JSON reports 24 tests and 205 subtests with zero failures, errors or skips, and 75 equal pre/post pins. The profile JSON reports 59 tests, 59 PASS records, zero failures/errors and 78 pre/post pins. It has no standalone skip-count or process-exit field; TEST's handoff supplies zero skips and final exit 0 for both suites. The documentation preserves that distinction.

There are 19 current real-checker observations: one PASS for the exact merged ten Python sources and 18 REJECT outcomes, including all three reintroduced `getattr` sites. A separately preserved historical rejection record is not counted as a current checker execution. The combined hash-only prerequisite inventory contains 113 distinct paths, rehashed unchanged. These identities do not establish hostile concurrent-filesystem integrity.

TEST exercised the actual 512-file count bound. It reduced the byte bound to 3 for the bounded unit case; it did not test a 512 MiB payload. Production bound constants remain unchanged. The canonical validator SelfTest and both earlier Markdown/sidecar checks passed with native exits 0.

The first source-suite attempt exited 1 after candidate checks, during post-run Git authentication before result output. A TEST audit hook expected an argv list but Windows supplied command-line strings. The diagnostic isolated the three exact Git identity queries; TEST made one test-only correction and reran. No CODE change resulted. The final source JSON preserves the initial test hash, phase, exit, cause and diagnostic; the original traceback remains in the TEST tool transcript. Final acceptance does not erase or relabel that history as a candidate or native execution result.

## Unverified claims and remaining boundaries

Acceptance is limited to the complete source development input and the bounded evidence above. Positive historical, design, schema and native prerequisites still use the disclosed test doubles; P1-P3 unit pins are not real positive historical acceptance. This decision does not close full F03 or infer the native `ArtifactMaterial.virtual_path` to runtime-manifest mapping.

Native compilation, materialization, current binary identity, runtime-authority integration, loaded/executed native-byte closure and complete positive historical acceptance remain **unverified**. Copied build and authority files retain their historical pins. No old expected hash is updated to manufacture current acceptance.

Windows ACLs, volume/root identity, symlink/junction/reparse behavior, rename/replacement, retained handles, repository exclusion, hostile concurrency and TOCTOU through output/evidence writes remain **unverified**. Full interpreter/standard-library/native-library closure, hostile introspection/global compromise and secure evidence production also remain **unverified**. The bounded tests rely on the developer host and evidence producer; they do not prove that environment secure.

There is no S0/E0 fixture, execution or scoring acceptance; no hidden-oracle or F0-content authorization; no real model/provider call; and no claim about Project Brain integration, central-system implementation, operational safety, economic value, model transfer or global audit completion. External artifact URL, redirects, digest, size and provenance are not validated by this source-only decision. A07 environment work remains a separate candidate.

These limitations constrain the decision; they are not automatic recommendations for another technical gate. The broader audit/maintenance objective remains active. Existing Git classification and approval requirements remain unchanged: this disposition authorizes no staging, commit, push, PR, merge, publication or new content access.

## Disposition preservation

This later record is stored only as `CONTROL-DISPOSITION.md` and `CONTROL-DISPOSITION.sha256`. Its sidecar uses lowercase SHA-256, two spaces, the Markdown basename and LF. Both remain outside the unchanged 30-entry reviewed manifest.

The canonical validator is `s0-lab/control/tools/verify-text-artifacts.ps1`, SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`. DOCUMENTATION authenticated it and reran native `powershell.exe -NoProfile -ExecutionPolicy Bypass -File` with `-SelfTest`, obtaining PASS and immediately captured exit 0. After creating this pair, DOCUMENTATION applies the same canonical tool with `-Path` to this Markdown file and reports its separately labeled results, immediate exit and both final pins to CONTROL. No substantive candidate verification is performed by DOCUMENTATION.
