# I0 independent review v0.1

## Scope and verdict

- candidate manifest: `d5f309e1d9575b2f40b5dd83adeb135a8f737a8982198858cdded4a106d9d373`
- reviewer: fresh read-only `s0_protocol_reviewer`
- verdict: **I0 implementation changes required**
- file writes by reviewer: 0
- sealed fixture, hidden oracle, executor output, real data, network, git, and subagent access: none

This verdict concerns the public-development harness only. It is not an I0
freeze, S0 readiness decision, isolation proof, or central-system validation.

## Major findings

### I0-RV1 — Frozen/public input boundaries were not enforced

The CLI accepted caller-selected workspace-relative canonical, schema,
question, package, and answer paths. Workspace containment prevented traversal
but did not prevent reading unrelated workspace JSON. The answer-validation API
also accepted a substituted permissive schema and empty question projection.
The isolated hash unittest did not make each entry point authenticate inputs
before use.

Required correction: bind each public input role to manifest-authenticated
paths and hashes, keep untrusted candidate answers in an explicitly allowed
output area, and make schema-check authenticate the public bundle before
loading designated instances.

### I0-RV2 — Forbidden-disclosure checks were incomplete

Independent mutations containing `ordering_source`, `source_record_id`,
`from_record_id`, `S0 ready`, or `P01B1MOSS001` were accepted. The policy and
actual public P01–P04 structures contain more condition-specific vocabulary
than the implementation blocked.

Required correction: cover the full public condition-specific field and label
surface and add one negative test per independent bypass class.

### I0-RV3 — CLI errors disclosed absolute host paths

A missing relative input was resolved to an absolute path and the raw
`FileNotFoundError` string was emitted. That exposed the detached worktree path
and violated the host-path-free error requirement.

Required correction: map filesystem failures to stable, path-free messages and
test the actual CLI exception route.

## Minor findings

### I0-RV4 — Failed transform could leave an empty file

The destination was opened with exclusive creation before transformation was
evaluated. Invalid canonical input could therefore leave a zero-byte output.
Compute bytes before opening the destination and test both failure residue and
overwrite refusal.

### I0-RV5 — Tests did not cover several boundary behaviors

Missing coverage included substituted policies, host-path disclosure, failure
residue, overwrite refusal, symlink escape where supported, and helper-mediated
transform dependencies. The 17/17 unittest result was a harness regression
result, not conformance, because a test intentionally detected four upstream
schema failures.

## Upstream frozen-input defect

The designated Draft 2020-12 suite returned four errors because the four
block-2 package IDs have 13 characters after `PKG-`, while the frozen
run-manifest schema requires exactly 12. All 11 schemas self-checked and the
other ten designated instances were valid. This is distinct from I0-RV1–RV5
and must not be auto-repaired by I0.

CONTROL additionally found the same naming conflict in the block-2 fixture and
transformation manifests: each has four invalid package IDs and four invalid
runner paths. Thus the broader public bundle has 20 related schema violations
across three instances, although the frozen designated 11-instance suite
exposes only four.

## Independently verified candidate behavior

- public manifest: 90/90 files, 56/56 JSON, no missing/extra/unsafe/symlinked files;
- candidate manifest: 13/13 files and exact self-excluding file-set equality;
- `unittest`: 17/17 regression tests passed;
- bundle integrity: passed;
- designated schema-check and full verify: exit 1 from the four upstream errors;
- eight package outputs: exact bytes and SHA-256 on two invocations;
- transform signature: `(canonical, profile)` with no model, executor, oracle,
  scoring, database, RAG, UI, network, Project Brain, dynamic execution,
  subprocess, or filesystem dependency in the transformer;
- covered answer and path failures returned nonzero, subject to findings above.

## Unchecked scope

No sealed fixture, hidden oracle, condition-to-A–D mapping, executor, model,
judge, scoring outcome, run record, real data, cost, economic value,
another-host reproducibility, Project Brain integration, or central-system path
was inspected or tested. Public phrase recognition does not establish
sealed-corpus generality.
