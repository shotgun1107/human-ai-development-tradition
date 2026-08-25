# S0 PUBLIC Windows Authenticode verifier implementation candidate v0.2

This directory preserves v0.1 unchanged and contains the bounded v0.2
revision responding to the six findings in the v0.1 independent code and
security review.

## Authority boundary

The trusted-host entry requires three externally pinned inputs before native
collection:

- the v0.2 outer implementation-manifest SHA-256;
- one canonical acquisition-record SHA-256; and
- the manifest SHA-256 of the acquisition-record producer.

The acquisition record binds the fixed request and final URL, zero redirects,
completed transfer, same-process retained-handle value, read-only/no-write-or-
delete-sharing handle contract, file ID, volume serial, non-reparse status,
byte length, and SHA-256. The verifier recomputes the record hash rather than
accepting caller fields independently.

The producer manifest and record pins are external CONTROL authorities. This
package does not authenticate or execute the producer implementation itself.

## Immutable verification lease

After authenticating the acquisition record, the native collector opens its
own `GENERIC_READ` handle with only `FILE_SHARE_READ`. Under the documented
Windows sharing contract, this open fails when an existing write/delete handle
or writable mapping conflicts, and it prevents new write/delete opens while
the lease remains active.

The collector compares the supplied handle, acquisition record, and private
lease by path, volume serial, 128-bit file ID, length, reparse status, and
SHA-256. All WinTrust work and all later hashes use only the verifier-owned
lease. Hashing uses `ReadFile` on that owned handle and does not duplicate a
shared file pointer.

## Native lifecycle and bounds

Every `WTD_STATEACTION_VERIFY` invocation enters cleanup before the returned
state is inspected. `WTD_STATEACTION_CLOSE` is therefore called even when the
state handle is null or later parsing fails. Every returned chain context is
owned and freed locally until successful ownership transfer, then freed by the
outer lifecycle.

Explicit PUBLIC bounds cover candidate bytes, certificate bytes, CTL bytes,
provider and rebuilt chain counts, store entries, observation bytes, URL
retrieval time, revocation age, and chain-call duration.

## Time and trust-state semantics

All Windows `FILETIME` values are serialized as fixed lowercase 16-hex text,
not JSON numbers. Each chain call records a before/after clock interval and
the exact `pftCacheResync` input. Freshness is accepted only when the Windows
age plus the complete call interval remains within the project maximum. The
implementation does not claim that Windows returned one exact revocation
reference instant.

The before/after store snapshot enumerates local-machine Root, CA, My, Trust,
AuthRoot, and Disallowed certificates and CTLs. Enumeration accepts only the
documented end status; all other errors and every store-close failure reject.
The snapshot is explicitly an observed-input mutation sentinel:
`effective_trust_authority_claimed=false`. Actual chain and policy results
remain separately mandatory.

## Runtime nonclaim

Package import is inert, but direct Python module execution still occurs in a
mutable trusted host. Disk manifests therefore establish only
`TRUSTED-HOST-DISK-CONSISTENCY-ONLY`.

Every result fixes:

- `executed_code_authority_established=false`; and
- `process_authority_granted=false`.

A positive 44-relation result is
`PASS-BOUNDED-TRUSTED-HOST-CONSISTENCY-NO-LIVE-AUTHORITY`. It does not
authorize a live artifact gate. A separately authenticated pre-import loader,
interpreter, and isolated execution boundary remain future work.

## Verification boundary

The PUBLIC suite uses canonical synthetic acquisition and native observations.
It exercises acquisition-pin substitution, URL/handle/file/hash drift,
immutable-lease contract drift, lifecycle ordering, chain and policy binding,
time-interval reversal and overrun, conservative revocation freshness,
store-snapshot failure claims, bounds, runtime-authority nonclaims, and
deterministic fail-close behavior.

No test calls a Windows trust API, opens a certificate store, accesses a
network, downloads a file, launches a candidate, installs software, builds,
or grants process authority. No real signature, certificate, timestamp,
revocation response, trust state, runtime materialization, rehearsal, F0, S0,
or E0 result is claimed.
