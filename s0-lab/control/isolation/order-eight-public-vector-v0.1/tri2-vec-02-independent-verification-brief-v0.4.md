# TRI2-VEC-02 independent verification brief v0.4

- `status`: public review-control revision candidate
- `review_kind`: fresh public mathematical and design verification
- `current_gate`: boundary revision only; independent review not yet open
- `target_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `maximum_claim`: CONTROL final-freeze consideration only
- `supersedes_after_freeze`: `tri2-vec-02-independent-verification-brief-v0.3.md`

## 1. Reviewer independence

The reviewer must be a fresh session that did not author, advise on, calculate,
or QA the candidate, derivation, any boundary revision, any predecessor review,
or this brief. It must not inherit an author/reviewer conversation and must not
use a subagent. Worktree separation is edit isolation, not secret or
independent information security.

All predecessor boundaries, briefs, and invalid reviews are excluded from the
review input set. They remain historical records but cannot be used as source
authority, transport diagnostics, an answer key, a waiver, or evidence about a
candidate row. Agreement with author arithmetic, candidate prose, copied
labels, library classifications, or reviewer memory is not evidence.

## 2. Maximum public input set

CONTROL must provide exact relative paths and SHA-256 values outside this brief
for exactly this maximum set:

1. repository-root `AGENTS.md` at the candidate commit;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. the canonical public protocol r1 Markdown and sidecar;
4. the v0.2 trust-root/role-isolation design revision and sidecar containing
   the frozen `S0-ED25519-STRICT-1` profile;
5. the v0.4 trust-root/role-isolation design revision, identity-authority
   matrix addendum, acceptance-plan addendum, independent review, and CONTROL
   integration decision, each with its sidecar;
6. `tri2-vec-02-order-eight-public-vectors-v0.1.md` and sidecar;
7. `tri2-vec-02-public-derivation-v0.1.md` and sidecar;
8. `tri2-vec-02-review-input-boundary-revision-v0.3.md` and sidecar; and
9. this v0.4 brief and its sidecar.

This is 24 files: two file-specific inputs and eleven Markdown/sidecar pairs.
All earlier boundaries, briefs, invalid reviews, and unlisted repository files
are excluded. No broad repository search, sealed material, private key,
implementation source, fixture, oracle, provider/model output, E0 material, S0
material, advisory output, or unlisted source is allowed.

Authenticate every supplied file before relying on it. A mismatch, missing or
duplicate input, ambiguous or reused path, stale procedural authority, extra
input, or canonical-validation failure yields `INVALID-REVIEW` rather than a
candidate finding.

## 3. Exact Git and write boundary

CONTROL must freeze and supply the exact candidate branch, commit, tree, sole
parent, parent tree, and parent-to-candidate diff. Initial status must be clean.
The candidate commit must add only these four files under the existing control
directory:

- this v0.4 brief and sidecar; and
- `tri2-vec-02-review-input-boundary-revision-v0.3.md` and sidecar.

Every predecessor artifact must remain byte-identical. The reviewer may write
exactly:

- `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.4.md`;
  and
- its same-basename `.sha256` sidecar.

No candidate input, implementation file, other directory, Git index, branch,
commit, remote, or `main` state may be changed.

## 4. Ordered integrity and read procedure

Before substantive review, the reviewer must:

1. verify Git identity, sole parent, exact four-added-path diff, and clean
   status;
2. hash all 24 supplied paths before reading any and establish manifest,
   resolved-path, and tracked-index uniqueness;
3. read `AGENTS.md`, this brief, and the v0.3 boundary completely;
4. run the authenticated canonical validator SelfTest and require every case
   to pass;
5. validate exactly the eleven admitted Markdown/sidecar pairs; and
6. distinguish byte identity, canonical format, checker preflight, source
   transport, role boundary, and substantive failures.

It may then build and retry an ephemeral transport checker against synthetic
bytes only until every v0.3-boundary section-6 preflight case passes. It may
then read only the admitted non-author protocol, strict-profile, and v0.4
authority documents. The live RFC pipeline and independent precomputation must
finish before the candidate vector or author derivation is opened.

After writing, validate the review pair, rehash all 24 inputs, confirm Git
identity is unchanged, and require status to contain exactly the two authorized
untracked v0.4 review outputs.

## 5. One-shot official RFC boundary

The sole source is:

`https://www.rfc-editor.org/rfc/rfc8032.txt`

After synthetic preflight passes, make exactly one direct in-memory request.
Do not use search, browser, HTML, rendered text, clipboard, cache, mirror,
local copy, or alternate source. Require one exact raw profile:

```text
RFC8032-WIRE-LF-1
length = 103210
sha256 = ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3
line_endings = 3363 LF, zero CR

RFC8032-WIRE-CRLF-1
length = 106573
sha256 = f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9
line_endings = 3363 CRLF, zero bare LF, zero bare CR
```

Require HTTP success, redirects disabled with exact final URL, `text/plain`,
ASCII-only bytes, no UTF-8 BOM, and no NUL. Leave LF unchanged or replace each
exact CRLF pair with one LF. No other transformation is allowed. Require:

```text
RFC8032-CANONICAL-LF-1
length = 103210
sha256 = ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3
line_endings = 3363 LF, zero CR

PARAMETER-1 = [19245:22067]
length = 2822
sha256 = a2ee2379339d2d9e81fc04d92411347edd7da98bbf2fb92983f299f4dddd7b08

ENCODING-ADDITION-1 = [22915:27092]
length = 4177
sha256 = 5e87337157810b1420fa543727fb74dbdecc7510b004a1100d9a58bcd7bc916d
```

Execute every exact byte row in v0.3-boundary section 5. Marker hex, slice,
offset, byte length, and occurrence count are all mandatory. Use an exact
byte-subsequence counter, not regex, wildcard, text search, decoded formulas,
line matching, or reviewer-selected markers.

Before source-text output, emit only bounded metadata: chosen profile ID,
lengths, hashes, marker IDs, offsets, lengths, counts, and pass/fail. If and
only if every assertion passes, emit the two slices and no full body, gap,
adjacent section, or other RFC bytes.

After the live request begins, any URL, response, media, ASCII, BOM, NUL,
profile, canonical, slice, marker, exclusion, diagnostic, or output-boundary
failure is terminal `INVALID-REVIEW`. Do not correct, retry, use a second
request, fall back, waive, or ask the author to repair the live review.

## 6. Independent precomputation before candidate read

Using only admitted non-author authority and the two emitted official slices,
independently freeze in session-local notes:

1. numeric `p`, `d`, `L`, and identity `I`;
2. the Ed25519 curve, canonical encode/decode, and complete addition rules;
3. the derivation from exact order eight to
   `d*y^4 + 2*y^2 - 1 = 0 mod p`;
4. every quadratic and square-root branch, including nonsquare rejection;
5. every field-valid x/y coordinate, x parity, and exact 32-byte encoding;
6. the intended `P != I`, `[4]`, `[8]`, `[L]`, and pairwise-distinction checks;
   and
7. the exact strict-profile rejection points for use as `A` and `R`.

Only after recording all results may the reviewer open the candidate and
author derivation. Compare exact row bytes and then perform the complete
hostile review. Author documents cannot repair a missing precomputed value.

Ephemeral public arithmetic is allowed. A reusable generator, cryptographic
helper, production verifier, key, signature, fixture, oracle, or implementation
file is forbidden.

## 7. Noncompensatory row criteria

Each of exactly four rows passes only if all criteria pass independently:

1. independent derivation produces the exact literal;
2. the literal is exactly 32 bytes and canonical decode succeeds;
3. canonical re-encoding is byte-identical;
4. `P != I`;
5. `[8]P = I`;
6. `[4]P != I`;
7. `[L]P != I`;
8. strict validation rejects it as `A` at the exact required predicate;
9. strict validation rejects it as `R` at the exact required predicate; and
10. the result is bound to exact row bytes, not a coordinate label.

One missing, ambiguous, inconsistent, or failed criterion fails the row. One
failed row fails the package. Extra, missing, or duplicate rows fail the
package. No substitution, waiver, retry, vote, aggregate score, or provider
fallback is allowed.

## 8. Mandatory hostile checks

At minimum, trace and reject or correctly classify:

- a checker used without all synthetic preflight cases passing;
- regex/wildcard/casefold/line matching used instead of exact marker bytes;
- marker hex decoded incorrectly, checked at the wrong offset, or accepted
  with the wrong length or occurrence count;
- either raw profile accepted without its complete hash and line shape;
- mixed endings, a third raw representation, or normalization beyond exact
  CRLF-to-LF conversion;
- slicing before canonical full-body validation or emitting extra RFC bytes;
- any changed bit, nibble, byte, sign bit, byte order, or field endianness;
- bit 255 mishandling, `y >= p`, negative zero, failed square-root recovery, or
  non-byte-identical re-encoding;
- `[8]P = I` asserted without `P != I` and `[4]P != I`;
- exact order eight asserted without computing `[L]P`;
- modular complement confused with unchecked bytewise complement;
- the nonsquare branch treated as a field point;
- missing parity, duplicate row, fifth candidate, or withdrawn
  `TRI2-VEC-01` value;
- author data, invalid-review arithmetic, historical similarity, or memory
  used as independent evidence;
- ordinary/cofactored provider acceptance substituted for the strict
  predicate;
- strict rejection asserted without public-key step 5 and signature step 3;
- a pass claimed to open implementation, protected material, E0, S0,
  provider/model work, or `main`; and
- any input mutation, hidden dependency, or out-of-scope read/write.

An unhandled or multiply interpreted mutation is a finding.

## 9. Severity and verdict

- `blocking`: lost independence, protected input, hidden authority, checker or
  source-boundary failure, gate escape, or repair requiring a closed gate.
- `major`: any derivation, literal, canonicality, point order, strict rejection,
  cardinality, or freeze rule is wrong, missing, or ambiguous.
- `minor`: bounded exactness or exposition defect that cannot change a byte,
  point, order, rejection, authority, or gate.

Allowed verdicts are exactly:

- `PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any substantive finding exists; or
- `INVALID-REVIEW`: integrity, baseline, checker, source, boundary, or
  independence failed.

A passing verdict does not itself freeze the package or open a later gate.

## 10. Required output and next gate

The report must state independence, Git baseline, all authenticated hashes,
validator and synthetic-preflight results, raw/canonical RFC proof, exact
marker audit, precomputed constants and branches, four row-by-row checks,
hostile traces, strict-profile mapping, findings, verdict, evidence limits, and
post-write audit.

If and only if the review is valid with zero findings, the maximum next gate is
a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`

The report must state that it performed public arithmetic only and did not
generate a key, implement production code, create protected material, invoke a
provider/model, execute E0 or S0, or authorize `main` integration.
