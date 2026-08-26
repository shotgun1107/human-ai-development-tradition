# S0 public external-pin recovery implementation v0.2 result preservation

This directory contains the bounded PUBLIC v0.2 revision of the external-pin
recovery implementation candidate for the build/runtime materialization
assembly rehearsal. The implementation gate was:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.2 REVISION OPEN`

The current result-preservation gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.2 INDEPENDENT CODE AND SECURITY REREVIEW RESULT PRESERVATION OPEN`

## Preserved outcome

The authenticated TEST handoff reports that the isolated verifier passed its
frozen 10-file source-and-test hash check before and after execution, ran the
exact 11 foundation and 8 materialization-security tests, observed zero
failures, errors, skips, or expected failures, and detected both mutation and
path-and-byte-swap sentinels. It authenticated the pinned candidate and test
bytes through an in-memory loader, rejected recursive inventory anomalies, and
exited 0 with status
`verified-candidate-test-bytes-under-unverified-host-runtime`. The interpreter
bytes and identity remained stable during the run, but the interpreter,
standard library, site, platform, and OS-DLL closure remain unverified. Host
runtime authority is `UNAUTHENTICATED` and its role is
`TRUSTED-PREREQUISITE`; only the candidate and test bytes are authenticated.

A fresh live acquisition run used an ephemeral root outside the repository and
derived the authenticated verifier-record digest internally rather than
accepting a caller-supplied digest. It exited 0 with status
`completed-blocked-nonexecuting`. The CPython 3.12.10
embeddable ZIP matched its frozen SHA-256, was authenticated, and was
materialized as 35 inert files. The archive and all 35 outputs were
final-reauthenticated. No acquired byte was executed, imported, installed,
compiled, or linked. All eight candidate modules were loaded only from
`<authenticated-memory>` after inventory and byte authentication, with no
repository-path fallback. The live harness, interpreter, standard library,
platform, OS-DLL, and network-stack closure remain unverified; runtime and
producer authority are `UNAUTHENTICATED` and `TRUSTED-PREREQUISITE`. Cycle 4
created the fresh external root exclusively, retained its identity for the
full lifecycle, used handle-relative evidence and sidecar writes, and
final-reauthenticated both records. The root identity remained stable and the
root persisted after handle close; no path fallback or deletion occurred.

The Visual Studio Build Tools bootstrapper was acquired but remains
`acquired-unauthenticated`. Its observed digest is evidence about the acquired
bytes only and was not promoted to pin or authentication authority. Its
authoritative expected digest and expected size remain absent. The jsonschema
source remains unavailable.

## Blocked state

The candidate remains blocked by 17 fixed-list candidate blockers and 4
live-specific blockers. Here, "fixed-list" means the statically defined list;
it does not mean that the blockers have been resolved. The exact lists and
evidence records are preserved in `STATUS_REPORT.md` and
`evidence-manifest.json`.

All process, installation, build, runtime, rehearsal, S0, and E0 claim and
validation states remain false. The live acquisition and inert materialization
do not authorize or validate any of those operations.

## Evidence boundary

The live external root is represented in PUBLIC artifacts only as
`<OUT-OF-REPOSITORY-EPHEMERAL-ROOT>`. The downloaded bytes, materialized files,
live evidence JSON, and its companion sidecar remain outside the repository.
This directory preserves their authenticated public identities and bounded
results, not the external files themselves.

The verification evidence SHA-256 is
`76d062c28817e09a8e2b10fc30b8bf7cee93ea00e5678c5e519007ddfc9c087e`.
The live evidence JSON SHA-256 recorded by its external companion sidecar is
`ee25ce05a42132f821ddaa7e682914fa65201bd25ea262a8e0cd7aaf7932ebaf`.
The external sidecar file SHA-256 is
`7681768362c98777cf64a1477574caddbffb48602dc77254319706776a7fbd95`.

Fresh independent review cycle 1 returned `REVISE-AND-REREVIEW` with 0
BLOCKING, 2 MAJOR, and 1 MINOR findings. It closed the bounded path/parent and
stable-identity/final-reauthentication review findings, while retaining open
findings for mutable exported pin authority and mutable verifier execution
inputs and inventory. It also identified caller-supplied verifier-digest
acceptance as MINOR. The cycle 2 implementation and TEST evidence address
those findings; at that point their closure remained unverified pending fresh
independent rereview.

Fresh rereview cycle 2 also returned `REVISE-AND-REREVIEW` with 0 BLOCKING, 2
MAJOR, and 1 MINOR findings. It closed the prior bounded findings
`BRM-EPRI01-IR-001`, `BRM-EPRI01-IR-002`, and `BRM-EPRI01-IR-003` within the
supported APIs, while `BRM-EPRI01-IR-004` remained open. The two new MAJOR
findings were the unpinned and unrecorded host-runtime closure and a live
harness repository import before hash authentication. The MINOR finding was
that the public reproduction commands omitted required evidence arguments.

Cycle 3 revised only the two TEST-owned verification scripts. The authenticated
cycle 3 evidence recorded candidate/test byte binding under an explicitly
unverified host runtime, authenticated-memory-only candidate loading in the
live harness, and complete verifier/live evidence commands.

Fresh rereview cycle 3 returned `REVISE-AND-REREVIEW` with 0 BLOCKING, 1
MAJOR, and 2 MINOR findings. It closed `BRM-EPRI01-IR-004` for the calibrated
candidate/test-byte scope, while runtime and live authority remained
explicitly absent. The MAJOR finding was that the live external-root identity
was not retained and an evidence-path reopen could rebind. The MINOR findings
were a verifier record described as pre/post despite being measured once and
direct-test reproduction commands that omitted `-S`.

Cycle 4 revises only the TEST-owned live verification script and the public
documentation. The authenticated cycle 4 evidence records retained-root and
handle-relative evidence binding, actual pre/post verifier-record rereads,
and corrected direct-test commands.

Fresh independent rereview cycle 4 authenticated 18 of 18 repository hashes
and 4 of 4 external hashes, then returned the exact verdict
`PASS-FOR-BOUNDED-WINDOWS-EXTERNAL-PIN-RECOVERY-IMPLEMENTATION-V0.2-NO-LIVE-AUTHORITY`
with 0 BLOCKING, 0 MAJOR, and 2 MINOR findings. The review was read-only,
performed no execution, did not access F0 content, and authenticated the exact
branch, HEAD, tree, and parent recorded in `STATUS_REPORT.md`.

The review closed `BRM-EPRI01-IR-001`, `BRM-EPRI01-IR-002`, and
`BRM-EPRI01-IR-003` in the bounded supported scope. It closed
`BRM-EPRI01-IR-004` only for calibrated candidate/test-byte binding under the
`UNAUTHENTICATED` / `TRUSTED-PREREQUISITE` host runtime. It also closed the
cycle 3 external-root MAJOR and both cycle 3 MINOR findings. Runtime, producer,
and live authority remain absent under `RUNTIME-PROFILE` and
`ACQUISITION-PRODUCER`.

Two reviewed MINOR findings remain. First, the published offline reproduction
command omitted its required `--verification-evidence` argument; this public
documentation defect is corrected during result preservation, after the
passing technical review. Second, the reviewed TEST harness's failed
`mklink /J` attempt against an already-existing root demonstrates
name-collision and replacement rejection, not dynamic in-place FSCTL reparse
conversion coverage. The TEST artifact remains unchanged, and this
documentation does not claim that broader coverage.

The technical cycle 4 rereview is complete. CONTROL result preservation is in
progress; independent review of the preservation-only documentation changes
is pending. No commit, push, or `main` integration is claimed or recorded here.

Maximum claim: under an unverified host-runtime and producer prerequisite, the
bounded harness authenticated the pinned candidate and test bytes, then
authenticated and inertly materialized the frozen CPython archive while
keeping all execution and downstream construction authority false. This is
not host-runtime or producer authentication, live supplier authority for Build
Tools, process authority, installation, build, runtime construction,
rehearsal, S0, E0, central-system, Project Brain integration,
operational-safety, economic-value, or model-to-model-transfer validation.
