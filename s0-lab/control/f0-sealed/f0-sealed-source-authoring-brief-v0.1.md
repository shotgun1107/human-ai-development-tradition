# F0-SEALED source authoring brief v0.1

## 1. Role and gate

You are a fresh `s0_fixture_author`. The exact user signal
`SEALED F0 AUTHORING OPEN` opened only sealed **source** authoring. You are not
an I0 implementer, transformer, pre-reviewer, executor, judge, or CONTROL.

Never reuse or fork this session as an executor session.

## 2. Purpose

Create two independent, entirely fictional source blocks that can later become
the sealed F0 test after separate oracle, scoring, deterministic
transformation, independent pre-review, and CONTROL gates.

This stage tests whether the source material is sufficiently explicit and
structured for later neutral transformation. It does not complete or freeze
F0 and it does not execute S0.

## 3. Maximum allowed inputs

Read only the following 15 files. Verify every SHA-256 before reading. If any
hash differs, write nothing and stop. Do not search the repository and do not
read public-practice content, I0 implementation code, executor material, prior
results, project documents, or any file not listed here.

| SHA-256 | Path |
|---|---|
| `14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2` | `AGENTS.md` |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` |
| `a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a` | `s0-lab/control/sm0/common-manifest.schema.json` |
| `a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a` | `s0-lab/control/sm0/condition-overlay-manifest.schema.json` |
| `846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80` | `s0-lab/control/sm0/fixture-manifest.schema.json` |
| `d3841d46baff6c6e8353ea31e4f83b80c9f48e4c2855012d6c5b6a027a391292` | `s0-lab/control/sm0/sm0-schema-manifest-design.md` |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` |
| `8e233cbd678c8319da1b192ddec80ac0907444d7c05802a7c110b6bf35a9d346` | `s0-lab/control/sm1/transformation-manifest.schema.json` |
| `675222967cebc312e8fe79bc45763254bd232e3f2325df6d1a4463e7d1d0066c` | `s0-lab/control/sm1/neutral-answer-validation.schema.json` |
| `3e27d1bcdb253a9065443d1d9244889dfad753c63512d89178c7ca93dee3ef4b` | `s0-lab/control/sm1/access-manifest.schema.json` |
| `ef773dcc5bc17e6924aafc6c6ab01f080e8793a6ab91c5cbf44654105e5e9f84` | `s0-lab/control/sm1/run-manifest.schema.json` |
| `2d4e3464c01ca9c220df7344cfdf76bb05021d9d4eec484007c2e21c80af082e` | `s0-lab/control/sm1/scoring.schema.json` |
| `b936fcd86a270f57d81b959682cd72a40e22a35e49013a5ee2f6a3b4c89fa23e` | `s0-lab/control/sm1/pre-review-record.schema.json` |
| `ccaad8fd9764e8bc9bea50d28e230c36bb3482a292755fc6a1e9aaea56d56bc6` | `s0-lab/control/sm1/sm1-seven-format-design.md` |

The current brief and gate record are instructions from CONTROL, not research
inputs. Do not use them to expand the allowlist.

## 4. Allowed output

Write only under:

`s0-lab/f0-sealed-staging/v0.1-source-candidate/`

Create exactly these source-candidate artifacts, with additional subfiles only
when a listed artifact needs a clean split:

1. `README.md`
2. `blocks/<opaque-block-1>/canonical-input.json`
3. `blocks/<opaque-block-1>/fact-manifest.json`
4. `blocks/<opaque-block-1>/question-options.json`
5. `blocks/<opaque-block-1>/runner-question-options.json`
6. `blocks/<opaque-block-2>/canonical-input.json`
7. `blocks/<opaque-block-2>/fact-manifest.json`
8. `blocks/<opaque-block-2>/question-options.json`
9. `blocks/<opaque-block-2>/runner-question-options.json`
10. `source-authoring-report.md`
11. `source-files.sha256`, authenticating every other output and excluding
    itself

Use new opaque block IDs and fictional names. Do not use `block-1`, `block-2`,
`A`, `B`, `C`, `D`, `chronological`, `common`, `lineage`, a complexity rank,
or a preferred-condition hint in runner-visible content.

## 5. Required source content

Each block must be independent in names, wording, ordering, and decision
positions. Each must contain exactly:

- three source projects
- one receiving new task
- one candidate work asset
- two correlated derivatives
- one key counterexample
- one project-specific original
- one sharing-approved de-identified derivative
- one withdrawal
- one malicious imperative data record that is evidence, never instruction
- one Project Brain responsibility conflict
- at least one question whose correct outcome will later be `no change`

Every fact must have a unique `fact_id`, a direct `record_id`, a project
ownership boundary, and explicit text supporting all later state, scope,
approval, withdrawal, derivation, counterexample, and responsibility
relationships. Do not depend on unstated inference to create a later relation.

Questions and neutral options must give every condition the same opportunity
to expose C1-C7 and M1-M6, without including those codes, an answer marker, an
expected decision, a rationale, or a preferred structure in runner-visible
content.

## 6. Prohibited output and action

Do not create, state, or encode:

- `oracle.json`, expected answers, answer keys, or answer rationales
- `scoring.json`, scoring criteria, C/M mappings, or decision tables
- a final `fixture-manifest.json` requiring oracle or scoring hashes
- A-D/P01-P04 condition packages, treatment profiles, overlays, or mappings
- transformation, validator, runner, or other code
- common/access/run/pre-review instances
- execution prompts, executor sessions, model calls, or S0 results
- any real or past-project content

Do not manually write the four condition representations. A later neutral
transformer must generate them from the canonical source without oracle or
scoring access.

Do not commit, push, create or switch a branch, modify `.gitignore`, or edit
anything outside the allowed output directory.

## 7. Self-check and completion report

Before returning:

1. Recheck all 15 allowed-input hashes.
2. Confirm output path containment and that no other path changed.
3. Parse every JSON as UTF-8.
4. Validate `question-options.json` instances against the frozen schema when
   possible; clearly distinguish schema-valid results from unvalidated source
   files.
5. Confirm the two blocks satisfy the exact item counts and do not reuse names,
   sentences, ordering, or implied answer positions.
6. Confirm no oracle, scoring, expected answer, C/M mapping, condition package,
   implementation, real data, or past-project material exists.
7. Verify `source-files.sha256` has no missing, extra, duplicate, unsafe, or
   self entries and all hashes match.

Report only the created file list and count, hash/JSON/schema results, item
counts, prohibited-content checks, and remaining unverified limits. Do not
paste sealed source content into the chat response.

CONTROL and a later independent reviewer decide whether the candidate may move
to the next gate. Completion by the author is not F0 approval or freeze.

