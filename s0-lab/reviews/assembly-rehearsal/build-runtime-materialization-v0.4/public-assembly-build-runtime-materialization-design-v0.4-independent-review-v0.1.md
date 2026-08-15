# S0 v0.14 public assembly build and runtime materialization design v0.4 independent review

- status: completed fresh independent PUBLIC design review
- verdict: REVISE-AND-REVIEW
- finding counts: 0 BLOCKING / 2 MAJOR / 0 MINOR
- implementation observed: none for the v0.4 design
- compiler or build observed: none
- runtime materialization or native execution observed: none
- F0 content access: none

## 1. Role and integrity result

I acted only as the fresh independent PUBLIC design reviewer. I did not
author, advise on, or QA v0.4, and I did not use an author conversation or
another reviewer conclusion. I read the authenticated v0.3 independent review
only as the exact two-finding specification.

The CONTROL-supplied Git identity matched exactly:

- origin:
  https://github.com/shotgun1107/human-ai-development-tradition.git;
- review branch:
  codex/s0-build-runtime-materialization-design-v04-review;
- HEAD and candidate remote-tracking ref:
  ab4e32871aea00b3d49580778a9c05de31ac0b79;
- tree:
  3b51cc794fc9a76e038ef02e1e09160c16e78528; and
- sole parent:
  bea7c81b359585abcd3479510feaac2b8c1d0ece.

The initial tracked and untracked change counts were zero. The canonical text
validator SelfTest passed. All nine externally pinned package manifests
matched before their targets were used. Their authenticated target counts
were exactly 6 / 7 / 9 / 9 / 6 / 6 / 5 / 3 / 4 for build/runtime v0.1,
v0.2, v0.3, v0.4, RPNP v0.4, RPNP integration v0.2, assembly v0.5, bounded
implementation, and bounded verification. All 55 literal target hashes
matched. The externally pinned v0.3 review pair, bounded CONTROL decision
pair, and all 18 supplied v0.4 artifact and sidecar hashes also matched.

All 30 admitted Markdown/sidecar pairs passed the canonical validator. All 21
admitted JSON/sidecar pairs passed strict UTF-8, byte-level UTF-8 BOM absence,
CR absence, final-LF, trailing-whitespace, canonical-sidecar, exact-hash, and
duplicate-key checks. All ten admitted schemas passed the Draft 2020-12
metaschema. All five nested absolute reference occurrences resolved through
the exact authenticated v0.1, v0.2, v0.3, and v0.4 schema set.

The three Microsoft Learn pages named by the authenticated design were opened
directly without broader research. They corroborated the
kernel32.dll SetFileInformationByHandle signature and DLL, the
FILE_INFO_BY_HANDLE_CLASS ordering that gives FileRenameInfoEx numeric value
22, and the FILE_RENAME_INFO Flags, RootDirectory, FileNameLength, and
FileName fields.

Reviewer-local execution-policy, command-quoting, matrix-field-name,
line-ending, and schema-generator errors were corrected and rerun. They
changed no candidate byte and are not candidate findings.

## 2. Bounded hostile reconstruction result

### 2.1 BRM-V03-IR-001 directory identity

The directory correction is constructible in isolation. Independent Python
and PowerShell serializers produced the same 912-byte ASCII/LF fake-PUBLIC
inventory and SHA-256
be10a6bff3d68ae8b49984bfdacd4c671bf255edb5a0bb69fdfeb00ac6f394f8.
The application identity key was index zero, followed by alpha/lib, beta/bin,
and zoo/bin in unsigned-ASCII identity-key order, which differed from the
case-preserving raw-path order.

The reconstruction implemented the strict directory parser, locale-free ASCII
lowercase transform, exact identity-key preimage and final LF, duplicate-key
rejection before hashing, FILE_ID_INFO pair uniqueness, reparse rejection,
and all six DLL-binding fields. Forty-six hostile cases covered empty,
leading, trailing, doubled, backslash, dot, dotdot, trailing-dot, control,
DEL, non-ASCII, overlength, and DOS-device paths; case and separator aliases;
wrong identity transforms and preimages; raw-path ordering; repeated or
malformed physical identities; reparse points; every binding field; and
host, PATH, registry, current-directory, user-site, and environment fill.
Every case stopped as BR-AUTH/0 before import or process creation, with no
output, and none was repaired by selecting one alias.

Result: the specific BRM-V03-IR-001 counterexample is closed by the v0.4
directory rules.

### 2.2 BRM-V03-IR-002 no-replace publication

The exact positive transaction was independently reconstructed as:

- kernel32.dll!SetFileInformationByHandle;
- FileRenameInfoEx class 22;
- FILE_RENAME_INFO.Flags equal to zero;
- replace-if-exists and POSIX-semantics bits unset;
- the retained runtime-A source handle with DELETE and SYNCHRONIZE;
- the same retained destination-parent handle and final leaf used by the
  recheck;
- exact UTF-16LE filename byte length without a terminal NUL;
- same-volume operation; and
- successful call as the sole publication linearization point.

For a clearly fake PUBLIC transaction, the schema's 20-field policy object
serialized to 896 RFC 8785-compatible JCS/UTF-8/final-LF bytes with SHA-256
3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b.
The exact 239-byte source-handle preimage hashed to
97bcb404e4118cad10cab90cf37e0dd1d0a65606af95c1665a57f7d03a306aa9.
The exact 304-byte parent-handle preimage hashed to
db64e1a08c0f307f021b44030f4e056966a03078d4ffde11821c0adcd6f2d4d7.
The fake final leaf had an exact 26-byte UTF-16LE length.

The absent-success, present-at-recheck, and created-after-recheck traces were
modeled without a native call. In the race trace, the intervening destination
remained unchanged, the call failed as BR-MATERIALIZE/1 with output bit one,
and no final record or authority was available. Twenty-six API, DLL, class,
structure, flags, access, handle, name, length, preimage, policy, volume,
retry, fallback, new-name, overwrite, delete, false-success, final-record,
PASS, live, rehearsal, and S0 attacks all rejected.

Two fake closed record packages validated. Seventy-four required-field
deletion, unknown-field, field-order, cross-boundary, target-row, and
success-field attacks rejected. The exact eleven publication phases, source
and parent bindings, failure class, no-retry rule, and postpublication
evidence boundary were preserved.

Result: the specific BRM-V03-IR-002 race counterexample is closed by the exact
v0.4 no-replace call in isolation.

### 2.3 Schemas, matrix, resources, and predecessor closure

One generated fake PUBLIC nested v0.4 admission package and the two v0.4
record packages validated through the authenticated v0.1 to v0.4 schema
chain. At twelve new v0.4 object depths, 131 required-field deletion and
unknown-field mutations all rejected. Uppercase and wrong-length digests
failed schema validation; all-zero or different meaningful hashes failed
their required semantic recomputation rather than receiving execution
authority.

The mutation matrix reconstructed as the v0.1 46 rows, exact v0.2 replacement
composition to 63 rows, 34 appended v0.3 rows, and 14 appended v0.4 rows.
The effective result was 111 unique IDs in the published order. Every row had
one nonempty primary failure and one Boolean output bit whose /0 or /1 suffix
agreed with that bit. Later cleanup, quarantine, record, and retry facts did
not replace the first primary failure.

The exact twelve resource values were equal across the v0.2 map and schema,
v0.3 schema, and v0.4 map and schema. All v0.4 predecessor package, review,
profile-schema, record-schema, and matrix pins matched authenticated bytes.
The v0.4 record schema IDs matched their profile bindings, and direct v0.3
execution remained forbidden.

The authenticated RPNP and integration packages independently fixed the
preloader direct imports to CreateProcessW then NtCreateFile, the guard direct
imports to the exact eleven RPNP observation calls, the guard export to
PyInit_s0_runtime_handle_guard_v0_4, and sole NtCreateFile root creation to the
native preloader. Full role import sets remain bound to separately
authenticated allowlist manifests. Static inspection of the exact bounded
implementation found only the offline bridge and fixed
candidate_only=true, native_api_reachable=false, and rehearsal_pass=false.
The candidate and its verifier were not executed.

The map/schema relation arrays were internally equal for v0.2, v0.3, and
v0.4, and each array had unique entries. The cross-version exact-retention
comparison and the no-replace policy-object comparison produced the two
findings below.

## 3. Findings

### BRM-V04-IR-001 — MAJOR — one nonreplaced v0.3 semantic relation is silently changed

Artifacts:
build-runtime-materialization-interface-map-v0.3.json semantic_relations[15];
build-runtime-materialization-interface-map-v0.4.json
semantic_relations[15]; build-runtime-materialization-profile-v0.4.schema.json
semantic_relations; and
public-assembly-build-runtime-materialization-design-revision-v0.4.md
Sections 1 and 4.

Fact: the authenticated v0.3 map and schema publish the exact relation
application-directory-equals-parent-of-verifier-application-runtime-row.
The v0.4 map and schema instead require
application-directory-equals-parent-of-verifier_application-runtime-row.
Only 41 of the 42 v0.3 relation byte strings are retained. The mismatch is at
one-based position 16.

Contradiction: v0.4 says that its two corrections replace only the rules
affected by BRM-V03-IR-001 and BRM-V03-IR-002, and that every other v0.3
relation remains exactly effective. Neither finding concerns the
application-directory source-role relation, and the v0.4 matrix contains no
declared replacement for it.

Counterexample: an exact-ID semantic validator dispatches the authenticated
v0.3 relation name and correctly reports it missing from the v0.4 required
array. A different validator treats the underscore spelling as a replacement
and executes it. Both behaviors are compatible with different parts of the
package, so exact nonregression and validator coverage are not uniquely
defined.

Required correction: restore the exact v0.3 relation byte string in the v0.4
map and schema. If a semantic change was intended, declare one exact
replacement mapping, update the composition and mutation inventory, and
explain why it is within the opened revision scope.

Impact: a nonreplaced runtime-resolution relation can be omitted or
reinterpreted by an exact-ID semantic validator. This affects required
runtime/provenance validation and is not a formatting-only defect.

### BRM-V04-IR-002 — MAJOR — the publication policy hash has two different same-named preimages

Artifacts: build-runtime-materialization-interface-map-v0.4.json
publication_no_replace_policy;
build-runtime-materialization-profile-v0.4.schema.json
publication_no_replace_policy and publication_no_replace_policy_sha256; and
public-assembly-build-runtime-materialization-design-revision-v0.4.md
Section 3.1.

Fact: the interface map's publication_no_replace_policy object has 17 fields.
The profile schema's same-named constant object has 20 fields. The schema adds
posix_semantics_flag_set=false, replace_if_exists_flag_set=false, and
source_handle_required_access=[DELETE,SYNCHRONIZE]. All 17 shared fields are
equal, but the objects are not.

Independent JCS serializers agreed that the map object produces 771 bytes and
SHA-256
327496706b587346b9ac749d49e4545cc5a8842e937579fdfbd7d16970ca1998,
while the schema object produces 896 bytes and SHA-256
3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b.
Both digests satisfy the profile's lowercase SHA-256 shape. The semantic
relation says only to hash the policy object and does not identify which of
the two same-named objects is normative.

Counterexample: one validator hashes the authenticated interface-map object
and records 327496..., while another hashes the profile instance's required
20-field constant and records 3fd2df.... JSON Schema accepts either digest in
publication_no_replace_policy_sha256, and both validators can claim that they
hashed the exact publication_no_replace_policy object. The prepublication
record can therefore bind two incompatible policy identities.

Required correction: publish one byte-identical closed policy object in the
map and schema, or explicitly name one object as the sole hash preimage and
rename the other as a nonauthoritative summary. Bind the expected construction
unambiguously in the design, semantic relation, record path, and mutations.

Impact: the access and flag-set facts are part of the publication authority
closure, and the ambiguity changes policy and record hashes. This is a
provenance and record-identity defect.

## 4. Nonregression and evidence limits

The two v0.3 findings are constructibly closed by the isolated v0.4 directory
and no-replace rules, but the new relation-retention and policy-preimage
defects prevent the complete package from having one machine interpretation.
No schema or semantic validation result was treated as an execution PASS.

This review is design evidence only. No source, compiler, build, binary,
runtime tree, native call, loaded image, platform behavior, live decision,
rehearsal, F0 input, provider/model task, S0 result, or E0 result was created
or observed. No implementation, compiler/build, native/runtime/platform probe,
provider/model, executor, judge, S0, or E0 operation was run.

## 5. Verdict and remaining gate

Verdict: REVISE-AND-REVIEW.

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 2 |
| MINOR | 0 |

The PASS-only gate
S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME
MATERIALIZATION DESIGN V0.4 CONTROL INTEGRATION OPEN is not opened. The
required next action is a bounded public design revision followed by a fresh
independent review of the exact revised package.

No commit or push was authorized or performed.
