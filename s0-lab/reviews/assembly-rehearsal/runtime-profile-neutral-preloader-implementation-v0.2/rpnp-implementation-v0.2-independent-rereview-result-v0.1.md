# Public assembly runtime profile and neutral preloader bounded public implementation candidate v0.2 independent rereview result v0.1

## 1. Decision

- gate reviewed: `S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER BOUNDED PUBLIC IMPLEMENTATION CANDIDATE V0.2 INDEPENDENT REREVIEW OPEN`;
- reviewer: one fresh `gpt-daybreak-blue-latest` independent implementation and security reviewer;
- verdict: `RETURN-TO-IMPLEMENTATION-REVISION`;
- findings: BLOCKING `0`, MAJOR `2`, MINOR `1`;
- bounded test result: `76 / 76 PASS`;
- implementation acceptance: not granted.

The passing test result does not override the two deterministic MAJOR
false-PASS paths described below.

## 2. Authenticated review subject

The reviewer and CONTROL independently authenticated the following Git
identity before relying on candidate bytes:

- repository: `human-ai-development-tradition`;
- candidate branch:
  `codex/s0-rpnp-v02-implementation-revision-v01`;
- candidate commit:
  `34f0422531499e342aecddc9c25c65e074658759`;
- candidate tree:
  `6bd6f6e2deb62e988dc87004b7e74fdbbd9191a0`;
- sole parent:
  `f6f4e2cc1413bb3d9d9dda2b7c4cdb791a04b7f7`;
- parent tree:
  `7a2d4e697abee3383477174310f167db1d554d09`;
- live remote candidate tip: exact commit match;
- candidate worktree and index: clean;
- F0 aggregate inventory: `32 / 11 / 10`;
- F0 worktree, index, untracked, ignored, skip-worktree, and
  assume-unchanged anomalies: `0`.

No F0 content or individual F0 filename was admitted to the review.

The following public authorities and closures authenticated:

- candidate implementation manifest: `11 / 11` exact target hashes;
- candidate implementation-manifest SHA-256:
  `4438611c8b2e06eba8a7c754a96accd1a248a7203c5876fe2eb0d48d0ec87faf`;
- candidate report SHA-256:
  `2453541a90a849c088534c79c9d7738dc1de0651fad9ca1a35d5c707befb06dd`;
- v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving v0.4 rereview preservation-record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- predecessor v0.1 through v0.4 schema pins: exact match;
- existing public assembly implementation manifest: `32 / 32` exact target
  hashes;
- canonical text-artifact validator SelfTest and every admitted Markdown and
  same-basename sidecar check: PASS.

## 3. Independent findings

### 3.1 MAJOR: mutable-after-check runtime-file substitution

Evidence:

- `implementation/s0_public_runtime_preloader/preloader.py:123-151`;
- `implementation/s0_public_runtime_preloader/semantic.py:298-302`.

`NeutralPreloader.prepare` validates `static_material.runtime_files` against
the authenticated manifest and later rereads that caller-held mapping to load
the launch control and launch artifacts. The validated bytes are not captured
into one private immutable snapshot that is used for both validation and
evidence construction.

The reviewer installed a stateful `Mapping` with `object.__setattr__`. It
returned honest manifest targets during validation and attacker-selected
launch-control and application bytes during the later reads. The method then
returned an offline prepared result containing all three
`BYTE_VERIFIED_RELATIONS`, `candidate_only=True`, and the attacker-selected
command line and evidence hashes.

This is a deterministic false-PASS against the claimed raw revalidation and
manifest-bound launch-input guarantees.

### 3.2 MAJOR: caller-controlled locator value in offline admission

Evidence:

- `implementation/s0_public_runtime_preloader/semantic.py:399-409`;
- `implementation/s0_public_runtime_preloader/evidence.py:296,309-311`.

`PostcreationObservation.source` is checked only during ordinary construction.
The public admission path does not reconstruct or revalidate the observation
after the caller can mutate the frozen dataclass with `object.__setattr__`.
The admission builder copies the mutated source into canonical output and
checks forbidden locator tokens only in object keys, not values.

The reviewer changed `source` to `0x0000000000000001`. The public admission
function returned a candidate diagnostic whose raw bytes contained that handle
locator despite the locator-free claim.

### 3.3 MINOR: caller-owned schema retained after audit

Evidence:

- `implementation/s0_public_runtime_preloader/schema.py:65-66`.

`FixedDraft202012Validator` retains the caller's mutable schema dictionary
after its keyword audit. Clearing the caller dictionary after construction
allowed a non-integer value through a validator that had originally required
an integer. The authenticated high-level candidate paths parse private schema
bytes and validate immediately, so the reviewer classified this direct API
route as MINOR rather than MAJOR.

## 4. Test evidence and coverage gap

The independent reviewer ran all bounded suites with
`PYTHONDONTWRITEBYTECODE=1`:

- v0.2 revision suite: `16 / 16 PASS`;
- v0.1 runtime/preloader regression suite: `13 / 13 PASS`;
- existing public assembly candidate regression suite: `47 / 47 PASS`;
- total: `76 / 76 PASS`.

The suites did not contain deterministic regressions for the stateful mapping,
mutated observation source, or post-audit schema mutation routes. Their passing
result therefore demonstrates regression stability, not closure of the three
findings.

## 5. Required minimum revision

A future implementation revision must, at minimum:

1. create one private immutable static-material snapshot at the caller
   boundary and use that same snapshot for manifest verification, launch-input
   loading, identity construction, and evidence construction;
2. reconstruct and revalidate every postcreation observation field at the
   caller boundary and never serialize caller-controlled source or locator
   text into the locator-free admission diagnostic;
3. copy or freeze the schema before keyword audit and retain only that private
   snapshot for validation; and
4. add deterministic regression tests reproducing and rejecting all three
   review probes.

## 6. Boundary and next candidate gate

This result does not authorize a runtime profile, native preloader, native API
invocation, platform probe, public assembly rehearsal, provider or model call,
F0 access, implementation acceptance, CONTROL integration, commit, push, PR,
merge, or main integration.

The next candidate gate, if separately and explicitly opened, is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER BOUNDED PUBLIC IMPLEMENTATION CANDIDATE V0.3 REVISION OPEN`

That gate's role is limited to producing a bounded v0.3 implementation
revision for the two MAJOR and one MINOR findings, adding the three regressions,
and rerunning the bounded offline suites. It does not itself approve the v0.3
candidate, open its independent rereview, materialize a runtime package, call a
native API, run the assembly rehearsal, access F0 content, or authorize Git
publication or main integration.

## 7. Review-session integrity

The independent reviewer made no file change and performed no native or
platform rehearsal, provider call, model call, F0 content access, S0 execution,
commit, push, merge, or PR action. This document is CONTROL's public
preservation of that completed read-only verdict.
