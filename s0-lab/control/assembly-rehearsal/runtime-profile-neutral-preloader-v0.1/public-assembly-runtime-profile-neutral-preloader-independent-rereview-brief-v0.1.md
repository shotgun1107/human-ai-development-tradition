# S0 v0.14 public assembly runtime profile and neutral preloader independent rereview brief v0.1

## 1. Role

You are the independent public design rereviewer for the S0 v0.14 public assembly runtime-profile and neutral-preloader design v0.1.

This role is read-only. Do not implement, compile, install dependencies, materialize a runtime profile, run a platform probe, invoke `MoveFileExW`, run the assembly rehearsal, create fixtures, access an oracle, commit, push, merge, or publish.

The exact review gate is `S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.1 INDEPENDENT REREVIEW OPEN`.

Do not use prior conversation as evidence. Use only the exact public inputs supplied by CONTROL under this brief.

## 2. Maximum allowed inputs

The allowlist is a maximum. Do not search the repository broadly.

CONTROL may supply only:

- the current root `AGENTS.md`;
- the authenticated v0.3 design and acceptance package;
- the authenticated v0.4 design revision and acceptance package;
- the authenticated v0.5 design revision, acceptance plan, interface map, design-package manifest, and independent rereview;
- the current public assembly implementation manifest and implementation report only, for the documented fail-closed runtime gap;
- the six logical v0.1 design-package artifacts, their same-basename SHA-256 sidecars, and `design-package-files.sha256`;
- the canonical public text-artifact validator required by repository policy;
- externally supplied Git commit/tree identifiers and file hashes needed to authenticate the allowlist.

The reviewer must not open implementation source files unless CONTROL issues a new, explicit allowlist. The reviewer must not infer permission from a mentioned path.

## 3. Permanently denied inputs for this role

Do not open, search within, quote, summarize, derive from, or transmit the contents of:

- `s0-lab/control/f0-sealed/**`;
- `s0-lab/f0-sealed-staging/**`;
- `s0-lab/reviews/f0-sealed/**`;
- any hidden oracle, canonical execution input, credential, personal data, customer data, secret, or past-project content;
- repository files outside the exact allowlist;
- network, provider, or model outputs used as design evidence;
- prior chats or another reviewer's conclusions.

If an unauthorized content read occurs, stop and return `INVALID-REVIEW` with a boundary-failure statement that does not reveal the content.

## 4. Authentication preflight

Before semantic review:

1. Verify the externally supplied Git commit and tree identifiers.
2. Verify each supplied artifact hash and sidecar.
3. Run the canonical text validator in self-test mode before relying on it.
4. Verify the three Markdown artifacts with that validator.
5. Parse the interface map and both schemas with duplicate-key rejection.
6. Validate both schemas against Draft 2020-12.
7. Verify `design-package-files.sha256` has exactly six sorted logical rows, with no self-row or sidecar row.
8. Confirm all predecessor pins match the supplied authenticated artifacts.

Any preflight failure returns `INVALID-REVIEW`. Do not repair an input.

## 5. Required semantic questions

Answer every question with citations to the supplied public artifacts.

### 5.1 Authority and circularity

- Is the pre-Python bootstrap circularity stated accurately?
- Is the preloader externally authenticated before entry, rather than trusted through self-hash or self-report?
- Is the Windows kernel plus CONTROL launcher clearly declared as the external trust base, without claiming that the assembly authenticates it?
- Does CONTROL retain a no-share authentication handle, create the preloader suspended, compare the child image identity, and resume only after equality?
- Does the authority graph make clear which actor authenticates every later actor?
- Can any caller-selected executable, dependency root, environment, current directory, or package discovery bypass the graph?

### 5.2 Runtime closure

- Does the runtime profile cover CPython, stdlib, extension modules, jsonschema and transitives, package metadata, private DLLs, and admitted system DLLs?
- Are exact private-tree inventory and named System32 dependencies distinguished correctly?
- Are Python module origin, loader, hash, and preload phase frozen?
- Are PE dependencies and DLL resolution roots frozen without relying on version checks?
- Are API-set contract-to-host mappings, KnownDLL resolution, static/delay/profiled-dynamic loads, and load phases represented without permitting SxS, redirection, registry, current-directory, Windows-directory, or `PATH` fallback?

### 5.3 Path, object, and time-of-check/time-of-use controls

- Are string-level path rules and file-object identity both required?
- Do no-reparse open, stream inventory, link count, handle hashing, identity checks, and retained handles close the substitution window?
- Is the final exact-set recheck placed immediately before admission commit?
- Are root replacement, output-parent replacement, case aliasing, ADS, hard links, and reparse paths rejected?

### 5.4 Native preloader neutrality

- Is the native PE profile small enough for independent audit?
- Are imports, dynamic loading, registry discovery, network, repair, fallback, retry, and alternate launchers closed?
- Is source-to-binary correspondence a required independent-review subject?
- Can preloader death or process-tree escape ever leave an authoritative success?

### 5.5 Launch and bootstrap

- Are flags, environment, `sys.path`, handles, job membership, and process ancestry exact?
- Is the verifier created suspended, assigned before resume, and unable to break away?
- Does the verifier bootstrap check admission before importing the verifier package?
- Are module and loaded-PE origin checks complete at the relevant stage?
- Does the audit policy latch denial even if candidate code catches an exception?

### 5.6 Runtime admission

- Is `RuntimeAdmission` authority based on a private, one-use, process-local identity rather than forgeable field equality?
- Are pipes, preloader image/process, verifier/job, nonce, roots, pins, and retained-handle digest bound together?
- Is the commit handshake exact, single-use, and terminal on failure?
- Can replay, copying, serialization, retry, or a public return-value constructor fabricate success?

### 5.7 Assembly and receipt compatibility

- Must both the v0.5 publication witness and runtime admission be atomically spent?
- Does the design preserve the receipt-v2 wire form without treating the current implementation or receipt hash as future execution authority?
- Are post-process status, output presence, exit code, stdout, and stderr excluded from PASS authority?

### 5.8 Failure routing and evidence

- Are pre-output authentication faults separated from post-launch boundary faults and publication/consumer faults?
- Can any unclassified process death or unauthenticated diagnostic become success?
- Does the acceptance plan require mutation evidence, negative tests, and a separate real-platform probe without treating any one as a substitute for the others?

### 5.9 Scope discipline

- Does the package avoid claims that implementation, platform behavior, S0, E0, central-system, Project Brain, operational safety, economic value, or model transfer are validated?
- Are F0 content, hidden oracle, provider/model/network, official rehearsal, Git publication, and main integration closed?
- Is the next gate only an independent rereview gate?

## 6. Finding format

Each finding must contain:

- stable identifier `RPNP-RR-###`;
- severity `BLOCKING`, `MAJOR`, or `MINOR`;
- exact artifact and section;
- falsifiable problem statement;
- concrete counterexample or missing evidence;
- smallest sufficient design correction;
- whether the correction changes a frozen interface, schema, threat model, or acceptance criterion.

Style preferences and future implementation suggestions that do not affect falsifiability belong in a non-blocking note and cannot change the verdict.

## 7. Verdict vocabulary

Return exactly one of:

- `PASS-FOR-PUBLIC-RUNTIME-PROFILE-AND-PRELOADER-IMPLEMENTATION-CONSIDERATION-ONLY`
- `REVISE-AND-REREVIEW`
- `INVALID-REVIEW`

`PASS-FOR-PUBLIC-RUNTIME-PROFILE-AND-PRELOADER-IMPLEMENTATION-CONSIDERATION-ONLY` requires zero unresolved `BLOCKING` or `MAJOR` findings and completed authentication preflight. It is not implementation authorization.

`REVISE-AND-REREVIEW` applies when the review is valid but a blocking or major design defect remains.

`INVALID-REVIEW` applies when authentication fails, the allowlist or role boundary is breached, required questions are omitted, or the reviewer cannot establish independence.

## 8. Required final statement

The review must state:

- the verdict exactly;
- the authenticated input inventory by approved basename and SHA-256;
- the number of findings by severity;
- whether any boundary failure occurred;
- that no implementation, compilation, platform probe, official rehearsal, F0-content access, commit, push, or main integration was performed;
- that a PASS, if issued, opens only implementation consideration under a separate explicit gate.
