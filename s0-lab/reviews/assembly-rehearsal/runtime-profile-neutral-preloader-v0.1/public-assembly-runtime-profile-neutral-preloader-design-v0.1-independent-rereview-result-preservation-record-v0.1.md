# Public assembly runtime profile and neutral preloader design v0.1 independent rereview result preservation record v0.1

- `record_kind`: CONTROL-authored normalized preservation of the fresh independent rereviewer result
- `review_verdict`: `REVISE-AND-REREVIEW`
- `review_scope`: public design v0.1 only
- `reviewer_method`: fresh, read-only, exact-path allowlist, no prior conversation or earlier reviewer output
- `base_commit`: `da4ad3af483652bd755deff9d024a9833c177d39`
- `base_tree`: `e5ad06934a9864b4c5665852e0097f3885d2d277`
- `base_parent`: `41e0b684a7cca387be6d264c4a5b63de2561fd7c`
- `design_package_manifest_sha256`: `13b69bfd8614ea57e49d317902e9563bd8a47eaa13a06be22065f81177b29cad`
- `provenance_limit`: this CONTROL preservation record is not a reviewer signature and is not an approving review artifact

## 1. Authentication result

The fresh independent rereviewer authenticated the exact commit, tree, parent,
all admitted Git blobs, 23 same-basename sidecars, four package manifests, 17
Markdown artifacts through the canonical validator, six JSON documents with
duplicate-key rejection, both new Draft 2020-12 schemas, and all five supplied
external pins.

The predecessor package manifests had exact logical row counts `5/5/5`; the
v0.1 runtime-profile and neutral-preloader package manifest had six exact rows.
All were sorted, unique, free of self and sidecar rows, and hash-correct.

No role-boundary failure occurred in the valid rereview. No F0 content,
implementation source, implementation test, hidden oracle, network, provider,
model, or prior-review result was used.

## 2. Verdict and finding counts

The exact verdict was:

`REVISE-AND-REREVIEW`

Finding counts were:

- `BLOCKING`: 0
- `MAJOR`: 3
- `MINOR`: 0

## 3. RPNP-RR-001 — bidirectional anonymous-pipe contradiction

The v0.1 design used one Windows anonymous liveness-pipe pair for both the
verifier-to-preloader commit request and the preloader-to-verifier reply.
Windows anonymous pipes are unidirectional. Supplying both actors with both
ends would also destroy exact direction and EOF ownership and allow self-read
or ordering races.

The smallest sufficient correction is two unidirectional channels:

1. verifier to preloader commit request; and
2. preloader to verifier commit reply.

The replacement must freeze exact retained and inherited ends, handle-list
membership, closure order, message order, EOF rules, and admission bindings.

This is a `MAJOR` frozen-interface and acceptance-criterion change. It does not
require a launch-envelope wire-schema change or threat-model expansion.

## 4. RPNP-RR-002 — nonexistent output-root identity

The v0.1 design created `RuntimeAdmission` before verifier-package import and
before the output leaf existed, while requiring it to bind an output-root file
object identity. At that time only the existing output-parent identity and the
canonical absent leaf can be authenticated. A not-yet-created directory has no
volume and file-index identity.

The smallest sufficient correction is a staged private admission state:

1. initially bind the exact output-parent identity and canonical absent leaf;
2. after exclusive root creation, authenticate and bind the created root object
   identity exactly once; and
3. require that root identity to equal the observer/witness root and pass the
   pre-commit recheck.

This is a `MAJOR` frozen-interface and acceptance-criterion change and a
clarification of the existing TOCTOU threat model. The launch-envelope wire
schema need not change.

## 5. RPNP-RR-003 — undefined process-count domain

The v0.1 runtime-profile schema fixed `maximum_processes` to one without
defining its counting domain. The architecture requires one preloader outside
the job and, during candidate execution, both verifier and candidate inside the
job. Applying one as the job active-process maximum prevents candidate launch;
interpreting it only as candidate count fails to express the exact job and
descendant boundary.

The smallest sufficient correction is separate exact limits and phases:

- exactly one preloader outside the job;
- exactly one verifier inside the job before candidate launch;
- exactly one candidate created for the run;
- at most two active job members during candidate execution;
- zero additional descendants and zero breakaway processes; and
- exactly one verifier remaining after candidate exit until terminal cleanup.

This is a `MAJOR` runtime-profile-schema, frozen-interface, process-threat-model,
and acceptance-criterion change.

## 6. Preserved positive conclusions

The rereviewer found the following v0.1 design areas adequate at design level:

- bootstrap circularity and the external Windows-kernel/CONTROL trust root;
- locked-handle, suspended-child-image equality before preloader resume;
- CPython, standard-library, extension, `jsonschema`, metadata, private-DLL,
  system-DLL, API-set, KnownDLL, module-origin, and PE-edge closure;
- native-preloader neutrality and source-to-binary review requirements;
- atomic publication-witness plus runtime-admission consumption;
- unchanged receipt-v2 wire form and rejection of status/output/stdout/stderr as
  PASS authority;
- failure routing and separation of mutation evidence from real-platform probe;
  and
- design-only claim limits and all closed F0, oracle, provider/model, rehearsal,
  S0/E0, central-system, Project Brain, safety, value, and transfer boundaries.

Those positive conclusions do not override the three `MAJOR` findings.

## 7. Required disposition

The v0.1 package does not open implementation consideration. CONTROL must issue
a corrected public design package, preserve the three corrections without
weakening predecessor invariants, and obtain a fresh independent rereview.

No implementation, file operation, compilation, dependency installation,
runtime-profile materialization, platform probe, official rehearsal, real
`MoveFileExW`, F0-content access, hidden-oracle access, provider/model/network
use, commit, push, PR, release, or main integration occurred in the independent
rereview.
