# URC-0.13 response to v0.12 independent review

- status: **author response proposal; not an independent verdict**
- gate: `F0-PUBLIC QUESTION CONTRACT V0.13 REDESIGN OPEN`
- reviewed predecessor: `s0-lab/reviews/f0-public/question-contract-v0.12/urc-v0.12-independent-review-v0.1.md`
- reviewed predecessor SHA-256: `626c07dad70f6943146974c2c2f19c9998a752b61e429570d78ffe231bfb66dc`
- companion proposal: `universal-response-contract-v0.13-candidate.md` and `public-falsification-plan-v0.10.md`

## 1. Scope and claim discipline

The v0.12 review returned `REVISE-AND-REVIEW` with zero blocking, three major, and zero minor findings. This response proposes bounded corrections for V12-M01, V12-M02, and V12-M03. It preserves authenticated predecessors and the U11 semantic slice rather than editing them in place.

The mappings below are author claims to be attacked by a fresh public-only reviewer. They do not establish closure, integration suitability, implementation, feasibility, validation, S0 success, or any empirical result.

## 2. V12-M01 — plural and digest-only status evidence

### 2.1 Review defect

The v0.12 status record had one `event_artifact_sha256`, while edges could carry multiple hashes or digest-only values. In particular, E25 admitted at least three syntactically possible commitments: either comparator hash or a hash of an unspecified container. There was no unique count, order, role, byte container, or copied-digest rule.

### 2.2 Proposed correction

Plan sections 4.3 and 4.4 replace the ambiguous field with a canonical evidence-receipt and evidence-bundle construction:

- every receipt has one exact ASCII grammar and one role-bound signature;
- a closed 14-edge table fixes receipt count, producer role, artifact kind, and entry order;
- E02 has exactly three named entries and E25 has exactly two fixed-role entries;
- each other status edge has exactly one named entry;
- a digest-only value is copied into `artifact_sha256` and is never rehashed as ASCII;
- length-delimited signed receipt envelopes form one exact bundle byte string;
- the status event commits only to SHA-256 of that entire exact bundle;
- E51 atomically stores the status envelope and its companion bundle, and E52 delivers both.

The public reader can therefore reproduce the one permitted bundle commitment and authenticate its edge, receipt count/order, producer roles, artifact kinds, signatures, and status transition without receiving protected source bytes. This remains a custody receipt, not proof that protected empirical contents are true.

### 2.3 Required hostile checks

The next review should attempt individual-digest substitution, ASCII double hashing, E02/E25 omission/reordering/duplication, wrong signer/kind/edge, alternate length framing, extra receipts, partial E51 writes, and status/bundle swaps.

## 3. V12-M02 — circular and underdefined key registry

### 3.1 Review defect

The v0.12 registry had no canonical record bytes, fixed order, designated signer, or noncircular public trust anchor. A registrar key contained only inside a registrar-signed registry could authenticate itself.

### 3.2 Proposed correction

Plan section 4.1 defines:

- exact CONTROL-root anchor record bytes and raw-key-derived key ID;
- a later user-approved Git integration commit and recorded anchor hash as the verifier's external starting point;
- exact registry record bytes, version, anchor hash, 22 fixed role entries, fixed ASCII order, raw keys, key IDs, and active status;
- exactly `control-root-authority` as registry signer;
- verification of the anchor before the registry and equality between the anchored root key and the registry root entry;
- rejection of signer, role, order, key, byte-form, status, or anchor substitution; and
- no key rotation under registry v1, so any change requires new review and a new user-approved integration root.

The anchor intentionally contains no commit identifier that would make the containing Git commit self-referential. The integration decision binds the already frozen anchor and registry artifact hashes. The current gate creates no keys and opens no integration.

### 3.3 Required hostile checks

The next review should attempt self-signed registrar bootstrap, root substitution, registry reordering, role/key substitution, duplicate or missing role, changed byte serialization, inactive/revoked entry, mismatched root entry, and use before a user-approved integration root exists.

## 4. V12-M03 — impossible E43/E45 recipient recomputation

### 4.1 Review defect

The v0.12 recipient received a comparison envelope and agreed table but not the left/right source bytes it was required to hash and compare. It also failed to distinguish hashes of signed envelopes from hashes of canonical table payloads.

### 4.2 Proposed correction

Plan section 4.5 chooses one explicit reproducible model:

- every E42 judge output and E44 comparator output is a generic signed envelope;
- the envelope's length-delimited `record_bytes` are the exact canonical table payload and contain no signer identity;
- independently signed envelopes may differ, while their extracted table records must be byte-identical;
- E43/E45 records separately commit to each exact source-envelope hash and each exact extracted-record hash;
- E43/E45 deliver both source envelopes, the signed comparison envelope, its digest, and the agreed record bytes to every recipient; and
- each recipient verifies all source and comparison signatures, extracts both record payloads, recomputes every envelope/record/comparison/agreed hash, and performs the byte comparison itself.

Thus the comparison is no longer accepted as an unverifiable custodian attestation. Envelope scope, record scope, roles, extraction, delivery, and equality are independently recomputable from authorized inputs.

### 4.3 Required hostile checks

The next review should attempt invented source hashes, missing source envelopes, bad source roles/signatures, envelope-versus-record hash substitution, left/right swapping, alternate payload extraction, unequal records, agreed-record substitution, and receipt by an unauthorized role.

## 5. Preserved predecessor properties

The v0.13 proposal retains without intentional semantic change:

- the complete U11 semantic atom, availability, strength, permission, cause, selector, C1-C7, consumption, response, and P3 rules;
- the global record-ID and cause ordering repairs;
- the 24-row bank balance, duplicate/example restrictions, schedules, stochastic models, resource ledger, isolation, rollback, and claim ceiling;
- eight E00 grants, E01-E56, 26 named stores, and 32 experimental matrix/index roles; and
- the v0.12 public publisher/reader and E53-E56 decision-publication path.

The plan changes key/signing grants and artifacts only where needed for canonical evidence receipts and recipient-verifiable comparison. The external `control-root-authority` is explicitly non-experimental and outside the 32 experimental role rows.

## 6. Author-side consistency checks required before review

Before freezing this proposal, CONTROL must verify:

1. every named source sidecar and predecessor-review sidecar;
2. unique 31-slot and 25-slot effective constructions;
3. exactly two count-one P5 slot-10 transforms to v0.13;
4. exact inventory of eight E00 grants, E01-E56, 26 stores, and 32 matrix/index rows;
5. exact 22-role registry inventory and ASCII order;
6. exact 14 status edges, with E02 count three, E25 count two, and all remaining counts one;
7. exact root, envelope, receipt, bundle, status, comparison, and publication grammar field order;
8. same-basename sidecars, strict UTF-8 without BOM, LF final newline, no CR, no trailing whitespace, and the exact six-file change set.

These checks are construction and document-consistency checks only. They are not cryptographic execution, key generation, role feasibility, implementation, or experiment results.

## 7. Requested next disposition

After the six v0.13 files freeze and are committed under separate user approval, the appropriate next gate is a fresh public-only `F0-PUBLIC QUESTION CONTRACT V0.13 INDEPENDENT REVIEW OPEN`. The reviewer should receive an exact public allowlist, authenticate every input, independently reconstruct both effective byte streams, attack all three mappings above, and recheck predecessor passes for non-regression.

No schema, bank, fixture, oracle, generator, comparator, runner, simulation, model call, scoring, sealed work, or S0 execution gate is opened by this response.
