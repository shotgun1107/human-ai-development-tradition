# F0-PUBLIC question contract v0.14 CONTROL integration decision

- `decided_at`: `2026-08-08T23:41:25.1569688+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `F0-PUBLIC QUESTION CONTRACT V0.14 CONTROL INTEGRATION AND MAIN MERGE OPEN`
- `source_branch`: `codex/s0-question-contract-v06-review`
- `reviewed_source_commit`: `dfdeeb3bbb51844a8f3ff186c0def0f0f2135c53`
- `pre_merge_main_commit`: `e050fdd1d43d7a9fe5a3bd59349804950b4587a3`

## Decision

The F0-PUBLIC question contract v0.14 proposal is **APPROVED FOR CONTROL INTEGRATION**.

Its independently reconstructed effective contract and public falsification plan are adopted as the current public S0 question-contract design baseline. Versions v0.5 through v0.13 remain preserved as design, failure, correction, and review evidence; they are not the active question contract.

The approved public source lineage may be merged into `main`. This decision does not authorize deletion of predecessor records, branches, worktrees, or the E0 lineage already present on `main`.

## Authenticated artifacts

| Artifact | SHA-256 |
|---|---|
| `universal-response-contract-v0.14-candidate.md` | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` |
| `public-falsification-plan-v0.11.md` | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` |
| `review-response-v0.9.md` | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` |
| `urc-v0.14-independent-review-v0.1.md` | `537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605` |

## Effective construction accepted by CONTROL

| Stream | Slot count | Raw slice bytes | Transformed slice bytes | Stream bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| Contract | 31 | 34,100 | 34,100 | 43,633 | `9cb737c425abc6e0a794b5c4ec439ec6e336022b93a2d2c8aa719c46a78810e3` |
| Plan | 25 | 71,327 | 71,329 | 79,676 | `e869a9e9b98a06c782180e3da9acf371bb35db4cb8855cd27c38a7c16471bd4c` |

The independent review verdict is `PASS-FOR-CONTROL-INTEGRATION-ONLY`, with zero blocking, zero major, and zero minor findings.

## Scope and remaining gates

This is proposal-text and CONTROL-integration acceptance only. It does not establish that S0 works or that any empirical effect exists.

The following remain closed unless separately and explicitly opened by the user:

- implementation schema or runner work;
- key generation or bank construction;
- fixture or hidden-oracle authoring;
- executor sessions or model runs;
- scoring, statistical conclusions, or S0 execution;
- sealed-material access;
- central-system or Project Brain implementation.

The `main` merge preserves the already integrated E0 history and does not change E0's independent status or open an E0 execution gate.
