# I0 / F0-PUBLIC refreeze gate decision v0.1

- decided_at: `2026-08-06T20:53:09.3757082+09:00`
- decision_role: `CONTROL`

## Decision

- F0-PUBLIC v0.1 corrected public-practice refreeze: **APPROVED**
- I0 minimum public-development harness content freeze: **APPROVED**
- sealed F0 fixture authoring: **CLOSED**
- hidden oracle creation: **CLOSED**
- executor A-D creation or execution: **CLOSED**
- S0 execution and scoring: **CLOSED**

The approvals above freeze only the fictional public-practice bundle and the
minimum local I0 harness at the authenticated hashes below. They do not approve
or validate the central system, Project Brain integration, operational safety,
economic value, model-to-model transfer, real-data use, executor isolation,
sealed-fixture quality, or an S0 outcome.

## Frozen hashes

| Artifact | SHA-256 |
|---|---|
| `s0-lab/public-practice/v0.1/bundle-files.sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` |
| `s0-lab/i0/verification/implementation-files.sha256` | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` |
| `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md` | `d9cf2823804bbab60ba62a57dd4a35f1f3e4c2da9f74e6a2d8fa0b8307eb5d6c` |
| `s0-lab/control/i0/i0-refreeze-limited-rereview-brief-v0.1.md` | `56fe17ce8b8bf51bd2aef65de7f1b3309e7c9300346829c17fbdbbfcf6c1f3dc` |
| `s0-lab/reviews/i0/i0-refreeze-limited-rereview-v0.1.md` | `8b0266b6ea73f45e0ec88dd3ae9eabff90e78f202adc386ebbafecfa8e6dbd19` |

The public manifest authenticates exactly 90 non-self files and the I0
manifest authenticates exactly 15 non-self files. Their authenticated file
sets, package bytes, and hashes remained unchanged across the fresh independent
rereview.

## CONTROL evidence

- B2 stems corrected from 13-character `P0xB2EMBER001` to fixed 12-character
  `P0xB2EMBR001` without changing package content bytes.
- public manifest: 90 entries, 56 UTF-8 JSON files, 8 packages; integrity exit 0
- all applicable frozen-schema validation: 19/19, 0 errors
- designated and related schema counts: 0 / 0
- I0 unittest: 36 total, 35 passed, 1 host-constrained symlink skip, 0 failures
- I0 integrity/schema-check/verify exits: 0 / 0 / 0
- verify status: `pass`; package reproduction: 8/8 exact and repeat-identical
- candidate and public manifests: no missing, extra, duplicate, unsafe path,
  self-entry, symlink, JSON failure, or hash mismatch
- repository residue: no `__pycache__`, `.pyc`, smoke, adversarial, or temporary
  test output

## Independent rereview

- Critical findings: 0
- Major findings: 0
- Minor findings: 0
- verdict:
  `I0/F0-PUBLIC refreeze candidate acceptable for CONTROL final-freeze decision`

The rereviewer was a fresh non-fork agent, received only the frozen brief and
its maximum allowlist, made no repository edits, and returned its review to
CONTROL for verbatim recording and hashing.

## Remaining limits and next gate

Direct symlink execution on a symlink-capable host and other-host runtime
reproducibility remain unchecked. Sealed fixtures, hidden oracle, condition
mapping, executors, models, judge, score, run records, real data, network,
database, RAG, UI, cost, Project Brain integration, central-system behavior,
operational safety, economic value, and model-to-model transfer remain
unimplemented or unvalidated.

The next protected activity is sealed F0 authoring. It remains closed until the
user provides a separate exact authorization in a later message. This decision
does not create that authorization. No commit, push, merge, branch deletion,
reset, clean, stash, executor session, model call, or S0 run was performed.
