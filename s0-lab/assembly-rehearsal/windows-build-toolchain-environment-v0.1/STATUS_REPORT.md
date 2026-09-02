# Windows Build Toolchain Environment V0.1 Status Report

Status: `PASS-BOUNDED — INTEGRATION-READY`

## Purpose

This auxiliary environment task removes the immediate Windows C++ build-tool blocker by discovering the existing toolchain, using the standard Microsoft installer only when the required workload was absent, and proving one isolated x64 compile-and-run path. It does not implement or run S0.

## Final independent review and CONTROL decision

Independent verdict: `PASS-BOUNDED — INTEGRATION-READY`; critical/high/medium/low findings: `0/0/0/0`. The review confirms R6 reboot discharge, rediscovery, smoke compile/run, and candidate defect count `0`.

CONTROL publication decision: accepted and published as the bounded local Windows build-toolchain environment evidence only. Local `main` and live `origin/main` both resolve exactly to candidate commit `2e45f2ce0dd37b0972bde820892588d087ae8d4f`, tree `79747c6b5676475a06237ca65946d6a54fa8cea1`, sole parent `8683c726eabbdb13d0229858ab68da125e3fe57a`. This does not broaden any claim to general compiler/security/production suitability or validate S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer.

Repository evidence is bound to base commit `8683c726eabbdb13d0229858ab68da125e3fe57a` and tree `c0ce101bc9140639651f3e8b64424c1448eaa1b1`.

## Final post-reboot verification (R6)

R6 `PASS` is the sole final post-reboot candidate verification. `vswhere` exit `0`, compile exit `0`, and run exit `0`; exact stdout was `S0_TOOLCHAIN_POST_REBOOT_OK`. Approximate boot UTC was `2026-09-02T03:56:15.5303584Z`. The R6 verification summary is 1,446 bytes, SHA-256 `043054FCDB6EDE25D1F9E10EF2CEF8340BE8DC2676BD84C03C2743784EBF0E43`; its inventory is 2,376 bytes, SHA-256 `660E9BEF00BE4940CEBE72E5D41A8AB661A57F41C47D3F740D2157CA1878314B`.

R3 and R5 evidence establish harness failures before compile/run and `0/0`; R4 preserves only a generic substantive failure after `0.292s` and does not prove stage/run counts. They are disclosed for provenance and are not candidate verification results. The pre-reboot historical `restartRequiredBeforeReliance=true` state is discharged and non-blocking for the current R6 candidate. A generic remaining pending rename, if evidenced, is not attributed to the installer.

R6 captured `relevant_installer_build_process_count=1`; process identity was unverified at capture time, so this count is not characterized as benign. Current targeted installer/compiler/MSI aggregates are all `0`, leaving no current cleanup blocker.

R6 artifact hashes: `smoke.cpp` `E5C21AE8268CE1570F37BEB15A5F66FA0A544AE77CC4DEF0F3FB57F9EA0CAEA1`; `smoke.obj` `38D49E2D335D20A2D621CEF44B79F28059342D46C977C088A8C361A3DAC7DC43`; `smoke.exe` `B0AE578967681A2BBCD3CD70B79C988C5366F9135970BDE6577883E8D82D68B0`; captured stdout `36425EEA7858A44D4683520E960BB6EB17A5395E33FFBAECE9106CB7C60C63D5`.

## Installation result

CODE invoked the following bootstrapper exactly once:

```text
"C:\Users\SSAFY\AppData\Local\Temp\s0-v01-live-504690da91a42646967203c8\artifacts\vs_BuildTools.exe" --quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended
```

- Start: `2026-09-02T03:09:03.4839677Z`
- End: `2026-09-02T03:13:01.8108048Z`
- Exit code: `3010`
- Installer artifact: `vs_BuildTools.exe`, 4,473,936 bytes, SHA-256 `236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29`
- Standard Windows Authenticode result before execution: `Valid`, Microsoft signer identity
- Installer process aggregate after work: `0`
- Existing Visual Studio 2017 WDExpress was preserved.
- The procedure did not make a global `PATH` mutation.

The source URL was not independently reacquired or authenticated in this gate. The official online package set is mutable and its transitive package bytes were not pinned.

## Installed and discovered environment

`vswhere` found one exact Visual Studio 2022 Build Tools instance:

- Instance ID: `c50d3a2f`
- Path: `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`
- Installation version: `17.14.37614.0`
- State: complete, launchable, non-prerelease

Exact `vswhere` queries returned the same instance with exit code `0` for:

- `Microsoft.VisualStudio.Workload.VCTools`
- `Microsoft.VisualStudio.Component.VC.Tools.x86.x64`
- `Microsoft.Component.MSBuild`
- `Microsoft.VisualStudio.Component.Windows10SDK`
- `Microsoft.VisualStudio.Component.VC.CMake.Project`

Observed tools in an isolated x64 developer environment:

| Tool | Path | Observed version |
| --- | --- | --- |
| MSVC `cl.exe` | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe` | toolset `14.44.35207`; binary `19.44.35228.0` |
| MSBuild | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe` | `17.14.51.32402` |
| Windows resource compiler | `C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\rc.exe` | SDK directory `10.0.26100.0` |
| CMake | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe` | `3.31.6-msvc6` |

In the current non-developer process, both `where.exe cl.exe` and `where.exe MSBuild.exe` exited `1` and did not resolve a path. Tool use therefore requires an activated developer environment or exact tool paths.

## Verification commands and results

The isolated child first ran:

```text
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64
```

Activation exited `0`. It then ran:

```text
cl.exe /nologo /W4 /WX /EHsc /Fe:smoke.exe /Fo:smoke.obj smoke.cpp
smoke.exe
```

Compilation exited `0`; execution exited `0`; exact standard output was `S0_TOOLCHAIN_SMOKE_OK\r\n` for the pre-reboot rehearsal. The final post-reboot R6 output was `S0_TOOLCHAIN_POST_REBOOT_OK`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `smoke.cpp` | 93 | `0126ac2ec9c0371c72ead715ed1ad9610a8dfe61e82c2af9b187c23261514f1e` |
| `smoke.obj` | 1,248 | `b96b59bd2bc992676de449e3439484c23437bdd32c6f0f2fc9c68271600e1203` |
| `smoke.exe` | 111,104 | `4f505ea933e19a916459c0538fdd4fe5d6c9da8ae883f41db9f0d249ce79f54d` |
| captured stdout | 23 | `9acf255a721370b090d067734fa4b984ecaf777d08e0dd3dee4f12a7ca6f9860` |

Post-verification compiler, installer, and `msiexec` process aggregates were all `0`.

## Evidence binding

The CODE raw root contained `0` files. The TEST/VERIFICATION raw root contained 61 physical files totaling 162,419 bytes with no reparse points. Its inventory binds 60 non-inventory files totaling 151,766 bytes; all listed sizes and SHA-256 values matched independently.

- `verification-summary.json`: 6,119 bytes, SHA-256 `ae629cdbef603c37363a33da78ab70aaf5d52d6b0754caa9f35204f8d05597ca`
- `inventory.json`: 10,653 bytes, SHA-256 `825569b20174c7c1d7eb8f7778dc9d9b6422a4a44073e7a7f2d0271871a8eafb`

## Reboot action

The Windows restart prerequisite is discharged for this candidate by R6. The approximate boot was `2026-09-02T03:56:15.5303584Z`; R6 rediscovered the exact instance and reran the bounded smoke check successfully. Any generic remaining pending rename, if evidenced, is not attributed to the installer.

## Allowed conclusions and limits

The evidence supports only that the named Build Tools instance and required named components were present after the installation, and that the observed isolated x64 smoke source compiled and ran successfully with the recorded commands and bytes.

It does not establish fixed source-URL or transitive-package provenance, mutable online package immutability, replay of installer argv, general compiler correctness, every SDK/library/architecture/generator/build system, or the historical absence of every global `PATH` edit. It does not validate S0, the central system, Project Brain integration, operational safety, economic value, or model-to-model transfer.
