# TRI2-VEC-02 order-eight public vectors v0.1

- `status`: public authoring freeze candidate
- `artifact_id`: `TRI2-VEC-02`
- `current_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR AUTHORING OPEN`
- `author_evidence`: completed
- `independent_verification`: pending
- `key_generation`: blocked
- `claim_kind`: public candidate bytes and author-side calculation only

## 1. Authority and limit

This artifact is the proposed successor required by the authenticated v0.4
trust-root and role-isolation design. It contains exactly four pairwise-
distinct candidate Ed25519 encodings for the nonidentity exact-order-eight
hostile class.

The four rows are not yet acceptance authority. The separately frozen public
derivation and a fresh independent verification must both pass before CONTROL
may consider a final vector freeze. Until then, key generation remains blocked
without substitution, waiver, or retry.

The withdrawn `TRI2-VEC-01` coordinates, relation, provenance, and literals are
historical failure evidence only. They are not used as authority for this
artifact. Similarity between a corrected result and any historical byte string
cannot replace the derivation or independent verification.

## 2. Exact candidate set

Each literal below is exactly 32 octets represented by 64 lowercase hexadecimal
characters. The final high bit is the RFC 8032 x-sign bit; the remaining 255
bits encode y in little-endian order.

| Row | Exact 32-byte encoding | x-sign bit | y coordinate label |
|---|---|---:|---|
| `TRI2-VEC-02-01` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a` | 0 | `y_high` |
| `TRI2-VEC-02-02` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa` | 1 | `y_high` |
| `TRI2-VEC-02-03` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` | 0 | `y_low` |
| `TRI2-VEC-02-04` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` | 1 | `y_low` |

There are no other `TRI2-VEC-02` candidate rows in this package.

## 3. Exact decoded coordinates

Let:

```text
p = 57896044618658097711785492504343953926634992332820282019728792003956564819949
x_even = 14399317868200118260347934320527232580618823971194345261214217575416788799818
x_odd = 43496726750457979451437558183816721346016168361625936758514574428539776020131
y_low = 2707385501144840649318225287225658788936804267575313519463743609750303402022
y_high = 55188659117513257062467267217118295137698188065244968500265048394206261417927
```

The four decoded points are:

| Row | x | y |
|---|---:|---:|
| `TRI2-VEC-02-01` | `x_even` | `y_high` |
| `TRI2-VEC-02-02` | `x_odd` | `y_high` |
| `TRI2-VEC-02-03` | `x_even` | `y_low` |
| `TRI2-VEC-02-04` | `x_odd` | `y_low` |

The author-side calculation established `x_even + x_odd = p` and
`y_low + y_high = p`. Those equalities are calculation results, not copied
provenance. A fresh verifier must reproduce them independently.

## 4. Author-side result matrix

The companion derivation records the equations, intermediate values, point
operations, and two calculation routes. At this authoring gate, every row
returned the following results:

| Required property | 01 | 02 | 03 | 04 |
|---|---|---|---|---|
| explicit derivation produces literal | pass | pass | pass | pass |
| RFC 8032 canonical decode | pass | pass | pass | pass |
| byte-identical re-encode | pass | pass | pass | pass |
| `P != I` | pass | pass | pass | pass |
| `[8]P = I` | pass | pass | pass | pass |
| `[4]P != I` | pass | pass | pass | pass |
| `[L]P != I` | pass | pass | pass | pass |
| strict rejection when used as `A` | pass | pass | pass | pass |
| strict rejection when used as `R` | pass | pass | pass | pass |
| fresh independent verification | pending | pending | pending | pending |

The first nine rows are author evidence only. The final row is
noncompensatory: all four `pending` cells must become independently frozen
passes before the package can be used.

## 5. Strict-profile rejection meaning

All four encodings decode canonically, re-encode identically, and are not the
identity. They are nevertheless invalid under `S0-ED25519-STRICT-1` because
that profile requires `[L]A = I` for a public key and `[L]R = I` for the encoded
signature point. The author calculation returns `[L]P != I` for every row.

Therefore:

- each row used as `Aenc` rejects at strict public-key validation step 5; and
- each row used as `Renc` rejects at strict signature validation step 3,
  before scalar or signature-equation acceptance can grant success.

Ordinary provider acceptance, a cofactored equation, or a copied small-order
label cannot substitute for these separate strict checks.

## 6. Closed boundaries

This artifact does not create or authorize:

- a generator, parser, schema, cryptographic library, production validator, or
  implementation;
- a private key, public-key generation ceremony, anchor, registry entry,
  signature, protected artifact, fixture, bank, label, or hidden oracle;
- a provider or model session, executor, judge, E0 test, S0 test, or central
  system; or
- migration to a downstream consumer or integration into `main`.

No private or sealed material was read or produced. The four literals and all
coordinates in this package are public hostile-test candidates.

## 7. Freeze and next gate

This authoring candidate becomes immutable evidence only after its Markdown,
the companion derivation, the independent-verification brief, and all three
same-basename sidecars are canonical and committed at one exact public
candidate commit.

That authoring freeze may permit only a separately opened fresh review gate:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`

No review opens automatically. A future zero-finding independent verdict may
permit only separate CONTROL final-freeze consideration; it does not itself
open key generation, implementation, E0, S0, or `main` integration.
