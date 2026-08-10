# F0-SEALED question-design competition brief v0.1

## 1. Purpose

Design a replacement for question-specific multiple-choice distractors that
keeps S0 answers objectively comparable while preventing option wording from
revealing the likely decision.

The design must continue measuring whether four representations of the same
facts change AI decision quality. It must not reward recognition of a nuanced
option, preferred structure vocabulary, or a sentence copied from source
records.

## 2. Maximum allowed inputs

Read only the following files after verifying each listed SHA-256. Do not
search the repository or read sealed staging, public-practice content, I0 code,
project history, executor material, or any other file.

| SHA-256 | Path |
|---|---|
| `14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2` | `AGENTS.md` |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` |
| `d3841d46baff6c6e8353ea31e4f83b80c9f48e4c2855012d6c5b6a027a391292` | `s0-lab/control/sm0/sm0-schema-manifest-design.md` |
| `db29efe079e7b6548b7afb6380cb548997a061da84009c235dfd5be220a5f033` | `s0-lab/control/sm0/sm0-freeze-record.md` |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` |
| `ccaad8fd9764e8bc9bea50d28e230c36bb3482a292755fc6a1e9aaea56d56bc6` | `s0-lab/control/sm1/sm1-seven-format-design.md` |
| `cdbd9dc560da7a41dfc57ec885def730edcdc7718f483f23c60d6868ddef5d00` | `s0-lab/control/sm1/sm1-freeze-record.md` |
| `9ba05453ea76c951903c6b4cf59eb03009204c98fecf32e3481c51a57c8662c7` | `s0-lab/control/f0-sealed/f0-sealed-source-authoring-decision-v0.1.md` |
| `fcbd8f1ab583e6d6e5d4c4188049dfe35a0b06674ba202882cefc7ac41fc82fb` | `s0-lab/reviews/f0-sealed/f0-sealed-source-limited-rereview-v0.3.md` |

The current gate record and this brief are CONTROL instructions and do not
expand the research allowlist.

## 3. Independent tracks

CONTROL assigns one track per fresh designer.

### Track M — minimal change

Prefer a shared, precommitted decision vocabulary and the smallest compatible
change to the frozen answer/question contracts. Preserve deterministic scoring
and current citation, affected-ID, uncertainty, and short-reason fields.

### Track V — measurement validity

Prioritize eliminating answer-shape cues even if a new structured-response
contract or protocol/schema version is required. Avoid unrestricted prose that
makes judging subjective.

Neither track may read the other proposal before completing its own.

## 4. Mandatory requirements

Every proposal must:

1. define exactly what the executor sees and writes
2. prevent question-specific tailored distractors
3. precommit any action vocabulary before sealed-source access
4. retain record citations, affected scope, uncertainty, and concise reason
5. avoid condition identity, representation vocabulary, target preference,
   risk codes, scoring roles, or answer markers in runner-visible material
6. make correct and incorrect outputs deterministically distinguishable enough
   for an independent judge
7. distinguish semantic decision errors from JSON/format errors
8. explain how the same contract applies across both blocks and all four
   conditions
9. state exact required changes to protocol v0.3, answer schema, and
   question-options schema, including when no change is needed
10. include an abstract worked example that contains no sealed/public fixture
    content and does not mark the expected answer
11. define public-only falsification tests for answer leakage, scoring
    reliability, inter-reviewer agreement, and executor burden
12. define rejection criteria and a rollback path
13. separate verified facts, design inferences, and proposals
14. state all unverified limits and prohibited claims

## 5. Comparative criteria

The later reviewer scores each proposal out of 100:

| Criterion | Points |
|---|---:|
| answer-shape leakage resistance | 25 |
| decision validity and coverage | 20 |
| deterministic scoring and reviewer agreement | 20 |
| fairness across A-D and two blocks | 15 |
| compatibility and migration risk | 10 |
| executor burden and operating cost | 5 |
| falsifiability and rollback clarity | 5 |

Noncompensatory failures:

- tailored question-specific distractors remain
- correct output depends on condition-specific vocabulary
- sealed or oracle access is required to define the answer contract
- judge must freely reinterpret unrestricted prose without a precommitted rule
- one condition receives more decision information or opportunity
- the proposal claims S0, central-system, operational, economic, safety, or
  transfer validation

## 6. Output contract

Write only the one proposal path assigned by CONTROL and its `.sha256`
sidecar. Do not edit any other path.

Required sections:

1. outcome summary
2. facts / inferences / proposal boundary
3. runner-visible contract
4. judge-visible contract
5. schema and protocol delta
6. abstract example
7. leakage and fairness analysis
8. public-only validation plan
9. migration and rollback
10. failure modes and unverified limits
11. recommendation

Do not implement code, create fixtures, edit frozen files, commit, push, or
create a branch. Proposal completion is not design approval.

