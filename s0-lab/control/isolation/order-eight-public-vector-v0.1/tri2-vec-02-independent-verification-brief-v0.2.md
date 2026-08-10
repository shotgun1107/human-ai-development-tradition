# TRI2-VEC-02 independent verification brief v0.2

- `status`: public review-control revision candidate
- `review_kind`: fresh public mathematical and design verification
- `current_gate`: boundary revision only; independent review not yet open
- `target_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `maximum_claim`: CONTROL final-freeze consideration only
- `supersedes_after_freeze`: `tri2-vec-02-independent-verification-brief-v0.1.md`

## 1. Reviewer independence

The reviewer must be a fresh session that did not author, advise on, calculate,
or QA the `TRI2-VEC-02` candidate, its derivation, or this revision. It must not
inherit an author or reviewer conversation and must not use a subagent.
Worktree separation is edit isolation, not secret or independent information
security.

The historical v0.1 `INVALID-REVIEW` is admitted only as evidence of the input-
boundary failure. It contains no accepted vector result and cannot be used as
an answer key. Agreement with candidate prose, historical bytes, author
arithmetic, a copied label, or a library classification is not evidence.

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
8. the historical `independent-verification-v0.1.md` invalid review and
   sidecar;
9. `tri2-vec-02-review-input-boundary-revision-v0.1.md` and sidecar; and
10. this v0.2 brief and its sidecar.

This is 26 files: two file-specific inputs and twelve Markdown/sidecar pairs.
The v0.1 brief is excluded as stale procedural authority. No broad repository
search, sealed material, private key, implementation source, fixture, oracle,
provider/model output, E0 material, S0 material, advisory output, or unlisted
source is allowed.

Authenticate every supplied file before relying on it. A mismatch, missing
input, ambiguous path, stale controlling brief, or canonical-validation
failure invalidates the review rather than becoming a vector finding.

## 3. Exact Git and write boundary

CONTROL must freeze and supply the exact candidate branch, commit, tree, sole
parent, parent tree, and exact parent-to-candidate diff. Initial status must be
clean. The candidate commit must add only these four files under the existing
control directory:

- this v0.2 brief and sidecar; and
- the input-boundary revision v0.1 and sidecar.

The reviewer may write exactly:

- `s0-lab/reviews/isolation/order-eight-public-vector-v0.1/independent-verification-v0.2.md`;
  and
- its same-basename `.sha256` sidecar.

No candidate input, implementation file, other directory, Git index, branch,
commit, remote, or `main` state may be changed.

## 4. Integrity and ordered-read procedure

Before substantive review, the reviewer must:

1. verify the supplied Git identity, sole parent, exact four-added-path diff,
   and clean status;
2. hash all 26 supplied paths before reading any;
3. read `AGENTS.md`, this brief, and the boundary revision completely;
4. run the authenticated validator SelfTest and require every case to pass;
5. validate all twelve admitted Markdown/sidecar pairs; and
6. distinguish byte-identity, canonical-format, boundary, and substantive
   failures.

Next, it may read the non-author protocol, strict profile, v0.4 authority, and
historical invalid review. It must not open the candidate vector artifact or
author derivation until it has completed the independent precomputation in
section 6.

After writing, it must validate the review pair, rehash all 26 inputs, confirm
Git identity is unchanged, and confirm status contains exactly the two
authorized untracked v0.2 review outputs.

## 5. Exact official RFC transport boundary

The only external source is:

`https://www.rfc-editor.org/rfc/rfc8032.txt`

Do not use search, browser, HTML, web-open, cached snippets, mirrors, or another
source. Pipe the HTTP response directly into a deterministic byte slicer. The
slicer must assert:

```text
full_length = 106573
full_sha256 = f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9

parameter_range = [19710:22589]
parameter_length = 2879
parameter_sha256 = c3ae421b10d8f0806b81686270b45c08012dc57e33ed5540a21529db5ec2bd68

encoding_addition_range = [23458:27770]
encoding_addition_length = 4312
encoding_addition_sha256 = 0261ec3acfb9b9fdb9e472e7baf9d4d386edafe803a707cf12e0e63280e3a67d
```

Before output, assert the parameter slice contains the published `p`,
`-121665/121666` definition of `d`, and `L`; assert the second slice contains
actual sections 5.1.2, 5.1.3, and 5.1.4; and assert neither output contains the
actual 5.1.1 or 5.1.5 heading. Emit only the two slices. Never expose the full
response, the gap, or adjacent sections to the reviewer context. Any transport,
length, hash, marker, or exclusion failure yields `INVALID-REVIEW` without
fallback.

## 6. Independent precomputation before candidate read

Using only the authenticated non-author authority and the two official slices,
the reviewer must independently freeze in its session notes:

1. numeric `p`, `d`, `L`, and identity `I`;
2. the Ed25519 curve, canonical encode/decode, and complete addition rules;
3. the derivation from exact order eight to
   `d*y^4 + 2*y^2 - 1 = 0 mod p`;
4. every quadratic and square-root branch, including nonsquare rejection;
5. every field-valid x/y coordinate, x parity, and exact 32-byte encoding;
6. the intended `P != I`, `[4]`, `[8]`, `[L]`, and pairwise-distinction checks;
   and
7. the exact strict-profile rejection points for use as `A` and `R`.

Only after recording those results may the reviewer open the candidate artifact
and author derivation. It must compare exact bytes and then perform the complete
hostile review. The author documents cannot repair a missing precomputed value.

Ephemeral public arithmetic is allowed. Materializing a generator, reusable
cryptographic helper, production verifier, key, signature, fixture, oracle, or
implementation file is forbidden.

## 7. Noncompensatory row criteria

Each of exactly four rows passes only if all criteria pass independently:

1. the independent derivation produces the exact literal;
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
failed row fails the package. Extra, missing, or duplicate candidate rows fail
the package. No substitution, waiver, retry, vote, aggregate score, or provider
fallback is allowed.

## 8. Mandatory hostile checks

At minimum, trace and reject or correctly classify:

- any changed bit, nibble, byte, sign bit, byte order, or field endianness;
- bit 255 mishandling, `y >= p`, negative zero, failed square-root recovery, or
  non-byte-identical re-encoding;
- `[8]P = I` asserted without `P != I` and `[4]P != I`;
- exact order eight asserted without computing `[L]P`;
- modular complement confused with an unchecked bytewise complement;
- the nonsquare branch treated as a field point;
- a missing parity, duplicate row, or fifth candidate;
- any withdrawn `TRI2-VEC-01` value or attribution used as authority;
- author data, provisional invalid-review arithmetic, or historical similarity
  treated as independent evidence;
- ordinary or cofactored provider acceptance used instead of the strict
  predicate;
- strict rejection asserted without public-key step 5 and signature step 3;
- a pass claimed to open key generation, implementation, protected material,
  E0, S0, provider/model work, or `main`; and
- any input mutation, post-review mutation, hidden dependency, or out-of-scope
  read/write.

An unhandled or multiply interpreted mutation is a finding.

## 9. Severity and verdict

- `blocking`: lost independence, protected input, hidden authority, gate escape,
  or a repair requiring a closed gate.
- `major`: any derivation, literal, canonicality, point order, strict rejection,
  cardinality, or freeze rule is wrong, missing, or ambiguous.
- `minor`: bounded exactness or exposition defect that cannot change a byte,
  point, order, rejection, authority, or gate.

Allowed verdicts are exactly:

- `PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any substantive finding exists; or
- `INVALID-REVIEW`: integrity, baseline, source, boundary, or independence
  failed.

A passing verdict does not itself freeze the package or open a later gate.

## 10. Required output and next gate

The review must state independence, Git baseline, all authenticated hashes,
validator results, RFC transport proof, precomputed constants and roots, four
row-by-row checks, hostile traces, strict-profile mapping, findings, counts,
verdict, evidence limits, and post-write audit.

If and only if the review is valid and has zero findings, the maximum next gate
is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`

The report must state that it performed public arithmetic only and did not
generate a key, implement production code, create protected material, invoke a
provider/model, execute E0 or S0, or authorize `main` integration.
