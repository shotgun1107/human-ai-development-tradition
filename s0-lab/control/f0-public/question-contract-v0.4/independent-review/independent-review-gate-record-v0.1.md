# URC-0.4 independent-review gate record v0.1

- opened_at: `2026-08-07` (KST)
- opening_signal: `F0-PUBLIC QUESTION CONTRACT V0.4 INDEPENDENT REVIEW OPEN`
- opening_role: `USER`
- control_role: `CONTROL`
- reviewer_role: fresh read-only `s0_protocol_reviewer`
- status: `OPEN FOR ONE INDEPENDENT DESIGN REVIEW`

## Purpose

Independently attempt to reject the protected URC-0.4 public question-contract candidate before any public fixture authoring, implementation, execution, sealed access, or S0 work is authorized.

## Maximum reviewer input allowlist

| SHA-256 | Path |
|---|---|
| `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | `AGENTS.md` |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` |
| `7230ac449d06a4eb4ea74887d1bf163bb3e6ed9808077f27e7d1e19dff154703` | `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-decision-v0.1.md` |
| `d1f2a41a4cfccf1e8e3e6bb8ceee186648e6dc2c4ea540f71e4b25f57a7aa806` | `s0-lab/control/f0-public/question-contract-v0.4/f0-public-question-contract-v0.4-gate-record.md` |
| `1a06737a8f7de90bdb8c0c467cf3bc0ccab236ced91e3fb364e91ea1dc1d4a82` | `s0-lab/control/f0-public/question-contract-v0.4/universal-response-contract-v0.4-candidate.md` |
| `9649bcffa2b8d39a03077b7797e537912525ed664d57486fd28466b0ca0440a8` | `s0-lab/control/f0-public/question-contract-v0.4/public-falsification-plan-v0.1.md` |
| `18be3f037ebed89f030dc3109f3b26566a2d5a39151980722009fe19cf69b1f7` | `s0-lab/control/f0-public/question-contract-v0.4/control-design-assessment-v0.1.md` |

The reviewer may also read this gate record, its sidecar, the review brief, and its sidecar as CONTROL instructions. These do not expand the substantive allowlist.

## Isolation and prohibition

The reviewer must not:

- inherit a designer, fixture author, executor, or earlier reviewer conversation;
- search the repository or inspect Git history;
- read sealed staging, source-authoring material, the held source candidate, an oracle, scoring instances, public fixture material, implementation, executor material, or another review;
- use outside sources or browse the web;
- modify or create files;
- propose question-specific expected answers;
- claim implementation, validation, sealed compatibility, or S0 results.

The reviewer may perform local, non-writing arithmetic or statistical calculations needed to verify claims in the allowed documents.

## Authorized result

The reviewer returns one complete review in its response. CONTROL may record that response verbatim in the approved review output path and create a SHA-256 sidecar. The reviewer itself makes no writes.

The review selects a design status only. It cannot authorize public bank creation, schemas, code, runs, sealed revision, executors, or S0.
