# S0 v0.14 trust-root and role-isolation design independent-review brief v0.1

- `status`: design candidate
- `review_kind`: fresh public-only hostile design review
- `claim_kind`: next-gate consideration only

## 1. Reviewer independence

The reviewer must be a fresh session that did not author this design, did not
author an implementation derived from it, and has not read sealed material,
an oracle, bank contents, labels, condition maps, executor outputs, E0 material,
or another reviewer conclusion about this trust-root/isolation candidate. The
authenticated v0.14 predecessor review is an allowed CONTROL-integrated
baseline record and does not violate that independence rule.

The review must use a separate clean worktree at the exact candidate commit.
Worktree separation prevents edit collision; it is not cited as a secrecy
boundary.

## 2. Maximum public input set

The eventual CONTROL handoff must freeze exact paths and SHA-256 values. The
maximum substantive set is:

1. repository-root `AGENTS.md` at the candidate commit;
2. `s0-lab/control/s0-protocol-v0.3.md` and sidecar;
3. the v0.14 universal response contract and sidecar;
4. the v0.14 public falsification plan and sidecar;
5. the v0.14 review response and sidecar;
6. the v0.14 independent review and sidecar;
7. the F0-PUBLIC v0.14 CONTROL integration decision and sidecar;
8. the I1 public runtime v0.2 CONTROL integration decision and sidecar;
9. the authenticated I1 public topology specification, public manifest, and
   implementation binding manifests;
10. `trust-root-role-isolation-design-v0.1.md` and sidecar;
11. `role-position-isolation-matrix-v0.1.md` and sidecar;
12. `isolation-acceptance-plan-v0.1.md` and sidecar; and
13. this brief and sidecar.

The reviewer may use the official public references linked by the design only
to verify platform or cryptographic facts. It must report any fact that cannot
be reproduced from those primary sources. No repository-wide search is
authorized by this brief.

## 3. Required hostile tabletop review

This is a design review. The reviewer must not provision a VM, change a host
setting, create a key, create a synthetic canary or fixture, write a test
script, invoke a model, or execute the implementation acceptance plan. Those
actions remain closed until a later implementation gate. The reviewer instead
constructs concrete tabletop mutations and traces each one to a unique
documented reject rule; an unhandled mutation is a finding.

The reviewer must independently reconstruct and trace:

- 32 aggregated rows, 40 positions, eight paired rows, 22 signer IDs, one
  out-of-matrix root authority, 27 stores, and 64 edges;
- exact mapping from every role position to signer identity or `none`;
- the four identity domains, disposable actor VMs, campaign-lifetime signer
  appliances, non-row root, and TCB infrastructure;
- one-position/one-invocation/new-VM semantics, exact eight future executor
  instances with maximum concurrency three, and all paired-role separation;
- no-NIC, no-Enhanced-Session, no-redirection, no-host-share, no-PowerShell-
  Direct, no-Git, and no-ambient-vault claims;
- exact input-ISO/output-VHDX/ingestion/staging direction, hostile filesystem
  rejection, temporary-replica lifecycle, and TCB mediator limits;
- omission-is-denial for every store and edge, including registrar payload
  exclusions;
- immutable object admission, duplicate rejection, and the need for later
  atomic E51/E54 implementation;
- noncircular external commit/anchor pinning and exact root-first registry
  verification;
- exact 22-entry v1 uniqueness, fixed order, root equality, key-ID computation,
  and root-only signature;
- 21 non-root PoP proofs, root registry-signature possession evidence,
  commitment/transcript binding, and exact external activation record;
- private-key custody, signer-appliance persistence, signing-domain/replay
  restriction, compromise stop, and absence of in-place v1 rotation/revocation;
- every signature-bearing public artifact classified exactly once as section-4
  or `inherited-signature-unresolved`, with no silent registry extension;
- exact E48 receipt plus E51 `A-0fff` commitment before E49 release;
- every acceptance-plan expected result for falsifiability, without executing
  it;
- the explicit `external-provider-isolation-unresolved` and
  `signer-custody-provider-unresolved` implementation blockers;
- the distinction between a public design, a later implementation, and an S0
  result; and
- all host-administrator, hypervisor, physical, side-channel, operator, and
  secure-erasure nonclaims.

At least one concrete mutation must be constructed on paper for each platform,
channel, hostile-filesystem, route, pair-independence, signer-custody,
key/registry, lifecycle, and claim-limit class, with the expected rejection
traced to exact candidate text. Agreement with author prose is not evidence.

## 4. Finding severity

- `blocking`: the design can expose a protected asset, destroy required role
  independence, create a circular/unverifiable trust root, contradict the
  frozen v0.14 topology, or cannot be implemented without opening a closed
  gate.
- `major`: a required route, custody rule, lifecycle transition, negative test,
  failure behavior, or security/nonclaim boundary is ambiguous or incomplete.
- `minor`: a bounded defect that cannot grant access, change experimental
  meaning, hide failure, or weaken independence, but still requires exact
  correction.

Severity may not be reduced because two reviewers or two implementations make
the same mistake.

## 5. Allowed verdicts

- `PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`: zero blocking, zero major,
  and zero minor findings.
- `REVISE-AND-REVIEW`: any blocking, major, or minor finding exists.
- `INVALID-REVIEW`: baseline, hash, input boundary, role independence, or
  evidence preservation failed.

No verdict authorizes implementation, key generation, protected S0 material,
executor creation, model calls, scoring, or S0 execution.

## 6. Required output

The reviewer writes one Markdown record and one same-basename SHA-256 sidecar
under a CONTROL-approved `s0-lab/reviews/isolation/` path. The record must state
baseline authentication, every input hash, independent reconstruction counts,
tabletop mutations traced, finding-by-finding evidence, exact verdict, maximum
claim, and exact next gate. It must state that no implementation test was run.
It must be validated with the canonical public text artifact validator before
transfer.
