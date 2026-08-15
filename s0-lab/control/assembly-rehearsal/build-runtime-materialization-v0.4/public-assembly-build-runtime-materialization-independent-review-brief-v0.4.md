# S0 v0.14 public assembly build and runtime materialization design v0.4 independent review brief

## 1. Reviewer role

Use one fresh independent PUBLIC design reviewer that did not author, advise,
or QA v0.4. Read the authenticated v0.3 independent review only as the exact
two-finding specification. Do not use an author conversation or another
reviewer conclusion.

Do not implement code, install or run a compiler, create source/runtime
bytes, build or load a binary, call a native API, run a Windows platform
probe, materialize a runtime tree, access F0 content, or run a provider,
model, executor, judge, S0, or E0 task.

## 2. CONTROL-supplied exact values

The assignment must provide literal origin, review branch, HEAD, tree, sole
parent, candidate remote-tracking ref and value, v0.3 review SHA-256, v0.3 and
v0.4 package-manifest SHA-256 values, every v0.4 artifact and sidecar hash,
every predecessor manifest pin below, and both output paths. Do not infer a
value from a moving branch, directory scan, neighboring path, author report,
or prior conversation.

## 3. Maximum PUBLIC inputs

1. `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. the authenticated v0.3 build/runtime package manifest, its nine exact
   targets and sidecars;
4. the v0.3 independent review and sidecar;
5. the v0.4 package manifest, its nine exact targets and sidecars;
6. the authenticated v0.1 build/runtime package manifest, six targets and
   sidecars;
7. the authenticated v0.2 build/runtime package manifest, seven targets and
   sidecars;
8. the authenticated RPNP v0.4 package manifest, six targets and sidecars;
9. the authenticated RPNP integration v0.2 package manifest, six targets and
   sidecars;
10. the authenticated assembly v0.5 package manifest, five targets and
   sidecars;
11. the bounded-integration CONTROL decision and sidecar;
12. the bounded implementation manifest and exact three targets; and
13. the bounded verification manifest and exact four targets.

A manifest target set means only literal paths encoded by the authenticated
manifest. Do not enumerate another directory or read another file. F0 checks
are aggregate-only.

The three Microsoft Learn URLs printed in the authenticated v0.4 design may
be opened only to verify the named public API, enum, and structure contract.
Do not broaden web research or use search results as candidate evidence.

## 4. Integrity procedure

Authenticate Git identity and initial clean state; run canonical validator
SelfTest; authenticate each manifest before targets; validate every Markdown
pair; validate JSON UTF-8, byte-level BOM absence, CR absence, final LF,
trailing whitespace, sidecar, exact hash, and duplicate-key rejection;
validate the v0.1, v0.2, v0.3, v0.4, v0.4 prepublication, and v0.4 final schemas
against Draft 2020-12; resolve the nested absolute base refs exactly; retain
all hashes for final recheck; and stop as `INVALID-REVIEW` only for a real
integrity, input, independence, or F0 failure. Correct ordinary reviewer-local
command errors and continue.

## 5. Required hostile reconstruction

### 5.1 `BRM-V03-IR-001`

Independently implement in memory the canonical directory parser, ASCII
lowercase identity-key transform, exact identity preimage, hashing, duplicate
rejection, order, `FILE_ID_INFO` uniqueness, reparse rejection, and DLL
binding map. Use at least two independent serializers.

Attack case aliases, separator aliases, trailing slash/dot, empty/dot/device
segments, locale or Unicode folding, duplicate identity keys, wrong preimage,
raw-path order, repeated physical identity, reparse point, and every binding
field. Confirm all fail before import or process and cannot be repaired by
selection.

### 5.2 `BRM-V03-IR-002`

Independently reconstruct the exact publication API, DLL, class name and
numeric value, structure, flags, source access and handle, parent handle,
name, byte length, same-volume condition, linearization point, phase order,
failure class, no-retry rule, and both closed record packages.

Model a destination created after recheck and before the call. Require the
no-replace call to fail without changing the destination and forbid final
record, PASS, fallback, retry, new name, live, rehearsal, or S0 authority.
Attack replacement and POSIX flags, alternate APIs/classes, reopened handles,
path recomputation, length drift, cross-volume operation, false success, and
record-field omission/injection.

### 5.3 Nonregression

Reconstruct the effective matrix as exact v0.3 97 plus v0.4 14, for 111
unique IDs. Require one primary failure and Boolean output bit per row.
Compare the exact ordered semantic relations in map and schema, all twelve
resources, authority pins, record-schema bindings, claim limits, and every
nonreplaced v0.3 relation.

Use clearly fake PUBLIC in-memory packages only. Schema validity is never an
execution or semantic PASS.

## 6. Severity and verdict

- `BLOCKING`: denied content, unpinned executable input, live/rehearsal/S0
  authority, or invalid review integrity;
- `MAJOR`: incomplete, contradictory, or multiply interpreted authority,
  directory, binary, runtime, publication, failure, record, resource, or
  provenance behavior;
- `MINOR`: bounded exactness issue unable to affect bytes, authority, or a
  primary conclusion.

Return exactly one:

- `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
  BLOCKING and zero MAJOR;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, input, independence, or F0 failure.

## 7. Evidence limits and outputs

State that no source, compiler, build, binary, runtime tree, native call,
loaded image, platform behavior, live decision, rehearsal, F0 input,
provider/model, S0, or E0 result was created or observed.

Write exactly:

1. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.4/public-assembly-build-runtime-materialization-design-v0.4-independent-review-v0.1.md`;
2. the same-basename `.sha256`.

Run canonical validation and final exact-two-file, input-hash, Git-identity,
F0-aggregate, quiet-diff, and `git diff --check` verification. Do not commit
or push.

With a valid PASS, the exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.4 CONTROL INTEGRATION OPEN`
