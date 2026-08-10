# TRI2-VEC-02 public derivation v0.1

- `status`: public author calculation record
- `derives_artifact`: `TRI2-VEC-02`
- `current_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR AUTHORING OPEN`
- `calculation_scope`: public Ed25519 field and point operations only
- `independent_verification`: not performed by this record

## 1. Facts, calculations, and claim boundary

The external mathematical source is RFC 8032 sections 5.1.2 through 5.1.4.
Those sections define the Ed25519 parameters, point encoding, canonical
decoding, and complete point-addition formulas:

<https://www.rfc-editor.org/rfc/rfc8032.html#section-5.1.2>

The authenticated project sources are the unchanged
`S0-ED25519-STRICT-1` profile in the v0.2 design and the `TRI2-VEC-02`
requirements adopted by the v0.4 CONTROL decision.

Facts attributed to those sources are separated here from author calculations.
The coordinates, roots, encoded bytes, and scalar-multiplication results below
are author calculations performed under the current gate. They are not a fresh
independent review and cannot satisfy the independent-verification blocker.

No claim is made that RFC 9381 publishes these coordinates or literals.

## 2. Field and curve constants

All arithmetic is modulo `p` unless stated otherwise.

```text
p = 2^255 - 19
  = 57896044618658097711785492504343953926634992332820282019728792003956564819949

d = -121665 / 121666 mod p
  = 37095705934669439343138083508754565189542113879843219016388785533085940283555

L = 2^252 + 27742317777372353535851937790883648493
  = 7237005577332262213973186563042994240857116359379907606001950938285454250989

I = (0, 1)
sqrt(-1) = 19681161376707505956807079304988542015446066515923890162744021073123829784752
```

Ed25519 uses the twisted Edwards equation:

```text
-x^2 + y^2 = 1 + d*x^2*y^2 mod p
```

## 3. Deriving the exact-order-eight coordinates

For doubling `P=(x,y)`, the complete affine addition formula gives:

```text
y([2]P) = (y^2 + x^2) / (1 - d*x^2*y^2) mod p
```

An exact-order-eight point doubles to an order-four point with y-coordinate
zero. Setting the numerator to zero gives `x^2 = -y^2`. Substituting this into
the curve equation gives:

```text
d*y^4 + 2*y^2 - 1 = 0 mod p
```

Let `z = y^2`. Then:

```text
d*z^2 + 2*z - 1 = 0 mod p
z = (-1 +/- sqrt(1+d)) / d mod p
```

The two square roots of `1+d` are:

```text
28684908821141429758912547916212233914183938327803420948194326298794999701186
29211135797516667952872944588131720012451054005016861071534465705161565118763
```

The first choice yields:

```text
z = 3685532557031388680362915159118232971324886473920755116993713661282644049091
```

Euler's criterion returns `z^((p-1)/2) = p-1`, so this branch has no y root in
the field and produces no Ed25519 point.

The second choice yields the quadratic residue:

```text
z = 53699909539325142115343624207863611371097067213659596252119297355370707899025
```

Its two square roots are:

```text
y_low  = 2707385501144840649318225287225658788936804267575313519463743609750303402022
y_high = 55188659117513257062467267217118295137698188065244968500265048394206261417927
```

Direct integer addition, not only modular equivalence, gives
`y_low + y_high = p`.

For either y root, `x^2 = -z mod p`. Its two square roots are:

```text
x_even = 14399317868200118260347934320527232580618823971194345261214217575416788799818
x_odd  = 43496726750457979451437558183816721346016168361625936758514574428539776020131
```

`x_even` has parity zero, `x_odd` has parity one, and direct integer addition
gives `x_even + x_odd = p`. The Cartesian product of the two x roots and two y
roots therefore gives exactly four pairwise-distinct points.

## 4. Constructing the exact encodings

RFC 8032 encodes y as 32-byte little-endian and stores x parity in the high bit
of the final octet. With that sign bit clear, the two y encodings are:

```text
y_high = c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a
y_low  = 26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05
```

Keeping the high bit clear selects `x_even`. Setting it selects `x_odd`. This
produces exactly:

```text
TRI2-VEC-02-01 = c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a
TRI2-VEC-02-02 = c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa
TRI2-VEC-02-03 = 26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05
TRI2-VEC-02-04 = 26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85
```

Clearing each sign bit recovers an integer less than `p`. RFC 8032 square-root
recovery returns the coordinate with the requested parity, the curve equation
holds, and re-encoding returns the identical 32 bytes for all four rows.

## 5. Point-order calculations

The author calculation produced these diagnostic encodings. They are operation
results, not additional `TRI2-VEC-02` candidate rows.

| Row | `[2]P` | `[4]P` | `[8]P` | `[L]P` |
|---|---|---|---|---|
| 01 | `0000000000000000000000000000000000000000000000000000000000000080` | `ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f` | `0100000000000000000000000000000000000000000000000000000000000000` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85` |
| 02 | `0000000000000000000000000000000000000000000000000000000000000000` | `ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f` | `0100000000000000000000000000000000000000000000000000000000000000` | `26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05` |
| 03 | `0000000000000000000000000000000000000000000000000000000000000000` | `ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f` | `0100000000000000000000000000000000000000000000000000000000000000` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa` |
| 04 | `0000000000000000000000000000000000000000000000000000000000000080` | `ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f` | `0100000000000000000000000000000000000000000000000000000000000000` | `c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a` |

For every row:

- `P != I` because its encoding differs from the canonical identity and its
  decoded coordinates differ from `(0,1)`;
- `[4]P` is the canonical order-two point, not the identity;
- `[8]P` is the canonical identity; therefore the point has exact order eight;
  and
- `[L]P` is one of the other nonidentity rows, so `[L]P != I`.

## 6. Two author-side calculation routes

The same inputs were evaluated with two separately expressed group-operation
routes in one authoring session.

Route A used the complete affine formulas:

```text
x3 = (x1*y2 + x2*y1) / (1 + d*x1*x2*y1*y2)
y3 = (y1*y2 + x1*x2) / (1 - d*x1*x2*y1*y2)
```

Route B used extended coordinates `(X,Y,Z,T)` with:

```text
A=(Y1-X1)*(Y2-X2)  B=(Y1+X1)*(Y2+X2)
C=2*d*T1*T2        D=2*Z1*Z2
E=B-A  F=D-C  G=D+C  H=B+A
(X3,Y3,Z3,T3)=(E*F,G*H,F*G,E*H)
```

Both routes used binary scalar multiplication from `I` and agreed on `[4]P`,
`[8]P`, and `[L]P` for all four rows. This agreement reduces a single-formula
transcription risk, but it is still author evidence because the same author
selected the inputs, constants, and comparison. It does not count as the
required fresh independent verification.

## 7. Strict rejection derivation

The frozen strict profile requires a decoded nonidentity public key `A` to
satisfy `[L]A = I` and a decoded nonidentity signature point `R` to satisfy
`[L]R = I`. Every row instead has `[L]P != I`.

Thus all four rows reject as `A` at strict public-key step 5 and reject as `R`
at strict signature step 3. This conclusion follows from the strict predicate
and the author point-order results; a fresh reviewer must reproduce both the
point results and the predicate mapping.

## 8. Reproduction and evidence limit

A fresh verifier must not treat this document's intermediate values as an
answer key. Starting from the authenticated constants and RFC formulas, the
verifier must independently:

1. solve the order-eight equation and identify the field-valid roots;
2. construct all four bytes from y and x parity;
3. decode and re-encode every literal canonically;
4. reproduce the identity, `[4]`, `[8]`, and `[L]` results;
5. establish pairwise distinction; and
6. map each result to both strict rejection paths.

No executable generator or production cryptographic code is frozen here. No
private key, signature, fixture, oracle, E0 run, or S0 run was created.
