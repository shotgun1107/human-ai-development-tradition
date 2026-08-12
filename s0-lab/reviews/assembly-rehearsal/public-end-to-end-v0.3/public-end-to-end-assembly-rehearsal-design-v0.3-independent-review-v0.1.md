# S0 v0.14 public end-to-end assembly rehearsal design v0.3 independent review v0.1

- `review_role`: fresh public-only independent design reviewer
- `review_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.3 INDEPENDENT REVIEW OPEN`
- `review_head`: `24f1130c35aa3ddd4015f7ed0abae58c1eae8cc1`
- `review_tree`: `7f089ba0ec0f57c58326f776534c33fbf67d4b9d`
- `review_kind`: design review only; no implementation or rehearsal execution
- `F0_content_access`: none
- `verdict`: `REVISE-AND-REVIEW`

## 1. Verdict

`REVISE-AND-REVIEW`

The v0.3 proposal closes M-04 and M-07 at proposal-text level and preserves
the reviewed v0.2 public flow. Two major findings remain. M-05 is not closed
because the purportedly exact Windows primitive profile never freezes the
foreign-function signature or calling convention. M-06 is not closed because
the consumer authenticates final names and frozen bytes but has no independent
binding to the two successful `MoveFileExW` events: copying the exact pending
objects to the two final names and removing the pending names produces the
same accepted predicate as the specified publication sequence.

Finding counts are: zero blocking, two major, and zero minor.

This is only a public design-review result. It does not implement or validate
the controller, Windows adapter, receipt, consumer, verifier, rehearsal,
platform behavior, provider/model use, F0 isolation, S0/E0, a central system,
Project Brain, operational safety, economic value, or model-to-model transfer.

## 2. Authenticated basis and boundary

CONTROL supplied an external 166-row public-input manifest. Before substantive
reading, the review authenticated its SHA-256 as
`f2398240266c24dfdfa6a252f47d405b10d2d26699ce11bbf9737c740bca5645`,
required exactly 166 canonical rows and 166 unique paths, and found zero
missing files, zero content-hash mismatches, zero escaping paths, and zero F0
family rows. The initial worktree was clean.

Git identity matched the external pins:

| Check | Authenticated value | Result |
|---|---|---|
| branch | `codex/s0-public-assembly-rehearsal-design-v03-review` | PASS |
| HEAD | `24f1130c35aa3ddd4015f7ed0abae58c1eae8cc1` | PASS |
| tree | `7f089ba0ec0f57c58326f776534c33fbf67d4b9d` | PASS |
| sole parent | `001f4f5303f918e76d5682ed2388e552e8270eee` | PASS |
| parent tree | `99f50df4ed0e0097fdd122062e208b41870854f7` | PASS |

The root policy and authenticated v0.3 independent-review brief were read in
full before the other substantive inputs. The canonical validator's
`-SelfTest` passed before reliance. All 14 admitted Markdown/sidecar pairs and
all three admitted JSON/replacement-sidecar pairs passed their applicable
UTF-8, BOM, final-LF, trailing-whitespace, JSON syntax, canonical sidecar
record, and content-hash checks.

The authenticated public-bundle manifest contains exactly 90 canonical unique
rows. Every row was admitted by the external manifest and matched its hash.
The v0.3 design-package manifest contains exactly five canonical unique rows;
every row was admitted and matched. The four authenticated implementation
manifests and the admitted API source rows were used only for the named I0,
I1, I2, and I3 interface checks.

The two future request artifacts are absent at this design-only commit, as the
review brief states. They were not created. Their logical bytes were
reconstructed in memory from authenticated public package/question bytes and
the frozen canonicalization rule.

No F0 content or filename was opened, searched, enumerated, quoted, hashed, or
used. No repository-wide search, provider/model/network/web call, controller
execution, platform probe, fixture, hidden oracle, executor, judge, scoring
asset, E0, or S0 run occurred.

## 3. Effective v0.2 plus v0.3 composition

### 3.1 Retained v0.2 authority

The effective design retains the fixed `BLK-PRACTICE0002/P01` case, the
authenticated 90-row public bundle, the exact I1 manifest grant, the
candidate-owned eager one-frame stub, the generic-I1 first-final disclaimer,
I2/I3 contract-only no-import dispositions, the ten-state flow through
`TEMP_RECORD_VERIFIED`, the exact 36-field run record, two fresh deterministic
executions, and all denied boundaries and nonclaims.

Independent in-memory reconstruction produced:

| Object | Bytes/fields | SHA-256 | Result |
|---|---:|---|---|
| request | 7,917 bytes | `990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2` | exact match |
| one-row request manifest | 135 bytes | `872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7` | exact match |
| run record | 36 fields / 2,046 bytes | `bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e` | exact match |

### 3.2 v0.3 replacements

The successor replaces only four areas:

1. It reserves four exact names, distinguishes initial collisions from later
   races, adds `STUB_INTEGRITY`, and orders semantic determinism before byte
   expectation and I/O.
2. It limits publication to Windows 10/11, one local NTFS volume, and direct
   `MoveFileExW` with numeric flags `0`, with no replace, copy, fallback, or
   retry path.
3. It changes success evidence from one record to an exact final record and
   receipt pair, requires both pending names absent, and introduces
   `QUARANTINED-FAILED` residue handling.
4. It places the implementation-manifest, design-package-manifest, fresh
   design-review, all five counters, primitive, paths, and publication values
   in a future pre-execution-frozen receipt.

## 4. M-04 disposition: closed

The failure machine assigns one primary class and truthful observed call count
to the required mutations:

| Mutation or first failed operation | Class | Calls |
|---|---|---:|
| any one of the four names exists during initial reservation | `AR-RESERVE` | 0 |
| either final destination appears after reservation | `AR-RECORD` | 1 |
| request rejected inside I1 before stub entry | `AR-INVOKE` | 0 |
| missing/non-callable close, close exception, close count 0 or 2, or another counter mismatch | `AR-INVOKE` | 1 |
| response differs after successful I1 and integrity | `AR-RESPONSE` | 1 |
| answer errors are nonempty | `AR-ANSWER` | 1 |
| unknown/missing/nondeterministic/noncanonical record value or retry nonzero | `AR-DETERMINISM` | 1 |
| semantic audit passes but serialization, exact-byte, hash, write, close, read-back, receipt, or rename fails | `AR-RECORD` | 1 |
| denied access simultaneous with any other failure | `AR-BOUNDARY` | observed |

`STUB_INTEGRITY` is one post-I1, pre-`INVOKED_ONCE` operation requiring all
five counters `1/1/1/1/0`. Determinism audit precedes serialization and byte
expectation, so the same field mutation cannot also become `AR-RECORD`.
Denied access is the only override; otherwise the earliest ordered failure is
primary and cleanup status is secondary. M-04 is closed at design level.

## 5. M-05 disposition: major finding

### M-05A - The foreign-function signature is not frozen

**Facts.** The package fixes Windows 10 or 11, local NTFS, same-volume serial
identity, direct `MoveFileExW`, numeric flags `0`, nonzero return for success,
captured Win32 error on failure, and prohibitions on replace, copy, fallback,
and retry. It explicitly excludes power loss, storage-controller loss, kernel
failure, and directory-metadata durability. Unsupported environments fail
`AR-AUTH/0` before reservation, and future review must exercise the real
primitive rather than a mock.

The package does not state the exact imported function signature: parameter
types, return type, and Windows calling convention are absent. The acceptance
plan merely requires a future reviewer to decide that the types are
"correct." That is not an externally frozen signature and permits more than
one implementation interpretation at the design-to-implementation boundary.

**Inference.** A misdeclared foreign function can truncate or misinterpret a
pointer, return value, or flags while still appearing to call the named API.
The design therefore does not yet meet the brief's exact signature requirement
for a bounded implementation.

**Required revision.** Freeze the exact `MoveFileExW` ABI declaration,
including both wide-string parameter types, the numeric flag parameter type,
the Boolean return type, and the applicable Windows calling convention. Make
future source review and real-primitive probes compare against that declaration
rather than an undefined notion of correctness.

## 6. M-06 disposition: major finding

### M-06A - Exact copied objects can satisfy the consumer without publication-event provenance

**Facts.** The consumer receives an authenticated output-root identity and
checks exact final names, absence of both pending names, regular non-reparse
objects, no accepted alias/alternate stream, frozen record and receipt bytes,
all receipt bindings, quarantine state, and one-time consumption. The receipt's
`publication_outcome` is a fixed string constructed by the same controller.
No receipt field binds independently observed results from the two
`MoveFileExW` calls, and the consumer accepts no external authenticated
publication-event evidence.

Consider this hostile presentation after exact pending objects have been
constructed: copy `run-record.pending` to `run-record.json`, copy
`publication-receipt.pending` to `publication-receipt.json`, then remove both
pending names. The two finals now have the exact frozen bytes and bindings in
the exact authenticated root. They are regular non-reparse files, no pending
name remains, the root need not be marked quarantined, and it need not have
been consumed before. Every stated consumer predicate passes even though
neither required publication move occurred.

**Inference.** Final pathname plus self-described frozen bytes proves the
presentation, not the required record-intermediate/receipt-commit event
sequence. The design expressly requires copied pending bytes at a final
pathname to be rejected, but its consumer cannot distinguish this hostile
pair from a valid pair. This can create accepted success evidence and is a
major evidence-semantics defect.

**Required revision.** Add a non-self-asserted, independently authenticated
binding that lets the consumer distinguish the two successful publication
events and their order from copied final bytes, or narrow the success claim
and hostile requirement so it does not claim that distinction. The revised
consumer tests must present copied exact record and receipt pending bytes
together at both final names, with pending names absent, and require rejection.

The other M-06 presentations are unambiguous: either final alone, either
pending name, wrong root/name, mismatched hashes or bindings, pending residue,
a quarantined root, and repeat consumption are all `not-success`. Cleanup
failure retains the first primary class and marks the root
`QUARANTINED-FAILED`. These rules do not repair the exact copied-pair case.

## 7. M-07 disposition: closed subject to M-06

The 18 receipt fields have explicit fixed or future-external authority:

| Authority | Fields |
|---|---|
| future external lowercase SHA-256 pins | `assembly_implementation_manifest_sha256`, `design_package_manifest_sha256`, `design_independent_review_sha256` |
| fixed record bindings | `record_path`, `record_sha256`, `receipt_path` |
| fixed stub counters | transport calls, script frames, yielded frames, close count, unconsumed-on-close = `1/1/1/1/0` |
| fixed platform/publication values | platform profile ID, `MoveFileExW`, flags `0`, publication outcome |
| fixed identity values | rehearsal ID, schema ID, consumer ID |

The future implementation gate must externally pin all three provenance
hashes and freeze the complete canonical receipt bytes, byte length, and
SHA-256 before execution. Placeholder, zero, unknown, missing, or internally
self-selected provenance hashes fail preflight. Single-field mutation probes
must make the consumer reject. This closes M-07's field-completeness and
pre-execution-freeze concern. M-06A separately shows that the fixed
publication-outcome value does not prove the publication event it names.

## 8. Hostile traces and non-regression

| Hostile case | Required result | Review disposition |
|---|---|---|
| interruption before record move | no valid pair | closed |
| interruption after record move and before receipt move | record alone; not-success | closed |
| interruption after receipt move | committed exact pair | closed within the declared process model |
| destination collision at initial check/create | `AR-RESERVE/0` | closed |
| destination appears after reservation | `AR-RECORD/1`, preserve other object | closed |
| source disappears at either move | `AR-RECORD/1`, no valid pair | closed |
| cross-volume, unsupported filesystem, network/removable/reparse/ADS | `AR-AUTH/0` before reservation | closed |
| receipt construction, write, read-back, byte/hash mismatch | `AR-RECORD/1` | closed |
| cleanup failure | retain primary, quarantine root | closed at rule level |
| wrong provenance, counter, path, primitive, flags, ID, or hash | preflight or consumer rejection | closed |
| copied exact pending record and receipt to both final names | not-success | open: M-06A |
| real primitive imported with an ABI variant | reject before execution | open: M-05A |

The authenticated 90-row bundle boundary, fixed B2/P01 selection, reconstructed
request/manifest/grant, generic-I1 disclaimer, zero/one-call accounting,
36-field record bytes/hash, I2/I3 no-import dispositions, deterministic repeat,
and denied boundaries are retained without detected regression. I0-I3 remain
unchanged. No raw response bytes, controller return value, or single final
object substitutes for consumer acceptance.

## 9. Findings

| ID | Severity | Summary |
|---|---|---|
| M-05A | major | Exact Windows foreign-function signature and calling convention are not frozen. |
| M-06A | major | An exact copied record/receipt pair can satisfy every stated consumer predicate without either required publication move. |

There are zero blocking findings and zero minor findings.

## 10. Evidence limits and maximum claim

Facts above are authenticated document/source observations or exact in-memory
byte reconstructions. Findings and closure decisions are review inferences.
No platform behavior, FFI binding, rename atomicity, cleanup, receipt, consumer,
controller, verifier, or rehearsal was implemented or executed.

Maximum claim: the authenticated v0.3 public package closes M-04 and M-07 at
design level and preserves the v0.2 public flow, but it is not ready for public
implementation consideration because the exact Windows ABI and copied-pair
consumer semantics remain incomplete.

## 11. Exact next gate

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN`

That gate may revise only the public design package to close M-05A and M-06A
and return a replacement-extension successor to a fresh public-only review. It
does not authorize implementation, execution, provider/model use, F0 access,
oracle/executor/judge/scoring work, S0/E0, commit, push, PR, release, or main
integration.
