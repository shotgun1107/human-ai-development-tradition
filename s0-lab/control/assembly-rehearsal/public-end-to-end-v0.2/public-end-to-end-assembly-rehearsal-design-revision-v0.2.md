# S0 v0.14 public end-to-end assembly rehearsal design revision v0.2

- `status`: public revision candidate; independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`
- `predecessor_design_commit`: `49ecc05dacebf043ed8b2b479eb021018d4b4fe6`
- `predecessor_review_commit`: `571c8751d0abb8acfb853d402c072fdb7667bde7`
- `predecessor_review_sha256`: `9bb097acba46bfcfd6eee88ffbf0e41709f371f08fbd2226f6bdb86b615f95dd`
- `active_baseline`: `central-system-v2.1-s0-preparation`
- `implementation_status`: not implemented
- `execution_status`: not executed
- `F0_content_access`: none

## 1. Revision purpose

This revision replaces the v0.1 assembly design for future implementation. It
closes the independent review's three blocking and four major findings without
modifying I0, I1, I2, I3, their manifests, or their public contracts.

The target remains one public, model-free wiring rehearsal:

`I0 public authentication/transform -> I1 authenticated one-shot stub -> I0 answer validation -> canonical public record`.

I2 and I3 remain exact contract preflights with explicit no-import
dispositions. No signer-media import is fabricated for repository-resident
public practice data.

## 2. Authenticated component and case pins

| Item | Exact SHA-256 |
|---|---|
| I0 implementation manifest | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` |
| I1 implementation manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` |
| I2 implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` |
| I3 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` |
| public bundle manifest | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` |
| canonical B2 input | `bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863` |
| P01 B2 package | `15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7` |
| B2 questions | `661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90` |
| public P01 answer | `c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf` |
| answer schema | `e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b` |
| I2 public contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |
| I3 public contract | `ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8` |

The fixed case remains `BLK-PRACTICE0002 / P01` with rehearsal ID
`S0-PUBLIC-AR-B2-P01-001`.

Its exact paths are:

- canonical: `s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/canonical-input.json`;
- package: `s0-lab/public-practice/v0.1/packages/P01B2EMBR001/input.json`;
- questions: `s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json`;
- public response: `s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json`;
- answer schema: `s0-lab/control/sm0/answer.schema.json`;
- I2 contract: `s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json`; and
- I3 contract: `s0-lab/i3/spec/import-decision-contract-v0.1.json`.

## 3. Full public-bundle boundary

I0 `verify_public_bundle` is retained. Its actual behavior defines the positive
preflight boundary: it authenticates the public bundle manifest, enumerates
the public-practice v0.1 bundle, requires the manifest's exact file set, reads
and hashes all 90 manifest rows, parses JSON entries, and checks both public
blocks.

The future execution allowlist therefore contains:

1. `s0-lab/public-practice/v0.1/bundle-files.sha256`; and
2. exactly the 90 relative paths recorded by that authenticated manifest.

Directory-metadata traversal is allowed only beneath the exact resolved
`s0-lab/public-practice/v0.1` bundle root because I0 uses recursive discovery.
It grants no additional file content: the accepted regular-file set remains
the manifest plus its exact 90 rows, and any discovered symlink or unexpected
regular file fails I0 authentication. Empty-directory presence is not claimed
to be authenticated by I0.

The manifest SHA-256 and row count are frozen above. Missing, additional,
duplicate, noncanonical, changed, or path-escaping rows fail `AR-AUTH` before
the stub can be called. The verifier may print only aggregate counts for paths
outside its exact public allowlist. This full public bundle authorization does
not authorize any F0 content family or otherwise unclassified repository path.

After full-bundle verification, the controller selects only the fixed case
files in section 2 for request construction and answer validation.

## 4. Exact I1 request authority

The future implementation must materialize these exact public artifacts:

| Property | Exact value |
|---|---|
| manifest path | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/request-files.sha256` |
| entry prefix | `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/` |
| allowed paths | exactly `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/request.json` |
| grant purpose | `s0-public-assembly-rehearsal-v01` |
| request bytes | 7,917 |
| request SHA-256 | `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2` |
| manifest bytes | 135 |
| manifest SHA-256 | `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7` |

The exact manifest bytes are:

```text
990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2  s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/request.json
```

with one ASCII LF after the displayed row.

The request is the eight-field object frozen in the interface map. It is
serialized as UTF-8 without BOM, recursively sorted object keys,
`ensure_ascii=true`, compact `,` and `:` separators, and one final LF.
Duplicate source keys reject. Runtime reconstruction must be byte-identical to
the frozen request before the manifest grant is bound.

The reviewed controller configuration receives the exact manifest path,
manifest digest, entry prefix, one allowed path, and purpose as independent
constants. It must not discover and trust a neighboring manifest.

## 5. Exact model-free stub and the first-final boundary

I1 intentionally stops at the first final frame; it cannot generically prove
that an arbitrary transport had no later frame. This revision makes no such
generic claim.

The only permitted transport is candidate-owned
`S0-PUBLIC-EXACT-ANSWER-STUB-1`. It is constructed before output reservation
from an eager immutable tuple of exact `ResponseFrame` values. The positive
script contains exactly one frame:

- `response_id=S0-PUBLIC-AR-B2-P01-RESPONSE-1`;
- `data` equals the authenticated 1,936-byte public answer;
- `final=true`.

The exact stub iterator tracks:

- `transport_calls`;
- `script_frame_count`;
- `yielded_frame_count`;
- `close_count`; and
- `unconsumed_frame_count_on_close`.

`invoke_once` increments `transport_calls` atomically as its first instruction,
before returning or raising. A second entry raises. The iterator increments
`yielded_frame_count` immediately before each yield. Its idempotence-rejecting
`close()` increments `close_count`, calculates
`script_frame_count - yielded_frame_count`, and raises if the result is not
zero. I1 propagates that close failure when the response would otherwise
succeed.

Thus a scripted correct final frame followed by a second frame fails
`AR-INVOKE` at close with one actual call. This proves only the fixed stub's
script exhaustion; it does not add trailing-frame detection to generic I1.
Success requires counters `1/1/1/1/0` in the order above.

## 6. I2 and I3 disposition

Preflight calls exact I2 and I3 `verify_contract_file` APIs. The run record
uses these exact values:

- `i2_disposition=contract-authenticated-no-import-route`;
- `i3_disposition=contract-authenticated-no-import-attempt`.

No I2 route, event, ledger, witness, or identifier and no I3 admission,
outcome, classification, completion, or destination authority may be created.
Attempting to do so is `AR-BOUNDARY`.

## 7. State and call-accounting machine

The success states are exact and ordered:

1. `NEW`
2. `PREFLIGHT_AUTHENTICATED`
3. `REQUEST_RECONSTRUCTED`
4. `OUTPUT_RESERVED`
5. `RUNNER_ENTERED`
6. `INVOKED_ONCE`
7. `RESPONSE_CAPTURED`
8. `ANSWER_VALIDATED`
9. `TEMP_RECORD_VERIFIED`
10. `COMPLETE`

Before `OUTPUT_RESERVED`, actual stub call count must be zero.
`OUTPUT_RESERVED -> RUNNER_ENTERED` occurs immediately before entering I1
`run_one_shot` and makes no call-count claim. The stub's first instruction is
the sole authority for actual call count. `RUNNER_ENTERED -> INVOKED_ONCE`
occurs only after I1 returns successfully and counters equal `1/1/1/1/0`.

If request validation fails inside I1 before stub entry, the observed call
count is zero. If stub entry or later iteration/close fails, it is one. Both
are `AR-INVOKE`, but the separately recorded observed count remains truthful.
No constructor is invoked after reservation because the immutable stub is
constructed and audited during preflight.

## 8. Record verification and atomic publication

The success record has the exact 36 fields and values in the interface map.
Its canonical bytes are 2,046 ASCII bytes and its SHA-256 is
`bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`.

The output root is newly created and empty. The controller:

1. exclusively creates `run-record.pending` in the final directory;
2. writes the canonical bytes, fsyncs, and closes it;
3. reopens and verifies exact bytes and SHA-256;
4. reaches `TEMP_RECORD_VERIFIED`;
5. calls one reviewed same-volume `atomic_no_replace_move` primitive from
   `run-record.pending` to `run-record.json`; and
6. treats successful atomic publication as the commit point and the transition
   to `COMPLETE`.

The primitive must fail if the final path exists and must leave either the
verified pending object or the final object, never a partial destination. Its
platform implementation and collision/race probes are future implementation
review inputs. Unsupported semantics fail preflight.

There is no fallible success check after publication. All byte/hash read-back
checks occur on the pending object. Before successful publication, every
failure closes descriptors and removes only the pending file. After successful
publication, the exact verified final file is the durable success evidence.
A failed run therefore cannot leave a final pass-looking record.

## 9. Unique failure classes and precedence

Exactly one primary class is assigned at the first failed ordered operation:

| Class | Exact domain |
|---|---|
| `AR-BOUNDARY` | denied path/capability or fabricated I2/I3 operation; overrides any otherwise simultaneous class |
| `AR-AUTH` | component, bundle, source, contract, request artifact, manifest, or grant authentication before runner entry |
| `AR-TRANSFORM` | authenticated I0 transform bytes differ from frozen package |
| `AR-RESERVE` | pending/final collision or initial exclusive pending creation failure |
| `AR-INVOKE` | any I1 `run_one_shot` exception, including strict JSON parse, stream, bounds, iterator, or close failure |
| `AR-RESPONSE` | I1 returned successfully but raw response hash/bytes differ from the fixed public answer |
| `AR-ANSWER` | I0 returns at least one answer-validation error |
| `AR-RECORD` | pending record serialization, write, fsync, close, read-back, hash, or atomic publication failure |
| `AR-DETERMINISM` | either completed repeat differs, a success record has a nondeterministic/unknown field, or retry count is not zero |

Denied access is the only override. Otherwise the earliest failed ordered
operation fixes the primary class. Cleanup failure is recorded separately as
`cleanup_status=failed`; it never changes an existing primary class. Cleanup
failure after an otherwise successful operation makes the primary class
`AR-RECORD`. No failure record is published at the success path.

## 10. Exact deterministic repeat

The verifier performs two independent executions in two fresh empty roots.
Each execution starts at `NEW`, constructs its own stub, has exactly one call
and zero retries, and publishes one exact final record. The second execution is
not a retry.

Both final record byte streams must equal the 2,046-byte frozen record and the
frozen SHA-256, not merely each other. Any difference is `AR-DETERMINISM`.
Temporary roots are verifier-owned and removed after the equality evidence is
captured.

## 11. Denied boundaries and maximum claim

Denied: F0 content, hidden oracle, provider/model/network/browser/MCP/tools,
executor/judge/scoring/condition map, keys/signatures/trust-root activation,
signer media/ledger/witness/VM/ACL, E0/S0 execution, central system, and
Project Brain.

This gate creates only revised public design documents. Maximum claim:

> The seven v0.1 independent-review findings have design-level repairs proposed
> for fresh independent review. No controller, rehearsal, S0 execution, model
> call, role isolation, or operational system has been implemented or tested.

## 12. Next gate

After this revision is committed and published, the exact next gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.2 INDEPENDENT REVIEW OPEN`
