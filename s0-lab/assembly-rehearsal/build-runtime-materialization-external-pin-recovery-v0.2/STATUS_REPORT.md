# External-pin recovery implementation v0.2 result-preservation status report

## Scope and provenance

- Result-preservation gate: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.2 INDEPENDENT CODE AND SECURITY REREVIEW RESULT PRESERVATION OPEN`
- Implementation gate: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN RECOVERY IMPLEMENTATION V0.2 REVISION OPEN`
- Branch at the authenticated handoff: `codex/s0-build-runtime-external-pin-recovery-implementation-v02-revision`
- Base HEAD: `a9264101b4fd0e678dad20131c03267b60b88bcc`
- Base tree: `6e62a22d8f262e6d40a63f1480f5984f9d6f63d2`
- Base parent: `defec54dd0f6bf9896bc22beab2732f4ae660e48`
- Repository state at handoff: all v0.2 candidate, test, verification, and documentation files were outside the base tree and had not been staged, committed, or pushed.
- External location representation: `<OUT-OF-REPOSITORY-EPHEMERAL-ROOT>`

The base commit and tree identify the inherited Git state. They are not a
commit or tree identity for the uncommitted v0.2 artifacts.

## Authenticated verification results

Direct TEST commands from the repository root:

```text
python -I -S -B s0-lab/assembly-rehearsal/build-runtime-materialization-external-pin-recovery-v0.2/tests/test_foundation_acquisition.py
python -I -S -B s0-lab/assembly-rehearsal/build-runtime-materialization-external-pin-recovery-v0.2/tests/test_materialization_security.py
```

- Foundation acquisition: exit 0, 11 of 11 tests passed.
- Materialization security: exit 0, 8 of 8 tests passed.

The two direct TEST files remained byte-identical through cycles 3 and 4 and
were not rerun in either cycle. The results above are the latest authenticated
direct evidence, not a claim of a new direct run.

Authenticated snapshot verifier command:

```text
python -I -S -B <v0.2>/verification/verify_candidate.py --evidence-out <fresh-out-of-repo-verifier-evidence.json>
```

- Exit: 0
- Status: `verified-candidate-test-bytes-under-unverified-host-runtime`.
- Frozen source-and-test hashes: 10 of 10 matched before and after execution.
- Isolated test cardinality: exactly 11 foundation plus 8 materialization-security tests.
- Results: nonce-bound and structured.
- Failures, errors, skips, and expected failures: 0, 0, 0, and 0.
- Authenticated execution input: pinned candidate and test bytes supplied on
  standard input and executed through an in-memory loader.
- Recursive inventory checks rejected reparse points, symlinks, nonregular
  entries, and unexpected files, including shadow `.pyd` and `.pyc` files.
- Five sentinels detected filesystem mutation, path-and-byte swap, shadow
  `.pyc`, shadow `.pyd`, and a forged child result.
- Verification evidence SHA-256: `76d062c28817e09a8e2b10fc30b8bf7cee93ea00e5678c5e519007ddfc9c087e`.
- Observed interpreter SHA-256: `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a`.
- Observed interpreter size: 104,952 bytes.
- Interpreter identity and bytes: stable before and after the run.
- Site loading: disabled.
- Authenticated scope: candidate and test byte binding only.
- Host-runtime authority and role: `UNAUTHENTICATED` and
  `TRUSTED-PREREQUISITE`.
- Unverified closure: interpreter, standard library, site, platform, and
  OS-DLLs.
- Applicable fixed-list blocker: `RUNTIME-PROFILE`.

For cycle-history preservation, the first cycle 2 verifier attempt failed
closed at 0 executed tests because
the authenticated in-memory test module was detached from `__main__`. TEST
made a minimal bootstrap-only correction before the authenticated passing
cycle 2 run. The initial fail-closed attempt was not counted as a pass.

The live command used the same acquisition harness, a fresh explicit
out-of-repository root, parsed and validated the verifier record, and derived
its digest internally:

```text
python -I -S -B <v0.2>/verification/acquire_live_artifacts.py --verification-evidence <canonical-verifier-record.json> --external-root <fresh-out-of-repo-root>
```

- Exit: 0
- Status: `completed-blocked-nonexecuting`
- Bound verifier record SHA-256: `76d062c28817e09a8e2b10fc30b8bf7cee93ea00e5678c5e519007ddfc9c087e`.
- Pre-live measurement: the canonical verifier record was read, parsed, and
  SHA-256 hashed before the live operation phase.
- Post-live measurement: after that phase the record was independently reread,
  reparsed, and rehashed.
- Pre/post result: both SHA-256 values and both full parsed records were
  identical.
- Candidate loading: all 8 modules loaded only from
  `<authenticated-memory>` after inventory and byte authentication.
- Repository-path candidate fallback: none.
- Live harness SHA-256: `b0d65dd7cc39e092e783002bfac5edf0d19032e4faecef14fd55d0c7ee620df0`.
- External root creation: fresh, exclusive, and secure.
- External root binding: identity retained for the full lifecycle; path
  fallback disabled.
- Evidence persistence: evidence JSON and companion sidecar written
  handle-relative and final-reauthenticated.
- External root final state: identity stable and root persisted after handle
  close; no deletion was performed.
- Runtime and producer authority and role: `UNAUTHENTICATED` and
  `TRUSTED-PREREQUISITE`.
- Unverified closure: live harness, interpreter, standard library, platform,
  OS-DLLs, and network stack.
- Producer and runtime authenticated: false and false.
- Applicable fixed-list blockers: `ACQUISITION-PRODUCER` and
  `RUNTIME-PROFILE`.
- Live evidence JSON SHA-256: `ee25ce05a42132f821ddaa7e682914fa65201bd25ea262a8e0cd7aaf7932ebaf`.
- The external companion sidecar recorded the same evidence JSON digest.
- External sidecar file SHA-256: `7681768362c98777cf64a1477574caddbffb48602dc77254319706776a7fbd95`.

Offline retained-root binding command:

```text
python -I -S -B <v0.2>/verification/acquire_live_artifacts.py --verification-evidence <canonical-verifier-record.json> --offline-binding-check
```

- Exit: 0
- Rename and replacement attacks: failed closed.
- Preexisting repository junction and direct repository target: failed
  closed.
- The failed `mklink /J` attempt against the already-existing retained-root
  name demonstrates name-collision and replacement rejection. It does not
  demonstrate dynamic in-place FSCTL reparse conversion coverage.
- Repository sentinel: absent.
- Evidence and sidecar binding: handle-relative and final-reauthenticated.
- Deletion: none.

An initial cycle 4 offline invocation encountered a syntax error before any
action. TEST made one minimal control-flow correction; only the subsequent
exit-0 run above is recorded as passing.

## Live artifact evidence

### CPython 3.12.10 embeddable ZIP

- Pin ID: `cpython-3.12.10-embed-amd64`
- Frozen source: `https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip`
- Expected and observed SHA-256: `4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3`
- Observed size and HTTP length: 11,133,606 bytes.
- Acquisition state: authenticated.
- Acquisition evidence SHA-256: `7548040d9f7cb484dfb5d78fe7783c673e6f020a34331007cca2a0b38850d4a7`.
- Materialization: 35 files, 22,501,299 bytes.
- Target-set SHA-256: `6fc8da66db95821ca8692de9d224d63673b11c0a47593cfa86fced2fb32549df`.
- Final reauthentication: the archive and all 35 outputs passed.

### Visual Studio Build Tools bootstrapper

- Pin ID: `vs-build-tools-17.14.39-17.14.37614.0`
- Acquisition state: `acquired-unauthenticated`.
- Observed SHA-256: `236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29`.
- Observed size and HTTP length: 4,473,936 bytes.
- Acquisition evidence SHA-256: `1a15a979d9a5b627ff92a2d195740c0a6a650558823cddcf7c3f7acf6a94b14a`.
- Authority boundary: the observed digest identifies the acquired bytes but is
  not an authoritative expected digest and was not promoted to one.
- Execution state: not executed.

### jsonschema source

- Acquisition state: unavailable.
- No materialization, import, installation, or execution occurred.

## Independent review history and final cycle 4 verdict

Fresh independent review cycle 1 returned `REVISE-AND-REREVIEW` with 0
BLOCKING, 2 MAJOR, and 1 MINOR findings.

- The bounded path/parent finding `BRM-EPRI01-IR-001` was closed by that
  review.
- The stable identity and final reauthentication finding
  `BRM-EPRI01-IR-002` was closed by that review.
- The exported frozen `ArtifactPin` remained mutable through
  `object.__setattr__`, and string-ID resolution returned a retained object
  without a frozen-snapshot recheck. `BRM-EPRI01-IR-003` remained open as
  MAJOR.
- The verifier hashed pinned paths before and after execution but executed
  mutable paths, and its inventory missed shadow `.pyd` and `.pyc` files.
  `BRM-EPRI01-IR-004` remained open as MAJOR.
- The live driver accepted a caller-supplied well-formed verifier digest. This
  was MINOR.

The cycle 2 implementation response moved authority to three closure-held
primitive tuples. Public pin objects and maps remain compatibility views;
downstream operations capture immutable trusted values and do not trust object
identity or reread exported views. TEST exercised mutation of all six exported
fields and views, rebinding, clones, subclasses, proxies, and mid-stream
mutation without finding a code defect. The revised verifier and live driver
results are recorded above.

Fresh independent rereview cycle 2 returned `REVISE-AND-REREVIEW` with 0
BLOCKING, 2 MAJOR, and 1 MINOR findings. Within the supported APIs it closed
the prior findings `BRM-EPRI01-IR-001`, `BRM-EPRI01-IR-002`, and
`BRM-EPRI01-IR-003`; `BRM-EPRI01-IR-004` remained open.

The two cycle 2 rereview MAJOR findings were:

- the verifier bound candidate and test bytes but did not pin or record the
  interpreter, standard-library, site, platform, and OS-DLL closure; and
- the live harness imported the repository candidate before performing its
  hash authentication.

The MINOR finding was that the public verifier and live reproduction commands
omitted the required `--evidence-out` and `--verification-evidence` arguments.

Cycle 3 changed only the two TEST-owned verification scripts. The final
verifier explicitly limits authentication to candidate and test bytes under an
unverified host runtime. The final live harness loads all eight candidate
modules from authenticated memory after inventory and byte authentication.
The reproduction commands above include every required evidence argument.

Fresh independent rereview cycle 3 returned `REVISE-AND-REREVIEW` with 0
BLOCKING, 1 MAJOR, and 2 MINOR findings. Within the calibrated supported scope
it closed the prior findings `BRM-EPRI01-IR-001`, `BRM-EPRI01-IR-002`,
`BRM-EPRI01-IR-003`, and `BRM-EPRI01-IR-004`. Runtime and live authority
remained explicitly absent.

The cycle 3 rereview findings were:

- MAJOR: the live external-root identity was not retained, and reopening the
  evidence path could bind to a replacement;
- MINOR: verifier-record pre/post stability was claimed although the record
  was measured only once; and
- MINOR: both direct-test reproduction commands omitted `-S`.

Cycle 4 changed only the TEST-owned live verification script. Its offline and
live evidence records retained-root binding, handle-relative evidence and
sidecar persistence, actual pre/post verifier-record rereads, and corrected
direct-test commands.

Fresh independent rereview cycle 4 authenticated this exact boundary:

- Repository hashes: 18 of 18.
- External hashes: 4 of 4.
- Branch: `codex/s0-build-runtime-external-pin-recovery-implementation-v02-revision`.
- HEAD: `a9264101b4fd0e678dad20131c03267b60b88bcc`.
- Tree: `6e62a22d8f262e6d40a63f1480f5984f9d6f63d2`.
- Parent: `defec54dd0f6bf9896bc22beab2732f4ae660e48`.
- Review mode: read-only, no F0 content access, and no acquired or repository
  artifact execution.

The exact verdict is:

`PASS-FOR-BOUNDED-WINDOWS-EXTERNAL-PIN-RECOVERY-IMPLEMENTATION-V0.2-NO-LIVE-AUTHORITY`

Finding counts are 0 BLOCKING, 0 MAJOR, and 2 MINOR. The review retained the
following calibrated dispositions:

- `BRM-EPRI01-IR-001`, `BRM-EPRI01-IR-002`, and `BRM-EPRI01-IR-003` are
  closed in the bounded supported scope.
- `BRM-EPRI01-IR-004` is closed only for calibrated candidate/test-byte
  binding under an `UNAUTHENTICATED` / `TRUSTED-PREREQUISITE` host runtime.
- The cycle 3 external-root MAJOR is closed in the bounded scope.
- The cycle 3 verifier-record pre/post and direct-command `-S` MINOR findings
  are closed.
- Runtime, producer, and live authority remain absent under
  `RUNTIME-PROFILE` and `ACQUISITION-PRODUCER`.

The 2 remaining MINOR findings are:

- The reviewed public offline command omitted the parser-required
  `--verification-evidence` argument. The corrected command appears above;
  this documentation reproduction defect is corrected during result
  preservation after the passing review.
- The TEST harness label for a failed `mklink /J` attempt against an existing
  root demonstrates name-collision and replacement rejection, not dynamic
  in-place FSCTL reparse conversion. The TEST artifact is unchanged, this
  limitation remains unresolved in that reviewed artifact, and this report
  does not claim the broader coverage.

Review-finding disposition and the candidate's fixed-list blocker state are
separate records; the authenticated candidate state still enumerates the same
17 fixed-list blockers below.

## Remaining blockers

The 17 fixed-list candidate blockers remain unresolved:

- `ACQUISITION-PRODUCER`
- `BRM-EPRI01-IR-001`
- `BRM-EPRI01-IR-002`
- `BRM-EPRI01-IR-003`
- `BRM-EPRI01-IR-004`
- `EFFECTIVE-TRUST-SNAPSHOT`
- `FRESHNESS-PROVENANCE`
- `IR-001`
- `IR-002`
- `IR-003`
- `JSONSCHEMA-TRANSITIVE-CLOSURE`
- `MATERIALIZER-SOURCE`
- `NATIVE-SOURCE`
- `OFFLINE-TOOLCHAIN-LAYOUT`
- `RUNTIME-PROFILE`
- `SEMANTIC-VALIDATOR`
- `SUPPLIER-ASSURANCE`

The 4 live-specific blockers also remain:

- `CPYTHON-EXPECTED-SIZE-UNPINNED`
- `VS-BUILD-TOOLS-UNAUTHENTICATED-PIN`
- `VS-BUILD-TOOLS-EXPECTED-SIZE-UNPINNED`
- `JSONSCHEMA-SOURCE-UNAVAILABLE`

"Fixed-list" describes a stable enumerated candidate list. It does not mean
that any blocker was fixed or cleared.

## Claim-state boundary

The authenticated handoff records every process, installation, build,
runtime, rehearsal, S0, and E0 claim and validation state as false. No acquired
byte was executed, imported, installed, compiled, or linked. No installer,
compiler, build, runtime construction, candidate process, rehearsal, S0, or E0
operation was authorized or performed by this gate.

The technical cycle 4 rereview is complete. CONTROL result preservation is in
progress. The following remain unverified or unpublished:

- independent review of the preservation-only documentation corrections;
- final CONTROL preservation and publication decisions;
- commit, push, and `main` integration of the v0.2 result;
- authentication of the interpreter, standard library, site, platform,
  OS-DLL, live-harness, and network-stack closure;
- authenticated acquisition-producer and runtime authority;
- supplier authority for the observed Build Tools digest;
- expected-size authority for CPython or Build Tools;
- jsonschema source and transitive-closure acquisition;
- installation, offline toolchain layout, build, runtime construction,
  rehearsal, S0, E0, central-system, Project Brain integration,
  operational-safety, economic-value, and model-to-model-transfer claims.

This report preserves authenticated CODE and TEST evidence. It does not make
an independent review or approval decision.
