# TRI2-VEC-02 independent verification v0.1

- `review_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `review_kind`: fresh public mathematical and design verification
- `review_status`: invalid because the admitted source boundary cannot support the required independent reconstruction
- `verdict`: `INVALID-REVIEW`
- `maximum_claim`: review-boundary failure only; no substantive vector disposition

## 1. Outcome

This review is invalid. The authenticated and externally permitted evidence does
not contain an independent source for the numeric Ed25519 curve parameter `d`
or its defining ratio `-121665/121666 mod p`. The allowed RFC 8032 byte slice
contains sections 5.1.2 through 5.1.4: it uses `p` and `d` symbolically in the
encoding and decoding rules and supplies the complete addition formulas, but it
does not define numeric `d`. The authenticated v0.2 strict-profile document
defines numeric `p` and `L` and the identity, but it also does not define `d`.

The author derivation contains numeric `d`, but the controlling brief expressly
forbids treating author intermediate values as an answer key. Using that value,
or using an unlisted remembered value, would introduce author or hidden
authority into the supposedly independent reconstruction. That would violate
the maximum input set and reviewer-independence requirements.

This is a review-integrity and source-boundary failure. It is not a substantive
finding that any candidate row, coordinate, encoding, point order, or strict-
rejection result is wrong. No row passes or fails by authority of this report.

## 2. Independence and boundary statement

This was a fresh reviewer session. It did not author, advise on, calculate for,
or QA the candidate before this review, and it used no subagent. It read only
the 22 explicitly admitted repository paths and the authenticated RFC byte
slice described below. It did not search the repository broadly, inspect
implementation source, protected or sealed material, a fixture, an oracle,
provider/model output, E0 material, or S0 material.

The author vector table and derivation were opened only after a provisional
session calculation. Once the missing independent authority for numeric `d`
was identified, all provisional arithmetic and comparisons depending on that
value were discarded as review evidence. They are not reported as independent
constants, roots, row results, or hostile-check dispositions.

## 3. Exact Git baseline

| Check | Authenticated value | Result |
|---|---|---|
| branch | `codex/s0-order-eight-public-vector-independent-verification` | pass |
| HEAD | `56fb3301630a4cf51643f0fa4a1f3351e9be5cf2` | pass |
| tree | `aa182994c6a884059d21f5610d90a543500768c9` | pass |
| sole parent | `5add6e5e1675793ad179e98e51ffa1515feb3db8` | pass |
| parent tree | `b949a345cc80283ab78c889fa3d1cbabeed04cba` | pass |
| initial status | clean | pass |
| parent-to-candidate diff | exactly the three candidate Markdown files and three same-basename sidecars under `s0-lab/control/isolation/order-eight-public-vector-v0.1/`, all added | pass |

The repository was not committed, pushed, rebased, merged, staged, or otherwise
mutated by this review. Only the authorized review pair was written.

## 4. Authenticated input hashes

All 22 paths were hashed before any content was read. Every value matched the
CONTROL-supplied SHA-256 record.

| SHA-256 | Exact path |
|---|---|
| `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` | `AGENTS.md` |
| `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | `s0-lab/control/tools/verify-text-artifacts.ps1` |
| `6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60` | `s0-lab/control/s0-protocol-v0.3-canonical-r1.md` |
| `88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3` | `s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256` |
| `e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4` | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md` |
| `41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3` | `s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256` |
| `5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md` |
| `8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256` |
| `19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md` |
| `22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256` |
| `f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md` |
| `3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256` |
| `82746f7c1b59fd162c1f54dc9e0e3d6d3c86b8ef7dc391fb5a10401e88157344` | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.md` |
| `28103747f4c3f9c55eb4f125a2de4365c430e31a001256a2c6cc3a9512dc00ea` | `s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.sha256` |
| `f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md` |
| `36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb` | `s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.sha256` |
| `a5195c25bf206a31ab59b2ce8e34a092d0e3921b1f252675b3ab7a859cb49668` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.md` |
| `07571711e531a5c206bf9e019ec5340a0771f7fefa296d3e68f47846e82ab9a5` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.sha256` |
| `cf10458557273de394a0b119afd2dc61d9301a9e9e6f8bb677926d367e0daf2d` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.md` |
| `9638dbc36ef57de0744babea58e0ef10e5c4758b683a5aa3b0aea98a0c832ecf` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.sha256` |
| `950fab100657607caa2f5f61acf81967e9903bef5fbe796588c4d2860f336abd` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.1.md` |
| `eb4670ab252d2430171972bfc6e6d5713dc3e65c5c32b992144c515382be8f7a` | `s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.1.sha256` |

## 5. Canonical validator results

The authenticated validator had SHA-256
`b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3`.
Its SelfTest passed all 11 cases, including byte-level UTF-8 BOM detection,
strict UTF-8, final-LF, trailing-whitespace, empty-file, and canonical-sidecar
positive and negative cases.

All ten admitted Markdown/sidecar pairs passed every separately reported
check: file presence, strict UTF-8, BOM absence, final LF, trailing-whitespace
absence, sidecar presence, sidecar strict UTF-8, sidecar BOM absence, sidecar
final LF, sidecar trailing-whitespace absence, canonical sidecar record/hash,
and artifact overall.

These are byte-identity and canonical-format results only. They do not repair
the substantive source-boundary defect.

## 6. RFC transport and admitted content

No web-search, web-open, or browser interface was used. The official RFC Editor
plain-text response was piped directly through the prescribed deterministic
PowerShell byte slicer. Before emitting any prose, the slicer established:

| Check | Required and observed value |
|---|---|
| full pipeline byte length | `106573` |
| full pipeline SHA-256 | `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9` |
| slice range | bytes `[23458:27770]` |
| slice byte length | `4312` |
| slice SHA-256 | `0261ec3acfb9b9fdb9e472e7baf9d4d386edafe803a707cf12e0e63280e3a67d` |
| required headings | `5.1.2.  Encoding`, `5.1.3.  Decoding`, and `5.1.4.  Point Addition` present |
| excluded headings | `5.1.1.  Modular Arithmetic` and `5.1.5.  Key Generation` absent |

Only that authenticated slice was exposed. It provides canonical encoding,
canonical decoding, complete extended-coordinate addition, and doubling
rules. It does not include the Ed25519 parameter-definition text needed to
authenticate numeric `d` independently.

## 7. Required reconstruction and hostile checks

The controlling brief requires independent reconstruction of `p`, `d`, `L`,
the order-eight equation and roots, four row bytes, decoding, re-encoding,
point orders, strict rejection, and all hostile cases. The independent source
chain fails before those noncompensatory criteria can be validly evaluated:

1. numeric `p`, numeric `L`, identity `I`, and the strict public-key/signature
   predicates are authenticated by the v0.2 profile;
2. encoding, decoding, and complete group-operation formulas are authenticated
   by the permitted RFC slice;
3. numeric `d` is absent from both of those independent sources; and
4. numeric `d` appears only in the author derivation, which cannot supply the
   missing independent premise.

Consequently, the equation, quadratic branches, roots, encodings, row-by-row
orders, strict-rejection mappings, pairwise distinction, byte mutations,
endianness mutations, negative-zero cases, nonsquare classification, and other
hostile traces were not validly completed by this review. Any provisional
session calculations are excluded rather than converted into evidence after
the boundary failure was discovered.

## 8. Finding disposition and counts

### `R2-INV-01` — blocking review-boundary defect

- `classification`: review integrity/boundary, not a substantive vector finding
- `status`: open
- `condition`: the allowed independent sources do not authenticate numeric
  Ed25519 `d`, while the brief requires independent reconstruction and forbids
  the author derivation from acting as the answer key
- `impact`: accepting any row result would require an unlisted or author-derived
  premise and would therefore lose reviewer independence
- `disposition`: invalidate the review; do not freeze, accept, reject, repair,
  waive, retry, or substitute any candidate row on this record

| Count domain | blocking | major | minor |
|---|---:|---:|---:|
| review-integrity defects | 1 | 0 | 0 |
| substantive vector findings | not assessed | not assessed | not assessed |

## 9. Verdict and next boundary

`INVALID-REVIEW`

The package is neither passed nor substantively failed by this report. The
maximum zero-finding next gate,
`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR CONTROL FINAL FREEZE DECISION OPEN`, is not
available.

No experimental next gate is authorized. CONTROL would first need to prepare
and authenticate a new review baseline whose maximum input set includes a
non-author primary-source byte slice that defines numeric Ed25519 `d` (and any
other constants the reviewer must reconstruct), while preserving an exact
semantic boundary. A new fresh reviewer could then act only after the user
separately opens `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION
OPEN` for that new baseline.

## 10. Evidence limits

This session performed public mathematical point operations only as provisional
working arithmetic; none is admitted as a valid independent result. It did not
implement production code, materialize a generator or reusable cryptographic
helper, generate a key, create a signature, fixture, oracle, protected or
sealed material, invoke a provider/model, execute E0 or S0, implement the
central system or Project Brain integration, validate operational safety,
economic value, or model-to-model transfer, or authorize `main` integration.

## 11. Post-write audit

- review-pair canonical validation: pass
- all 22 input hashes unchanged: pass
- branch, HEAD, tree, parent, and parent tree unchanged: pass
- Git status exactly the two authorized untracked review outputs: pass
