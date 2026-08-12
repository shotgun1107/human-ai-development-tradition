# S0 v0.14 public assembly rehearsal acceptance plan v0.3

- `status`: public design acceptance candidate
- `implementation_status`: not implemented
- `execution_status`: not executed
- `scope`: M-04 through M-07 closure and v0.2 non-regression

## 1. Future implementation scope

A later, separately opened implementation gate may add only the public
controller, exact request/manifest, exact stub, Windows publication adapter,
evidence consumer, tests, verifier, implementation manifest, design-package
manifest, report, and after a separate execution gate the two-object result.

It must not modify I0-I3, their manifests or contracts, public-practice data,
F0, an oracle, provider/model, executor, judge, signer, or S0 asset.

## 2. Pre-import authentication

Before importing candidate code, a fresh reviewer must:

1. authenticate the implementation manifest from an external lowercase pin;
2. authenticate the v0.3 design-package manifest and the fresh independent
   design-review artifact from external lowercase pins;
3. authenticate all I0-I3 manifests and required rows;
4. authenticate the public bundle manifest and all 90 entries;
5. authenticate the fixed case, answer schema, I2/I3 contracts, request
   manifest, and request;
6. reject extra, missing, symlink, reparse, alternate-stream, and path-escaping
   candidate inputs;
7. statically reject denied imports, paths, fallback publication primitives,
   retry paths, and replace/copy flags; and
8. freeze the complete receipt object, canonical bytes, byte length, and
   SHA-256 before execution.

Candidate execution begins only after every admitted byte is stable and
authenticated.

## 3. Platform preflight

The verifier must fail before output reservation unless it independently
proves all of the following:

- Windows version is 10 or 11;
- the output root is on a local NTFS volume;
- all four output paths resolve beneath one newly created empty root;
- source and destination volume serial numbers are equal;
- no output path is a symlink, junction, reparse point, or alternate stream;
- the imported Win32 function is `MoveFileExW` with correct argument and return
  types;
- both calls use numeric flags `0`;
- replace-existing, copy-allowed, fallback, and retry logic are absent; and
- the claim excludes power loss and directory-metadata durability.

Unsupported or ambiguous environments are `AR-AUTH/0` and cannot run.

## 4. Positive run

For each of two fresh output roots:

1. authenticate all inputs and the platform profile;
2. verify the four exact output names are absent;
3. exclusively create and retain the `run-record.pending` handle;
4. run the inherited I0/I1 public flow once;
5. require `STUB_INTEGRITY` counters `1/1/1/1/0`;
6. require the exact response and zero I0 answer errors;
7. run `DETERMINISM_AUDIT` before serialization;
8. produce and verify the exact 2,046-byte run record;
9. call `MoveFileExW(run-record.pending, run-record.json, 0)` once;
10. construct the receipt from the three external provenance pins and fixed
    values;
11. exclusively write and verify `publication-receipt.pending`;
12. call `MoveFileExW(publication-receipt.pending,
    publication-receipt.json, 0)` once; and
13. call the exact consumer and require one valid evidence pair.

The receipt move, not the record move, is the `COMPLETE` commit point. No
fallible success check is performed by the controller after that move. The
verifier's later consumer call evaluates retained evidence; it does not alter
the controller's committed state.

## 5. M-04 routing probes

| Mutation | Calls | Required class |
|---|---:|---|
| any of four names exists at initial reservation | 0 | `AR-RESERVE` |
| record final appears after reservation | 1 | `AR-RECORD`; preserve destination |
| receipt final appears after reservation | 1 | `AR-RECORD`; preserve destination |
| stub has no callable close | 1 | `AR-INVOKE` |
| close raises or close count is 0 or 2 | 1 | `AR-INVOKE` |
| any other stub counter differs | 1 | `AR-INVOKE` |
| unknown/missing/nondeterministic field or retry nonzero | 1 | `AR-DETERMINISM` |
| semantics pass but serialized bytes/length/hash differ | 1 | `AR-RECORD` |

Every probe records the exact rejecting operation and state. No mutation may
match two primary classes. Denied access remains the only override.

## 6. M-05 publication probes

The implementation review must exercise the real supported Windows/NTFS
primitive, not an in-memory substitute, for these bounded cases:

- same-volume source and absent destination succeeds once;
- existing destination fails without changing either source or destination;
- source missing fails;
- cross-volume, non-NTFS, reparse, alternate stream, network, and removable
  targets fail preflight;
- injected process termination before each call yields no valid evidence pair;
- termination after record move but before receipt move leaves no valid
  evidence pair;
- exact flags and call count are independently captured; and
- source contains no replace, copy/delete, retry, or fallback branch.

The tests may claim only process-interruption/API-failure semantics. They must
not claim power-loss durability, kernel-crash safety, or persistent directory
metadata ordering.

## 7. M-06 consumer and residue probes

The exact consumer must reject each of the following:

- either pending pathname;
- run record alone;
- receipt alone;
- copied pending bytes renamed to the final record path without a valid
  receipt;
- copied receipt bytes paired with a different output root or record;
- valid bytes at any noncanonical pathname;
- a pair with either pending file still present;
- a pair in a quarantined root;
- a pair with a link, reparse point, alternate stream, changed hash, changed
  binding, or reused output-root identity; and
- a final record left after receipt construction or publication failure.

Cleanup failure must leave the run classified by its first primary error and
set the root to `QUARANTINED-FAILED`. Cleanup status is secondary and cannot
manufacture success.

## 8. M-07 provenance probes

Before execution, independently mutate each receipt provenance field:

- assembly implementation-manifest hash;
- v0.3 design-package-manifest hash;
- independent design-review artifact hash;
- run-record hash and path;
- receipt path;
- all five stub counters;
- platform profile, primitive, and flags;
- rehearsal ID and publication outcome; and
- consumer ID.

Every single mutation must make the consumer reject. Placeholder, zero,
unknown, internally self-asserted, or non-external provenance pins must fail
preflight.

## 9. v0.2 non-regression

The reviewer must independently retain and verify:

- full-bundle manifest plus exactly 90 rows;
- fixed B2/P01 selection;
- request and request-manifest bytes/hashes;
- I1 grant identity;
- one-frame stub and generic-I1 disclaimer;
- truthful zero/one-call evidence;
- exact 36-field run record and hash;
- I2/I3 contract-only no-import dispositions;
- two fresh deterministic executions; and
- every denied boundary and nonclaim.

## 10. Required future evidence

A candidate implementation review must output:

- authenticated input and manifest table;
- platform/volume/primitive evidence;
- routing table with exact class and call count;
- all mutation results;
- frozen record and receipt bytes/hashes;
- consumer positive and negative results;
- two-run equality against external pins;
- proof that F0 and closed APIs remained unopened/unexecuted; and
- exact Git scope and post-test stability.

## 11. Verdict vocabulary

The fresh design review may return only:

- `PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `REVISE-AND-REVIEW`; or
- `INVALID-REVIEW`.

No check in this acceptance plan has been implemented or run under the current
design revision gate.
