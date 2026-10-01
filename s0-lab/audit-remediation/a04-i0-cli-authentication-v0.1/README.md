# a04-i0-cli-authentication-v0.1

Status at packet freeze: **PENDING independent review and CONTROL disposition**. Any later disposition belongs in a separate record; this packet does not approve itself.

This is bounded auxiliary audit-remediation work: require the existing frozen public manifest authentication before the `integrity`, `schema-check`, and `verify` CLI handlers. The correction reuses the existing authenticator and pin. It introduces no verifier architecture, dependency installation, or experimental gate.

## Identity and roles

- Date: 2026-09-16; baseline: `central-system-v2.1-s0-preparation`.
- Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.
- Branch: `codex/windows-build-toolchain-environment-v0.1`.
- HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.
- CONTROL: `/root`; CODE IMPLEMENTATION: `/root/audit_a04_cli_code`; TEST/VERIFICATION: `/root/audit_a04_cli_test`.
- DOCUMENTATION: fresh replacement `/root/audit_a04_cli_docs_replacement`; fresh read-only INDEPENDENT REVIEW remains to be assigned by CONTROL.
- Sequence: CONTROL freeze -> CODE -> TEST -> DOCUMENTATION -> fresh INDEPENDENT REVIEW -> CONTROL decision. No role is absorbed by DOCUMENTATION.
- CONTROL supplied the pre-CODE matrix below. This packet records that supplied freeze; it does not retroactively create it or broaden the allowlist.

## Frozen inputs and output scope

| Input | SHA-256 / restriction |
| --- | --- |
| Root `AGENTS.md` | `4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065` |
| `s0-lab/i0/verification/implementation-files.sha256` | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` |
| Original implementation | Only its eleven `implementation/s0_i0/*.py` rows named below and `requirements.txt`; all twelve original pins preserved |
| Candidate implementation | Same twelve relative paths/pins, except `implementation/s0_i0/cli.py`: `819edaf785558b620aa7b79036560d4fb895d7ce513a5cc4173fad04df8e43f9` |
| `s0-lab/public-practice/v0.1/bundle-files.sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637`; 90 rows are metadata only, not permission to read their targets |
| `s0-lab/public-practice/v0.1/examples/answer.json` | `e66d631210fae9519cd94e618061674f68ac869b04fc38416c8ee50a3f85b43f` |
| `tests/test_cli_authentication.py` | `7c4025d162735e15a1537ffe94e8dc1feadbee50f550d4f60f6b69a6f29766b6` |
| `verification/test-results.json` | `25a8a87f553a8a54d1d2967c0cea3a152b56c83ee9c1383805d3cf1007b92bc9` |
| `verification/test-stdout.txt` | `36de0254b133f12c722ffa062a95de332766bd12bdbaec004712f5a0b5f79c09` |
| `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |

The eleven exact module basenames are `__init__.py`, `answer_validation.py`, `authentication.py`, `cli.py`, `error_reporting.py`, `integrity.py`, `json_validation.py`, `paths.py`, `schema_suite.py`, `transform.py`, and `verification.py`. Other rows in the original implementation manifest confer no content access. Candidate-local paths in this packet are relative to `s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1`.

DOCUMENTATION writes only `README.md`, `README.sha256`, and `artifact-files.sha256`. The latter pins exactly seventeen artifacts: twelve candidate implementation files, three TEST files, this README, and its sidecar; it excludes itself. Its digest is supplied in the handoff. Referenced paths are not an expanded role allowlist.

## Change and observed evidence

Only `cli.py` differs from the twelve original source files. It imports existing `_authenticate_bundle_manifest` and invokes it inside the existing `try`, after workspace resolution and before the three named handlers. Existing full-content check wiring, transform and answer paths, output handling, and error redaction are unchanged. Original source bytes and frozen expected pins were not rewritten.

Authenticated TEST evidence records 29 tests, 26 observations, zero failures/errors/skips, unchanged pre/post Git identity and all 28 input pins, and removed scratch. Original and candidate implementation inventories were exact during that run. DOCUMENTATION authenticated the supplied evidence and all 24 original/candidate source pins; it did not rerun substantive tests.

- The real CLI entry, manifest authenticator, SHA-256, and manifest parser were exercised. The original manifest reaches a raising handler spy after authentication; this is dispatch evidence, not a successful full command.
- Altered manifests, changed content with a matching replacement manifest, malformed manifests, missing manifests, and injected unreadability fail before handler dispatch, with nonzero exit and redacted JSON errors. Baseline CLI spies distinguish the prior absence of the common guard.
- A content-only mutation passes the manifest guard as designed, then a narrow example-digest handler double rejects it. Full-content checking remains statically wired, but complete 90-file verification was not run.
- Under `-I -S`, real `jsonschema` was unavailable. An explicit import-only double raises if validation is attempted; handler doubles prevent any claim of real schema validation. The permission case injects `Path.read_bytes` failure and is not an OS ACL test.
- Transform/answer spies observe their existing entry and no new common guard. Real answer, oracle, schema, transform, and complete verification behavior remain unverified.

TEST reproduction command, from the repository root (for an authorized TEST rerun only):

```powershell
& "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe" -I -S -B "C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/tests/test_cli_authentication.py"
```

The runner writes the frozen TEST evidence files and creates/removes bounded scratch; read-only reviewers must not run it. Recorded runtime: CPython 3.12.10, MSC v.1943, 64 bit AMD64. Full CLI/dependency integration remains unverified.

## Supplied bounded pre-CODE checklist

| Row / surface | CODE owner action | TEST expectation | DOCUMENTATION limit | REVIEW closure criterion |
| --- | --- | --- | --- | --- |
| A: source/inventory/imports | Preserve exact twelve source paths per tree and original pins | Fail missing/shadow inventory; authenticate pins and loaded candidate paths | OS, Python, standard library, dependencies trusted; no secure closure claim | Exact inventory/pins and narrow import evidence support only this candidate |
| B: manifest authority / dispatch | Existing fixed-pin check before exactly three handlers; no expected-pin rewrite | Original dispatch; changed/matching/malformed/missing/unreadable reject before handler; nonzero redacted JSON; baseline distinguishes absence | Fixed-manifest guard claim only | Pin check is reached first inside existing error path; cases discriminate old/new flow |
| C: content flow | Retain existing content-integrity wiring | Real guard plus explicit narrow content double and static wiring check | Full ninety-file integrity/schema execution unverified | No substitution of double results for complete validation |
| D: other commands | Leave transform/answer paths and permissions unchanged | Existing-entry spies; no new common guard | No real answer/oracle/schema/transform validation | No new content permissions or behavior claim |
| E: mutable authority / concurrency / Windows | No expanded defense or authority | Record unverified mutable workspace/pins, rebinding, introspection, TOCTOU, concurrent mutation, and path lifecycle | ACLs, volume/root identity, symlinks/junctions/reparse, rename/replacement, retained identities/handles, repository exclusion, import/native closure unverified; no new URL/redirect/download/network authority | No hostile-runtime, verified-versus-executed byte continuity, or path-security claim |
| F: dependencies / evidence writes | No install, F0 access, or new experimental fixtures | Fail-if-used double; bounded benign scratch cleanup; trusted output producer | Producer, output root, sidecars, failure/cleanup/close evidence are not secure evidence or hostile-path proof | Stub disclosure and evidence/output limitations remain explicit |
| G: resources / reproducibility | Only isolated, diagnosed bounded correction | Exact command/pins/pre-post evidence; TEST does not fix CODE; diagnostic matrix before a second speculative correction | Stop at two independent reject/correct cycles or auxiliary work over thirty minutes; no architecture expansion | Review only the bounded guard claim; wider unknowns stay unverified |

These are bounded cases, not an exhaustive attack model. Any unverified prerequisite blocks broader authority or claims. Review should assess the frozen required claim without turning every nonclaim into new implementation work.

## Procedure and disposition boundaries

CONTROL reports the prior DOCUMENTATION role was retired after malformed PowerShell path-array construction and nonterminating errors allowed three authorized TEST files to be read before hash validation. That role reported no denied/F0 read and no writes. CONTROL rechecked all three pins and output absence before replacement. This replacement independently authenticated literal inputs before content use and found all three output paths absent. This account preserves attribution; replacement and later matching hashes do not retroactively validate the prior procedure.

One opaque unclassified Git-status blocker persists according to CONTROL; no Git publication is authorized. This packet performs no Git mutation. No F0 content, hidden oracle, S0/E0 fixture creation or execution/scoring, real model/provider call, network/download, installation, or independent acceptance is authorized by this work. S0, the central system, Project Brain integration, operational safety, economic value, and model-to-model transfer remain unimplemented/unvalidated claims outside this packet.

Before handoff, DOCUMENTATION must run the pinned canonical validator in native Windows PowerShell with `-SelfTest`, then `-Path` for this README, capturing each exit code immediately. Final output hashes and those check results are transmitted to CONTROL after artifact freeze; they are not a self-approval verdict.
