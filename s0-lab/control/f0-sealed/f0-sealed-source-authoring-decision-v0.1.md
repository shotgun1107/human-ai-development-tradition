# F0-SEALED source authoring decision v0.1

- decided_at: `2026-08-07` (KST)
- decision_role: `CONTROL`
- user_gate: `SEALED F0 AUTHORING OPEN`
- candidate: `s0-lab/f0-sealed-staging/v0.1-source-candidate/`

## Decision

- limited source-authoring activity: **COMPLETED WITH HOLD**
- sealed source candidate approval/freeze: **NOT APPROVED**
- required next design action: **QUESTION-DESIGN CHANGE**
- additional wording-level revision under the current design: **STOPPED**

The two synthetic source blocks and their fact structure are mechanically
sound enough to preserve as a design candidate, but the runner-visible
multiple-choice design is not acceptable for a source-authoring approval.

This is not complete F0, a sealed fixture freeze, pre-run approval, or an S0
result.

## Authenticated candidate

| Artifact | SHA-256 |
|---|---|
| `source-files.sha256` | `0bfeeeb9fd76624412e370fc652aa509086774132c85f0914ac2d1d0a1c421a9` |
| `source-authoring-report.md` | `5affb047f7f4836f137a45963e115a6f6d14cc62c0284b00ab79360c2c78c91f` |

The self-excluding source ledger authenticates exactly ten non-self files.
CONTROL independently reproduced:

- exact file set and ledger: 10/10, no missing, extra, duplicate, unsafe, self,
  or mismatched entry
- UTF-8 JSON and duplicate-key parsing: 8/8
- frozen Draft 2020-12 question schema: 2/2, zero errors, using Python 3.12.10
  and `jsonschema 4.26.0`
- runner projection structural equality and projection hashes: 2/2
- maximum within-question option-length ratio after revision 3: 1.172

## Review sequence

| Review | Result | SHA-256 |
|---|---|---|
| initial source limited review | Major 2; revision required | `6ca38399c2f7594443bb99912210cc79cbdc676bec292c504a842b9788ea2a47` |
| revision 1 limited rereview | FSR-M-01 resolved; FSR-M-02 Major | `49b986338f42b9ab8d40ed92f53e6a7f11cf8391085e8723e73efe3fc38fdcd4` |
| revision 2 limited rereview | FSR-M-02 Major | `38c2866d240cbe2214c6a31e534003b9c843d21c53c94a96bb575e74b24ee494` |
| revision 3 final wording-level rereview | FSR-M-02 Major; design change required | `fcbd8f1ab583e6d6e5d4c4188049dfe35a0b06674ba202882cefc7ac41fc82fb` |

Fresh read-only reviewers confirmed the following as passed after revision:

- material independence of the two blocks
- protocol §4.1 source counts and direct fact mappings
- explicit relationship support and synthetic-data boundary
- absence of oracle, answer, scoring, package, implementation, execution, and
  judge material
- absence of runner-visible condition, evaluation, scoring, structure-rank,
  or D-favoring vocabulary
- honest remaining limits

The remaining Major finding is `FSR-M-02`: some choices still uniquely embody
or echo the decisive source qualification, so likely selections can be
recovered from answer shape rather than requiring the intended comparison of
representations.

## Stop rule and next gate

Three wording-level revisions did not resolve the same Major condition. More
paraphrasing is likely to overfit the reviewer while leaving the design problem
intact. CONTROL therefore stops the current authoring loop.

The next work must redesign how neutral decisions are presented—for example,
using a shared decision vocabulary or another precommitted option-generation
method—then receive independent review before the source candidate is revised
again.

A suggested future authorization signal is:

`F0-SEALED QUESTION DESIGN REOPEN`

This record does not open that gate.

## Still closed

- hidden oracle and expected answers
- scoring content
- final fixture manifests
- deterministic sealed transformation and A-D packages
- condition mapping and executor-facing material
- formal pre-run review
- executor A-D, judge, S0 execution, and scoring
- central-system, Project Brain, operational, economic, safety, or transfer
  conclusions

The source candidate remains staging material. It must not be committed,
pushed, published, or provided to an executor while this HOLD remains.

