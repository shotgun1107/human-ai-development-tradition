# S0 v0.14 trust-root and role-isolation independent-rereview brief v0.4

- `status`: rereview brief revision candidate
- `current_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION INDEPENDENT REREVIEW BRIEF REVISION OPEN`
- `review_kind`: fresh public-only hostile full design rereview after canonical protocol refreeze
- `review_scope`: authenticated read-only v0.1 + v0.2 + v0.3 composition, finding closure, and non-regression
- `claim_kind`: future independent-rereview launch consideration only
- `semantic_protocol_version`: `0.3`
- `canonical_protocol_revision`: `canonical-r1`
- `authoring_base_commit`: `f49d8bd04299a38a7417c2cafe96907acca5e4e5`
- `authoring_base_tree`: `cc2aa37f56ec665c56ad6cb5b7b16aafb4fc3e0e`

## 1. Revision authority and limit

This brief is the successor to
`trust-root-role-isolation-independent-review-brief-v0.3.md`. It changes only
the review-control layer required after the public protocol canonicalization:

1. the noncanonical predecessor protocol pair is replaced by the finally
   refrozen `s0-protocol-v0.3-canonical-r1` pair;
2. the independent limited rereview and CONTROL final-refreeze decision pairs
   are admitted only as protocol-byte and review-validity evidence;
3. an exact 56-path maximum input contract and candidate commit/tree handoff
   contract replace category-only discovery;
4. the fresh full-rereview output receives a new non-colliding path; and
5. the next possible gate is stated without opening it.

The trust-root/role-isolation v0.1, v0.2, and v0.3 design content, the two
finding closure tests, hostile cases, frozen counts, severity rules, and
nonclaims are not revised by this brief. This record is not a design fix,
independent review, CONTROL integration decision, implementation result, or
S0 authorization.

The prior `INVALID-REVIEW` remains historical evidence that no substantive
v0.3 review was completed. Its review body is deliberately excluded from the
new reviewer input set so that a fresh reviewer does not inherit another v0.3
reviewer conclusion.

## 2. Reviewer independence

The reviewer must be a fresh session that did not author or advise on the
v0.1, v0.2, or v0.3 isolation candidates, this brief revision, or any
implementation or author-side QA derived from them. The reviewer must not
inherit another v0.3 design-review conversation or conclusion and must not use
or spawn a subagent.

The reviewer must not read the historical invalid-review body, sealed
material, oracle, bank, labels, condition map, executor output, E0, or any
unlisted source. The authenticated v0.2 independent review is required
predecessor evidence, not an answer key. The protocol canonical-r1 limited
rereview is admitted only to establish the protocol-document refreeze chain;
it contains no authority to decide `TRI2-M01`, `TRI2-m01`, or any substantive
v0.3 design question.

The reviewer must independently decide whether `TRI2-M01` and `TRI2-m01` are
repaired and may add a finding for any v0.3 regression supported by the
authenticated public inputs.

Use a separate clean worktree at the exact CONTROL-supplied candidate commit.
Candidate inputs are read-only. Worktree separation is edit isolation, not
secrecy or independent information security.

## 3. Authenticated handoff contract

Before the reviewer reads substantive candidate content, CONTROL must supply
all of the following in the session-start handoff:

1. repository identity and exact candidate branch;
2. exact candidate commit and tree;
3. required exact parent commit
   `f49d8bd04299a38a7417c2cafe96907acca5e4e5` and parent tree
   `cc2aa37f56ec665c56ad6cb5b7b16aafb4fc3e0e`;
4. the exact 54 fixed path/hash records in section 4;
5. the exact path and computed SHA-256 of this brief and its same-basename
   sidecar, bringing the maximum set to 56 paths;
6. the one authorized review output Markdown path and same-basename sidecar
   path from section 11; and
7. the exact current gate, reviewer role, read boundary, write boundary, and
   closed-gate statement.

The candidate commit must have exactly one parent, and that parent must equal
the required parent exactly. Its parent-to-candidate tracked diff must contain
only these two paths:

- `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.md`
- `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.sha256`

The handoff must contain identity and boundary facts, not an author summary of
the expected substantive verdict. The reviewer must independently verify the
branch, HEAD, tree, exact parent, exact two-path diff, initial clean status,
every supplied SHA-256, and the validator hash before relying on candidate
content. A mismatch, missing record, unexpected path, dirty baseline, or
non-exact parent makes the review `INVALID-REVIEW`; do not repair the input or
continue to a substantive verdict.

## 4. Maximum input set and fixed hashes

The maximum set is exactly 56 paths: the following 54 fixed paths plus this
brief and its same-basename sidecar supplied under section 3. The fixed hashes
below were computed at the authoring base commit. The reviewer must recompute
them and compare them with the CONTROL handoff; the values are evidence to
check, not permission to skip authentication.

```text
ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844  AGENTS.md
b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3  s0-lab/control/tools/verify-text-artifacts.ps1
6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60  s0-lab/control/s0-protocol-v0.3-canonical-r1.md
88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3  s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256
49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0  s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.md
ff71deea0b0aaac3a6f46d703376b22f677baa4d0e20be22a42f98a449706766  s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.sha256
a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee  s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md
7f30298de0667cd01991e72704b963a20ebb558e1e76474eb212d8a67842d888  s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.sha256
b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9  s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.md
24ce405c3987410cd2a2f6cba0ce4ec83a235f8b23b013d908675797432e8310  s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.sha256
537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605  s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.md
e73f0bb18e65f39b6ebb8ac0fda00ef4f756a3a01000f97db9fb9a41ac0eaf6c  s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.sha256
f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65  s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md
8c90eda5c1557c1f31e977f94ec6985e8799a692e56141a830e6cc8ff7f685b4  s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.sha256
167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925  s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.md
36a1565b93df98f2d18f8447280458df66a0d38dacf2aa4bb56cc4b7a7564c40  s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.sha256
fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08  s0-lab/i1/spec/public-runtime-v0.14.json
9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e  s0-lab/i1/spec/public-runtime-files.sha256
668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c  s0-lab/i1/verification/implementation-files.sha256
1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6  s0-lab/i1/verification/implementation-manifest.sha256
6a062383742e90409f5dac9c443de90b93773c266525ba00f3802b60d40ff6fc  s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.md
7a0bc9043ae8ac2e59d4ef0aa1a8723835865717f0054e818711cc7809df8601  s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.sha256
ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0  s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.md
08fef8b7e5c31f94983b5f24cdfae44aeb5f7137cbcf81854130f589ea6ac61d  s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.sha256
71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937  s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.md
6caf7c1ca42e5ed1c81f45d481cc4403d637156068d8a9f48d61d98a9349dc3a  s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.sha256
88ca9ae00ee8a76f1f01865be7ffc106afede4a8207c86fab1bb72c9099e8d7a  s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.md
5553c4fa3698186ad1eae160143e4a97b30aba651e033db38f4c3d654352224a  s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.sha256
d99cf801719e2f524ca87fe3741b8a6776c4682df304d9448c245e5d3fee7404  s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.md
e6c8497753878df8407dd23cfa606927e09909a8486b398206bb237a75f76e7d  s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.sha256
e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md
41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256
3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1  s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md
566bba9b81d4ed5216f9c49c01448154f0a2a53ee6d9cfa13e0d9993475df70c  s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.sha256
534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1  s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md
29ec3013bab28aa1265653ad4badc034381fa91cbd40a0aa44443359a9d70060  s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.sha256
5c961d3bba03e12e07d34aede1207448565bf3456d0bffb6cad1602f1bbd2494  s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.md
ac64d54c204d17e4d541e08ab1e1ab487c2f2a43542aa317958130250383cc90  s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.sha256
610b4ca1b03d7539cdcaf526a03bf3877cfca24426fd9f58b816aa0012d6db27  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.md
964b09d8c42ee5680f15eda27659aded87571ce6b77a734affe9253473114da4  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.sha256
67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990  s0-lab/reviews/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-v0.2-independent-review.md
cf0f919f266cf765611bb84944f44441db8a14e7eb9183052c89d9cb8a467d21  s0-lab/reviews/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-v0.2-independent-review.sha256
a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b  s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.md
90b2643bd2128339261ea0eae6c334ae757d5fa096cae3e9d73b8ff7ae606757  s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.sha256
5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a  s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.md
14ad4440f996f6b637b8adb667b3975a9040ee70d8da503d5be700646438d72b  s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.sha256
bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3  s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.md
d2bac18a3bef1ec769e9f97149fa6d74bd4536b7454151ec6113fe355f9a86d7  s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.sha256
9b263749943507bd1b21e87f089a8bf02bfc446f13b8d5b02f363ab24ab24d36  s0-lab/control/isolation/trust-root-role-isolation-v0.3/review-response-v0.2.md
1ecd2755a85477befd9ac36af069d2096c241de5d2698c8478feb363c54efb3e  s0-lab/control/isolation/trust-root-role-isolation-v0.3/review-response-v0.2.sha256
e10813ad559e9ea66f3c197a0a9b99649d4d68e9f5b475eee1a8395dd796dbaf  s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.md
d47178efc71641a34c7a1fcbcfbc0a580491a26393c4c62316c30074de1d7da5  s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.sha256
512714d8745bb78c08b0b6fd085f978c84fb0b7d2439dbbae0138d2f92ef9b90  s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md
7ef1b8461efcf822baf0f29854d02e08c3f42dc519a1fffe02a997140aa7e392  s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.sha256
```

The two externally authenticated brief paths are:

- `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.md`
- `s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.sha256`

The full set contains 25 Markdown/same-basename-sidecar pairs and six other
public control or manifest files. The reviewer must not enumerate the
repository to discover inputs.

The canonical-r1 protocol retains candidate-era status text in its frozen
header. That header is byte-preserved history, not the current authority
state. The admitted CONTROL final-refreeze decision pair is the authority that
makes the canonical-r1 bytes current for this newly opened public review.

The following tracked historical records are explicitly outside the maximum
input set and must not be read or validated in this rereview:

- `s0-lab/control/s0-protocol-v0.3.md` and its sidecar;
- `trust-root-role-isolation-independent-review-brief-v0.3.md` and its
  sidecar; and
- `refreeze-candidate-record-v0.1.md`, `limited-rereview-brief-v0.1.md`, and
  their sidecars, because the final CONTROL decision and independent limited
  rereview are the narrower sufficient provenance inputs; and
- any prior trust-root/role-isolation v0.3 independent-review body, including
  the historical invalid-review record.

The reviewer may open only official primary references linked by the admitted
candidate documents to check cryptographic provenance. Broad repository
search, advisory output, implementation code beyond the explicitly admitted
I1 public topology inputs, sealed paths, and any unlisted document are
forbidden.

Authenticate every supplied file before relying on its content. A sidecar
hash match establishes exact byte identity only; it does not override a
canonical text-validator failure. Conversely, a formatting-validator failure
is not a hash mismatch. Either defect must be reported distinctly and forces
`INVALID-REVIEW` before substantive reconstruction.

Run the authenticated canonical validator SelfTest before relying on it.
Validate exactly the 25 admitted Markdown/sidecar pairs and no excluded
historical pair. The six other admitted files receive their applicable exact
SHA-256 and file-specific read-only checks, not invented Markdown-sidecar
semantics.

## 5. Read-only design-review boundary

This is a tabletop public-document review. Do not provision or configure a VM,
host, sandbox, account, network, clipboard, Git restriction, ACL, vault, store,
signer, ledger, witness, or provider. Do not create a key, anchor, registry,
signature, cryptographic vector, canary, fixture, bank, label, oracle,
condition map, package, script, helper, validator, model call, or acceptance
harness. Do not execute Ed25519, HKDF, vector construction, or any acceptance
test.

Canonical text validation and SHA-256 checks are document-integrity checks,
not implementation or acceptance evidence. The reviewer may write only the
CONTROL-authorized review Markdown and its same-basename sidecar. Do not modify
candidate files, commit, push, merge, open a PR, or prepare implementation.

## 6. Required independent reconstruction

Without trusting the author response, protocol-refreeze evidence, or prior
review conclusions as an answer key, reconstruct:

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
7. preallocation and single use of the reserved, admission-frozen, pending,
   and completion signer-media event IDs, plus the exact rule by which the
   outcome frame and completion event bind each other without a hash cycle;
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
11. the effective acceptance-row inventory, replacement/addition semantics,
    and noncompensatory rule; and
12. all frozen topology, A-D fairness, signature-scope, provider,
    implementation, protected-material, E0, and S0 invariants and nonclaims.

## 7. Mandatory hostile tabletop cases

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
- any claim that RFC 9381 section 5.4.5 contains the decimal coordinate or
  four encodings; and
- any topology, A-D opportunity, signature-scope, closed-gate, or claim-limit
  regression.

Agreement with prose is not evidence. Every handled mutation must trace to one
exact fail-closed rule and observable record. An unhandled or multiply
interpreted mutation is a finding.

## 8. Finding-specific closure criteria

### 8.1 `TRI2-M01`

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

### 8.2 `TRI2-m01`

Pass only if the false RFC attribution is removed and the four exact 32-byte
encodings follow from a complete, independently checkable derivation or an
official primary source that actually contains them. The strict nonidentity
order-`L` acceptance predicate must remain unchanged, and a future independent
implementation reviewer must still reproduce construction, canonical
decoding, and point order rather than trust a copied label.

## 9. Frozen non-regression invariants

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

## 10. Severity and verdict

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
material, provider/model sessions, judge handoff, scoring, E0, or S0
execution.

## 11. Required output and exact next authority

CONTROL authorizes creation of only this one output directory if it is absent:

- `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/`

Do not create any other directory. Inside that directory, write exactly one
Markdown review and one same-basename `.sha256` sidecar:

- `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/trust-root-role-isolation-design-v0.3-independent-rereview.md`
- `s0-lab/reviews/isolation/trust-root-role-isolation-v0.3-rereview/trust-root-role-isolation-design-v0.3-independent-rereview.sha256`

State baseline and independence, all authenticated input hashes, effective
composition, import-outcome reconstruction, vector-provenance reconstruction,
hostile mutation traces, finding dispositions, new findings, effective counts,
verdict, maximum claim, and exact next authority. State explicitly that no
implementation, cryptographic, platform, provider, model, acceptance, E0, or
S0 test was run.

Before relying on the canonical public text-artifact validator, run its
SelfTest. Validate every explicitly admitted input/sidecar pair read-only and
then the authorized review output pair; do not enumerate or validate anything
outside the maximum input set. Preserve every candidate input unchanged.

A zero-finding verdict permits only separate CONTROL integration
consideration. It does not open that gate by itself. After a valid zero-finding
review, the maximum gate the user may separately open is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION CONTROL INTEGRATION DECISION OPEN`

If any finding exists or the review is invalid, no later gate opens
automatically. CONTROL must preserve the result and decide whether to request
a bounded revision, a new evidence repair, or no further action. Downstream
migration, implementation, protected material, provider/model sessions, E0,
and S0 remain closed in every verdict.

After this brief pair itself passes canonical validation, is committed as the
exact two-path child required by section 3, and is published for an
authenticated handoff, the maximum gate the user may separately open is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION INDEPENDENT REREVIEW OPEN`

That gate is not opened by this brief and remains distinct from the later
CONTROL integration gate available only after a valid zero-finding rereview.
