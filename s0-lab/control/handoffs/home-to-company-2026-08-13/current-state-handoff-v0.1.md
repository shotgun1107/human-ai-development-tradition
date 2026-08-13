# Home-to-company CONTROL handoff — 2026-08-13

## 1. Purpose and evidence boundary

This record transfers the public Git-tracked work completed on the home PC to
the company PC. Git objects, current repository instructions, canonical text
sidecars, and the named manifests are evidence. Conversation memory is not.

No F0 content or individual F0 filename was opened while producing this
handoff. The three PUBLIC-GIT / AI-CONTENT-DEFAULT-DENY families were checked
only by aggregate inventory and quiet-diff state.

## 2. Git handoff identity

- repository: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- handoff branch: `codex/home-to-company-handoff-20260813`
- public design payload commit:
  `a44e68d2994168a87bbf63d1b9f016496b82908b`
- payload tree: `ccc418fa7ce415718f3facf39cacf62df4872263`
- payload parent: `f336995da41d201a9132246d7fffd0506f9a5a01`
- payload-parent tree: `c3c351b2dcf2fc19364a7b5248c13343ae6345dd`
- locally recorded `origin/main` at handoff preparation:
  `402a4a0ef6ff60c00ddf84b5ea46fdc766f28984`

The final handoff commit and tree are intentionally supplied out of band in
the CONTROL chat after the handoff record itself is committed. A Git commit
cannot truthfully contain its own object ID.

## 3. Past

The authenticated v0.3 independent rereview concluded
`REVISE-AND-REREVIEW` with zero blocking findings and two major findings:

1. the verifier guard could inspect the five known handles but could not prove
   verifier-wide absence of unknown or opposite handles from the frozen call
   surface; and
2. the v0.3 runtime-profile schema did not force every closure predicate that
   the prose design promised.

The predecessor evidence remained unchanged:

- v0.3 design-package manifest SHA-256:
  `c2ecd2931e15a99b68d3e669026342f59a42995268f8b4937ba96e63d731481b`
- v0.3 rereview preservation-record SHA-256:
  `9085e20666fdaa1246e47430993149f103c31c4e0e64652ad57d77bbed42675e`

## 4. Work completed on the home PC

The home CONTROL session created the v0.4 public design candidate under:

`s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/`

The package has six logical artifacts, six same-basename SHA-256 sidecars, and
one six-row package manifest, for thirteen files total.

The material changes are:

- the authenticated neutral preloader constructs the sole exact five-entry
  Windows child-handle list;
- pinned Windows process-creation semantics apply that list;
- the in-process guard validates only the five known locators and makes no
  process-wide unknown-handle absence claim;
- a later real-Windows decoy probe is required to test omitted inheritable
  handles and opposite pipe ends;
- one precreation launch-evidence record is used, while the postcreation
  admission binds its digest, the actual verifier PID, and the exact success
  policy;
- the v0.4 JSON Schema closes platform, PE/import/build provenance,
  process-creation, guard, locator, admission, atomic-root, terminal, and
  semantic-validation fields with explicit required properties and constants;
  and
- the acceptance plan separates static design/schema checks from later
  implementation and Windows-platform probes.

The six-row package-manifest SHA-256 is:

`abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`

## 5. Verification completed

- canonical text validator SelfTest: PASS
- four Markdown artifact/sidecar pairs: PASS
- both JSON documents: strict UTF-8, no BOM, final LF, no trailing
  whitespace, canonical sidecar: PASS
- Draft 2020-12 schema metaschema and generated valid instance: PASS
- required-field deletion mutations: 185/185 rejected
- unknown-property mutations: 28/28 rejected
- constant mutations: 106/106 rejected
- interface-map/schema binding checks: 9/9 PASS
- exact v0.4 change set: 13 files, no outside-scope change
- F0 aggregate: 32/11/10, total 53
- F0 worktree/index/untracked/ignored/special-index differences: 0/0/0/0/0

These are design and static-validation results. They are not a completed
runtime, a real Windows probe, an S0 run, or an effect result.

## 6. Current state

The v0.4 package is a public design candidate only. It has not received a
fresh independent v0.4 rereview and must not be described as integrated or
accepted.

No implementation, key material, protected input, provider/model call,
executor, judge, scoring, S0/E0 run, central system, or Project Brain work was
opened by this handoff.

## 7. Next technical gate

After the company CONTROL session authenticates the final handoff tip and this
record, the natural next gate is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER DESIGN V0.4 INDEPENDENT REREVIEW OPEN`

That gate is not opened by this record. It requires a fresh independent
review role with the exact public allowlist and external commit/tree/hash pins.
