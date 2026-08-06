# I0 public-development verification report

## Status

- Candidate implementation tests: **PASS** (36 total: 35 passed, 1 symlink test skipped on this Windows host)
- Frozen public bundle integrity: **PASS** (`90/90` manifest entries, `56/56` JSON parses)
- Exact deterministic package regeneration: **PASS** (`8/8`, including two-run byte equality)
- Designated Draft 2020-12 instance validation: **PASS** (`11/11`, `0` errors)
- All applicable public schema instances: **PASS** (`19/19`, `0` errors)
- Broader related upstream impact audit: **PASS** (`0` errors)
- Overall I0 freeze readiness: **NOT CLAIMED**

This is a technical public-fixture development record. It is not an S0 run,
score, sealed-fixture approval, executor result, operational-isolation proof,
economic claim, or central-system validation.

## Runtime

- Python: `3.12.10`
- Python executable SHA-256: `0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14`
- `jsonschema`: `4.26.0`
- validator: `Draft202012Validator` with explicit `FormatChecker`
- tests: Python standard-library `unittest`
- network access during implementation and verification: none

## Commands executed

All current refreeze commands ran from the repository root with
`s0-lab/i0/implementation` on `PYTHONPATH` and CONTROL's external temporary
Python interpreter.

```powershell
python -m unittest discover -s s0-lab/i0/tests -v
python -m unittest discover -s s0-lab/i0/tests -v
python -m s0_i0.cli integrity
python -m s0_i0.cli schema-check
python -m s0_i0.cli verify
python -m s0_i0.cli transform --canonical s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/canonical-input.json --profile P03 --output s0-lab/i0/verification/cli-transform-smoke-v2.json
python -m s0_i0.cli answer-check --answer s0-lab/public-practice/v0.1/examples/answer.json --answer-schema s0-lab/control/sm0/answer.schema.json --questions s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0001/questions.json --input s0-lab/public-practice/v0.1/packages/P01B1MOSS001/input.json
python -m s0_i0.cli answer-check --answer s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json --answer-schema s0-lab/control/sm0/answer.schema.json --questions s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json --input s0-lab/public-practice/v0.1/packages/P01B2EMBR001/input.json
```

Expected exit results:

| Command | Exit | Meaning |
|---|---:|---|
| `unittest` | `0` | 36 total: 35 passed; 1 symlink creation test skipped on this Windows host |
| `integrity` | `0` | frozen public bundle integrity passed |
| `schema-check` | `0` | designated eleven and the broader ID/path audit reported zero errors |
| `verify` | `0` | overall technical verification passed and reproduced all eight packages |
| `transform` smoke | `0` | generated P03/block-2 hash matched `7785e4ec...e1a2807` exactly; temporary output removed |
| both `answer-check` commands | `0` | both public expected answers passed neutral format policy |

The final adversarial smoke invoked three standalone CLI failures: a noncanonical
but public JSON substituted as transform input, a non-approved schema substituted
for answer checking, and a missing I0 answer candidate. Each returned exit `2`
with one parseable JSON error, contained zero absolute host/worktree path strings,
and created no output file.

## Resolved upstream discrepancy

The prior public bundle used four 13-character block-2 package payloads:

- `PKG-P01B2EMBER001` through `PKG-P04B2EMBER001`

The frozen `run-manifest.schema.json` requires `^PKG-[A-Z0-9]{12}$`. Under the
separately authorized `F0-PUBLIC REOPEN` gate, those payloads and paths were
renamed to `P0xB2EMBR001`. Package content hashes and bytes did not change.

The designated eleven, the former broader three-instance impact audit, and an
expanded 19-instance applicable-schema pass now all report zero errors. The
earlier 4/20 result remains historical defect-discovery evidence, not the
current candidate result.

## Verified behavior

- All controlling SHA-256 values checked before use.
- Bundle manifest is self-excluding, path-safe, exactly 90 entries, and equal
  to the on-disk public file set.
- All 90 file hashes match and all 56 public JSON files decode as UTF-8 JSON.
- Published fact and record-content aggregates reproduce for both blocks.
- Existing packages preserve complete fact, record, project, timestamp, and
  text objects; package sizes reproduce and remain below the 15% ceiling.
- One canonical object plus one opaque P01-P04 profile regenerates all eight
  expected package files exactly; a second invocation is byte-identical.
- Standalone transform accepts only the two manifest-authenticated canonical
  hashes. Answer validation fixes its schema, two question projections, and
  eight packages to authenticated allowlists; arbitrary workspace substitutes
  are rejected.
- The transform API has no oracle, scoring, expected-output, other-block,
  filesystem, or network input.
- Neutral answer validation runs `answer.schema.json` first, then checks exact
  question membership, option membership, citations, affected IDs, ordering,
  and forbidden structural disclosure without ordinary oracle/scoring access.
- Absolute and traversing paths are rejected; CLI failures are nonzero and
  machine-readable, and missing-file errors contain no absolute host/worktree
  path. Transformation bytes are computed before exclusive output creation;
  malformed input leaves no empty file and existing output is not overwritten.
- CLI and internal verification records share the same path-free exception
  sanitizer. A simulated internal `FileNotFoundError` containing the absolute
  worktree path produced exit `1`, parseable JSON, and zero host-path strings.

## Unchecked and unproven scope

- The P03/P04 public adapters recognize explicit wording in the two fictional
  practice corpora. They are not proof that a future independently authored
  sealed corpus has enough structured canonical information for safe
  deterministic transformation.
- No hidden oracle, sealed fixture, condition mapping, real or past-project
  data, AI model, executor, judge, scoring outcome, database, RAG, UI, network
  service, Project Brain integration, or central-system path was read, created,
  or exercised.
- Runtime reproducibility on another host was not tested.
- The Windows host denied symbolic-link creation, so the direct symlink escape
  test was skipped. Absolute paths, explicit traversal, resolved containment,
  manifest allowlists, and four substituted-input attacks passed.
- CONTROL has verified the refreeze candidate. A fresh independent limited
  rereview has not yet approved or frozen it.
