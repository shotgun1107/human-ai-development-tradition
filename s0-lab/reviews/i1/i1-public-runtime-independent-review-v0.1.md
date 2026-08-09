# I1 public-runtime independent hostile review

- Gate: `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES INDEPENDENT REVIEW OPEN`
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Authority: frozen public implementation prerequisites only
- Review mode: fresh, independent, read-only
- Repository files modified: none
- E0, sealed, oracle, fixture, bank, executor, and other-agent outputs inspected: none

## 1. Baseline and authentication

### Git baseline

| Check | Observed | Result |
|---|---|---|
| Origin | `https://github.com/shotgun1107/human-ai-development-tradition.git` | PASS |
| Branch | `codex/s0-i1-public-runtime` | PASS |
| HEAD | `4a63aa3b0267aad83dfe453de7fb8c15a572c54a` | PASS |
| Remote branch ref | `4a63aa3b0267aad83dfe453de7fb8c15a572c54a` | PASS |
| Candidate parent | `c0f4e09f5566e80ffe08b3a8af30638f53fbcad4` | PASS |
| Initial worktree/index | clean | PASS |
| Candidate change set | exactly 28 additions under `s0-lab/i1/**` | PASS |
| Other added/modified/deleted paths | none | PASS |
| Git object modes | 28/28 regular `100644` blobs | PASS |
| Final worktree/index | clean | PASS |

### Canonical Markdown verification

`verify-text-artifacts.ps1 -SelfTest` passed all eleven self-tests.

All six allowlisted same-basename sidecars contained the correct hash for the exact Markdown bytes:

| Artifact | SHA-256 | Result |
|---|---|---|
| `s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | Hash/sidecar PASS; canonical trailing-whitespace check FAIL |
| `universal-response-contract-v0.14-candidate.md` | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` | PASS |
| `public-falsification-plan-v0.11.md` | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` | PASS |
| `review-response-v0.9.md` | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` | PASS |
| `urc-v0.14-independent-review-v0.1.md` | `537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605` | PASS |
| `control-integration-decision-v0.1.md` | `f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65` | PASS |

The protocol’s pre-existing lines 3–6 each end in two Markdown hard-break spaces. UTF-8, BOM, final-LF, sidecar format, and sidecar hash all passed. This is not a candidate change or hash mismatch, so substantive review continued, but canonical text hygiene did not fully pass.

`AGENTS.md` independently hashed to `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d`.

### I1 manifests

| Manifest | Required/observed SHA-256 | Rows |
|---|---|---:|
| `spec/public-runtime-files.sha256` | `4469834a5aa480575cd9384a14881b83e596646686ce04f35fcb7bd9502faed2` | 7/7 authenticated |
| `verification/implementation-files.sha256` | `314e3e2f9ba4ffccdfa6b01b55a212b0f32e49d54139ee9800d4e40f04249487` | 26/26 authenticated |
| `verification/implementation-manifest.sha256` | `51249ad017b0ad2882b169e650b5a8b23247fd3d087ce2452e28db74a38de0d9` | one correct anchor row |

Every row had canonical relative syntax, no duplicate, no escape, an existing regular file, and the exact recorded digest. The 26 payload rows plus the payload manifest and anchor equal the candidate’s exact 28-file set, with no missing or extra tracked path. The seven public-spec rows also exactly match the public-spec namespace excluding its manifest.

## 2. Method and shipped verification

The review read only the exact public allowlist. It used targeted Git metadata, the canonical validator, direct file reads, shipped tests, and read-only/in-memory or automatically deleted temporary counterexamples.

Shipped results reproduced:

- Unit tests: 32 run, 31 passed, one direct symlink test skipped because Windows symlink privilege was unavailable.
- CLI structural verification: machine-readable `status=pass`.
- `verify-i1.ps1`: exit 0.
- `git diff --check`: no candidate whitespace errors.
- Static topology audit: zero reported issues.

These results are construction tests, not operational security or S0 evidence.

## 3. Requirement-by-requirement assessment

| Requirement | Assessment |
|---|---|
| 32 aggregated role rows | Static inventory PASS |
| 40 positions / eight paired rows | PASS |
| 22 fixed signer IDs | PASS |
| 27 literal stores | PASS |
| E00A–E00H and E01–E56 | PASS; 64 exact edge IDs |
| Role/store/edge static cross-index | PASS for the frozen JSON projection |
| Omission-as-denial | Static store table is correct, but runtime enforcement is bypassable; I1-M02 |
| 14 status edges / 15 states / 17 receipts / 15 E51 pairs | PASS |
| E02 three receipts, E25 two, all other status edges one | PASS |
| Receipt grammar and fixed role/kind order | PASS only with an unmodified trusted topology argument |
| Bundle framing and E25 order | PASS only with an unmodified trusted topology argument |
| Status sequence, previous hash, bundle commitment, prefix mask, timestamp order | PASS for correctly typed inputs |
| Generic signed-envelope framing, record length/hash, role/key lookup, injected decision | Structurally PASS; no cryptographic-security claim |
| ROOT zero-receipt bundle and expected manifest-hash comparison | Structurally PASS; root authority remains external and unimplemented |
| E43/E45 comparison and publication record bindings | Not implemented or tested; I1-M06 |
| Public-spec source-hash anchors | PASS; all six exact digests match authenticated inputs |
| Same-bytes entry consumption | PASS for returned bytes |
| Traversal, static symlink/reparse, containment, entry substitution | PASS for tested/static cases |
| Complete manifest namespace under concurrent change | FAIL; I1-M04 |
| One transport-method invocation and no runner retry | PASS |
| Frozen no-tool/no-state policy object | PASS as an injected policy value, not provider enforcement |
| First final response only | PASS |
| 8,192-byte check before decoding/parsing | PASS |
| BOM, UTF-8, duplicate-key, surrogate, NFC, and non-finite JSON rejection | PASS |
| Authenticated request authority | FAIL; arbitrary/forged manifest authority is accepted, I1-M01 |
| Type/resource robustness | FAIL; invalid serializer output and unbounded empty frames, I1-M05 |
| Exclusive no-overwrite result creation | PASS in ordinary tested cases |
| Published schema accuracy | FAIL; schemas accept prohibited structures, I1-M03 |
| README/report test-count claims | Reproduced |
| README/report provenance, schema, and complete-set claims | Exceed demonstrated behavior; findings below |
| Provider/network/key/root/registry/bank/question/answer/fixture/oracle/model/scoring/simulation/sealed/E0/Project Brain implementation | Absent as required |
| D-favoring vocabulary or post-result threshold logic in I1 | None found |
| Actual A–D source/model/authority/time/scoring equality | Not implemented or validated and cannot be inferred from I1 |

## 4. Findings

### I1-M01 — major — Manifest provenance and runner authority are forgeable

Evidence:

- `s0-lab/i1/implementation/s0_i1/auth.py:108-113` defines `AuthenticatedManifest` without guarded provenance.
- `auth.py:246-266` accepts any object exposing `.entries` and `.manifest.sha256`, then creates an internally privileged `AuthenticatedBytes`.
- `s0-lab/i1/implementation/s0_i1/runner.py:98-103` checks only the internal token and self-hash. It does not bind `relative_path`, `authority_sha256`, or `authority_kind` to an independently trusted authority.
- `s0-lab/i1/tests/test_runner.py:32-47` itself creates a caller-authored manifest and anchor.
- The stronger claims appear at `s0-lab/i1/README.md:28-31` and `s0-lab/i1/verification/verification-report.md:47-50`.

Reproducible counterexample:

```python
fake = SimpleNamespace(
    entries={"request.bin": sha256_bytes(raw)},
    manifest=SimpleNamespace(sha256="f" * 64),
)
request = authenticate_manifest_entry(root, fake, "request.bin")
run_one_shot("RUN.FORGED.AUTHORITY", request, transport)
```

Observed:

```text
MANIFEST_FILE_EXISTS=False
FORGED_MANIFEST_OBJECT_ACCEPTED=True
FORGED_AUTHORITY_SHA256=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
```

Thus the transport can be invoked with arbitrary bytes even though no manifest exists. A self-authored real manifest also succeeds.

Required closure: bind authenticated bytes to a specific independently trusted anchor/path/grant and verify that authority at the runner boundary, or explicitly downgrade this to caller-asserted same-byte integrity and keep it unusable as A–D authority/equality evidence. Add forged-object and self-authored-anchor negative tests.

### I1-M02 — major — Post-load topology mutation bypasses receipt identity and omission-denial checks

Evidence:

- `s0-lab/i1/implementation/s0_i1/topology.py:444-461` authenticates the topology but returns a mutable `deepcopy`.
- `s0-lab/i1/implementation/s0_i1/canonical.py:236-262` constructs the accepted receipt table directly from the supplied mapping.
- `canonical.py:290-362` and `canonical.py:422-469` do not authenticate or revalidate that mapping.
- `topology.py:464-484` likewise performs store authorization directly against an arbitrary supplied dictionary.

Counterexample:

1. Load the authentic topology.
2. Change E05’s producer from `content-intake` to `simulation-builder`.
3. Add `public-executor` as a `raw-output-vault` reader.
4. Build a valid ROOT→E02→E05 prefix using the mutated identities.
5. Call `validate_status_chain` and `require_store_read`.

Observed:

```text
MUTATED_TOPOLOGY_ISSUES=2
MUTATED_E05_ROLE_ACCEPTED=simulation-builder
MUTATED_STORE_GRANT_ACCEPTED=true
```

The standalone audit detects the mutation, but the enforcement functions never invoke it.

Required closure: enforce an authenticated immutable topology snapshot—or the exact frozen projection digest—at each policy/parser boundary. Arbitrary mappings must not define receipt authorities or store access. Add mutation-after-load tests for receipts, stores, positions, and signer mappings.

### I1-M03 — major — Published schemas validate forbidden v0.14 structures

Evidence:

- `evidence-receipt.schema.json:7-11` permits any `E00`–`E99` and any syntactically valid role/kind.
- `evidence-bundle-structure.schema.json:5-10` does not require the ROOT manifest binding, relate `entry_count` to envelopes, or constrain status edges.
- `status-record.schema.json:7-13` permits `E99`, arbitrary masks/states, and unrelated sequence/event combinations.
- `s0-lab/i1/implementation/s0_i1/verification.py:79-84` calls only `Draft202012Validator.check_schema`; it tests metaschema validity, not conformance to v0.14.
- No negative schema-instance tests exist.

Direct Draft 2020-12 validation observed:

```text
RECEIPT_E99_ACCEPTED=True
ROOT_WITHOUT_MANIFEST_ACCEPTED=True
E25_COUNT_ARRAY_MISMATCH_ACCEPTED=True
INVALID_STATUS_RELATIONS_ACCEPTED=True
```

Required closure: make the schemas enforce all expressible fixed inventories and ROOT/non-ROOT conditions, and pair cross-field/hash relationships with the authoritative runtime validator. Add negative instance suites. If the files are intentionally non-authoritative shapes, rename and document them accordingly and remove any implication that their validation proves record conformance.

### I1-M04 — major — Complete-file-set authentication has a post-enumeration TOCTOU gap

Evidence:

- `s0-lab/i1/implementation/s0_i1/auth.py:274-285` enumerates the namespace once and compares it with the manifest.
- Only after that comparison, `auth.py:286-290` authenticates entries individually.
- There is no snapshot, directory-generation binding, or final namespace check.

Counterexample: inject an unmanifested file on the first per-entry authentication call, after enumeration has completed.

Observed:

```text
AUTHENTICATED_ENTRY_COUNT=1
UNMANIFESTED_EXTRA_PRESENT_AFTER_SUCCESS=True
```

The function returned success while its promised complete namespace contained an unmanifested file.

Required closure: use a stable immutable snapshot/trusted Git tree or another mechanism that binds enumeration and entry reads to the same namespace state. If that is outside this gate, narrow the claim to authentication of consumed entry bytes and explicitly disclaim concurrent complete-file-set security.

### I1-M05 — major — Exact serializers/parsers and frame processing lack runtime type and resource bounds

Evidence:

- `s0-lab/i1/implementation/s0_i1/canonical.py:96-103` converts an unbounded decimal with `int()` without a digit ceiling or normalization of `ValueError`.
- `canonical.py:365-392` accepts Python `bool` as an integer and emits noncanonical text.
- `s0-lab/i1/implementation/s0_i1/runner.py:113-131` accepts empty chunks, non-string truthy response IDs, and non-boolean truthy `final` values; the byte ceiling does not bound frame count or work.

Observed:

```text
OVERSIZED_DECIMAL_EXCEPTION=ValueError
BOOL_SERIALIZER_SEQUENCE_LINE=sequence=True
BOOL_SERIALIZER_ROUNDTRIP=CanonicalRecordError
EMPTY_FRAME_STREAM_ACCEPTED_COUNT=100001
RESPONSE_BYTES=2
```

An infinite empty-frame iterator never reaches the 8,192-byte ceiling.

Required closure: reject `bool` and other non-exact integer types before serialization, bound decimal digit counts before conversion, normalize malformed records to the stable canonical error class, require exact frame field types, and impose a finite empty-frame/frame-count bound or explicitly delegate it to a separately frozen transport contract.

### I1-M06 — major — Current-plan comparison and publication bindings remain topology-only

The allowlisted plan defines recipient-verifiable E43/E45 comparison records at `public-falsification-plan-v0.11.md:315-336` and the publication receipt at lines 338–353. These bind source-envelope hashes, extracted-record hashes, roles, common-record equality, publication equality, and timestamps.

No I1 file contains:

- `URC-0.14-COMPARISON-1`
- `URC-0.14-PUBLICATION-1`
- `left_envelope_sha256`
- `source_record_sha256`
- `published_record_sha256`

`canonical.py` ends with status-chain validation. A syntactically signed but internally inconsistent E43 comparison record is therefore accepted as an opaque generic envelope:

```text
INCONSISTENT_COMPARISON_RECORD_ACCEPTED_AS_GENERIC_ENVELOPE=True
```

Generic-envelope acceptance is not the recipient recomputation required by the plan.

Required closure: implement and mutation-test these current-plan public record bindings, or explicitly identify them as closed and narrow I1’s completeness claim. Do not treat generic-envelope parsing as comparison/publication validation.

### I1-m01 — minor — The standalone payload verifier has no independent trust anchor

Evidence:

- `s0-lab/i1/tools/verify-i1.ps1:35-47` trusts the adjacent `implementation-manifest.sha256`; no frozen expected anchor is accepted or embedded.
- Its line 36 also combines empty/BOM/CR/non-ASCII failures and checks only first byte `EF`, contrary to independently labeled byte checks and exact `EF BB BF` BOM detection.
- `s0-lab/i1/README.md:70-73` calls the payload manifest separately anchored without explaining the external trust requirement.

In an automatically deleted temporary copy, changing `README.md`, updating its manifest row, and rewriting the adjacent anchor still produced:

```text
COORDINATED_CHANGE_VERIFIER_EXIT=0
```

The current review was not fooled because it independently pinned `51249ad...`; therefore this does not invalidate the frozen candidate bytes.

Required closure: require an expected anchor digest from an independently authenticated caller or clearly state that the script is only a construction checker. Separate its text diagnostics and use exact three-byte BOM detection.

## 5. Predecessor and boundary non-regression

- All six embedded source hashes equal the authenticated protocol, contract, plan, response, review, and CONTROL-decision bytes.
- The candidate is additive and changes no predecessor.
- Static inventory exactly preserves 32 rows, 40 positions, 22 signer IDs, 27 stores, all 64 edges, and the status counts.
- No I1 source contains D-targeting vocabulary, a selection rule, post-result threshold mutation, oracle/scoring access, or an answer hint.
- References to bank, fixture, oracle, score, sealed, E0, model, simulation, and Project Brain occur only in explicit boundary disclaimers or inherited public role identifiers.
- There is no provider/network implementation, cryptographic implementation, key generation, root/registry artifact, store backend, ACL enforcement, atomic-write backend, model invocation, executor creation, scoring, or empirical analysis.
- The one-shot code does not establish that A–D receive equal facts, authority, model revision, reasoning level, wall-clock allowance, questions, or scoring opportunities. Those remain future frozen-manifest and operational checks.
- The tests are synthetic construction tests and cannot support central-system, Project Brain, safety, economic, transfer, production, or S0 conclusions.

## 6. Maximum justified claim

At commit `4a63aa3b0267aad83dfe453de7fb8c15a572c54a`, the authenticated I1 candidate contains the correct static v0.14 public inventory and several useful non-semantic byte-level construction helpers. The shipped test counts and ordinary-path results reproduce.

It does not yet provide trustworthy request authority, immutable topology enforcement, exact schema conformance, concurrent complete-file-set authentication, fully bounded record/frame handling, or the current plan’s comparison/publication validation. It therefore cannot yet serve as the reviewed public prerequisite layer, and it supplies no A–D fairness, operational-security, model, scoring, or S0 evidence.

## 7. Verdict

**REVISE-AND-REVIEW**
