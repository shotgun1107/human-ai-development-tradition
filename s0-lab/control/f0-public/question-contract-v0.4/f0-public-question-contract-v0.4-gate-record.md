# F0-PUBLIC question contract v0.4 design gate record

- opened_at: `2026-08-07` (KST)
- opening_signal: `F0-PUBLIC QUESTION CONTRACT V0.4 DESIGN OPEN`
- opening_role: `USER`
- control_role: `CONTROL`
- status: `OPEN FOR PUBLIC DESIGN ONLY`

## Authorized purpose

Design a public, condition-neutral successor response contract for S0 questions. The design must remove question-specific answer shapes, reduce the 96-combination ambiguity of Track V, define deterministic observation rules, and precommit a public-only falsification plan.

This gate may create normative Markdown specifications, abstract serialization examples that do not assert a correct answer, analytic resource bounds, review criteria, and a CONTROL design assessment.

## Maximum input allowlist

| SHA-256 | Path | Role |
|---|---|---|
| `07b023666957b357c35ebc9b0da877df615d483064f7c34e85002dded5ad4ca6` | `AGENTS.md` | current repository instructions |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` | frozen predecessor protocol |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` | frozen predecessor answer format |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` | frozen predecessor question format |
| `5f55208f5b0a2c41d0b723cdf92aa53ce3b77a700fa424da3d5b434dd08bd032` | `s0-lab/control/f0-sealed/question-design/proposals/structured-response-v0.1.md` | selected Track V proposal |
| `4d62506c941c2695eb7861db825a58f4814637ffa846dd27e792b17177f29795` | `s0-lab/reviews/f0-sealed/question-design/f0-sealed-question-design-comparative-review-v0.1.md` | independent comparative findings |
| `7230ac449d06a4eb4ea74887d1bf163bb3e6ed9808077f27e7d1e19dff154703` | `s0-lab/control/f0-sealed/question-design/f0-sealed-question-design-decision-v0.1.md` | predecessor CONTROL decision and conditions |

An allowlist is a maximum. The sealed source candidate, source-authoring records, oracle material, scoring instances, condition packages, executor material, project history, and unrelated repository content remain closed.

## Authorized outputs

Only the following design package may be added under this gate:

1. this gate record and SHA-256 sidecar;
2. `universal-response-contract-v0.4-candidate.md` and sidecar;
3. `public-falsification-plan-v0.1.md` and sidecar;
4. `control-design-assessment-v0.1.md` and sidecar.

The candidate files are proposals, not frozen protocol or schema artifacts.

## Explicitly closed work

This gate does not authorize:

- reading or modifying sealed staging;
- creating or revising questions, source records, fixtures, answers, rationales, an oracle, or scoring instances;
- editing protocol v0.3, SM0, SM1, or any other frozen file;
- creating executable JSON Schema, validators, comparators, runners, packages, or other implementation code;
- conducting the public tests, launching executors, judging S0, or running S0;
- using real, customer, personal, secret, brand, competition, outsourced, or past-project content;
- claiming public validation, sealed usability, S0 implementation, or broader-system effects;
- committing or pushing without the approval procedure in `AGENTS.md`.

## Exit rule

CONTROL may close this design gate after the candidate contract and falsification plan are internally checked against every predecessor condition. Independent review remains mandatory before the candidate can be frozen or used to authorize public fixture creation. A self-assessment is not independent review.
