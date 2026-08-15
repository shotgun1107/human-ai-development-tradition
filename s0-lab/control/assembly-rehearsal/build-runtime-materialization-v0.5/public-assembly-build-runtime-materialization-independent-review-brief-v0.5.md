# S0 v0.14 public assembly build and runtime materialization design v0.5 independent review brief

## 1. Reviewer role

Use one fresh independent PUBLIC design reviewer that did not author, advise,
or QA v0.5. Read the authenticated v0.4 independent review only as the exact
two-finding specification. Do not use an author conversation or another
reviewer conclusion.

Do not implement code, install or run a compiler, create source/runtime bytes,
build or load a binary, call a native API, run a platform probe, materialize a
runtime tree, access F0 content, or run a provider, model, executor, judge, S0,
or E0 task.

## 2. CONTROL-supplied exact values

The assignment must provide literal origin, review branch, HEAD, tree, sole
parent, candidate remote-tracking ref and value, v0.4 review SHA-256, v0.1
through v0.5 package-manifest SHA-256 values, every v0.5 artifact and sidecar
hash, and both output paths. Do not infer a value from a moving branch,
directory scan, neighboring path, author report, or prior conversation.

## 3. Maximum PUBLIC inputs

1. `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. the authenticated v0.1 build/runtime package manifest, its six exact
   targets and sidecars;
4. the authenticated v0.2 build/runtime package manifest, its seven exact
   targets and sidecars;
5. the authenticated v0.3 build/runtime package manifest, its nine exact
   targets and sidecars;
6. the authenticated v0.4 build/runtime package manifest, its nine exact
   targets and sidecars;
7. the authenticated v0.4 independent review and sidecar; and
8. the v0.5 package manifest, its seven exact targets and sidecars.

A manifest target set means only literal paths encoded by the authenticated
manifest. Do not enumerate another directory or read another file. F0 checks
are aggregate-only.

The v0.5 revision changes no Windows API fact. Do not browse or perform a
platform probe. Treat the authenticated v0.4 review's bounded API finding
closure only as predecessor design evidence, not as observed runtime behavior.

## 4. Integrity procedure

Authenticate Git identity and initial clean state; run canonical validator
SelfTest; authenticate each manifest before targets; validate every Markdown
pair; validate JSON UTF-8, byte-level BOM absence, CR absence, final LF,
trailing whitespace, sidecar, exact hash, and duplicate-key rejection;
validate the v0.1 through v0.5 schemas against Draft 2020-12; resolve every
nested absolute base reference only through the exact authenticated schema
registry; retain all hashes for final recheck; and stop as `INVALID-REVIEW`
only for a real integrity, input, independence, or F0 failure. Correct ordinary
reviewer-local command errors and continue.

## 5. Required hostile reconstruction

### 5.1 `BRM-V04-IR-001`

Independently reconstruct the v0.4 68-entry relation array and apply the exact
zero-based index-15 patch. Prove all other bytes, indices, order, uniqueness,
and count are retained. Use two independent serializers for the exact
`S0-BRM-SEMANTIC-RELATIONS-5` preimage and require 6,805 bytes plus SHA-256
`5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`.

Attack the required old and new values, index, other relations, order, count,
duplicates, grammar, decimal form, ASCII/LF framing, and digest. Prove every
case fails `BR-AUTH/0` before import or process and cannot fall back to direct
v0.4 execution.

### 5.2 `BRM-V04-IR-002`

Resolve only `base_profile.publication_no_replace_policy` as normative.
Independently reconstruct its exact 20-field object. Use two independent JCS
serializers and require 896 UTF-8-plus-final-LF bytes and SHA-256
`3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`.

Attack the historical 17-field map summary, source path, field set and values,
array order, serialization, final LF, base digest, outer digest, and both
record bindings. Prove there is one hash authority and no schema-only or
caller-selected alternate.

### 5.3 Package and nonregression

Build clearly fake PUBLIC in-memory v0.5 packages through the exact v0.1 to
v0.5 schema registry. Delete every new required field and inject unknown
fields at every new object depth. Attack all consts and meaningful hashes.

Reconstruct the exact effective matrix as 111 authenticated v0.4 rows plus
four published v0.5 rows, for 115 unique IDs. Require one primary failure and
one matching output bit per row. Confirm that every other v0.4 rule, relation,
record, resource, authority, runtime/binary rule, failure precedence, and claim
limit remains unchanged.

## 6. Severity and verdict

- `BLOCKING`: denied content, unpinned executable input, live/rehearsal/S0
  authority, or invalid review integrity;
- `MAJOR`: incomplete, contradictory, or multiply interpreted relation,
  policy, authority, record, failure, provenance, or nonregression behavior;
- `MINOR`: bounded exactness issue unable to affect bytes, authority, record
  identity, or a primary conclusion.

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

1. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.5/public-assembly-build-runtime-materialization-design-v0.5-independent-review-v0.1.md`;
2. the same-basename `.sha256`.

Run canonical validation and final exact-two-file, input-hash, Git-identity,
F0-aggregate, quiet-diff, and `git diff --check` verification. Do not commit or
push.

With a valid PASS, the exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.5 CONTROL INTEGRATION OPEN`
