# S0 v0.14 public assembly build and runtime materialization acceptance plan v0.2

- `status`: bounded design-revision acceptance candidate
- `implementation_status`: not implemented
- `build_status`: not executed
- `runtime_materialization_status`: not executed
- `scope`: closure of BRM-IR-001 through BRM-IR-005 only

## 1. Acceptance threshold

Fresh independent review must return zero BLOCKING and zero MAJOR findings.
Any MINOR requires explicit CONTROL disposition. A PASS permits only CONTROL
integration consideration followed by a separately opened implementation
candidate gate.

No test in this plan may install or run a compiler, create native source,
build or load a binary, materialize a runtime tree, call a native API, run a
platform probe, access F0 content, or run a provider, model, S0, or E0 task.

## 2. Integrity and composition

Before semantic review, independently authenticate:

1. exact Git identity and clean initial state;
2. the v0.1 package and its independent review;
3. the v0.2 package manifest before any v0.2 content;
4. every Markdown/sidecar with the canonical validator after SelfTest;
5. every JSON with strict UTF-8, no BOM or CR, final LF, no trailing
   whitespace, duplicate-key rejection, canonical sidecar, and exact hash;
6. the v0.1 and v0.2 schemas against Draft 2020-12 metaschema; and
7. every named predecessor manifest before any target read.

The reviewer must prove that v0.2 is a mandatory wrapper around an exact v0.1
base profile. A direct v0.1 profile, optional wrapper, partial composition,
candidate-selected base schema, or another base hash is a MAJOR failure.

F0 checking is aggregate-only at `32 / 11 / 10`, with no content or filename
read and no worktree, index, untracked, ignored, skip-worktree,
assume-unchanged, or parent-diff anomaly.

## 3. BRM-IR-001 closure tests

The closed v0.2 wrapper must require baseline commit, baseline tree, bounded
verification manifest, integration v0.1 design manifest, exact v0.2 package
manifest, and approving v0.2 review.

For each of the ten external pin classes, test missing, uppercase, malformed,
all-zero, predecessor, moving-version, candidate-selected, valid-shaped but
unauthenticated, and target-set mismatch variants. Each must stop before
candidate import or process creation with its exact `BR-AUTH/0`,
`BR-SOURCE/0`, or `BR-TOOLCHAIN/0` class.

The reviewer must explicitly test that:

- the canonical base-profile hash is an outer hash of the embedded profile,
  not a self-hash of the admission package;
- the review hash and v0.2 package hash are outer authorities;
- all eight manifest identities bind count, total bytes, and target-set hash;
- the six overlapping v0.1 and v0.2 closure fields are byte-identical; and
- the runtime-tree profile is distinct from the output runtime-package
  manifest.

## 4. BRM-IR-002 closure tests

Construct one valid-shaped, nonexecutable PUBLIC placeholder for each of the
two binary roles. It must remain fake design data and must never be loaded.

For every required field, remove it and add one unknown field. Mutate each
digest, count, role, machine, entry point, subsystem, image size, relocation,
resource, Windows manifest, load-config, import/export manifest, allowlist,
mitigation, and zero predicate. Every case must fail schema or the named
semantic relation.

Required hostile cases include:

- missing guard entry point or unexpected export;
- changed direct import assignment;
- added, removed, reordered, ordinal, bound, or delay import;
- nonzero CLR, CodeView, debug, PDB, TLS, certificate, writable-executable,
  dynamic-loader, FFI, shell/network/provider/plugin, host-path, or timestamp
  count;
- absent relocation table or changed resource/manifest identity;
- inspector PASS text without exact parsed predicates; and
- inspected bytes differing from built or materialized bytes.

No binary may be loaded during these tests.

## 5. BRM-IR-003 closure tests

The schema must require all fourteen runtime role keys. The semantic validator
must reject a missing, extra, duplicated, multiply assigned, or absent-path
role and any base runtime row not covered exactly once.

Test exact CPython ABI, ordered `-I/-S/-B`, jsonschema 4.26.0 and its manifest,
module-map and DLL-map uniqueness, source hashes, application selection, and
DLL search policy.

Each of these must reject independently:

- host Python or host DLL satisfies a missing row;
- user site, `site`, `PYTHONPATH`, current directory, PATH, registry, package
  installation, or ambient module discovery participates;
- bytecode is read or written;
- a namespace fallback or unlisted module is imported;
- a module/DLL mapping names a missing or different runtime row;
- dependency or jsonschema transitive closure is incomplete; or
- an unclassified runtime row exists.

## 6. BRM-IR-004 closure tests

Independently reconstruct the effective matrix using only the authenticated
base matrix and v0.2 algorithm. It must contain 63 unique rows:

- 43 retained enriched rows;
- 3 replacements for missing/partial/extra output;
- 8 before/after-output resource-bound replacements; and
- 9 retry rows preserving every possible prior primary class.

Every effective row must contain exactly one primary failure and one Boolean
`output_created_before_primary_failure`. The failure suffix must match the
Boolean. Reordering, duplicate ID, omitted replacement, retained removed row,
changed failure, changed Boolean, or changed insertion position rejects.

For overlap tests, inject cleanup, quarantine, record, and retry failure after
each primary class. The first class must remain unchanged and the later event
must be secondary. No retry may reuse an input, root, object, output, cache,
record, or candidate version.

## 7. BRM-IR-005 closure tests

The publication owner must be literal A before any build. B must never become
eligible for selection. After equality, B must be quarantined and verified
before any A publication action.

The exact positive order is:

1. runtime equality;
2. B quarantine;
3. prepublication record freeze/read-back;
4. destination-absent recheck;
5. one same-volume atomic A rename;
6. retained-parent reopen and final identity/file/hash verification; and
7. final diagnostic record freeze/read-back.

Reject every skipped, repeated, swapped, or fabricated phase. Specifically
reject a prepublication record that claims rename success or final identity,
a final record written before final rehash, a B publication, result-based
owner selection, destination replacement, cross-volume move, duplicate
publish, and postpublication mutation.

If a postpublication check or final-record operation fails, verify that the
candidate is quarantined and that no live, rehearsal, or S0 authority is
granted. The review must not treat actual filesystem behavior as tested; this
is a design-level state-machine and counterexample review only.

## 8. Cross-file exactness

Require all of the following exact equalities:

- the 31 semantic relations are byte-for-byte identical in the interface map
  and schema;
- all twelve resource values match v0.1 map, v0.1 schema, v0.2 map, and v0.2
  schema;
- the external pin class order is identical across design, map, and review
  brief;
- the binary field inventory matches schema required fields;
- the runtime role key order matches map and schema;
- the publication phase order matches design, map, and schema; and
- the effective mutation count and replacement arithmetic match every file.

Use one valid-shaped synthetic admission package only for schema and semantic
construction tests. All hashes must be declared fake. It cannot be accepted
as an actual profile or execution input.

## 9. Nonregression and claim boundary

Confirm that v0.2 changes only the five reviewed defects. It must retain:

- two clean builds and all-output equality;
- exact source and offline toolchain closure;
- unsigned binary policy;
- static inspection without loading;
- exact runtime paths and file set;
- preloader-only later native root creation;
- later real-Windows handle, decoy, loaded-image, and atomicity probes;
- diagnostic-only records and candidate root; and
- closed F0, provider/model, live, rehearsal, S0, E0, central-system, and
  Project Brain boundaries.

## 10. Verdict and next gate

Return exactly one:

- `PASS-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY` with zero
  BLOCKING and zero MAJOR findings;
- `REVISE-AND-REVIEW` with any finding; or
- `INVALID-REVIEW` for integrity, input, role, independence, or F0 failure.

With a valid PASS, CONTROL may consider design integration. No review result
opens implementation, build, materialization, native execution, platform
probe, live assembly, official rehearsal, F0, S0, E0, commit, push, PR, merge,
release, signing, or deployment.
