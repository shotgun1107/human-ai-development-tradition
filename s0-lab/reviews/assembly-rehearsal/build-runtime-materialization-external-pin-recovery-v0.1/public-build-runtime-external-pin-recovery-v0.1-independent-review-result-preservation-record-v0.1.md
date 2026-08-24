# S0 v0.14 public build/runtime external-pin recovery v0.1 independent review result preservation record v0.1

- `preserved_at`: `2026-08-24T15:13:55.7376502+09:00`
- `preservation_role`: `CONTROL`
- `review_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.1 INDEPENDENT REVIEW OPEN`
- `result_preservation_gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.1 INDEPENDENT REVIEW RESULT PRESERVATION OPEN`
- `review_agent_model`: `gpt-5.6-sol`
- `review_reasoning_effort`: `xhigh`
- `requested_daybreak_model_status`: `unavailable-to-orchestrator`
- `reviewed_branch`: `codex/s0-build-runtime-external-pin-recovery-v01`
- `reviewed_commit`: `e9393501d66798f99c30deae64af37762a7d9245`
- `reviewed_tree`: `0b1ca16d67f0d0597bc523b3024cd41f3a9075c7`
- `reviewed_parent`: `39263f431a82649ddc0bbd3545ed6d95b0780adc`
- `reviewed_parent_tree`: `6697b497565ddde92dffc6b9eb8ee528ea4a2e83`
- `verdict`: `REVISE-AND-REREVIEW`
- `finding_counts`: `0 BLOCKING / 1 MAJOR / 0 MINOR`
- `download_install_build_status`: `not run or opened`
- `F0_content_access`: `none`

## 1. Preservation purpose

This record preserves the exact read-only independent review result for the
company-side v0.1 external-pin recovery package. It does not revise the
reviewed bytes, close the finding, authorize acquisition, or open a later
gate.

The requested Daybreak-Blue model was not available to the orchestrator. The
review used the disclosed strongest available fallback,
`gpt-5.6-sol` with `xhigh` reasoning. This record does not relabel that reviewer
as Daybreak-Blue. Later adversarial implementation or security reviews are to
use `gpt-5.6-sol` with `ultra` reasoning when available.

## 2. Authentication result

The independent reviewer reproduced all supplied Git identities:

- origin:
  `https://github.com/shotgun1107/human-ai-development-tradition.git`;
- branch and live remote tip:
  `codex/s0-build-runtime-external-pin-recovery-v01` at
  `e9393501d66798f99c30deae64af37762a7d9245`;
- reviewed tree:
  `0b1ca16d67f0d0597bc523b3024cd41f3a9075c7`;
- sole parent:
  `39263f431a82649ddc0bbd3545ed6d95b0780adc`; and
- parent tree:
  `6697b497565ddde92dffc6b9eb8ee528ea4a2e83`.

The initial worktree and index were clean. The reviewed commit changed exactly
the seven authorized recovery-package paths and no F0 path.

The recovery-package manifest matched SHA-256
`2be3d8428502a5aeb92cbf4253ce3ec6dc39071aacc35f36b12f707ab5d8dc8e`.
Its three logical targets and their same-basename sidecars matched exactly.

F0 remained aggregate-only:

- inventories: `32 / 11 / 10`;
- parent-to-candidate F0 changes: `0`; and
- F0 content or individual filename access: none.

## 3. Canonical and authority checks

The canonical text validator was read completely. Its SelfTest passed all
cases before use, and both new Markdown/sidecar pairs passed every independently
labeled UTF-8, BOM, final-LF, trailing-whitespace, sidecar-format, and hash
check.

The selection JSON passed strict UTF-8 and duplicate-key rejection plus its
complete internal invariant audit. All six predecessor hashes named under
`base_authority` matched their exact authorized files.

The reviewer authenticated the v0.5 seven-target design manifest and
sidecars. The v0.6 implementation manifest matched its supplied hash and
structurally contained ten unique valid rows.

## 4. Frozen external-pin reconstruction

The reviewed selection preserved the predecessor order and binding of all ten
classes:

1. native source → `external_pin_closure.native_source`;
2. materializer and inspector source →
   `external_pin_closure.materializer_inspector_source`;
3. offline toolchain bundle →
   `external_pin_closure.offline_toolchain_bundle`;
4. compiler, linker, SDK, headers, libraries, and CRT →
   `external_pin_closure.compiler_linker_sdk_crt_identities`;
5. CPython distribution → `external_pin_closure.cpython_distribution`;
6. Python dependencies → `external_pin_closure.python_dependencies`;
7. Windows platform → `external_pin_closure.windows_platform`;
8. canonical build profile → embedded `base_profile` plus
   `base_profile_sha256`;
9. runtime-tree profile → `external_pin_closure.runtime_tree_profile`; and
10. approving review →
    `authority_extension.approving_design_review_sha256`.

The availability claim was truthful: `0 / 8` complete external four-field
manifest identities and `2 / 2` authenticated nonmanifest authorities.
Versions, URLs, local observations, and component names were not upgraded into
manifest authority.

## 5. Official-source verification

The reviewer independently confirmed:

- Microsoft fixed Visual Studio Build Tools 2022 release `17.14.39`, build
  `17.14.37614.0`, dated 2026-08-18;
- workload `Microsoft.VisualStudio.Workload.VCTools`;
- components `Microsoft.VisualStudio.Component.VC.Tools.x86.x64` and
  `Microsoft.VisualStudio.Component.Windows11SDK.26100`;
- component- and language-limited offline layouts and `--noWeb` failure when
  selected material is missing;
- CPython 3.12.10 Windows AMD64 embeddable artifact name, URL, SPDX, and
  SHA-256
  `4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3`;
  and
- `jsonschema-4.26.0-py3-none-any.whl`, its exact URL, SHA-256
  `d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce`,
  size 90,630 bytes, non-yanked state, Python requirement, mandatory roots,
  and format-extra dependency roots.

The official evidence sources were Microsoft Learn and official Microsoft
download endpoints, Python.org release/SPDX/Sigstore endpoints, and PyPI
project/JSON/file endpoints.

## 6. Preserved finding

### `BRM-EPR-V01-IR-001` — MAJOR

**Title:** the bootstrapper is identified after download but is not
authenticated before execution.

#### Evidence

The v0.1 selection binds the Microsoft release-history page, release and build
labels, workload, and component IDs. It does not bind the exact fixed Build
Tools download-link target.

The acceptance plan records the downloaded bootstrapper length and SHA-256,
Product Version, channel identities, and layout hashes only after acquisition.
It does not require fail-closed Authenticode signer, trust-chain, timestamp,
or revocation evidence before the first bootstrapper execution.

Microsoft's official offline-installation certificate guidance states that
Visual Studio Setup relies on Authenticode trust to protect against a
compromised download location.

#### False-claim path

A substituted executable can advertise Product Version `17.14.39`, create an
attacker-selected layout and manifests, and then receive newly computed,
internally consistent hashes. Those hashes identify the substituted bytes but
do not authenticate Microsoft origin. The v0.1 contract could therefore admit
a counterfeit acquisition snapshot for later review.

#### Minimum correction

1. Bind the exact official fixed 17.14.39 Build Tools link target selected from
   the release-history row.
2. Before first execution, require fail-closed embedded Authenticode
   verification, trusted-chain and Microsoft signer evidence, timestamp
   validation, revocation disposition, and an explicitly approved trust-root
   and platform procedure.
3. Record the resolved endpoint, bootstrapper bytes and hash, signature
   evidence, and applicable signed layout-content verification.
4. Reject unsigned, untrusted, wrong-signer, wrong-version,
   endpoint-substituted, or unverifiable material before layout creation.

## 7. Other independent conclusions

- The current component catalog is observation evidence only. The later fixed
  layout inventory must become authority.
- Partial-layout dependency closure remains unclaimed and requires exact
  enumeration.
- The 24 GiB toolchain ceiling is a hard stop, not evidence that the selected
  layout fits.
- The Python dependency closure remains explicitly unresolved.
- Local Windows and SDK observations remain nonauthority.
- Source authoring is correctly separated from acquisition.
- No self-reference was found.
- Downloaded bytes remain publication-ineligible without a later explicit
  classification decision.
- No reviewed wording grants build, installation, compiler, runtime,
  rehearsal, or S0 authority.

## 8. Verdict

**Verdict: `REVISE-AND-REREVIEW`.**

Finding counts:

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| MAJOR | 1 |
| MINOR | 0 |

The v0.1 package must not proceed to acquisition consideration until
`BRM-EPR-V01-IR-001` is corrected and the exact revised bytes pass a fresh
independent review.

## 9. Next gate

The next permissible technical gate candidate is:

`S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION EXTERNAL PIN BUNDLE RECOVERY V0.2 REVISION OPEN`

That gate may revise only the bounded PUBLIC recovery selection and acceptance
contract needed to close the preserved finding. It does not authorize artifact
download, installation, native source authoring, compiler invocation, build,
runtime materialization, platform probing, rehearsal, S0, or E0.

After correction, a fresh independent review must use the exact revised
commit/tree/package pins. For adversarial security review, the configured
review model is `gpt-5.6-sol` with `ultra` reasoning when available.

This preservation record itself opens no later gate and authorizes no Git
publication action.
