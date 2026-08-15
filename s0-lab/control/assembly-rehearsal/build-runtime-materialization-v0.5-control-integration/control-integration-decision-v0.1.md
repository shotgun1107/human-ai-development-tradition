# S0 v0.14 public assembly build and runtime materialization design v0.5 CONTROL integration decision v0.1

- `decided_at`: `2026-08-15T18:30:27.0764176+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN V0.5 CONTROL INTEGRATION OPEN`
- `decision_worktree_branch`: `codex/s0-build-runtime-materialization-design-v05-control`
- `decision_input_branch`: `codex/s0-build-runtime-materialization-design-v05-review`
- `decision_input_commit`: `cda5da15592b1d4937e2331c0d6d4263f681b50f`
- `decision_input_tree`: `46d4fb9d59fa8f6442ed825ad5fe6be944d6a3be`
- `reviewed_design_commit`: `4ff53abe7cfad4be62a61be0423a5a9343abbb21`
- `reviewed_design_tree`: `96c91e176a98217a6d4aef57e420b5d0ad5a8b8d`
- `decision`: `ACCEPT-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY`
- `implementation_status`: closed until the exact implementation gate is opened
- `build_and_runtime_status`: not executed
- `F0_content_access`: none

## 1. CONTROL decision

CONTROL accepts the authenticated public build/runtime materialization v0.5
design package and its fresh zero-finding independent review as the current
design authority for a bounded public implementation candidate.

This decision:

1. composes the authenticated v0.4 package with every mandatory v0.5
   correction;
2. adopts the exact one-position semantic-relation patch and its
   `S0-BRM-SEMANTIC-RELATIONS-5` digest;
3. adopts the single 20-field publication no-replace policy authority and its
   exact JCS-plus-LF digest;
4. retains all nonreplaced v0.4 record, Windows directory, publication,
   runtime, binary, resource, failure-precedence, and claim-boundary rules;
   and
5. permits only a separately bounded public implementation-candidate gate.

It does not compile, build, materialize, load, or execute a runtime. It does
not call a native API, run a rehearsal, access F0 content, or open S0/E0.

## 2. Authenticated decision evidence

| Artifact | SHA-256 | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current role and publication/access boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | Markdown and sidecar validation |
| v0.5 package manifest | `ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c` | exact seven-target package binding |
| v0.5 design revision | `bb16668538fcfd03cf057454de8fc99045f18e395a4a316a7d331c925151de44` | mandatory overlay and claim boundary |
| v0.5 interface map | `c507663d94d69007adff469d986743bf13ac6e098c91f56ef3bb3012b01ca3c0` | relation and policy authority bindings |
| v0.5 profile schema | `e8a59dc3274861f047bc4bb833a365d3fbe4d60690e11d48b3e6704273e33b4b` | closed machine package |
| v0.5 mutation matrix | `cc7dd0b90e6dc350c9601e0462435c9de628a32f3e709c5cf0e245e8da522f8e` | 115-row effective rejection matrix |
| v0.5 acceptance plan | `a20a8bbe75f2f1ced3a061fc32341bc316179a55c2450257b8b213aa2ea69b52` | noncompensatory review requirements |
| v0.4 review response | `0d02b5a108dae870f0ee08da2cecf8b4831af3d141ca224fe0a9a3f2493e17c9` | exact predecessor-finding disposition |
| v0.5 independent review | `5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9` | fresh zero-finding independent evidence |

The canonical validator SelfTest passed before CONTROL relied on it. The
decision-critical Markdown/sidecar pairs passed every canonical check. The
reviewer authenticated the admitted v0.1-v0.5 package chain, independently
reconstructed both corrected authorities, and reported zero blocking, major,
or minor findings. CONTROL does not reinterpret that design evidence as
implementation or runtime evidence.

## 3. Accepted closures

### 3.1 `BRM-V04-IR-001`

The effective 68-entry relation array changes only zero-based index 15 from
the v0.4 underscore spelling to the authenticated v0.3 hyphenated spelling.
Every other index and byte string remains identical. The exact ASCII/LF
preimage is 6,805 bytes and has SHA-256:

`5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`

Direct v0.4 execution and any alternate patch, order, count, grammar, or
digest remain inadmissible.

### 3.2 `BRM-V04-IR-002`

The sole normative policy hash preimage is:

`base_profile.publication_no_replace_policy`

It is the exact closed 20-field object. Its RFC 8785 JCS UTF-8 bytes plus one
final LF total 896 bytes and have SHA-256:

`3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`

The historical 17-field interface-map summary is nonauthoritative. The outer
profile and retained prepublication/final record chain must bind the same
normative digest.

## 4. Nonregression and evidence limit

The effective mutation matrix is the exact 111-row v0.4 matrix followed by
four v0.5 rows, for 115 unique rows. All v0.4 behavior not explicitly replaced
by the two closures remains mandatory.

The maximum accepted claim is public design readiness for a bounded
implementation candidate. No source implementation, toolchain, compiler,
binary, runtime tree, native API behavior, platform behavior, process,
rehearsal, provider/model action, executor, judge, S0, E0, central system, or
Project Brain result follows from this decision.

## 5. Conditions on a future implementation candidate

A future candidate must:

1. authenticate the exact v0.1-v0.5 design lineage before loading candidate
   code or creating a process;
2. implement the effective v0.5 composition, never direct v0.4 fallback;
3. reconstruct and verify both exact preimages and digests above;
4. preserve the retained v0.4 record schemas, publication phase order,
   Windows directory/no-replace transaction, resource values, authority pins,
   runtime/binary rules, and first-failure precedence;
5. exercise the 115-row negative contract with PUBLIC synthetic material
   only; and
6. remain unable to claim a real build, runtime, rehearsal, S0, or E0 result
   until later independently reviewed gates explicitly authorize and observe
   those actions.

Any authority mismatch, missing input, alternate serialization, schema-only
success, direct-v0.4 path, or nonzero F0-access event blocks the candidate.

## 6. Decision and next gate

**Decision: `ACCEPT-FOR-PUBLIC-BUILD-RUNTIME-IMPLEMENTATION-CONSIDERATION-ONLY`.**

The exact next permissible gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION CANDIDATE OPEN`

That gate may create only a bounded PUBLIC implementation candidate and its
PUBLIC synthetic verification material. It does not authorize F0 access,
native/process/provider/model execution, a real build, a rehearsal, S0/E0,
main integration, PR, release, or production claims.

## 7. Maximum claim

CONTROL has accepted the authenticated zero-finding v0.5 public
build/runtime materialization design for bounded implementation-candidate
consideration. Nothing has yet been compiled, built, materialized, loaded, or
executed by this gate.
