# S0 v0.14 public assembly build and runtime materialization design v0.3 independent review

- `status`: completed fresh independent PUBLIC design review
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: `0 BLOCKING / 2 MAJOR / 0 MINOR`
- `implementation_observed`: none for the v0.3 design
- `compiler_or_build_observed`: none
- `runtime_materialization_or_native_execution_observed`: none
- `F0_content_access`: none

## 1. Role and integrity result

I acted only as the fresh independent PUBLIC design reviewer. I did not
author, advise on, or QA v0.3, and I did not use an author conversation or
another reviewer result. I read the authenticated v0.2 independent review
only as the exact four-finding specification.

The CONTROL-supplied Git identity matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- review branch:
  `codex/s0-build-runtime-materialization-design-v03-review`;
- HEAD and candidate remote-tracking ref:
  `5f1238cb804e1aaa161011e25e967def26514bad`;
- tree:
  `9bdfeaca3465da0da2968199ef9868e5d59a3f84`; and
- sole parent:
  `9917f3c645c4e90f3dc84f4a3e0cb76c1be66d3b`.

The initial tracked and untracked change counts were zero. The canonical text
validator SelfTest passed. All seven externally pinned package manifests
matched before their targets were used. Their authenticated logical-target
counts were exactly `7 / 9 / 6 / 6 / 5 / 3 / 4` for build/runtime v0.2,
build/runtime v0.3, RPNP v0.4, RPNP integration v0.2, assembly v0.5,
bounded implementation, and bounded verification. Every listed target hash
matched. The bounded CONTROL decision pair and v0.2 review pair also matched
their external pins.

All 23 admitted Markdown/sidecar pairs passed the canonical validator. All
13 admitted JSON files passed strict UTF-8, UTF-8 BOM absence, CR absence,
final-LF, trailing-whitespace, canonical-sidecar, exact-hash, and
duplicate-key checks. All six admitted schemas passed the Draft 2020-12
metaschema. The v0.3 absolute base reference resolved to the exact
authenticated v0.2 schema, and the two record references resolved to the
exact authenticated v0.3 record schemas.

Final verification reproduced every package and target hash, every externally
pinned v0.3 sidecar and review/decision pair, and the exact Git identity. The
only worktree changes were this review Markdown and sidecar. Tracked worktree
and index quiet-diff exits were zero. F0 aggregate counts were exactly
`32 / 11 / 10`; worktree, index, and parent F0 quiet-diff exits were all zero,
and F0 untracked, ignored, skip-worktree, and assume-unchanged counts were all
zero. Canonical output validation and `git diff --check` passed.

Reviewer-local PowerShell execution-policy and Python command-quoting errors
were corrected and rerun. They changed no candidate byte and are not
candidate findings.

## 2. Bounded hostile reconstruction result

### 2.1 BRM-V02-IR-001 target-set grammar

The target-set correction is constructible. Two independent in-memory
serializers produced the same 488-byte ASCII/LF preimage and SHA-256
`b9c505a86b74d8ddf906bd82b70b2e34ccfd368f8fde7edcaf57b1ebb917f8b1`
for three clearly fake PUBLIC rows. The reconstruction fixed the schema ID,
header and row order, canonical unsigned decimals, ASCII path bytes, path and
target byte lengths, lowercase target hashes, target count, aggregate bytes,
and terminal LF.

Changed grammar, CRLF, missing final LF, uppercase digest, leading-zero
decimal, absolute/dot/non-ASCII path, duplicate, reorder, empty set, count,
length, target hash, and total-byte mismatches all fail before candidate
import or process creation. `BRM-V02-IR-001` is closed.

### 2.2 BRM-V02-IR-002 import-role ownership

The authenticated RPNP v0.4 profile supplies the exact eleven observation
call names and order, its direct-import closure policy, the guard
initialization symbol, and the preloader's `CreateProcessW` and `NtCreateFile`
obligations. The authenticated integration v0.2 design assigns the sole
`NtCreateFile` transaction to the native preloader.

The v0.3 effective policy consequently fixes two preloader direct imports,
eleven guard direct imports in RPNP order, and exactly one guard export. It
forbids guard `NtCreateFile`, requires each full import set to equal its
separately authenticated role allowlist, and keeps inspection byte-bound
without loading an image. Omission, extra, order, role, owner-DLL, export, and
allowlist mutations have one `BR-BINARY/1` result. `BRM-V02-IR-002` is
closed.

### 2.3 BRM-V02-IR-003 DLL-search closure

The positive derivation is otherwise deterministic: index zero is the parent
of the exact `verifier_application` row; byte-identical application and DLL
parents are removed; remaining parents are byte-sorted; directory hashes use
the exact `directory=<virtual_directory>\n` preimage; and map-order bindings
repeat name, path, parent, index, and hash. Host, PATH, registry, current
directory, user-site, and environment fill are forbidden.

Finding `BRM-V03-IR-001` remains because directory identity is only raw-byte
unique and does not reject Windows path aliases.

### 2.4 BRM-V02-IR-004 records and publication

The prepublication and final schemas are closed Draft 2020-12 objects. Their
body inventories contain exactly 17 and 15 ordered fields, respectively.
Two fake PUBLIC packages validated, while 66 required-field deletion,
unknown-field, cross-boundary, and nested-target-row mutations failed. The
three body hashes are semantically required to agree, and the ten publication
phases correctly place close/readback, the destination recheck, rename,
postpublication rehash, and final record freezes.

Finding `BRM-V03-IR-002` remains because the recheck and rename do not form
one fail-if-present transaction. The machine contract does not bind a
no-replace rename primitive or flags.

### 2.5 Matrix, relations, resources, and authority

The published v0.2 retained rows and replacement groups reconstruct 63 unique
IDs. Appending the 34 v0.3 rows in published order produces 97 unique IDs.
Every row has one nonempty primary failure label and one Boolean output bit;
all 97 `/0` and `/1` suffixes agree with that bit. Retry rows retain the prior
primary class, and later cleanup, quarantine, record, and retry facts cannot
replace the first primary failure.

The map and schema carry the same 42 unique v0.3 semantic relations in the
same order. The v0.2 map and schema likewise agree on their 31 relations.
The twelve resource names and values are exactly equal in the v0.2 map,
v0.2 schema, and v0.3 schema. The successor forbids direct v0.2 execution,
requires the semantic validator to execute all nonreplaced v0.2 relations,
and keeps `candidate_only=true` and `build_execution_authorized=false`.

The bounded predecessor remains an offline diagnostic candidate. Static
inspection of its exact authenticated source confirms the diagnostic fixes
`candidate_only=true`, `native_api_reachable=false`, and
`rehearsal_pass=false`; its candidate source exposes no direct native,
process, network, or provider surface. I did not execute that candidate or
its verifier.

## 3. Findings

### BRM-V03-IR-001 — MAJOR — DLL directories are not unique by admitted Windows path identity

Artifacts: `public-assembly-build-runtime-materialization-design-revision-v0.3.md`
§4; `build-runtime-materialization-profile-v0.3.schema.json`
`$defs.virtual_directory` and
`effective_runtime_dll_search_policy`; and
`build-runtime-materialization-mutation-matrix-v0.3.json`
`BRM-V03-DLLDIR-004/008`.

The derivation removes only byte-identical DLL-parent directories and sorts
raw ASCII bytes. The schema also permits empty path segments and trailing
slashes. It therefore accepts parents such as `Lib`, `lib`, `Lib/`, or paths
containing doubled separators as distinct directory rows and indices. The
same design separately recognizes that DLL names need ASCII-lowercase
collision handling, but it defines no equivalent directory-alias rule.

Counterexample: an embedded schema-valid runtime map places one DLL at
`Lib/a.dll` and another at `lib/b.dll`. The v0.3 algorithm produces two
byte-unique directory identities and two indices. On the admitted ordinary
Windows case-insensitive path model they can identify the same directory, so
search order and resolution identity are not uniquely represented. A
separator alias provides the same counterexample without changing case.

Required correction: define one canonical directory path grammar with no
empty or trailing segments, bind the admitted Windows comparison rule, reject
case-fold and separator aliases before directory hashing, and add explicit
case/alias directory mutations. Keep exact DLL-name collision and resolution
binding checks.

Impact: the ordered search inventory and directory indices can still have two
machine-valid interpretations that affect DLL byte resolution. This is a
runtime/provenance closure defect, not a formatting issue.

### BRM-V03-IR-002 — MAJOR — destination recheck is not coupled to a no-replace atomic rename

Artifacts: `public-assembly-build-runtime-materialization-design-revision-v0.3.md`
§5; `build-runtime-materialization-profile-v0.3.schema.json`
`publication_transaction`; and
`build-runtime-materialization-mutation-matrix-v0.3.json`
`BRM-V03-PUBLISH-001/002/003`.

The design requires an absence observation immediately before a separately
described `single-same-volume-atomic-rename`, but it does not bind this runtime
tree publication to an exact fail-if-destination-exists/no-replace primitive
or flag set. Prohibiting candidate callbacks and path recomputation does not
exclude an external actor between the observation and rename. The inherited
assembly v0.5 file-publication primitive is not named as the primitive for
this distinct runtime-tree transaction.

Counterexample: the recheck observes the intended name absent; another actor
creates that name; an implementation uses a replacement-capable atomic rename
for A. The final destination then has A's identity and hashes, so the existing
postpublication checks and record schemas can pass even though the
intervening object was overwritten. Another implementation uses a no-replace
rename and fails. Both can describe their operation as the schema's string
`single-same-volume-atomic-rename`.

Required correction: bind an exact same-volume atomic rename primitive and
numeric flags whose operation fails when the destination exists, require that
collision failure to preserve `BR-MATERIALIZE/1` and grant no authority, and
add a mutation for destination creation after recheck but before the rename
linearization point. Alternatively use one exact atomic create-if-absent
publication operation that makes the separate observation nonauthoritative.

Impact: publication behavior remains multiply interpreted and can overwrite
a raced destination while producing schema-valid final evidence.

## 4. Nonregression and evidence limits

The revision retains exact predecessor pins, source/toolchain closure, two
clean builds, byte equality, byte-bound static inspection, runtime roles and
module mapping, resource ceilings, immutable primary failures, preselected A
ownership, B quarantine, diagnostic-only records, and later platform-test
boundaries. No schema or semantic-validation success grants build, live,
rehearsal, or S0 authority.

This review is design evidence only. No v0.3 build/runtime-materialization
source, compiler, build, binary, runtime tree, native call, loaded image,
platform behavior, live decision, rehearsal, F0 input, provider/model task,
S0 result, or E0 result was created or observed. No implementation,
compiler/build, native/runtime/platform probe, provider/model, executor,
judge, S0, or E0 operation was run. The exact bounded predecessor source was
read only to confirm its diagnostic claim boundary; it was not executed.

## 5. Verdict and remaining gate

Verdict: `REVISE-AND-REVIEW`.

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 2 |
| MINOR | 0 |

The PASS-only gate
`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.3 CONTROL INTEGRATION OPEN`
is not opened. The required next action is a bounded design revision followed
by a fresh independent review of the revised exact package.

No commit or push was authorized or performed.
