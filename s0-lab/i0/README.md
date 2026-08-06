# I0 minimum public-development harness

This directory contains only a local Python harness for the frozen, fictional
F0-PUBLIC practice bundle. It checks bundle integrity, the eleven Draft 2020-12
schema mappings, deterministic P01-P04 package generation, and neutral answer
format rules. It does not call an AI model, launch an executor, read a hidden
oracle, score an S0 outcome, or implement the central system.

## Runtime

- Python 3.12.10
- `jsonschema[format]==4.26.0`
- standard-library `unittest`

Current limited re-review regression result: 36 tests total, 35 passed and 1
symlink test skipped on this Windows host. The same result was repeated twice.

The dependency is expected in CONTROL's external temporary virtual environment.
The implementation never installs packages or accesses the network.

## Commands

Run from the repository root after adding `s0-lab/i0/implementation` to
`PYTHONPATH`:

```powershell
python -m s0_i0.cli integrity
python -m s0_i0.cli schema-check
python -m s0_i0.cli verify
python -m unittest discover -s s0-lab/i0/tests -v
```

The `transform` and `answer-check` subcommands accept only workspace-relative
paths. Transform accepts only the two manifest-authenticated public canonical
files. Answer checking fixes the schema, questions, and package to authenticated
allowlists; the answer itself must be one of two frozen public examples or an
untrusted candidate below `s0-lab/i0/`. Transform output must remain below
`s0-lab/i0/`, is created exclusively, and is never overwritten. Failures return
nonzero JSON without absolute host paths.

## Known frozen-input defect

The real Draft 2020-12 engine finds four errors in the designated eleven-instance
check: all four block-2 package IDs in `run-manifest.json` contain 13 characters
after `PKG-`, while the frozen schema permits exactly 12. These four errors are
defect detection, not a conformance pass.

A broader, separately labelled impact audit finds the same ID/path defect eight
times in the block-2 `fixture-manifest.json` and eight times in the block-2
`transformation-manifest.json`. The related upstream impact is therefore 20
violations: 4 designated plus 16 additional. The harness reports them and never
rewrites any frozen input. This candidate cannot be treated as an I0 freeze or
as readiness for sealed fixture work until CONTROL resolves and re-freezes the
upstream inconsistency.

## Boundary

Exact regeneration of eight public packages is a public-format check only. The
P03/P04 adapters recognize explicit phrases in the two practice corpora; they
do not establish that a future sealed corpus can be transformed safely. No S0,
operational isolation, economic value, Project Brain integration, or
model-to-model transfer claim is made. The Windows test host did not permit
creating a symbolic link, so the symlink-specific test is skipped; absolute,
traversal, resolved-containment, manifest allowlist, and substitution attacks
remain covered.
