# S0 v0.14 public assembly runtime profile and neutral preloader independent rereview brief v0.2

## 1. Role and exact gate

You are the fresh independent public design rereviewer for:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.2 INDEPENDENT REREVIEW OPEN`

This role is read-only. Do not implement, edit, create a review file, compile,
install dependencies, materialize a runtime profile, create a pipe/job/process
or output root, run implementation tests, platform-probe, invoke
`MoveFileExW`, rehearse, access an oracle, commit, push, merge, or publish.

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
- authenticated v0.3, v0.4, v0.5 design packages and approving v0.5 rereview;
- current public assembly implementation manifest and candidate report only,
  without source or tests;
- all six logical v0.1 runtime/preloader design artifacts, sidecars, and package
  manifest;
- the CONTROL v0.1 rereview-result preservation record and sidecar;
- all six logical v0.2 design-revision artifacts, sidecars, and package
  manifest; and
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
6. Validate both v0.1 schemas and the v0.2 schema as Draft 2020-12.
7. Verify every package manifest's exact row count, order, uniqueness, admitted
   path set, target hash, and absence of self/sidecar rows.
8. Reproduce all externally supplied predecessor, review-record, and current
   package pins.

Do not repair an input. Any incomplete or failed preflight is
`INVALID-REVIEW`.

## 5. Required semantic questions

Answer every subsection with exact artifact and section citations.

### 5.1 Replacement scope and nonregression

- Does v0.2 replace only the three reviewed defects?
- Are all v0.1 trust-root, runtime-closure, path, PE/DLL, audit, receipt,
  failure, and claim-limit predicates preserved?
- Is the review-result record correctly treated as CONTROL normalization rather
  than a reviewer signature or approval?

### 5.2 Channel topology

- Are admission, commit request, and commit reply three distinct unidirectional
  pipes with one sender and one receiver each?
- Are inherited and retained ends exact, minimal, nonduplicated, and closed at
  deterministic points?
- Do exact frame-plus-EOF rules reject short, extra, repeated, reordered,
  self-read, reconnect, retry, alternate, broken, and timeout conditions?
- Can an inherited opposite end, numeric handle copy, or public wrapper create
  authority?

### 5.3 Absent-leaf and created-root binding

- Does the initial admission bind only an existing parent identity and absent
  leaf, with no nonexistent-object identity?
- Is root creation exclusive, verifier-owned, exactly once, and followed by
  no-reparse retained-handle authentication before candidate creation?
- Are state transitions one-way and terminal on invalid attempts?
- Do admission, observer witness, preloader recheck, and consumer all bind the
  same retained root object identity rather than a pathname?

### 5.4 Commit and consumer order

- Does publication finish before commit begins?
- Does exact reply produce only `COMMIT-ACKED`, not success?
- Does the first live-consumer attempt atomically spend both exact same-run,
  same-root authorities into `SPENT` or `REJECTED`?
- Can any retry, copied value, status, output presence, stdout, stderr, exit
  code, or `OK` frame fabricate PASS?

### 5.5 Process and job domains

- Is the preloader clearly outside the job and separately counted?
- Do job flags and active limit permit exactly verifier plus one candidate and
  no third member?
- Are verifier/candidate creation counts, phase totals, precommit accounting,
  breakaway denial, and zero extra descendants explicit?
- Are job totals combined with separate retained candidate PID/image evidence
  rather than overclaiming what job counters prove?
- Is legacy `maximum_processes` inert and unambiguously replaced?
- Is the future v0.2 runtime-profile package an exact externally pinned
  three-row composition, with v0.1 package authority clearly superseded?

### 5.6 Cross-finding ordering and failure routing

- Is the exact order admission, root bind, candidate, publication, request,
  recheck, reply, consumer enforced?
- Are pre-import authentication, post-launch boundary, and publication/consumer
  failures routed consistently with the effective v0.5 design?
- Is an in-run created-root delete/rename forbidden after failure, and can
  quarantine, later diagnostic cleanup, an empty root, or an unauthenticated
  diagnostic ever upgrade failure?

### 5.7 Implementability and acceptance evidence

- Can each frozen transition be implemented using the named Windows/Python
  mechanisms without hidden duplex, object-identity, or process-count
  assumptions?
- Does the acceptance plan cover positive, hostile, mutation, source/binary,
  process-lifetime, and cross-finding tests?
- Are real-platform probes separate and still required later?

### 5.8 Security and claim boundaries

- Are implementation, compilation, runtime materialization, platform probe,
  official rehearsal, F0, oracle, provider/model/network, S0/E0, central
  system, Project Brain, safety, economic value, transfer, Git publication,
  and main integration still closed?
- Does a possible PASS open only implementation consideration under a new gate?

## 6. Finding format

Each finding must contain:

- stable identifier `RPNP2-RR-###`;
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
real `MoveFileExW`, F0 access, oracle, network, commit, push, or integration
occurred. If PASS is issued, state that it opens only separate implementation
consideration.
