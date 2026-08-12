# S0 v0.14 public end-to-end assembly rehearsal design independent review brief v0.1

## 1. Role

Act as a fresh public-only independent design reviewer. Review the design
without implementing the controller, producing request or response artifacts,
running the rehearsal, invoking a provider/model, or reading any F0 content.

Do not treat author self-description, previous conversation, or another
reviewer's conclusion as evidence.

## 2. Maximum input set

The review allowlist is limited to:

1. root `AGENTS.md`;
2. the authenticated I0-I3 integration-readiness audit v0.1 and sidecar;
3. the four I0-I3 implementation manifests;
4. I0-I3 public README files and only the manifest-listed implementation files
   required to verify the named public APIs;
5. the fixed public-practice files and answer schema named in the design;
6. the I2 v0.4 and I3 v0.2 public contract JSON files;
7. `public-end-to-end-assembly-rehearsal-design-v0.1.md` and sidecar;
8. `assembly-rehearsal-interface-map-v0.1.json` and sidecar; and
9. `assembly-rehearsal-acceptance-plan-v0.1.md` and sidecar.

The allowlist is a maximum. Do not browse the repository or inspect unrelated
files. The three F0 content families are denied even though they are tracked in
Git.

## 3. Authentication before substance

Before reviewing meaning, verify:

- exact branch, HEAD, origin, and clean worktree specified by CONTROL;
- all available same-basename sidecars;
- the four implementation-manifest hashes;
- the fixed public case hashes; and
- the design's exact four-file logical package and sidecars.

Any mismatch makes the review `INVALID-REVIEW`; do not continue to substantive
inspection.

## 4. Required independent questions

The reviewer must answer each question with evidence.

1. Does the design exercise the actual I0 transform and answer validator, not
   a reimplementation or a self-asserted replacement?
2. Is the I1 request authenticated through its existing external-manifest
   grant rather than passed as caller-invented trusted bytes?
3. Does the stub preserve exactly one invocation, first-final response,
   response bounds, no retries, and cleanup semantics?
4. Is the request envelope deterministic, complete enough to carry both the
   public package and questions, and free of hidden runtime choices?
5. Are I2 and I3 handled honestly? In particular, is contract verification
   sufficient for this no-import public case, and does the design avoid
   fabricating signer-media success merely to claim coverage?
6. Does the state machine prevent invocation before output reservation,
   success before validation, overwrite, resume, or retry?
7. Can the run record be reconstructed uniquely and repeated byte-identically
   without timestamps, randomness, host paths, or environment-dependent data?
8. Do failure classes preserve zero-call versus one-call facts and guarantee
   removal of incomplete success artifacts?
9. Can the future verifier detect denied path access without opening or
   enumerating F0 content?
10. Is the proposed controller the smallest adapter, with no need to modify
    I0-I3 or add a general I4/security subsystem?
11. Does any statement imply that S0, role isolation, trust root, provider
    execution, scoring, or model effects have been implemented or validated?
12. Are the acceptance criteria sufficient to distinguish a wiring success
    from merely rerunning component unit tests?

## 5. Required hostile counterexamples

At design level, trace at least these counterexamples:

- request manifest authentic but reconstructed I0 package differs;
- output collision before invocation;
- transport called once but never produces a final frame;
- valid JSON response with wrong public-response hash;
- exact public-response hash but non-empty I0 validation errors;
- record write succeeds but final close or read-back fails;
- a second execution is mislabeled as a retry;
- a design variant adds an I2 accepted route without a real signer-media
  import; and
- a denied path is introduced through configuration rather than a literal
  source string.

For each, identify the exact rejecting state and stable failure class. If the
design cannot determine one uniquely, report a finding.

## 6. Finding levels

- `blocking`: the flow cannot be constructed, can invoke more than once, can
  consume denied information, or can claim success without the required
  validation and committed record.
- `major`: a material interface, state, evidence, or cleanup rule remains
  ambiguous enough to permit incompatible implementations.
- `minor`: a bounded exactness or documentation defect that does not permit a
  false success or boundary violation.

## 7. Verdict

Return exactly one:

- `PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `REVISE-AND-REVIEW`; or
- `INVALID-REVIEW`.

The review record must list all findings, disposition each required question,
state the maximum allowed claim, name the exact next gate, and have a
same-basename SHA-256 sidecar.

A PASS does not authorize implementation, rehearsal execution, provider/model
use, F0 access, S0 execution, commit, push, PR, or main merge.
