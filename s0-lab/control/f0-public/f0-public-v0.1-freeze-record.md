# F0-PUBLIC v0.1 freeze record

- status: `FROZEN—PUBLIC-PRACTICE-ONLY`
- frozen_at: `2026-08-06T15:35:56.3502471+09:00`
- next_gate: `I0` — closed pending exact user authorization

## Frozen controlling inputs

| Artifact | SHA-256 |
|---|---|
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| `s0-lab/control/sm0/sm0-freeze-record.md` | `db29efe079e7b6548b7afb6380cb548997a061da84009c235dfd5be220a5f033` |
| `s0-lab/control/sm1/sm1-freeze-record.md` | `cdbd9dc560da7a41dfc57ec885def730edcdc7718f483f23c60d6868ddef5d00` |
| `s0-lab/control/f0-public/f0-public-gate-record.md` | `cce574512db0fe46bfb56c7be30a04c261931772441ff160ca125b00f88b5c34` |
| `s0-lab/control/f0-public/f0-public-authoring-brief.md` | `cc30d87e96e58e80edb8ebebee062e87f753b7edbac61b1fbc2db536c213dcb7` |
| `s0-lab/control/f0-public/f0-public-independent-review-brief.md` | `54c6480a250cca67634d415a127b95c909cc0a4e0bcedc34ff0b9a13cbe14cb8` |

## Frozen output and reviews

| Artifact | SHA-256 |
|---|---|
| `s0-lab/public-practice/v0.1/bundle-files.sha256` | `993f44896184617035609f117060c3a16d36bd44a7284178de3c5dd0ea6ec47f` |
| `s0-lab/reviews/f0-public-v0.1-independent-review.md` | `8af7e36ecb46fa24d991e81ce08af4fcb143f1ac1119396af1a4f245731633c5` |
| `s0-lab/reviews/f0-public-v0.1-final-limited-rereview.md` | `54903fdd5d640110c7653d6259a0d9796a78b0382297d9fc30b50730abc9cecb` |

The bundle manifest fixes 90 non-self files in a 91-file directory. Independent rereview verdict: `현재 F0-PUBLIC 동결 가능`.

## Verified at freeze

- manifest entries: 90/90, missing/extra/hash mismatch/self-entry: 0
- authored JSON parse: 56/56
- P01–P04 fact equality: pass for both practice blocks
- public questions: 7 per block and condition
- maximum byte excess: block 1 `13.4676%`, block 2 `14.2098%`
- runner answer-hint regression search: 0
- P04 counterexample provenance includes source and target-identifying facts: pass
- published `fact_set_sha256` and `record_content_set_sha256`: independently reproduced
- prior findings F0P-B01, B02, M01, N01, N02: all sufficient

## Boundary and residual limitation

This freeze approves only the fictional public schema-practice bundle for later I0 implementation checks. It does not approve or create sealed F0 material, a hidden oracle, implementation, model/session isolation, an executor, a run, a score, or evidence of system effectiveness.

No Draft 2020-12 validator engine was available. Static schema review passed, but validator-engine validation remains a required I0 entry check. No commit, push, or branch was created.
