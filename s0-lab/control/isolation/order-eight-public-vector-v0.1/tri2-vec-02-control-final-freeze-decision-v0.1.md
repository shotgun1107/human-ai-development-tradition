# TRI2-VEC-02 CONTROL final freeze decision v0.1

- `decision_date`: `2026-08-11 KST`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`
- `source_branch`: `codex/s0-order-eight-public-vector-independent-verification-v04-r2`
- `source_tip`: `439020a20ff7781673f561355246ee9013180d1e`
- `source_tree`: `de65d6f632aecbecfd73d86cf835da075759973d`
- `reviewed_candidate_commit`: `bb19e6aaf6cdbd34908670876b5badeff27a6eec`
- `reviewed_candidate_tree`: `617d6026e4989484ae123cbb9daaf8fdb754e957`
- `decision`: `FREEZE-TRI2-VEC-02-PUBLIC-PACKAGE`
- `claim_kind`: authenticated public vector evidence only

## 1. CONTROL decision

CONTROL freezes `TRI2-VEC-02` as the public exact-order-eight hostile-vector
package required by the adopted S0 v0.14 trust-root and role-isolation v0.4
design.

The freeze is limited to the exact bytes, public derivation, and independent
verification evidence identified in this decision. It does not modify the
authoring candidate retrospectively. Statements such as `pending` inside the
authoring artifact remain immutable records of that earlier gate; the later
independent report and this CONTROL decision supply the succeeding status.

The package contains exactly four pairwise-distinct canonical Ed25519
encodings. Each has independently demonstrated nonidentity exact order eight
and rejection at both required `S0-ED25519-STRICT-1` subgroup predicates.
There are no accepted substitute, optional, fifth, or fallback rows.

## 2. Authenticated decision inputs

The canonical validator SelfTest passed all eleven cases before these inputs
were used. Each listed Markdown/sidecar pair passed strict UTF-8, BOM absence,
final LF, trailing-whitespace absence, canonical sidecar form, and exact hash
validation.

| Input | Complete-file SHA-256 |
|---|---|
| `AGENTS.md` | `c6c8045864b12453050e351e855444216ba363b767bb66b0bd67bb090ce1034a` |
| `verify-text-artifacts.ps1` | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` |
| `trust-root-role-isolation-design-revision-v0.4.md` | `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` |
| its `.sha256` sidecar | `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` |
| `control-integration-decision-v0.1.md` | `f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0` |
| its `.sha256` sidecar | `36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb` |
| `tri2-vec-02-order-eight-public-vectors-v0.1.md` | `a5195c25bf206a31ab59b2ce8e34a092d0e3921b1f252675b3ab7a859cb49668` |
| its `.sha256` sidecar | `07571711e531a5c206bf9e019ec5340a0771f7fefa296d3e68f47846e82ab9a5` |
| `tri2-vec-02-public-derivation-v0.1.md` | `cf10458557273de394a0b119afd2dc61d9301a9e9e6f8bb677926d367e0daf2d` |
| its `.sha256` sidecar | `9638dbc36ef57de0744babea58e0ef10e5c4758b683a5aa3b0aea98a0c832ecf` |
| `tri2-vec-02-review-input-boundary-revision-v0.3.md` | `b8f7b5d62da008896797298da2a1c24decc3553c7e120025bcfaf15ccdcd56c3` |
| its `.sha256` sidecar | `011b7c9413977d3003cc621db7aedf186b14dd1dc6a1601a490452d4abed3ef1` |
| `tri2-vec-02-independent-verification-brief-v0.4.md` | `b5a0ce94e7d0008ad3f69b62484b81ecbab81bab38c6cd3d68e83457923ec46c` |
| its `.sha256` sidecar | `f12367fd3edc89bb97e6558541b940d383bb94da441d7c2111fec7640a2ebcc7` |
| `independent-verification-v0.4.md` | `fb5df64e3428904d097b0f6130fdc20dbb945f96957934e210377d7dbd842438` |
| its `.sha256` sidecar | `cd0f303b62b04d55508fcbe967adabf1c1eeb9cafb08dee8bc985c555b7d39f9` |

The independent report's commit has the reviewed candidate as its sole parent
and adds only the authorized review Markdown and sidecar. No candidate input
was changed by that review commit.

## 3. Exact frozen vector set

The exact set is:

| Row | Frozen 32-byte lowercase hexadecimal encoding |
|---|---|
| `TRI2-VEC-02-01` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a` |
| `TRI2-VEC-02-02` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa` |
| `TRI2-VEC-02-03` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` |
| `TRI2-VEC-02-04` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` |

The row IDs, order, lowercase spelling, and all 32 bytes are normative. Any
bit, nibble, byte, order, label, cardinality, or file-hash change creates a new
candidate requiring a separately opened authoring and independent-review
lineage. Historical `TRI2-VEC-01` material remains withdrawn and cannot be
substituted.

## 4. Independent result accepted by CONTROL

The accepted independent verdict is:

`PASS-FOR-CONTROL-VECTOR-FREEZE-CONSIDERATION-ONLY`

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |

CONTROL accepts the following bounded results for every one of the four exact
rows:

1. an independent derivation produced the literal;
2. the literal is exactly 32 bytes and canonical decode succeeded;
3. canonical re-encoding reproduced identical bytes;
4. `P != I`;
5. `[8]P = I`;
6. `[4]P != I`;
7. `[L]P != I`;
8. strict public-key validation rejects it as `A` at step 5;
9. strict signature-point validation rejects it as `R` at step 3; and
10. the result is bound to the exact row bytes.

All four rows were pairwise distinct. The fresh reviewer authenticated exactly
24 public inputs, passed the canonical validator and synthetic checker
preflight, made one successful bounded RFC 8032 request, independently froze
the arithmetic before reading the author candidate, and completed the required
hostile checks. Its post-write audit found all inputs unchanged and exactly
the two authorized review outputs.

## 5. Effect on the adopted v0.4 public design

The adopted v0.4 design withdrew unsupported `TRI2-VEC-01` authority and
required a future `TRI2-VEC-02` package with exactly four pairwise-distinct
nonidentity exact-order-eight encodings, public derivation, canonical
decode/re-encode, `[4]`, `[8]`, `[L]`, and strict `A`/`R` rejection evidence
independently frozen before key generation.

This decision satisfies that **public evidence prerequisite**. The frozen
package may therefore be cited by a later, separately authorized
machine-readable successor or acceptance design using the exact artifact and
hash bindings in this decision.

This does not itself authorize key generation. Provider choice, cryptographic
implementation, machine-readable schema generation, consumer migration,
platform provisioning, and acceptance execution remain separate gates. If a
later consumer cannot bind or reproduce the exact frozen package, it must fail
closed rather than substitute, waive, regenerate, or select another vector.

## 6. Immutability and versioning

The frozen primary evidence is the vector artifact and public derivation pair.
The v0.3 boundary, v0.4 brief, and passing v0.4 independent review are frozen
supporting provenance. Their exact hashes are part of this decision.

Do not edit a frozen file in place. Corrections require:

1. a new versioned artifact and sidecar;
2. an explicit replacement map;
3. a fresh independent review using an authenticated input boundary; and
4. a new CONTROL decision.

Prior failed boundaries, invalid reviews, and withdrawn vectors remain
historical evidence. They are not silently rewritten, deleted, or treated as
successful predecessors.

## 7. Closed gates and maximum claim

This decision performed public document authentication and CONTROL evidence
integration only. It did not perform new curve arithmetic, fetch an external
source, implement a parser or cryptographic operation, generate a key, create
protected material, provision a provider or platform, execute E0 or S0, or
integrate any branch into `main`.

Still closed are implementation, machine-readable generation, key generation,
private-key custody, anchor or registry operations, signature execution,
fixtures, oracle, executors, provider/model sessions, scoring, E0, S0, central
system implementation, Project Brain integration, operational safety,
economic value, production readiness, and model-to-model transfer.

The maximum supported claim is that `TRI2-VEC-02` is frozen as authenticated
public hostile-vector evidence satisfying the v0.4 design's pre-key-generation
vector-evidence prerequisite. No operational or experimental result follows.

After this decision pair is canonically validated, committed, and published,
the vector lineage may be considered in a separately authorized public
`main` integration decision. No merge opens automatically.
