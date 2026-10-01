# A05 profile composition v0.1

This is a bounded public source/unit candidate for the F03 profile-composition data-flow correction. Independent review is **PENDING** at this documentation freeze; CONTROL has not accepted the candidate. It is not live-path integration or a complete historical, native, assembly, S0, or E0 validation.

The candidate separates the original historical P4 profile from the effective current profile and gives current runtime material an explicit, separately checked closure. It uses the existing JSON, manifest, and SHA-256 primitives. This is auxiliary source-remediation work within the authorized F01-F08 corrections; it does not establish the central system or open an execution gate.

## Authenticated baseline and ownership

The authenticated repository is `C:/Users/SSAFY/Documents/ai-development-tradition`, branch `codex/windows-build-toolchain-environment-v0.1`, HEAD `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`, tree `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`. The root `AGENTS.md` SHA-256 is `393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e`. These identify the inherited baseline; the new candidate files are separately pinned by `candidate-files.sha256`.

CONTROL is `/root`; CODE is `/root/audit_a05_code`; TEST/VERIFICATION is `/root/audit_a05_test`; DOCUMENTATION is `/root/audit_a05_docs`. A fresh read-only `/root/audit_a05_review` is planned after this handoff. Documentation reports authenticated source and TEST evidence and does not independently approve either.

Only candidate `profile.py` and `preloader.py` differ from the authenticated recovery source. The other eight candidate modules are byte-identical to their originals. Original source, recovered historical P4, schemas, and interface map remain preserved. The exact read/write limits, pins, ownership, and pre-CODE checklist transcription are in [SCOPE-AND-CHECKLIST.md](SCOPE-AND-CHECKLIST.md).

## Source correction and caller migration

`SuccessorProfileMaterial` requires three additional caller inputs: `current_runtime_manifest_raw`, `expected_current_runtime_manifest_sha256`, and `current_runtime_files`. Missing arguments fail; there is no historical-runtime fallback. Runtime and package maps are copied into bounded immutable snapshots, and the current manifest digest is checked against the explicit supplied expected digest. That digest is caller-supplied candidate data, not independently issued authority.

The successor validator first executes the full historical validator, then retains the ordered P1-P4 pins and the existing design, schema/map, semantic-validator binding, and native provenance gates. Their requirements have not been relaxed to accommodate missing material. The original historical validator, design gate, and native gate bodies are preserved, as checked by TEST's AST comparison.

The current package must have exactly these six rows, in the existing manifest order:

1. `runtime-files.sha256`
2. `runtime-profile-v0.1.json`
3. `runtime-profile-v0.2.json`
4. `runtime-profile-v0.3.json`
5. `runtime-profile-v0.4.json`
6. `runtime-profile-v0.5.json`

The first row binds the separately verified current runtime manifest and its exact byte inventory. P1-P4 retain their frozen predecessor pins; P4 and P5 bind the supplied original P4 and successor overlay bytes. The effective object is canonicalized and hashed separately, retaining the historical package closure and historical semantic-relation scope.

| Identity or consumer | Source used by this candidate |
| --- | --- |
| Effective profile object, raw bytes, and digest | One canonical composed snapshot with current closure and overlay |
| Original P4 raw bytes and digest | Separately retained historical profile identity |
| Launch control and launch artifacts | Validated current runtime snapshot |
| Launch package digest | Validated current six-row package manifest |
| Evidence/admission `runtime_profile_v0_4_sha256` | Original historical P4 digest |
| Prepared-launch `runtime_profile_sha256` | Effective composed profile digest |
| Static-relation scope | `historical-profile-v0.4`; deferred relations stay deferred |

The preloader revalidates raw inputs on each call. It reads control, artifacts, and package material from the same validated current snapshot; missing current control or artifacts fail even when historical versions exist. Its results remain ordinary caller-mintable data with `candidate_only=True` and `native_api_reachable=False`. Neither the result type nor coherent hashes grant launch capability or prove that native bytes were executed or imported.

## Authenticated bounded verification

The final TEST evidence records **36 tests, 0 failures, 0 errors**. All 26 pinned inputs have identical pre/post hashes; DOCUMENTATION authenticated those pins again before using the evidence. The test source and stdout hashes agree with the authenticated result record.

| TEST-owned artifact | SHA-256 |
| --- | --- |
| `tests/test_profile_composition.py` | `a1a20ede2c99ebb6e0fa8b8196d6e809f63d13f22418fd7ad193806830fc6812` |
| `verification/test-results.json` | `03277de88f8c3353c72aefcc7fbb3723fb633bd385b89027b8cf9cc92a71af77` |
| `verification/test-stdout.txt` | `c15324516b0fc1685c0ee9884dc65da1f7788f4ed7236bdfc3198a0c406ba1ab` |

The recorded command, run by TEST and not rerun by DOCUMENTATION, is:

```powershell
& 'C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe' -I -S -B -X utf8 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a05-profile-composition-v0.1/tests/test_profile_composition.py'
```

The recorded interpreter is Python `3.12.10`; the authenticated executable SHA-256 is `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`. The report inventories the test and the ten candidate repository modules imported. Original source was read for preservation/AST comparison, not imported or executed. The harness prohibits network, subprocess, and native-load audit events and uses only the two exact verification output paths; this is not a proof against a hostile interpreter.

The 36 tests cover current manifest/package binding, malformed and mismatched inputs, immutable snapshots and caller mutations, historical/effective identity separation, preserved gates and ordering, and real downstream launch/evidence/admission data consumers. A real negative test uses the pinned P4 and v0.4 schema, reaches `validate_static_relations`, and rejects the deliberately incomplete predecessors at `profile-predecessor-hashes-equal` before successor design work.

Positive composition and consumer tests explicitly replace unavailable upstream prerequisites: the full historical validator returns a coherent P4 data wrapper; P1-P3 pins are replaced by benign unit-parameter hashes; design and native gates are no-op spies; and overlay-schema validation is a no-op for the minimal overlay. P4 and v0.5 schema/map byte pins remain real. Negative diagnostics also isolate individual gates using labelled preceding-gate doubles. These doubles do not establish any missing historical, design, schema, or native prerequisite.

The runtime count limit of 512 is exercised directly. The 512 MiB byte-bound behavior is exercised with a labelled temporary three-byte limit, without allocating a 512 MiB payload. Manifest length limits are tested directly with bounded inputs. The tests use benign in-memory unit parameters; they create no S0/E0 execution fixtures or hidden oracle.

CONTROL's handoff records an initial 36-test pass, followed by strengthening the same historical-semantic-negative assertion and a final 36-test pass after the changed test bytes. No CODE correction or expanded test scope occurred between those runs. The durable final artifacts above substantiate the final run; this paragraph attributes the earlier run history to the handoff, not to an invented second result file.

## Limits and unresolved integration

The complete positive historical material bundle is unavailable. Full F03 integration and native execution remain blocked. Native `ArtifactMaterial.virtual_path` values have no authenticated mapping to the current runtime-manifest keys in the allowed input set. That mapping is **UNVERIFIED**; no aliases were guessed, and existing native checks were preserved. This candidate cannot claim complete current-native/runtime acceptance.

Actual executed/imported native byte identity, installed interpreter/stdlib/native closure, external URL/redirect/digest/size/provenance verification, and hostile interpreter/global compromise remain **UNVERIFIED**. Windows ACLs, volume/root identity, symlink/junction/reparse behavior, concurrent rename/replacement, retained identities/handles, repository exclusion, and TOCTOU through output/evidence writes also remain **UNVERIFIED**. The in-memory virtual-path rejects and observed non-reparse output ancestry are bounded data and trusted-maintenance observations, not adversarial Windows filesystem isolation.

No native lifecycle, filesystem evidence writer, native cleanup/close behavior, or live launch was validated. The TEST harness writes deterministic JSON/text results to its two owned paths and checks exact input hashes before and after; it creates no scratch artifacts. Documentation sidecars are checked with the canonical text tool. These measures support this source/unit handoff only.

S0/E0 execution or scoring, hidden-oracle creation, provider calls, central-system or Project Brain integration, operational safety, economic value, and model-to-model transfer are not implemented or validated by this candidate. No Git publication or wider access is authorized by this document.

## Artifact closure

`candidate-files.sha256` contains exactly 17 ASCII-sorted repository-relative records: ten implementation files, three TEST files, and the two Markdown documents with their two sidecars. It excludes itself and any future CONTROL disposition. The manifest digest and final documentation hashes belong in the handoff; this README does not embed the manifest's own digest.

The required next sequence is fresh independent review, followed by CONTROL's decision. A later review or decision must be represented separately and must not rewrite this pending documentation freeze or the original frozen input hashes.
