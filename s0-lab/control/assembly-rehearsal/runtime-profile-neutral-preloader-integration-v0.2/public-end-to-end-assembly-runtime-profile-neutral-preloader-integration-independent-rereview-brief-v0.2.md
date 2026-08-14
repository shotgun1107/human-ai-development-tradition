# Public end-to-end assembly runtime profile and neutral preloader bounded integration design v0.2 independent rereview brief

## 1. Role and decision

Use one fresh independent public integration-design reviewer. The reviewer is
read-only and judges authenticated Git bytes, not prior conversation, CONTROL
summaries, candidate self-reports, or implementation intent.

Required verdict:

- `PASS-FOR-BOUNDED-ASSEMBLY-RUNTIME-PRELOADER-INTEGRATION-IMPLEMENTATION-CONSIDERATION-ONLY`;
- `RETURN-TO-INTEGRATION-DESIGN-REVISION`; or
- `INVALID-REVIEW` after authentication or input-boundary failure.

PASS requires zero BLOCKING and zero MAJOR. MINOR findings require explicit
CONTROL disposition and do not silently change authority.

## 2. Allowed inputs

The allowlist is a maximum. Do not search the repository broadly.

### 2.1 Policy and validator

- root `AGENTS.md`;
- `s0-lab/control/tools/verify-text-artifacts.ps1`.

### 2.2 Exact v0.2 integration package

Under
`s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/`,
only:

- `design-package-files.sha256`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-design-v0.2.md`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-interface-map-v0.2.json`;
- `integration-interface-map-v0.2.schema.json`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-acceptance-plan-v0.2.md`;
- `v0.1-independent-rereview-response-v0.1.md`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-independent-rereview-brief-v0.2.md`; and
- each logical artifact's same-basename `.sha256` sidecar.

### 2.3 Exact v0.1 predecessor package

Under
`s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.1/`,
only:

- `design-package-files.sha256`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-design-v0.1.md`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-interface-map-v0.1.json`;
- `integration-interface-map-v0.1.schema.json`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-acceptance-plan-v0.1.md`;
- `public-end-to-end-assembly-runtime-profile-neutral-preloader-integration-independent-rereview-brief-v0.1.md`; and
- each logical artifact's same-basename `.sha256` sidecar.

The v0.2 response document is the only admitted repository account of the
returned findings. It is still an author artifact: the reviewer must
independently reproduce each defect premise and judge each proposed closure.
Prior conversation is not evidence.

### 2.4 Exact assembly authorities and relevant sources

- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md` and its same-basename sidecar;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_candidate/constants.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_candidate/controller.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/consumer.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/harness.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/observer.py`;
- `s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/s0_public_assembly_verifier/authority.py`;
- `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/design-package-files.sha256`;
- `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-revision-v0.5.md` and sidecar;
- `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-interface-map-v0.5.json` and sidecar;
- `s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/assembly-rehearsal-acceptance-plan-v0.5.md` and sidecar; and
- `s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.md` and sidecar.

The 32-row manifest must be parsed before target access. Targets outside the
six named source files remain hash-only unless CONTROL expands the allowlist.

### 2.5 Exact runtime/preloader authorities

- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256`;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.4.md` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.4.json` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/runtime-profile-v0.4.schema.json` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.4.md` and sidecar;
- `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.3.md` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-interface-map-v0.3.json` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/public-assembly-runtime-profile-neutral-preloader-acceptance-plan-v0.3.md` and sidecar;
- `s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/public-assembly-runtime-profile-neutral-preloader-design-revision-v0.2.md` and sidecar;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/implementation-files.sha256`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/public-assembly-runtime-profile-neutral-preloader-implementation-candidate-report-v0.3.md` and sidecar;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/integration.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/preloader.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/profile.py`;
- `s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/implementation/s0_public_runtime_preloader/source_audit.py`; and
- `s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-implementation-v0.3/rpnp-implementation-v0.3-independent-rereview-result-v0.1.md` and sidecar.

The v0.4 design manifest may be parsed structurally as its exact six-row
manifest, but only the four target contents named above may be opened or
hashed. Its other two rows remain structural-only. No other manifest target
content is admitted without an exact CONTROL expansion.

## 3. Forbidden inputs and actions

The reviewer must not access F0 content, search broadly, read an unlisted
manifest target, edit files, implement, build, install, materialize a runtime,
load a binary, call a native API, start a child, create an output root, run a
platform probe or rehearsal, access an oracle/provider/network, commit, push,
open a PR, merge, or open a later gate.

F0 checks are aggregate-only: expected inventory `32 / 11 / 10`, with all
local anomaly counts zero.

## 4. Authentication preflight

Before semantic reading, the reviewer must:

1. authenticate CONTROL-supplied exact branch, commit, tree, sole parent,
   upstream, and live remote tip;
2. require clean worktree and index;
3. reproduce every external pin in the design and map;
4. run canonical validator SelfTest and validate every admitted Markdown
   pair;
5. parse both v0.2 JSON artifacts with duplicate-key rejection;
6. meta-validate the schema as Draft 2020-12 when an authenticated local
   validator is available; otherwise state the limitation and perform a
   complete closed-vocabulary schema audit without making a metaschema claim;
7. validate the exact interface map against the schema;
8. require a canonical six-row package manifest with exact hashes;
9. authenticate predecessor manifests before following admitted rows; and
10. complete aggregate-only F0 inventory and quiet checks.

Any authentication or boundary failure is `INVALID-REVIEW`. Do not repair an
input or continue semantic judgment in that role.

## 5. Required adversarial questions

Answer each explicitly:

1. Does v0.2 preserve the current zero-call gap and unconditional live
   fail-close?
2. Is the native preloader now the only possible root creator, with no
   contradictory parent reservation or hidden handle handoff?
3. Can any path, alias, reopen, second create, alternate API, or caller object
   substitute for the retained original root handle?
4. Does the verifier receive only the same-object reduced duplicate in exact
   handle position four?
5. Are post-create failures necessarily quarantined and nonupgradeable?
6. Does every outer transition have one owner and current-run predicate?
7. Is guard binding ordered after verifier resume but before Python import and
   child controller `NEW`?
8. Must the child traverse all ten states, and is `COMPLETE` still explicitly
   nonauthority?
9. Must publication witness issuance, child completion, admission commit,
   preloader reply, and live-consumer spend all occur in the frozen order?
10. Can generic terminal text, process exit, files, hashes, reports, preloader
    `OK`, stale authority, or an offline result produce a false live decision?
11. Do nested failure and terminal states deterministically map to outer
    `REJECTED` without retry or success upgrade?
12. Does `LIVE-CONSUMED` remain bounded same-process acceptance rather than
    official rehearsal PASS, S0, or serialized authority?

## 6. Finding requirements

Every finding must include stable ID, severity, exact file/line evidence,
violated authority, deterministic false-PASS or ambiguity argument, impact,
and smallest correction direction.

Any route that permits a second root creator, path substitution, early root
action, incomplete nested-state composition, premature positive terminal,
child `COMPLETE` as authority, consumer bypass, offline-to-live upgrade, or
release of current fail-close without later evidence is at least MAJOR.

## 7. Verdict boundary

PASS means only that this exact v0.2 public integration design is coherent
enough for separately opened bounded implementation consideration. It does
not approve code, builds, binaries, runtime material, native calls, platform
behavior, live assembly, official rehearsal, F0 or oracle access, S0,
production use, Git publication, or main integration.
