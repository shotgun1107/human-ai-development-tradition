# S0 v0.14 public build/runtime materialization implementation v0.1 independent review

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.1 INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent PUBLIC implementation reviewer
- `reviewed_commit`: `71b6a85ebb7ba26baed178621b2ace4b27c55988`
- `reviewed_tree`: `8c159786a363d2d01d3f3df3108a6ba596973a21`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: 1 BLOCKING / 4 MAJOR / 0 MINOR
- `F0_content_access`: none

## 1. Outcome

The candidate's single intended entry point authenticates the five public
design closures, reconstructs the corrected v0.5 relation and policy
identities, and returns `BLOCKED-MISSING-EXTERNAL-PIN` without performing a
build, materialization, native call, network/provider action, rehearsal, S0,
or E0 operation. That bounded path is useful construction evidence.

The published package is not yet a trustworthy API-level implementation of
that boundary. Exported dataclasses and helpers can manufacture a false
execution-authority bit, detach diagnostic fields from their authenticated raw
record, reuse an authentication marker over mutated pinned bytes, mutate the
normative policy without changing its reported digest, admit invalid runtime
plans, and import an ambient schema dependency over caller-selected schemas.
The candidate therefore has one false-authority boundary bypass and several
material contract mismatches. It is not eligible for the next CONTROL
integration gate.

## 2. Input and repository authentication

Before importing candidate code, I authenticated all of the following:

- origin exactly
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- branch exactly
  `codex/s0-build-runtime-materialization-implementation-v01-review`;
- HEAD and remote candidate ref exactly
  `71b6a85ebb7ba26baed178621b2ace4b27c55988`;
- tree exactly `8c159786a363d2d01d3f3df3108a6ba596973a21`;
- sole parent exactly `5766850afd380b63262ece118940959bd5c68986`;
  and
- initial worktree/index/untracked entry count zero.

The implementation and verification manifests matched their external pins
`43a6670acf7165678852b664b9d4752611d7433b43473fe5376c5e1a64bafd70`
and
`ed71337cc50acfd56f8b2f3b6255aa97d176b72568af7af70606e9c234b79f94`.
Their exact target counts were 10 and 6. All paths were ordinal-unique and
case-fold-unique, every target was present, and every target hash matched.

The v0.1 through v0.5 design manifests matched their five external pins and
their exact 6 / 7 / 9 / 9 / 7 target closures. The approving review and
CONTROL decision Markdown hashes matched
`5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`
and
`d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`.

The canonical validator SelfTest passed. The candidate README, candidate
report, approving design review, and CONTROL decision Markdown/sidecar pairs
all passed independently labeled UTF-8, BOM, final-LF, trailing-whitespace,
sidecar-format, and sidecar-hash checks. The candidate commit's exact change
set was the 17-file union of both manifests and their targets, with zero
unexpected and zero missing paths.

Aggregate-only F0 inventory checks returned exactly 32 / 11 / 10. No F0
filename or content was enumerated, opened, searched, quoted, summarized, or
used.

## 3. Positive verification evidence

The authenticated-snapshot verifier was run with implementation pin
`43a6670acf7165678852b664b9d4752611d7433b43473fe5376c5e1a64bafd70`.
Its isolated `python -I -B` child passed 13 of 13 focused tests. Candidate code
was imported only from the authenticated temporary snapshot. The original
pre/post input swap sentinel passed. Static inspection found no candidate
filesystem, process, native, network, provider, model, build, materialization,
rehearsal, S0, or E0 call surface.

An independent PowerShell reconstruction, not the candidate serializer,
confirmed:

- the v0.4 map/schema relation authorities match, the required old relation is
  unique at zero-based index 15, and the patched 68-relation preimage is 6,805
  bytes with SHA-256
  `5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`;
- the sole normative 20-field policy JCS-plus-LF preimage is 896 bytes with
  SHA-256
  `3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`;
- effective matrix counts are 63 / 97 / 111 / 115, all 115 IDs are unique,
  and every primary-failure suffix matches its output-created bit; and
- all six retained resource-limit authorities agree on the same 12 positive
  integer ceilings.

The intended `prepare_public_build_runtime_candidate` path has no
caller-selected external-pin parameter. On the exact authenticated closure it
reconstructs the v0.5 relation/policy/matrix facts and terminates at
`BLOCKED-MISSING-EXTERNAL-PIN`. Direct v0.4 fallback, alternate manifest
targets, missing/extra targets, and schema shape alone do not make that entry
point authorize execution.

## 4. Findings

### BRM-I01-IR-001 — BLOCKING — exported objects can manufacture false authority and detach authority from bytes

`RuntimeMaterializationPlan` is exported and has no invariant check. Starting
from the function's valid nonexecuting plan, ordinary
`dataclasses.replace(plan, execution_authorized=True)` succeeds. This creates
an object of the package's declared plan type carrying a false positive
authority bit.

`BuildRuntimeDiagnostic` verifies only that `raw` hashes to `sha256` and that
five authority booleans remain false. It does not prove that
`external_pin_status`, relation/policy digests, mutation count, primary
failure, or trace are the values encoded in `raw`. A hostile in-memory test
changed the status to `PRESENT`, the mutation count to `-7`, and the relation
digest to all zeroes while retaining the exact original raw bytes and hash;
construction succeeded.

`AuthenticatedDesign.marker` is also reusable. After one legitimate
authentication, a hostile test replaced the bytes of the pinned v0.5 profile
schema with `{}` plus LF, preserved the public marker through
`dataclasses.replace`, and `validate_effective_design` still returned the
accepted relation and policy identities. The validator neither reauthenticates
the supplied object nor consumes that required pinned schema.

These are not claims about hostile OS isolation. They are same-process API
facts. Python object privacy is not an information-security boundary, so the
package must either make these objects non-authoritative diagnostics and say
so exactly, or verify a complete canonical byte record at every authority
transition. As shipped, the public API can express false authority and false
byte binding. This meets the review rubric's BLOCKING false-authority/boundary
bypass condition.

### BRM-I01-IR-002 — MAJOR — the authenticated normative policy result is only shallowly immutable

`validate_effective_design` wraps the policy's outer dict in
`MappingProxyType`, but the 20-field policy contains the mutable
`source_handle_required_access` list. Appending a new value succeeds while
`publication_policy_sha256` remains the authenticated v0.5 digest. The
returned object therefore no longer uniquely represents the 896-byte policy
it claims to identify.

Deep-freeze every nested list/object, or return only canonical immutable bytes
plus a recomputed digest. Add a hostile test that attempts nested mutation and
requires rejection or isolation.

### BRM-I01-IR-003 — MAJOR — runtime planning does not enforce the closed path, type, and resource contract

Independent in-memory hostile tests established all of these accepted cases:

1. a duck-typed object that is not a `RuntimeRow` was accepted as a runtime
   row;
2. simultaneous file rows `runtime/a` and `runtime/a/b` were accepted even
   though one virtual path must be both a file and a directory;
3. the caller raised `maximum_bytes` and obtained a plan larger than the
   retained 2,147,483,648-byte runtime-tree ceiling; and
4. `S0-LAB/CONTROL/F0-SEALED/...`, a Windows case alias of a denied repository
   prefix, was accepted because denied-prefix matching is case-sensitive.

The package also exports directly constructible directory and plan records,
while its DLL helper derives only directories and not the design-required
bijection of DLL names, paths, hashes, parents, identity keys, and directory
indices. It has no physical-identity representation, which is acceptable only
as a later-runtime block, not as a completed runtime-plan validator.

Use exact row types, fixed authenticated resource ceilings, Windows-identity
comparison for denied classes, file/directory prefix-collision rejection, and
one design-bound DLL resolution plan. Caller-selected larger bounds must not
be authority.

### BRM-I01-IR-004 — MAJOR — the schema dependency and schema authority block is descriptive, not enforced

The main candidate path avoids `schema.py`, but that shipped module imports
ambient `jsonschema` and `referencing` at module import and exposes
`validate_profile(profile_raw, effective_schema_raw, schema_bytes)` over
caller-selected bytes. It does not bind the effective schema or registry to
`AuthenticatedDesign`, the authenticated manifests, or an external dependency
pin. It even converts the supplied mapping to a plain dict before the helper's
exact-dict check.

Consequently the verifier's
`JSONSCHEMA_DEPENDENCY_STATUS=BLOCKED-MISSING-EXTERNAL-PIN` line is true only
for the chosen main import graph, not an enforced property of the shipped
implementation surface. A caller can import the adapter when a host copy is
present and obtain schema-only success from caller-selected schemas. Keep the
adapter unavailable until the dependency closure is authenticated, or make
it require an authenticated design/dependency capability and reject every
alternate schema registry.

### BRM-I01-IR-005 — MAJOR — record evidence does not reconstruct the retained records and labels unobserved I/O identities

`construct_in_memory_record` accepts any exact dict, serializes it, and copies
one in-memory digest into `body_canonical_sha256`,
`body_closed_file_sha256`, and `body_readback_sha256`. No file was closed or
read back, and neither retained v0.4 record schema, body field order,
prepublication/final phase, policy binding, target-set binding, nor
transaction relation is checked.

The report discloses that the helper is in-memory, but fields named
closed-file and readback remain observation claims in the controlling design.
An unperformed observation must be absent or explicitly unavailable, not
copied from the canonical hash. The candidate may honestly remain blocked
until materialization and schema dependencies exist; it may not represent
those missing observations as `RecordEvidence`.

## 5. External-pin and boundary assessment

The aggregate `BLOCKED-MISSING-EXTERNAL-PIN` outcome of the intended entry
point is honest: this gate did not supply a complete authenticated native
source, materializer/inspector source, toolchain, compiler/linker/SDK/CRT,
CPython, dependency, Windows-platform, build-profile, and runtime-tree
closure. The already authenticated approving review does not make that
overall closure complete. Refusing caller-selected pins is correct.

That honest terminal state does not cure the exported-object, mutable-policy,
planning, schema, or record defects above. The candidate currently
reconstructs the fixed relation, policy digest, matrix, and resource summary;
it does not uniquely reconstruct an authenticated path/DLL/runtime plan, the
retained record packages, or one byte-bound claim-boundary record. Those
surfaces must stay explicitly unavailable until they can be built from exact
authenticated inputs.

## 6. Evidence boundary

This review used only authenticated PUBLIC inputs from the exact allowlist and
clearly fake in-memory hostile values. No compiler, toolchain, native source,
binary, filesystem materialization, runtime tree, native API, real candidate
process, Windows platform probe, network, provider/model operation, rehearsal,
S0, or E0 execution was performed or observed. The shipped verifier's one
isolated Python unittest child and the reviewer's in-memory Python tests were
PUBLIC verification orchestration only. No F0 input was accessed.

Nothing in this review establishes the central system, Project Brain
integration, operational safety, economic value, production readiness, or
model-to-model transfer.

## 7. Verdict and exact next gate candidate

Verdict: `REVISE-AND-REVIEW`.

The exact next gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.2 REVISION OPEN`

This review does not open that gate and does not authorize commit, push, PR,
main integration, build execution, materialization, platform testing,
rehearsal, S0, or E0 work.
