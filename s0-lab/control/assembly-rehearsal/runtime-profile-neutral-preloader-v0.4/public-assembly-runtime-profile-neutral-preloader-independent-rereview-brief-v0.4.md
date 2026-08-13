# S0 v0.14 Public Assembly Runtime Profile and Neutral Preloader Independent Rereview Brief v0.4

## 1. Role, gate, and result channel

You are a fresh independent public-design rereviewer for:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.4 INDEPENDENT REREVIEW OPEN`

This role is read-only. Return the complete review in the final response to
CONTROL. Do not create or edit a repository review file. CONTROL may later
preserve the returned result in a separately identified normalization record,
which is not a reviewer signature or approval.

Do not implement, compile, install, materialize a runtime profile, create a
pipe/job/process/guard/root, execute implementation tests, run a platform
probe, invoke native APIs, rehearse, access an oracle, call another agent,
commit, push, merge, or publish.

Do not use prior conversation, author explanation outside the exact allowlist,
an invalid earlier review, or another reviewer conclusion as evidence.

## 2. Exact-path and external-pin requirement

Before review, CONTROL must provide:

- exact repository, branch, commit, tree, sole parent, parent tree, and
  authenticated source-ref identities;
- a literal list of every permitted file path;
- an external SHA-256 pin for root `AGENTS.md`, the canonical validator, every
  package manifest, predecessor review record, implementation manifest and
  candidate report admitted below; and
- the expected initial clean state.

Access each supplied path individually. A directory or package name is not
permission to list it. If any path or required pin is missing, return
`INVALID-REVIEW` before substantive reading. The maximum logical input set is:

- current root `AGENTS.md`;
- canonical public text-artifact validator;
- authenticated assembly v0.3, v0.4, and v0.5 design packages and approving
  v0.5 rereview;
- current public assembly implementation manifest and candidate report only,
  without following manifest rows into source or tests;
- all six logical v0.1 runtime/preloader artifacts, sidecars, and package
  manifest;
- CONTROL v0.1 rereview-result preservation record and sidecar;
- all six logical v0.2 artifacts, sidecars, and package manifest;
- CONTROL v0.2 rereview-result record and sidecar;
- all six logical v0.3 artifacts, sidecars, and package manifest;
- CONTROL v0.3 rereview-result preservation record and sidecar;
- all six logical v0.4 artifacts, sidecars, and package manifest; and
- externally supplied Git identities and SHA-256 pins needed to authenticate
  those exact paths.

CONTROL may narrow this set. It may not broaden it by implication.

## 3. Permanently denied inputs

Do not open, list, search within, quote, summarize, derive from, or transmit:

- `s0-lab/control/f0-sealed/**`;
- `s0-lab/f0-sealed-staging/**`;
- `s0-lab/reviews/f0-sealed/**`;
- implementation source or tests;
- an implementation-manifest target;
- any repository path outside the supplied literal list;
- hidden oracle, canonical execution input, credential, personal/customer or
  secret material;
- network, provider, model, or prior-chat output.

Any unauthorized access invalidates the role. Stop and return
`INVALID-REVIEW` without revealing the unauthorized name or content.

## 4. Authentication preflight

Before semantic review:

1. verify commit, tree, sole parent, source ref, and clean pinned source;
2. reproduce every supplied external SHA-256;
3. run canonical-validator SelfTest before relying on it;
4. validate every allowed Markdown/sidecar pair;
5. parse every allowed JSON with duplicate-key rejection and validate its
   sidecar;
6. validate all admitted assembly and runtime/preloader schemas as Draft
   2020-12;
7. verify every design-package manifest's exact row count, order, uniqueness,
   admitted path set, target hash, and no self/sidecar row;
8. structurally authenticate the implementation manifest without opening,
   hashing, or following its target files; and
9. reproduce predecessor, review-record, candidate-report, and current package
   pins.

Do not repair an input. Any incomplete or failed preflight is
`INVALID-REVIEW`.

## 5. Required semantic questions

Answer every subsection with exact artifact and section/key citations.

### 5.1 Scope and finding closure

- Does v0.4 replace only inheritance-responsibility and profile/schema closure?
- Are `RPNP3-RR-001` and `RPNP3-RR-002` actually closed?
- Are v0.3 atomic-root and terminal corrections preserved?
- Are all unrelated predecessor trust, process/job, channel, commit, receipt,
  routing, and claim-limit predicates preserved?
- Is the v0.3 record treated as CONTROL normalization, not reviewer approval?

### 5.2 Responsibility and observability

- Is each exact-list, opposite-end, decoy, locator, known-object, and
  process-wide claim assigned to a component that can observe or establish it?
- Does the guard explicitly stop claiming unknown-handle enumeration?
- Does the design distinguish preloader construction evidence from guard
  observation and platform behavior?
- Is pinned kernel behavior treated as an assumption requiring bounded
  platform evidence rather than as already proven?

### 5.3 Exact process creation

- Are `CreateProcessW`, `STARTUPINFOEXW`, the single attribute, attribute ID,
  five-handle order, 40-byte array, flags, `bInheritHandles`, startup flags,
  lifetime, and process result exact and implementable?
- Can a caller, environment, callback, alternate creation path, standard
  handle, opposite end, or unrelated inheritable handle enter authority?
- Are application, command-line, environment, current-directory, token,
  mitigation, and job inputs still authenticated?

### 5.4 Launch evidence and native guard

- Do the launch-evidence record and postcreation admission avoid circularity
  and bind only facts available to their respective producers/consumers?
- Does the admission frame bind only hashes while keeping raw handle values
  out?
- Can evidence substitution, stale PID, changed locator, admission mismatch,
  copied wrapper, partial return, module alias, reload, second call, or generic
  FFI produce authority?
- Is every known-handle validation within the frozen guard API surface?

### 5.5 Schema completeness

- Does the v0.4 schema require every package, platform, source/build/import,
  compiler/linker, binary/loaded-image, initialization, handle, guard,
  process-creation, admission, atomic-root, retention, state, and residue
  predicate promised by the design?
- Does every object reject unknown properties?
- Are exact arrays, orders, policy IDs, Booleans, counts, API constants,
  identities, and hashes constrained?
- Can the v0.3 counterinstance or any equivalent omission still validate?

### 5.6 Cross-object semantic relations

- Are all relations that JSON Schema cannot execute named exactly?
- Is an independently authenticated validator identity mandatory?
- Does the acceptance plan require one negative mutation for every relation?
- Could mere presence of a relation-name string be mistaken for executed
  evidence?

### 5.7 Platform and race evidence

- Does the later decoy probe directly test omitted inheritable handles,
  opposite ends, concurrency, and every admitted build?
- Does it avoid using guard success as proof of unknown-handle absence?
- Are the existing root substitution/usability probes preserved?
- Does a failed or unsupported platform stop rather than relax the design?

### 5.8 Nonregression and gate separation

- Are atomic root, channel, state, commit, process/job, runtime/import,
  receipt/publication, routing, and claim boundaries preserved?
- Are source review, build, binary/import review, semantic validation,
  platform probe, and official rehearsal still distinct later gates?
- Does PASS open only separate implementation consideration?

## 6. Finding format

Every finding must include:

- stable ID `RPNP4-RR-###`;
- severity `BLOCKING`, `MAJOR`, or `MINOR`;
- exact artifact and section/key;
- falsifiable defect and counterexample or missing evidence;
- smallest sufficient correction; and
- interface, schema, threat-model, or acceptance impact.

## 7. Verdict vocabulary

Return exactly one:

- `PASS-FOR-PUBLIC-RUNTIME-PROFILE-AND-PRELOADER-IMPLEMENTATION-CONSIDERATION-ONLY`
- `REVISE-AND-REREVIEW`
- `INVALID-REVIEW`

PASS requires completed preflight, every semantic question answered, intact
input boundary, and zero unresolved BLOCKING or MAJOR findings. PASS is not
implementation authorization.

## 8. Required final statement

State the exact verdict, authenticated basename/hash inventory, finding
counts, boundary status, and that no implementation, file creation, build,
dependency installation, runtime materialization, implementation test,
platform probe, rehearsal, real native API, F0, oracle, network/provider/model,
commit, push, merge, publication, or integration occurred. If PASS is issued,
state that it opens only separate implementation consideration.
