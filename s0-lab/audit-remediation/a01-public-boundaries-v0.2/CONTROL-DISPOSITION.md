# A01 v0.2 CONTROL disposition

CONTROL decision: `ACCEPT-BOUNDED-F02-DELETE-FLAG-AND-F04-REGRESSION`.

DOCUMENTATION records the review result and decision supplied by CONTROL; this document is not a DOCUMENTATION-authored independent review. It is a later record outside the frozen 18-entry manifest. The original README's review-pending status remains truthful at its freeze.

- Candidate: `a01-public-boundaries-v0.2`.
- Frozen manifest SHA-256: `c26f8a02c4dc306e9639dfefd26ee8e41793ffb45998b84c7c2841490772f972`.
- Frozen README SHA-256: `f758d67703bcab5870fd42232dfbe4caa42090a37a18d37c62bb3754d09d3216`.
- Runtime guard SHA-256: `811f1df27a44d70948f3e37fedcba976189fd5b58ff61a6e029c14d74c768f7a`.
- Branch: `codex/windows-build-toolchain-environment-v0.1`; HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.

Fresh read-only reviewer `/root/audit_a01_v02_review` returned primary PASS with no findings for the frozen narrow Windows delete-on-close claim. CONTROL reports that the reviewer authenticated Git identity, policy, both manifests, validator, README and all 18 entries, with zero hash mismatches at final recheck and a valid sidecar. The reviewer did not rerun substantive tests or canonical validation, write files, execute native validation, access network services, or read F0 content.

The review verified independent legacy-integer and third-argument flag checks at runtime-guard lines 217–225, with latched denial before approved-read or pending-output allowances at lines 241–254. Existing `None` validation and ordinary classification remain at lines 213–230. The other eight implementation files remain unchanged.

Reviewed evidence covers `None`, integer, string-plus-third-flags and conflicting representations; three path classes; invalid flags; and 18 actual delete-flag child cases carrying flag 64. Those cases record delete-denial messages, later read/health latching and intact parent-observed bytes. Ordinary reads, storage reads and pending writes retain their tested behavior. Counts agree: 26 tests, 332 subtests, 31 child observations, 36 F-04 API-double observations, zero failures/errors/skips and zero scratch residue. Unchanged F-04 source/test evidence covers EOF/non-EOF handling, close failures, error capture, alternate-stream rejection and rejection classes.

Acceptance covers only this path-open flag contract and bounded regressions. Descriptor authority, hostile globals/introspection, interpreter/import closure, future flags, other platforms, hostile concurrency, Windows ACL/root/reparse/retained-handle/TOCTOU lifecycle, and output/evidence-producer security remain **UNVERIFIED**. No full controller/native/runtime integration, S0/E0, OS sandbox, general security, operational-safety, economic-value or model-transfer claim is established.

Timing disclosure: the user-approved continuation carried a 10–20 minute estimate starting approximately 07:18 UTC on 2026-09-16. Fresh review finished approximately 07:40 UTC, about 22 minutes later, so the estimate was exceeded. CONTROL reports informing the user of that overrun; only final review evidence crosschecks and this decision record continued, with no new correction or expanded scope. This record does not retroactively change the freeze or claim the estimate was met.

F0 access restrictions and the one opaque unclassified Git-status blocker remain unchanged. This decision grants no staging, commit, push, PR, merge, installation, model/provider execution or experimental gate. The project remains in `central-system-v2.1-s0-preparation`.

DOCUMENTATION reauthenticated all 18 frozen entries before creating this record. Its same-basename sidecar is checked with the already self-tested canonical Windows PowerShell validator; actual validation outcome and both new hashes are supplied in the documentation handoff.
