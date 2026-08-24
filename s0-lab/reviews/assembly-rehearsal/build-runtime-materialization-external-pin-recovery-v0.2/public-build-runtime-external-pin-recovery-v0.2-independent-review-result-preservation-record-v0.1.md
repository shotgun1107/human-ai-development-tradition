# S0 v0.14 public build/runtime external-pin recovery v0.2 independent review result preservation record v0.1

- `preserved_at`: `2026-08-24T17:55:52.2123015+09:00`
- `preservation_role`: `CONTROL`
- `review_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.2 INDEPENDENT REVIEW OPEN`
- `review_agent_model`: `gpt-5.6-sol`
- `review_reasoning_effort`: `ultra`
- `reviewed_branch`: `codex/s0-build-runtime-external-pin-recovery-v02`
- `reviewed_commit`: `fd9415dd8e8bfc2eabda515398844097cd9cae1d`
- `reviewed_tree`: `acefe36c123f525da995e248dd2ff9396a922d7a`
- `reviewed_parent`: `6297af402d82e7469bce28fbb16b171608e9d69d`
- `reviewed_parent_tree`: `ed8ef0227171502fc900ad10179c733aaff1efaa`
- `package_manifest_sha256`: `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`
- `verdict`: `PASS-FOR-PUBLIC-EXTERNAL-PIN-RECOVERY-TRUST-PROFILE-CONSIDERATION-ONLY`
- `finding_counts`: `0 BLOCKING / 0 MAJOR / 0 MINOR`
- `F0_content_access`: `none`

## 1. Result

The fresh `gpt-5.6-sol` reviewer used `ultra` reasoning and completed 100%
coverage of the exact candidate, predecessor, validator, and relevant design
authority allowlist.

The review found no blocking, major, or minor finding. It supports only
consideration of a later PUBLIC Windows Authenticode trust-profile design.

No acquisition, download, trust-store mutation, source authoring,
installation, compiler, build, runtime, platform, rehearsal, S0, or E0 gate
was opened.

## 2. Authentication

The reviewer independently reproduced:

- exact origin and remote branch tip;
- commit `fd9415dd8e8bfc2eabda515398844097cd9cae1d`;
- tree `acefe36c123f525da995e248dd2ff9396a922d7a`;
- sole parent `6297af402d82e7469bce28fbb16b171608e9d69d`;
- parent tree `ed8ef0227171502fc900ad10179c733aaff1efaa`;
- clean worktree and index;
- exactly nine added v0.2 package paths; and
- package-manifest SHA-256
  `1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83`.

The four manifest targets, all same-basename sidecars, canonical ordering, and
hashes matched exactly.

F0 remained aggregate-only at `32 / 11 / 10` with zero parent-to-candidate
change. No F0 content or individual filename was accessed.

## 3. Canonical and predecessor checks

- canonical validator read completely: PASS;
- validator SelfTest: PASS;
- three new Markdown/sidecar pairs: PASS;
- strict JSON parsing and recursive duplicate-key rejection: PASS;
- complete grouped invariant audit: PASS;
- v0.1 package-manifest SHA-256
  `2be3d8428502a5aeb92cbf4253ce3ec6dc39071aacc35f36b12f707ab5d8dc8e`:
  PASS; and
- v0.1 review-preservation-record SHA-256
  `69be977790a8ed3d7288d6fe03655a94997770f6fe70b9b6a60c8880fcaaf070`:
  PASS.

## 4. Official fixed-target verification

The official Microsoft Visual Studio 2022 release-history row jointly bound:

- fixed release `17.14.39`;
- date `2026-08-18`;
- build `17.14.37614.0`; and
- the exact selected Build Tools target:

`https://download.visualstudio.microsoft.com/download/pr/fa619120-9c0e-47e6-bfe0-3ee96fb671b2/236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/vs_BuildTools.exe`

A metadata-only request returned HTTP 200 at the identical URI without a
redirect location. No executable byte was downloaded.

The exact ordinal URL rule, zero-redirect final-URI rule, and explicit warning
that the digest-looking path component is not artifact authentication were
accepted.

## 5. Prior-finding disposition

`BRM-EPR-V01-IR-001`: **CLOSED**.

The reviewer found that v0.2 closes the prior counterfeit-bootstrapper path:

1. the exact fixed Microsoft target is frozen;
2. a separately outer-authenticated trust profile is mandatory;
3. candidate-derived signer, certificate, chain, root, timestamp, flags, and
   store state cannot approve themselves;
4. missing or unverifiable authority stops before process creation;
5. embedded signature, approved Microsoft signer, certificate chain, root,
   timestamp, algorithms, revocation, and stable bytes are required; and
6. signed layout-content authentication remains independently mandatory.

## 6. Adversarial conclusion

The contract rejects before execution every required mutation class,
including substituted same-version bytes, unsigned or wrong-signer material,
subject spoofing, alternate roots, changed chains, invalid timestamps,
revocation failures and soft-fails, ignored policy errors, wrong algorithms,
redirects and URI aliases, post-verification mutation, file-identity swaps,
missing trust profiles, trust enrollment from the new layout, unbound layout
content, and layouts over 24 GiB.

Root distrust and revocation remain governed by the exact future trusted and
disallowed-store profile. Verify-to-exec identity remains a mandatory later
design obligation. If either future mechanism is not exact, bootstrapper
execution remains forbidden.

## 7. Nonregression and nonclaims

The exact ten external-pin class order and bindings remain unchanged. Native
and materializer/inspector source remain separate work. Toolchain acquisition
remains blocked on a future trust profile. Python transitive closure, Windows
platform identity, runtime-tree profile, and publication eligibility remain
unavailable.

This review establishes no authenticated bootstrapper, trust profile,
external pin bundle, download, installation, compiler, build, binary, runtime,
Windows behavior, rehearsal, S0, central system, or Project Brain result.

## 8. Verdict and next technical gate

**Verdict:**
`PASS-FOR-PUBLIC-EXTERNAL-PIN-RECOVERY-TRUST-PROFILE-CONSIDERATION-ONLY`.

Finding counts:

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 0 |
| MINOR | 0 |

The next technical gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE TRUST PROFILE V0.1 AUTHORING OPEN`

That gate requires a separate user decision. This preservation record grants
no Git publication or technical execution authority.
