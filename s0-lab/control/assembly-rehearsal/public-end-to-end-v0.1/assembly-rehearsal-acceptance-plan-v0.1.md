# S0 v0.14 public assembly rehearsal acceptance plan v0.1

- `status`: public design acceptance candidate
- `implementation_status`: not implemented
- `execution_status`: not executed
- `scope`: one fixed public-practice, model-free assembly controller

## 1. Acceptance principle

The later implementation is accepted only if an independent reviewer can
reconstruct the exact case, component pins, call graph, state machine, and
success record from the design package and then observe the same deterministic
result twice with a stub transport.

Component unit-test history is supporting evidence. It is not a substitute for
the composed rehearsal.

## 2. Required implementation inventory

The successor implementation gate may add only:

1. one small public assembly-controller package;
2. one exact public request artifact and its one-entry manifest;
3. one model-free exact-answer stub transport;
4. public unit and integration tests;
5. one verifier with an externally supplied implementation-manifest pin;
6. one verification report and implementation manifest; and
7. after execution is separately authorized, one canonical public run record.

It may not modify I0, I1, I2, I3, the public-practice bundle, SM0/SM1,
protocol files, or F0 files.

## 3. Static preflight checks

Before importing or executing candidate code, the verifier must check:

- exact implementation file set and lowercase SHA-256 manifest;
- no symlink, reparse-point, alternate-data-stream, or path escape in the
  candidate namespace;
- exact hashes for the I0-I3 implementation manifests;
- exact public bundle manifest, fixed case files, answer schema, I2 contract,
  and I3 contract;
- the request manifest has exactly one sorted, canonical row;
- the request artifact hash equals that row and the externally reviewed pin;
- imports contain no provider, network, browser, MCP, subprocess, key,
  signature, VM, ledger, executor, judge, scoring, F0, E0, S0, central-system,
  or Project Brain capability; and
- the controller exposes no case, block, profile, path, model, or retry option.

The verifier must use a snapshot or equivalent stable-byte execution scheme
and must rehash all authenticated inputs after execution.

## 4. Positive composed rehearsal

For each of two independent temporary roots, the verifier performs this exact
sequence:

1. authenticate all pins and public inputs;
2. call I2 and I3 public contract verification;
3. call I0 public-bundle verification;
4. call I0 P01 transformation and compare exact package bytes;
5. reconstruct and compare the exact request envelope;
6. create the I1 manifest grant and authenticate the request entry;
7. exclusively reserve the run-record path;
8. call I1 `run_one_shot` once with the exact public-answer stub;
9. compare the raw response with the fixed public response hash;
10. call I0 answer validation and require an empty error list;
11. serialize, write, fsync, close, and re-read the canonical run record; and
12. remove all temporary files other than the retained candidate record.

Each execution must report one transport call, zero retries, one response
frame, one final frame, zero answer errors, and zero denied-input accesses
within the instrumented allowlist.

The two run-record byte streams and hashes must be identical.

## 5. Required hostile mutations

Each mutation below is a separate test with its own expected failure class.
No later check may hide an earlier failure.

| Mutation | Required result |
|---|---|
| I0, I1, I2, or I3 implementation-manifest hash changed | `AR-AUTH`, zero calls |
| canonical, package, questions, answer, or schema byte changed | `AR-AUTH`, zero calls |
| I0 transform output differs from frozen package | `AR-TRANSFORM`, zero calls |
| request field missing, extra, reordered logically, duplicated, or changed | `AR-AUTH`, zero calls |
| request manifest missing, extra row, uppercase digest, or wrong path | `AR-AUTH`, zero calls |
| output path exists before run | `AR-RESERVE`, zero calls |
| transport attempts a second invocation | `AR-INVOKE`, fail |
| transport yields zero frames | `AR-INVOKE`, cleanup |
| transport yields a non-final stream | `AR-INVOKE`, cleanup |
| response ID changes mid-stream | `AR-INVOKE`, cleanup |
| frame count 257 or response size 8,193 bytes | `AR-INVOKE`, cleanup |
| bytes follow the final frame | `AR-INVOKE`, cleanup |
| iterator close fails | `AR-INVOKE`, no success record |
| response hash differs from the fixed public answer | `AR-RESPONSE`, cleanup |
| response is invalid JSON or not an object | `AR-INVOKE` or `AR-RESPONSE`, cleanup |
| I0 answer validation returns any error | `AR-ANSWER`, cleanup |
| record write, fsync, close, or read-back differs | `AR-RECORD`, no success claim |
| any F0, oracle, provider, model, network, tool, executor, judge, scoring, key, signer-media, ledger, E0, or S0 path is requested | `AR-BOUNDARY`, zero further work |
| I2 route/event or I3 admission/outcome is fabricated for this case | `AR-BOUNDARY`, fail |
| any timestamp, random value, host path, or username enters the record | deterministic-repeat failure |

## 6. State-machine invariants

The independent verifier must prove from tests and source that:

- only the nine states in the interface map exist;
- every successful transition advances exactly one state;
- invocation is unreachable before successful exclusive reservation;
- response validation is unreachable without exactly one invocation;
- record commit is unreachable with any answer error;
- `COMPLETE` is unreachable without durable close and read-back equality;
- no failure state can return to an earlier state; and
- no retry, resume, overwrite, append-to-existing, or partial-success path
  exists.

## 7. Boundary evidence

The verifier's exact allowlist may include only:

- the reviewed candidate namespace;
- the exact I0-I3 manifest-listed public implementation files needed for the
  imports;
- the exact public case files in the design;
- the answer schema;
- the exact I2/I3 public contracts; and
- the canonical text-artifact validator.

It must not list, open, search, or hash F0 content. F0 non-access is supported
by the controller's exact allowlist, static path/import audit, and an
instrumented file-open sentinel for the candidate process. This is bounded
test evidence, not an OS security or hostile-process isolation claim.

## 8. Resource limits

Per execution:

- controller process: 1;
- stub transport invocation: exactly 1;
- retries: 0;
- response frames: exactly 1 in the positive path;
- response bytes: the fixed 1,936-byte public answer;
- provider/model/network/tool calls: 0;
- persistent success records: 1;
- persistent incomplete records after failure: 0.

The implementation verifier must define a finite wall-clock timeout. A timeout
is failure, not grounds for retry.

## 9. Acceptance verdict

The independent implementation review may return only:

- `PASS-FOR-PUBLIC-REHEARSAL-EXECUTION-CONSIDERATION-ONLY`;
- `REVISE-AND-REVIEW`; or
- `INVALID-REVIEW`.

PASS requires every static, positive, hostile, state-machine, cleanup,
repeatability, exact-change-set, and input-stability check to pass. It does not
authorize provider/model use, F0 access, executor creation, S0 execution, main
integration, commit, or push.

## 10. Present result

No check in this plan has been executed under the current design gate. Every
expected result above is a future acceptance criterion, not current evidence.
