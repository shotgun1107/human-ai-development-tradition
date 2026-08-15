# S0 v0.14 public build/runtime materialization implementation v0.3 independent review

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.3 INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent PUBLIC implementation reviewer
- `reviewed_commit`: `1593af5c6553594ec9dd74c6c0148770deeed3f0`
- `reviewed_tree`: `5a6b055a2d52384c97504f0f9919dc34cc56e80b`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: 0 BLOCKING / 3 MAJOR / 0 MINOR
- `F0_content_access`: none

## 1. Outcome

The v0.3 candidate closes several concrete v0.2 defects. Plain invented
mutation matrices and resource maps reject, accepted semantic containers are
copied into immutable values, runtime path-index results are reconstructed
from immutable rows, case-folded file/directory prefix collisions reject, and
exact or descendant aliases of all three denied roots reject. `RuntimeRow`
now implements the retained eight-field codec. The public runtime and DLL plan
entry points honestly remain unavailable at
`BLOCKED-MISSING-EXTERNAL-PIN`.

The revision still has three material API-level identity defects. An exported
`EffectiveDesign` can carry caller-invented digest objects because its digest
fields are compared without exact-type validation. The DLL diagnostic layer
implements the superseded case-preserving directory hash and raw-path order,
not the effective v0.4/v0.5 identity-key rules, and its exported aggregate can
be directly constructed with mutually inconsistent or denied directory data.
Finally, the exported diagnostic record codecs admit Boolean/integer schema
drift and arbitrary noncanonical bytes under a field named
`body_canonical_sha256`.

None of these defects sets an execution-authority bit or opens a build,
materialization, native, network, provider, rehearsal, S0, or E0 surface.
They are therefore MAJOR rather than BLOCKING. They prevent a zero-finding
next-gate verdict.

## 2. Input and repository authentication

Before substantive review, the following matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- isolated review branch:
  `codex/s0-build-runtime-materialization-implementation-v03-review`;
- HEAD and candidate source remote ref:
  `1593af5c6553594ec9dd74c6c0148770deeed3f0`;
- reviewed tree:
  `5a6b055a2d52384c97504f0f9919dc34cc56e80b`;
- sole parent:
  `4f2085b5bc76a30fc39d4d82904395a33e08b432`; and
- initial tracked/index/untracked change count: zero.

The implementation and verification manifests matched their external pins:

- implementation:
  `4c91cc9c248894e8ec2f30cc5339061f591e21ac63429a2b046194a7458095a5`;
- verification:
  `beb4adc2b055d06900c5b3fff2255f8455ab4d10ce9aef8cc49ade92e6a848a9`.

Their authenticated target union plus the verification manifest itself was
exactly 17 case-fold-unique candidate files. Every target existed and every
target hash matched. The candidate commit changed exactly those same 17
files, with zero extra or missing path.

The five design manifests matched their external pins
`bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c`,
`47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`,
`1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277`,
`7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884`,
and
`ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c`.
Their 6 / 7 / 9 / 9 / 7 target closures had zero missing target, malformed
row, duplicate target, or hash mismatch.

The approving v0.5 design review, CONTROL decision, v0.1 implementation
review, and v0.2 implementation review matched their pins
`5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`,
`d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`,
`fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b`,
and
`321f8a29edabbd2592e60cac3c58c46af3cba35e157956cf710b92615df9af59`.
Both admitted predecessor implementation-review sidecars matched their
Markdown identities.

The canonical validator SelfTest passed. After writing, the review Markdown
and sidecar passed its independently labeled UTF-8, BOM, final-LF,
trailing-whitespace, sidecar-format, and sidecar-hash checks.

Aggregate-only F0 checks returned exactly 32 / 11 / 10 tracked entries.
Worktree and index quiet-diff codes were zero, as were untracked, ignored,
skip-worktree, and assume-unchanged anomaly counts. No F0 filename or content
was enumerated, opened, searched, quoted, summarized, or used.

## 3. Verification evidence

### 3.1 Author evidence

The externally authenticated verifier copied only authenticated PUBLIC bytes
into a temporary snapshot and launched an isolated `python -I -B` unittest
child. All 20 shipped tests passed with no failure, error, or skip. The
candidate and design manifest authentication, auxiliary review pins,
original-input swap sentinel, schema-dependency block, and nonexecution
terminal fields all passed.

The author suite positively covered ordinary invented matrices and resource
maps, caller-backed path-index mutation, the prior raw-case prefix inversion,
denied-root aliases, the eight runtime-row fields, alternate caller DLL order
at the blocked plan entry, unconditional schema blocking, and unavailable
filesystem observations. That is useful regression evidence, but it did not
exercise the three findings below.

### 3.2 Independent hostile evidence

Independent PUBLIC in-memory tests first replayed 19 predecessor-closure
cases. All 19 behaved as required:

- invented 115-row matrices and twelve-entry resource maps rejected;
- the runtime diagnostic path index remained stable after an unrelated
  caller mapping was cleared;
- the `Runtime/A/b` plus `runtime/a` case-folded prefix inversion rejected;
- case aliases of each denied root, including descendants, rejected;
- zero runtime bytes, open classification, invalid semantic role and phase,
  invalid provenance digest, and traversal provenance path rejected;
- A/B and B/A caller DLL orders both failed at the plan entry; and
- runtime planning, DLL-directory derivation, DLL planning, schema registry
  authentication, and profile validation remained blocked without external
  pins.

A separate eight-case hostile matrix then produced eight unexpected accepted
objects or divergences:

1. an arbitrary equality-spoofing digest object was retained by a newly
   constructed `EffectiveDesign`;
2. a rejected `BuildRuntimeDiagnostic` accepted Boolean `false` as its
   zero-valued mutation count;
3. `InMemoryRecordDiagnostic` accepted non-JSON, non-LF bytes as a canonical
   body;
4. DLL directories were ordered by case-preserving path rather than the
   lowercase identity key;
5. DLL directory digests used a different preimage from the effective design;
6. a factory-produced DLL structure accepted application-path rebinding;
7. an empty DLL aggregate accepted; and
8. an unused directory at an exact denied-root case alias accepted inside a
   directly constructed DLL aggregate.

These tests used only authenticated design bytes and clearly fake in-memory
values. They did not compile, build, materialize, call a native API, access a
network or provider, launch the candidate, run a rehearsal, or execute S0/E0.

## 4. Prior-finding disposition

| Prior finding | Disposition | Independent evidence |
|---|---|---|
| `BRM-I02-IR-001` | PARTIALLY CLOSED | Plain invented matrix/resource values reject and path-index backing mutation no longer affects an accepted diagnostic. Exact digest-field authority remains forgeable under `BRM-I03-IR-001`. |
| `BRM-I02-IR-002` | CLOSED | Prefix analysis now sorts case-folded identities, and exact or descendant aliases of all denied roots reject in `RuntimeRow` and `DllRow`. |
| `BRM-I02-IR-003` | PARTIALLY CLOSED | The eight-field runtime row is closed and all runtime/DLL plan entry points reject without an external pin. The published DLL structure and identity diagnostics contradict retained design semantics and admit inconsistent direct construction under `BRM-I03-IR-002`. |

## 5. Findings

### BRM-I03-IR-001 - MAJOR - `EffectiveDesign` digest identity remains caller-forgeable

`EffectiveDesign.__post_init__` now reconstructs the complete matrix,
resources, relations, and policy from a stable authenticated source and
byte-compares the values. That closes the ordinary invented-value cases.
However, the two digest fields are never required to be exact strings and are
not normalized into immutable copies. They are accepted solely through
`self.relations_sha256 != expected` and
`self.publication_policy_sha256 != expected` comparisons.

Starting from the legitimate authenticated object, the independent hostile
test used `dataclasses.replace` to set `relations_sha256` to a mutable
non-string object whose equality method reports equality with any value. The
constructor succeeded and retained that same caller object. The identical
attack applies to `publication_policy_sha256`.

This does not affect the internally produced object returned by the intended
candidate entry point, but the package exports `EffectiveDesign` as a public
type whose name and constructor assert authenticated semantic identity. As in
the prior review, a public authority-bearing object must not depend on a
caller's comparison method. Require exact `str`, require exact lowercase
SHA-256 grammar, compare to the reconstructed digest, and store the exact
expected immutable string.

### BRM-I03-IR-002 - MAJOR - DLL diagnostics contradict effective identity rules and do not preserve aggregate coherence

The authenticated v0.4 rule retained by v0.5 defines the exact directory
preimage as:

```text
windows_directory_identity_key=<ascii-lowercase-canonical-virtual-directory>
```

with one final LF. It explicitly rejects hashing the original case-preserving
path. After the application directory at index zero, remaining directories
must be sorted by strict unsigned-ASCII bytes of the lowercase identity key;
raw case-preserving paths never determine order.

The candidate instead hashes
`directory=<case-preserving-directory>\n` and sorts remaining parent
directories by their case-preserving path bytes. For the accepted fake rows
under `Runtime/Z` and `runtime/a`, it returned:

`runtime/app | Runtime/Z | runtime/a`

instead of the required identity-key order:

`runtime/app | runtime/a | Runtime/Z`.

For `Runtime/Z`, the candidate digest was
`eacde88d6f3f0fd94e714c33688f64ff7cedad1b65c4e9ecfe99e8ba31cf3b43`,
while an independent hash of the effective preimage was
`6e1c6a01c79a9c38f2a4ea02f972eb61ed782cda70cd65e99dcaad2e5c94a51d`.
Even the lowercase input produces a different candidate digest because the
field name in the preimage is wrong.

The aggregate class also validates less than its factory. Replacing only the
application path of a factory-produced result with another valid parent
succeeded without updating directory zero. Direct construction separately
accepted an empty directory/binding inventory and an unused directory at the
exact case alias `S0-LAB/CONTROL/F0-SEALED`. The constructor does not require
directory zero to equal the application parent, require a nonempty bijection,
require every directory to be used, or repeat denied-root checks for directory
rows.

The constant `authority_status=BLOCKED-MISSING-EXTERNAL-PIN` correctly stops
these values from becoming validated plans, and the real plan functions
remain closed. It does not make a contradictory value an exact ordered
structure diagnostic. The successor should either remove these normative-
named diagnostics until the design-bound closure exists or derive, copy, and
fully revalidate every field under the effective v0.4/v0.5 identity rules.

### BRM-I03-IR-003 - MAJOR - exported diagnostic records admit false canonical and field-type identities

`BuildRuntimeDiagnostic` byte-binds its raw JSON and checks its closed key set,
but its rejected branch compares `mutation_row_count != 0` without requiring
an exact integer. JSON Boolean `false` equals integer zero in Python, so an
independently canonicalized rejected record with
`"mutation_row_count":false` constructed successfully. Its property is
declared as an integer but returns a Boolean.

`InMemoryRecordDiagnostic` likewise verifies only that
`body_canonical_sha256` hashes `body_raw`. Direct construction with the exact
bytes `not-json`, their SHA-256, and the honest default unavailable
observations succeeded. The bytes have no JSON grammar or final LF and are not
the canonical output of the shipped constructor, yet the accepted object
labels their digest `body_canonical_sha256`.

Neither case claims a file close/readback, materialization, or execution, so
this is not a false operational result. It is still a material record-identity
defect in exported byte-bound diagnostic types. Exact integer-vs-Boolean
validation and equality to a parsed-and-reencoded canonical body are required
at construction and every record transition.

## 6. Verifier and forbidden-capability assessment

The review authenticated the verifier through the externally pinned
verification manifest before running it. Its snapshot bound the candidate
manifest and ten targets, all five design closures, the approving v0.5 review,
the CONTROL decision, and the v0.1/v0.2 implementation reviews. Candidate
imports occurred only from the authenticated temporary snapshot. The
before/after original-input sentinel passed.

Manual inspection of every authenticated candidate source found no candidate
filesystem, process, native, network, provider/model, compiler, build,
materialization, rehearsal, S0, or E0 call surface. The verifier's temporary
PUBLIC filesystem and Python unittest subprocess were review orchestration,
not candidate authority or operational evidence.

The shipped verifier does not cover custom-comparison digest fields, the
effective v0.4 directory preimage, case-folded identity-key ordering, direct
DLL aggregate construction, rejected-record Boolean drift, or direct
noncanonical record bodies. Its 20-test PASS is positive regression evidence,
not proof of the complete API contract.

## 7. Evidence boundary and maximum claim

This review used only the authenticated PUBLIC allowlist and clearly fake
in-memory hostile values. It did not access F0 content. It did not use a
compiler, native source, binary, runtime tree, native API, platform probe,
network, provider/model, executor, judge, rehearsal, S0, or E0 operation.

Maximum supported claim: v0.3 is a PUBLIC, nonexecuting revision that closes
the ordinary invented matrix/resource, mutable path-index, case-folded runtime
prefix, denied-root alias, and eight-field runtime-row defects while keeping
all external-pin plan authority blocked. It does not yet provide unforgeable
semantic diagnostic identities, design-consistent DLL identity diagnostics,
or exact exported diagnostic record codecs.

Nothing establishes a real build, materialization, Windows behavior,
rehearsal, S0, the central system, Project Brain integration, operational
safety, economic value, or model-to-model transfer.

## 8. Verdict and exact next gate candidate

Verdict: `REVISE-AND-REVIEW`.

The exact next gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.4 REVISION OPEN`

This review does not open that gate and does not authorize commit, push, PR,
main integration, build execution, materialization, platform testing,
rehearsal, S0, or E0 work.
