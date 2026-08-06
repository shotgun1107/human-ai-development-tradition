# I0 independent review brief

## Role and status

Act as a fresh, read-only `s0_protocol_reviewer`. The user opened only `I0`.
Review the public-development implementation candidate; do not implement fixes,
edit files, create fixtures, inspect sealed material, or run S0. The candidate is
not frozen. Its verification currently fails because the frozen public
run-manifest and its schema disagree on four package IDs.

## Maximum allowed input

Read only:

- `AGENTS.md`
- `s0-lab/control/s0-protocol-v0.3.md`
- `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md`
- every file in `s0-lab/control/i0/`
- the 11 schema files and hashes listed by `i0-implementation-brief.md`
- `s0-lab/public-practice/v0.1/bundle-files.sha256` and only its 90 listed files
- `s0-lab/i0/verification/implementation-files.sha256` and only its 13 listed files

Do not search the repository broadly. Do not read another project, real data,
sealed fixture, hidden oracle, scoring outcome, or executor output. The public
scoring example that belongs to the frozen 90-file bundle may be inspected only
for schema/integrity boundaries, never as an outcome oracle.

## Environment

- worktree: `C:/Users/SSAFY/AppData/Local/Temp/ai-development-tradition-i0-c9f68f3`
- Python: `C:/Users/SSAFY/AppData/Local/Temp/ai-development-tradition-i0-venv-c9f68f3/Scripts/python.exe`
- Python SHA-256: `0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14`
- dependency: `jsonschema[format]==4.26.0`
- candidate manifest SHA-256: `d5f309e1d9575b2f40b5dd83adeb135a8f737a8982198858cdded4a106d9d373`

No network, package installation, subagent, git operation, or file write is
permitted. Tests must run with `PYTHONDONTWRITEBYTECODE=1`.

## Review requirements

Independently verify and report:

1. every allowed frozen/control/candidate hash before reliance;
2. candidate file-set equality with its self-excluding manifest;
3. no prohibited AI call, executor/orchestration, hidden-oracle, sealed-fixture,
   S0 scoring, database, RAG, UI, network, Project Brain, or real-data capability;
4. bundle integrity, all 11 schema self-checks and instance checks using the real
   Draft 2020-12 engine with explicit format checking;
5. the exact cause and count of the frozen run-manifest/schema discrepancy;
6. exact eight-package byte reproduction and repeat determinism, while checking
   that the transformer does not consume an oracle, scoring file, expected output,
   another block, filesystem, or network input;
7. neutral-answer validation for missing, duplicate, extra, unsorted, invalid,
   uncited, invalid-affected-ID, and forbidden-disclosure cases;
8. path containment, symlink handling, overwrite behavior, failure exit codes,
   stable error order, and accidental absolute-host-path disclosure;
9. whether tests genuinely exercise the requirements or merely encode the
   candidate's implementation and known defect;
10. documentation honesty, dependency pinning, simplicity, and any unsupported
    readiness claim.

Treat the public adapter's phrase recognition as a known limitation, not proof
of sealed-fixture generality. Distinguish implementation findings from the
upstream frozen-input defect.

## Output

Return a read-only review with:

- verified hashes and exact commands;
- findings ordered `Critical`, `Major`, `Minor`, each with file and line evidence;
- upstream-defect confirmation and the smallest safe correction direction,
  without making the correction;
- one verdict: `I0 implementation acceptable but upstream refreeze required`,
  `I0 implementation changes required`, or `I0 candidate rejected`;
- explicit unchecked scope.

Do not claim I0 frozen, S0 ready, isolation proven, or central-system validation.
