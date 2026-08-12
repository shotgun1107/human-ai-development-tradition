# S0 v0.14 I2 public implementation v0.4 CONTROL integration decision v0.1

- `decided_at`: `2026-08-12T10:56:28.2046675+09:00`
- `decision_role`: `CONTROL`
- `user_gate`: `S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 CONTROL INTEGRATION DECISION OPEN`
- `source_branch`: `codex/s0-trust-root-role-isolation-public-implementation-v04-control-integration`
- `review_evidence_tip`: `66afb460cc6a166872bf3936a459cd4b9ab05ee4`
- `review_evidence_tree`: `433931edd62dc44ca1494148243c68f5bba30867`
- `reviewed_candidate_commit`: `cfb532f72a1434095e2a7af754e9f7c414e3b888`
- `reviewed_candidate_tree`: `1aadf50b88c7c6fa1de56f6582739dc65e6f1a43`
- `candidate_parent`: `5e374933a80fd89afb85649c83353317d40581ec`
- `candidate_parent_tree`: `c4009b80735df3c0b39aff8bbfc5d2c6ab94575b`
- `decision`: `APPROVE-PUBLIC-IMPLEMENTATION-INTEGRATION-ONLY`
- `claim_kind`: bounded public model-free construction only

## 1. Decision

CONTROL approves the authenticated I2 public implementation v0.4 candidate
for integration as the current bounded public construction lineage within
`central-system-v2.1-s0-preparation`.

This decision accepts the candidate's public byte codec, structural lifecycle
checks, caller-supplied trace and route-set checks, authenticated public input
bindings, and ceiling-free nonnegative integer sequence normalization. It does
not accept or claim an actual trust root, operational role isolation, key or
registry authority, durable ledger or witness, platform isolation, provider or
model execution, E0, or S0.

The predecessor v0.2 and v0.3 candidates and their reviews remain immutable
history. Their defects are not erased or retroactively described as passes.
The effective implementation candidate is v0.4 together with its exact
authenticated public sources and the accepted independent review.

## 2. Authenticated decision evidence

| Evidence | SHA-256 or Git identity |
|---|---|
| candidate commit | `cfb532f72a1434095e2a7af754e9f7c414e3b888` |
| candidate tree | `1aadf50b88c7c6fa1de56f6582739dc65e6f1a43` |
| implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` |
| implementation-manifest anchor file | `82d0167eaa8bde75b58f5c3bf116de1a91e555f16e7de85444f3eaf6736df00c` |
| public-source manifest | `e55b5945141d77a72880b6a9803e9d98ef0a92669711478bccdda043b0bd95a1` |
| v0.4 public contract | `713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da` |
| candidate README | `e0a89bf910ac4d1945f2ece78242c315a2a0b66760375004e2eb726187c4a9ae` |
| candidate verification report | `2ad17e66cf1cae6d0962c5eb0ca17d79b5419bd8c8f6831afac549332cedb7d4` |
| independent review | `2a7dec6bbbece90ce8da151ead4ce19a64e857e33530729b6983646b68b9693f` |
| independent review sidecar file | `0451ea3300dd8f074ced192e351bd37d54dcd7594f1b5308f673d29dac2cf0df` |
| review evidence commit | `66afb460cc6a166872bf3936a459cd4b9ab05ee4` |
| review evidence tree | `433931edd62dc44ca1494148243c68f5bba30867` |

The candidate commit is the sole parent of the review-evidence commit. The
candidate change set is confined to `s0-lab/i2/**`; the review commit adds only
the independent review Markdown and its same-basename sidecar. CONTROL found
no unrelated tracked change in either step.

The implementation manifest contains 16 authenticated payload rows and binds
the exact 12-row public-source manifest. The manifest anchor contains the exact
implementation-manifest hash. The candidate contract, documentation, tests,
verifier, public sources, and review evidence therefore form one explicit
byte-identified lineage rather than an inferred collection of latest files.

## 3. Independent result accepted by CONTROL

The independent verdict is:

`PASS-FOR-CONTROL-INTEGRATION-CONSIDERATION-ONLY`

| Severity | Count |
|---|---:|
| blocking | 0 |
| major | 0 |
| minor | 0 |

CONTROL accepts these bounded dispositions:

1. `I2-V03-m01` is closed. Both exported global-link and global-chain APIs
   accept a canonical 5,001-digit nonnegative integer exactly like its text,
   use no process-global digit-limit mutation, and return stable project
   errors for invalid forms rather than leaking a raw runtime exception.
2. `I2-V02-M01` remains closed at the caller-supplied-set boundary. Repeated
   or contradictory occurrences of one immutable route identity reject.
3. `I2-V02-M02` remains closed at the caller-supplied-set boundary. Result
   media and all four preallocated event IDs have single ownership, and the
   tested cross-route collision classes reject in either order.
4. No new implementation, contract, documentation, manifest, or closed-gate
   regression was identified.

These are public construction results only. They do not establish project-
lifetime uniqueness, atomic append, durability, appliance behavior, actual
registry authority, or hostile same-process isolation.

## 4. CONTROL verification

CONTROL independently authenticated the candidate and review Git lineage and
re-ran the public checks before making this decision.

- The canonical text validator SelfTest passed all 11 cases.
- Candidate README, candidate verification report, and independent review
  pairs passed every separately labelled UTF-8, BOM, final-LF, trailing-
  whitespace, sidecar-format, sidecar-hash, and overall check.
- The shipped verifier was run with external manifest pin
  `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6`.
- It authenticated 16 implementation rows and 12 public-source rows.
- Unit tests were 38 run, 38 passed, with zero skips.
- Static integrity, public-source integrity, contract CLI, import audit,
  model-free behavior, snapshot stability, and final stability passed.
- Closed boundaries remained `BLOCKED_NOT_EXECUTED`.
- The three F0 path-family aggregate counts remained 32, 11, and 10 with no
  candidate or review change. No F0 filename or content was used.

The author verification report was treated as a claim to corroborate. The
independent review and CONTROL rerun, rather than author assertion alone,
support this decision.

## 5. Effective public implementation boundary

The accepted candidate provides only these bounded public mechanisms:

1. Exact parsing, serialization, and SHA-256 for the 31-line ASCII/LF
   `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` record.
2. Structural validation of the declared `R/A/P/C` lifecycle variants,
   route-local predecessor links, and caller-supplied global predecessor and
   sequence links.
3. Duplicate event-ID, duplicate route-identity, and result-media plus
   preallocated-ID ownership checks within caller-supplied traces and route
   sets.
4. Exact public binding to the I1 signer inventory and frozen public
   `TRI2-VEC-02` evidence.
5. Canonical unsigned decimal handling for exact text and nonnegative integer
   inputs, including values beyond Python's direct integer-to-string safety
   ceiling, without modifying that global safety setting.
6. Explicit fail-closed entry points for exact grammars or authorities that
   are not present in the authenticated public inputs.

The package's frozen dataclasses and private provenance markers are trusted
same-process API discipline. They are not a security boundary against hostile
code in the same Python process.

## 6. Closed gates and nonclaims

This decision does not authorize or claim any of the following:

- exact import-admission or import-outcome grammar not present in the public
  source set, complete outcome classification, project-lifetime uniqueness,
  atomic append, durable ledger, or witness validation;
- key generation, private-key custody, signature or curve operations, anchor,
  registry activation, rotation, revocation, or cryptographic correctness;
- VM, sandbox, operating-system account, ACL, network, clipboard, Git, vault,
  appliance, provider, or platform enforcement;
- protected material, hidden oracle, canonical execution input, fixture,
  condition map, executor, judge, scoring, or statistics;
- provider or model sessions, E0, S0, central-system implementation, Project
  Brain integration, operational safety, economic value, production
  readiness, or model-to-model transfer; or
- `main` integration.

No key, registry, signature, VM or sandbox, provider or model, protected
material, fixture or oracle, E0, or S0 work was performed for this decision.

## 7. Integration and next gate

CONTROL adopts this exact v0.4 candidate and independent-review lineage for
separate `main` integration consideration. This decision pair may be
preserved on its dedicated branch after ordinary commit and push approval.

This decision does not merge, fast-forward, rebase, or otherwise alter
`main`. It also does not open the next gate automatically. The maximum next
gate that the user may separately open is:

`S0 V0.14 TRUST ROOT AND ROLE ISOLATION PUBLIC IMPLEMENTATION V0.4 MAIN INTEGRATION DECISION OPEN`

A later main decision must authenticate this decision pair, the review tip,
the candidate commit and tree, and the exact relationship to the then-current
`origin/main` before granting any main integration action.

## 8. Maximum claim

The maximum supported claim is that the authenticated I2 v0.4 public,
model-free construction candidate closes the three reviewed public API and
caller-supplied-set defects without an identified regression and is approved
by CONTROL for separate main-integration consideration.

No actual trust root, operational role isolation, cryptographic system,
durable authority, provider or model behavior, E0 effect, S0 result, central
system, Project Brain, operational, economic, production, or transfer claim
follows from this decision.
