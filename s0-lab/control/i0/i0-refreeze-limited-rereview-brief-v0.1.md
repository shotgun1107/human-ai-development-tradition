# I0 / F0-PUBLIC refreeze limited rereview brief v0.1

## Role and authority

You are a fresh independent limited rereviewer. You did not author the public
bundle correction or the I0 dependent updates. This review is read-only: do not
edit files, recalculate a mismatched frozen hash into acceptance, install
packages, access the network, call a model, create fixtures or hidden answers,
run S0, commit, push, merge, reset, clean, stash, or create another agent.

This review may decide only whether the identifier-only refreeze candidate is
acceptable for a later CONTROL final-freeze decision. It is not itself a
freeze, sealed-fixture authorization, S0 readiness decision, isolation proof,
or central-system validation.

## Repository state to authenticate

- expected branch: `codex/i0-public-harness-candidate`
- reviewed ancestor: `73c98f8`
- pre-correction handoff ancestor: `2a661e5`
- expected public bundle manifest SHA-256:
  `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637`
- expected public bundle entries: exactly 90 non-self files
- expected public JSON files: exactly 56
- expected I0 candidate manifest SHA-256:
  `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae`
- expected I0 candidate entries: exactly 15 non-self files
- expected F0-PUBLIC refreeze-record SHA-256:
  `d9cf2823804bbab60ba62a57dd4a35f1f3e4c2da9f74e6a2d8fa0b8307eb5d6c`

The worktree is intentionally dirty with the unstaged refreeze candidate. Do
not require a clean worktree and do not stage or alter it. The four old package
paths should appear deleted and the four corrected paths untracked until a
later authorized commit; compare their bytes read-only.

## Maximum allowed inputs

Do not search or read the repository outside this allowlist.

1. `AGENTS.md`
2. this brief and its `.sha256` sidecar
3. `s0-lab/README.md`
4. `s0-lab/control/i0/i0-gate-decision.md` and sidecar
5. `s0-lab/reviews/i0/i0-limited-rereview-v0.1.md` and sidecar
6. `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md` and sidecar
7. every file authenticated by
   `s0-lab/public-practice/v0.1/bundle-files.sha256`, plus that manifest
8. every file authenticated by
   `s0-lab/i0/verification/implementation-files.sha256`, plus that manifest
9. these frozen schemas only:
   - `s0-lab/control/sm0/answer.schema.json`
   - `s0-lab/control/sm0/common-manifest.schema.json`
   - `s0-lab/control/sm0/condition-overlay-manifest.schema.json`
   - `s0-lab/control/sm0/fixture-manifest.schema.json`
   - `s0-lab/control/sm1/question-options.schema.json`
   - `s0-lab/control/sm1/transformation-manifest.schema.json`
   - `s0-lab/control/sm1/neutral-answer-validation.schema.json`
   - `s0-lab/control/sm1/access-manifest.schema.json`
   - `s0-lab/control/sm1/run-manifest.schema.json`
   - `s0-lab/control/sm1/scoring.schema.json`
   - `s0-lab/control/sm1/pre-review-record.schema.json`
10. read-only Git metadata required for `status`, branch/HEAD/ancestor checks,
    `diff --check`, and diffs limited to the files above
11. the existing external CONTROL Python 3.12 environment at
    `C:/tmp/hadt-i0-control-2a661e5-py312`, only for the commands below

The allowlist is a maximum, not a suggestion to inspect unrelated files.

## Frozen correction intent

The prior public bundle used four 13-character block-2 package stems:
`P0xB2EMBER001`. The frozen schemas require 12 characters. The authorized
correction is only:

`P0xB2EMBER001` -> `P0xB2EMBR001`

The correction may update the four package paths, three affected public
manifests, dependent public hashes/references, public validation report, F0
refreeze record, I0 authenticated allowlists, I0 regression expectations, I0
verification report, and both self-excluding manifests. Facts, questions,
options, transformations, expected decisions, scoring rules, package bytes,
and package content hashes must not change.

## Required independent checks

1. Verify every supplied sidecar before reading its target.
2. Verify both manifest SHA-256 values, exact file sets, every listed file hash,
   no self-entry, duplicate, missing, extra, absolute path, `..`, backslash,
   symlink, or JSON parse failure.
3. Confirm the four corrected package files retain these exact content hashes:
   - P01: `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7`
   - P02: `5a87fbe35c56c0a754149ba47e5f42a7af046ebd705514cf208639caaccf3aae`
   - P03: `7785e4ece12a23fcb9f70c334bb8218fd8eb3c2bdcad2593a2a9c56b6e1a2807`
   - P04: `a27de682b641907685db3052656c200edb866b5e3356288426bd5f0bab226af6`
4. Confirm no operational public manifest, I0 implementation, or I0 test still
   uses `B2EMBER001`; historical discussion may retain the old string.
5. Inspect the allowlisted diff for identifier-only scope, complete dependent
   hash propagation, unchanged safety boundaries, and no overclaim of final
   freeze or S0 readiness.
6. With repository root computed from the current checkout, set
   `PYTHONPATH=s0-lab/i0/implementation` and `PYTHONDONTWRITEBYTECODE=1`, then
   run with the external Python 3.12 interpreter:
   - `python -m unittest discover -s s0-lab/i0/tests -v`
   - `python -m s0_i0.cli integrity`
   - `python -m s0_i0.cli schema-check`
   - `python -m s0_i0.cli verify`
7. Independently validate all 19 applicable public instances against the eleven
   frozen Draft 2020-12 schemas with explicit format checking.
8. Confirm expected results: 36 tests, 35 pass, at most one host-constrained
   symlink skip, no failure; all three CLI exits 0; manifest 90, JSON 56,
   packages 8; designated and related schema errors 0; verify status `pass`;
   package reproduction 8/8 exact and repeat-identical.
9. Confirm `git diff --check` passes and no `__pycache__`, `.pyc`, or temporary
   smoke/adversarial output remains in the repository.

Stop immediately and report without repair on any mismatch, missing/extra
file, unsafe path, unexpected symlink, JSON failure, schema error, package-byte
change, test failure, host-path leakage, stale operational identifier, or
meaning/scoring change.

## Required response

Return a concise review containing:

- manifest and sidecar authentication results
- exact correction-scope assessment
- test and schema results with exit codes/counts
- findings grouped as Critical, Major, Minor, or none
- unchecked scope
- exactly one verdict:
  - `I0/F0-PUBLIC refreeze candidate acceptable for CONTROL final-freeze decision`
  - `I0/F0-PUBLIC refreeze candidate requires changes`
  - `I0/F0-PUBLIC refreeze candidate review unable to complete`

Do not write the review into the repository. Return it to CONTROL for verbatim
recording and hashing after review completion.
