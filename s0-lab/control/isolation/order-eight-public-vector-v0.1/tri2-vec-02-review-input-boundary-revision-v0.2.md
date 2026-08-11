# TRI2-VEC-02 review input boundary revision v0.2

- `status`: public review-control revision candidate
- `current_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN`
- `responds_to`: `independent-verification-v0.2.md`
- `responds_to_sha256`: `1214e3b30e0002210b3e1fa2ffa5aad2443786284320bea98e5240daef7baaf3`
- `scope`: repair official-source transport identity while retaining independent numeric `d` authority
- `vector_bytes_changed`: no
- `author_derivation_changed`: no
- `independent_verification_performed`: no

## 1. Trigger, facts, and bounded conclusion

The authenticated v0.2 independent verification returned `INVALID-REVIEW`
before any RFC slice, vector arithmetic, candidate comparison, or row judgment.
The official RFC Editor response observed by that reviewer was an LF-only
103,210-byte body with SHA-256
`ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3`.
The v0.1 boundary instead required a 106,573-byte body with SHA-256
`f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9`.

The same review established, without exposing either prescribed slice, that
the latter identity is exactly the former body after replacing each of its
3,363 LF line endings with CRLF. This explains the mismatch but did not waive
the frozen raw-response rule.

CONTROL repeated a bounded public transport check on 2026-08-11 KST. The
official URL returned HTTP 200 `text/plain`, 103,210 ASCII bytes, 3,363 LF
line endings, no CR byte, and the same `ed63657...` SHA-256. Deterministic CRLF
expansion reproduced the exact 106,573-byte `f13ab006...` predecessor value.
No vector coordinate, encoding, curve operation, point order, or strict
rejection was calculated or assessed in this author-side check.

The bounded conclusion is that v0.1 froze a line-ending representation as if
it were the sole wire representation. The content authority was not shown to
be wrong. This revision therefore admits only two byte-exact representations
of the same official ASCII text, canonicalizes them by one exact rule, and
freezes all later slicing against the canonical LF bytes.

## 2. Replacement map

After this v0.2 pair and the v0.3 brief pair are canonical, committed, and
published at one exact candidate commit:

- this v0.2 boundary replaces
  `tri2-vec-02-review-input-boundary-revision-v0.1.md` as current transport
  authority;
- `tri2-vec-02-independent-verification-brief-v0.3.md` replaces the v0.2 brief
  as current procedural authority;
- the v0.1 boundary, v0.2 brief, and both `INVALID-REVIEW` reports remain
  immutable historical evidence but are excluded from the fresh review's
  substantive input set; and
- the vector candidate and public derivation remain byte-identical and are not
  amended or endorsed by this revision.

No predecessor artifact may be overwritten, retroactively normalized, or
reinterpreted as a passing review.

## 3. Sole official source and accepted raw profiles

The only external source is the RFC Editor plain-text publication:

`https://www.rfc-editor.org/rfc/rfc8032.txt`

The reviewer must obtain response-body bytes directly from this exact HTTPS
URL. Search results, browsers, HTML pages, rendered text, clipboard content,
cached snippets, mirrors, local copies, author copies, and alternate sources
are forbidden.

Before normalization, exactly one of these two complete raw profiles must
match:

| Profile | Length | SHA-256 | Exact line-ending shape |
|---|---:|---|---|
| `RFC8032-WIRE-LF-1` | 103,210 | `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3` | 3,363 LF, zero CR |
| `RFC8032-WIRE-CRLF-1` | 106,573 | `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9` | 3,363 CRLF, zero bare LF, zero bare CR |

For either profile, every byte must be ASCII, the first three bytes must not
be an UTF-8 BOM, and no NUL byte may occur. A response that matches neither
complete length/hash/line-ending profile is terminally invalid. The reviewer
must not add another profile, trim bytes, decode and reserialize text, repair
mixed endings, follow a semantic fallback, or continue after failure.

The two profiles are not competing source authorities. They are two exact
line-ending representations whose equivalence is independently checkable by
the canonicalization rule below.

## 4. Canonical LF identity and permitted slices

Canonicalization is byte-defined:

1. `RFC8032-WIRE-LF-1` is unchanged.
2. For `RFC8032-WIRE-CRLF-1`, replace each exact `0x0d 0x0a` pair with one
   `0x0a` byte.
3. Perform no other decoding, replacement, trimming, insertion, deletion, or
   Unicode normalization.

The result must match this single canonical identity before any slice is
formed or emitted:

```text
canonical_profile = RFC8032-CANONICAL-LF-1
canonical_length = 103210
canonical_sha256 = ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3
canonical_lf_count = 3363
canonical_cr_count = 0
```

Only the following half-open byte ranges of the canonical LF body may be
emitted to the reviewer's reasoning context.

### 4.1 Parameter-table slice

```text
python_half_open_range = [19245:22067]
inclusive_byte_range = 19245-22066
length = 2822
sha256 = a2ee2379339d2d9e81fc04d92411347edd7da98bbf2fb92983f299f4dddd7b08
first_heading = 5.1.  Ed25519ph, Ed25519ctx, and Ed25519
```

This slice must contain the RFC definitions `2^255 - 19`,
`-121665/121666`, and
`2^252+27742317777372353535851937790883648493`. It supplies independent
primary-source authority for numeric `p`, `d`, and `L`. It must not contain
the actual `5.1.1.  Modular Arithmetic` heading.

### 4.2 Encoding-through-addition slice

```text
python_half_open_range = [22915:27092]
inclusive_byte_range = 22915-27091
length = 4177
sha256 = 5e87337157810b1420fa543727fb74dbdecc7510b004a1100d9a58bcd7bc916d
first_heading = 5.1.2.  Encoding
```

This slice must contain the actual `5.1.2.  Encoding`, `5.1.3.  Decoding`, and
`5.1.4.  Point Addition` headings. It must contain neither the actual 5.1.1
heading nor the actual `5.1.5.  Key Generation` heading.

The gap, full body, adjacent sections, and bytes outside these two ranges must
never be emitted to the reviewer context. Hashing and scanning the unexposed
body solely to enforce this boundary is transport validation, not semantic
review input.

## 5. Deterministic fail-closed transport procedure

The fresh reviewer must use one in-memory pipeline that, before emitting any
text:

1. requires a successful response from the exact HTTPS URL and media type
   `text/plain`;
2. checks ASCII, BOM, NUL, complete length, complete SHA-256, and exact
   line-ending shape against one and only one raw profile in section 3;
3. applies only the profile-specific byte canonicalization in section 4;
4. checks the complete canonical LF length, SHA-256, LF count, and CR count;
5. forms exactly the two canonical half-open byte ranges;
6. checks both slice lengths, SHA-256 values, required markers, and forbidden
   headings; and
7. emits only those two slices.

The raw response, canonical full body, gap, and slices must remain ephemeral
and must not be written to the repository or a reusable helper artifact.
Missing, changed, redirected-to-another-source, mixed-ending, partial,
duplicated, malformed, non-ASCII, BOM-prefixed, NUL-containing, wrong-profile,
wrong-canonical, wrong-slice, wrong-marker, or extra-output data yields
`INVALID-REVIEW` without retry, alternate source, waiver, or author repair.

## 6. Independence order

A fresh reviewer must authenticate the supplied repository files, read only
the controlling v0.3 brief and non-author authority inputs, and complete the
transport procedure above. Before opening the candidate vector artifact or
author derivation, it must independently freeze in session-local notes:

- numeric `p`, `d`, and `L` reconstructed from the parameter slice;
- the curve, identity, canonical encoding/decoding, and complete addition
  rules from admitted non-author authority;
- the exact-order-eight equation and every quadratic and square-root branch;
- every independently derived coordinate, parity, and exact 32-byte encoding;
  and
- the intended decode, re-encode, pairwise-distinction, `P != I`, `[4]`, `[8]`,
  `[L]`, and strict `A`/`R` rejection checks.

Only after that freeze may it open the two author documents for exact
comparison and hostile review. The predecessor invalid reviews, predecessor
boundary, predecessor brief, reviewer memory, library labels, or candidate
prose cannot supply a missing precomputed value.

## 7. Nonclaims and closed gates

This revision changes only public review-input transport and procedural
authority. It does not change or validate any candidate byte, derivation,
point order, strict predicate, role topology, signer, store, edge, provider,
or S0 protocol rule.

It creates no vector pass or freeze; no implementation, reusable helper,
generator, key, signature, fixture, bank, label, oracle, protected material,
provider/model session, E0 run, S0 run, central-system implementation, Project
Brain integration, operational-safety claim, economic-value claim, or `main`
integration authority.

## 8. Exact next gate

After this pair and the v0.3 brief pair are canonical, frozen at one exact
candidate commit, independently QA-checked, and published, the maximum next
gate is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`

No review or later gate opens automatically.
