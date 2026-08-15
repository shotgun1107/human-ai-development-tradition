# S0 v0.14 public assembly build and runtime materialization acceptance plan v0.3

## 1. Scope

This plan tests only proposal-text and machine-contract closure of the four
v0.2 review findings. It does not compile, build, load, materialize, call a
native API, probe Windows, access F0 content, or run a provider, model, S0, or
E0 task.

Authenticate the v0.2 package manifest, v0.2 review, v0.3 package manifest,
all nine v0.3 logical artifacts and sidecars, and the predecessor manifests
named by the independent-review brief before reading their targets.

## 2. Schema and composition checks

1. validate the v0.2 and v0.3 admission schemas and both record schemas
   against Draft 2020-12 metaschema;
2. resolve the v0.3 base `$ref` to the exact authenticated v0.2 schema and the
   two record `$ref` values to the exact authenticated v0.3 record schemas;
3. require `direct_v0_2_execution_allowed=false`;
4. validate one clearly fake PUBLIC in-memory placeholder admission package;
5. remove every required field and add one unknown field at every new object
   depth; and
6. confirm schema validation remains diagnostic-only.

## 3. Target-set construction checks

Independently serialize the exact `S0-BRM-TARGET-SET-PREIMAGE-1` preimage from
at least three PUBLIC in-memory target rows. Confirm byte-for-byte equality
between two independent constructions and one SHA-256 result.

Reject each of the eight `BRM-V03-TARGETSET-*` rows: changed grammar, invalid
path, duplicate path, wrong order, length/hash mismatch, count mismatch,
total-byte mismatch, and empty set. Also reject locale sorting, filesystem
enumeration order, UTF-16, CRLF, missing final LF, uppercase digest, leading
zero decimal, case folding, and target rows that change after authentication.

## 4. Binary-role checks

Reconstruct the preloader's ordered two-import list and the guard's ordered
eleven-import list directly from authenticated RPNP v0.4 inputs. Confirm the
guard export and the complete role import-allowlist equality. Reject all six
`BRM-V03-BINARY-*` mutations, swapped roles, reordered lists, a guard
`NtCreateFile`, missing preloader root creation, a missing guard observation
call, wrong DLL owner, and an import outside the authenticated allowlist.

Static analysis is on exact bytes and may not load a target.

## 5. DLL-directory and resolution checks

Build one fake PUBLIC runtime role map and DLL map in memory. Independently
derive the application directory and sorted unique DLL-parent directories.
Require contiguous indices, exact directory identity hashes, exact map-order
resolution bindings, ASCII-lowercase DLL-name uniqueness, and exact path/hash
selection.

Reject all eight `BRM-V03-DLLDIR-*` mutations plus a case-only DLL-name
collision, a parent-directory mismatch, an out-of-range directory index, an
application directory at a nonzero index, and any directory from PATH,
registry, current directory, environment, user site, or host enumeration.

## 6. Record and publication checks

Construct clearly fake PUBLIC in-memory prepublication and final packages.
Validate exact required and forbidden fields, exact body-field order, the
record codec, and equality of canonical, closed-file, and retained-parent
readback body hashes.

The positive phase order is exactly:

1. runtime equality;
2. B quarantine;
3. prepublication body freeze;
4. prepublication body close/read-back verification;
5. destination-absence recheck through the same retained parent and name;
6. one same-volume atomic A rename;
7. retained-parent reopen and final identity/file/hash/target-set checks;
8. final body freeze;
9. final body close/read-back verification; and
10. final diagnostic record freeze.

Reject all twelve `BRM-V03-PRECORD-*`, `BRM-V03-PUBLISH-*`, and
`BRM-V03-FRECORD-*` rows. Specifically reject cross-boundary fields, missing
or unknown fields, mismatched body hashes, stale absence, parent/name change,
destination creation between observations, final record before rehash, row
set mismatch, repeated publication, and any authority after failure.

## 7. Matrix and nonregression checks

Authenticate and reconstruct the v0.2 effective 63 rows. Append exactly the
34 v0.3 rows in published order and require 97 unique IDs. Check Boolean
output state against `/0` and `/1` for all 97 rows and preserve the first
failure through cleanup, quarantine, record, and retry faults.

Require exact equality of the 42 semantic relations between interface map and
profile schema, exact equality of the twelve resource limits with v0.2, and
no change to nonreplaced v0.2 authority, source, toolchain, reproducibility,
runtime-role, module-map, failure, claim, or closed-gate rules.

## 8. Pass condition and evidence limit

A fresh independent reviewer may return
`PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` only with
zero BLOCKING and zero MAJOR findings. Any finding yields
`REVISE-AND-REVIEW`; integrity or role failure yields `INVALID-REVIEW`.

Passing this plan proves only a bounded public design. It does not prove an
implementation, build, binary, runtime tree, native behavior, platform
behavior, rehearsal, F0 result, provider/model result, S0, or E0.
