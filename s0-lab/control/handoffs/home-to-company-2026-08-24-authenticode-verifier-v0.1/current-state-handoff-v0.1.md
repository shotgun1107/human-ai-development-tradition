# Home-to-company handoff: Windows Authenticode verifier v0.1

## 1. Purpose

This PUBLIC handoff transfers the completed home-PC Authenticode verifier
implementation candidate to the company PC without merging main or opening a
new technical gate.

Repository:
`https://github.com/shotgun1107/human-ai-development-tradition.git`

The final handoff commit and tree include this document and therefore cannot
be embedded in their own bytes. CONTROL's completion report supplies those two
external exact pins.

## 2. Payload identity

- implementation branch:
  `codex/s0-windows-authenticode-verifier-v01`;
- implementation commit:
  `9b32090c06ab8f8c38f9540f07c04ee3b785a364`;
- implementation tree:
  `90ec2aa376cf9532d54a240619442b3a9ee823b9`;
- sole parent and v0.2 review-preservation commit:
  `2709a46faf5502e96c24bc7731e201398042b6b6`;
- payload parent tree:
  `ff26c918344e3d7ed71cd4d66484b652f333d5a3`;
- handoff-time `origin/main`:
  `39263f431a82649ddc0bbd3545ed6d95b0780adc`; and
- handoff branch:
  `codex/home-to-company-handoff-20260824-authenticode-v01`.

The implementation branch was pushed and its live remote SHA was verified as
the exact implementation commit above. `origin/main` and the v0.2 review
commit are both ancestors of the payload. The payload is not contained in
main.

## 3. Implemented result

The payload adds exactly 20 PUBLIC files under:

`s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.1/`

It contains:

- a Windows ctypes native observation collector;
- an installed-source authority authenticator;
- a deterministic 39-relation semantic validator;
- a fail-closed public runtime entry;
- 13 PUBLIC synthetic tests;
- policy, native, semantic, orchestrator, outer implementation, and
  verification manifests; and
- canonical README and implementation report pairs.

Exact package identities:

- implementation manifest SHA-256:
  `11e2f27fc4993f8b60bca17852f2112fb1d20c901b7044572deb325147cafc6f`;
- verification manifest SHA-256:
  `5f70306946c4ac70f314abe373f7b415e785a845fcca1e77f34a8e8748e81ebc`;
- implementation report SHA-256:
  `2f4473274e7a9b575fc0c848f4806d0b56c6b6218aa5b9aac6250343c585f54c`.

## 4. v0.2 review-finding disposition

The implementation addresses all three v0.2 blocking findings as candidate
code:

1. outer and subordinate source manifests, observation-byte hashing,
   authority-copy equality, computed relation trace, and trace-to-decision
   binding address `BRM-AUTH02-IR-001`;
2. actual event-site chronology, provider-state identity, fixed signer and
   countersigner indexes, chain-context hashes, `pTime`, reference time, and
   deterministic revocation freshness address `BRM-AUTH02-IR-002`; and
3. the user-authorized project supplier composite replaces the unsupported
   leaf-guarantee claim for `BRM-AUTH02-IR-003`.

The source explicitly keeps
`official_leaf_guarantee_claimed=false`. The project criterion is exact
Microsoft URL plus generic Authenticode, normal Authenticode policy,
same-chain Microsoft-root policy with test roots disabled, code-signing EKU,
mandatory timestamp, revocation, and trust-state checks. It is not represented
as an official Microsoft leaf-publisher guarantee.

These are author-side candidate dispositions. No finding is independently
closed yet.

## 5. Verification result

The authenticated-snapshot verifier reported:

- outer implementation manifest: PASS, 12 rows;
- subordinate manifests: PASS, `1 / 1 / 3 / 3` rows;
- predecessor v0.2 trust-profile and recovery manifests: PASS, `8 / 4` rows;
- preserved v0.2 trust-profile and recovery reviews: PASS;
- static semantic/live-authority separation: PASS;
- focused PUBLIC synthetic tests: `13 / 13` PASS;
- original-input swap sentinel: PASS;
- native, network, provider, and candidate-process calls during tests: zero;
  and
- process authority granted: false.

The canonical text validator passed the README and implementation report
pairs. The candidate namespace closed at exactly 20 files.

## 6. F0 and nonpublic boundary

The inherited PUBLIC-GIT F0 inventory remains `32 / 11 / 10`, total 53. Its
content and internal filenames were not opened, searched, quoted, summarized,
or passed to another agent. Worktree, index, and parent comparisons were quiet
for all three families.

No hidden oracle, credential, key, personal data, real-customer data, or other
`NONPUBLIC-OUT-OF-REPO` material was created or committed.

## 7. What did not happen

No real bootstrapper or certificate was downloaded or inspected. No Windows
trust API, certificate-store query, CRL/OCSP retrieval, candidate process,
installer, compiler, build, runtime materialization, platform probe,
rehearsal, F0 role, S0, or E0 was executed.

The native adapter is implemented but has only been exercised through the
invalid-handle fail-close boundary. Its ABI and security behavior require a
fresh independent code/security review before any live artifact gate.

No PR, release, main merge, branch deletion, history rewrite, or external-pin
promotion occurred.

## 8. Company-PC synchronization rule

First preserve and inspect the existing company repository. If it is dirty or
contains stash, local-only commits, or conflicting worktrees, do not move it.
Fetch only the exact handoff branch and materialize the externally pinned final
handoff commit in a separate clean worktree.

If the company repository is fully clean, the exact handoff branch may be
fetched and materialized at the externally pinned final commit. Do not use an
unpinned `git pull`.

Before any materialization or later push, verify aggregate F0 `32 / 11 / 10`
and every required quiet/anomaly condition without printing protected
filenames.

## 9. Next technical gate

The next technical gate is implementation review, not another trust-profile
design revision:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.1 INDEPENDENT CODE AND SECURITY REVIEW OPEN`

That gate remains closed during synchronization. The first company-PC task is
only exact Git synchronization, document authentication, and state reporting.

