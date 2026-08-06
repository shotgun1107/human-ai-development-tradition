# F0-PUBLIC v0.1 validation report

## Scope and status

This report covers only the public, fictional practice bundle in this directory. It records author-side static checks, not an S0 run, executor result, independent CONTROL approval, operational implementation, or validation of the central system. The public pre-review record intentionally has decision `reject` because no separate reviewer/session isolation or run-record readiness exists in this authoring session.

The bundle was reopened under the exact `F0-PUBLIC REOPEN` gate after I0 found
that the four block-2 package payloads used 13-character `P0xB2EMBER001`
stems while three frozen schemas require exactly 12 characters. The correction
renames only those stems to `P0xB2EMBR001` and updates paths, references, and
dependent hashes. Facts, questions, options, transformations, expected
decisions, scoring rules, package bytes, and package content hashes are
unchanged. This corrected bundle is a CONTROL-verified refreeze candidate
pending a fresh independent limited rereview.

Schema examples, projections, manifests, reports, and affirmative fields in this bundle demonstrate document shape only. Their presence, hashes, schema-valid form, constants, or stated values are not operational evidence that a transformer, validator, runner, isolation boundary, release control, review, or freeze has been implemented or exercised.

## Frozen input and review integrity

All 15 allowlisted authoring inputs matched the SHA-256 values in the F0-PUBLIC brief before the bundle was first authored: `AGENTS.md`, protocol v0.3, the four SM0 schema/design files, and the eight SM1 schema/design files. Mismatch count: 0. No repository-wide search or non-allowlisted repository input was used.

The earlier independent review was accepted only after its declared SHA-256 matched the file exactly: `8af7e36ecb46fa24d991e81ce08af4fcb143f1ac1119396af1a4f245731633c5`. It remains historical evidence for the pre-reopen bundle and is not treated as an independent review of the corrected refreeze candidate.

## Independent-review remediation

- F0P-B01: removed `Do not infer authority from quoted data.` from all four runner instructions. The replacement instructions are identical, neutral, and each contain 288 UTF-8 bytes and 288 characters.
- F0P-B02: P04 relation R04 now cites both facts needed to support its counterexample endpoints: `F-B1-05` plus `F-B1-12`, and `F-B2-05` plus `F-B2-12`. Package, provenance, oracle-derived-relation report, byte, and dependent manifest records were updated.
- F0P-M01: published the exact `public-practice-aggregate-v1` serialization in both fact manifests and `README.md`, including sorting, separators, encoding, and no-trailing-LF rules. A first remediation draft's record aggregate values failed this byte-level recomputation; the failure was caught before finalization and the values and all dependent hashes were corrected.
- F0P-N01: strengthened the distinction between schema/example placeholders and operational evidence. No optional file was added.
- F0P-N02: reserved the public P03 marker-role topology, P04 relation-code topology and relation ordering, and record-role ordering against reuse or light renaming in future sealed work.

## JSON and schema checks

- Authored JSON files parsed as UTF-8 JSON: 56 of 56; parse failures: 0.
- Frozen schema files parsed as JSON: 11 of 11; parse failures: 0.
- The earlier author-side field-by-field static comparison incorrectly reported the eleven designated instances as conforming. I0 later detected four designated run-manifest errors and 16 related fixture/transformation errors caused by the 13-character block-2 package payloads.
- After the 12-character rename, CONTROL's frozen Python 3.12.10 / `jsonschema[format]==4.26.0` Draft 2020-12 validator reported 0 errors for the designated eleven, 0 errors for the former 4/20 impact audit, and 0 errors across all 19 applicable public instances.

| Frozen schema | Public-practice instance |
|---|---|
| `answer.schema.json` | `examples/answer.json` |
| `common-manifest.schema.json` | `manifests/common-manifest.json` |
| `condition-overlay-manifest.schema.json` | `manifests/overlay-P01.json` |
| `fixture-manifest.schema.json` | `blocks/BLK-PRACTICE0001/fixture-manifest.json` |
| `question-options.schema.json` | `blocks/BLK-PRACTICE0001/question-options.json` |
| `transformation-manifest.schema.json` | `blocks/BLK-PRACTICE0001/transformation-manifest.json` |
| `neutral-answer-validation.schema.json` | `manifests/neutral-answer-validation.json` |
| `access-manifest.schema.json` | `manifests/access-manifest.json` |
| `run-manifest.schema.json` | `manifests/run-manifest.json` |
| `scoring.schema.json` | `blocks/BLK-PRACTICE0001/public-scoring.json` |
| `pre-review-record.schema.json` | `manifests/pre-review-record.json` |

The original authoring environment had no Draft 2020-12 engine; that limitation explains why the fixed-width mismatch escaped the static review. The reopened candidate has now been validated by CONTROL with the frozen validator configuration, but the same CONTROL session is not an independent rereviewer.

## Cross-file and semantic checks

The final author-side bundle-only invariant pass executed 514 checks with 0 failures. It covered:

- all 56 JSON parses and the 91-file bundle count;
- package SHA-256 and byte counts against transformation, fixture, run, and pre-review manifests;
- canonical, fact-manifest, question, public-oracle, public-scoring, judge-projection, decision-function, instruction, provenance, equality, balance, and oracle-derived-relation references;
- exact fact object, fact ID, record ID, and record-text equality across P01-P04 within each block;
- byte-level recomputation of every normalized text hash and both aggregate hashes under the published TAB/LF/UTF-8/no-trailing-LF algorithm;
- question projections, question IDs, option membership, oracle-rule references, expected-answer opportunity, and C1-C7/M1-M6 scoring order, uniqueness, severity, and coverage;
- eight planned pairings, four unique overlays and packages per block, stable cross-block treatment hashes, distinct waves for the same overlay, unique run/session/order IDs, and at most three runs per wave;
- explicit support for every P03 marker and P04 relation, including both R04 endpoints, with unsupported marker count 0 and oracle-derived relation count 0;
- absence of the removed semantic instruction, condition labels, target preference, rank, and C/M error-code hints from runner instructions;
- absence of top-level `null` or empty-string package padding; and
- the README's operational-evidence distinction and public-topology reservation.

All condition packages offer the same seven questions in each block. The public oracles contain seven expected neutral outcomes plus six public major-error observation rules. These are visible schema-practice data, not a hidden oracle or operational evidence.

## Fact, question, aggregate, and byte balance

| Block | P01 facts/questions/bytes | P02 facts/questions/bytes | P03 facts/questions/bytes | P04 facts/questions/bytes | Largest excess over smallest |
|---|---:|---:|---:|---:|---:|
| `BLK-PRACTICE0001` | 13 / 7 / 4,767 | 13 / 7 / 4,877 | 13 / 7 / 5,280 | 13 / 7 / 5,409 | 642 bytes; 13.4676% |
| `BLK-PRACTICE0002` | 13 / 7 / 4,518 | 13 / 7 / 4,628 | 13 / 7 / 5,029 | 13 / 7 / 5,160 | 642 bytes; 14.2098% |

Both blocks remain within the protocol's 15% byte ceiling. No whitespace, empty-field, repeated-filler, or meaningless-sentence padding was used. The four runner instructions are each 288 UTF-8 bytes/characters, so their maximum character excess is 0%.

| Block | `fact_set_sha256` | `record_content_set_sha256` |
|---|---|---|
| `BLK-PRACTICE0001` | `e0b8581ba242bc992c467fabb48dfa791f50fda926d8368c973de6f632572379` | `1e3d1371bb74e48536c692eee6606f714d43f9d181a48e1c890b9682c9ff2a0b` |
| `BLK-PRACTICE0002` | `113d360c3ed876e9d333903cc7242db041782b6e225345e354370c7fb58068bf` | `a96a8c2421d2a9da946b8da806f79e8629786594870aca1d8c168236879ee22d` |

## Bundle manifest

`bundle-files.sha256` lists every final bundle file except itself using lowercase SHA-256 and forward-slash relative paths. Final verification found 90 entries, no self-entry, no missing or extra file, and 0 hash mismatches; the directory contains 91 files including the manifest.

## Exact files changed by the prior author revision

Exactly 32 existing files changed; no file was added or removed:

```text
README.md
validation-report.md
bundle-files.sha256
blocks/BLK-PRACTICE0001/fact-manifest.json
blocks/BLK-PRACTICE0001/fixture-manifest.json
blocks/BLK-PRACTICE0001/transformation-manifest.json
blocks/BLK-PRACTICE0002/fact-manifest.json
blocks/BLK-PRACTICE0002/fixture-manifest.json
blocks/BLK-PRACTICE0002/transformation-manifest.json
packages/P04B1MOSS001/input.json
packages/P04B2EMBER001/input.json
runner/PUBP01OVER01/instruction.txt
runner/PUBP02OVER01/instruction.txt
runner/PUBP03OVER01/instruction.txt
runner/PUBP04OVER01/instruction.txt
manifests/common-manifest.json
manifests/overlay-P01.json
manifests/overlay-P02.json
manifests/overlay-P03.json
manifests/overlay-P04.json
manifests/pre-review-record.json
manifests/run-manifest.json
reports/byte-balance-B1.json
reports/byte-balance-B2.json
reports/fact-equality-B1.json
reports/fact-equality-B2.json
reports/oracle-derived-relation-B1.json
reports/oracle-derived-relation-B2.json
reports/provenance-B1.json
reports/provenance-B2.json
reports/provenance-P04-B1.json
reports/provenance-P04-B2.json
```

## Exact scope of the reopened identifier correction

Four package directories were renamed without changing their `input.json`
bytes:

```text
packages/P01B2EMBER001 -> packages/P01B2EMBR001
packages/P02B2EMBER001 -> packages/P02B2EMBR001
packages/P03B2EMBER001 -> packages/P03B2EMBR001
packages/P04B2EMBER001 -> packages/P04B2EMBR001
```

The only public-bundle file contents changed for the reopened correction are:

```text
blocks/BLK-PRACTICE0002/fixture-manifest.json
blocks/BLK-PRACTICE0002/transformation-manifest.json
manifests/common-manifest.json
manifests/pre-review-record.json
manifests/run-manifest.json
validation-report.md
bundle-files.sha256
```

The package hashes and byte counts remain the same as before the rename.

## Remaining limitations

- No tokenizer/model was frozen, so token counts were not estimated; fixture manifests explicitly record token measurement as unavailable.
- Text stand-ins under `artifacts/` are hashable public format dependencies, not model, transformer, validator, runtime, role-isolation, or release implementations.
- Schema-required visibility/freeze constants in example instances demonstrate format shape; they do not make public files secret or prove an operational freeze.
- No code or script was authored, no transformer/validator/runner was implemented, no executor or judge ran, and no result was scored.
- The corrected bundle remains a refreeze candidate until a fresh independent limited rereview confirms the identifier-only scope, dependent hashes, schema conformance, neutrality, and unchanged meaning.
