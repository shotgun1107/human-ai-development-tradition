# S0 v0.14 public assembly runtime profile and neutral preloader independent rereview brief v0.3

## 1. Role and exact gate

You are the fresh independent public design rereviewer for:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.3 INDEPENDENT REREVIEW OPEN`

This role is read-only. Do not implement, edit, create a review file, compile,
install dependencies, materialize a runtime profile, create a pipe, job,
process, native guard, or output root, run implementation tests,
platform-probe, invoke `NtCreateFile` or `MoveFileExW`, rehearse, access an
oracle, commit, push, merge, or publish.

Do not use prior conversation, invalid earlier review attempts, another
reviewer's conclusions, or author explanations outside the exact public
allowlist as evidence.

## 2. Exact-path access rule

CONTROL must supply an explicit list of every permitted file path. Access each
path individually. Do not enumerate a directory, run a repository-wide search,
or inspect a filename outside that list. A directory or package name is not
permission to list its contents.

The maximum logical input set is:

- current root `AGENTS.md`;
- canonical public text-artifact validator;
- authenticated assembly v0.3, v0.4, and v0.5 design packages and approving
  v0.5 rereview;
- current public assembly implementation manifest and candidate report only,
  without implementation source or tests;
- all six logical v0.1 runtime/preloader design artifacts, sidecars, and
  package manifest;
- the CONTROL v0.1 rereview-result preservation record and sidecar;
- all six logical v0.2 runtime/preloader design-revision artifacts, sidecars,
  and package manifest;
- the CONTROL v0.2 rereview-result preservation record and sidecar;
- all six logical v0.3 runtime/preloader design-revision artifacts, sidecars,
  and package manifest; and
- externally supplied Git identities and SHA-256 pins required to authenticate
  those exact paths.

An explicit future CONTROL prompt may narrow this set. It may not broaden it by
implication.

## 3. Permanently denied inputs

Do not open, list, search within, quote, summarize, derive from, or transmit the
contents of:

- `s0-lab/control/f0-sealed/**`;
- `s0-lab/f0-sealed-staging/**`;
- `s0-lab/reviews/f0-sealed/**`;
- implementation source or tests;
- any repository path outside the exact supplied list;
- hidden oracle, canonical execution input, credentials, personal/customer or
  secret material;
- network, provider, or model outputs; or
- prior chats or previous reviewer work.

Any unauthorized filename or content access invalidates the role. Stop and
return `INVALID-REVIEW` without revealing the unauthorized name or content.

## 4. Authentication preflight

Before semantic review:

1. Verify the supplied commit, tree, parent, and clean pinned-source condition.
2. Recompute every supplied logical artifact and sidecar hash.
3. Run the canonical validator SelfTest before relying on it.
4. Verify every allowed public Markdown with a same-basename sidecar.
5. Parse every allowed JSON with duplicate-key rejection.
6. Validate both assembly schemas and runtime/preloader schemas v0.1, v0.2,
   and v0.3 as Draft 2020-12.
7. Verify every package manifest's exact row count, order, uniqueness, admitted
   path set, target hash, and absence of self/sidecar rows.
8. Reproduce all externally supplied predecessor, review-record, and current
   package pins.

Do not repair an input. Any incomplete or failed preflight is
`INVALID-REVIEW`.

## 5. Required semantic questions

Answer every subsection with exact artifact and section citations.

### 5.1 Replacement scope and finding closure

- Does v0.3 replace only the handle-discovery, root-create/open race, related
  failure routing, and terminal-retry clauses?
- Does the response faithfully close `RPNP2-RR-001`, `RPNP2-RR-002`, and
  `RPNP2-RR-003` rather than merely restating them?
- Are all unrelated v0.1/v0.2 trust, closure, channel, process/job, commit,
  receipt, failure, and claim-limit predicates preserved?
- Is the v0.2 review record correctly treated as CONTROL normalization rather
  than reviewer signature or approval?

### 5.2 Handle discovery and locator authority

- Does the exact command line make all five inherited handles discoverable
  without using an admission frame that itself requires an unknown handle?
- Are order, representation, count, duplicate rejection, standard-handle
  exclusion, and argv scrubbing complete and implementable?
- Are numeric locators explicitly non-authoritative?
- Can an extra, substituted, stale, closed, wrong-type, wrong-direction, or
  overprivileged handle reach a Python wrapper or admission authority?

### 5.3 Native bootstrap guard

- Is the exact extension source/binary/build/import closure authenticated
  before use without creating a new circular trust dependency?
- Is `bind_once_v3` genuinely one-use on both success and failure?
- Are type, access direction, root identity, preloader PID/image, verifier
  identity, peer/protocol, nonce, frame, and EOF checks sufficient and ordered
  before authority publication?
- Can partial return, exception recovery, module reload, alias import, copied
  capsule, generic FFI, or a second call produce authority?
- Are explicit-list provenance and opposite-end absence allocated correctly
  between authenticated preloader construction and guard-side validation?

### 5.4 Atomic output-root construction

- Does one parent-relative `NtCreateFile` call both create the absent leaf and
  return the sole retained root handle?
- Are the x64 ABI, eleven arguments, flags, access, share, disposition,
  `OBJECT_ATTRIBUTES`, `UNICODE_STRING`, status, and information result exact?
- Do `OBJ_DONT_REPARSE`, relative naming, `FILE_CREATE`, post-call checks, and
  continuous handle retention eliminate every create/open substitution route?
- Do disabled parent case sensitivity plus `OBJ_CASE_INSENSITIVE` force a
  concurrently inserted case alias to collide while exact post-create case is
  still verified?
- Can a collision, case alias, reparse object, warning status, different
  returned object, alternate API, retry, or pathname reopen be accepted?
- Does the reduced-access inherited duplicate bind the same root object while
  the preloader retains the original?

### 5.5 Runtime and native trust closure

- Is adding `ntdll.dll!NtCreateFile` compatible with the existing external
  CONTROL-launcher and Windows-kernel trust roots?
- Are exact `ntdll.dll` file/PE/export identities checked before the first
  authoritative native call?
- Does the v0.3 schema force the guard, build, import, platform, locator,
  atomic-root, predecessor, and terminal policies needed by the design?
- Is the future runtime package exactly four externally pinned rows with no
  predecessor ambiguity or unmanifested build/runtime input?

### 5.6 State and commit ordering

- Is preloader order exactly absent intent, atomic root, retained identity,
  suspended verifier, handle bind, publication, commit request, preloader
  recheck, reply, and consumer?
- Does the verifier begin only in `ROOT-CREATED-BOUND` after successful native
  binding?
- Do invalid nonterminal transitions become `REJECTED` while attempts against
  `SPENT` or `REJECTED` fail without state mutation?
- Can concurrency, retry, copied authority, `OK`, output presence, exit code,
  stdout, or stderr produce a second result or fabricate PASS?

### 5.7 Failure routing and residue

- Does pre-create authentication failure remain root-absent `AR-AUTH/0`?
- Does every failure after `FILE_CREATED` but before verifier admission remain
  `AR-BOUNDARY/0` with quarantined-root residue?
- Can a native-guard exception be relabeled, caught, retried, or downgraded?
- Are cleanup and close-then-path operations diagnostic only and unable to
  upgrade failure?

### 5.8 Implementability and acceptance evidence

- Can the frozen locator, native guard, `NtCreateFile`, handle duplication,
  and transition mechanisms be implemented on admitted Windows builds without
  an unstated API, access right, share-mode, or object-provenance assumption?
- Does the acceptance plan cover positive, hostile, race, state, source,
  binary/import, and cross-finding mutations?
- Does it require a real-platform proof that the retained root handle both
  prevents substitution and permits the frozen output operations?
- Are build, platform probe, implementation, and official rehearsal still
  separate later gates?

### 5.9 Security and claim boundaries

- Are implementation, compilation, runtime materialization, platform probe,
  official rehearsal, F0, oracle, provider/model/network, S0/E0, central
  system, Project Brain, safety, economic value, transfer, Git publication,
  and main integration still closed?
- Does a possible PASS open only implementation consideration under a new
  explicit gate?

## 6. Finding format

Each finding must contain:

- stable identifier `RPNP3-RR-###`;
- severity `BLOCKING`, `MAJOR`, or `MINOR`;
- exact artifact and section;
- falsifiable issue and counterexample or missing evidence;
- smallest sufficient correction; and
- frozen interface, schema, threat-model, or acceptance impact.

## 7. Verdict vocabulary

Return exactly one:

- `PASS-FOR-PUBLIC-RUNTIME-PROFILE-AND-PRELOADER-IMPLEMENTATION-CONSIDERATION-ONLY`
- `REVISE-AND-REREVIEW`
- `INVALID-REVIEW`

PASS requires completed preflight, every question answered, no boundary
failure, and zero unresolved `BLOCKING` or `MAJOR` findings. PASS is not
implementation authorization.

## 8. Required final statement

State the exact verdict, authenticated basename/hash inventory, finding counts,
boundary status, and that no implementation, file creation, compilation,
dependency installation, runtime materialization, platform probe, rehearsal,
real `NtCreateFile`, real `MoveFileExW`, F0 access, oracle, network, commit,
push, or integration occurred. If PASS is issued, state that it opens only
separate implementation consideration.
