# TRI2-VEC-02 review input boundary revision v0.3

- `status`: public review-control revision candidate
- `current_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR REVIEW INPUT BOUNDARY REVISION OPEN`
- `responds_to`: `independent-verification-v0.3.md`
- `responds_to_sha256`: `205caf14d8984d299f3a2545ed04328f53a4c6eac229009b1035b72fdc6f3ef1`
- `scope`: replace ambiguous semantic marker checks with exact byte assertions and synthetic preflight
- `transport_profiles_changed`: no
- `canonical_body_changed`: no
- `slice_ranges_changed`: no
- `vector_bytes_changed`: no
- `author_derivation_changed`: no
- `independent_verification_performed`: no

## 1. Trigger and exact defect

The authenticated v0.3 independent verification returned `INVALID-REVIEW`
before emitting either RFC slice, starting independent vector arithmetic, or
opening the candidate and author derivation. It passed the exact raw/canonical
body checks, both slice length/hash checks, and the parameter-slice first-
heading check. It then terminated at `P_MARKER_FAILED`.

The v0.2 boundary required the parameter slice to contain the published `p`,
`d`, and `L` definitions, but the controlling brief described one check only
as the "published-`p` marker". Neither document froze the exact marker byte
array, relative offset, occurrence count, or comparison algorithm. A reviewer
could therefore construct a plausible but absent expression such as
`p = 2^255 - 19`, use regex semantics for `^`, or otherwise disagree with the
author about what constituted the same semantic marker even though the full
slice hash already matched.

The official parameter table actually contains the literal ASCII bytes for
`2^255 - 19` inside a table row, not the expression `p = 2^255 - 19`. This
revision removes that interpretation gap. It changes no source identity,
slice, candidate byte, derivation, curve claim, point-order claim, or strict-
profile rule.

## 2. Replacement map

After this v0.3 pair and the v0.4 brief pair are canonical, committed, and
published at one exact candidate commit:

- this v0.3 boundary replaces v0.2 as current transport/marker authority;
- `tri2-vec-02-independent-verification-brief-v0.4.md` replaces the v0.3
  brief as current procedural authority;
- v0.1 and v0.2 boundary revisions, v0.1 through v0.3 briefs, and all three
  `INVALID-REVIEW` reports remain immutable historical evidence but are
  excluded from the fresh review's substantive input set; and
- the candidate vector artifact and public derivation remain byte-identical.

No predecessor may be overwritten, normalized retroactively, or treated as a
passing vector review.

## 3. Sole source, raw profiles, and canonical identity

The sole external source remains:

`https://www.rfc-editor.org/rfc/rfc8032.txt`

Only direct in-memory response-body bytes from that exact HTTPS URL are
allowed. Search, browser, HTML, rendered text, clipboard, cache, mirror, local
copy, and alternate source are forbidden.

Before normalization, exactly one complete profile must match:

| Profile | Length | SHA-256 | Line-ending shape |
|---|---:|---|---|
| `RFC8032-WIRE-LF-1` | 103,210 | `ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3` | 3,363 LF, zero CR |
| `RFC8032-WIRE-CRLF-1` | 106,573 | `f13ab006baa1a30a7835113927e9d23ca9d9c460f352e721cbcdff8adbf1dee9` | 3,363 CRLF, zero bare LF, zero bare CR |

Require HTTP success, exact final URL with redirects disabled, media type
`text/plain`, ASCII-only bytes, no UTF-8 BOM, and no NUL. Leave the LF profile
unchanged. Replace every exact CRLF pair in the CRLF profile with one LF byte.
Perform no other transformation. The result must be:

```text
profile = RFC8032-CANONICAL-LF-1
length = 103210
sha256 = ed63657ff389301282b169b0abde9b5dd2c7e4d524fdfa5da6ff3094fc93c4c3
line_endings = 3363 LF, zero CR
```

Any other raw or canonical representation is terminally invalid.

## 4. Exact canonical slices

Only these two half-open ranges of the canonical LF body may be formed:

| Slice | Range | Length | SHA-256 |
|---|---|---:|---|
| `PARAMETER-1` | `[19245:22067]` | 2,822 | `a2ee2379339d2d9e81fc04d92411347edd7da98bbf2fb92983f299f4dddd7b08` |
| `ENCODING-ADDITION-1` | `[22915:27092]` | 4,177 | `5e87337157810b1420fa543727fb74dbdecc7510b004a1100d9a58bcd7bc916d` |

The full body, gap, adjacent sections, and all other ranges may be hashed or
scanned only to enforce the boundary. They must never be emitted to the
reviewer's reasoning context.

## 5. Exact marker byte contract

Marker matching is byte equality, not text interpretation. For each row:

1. decode the listed lowercase hex into one byte array without adding a
   terminator;
2. require the declared byte length;
3. count every exact, potentially overlapping occurrence in the designated
   slice using ordinal byte-for-byte equality;
4. for required rows, require exactly one occurrence beginning at the exact
   zero-based relative offset; and
5. for forbidden rows, require zero occurrences and no offset.

Do not use regex, wildcard, case folding, line parsing, Unicode decoding,
whitespace normalization, a reconstructed formula, or a reviewer-selected
marker. The readable label is explanatory; the hex bytes, slice, offset,
length, and count jointly define the assertion.

### 5.1 `PARAMETER-1`

| ID | Meaning | Relative offset | Length | Count | Exact lowercase hex |
|---|---|---:|---:|---:|---|
| `P-H1` | section 5.1 heading | 0 | 40 | 1 | `352e312e20204564323535313970682c20456432353531396374782c20616e642045643235353139` |
| `P-P` | literal `2^255 - 19` | 356 | 10 | 1 | `325e323535202d203139` |
| `P-D` | literal `-121665/121666` | 940 | 14 | 1 | `2d3132313636352f313231363636` |
| `P-L` | literal `2^252+27742317777372353535851937790883648493` | 1,559 | 44 | 1 | `325e3235322b3237373432333137373737333732333533353335383531393337373930383833363438343933` |
| `P-NO-511` | forbidden section 5.1.1 heading | none | 26 | 0 | `352e312e312e20204d6f64756c61722041726974686d65746963` |

### 5.2 `ENCODING-ADDITION-1`

| ID | Meaning | Relative offset | Length | Count | Exact lowercase hex |
|---|---|---:|---:|---:|---|
| `E-512` | section 5.1.2 heading | 0 | 16 | 1 | `352e312e322e2020456e636f64696e67` |
| `E-513` | section 5.1.3 heading | 754 | 16 | 1 | `352e312e332e20204465636f64696e67` |
| `E-514` | section 5.1.4 heading | 2,233 | 22 | 1 | `352e312e342e2020506f696e74204164646974696f6e` |
| `E-NO-511` | forbidden section 5.1.1 heading | none | 26 | 0 | `352e312e312e20204d6f64756c61722041726974686d65746963` |
| `E-NO-515` | forbidden section 5.1.5 heading | none | 22 | 0 | `352e312e352e20204b65792047656e65726174696f6e` |

The exact full-slice SHA-256 remains the primary byte-identity proof. These
rows are deterministic semantic-boundary checks; they cannot replace or waive
the full-slice hash.

## 6. Synthetic checker preflight

Before the sole live RFC request, the reviewer may develop and retry an
ephemeral checker only against synthetic byte arrays. This preflight is not a
source attempt and supplies no review evidence until all cases pass.

The checker must at minimum prove that it:

- counts overlapping exact byte subsequences and reports their offsets;
- distinguishes ASCII `0x5e` from regex or exponent syntax;
- accepts an exact marker at offset zero and at a nonzero offset;
- returns zero for an absent marker;
- rejects wrong offset, length, count, and one-bit-changed hex;
- canonicalizes synthetic CRLF to LF byte-for-byte;
- rejects bare CR and a profile with mixed line endings; and
- extracts half-open byte slices without an inclusive-end error.

Syntax, shell-quoting, or local assertion defects may be corrected only during
this synthetic preflight. After all preflight cases pass and the checker
issues the live HTTPS request, there is exactly one source attempt. A live
transport, profile, canonical, slice, marker, exclusion, or output-boundary
failure is terminal `INVALID-REVIEW` without corrected retry or fallback.

## 7. Live fail-closed procedure

The one live pipeline must, before emitting any source text:

1. establish one exact raw profile and all HTTP/ASCII/BOM/NUL constraints;
2. canonicalize by the sole profile rule and establish the complete canonical
   identity;
3. form both exact ranges and establish both complete slice identities;
4. execute every marker row in section 5 by exact byte comparison;
5. emit one bounded machine-readable audit containing only profile ID,
   lengths, hashes, marker IDs, offsets, lengths, counts, and pass/fail; and
6. only if every assertion passes, emit the two slices and no other source
   bytes.

Diagnostic metadata may not contain RFC source text. If a live failure occurs,
the audit must identify the exact failed row or stage without emitting a slice
or using a second request.

## 8. Independence order

A fresh reviewer must authenticate the supplied repository inputs, read the
controlling v0.4 brief and this boundary, pass the synthetic checker preflight,
read only admitted non-author authority, and complete the live source pipeline.
Before opening the candidate vector or author derivation, it must independently
freeze numeric `p`, `d`, `L`, every algebraic branch, coordinate, parity,
encoding, point-order check, and strict `A`/`R` rejection check required by the
brief.

Only then may it open the author documents for exact comparison. Predecessor
invalid reviews, predecessor boundaries/briefs, reviewer memory, library
labels, and candidate prose cannot supply a missing value.

## 9. Author-side bounded QA and evidence limit

CONTROL checked the current official LF body and the exact CRLF expansion on
2026-08-11 KST. Both produced the frozen canonical body, both slice hashes,
and every exact byte row above. This is author-side boundary QA only. It is not
independent source evidence, vector arithmetic, or a candidate result.

No candidate, derivation, point, key, signature, fixture, oracle, protected
material, provider/model session, E0, S0, implementation, central system,
Project Brain integration, operational-safety claim, economic-value claim, or
`main` integration was opened or authorized.

## 10. Exact next gate

After this pair and the v0.4 brief pair are canonical, frozen at one exact
candidate commit, independently QA-checked, and published, the maximum next
gate is a separately opened:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`

No review or later gate opens automatically.
