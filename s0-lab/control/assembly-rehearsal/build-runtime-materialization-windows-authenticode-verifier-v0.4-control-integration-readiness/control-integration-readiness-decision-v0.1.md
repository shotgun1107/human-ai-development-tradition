# S0 v0.14 Windows Authenticode verifier v0.4 CONTROL integration readiness decision v0.1

- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.4 CONTROL INTEGRATION READINESS DECISION OPEN`
- `decision_worktree_branch`: `codex/s0-windows-authenticode-verifier-v04-control-integration-readiness`
- `decision_base_commit`: `dfa31376f11a7e2267f9ac1aaea38f99c194f846`
- `decision_base_tree`: `c9811dd95ea1de1dc57c5043c9897aec247d345f`
- `reviewed_candidate_commit`: `84f21ecf183b44f67dfab507f732c273d7b70d5a`
- `reviewed_candidate_tree`: `7d2cf3ec835ba4c7a6956c6c641d6a51f1065f09`
- `decision`: `ACCEPT-VERIFIER-V0.4-FOR-RECOVERY-V0.3-REVISION-CONSIDERATION-ONLY`
- `verifier_component_status`: `COMPLETE-BOUNDED-PUBLIC-NO-LIVE-AUTHORITY`
- `direct_parent_integration_status`: `NOT READY`
- `external_pin_bundle_status`: `BLOCKED`
- `F0_content_access`: none

## 1. CONTROL authority and scope

CONTROL accepts the authenticated Windows Authenticode verifier v0.4 only as
a complete bounded PUBLIC no-live-authority component that recovery v0.3 may
consider during a separate revision gate.

This decision does not accept the verifier as a closed external pin for direct
parent integration. It does not close the external-pin bundle, revise or
reauthorize recovery v0.2 or trust-profile v0.2, or create live acquisition,
signature, certificate-store, trust-state, loaded-code, executed-code,
effective-trust, or process evidence.

No compiler, build, bootstrapper, runtime, native API, process, rehearsal, S0,
or E0 action is authorized or executed by this gate.

## 2. Authenticated evidence

The following are authenticated facts supplied to CONTROL; the decision in
later sections is CONTROL's bounded use of those facts.

| Artifact or identity | SHA-256 or Git identity | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `146569c6e263759f7784e863e66916b599081516c4aa79609bd9c2fc4272c316` | current role, continuity, Git, and F0 boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | Markdown and sidecar validation |
| v0.6 CONTROL decision | `d9292c9dd495afebdc6a7fc2b648acef31be0de5f4be418e232c503fa16e33c8` | parent `BLOCKED-MISSING-EXTERNAL-PIN` boundary |
| recovery v0.2 package manifest | `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83` | current recovery-package binding |
| recovery v0.2 selection | `678667606c11131cf6b9850c38d3b8aa833bf39b6eab33cff21f3e550d1f1019` | selected toolchain and preexecution trust requirement |
| trust-profile v0.2 package manifest | `315f89b1b13151ab9abe2aaff7ae64d23afa959ace8bd37f52ec4e872cc807c0` | trust-profile package binding |
| trust-profile v0.2 JSON | `4b854426e61e5b7c9cb8bbe549541813066e02f1b72208de9ad15cc548a6b66c` | current trust-profile machine authority |
| trust-profile v0.2 independent review | `f3e738c3d1bee80014b033e16681cadfdb1847087aa84ac855ee089bc26c7a45` | required revision and alignment boundary |
| verifier v0.4 implementation manifest | `ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c` | exact implementation closure |
| verifier v0.4 verification manifest | `c977c482fc1c7364941072327168d233d31d54f6a7301b4cf3392948294515c1` | exact verification closure |
| verifier v0.4 independent rereview | `8d27c1eacc2f988fe8910b0c4ac8fee769f916d454b13d7c4dee97af3cfaaf58` | bounded PASS verdict and zero blockers |
| verifier v0.4 rereview sidecar file | `294cedc1a2ab18dfb27c1e2a62e95eac877399942275dba06491d8714c39ddb5` | exact preserved review record |
| reviewed verifier candidate | commit `84f21ecf183b44f67dfab507f732c273d7b70d5a`; tree `7d2cf3ec835ba4c7a6956c6c641d6a51f1065f09` | reviewed component identity |
| preserved review lineage | commit `dfa31376f11a7e2267f9ac1aaea38f99c194f846`; tree `c9811dd95ea1de1dc57c5043c9897aec247d345f` | exact readiness-decision base |

The independent verdict is
`PASS-FOR-BOUNDED-WINDOWS-AUTHENTICODE-VERIFIER-V0.4-NO-LIVE-AUTHORITY`
with zero blocking findings. The independent manifest-bound verifier passed
`23 / 23`; authenticated snapshot and swap-sentinel checks passed; and
candidate native, network, provider, and process call counts were zero.

The author README, revision report, and response historically recorded the
final manifest-bound run as pending at authoring time. The later independent
PASS and preserved review supersede that pending status for verifier review
only. Those historical author artifacts remain unchanged and are not promoted
into live evidence.

F0 tracked inventory was `32 / 11 / 10`; no F0 content was accessed, and all
applicable quiet-state and anomaly aggregates were zero.

## 3. Accepted verifier closure

CONTROL accepts these component-level facts:

1. the exact v0.4 implementation and verification manifests bind the reviewed
   verifier package;
2. `BRM-AUTHV03-IR-001` is closed in bounded synthetic and static evidence;
3. the corrected authority namespace and exact manifest union passed the
   independent review;
4. QPC remains the conservative elapsed-time authority, while external
   producer truth and endpoint-clock limitations remain explicit; and
5. the maximum component status is
   `COMPLETE-BOUNDED-PUBLIC-NO-LIVE-AUTHORITY`.

No further verifier revision or independent rereview is required unless
recovery v0.3 changes the verifier contract or supplies an incompatible
authority.

## 4. Parent readiness matrix

| Surface | Status | CONTROL disposition |
|---|---|---|
| verifier v0.4 component | `COMPLETE-BOUNDED-PUBLIC-NO-LIVE-AUTHORITY` | accepted as a bounded input candidate |
| direct parent integration as a closed external pin | `NOT READY` | verifier evidence alone is insufficient |
| external-pin bundle | `BLOCKED` | unresolved pin classes remain |
| recovery v0.3 alignment/revision | candidate consideration permitted | requires a separate exact gate and revision |
| recovery v0.2 package | not revised or reauthorized | retains its existing missing and unresolved pins |
| trust-profile v0.2 | `BLOCKED-REQUIRES-RECOVERY-V0.3-ALIGNMENT-AND-VERIFIER-IMPLEMENTATION` | verifier portion improved; package review dispositions remain |
| build, compiler, bootstrapper, runtime, live native, process, rehearsal, S0, E0 | not authorized or executed | remains closed |

The v0.6 parent decision remains `BLOCKED-MISSING-EXTERNAL-PIN`. Recovery v0.2
still has multiple missing or unresolved pin classes, and its selected
toolchain requires preexecution Authenticode authority. Trust-profile v0.2
still requires recovery v0.3 alignment and revision under its independent
review.

Verifier v0.4 closes only the bounded verifier-implementation portion. It does
not itself revise either parent package or produce live acquisition or trust-
state evidence.

## 5. Unresolved blockers

The external-pin bundle remains blocked until separate authorities close each
required class. In particular:

- producer-time acquisition truth remains external to the verifier;
- effective-trust and acquisition-producer authorities remain undefined for
  parent integration;
- disk-manifest consistency does not prove loaded or executed bytes or atomic
  authority against a mutable hostile host;
- recovery and trust-profile semantics have not yet been reconciled with the
  algorithm-agile verifier contract and review dispositions;
- every external-pin class outside this verifier remains blocked; and
- no live Windows trust, store, native, network, build, runtime, or process
  observation exists.

## 6. Conditions for recovery v0.3 consideration

A recovery v0.3 revision candidate must:

1. bind the exact verifier candidate commit and tree, implementation manifest,
   verification manifest, independent-review Markdown, and review sidecar
   hashes recorded in section 2;
2. reconcile recovery v0.2 with the algorithm-agile verifier semantics and
   every applicable trust-profile independent-review disposition;
3. define the remaining effective-trust and acquisition-producer authorities
   without promoting trusted-host disk consistency into live authority;
4. require process count zero before any authorized execution boundary;
5. leave every other external-pin class blocked until separately closed by
   authenticated evidence; and
6. fail closed on any pin, schema, authority, lineage, or claim mismatch.

These are candidate-revision conditions, not evidence that recovery v0.3 or
the external-pin bundle already exists or passes.

## 7. Decision and next candidate gate

**Decision: `ACCEPT-VERIFIER-V0.4-FOR-RECOVERY-V0.3-REVISION-CONSIDERATION-ONLY`.**

The exact next candidate gate to record, but not open, is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.3 REVISION OPEN`

Only an explicit future opening of that exact gate may authorize a bounded
recovery v0.3 revision candidate. This decision does not open it and does not
authorize direct integration, a build, runtime materialization, native or
process execution, rehearsal, F0 access, S0, E0, a PR, or a `main` merge.

## 8. Maximum claim

CONTROL has accepted verifier v0.4 as a complete bounded PUBLIC no-live-
authority component for recovery v0.3 revision consideration only. The direct
parent is not ready, and the external-pin bundle remains blocked. No actual
external-pin closure, live trust authority, operational safety, economic
value, central-system integration, or Project Brain integration follows.
