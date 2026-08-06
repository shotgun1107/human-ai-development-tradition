# I0 limited rereview v0.1

## Verdict

**I0 implementation acceptable but upstream refreeze required.**

Candidate manifest:
`e67004179fc9d922b9fb6d822ac961d576f9c6ca07cd512d4508e29ca038c105`

No new Critical or Major issue was found. This is not an I0 freeze, schema
conformance result, sealed-fixture approval, S0 readiness decision, isolation
proof, or central-system validation.

## Prior finding dispositions

| Finding | Disposition | Evidence summary |
|---|---|---|
| I0-RV1 input boundaries | Resolved | manifest-authenticated role allowlists reject arbitrary and wrong-public canonical, schema, question, package, and answer inputs |
| I0-RV2 forbidden disclosure | Resolved | profile fields, package IDs, relation/error codes, rankings, and readiness/implementation claims rejected in independent mutations |
| I0-RV3 host path leakage | Resolved | shared sanitizer covers ordinary CLI and internally retained verify errors; missing-file tests exposed no host/worktree text |
| I0-RV4 empty residue/overwrite | Resolved | transform completes in memory before exclusive creation; failure leaves no file and existing bytes remain unchanged |
| I0-RV5 test gaps | Resolved with host limitation | expanded boundary, policy, AST, leakage, residue, overwrite, and symlink-attempt coverage; direct symlink execution skipped because Windows denied creation |

## Independent verification

- controlling hashes: 21/21 matched;
- public bundle: 90/90 manifest entries, 56/56 UTF-8 JSON files;
- candidate: exactly 15 listed files before and after tests, no extras or symlinks;
- unittest run 1: 36 total, 35 passed, 1 symlink test skipped;
- unittest run 2: 36 total, 35 passed, 1 symlink test skipped;
- integrity: exit 0;
- schema-check: exit 1 from four designated upstream errors;
- broader audit: 20 related upstream errors = 4 designated + 16 additional;
- verify: exit 1 while retaining the upstream failure;
- package reproduction: 8/8 exact bytes and 8/8 repeat-identical;
- arbitrary/wrong-public substitutions, permissive policy substitutions,
  disclosure mutations, missing-file paths, residue, and overwrite attacks were
  independently exercised and rejected.

## Remaining upstream defect

The four block-2 package identifiers have 13 characters after `PKG-`, while the
three frozen schema locations require 12. This yields:

- run manifest: 4 package-ID errors;
- block-2 fixture manifest: 4 package-ID and 4 runner-path errors;
- block-2 transformation manifest: 4 package-ID and 4 runner-path errors.

The designated eleven-instance result remains four; the expanded impact is 20.
I0 correctly reports and does not repair the frozen inputs.

## Unchecked scope

Direct symlink execution on a symlink-capable host, another-host runtime
reproducibility, sealed fixture, hidden oracle, condition-to-A–D mapping,
executor, model, judge, scoring outcome, run record, real data, network,
database, RAG, UI, cost, Project Brain integration, and central-system paths
remain unchecked. Public phrase recognition does not establish sealed-corpus
generality.
