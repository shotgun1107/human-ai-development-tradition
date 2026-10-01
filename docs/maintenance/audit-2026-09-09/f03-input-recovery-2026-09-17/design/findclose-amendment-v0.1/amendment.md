# FindClose amendment v0.1 to the v0.5 design

Date: 2026-09-08. State: authored input awaiting TEST, fresh independent
review, and CONTROL acceptance/re-freeze. This is a bounded additive
amendment for the current corrected implementation candidate, not a global
design version or an implementation/runtime result.

CONTROL recorded the user's direction to perform its specifically proposed
FindClose-only remediation and continue the original implementation and
verification. That direction applies only to this candidate scope. It does
not amend root AGENTS, establish standing authorization, grant Git or F0
authority, or open stage 70/80 or S0. Root AGENTS remains SHA-256
`6bff2cef0ddd3ecef6e3f997ec34e9460dc4097c4d46cae73bb32f5ddc10966c`.

Base/main commit: `5ad4632e9ceec64fff53ee26bb3557e95f817d4c`; tree:
`f8221aaa04ef529ec11f3057b53efa31d02bd86e`; branch:
`codex/runtime-profile-neutral-preloader-v05-corrected-implementation`.
The worktree is `C:/Users/SSAFY/AppData/Local/Temp/rpnp05-impl-20260908`.
No amendment publication or main integration is claimed.

## Frozen inputs and effective authority

All seven base design files, their sidecars, and the base manifest remain
byte-identical. Their directory is the parent of this amendment directory.

| Artifact | SHA-256 |
|---|---|
| Base `design-package-files.sha256` | `058a8b8bcd8ed2068a6b5c0a8f3c9dc16425f51d8aaaa505b6d6d36f4fab6c98` |
| Base interface map | `83d10d27ce3f6aae21417be435691000f7583a58c86297f46b09752cc633a336` |
| Base schema | `19d63a0c0d30369aaaae051e151641af5c6cf1fc71463fadf99bc37068121364` |
| Effective `public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json` in this directory | `f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623` |
| Effective `runtime-profile-v0.5.schema.json` in this directory | `04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e` |

Authenticate the complete base package first, then this directory's
`amendment-files.sha256`, which binds this document and both effective JSON
files without hashing itself. Subject to CONTROL acceptance, this amendment
takes precedence only for the preloader's `FindClose` membership, resulting
supporting/total counts, and the necessary effective-map digest binding.
Every other base obligation remains authoritative; selective or mixed
map/schema use rejects. The unchanged schema `inventory_authority` value
`exact-decision-and-supporting-call-sets-in-v0.5-interface-map` resolves to
the digest-pinned effective map here. The effective schema changes only
`properties.interface_map_sha256.const` to that map's digest.

The effective map changes only
`native_api_contract.source_derived_v0_4.preloader.supporting_calls`, inserting
`FindClose` in ASCII order. Its exact supporting set is `CloseHandle`,
`DeleteProcThreadAttributeList`, `FindClose`, `GetCurrentProcess`,
`GetLastError`, `GetTickCount`, `Sleep`, `TerminateProcess`: 8 supporting
calls plus the unchanged 44 decision calls, total 52 (formerly 7/51).
Existing source hashes and virtual paths remain historical v0.4 evidence;
they do not claim that the old source contains `FindClose` or identify a new
binary. Future implementation provenance must bind the actual corrected
source and binary to this amended normative inventory.

## Exact clause precedence

The following base clauses are resolved by this amendment. Filenames below
are exact names within the authenticated seven-row base manifest; line
references identify immutable base bytes.

| Base artifact and clause | Effective reading |
|---|---|
| `public-assembly-runtime-profile-neutral-preloader-design-revision-v0.5.md`, section 2 lines 51-58 and section 2.2 lines 89-108 | Retain source/import/profile equality, ordering, unknown/alternate-call rejection, all 44 decision calls and import families; supporting lines 104-106 acquire `FindClose`, count 8, total 52. |
| `public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.5.md`, adversarial row 9 line 47 | Preloader comparison is exact 44+8; the guard remains 18+4 and future materializer remains 29. The complete 15-row threat freeze and cleanup expectations still apply. |
| `public-assembly-runtime-profile-neutral-preloader-independent-rereview-brief-v0.5.md`, map/schema pins lines 65-68 and review question 2 lines 112-119 | Old pins remain base evidence; this amendment supplies effective pins. Preloader review expects 44+8 with all other equality and materializer obligations unchanged. |
| `public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json`, `native_api_contract.inventory_equality`, `source_derived_v0_4.preloader`, and `semantic_relations` | Apply exact source/import/profile equality to the effective supporting list; only line 217 gains `FindClose`. Historical source identity and all other keys stay unchanged. |
| `runtime-profile-v0.5.schema.json`, `properties.interface_map_sha256` line 107, `native_api_contract.inventory_authority` line 190, and source/import equality | Effective copy replaces only the map-digest constant; authority resolves to the effective map. All other schema bytes and constraints are preserved. |
| `v0.4-implementation-independent-rereview-response-v0.1.md`, `RPNP4-IRR-001` row line 28 and map/schema hash references | Historical results remain historical; future normative preloader 44+7 becomes 44+8, with the effective pins above. |
| `v0.5-independent-rereview-response-v0.1.md`, map/schema pins lines 23-26 | Pins remain historical base evidence; effective authority uses this amendment's pins. Its materializer `LocalFree` correction and every other claim remain unchanged. |

This precedence does not rewrite any historical review outcome. It is not
permission to omit required calls, weaken equality, use hidden alternate
routes, or replace successful materialization with unconditional rejection.

## Lifecycle, boundaries, and handoff

The corrected preloader must give search handles their standard `FindClose`
lifetime owner through normal and failure exits. Ordinary kernel handles
retain `CloseHandle` ownership. The existing direct-import families, guard
and materializer API sets, evidence-v2 grammar, physical-path requirements,
resource limits, and all other 15-row freeze obligations remain unchanged.
No token redesign, new requirement from C, or new trust system is introduced.

The unchanged feasibility report at
`s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.5/verification/implementation-feasibility-report-v0.1.md`
has SHA-256 `2cd3b3db9605d204bfa7b4f95c197676dea7c0718f533f0841402491c5f5e20c`.
The unchanged parent-directory
`v0.5-implementation-feasibility-control-decision-v0.1.md` has SHA-256
`b9eabb4ceb220d3ee1c09a6a1ba9e7a405b0a72db3a0b60a93304f7796641202`.
They preserve the sole finding `RPNP-IMPL5-FEASIBILITY-001`; A's token
impossibility theory is withdrawn and C is unverified interpretation only.
No new runtime observation is claimed by this amendment.

For this design-only substep, CODE is explicitly skipped because there is no
source/configuration implementation action; these JSON design artifacts
belong to DOCUMENTATION. Sequence: CONTROL freeze -> DOCUMENTATION inputs ->
dedicated TEST exact-delta and negative-mutation checks -> DOCUMENTATION
evidence -> fresh read-only REVIEW -> CONTROL acceptance/re-freeze. Only
then does the resumed CODE -> TEST -> DOCUMENTATION -> fresh implementation
REVIEW sequence proceed. Existing controller, adapter, runtime and toolchain
remain reusable. No amendment acceptance, implementation PASS, production
materialization, safety/value/transfer, stage 70/80, S0, or Git authority is
implied by this authored input.
