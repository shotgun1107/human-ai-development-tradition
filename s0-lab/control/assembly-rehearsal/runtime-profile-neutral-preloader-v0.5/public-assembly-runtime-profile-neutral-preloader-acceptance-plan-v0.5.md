# Public Assembly Runtime Profile + Neutral Preloader Acceptance Plan v0.5

Status: design-level acceptance plan; no implementation or platform proof

## 1. Candidate and package authentication

This plan judges only whether successor DESIGN v0.5, composed in full after
authenticated v0.4, closes `RPNP4-IRR-001`, `RPNP4-IRR-002`, and
`RPNP4-IRR-003` without weakening any unaffected predecessor obligation.
Selective predecessor use rejects.

Review input is valid only when base commit
`440f4342bb27398c6f2a4131d5518f2b55722f4c`, tree
`c77b078ac934ab7a8b31142bad337cf86ee16ca1`, all seven ASCII-sorted unique
manifest rows, their exact hashes, and same-basename sidecars reproduce. The
canonical text validator SelfTest and five Markdown checks must pass; JSON
must be strict UTF-8, no BOM, final LF, duplicate-key-free, and valid against
Draft 2020-12. F0 access, input repair, an unauthorized path, or any pin
mismatch makes the review invalid before semantic judgment.

TEST4 artifact manifest
`6c49ee508d79d51fab693d6866b6782df14cf32e67237934c0fa24b2ff3e256f`
records PASS 23 / FAIL 0 / UNVERIFIED 3, zero candidate failures, and zero
harness failures. Its command used Python 3.12.10 and jsonschema 4.26.0,
exited 0, and ran in 323 ms. It rejected all 595 mutations: 5 overlay,
11 `LocalFree` cleanup, 208 evidence, 349 schema, 5 v1/v2 mixing, 11 physical,
and 6 cross-cutting.
This is synthetic/static design evidence, not implementation, OS, filesystem,
API, PE/import/loaded-image, stage-70/80, or live-assembly evidence.

## 2. Frozen bounded adversarial matrix

Every row is mandatory. “Reject” means fail closed before granting or
continuing output/evidence authority and leave no authoritative partial
result. Unknowns remain `UNVERIFIED` and block broader claims.

| # / surface | CODE IMPLEMENTATION defense/action | TEST/VERIFICATION diagnostic and expected fail-closed result | DOCUMENTATION allowed claim / required nonclaim | INDEPENDENT REVIEW closure criterion |
|---|---|---|---|---|
| 1. Attacker and concurrency | Admit same-user races over paths, reparse/junction/mount aliases, materialization, evidence, environment, extra files, and inheritable decoys; expose no caller bypass. | Schedule pre/during/post rename, replacement, alias, injection, evidence, and decoy races; each rejects deterministically with no output authority. | Claim only the bounded same-user contract and tests; disclaim administrator/kernel resistance. | Every admitted capability has an exact owner and discriminating fail-closed case. |
| 2. Authority sources | Trust only exact Git-pinned design/implementation bytes, frozen runtime/package pins, admitted Windows semantics, authenticated launcher/preloader/guard identities, and retained handles. Label paths, CLI, environment, mutable files, caller claims, and moving refs untrusted. | Mutate each untrusted source independently; no caller-minted value may become authority. | State every unverified prerequisite; make no authority claim from path text or caller assertion. | Reject any caller-mintable, moving, or unlabeled authority. |
| 3. Complete flow | Version every edge: external pins -> materialization -> complete profile validation -> preloader -> evidence v2 -> `CreateProcessW` -> admission -> guard -> import -> output/evidence. | Break/rebind each edge one at a time; each rejects before the next authority transition. | Claim specification of the enumerated flow only; distinguish it from executed evidence. | No orphan input, output, version, digest, identity, or consumer binding. |
| 4. Mutability and rebinding | Bind bytes by hash, objects by retained handle/identity, and transaction by nonce/PID/version; forbid pathname reopen and branch-name authority. | Swap bytes or objects between check/use and nonce/PID/version/digest between stages; all reject. | Preserve TOCTOU as unverified beyond tested implementation/platform scope. | The verified object/bytes must be the object/bytes used through terminal evidence. |
| 5. Verified versus executed bytes | Bind executable, DLL, Python stdlib/package/native extension, schema/validator, bootstrap, imports, and loaded images end to end. | Inject alternate or shadow bytes at every source/build/import/load edge; each rejects. | No live-execution or loaded-image claim from design checks. | Complete source -> binary -> imported/loaded mapping with exact identity equality. |
| 6. Interpreter/stdlib/native/import closure | Deny environment, user-site, `PYTHONPATH`, plugin, FFI, and dynamic-loader routes; preserve exact direct and loader closure. | Mutate each route and direct/native/stdlib inventory element; partial inventory rejects. | Retain full-loader-closure nonclaim until a later live probe. | No partial inventory may be presented as full closure; every allowed route is pinned. |
| 7. Inventory and shadows | Require unique ASCII-sorted exact manifests; reject unlisted files, ADS, case aliases, hardlink/reparse aliases, duplicate logical paths, and shadows. | Add each shadow class and duplicate/order mutation; each rejects. | Claim only enumerated-inventory closure, not all possible filesystem behavior. | No silent file, stream, alias, or duplicate class remains. |
| 8. External artifacts | Preserve exact inherited URL, final URL/redirect, digest, size, and provenance fields; add no downloader or trust subsystem. | Change each field independently; schema/semantic validation rejects. | State supplier, TLS, and provenance beyond existing pins unverified. | No upgraded live-authority claim and no weakened inherited pin. |
| 9. Native API inventory | Derive exact source calls; partition decision-semantic/supporting; require equality with profile, build/import manifest, binary imports, and loaded routes. Freeze the future materializer as exactly 29 ASCII-sorted unique calls with `LocalFree` the sole explicitly classified supporting cleanup call. Unknown/alternate calls reject. | Independently extract and compare exact guard 18+4 and preloader 44+7 sets, including the five former omissions; require future-materializer map/schema parity and reject omission, duplicate, wrong category, alternate cleanup, unknown call, or missing owner/relation. TEST4 rejected 11/11 targeted cases. | Claim exact design inventory and role split only. | Source/import/profile equality is complete, `LocalFree` cleanup is exact, and no hidden alternate route exists. |
| 10. Evidence grammar | Use only `S0-LAUNCH-HANDLE-SET-EVIDENCE-2`: US-ASCII, no BOM/CR, exact final LF, one header plus eight ordered groups and 45 ordered fields; place `external_pin_digest` and `workspace_root` in `run-authority`. | Mutate each name, order, group, constant, width, normalization, encoding, final LF, and producer/consumer/schema/interface/admission version; each rejects; any v1/v2 mix rejects. | Claim canonical grammar closure, not truth of platform-produced field values. | One canonical grammar and explicit reject-only migration; all layers bind v2. |
| 11. Windows path lifecycle | Bind ACL/effective token, volume/root and stable file identity; open every ancestor relative to retained handles; reject symlink, junction, reparse, mount, rename/replacement, base identity, and repository identity/containment/alias; create leaf once relative to retained parent; root all later writes/evidence in retained output identity. | Exercise alias parent, mount, swapped ancestor/leaf, same object via alternate path, base-inside-output/output-inside-base, output/evidence under repository, and unsupported filesystem/API; reject with no authoritative output. | Limit claim to the specified Windows/filesystem contract; lexical containment is non-authority. | Physical retained-handle containment, explicit repository exclusion, and TOCTOU closure through final writes are complete. |
| 12. Evidence producer and output | Bind producer identity, output/evidence roots, sidecars, pre/post measurements, transaction terminal state, and exact reproducible command. | Mutate output/evidence after production and rebind producer or transaction; mismatch rejects. | Label evidence synthetic or real-Windows accurately. | Evidence cannot outlive, rebind, or detach from its producer transaction. |
| 13. Failure, cleanup, and close | Give every acquired handle/process/thread/file one terminal owner; the materializer owns each successful `GetSecurityInfo` allocation and releases it with `LocalFree` exactly once on every success, failure, timeout, cleanup, and close path; terminate suspended child on error; quarantine partial output; never retry into new authority; record bounded cause; close once. | Inject failure after each acquisition and on timeout/cleanup; omit or substitute `LocalFree`, remove the owner/relation, or add an unknown call; each rejects and leaves no child, handle, file, allocation, or authority residue. | Make no cleanup claim beyond the exact design checks and later executed cases. | Every acquire/allocation path has an exact close/free terminal owner and no retry authority. |
| 14. Resource bounds | Enforce admission 8,192 bytes, evidence 65,536 bytes, five handles, runtime 512 files/536,870,912 bytes, and inherited or explicitly frozen finite path, component, frame, timeout, wait, and concurrency limits. | Test each boundary and one-past; overflow, unbounded read/wait/loop, and absent required limit reject. | State only exact configured limits and tested boundaries. | All reads, loops, waits, frames, paths, files, bytes, and concurrency are finitely bounded. |
| 15. Claims and blockers | Encode only design-contract closure; do not encode implementation or downstream acceptance. | Confirm nonclaims are mandatory; broader-claim mutations reject. | Repeat: no implementation, real-Windows proof, live bridge, rehearsal, S0, safety, value, or transfer claim; list all `UNVERIFIED` items. | PASS only with zero BLOCKING and zero MAJOR on the frozen delta and no predecessor regression; otherwise `CORRECT/RETEST` or `REJECT`. |

After an unexplained failure, and always before a second speculative
correction for the same blocker, TEST/VERIFICATION must produce a
discriminating diagnostic matrix that isolates the next correction. Repeated
hypothesis-only CODE edits are not admissible evidence.

## 3. Finding closure and review threshold

The reviewer must determine independently:

1. `RPNP4-IRR-001`: exact guard, preloader, and materializer API inventories,
   role partitions, import families, and equality/rejection rules match the
   authenticated sources and machine contracts;
2. `RPNP4-IRR-002`: evidence v2 has exactly one header, eight named groups,
   45 unique ordered fields, exact widths/normalizations, run-authority
   placement, and reject-only v1/v2 migration; and
3. `RPNP4-IRR-003`: physical output/evidence ancestry, repository exclusion,
   retained identity, rename/replacement, relative leaf creation, and terminal
   rooting are complete design predicates; and
4. `RPNP5-IRR-001`: the future materializer set is exactly 29 ASCII-sorted
   unique calls, `LocalFree` is its sole explicitly classified supporting
   cleanup call, every successful `GetSecurityInfo` allocation has exact-once
   `LocalFree` ownership on every terminal path, and omission, substitution,
   unknown calls, or map/schema drift reject.

A design PASS requires a valid fresh read-only review, BLOCKING 0, MAJOR 0,
explicit closure of all three findings, and no regression. MINOR findings
require explicit CONTROL disposition. `CORRECT/RETEST` applies when repair is
bounded and re-reviewable; `REJECT` applies when the candidate cannot satisfy
the frozen claim without redesign or unauthorized scope; `INVALID-REVIEW`
applies to input, role, hash, or boundary failure.

PASS permits CONTROL to consider a separate corrected-implementation gate
only. It does not authorize implementation, stage 70/80, live assembly,
official rehearsal, F0, S0, Git staging/commit/push, or any platform,
operational-safety, economic-value, or transfer claim.

Unverified items remain: v0.1-v0.4 predecessor profile bytes outside TEST4's
allowlist; OS/filesystem/API/runtime behavior; PE/import/loaded-image and full
loader closure; stage 70; stage 80; and live assembly.
