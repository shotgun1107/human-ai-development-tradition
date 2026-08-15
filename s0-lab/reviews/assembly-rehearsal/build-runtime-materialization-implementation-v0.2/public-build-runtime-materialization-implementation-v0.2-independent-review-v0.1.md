# S0 v0.14 public build/runtime materialization implementation v0.2 independent review

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.2 INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent PUBLIC implementation reviewer
- `reviewed_commit`: `be65843cb643346d044e692d367890b171d192ab`
- `reviewed_tree`: `e8781683d46d2662d6dfda05a25b72bc0a0ac33a`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: 0 BLOCKING / 3 MAJOR / 0 MINOR
- `F0_content_access`: none

## 1. Outcome

The v0.2 candidate materially improves the bounded nonexecuting layer. It
reauthenticates the complete design closure at semantic transitions, derives
diagnostic properties from one canonical byte record, recursively freezes the
internally produced policy and matrix, removes ambient schema imports, reports
file close/readback as unavailable, and keeps the intended entry point at
`BLOCKED-MISSING-EXTERNAL-PIN`. The authenticated-snapshot verifier passed all
18 shipped tests.

The revision does not fully close the prior authority and runtime-planning
findings. Public constructors can still produce an `EffectiveDesign` carrying
invented matrix and resource authorities, and caller-owned mapping backings can
mutate an already accepted plan. The runtime prefix test misses one valid
case-preserved ordering of a Windows-case-folded file/directory collision. The
runtime row and DLL helpers also remain generic caller-selected structures,
not the exact design-bound runtime manifest and DLL map: required provenance
fields and several closed field grammars are absent, and mutually inconsistent
DLL orders are both admitted.

These defects do not set an execution-authority bit and no execution path was
opened, so they are MAJOR rather than BLOCKING. They prevent a zero-finding
next-gate verdict.

## 2. Input and repository authentication

Before substantive review, the following matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- remote candidate ref and reviewed commit:
  `be65843cb643346d044e692d367890b171d192ab`;
- reviewed tree:
  `e8781683d46d2662d6dfda05a25b72bc0a0ac33a`;
- sole parent:
  `f188a7932d2472ae0700e1f3a70a2184cbb93860`;
- isolated review branch:
  `codex/s0-build-runtime-materialization-implementation-v02-review`; and
- initial worktree/index/untracked entry count: zero.

The implementation and verification manifests matched their external pins:

- implementation:
  `13d5d3dea763fa3bfaa095e1d3f235734323acacf153dab788b7cb6baac73128`;
- verification:
  `f08c35d925cbb50b5e57db7c3f0c79b7df1ee10136fbade73915dce8c4e646fe`.

Their exact target counts were 10 and 6. Together with the verification
manifest itself they described exactly 17 case-fold-unique files under the
candidate root. Every target existed and every target hash matched. The exact
candidate commit change set was those same 17 files, with zero extra and zero
missing paths.

The five design manifests matched external pins
`bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c`,
`47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`,
`1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277`,
`7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884`,
and
`ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c`.
Their exact target counts were 6 / 7 / 9 / 9 / 7, with zero missing target,
hash mismatch, or case alias.

The v0.1 implementation review, approving v0.5 design review, and CONTROL
decision matched their pins
`fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b`,
`5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`,
and
`d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`.
The canonical validator SelfTest and the admitted Markdown/sidecar checks
passed.

Aggregate-only F0 checks returned exactly 32 / 11 / 10 tracked entries. Parent,
worktree, and index quiet diffs were zero, as were untracked, ignored,
skip-worktree, and assume-unchanged anomaly counts. No F0 filename or content
was enumerated, opened, searched, quoted, summarized, or used.

## 3. Verification evidence

The candidate's externally pinned authenticated-snapshot verifier ran an
isolated `python -I -B` unittest child. All 18 shipped tests passed with no
failure, error, or skip. Design-manifest authentication, auxiliary pins,
original-input swap sentinel, and the stated no-execution terminal fields all
passed.

Independent fake PUBLIC in-memory attacks then retested every prior finding:

- reused markers over mutated pinned bytes and direct construction with the
  module-private marker both rejected during full reauthentication;
- attempts to detach diagnostic fields from canonical bytes rejected;
- the internally produced policy rejected nested mutation;
- oversized caller resource bounds, duck runtime rows, ordinary raw-order
  prefix collisions, and denied-prefix case aliases with descendants rejected;
- caller-selected schema validation remained unconditionally blocked; and
- false close/readback observations rejected while the honest status remained
  `UNAVAILABLE-NOT-MATERIALIZED`.

The independent attacks also found the three MAJOR defects below. These tests
did not compile, build, materialize, open a native API, access a network or
provider, run a rehearsal, or execute S0/E0.

## 4. Prior-finding disposition

| Prior finding | Disposition | Evidence |
|---|---|---|
| `BRM-I01-IR-001` | PARTIALLY CLOSED | False execution-bit replacement, diagnostic divergence, and mutated authenticated bytes reject. Exported semantic/plan objects remain forgeable or post-construction mutable under `BRM-I02-IR-001`. |
| `BRM-I01-IR-002` | CLOSED | The internally returned policy and matrix values are recursively immutable and retain their authenticated identities. |
| `BRM-I01-IR-003` | NOT CLOSED | Fixed bounds and several exact-type/path checks work, but case-folded prefix order and the design-bound row/DLL contract remain open under `BRM-I02-IR-002` and `BRM-I02-IR-003`. |
| `BRM-I01-IR-004` | CLOSED | The shipped schema adapter imports no ambient schema implementation and has no success path without a later authenticated dependency closure. |
| `BRM-I01-IR-005` | CLOSED | The record helper makes no close/readback hash claim and rejects any substituted observation. |

## 5. Findings

### BRM-I02-IR-001 - MAJOR - exported semantic and plan objects do not preserve their validated identities

`EffectiveDesign.__post_init__` authenticates the relation and policy
identities, but it checks the matrix only for 115 unique IDs and failure-suffix
shape, and checks resources only for twelve positive integer entries. Starting
from the legitimate authenticated result, independent tests replaced all 115
rows with invented `FAKE-*` rows and separately replaced all twelve resource
names and values with invented entries. Both constructions succeeded as the
package's exported `EffectiveDesign` type.

The same issue exists as post-construction mutation for accepted mapping
proxies. A direct `RuntimeMaterializationPlan` built with a caller-owned dict
behind `MappingProxyType` passed validation; clearing that backing dict after
construction changed `path_index` from one entry to zero while `rows` and the
accepted plan object remained unchanged. `MappingProxyType` prevents writes
through the proxy but does not freeze a caller-owned backing mapping.

The intended entry point does not consume a caller-supplied `EffectiveDesign`
and `execution_authorized` remains the constant false property. This is not
the v0.1 false-execution-bit BLOCKING defect. It is still a material API-level
identity defect: exported objects named as authenticated effective design and
validated materialization plans can diverge from the bytes or rows they claim
to represent.

The successor must either make these structures explicitly nonauthoritative
diagnostics, remove direct public construction from authority transitions, or
copy and reauthenticate every complete closed value at each use. Matrix rows
and resources must be bound to the authenticated design closure, not merely to
cardinality and shape.

### BRM-I02-IR-002 - MAJOR - Windows-case-folded prefix collision checking depends on raw-case sort order

`plan_runtime_tree` first requires raw unsigned-ASCII path order, then creates
lowercase Windows identity keys, but it checks descendants only at later tuple
indices. This assumes raw-case ordering and lowercase ordering are identical.
They are not.

The exact ordered rows `Runtime/A/b` and `runtime/a` pass the raw ASCII-order
test. Their Windows keys are `runtime/a/b` followed by `runtime/a`. The first
key does not see a later descendant and the second key has no later entry, so
the function returns an accepted plan in which one Windows path is a file and
the other requires that same path to be a directory.

The denied-class comparison has a related edge: the exact case alias
`S0-LAB/CONTROL/F0-SEALED` is accepted because the configured denied value ends
with `/` and only descendant prefixes are tested. The same value with a child
does reject. A materialization path contract must reject both the exact denied
root identity and all descendants.

Prefix testing must operate on a separately sorted Windows identity-key set,
or compare every pair independent of input order. Denied identities must use
an exact-or-descendant predicate after case folding.

### BRM-I02-IR-003 - MAJOR - runtime and DLL helpers remain caller-selected rather than design-bound

The retained profile's exact runtime row contains eight fields, including
`provenance_manifest_sha256` and `provenance_path`; requires byte length at
least one; closes classification to the published enum; and constrains the
semantic-role and load/read-phase grammars. `RuntimeRow` has no provenance
fields, accepts zero bytes, and accepts arbitrary nonempty role,
classification, and phase strings. One such row passed `plan_runtime_tree`.
It therefore cannot be a lossless representation of the authenticated runtime
manifest row.

The DLL helper likewise accepts caller-supplied `DllRow` values without an
authenticated profile or map binding. The design requires exactly one binding
per authenticated `dll_map` row in exact map order. Independent tests supplied
the same two DLL rows in A/B and B/A order; both plans succeeded. A DLL path
under a case alias of a denied repository class also succeeded. Because no
authenticated source inventory is an input, the helper cannot distinguish the
required map order from a caller-selected alternate and cannot prove missing
or extra bindings.

Physical identity observation may honestly remain unavailable until a later
materialization gate. The PUBLIC planning layer must nevertheless represent
the complete closed virtual row and derive one unique runtime/DLL plan from an
authenticated design/profile input, or explicitly stop before publishing
those objects as validated plans.

## 6. Verifier and forbidden-capability assessment

The review authenticated the verifier through the externally pinned
verification manifest before running it. Its snapshot binds the implementation
manifest and ten targets, the five design closures, the approving review, the
CONTROL decision, and the v0.1 implementation review. Candidate imports occur
only inside the authenticated temporary snapshot, and the before/after input
sentinel passed.

Static and manual inspection found no candidate filesystem, native, process,
network, provider/model, compiler, build, materialization, rehearsal, S0, or
E0 call surface. The verifier's subprocess and temporary filesystem use are
review orchestration only and are not imported by candidate code.

The shipped verifier does not expose the hostile cases in Findings 1 through
3, so its 18-test PASS is positive regression evidence rather than proof of
the complete contract.

## 7. Evidence boundary and maximum claim

This review used only the authenticated PUBLIC allowlist and clearly fake
in-memory hostile values. It did not access F0 content. It did not use a
compiler, native source, binary, runtime tree, native API, platform probe,
network, provider/model, executor, judge, rehearsal, S0, or E0 operation.

Maximum supported claim: v0.2 is a PUBLIC, nonexecuting implementation
revision that closes the schema and record findings and improves byte-bound
diagnostics and planning checks, while remaining blocked on external pins. It
does not yet implement a uniquely design-bound, mutation-stable runtime/DLL
planning authority. Nothing establishes a real build, materialization,
Windows behavior, rehearsal, S0, central system, Project Brain integration,
operational safety, economic value, or model-to-model transfer.

## 8. Verdict and exact next gate candidate

Verdict: `REVISE-AND-REVIEW`.

The exact next gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.3 REVISION OPEN`

This review does not open that gate and does not authorize commit, push, PR,
main integration, build execution, materialization, platform testing,
rehearsal, S0, or E0 work.
