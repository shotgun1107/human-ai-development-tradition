# F0-PUBLIC v0.1 freeze record

- status: `REFREEZE-CANDIDATE—CONTROL-VERIFIED`
- frozen_at: `2026-08-06T15:35:56.3502471+09:00`
- reopened_at: `2026-08-06` under exact gate `F0-PUBLIC REOPEN`
- refreeze_candidate_at: `2026-08-06T20:34:00.2594157+09:00`
- next_gate: fresh independent limited rereview — required before final refreeze

## Frozen controlling inputs

| Artifact | SHA-256 |
|---|---|
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| `s0-lab/control/sm0/sm0-freeze-record.md` | `db29efe079e7b6548b7afb6380cb548997a061da84009c235dfd5be220a5f033` |
| `s0-lab/control/sm1/sm1-freeze-record.md` | `cdbd9dc560da7a41dfc57ec885def730edcdc7718f483f23c60d6868ddef5d00` |
| `s0-lab/control/f0-public/f0-public-gate-record.md` | `cce574512db0fe46bfb56c7be30a04c261931772441ff160ca125b00f88b5c34` |
| `s0-lab/control/f0-public/f0-public-authoring-brief.md` | `cc30d87e96e58e80edb8ebebee062e87f753b7edbac61b1fbc2db536c213dcb7` |
| `s0-lab/control/f0-public/f0-public-independent-review-brief.md` | `54c6480a250cca67634d415a127b95c909cc0a4e0bcedc34ff0b9a13cbe14cb8` |

## Current candidate output and historical reviews

| Artifact | SHA-256 |
|---|---|
| `s0-lab/public-practice/v0.1/bundle-files.sha256` | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` |
| `s0-lab/reviews/f0-public-v0.1-independent-review.md` | `8af7e36ecb46fa24d991e81ce08af4fcb143f1ac1119396af1a4f245731633c5` |
| `s0-lab/reviews/f0-public-v0.1-final-limited-rereview.md` | `54903fdd5d640110c7653d6259a0d9796a78b0382297d9fc30b50730abc9cecb` |

The bundle manifest fixes 90 non-self files in a 91-file directory. The two
listed review hashes cover the pre-reopen bundle only. Their historical verdict
is not reused as approval of this corrected candidate.

## Verified for the refreeze candidate

- manifest entries: 90/90, missing/extra/hash mismatch/self-entry: 0
- authored JSON parse: 56/56
- all applicable Draft 2020-12 public instances: 19/19, errors: 0
- designated eleven schema instances: 11/11, errors: 0
- former broader ID/path impact audit: designated 0, additional 0, related 0
- I0 regression: 36 total, 35 passed, 1 host-constrained symlink skip, 0 failures
- I0 integrity/schema-check/verify exits: 0/0/0; verify status: `pass`
- deterministic package reproduction: 8/8 exact bytes and 8/8 repeat-identical
- P01–P04 fact equality: pass for both practice blocks
- public questions: 7 per block and condition
- maximum byte excess: block 1 `13.4676%`, block 2 `14.2098%`
- runner answer-hint regression search: 0
- P04 counterexample provenance includes source and target-identifying facts: pass
- published `fact_set_sha256` and `record_content_set_sha256`: independently reproduced
- prior findings F0P-B01, B02, M01, N01, N02: unchanged by the identifier-only correction

## Boundary and residual limitation

This CONTROL result covers only the fictional public schema-practice refreeze
candidate and its I0 regression. It is not yet the fresh independent limited
rereview required for final refreeze. It does not approve or create sealed F0
material, a hidden oracle, model/session isolation, an executor, a run, a score,
or evidence of system effectiveness.

The original static review missed the fixed-width defect. This candidate was
rechecked with CPython 3.12.10 and `jsonschema[format]==4.26.0`; no commit, push,
merge, sealed-fixture work, or S0 execution occurred.
