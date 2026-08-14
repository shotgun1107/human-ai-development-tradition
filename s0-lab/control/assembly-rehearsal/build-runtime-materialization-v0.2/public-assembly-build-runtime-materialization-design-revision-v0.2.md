# S0 v0.14 public assembly build and runtime materialization design revision v0.2

- `status`: bounded revision candidate; fresh independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.2 REVISION OPEN`
- `base_design_sha256`: `2acbdfa35d09ba19f085f7cbff19a5c06a3605a58617e2165383f81391542c11`
- `base_interface_map_sha256`: `e0a5d539a2672cf5ac93ad1db8bc48c89a1f380e8c3430de85ef140812c43963`
- `base_profile_schema_sha256`: `77977adfd852cae50589f68996c7e2c06fdb5b58164a469d0d87436c8761d254`
- `base_mutation_matrix_sha256`: `326144bda84cfdd77c2dfaa4e6c5bd069852a8e74bc6edfc1f9e165b8a50420b`
- `v0.1_review_sha256`: `85c917496b04246be173dafa2ffd729fa80e836d363de0ab982f593c42efa292`
- `implementation_status`: not implemented
- `build_status`: not executed
- `runtime_materialization_status`: not executed
- `native_execution_status`: not executed
- `F0_content_access`: none

## 1. Revision scope and strict composition

This revision closes only findings BRM-IR-001 through BRM-IR-005. It adds no
compiler choice, source bytes, toolchain, binary, runtime distribution,
runtime tree, native execution, platform probe, live authority, rehearsal, or
S0 execution.

The effective v0.2 contract is exactly:

1. the authenticated v0.1 design, acceptance plan, interface map, mutation
   matrix, and profile schema;
2. this revision package; and
3. the replacements expressly identified below.

The v0.2 admission schema wraps one complete v0.1 base profile. Direct use of
a v0.1 profile for build execution is forbidden after v0.2 integration. The
wrapper is mandatory because v0.1 has closed objects that cannot be safely
extended in place. The semantic validator must validate the embedded base
profile against the exact v0.1 schema, canonicalize its exact JSON bytes,
compare those bytes with `base_profile_sha256`, and then enforce every v0.2
relation. Passing either schema alone is never acceptance.

Where this revision replaces a v0.1 rule, the replacement is complete and
the former rule is not simultaneously active. Every other v0.1 rule remains
unchanged.

## 2. BRM-IR-001: complete authority and ten-pin closure

### 2.1 Retained public authority

The v0.2 wrapper requires these values that the v0.1 closed authority object
could not encode:

- baseline commit
  `64077a5862aa5678a83ba2f9f48fc71493ed2808`;
- baseline tree
  `db271b4f08cabcdb038d17ce0d1705d2897b5115`;
- bounded verification manifest
  `8f8140d678e5846639ff382b32035c342dc8b2dd7d929da5ff37a759f8aa9d7b`;
- integration v0.1 design manifest
  `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b`;
- exact v0.2 design-package manifest SHA-256; and
- the fresh approving v0.2 independent-review Markdown SHA-256.

The wrapper and embedded base profile are compared to original authenticated
bytes in the same outer operation. A prior PASS object, moving branch,
candidate-selected value, discovered file, or decoded object cannot supply a
missing authority.

### 2.2 Ten external pin classes

The v0.2 admission package represents the ten classes without self-reference:

| Class | Exact v0.2 binding | First failure |
|---|---|---|
| native source | `external_pin_closure.native_source` | `BR-SOURCE/0` |
| materializer and inspector source | `external_pin_closure.materializer_inspector_source` | `BR-SOURCE/0` |
| offline toolchain bundle | `external_pin_closure.offline_toolchain_bundle` | `BR-TOOLCHAIN/0` |
| compiler, linker, SDK, headers, libraries, CRT | `external_pin_closure.compiler_linker_sdk_crt_identities` | `BR-TOOLCHAIN/0` |
| CPython distribution | `external_pin_closure.cpython_distribution` | `BR-SOURCE/0` |
| Python dependencies | `external_pin_closure.python_dependencies` | `BR-SOURCE/0` |
| Windows platform | `external_pin_closure.windows_platform` | `BR-AUTH/0` |
| canonical build profile | canonical embedded `base_profile` plus `base_profile_sha256` | `BR-TOOLCHAIN/0` |
| runtime-tree profile | `external_pin_closure.runtime_tree_profile` | `BR-SOURCE/0` |
| approving review | `authority_extension.approving_design_review_sha256` | `BR-AUTH/0` |

Each manifest identity binds its manifest hash, exact target count, aggregate
target bytes, and target-set hash. The outer verifier authenticates every
manifest and target before candidate import, source admission, tool
resolution, or process creation. The semantic validator requires the six
v0.1 external closure values to equal their corresponding v0.2 identities.

The current package cannot populate future pins and remains
`BLOCKED-MISSING-EXTERNAL-PIN`.

## 3. BRM-IR-002: complete native binary policy

The v0.2 wrapper contains exactly one `native_preloader` profile and exactly
one `runtime_handle_guard` profile. Each profile binds the exact artifact
bytes and all inspection products. It contains no general PASS boolean.

Both roles require exact artifact length and SHA-256, PE32+ AMD64 identity,
entry point, subsystem, image size, section manifest, import and export
manifests, import and export allowlist manifests, relocation table, resource
table, Windows manifest, load-config bytes, and the four mitigations ASLR,
HIGH_ENTROPY_VA, NX compatibility, and Control Flow Guard.

The following independently measured counts must be zero:

- Authenticode certificate-table size;
- bound and delay imports;
- CLR header size;
- CodeView records, debug directories, and PDB references;
- TLS callbacks and writable-executable sections;
- dynamic-loader and generic-FFI imports;
- shell, network, provider, and plugin imports;
- embedded host-path matches; and
- unbound timestamps.

The relocation table must be present and bound by hash. The static inspector
must parse authenticated bytes without loading the image. Its import and
export enumerations must exactly equal the independently authenticated
allowlist manifests; reordered, ordinal-substituted, added, or removed entries
fail `BR-BINARY/1`.

The preloader has the exact required direct import
`kernel32.dll!CreateProcessW` and no required export. The guard has the exact
required direct import `ntdll.dll!NtCreateFile` and exact export
`PyInit_s0_runtime_handle_guard_v0_4`. These assignments do not permit other
imports: the complete allowlist manifests remain controlling.

The inspected artifact hash, built-output row, materialized runtime row, and
later loaded-image observation must all be identical. This design still does
not claim the later loaded-image observation has occurred.

## 4. BRM-IR-003: exact CPython and source-only runtime closure

The v0.2 runtime extension requires exact bindings to unique rows of the
embedded base runtime package for all of these role keys:

- verifier application;
- CPython DLL and standard library;
- native guard;
- Python dependencies and bootstrap;
- assembly source;
- I0, I1, I2, and I3 source;
- profiles, manifests, and fixed public inputs.

Every embedded base runtime row must appear in exactly one required role or
the candidate is rejected. Every referenced path must exist exactly once in
the base runtime rows. No unclassified or extra runtime row is allowed.

The interpreter contract is exactly CPython 3.12 Windows AMD64 with initial
flags in this order: `-I`, `-S`, `-B`. `jsonschema` is exactly version 4.26.0
and its distribution manifest must equal the authenticated Python-dependency
closure. The exact module map binds each importable module name to one
authenticated source runtime path and SHA-256. The exact DLL map binds every
loadable DLL name to one authenticated runtime path and SHA-256.

The only import algorithm is
`exact-module-map-no-namespace-fallback-no-bytecode`. Namespace fallback,
bytecode read or write, host Python, user site, `site` import, `PYTHONPATH`,
current-directory import, PATH or registry application selection, package
installation, and any unlisted module or DLL are forbidden.

The verifier application is selected only by its exact authenticated runtime
row. DLL search is limited to the application directory and explicitly
authenticated runtime directories. A missing role, module, DLL, source byte,
or dependency stops with `BR-MATERIALIZE/1`; a native byte mismatch stops with
`BR-BINARY/1`.

## 5. BRM-IR-004: one output state and one primary failure per mutation

The v0.2 mutation matrix is the only effective mutation inventory. It is
constructed mechanically from the authenticated 46-row base matrix:

1. traverse base rows in their original order;
2. enrich each retained row with its explicit primary failure and
   `output_created_before_primary_failure` value;
3. remove exactly `BRM-BUILD-003`, `BRM-BUILD-005`, and `BRM-RETRY-001`;
4. insert the listed replacement rows at the removed row's original position;
5. require exactly 63 effective rows and unique IDs.

The missing-output case is split into no-output and partial-output cases, and
the extra-output case is separate. Timeout, captured-output, private-byte, and
process-count failures each have before-output and after-output rows. Retry is
split across every possible prior primary class.

`/0` is valid only when no admitted output or created residue exists at the
first failed action boundary. `/1` is valid when any admitted output or
created residue exists. Once frozen, the first primary failure is immutable.
Cleanup, quarantine, record, or retry failures are secondary facts and never
replace it. A retry is rejected before input, root, output, or residue reuse
and preserves the exact prior class.

## 6. BRM-IR-005: noncircular deterministic publication

Build root A is the publication owner before either build starts. Root B is
only the comparison peer. Equality cannot cause owner selection, and the
candidate may never choose the better output.

After both runtime trees and manifests compare byte-for-byte equal, the exact
order is:

1. atomically quarantine B under the retained private parent and verify its
   new nonpublication identity;
2. freeze the prepublication record;
3. require the destination to remain absent;
4. atomically rename A once, on the same volume, into a private,
   non-authoritative candidate destination;
5. reopen the final destination through retained parent-relative authority;
6. verify object identity, exact file set, every byte hash, aggregate byte
   count, and manifest hash;
7. freeze and read back the final diagnostic records; and
8. expose only the diagnostic candidate path and records to a later,
   separately gated launcher.

The prepublication record contains exactly the transaction ID, authenticated
admission hashes, A and B staging identities, equality evidence hash,
preselected owner A, comparison peer B, B quarantine receipt hash, retained
destination-parent identity, intended final name, destination-absent
observation, and prepublication state. It must not contain atomic-rename
success, final destination identity, postpublication rehash, or final PASS.

The final materialization record contains the prepublication-record hash,
transaction ID, atomic-rename result, A's prepublication identity, final
destination identity, reopened manifest hash, exact file count, total bytes,
and every final row hash. It is written only after those facts exist.

If B quarantine, prepublication record freeze, destination check, or atomic
rename fails, publication does not occur and the first failure is
`BR-MATERIALIZE/1` or `BR-RECORD/1` at the exact failed boundary. If final
identity verification or final record freeze/read-back fails, the already
published candidate is quarantined and no live or rehearsal authority is
granted. Publication and every record are diagnostic only.

## 7. Machine contracts and equality rules

The v0.2 interface map, admission schema, and mutation matrix are normative.
The semantic relation list in the interface map and schema must be
byte-for-byte identical and executed by one separately authenticated
semantic-validator implementation. String presence is not execution evidence.

The semantic validator must additionally prove:

- exactly one preloader and one guard profile;
- uniqueness and total coverage of runtime roles, module names, DLL names,
  virtual paths, command IDs, tool IDs, and effective mutation IDs;
- all cross-object hash and byte-equality relations;
- exact 63-row mutation reconstruction;
- fixed publication owner A and comparison peer B; and
- identical twelve-field resource limits across the v0.1 profile, v0.1 map,
  v0.2 map, and v0.2 wrapper.

Schema validation or semantic-validator success cannot authorize a build.
The independently pinned outer verifier must authenticate the schema,
validator implementation, admission package, all manifests, and all target
bytes before importing candidate code or starting a process.

## 8. Failure and record authority

The v0.1 failure vocabulary remains unchanged. v0.2 makes its selection
deterministic; it does not add a success authority. Build, binary,
prepublication, final materialization, and semantic-validation records are
canonical public diagnostics only.

No record, published candidate root, schema-valid profile, equal build, or
static inspection result is a reusable capability, native execution approval,
platform-probe result, live decision, rehearsal PASS, or S0 result. A later
operation must reauthenticate original bytes and receive its own exact gate.

## 9. Resource limits

The twelve v0.1 numeric ceilings remain unchanged and are repeated exactly in
the v0.2 map and schema. They are maximums, not evidence that a future build
will fit or finish. Any limit change requires another reviewed design version.

## 10. Review and implementation boundary

A fresh independent reviewer must authenticate the complete v0.1 basis, the
v0.1 independent review, and this exact v0.2 package. It must reconstruct the
wrapper, all 31 semantic relations, the 63-row effective mutation matrix, the
two complete binary profiles, runtime role closure, and publication sequence.

With zero BLOCKING and zero MAJOR findings, CONTROL may consider integrating
the design and then opening a separate implementation candidate gate. That
later gate must supply every currently missing external pin. It may implement
source, validators, inspector, materializer, and build controller, but it does
not automatically authorize build execution.

## 11. Closed boundaries and maximum claim

This revision does not create or validate native source, toolchain, compiler,
SDK, CPython distribution, dependency package, binary, runtime tree, Windows
behavior, platform probe, live assembly, official rehearsal, F0 content,
provider/model call, S0, E0, central system, or Project Brain.

Maximum claim: v0.2 is a bounded public design revision that removes the five
identified machine-contract ambiguities while keeping build, materialization,
native execution, platform, live, and rehearsal authority closed.
