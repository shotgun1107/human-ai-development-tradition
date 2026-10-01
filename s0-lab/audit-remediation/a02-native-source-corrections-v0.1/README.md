# a02-native-source-corrections-v0.1 review packet

Status at document freeze, 2026-09-16: TEST/VERIFICATION reported PASS; fresh INDEPENDENT REVIEW and CONTROL acceptance are pending. This is a frozen packet, not a living status page. Record later disposition separately without rewriting these bytes.

This auxiliary remediation corrects the F-01 physical source inventory and bounded F-08 Python helpers. It supplies a reviewable source delta and public regression evidence. It is not a complete runnable native candidate, integration, or native build. The project remains at `central-system-v2.1-s0-preparation`.

## Identity, ownership, and allowed inputs

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition` (`P`). Candidate directory (`C`): `s0-lab/audit-remediation/a02-native-source-corrections-v0.1`. Source directory (`S`): `docs/maintenance/audit-2026-09-09/source-snapshot-2026-09-16`. Paths below are relative to these explicit roots; no recursive discovery is authorized.

- Branch: `codex/windows-build-toolchain-environment-v0.1`.
- Pinned HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
- CONTROL: root session, freeze/allowlists/decision; CODE IMPLEMENTATION: `audit_a02_code`, implementation only; TEST/VERIFICATION: `audit_a02_test_resumed`, harness and execution only; DOCUMENTATION: `audit_a02_docs`, this packet/sidecar/manifest only. A separate fresh read-only reviewer is required.
- CONTROL reports that the earlier TEST role was interrupted before writes; a new TEST role resumed under the same freeze. DOCUMENTATION did not inspect that earlier session or its history.
- DOCUMENTATION authenticated current branch/HEAD/tree, root policy, the three TEST artifacts, and each source/candidate pin below. It used authenticated TEST evidence and the CONTROL handoff; it performed no substantive test rerun or independent approval. Its exposure is confined to that handoff and the exact authorized public inputs.
- Role sequence: CONTROL freeze -> CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW -> CONTROL disposition. No role may expand its allowlist; the review dispatch must explicitly release the packet and primary inputs below.

| Input relative to named root | Bytes | SHA-256 |
| --- | ---: | --- |
| `P/AGENTS.md` | 30777 | `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065` |
| `S/s0_neutral_preloader_v0_5.cpp` | 81162 | `6230ef69d5b4b175968f7576b43aeb5ae15fa3646c59778f84b5c3877c0ef9ec` |
| `S/canonical.py` | 5835 | `f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4` |
| `S/source_audit.py` | 24041 | `c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99` |
| `C/implementation/native/s0_neutral_preloader_v0_5.cpp` | 81191 | `88e2a05bbb643c18247844b9aa38b0b327215730f8cf0fd44925e077df5c6e53` |
| `C/implementation/s0_public_runtime_preloader/canonical.py` | 5980 | `14b30ef5688f3340b78215632fba4f0f4360b2d394ca56730979ac5e6f5c1ff0` |
| `C/implementation/s0_public_runtime_preloader/source_audit.py` | 24115 | `7b65cfec819544a258ecb0cb9f25346b0c9c6606c52f12448d0a8d6954f57e6c` |
| `C/implementation/s0_public_runtime_preloader/errors.py` | 643 | `20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86` |
| `C/implementation/s0_public_runtime_preloader/__init__.py` | 64 | `57adf310b3589dadfc4c69369def09c3185d99983e7a42a5772c431c60bb250a` |
| `C/tests/test_source_corrections.py` | See file | `8b4987b3853a91076edee3b595ab8cf8171f0ec72e48b82b090b1f2af26f9a84` |
| `C/verification/test-results.json` | See file | `f92bed1e82dc4b1ad7ad5b56cdbdffcef62a398aab05602366822fe881d01f18` |
| `C/verification/test-stdout.txt` | See file | `adb717f8c63a92d4b8b24b461b89f5678e931a4cb7582424041f9093f80f85e7` |

The three `S` files are unchanged recovery inputs; this packet does not promote them into validated native execution material. CONTROL supplied the public `errors.py` text from `Temp/rpnp05-impl-20260908/s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/implementation/s0_public_runtime_preloader/errors.py`, public command record `exec-6e836a00-4096-41ee-a9a5-97af659228b2`; the restored file matches the supplied original size/hash. This is attributed provenance, not a DOCUMENTATION history read. The candidate initializer contains only a docstring and does not recover the full package exports.

## Correction and measured evidence

CODE added only `runtime-profile-v0.5.json` to `ReverifyPackage`'s physical package list. Both initial and terminal source lists now contain the same seven entries, with P5 exactly once. Static checks confirm list comparison and directory-check call sites. The baseline had seven initial entries and six terminal entries. In-memory missing, duplicate, and extra list mutations were rejected by the test's inventory predicate; this is not a measurement of native runtime rejection.

`canonical.py` now rejects raw empty, dot, and dot-dot segments before `PurePosixPath` normalization. Direct path, manifest parsing, and material verification tests discriminate the four formerly accepted dot aliases. Normal relative paths remain accepted; traversal, absolute/drive paths, backslashes, colons, NUL, length, and slash aliases are rejected in the tested cases. These are lexical helper claims, not Windows filesystem containment claims.

`source_audit.py` adds the `MoveFile` name family to the bounded unclassified-call diagnostic and narrows its comment accordingly. Tested family variants reject for each known role, while the baseline accepted `MoveFileW`; existing `GetTempPathW` rejection remains. Known role inventories pass, comments/strings are not treated as calls, and unknown-role/inventory mismatches reject. This is not a complete Windows API classifier or native capability enforcement.

Authenticated TEST evidence reports 21 tests and 116 subtests, zero failures/errors/skips, 0.25 seconds total (unittest body 0.023 seconds). Pre/post identity, input sizes and hashes were equal. Candidate implementation inventory was exactly five files, zero missing/extra/shadow entries; no scratch was used or found. Eight explicit module loads used the authenticated byte buffers, with module paths/origins recorded. Minimal-diff assertions constrain the C++ change to one entry and the Python changes to the described raw-segment guard, family, and comment.

The interpreter was CPython 3.12.10, `C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe`, SHA-256 `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`, flags `-I -S -B`. The interpreter, standard library, OS, Git identity tool, and output root are trusted prerequisites, not an authenticated hostile import/native closure.

Reproduction command, from `P`, for a separately authorized TEST role only:

```powershell
& "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe" -I -S -B "C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a02-native-source-corrections-v0.1/tests/test_source_corrections.py"
```

The runner rewrites `verification/test-results.json` and `verification/test-stdout.txt`, including elapsed time; a read-only reviewer MUST NOT run it against this frozen packet. Review the source and recorded evidence. Any authorized rerun must preserve this evidence and receive its own exact output authorization.

## CONTROL-supplied pre-CODE bounded checklist

The following records the pre-CODE freeze supplied by CONTROL. It is a bounded model of local source bytes and benign in-memory strings, not coverage of every attack. Each column assigns the named role its responsibility; unknown prerequisites cannot support broader authority.

| Row / surface | CODE owner action | TEST owner check / required rejection | DOCUMENTATION allowed claim / required nonclaim | Fresh REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| A: inputs, import and shadow inventory | Preserve exact source-three/candidate-five boundaries and pins. | Authenticate inventory/pins and executed buffers; missing/shadow/pin mismatch aborts. | Exact observed inventory/imports only; trusted Python/stdlib/OS is not secure closure. | Primary pins, import records and scope agree; no closure promotion. |
| B: F-01 full source flow | Add only missing P5 entry in terminal list. | Initial/terminal exact same seven, P5 once, both consumption sites; baseline six vs seven and in-memory missing/extra/duplicate lists reject. | Static list correction only; native rejection/execution unverified. | One-entry delta and static/diagnostic limits supported. |
| C: F-08 path flow | Reject raw empty/dot/dot-dot before normalization. | Normal cases pass; aliases/traversal/absolute/drive/backslash/colon/NUL/length fail; propagate through both manifest helpers. | Lexical validation only; OS path containment unverified. | Guard order and direct/manifest discriminators support the narrow claim. |
| D: API diagnostic | Add MoveFile family and bound comment. | Known inventories pass; MoveFile variants/GetTempPathW reject; strings/comments ignored; role/inventory mismatch rejects; baseline discriminator. | Listed family diagnostic only; all-API proof, PE/object and native controls unverified. | Changed family and unchanged controls match primary evidence. |
| E: authority and external inputs | Add no authority mint/rebind, URL, redirect, download, network or native action. | Bound inputs to local source and in-memory benign strings; no broader authority test. | No new authority asserted; hostile introspection, mutable fields, rebinding and concurrency unverified. | No external-artifact provenance or authority claim beyond tested bytes. |
| F: Windows path lifecycle | Leave ACLs, volume/root, symlink/junction/reparse, rename/replacement, retained handles, repository exclusion and TOCTOU defenses unchanged. | No Windows lifecycle execution in this gate; all such properties remain unverified through output/evidence writes. | No Windows containment, race safety or operational safety claim. | No unchanged/unverified prerequisite promoted to verified safety. |
| G: execution/evidence/close flow | Preserve minimal input deltas; no evidence-producing code expansion. | Exact command/interpreter/imports, pre/post pins, diffs, hashes and no scratch; authentication mismatch aborts. | Recorded reproducibility and no cleanup required; trusted output root, failure/close safety and secure producer unverified. | Evidence matches pins and command; read-only review does not overwrite it. |
| H: bounds and correction discipline | No speculative second correction without TEST diagnosis; no architecture expansion. | Isolate any unexplained failure with a discriminating matrix before another correction; no TEST code fixes. | Preserve bounded outcomes; two reject/correct cycles or 30-minute auxiliary limit require CONTROL/user decision. | Review only required narrow claims; do not expand the threat model or hide a limit. |

## Freeze and remaining boundaries

`artifact-files.sha256` contains exactly ten candidate-relative entries: five implementation files, the three TEST artifacts, this README, and `README.sha256`. It excludes itself. Root policy, the three recovery source inputs, interpreter, and validator are separately pinned prerequisites, not candidate manifest entries. CONTROL receives the manifest's own hash after creation.

Canonical documentation validator: `P/s0-lab/control/tools/verify-text-artifacts.ps1`, SHA-256 `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`. DOCUMENTATION runs native Windows PowerShell `-NoProfile -ExecutionPolicy Bypass -File` with `-SelfTest`, then `-Path C/README.md`, captures each exit immediately, and reports the results to CONTROL without modifying this frozen packet afterward.

No native compilation/calls, object or PE execution, integration, S0/E0 fixture creation/execution/scoring, F0-content access, hidden oracle, provider/model calls, network, or paid service was authorized here. No claim establishes the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer. Worktree/session separation alone does not establish enforced read isolation.

CONTROL reports one opaque unclassified status item blocking Git mutation/publication; this role did not enumerate it or mutate Git. Passing source tests does not remove that blocker. Fresh review and CONTROL disposition remain pending at this document freeze; acceptance must be limited to the specified source/helper corrections.
