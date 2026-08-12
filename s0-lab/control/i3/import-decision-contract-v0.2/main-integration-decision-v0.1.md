# S0 v0.14 I3 public import-decision contract v0.2 main integration decision v0.1

- `status`: main integration decision
- `decision_gate`: `S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 MAIN INTEGRATION DECISION OPEN`
- `decision_base`: `400726402d8a36280cd9a09a7d49f1748b07941b`
- `decision_base_tree`: `d870b7abc177e5bbcc3d856652aac70cd937f448`
- `observed_origin_main`: `0a82a8a091f4aae37b6cf22bd736cc228c420c7f`
- `observed_origin_main_tree`: `f5420e159fb4653651773ebff9adef0f9b7e0d2e`
- `decision`: `APPROVE-SEPARATE-MAIN-FAST-FORWARD-ONLY`
- `implementation_status`: closed

## 1. Decision

The authenticated I3 v0.2 public design lineage is approved for a separately
opened main fast-forward operation.

This decision does not move `main`. It establishes only that, at the observed
remote state, `origin/main` can advance linearly from
`0a82a8a091f4aae37b6cf22bd736cc228c420c7f` to
`400726402d8a36280cd9a09a7d49f1748b07941b` without a merge commit, rebase,
history rewrite, unrelated path change, or F0 inventory change.

## 2. Fast-forward proof

The observed comparison was:

| Check | Result |
|---|---|
| `origin/main` | `0a82a8a091f4aae37b6cf22bd736cc228c420c7f` |
| proposed integrated tip | `400726402d8a36280cd9a09a7d49f1748b07941b` |
| `origin/main...tip` left/right count | `0 / 6` |
| main is an ancestor of tip | yes |
| tip is already an ancestor of main | no |
| main-only commit | zero |
| changed paths | 24 |
| changed paths under approved `s0-lab/control/i3/**` | 20 |
| changed paths under approved `s0-lab/reviews/i3/**` | 4 |
| changed paths outside those public I3 paths | zero |

The six linear commits are:

1. `620f3afaa8dd7c35a55f73465df885f8f4e8d6d7` — I3 public boundary;
2. `c1af996699287c86d5142a96873eedfd78815d4e` — v0.1 design;
3. `d2167aebe6b295b99982bed15f5a0d79720c899d` — v0.1 independent review;
4. `9df5bf8ae4a834fdcb0ca0b89eb03d0e04a6e5bb` — v0.2 bounded revision;
5. `f999454e226d075d8643a5b75a1b7fa93d27acea` — v0.2 zero-finding independent rereview; and
6. `400726402d8a36280cd9a09a7d49f1748b07941b` — CONTROL integration decision.

No commit is omitted between the observed main and proposed tip.

## 3. Evidence and design disposition

The exact accepted design inputs remain:

| Artifact | SHA-256 |
|---|---|
| I3 boundary v0.1 | `9a638245f57fe49b4e3557748f0b37d097d794acc9d9650bac7fc7ea2af50aae` |
| v0.1 independent review | `572c9b41f4a5d6ee09f46ae5909554252f166b6aa27a78ad0f2e6ca04dfecd1c` |
| v0.2 main contract | `f04dae684b7373a4c613c3f0e357ef8266f0bf307e78e78d105cb04168f61594` |
| v0.2 field-and-binding table | `b034fadf16e7b5d11594c6987ba714e791ef2b2d02409589c6e7b90126e2fa02` |
| v0.2 classification table | `82f787c737f0a255970679b4c501b93061de7b7778e10843d71c047aa69ea706` |
| v0.2 implementation/test brief | `182df459eee2877d5c4710794ad7a7c86a56a44abe7ce14d09e629fc1c29ac62` |
| v0.2 independent rereview | `e915ed191a685afe9d6cfbc905f38ab589090535f4435a88a80ddf5d093b9fac` |
| v0.2 CONTROL integration decision | `76f61014ee733f37fb05f3cd22acfc01a23a02b69e926421e76b8279e676b08a` |
| unchanged I2 v0.4 contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |

The independent rereview reported zero blocking, zero major, and zero minor
findings. It independently closed `I3-IR-B01`, `I3-IR-M01`, and
`I3-IR-M02`. CONTROL then accepted the package only for main integration
consideration.

V0.2 is the proposed current I3 design authority. V0.1 remains immutable
historical evidence and is not an alternative implementation choice.

## 4. F0 preservation

The observed `origin/main` and proposed tip both contain exactly:

- 32 tracked entries under the CONTROL F0 family;
- 11 tracked entries under the staging F0 family; and
- 10 tracked entries under the review F0 family.

The quiet diff between main and the proposed tip is zero for all three
families. No filename or content from those default-deny paths was used as a
decision input. Their tracked presence is repository synchronization, not AI
content authority.

## 5. Exact conditions on the later fast-forward

A later `MAIN FAST-FORWARD OPEN` operation may proceed only if it independently
rechecks all of the following immediately before the Git-changing action:

1. live `origin/main` is still exactly
   `0a82a8a091f4aae37b6cf22bd736cc228c420c7f`;
2. the pushed integration source tip is exactly the commit containing this
   decision as a direct child of `400726402d8a36280cd9a09a7d49f1748b07941b`;
3. main is an ancestor of that final source tip and the left count remains
   zero;
4. the source contains only the reviewed 24 I3 paths plus this decision pair;
5. F0 counts remain 32/11/10 and quiet F0 diff from the approved parent is
   zero;
6. the worktree, index, stash, and unclassified local status satisfy current
   repository Git rules; and
7. the operation is a fast-forward only, with no merge commit, rebase, force,
   reset, deletion, or history rewrite.

If live main has moved, any input hash differs, an unexpected path appears, or
the relationship is no longer a fast-forward, the later operation must stop
and report. This decision cannot be stretched to a different main or tip.

## 6. What main integration will and will not mean

After the separately authorized fast-forward, main may claim only that the I3
v0.2 public import-decision **design** and its review lineage are integrated.

It will not mean that any parser, serializer, classifier, finalizer, test
harness, fixture, medium, import route, ledger, witness, registry, key,
signature, VM, platform, provider, model, F0 experiment, E0, or S0 has been
implemented or validated.

The implementation gate remains separate. Main integration cannot open it
automatically.

## 7. Closed actions

This decision does not authorize:

- changing or pushing `main`;
- creating a merge commit, PR, release, tag, or branch deletion;
- implementation or test construction;
- F0 content access or modification;
- fixture/oracle/executor/judge work;
- provider/model sessions, E0, or S0; or
- central-system or Project Brain implementation.

## 8. Decision and next gate

**Decision: `APPROVE-SEPARATE-MAIN-FAST-FORWARD-ONLY`.**

The exact next permissible gate is:

`S0 V0.14 I3 PUBLIC IMPORT DECISION CONTRACT V0.2 MAIN FAST-FORWARD OPEN`

That gate authorizes only the bounded Git fast-forward after all section 5
conditions are freshly reproduced. It does not authorize implementation.

## 9. Maximum claim

At the observed Git state, the complete I3 v0.2 public design lineage is
eligible for a separate exact main fast-forward. Main has not been changed by
this decision.
