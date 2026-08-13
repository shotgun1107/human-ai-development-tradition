# S0 v0.14 public end-to-end assembly rehearsal design v0.4 independent rereview v0.1

- review_role: fresh public-only independent design rereviewer
- review_gate: S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.4 INDEPENDENT REREVIEW OPEN
- review_head: d85cb891a598e54c581c80ebc6c677dd779ceefa
- review_tree: da8147a5af7b9b73ee606817a5ffbdda5d4afec1
- review_kind: design rereview only; no implementation or rehearsal execution
- F0_content_access: none
- verdict: REVISE-AND-REVIEW

## 1. Verdict

The v0.4 package freezes one literal MoveFileExW ABI and repairs the core
copied-pair defect by requiring a verifier-owned, same-process, identity-bound
two-event witness. It also retains the v0.3 M-04 routing rules and the v0.2
public flow.

It is not ready for public implementation consideration. Two major findings
and one minor finding remain. First, the inherited frozen receipt still names
the v0.3 consumer and platform profile and does not unambiguously retarget its
design/review provenance to the effective v0.4 package. Second, the retained
frozen run record still calls its result a rehearsal pass even though v0.4
requires retained files to state that controller completion is not PASS and
that post-process files are offline-not-success. Finally, the required
23-field event does not freeze the positive-call meaning of
last_error_uint32.

This is only a public design-rereview result. It does not implement or validate
the ABI, observer, witness, consumer, controller, rehearsal, Windows behavior,
provider/model use, F0 isolation, S0/E0, a central system, Project Brain,
operational safety, economic value, or model-to-model transfer.

## 2. Authenticated basis and boundary

Before substantive reading, the externally supplied 179-row maximum manifest
was parsed as 179 unique public paths. All paths existed, all SHA-256 values
matched, and zero rows entered any of the three F0 default-deny families. The
initial worktree was clean.

Git identity matched the external pins:

| Check | Authenticated value | Result |
|---|---|---|
| branch | codex/s0-public-assembly-rehearsal-design-v04-rereview | PASS |
| HEAD | d85cb891a598e54c581c80ebc6c677dd779ceefa | PASS |
| tree | da8147a5af7b9b73ee606817a5ffbdda5d4afec1 | PASS |
| sole parent | 3705571a1762f4e9d37738624b2c9f7b27afc9d6 | PASS |
| parent tree | 458080dcceffb5f6010e229c98afad9072678343 | PASS |
| parent-to-candidate scope | exact 11 authenticated v0.4 package files | PASS |

The root policy and authenticated v0.4 rereview brief were read in full before
the other substantive inputs. The canonical validator SelfTest passed. All 19
admitted Markdown/sidecar pairs passed the canonical validator. All four
admitted JSON/replacement-sidecar pairs separately passed file presence,
strict UTF-8, BOM absence, final LF, trailing-whitespace absence, JSON syntax,
sidecar presence and text checks, canonical sidecar record, and content hash.

The authenticated v0.4 design-package manifest contains exactly five unique
rows and all five content hashes match. The authenticated public-bundle
manifest contains exactly 90 unique rows and all 90 content hashes match. The
four authenticated implementation manifests and named I0-I3 API sources were
used only for the bounded public interface checks.

Independent in-memory reconstruction produced:

| Object | Bytes/fields | SHA-256 | Result |
|---|---:|---|---|
| request | 7,917 bytes | 990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2 | exact match |
| one-row request manifest | 135 bytes | 872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7 | exact match |
| run record | 36 fields / 2,046 bytes | bc13615933766fd84435fe4faf2d05b37a495b160f8529c699c73aec7784650e | exact match |

No F0 content or filename was opened, searched, enumerated, quoted, or used.
No repository-wide search, network, provider/model call, controller execution,
platform probe, implementation, fixture, hidden oracle, executor, judge,
scoring asset, E0, or S0 run occurred. The author response was not used as an
answer key; it was read only after independent reconstruction and hostile-case
analysis identified the findings below.

## 3. Effective composition

The effective candidate is v0.3 plus only the v0.4 replacements.

Retained from v0.3 and v0.2 are the fixed 90-row public bundle, B2/P01 case,
request/grant/stub, generic-I1 first-final disclaimer, I2/I3 contract-only
no-import dispositions, ten-state flow through TEMP_RECORD_VERIFIED, exact
36-field record, two fresh deterministic executions, four output names,
initial-versus-race routing, STUB_INTEGRITY with counters 1/1/1/1/0,
determinism-before-record validation, receipt fields and external provenance,
quarantine semantics, unique failure classes, denied-boundary override, and
all nonclaims.

The v0.4 replacements are:

1. one literal 64-bit Windows MoveFileExW declaration and ctypes binding;
2. withdrawal of files as standalone success evidence;
3. a verifier-parent observer, child IPC boundary, private run capability,
   two immutable move events, and one private witness;
4. a same-process live consumer with current-file identity continuity and
   one-use witness consumption; and
5. separation of candidate-controller COMPLETE from rehearsal PASS.

The retained receipt and run-record definitions are precisely where the two
major non-regressions below conflict with the replacements.

## 4. M-05A disposition: closed at design-text level

The normative declaration is exact:

    BOOL WINAPI MoveFileExW(
        LPCWSTR lpExistingFileName,
        LPCWSTR lpNewFileName,
        DWORD   dwFlags
    );

The supported process is 64-bit CPython 3.12.x on 64-bit Windows 10 or 11,
with one authenticated local-NTFS root on one volume. The binding fixes system
kernel32.dll, export MoveFileExW, Microsoft x64 WINAPI, loader
ctypes.WinDLL("kernel32", use_last_error=True), argument types
[ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32], and return type
ctypes.c_int32.

Both paths must be absolute extended-length Win32 paths derived from the
authenticated canonical paths. Embedded NUL rejects. Flags are unsigned
32-bit numeric zero. ctypes.set_last_error(0) is immediately before the
single call. Any signed 32-bit nonzero return is success; after zero,
ctypes.get_last_error() is the immediate next operation and its unsigned
32-bit value is diagnostic only.

Every alternate architecture, OS, filesystem, DLL/export, loader, convention,
parameter/return type, path form, NUL case, flag, fallback, or retry fails
AR-AUTH/0 before reservation. A real supported-profile API failure is
AR-RECORD/1. No mock result can satisfy the real-profile row. These rules
close the v0.3 M-05A signature defect at public design-text level, subject to
the positive-event field exactness finding N-01.

## 5. M-06A disposition: core copied-pair predicate repaired

The verifier parent, not the candidate child, owns the observer, exact FFI
function, private run capability, trace, witness, and live consumer. The child
receives only its anonymous-pipe endpoint and may send exactly
PUBLISH_RECORD plus LF, then PUBLISH_RECEIPT plus LF. Extra, partial,
duplicate, reordered, non-ASCII, or post-terminal bytes reject.

The two exact observer operations are:

1. run-record.pending to run-record.json; and
2. publication-receipt.pending to publication-receipt.json.

For each, the observer authenticates root and paths, captures source identity
(volume_serial_number, file_index_high, file_index_low), length, and SHA-256,
requires the destination absent, performs the one flags-zero call, requires
source absence after success, and requires the destination identity, length,
and hash to match. The immutable event contains all 23 interface-map fields.

Only two exact ordered successful events bound to the same observer, child,
capability, endpoint, and root may issue the private process-local witness.
The live consumer additionally requires the exact witness and trace, current
final-file identity/hash continuity, absent pending names, valid receipt and
external bindings, nonquarantined root, and an unused witness. Successful
consumption is one-use. The witness is unavailable after process restart.

This rejects copied exact final bytes without a witness and distinguishes a
later byte-for-byte copy replacement by changed file identity. It repairs the
specific v0.3 M-06A false predicate. Finding M-06B below concerns the retained
files' contradictory claims, not the witness predicate itself.

## 6. Mandatory hostile table-tops

| Hostile case | Rejecting authority and result | Disposition |
|---|---|---|
| exact pending bytes copied to both finals; pending names removed; no witness | live consumer exact-witness predicate; not-success and overall AR-RECORD/1 | closed |
| fabricated, copied, serialized, or repr-derived witness-like value | private type plus exact object identity; reject | closed |
| witness from another observer, capability, child, endpoint, root, or files | identity, binding, and current-file predicates; reject | closed |
| zero, one, reordered, duplicated, mismatched, or failed move events | witness issuer exact two-event predicate; no witness | closed |
| real ordered events and exact private witness with matching current files | same-process live consumer; sole positive row | closed at design level |
| replay of an already consumed witness | atomic one-use state; reject | closed |
| exact final bytes replaced by a copy after valid moves | current file identity differs from event destination; reject | closed |
| verifier process restart or offline files | process-local witness unavailable; offline-not-success | closed as authority rule |
| controller reaches COMPLETE but consumer rejects or is not called | controller state is not PASS; overall AR-RECORD/1 | closed as control rule |
| inherited receipt names old consumer/profile while live authority uses new IDs | no v0.4 equality predicate; M-07A | open |
| retained record labels itself rehearsal pass after process exit | conflicts with required file claim; M-06B | open |

## 7. M-04 and public-flow non-regression

M-04's ordered routing remains unique at design level:

| First failed operation | Calls | Primary class |
|---|---:|---|
| any initial four-name collision or reservation failure | 0 | AR-RESERVE |
| a destination appears after reservation or either publication fails | 1 | AR-RECORD |
| request rejects inside I1 before stub entry | 0 | AR-INVOKE |
| stub entry, stream, close, or any 1/1/1/1/0 integrity mismatch | 1 | AR-INVOKE |
| successful I1 but wrong response | 1 | AR-RESPONSE |
| nonempty answer-validation errors | 1 | AR-ANSWER |
| unknown, missing, nondeterministic, noncanonical field, or retry nonzero | 1 | AR-DETERMINISM |
| post-semantic serialization, I/O, receipt, observer, witness, or consumer failure | 1 | AR-RECORD |
| denied access simultaneous with another failure | observed | AR-BOUNDARY override |

The authenticated bundle/case/request/grant/stub/record, exact five counters,
two independent deterministic executions, I2/I3 no-import dispositions,
quarantine rule, and denied boundaries remain present. No raw response,
controller return, file, or pair is authorized to substitute for live-consumer
acceptance. M-04 remains closed. M-07 is reopened by the stale binding defect.

## 8. Findings

### M-07A - The retained receipt binds stale authority identities

Severity: major.

Facts. Effective composition retains the exact v0.3 receipt schema and
bindings. Its frozen evidence_consumer_id is
S0-PUBLIC-ASSEMBLY-EVIDENCE-CONSUMER-1, while v0.4's sole authorized consumer
is S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2. Its frozen platform_profile_id is
S0-WIN-NTFS-MOVEFILEEX-NOREPLACE-PROCESS-1, while every accepted v0.4 event
must name S0-WIN64-NTFS-MOVEFILEEXW-CTYPES-ABI-2. The v0.4 package requires
the live consumer only to validate the v0.3 receipt bindings; it does not add
an equality rule tying those retained fields to the new authorities.

The retained design and independent-review hash fields were defined to bind
the v0.3 design package and its approving review. V0.4 does not explicitly
retarget them to the exact v0.4 five-row design-package manifest and this
rereview artifact. Calling the provenance rules unchanged leaves both old and
new interpretations available.

Inference. A future implementation can satisfy the literal v0.3 receipt while
the receipt attests an obsolete consumer and platform profile. The live trace
separately checks the new ABI and witness, so this does not by itself
manufacture a witness, but M-07's externally frozen implementation, design,
review, consumer, and profile provenance is incomplete and inconsistent.

Required revision. Define a v0.4 successor receipt and freeze its exact schema
semantics. It must bind the live-consumer-2 ID, ABI-profile-2 ID, exact v0.4
design-package-manifest external pin, and the fresh rereview external pin.
Require single-field mutations and any old-ID or old-package pin to reject,
then freeze canonical receipt bytes, length, and SHA-256 before execution.

### M-06B - Retained file bytes still assert rehearsal PASS

Severity: major.

Facts. V0.4 retains the exact 36-field, 2,046-byte run record. Its frozen
result value is public-assembly-rehearsal-pass-not-s0 and its state is
COMPLETE. V0.4's acceptance plan simultaneously requires the candidate report
and retained files to say that controller COMPLETE is not rehearsal PASS, only
live-consumer acceptance is PASS, and post-process files are
offline-not-success. It declares any offline/pass-from-files documentation
statement or code branch a major regression. No v0.4 replacement changes the
record bytes or redefines that pass-valued field as controller-local only.

Inference. The authorized decision API remains witness-gated, but the retained
output directly contradicts the narrowed claim and cannot satisfy the
acceptance plan's own retained-file requirement. After process exit, the
frozen file says pass while its governing design says it is not success.

Required revision. Version the record/receipt claim fields or otherwise freeze
unambiguous bytes that describe only candidate-controller completion, state
that live-consumer acceptance is required for rehearsal PASS, and mark
post-process artifacts offline-not-success-diagnostic-only. Reconstruct and
externally pin the revised record and receipt bytes and hashes.

### N-01 - Positive-event last-error semantics are not frozen

Severity: minor.

Facts. Every event must contain last_error_uint32. The ABI rule clears last
error immediately before the call and captures it immediately only after a
zero return. A positive witness requires nonzero returns, but the package does
not state whether the positive event records constant zero, calls
get_last_error() after successful return, or uses another representation.

Inference. This does not change the nonzero success predicate or let a failed
call pass, but it leaves more than one definition of the exact 23-field
positive event.

Required revision. Freeze the positive-call value and acquisition rule for
last_error_uint32, while retaining immediate capture as the next operation
after a zero return.

Finding counts are zero blocking, two major, and one minor.

## 9. Evidence limits and maximum claim

Facts above are authenticated document/source observations or exact in-memory
byte reconstructions. Closure and finding dispositions are review inferences.
No FFI call, platform behavior, file identity, observer, capability, witness,
consumer, controller, receipt, cleanup, or rehearsal was implemented or
executed.

Maximum claim: v0.4 closes the literal ABI-signature defect and repairs the
core copied-pair authorization predicate at public design-text level. It is
not ready for public implementation consideration because its inherited
receipt authority identities and retained pass-valued output contradict the
new live-consumer design, and one positive event field remains underspecified.

## 10. Exact next gate

S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN REVISION OPEN

That gate may revise only the public design package to resolve M-07A, M-06B,
and N-01 and return a replacement-extension successor to a fresh public-only
review. It does not authorize implementation, platform execution, rehearsal,
provider/model use, F0 access, oracle/executor/judge/scoring work, S0/E0,
commit, push, PR, release, or main integration.
