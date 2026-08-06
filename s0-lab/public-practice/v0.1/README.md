# F0-PUBLIC practice bundle v0.1

This directory is a fully public, fictional practice fixture for checking how the frozen S0 protocol and the eleven SM0/SM1 JSON formats connect. It is not sealed F0 material, a hidden oracle, an S0 run, a score, or evidence that any central system, Project Brain integration, safety property, economic benefit, or model transfer works.

## Contents and use

- `blocks/` contains two synthetic canonical corpora, fact manifests, public question/option manifests, public oracles, public scoring examples, and public fixture/transformation manifests.
- `packages/` contains the eight expected public input expressions: P01-P04 for each practice block.
- `runner/` contains public runner projections and four equal-opportunity practice instructions.
- `manifests/` contains public-practice instances of the remaining SM0/SM1 formats.
- `examples/answer.json` is the expected neutral answer for the first practice block.
- `artifacts/`, `control/`, `judge/`, and `reports/` contain schema-example placeholders or public projections needed to make references inspectable. They exist only to satisfy and demonstrate document shape. Their presence, hash, schema constant, or affirmative example field is not operational evidence of an implementation, execution, isolation boundary, release control, review, or validation result.
- `validation-report.md` records static checks and limitations. `bundle-files.sha256` fixes every final bundle file except itself.

To inspect the practice bundle, parse each JSON file as UTF-8, validate the eleven mapped instances listed in `validation-report.md` against the frozen schemas, recompute referenced SHA-256 values, compare every package's fact/record/text set, and check each block's largest byte excess against its smallest package. Do not treat the public expected answer as an executor result.

## Data and evidence boundary

Every name, project, task, sentence, identifier, timestamp, answer position, and relationship in this directory was invented for this practice bundle. No customer, personal, secret, real-project, past-project, brand, competition, or contract data was used. The public oracle and public scoring files are visible practice data only and are not hidden answers.

The names, wording, ordering, option placement, answers, P03 marker-role topology, P04 relation-code topology and relation ordering, and record-role ordering across each event sequence are reserved against reuse in any future sealed block. A future sealed block must not copy or lightly rename those public structures. Public-practice results must never enter S0 structural scoring. Any later change prompted by this bundle requires a new frozen hash before a separately authorized activity.

## Reproducible aggregate hashes

The aggregation algorithm is `public-practice-aggregate-v1`:

1. Decode each JSON `text` value. Hash its exact Unicode string as UTF-8 without BOM; do not trim it, normalize Unicode, or rewrite line endings. Publish the lowercase hexadecimal result as `normalized_text_sha256`.
2. For `fact_set_sha256`, take every raw `fact_id`, sort ascending by Unicode code point, serialize the sorted IDs separated by exactly one LF byte (`0x0a`), add no trailing LF, encode as UTF-8 without BOM, and SHA-256 hash those bytes.
3. For `record_content_set_sha256`, serialize each fact as raw `record_id`, exactly one TAB byte (`0x09`), then its 64-character lowercase `normalized_text_sha256`. Sort these complete serialized lines ascending by Unicode code point, join them with exactly one LF byte (`0x0a`), add no trailing LF, encode as UTF-8 without BOM, and SHA-256 hash those bytes.

All identifiers and hashes in these aggregates are ASCII, so Unicode code-point ordering is independently reproducible as bytewise ascending order here. The published block values are checked in `validation-report.md`.

## Condition-neutral labels

The only public expression labels are P01, P02, P03, and P04. They identify different presentations of the same facts and questions; they do not state a rank or preferred structure. Each P01-P04 package for a block preserves the identical `fact_id`, `record_id`, project boundary, timestamp, and fact text set.

## Status

This is author-produced schema-practice candidate material. Even a schema-valid JSON example is not an operational manifest or evidence that its assertions occurred. It is not complete until CONTROL performs the separately required independent review. No executor session may be forked from or reuse this authoring session.
