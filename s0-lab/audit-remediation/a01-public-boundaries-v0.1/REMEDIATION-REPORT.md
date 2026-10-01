# A01 public boundary helpers v0.1: review packet

## Scope and ownership

Date: 2026-09-16. This is auxiliary tooling/evidence work within the authorized F-01 through F-08 remediation. Its one-sentence purpose is to correct F-02 audit-event flag parsing and F-04 stream-inventory error handling in a separate version, with bounded public regression evidence. No complete assembly, native publication lifecycle, integration, or S0/E0 claim is requested.

| Role | Assignment and ownership |
| --- | --- |
| CONTROL | `/root`: gate, exact input pins, adversarial freeze, handoffs, eventual disposition and any separately approved Git actions |
| CODE IMPLEMENTATION | `/root/audit_a01_code`: nine implementation files; two helper corrections and the approved dependency closure |
| TEST/VERIFICATION | `/root/audit_a01_test`: two tests and two result files; substantive execution |
| DOCUMENTATION | `/root/audit_a01_docs`: this report, README, their sidecars, and artifact manifest; authenticated evidence only |
| INDEPENDENT REVIEW | PENDING: fresh, read-only role assigned by CONTROL after this packet is frozen; no acceptance decision yet |

Sequence: CONTROL freeze -> CODE handoff -> TEST handoff -> DOCUMENTATION handoff -> fresh INDEPENDENT REVIEW -> CONTROL decision. Documentation did not edit implementation/tests, rerun substantive tests, or mutate Git. Its supplied input exposure is the exact packet below and CONTROL's bounded assignment; it is not an independent reviewer. One opaque unclassified status item reported by CONTROL remains a Git-publication blocker. This packet grants no commit, push, F0-content access, hidden-oracle/fixture creation, real provider calls, or system setup authority.

## Identity and exact input boundary

Repository `P` is `C:/Users/SSAFY/Documents/ai-development-tradition`. Candidate `C` is `s0-lab/audit-remediation/a01-public-boundaries-v0.1`. Baseline implementation `B` is `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation`. Paths below are literal paths relative to these roots, not recursive read grants.

| Pinned item | Value |
| --- | --- |
| Branch | `codex/windows-build-toolchain-environment-v0.1` |
| HEAD | `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` |
| HEAD tree | `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` |
| `P/AGENTS.md` SHA-256 | `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065` |
| `P/s0-lab/control/tools/verify-text-artifacts.ps1` SHA-256 | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

HEAD/tree identify the repository baseline; the separate candidate's working-file bytes are pinned by `C/artifact-files.sha256`, not asserted to be contained in that commit. The manifest lists exactly 17 files: nine implementation files, two tests, two evidence files, two Markdown documents, and their two sidecars. It excludes itself to avoid a hash cycle; CONTROL must pin its digest in the review handoff.

The maximum proposed read-only review packet is those exact 17 manifest entries, the manifest itself, the seven baseline files below, `P/AGENTS.md`, and the exact validator above (27 files total). CONTROL's role dispatch remains authoritative. No source string, imported name, link, evidence path, or this report authorizes further repository reads. Historical reports, other candidates, F0 content, and conversation history are outside this packet.

| Exact suffix under `B` | Original SHA-256 |
| --- | --- |
| `s0_public_assembly_candidate/constants.py` | `912a5e706751e43441da894edefca02f333b0c173fd1bf1c6647d75f2f353025` |
| `s0_public_assembly_candidate/errors.py` | `be97286ca93c68dba0611efca3795b896da64513aae3e2b053ab30b97f5f3a06` |
| `s0_public_assembly_candidate/runtime_guard.py` | `be88d4bb151f4fe01a541a6ca7227e940fab53c5eb2d4d9ac8ccfb833675542d` |
| `s0_public_assembly_candidate/storage.py` | `5564994d7ba4e10d18b0ef4ba5c3fca51fe35cce5609933cd04d10eebd1fcd2c` |
| `s0_public_assembly_verifier/errors.py` | `70ca57f1704d41e74ca13a2e5174c657b4f9aa6fd41e435ab7f082a95016e4bb` |
| `s0_public_assembly_verifier/models.py` | `cade60d1a260dd58e6d611a691f2d5907d1992cea5f0a4f702e9476558cc74a8` |
| `s0_public_assembly_verifier/win32.py` | `db25d1c4db74f684a54f400ea1dd5f1478d0075c15d1460ff5baf0bef28f4996` |

Candidate `runtime_guard.py` is `693b8f8283cdf476cdeaa263c3021f2a161cd52da08e7c5a877725dc6586eda4`; candidate `win32.py` is `dd250e352431390885adfb4a95244d96622bc9546bd003f585b1afb579143f68`. The other five listed dependency files match their baseline bytes; the two candidate package initializers are independently pinned by the manifest. `constants.py` was the pre-test input amendment A01-INPUT-1, admitted as byte-identical dependency closure. Its path strings grant no content access. Original hashes remain attached to original files and are not revised to make candidate tests pass.

## CONTROL-supplied pre-CODE requirements

This matrix records the bounded freeze supplied to DOCUMENTATION by CONTROL. It is a requirements record, not a claim that every prerequisite was tested. CODE owns the implementation actions; TEST owns discriminating checks; DOCUMENTATION may claim only authenticated observations; fresh REVIEW owns its closure assessment.

| Surface | CODE action | TEST expected result | Permitted DOC claim / required nonclaim | REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| 1. Inventory, pins, import closure | Keep the exact nine-file candidate and approved baseline inputs; add no shadow import | Missing/extra/shadow or pin mismatch rejects; record loaded paths | Measured pins and imported paths only; trusted CPython, stdlib, native libraries and OS are prerequisites, hostile-runtime closure unverified | Exact packet and loaded-path checks support the narrow claim without silently trusting extra inputs |
| 2. Installed sentinel | Preserve actual sentinel installation and unchanged storage helper | Isolated child reads approved benign bytes through pathlib, `os.open`, and storage; distinguish original behavior | Child observations only; no controller or native-success claim | Tests exercise installed code and discriminate the original `None`-mode defect |
| 3. Audit flags and policy | For mode `None`, require an exact nonnegative third-argument integer; retain valid string/legacy-int and pending-name policy | Missing/None/bool/noninteger/negative flags reject and latch; O_RDONLY reads stay approved; O_WRONLY/O_RDWR/O_CREAT/O_TRUNC/O_APPEND obey write policy | Corrected helper behavior for bounded arguments, with existing approved pending reads retained; no broader file authority | Flag source/type and read/write classification preserve the existing allowlist and denial latch |
| 4. Path lifecycle | Retain containment/reparse checks and local scratch scope | Escapes and a reparse marker reject; no personal/F0 inputs | Existing checks retained; ACLs, volume/root identity, symlink/junction/rename races, retained identities/handles, privileged replacement, repository exclusion and full TOCTOU through evidence writes remain unverified | No helper result is promoted to complete Windows-path or evidence-output security |
| 5. Stream enumeration | Accept only EOF 38 as termination; capture last error before close can clobber it | API doubles distinguish First EOF/other errors, Next EOF/5/others, ADS/multiple entries; rejection is AR-AUTH/0 preflight or AR-RECORD/1 publication | API-double control flow and error classes only; no actual ADS or native-publication success | Failed/incomplete enumeration cannot report success and close clobber does not alter enumeration classification |
| 6. Close/failure lifecycle | Reject failed stream-handle close, including after normal EOF | EOF+close failure and enumeration+close failure reject; valid handle closes once, invalid handle never closes | Cleanup failure may be the surfaced exception with enumeration failure retained as context; other native-handle lifecycles unverified | No tested failure path succeeds and the primary failure context remains available |
| 7. Authority and attackers | Introduce no new caller-mintable/rebindable authority, URL, redirect, download, digest/provenance, or network authority | Bounded local cases only; do not imply hostile introspection or concurrent adversaries were exercised | Same-process introspection, arbitrary field mutation, concurrency/races, OS isolation and real ADS exploitation unverified | Existing same-process authority assumptions remain explicit; no external-artifact claim is invented |
| 8. Evidence flow | Keep helper edits separate from TEST-owned evidence production | Record commands, interpreter, imported paths, pre/post pins, counts/skips and scratch cleanup | Evidence links measured files -> exact imports -> child/API-double observations -> TEST-owned results; runtime and output-root integrity beyond measurements unverified | Report and manifest match authenticated evidence; helper success never becomes system success |
| 9. Resources and stop rules | Limit changes to two helpers and approved closure; no speculative expansion | TEST cannot fix CODE; isolate an unexplained failure with a diagnostic matrix before a second speculative correction | Bounded regression evidence only; cleanup/resource and trusted-environment limits explicit | Stop affected auxiliary work at purpose expansion, architectural redesign, 30 minutes, or two independent reject/correct cycles pending CONTROL/user decision |

## Authenticated observations and reproduction

Evidence producer: TEST/VERIFICATION. DOCUMENTATION authenticated both result files before using their contents, then authenticated all nine candidate and seven baseline implementation hashes against the recorded before/after maps. Branch, HEAD, tree, AGENTS pin, and both test pins matched the supplied handoff. No substantive test was rerun by DOCUMENTATION.

| Evidence file under `C` | SHA-256 |
| --- | --- |
| `tests/test_runtime_guard.py` | `9b6795262f8fa8fb6b1b0a2e98d17e78ee4d199041918acae37ccca20b326bfa` |
| `tests/test_stream_inventory.py` | `4733df59dc05a30c2a8ec2c7e35b9a90d8e6f8f30f5d3be79632a735e64d3496` |
| `verification/test-results.json` | `b10e144c25110ed7880975e62295ac722939e14b1f441e687c6b0b1ac7c32d1e` |
| `verification/test-stdout.txt` | `3f519ec90d3c65326190976611392dc972016c2cdb199776dc80e174738f0235` |

The recorded result is 23 tests and 88 subtests, zero failures/errors/skips, 13 isolated child observations, and 36 stream-double scenarios. These are overlapping measures. The harness records 0.968 seconds; unittest stdout records 0.768 seconds. All nine candidate and seven baseline pre/post pins match; scratch remaining count is zero. Interpreter: 64-bit CPython 3.12.10, `-I -S -B` (isolated, no site initialization, no bytecode writes). This interpreter/stdlib/OS is a trusted prerequisite, not independently authenticated execution closure.

For the three approved read paths, candidate children returned the same 41 bytes with SHA-256 `953161e266aeebae1bfd8ab4740cd854aa4970ede0f227d79617130ff41b3ccf`. Baseline pathlib read succeeded, while baseline `os.open` and unchanged storage read were rejected for an invalid mode. Candidate denied-path cases remained rejected with the violation latch, and the allowed pending-write case retained the same benign bytes. Stream evidence uses actual helper code with API doubles: baseline discrimination exposes unchecked Next error and close failure. Combined enumeration/close failure in the candidate reports close failure with enumeration failure in exception context. No native stream API call was made by these scenarios.

Recorded PowerShell reproduction command, working directory `P`:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a01-public-boundaries-v0.1/tests/test_runtime_guard.py'
```

The runner loads the second test file, authenticates its fixed inputs, bounds children to 15 seconds and Git identity queries to 10 seconds, uses only owned local scratch, and rewrites the two TEST-owned result files. Reproduction therefore belongs to an authorized TEST handoff; a read-only reviewer must not run it and overwrite the frozen evidence. Any authorized rerun must preserve this packet's original hashes and distinguish new measurements and environments.

Text publication checks use the pinned canonical validator through native Windows PowerShell: `-SelfTest`, then separate `-Path` invocations for `C/README.md` and `C/REMEDIATION-REPORT.md`; each native exit code is captured immediately. DOCUMENTATION records final check outcomes and the five output hashes in its handoff so neither report nor manifest hashes itself.

## Limits and disposition

Independent review: **PENDING**. CONTROL acceptance/publication: **PENDING**, with no Git mutation authorized here. No historical finding outside these two helper corrections is closed by this document.

The evidence does not establish complete assembly correctness, controller operation, a full native publication or handle lifecycle, same-process tamper resistance, concurrent attacker resistance, OS isolation, Windows ACL/identity/TOCTOU guarantees, real ADS exploitation resistance, download/provenance security, or evidence-producer security beyond the stated measurements. It does not validate S0/E0 execution/scoring, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer. Those unverified prerequisites block broader claims; they are not automatically new work gates.
