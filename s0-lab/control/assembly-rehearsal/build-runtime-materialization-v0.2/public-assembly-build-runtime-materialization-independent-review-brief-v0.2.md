# S0 v0.14 public assembly build and runtime materialization design v0.2 independent review brief

## 1. Reviewer role

Use one fresh independent PUBLIC design reviewer that did not author, advise
on, or QA v0.2. The reviewer may read the authenticated v0.1 review only as
the exact finding specification, not as evidence that v0.2 closes it.

Do not implement code, install or run a compiler, create source or runtime
bytes, build or load a binary, call a native API, run a platform probe,
materialize a runtime tree, access F0 content, or run a provider, model,
executor, judge, S0, or E0 task.

## 2. Exact values CONTROL must supply

The assignment must provide literal origin, review branch, HEAD, tree, sole
parent, candidate remote-tracking ref and value, v0.1 review SHA-256, v0.1 and
v0.2 package-manifest SHA-256 values, every v0.2 artifact and sidecar hash,
every predecessor manifest pin named below, and the two output paths.

Do not infer a value from a moving branch, directory scan, neighboring file,
author report, previous conversation, or expected name.

## 3. Exact maximum PUBLIC inputs

The maximum input set is:

1. `AGENTS.md`;
2. `s0-lab/control/tools/verify-text-artifacts.ps1`;
3. `s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.1/design-package-files.sha256`, its exact six logical targets, and their same-basename sidecars;
4. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.1/public-assembly-build-runtime-materialization-design-v0.1-independent-review-v0.1.md` and sidecar;
5. `s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.2/design-package-files.sha256`, its exact logical targets, and their same-basename sidecars;
6. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`, its exact six targets, and their same-basename sidecars;
7. `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/design-package-files.sha256`, its exact six targets, and their same-basename sidecars;
8. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/design-package-files.sha256`, its exact five targets, and their same-basename sidecars;
9. `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.2/bounded-integration-implementation-v0.1-control-integration-and-main-merge-decision-v0.1.md` and sidecar;
10. `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/implementation-files.sha256` and its exact three targets; and
11. `s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/verification-files.sha256` and its exact four targets.

A manifest target set means only the literal paths encoded by that manifest
after the manifest matches the external pin. Do not enumerate another
directory or read another file. F0 verification is aggregate-only.

## 4. Integrity procedure

1. authenticate exact Git identity and initial clean state;
2. run canonical validator SelfTest;
3. authenticate each package manifest before reading its targets;
4. validate each Markdown/sidecar pair separately;
5. validate JSON UTF-8, BOM absence by leading bytes, CR absence, final LF,
   trailing whitespace, canonical sidecar, and exact hash;
6. parse every JSON with duplicate-key rejection;
7. validate v0.1 and v0.2 schemas against Draft 2020-12 metaschema;
8. resolve the v0.2 absolute `$ref` ID to the exact authenticated v0.1 schema;
9. retain all input hashes for one final recheck; and
10. stop as `INVALID-REVIEW` on a real integrity, input, independence, or F0
   failure.

Correct and rerun ordinary reviewer-local command, quoting, library, or output
parser errors. They are not candidate findings unless candidate bytes caused
them.

## 5. Required bounded hostile reconstruction

Independently reconstruct only the five predecessor findings and associated
nonregression surface. Do not reopen unrelated policy design.

### 5.1 BRM-IR-001

Prove all retained authority and ten external pin classes are exact and
non-self-referential. Attack missing, malformed, placeholder,
candidate-selected, moving, predecessor, target-count, byte-count, target-set,
and cross-object equality cases. Require failure before import or process.

### 5.2 BRM-IR-002

Reconstruct the two binary profiles. Mutate every required field, zero count,
role-specific direct import/export, allowlist, mitigation, and identity chain.
Confirm inspection is byte-bound and never loads the target.

### 5.3 BRM-IR-003

Reconstruct the fourteen role keys, CPython ABI and flags, jsonschema binding,
module and DLL maps, source-only resolver, application/DLL selection, and all
ambient denials. Attack missing, extra, duplicate, unclassified, host-filled,
bytecode, namespace-fallback, and mismatched-row cases.

### 5.4 BRM-IR-004

Reconstruct the 63-row effective matrix from base order. Require 43 retained
rows and twenty replacements, unique IDs, exact insertion positions, one
Boolean output state, one matching primary failure, and immutable first-fault
precedence. Inject cleanup, record, and retry failures after every class.

### 5.5 BRM-IR-005

Reconstruct the exact publication order and record field boundaries. Attack B
selection, result-based owner selection, B not quarantined, prepublication
overclaim, destination race, repeated/cross-volume publication, final record
before rehash, postpublication mutation, and failure-to-authority promotion.

## 6. Cross-file and schema tests

The reviewer must independently check:

- exact equality of the 31 semantic relations in map and schema;
- exact twelve resource values across v0.1 and v0.2 artifacts;
- exact external pin, binary field, runtime role, phase, and mutation
  inventories;
- strict `additionalProperties: false` at authority-bearing objects;
- required-property and unknown-property rejection at every new depth;
- lowercase digest enforcement;
- semantic uniqueness and total-coverage relations JSON Schema cannot express;
  and
- one clearly fake PUBLIC in-memory placeholder admission package against both
  schemas, without treating it as execution input.

## 7. Severity and verdict

- `BLOCKING`: permits denied content, unpinned executable input, or live,
  rehearsal, or S0 authority, or invalidates review integrity;
- `MAJOR`: leaves authority, binary, runtime, failure, publication, resource,
  or provenance behavior incomplete, contradictory, or multiply interpreted;
- `MINOR`: bounded exactness issue that cannot affect bytes, authority, or a
  primary conclusion.

Return exactly one:

- `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
  BLOCKING and zero MAJOR findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, input, independence, or F0 failure.

## 8. Evidence limits

The result is design evidence only. State explicitly that no source,
compiler, build, binary, runtime tree, native call, loaded image, platform
behavior, live decision, rehearsal, F0 input, provider/model, S0, or E0 result
was created or observed.

## 9. Exact authorized outputs

Write exactly:

1. `s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.2/public-assembly-build-runtime-materialization-design-v0.2-independent-review-v0.1.md`;
2. the same-basename `.sha256`.

Run canonical validation and final exact two-file, input hash, Git identity,
F0 aggregate, and `git diff --check` verification. Do not commit or push.

With a valid PASS, the exact next candidate gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.2 CONTROL INTEGRATION OPEN`
