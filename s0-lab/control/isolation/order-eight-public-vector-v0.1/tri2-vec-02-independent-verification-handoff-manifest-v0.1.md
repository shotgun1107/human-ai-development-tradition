# TRI2-VEC-02 independent verification CONTROL handoff manifest v0.1

- `status`: public CONTROL launch record candidate
- `authoring_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION HANDOFF MANIFEST AUTHORING OPEN`
- `target_gate`: `S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`
- `candidate_branch`: `codex/s0-order-eight-public-vector-review-input-boundary-r3`
- `candidate_commit`: `bb19e6aaf6cdbd34908670876b5badeff27a6eec`
- `candidate_tree`: `617d6026e4989484ae123cbb9daaf8fdb754e957`
- `claim_kind`: launch-input integrity only; no vector or review result

## 1. Purpose and authority boundary

This record supplies the exact external path and SHA-256 manifest required by
section 2 of `tri2-vec-02-independent-verification-brief-v0.4.md`. It repairs
only the missing CONTROL launch packet that caused independent verification
v0.4 to stop before substantive review.

This file and its sidecar are **not reviewer inputs**. They are CONTROL records
used to construct the fresh review task payload. A reviewer must receive the
exact block in section 4 directly in its task prompt and must not open this
manifest from the repository. Treating this file as a twenty-fifth input would
violate the controlling brief.

The previous `independent-verification-v0.4.md`, all earlier boundaries,
briefs, invalid reviews, and every unlisted repository file remain excluded.
Nothing in this record waives a hash, canonical-format, independence, source,
or failure-closed requirement.

## 2. Frozen Git identity

The fresh reviewer must use a new clean worktree checked out directly at the
candidate commit, not at this manifest-authoring branch or the previous invalid
review branch.

```text
candidate branch = codex/s0-order-eight-public-vector-review-input-boundary-r3
candidate commit = bb19e6aaf6cdbd34908670876b5badeff27a6eec
candidate tree = 617d6026e4989484ae123cbb9daaf8fdb754e957
sole parent = 3c41b54895d105496aa748ffe367939fefd0bd9e
parent tree = 1ce3864bac33d4c98b991016e58edf9dc022cd49
```

The exact parent-to-candidate diff is four additions and no other change:

```text
A  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.md
A  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.sha256
A  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.md
A  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.sha256
```

Any different commit, tree, parent, diff, initial status, or supplied input is
terminal `INVALID-REVIEW` under the controlling brief.

## 3. Manifest construction facts

CONTROL constructed the list from the exact categories in brief v0.4 section
2 and resolved them only through the tracked public index. The list contains:

- two file-specific inputs;
- eleven Markdown/sidecar pairs;
- 24 unique relative paths total; and
- no F0-SEALED, implementation, fixture, oracle, E0, S0, provider/model, prior
  boundary, prior brief, prior invalid review, or manifest path.

All 24 files existed, were tracked, had unique textual paths, and were
byte-identical between the candidate commit and the manifest-authoring base.
The hashes below are ordinary SHA-256 of the complete file bytes, not Git blob
object IDs.

## 4. Exact external reviewer input block

CONTROL must copy the following 24 records byte-for-byte into the fresh
reviewer's task prompt. Do not replace it with a path to this manifest.

```text
c6c8045864b12453050e351e855444216ba363b767bb66b0bd67bb090ce1034a  AGENTS.md
b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3  s0-lab/control/tools/verify-text-artifacts.ps1
6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60  s0-lab/control/s0-protocol-v0.3-canonical-r1.md
88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3  s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256
e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md
41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3  s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256
5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3  s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md
8332a01452c3207321e48b6fde5736ed2ecccda493474ae05cd51f5723fad545  s0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256
19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8  s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md
22333a6d80cd32ddd60947c6ade212331eece9b1e067958fc2264d1882f20f9a  s0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256
f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73  s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md
3765f11d814d1fbacb55b3a3600f642c51d4d2a16d5012bfaa7ba9680fe9f03d  s0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256
82746f7c1b59fd162c1f54dc9e0e3d6d3c86b8ef7dc391fb5a10401e88157344  s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.md
28103747f4c3f9c55eb4f125a2de4365c430e31a001256a2c6cc3a9512dc00ea  s0-lab/reviews/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-v0.4-independent-review.sha256
f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0  s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md
36866659b1c401b5775c581c675b999489d786e7d5feb62cd9afa262de33c9cb  s0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.sha256
a5195c25bf206a31ab59b2ce8e34a092d0e3921b1f252675b3ab7a859cb49668  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.md
07571711e531a5c206bf9e019ec5340a0771f7fefa296d3e68f47846e82ab9a5  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-order-eight-public-vectors-v0.1.sha256
cf10458557273de394a0b119afd2dc61d9301a9e9e6f8bb677926d367e0daf2d  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.md
9638dbc36ef57de0744babea58e0ef10e5c4758b683a5aa3b0aea98a0c832ecf  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-public-derivation-v0.1.sha256
b8f7b5d62da008896797298da2a1c24decc3553c7e120025bcfaf15ccdcd56c3  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.md
011b7c9413977d3003cc621db7aedf186b14dd1dc6a1601a490452d4abed3ef1  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-review-input-boundary-revision-v0.3.sha256
b5a0ce94e7d0008ad3f69b62484b81ecbab81bab38c6cd3d68e83457923ec46c  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.md
f12367fd3edc89bb97e6558541b940d383bb94da441d7c2111fec7640a2ebcc7  s0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-independent-verification-brief-v0.4.sha256
```

## 5. Fresh-review launch rules

CONTROL must create a fresh worktree directly from candidate commit
`bb19e6aaf6cdbd34908670876b5badeff27a6eec` and a fresh review session that
did not participate in authoring, QA, transport debugging, or any predecessor
review. The task prompt must include:

1. the exact target gate;
2. the frozen Git identity and four-path diff from section 2;
3. the 24-record block from section 4;
4. the exact path to brief v0.4; and
5. an instruction to follow that authenticated brief without opening this
   manifest or any excluded predecessor record.

The reviewer must not inherit this authoring conversation, use a subagent, or
receive the previous invalid-review conclusion. The new review branch should
be distinguishable from the historical invalid-review branch. The authorized
output remains the brief's exact v0.4 review pair because the fresh candidate
worktree does not contain the historical invalid output.

## 6. Pre-launch CONTROL checks

Before dispatch, CONTROL must independently require:

- candidate commit, tree, sole parent, parent tree, and four-path diff match;
- initial candidate worktree status is clean;
- the task payload contains exactly 24 unique manifest records;
- every relative path resolves inside the candidate worktree, is tracked once,
  and hashes to the supplied value before any substantive read;
- the manifest file, previous invalid review, and every excluded predecessor
  are absent from the reviewer input list; and
- no F0-SEALED filename, hash, count, or content is supplied or inspected.

If any check fails, do not repair the running reviewer. Stop before dispatch,
correct the CONTROL launch packet, and use a different fresh session.

## 7. Claim and next gate

This authoring step performed path resolution, SHA-256 hashing, Git identity
checks, and public document packaging only. It did not fetch RFC 8032, perform
vector arithmetic, read or assess the candidate vector or derivation content,
generate a key, implement code, create protected material, invoke a provider,
or execute E0 or S0.

After this manifest pair is canonically validated and preserved, the maximum
next gate is a separately opened fresh:

`S0 V0.14 ORDER-EIGHT PUBLIC VECTOR INDEPENDENT VERIFICATION OPEN`

Neither this record nor its publication passes the vector package, opens the
CONTROL final-freeze decision, or authorizes `main` integration.
