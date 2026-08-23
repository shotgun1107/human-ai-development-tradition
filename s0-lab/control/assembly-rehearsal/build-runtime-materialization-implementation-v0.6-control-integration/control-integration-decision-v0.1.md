# S0 v0.14 public build/runtime materialization implementation v0.6 CONTROL integration decision v0.1

- `decided_at`: `2026-08-23T22:33:39.7686726+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION IMPLEMENTATION V0.6 CONTROL INTEGRATION AND MAIN MERGE OPEN`
- `origin`: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- `initial_origin_main`: `64077a5862aa5678a83ba2f9f48fc71493ed2808`
- `decision_worktree_branch`: `codex/s0-build-runtime-materialization-implementation-v06-control-integration`
- `decision_input_branch`: `codex/s0-build-runtime-materialization-implementation-v06-review`
- `decision_input_commit`: `437c0f8de349068a374a4476310b3e216c8ef542`
- `decision_input_tree`: `63892a4cfbdb47666a411098bc064817aba95281`
- `reviewed_candidate_commit`: `5cddbd929a3c728489019eb0e7de81f2020dab48`
- `reviewed_candidate_tree`: `aa1d500e046cb0f00a9f660f5be7cfedf8365622`
- `reviewed_candidate_parent`: `a2c2ccf4d4d96b6ffd5fba4a2cf5d7885d46b600`
- `decision`: `ACCEPT-FOR-PUBLIC-BUILD-RUNTIME-MAIN-INTEGRATION-ONLY`
- `external_pin_status`: `BLOCKED-MISSING-EXTERNAL-PIN`
- `build_execution_authorized`: false
- `runtime_materialized`: false
- `native_process_provider_action`: none
- `rehearsal_S0_E0_status`: not run or opened
- `F0_content_access`: none

## 1. CONTROL decision

CONTROL accepts the exact authenticated PUBLIC, nonexecuting v0.6
prerequisite-layer revision and its zero-finding independent review for main
integration only.

The accepted implementation reconstructs fresh exact child values at every
exported runtime/DLL aggregate boundary. The independent review reports that
the prior v0.4 findings and `BRM-I05-IR-001` are closed, with zero blocking,
major, or minor findings.

This decision does not provide the ten missing external pin classes. It does
not compile, build, materialize, load, publish, quarantine, call a native API,
launch a process, contact a provider/model, run a rehearsal, or execute S0/E0.

## 2. Authenticated identities and evidence

| Artifact or identity | SHA-256 or Git identity | CONTROL use |
|---|---|---|
| root `AGENTS.md` | `7b2e50a55ed2bf3b92ecbfd1e418f018ca51f2a85c5eac0b9d0c9bdf59169b86` | current role, Git publication, and F0 access boundary |
| canonical text validator | `b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3` | Markdown and sidecar validation |
| v0.6 README | `6c452b11490e2bdb2f8912f998ed7b134c8e3f6380851bef418bc23b8cc503a5` | candidate scope and maximum claim |
| v0.6 implementation manifest | `c653931163e1818fe17b0f53b7d7e6d9e843cde3eea8752b952c8b30dd796798` | exact ten-target implementation binding |
| v0.6 candidate report | `af0208998a3733c6a23d54772945e1f3121b7eed9aa40261070285e48d54bf8e` | author-side finding disposition and evidence |
| v0.6 verification manifest | `b4551c3f8b79d6a56a7a48fda0e595a0da5523f64bdcdccf5122cb12e2f87b06` | exact six-target verification binding |
| v0.6 independent review | `821dc552b91efe1e7590b449e5e407b58ea9989590ac7149526e926c45a8f263` | fresh zero-finding independent evidence |
| v0.5 independent review | `3a1a219bf41a5d38cf1b4df3545ee44ab96b8e4cdea314e0565f9f6593575c68` | predecessor major-finding boundary |
| initial remote main | `64077a5862aa5678a83ba2f9f48fc71493ed2808` | exact compare-and-swap base |
| reviewed candidate | commit `5cddbd929a3c728489019eb0e7de81f2020dab48`; tree `aa1d500e046cb0f00a9f660f5be7cfedf8365622` | reviewed implementation identity |
| review input | commit `437c0f8de349068a374a4476310b3e216c8ef542`; tree `63892a4cfbdb47666a411098bc064817aba95281` | accepted pre-decision lineage tip |

The implementation and verification manifests authenticated ten and six
targets respectively. Their union plus the verification manifest itself is
the exact 17-file v0.6 candidate namespace. The review pair adds exactly two
PUBLIC records.

The canonical validator SelfTest passed all eleven named cases before use.
The v0.6 candidate report and independent review pairs passed every
independently labeled UTF-8, BOM, final-LF, trailing-whitespace,
sidecar-format, and sidecar-hash check.

## 3. Finding closure and nonregression

The v0.5 review returned `REVISE-AND-REVIEW` with one major finding:
`BRM-I05-IR-001`. It showed that aggregate validators could accept exact child
dataclasses whose fields had been reflectively mutated after construction.

The v0.6 candidate reconstructs and stores fresh exact values for:

- all eight `RuntimeRow` fields;
- all three `DllRow` fields;
- all four `DllDirectoryDiagnostic` fields; and
- all seven `DllResolutionRowDiagnostic` fields.

The v0.6 independent review reports `BRM-I05-IR-001` closed. It also reports
the three authenticated v0.4 findings closed: exact target-row
reconstruction, RFC 8785 UTF-16 property ordering, and exact-string manifest
logical-path validation.

No accepted diagnostic becomes execution authority. Runtime/DLL plan and
schema surfaces remain fail-closed without the required external pins.

## 4. Verification evidence

The authenticated-snapshot verifier passed all 30 shipped PUBLIC synthetic
tests with no failure, error, or skip. It reported:

- exact candidate and design-manifest authentication;
- snapshot-only test execution and original-input swap sentinel success;
- zero candidate filesystem, process, native, network, or provider calls;
- `BLOCKED-MISSING-EXTERNAL-PIN`; and
- false build-execution, runtime-materialization, and rehearsal fields.

The fresh independent review additionally reports 770 logical checks:

| Independent surface | Checks | Result |
|---|---:|---|
| runtime rows and aggregates | 181 | no unexpected acceptance |
| DLL rows, directories, resolutions, and aggregates | 220 | no unexpected acceptance |
| adjacent authority, codec, record, schema, and blocked-plan surfaces | 121 | no unexpected acceptance |
| independent contract reconstruction | 248 | no unexpected divergence |

Review orchestration used a temporary PUBLIC snapshot and a Python unittest
child. Those are reviewer actions, not candidate process or runtime evidence.

## 5. Intentionally blocked boundaries

The ten external pin classes remain unavailable. Accordingly, design-bound
runtime/DLL planning, physical directory identity, schema dependency closure,
native source/toolchain/build, PE inspection, runtime materialization,
publication, quarantine, filesystem close/readback evidence, platform
behavior, and operational execution remain blocked.

This integration does not establish Windows behavior, operational safety,
economic value, production readiness, model-to-model transfer, the central
system, or Project Brain integration.

## 6. Exact main-integration lineage and conditions

The accepted Git history is a linear, zero-merge descendant of the exact
initial `origin/main` commit. From `64077a5862aa5678a83ba2f9f48fc71493ed2808`
through the v0.6 review tip there are 23 first-parent commits and no merge
commit. The range contains 207 added PUBLIC paths, zero modified paths, zero
deleted paths, and zero paths outside the approved build/runtime
materialization design, implementation, review, and CONTROL lineage.

Main integration is permitted only if all of these conditions hold:

1. this decision Markdown and its canonical sidecar are the only new paths;
2. the decision input remains commit `437c0f8de349068a374a4476310b3e216c8ef542`
   with tree `63892a4cfbdb47666a411098bc064817aba95281`;
3. live remote `main` still equals
   `64077a5862aa5678a83ba2f9f48fc71493ed2808` immediately before push;
4. candidate and review manifests, hashes, verdict, and zero-finding count
   remain unchanged;
5. the integration worktree and index contain no unclassified change;
6. aggregate-only F0 inventory remains 32 / 11 / 10, every applicable
   worktree/index/parent comparison is quiet, and every anomaly count is zero;
7. `main` advances only by fast-forward to the exact CONTROL integration tip,
   guarded by the exact old remote-main value; and
8. the post-push remote SHA, tree, ancestry, and F0 aggregates are checked
   exactly once.

No merge commit, pull, rebase, history rewrite, PR, release, branch deletion,
or unrelated cleanup is authorized or needed.

## 7. Decision

**Decision: `ACCEPT-FOR-PUBLIC-BUILD-RUNTIME-MAIN-INTEGRATION-ONLY`.**

CONTROL authorizes the exact accepted linear lineage plus this decision pair
to become the new `main` tip under the conditions in section 6. This decision
does not open any later implementation, external-pin, build, runtime,
platform, rehearsal, S0, or E0 gate.

## 8. Maximum claim

CONTROL has accepted and integrated a PUBLIC, nonexecuting prerequisite-layer
implementation revision that passed its bounded independent review. Nothing
has been compiled, built, materialized, loaded, published, or operationally
executed by this gate.
