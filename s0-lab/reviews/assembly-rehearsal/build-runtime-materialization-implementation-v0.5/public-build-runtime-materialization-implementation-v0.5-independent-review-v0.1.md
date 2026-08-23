# S0 v0.14 public build/runtime materialization implementation v0.5 independent review

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.5 INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent PUBLIC implementation reviewer
- `reviewed_commit`: `e5f6608f1cf239dd89e2951ea077e87c2c810a5d`
- `reviewed_tree`: `08416d25c85693db7285ba168356ac37da0c2a63`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: 0 BLOCKING / 1 MAJOR / 0 MINOR
- `F0_content_access`: none

## 1. Outcome

The v0.5 candidate closes all three authenticated v0.4 implementation
findings. The target-set codec now requires a nonempty exact tuple of exact
`TargetRow` objects and reconstructs every row before serialization. The JCS
codec recursively orders object properties by UTF-16 code units, including
U+10000 before U+E000 at nested depths. Manifest logical paths require exact
strings before comparison, so equality-spoofing and exception-raising objects
both take the stable rejected diagnostic path.

The shipped authenticated-snapshot verifier passed all 26 tests, and the
intended entry point still terminates at
`BLOCKED-MISSING-EXTERNAL-PIN` with every execution and operational claim bit
false.

Independent adjacent testing nevertheless found one material aggregate-codec
defect. The runtime and DLL structural validators trust the prior
`__post_init__` execution of exact child dataclass instances instead of
reconstructing every child and revalidating its complete closed field set.
Reflectively mutated exact children therefore cross those exported aggregate
boundaries and produce accepted diagnostics with invalid provenance, digest,
path, enumeration, length, name, and integer fields. This is the same
post-construction mutation class that v0.5 correctly rejects at the target-set
boundary.

The affected values remain diagnostics whose authority status is
`BLOCKED-MISSING-EXTERNAL-PIN`; the design-bound runtime/DLL plan entry points
always reject. No build, materialization, native, process, provider, rehearsal,
S0, or E0 authority was opened. The defect is therefore MAJOR rather than
BLOCKING, but it prevents a zero-finding verdict.

## 2. Input and repository authentication

Before substantive review, the following matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- isolated review branch:
  `codex/s0-build-runtime-materialization-implementation-v05-review`;
- HEAD and candidate source remote ref:
  `e5f6608f1cf239dd89e2951ea077e87c2c810a5d`;
- reviewed tree:
  `08416d25c85693db7285ba168356ac37da0c2a63`;
- sole parent:
  `eb5da0cb4a38113b1225c3dbb352fcd810584739`; and
- initial worktree, index, and untracked counts: zero.

The implementation and verification manifests matched their external pins:

- implementation:
  `9e3dd30dc3e179313763c1624041386b025c6bf273c49bd767f03bfbb36799ca`;
- verification:
  `6933564337e7a53051d7ee87836a76bdd68c1fbec6bc5ffe0d679ca0097985f8`.

Their target union plus the verification manifest itself was exactly 17
ordinal- and case-fold-unique candidate files. Every target existed and
matched its authenticated digest. The candidate commit changed exactly those
17 files relative to its sole parent, with zero missing or extra path.

The five design manifests matched their external pins
`bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c`,
`47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`,
`1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277`,
`7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884`,
and
`ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c`.
Their exact 6 / 7 / 9 / 9 / 7 target closures had zero malformed row,
duplicate, missing target, or digest mismatch.

The approving design review, CONTROL decision, and v0.1 through v0.4
implementation reviews matched their supplied Markdown pins
`5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`,
`d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`,
`fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b`,
`321f8a29edabbd2592e60cac3c58c46af3cba35e157956cf710b92615df9af59`,
`b7e4fa3ccbd9c75c1aa00cbae4e5a3b460846533e551002b2ed1f437d4275cc1`,
and
`f6e61510a2d63966d72d5d88018d3e0dbcaeb0d3a391dba27cc3902a071a486f`.
All six same-basename sidecars passed the canonical validator.

The canonical validator SelfTest passed all eleven cases. Initial aggregate-
only F0 checks returned exactly 32 / 11 / 10 tracked entries. Worktree, index,
and parent quiet-diff codes were zero, as were untracked, ignored,
skip-worktree, and assume-unchanged anomaly counts. No F0 internal filename or
content was enumerated, opened, searched, quoted, summarized, or used.

Reviewer-local PowerShell argument binding, scalar indexing, constructor
overload, and serializer-overload errors were corrected and rerun. They
changed no candidate byte and are not candidate findings.

## 3. Verification evidence

### 3.1 Shipped verifier

The externally authenticated verifier was run with the exact implementation
pin. It copied authenticated PUBLIC bytes into a temporary snapshot and ran an
isolated `python -I -B` unittest child. All 26 tests passed with no failure,
error, or skip. Candidate/design manifest authentication, auxiliary review
pins, schema-dependency blocking, original-input swap sentinel, and all
nonexecution terminal fields passed.

Manual source inspection confirmed that candidate modules have no filesystem,
process, native, network, provider/model, compiler, build, materialization,
rehearsal, S0, or E0 call surface. The verifier's temporary PUBLIC filesystem
and unittest process were verification orchestration, not candidate authority
or operational evidence.

### 3.2 Independent contract reconstruction

An independent PowerShell construction, separate from the candidate codecs,
confirmed:

- the one-position relation patch preserves 68 unique relations, produces
  exactly 6,805 ASCII/LF bytes, and hashes to
  `5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`;
- the sole normative 20-field policy produces exactly 896 JCS-compatible
  UTF-8-plus-final-LF bytes and hashes to
  `3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`;
  and
- the effective matrix reconstructs as 46 / 63 / 97 / 111 / 115 rows, with
  115 unique IDs and exact `/0` or `/1` suffix agreement with every Boolean
  output-created field.

### 3.3 Independent hostile evidence

An authenticated-import PUBLIC in-memory suite produced 34 expected positive
or rejection results with zero expectation failure. It covered candidate
blocking, exact authority flags, target-set byte grammar, exact tuple and row
types, post-construction target-row mutation, UTF-16 root and nested JCS order,
canonical record acceptance, noncanonical record rejection, lone-surrogate
rejection, exact-string manifest labels, stable comparison-spoof rejection,
semantic backing-map isolation, invented-resource rejection, authority-byte
reauthentication, record input copying, schema blocking, hostile paths, and
mutated DLL-input revalidation.

A focused adjacent matrix then produced twelve unexpected acceptances:

1. a `RuntimeRow` whose `semantic_role` was changed to invalid uppercase text;
2. a malformed provenance-manifest digest;
3. a traversal `provenance_path`;
4. Boolean `false` as the row byte length, yielding one accepted file and
   aggregate `total_bytes=0`;
5. a malformed target digest;
6. an open, unlisted classification;
7. a lowercase load/read phase;
8. a DLL resolution child whose name no longer matched the `.dll` grammar;
9. a malformed DLL target digest;
10. Boolean `false` as a DLL resolution directory index;
11. a malformed DLL directory-identity digest; and
12. Boolean `false` as a DLL directory index.

These cases used exact candidate dataclass instances, mutated them with
`object.__setattr__`, and then submitted them to a fresh exported factory or
aggregate reconstruction. No existing accepted output was merely inspected
after caller-side sabotage: the candidate boundary itself accepted each
mutated child while creating or reconstructing an aggregate.

## 4. Prior-finding disposition

| Prior finding | Disposition | Independent evidence |
|---|---|---|
| `BRM-I04-IR-001` | CLOSED | `target_set_preimage` requires a nonempty exact tuple of exact `TargetRow` values, reconstructs each row, matches an independent exact preimage, and rejects duck, subclass, list, empty, traversal-mutated, Boolean-length, and malformed-digest cases. |
| `BRM-I04-IR-002` | CLOSED | `jcs_lf` places U+10000 before U+E000 at the root and inside nested objects; record construction emits the same bytes, and reversed non-RFC bytes reject. |
| `BRM-I04-IR-003` | CLOSED | Equality-spoofing, exception-raising, and integer manifest logical paths all return the stable `CANDIDATE-REJECTED` / `BR-AUTH/0` diagnostic without caller-dispatched comparison or escaped exception. |

## 5. Finding

### BRM-I05-IR-001 - MAJOR - runtime and DLL aggregates do not revalidate complete child identities

`RuntimeRow.__post_init__` correctly closes its eight fields. However,
`_validate_runtime_rows` checks only that each element has exact
`RuntimeRow` type, then consumes a subset of fields for path order, identity
keys, role uniqueness, and aggregate byte count. It does not reconstruct each
row through `RuntimeRow(...)` and does not repeat the semantic-role grammar,
provenance digest/path, per-row byte-length type/range, target digest,
classification enum, or load/read-phase checks. Both
`inspect_runtime_tree_structure` and `RuntimeTreeStructureDiagnostic` rely on
that incomplete aggregate validator.

The seven mutated runtime cases in Section 3.3 were therefore accepted. The
Boolean-length case is especially concrete: one exact row crossed the
aggregate boundary with `byte_length=false` and produced an accepted
`RuntimeTreeStructureDiagnostic(file_count=1, total_bytes=0)`, contradicting
the retained exact-integer and minimum-one-byte row contract.

`DllResolutionStructureDiagnostic.__post_init__` has the analogous issue. It
requires exact child classes and checks relational coherence, but it does not
reconstruct `DllDirectoryDiagnostic` or `DllResolutionRowDiagnostic` before
use. Mutated child names, target and identity digests, and Boolean indices
therefore survived a fresh `dataclasses.replace` aggregate reconstruction.
The ordinary `inspect_dll_resolution_structure` input path does reconstruct a
mutated `DllRow` and correctly rejects it; the defect is specifically the
exported aggregate's trust in already constructed child objects.

This is not merely a complaint that Python objects are caller-mutable. The
v0.5 candidate itself recognizes reflective post-construction mutation as an
admitted hostile input class and repairs it by reconstructing every
`TargetRow` at the target-set boundary. The adjacent runtime and DLL
aggregate boundaries consume exact public child dataclasses under the same
model but do not apply that repair. They can consequently publish false
structural identities even though their named child codecs reject those same
values directly.

No accepted aggregate can authorize execution: `authority_status` remains
`BLOCKED-MISSING-EXTERNAL-PIN`, `execution_authorized` remains false, and
`plan_runtime_tree`, `derive_dll_directories`, and `plan_dll_resolution`
always reject. The finding is therefore MAJOR rather than BLOCKING.

Require aggregate construction to rebuild every runtime and DLL child through
its exact closed constructor before any field is consumed or stored. Store
only the rebuilt immutable children, then perform aggregate coherence checks.
Add hostile cases for every child field, including Boolean/integer equality,
provenance paths and digests, DLL names and hashes, and directory identity
fields.

## 6. Verifier and forbidden-capability assessment

The verifier authentically binds the candidate manifest and ten targets, all
five design closures, the approving design review, the CONTROL decision, and
all four predecessor implementation reviews before snapshot import. Its
before/after input sentinel passed.

The shipped suite directly covers the three v0.4 findings but does not submit
reflectively mutated `RuntimeRow`, `DllDirectoryDiagnostic`, or
`DllResolutionRowDiagnostic` children to fresh aggregate construction. Its
26-test PASS is useful regression evidence, not proof of the complete
exported aggregate contract.

The ten external pin classes remain absent. Schema validation, design-bound
runtime planning, physical directory identity, native build, materialization,
publication, close/readback observation, and operational execution remain
correctly blocked. Those unavailable boundaries are not candidate defects in
this review.

## 7. Evidence boundary and maximum claim

This review used only the authenticated PUBLIC allowlist and clearly fake
in-memory hostile values. It did not access F0 content. It did not use native
source, a compiler, toolchain, binary, runtime tree, native API, platform
probe, network, provider/model, executor, judge, rehearsal, S0, or E0
operation. No key, signature, real/private/secret data, or operational input
was used.

Maximum supported claim: v0.5 is a PUBLIC, nonexecuting revision that closes
all three v0.4 findings, reconstructs the retained relation, policy, matrix,
authority, record-codec, and blocking contracts, and keeps all external-pin
plan authority unavailable. It does not yet preserve the complete closed
identity of reflectively mutated runtime/DLL children at exported aggregate
boundaries.

Nothing establishes a real build, materialization, Windows behavior,
rehearsal, S0, the central system, Project Brain integration, operational
safety, economic value, or model-to-model transfer.

## 8. Verdict and exact next gate candidate

Verdict: `REVISE-AND-REVIEW`.

The exact next gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.6 REVISION OPEN`

This review does not open that gate and does not authorize commit, push, PR,
main integration, build execution, materialization, platform testing,
rehearsal, S0, or E0 work.
