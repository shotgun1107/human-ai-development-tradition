# S0 v0.14 public assembly build and runtime materialization design v0.3 independent review brief

## 1. Reviewer role

Use one fresh independent PUBLIC design reviewer that did not author, advise,
or QA v0.3. Read the authenticated v0.2 review only as the exact four-finding
specification. Do not use an author conversation or another reviewer result.

Do not implement code, install or run a compiler, create source/runtime
bytes, build or load a binary, call a native API, run a platform probe,
materialize a runtime tree, access F0 content, or run a provider, model,
executor, judge, S0, or E0 task.

## 2. CONTROL-supplied exact values

The assignment must provide literal origin, review branch, HEAD, tree, sole
parent, candidate remote-tracking ref and value, v0.2 review SHA-256, v0.2 and
v0.3 package-manifest SHA-256 values, every v0.3 artifact and sidecar hash,
every predecessor manifest pin below, and both output paths. Do not infer a
value from a moving branch, directory scan, neighbor, author report, or prior
conversation.

## 3. Maximum PUBLIC inputs

1. `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. the authenticated v0.2 build/runtime package manifest, its seven exact
   targets and sidecars;
4. the v0.2 independent review and sidecar;
5. the v0.3 package manifest, its nine exact targets and sidecars;
6. the authenticated RPNP v0.4 package manifest, six targets and sidecars;
7. the authenticated RPNP integration v0.2 package manifest, six targets and
   sidecars;
8. the authenticated assembly v0.5 package manifest, five targets and
   sidecars;
9. the bounded-integration CONTROL decision and sidecar;
10. the bounded implementation manifest and exact three targets; and
11. the bounded verification manifest and exact four targets.

A manifest target set means only literal paths encoded by that manifest after
the manifest matches its external pin. Do not enumerate another directory or
read another file. F0 verification is aggregate-only.

## 4. Integrity procedure

Authenticate Git identity and clean state; run canonical validator SelfTest;
authenticate each manifest before targets; validate every Markdown pair;
validate JSON UTF-8, byte-level BOM absence, CR absence, final LF, trailing
whitespace, sidecar, and exact hash; reject duplicate JSON keys; validate all
four schemas against Draft 2020-12 metaschema; resolve the v0.3 absolute base
and record references to exact authenticated schemas; retain hashes for final
recheck; and stop as `INVALID-REVIEW` only for a real integrity, input,
independence, or F0 failure. Correct ordinary reviewer-local command errors
and continue.

## 5. Required bounded hostile reconstruction

### 5.1 BRM-V02-IR-001

Independently serialize the target-set preimage. Attack grammar, encoding,
line endings, paths, order, duplicate, empty, decimal, count, length, target
hash, total bytes, and final LF. Require failure before import or process.

### 5.2 BRM-V02-IR-002

Reconstruct the preloader's two and guard's eleven direct imports from
authenticated RPNP v0.4. Attack owner role, owner DLL, order, omission, extra,
guard export, and full import-allowlist equality. Confirm byte-bound static
inspection never loads a target.

### 5.3 BRM-V02-IR-003

Independently derive the application directory, ordered unique DLL-parent
directories, directory identity hashes, and DLL resolution bindings. Attack
missing, extra, duplicate, reorder, case collision, host/PATH/registry/current
directory fill, application role, path, index, and hash.

### 5.4 BRM-V02-IR-004

Reconstruct both closed record packages and exact publication phase order.
Attack missing, unknown, and cross-boundary fields; body order and codec;
close/readback hashes; stale or skipped destination recheck; parent/name
change; destination race; final record before all rehash facts; duplicate
publication; and failure-to-authority promotion.

### 5.5 Nonregression

Reconstruct the 97-row matrix as exact v0.2 63 plus v0.3 34. Require one
primary failure and Boolean output bit per row. Compare the exact 42 semantic
relations in map and schema, all twelve resources, claim limits, and every
nonreplaced v0.2 relation.

## 6. Severity and verdict

- `BLOCKING`: denied content, unpinned executable input, live/rehearsal/S0
  authority, or invalid review integrity;
- `MAJOR`: incomplete, contradictory, or multiply interpreted authority,
  binary, runtime, failure, publication, resource, or provenance behavior;
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

1. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.3/public-assembly-build-runtime-materialization-design-v0.3-independent-review-v0.1.md`;
2. the same-basename `.sha256`.

Run canonical validation and final exact-two-file, input-hash, Git-identity,
F0-aggregate, quiet-diff, and `git diff --check` verification. Do not commit
or push.

With a valid PASS, the exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.3 CONTROL INTEGRATION OPEN`
