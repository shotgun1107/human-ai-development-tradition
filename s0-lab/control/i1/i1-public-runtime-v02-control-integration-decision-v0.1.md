# I1 public runtime v0.2 CONTROL integration decision

- `decided_at`: `2026-08-09T17:32:10.2199414+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES CONTROL INTEGRATION AND MAIN MERGE OPEN`
- `source_branch`: `codex/s0-i1-public-runtime-v02`
- `review_evidence_tip`: `133c1b6531bcea75637c730e24ae4a0100e42d7c`
- `reviewed_candidate_commit`: `105aa12c93bdbca9b693ae600806d0359d621d7e`
- `pre_merge_main_commit`: `c0f4e09f5566e80ffe08b3a8af30638f53fbcad4`

## Decision

The I1 public runtime v0.2 candidate is **APPROVED FOR CONTROL
INTEGRATION** as the current public, non-semantic S0 implementation-
prerequisite baseline.

The source lineage may be fast-forward merged into `main` together with this
decision and its same-basename SHA-256 sidecar. I1 v0.1, its rejecting review,
the v0.2 revision review, and the final limited rereview remain preserved as
construction, failure, correction, and review evidence. They are not rewritten
as successful predecessor versions.

This decision accepts only the authenticated public construction layer and its
truthfully stated boundaries. It does not accept an S0 result or authorize the
next phase automatically.

## Authenticated identities

| Artifact | SHA-256 |
|---|---|
| `spec/public-runtime-files.sha256` | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e` |
| `verification/implementation-files.sha256` | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` |
| `verification/implementation-manifest.sha256` | `1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6` |
| `i1-public-runtime-independent-review-v0.1.md` | `fbd0a2d730010d3de5c451663836627c0cae55746191a402af3b0cea1c434882` |
| `i1-public-runtime-v02-independent-review-v0.1.md` | `0f488a479d2feaa7de1afc10316e20f635017265ba9d95268993953582dd050d` |
| `i1-public-runtime-v02-minor-rereview-v0.1.md` | `850d1f5f867e1ea8c0a1022933b478774bcc84ad8e3e462fe080659b54da9e23` |
| `i1-public-runtime-v02-minor-rereview-v0.1.sha256` | `a521b0209b12e591dc1ce01827d9eb6c15fabadb6a7be4f7e1d50ca3815d404d` |

The final implementation manifest authenticates exactly 26 payload files.
Together with that manifest and its one-line binding file, the I1 tree contains
exactly 28 tracked regular files.

## Review result accepted by CONTROL

The final independent limited rereview verdict is
`PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`.

- All six major and the original minor I1 v0.1 findings are closed within the
  explicitly limited public construction scope.
- The later exact-string path-contract finding `I1-v02-m01` is closed.
- No blocking, major, or minor finding remains in the final rereview scope.
- The shipped verifier passed with 61 tests: 60 passed and one direct Windows
  symlink-creation test was skipped because the host denied that privilege.
  Privilege-free reparse rejection coverage still ran.
- The independent review separately exercised manifest authority, immutable
  topology, schema/runtime relations, resource bounds, E43/E45 comparison,
  E54-E56 publication bindings, verifier bootstrap, and exact string-path
  behavior rather than treating shipped self-tests as self-proving.

## Public construction accepted by CONTROL

The accepted layer provides:

- an authenticated seven-file public specification namespace;
- the frozen public topology inventory of 32 aggregated role rows, 40 row
  positions, 22 signer role IDs, 27 stores, and 64 edge rows;
- 14 status edges, 15 prefix states, 17 receipts, and 15 E51 pairs;
- exact public codecs and recipient recomputation for the reviewed receipt,
  bundle, status, comparison, and publication records;
- a bounded provider-neutral one-shot boundary with no provider, network,
  retry, tool, or persistent-state implementation;
- externally pinned implementation verification before candidate Python
  execution; and
- exact canonical POSIX-relative string identifiers at the public manifest
  entry boundary.

These are construction properties under trusted injected inputs. They are not
evidence that operational roles, storage, signatures, models, or S0 work.

## Main integration check

At decision time, `origin/main` was exactly
`c0f4e09f5566e80ffe08b3a8af30638f53fbcad4` and was an ancestor of the review
evidence tip. The pre-decision source diff from that `main` contains:

- one approved `AGENTS.md` operating-rule clarification;
- the 28-file public I1 tree; and
- three preserved I1 review records with their three sidecars.

There are no deletions or file-mode changes. The commit containing this
decision may be fast-forward integrated only if the worktree remains clean,
the source lineage still contains the authenticated review evidence tip, the
remote `main` SHA remains the recorded pre-merge value, and the only additional
paths are this decision and its sidecar.

The merge preserves all history already present on `main`, including the
independent E0 lineage and its unchanged status. It does not delete predecessor
branches, reviews, or worktrees.

## Remaining closed gates

The following remain closed unless the user separately and explicitly opens
the exact gate:

- trust-root and role-isolation design or implementation;
- process, VM, sandbox, vault, network, clipboard, or Git isolation setup;
- Ed25519 key generation, private-key custody, anchor, registry, rotation, or
  revocation artifacts;
- store backends, durable ACL enforcement, atomic writes, or duplicate-
  publication prevention;
- benchmark or power analysis;
- bank, label, fixture, projection, package, or hidden-oracle authoring;
- executor creation, provider/model calls, retry, scoring, or statistics;
- sealed-material access or E0 execution; and
- S0 execution, central-system implementation, or Project Brain integration.

No A-D fairness, cryptographic security, operational safety, economic value,
production readiness, model-to-model transfer, central-system behavior, or S0
effect follows from this CONTROL integration decision.
