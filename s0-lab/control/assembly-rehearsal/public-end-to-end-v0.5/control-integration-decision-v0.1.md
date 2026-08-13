# S0 v0.14 public end-to-end assembly rehearsal design v0.5 CONTROL integration decision v0.1

- `decided_at`: `2026-08-13T11:01:25.4139975+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.5 CONTROL INTEGRATION DECISION OPEN`
- `decision_worktree_branch`: `codex/s0-public-assembly-rehearsal-design-v05-control-integration`
- `decision_input_branch`: `codex/s0-public-assembly-rehearsal-design-v05-rereview`
- `decision_input_commit`: `64e2d0a77a63564e9621508bff23938b0041c06a`
- `decision_input_tree`: `468f3cd147ddad26ce0b92afcf6c807bc6cefe97`
- `reviewed_design_commit`: `94f6f22c58cb00d047dc0e9ca0b6482024185e62`
- `reviewed_design_tree`: `4953982671a367047164388fb9891fc6bd12fcfd`
- `decision`: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`
- `implementation_status`: closed
- `execution_status`: not executed
- `F0_content_access`: none

## 1. CONTROL decision

CONTROL accepts the authenticated public assembly rehearsal design v0.5
package and its fresh zero-finding independent rereview as eligible for a
separately opened main integration decision.

This decision does exactly four things:

1. adopts v0.3 plus the bounded v0.4 and v0.5 replacements as the current
   proposed public assembly rehearsal design baseline;
2. records the independent design-text closure of `M-07A`, `M-06B`, and
   `N-01` while preserving the v0.4 closures of `M-05A` and core `M-06A`
   plus inherited `M-04`;
3. preserves the distinction between candidate-controller `COMPLETE`,
   same-process live-consumer rehearsal PASS, and offline diagnostic files;
   and
4. permits only a separately opened main integration decision gate.

It does not merge or fast-forward main, implement a controller, execute the
Windows publication ABI, run a rehearsal, access F0 content, or open S0/E0.

## 2. Authenticated decision evidence

| Artifact | SHA-256 | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current role, Git-public/F0-access split, and gate boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | public Markdown validation |
| v0.5 design revision | `849e0655e7f73b78eeb039b09357c48f150c637f8cf527dec2a9990b9d240f5b` | effective bounded successor rules |
| v0.5 interface map | `6c2f5ac03ee6cbfad406e96c5cb35ceb5f548e74f04c37e71307b155a18915a4` | exact record, receipt, event, and authority values |
| v0.5 acceptance plan | `82c1bdcbf74ae4135b1c7b8522e261f8e5124bcde353a87adc924a2908b07e0c` | future implementation and rejection requirements |
| v0.4 rereview response | `70341264ae740f05fabdf78f69bcd8fa4bbf2fe73e6ed764fcb65b4c58827c0d` | bounded author response to three predecessor findings |
| v0.5 rereview brief | `34b73448430d3d9978ed804829cafff630b53965e087314531e1f525380ea625` | independent scope and noncompensatory criteria |
| v0.5 design-package manifest | `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802` | exact five-file design package binding |
| v0.4 independent rereview | `b501acacfb04ce62d8c831b303d2c20e1e0cee5f60290a2aa8e287ca7cdd3942` | predecessor findings and historical evidence |
| v0.5 independent rereview | `7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137` | fresh zero-finding disposition |

The canonical validator SelfTest passed all eleven cases before CONTROL
relied on it. The five decision-critical Markdown/sidecar pairs passed every
canonical check. The interface-map JSON passed strict UTF-8 decoding, BOM
absence, final-LF, JSON parsing, canonical sidecar-record, and content-hash
checks.

The independent reviewer authenticated 192 exact public inputs, found zero
missing or mismatched inputs and zero F0 rows, validated 24 Markdown pairs and
five JSON pairs, and rehashed all 192 inputs unchanged after writing. That is
independent review evidence; CONTROL did not relabel it as implementation or
runtime evidence.

## 3. Git and evidence lineage

The accepted lineage is linear:

```text
78d95cf9a82c40ac33a6b0b3c54979765c96474f
  -> 94f6f22c58cb00d047dc0e9ca0b6482024185e62
  -> 64e2d0a77a63564e9621508bff23938b0041c06a
```

- `78d95cf` contains the authenticated v0.4 independent rereview;
- `94f6f22` adds exactly the v0.5 public design package; and
- `64e2d0a` adds exactly the fresh v0.5 independent rereview pair.

The CONTROL decision worktree began clean at `64e2d0a`, tree
`468f3cd147ddad26ce0b92afcf6c807bc6cefe97`. The reviewed design commit is
its sole parent. The inherited PUBLIC-GIT F0 inventory remained 32/11/10 and
the reviewed lineage changed none of those three path families.

No candidate or review input was modified during this decision.

## 4. Finding dispositions accepted by CONTROL

### 4.1 `M-07A`: closed at public design-text level

Receipt-v2 has exactly 21 fields and binds the current authorities:

- `S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2`;
- `S0-PUBLIC-ASSEMBLY-PUBLICATION-OBSERVER-2`;
- `S0-WIN64-NTFS-MOVEFILEEXW-CTYPES-ABI-2`;
- the exact run-record-v3 hash;
- the exact v0.5 design-package-manifest file hash;
- the fresh approving v0.5 rereview Markdown hash; and
- a separately authenticated future public implementation-manifest hash.

Every admissible three-digest tuple serializes to exactly 1,173 bytes. Actual
receipt bytes and SHA-256 correctly remain closed until the true future
implementation manifest and the other two exact external pins are all
available. A placeholder, predecessor pin, candidate-selected pin, malformed
digest, stale authority ID, or old record hash is inadmissible.

### 4.2 `M-06B`: closed at public design-text level

Run-record-v3 has exactly 38 fields, 2,224 bytes, and SHA-256
`73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6`.

Its `COMPLETE` state means only that the candidate controller finished. Its
result remains `candidate-controller-complete-awaiting-live-consumer`, and
all retained post-process artifacts are
`offline-not-success-diagnostic-only`. Only same-process
`S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2` atomic acceptance may issue rehearsal
PASS. The predecessor 36-field, 2,046-byte pass-valued record is not an
alternative authority.

### 4.3 `N-01`: closed at public design-text level

The event has two disjoint last-error paths:

- zero signed return: immediately read `ctypes.get_last_error()` and record
  the captured unsigned 32-bit failure code; and
- nonzero signed return: do not read last error and record literal integer
  zero as the not-sampled-on-success sentinel.

The signed return and terminal status disambiguate a captured failure code of
zero from the success sentinel. No last-error value grants success by itself.

### 4.4 New findings

The fresh independent rereview reported:

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |

Its exact verdict was
`PASS-FOR-PUBLIC-IMPLEMENTATION-CONSIDERATION-ONLY`.

## 5. Effective public design baseline adopted

CONTROL adopts only the following public design claims:

1. the effective composition is v0.3 plus the bounded v0.4 replacements plus
   the bounded v0.5 replacements;
2. the literal 64-bit Windows `MoveFileExW` ABI, verifier-parent observer,
   candidate-child IPC restriction, private capability and witness, exact
   two-event trace, file-identity continuity, and one-use live consumer remain
   required future behavior;
3. run-record-v3 is the only current record schema and is diagnostic rather
   than PASS authority;
4. receipt-v2 is the only current receipt schema and requires all three
   externally authenticated current pins;
5. copied files, copied or replayed witness-like objects, stale pins,
   replacement files, missing or malformed move events, consumer failure, and
   process restart cannot yield rehearsal PASS;
6. inherited M-04 failure routing, four output names, five counters,
   deterministic repeat, quarantine, fixed bundle/case/request/grant/stub,
   and I2/I3 no-import dispositions remain unchanged; and
7. every implementation, platform-execution, F0, provider/model,
   executor/judge, S0/E0, central-system, and Project Brain boundary remains
   closed.

The v0.1-v0.4 packages and reviews remain immutable historical design and
correction evidence. They are not competing current authorities.

## 6. Noncompensatory conditions

Main integration consideration is allowed only while all of the following
remain exact:

1. the v0.5 design-package and rereview hashes in section 2;
2. the linear design-to-rereview ancestry in section 3;
3. zero findings in the authenticated v0.5 rereview;
4. the 38-field/2,224-byte run-record-v3 and its frozen hash;
5. the 21-field/1,173-byte receipt-v2 contract and its three external pin
   meanings;
6. the distinction among controller COMPLETE, live-consumer PASS, and
   offline diagnostic files;
7. unchanged F0 aggregate inventory and no F0 content access; and
8. no implementation, platform, rehearsal, provider/model, S0, or E0 claim.

Any mismatch blocks main integration consideration. A later commit or merge
cannot silently replace the reviewed bytes or reinterpret a historical value
as current authority.

## 7. Gates that remain closed

This CONTROL decision does not authorize:

- public assembly controller, FFI wrapper, observer, capability, witness,
  live consumer, receipt builder, verifier, tests, or manifests;
- Windows, NTFS, process, filesystem, VM, sandbox, account, or provider
  provisioning or execution;
- public assembly rehearsal execution or any claim that it passed;
- F0 content access, hidden-oracle, fixture, executor, judge, scoring, E0, or
  S0 work;
- central-system or Project Brain implementation, operational safety,
  economic value, production readiness, or model-to-model transfer; or
- main merge, fast-forward, PR, release, branch deletion, commit, or push.

The current maximum claim remains authenticated public design acceptance
only. No operational system has been implemented or validated by this gate.

## 8. Decision and next gate

**Decision: `ACCEPT-FOR-MAIN-INTEGRATION-CONSIDERATION-ONLY`.**

The exact next permissible gate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL DESIGN V0.5 MAIN INTEGRATION DECISION OPEN`

That gate may decide whether this authenticated v0.5 design and review
lineage should be integrated into main. It does not itself perform a merge or
fast-forward and cannot open implementation automatically.

## 9. Maximum claim

CONTROL has accepted the authenticated zero-finding public assembly rehearsal
design v0.5 package for a separate main integration decision. No controller,
Windows ABI behavior, observer, witness, consumer, receipt instance,
rehearsal, F0, provider/model, S0/E0, central-system, Project Brain,
operational, economic, production, or transfer result follows from this
decision.
