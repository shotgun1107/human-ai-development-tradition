# S0 v0.14 public assembly rehearsal acceptance plan v0.2

- `status`: public revision acceptance candidate
- `implementation_status`: not implemented
- `execution_status`: not executed

## 1. Exact future implementation scope

The future bounded implementation may add only a public controller, the exact
request and manifest, the exact stub, tests, a verifier, manifests/report, and
after a separate execution gate the canonical record. It must not modify I0-I3
or create any F0, oracle, provider/model, executor, judge, signer, or S0 asset.

## 2. Pre-execution authentication

Before candidate import:

1. authenticate the implementation manifest from an external lowercase pin;
2. authenticate all four component manifests and their exact rows;
3. authenticate the public bundle manifest and exactly all 90 entries;
4. authenticate the fixed case, answer schema, and I2/I3 contracts;
5. authenticate the exact 135-byte request manifest and 7,917-byte request;
6. reconstruct the request and require SHA-256 `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2`;
7. reject extra, missing, symlink, reparse, alternate-stream, or path-escaping
   candidate inputs; and
8. statically reject denied imports, literal paths, configuration paths, and
   capabilities.

Candidate execution occurs only from authenticated stable bytes. Inputs are
rehashed after both runs.

## 3. Positive execution

In each of two fresh empty output roots:

1. verify I2 and I3 exact public contracts;
2. call I0 full public-bundle verification;
3. call I0 P01 transform and compare exact package bytes;
4. reconstruct the exact request and bind the exact I1 manifest grant;
5. construct and audit the one-frame immutable stub;
6. exclusively create `run-record.pending`;
7. enter I1 once and require stub counters `1/1/1/1/0`;
8. require exact fixed public response bytes/hash;
9. call I0 answer validation and require zero errors;
10. write, fsync, close, reopen, and verify the exact 2,046-byte pending record;
11. atomically move pending to absent `run-record.json` without replacement;
12. treat publication as `COMPLETE` with no later fallible success check.

Both final files must equal SHA-256
`bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e`.

## 4. Required mutations

| Mutation | Calls | Exact class |
|---|---:|---|
| any component, public-bundle, 90-row inventory, case, schema, contract, request, or grant mismatch | 0 | `AR-AUTH` |
| denied or unclassified path/capability requested, including fabricated I2/I3 operation | 0 or observed current count | `AR-BOUNDARY` |
| I0 transformed bytes differ | 0 | `AR-TRANSFORM` |
| pending or final name exists | 0 | `AR-RESERVE` |
| I1 rejects request before stub entry | 0 | `AR-INVOKE` |
| stub raises on entry, iteration, bounds, strict JSON, or close | 1 | `AR-INVOKE` |
| correct final frame followed by one scripted frame | 1 | `AR-INVOKE`; close reports one unconsumed frame |
| empty/nonfinal/mixed-ID/257-frame/8,193-byte stream | 1 | `AR-INVOKE` |
| I1 returns but bytes/hash differ | 1 | `AR-RESPONSE` |
| I0 answer errors nonempty | 1 | `AR-ANSWER` |
| pending write/fsync/close/read-back/hash or atomic publish fails | 1 | `AR-RECORD`; no final file |
| repeat bytes/hash differ, unknown/nondeterministic record field appears, or retry count is nonzero | 1 per completed execution | `AR-DETERMINISM` |

Strict invalid/non-object JSON is always `AR-INVOKE` because I1 parses before
return. Response mismatch is reachable only after a successful I1 return.

## 5. Atomic-publication probes

The implementation review must independently prove:

- pending and final are in one filesystem directory and volume;
- final collision causes no replacement and preserves the prior final bytes;
- failure before publish removes pending and leaves final absent;
- interruption/fault injection at each prepublication operation never creates
  final;
- successful publish leaves final equal to the already verified pending bytes
  and pending absent as one primitive outcome; and
- no check or cleanup operation capable of invalidating success occurs after
  publish.

If the host cannot supply these semantics, the implementation is unsupported
and cannot run.

## 6. State and accounting probes

Every transition is tested. `RUNNER_ENTERED` is set immediately before the I1
call. The stub counter, not controller state, records actual transport entry.
Tests must cover zero-call request rejection, one-call entry failure, one-call
missing final, one-call close failure, successful one call, attempted second
entry, and truthful counters in every diagnostic.

No failure may return to an earlier state, resume a partial run, overwrite an
existing output, or retry.

## 7. Boundary evidence

The candidate's public file-open sentinel allowlist is exactly:

- reviewed candidate and authenticated component payload paths needed to run;
- public bundle manifest plus all 90 authenticated rows;
- directory-metadata traversal only below the exact public bundle root, for
  I0 recursive discovery, without authorizing any additional file bytes;
- answer schema and I2/I3 contracts;
- exact request manifest and request; and
- verifier-owned temporary output roots.

It excludes all F0 families and otherwise unclassified paths. The sentinel
compares a normalized attempted path before open; it does not inspect a denied
directory. This is bounded same-process evidence only.

## 8. Verdict vocabulary

Independent implementation review may return only:

- `PASS-FOR-PUBLIC-REHEARSAL-EXECUTION-CONSIDERATION-ONLY`;
- `REVISE-AND-REVIEW`; or
- `INVALID-REVIEW`.

No test in this acceptance plan has been run under the design-revision gate.
