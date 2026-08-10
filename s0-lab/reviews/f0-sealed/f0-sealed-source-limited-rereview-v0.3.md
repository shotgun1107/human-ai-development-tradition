# F0-SEALED source revision 3 final wording-level rereview v0.3

- rereview_role: fresh read-only `s0_protocol_reviewer`
- reviewed_candidate: revision 3
- decision_scope: source-authoring decision only

## Input authentication

**PASS**. The brief and four prerequisite sidecar pairs matched, the frozen
schema matched its freeze record, and the candidate ledger was safe, unique,
self-excluding, and matched all ten file hashes.

## FSR-M-02

**Unresolved — Major.** Several evidence-status, untrusted-data, withdrawal,
responsibility, and unchanged-state option sets still contain one choice that
uniquely embodies or closely echoes the decisive source qualification. Likely
selections remain recoverable from source wording despite bounded
alternatives.

Evidence locations:

- `blocks/*/runner-question-options.json:questions[*].options[*].runner_text`
- `blocks/*/canonical-input.json:records[*]`

## Regression check

**PASS.** The rereviewer confirmed:

- FSR-M-01 material block independence
- exact source counts
- 13/13 direct mappings and body hashes per block
- explicit source support
- synthetic and prohibited-material boundaries
- runner-projection equality and hashes
- no runner-visible condition, evaluation, scoring, or D-favoring cue
- honest remaining limits

No reviewed evidence indicated a post-result threshold change.

## Findings

- Critical: 0
- Major: 1 (`FSR-M-02`)
- Minor: 0

## Verdict

`revision 3 requires question-design change before CONTROL decision`

The wording-level stop rule is now active. Additional cosmetic revisions are
not authorized by this review path.

## Remaining unverified limits

- independent Draft 2020-12 engine validation as part of the rereviewer role
- direct cross-revision source-hash comparison by the rereviewer
- actual A-D equality of source information, authority, model/reasoning
  conditions, time, limits, and scoring opportunities
- transformation equivalence and byte ceiling
- oracle/scoring/provenance
- formal pre-run approval, executor isolation, judging, and S0
- broader system, safety, economic, or transfer conclusions

