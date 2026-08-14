# S0 v0.14 public assembly build and runtime materialization acceptance plan v0.1

- `status`: design-level acceptance candidate
- `implementation_status`: not implemented
- `build_status`: not executed
- `runtime_materialization_status`: not executed
- `scope`: source, toolchain, build, binary, and runtime-tree design only

## 1. Acceptance threshold

Fresh independent design review must return zero BLOCKING and zero MAJOR
findings. Any MINOR requires explicit CONTROL disposition. Passing this plan
permits only consideration of a separate implementation gate.

No design verdict authorizes tool installation, compiler execution, native
source implementation, runtime-tree creation, native API use, platform probe,
or rehearsal.

## 2. Authentication before substance

The reviewer must fail with `INVALID-REVIEW` before semantic judgment if:

- repository origin, exact branch, commit, tree, sole parent, or clean state
  differs from the CONTROL-supplied values;
- the package manifest is not exact, ASCII-sorted, unique, canonical, and
  hash-correct;
- any Markdown or sidecar fails the canonical validator after SelfTest;
- any JSON has a BOM, invalid UTF-8, CR, missing final LF, trailing whitespace,
  duplicate key, noncanonical sidecar, or parse failure;
- the profile schema fails Draft 2020-12 metaschema validation;
- any predecessor manifest or target differs from its supplied pin;
- the review input list is incomplete or exceeded; or
- F0 content is accessed.

F0 verification is aggregate-only: `32 / 11 / 10`, with zero content read and
zero worktree, index, untracked, ignored, skip-worktree, assume-unchanged, or
parent-diff anomaly.

## 3. Required independent reconstruction

Without treating author prose as an answer key, the reviewer must establish:

1. the current assembly/RPNP integration remains bounded offline Python and
   cannot create native or live authority;
2. effective RPNP v0.4 requires exact source/build/tool/import/binary/loaded
   image and runtime-package closure;
3. the future native preloader and guard source do not yet exist and are
   mandatory external implementation inputs;
4. Python runtime and dependency bytes are a separate exact closure, not the
   current host interpreter;
5. a tool name or version label cannot substitute for an exact offline bundle;
6. the build has exactly two clean, nonsharing roots and requires complete
   output byte equality;
7. static binary inspection precedes runtime publication;
8. runtime materialization has one exact file set and one atomic publication;
9. build records and runtime files remain diagnostic-only; and
10. platform behavior, live acceptance, rehearsal, and S0 remain later gates.

Any contradiction is at least MAJOR. Any path that can grant live or rehearsal
authority from a build record is BLOCKING.

## 4. External-pin closure review

The reviewer must confirm that all ten external pin classes in the design are
mandatory before implementation. Construct one missing, uppercase, malformed,
placeholder, predecessor, moving-version, candidate-selected, and valid-shaped
but unauthenticated digest case for every class.

Every nonexact case must stop before candidate import or process creation with
`BR-AUTH/0`, `BR-SOURCE/0`, or `BR-TOOLCHAIN/0` as applicable. No callback,
default path, discovery result, package install, local newest version, or
previous validation object may fill the missing value.

## 5. Source and toolchain closure matrix

Design acceptance requires all of the following.

| Proposition | Required rule | Reject if |
|---|---|---|
| Retained Python source | Exact manifested bytes copied without transformation | Generated, normalized, byte-compiled, or unmanifested source is admitted |
| Native source | New exact public manifest under a later gate | A binary or design statement substitutes for source |
| Offline RPNP code | Remains offline plan/validator evidence | It is promoted into a live preloader or guard |
| Tool selection | Exact manifest virtual path and hash | PATH, registry, installer, environment, or filename selects a tool |
| Tool dependencies | Every executable/DLL/header/library/response file listed | A host SDK or dependency is discovered implicitly |
| Process environment | Closed map from profile only | User profile, inherited temp, locale, PATH, extension, plugin, cache, or telemetry leaks in |
| Network/package manager | Absent | Any download, update, restore, pip, NuGet, or provider call is reachable |

The review must not select a real compiler version. It judges whether a later
externally pinned choice has one fail-closed interpretation.

## 6. Build-profile schema review

The supplied schema must:

- have strict `additionalProperties: false` at every authority-bearing object;
- require all current authority pins and all six external closure manifests;
- require exact tool identities, commands, source date, virtual source root,
  resource limits, two-build policy, two native binary profiles, runtime rows,
  and all fourteen semantic relations plus the exact semantic-validator identity;
- reject a missing property at every required depth;
- reject an unknown property at every closed depth;
- reject uppercase or wrong-length digests;
- reject duplicate runtime paths or command IDs through the semantic validator
  where JSON Schema cannot express uniqueness by subfield;
- reject a command whose `tool_id` is missing, duplicated, role-incompatible,
  or not byte-identical to its authenticated toolchain-manifest row;
- reject a profile with `build_execution_authorized_by_profile=true`; and
- keep `candidate_only=true` even after a complete profile is constructed.

One valid-shaped PUBLIC placeholder instance may be used for schema
construction tests only. Its hashes must be clearly fake and it must never be
used as build input or reported as an admitted profile.

## 7. Command-plan review

For each future command, independently trace tool, argv, working directory,
environment, stdin, outputs, timeout, capture limit, and exit code. Required
negative cases include:

- shell invocation or a command string in place of argv;
- relative or PATH-selected tool;
- unlisted environment key;
- response file not present as authenticated bytes;
- compiler plugin, extension, cache, telemetry, incremental, or package-manager
  route;
- input not named by an authenticated source/toolchain manifest;
- output not declared before execution;
- output written outside the current clean build root;
- process count above one;
- timeout or output bound exceeded; and
- success exit with a missing or extra output.

Each must map to one first failure class. A generic catch-all that can obscure
whether bytes were produced is MAJOR.

## 8. Reproducibility review

The reviewer must reconstruct the exact A/B transaction and reject:

- one build only;
- shared root, object, cache, generated file, process, environment object, or
  temporary path;
- different command order or source snapshot;
- matching manifests with one mismatched file;
- matching binaries with a mismatched runtime data file;
- normalized or patched output after comparison;
- choosing one of two unequal outputs;
- comparing only hashes without independently re-reading exact bytes;
- missing or extra output in either root; and
- a retry that reuses either failed root.

The only positive relation is identical path sets, lengths, bytes, hashes,
static inspection, runtime manifests, and runtime files for A and B.

## 9. PE and import review

Static inspection must be from authenticated bytes and must not load the
target. The reviewer must verify that the design requires exact values for all
profile fields rather than trusting a tool's PASS string.

Mandatory negative cases include:

- non-AMD64 or non-PE32+ image;
- wrong entry point, subsystem, section, image size, resource, or manifest;
- added, removed, reordered, ordinal-substituted, delay, or bound import;
- unreviewed export or missing guard initialization export;
- `LoadLibrary*`, `GetProcAddress`, generic FFI, network, shell, provider, or
  plugin path;
- certificate table, TLS callback, CLR header, PDB/CodeView/debug directory,
  host path, or writable-executable section;
- missing ASLR, high-entropy VA, NX, or CFG policy;
- built binary differing from the materialized runtime row; and
- loaded-image equality treated as proven before the later platform probe.

The unsigned policy is exact: certificate-table size zero. No signing key or
service may appear in this design or its implementation review inputs.

## 10. Runtime-tree review

The reviewer must independently model Windows path normalization and reject:

- absolute, drive, UNC, backslash, colon, NUL, empty segment, dot segment,
  trailing dot/space, reserved-device, noncanonical, or case-fold-colliding
  virtual path;
- file/directory type conflict;
- symlink, junction, mount point, reparse point, hard link, ADS, sparse alias,
  or other unexpected object type;
- missing, extra, duplicate, reordered, or hash-mismatched row;
- `.pyc`, PDB, log, test, toolchain, source, key, cache, temp, user, F0, or
  unclassified file;
- write without exact-length read-back;
- identity change between write and rehash;
- destination already present;
- cross-volume or non-atomic publication;
- partial or duplicate publication;
- post-publication mutation; and
- cleanup that upgrades quarantined residue.

The A and B materializers must independently produce identical final manifest
bytes and identical file bytes. Publication records alone are insufficient.

## 11. Runtime import and authority review

The runtime must include exact rows for the selected verifier application,
CPython DLL and standard library, native guard, dependency closure, bootstrap,
assembly and component source, profiles, manifests, and fixed public inputs.

Reject if:

- current host Python or site packages satisfy a missing row;
- PATH, PYTHONPATH, user site, registry, current-directory fallback, or package
  installation participates;
- bytecode is loaded or written;
- a module outside the authenticated source-only map imports;
- jsonschema's exact distribution or transitive closure is missing;
- a loaded DLL differs from its final runtime row;
- the known-five guard is upgraded into process-wide absence evidence; or
- build/package success is treated as a Windows platform probe.

## 12. Failure and record review

Every mutation in the package matrix must have one expected first failure
class and a before/after-output bit. The reviewer must trace overlapping
failures and confirm that the earlier primary class survives cleanup and
record-writing failures.

Build, binary, and materialization records must be canonical, byte-bound, and
diagnostic-only. Reject any field or API that can recreate a private witness,
admission, live decision, rehearsal PASS, provider authority, or S0 state.

## 13. Resource-bound review

Independently confirm all twelve numeric bounds in the interface map and
schema agree. Mutate each bound above and below the frozen value. A future
implementation may consume less but may not expand a bound without a new
design revision and review.

The resource design is a safety ceiling, not evidence that the build will fit,
finish, or perform well on any current PC.

## 14. Nonregression and closed gates

The reviewer must confirm this design does not weaken:

- assembly v0.5 diagnostic versus live PASS separation;
- RPNP v0.4 source/build/import and known-five responsibility allocation;
- integration v0.2 preloader-only root creation and exact nested state order;
- bounded integration's offline-only flags and exact public closures;
- later real-Windows decoy, handle, root, loaded-image, and atomicity probes;
- F0 and hidden-oracle boundaries; or
- S0/E0, central-system, Project Brain, production, safety, and economic
  nonclaims.

## 15. Verdict vocabulary and next gate

Return exactly one:

- `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
  BLOCKING and zero MAJOR findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, input, role, or F0 boundary failure.

With a valid PASS, CONTROL may consider a design integration gate. Neither the
review nor integration opens implementation, build execution, materialization,
platform probing, live assembly, official rehearsal, F0, S0, E0, commit,
push, PR, main merge, signing, deployment, or release.
