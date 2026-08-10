# TRI2-VEC-02 independent verification brief v0.1

- `status`: public review-control candidate
- `review_kind`: fresh public mathematical and design verification
- `current_gate`: authoring only; review gate not yet open
- `target_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `maximum_claim`: CONTROL final-freeze consideration only

## 1. Reviewer independence

The reviewer must be a fresh session that did not author, advise on, calculate,
or QA the `TRI2-VEC-02` candidate or its derivation. It must not inherit an
author or another reviewer conversation, must not use a subagent, and must not
read a prior `TRI2-VEC-02` review conclusion. Worktree separation is edit
isolation, not secret or independent information security.

The reviewer must derive and calculate independently. Agreement with the
candidate prose, historical bytes, an author transcript, a copied label, or a
library's small-order classification is not evidence.

## 2. Maximum public input set

CONTROL must provide exact relative paths and SHA-256 values outside this brief
for the following maximum set:

1. repository-root `AGENTS.md` at the candidate commit;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. the canonical public protocol r1 Markdown and sidecar;
4. the v0.2 trust-root/role-isolation design revision and sidecar containing
   the frozen `S0-ED25519-STRICT-1` profile;
5. the v0.4 trust-root/role-isolation design revision, identity-authority
   matrix addendum, acceptance-plan addendum, independent review, and CONTROL
   integration decision, each with its same-basename sidecar;
6. `tri2-vec-02-order-eight-public-vectors-v0.1.md` and sidecar;
7. `tri2-vec-02-public-derivation-v0.1.md` and sidecar; and
8. this brief and its same-basename sidecar.

The reviewer may open only RFC 8032 sections 5.1.2 through 5.1.4 from the RFC
Editor as an external primary source. No broad repository search, sealed
material, private key, implementation source, fixture, oracle, provider/model
output, E0 material, S0 material, advisory output, or unlisted source is
allowed.

Authenticate every supplied file before relying on it. A mismatch, missing
input, ambiguous path, stale brief, or canonical-validation failure invalidates
the review rather than becoming a substantive vector finding.

## 3. Exact Git and write boundary

CONTROL must freeze and supply the exact candidate branch, commit, tree, sole
parent, parent tree, and exact parent-to-candidate path diff. The initial
worktree must be clean. The candidate commit must add only the three authorized
public Markdown files and their same-basename sidecars under:

`s0-lab/control/isolation/order-eight-public-vector-v0.1/`

The reviewer may create only this missing output directory if needed:

`s0-lab/reviews/isolation/order-eight-public-vector-v0.1/`

It may write exactly:

- `independent-verification-v0.1.md`; and
- `independent-verification-v0.1.sha256`.

No candidate input, other directory, implementation file, Git index, branch,
commit, remote, or `main` state may be changed.

## 4. Integrity procedure

Before substantive review, the reviewer must:

1. verify the supplied Git identity and exact six-path candidate diff;
2. confirm initial clean status;
3. authenticate every supplied input by SHA-256;
4. run the authenticated validator SelfTest and require every case to pass;
5. validate every admitted Markdown/sidecar pair; and
6. distinguish byte-identity, canonical-format, and substantive failures.

After writing, it must validate the review pair, rehash every input, confirm the
Git identity is unchanged, and confirm status contains exactly the two
authorized untracked review outputs.

## 5. Required independent reconstruction

Without trusting the author derivation as an answer key, independently
reconstruct:

1. `p`, `d`, `L`, the Edwards identity, canonical encoding, canonical decoding,
   and complete addition rules from RFC 8032;
2. the unchanged strict public-key and signature-point predicates from
   `S0-ED25519-STRICT-1`;
3. why an exact-order-eight point that doubles to y-coordinate zero satisfies
   `d*y^4 + 2*y^2 - 1 = 0 mod p`;
4. every quadratic branch, including why one candidate `z=y^2` branch has no
   field square root;
5. the two valid y roots, two x roots, their parities, and the four exact
   32-byte encodings;
6. canonical decode and byte-identical re-encode for every row;
7. `P != I`, `[8]P = I`, `[4]P != I`, and `[L]P != I` for every row;
8. pairwise distinction of the four points and bytes;
9. rejection of every row as both `A` and `R` under the exact strict profile;
   and
10. the authoring, independent-verification, CONTROL freeze, key-generation,
    implementation, E0, S0, and `main` gate boundaries.

The reviewer must independently author its calculation method. It may use two
different RFC-consistent group-operation formulations as internal
corroboration, but neither an author result nor a generic provider verdict can
replace explicit field, encoding, and order checks.

Ephemeral public arithmetic in the review session is allowed. Materializing a
generator, reusable cryptographic helper, production verifier, key, signature,
fixture, or implementation file is not allowed.

## 6. Noncompensatory row criteria

Each of the exactly four rows passes only if all criteria pass independently:

1. an explicit public derivation produces the exact literal;
2. the literal is exactly 32 bytes and RFC 8032 canonical decode succeeds;
3. canonical re-encoding is byte-identical;
4. `P != I`;
5. `[8]P = I`;
6. `[4]P != I`;
7. `[L]P != I`;
8. strict validation rejects it as `A` at the exact required predicate;
9. strict validation rejects it as `R` at the exact required predicate; and
10. the result is bound to the row's exact bytes, not only a coordinate label.

One missing, ambiguous, inconsistent, or failed criterion fails the row. One
failed row fails the package. Extra, missing, or duplicate candidate rows fail
the package. No substitution, waiver, retry, majority vote, aggregate score,
or provider fallback is allowed.

## 7. Mandatory hostile checks

At minimum, trace and reject or correctly classify:

- one changed bit, nibble, byte, sign bit, byte order, or field endianness;
- a y value with bit 255 mishandled, `y >= p`, negative zero, failed square-root
  recovery, or non-byte-identical re-encoding;
- using only `[8]P = I` without proving `[4]P != I` and `P != I`;
- using exact order eight as a verbal label without computing `[L]P`;
- confusing a modular complement with an unchecked bytewise complement;
- choosing the nonsquare quadratic branch as if it produced a field point;
- omitting one x parity, duplicating one row, or introducing a fifth candidate;
- reusing any withdrawn `TRI2-VEC-01` coordinate, relation, attribution, or
  literal as authority;
- treating the author derivation, author dual-route agreement, or historical
  similarity as independent evidence;
- accepting a row because an ordinary/cofactored provider accepts it;
- claiming strict rejection without identifying public-key step 5 and
  signature step 3;
- claiming that vector success opens key generation, implementation, E0, S0,
  provider/model work, protected material, or `main` integration; and
- any input mutation, post-review mutation, hidden dependency, or out-of-scope
  read/write.

An unhandled or multiply interpreted mutation is a finding.

## 8. Severity and verdict

- `blocking`: lost independence, protected/secret input, hidden authority,
  forgeable evidence, a gate escape, or a repair requiring a closed gate.
- `major`: any required derivation, literal, canonicality, point-order, strict-
  rejection, row-cardinality, or freeze rule is wrong, missing, or ambiguous.
- `minor`: a bounded exactness or exposition defect that cannot change a byte,
  point, order, rejection result, authority, or gate.

Allowed verdicts are exactly:

- `PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any finding exists; or
- `INVALID-REVIEW`: integrity, baseline, boundary, or independence failed.

A passing verdict does not itself freeze the vector package or open any later
gate.

## 9. Required output

The review Markdown must state the independence and boundary, exact Git
baseline, all authenticated hashes, validator results, independently derived
constants and roots, four row-by-row encodings and checks, hostile traces,
strict-profile mapping, finding dispositions, counts, verdict, evidence limits,
and exact next gate.

If and only if the review is valid and has zero findings, the maximum next gate
is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`

The review must state explicitly that it ran public mathematical point
operations only and did not implement production code, generate a key, create
protected material, invoke a provider/model, execute E0 or S0, or authorize
`main` integration.
