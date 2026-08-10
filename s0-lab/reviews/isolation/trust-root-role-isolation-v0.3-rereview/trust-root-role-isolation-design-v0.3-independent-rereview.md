# S0 v0.14 trust-root and role-isolation design independent rereview v0.3

- review kind: fresh public-only hostile full design rereview
- review date: 2026-08-10 KST
- gate: S0 V0.14 TRUST ROOT AND ROLE ISOLATION INDEPENDENT REREVIEW OPEN
- worktree: C:\Users\SSAFY\AppData\Local\Temp\ai-development-tradition-s0-isolation-v03-independent-rereview
- branch: codex/s0-isolation-v03-independent-rereview
- reviewed commit: bd8c0ce38620df69bff39a1617b651f28613346b
- reviewed tree: 896d0ac1921b19a3fb7fd2845a2776abcdeb6c8b
- verdict: REVISE-AND-REVIEW
- finding count: zero blocking, one major, one minor
- claim kind: public design review only

No implementation, cryptographic, platform, provider, model, acceptance, E0,
or S0 test was run. No VM, account, network, ACL, vault, store, signer, ledger,
witness, key, vector, fixture, oracle, package, executor, or model session was
created or exercised.

## 1. Review authority, independence, and boundary

This reviewer did not author or advise the v0.1, v0.2, or v0.3 candidate, the
operative rereview brief, author-side QA, or any implementation derived from
them. No subagent was used. No earlier v0.3 reviewer conversation or conclusion
was inherited or sought.

The review used only the exact 56-path maximum input set authenticated in
section 2. The predecessor s0-protocol-v0.3 pair, the old v0.3 brief pair,
refreeze-candidate-record pair, limited-rereview-brief pair, every historical
v0.3 review body, sealed or oracle material, bank, labels, condition map,
executor output, E0, implementation code outside the four admitted I1 topology
files, and every other unlisted path were not read. The admitted canonical
limited rereview and CONTROL final-refreeze decision were used only to
establish current canonical-protocol provenance, never as an answer key for
the substantive findings.

No repository-wide enumeration or search was used. Worktree separation is
treated only as edit isolation, not secrecy or independent information
security. Candidate inputs remained read-only. The only writes are the
CONTROL-authorized review Markdown and its same-basename sidecar.

## 2. Baseline and input authentication

### 2.1 Git handoff

Before substantive candidate reading, the following exact facts were
independently checked:

| Check | Required and observed value | Result |
|---|---|---|
| branch | codex/s0-isolation-v03-independent-rereview | pass |
| HEAD | bd8c0ce38620df69bff39a1617b651f28613346b | pass |
| HEAD tree | 896d0ac1921b19a3fb7fd2845a2776abcdeb6c8b | pass |
| parent count | exactly one | pass |
| exact parent | f49d8bd04299a38a7417c2cafe96907acca5e4e5 | pass |
| parent tree | cc2aa37f56ec665c56ad6cb5b7b16aafb4fc3e0e | pass |
| parent-to-candidate diff | exactly the operative v0.4 brief Markdown and sidecar, both added | pass |
| initial porcelain status | zero entries | pass |

The exact added paths were:

1. s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.md
2. s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.sha256

### 2.2 Exact 56-file SHA-256 authentication

Every supplied path existed and its independently computed file SHA-256
matched. The values below are file hashes; for a sidecar row, the value is the
hash of the sidecar file itself.

| # | Exact input | Verified SHA-256 |
|---:|---|---|
| 1 | AGENTS.md | ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844 |
| 2 | s0-lab/control/tools/verify-text-artifacts.ps1 | b976b235313aefc748eb92b7e8e99868ce5a289194d8ecfcaa7860acaa42a1f3 |
| 3 | s0-lab/control/s0-protocol-v0.3-canonical-r1.md | 6646a8c3f46a06c147d4ab2a94da47ee2262b5729a20b44fa0bd842b9b697f60 |
| 4 | s0-lab/control/s0-protocol-v0.3-canonical-r1.sha256 | 88d8bcaf7e2b9c14fe71a267cbc19c4a21c4c003187348a3cf6dc323e618a3f3 |
| 5 | s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.md | 49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0 |
| 6 | s0-lab/control/f0-public/question-contract-v0.14/universal-response-contract-v0.14-candidate.sha256 | ff71deea0b0aaac3a6f46d703376b22f677baa4d0e20be22a42f98a449706766 |
| 7 | s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.md | a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee |
| 8 | s0-lab/control/f0-public/question-contract-v0.14/public-falsification-plan-v0.11.sha256 | 7f30298de0667cd01991e72704b963a20ebb558e1e76474eb212d8a67842d888 |
| 9 | s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.md | b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9 |
| 10 | s0-lab/control/f0-public/question-contract-v0.14/review-response-v0.9.sha256 | 24ce405c3987410cd2a2f6cba0ce4ec83a235f8b23b013d908675797432e8310 |
| 11 | s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.md | 537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605 |
| 12 | s0-lab/reviews/f0-public/question-contract-v0.14/urc-v0.14-independent-review-v0.1.sha256 | e73f0bb18e65f39b6ebb8ac0fda00ef4f756a3a01000f97db9fb9a41ac0eaf6c |
| 13 | s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.md | f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65 |
| 14 | s0-lab/control/f0-public/question-contract-v0.14/control-integration-decision-v0.1.sha256 | 8c90eda5c1557c1f31e977f94ec6985e8799a692e56141a830e6cc8ff7f685b4 |
| 15 | s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.md | 167a0bf4e4bf408ad0a01e9ee45273ffcb0b9a0c06e3b5a22e63e19978cd2925 |
| 16 | s0-lab/control/i1/i1-public-runtime-v02-control-integration-decision-v0.1.sha256 | 36a1565b93df98f2d18f8447280458df66a0d38dacf2aa4bb56cc4b7a7564c40 |
| 17 | s0-lab/i1/spec/public-runtime-v0.14.json | fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08 |
| 18 | s0-lab/i1/spec/public-runtime-files.sha256 | 9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e |
| 19 | s0-lab/i1/verification/implementation-files.sha256 | 668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c |
| 20 | s0-lab/i1/verification/implementation-manifest.sha256 | 1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6 |
| 21 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.md | 6a062383742e90409f5dac9c443de90b93773c266525ba00f3802b60d40ff6fc |
| 22 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1.sha256 | 7a0bc9043ae8ac2e59d4ef0aa1a8723835865717f0054e818711cc7809df8601 |
| 23 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.md | ee6d0e02bdbc324c05a300ba949505a22ac8bdbe2f02a72509776bfaa22ccdd0 |
| 24 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/role-position-isolation-matrix-v0.1.sha256 | 08fef8b7e5c31f94983b5f24cdfae44aeb5f7137cbcf81854130f589ea6ac61d |
| 25 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.md | 71b4814c3c040fb5a822c2af8214d27c71b63c627cd0fedd1cee3c7178997937 |
| 26 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/isolation-acceptance-plan-v0.1.sha256 | 6caf7c1ca42e5ed1c81f45d481cc4403d637156068d8a9f48d61d98a9349dc3a |
| 27 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.md | 88ca9ae00ee8a76f1f01865be7ffc106afede4a8207c86fab1bb72c9099e8d7a |
| 28 | s0-lab/control/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-independent-review-brief-v0.1.sha256 | 5553c4fa3698186ad1eae160143e4a97b30aba651e033db38f4c3d654352224a |
| 29 | s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.md | d99cf801719e2f524ca87fe3741b8a6776c4682df304d9448c245e5d3fee7404 |
| 30 | s0-lab/reviews/isolation/trust-root-role-isolation-v0.1/trust-root-role-isolation-design-v0.1-independent-review.sha256 | e6c8497753878df8407dd23cfa606927e09909a8486b398206bb237a75f76e7d |
| 31 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.md | e50d7a3ed0f4e1e4a440e671201287de46fdd3c5de6bb719b4d4602ecee500f4 |
| 32 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-revision-v0.2.sha256 | 41d8de2afbb9ee53424a498b1d05820939f339fc3f7b161ec74b2a2d617728b3 |
| 33 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.md | 3ac2ecf63451dd022024b2b658866b2f50b5e920c33b6f39d563d873b3b419c1 |
| 34 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/identity-authority-matrix-addendum-v0.2.sha256 | 566bba9b81d4ed5216f9c49c01448154f0a2a53ee6d9cfa13e0d9993475df70c |
| 35 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.md | 534fc5587d9bd3bf6c5bad5bf66c26d838cacb7db1d14a915c8dc9b6d1474db1 |
| 36 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/isolation-acceptance-plan-addendum-v0.2.sha256 | 29ec3013bab28aa1265653ad4badc034381fa91cbd40a0aa44443359a9d70060 |
| 37 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.md | 5c961d3bba03e12e07d34aede1207448565bf3456d0bffb6cad1602f1bbd2494 |
| 38 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/review-response-v0.1.sha256 | ac64d54c204d17e4d541e08ab1e1ab487c2f2a43542aa317958130250383cc90 |
| 39 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.md | 610b4ca1b03d7539cdcaf526a03bf3877cfca24426fd9f58b816aa0012d6db27 |
| 40 | s0-lab/control/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-independent-review-brief-v0.2.sha256 | 964b09d8c42ee5680f15eda27659aded87571ce6b77a734affe9253473114da4 |
| 41 | s0-lab/reviews/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-v0.2-independent-review.md | 67617db3b89e8067cd069609d0705f7b853f741acb5fc40eba4b675435327990 |
| 42 | s0-lab/reviews/isolation/trust-root-role-isolation-v0.2/trust-root-role-isolation-design-v0.2-independent-review.sha256 | cf0f919f266cf765611bb84944f44441db8a14e7eb9183052c89d9cb8a467d21 |
| 43 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.md | a6fd2575052b6cbc4ae9b3a29f27f1b2338a4e6a7044285e89725eeee215b66b |
| 44 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-design-revision-v0.3.sha256 | 90b2643bd2128339261ea0eae6c334ae757d5fa096cae3e9d73b8ff7ae606757 |
| 45 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.md | 5553758d0a4bdab2dd8e747b931830287e3f522437f944b838bf87f037dc7d5a |
| 46 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/identity-authority-matrix-addendum-v0.3.sha256 | 14ad4440f996f6b637b8adb667b3975a9040ee70d8da503d5be700646438d72b |
| 47 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.md | bd14249f524f37444cc4a82b676505f640492b5244d920a78fcd2820a71cebe3 |
| 48 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/isolation-acceptance-plan-addendum-v0.3.sha256 | d2bac18a3bef1ec769e9f97149fa6d74bd4536b7454151ec6113fe355f9a86d7 |
| 49 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/review-response-v0.2.md | 9b263749943507bd1b21e87f089a8bf02bfc446f13b8d5b02f363ab24ab24d36 |
| 50 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/review-response-v0.2.sha256 | 1ecd2755a85477befd9ac36af069d2096c241de5d2698c8478feb363c54efb3e |
| 51 | s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.md | e10813ad559e9ea66f3c197a0a9b99649d4d68e9f5b475eee1a8395dd796dbaf |
| 52 | s0-lab/reviews/protocol-refreeze-v0.3-canonical-r1/limited-rereview-v0.1.sha256 | d47178efc71641a34c7a1fcbcfbc0a580491a26393c4c62316c30074de1d7da5 |
| 53 | s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.md | 512714d8745bb78c08b0b6fd085f978c84fb0b7d2439dbbae0138d2f92ef9b90 |
| 54 | s0-lab/control/protocol-refreeze-v0.3-canonical-r1/control-final-refreeze-decision-v0.1.sha256 | 7ef1b8461efcf822baf0f29854d02e08c3f42dc519a1fffe02a997140aa7e392 |
| 55 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.md | a442353a2d6e0041106222320810650a0ec14823e84d4239ae487d0355c701dd |
| 56 | s0-lab/control/isolation/trust-root-role-isolation-v0.3/trust-root-role-isolation-independent-rereview-brief-v0.4.sha256 | 356b58d5025ce8b899cc40d4399c14bfc1000f464daa3c4ef2800614cf23ae63 |

### 2.3 Canonical and file-specific validation

The authenticated validator was read only after its hash matched. Its SelfTest
then passed all eleven cases: Markdown and sidecar no-BOM controls, valid CRLF,
actual BOM rejection, missing-final-LF rejection, trailing-space rejection,
trailing-tab/CRLF rejection, invalid-UTF-8 rejection, empty-file rejection,
canonical-sidecar acceptance, and noncanonical-sidecar rejection.

Exactly 25 admitted Markdown/same-basename-sidecar pairs were passed to the
validator. Every independently labeled file-presence, UTF-8, BOM, final-LF,
trailing-whitespace, sidecar-presence, sidecar-text, sidecar-record/hash, and
artifact-overall check passed; final result was OVERALL=PASS. No excluded
historical pair was validated.

The six other files received only applicable checks:

- AGENTS.md and the validator matched their exact hashes; the validator's
  applicable executable check was its passing SelfTest.
- public-runtime-v0.14.json parsed as JSON. Its declared counts matched its
  actual arrays: 32 role rows, 40 positions, eight paired rows, 27 stores, 46
  explicit reader entries, 64 edges, and 22 signer roles.
- public-runtime-files.sha256 contained seven canonical, unique records and
  bound the admitted runtime JSON hash.
- implementation-files.sha256 contained 26 canonical, unique records and
  cross-bound the admitted runtime JSON and public-runtime manifest hashes.
- implementation-manifest.sha256 contained the one canonical record binding
  implementation-files.sha256 to
  668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c.

These were document-integrity and public-topology checks, not implementation or
acceptance tests.

## 3. Independent effective-composition reconstruction

The effective design is the authenticated v0.1 base plus the exact v0.2
overlay plus the exact v0.3 overlay. Review responses explain author intent but
grant no authority. Review briefs control reviewer inputs and outputs but are
not design clauses.

### 3.1 v0.2 over v0.1

The v0.2 replacement map independently reconstructs as follows:

1. v0.2 section 6 replaces the v0.1 invocation-ID generation and duplicate
   sentences, every separate invocation-nonce reference, and the old
   invocation-secret clause.
2. The v0.1 signed-descriptor phrase alone becomes an unsigned TCB-bound
   invocation descriptor; v0.2 section 5 supplies its authority, bytes,
   admission, and verification order.
3. v0.2 sections 4.1 through 4.5 replace the two named v0.1 signer-request and
   media paragraphs and all of v0.1 section 5.3.
4. v0.2 section 4.4 replaces the named non-root signer-state paragraph.
5. Matrix section 1 is supplemented, and conflicts replaced, by v0.2 section
   6; matrix section 3 is replaced by v0.2 section 4.5 and authority-addendum
   sections 2 through 3.
6. Matrix section 7 is supplemented by the named strict-profile, scope,
   descriptor, invocation, and machine-readable-successor clauses.
7. Acceptance-plan section 2 actor/signer fields and only the rows named by
   the v0.2 addendum are replaced. Fifteen rows are added to the predecessor
   92, producing 107.

That overlay supplies the nonidentity order-`L` Ed25519 profile, the
noncircular PoP/root/import state path, three signature scopes, the unsigned
TCB descriptor/admission path, and the one globally reserved invocation ID.
No unlisted v0.1 meaning is changed.

### 3.2 v0.3 over v0.2

The v0.3 overlay is confined to the two v0.2 findings:

| v0.2 clause | Effective v0.3 treatment |
|---|---|
| strict-profile section 3.5 order-eight attribution bullet | replaced by v0.3 section 3 |
| section 4.3.5 import admission and import-only zero-result-media rule | replaced for the three imports by v0.3 sections 2.2 and 2.3 |
| section 4.3.6 signing-only result-medium phrases, import event grammar, and import result/state evidence | replaced for imports by v0.3 sections 2.4 through 2.7 |
| section 4.4 evidence for the three import transitions | supplemented and, on conflict, replaced by v0.3 sections 2.5 and 2.6 |
| v0.2 authority rows for the three imports, admission, and signer-media evidence | supplemented by the v0.3 authority addendum |
| v0.2 acceptance evidence and import meanings of ISO-K20, ISO-K25, ISO-K31, ISO-K33, plus ISO-K28 vector provenance | replaced only as stated by the v0.3 acceptance addendum |

The v0.3 acceptance plan adds or removes no row. Outside the named
replacement scopes, no conflict or topology, fairness, signature-scope,
provider, implementation, protected-material, E0, or S0 regression was found.
The two defects in sections 4.6 and 5 of this review are inside the two stated
repair scopes; they do not imply an unlisted third design change.

The canonical-r1 protocol bytes are current for this newly opened review
because of the admitted CONTROL final-refreeze decision. Candidate-era status
text in the canonical header is preserved history. The provenance pair does
not decide either substantive finding.

## 4. Independent `TRI2-M01` reconstruction

### 4.1 Routes and exact state map

One `import-outcome-v1` route applies to exactly these three state-changing
imports:

| Import class | Before state | Accepted after state |
|---|---|---|
| `preactivation-context-v1` | `key-generated` | `pop-context-bound` |
| `registry-binding-v1` | `pop-issued` | `registry-bound` |
| `activation-binding-v1` | `registry-bound` | `active` |

The outcome kind is not a fourth import class. The route is TCB control media
on an existing administrative path, not an experimental topology object.

### 4.2 Preallocation and complete admission bytes

Before admission freezes, CONTROL host preflight independently generates and
reserves one fresh nonzero 32-byte `result_media_id` and the four route event
IDs: reserved, admission-frozen, pending, and completion. Each is single-use
in the project-lifetime admission/signer-media ledger. The exact ordered
ASCII/LF admission record is:

```text
import_admission_schema=S0-SIGNER-IMPORT-ADMISSION-2
authority_id=control-host-preflight
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
import_class=<preactivation-context-v1, registry-binding-v1, or activation-binding-v1>
from_state=<the exact class-mapped source state>
to_state=<the exact class-mapped destination state>
package_sha256=<64 lowercase hex>
package_object_id=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
result_media_kind=import-outcome-v1
result_media_id=<64 lowercase hex, nonzero>
reserved_media_event_id=<64 lowercase hex>
admission_frozen_media_event_id=<64 lowercase hex>
pending_media_event_id=<64 lowercase hex>
completion_media_event_id=<64 lowercase hex>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_max_bytes=2048
admission_event_id=<byte-equal to admission_frozen_media_event_id>
decision=approved
```

It has one final LF and no BOM, CR, extra field, or trailing space. Its hash is
the import `admission_record_sha256`. Class, states, package hash/object,
one-use capability, outcome kind/schema/capacity, medium ID, and all four event
IDs are therefore admission-bound before attachment.

### 4.3 Media and complete outcome bytes

While powered off, the target receives exactly the immutable read-only import
ISO plus one fresh zero-filled fixed-capacity 2,048-byte raw medium. The host
never mounts it. The TCB service may write at most one frame of at most 2,048
bytes, in this exact order:

```text
import_outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
tcb_service_id=S0-IMPORT-TRANSITION-TCB-1
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
import_class=<exact import class>
from_state=<exact class-mapped source state>
to_state=<exact class-mapped destination state>
package_sha256=<64 lowercase hex>
package_object_id=<64 lowercase hex>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex>
admission_record_sha256=<64 lowercase hex>
result_media_kind=import-outcome-v1
result_media_id=<64 lowercase hex>
reserved_media_event_id=<64 lowercase hex>
admission_frozen_media_event_id=<64 lowercase hex>
pending_media_event_id=<64 lowercase hex>
completion_media_event_id=<64 lowercase hex>
before_state=<exact source state>
after_state=<exact destination, exact source, or indeterminate>
before_configuration_state_sha256=<64 lowercase hex>
after_configuration_state_sha256=<64 lowercase hex or 64 zeroes only when indeterminate>
decision=<accepted or rejected>
reason=<none, parse-rejected, validation-rejected, or state-commit-failed>
outcome_body_sha256=<SHA-256 of every preceding frame byte including the LF after reason>
```

The frame has one final LF and no BOM, CR, extra field, or trailing space. All
remaining medium bytes are zero. The complete-frame hash includes the final
hash line and LF. Accepted/none requires exact source to destination,
nonzero unequal configuration hashes, and destination persistence before
emission. Parse or validation rejection requires source to unchanged source
and equal nonzero hashes. State-commit failure requires source to
`indeterminate` and a zero after-state hash. Every other tuple is malformed.

### 4.4 Authority, cycle avoidance, persistence, and cleanup

The unsigned frame's authority is the pinned appliance image and launch
identity, the exact `S0-IMPORT-TRANSITION-TCB-1` service, one-use capability,
exact ISO/outcome object handles, powered-off exclusive attachment, admission
and event bindings, frame hashes, and ledger/witness chain together. It is
not cryptographic proof against a malicious host or hypervisor and is not a
fourth signature scope.

The four event IDs are admission-frozen before execution. The outcome frame
binds the planned completion event by ID, not by its future hash. The eventual
completion event binds the complete frame hash and chains by
`previous_event_sha256` and `prior_route_event_id`. This avoids a frame/event
hash cycle while retaining identity and sequence binding.

Only after both media are detached and classification is final may the exact
completion event be appended. Exact frame bytes/hashes may be retained only
inside existing named ceremony evidence. Both TCB temporary replicas are
destroyed only after evidence is sealed and before any later route. This is
operational deletion, not cryptographic erasure. The target retains only the
bounded IDs, hashes, decision, configuration state, and anti-replay state
already allowed by v0.2.

### 4.5 Fixed classification and lifecycle

After `pending`, abnormal-end evidence has first precedence and classifies
`crash`, ignoring apparent frame bytes. Normal shutdown with no complete frame
is `missing`. Multiple outcome media, multiple frames/magic values, or any
nonzero tail after the canonical final LF is `duplicate`. A malformed or
oversized frame, bad body hash, binding/state/host-evidence mismatch, or
anti-replay conflict is `disagreement`. One valid rejected frame then maps to
its exact `parse-rejected`, `validation-rejected`, or `state-commit-failed`
reason. Only one valid fully agreeing accepted frame maps to `accepted`.

Only `accepted` may append `consumed/accepted` and make the destination state
available. Every other post-pending class invalidates the candidate, forbids
retry or selective replay, and appends `terminal/rejected` when the exact
preallocated completion ID and ledger/witness append remain usable. A
completion collision, unavailable ledger/witness, or failed append permits no
invented completion ID or event; existing conflict/failure evidence is the
observable stop record.

A failure before `pending` is not an import-outcome classification. It follows
the inherited admission lifecycle and, if appendable, terminates from the
last durable `reserved` or `admission-frozen` state with `outcome_class=none`
and zero frame hash. A preallocation collision or unavailable ledger/witness
again permits no invented terminal append.

### 4.6 Import event reconstruction and unresolved exactness

The inherited exact v0.2 event grammar, in order, is:

```text
signer_media_event_schema=S0-SIGNER-MEDIA-LEDGER-EVENT-1
namespace=signer-media
sequence=<canonical unsigned decimal, beginning at 0>
previous_event_sha256=<64 lowercase hex; 64 zeroes only at sequence 0>
event_id=<64 lowercase hex>
prior_route_event_id=<64 lowercase hex; 64 zeroes only at the route's reserved event>
campaign_id=<64 lowercase hex>
ceremony_id=<64 lowercase hex>
signer_id=<exact registry role ID>
route_kind=<import, nonroot-request, or root-ceremony>
route_class=<exact import_class, request_class, or ceremony_class literal>
request_id=<64 lowercase hex, or 64 zeroes only for an import>
attachment_capability_id=<64 lowercase hex>
admission_event_id=<64 lowercase hex; zero only before admission freeze>
admission_record_sha256=<64 lowercase hex; zero only before admission freeze>
media_object_sha256=<64 lowercase hex, or 64 zeroes before admission freeze>
media_object_id=<64 lowercase hex, or 64 zeroes before admission freeze>
result_media_id=<64 lowercase hex, or 64 zeroes only for an import>
state=<reserved, admission-frozen, pending, consumed, or terminal>
terminal_from=<none, reserved, admission-frozen, or pending>
decision=<reserved, approved, executing, accepted, or rejected>
```

v0.3 says the replacement import schema
`S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` retains every v0.2 field and adds this
ordered block:

```text
result_media_id=<the route's nonzero outcome-medium ID>
result_media_kind=import-outcome-v1
reserved_media_event_id=<the preallocated reserved event ID>
admission_frozen_media_event_id=<the preallocated admission-frozen event ID>
pending_media_event_id=<the preallocated pending event ID>
completion_media_event_id=<the preallocated consumed-or-terminal event ID>
outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1
outcome_frame_sha256=<64 zeroes before completion; exact complete-frame hash when one valid frame exists>
outcome_class=<none, accepted, parse-rejected, validation-rejected, state-commit-failed, crash, missing, duplicate, or disagreement>
before_appliance_state=<exact source state or none before pending>
after_appliance_state=<exact destination, exact source, indeterminate, or none before completion>
```

The intended lifecycle and immediately-prior route chaining are intelligible:
reserved, admission-frozen, pending, then exactly one consumed or terminal
completion, using the corresponding four preallocated IDs. Before completion,
the frame hash is zero and class is none; pending names the expected source;
completion binds classification, available frame hash, and state evidence.

The complete event bytes are nevertheless not exact. The retained v0.2
grammar already contains `result_media_id` immediately before `state`,
`terminal_from`, and `decision`; the purported added block begins with
`result_media_id` again. v0.3 does not say that this first line replaces the
inherited line, that the rest of the block is inserted there, or that the
whole block is appended after all inherited fields. Those readings yield
different field orders, duplicate-field behavior, event bytes, and event
hashes. It also does not fix `before_appliance_state` and
`after_appliance_state` values for terminal events reached directly from
`reserved` or `admission-frozen`. Therefore the required complete ordered
event grammar and pre-pending terminal record remain multiply interpretable.
This is the major finding in section 8 and leaves `TRI2-M01` open.

## 5. Independent `TRI2-m01` reconstruction

The false claim that RFC 9381 section 5.4.5 supplies the decimal coordinate
or four encodings is absent. The v0.2 strict nonidentity order-`L` predicate
and the requirement for future independent canonical decoding,
re-encoding, `[8]P = I`, `[4]P != I`, and `[L]P != I` checks survive.

The proposed derivation instead states `p = 2^255 - 19`, gives a decimal `y0`,
sets `y1 = p - y0`, encodes the canonical 255-bit `y` little-endian, and uses
the high bit of byte 31 for the `x` sign. Its literal cleared-sign prefixes
are:

| Claimed coordinate | Cleared-sign little-endian prefix |
|---|---|
| `y0` | `26 e8 95 8f c2 b2 27 ...` |
| `y1` | `c7 17 6a 70 3d 4d 41 ...` |
| `p` | `ed ff ff ff ff ff ff ...` |

If `y1 = p - y0`, byte addition with carries must reproduce canonical `p`.
Bytes 0 through 5 sum to `ed ff ff ff ff ff` with no carry. Byte 6 then sums
to `0x27 + 0x41 = 0x68`, not `0xff`. The sign bit is byte 31 and cannot repair
this earlier-byte contradiction. Thus the second literal pair does not follow
from the stated derivation. This bounded public-text exactness defect leaves
`TRI2-m01` open as the minor finding in section 8. No point decode,
multiplication, cryptographic library, or executable vector was used.

## 6. Mandatory hostile tabletop traces

The following paper traces apply independently to all three import classes,
with the class-specific source and destination states in section 4.1. In the
table, an exact `terminal/rejected` append is required only when the frozen
completion ID and ledger/witness remain usable. Otherwise the existing
collision, unavailable-head, failed-append, or unknown-pending evidence is the
stop record and no completion is invented.

| Mutation or observation | Unique fail-closed trace and observable record |
|---|---|
| One exact accepted frame with durable expected after-state and matching host evidence | After exact pending, detach both media, validate the complete frame and all host bindings, then append the one preallocated `consumed/accepted` event with `outcome_class=accepted`, exact frame hash, source state, and class-mapped destination. This is the sole success path. |
| Exact parse rejection | A valid `rejected/parse-rejected` frame must show source-to-source and equal nonzero configuration hashes; append terminal with that class and frame hash. It cannot advance state or retry. |
| Exact validation rejection | The same source-to-source and equal-hash rule applies, but the terminal class is `validation-rejected`. It cannot advance state or retry. |
| Exact state-commit failure | A valid `rejected/state-commit-failed` frame must show source-to-`indeterminate` and a zero after-state hash; append terminal with that class. No destination-state availability may be inferred. |
| Crash before state persistence | Abnormal-end evidence has precedence over bytes. Ignore any apparent frame, classify `crash`, retain the bounded raw/host observation, and terminalize if appendable. The source is not promoted. |
| Crash after persistence but before frame completion | Abnormal-end evidence still wins. Partial or apparent bytes cannot make the already-written target state available; classify `crash`, invalidate the candidate, and do not retry or claim completion. |
| Crash after frame completion but before shutdown | The otherwise plausible frame is ignored because controlled shutdown evidence does not agree. Classify `crash`; no consumed event or destination-state claim is allowed. |
| Host crash before completion-event persistence | The route remains pending or its append is uncertain. On recovery, no consumed event may be reconstructed or assigned a new ID; the pending/append evidence invalidates the candidate without retry. |
| All-zero or absent outcome bytes after normal shutdown | Classify `missing`; record zero frame hash in terminal evidence when appendable. Shutdown or detachment alone is never success. |
| Partial or truncated bytes with no complete frame | Under normal shutdown, classify `missing`; under abnormal shutdown, the earlier `crash` precedence applies. |
| One oversized, malformed, extra-field, reordered, bad-body-hash, or otherwise noncanonical purported complete frame | Classify `disagreement`, retain the bounded raw observation/classification, and do not advance state. |
| Nonzero byte after the one canonical final LF | The earlier `duplicate` rule applies, even if the prefix is a valid frame. |
| More than one magic/frame or more than one outcome medium | Classify `duplicate`; no frame is selected and no retry is allowed. |
| Medium beyond the exact immutable-ISO-plus-fresh-outcome pair | If detected before pending, reject through the inherited admission lifecycle with no outcome class. If it appears after pending, it is an attachment/admission disagreement; an added outcome medium is specifically `duplicate`. |
| Completion-ID/event conflict or ledger/witness failure | Never redraw an ID, select an existing event, or invent an append. Preserve the exact conflict/head/failure evidence, invalidate the candidate, and make no completion claim. |
| Replayed outcome or reused capability, event ID, or `result_media_id` | A preflight collision rejects without redraw and before pending. A mismatch or anti-replay conflict found after pending is `disagreement`; only the original reservation remains authoritative. |
| Wrong campaign, ceremony, signer, class, from/to state, package hash/object, admission event/hash, capability, outcome kind/medium ID, or any signer-media event ID | The exact admission/frame/host binding fails and classification is `disagreement`; the mismatching field and raw/frame evidence identify the stop. |
| Cross-signer, cross-class, cross-package, or cross-campaign substitution | The same exact binding failure produces `disagreement`, never a transferable outcome or authority. |
| Accepted frame with unchanged or wrong appliance state/hash | The accepted tuple is not one of the total allowed combinations and conflicts with durable/host evidence; classify `disagreement`, not accepted. |
| Rejection frame after unauthorized appliance-state advance | Parse/validation rejection requires unchanged state, while commit failure requires indeterminate. Any observed advance conflicts with the declared tuple and is `disagreement`; neither source nor destination is authorized for further use. |
| Host/appliance disagreement | Classification is `disagreement`; a host preference cannot override the frame, pinned-service contract, durable state, admission, anti-replay state, or event chain. |
| Host infers success from shutdown, detachment, elapsed time, or absence of an error | With no exact frame this is `missing`, and with conflicting evidence it is `disagreement`; neither permits consumed. |
| Host tries to append consumed without one exact accepted frame | The state/event combination violates the grammar and ledger rule. Reject the append, retain the failed/conflicting ledger evidence, and do not invent completion. |
| Cleanup before evidence persistence | The ordering rule is violated. Candidate state is not available, cleanup cannot substitute for the missing evidence, and the route cannot proceed to another attachment. |
| Stale medium retained for a later route | The powered-off admission check rejects simultaneous, stale, prior, reused, or nonexclusive media before boot; after-pending discovery is a binding disagreement. |
| Outcome bytes contain protected or private-key material | They cannot match the exact public ASCII frame and violate the inherited no-protected-byte route boundary. Treat as candidate-invalidating protected-asset exposure, grant no state authority, and do not treat the bytes as an accepted public result. No such exposure was observed in this document-only review. |
| Unsigned outcome treated as a signature scope, key, signer, role, store, reader, edge, or experimental authority | Reject the scope/topology inventory and import authority. The outcome is only bounded TCB control evidence in the existing route and ledger namespace. |
| Derivation fails to reproduce a literal encoding | The table cannot pass ISO-K28 provenance. The second coordinate pair fails this paper trace as shown in section 5. |
| Little-endian/sign-bit swap, noncanonical field encoding, failed point-class proof, or trust in a copied label | Reject the future vector evidence; the independent construction, canonical decode/re-encode, and order checks remain mandatory. |
| Claim that RFC 9381 section 5.4.5 supplies the decimal coordinate or encodings | Reject the provenance claim. The effective v0.3 text correctly removes it, but its replacement arithmetic is still inconsistent. |
| Topology, A-D opportunity, signature-scope, provider, closed-gate, or claim-limit drift | Reject the affected inventory or package. The authenticated public counts and nonclaims in section 7 show no such v0.3 drift. |

These routes are otherwise deterministic on paper, but the event-serialization
ambiguity in section 4.6 prevents the required successful or terminal event
from having one exact byte string and event hash. Thus the hostile traces do
not close `TRI2-M01`.

## 7. Frozen inventory and non-regression audit

### 7.1 Acceptance inventory

The effective inventory is the 92 v0.1 rows, with only the exact v0.2
replacements, plus these 15 v0.2 additions:

- `ISO-P16` through `ISO-P19` (four);
- `ISO-C13` through `ISO-C14` (two);
- `ISO-R22` (one); and
- `ISO-K27` through `ISO-K34` (eight).

That is exactly 107: platform 19, channels 14, media/routes 22,
independence eight, trust/signer 34, and lifecycle ten. v0.3 adds or deletes
no row. It replaces only its specified import evidence and import meanings of
`ISO-K20`, `ISO-K25`, `ISO-K31`, and `ISO-K33`, and the negative-vector
provenance for `ISO-K28`. Every row remains noncompensatory: no pass, waiver,
skip, provider default, operator judgment, or substituted result can offset a
failure elsewhere.

### 7.2 Exact frozen counts

| Inventory | Effective count or value | Result |
|---|---:|---|
| aggregated role rows | 32 | preserved |
| role positions | 40 | preserved |
| paired rows | 8 | preserved |
| experimental section-4 signers | 21 | preserved |
| `none` positions | 19 | preserved |
| non-row root | 1 | preserved |
| registry IDs | 22 | preserved |
| experimental stores | 27 | preserved |
| explicit readers | 46 | preserved |
| edge rows | 64 | preserved |
| acceptance rows | 107 | preserved |
| ledger namespaces | 3 | preserved |
| future executor invocation/session units | 8 | preserved |
| maximum concurrency | 3 | preserved |
| exclusive signature scopes | 3 | preserved |

The three signature scopes remain exactly `preactivation-pop-v1`,
`section4-generic-envelope-v1`, and `inherited-signature-unresolved`. Import
packages, admissions, unsigned outcomes, event records, request/ceremony
classes, and TCB descriptors are not added scopes.

### 7.3 Fairness, topology, and nonclaims

Conditions A through D retain identical source information, authority, model
condition, time, output, and scoring opportunity. No condition receives an
extra role, signer, store, reader, edge, route, signature scope, model call, or
hidden information. The outcome medium/frame, TCB service, admissions, and
signer-media events are temporary or control objects on an existing route and
do not change the 27/46/64 experimental topology.

The three ledger namespaces, split-edge rules, E49 boundary, eight executor
units, and concurrency cap remain inherited. Provider selections remain
unresolved blockers. No implementation, protected material, key generation,
provider/model session, fixture, oracle, condition map, judge handoff,
scoring, E0, or S0 authority is created. The public runtime JSON and manifest
counts corroborate the frozen public topology only; they are not execution or
implementation evidence.

## 8. Finding dispositions

| Finding ID | Severity | Disposition | Independent basis | Required bounded repair |
|---|---|---|---|---|
| `TRI2-M01` | major | open | The new import event says it retains all ordered v0.2 fields but repeats `result_media_id` at the start of an added block without specifying replacement or insertion position. Multiple event serializations and hashes result. Direct pre-pending terminal state-evidence values are also not fixed. | Publish one complete ordered `S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1` grammar with one occurrence of every field, explicit schema value, exact per-state values including terminal-from-reserved and terminal-from-admission-frozen, and unambiguous event-hash bytes. Then obtain a fresh review. |
| `TRI2-m01` | minor | open | The cleared-sign byte prefixes for the asserted `y0` and `p-y0` add to `... 68 ...`, not `... ff ...`, at byte 6 with no incoming carry. The second literal pair therefore does not follow the stated arithmetic. | Correct the coordinate/relation or literal pair, preserve the absent RFC 9381 attribution and strict predicate, and require future independent construction, canonical decoding/re-encoding, and order checks. Then obtain a fresh review. |

There are no new findings outside the two declared v0.3 repair scopes. The
durable-state route was not separately cited: within the stated threat model,
the pinned TCB service plus exact frame, attachment, admission, anti-replay,
host, and ledger contract is a design-level authority assumption. A service
that lies about durable state violates that pinned TCB contract and the
applicable future evidence rows; this document review does not show that such
an implementation exists.

The event defect is major because a required event, persistence record, and
hash serialization remain ambiguous. It is not classified blocking: the
public design does not thereby grant forgeable or circular authority, expose a
protected asset, destroy reviewer/A-D independence, contradict frozen
topology, or require opening a closed implementation gate to repair the text.
The vector defect is minor because it is a bounded public literal/derivation
inconsistency; the unchanged strict predicate continues to reject the intended
point class and no authority or hidden failure is created by the typo itself.

Finding count is therefore zero blocking, one major, and one minor.

## 9. Verdict, maximum claim, and next authority

`REVISE-AND-REVIEW`

The maximum supported claim is that the authenticated v0.3 public design
preserves the frozen topology, isolation, fairness, signature-scope, and
closed-gate boundaries, and proposes a largely reconstructable bounded import
outcome route, but it does not close either predecessor finding. This is a
public document finding only, not evidence about an implementation or live
system.

Because findings exist, no later gate opens automatically and the
zero-finding CONTROL-integration-consideration gate is unavailable on this
record. Exact next authority remains with CONTROL: preserve this result and
decide whether to request a bounded public-text revision/new evidence repair
or no further action. Implementation, provisioning, cryptographic-vector
execution, keys, protected material, provider/model sessions, judge handoff,
scoring, E0, and S0 remain closed.

## 10. Evidence classification and limits

- Facts are the authenticated bytes and hashes, Git identity, canonical-text
  results, literal design clauses, JSON/manifest structure, and frozen counts
  reported above.
- Inferences are the effective-composition reconstruction, hostile paper
  traces, event-grammar ambiguity, arithmetic contradiction, severities, and
  verdict.
- Proposals are only the bounded repairs in section 8. They grant no authority
  and were not implemented.
- Test results are limited to document hashing, canonical text validation,
  validator SelfTest, JSON parsing, and manifest-shape checks. No
  implementation, cryptographic, platform, provider, model, acceptance, E0,
  or S0 test was run.

No key, vector, fixture, script, helper, VM, account, network, ACL, vault,
signer, ledger, witness, provider, model, executor, oracle, bank, label,
condition map, protected material, or customer/personal/secret content was
created, provisioned, executed, or accessed for this review.
