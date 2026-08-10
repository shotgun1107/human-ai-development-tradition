# TRI2-VEC-02 review input boundary revision v0.1

- `status`: public review-control revision candidate
- `current_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN`
- `scope`: repair independent primary-source authority for Ed25519 constants only
- `vector_bytes_changed`: no
- `author_derivation_changed`: no
- `independent_verification_performed`: no

## 1. Trigger and exact defect

The authenticated independent review at commit
`dbba47b47c5c82649acfc2d839e18119344cd514` returned
`INVALID-REVIEW`. Its Markdown SHA-256 is:

`e1625e0e77dfa55571a6cad08f947d832f9cec6a80111b6ccfedc7cdf519273f`

The review did not find a substantive vector error. It found that the v0.1
review boundary admitted RFC 8032 sections 5.1.2 through 5.1.4, which define
encoding, decoding, and addition with symbolic `p` and `d`, but do not define
numeric `d`. The authenticated non-author project source defines numeric `p`
and `L`, but not numeric `d`. The only admitted numeric `d` was in the author
derivation, which cannot serve as independent authority for checking itself.

This revision repairs only that input-boundary defect. It does not adopt,
reject, recalculate, or modify any `TRI2-VEC-02` coordinate, literal, point-
order result, or strict-profile result.

## 2. Official primary source and byte identity

The only external source remains the RFC Editor plain-text publication:

`https://www.rfc-editor.org/rfc/rfc8032.txt`

CONTROL observed the exact response as:

```text
full_length = 106573
full_sha256 = f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9
```

The fresh reviewer may expose only these two disjoint slices to its reasoning
context.

### 2.1 Parameter-table slice

```text
python_half_open_range = [19710:22589]
inclusive_byte_range = 19710-22588
length = 2879
sha256 = c3ae421b10d8f0806b81686270b45c08012dc57e33ed5540a21529db5ec2bd68
first_heading = 5.1.  Ed25519ph, Ed25519ctx, and Ed25519
```

This slice contains the RFC 8032 Ed25519 parameter table, including the exact
published definitions of `p`, `d` as `-121665/121666`, and `L`. It ends before
the actual `5.1.1.  Modular Arithmetic` heading.

### 2.2 Encoding-through-addition slice

```text
python_half_open_range = [23458:27770]
inclusive_byte_range = 23458-27769
length = 4312
sha256 = 0261ec3acfb9b9fdb9e472e7baf9d4d386edafe803a707cf12e0e63280e3a67d
first_heading = 5.1.2.  Encoding
```

This slice contains actual sections 5.1.2, 5.1.3, and 5.1.4. It ends before
the actual `5.1.5.  Key Generation` heading.

The gap between the slices is intentionally not exposed. The reviewer does not
need RFC section 5.1.1 to reconstruct the required constants, encoding,
decoding, and complete point-addition calculations.

## 3. Deterministic transport rule

The reviewer must not use web search, a browser, or an RFC HTML page. Those
interfaces can expose adjacent sections. It must retrieve the official text
through a pipeline in which the HTTP response flows directly into a
deterministic byte slicer. Before emitting either slice, the slicer must:

1. assert the full response length and SHA-256 above;
2. form exactly the two half-open byte ranges above;
3. assert each slice length and SHA-256;
4. assert the parameter slice contains `-121665/121666`, `2^255 - 19`, and
   `2^252+27742317777372353535851937790883648493`;
5. assert the second slice contains the three required section headings;
6. assert neither emitted slice contains the actual 5.1.1 or 5.1.5 heading;
   and
7. emit only the two slices, never the full response or intervening bytes.

Hashing and slicing unexposed bytes is transport validation, not semantic
reading. Failure of any assertion makes the review invalid without fallback.

## 4. Independence order

After authenticating all admitted files, a fresh reviewer must read the
controlling v0.2 brief and non-author authority documents, then retrieve the
two official slices. Before opening either author candidate document, it must
independently freeze in its session notes:

- numeric `p`, `d`, and `L` reconstructed from the official parameter table;
- the order-eight equation and all root branches;
- the independently derived candidate coordinates and exact encodings; and
- the intended decode, re-encode, `[4]`, `[8]`, `[L]`, and strict-rejection
  checks.

Only then may it open the candidate artifact and author derivation for byte-
for-byte comparison and hostile review. The historical invalid review may be
used only to confirm this boundary repair; it provides no substantive vector
answer.

## 5. Replacement and non-regression

After this revision pair and the v0.2 brief pair are canonical and frozen at
one exact commit:

- `tri2-vec-02-independent-verification-brief-v0.2.md` becomes the sole current
  procedural authority for the next review;
- the v0.1 brief and v0.1 invalid review remain immutable historical evidence;
- the candidate vector artifact and public derivation remain byte-identical;
  and
- every v0.4 pre-key-generation blocker remains closed.

This revision creates no vector pass, independent result, implementation,
generator, key, signature, fixture, oracle, provider/model session, E0 run, S0
run, or `main` integration authority.

## 6. Exact next gate

After the four new public files are canonical, committed, and published, the
maximum next gate is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`

A new fresh reviewer must start from the revised authenticated baseline. No
review or later gate opens automatically.
