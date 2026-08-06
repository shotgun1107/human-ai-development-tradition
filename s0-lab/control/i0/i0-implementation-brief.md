# I0 minimum implementation brief

## 1. Role and boundary

The fresh I0 implementation builder owns only the minimum public-development harness. It is not a fixture author, executor A–D, pre-review judge, post-run judge, or central-system developer. This session must never be reused or forked into an executor session.

The implementation may prove only that the frozen public formats can be loaded, transformed, validated, and checked deterministically. It cannot prove system effectiveness, operational isolation, economic value, or model-to-model transfer.

## 2. Frozen allowed inputs

The allowlist is a hard maximum. Verify every controlling SHA-256 before reading substantive content. On any mismatch, write nothing and stop.

| SHA-256 | Path |
|---|---|
| `14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2` | `AGENTS.md` |
| `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | `s0-lab/control/s0-protocol-v0.3.md` |
| `3f8e3ef230d7cad298ac555e045d8e9b5755ea82e8f33154d1685d8b526f8a6c` | `s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md` |
| `993f44896184617035609f117060c3a16d36bd44a7284178de3c5dd0ea6ec47f` | `s0-lab/public-practice/v0.1/bundle-files.sha256` |
| `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` | `s0-lab/control/sm0/answer.schema.json` |
| `a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a` | `s0-lab/control/sm0/common-manifest.schema.json` |
| `a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a` | `s0-lab/control/sm0/condition-overlay-manifest.schema.json` |
| `846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80` | `s0-lab/control/sm0/fixture-manifest.schema.json` |
| `5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0` | `s0-lab/control/sm1/question-options.schema.json` |
| `8e233cbd678c8319da1b192ddec80ac0907444d7c05802a7c110b6bf35a9d346` | `s0-lab/control/sm1/transformation-manifest.schema.json` |
| `675222967cebc312e8fe79bc45763254bd232e3f2325df6d1a4463e7d1d0066c` | `s0-lab/control/sm1/neutral-answer-validation.schema.json` |
| `3e27d1bcdb253a9065443d1d9244889dfad753c63512d89178c7ca93dee3ef4b` | `s0-lab/control/sm1/access-manifest.schema.json` |
| `ef773dcc5bc17e6924aafc6c6ab01f080e8793a6ab91c5cbf44654105e5e9f84` | `s0-lab/control/sm1/run-manifest.schema.json` |
| `2d4e3464c01ca9c220df7344cfdf76bb05021d9d4eec484007c2e21c80af082e` | `s0-lab/control/sm1/scoring.schema.json` |
| `b936fcd86a270f57d81b959682cd72a40e22a35e49013a5ee2f6a3b4c89fa23e` | `s0-lab/control/sm1/pre-review-record.schema.json` |

After verifying the public bundle manifest, the builder may read only its 90 listed files. Do not search or inspect any other repository file. The two I0 control files in `s0-lab/control/i0/` are also allowed but builder-owned output excludes them.

## 3. Runtime and dependency

- Python: `3.12.10`
- Validator: `jsonschema[format]==4.26.0`
- Use `Draft202012Validator`, schema self-checking, and an explicitly enabled `FormatChecker`.
- The dependency is installed by CONTROL into a temporary external virtual environment. The builder must not access the network or install additional packages.
- Use Python standard library `unittest`; do not add pytest or other dependencies.

## 4. Allowed output

Write only below `s0-lab/i0/`, excluding `s0-lab/control/i0/`.

Required layout, unless a smaller equivalent is clearly justified:

```text
s0-lab/i0/
  README.md
  requirements.txt
  implementation/
    ... minimum Python package ...
  tests/
    ... unittest suite ...
  verification/
    verification-report.md
    implementation-files.sha256
```

Do not modify frozen inputs, `.codex/`, root documentation, git configuration, or any other path. Do not commit, push, create a branch, or add a worktree.

## 5. Required implementation

### A. Frozen bundle integrity

- verify the self-excluding 90-entry bundle manifest, file-set equality, path safety, and SHA-256 values;
- parse every public JSON file as UTF-8;
- reproduce `fact_set_sha256` and `record_content_set_sha256` using the published algorithm;
- reproduce package byte counts and enforce the 15% ceiling.

### B. Draft 2020-12 validation

- validate all 11 frozen schemas themselves;
- validate the 11 designated public instances listed in `validation-report.md`;
- enable format assertion explicitly;
- return stable, sorted, machine-readable validation errors without absolute host paths.

### C. Deterministic public transformation

- accept only one public canonical input plus one opaque profile `P01`–`P04`;
- never accept oracle or scoring input;
- generate the corresponding package deterministically without reading another block or expected output during transformation;
- preserve exact fact, record, project, timestamp, and text content;
- produce package bytes whose SHA-256 exactly matches all eight frozen public package files;
- a second identical invocation must be byte-identical.

### D. Neutral answer validation

- validate `answer.schema.json` first;
- enforce exactly one sorted answer per public question;
- enforce allowed decision IDs and cited/affected-record policies from the public question projection;
- reject missing, duplicate, extra, invalid, unsorted, or forbidden-disclosure answers;
- report protocol error categories without consulting public oracle/scoring for ordinary answer-format validation.

### E. CLI and integrity record

Provide the smallest local CLI needed to run the four functions. Commands must use workspace-relative paths, reject `..` and absolute paths, avoid network access, and return nonzero on failure. Verification output records input/output hashes, bytes, validator/runtime versions, start/end times, and errors. It is a technical test record, not an S0 run record or cost claim.

## 6. Required tests

At minimum test:

1. all frozen input hashes before use;
2. all 11 schema instances with Draft 2020-12 + format checking;
3. bundle file-set/hash/JSON/aggregate/byte integrity;
4. exact eight-package regeneration and two-run determinism;
5. fact equality across P01–P04 for both blocks;
6. valid public answers for both blocks;
7. negative answers: missing, duplicate, extra, invalid option, bad citations, bad affected IDs, unsorted IDs, forbidden disclosure;
8. absolute/traversal path rejection;
9. transform API/CLI has no oracle or scoring input;
10. stable sorted error output and nonzero CLI failure exits.

## 7. Prohibited implementation

- no AI/model call, executor launch, agent orchestration, hidden oracle, sealed fixture, scoring of S0 outcomes, or condition-to-A–D restoration;
- no database, RAG, vector store, UI, web server, network service, Project Brain integration, plugin, telemetry service, or real-data adapter;
- no auto-repair of frozen inputs and no rewriting files to make a test pass;
- no claim beyond public-development format correctness.

## 8. Completion report

Report created files, exact commands, test counts, failures, dependency/runtime versions, implementation manifest hash, and honest unchecked scope. CONTROL and an independent reviewer must approve the candidate before I0 is considered frozen or usable for sealed F0.
