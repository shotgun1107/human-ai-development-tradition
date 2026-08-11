# TRI2-VEC-02 independent verification v0.4

- `review_kind`: fresh public mathematical and design verification
- `review_date`: 2026-08-11 KST
- `review_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `worktree`: `C:\Users\SSAFY\AppData\Local\Temp\ai-development-tradition-s0-order-eight-vector-review-v04-r2`
- `branch`: `codex/s0-order-eight-public-vector-independent-verification-v04-r2`
- `reviewed_commit`: `bb19e6aaf6cdbd34908670876b5badeff27a6eec`
- `reviewed_tree`: `617d6026e4989484ae123cbb9daaf8fdb754e957`
- `verdict`: `PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`
- `finding_count`: zero blocking, zero major, zero minor
- `claim_kind`: public arithmetic and bounded review evidence only

## 1. Independence, authority, and limits

This was a fresh independent review. The reviewer did not author, advise on,
calculate, or QA the candidate, derivation, boundary, brief, or any predecessor
review, inherited no author or reviewer conversation, and used no subagent.
Candidate and derivation files remained unopened until the complete independent
precomputation was frozen in session-local output.

Only the exact 24 externally supplied public inputs in section 2 and the two
bounded official RFC slices were used. No predecessor boundary, predecessor
brief, invalid review, manifest file, unlisted repository file, implementation
source, fixture, oracle, provider/model output, E0 material, S0 material, or
advisory output was read. No `F0-SEALED` path was opened, enumerated, hashed,
searched, quoted, or summarized. Worktree separation is treated only as edit
isolation, not independent information security.

The only writes are this report and its same-basename SHA-256 sidecar. This
review performed public arithmetic only. It generated no key, signature,
fixture, oracle, protected material, reusable generator, cryptographic helper,
production verifier, implementation, provider/model session, E0 run, or S0
run, and it grants no `main` authority.

## 2. Pre-read integrity and authentication

### 2.1 Git and path gate

All checks completed before any file content was read.

| Check | Required and observed value | Result |
|---|---|---|
| manifest cardinality | exactly 24 paths | pass |
| supplied relative-path uniqueness | 24 of 24 | pass |
| resolved-path uniqueness | 24 of 24 | pass |
| tracked stage-zero index uniqueness | exactly one entry for each supplied path | pass |
| branch | `codex/s0-order-eight-public-vector-independent-verification-v04-r2` | pass |
| HEAD | `bb19e6aaf6cdbd34908670876b5badeff27a6eec` | pass |
| HEAD tree | `617d6026e4989484ae123cbb9daaf8fdb754e957` | pass |
| sole parent | `3c41b54895d105496aa748ffe367939fefd0bd9e` | pass |
| parent tree | `1ce3864bac33d4c98b991016e58edf9dc022cd49` | pass |
| initial status | clean, zero porcelain entries | pass |
| parent-to-candidate diff | exactly the v0.4 brief pair and v0.3 boundary pair, all four added | pass |

The first local diff-set comparison used a malformed PowerShell expected-array
expression and returned false without changing or reading repository content.
The same expression defect recurred in the initial post-write audit, and one
correction attempt stopped at PowerShell parsing. Final explicit four-literal
comparisons returned four actual, four expected, and zero differences. The Git
diff itself was unchanged and exact throughout.

### 2.2 Exact 24-path SHA-256 authentication

Every supplied path existed and matched its externally supplied file hash
before any content was read. Sidecar rows below are hashes of the sidecar files
themselves.

| # | Exact input | Verified SHA-256 |
|---:|---|---|
| 1 | `AGENTS.md` | `c6c8045864b12453050e351e855444216ba363b767bb66b0bd67bb090ce1034a` |
| 2 | `s0-lab/control/tools/verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| 3 | `s0-lab/control/s0-protocol-v0.3-canonical-r1.md` | `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` |
| 4 | `s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256` | `88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3` |
| 5 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md` | `e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4` |
| 6 | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256` | `41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3` |
| 7 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| 8 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256` | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| 9 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` | `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` |
| 10 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256` | `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` |
| 11 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` | `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` |
| 12 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256` | `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` |
| 13 | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.md` | `82746f7c1b59fd162c1f54dc9e0e3d6d3c86b8ef7dc391fb5a10401e88157344` |
| 14 | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.sha256` | `28103747f4c3f9c55eb4f125a2de4365c430e31a001256a2c6cc3a9512dc00ea` |
| 15 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md` | `f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0` |
| 16 | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.sha256` | `36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb` |
| 17 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.md` | `a5195c25bf206a31ab59b2ce8e34a092d0e3921b1f252675b3ab7a859cb49668` |
| 18 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.sha256` | `07571711e531a5c206bf9e019ec5340a0771f7fefa296d3e68f47846e82ab9a5` |
| 19 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.md` | `cf10458557273de394a0b119afd2dc61d9301a9e9e6f8bb677926d367e0daf2d` |
| 20 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.sha256` | `9638dbc36ef57de0744babea58e0ef10e5c4758b683a5aa3b0aea98a0c832ecf` |
| 21 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.md` | `b8f7b5d62da008896797298da2a1c24decc3553c7e120025bcfaf15ccdcd56c3` |
| 22 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.sha256` | `011b7c9413977d3003cc621db7aedf186b14dd1dc6a1601a490452d4abed3ef1` |
| 23 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.md` | `b5a0ce94e7d0008ad3f69b62484b81ecbab81bab38c6cd3d68e83457923ec46c` |
| 24 | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.sha256` | `f12367fd3edc89bb97e6558541b940d383bb94da441d7c2111fec7640a2ebcc7` |

## 3. Canonical validation and checker preflight

The authenticated validator's first direct launch was blocked by the host
PowerShell execution policy before the script loaded. The same authenticated
script was then invoked with process-scoped `-ExecutionPolicy Bypass`; its
SelfTest passed all 11 cases. Exactly eleven admitted Markdown/sidecar pairs
were then validated, once each. Every UTF-8, BOM-absence, final-LF,
trailing-whitespace, sidecar-presence, sidecar-format/hash, and overall check
passed.

The ephemeral transport checker was tested only against synthetic bytes before
source access. Two permitted synthetic retries corrected a nullable-zero
offset representation and an unavailable host formatting method. The complete
15-case preflight then passed:

- overlapping exact subsequence counts and offsets;
- literal ASCII caret rather than regex/exponent semantics;
- exact markers at offset zero and nonzero, plus absent-marker zero count;
- wrong offset, length, count, one-bit hex, and non-lowercase hex rejection;
- exact CRLF-to-LF conversion;
- bare-CR and mixed-ending rejection; and
- half-open slicing without inclusive-end error.

A later live-command invocation stopped at local `INITIALIZE` before an HTTP
client or request existed because Windows PowerShell had not loaded the built-
in `System.Net.Http` assembly. No DNS lookup or source request began. A
synthetic-only initialization extension loaded that assembly and proved client
construction plus redirects disabled. The sole actual source request described
in section 4 was then issued exactly once. It was not retried and no fallback
was used.

## 4. One-shot official RFC proof

The sole request was a direct in-memory GET to
`https://www.rfc-editor.org/rfc/rfc8032.txt` using one `SendAsync` call.
Redirects were disabled. HTTP success, exact final URL, media type
`text/plain`, ASCII-only bytes, no UTF-8 BOM, and no NUL all passed.

| Object | Profile/range | Length | SHA-256 | Line shape | Result |
|---|---|---:|---|---|---|
| raw body | `RFC8032-WIRE-LF-1` | 103210 | `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3` | 3363 bare LF, zero CRLF, zero bare CR | pass |
| canonical body | `RFC8032-CANONICAL-LF-1` | 103210 | `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3` | 3363 bare LF, zero CRLF, zero bare CR | pass |
| parameter slice | `[19245:22067]` | 2822 | `a2ee2379339d2d9e81fc04d92411347edd7da98bbf2fb92983f299f4dddd7b08` | emitted only after all checks | pass |
| encoding/addition slice | `[22915:27092]` | 4177 | `5e87337157810b1420fa543727fb74dbdecc7510b004a1100d9a58bcd7bc916d` | emitted only after all checks | pass |

The complete canonical body was authenticated before slicing. Before either
slice was emitted, the checker emitted only bounded metadata and ran every
marker as exact, potentially overlapping byte-subsequence equality.

| Marker | Slice | Required/observed offset | Length | Required/observed count | Result |
|---|---|---:|---:|---:|---|
| `P-H1` | `PARAMETER-1` | 0 / 0 | 40 | 1 / 1 | pass |
| `P-P` | `PARAMETER-1` | 356 / 356 | 10 | 1 / 1 | pass |
| `P-D` | `PARAMETER-1` | 940 / 940 | 14 | 1 / 1 | pass |
| `P-L` | `PARAMETER-1` | 1559 / 1559 | 44 | 1 / 1 | pass |
| `P-NO-511` | `PARAMETER-1` | none / none | 26 | 0 / 0 | pass |
| `E-512` | `ENCODING-ADDITION-1` | 0 / 0 | 16 | 1 / 1 | pass |
| `E-513` | `ENCODING-ADDITION-1` | 754 / 754 | 16 | 1 / 1 | pass |
| `E-514` | `ENCODING-ADDITION-1` | 2233 / 2233 | 22 | 1 / 1 | pass |
| `E-NO-511` | `ENCODING-ADDITION-1` | none / none | 26 | 0 / 0 | pass |
| `E-NO-515` | `ENCODING-ADDITION-1` | none / none | 22 | 0 / 0 | pass |

No full body, gap, adjacent section, diagnostic source excerpt, local copy,
cache, HTML, browser, search result, mirror, or alternate RFC source was
emitted or used.

## 5. Independent precomputation before author read

### 5.1 Constants, curve, and rules

Using only the authenticated non-author authority and the two official slices,
the following values were frozen before opening the candidate or derivation:

```text
p = 57896044618658097711785492504343953926634992332820282019728792003956564819949
d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
L = 7237005577332262213973186563042994240857116359379907606001950938285454250989
I = (0, 1)
sqrt(-1) = 19681161376707505956807079304988542015446066515923890162744021073123829784752
```

The curve is `-x^2 + y^2 = 1 + d*x^2*y^2 mod p`. Encoding is the 255-bit
little-endian `y` with `x mod 2` in bit 255. Decoding clears bit 255, rejects
`y >= p`, recovers `x` with the exact RFC square-root branches, rejects failed
recovery and negative zero, selects the required parity, and must re-encode
byte-identically. Point operations used the complete RFC extended-coordinate
addition formulas and binary scalar multiplication from `I`.

### 5.2 Equation and all branches

For exact-order-eight `P`, `[2]P` has order four and its y-coordinate is zero.
The doubling numerator gives `x^2 = -y^2`; substituting into the curve equation
with `t = y^2` gives:

```text
d*t^2 + 2*t - 1 = 0 mod p
t = (-1 +/- sqrt(1+d)) / d mod p
```

The independent square root of `1+d` and its negation were:

```text
28684908821141429758912547916212233914183938327803420948194326298794999701186
29211135797516667952872944588131720012451054005016861071534465705161565118763
```

The first quadratic branch produced
`3685532557031388680362915159118232971324886473920755116993713661282644049091`,
which is nonsquare and produces no field point. The second produced the
quadratic residue
`53699909539325142115343624207863611371097067213659596252119297355370707899025`.
Its two y roots are:

```text
y_low  = 2707385501144840649318225287225658788936804267575313519463743609750303402022
y_high = 55188659117513257062467267217118295137698188065244968500265048394206261417927
```

For either y root, x recovery produced:

```text
x_even = 14399317868200118260347934320527232580618823971194345261214217575416788799818
x_odd  = 43496726750457979451437558183816721346016168361625936758514574428539776020131
```

The parities are respectively zero and one. Independently,
`y_low + y_high = p` and `x_even + x_odd = p`. These are modular-coordinate
relations, not unchecked bytewise complements.

## 6. Four noncompensatory row results

The candidate and derivation were opened only after section 5 was frozen. Their
four bytes, coordinates, branch classification, encodings, scalar results, and
strict rejection locations exactly matched the independent results.

| Row | Exact 32-byte encoding | x | y | parity | `[4]P` | `[8]P` | `[L]P` encoding |
|---|---|---:|---:|---:|---|---|---|
| `TRI2-VEC-02-01` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a` | `x_even` | `y_high` | 0 | order-two point | `I` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` |
| `TRI2-VEC-02-02` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa` | `x_odd` | `y_high` | 1 | order-two point | `I` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` |
| `TRI2-VEC-02-03` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` | `x_even` | `y_low` | 0 | order-two point | `I` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa` |
| `TRI2-VEC-02-04` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` | `x_odd` | `y_low` | 1 | order-two point | `I` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a` |

The order-two point is `(0,p-1)` with canonical encoding
`ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f`.
The identity encoding is
`0100000000000000000000000000000000000000000000000000000000000000`.

Every row independently passed all ten required criteria:

| Criterion | 01 | 02 | 03 | 04 |
|---|---|---|---|---|
| independent derivation produces exact literal | pass | pass | pass | pass |
| exact length 32 and canonical decode | pass | pass | pass | pass |
| byte-identical canonical re-encode | pass | pass | pass | pass |
| `P != I` | pass | pass | pass | pass |
| `[8]P = I` | pass | pass | pass | pass |
| `[4]P != I` | pass | pass | pass | pass |
| `[L]P != I` | pass | pass | pass | pass |
| strict rejection as `A` at required predicate | pass | pass | pass | pass |
| strict rejection as `R` at required predicate | pass | pass | pass | pass |
| result bound to exact row bytes | pass | pass | pass | pass |

All four rows are pairwise distinct. There is no missing, duplicate, or fifth
candidate row.

## 7. Strict-profile mapping

For every row used as `Aenc`, exact length, canonical decode, byte-identical
re-encode, and `A != I` pass. Strict public-key validation then rejects at
step 5 because `[L]A != I`.

For every row used as `Renc`, signature step 2 canonical decode and re-encode
pass and `R != I`. Strict signature validation rejects at step 3 because
`[L]R != I`, before scalar or signature-equation success could authorize the
signature. Ordinary provider success, a cofactored equation, a library label,
or a truthy non-Boolean result cannot substitute for either predicate.

## 8. Mandatory hostile traces

All checker/source boundary mutations had one fail-closed result: use before
complete synthetic preflight, regex/wildcard/casefold/line matching, bad marker
hex/offset/length/count, incomplete raw-profile identity, mixed or third line
shape, excess normalization, slicing before full-body authentication, and
extra source emission all reject or terminate the review. The actual pipeline
used exact byte operations and passed each assertion before slice emission.

The candidate/package hostile traces also had one result each:

| Mutation or substitution | Classification |
|---|---|
| changed bit, nibble, byte order, or field endianness | reject exact row-byte mismatch |
| row 01 sign bit toggled to the bytes of row 02 | reject row-01 binding and resulting duplicate/substitution |
| bit 255 interpreted as y data instead of x parity | reject under RFC decode/row binding |
| `y >= p` | reject at decoding step 1 |
| negative zero | reject at decoding step 4 |
| y value 2 with failed square-root recovery | reject as nonsquare |
| non-byte-identical re-encoding | reject canonicality |
| `[8]P = I` without independent `P != I` and `[4]P != I` | reject incomplete order proof |
| exact order eight without `[L]P` | reject incomplete strict-subgroup evidence |
| integer `p-y` replaced with bytewise complement | reject; bytewise complement is not the other coordinate encoding |
| nonsquare quadratic branch treated as a point | reject; it has no field y root |
| missing parity, duplicate row, fifth row, missing row, or row-label swap | reject exact cardinality/distinction/row binding |
| a withdrawn `TRI2-VEC-01` label or historical value used as authority | reject; withdrawn history is not evidence |
| author arithmetic, invalid-review arithmetic, similarity, or memory used as independent evidence | reject; independent precomputation preceded author read |
| ordinary/cofactored provider acceptance used for the strict result | reject predicate substitution |
| strict rejection without public-key step 5 and signature step 3 | reject incomplete mapping |
| pass used to open implementation, protected material, provider/model work, E0, S0, or `main` | reject gate escape |
| input mutation, hidden dependency, unlisted read, or unauthorized write | terminal `INVALID-REVIEW` condition; none occurred |

No mutation was unhandled, multiply interpreted, waived, retried after source
request, or decided by an operator-selected alternative.

## 9. Findings, verdict, and maximum next gate

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |
| total | 0 |

`PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`

The maximum supported claim is that the authenticated public candidate has
exactly four pairwise-distinct canonical nonidentity exact-order-eight points,
each independently bound to its exact bytes and independently shown to fail
the unchanged strict public-key and signature-point subgroup predicates.

This verdict does not freeze the package and opens no later gate automatically.
The maximum next gate is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`

## 10. Evidence classification and post-write audit

- Facts are the supplied and reproduced Git identities, 24 file hashes,
  canonical-validator results, exact HTTP/byte/hash/marker observations,
  authenticated document clauses, and exact candidate bytes.
- Inferences are the algebraic derivation, branch classification, point and
  scalar results, hostile classifications, finding count, and verdict.
- Proposals: none. The possible next gate is a brief-defined authority limit,
  not an automatically opened recommendation.
- Test results are limited to read-only Git/index checks, SHA-256 and canonical
  text validation, synthetic checker tests, the sole bounded RFC request,
  ephemeral public field/group arithmetic, and hostile public-byte tests.

After the final report and sidecar write, the canonical validator passed the
review pair; all 24 inputs rehashed with zero mismatches; branch, HEAD, trees,
sole parent, and exact four-addition diff remained unchanged; and porcelain
status contained exactly the two authorized untracked v0.4 review outputs.
The Git index, candidate inputs, branch, commit, remote, and `main` were not
changed.
