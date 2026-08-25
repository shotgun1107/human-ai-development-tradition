# S0 PUBLIC Windows Authenticode verifier implementation candidate v0.3

This directory preserves v0.2 unchanged and contains the bounded v0.3
revision responding to the three findings in the v0.2 independent code and
security rereview.

## Acquisition path authority

The externally pinned canonical acquisition record now includes:

- `acquired_path`, produced by `GetFinalPathNameByHandleW` with
  `FILE_NAME_NORMALIZED | VOLUME_NAME_GUID`; and
- an exact path-semantics identifier fixing volume-GUID form, ordinal-exact
  comparison, and no alternate data stream.

The record rejects non-volume-GUID paths, ADS syntax, forward slashes,
embedded nulls, wildcard characters, empty or dot segments, and trailing
space or dot normalization ambiguity.

The collector obtains the same volume-GUID final path independently from the
supplied retained handle and the verifier-owned lease. Acquisition record,
supplied handle, and lease paths must be exact equal. A hard-link alias,
rename, case-only path change, reparse-derived alternate name, or ADS path
therefore rejects unless it is the exact final path pinned by acquisition.

The caller's `full_path` is used only to open the lease; the lease final path
must still equal the acquisition authority path.

## Exceptional store-context ownership

Certificate and CTL enumeration keeps the current returned context under
explicit local ownership. If encoding, size, entry-bound, or another
processing check raises before the context is passed back to the next
enumeration call, cleanup invokes `CertFreeCertificateContext` or
`CertFreeCTLContext` before closing the store.

Cleanup attempts every applicable context free and store close even when one
operation reports failure, then rejects. PUBLIC fake-API tests count the
certificate, CTL, and store cleanup calls on success and failure paths.

## Monotonic freshness interval

Each `CertGetCertificateChain` call is bracketed by both:

- fixed-hex UTC FILETIME start and return values; and
- fixed-hex `QueryPerformanceCounter` frequency, start, and return values.

The freshness margin and 30-second duration bound use the ceiling of QPC
elapsed time. The semantic validator also compares UTC elapsed time with QPC
elapsed time using exact integer cross-products and a two-second tolerance.
QPC reversal, duration overrun, UTC reversal, and hidden backward-then-recover
clock discontinuity all reject.

Large FILETIME and QPC values remain 16-hex JSON text, so the v0.2 JSON exact-
integer correction is preserved.

## Preserved v0.2 boundaries

The verifier still requires externally pinned implementation, acquisition-
record, and acquisition-producer manifest hashes. Its private
`GENERIC_READ`/`FILE_SHARE_READ` lease remains open through all WinTrust and
hash work. VERIFY/CLOSE and chain-context ownership remain fail-closed.

Package import remains inert. Disk manifests establish only
`TRUSTED-HOST-DISK-CONSISTENCY-ONLY`; executed-code and process authority stay
false. The six-store snapshot remains an observed mutation sentinel with
`effective_trust_authority_claimed=false`.

A positive 44-relation result remains
`PASS-BOUNDED-TRUSTED-HOST-CONSISTENCY-NO-LIVE-AUTHORITY`. It cannot authorize
a live-artifact gate.

## Verification boundary

The PUBLIC suite exercises path grammar and path substitution, acquisition
pins, immutable lease drift, certificate/CTL exceptional cleanup, QPC and UTC
interval substitution, freshness, lifecycle, bounds, authority nonclaims, and
all preserved v0.2 hostile cases.

No test calls a Windows trust API, opens a real certificate store, accesses a
network, downloads a file, launches a candidate, installs software, builds,
or grants process authority. No real signature, certificate, timestamp,
revocation response, trust state, runtime materialization, rehearsal, F0, S0,
or E0 result is claimed.
