# S0 v0.14 public build/runtime materialization implementation v0.4 independent review

- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.4 INDEPENDENT REVIEW OPEN`
- `review_role`: fresh independent PUBLIC implementation reviewer
- `reviewed_commit`: `d6638a3afc12766633faed530be10eaa8e51785d`
- `reviewed_tree`: `fc60df7ffd20e356636f65cccd4e0140acf6b921`
- `verdict`: `REVISE-AND-REVIEW`
- `finding_counts`: 0 BLOCKING / 2 MAJOR / 1 MINOR
- `F0_content_access`: none

## 1. Outcome

The v0.4 revision closes most of the three v0.3 implementation findings. The
two `EffectiveDesign` digest fields now require exact lowercase SHA-256 text,
the retained source manifest-hash tuple rejects non-string entries, the DLL
diagnostic layer now uses the exact lowercase identity-key preimage and order
and revalidates a closed nonempty aggregate, and the exported diagnostic
records reject Boolean/integer drift and arbitrary non-JSON bodies. All 23
shipped authenticated-snapshot tests passed.

Independent hostile testing nevertheless found two material canonical-codec
defects and one narrower authenticated-input type defect. The exported target-
set codec accepts a duck row with traversal text, negative lengths, and a
malformed digest and emits bytes labelled as the exact target-set preimage.
The exported JSON/record codec sorts non-ASCII object keys by Python code
point rather than the UTF-16 code-unit order required by RFC 8785, accepts its
own divergent bytes as canonical, and rejects the RFC-ordered bytes. Finally,
one manifest bundle path can still delegate comparison to a caller object;
an equality spoof authenticates and an exception-raising comparator escapes
the intended rejected diagnostic.

None of these defects creates an execution-authority bit or opens build,
materialization, native, process, network, provider, rehearsal, S0, or E0
authority. The two false canonical identities are MAJOR API-level defects.
The normalized-away manifest label defect is MINOR because every retained
byte and retained path remains fixed by the external pins.

## 2. Input and repository authentication

Before substantive review, the following matched exactly:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- isolated review branch:
  `codex/s0-build-runtime-materialization-implementation-v04-review`;
- HEAD and candidate source remote ref:
  `d6638a3afc12766633faed530be10eaa8e51785d`;
- reviewed tree:
  `fc60df7ffd20e356636f65cccd4e0140acf6b921`;
- sole parent:
  `0b1bc528b3ba255b01c395f2c2fa1756ef879afb`; and
- initial worktree/index/untracked change count: zero.

The implementation and verification manifests matched their external pins:

- implementation:
  `9067671d2e36c50104a8463c1a771df6d36b51ff910c0243d00aeab7763ff594`;
- verification:
  `502134d26b42c7512d08540fe5efae80924ac06399369911746281688b1d6861`.

The manifests' 16 targets plus the verification manifest itself were exactly
17 case-fold-unique candidate files. Every target existed and matched its
authenticated digest. The candidate commit changed exactly those same 17
files relative to its sole parent, with zero missing or extra path.

The five design manifests matched their external pins
`bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c`,
`47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304`,
`1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277`,
`7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884`,
and
`ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c`.
Their 6 / 7 / 9 / 9 / 7 target closures had zero malformed row, duplicate,
case alias, missing target, or digest mismatch.

The approving v0.5 design review, CONTROL integration decision, and v0.1,
v0.2, and v0.3 implementation reviews matched the verifier pins
`5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9`,
`d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf`,
`fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b`,
`321f8a29edabbd2592e60cac3c58c46af3cba35e157956cf710b92615df9af59`,
and
`b7e4fa3ccbd9c75c1aa00cbae4e5a3b460846533e551002b2ed1f437d4275cc1`.
The separately admitted v0.3 review sidecar matched that Markdown identity.

The canonical validator SelfTest passed all eleven cases. The first direct
PowerShell launch was blocked by the host execution policy; the same
authenticated script passed under explicit process-local execution-policy
bypass. This was reviewer orchestration and changed no candidate byte.

Initial aggregate-only F0 checks returned exactly 32 / 11 / 10 tracked
entries. Worktree and index quiet-diff codes were zero, as were untracked,
ignored, skip-worktree, and assume-unchanged anomaly counts. No F0 internal
filename or content was enumerated, opened, searched, quoted, summarized, or
used.

## 3. Verification evidence

### 3.1 Shipped evidence

The externally authenticated verifier copied only authenticated PUBLIC bytes
into a temporary snapshot and launched an isolated `python -I -B` unittest
child. All 23 shipped tests passed with no failure, error, or skip. Candidate
and design manifest authentication, auxiliary review pins, schema-dependency
blocking, original-input swap sentinel, and all nonexecution terminal fields
passed.

The shipped suite positively covers the three v0.3 findings: both
`EffectiveDesign` digest equality spoofs reject; the effective DLL identity
preimage, identity-key order, application directory zero, nonempty aggregate,
contiguous indices, closed used-directory set, denied directories, and
application rebinding are checked; and Boolean mutation counts and arbitrary
noncanonical record bodies reject. It also covers adjacent runtime aggregate
integer types and the closed no-execution surfaces.

### 3.2 Independent hostile evidence

An independent 31-case PUBLIC in-memory matrix imported only the already
authenticated candidate bytes and used clearly fake values. Positive results
included:

- both `EffectiveDesign` digest equality spoofs rejected, and a spoofed
  retained manifest-hash entry rejected;
- DLL identity-key ordering and the exact
  `windows_directory_identity_key=<lowercase-key>` plus LF digest matched an
  independent hash;
- application rebinding, empty aggregates, unused directories, noncontiguous
  Boolean indices, case-folded duplicate DLL names, application-parent case
  aliases, and exact aliases of all three denied roots rejected;
- Boolean `mutation_row_count`, arbitrary non-JSON record bytes, false
  filesystem observations, Boolean runtime aggregates, case-folded runtime
  aliases, and case-folded file/directory prefix collisions rejected; and
- mutation of caller-owned record objects and runtime input iterables did not
  alter accepted diagnostics.

Four unexpected observations established the findings below:

1. a duck target row with path `../outside`, byte length `-1`, and digest
   `not-a-digest` was accepted by `target_set_preimage`;
2. the emitted target-set bytes included both
   `total_target_bytes=-1` and `target_byte_length=-1`;
3. a record containing object keys U+10000 and U+E000 was emitted in Python
   code-point order, accepted as canonical, and the RFC 8785 UTF-16-ordered
   bytes were rejected; and
4. a non-string equality-spoof manifest logical path authenticated, while an
   exception-raising path comparator propagated `RuntimeError` from the
   intended candidate entry point instead of producing `CANDIDATE-REJECTED`.

These tests did not compile, build, materialize, call a native API, access a
network or provider, launch the candidate, run a rehearsal, or execute S0/E0.

## 4. Prior-finding disposition

| Prior finding | Disposition | Independent evidence |
|---|---|---|
| `BRM-I03-IR-001` | PARTIALLY CLOSED | Both `EffectiveDesign` digest fields now require exact strings and reject equality spoofs; retained `AuthenticatedDesign.manifest_hashes` entries also require exact strings. The adjacent source-bundle logical path still delegates comparison to a caller object under `BRM-I04-IR-003`. |
| `BRM-I03-IR-002` | CLOSED | The exact retained DLL preimage and identity-key order match; application directory zero, nonempty and contiguous directories/rows, closed used-directory set, denied-root rejection, application binding, and direct-constructor coherence all held under hostile testing. |
| `BRM-I03-IR-003` | PARTIALLY CLOSED | Exact Boolean/integer checks and arbitrary-body rejection are repaired in `BuildRuntimeDiagnostic`, `InMemoryRecordDiagnostic`, and adjacent aggregate types. A narrower but real RFC 8785 canonical-byte divergence remains in the same exported record codec under `BRM-I04-IR-002`. |

## 5. Findings

### BRM-I04-IR-001 - MAJOR - the exported target-set codec accepts invalid duck rows

`TargetRow.__post_init__` correctly validates canonical virtual paths,
nonnegative exact integer byte lengths, and lowercase SHA-256 text. However,
`target_set_preimage` does not require its elements to be exact `TargetRow`
objects and does not repeat those validations at the codec boundary. It reads
the three attributes from any object.

The hostile row used:

```text
path=../outside
byte_length=-1
sha256=not-a-digest
```

The function returned an `S0-BRM-TARGET-SET-PREIMAGE-1` byte string containing
the traversal path, malformed digest, and negative canonical-decimal fields.
This contradicts the retained design's nonempty repository-relative ASCII
path grammar, canonical unsigned-decimal lengths, and 64-character lowercase
digest grammar. A consumer can therefore hash bytes produced by the package's
named canonical target-set codec that are outside the exact target-set
contract.

This helper is not reached by the intended blocked candidate entry point and
does not grant execution authority, so the finding is MAJOR rather than
BLOCKING. Require an exact nonempty tuple of exact `TargetRow` objects, copy
it, and revalidate every field before constructing the preimage.

### BRM-I04-IR-002 - MAJOR - the exported record codec misorders valid non-ASCII JCS object keys

The retained record contract requires RFC 8785 JCS UTF-8 plus one final LF.
RFC 8785 orders object property names by their UTF-16 code units. The exported
`jcs_lf` helper instead uses Python `json.dumps(sort_keys=True)`, which orders
strings by Unicode code point. The helper's comment narrows its intended
implementation to an ASCII domain, but neither `jcs_lf`,
`construct_in_memory_record`, nor `InMemoryRecordDiagnostic` rejects
non-ASCII object keys.

For the valid JSON object with keys U+10000 and U+E000, UTF-16 order places
U+10000 (`D800 DC00`) before U+E000. The candidate placed U+E000 first. Its
accepted bytes had SHA-256:

`855092a2e2a4a9076c7a3286ed160eaeb82dd1ff70ca0b9c6fa21feaa883b67f`.

The RFC-ordered bytes had SHA-256:

`bf1887a7f413e6c4569346461e61afe2fcb3fdf3708208710a59a22044d8e4b8`.

Direct `InMemoryRecordDiagnostic` construction accepted the first byte string
as canonical and rejected the second. Thus the v0.3 arbitrary-byte defect is
substantially repaired, but the public codec still assigns a false canonical
identity to a valid JSON object. This does not affect the candidate's current
ASCII fixed diagnostic or open execution, but it is a material record-identity
defect. Implement the exact RFC 8785 property sort or explicitly reject every
value outside a completely enforced ASCII-key domain before assigning a
canonical digest.

### BRM-I04-IR-003 - MINOR - manifest logical-path comparison is caller-dispatched

`_authenticate_manifest` requires an exact `ManifestBundle`, exact bytes, and
an exact target dict, but it evaluates `bundle.logical_path != expected_path`
without first requiring `type(bundle.logical_path) is str`. A mutable
non-string object whose equality methods report a match authenticated. A
second object whose comparison raised `RuntimeError` escaped
`prepare_public_build_runtime_candidate` rather than returning its documented
rejected diagnostic.

The externally pinned manifest bytes, target closure, and expected literal
path are still used to build the resulting `AuthenticatedDesign`; the caller
object is discarded. No wrong byte, wrong retained path, or authority bit was
produced, which limits severity to MINOR. Check the exact string type before
any comparison and convert all malformed bundle fields into the stable
authentication error taxonomy.

## 6. Verifier and forbidden-capability assessment

Manual inspection of every authenticated candidate source, test, report,
manifest, sidecar, and verifier file found no candidate filesystem, process,
native, network, provider/model, compiler, build, materialization, rehearsal,
S0, or E0 call surface. The verifier's temporary PUBLIC filesystem and Python
unittest subprocess were review orchestration, not candidate authority or
operational evidence.

The verifier binds the candidate manifest and its ten targets, all five
design closures, the approving v0.5 review, the CONTROL decision, and the
v0.1-v0.3 implementation reviews before snapshot import. Its original-input
swap sentinel passed. The shipped static forbidden-surface scan passed.

The shipped suite does not test duck target rows, UTF-16 JCS property order,
or caller-dispatched manifest path comparisons. Its 23-test PASS is useful
regression evidence, not proof of the complete exported API contract.

## 7. Evidence boundary and maximum claim

This review used only the authenticated PUBLIC allowlist and clearly fake
in-memory hostile values. It did not access F0 content. It did not use a
compiler, native source, binary, runtime tree, native API, platform probe,
network, provider/model, executor, judge, rehearsal, S0, or E0 operation.

Maximum supported claim: v0.4 is a PUBLIC, nonexecuting revision that repairs
the principal digest, DLL-identity/coherence, Boolean-type, and arbitrary-
record-body defects while keeping every external-pin plan authority blocked.
It does not yet provide exact fail-closed behavior across all exported
canonical codecs and authenticated input fields.

Nothing establishes a real build, materialization, Windows behavior,
rehearsal, S0, the central system, Project Brain integration, operational
safety, economic value, or model-to-model transfer.

## 8. Verdict and exact next gate candidate

Verdict: `REVISE-AND-REVIEW`.

The exact next gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.5 REVISION OPEN`

This review does not open that gate and does not authorize commit, push, PR,
main integration, build execution, materialization, platform testing,
rehearsal, S0, or E0 work.
