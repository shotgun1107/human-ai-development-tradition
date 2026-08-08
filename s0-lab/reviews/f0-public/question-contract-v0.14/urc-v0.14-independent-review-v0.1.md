# URC-0.14 independent hostile public-only review

- Review type: `fresh independent hostile public-only design review`
- Review date: `2026-08-08` (KST)
- Repository: `C:\Users\kimsiyeol\Documents\human-ai-development-tradition`
- Origin: `https://github.com/shotgun1107/human-ai-development-tradition.git`
- Branch: `codex/s0-question-contract-v06-review`
- Commit: `5efd521f183e514a55bb814116b4085c0d3eb4a6`
- Gate: `F0-PUBLIC QUESTION CONTRACT V0.14 INDEPENDENT REVIEW OPEN`
- Authority: proposal-text review and CONTROL-integration suitability only

No schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, key generation, model call, scoring, executor work, sealed access, S0 execution, branch change, commit, push, or later gate occurred.

## 1. Input boundary and authentication

**Input-boundary verdict: PASS.** Before substantive reading, the required repository, origin, branch, HEAD, and clean worktree matched exactly. All eighteen allowlisted Markdown files were read in full and no other substantive repository file was inspected. The seventeen required same-basename sidecars each matched the exact Markdown bytes. `AGENTS.md` has no expected sidecar; its independently computed digest is below.

| Exact input | Verified SHA-256 | Authentication |
|---|---|---|
| `AGENTS.md` | `656c84c83b78562a3210b50665f02c1200e2552fa8bd879394085c4fb626cf8d` | computed; no sidecar expected |
| `docs/tradition/s0-e0-boundary-and-parallel-work.md` | `b883aca0bbd3dbaeb8e06846942e23573de85c83f61e32e3c41ed7e4e201918b` | matching sidecar |
| `s0-lab/control/s0-protocol-v0.3.md` | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/universal-response-contract-v0.7-candidate.md` | `11977d20cd7b16be95259571a0b1f5684345bab16dba4271b7d89587368ea62d` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.7/public-falsification-plan-v0.4.md` | `8fd3a942dfbd14c4123f9cd614ead2621f2d8ff93941067e85627d2239519cb7` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.8/public-falsification-plan-v0.5.md` | `b960f6b8d39adfd07e6840f6d06f847b3269fb3bb0e9eeabe5f5a930e982ea0f` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/universal-response-contract-v0.9-candidate.md` | `2cc20e4afe84fead2a28b85a9fe4c77ae0ce3e69155a18eec5278924b936fe47` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.9/public-falsification-plan-v0.6.md` | `f610f7a226f3f03035b8d425079b3643e76687e19b295077ad017c84795d45ae` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/universal-response-contract-v0.10-candidate.md` | `650a1be0fefd3643a2d0be940669038cac1c46d5695613efdb9d5cb3c37b780b` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.10/public-falsification-plan-v0.7.md` | `07edb8ec3044874f39ed60f1a6952eb64e369715fc1501fd309888c9b24d09dd` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.11/universal-response-contract-v0.11-candidate.md` | `ae4620c1b532906538252ed503cf39211c46371d4e1eebdbe9a5ef5136528807` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/universal-response-contract-v0.13-candidate.md` | `994ad92b48bdf5d5bd779a6b2fd13a7bbc13bbfd4420beb7066a26910f7e849c` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/public-falsification-plan-v0.10.md` | `6e82b1586df4fcb4a2c12bae9519ca1a9073ccbdb5ba4fcc33f8d789e3b15973` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.13/review-response-v0.8.md` | `4cf728bce26030c6c41b8d7431c27407ad24e88ae9ef1639ca30cc0fa01efc36` | matching sidecar |
| `s0-lab/reviews/f0-public/question-contract-v0.13/urc-v0.13-independent-review-v0.1.md` | `4098e2060cf5c48677981999fe3fdb1c0683f1cb3a319811a5c64ec41170dd76` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.md` | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md` | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` | matching sidecar |
| `s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.md` | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` | matching sidecar |

No repository-wide search, E0 artifact, sealed/private/oracle material, fixture, schema, runner, implementation, output, web source, or external source was used. Sidecars were authentication metadata only. Worktree separation was treated as edit isolation, not secret isolation.

## 2. Review rule and finding classification

- **PASS** means the authenticated proposal text selects one reviewed construction or route without a result-affecting unlisted choice. It does not mean implemented or validated.
- **FAIL** means a contradiction, missing definition, omitted mandatory payload, unauthorized recipient/store/buffer, unverifiable required check, incomplete topology, or executable counterexample remains.
- **UNCLEAR** means materially different conforming constructions or workflows remain possible.

Finding severities are blocking, major, and minor. The official verdict may be `PASS-FOR-CONTROL-INTEGRATION-ONLY` only when none remains.

## 3. Independent effective-document reconstruction

### 3.1 Exact 31-slot contract

**PASS for byte construction.** U7, U9, U10, U11, and U14 authenticate. Every named heading resolves exactly once. Full and preamble ranges satisfy the published level/order rules, and all 31 predecessor slots are classified once.

The exact source run is slots 1-5 U14; 6-14 U7; 15-19 U9; 20 U10; 21 U11; 22-25 U9; 26-30 U7; and 31 U14. Preamble slots are 2, 6, 12, 17, 23, and 26. Slot 25 is the consecutive U9 sections 8.2-8.5 range. Contract records have no transform fields.

Two independent in-memory reconstructions, one string-slice and one raw-byte heading implementation, agreed exactly:

```text
effective_contract_slots=31
effective_contract_raw_slice_bytes=34100
effective_contract_transformed_slice_bytes=34100
effective_contract_stream_bytes=43633
effective_contract_sha256=9cb737c425abc6e0a794b5c4ec439ec6e336022b93a2d2c8aa719c46a78810e3
```

### 3.2 Exact 25-slot plan

**PASS for byte construction.** P4, P5, P6, and P11 authenticate. P7-P10 are evidence only. Every slot resolves and is classified once. Preamble slots are 12, 17, and 21.

The exact source sequence is P11, P4, P5, P11, P11, P5, P11, P11, P4, P5, P4, P4, P4, P4, P4, P5, P4, P4, P4, P6, P4, P4, P5, P4, P11. The authenticated raw P5 section 8 slice is 721 bytes and contains exactly one ASCII `v0.8` and one ASCII `URC-0.8`. The ordered count-one transforms produce 723 bytes.

Two independent in-memory reconstructions agreed exactly:

```text
effective_plan_slots=25
effective_plan_raw_slice_bytes=71327
effective_plan_transformed_slice_bytes=71329
effective_plan_stream_bytes=79676
effective_plan_sha256=e869a9e9b98a06c782180e3da9acf371bb35db4cb8855cd27c38a7c16471bd4c
```

These are local construction-test results, not stored effective artifacts, implementations, frozen manifests, simulations, signatures, or empirical results. The author response was not used as an expected-value source.

## 4. Required v0.13 finding dispositions

| Finding | Decision | Independent v0.14 assessment |
|---|---|---|
| V13-M01 - E25/E35/E48 receipts delete mandatory payloads | **PASS AT PROPOSAL-TEXT LEVEL** | E25 now puts each exact implementation/mutation-table payload and digest in its matching comparator vault for its matching operator, while only each signed receipt reaches registrar. E35 writes exact agreed map bytes to `analysis-map-vault` for E47. E48 delivers exact frozen anonymous analysis bytes and hash to final decision while registrar receives only the receipt. E27, E29, and E50 use the same explicit split. |
| V13-M02 - pair-only registrar store cannot write bundleless genesis | **PASS AT PROPOSAL-TEXT LEVEL** | ROOT has one exact zero-receipt bundle containing the authenticated integration-manifest hash. Genesis commits to that exact bundle, and E51 atomically appends an envelope/bundle pair for sequence 0 and all fourteen later states. |
| V13-M03 - E25 plural bundle has no assembler or route | **PASS AT PROPOSAL-TEXT LEVEL** | Each isolated builder sends only its own signed receipt to registrar. Registrar verifies and stores immutable copies under fixed tuple keys, and registrar alone assembles the fixed-order bundle after the complete receipt set exists and every lower-bit pair freezes. Neither builder receives the other receipt. |
| V13-m01 - only freeze sequence names v0.10 | **PASS** | Effective slot 7 is now P11 section 6. It names the frozen v0.14 design triplet and sidecars, makes the review record an output rather than its own input, and accepts only exact verdict `PASS-FOR-CONTROL-INTEGRATION-ONLY`. |

No blocking, major, or minor finding remains.

## 5. Payload, receipt-vault, and status-topology audit

### 5.1 Mandatory payload delivery versus registrar exposure

| Edge | Protected payload route | Registrar route | Result |
|---|---|---|---|
| E25 | builder 1/2 exact table bytes plus digest to own comparator vault; own operator is sole reader | two independent fixed-role signed receipts | **PASS** |
| E27 | exact abstract table/rejection summary to `catalog-vault` | one signed digest receipt | **PASS** |
| E29 | exact instance table/rejection summary to `catalog-vault` | one signed digest receipt | **PASS** |
| E35 | exact agreed blinded-map bytes to `analysis-map-vault`; E47 supplies bytes/digest to analysis | one signed digest receipt | **PASS** |
| E48 | exact frozen statistics/decision-input bytes and hash directly to final decision | one signed digest receipt | **PASS** |
| E50 | exact decision record to `final-decision-vault`; E53 supplies it to publisher | one signed digest receipt | **PASS** |

Literal execution therefore leaves every downstream consumer with required bytes. A receipt cannot substitute for a payload, and either registrar store is denied protected payload bytes.

### 5.2 Receipt arrival, storage, replacement, and order

**PASS.** Every status producer sends individual signed envelopes on the named evidence edge. Registrar verifies signer, signature, edge, producer role, artifact kind, digest syntax, and acceptance result before writing an immutable envelope copy to `registrar-receipt-vault` under `(edge, producer_role, artifact_kind)`.

Duplicates, replacement, extra receipts, and late receipts after that edge's status pair reject. Early arrival is explicitly permitted storage, not an ambient buffer. It cannot advance status: bundle construction is forbidden until the complete row-specific set exists and every lower-bit pair freezes. Only registrar reads the receipt vault and constructs bundles; the vault contains no protected payload.

E02 has one producer and exactly three receipt kinds in fixed order. E25 has two fixed producers, one common kind, two separate deliveries, and fixed builder-1 then builder-2 order. Both plurality cases therefore have one authorized construction path.

### 5.3 Executable route attacks

| Attempted construction | Required result under the text |
|---|---|
| place only an E25 receipt in a comparator vault | mandatory payload omission; P0/P1 and equality/stop rules reject |
| send either E25 payload to registrar | protected-payload exposure; reject |
| let builder 1 receive builder 2's receipt or assemble the bundle | denylist and P1 mutation; reject |
| use two E25 receipts signed by one role | fixed tuple key/role/count mismatch; reject |
| replace an earlier receipt at the same tuple key | immutable-key replacement; reject |
| construct E35 or E48 status before a lower-bit pair freezes | registrar assembly timing violation; reject |
| release E49 on receipt arrival without the E48 status commitment | E49 prerequisite failure; reject |

These are construction attacks against the proposal. No implementation or cryptographic execution occurred.

## 6. ROOT, registry, E51, and E52 audit

### 6.1 ROOT and genesis

**PASS.** The ROOT companion is one exact ASCII/LF bundle with v0.14 schema, `edge=ROOT`, `entry_count=0`, and one authenticated CONTROL-integration-manifest SHA-256. It has no receipt entry. Genesis commits to SHA-256 of these exact bytes, not directly to a free manifest field.

The externally authenticated, user-approved integration commit/manifest hash supplies the comparison value. A changed or omitted manifest hash, nonzero count, alternate schema/field order, generic empty bundle, or genesis without the bundle fails ROOT/E51/E52 checks. The bundle has no commit self-reference.

### 6.2 Atomic storage and public verification

**PASS.** E51 is the only `registrar-store` writer and appends exactly one registrar-signed status envelope plus its exact companion bundle atomically for all fifteen states. Partial/duplicate writes reject. E52 is the only read route and delivers all pairs from genesis through the requested digest.

The public status reader starts from the user-approved integration commit and manifest hash, authenticates anchor then root-signed registry, checks ROOT manifest binding, verifies registrar and producer signatures, recomputes receipt, bundle, status, and previous-record hashes, and checks count, order, edge, sequence, prefix mask, state, and increasing time. This verifies custody receipts and exact commitments, not protected contents or empirical truth.

### 6.3 Noncircular root and 22-entry registry

**PASS AT PROPOSAL-TEXT LEVEL.** Trust starts from a later user-approved exact Git commit and anchor hash. The anchor has exact key bytes/key ID and no containing-commit field. Registry bytes fix version, anchor hash, 22 numbered active entries in strict ASCII order, raw keys, recomputed key IDs, and only `control-root-authority` as signer. The anchored key and registry root entry must match. Substitution, duplicate/missing role or key, reorder, inactive status, alternate bytes, or unreviewed rotation rejects.

Key generation, private-key custody, Git integration, signature execution, and operational feasibility remain closed.

## 7. E42-E45 comparison and publication audit

### 7.1 Recipient-verifiable comparison

**PASS.** E42 and E44 outputs are fixed-role signed envelopes whose length-delimited records are identity-free canonical table payloads. E43/E45 bind each source-envelope hash separately from each extracted-record hash, fix left/right roles, bind the common agreed-record hash, and deliver both source envelopes, signed comparison envelope, named comparison digest, and agreed record bytes to every listed recipient.

Comparator operators for E43 and analysis for E45 repeat signature, extraction, role, hash-scope, and byte-equality checks. A missing source, left/right swap, envelope/record hash substitution, alternate extraction, unequal source records, changed agreed record, bad signer, or custodian-only attestation rejects.

### 7.2 Decision publication

**PASS.** E50 stores exact decision bytes while sending only a receipt to registrar. E53 supplies the record/digest to the publisher. E54 atomically writes byte-identical decision bytes and the publisher-signed canonical receipt. E55 delivers both to the terminal reader. E56 returns only the publication-receipt-envelope digest and its signed evidence receipt to registrar. No decision bytes reach registrar.

## 8. Freeze, inventory, and non-regression

### 8.1 V0.14 design-triplet freeze

**PASS.** The only sequence first freezes the three current v0.14 design files and sidecars, then obtains a fresh review. The review record is explicitly an output, avoiding self-reference. The current version and the sole acceptable verdict are exact. Historical v0.10/v0.13 review tokens cannot satisfy the step.

The remaining sequence preserves the 31/25 construction freeze, catalogs, resource benchmark/stops, first-sufficient N, pre-label balance/duplicate checks, independent labels, instance projection, package/runtime freeze, noncompensatory P0-P4 ordering, and pre-map analysis freeze. No inherited balance or freeze obligation was dropped.

### 8.2 Independent inventory facts

Targeted parsing found:

- eight E00 grants and exactly one row for every E01-E56 edge, 64 unique rows total;
- 27 unique literal stores;
- 32 role-matrix rows and 32 role-index rows;
- 22 unique registry roles in strict ASCII order;
- 14 status edges and 17 total receipts: E02 three, E25 two, all others one; and
- 15 permitted prefix status states from `A-0000` through `A-3fff`.

These counts do not prove topology closure. Closure follows only from the route checks in sections 5-7; the counts are inventory tests.

### 8.3 Predecessor non-regression

| Area | Result | Assessment |
|---|---|---|
| 24 response rows / 64 vectors | **PASS** | Direct operation remains only `authorized; none`; 16 H=G=1 vectors reject. |
| response/answer/field consequences | **PASS** | Pre-parse invalidity, membership zeroing, answer-local handling, independent field availability, M5, and P3/P4 consequences are unchanged. |
| semantic atoms and T/F/U | **PASS** | U11 section 4 enters byte-identically at slot 21; strength, permission, causes, selectors, reason judgment, consumption, and P3 Y do not change. |
| record-ID/cause order; target/C4 | **PASS** | Canonical scalar-JSON byte order, outer cause order, target typing, and exact dependent/target/direct branches remain. |
| catalogs | **PASS AS ARITHMETIC/POLICY** | `20+4+4=28`, `7*256=1,792`, `4*10*3*3*5*4*128=921,600`, `1+28+C(28,2)=407`, and `720*2^12=2,949,120`. |
| bank balance | **PASS AS POLICY** | N remains 240-720 and each row has exactly N/24 questions; development-example and duplicate-key exclusions remain pre-label stops. |
| P2 statistics/schedule | **PASS AS UNEXECUTED DESIGN** | Marginals, Bonferroni allocation, fit/audit separation, power rules, and K=N/12 divisibility/four-rotation balance remain. |
| P3 statistics/schedule | **PASS AS UNEXECUTED DESIGN** | Shifted-null probabilities remain within the written range; K=N/8 has residue 2 or 6 and the opposite-rotation construction preserves balance. |
| calls/tokens/resources | **PASS AS ARITHMETIC/POLICY; UNVERIFIED** | N=720 remains 240 P2 plus 720 P3/P4 calls, with inherited token, 240-hour, compute, storage, calendar, signing, and monetary stops. |
| isolation/blinding | **PASS** | Fresh roots, no ambient transfer, opaque schedule, blinded analysis, delayed semantic-map release, no retry, and drift invalidation remain. |
| rollback/publication | **PASS** | Untouched-bank rollback, no waiver, no post-map analysis, exact publication, and status/public-reader routes remain. |
| claim ceiling | **PASS** | A review pass permits at most CONTROL consideration; every implementation, data, key, model, sealed, S0, and effect claim remains closed. |

All pass statements are proposal-text, construction, arithmetic, or policy results. They are not empirical results or implementation evidence.

## 9. Facts, inferences, proposals, and construction tests

### 9.1 Facts established here

- Baseline and all eighteen input digests authenticated.
- Both effective streams have the exact counts and hashes in section 3 under two independent reconstruction methods.
- Literal payload/receipt routes exist for E25, E27, E29, E35, E48, and E50.
- The receipt vault, registrar-only assembly, ROOT pair, E51/E52, registry, E43/E45, and publication paths are normatively connected.
- No blocking, major, or minor proposal-text defect remains.
- No implementation, signature, key, bank, simulation, comparator, model, or S0 execution was inspected or created.

### 9.2 Review inferences

- Authenticated receipts do not prove protected payload truth, but the design no longer confuses receipts with payload delivery.
- Early receipt storage does not create an alternate status order because lower-bit pair freeze is a separate precondition for bundle construction.
- The user-approved commit/manifest and anchor are external future trust inputs, not hidden experimental transfers.
- Exact cardinalities support inventory checking but are not used as topology proof.

### 9.3 Proposals preserved as proposals

- The root, registry, receipt, bundle, atomic write, ACL, comparison, publication, and cryptographic operations remain unimplemented.
- P0/P1 mutation catalogs and all later experiment work still require separate gates and independent evidence.

### 9.4 Local construction tests

- Strict UTF-8 source round trips and exact heading uniqueness passed for every effective source.
- Both P5 transforms had the required count one and added exactly two transformed bytes.
- Inventory parsing found the counts in section 8.2.
- Candidate arithmetic gives N/24 values 10, 14, 18, 22, 26, and 30; N/12 values 20, 28, 36, 44, 52, and 60; and N/8 residues 6, 2, 6, 2, 6, and 2 modulo 8.
- No cryptographic, catalog, comparator, serializer, generator, judge, simulation, model, P0-P4, or S0 run occurred.

## 10. Maximum justified claim and unresolved feasibility

The maximum defensible claim is:

> At commit `5efd521f183e514a55bb814116b4085c0d3eb4a6`, the authenticated URC-0.14 package is an unimplemented public redesign proposal. Its 31-slot contract and 25-slot plan are independently reconstructable. At proposal-text level it closes V13-M01 through V13-M03 and V13-m01, preserves inherited semantics, ordering, C4, catalogs, balance, schedules, statistics, resources, isolation, rollback, publication, and claim ceiling, and has no remaining blocking, major, or minor defect. It is suitable only for CONTROL consideration.

Unresolved feasibility includes synthetic authoring, executor usability, independent agreement, catalog and statistical power, exact model revision, ACL stores, receipt/key custody, Ed25519 operations, atomic writes, durable public delivery, human/compute/storage/calendar cost, and every empirical outcome.

This review does not authorize or establish key generation, CONTROL integration completion, schema, bank, question, answer, fixture, oracle, generator, comparator, runner, simulation, model execution, scoring, public validation, sealed compatibility, representation superiority, S0 success, central-system implementation, Project Brain integration, operational safety, economic value, production readiness, model stability, or model-to-model transfer.

## 11. Exact next-gate limit

CONTROL may consider the authenticated v0.14 public contract/plan and this review under a separate decision. No later gate opens automatically. In particular, do not begin key generation, implementation, data authoring, sealed work, model calls, S0 execution, or E0-dependent work from this verdict alone.

## 12. Final verdict

PASS-FOR-CONTROL-INTEGRATION-ONLY
