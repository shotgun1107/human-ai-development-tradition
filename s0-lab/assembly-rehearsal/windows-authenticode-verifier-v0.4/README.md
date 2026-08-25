# S0 PUBLIC Windows Authenticode verifier implementation candidate v0.4

This directory preserves v0.3 unchanged and contains the bounded v0.4
revision responding to `BRM-AUTHV03-IR-001` from the v0.3 independent code
and security rereview.

## Chain-context ownership correction

The chain builder establishes local ownership state before
`CertGetCertificateChain` and enters a cleanup-protected `try` immediately
after the API returns. A non-null returned context therefore remains locally
owned while return-time UTC and QPC values are sampled and while the chain is
parsed and serialized.

The `finally` block frees a non-null context exactly once on API failure or
any later exception while ownership remains local. A null context is not
freed. On success, ownership transfers to the caller, which performs its one
normal cleanup.

Focused PUBLIC fake-API tests cover post-return QPC failure, API failure with
non-null and null contexts, parsing failure without double-free, successful
transfer followed by caller cleanup, and an AST ownership-guard assertion.
These are author-side revision tests, not independent finding closure.

## Acquisition and producer authority

The exact volume-GUID acquisition path, supplied-handle path, and private-
lease path remain ordinal-equal candidate-side checks. The acquisition
producer remains an external CONTROL authority: these comparisons do not
prove when the producer sampled the path or authenticate the producer itself.

The verifier-owned `GENERIC_READ`/`FILE_SHARE_READ` lease remains open through
WinTrust and hashing. Package import remains inert, and disk manifests provide
only `TRUSTED-HOST-DISK-CONSISTENCY-ONLY` evidence. Executed-code, process,
effective-trust, and live authority remain false.

## Clock and freshness boundary

QPC remains authoritative for monotonic chain-call duration and the
conservative freshness margin. UTC and QPC endpoint intervals are compared
using exact integer arithmetic; endpoint divergence beyond the two-second
tolerance fails closed.

Endpoint comparison cannot observe a fully cancelling intermediate wall-clock
excursion that returns to the same net UTC interval before the return sample.
No claim is made that every backward-then-recover wall-clock excursion is
detectable.

## Verification boundary and status

The TEST role directly ran:

`python -I -B -m unittest discover -s s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.4/tests -v`

Result: 23 tests run, 21 passed, 2 skipped, and zero failures or errors. The
run produced no bytecode and invoked no live native, certificate-store,
network, build, or candidate-process operation.

This direct result predates the later `authority.py` namespace correction. No
tests have been rerun after that CODE change. The full manifest-bound
`verify_candidate.py` run remains pending for the TEST role after this
documentation and manifest cascade. This v0.4 revision remains a candidate
requiring fresh independent code and security rereview.

No real signature, certificate, timestamp, revocation response, Windows trust
state, network response, build, runtime materialization, rehearsal, F0 role,
S0, or E0 result is claimed. No live-artifact gate is authorized.
