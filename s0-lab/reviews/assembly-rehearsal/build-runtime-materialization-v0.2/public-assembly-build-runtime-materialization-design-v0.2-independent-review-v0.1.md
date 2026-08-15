# S0 v0.14 public assembly build and runtime materialization design v0.2 independent review

- `status`: completed fresh independent PUBLIC design review
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: `0 BLOCKING / 4 MAJOR / 0 MINOR`
- `implementation_observed`: none for the v0.2 design
- `compiler_or_build_observed`: none
- `runtime_materialization_or_native_execution_observed`: none
- `F0_content_access`: none

## 1. Role and integrity result

I acted only as the fresh independent PUBLIC design reviewer. I did not
author, advise on, or QA v0.2, and I did not use an author conversation or
another review conclusion. I read the authenticated v0.1 review only as the
five-finding specification.

The CONTROL-supplied Git identity matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- review branch:
  `codex/s0-build-runtime-materialization-design-v02-review`;
- HEAD:
  `5aca01a210a436f1be67bdfbc1fb2859af68f5f9`;
- tree:
  `a0355b83d278640baa724dc56698d9d7f4ad22e3`;
- sole parent:
  `28f63ad7abafbef1e6d3574315d12b04def514fb`; and
- candidate remote-tracking ref value:
  `5aca01a210a436f1be67bdfbc1fb2859af68f5f9`.

The initial worktree change count was zero. The canonical text validator
SelfTest passed. Every externally supplied package-manifest pin matched before
its literal targets were read. The authenticated logical-target counts were
exactly `6 / 7 / 6 / 6 / 5 / 3 / 4` for build/runtime v0.1, build/runtime
v0.2, RPNP v0.4, RPNP integration v0.2, assembly v0.5, bounded
implementation, and bounded verification. Every listed target hash matched.

The v0.1 review SHA-256 matched
`85c917496b04246be173dafa2ffd729fa80e836d363de0ab982f593c42efa292`.
The v0.2 package-manifest SHA-256 matched
`47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`.
All seven v0.2 artifact hashes and all seven externally supplied sidecar
hashes matched.

All 22 admitted Markdown/sidecar pairs passed the canonical validator
separately. All 11 admitted JSON files passed strict UTF-8 decoding, UTF-8 BOM
absence, CR absence, final-LF, trailing-whitespace, canonical-sidecar, exact
hash, and duplicate-key rejection checks. The v0.1 and v0.2 schemas passed
the Draft 2020-12 metaschema. The v0.2 absolute reference
`urn:s0:public-assembly:build-runtime-materialization:profile:1` resolved to
the exact authenticated v0.1 schema with that `$id`.

The F0 aggregate inventory was `32 / 11 / 10`. Worktree and parent quiet-diff
exits were `0 / 0 / 0`; local-status, skip-worktree, and assume-unchanged
counts were all zero. No F0 filename or content was read.

Reviewer-local Git pathspec, PowerShell array binding and execution-policy,
schema-sidecar basename, Python quoting, and fake-placeholder formatting
errors were corrected and rerun. They changed no candidate byte and are not
candidate findings.

## 2. Bounded reconstruction result

### 2.1 BRM-IR-001 authority closure

The wrapper requires the four previously omitted retained authorities, the
v0.2 package hash, and a fresh review hash. It represents eight manifest pin
classes plus the canonical embedded base-profile hash and approving-review
hash. The embedded base profile is an absolute-reference v0.1 instance rather
than a direct executable profile. Removal of all six authority-extension
fields, all eight external-pin classes, and all 32 nested manifest-identity
fields was rejected by schema validation.

The integration-v0.1 manifest pin is not an unresolved predecessor claim. The
authenticated integration-v0.2 package independently carries
`f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b`,
which equals the v0.2 wrapper constant.

Finding BRM-V02-IR-001 remains because the new target-set digest has no one
constructible meaning.

### 2.2 BRM-IR-002 binary closure

The schema requires exactly two closed 35-field binary profiles. All 70
required-field removals, all 28 nonzero-predicate mutations, and all 12 tested
role, direct-import, export, mitigation, relocation, and load-state mutations
were rejected. Artifact, section, import, export, allowlist, relocation,
resource, Windows-manifest, and load-config digests are byte-shaped and the
static-inspector load flag is fixed false.

Finding BRM-V02-IR-002 remains because the role-specific direct-import
assignment contradicts the effective authenticated RPNP contract.

### 2.3 BRM-IR-003 runtime closure

The 14 runtime role keys are identical and in the same order in the interface
map and schema. All 22 runtime-policy field removals and all 14 role-key
removals were rejected. The schema binds CPython 3.12 Windows AMD64, ordered
`-I / -S / -B`, jsonschema 4.26.0, source-only module mapping, DLL mapping,
application selection, bytecode denial, and the named ambient denials.
Uniqueness and total coverage are correctly identified as semantic-validator
relations rather than falsely claimed as JSON Schema properties.

Finding BRM-V02-IR-003 remains because the allowed DLL-search directories and
their construction are not represented.

### 2.4 BRM-IR-004 failure matrix

Independent reconstruction passed. The authenticated base has 46 unique
rows. Removing exactly `BRM-BUILD-003`, `BRM-BUILD-005`, and
`BRM-RETRY-001` leaves 43 retained rows in base order. Inserting the listed
`3 / 8 / 9` replacement groups at the removed rows' positions produces
exactly 63 unique rows. Every row has one Boolean output state, and every
failure suffix agrees with that Boolean. All nine retry rows preserve one of
the exact prior primary classes. Cleanup, quarantine, record, and retry
failures are expressly secondary and cannot replace the frozen first fault.

No finding remains under BRM-IR-004.

### 2.5 BRM-IR-005 publication and records

The design now preselects A as owner, makes B the comparison peer, quarantines
B before A publication, separates prepublication and final records, limits
publication to one same-volume atomic rename, verifies the reopened final
identity and bytes before the final record, and grants no authority after a
later failure.

Finding BRM-V02-IR-004 remains because the machine contract neither defines
the two record field schemas nor includes the required last-moment
destination-absence recheck in its ordered publication phases.

## 3. Cross-file and hostile-test results

The interface map and schema contain the same 31 semantic relations in the
same order. The twelve resource fields and values are exactly equal across
the v0.1 map, v0.1 schema, v0.2 map, and v0.2 schema. Every typed object added
by v0.2 is closed with `additionalProperties: false`, and its property set is
its required set. Required-property and unknown-property mutations rejected
at all 14 tested new object depths.

All 91 digest-named fields in one clearly fake PUBLIC in-memory admission
package rejected uppercase mutations. That fake package validated first as an
embedded v0.1 profile and then as a v0.2 wrapper through the authenticated
absolute reference. It was never persisted or treated as an execution input.
Schema validity was not treated as semantic acceptance: duplicate roles,
module names, DLL names, virtual paths, and uncovered base rows still require
the separately authenticated semantic validator.

The external-pin hostile reconstruction covered missing, uppercase,
malformed, all-zero, predecessor, moving, candidate-selected,
valid-shaped-but-unauthenticated, count, byte-count, target-set, and
cross-object mismatch cases. The design assigns the correct pre-import or
pre-process failure family, but BRM-V02-IR-001 prevents one exact target-set
comparison from being implemented without invention.

The publication hostile reconstruction covered B selection, result-based
selection, unquarantined B, prepublication overclaim, destination race,
repeated or cross-volume publication, final record before rehash,
postpublication mutation, and failure-to-authority promotion. The prose
rejects each, but BRM-V02-IR-004 leaves the record boundary and destination
recheck outside the closed machine contract.

## 4. Findings

### BRM-V02-IR-001 — MAJOR — `target_set_sha256` has no canonical construction

Each external manifest identity requires `manifest_sha256`, `target_count`,
`total_target_bytes`, and `target_set_sha256`. The design says the last field
binds the exact target set, but no v0.2 artifact defines the bytes to hash,
path encoding, row grammar, ordering, inclusion of target digests or lengths,
or duplicate/collision handling. The 31 semantic relations also contain no
construction rule for this value.

Counterexample: one implementation hashes ASCII-sorted
`path + digest` records while another hashes the ordered target digests only.
Both can authenticate the same manifest and targets and both can describe
their lowercase result as the target-set hash. The schema accepts either, so
the external authority identity remains multiply interpreted before import or
process creation.

Required correction: freeze one canonical byte grammar and ordering for the
target-set preimage, including path, digest, length, duplicate, and empty-set
rules; add an exact semantic relation; and require the hostile target-set
tests to use that construction.

### BRM-V02-IR-002 — MAJOR — `NtCreateFile` is assigned to the wrong binary role

The authenticated RPNP v0.4 schema binds
`atomic_root_policy.direct_import` to `ntdll.dll!NtCreateFile`, and its process
creation policy binds `kernel32.dll!CreateProcessW`. The authenticated
integration v0.2 design says the native preloader alone performs the sole
`NtCreateFile` transaction. The authenticated RPNP guard contract instead
lists its guard observation calls and does not assign root creation to the
guard.

The v0.2 binary schema nevertheless fixes the preloader's
`required_direct_imports` to only `kernel32.dll!CreateProcessW` and fixes the
guard's list to `ntdll.dll!NtCreateFile`. This contradicts the relation that
guard exports and direct-import assignments equal the effective RPNP design.
Complete allowlist-manifest hashes cannot repair a wrong role-specific
requirement.

Counterexample: a schema-valid package makes the guard import
`NtCreateFile` and omits the preloader's required root-creation import. It
passes the structural role conditions but cannot implement the authenticated
preloader-only root transaction.

Required correction: bind the preloader's exact complete required direct
imports, including both root creation and process creation, and bind the
guard's actual effective direct-import closure. Make the interface map and
role-specific hostile tests compare those exact lists to RPNP v0.4.

### BRM-V02-IR-003 — MAJOR — DLL search directories are named but not bound

The runtime wrapper has an exact DLL map and the constant label
`application-directory-and-explicit-authenticated-runtime-directories-only`.
It has no field for the allowed directory set or order, no canonical rule that
derives those directories from the DLL map or base runtime rows, and no
semantic relation connecting the actual search list to such a derivation.
The existing DLL relation proves only that map entries reference
authenticated rows.

Counterexample: two implementations use the same schema-valid role and DLL
maps, while one searches only each mapped DLL's parent and the other adds a
different authenticated runtime directory. Both satisfy the policy label,
but name collision and dependency resolution can select different bytes.

Required correction: encode one exact ordered, unique DLL-search-directory
inventory or one canonical derivation from authenticated runtime rows; bind
application-directory treatment and every DLL resolution to it; and reject
missing, added, reordered, host-filled, or registry/PATH-derived directories.

### BRM-V02-IR-004 — MAJOR — publication records and the destination recheck are not machine-closed

The schema and interface map carry only the string identifiers
`S0-PUBLIC-ASSEMBLY-RUNTIME-MATERIALIZATION-PREPUBLISH-RECORD-2` and
`S0-PUBLIC-ASSEMBLY-RUNTIME-MATERIALIZATION-FINAL-RECORD-2`. No admitted
artifact defines either record as a closed object with the exact fields listed
in the design. Consequently, required-field omission, unknown-field addition,
and forbidden cross-boundary field placement cannot be rejected by the
machine contract.

The prose also requires a destination-absent recheck after the prepublication
record is frozen and immediately before the atomic A rename. The interface
map and schema's six publication phases jump directly from
`PREPUBLICATION-RECORD-FROZEN` to `RUNTIME-A-ATOMICALLY-PUBLISHED`; no phase,
field, or semantic relation binds that recheck.

Counterexample: an implementation freezes a prepublication record containing
an extra final-identity field, observes destination absence only before that
freeze, skips the required recheck, and attempts the rename after another
actor creates the destination. The machine phase sequence and record-schema
ID strings cannot distinguish this from the required transaction.

Required correction: add exact closed schemas for both records with all
required and forbidden fields, include close/read-back hashes, add an explicit
destination-absent-recheck phase between prepublication freeze and rename,
and bind its retained-parent observation and failure precedence in the map,
schema, relations, and hostile matrix.

## 5. Nonregression and evidence limits

The revision retains two clean builds, all-output byte equality, exact source
and offline-toolchain closure, unsigned static binary inspection without
loading, exact runtime paths and file set, later preloader-only root creation,
later real-Windows handle/decoy/loaded-image/atomicity probes, diagnostic-only
records and candidate roots, and closed F0, provider/model, live, rehearsal,
S0, E0, central-system, and Project Brain boundaries.

The authenticated bounded predecessor remains an offline Python diagnostic
with `candidate_only=true`, `native_api_reachable=false`, and
`rehearsal_pass=false`. I did not execute that implementation or its verifier.

This review is design evidence only. No build/runtime-materialization source,
compiler, build, binary, runtime tree, native call, loaded image, platform
behavior, live decision, rehearsal, F0 input, provider/model task, S0 result,
or E0 result was created or observed. No implementation, compiler/build,
native/runtime/platform probe, provider/model, executor, judge, S0, or E0
operation was run.

## 6. Verdict and remaining gate

Verdict: `REVISE-AND-REVIEW`.

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 4 |
| MINOR | 0 |

The PASS-only gate
`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.2 CONTROL INTEGRATION OPEN`
is not opened. The required next action is a bounded design revision followed
by a fresh independent review of the revised exact package.

No commit or push was authorized or performed.
