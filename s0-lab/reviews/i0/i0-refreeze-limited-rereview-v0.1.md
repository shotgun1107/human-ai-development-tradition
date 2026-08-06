## I0/F0-PUBLIC refreeze limited rereview

### Authentication

- Expected branch confirmed: `codex/i0-public-harness-candidate`.
- `HEAD` is `2a661e5`; reviewed ancestor `73c98f8` and handoff ancestor `2a661e5` authenticated.
- Sidecars matched:
  - rereview brief: `56fe17ce...1f3dc`
  - I0 gate decision: `9df3027b...4450`
  - prior limited rereview: `8217c581...4433`
  - F0-PUBLIC refreeze record: `d9cf2823...5d6c`
- Public manifest: `e41ee6c...eb637`; exactly 90 non-self entries and 56 valid UTF-8 JSON files.
- I0 manifest: `f57514f9...12ae`; exactly 15 non-self entries.
- Both manifests had zero missing, extra, duplicate, unsafe, absolute, traversal, backslash, self, hash-mismatched, or symlink entries. Post-test authentication remained unchanged.
- All eleven frozen schemas matched their authenticated hashes and parsed successfully.

### Correction scope

The diff is identifier-only and propagates dependent hashes completely. Operational references consistently change `P0xB2EMBER001` to `P0xB2EMBR001`. Remaining old strings occur only in explicitly historical discussion.

The four renamed package files are byte-identical to their pre-correction versions:

- P01: 4,518 bytes, `15bace15...e03b7`
- P02: 4,628 bytes, `5a87fbe3...3aae`
- P03: 5,029 bytes, `7785e4ec...2807`
- P04: 5,160 bytes, `a27de682...af6`

No facts, questions, options, transformation semantics, expected decisions, scoring rules, package content hashes, safety boundaries, or readiness claims changed. The records continue to withhold final freeze, sealed-fixture authorization, and S0 readiness.

### Tests and schemas

- Unit tests: exit `0`; 36 total, 35 passed, one host-constrained symlink skip, zero failures.
- `integrity`: exit `0`; 90 manifest entries, 56 JSON files, 8 packages.
- `schema-check`: exit `0`; designated errors `0`, additional errors `0`, related errors `0`.
- Independent Draft 2020-12 validation with explicit format checking: exit `0`; 19/19 applicable instances, zero errors.
- `verify`: exit `0`; status `pass`.
- Package reproduction: 8/8 exact and repeat-identical.
- Host-path leakage checks passed.
- `git diff --check`: exit `0`.
- No `__pycache__`, `.pyc`, smoke, adversarial, or temporary output residue detected.

### Findings

- Critical: none
- Major: none
- Minor: none

### Unchecked scope

Direct symlink execution on a symlink-capable host, other-host reproducibility, sealed fixtures, hidden oracle, condition-to-executor mapping, executors, models, judge, scoring outcomes, run records, real data, network, database, RAG, UI, cost, Project Brain integration, central-system behavior, operational safety, economic value, and model-to-model transfer remain unchecked.

### Verdict

I0/F0-PUBLIC refreeze candidate acceptable for CONTROL final-freeze decision
