# S0 v0.14 trust-root and role-isolation independent-review brief v0.3

- `status`: design revision candidate
- `review_kind`: fresh public-only hostile design rereview
- `review_scope`: authenticated read-only v0.3 delta and non-regression
- `claim_kind`: CONTROL integration consideration only

## 1. Reviewer independence

The reviewer must be a fresh session that did not author or advise on the
v0.1, v0.2, or v0.3 isolation candidates and did not produce an implementation
or author-side QA result derived from them. The reviewer must not inherit or
read another v0.3 reviewer conclusion and must not use a subagent.

The reviewer must not read sealed material, oracle, bank, labels, condition
map, executor output, E0, or any unlisted source. The authenticated v0.2 review
is required predecessor evidence, not an answer key. The reviewer must
independently decide whether `TRI2-M01` and `TRI2-m01` are repaired and may add
a finding for a v0.3 regression supported by the authenticated public inputs.

Use a separate clean worktree at the exact candidate commit. Candidate inputs
are read-only. Worktree separation is edit isolation, not secrecy or
independent information security.

## 2. Maximum input set

CONTROL must supply exact paths and SHA-256 values. The maximum substantive set
is the following files and their same-basename sidecars where present:

1. repository-root `AGENTS.md` at the candidate commit;
2. `s0-lab/control/s0-protocol-v0.3.md`;
3. the v0.14 universal response contract, public falsification plan, review
   response, independent review, and CONTROL integration decision;
4. the I1 public runtime v0.2 CONTROL integration decision, authenticated
   public topology JSON, public-spec manifest, implementation-files manifest,
   and implementation binding manifest;
5. all four v0.1 isolation candidate Markdown files and the v0.1 independent
   review;
6. the v0.2 design revision, identity-authority matrix addendum, isolation
   acceptance-plan addendum, review response, independent-review brief, and
   independent review;
7. `trust-root-role-isolation-design-revision-v0.3.md`;
8. `identity-authority-matrix-addendum-v0.3.md`;
9. `isolation-acceptance-plan-addendum-v0.3.md`;
10. `review-response-v0.2.md`; and
11. this independent-review brief.

The reviewer may open only official primary references linked by the candidate
to check cryptographic provenance. Broad repository search, advisory output,
implementation code beyond the explicitly authenticated I1 topology inputs,
sealed paths, and any unlisted document are forbidden.

Authenticate every supplied file before relying on its content. A sidecar hash
match establishes exact byte identity only; it does not override a canonical
text-validator failure. Conversely, a formatting-validator failure is not a
hash mismatch. Either defect must be reported distinctly and resolved before a
substantive pass verdict.

## 3. Read-only design-review boundary

This is a tabletop public-document review. Do not provision or configure a VM,
host, sandbox, account, network, clipboard, Git restriction, ACL, vault, store,
signer, ledger, witness, or provider. Do not create a key, anchor, registry,
signature, cryptographic vector, canary, fixture, bank, label, oracle, condition
map, package, script, helper, validator, model call, or acceptance harness. Do
not execute Ed25519, HKDF, vector construction, or any acceptance test.

Canonical text validation and SHA-256 checks are document-integrity checks, not
implementation or acceptance evidence. The reviewer may write only the
CONTROL-authorized review Markdown and its same-basename sidecar. Do not modify
candidate files, commit, push, merge, open a PR, or prepare implementation.

## 4. Required independent reconstruction

Without trusting the author response, reconstruct:

1. the exact v0.1 plus v0.2 plus v0.3 effective composition and replacement
   map, confirming that v0.3 changes only the two reviewed findings;
2. one outcome route and exact state mapping for each of
   `preactivation-context-v1`, `registry-binding-v1`, and
   `activation-binding-v1`;
3. the exact `import-outcome-v1` media admission and lifecycle, including a
   fresh nonzero `result_media_id`, medium capacity exactly 2,048 bytes, frame
   length at most 2,048 bytes, raw-media access, one-frame limit, zero
   remainder, persistence order, and cleanup;
4. the complete ordered bytes of `S0-SIGNER-IMPORT-ADMISSION-2`, including the
   class/state/package/object/capability bindings, exact outcome schema and
   kind, capacity, all four preallocated event IDs, and admission-event
   equality;
5. the authority and complete ordered bytes of
   `S0-SIGNER-IMPORT-OUTCOME-1` under `S0-IMPORT-TRANSITION-TCB-1`, including
   campaign, ceremony, signer, class, from/to state, package hash and object
   ID, admission event and hash, capability, outcome-medium kind and identity,
   all event IDs, before/after states and configuration-state hashes, decision,
   reason, body hash, final LF, and zero remainder;
6. the complete `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` extension, including
   outcome kind/schema/hash/class, state evidence, the inherited fields, and
   exact prior-event chaining;
7. preallocation and single use of the reserved, admission-frozen, pending, and
   completion signer-media event IDs, plus the exact rule by which the outcome
   frame and completion event bind each other without a hash cycle;
8. the full fixed-precedence outcome classification: `crash`, `missing`,
   `duplicate`, `disagreement`, `parse-rejected`, `validation-rejected`,
   `state-commit-failed`, and `accepted`; only accepted may become consumed,
   every other post-pending class requires terminal when appendable, and a
   completion collision or ledger/witness failure permits no invented
   completion;
9. the distinct pre-pending admission-failure lifecycle and the rule that it
   has no import-outcome classification;
10. the corrected algebraic derivation and four literal 32-byte order-eight
   encodings, with the false RFC 9381 attribution absent and the later
   independent construction/order check preserved;
11. the effective acceptance-row inventory, replacement/addition semantics, and
   noncompensatory rule; and
12. all frozen topology, A-D fairness, signature-scope, provider, implementation,
   protected-material, E0, and S0 invariants and nonclaims.

## 5. Mandatory hostile tabletop cases

At minimum, trace these mutations on paper for all three import classes where
applicable:

- one exact accepted frame with the expected durable after-state and matching
  host evidence;
- parse rejection, validation rejection, and state-commit failure, each with
  before/after state appropriate to its decision;
- crash before state persistence, after persistence but before frame
  completion, after frame completion but before shutdown, and before host
  completion-event persistence;
- absent, partial, truncated, oversized, malformed, extra, reordered, or
  nonzero-tail outcome bytes;
- more than one outcome frame or outcome medium, any medium beyond the exact
  ISO-plus-outcome pair, nonzero tail, completion-ID/event conflict, replayed
  outcome, reused capability, reused event ID, or reused `result_media_id`;
- wrong campaign, ceremony, signer, import class, from/to state, package hash,
  admission hash, capability, medium identity, or signer-media event ID;
- cross-signer, cross-class, cross-package, and cross-campaign substitution;
- an accepted frame with unchanged or wrong appliance state, and a rejection
  frame after an unauthorized state advance;
- host/appliance disagreement, host inference from shutdown or detachment, and
  a host attempt to mark consumed without one exact accepted frame;
- cleanup attempted before evidence persistence, stale medium retained for a
  later route, or outcome bytes containing protected or private-key data;
- treating the unsigned outcome as a new signature scope, key, signer, role,
  store, reader, edge, or experimental authority;
- a derivation step that does not reproduce each literal encoding, swaps
  little-endian/sign-bit handling, admits a noncanonical field encoding, or
  fails to establish the intended point class at design level;
- any claim that RFC 9381 section 5.4.5 contains the decimal coordinate or four
  encodings; and
- any topology, A-D opportunity, signature-scope, closed-gate, or claim-limit
  regression.

Agreement with prose is not evidence. Every handled mutation must trace to one
exact fail-closed rule and observable record. An unhandled or multiply
interpreted mutation is a finding.

## 6. Finding-specific closure criteria

### 6.1 `TRI2-M01`

Pass only if every import class has one bounded canonical host-observable
outcome route whose authority, bytes, media, state persistence, event order,
and cleanup are exact. The frame and completion evidence must bind every
required identity/hash/state/event value without circularity. Exactly one
state-consistent `accepted` outcome may advance to `consumed`; parse or
validation rejection, state-commit failure, crash, missing or duplicate
outcome, and any host/appliance disagreement must be distinguishable, require
terminal when the exact append is possible, and permit no completion claim
when it is not. No new experimental topology object or signature scope may be
added.

### 6.2 `TRI2-m01`

Pass only if the false RFC attribution is removed and the four exact 32-byte
encodings follow from a complete, independently checkable derivation or an
official primary source that actually contains them. The strict nonidentity
order-`L` acceptance predicate must remain unchanged, and a future independent
implementation reviewer must still reproduce construction, canonical decoding,
and point order rather than trust a copied label.

## 7. Frozen non-regression invariants

The reviewer must confirm all of the following remain exact:

- 32 aggregated role rows, 40 role positions, and eight paired rows;
- 21 experimental section-4 signers, 19 `none` positions, one non-row root,
  and 22 registry IDs;
- 27 stores, 46 explicit readers, and 64 edge rows;
- 107 noncompensatory acceptance rows, three ledger namespaces, eight future
  executor invocation/session units, and maximum concurrency three;
- identical A-D source information, authority, model condition, time, output,
  and scoring opportunity;
- three exclusive signature scopes; and
- all inherited provider, implementation, protected-material, E0, and S0
  blockers and nonclaims.

The outcome medium, frame, TCB service, admissions, and signer-media events may
exist only as TCB temporary/control objects. They cannot silently alter an
experimental role, signer, store, reader, edge, or authority.

## 8. Severity and verdict

- `blocking`: protected-asset exposure, lost reviewer or A-D independence,
  forgeable/circular authority, frozen-topology contradiction, or a repair
  that requires a closed implementation gate.
- `major`: a required outcome, state, authority, event, media, persistence,
  cleanup, failure, or nonclaim remains ambiguous or incomplete.
- `minor`: a bounded exactness or provenance defect that cannot grant
  authority, weaken isolation, alter experimental meaning, or hide failure.

Allowed verdicts are:

- `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`: zero findings;
- `REVISE-AND-REVIEW`: any finding exists; or
- `INVALID-REVIEW`: baseline, hash, validator, boundary, independence, or
  evidence failed.

No verdict opens implementation, provisioning, key generation, protected
material, provider/model sessions, judge handoff, scoring, E0, or S0 execution.

## 9. Required output

Write exactly one Markdown review and one same-basename `.sha256` sidecar under
the CONTROL-approved v0.3 isolation-review path. State baseline and
independence, all authenticated input hashes, effective composition, import
outcome reconstruction, vector-provenance reconstruction, hostile mutation
traces, finding dispositions, new findings, effective counts, verdict, maximum
claim, and exact next gate. State explicitly that no implementation,
cryptographic, platform, provider, model, acceptance, E0, or S0 test was run.

Before relying on the canonical public text-artifact validator, run its
SelfTest. Validate every explicitly supplied input/sidecar pair read-only and
then the authorized review output pair; do not enumerate or validate anything
outside the maximum input set. Preserve every candidate input unchanged. A
zero-finding verdict permits only separate CONTROL integration consideration;
it does not open that or any later gate by itself.
