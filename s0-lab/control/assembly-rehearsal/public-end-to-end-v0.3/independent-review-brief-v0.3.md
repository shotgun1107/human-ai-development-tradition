# S0 v0.14 public assembly rehearsal design v0.3 independent review brief

## 1. Reviewer and boundary

Use a fresh public-only reviewer that did not author or advise on v0.3. The
reviewer must not inherit another v0.3 review conclusion or use a subagent.

Do not implement or execute the controller, Windows adapter, receipt,
consumer, verifier, or rehearsal. Do not access F0 content, create an oracle,
executor, judge, or scoring asset, or call a provider/model/network service.

This is a public document/source review only. Worktree separation protects
edits, not secrets.

## 2. Maximum inputs

CONTROL must externally supply exact paths and SHA-256 values. The maximum
substantive set is:

1. root `AGENTS.md`;
2. the I0-I3 readiness audit and sidecar;
3. the complete v0.1 design package, official review, and sidecars;
4. the complete v0.2 design package, official review, and sidecars;
5. the five v0.3 candidate artifacts, their sidecars, and the externally
   pinned `design-package-files.sha256` manifest;
6. all four authenticated implementation manifests and only their rows needed
   for the named I0/I1/I2/I3 APIs;
7. the authenticated public-bundle manifest and exactly its 90 entries;
8. the fixed case inputs, answer schema, I2/I3 public contracts, exact request,
   and one-row request manifest; and
9. the canonical public text validator.

No repository-wide search, F0 path content, unrelated implementation source,
prior advisory output, or unlisted file is permitted. Authenticate every
supplied byte before substantive reliance. Any baseline, hash, allowlist,
validator, or independence failure yields `INVALID-REVIEW`.

## 3. Required reconstruction

Without treating the author response as an answer key, reconstruct:

1. the exact v0.2 rules retained by v0.3 and the replacement map;
2. the initial four-name reservation and initial-versus-race collision split;
3. the post-I1 `STUB_INTEGRITY` operation and all five counters;
4. determinism-audit, serialization, byte expectation, and I/O ordering;
5. the exact Windows 10/11 local-NTFS `MoveFileExW(flags=0)` profile and claim
   limit;
6. the record-intermediate then receipt-commit publication sequence;
7. every receipt field, its fixed or external authority, and the future
   pre-execution freeze requirements;
8. the exact two-object consumer and quarantine rules;
9. every failure route, state, call count, and precedence; and
10. all inherited public-case, I0/I1, run-record, I2/I3, F0, and closed-gate
    invariants.

## 4. M-04 closure tests

Pass only if each mutation maps to one class and call count:

- each of four initial-name collisions;
- each final destination appearing after reservation;
- missing/non-callable close, close exception, close count 0 or 2, and every
  other counter mismatch;
- unknown, missing, changed, nondeterministic, or retry-bearing record fields;
- semantic success followed by serialization, exact-byte, hash, write,
  read-back, or rename failure; and
- simultaneous denied access plus another failure.

The review must prove `AR-BOUNDARY` is the only override, initial collisions
are `AR-RESERVE/0`, races are `AR-RECORD/1`, stub-integrity failures are
`AR-INVOKE`, and determinism cannot also become `AR-RECORD`.

## 5. M-05 closure tests

Determine whether the proposed profile is precise enough for a bounded future
implementation. Require one exact OS/filesystem set, one primitive/signature,
numeric flags, same-volume proof, no-replace behavior, error result, and
prohibition of copy/delete/fallback/retry.

Reject any text that implies power-loss durability, kernel-crash safety, or
directory-metadata persistence. Confirm that unsupported environments fail
before reservation and that later implementation review must exercise the
real primitive rather than a mock.

## 6. M-06 closure tests

Trace these evidence presentations:

- valid record and valid receipt at exact paths;
- either object alone;
- either pending pathname;
- copied pending bytes at a final pathname;
- correct bytes under a different root or name;
- a mismatched pair;
- either pending object retained beside finals;
- cleanup failure and a quarantined root; and
- repeat consumption of one output-root identity.

Only the exact final pair with both pending names absent and every binding
valid may pass. No raw byte stream or controller return value may substitute
for consumer acceptance.

## 7. M-07 closure tests

For every receipt field, identify whether its authority is a fixed v0.3 value
or a future external pin. Confirm explicit bindings for:

- assembly implementation manifest;
- v0.3 design-package manifest;
- fresh independent design-review artifact;
- exact run-record hash/path and receipt path;
- all five stub counters;
- platform profile, primitive, and flags;
- rehearsal ID, publication outcome, and consumer ID.

Require future implementation freeze of the actual external hashes and exact
receipt bytes/length/hash before execution. Self-asserted or placeholder
provenance must fail.

## 8. Non-regression and hostile cases

Independently retain v0.2's authenticated 90-row bundle boundary, fixed case,
request/manifest/grant, generic-I1 disclaimer, zero/one-call accounting,
36-field run-record bytes/hash, I2/I3 no-import dispositions, deterministic
repeat, and denied boundaries.

At minimum tabletop process interruption before and after each rename,
destination collision at every timing, source disappearance, cross-volume and
unsupported filesystem, receipt construction/write mismatch, cleanup failure,
wrong provenance, wrong counters, wrong paths, and copied residue.

Agreement with prose is not evidence. An unhandled or multiply interpreted
case is a finding.

## 9. Findings and verdict

- `blocking`: a defect can create accepted success evidence, cross a denied
  boundary, or make independent review impossible.
- `major`: required routing, platform, evidence, provenance, or non-regression
  semantics remain incomplete or contradictory.
- `minor`: bounded exactness defect that cannot grant success or authority.

Return exactly one:

- `PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY` when findings are zero;
- `REVISE-AND-REVIEW` when any finding exists; or
- `INVALID-REVIEW` when integrity, boundary, or independence fails.

No verdict automatically opens implementation, execution, provider/model,
F0, S0/E0, commit, push, PR, or main integration.

## 10. Required output

Write exactly one public review Markdown and same-basename
replacement-extension sidecar under a CONTROL-authorized v0.3 review path.
Include authenticated basis, effective composition, all four finding
dispositions, hostile traces, non-regression, findings, verdict, evidence
limits, maximum claim, and exact next gate.

Before relying on the canonical validator, run its SelfTest. After writing,
validate the output pair, rehash every admitted input, confirm unchanged Git
identity, and require the final status to contain only the two authorized
review outputs.
