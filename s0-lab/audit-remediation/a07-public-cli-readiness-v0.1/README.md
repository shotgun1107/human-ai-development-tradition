# A07 public CLI readiness v0.1

Status: **TEST PASS / REVIEW PENDING** (2026-09-29).

The recorded TEST/VERIFICATION run successfully executed the existing A04 public CLI with real `jsonschema[format]==4.26.0` in the project-local `.venv-public` environment. The missing dependency blocker is removed for these three commands on this host. Fresh independent review and CONTROL disposition remain pending; the wider audit/maintenance goal remains open.

This is core preparation for using the existing public CLI. It does not open or complete S0/E0, create a fixture or oracle, call a model/provider, or validate the central system, Project Brain, operational safety, economic value, or model-to-model transfer.

## Recorded result

The single recorded test run returned exit code `0`. It called `pip --isolated check`, `integrity`, `schema-check`, and `verify` once each; all returned `0`.

| Check | Recorded result |
| --- | --- |
| Installed dependency consistency | `No broken requirements found.` |
| `integrity` | 90 manifest entries, 56 JSON files, 8 existing packages |
| `schema-check` | 11 designated schemas; 0 designated errors and 0 broader impact errors |
| `verify` | `status=pass`, `not_an_s0_run=true`; all 8 generated in-memory package byte sequences matched the existing public packages |
| Runtime observations in each CLI child | Python 3.12.10; real jsonschema 4.26.0 in `.venv-public`; all 11 A04 module origins matched the admitted source; 0 unexpected repository modules |
| Installed distributions | Exactly the 18 locked packages plus bootstrap pip 25.0.1 |
| Preservation | All 122 admitted input hashes and sizes unchanged before/after the run; source and bundle inventories unchanged; 0 extra, missing, or observed reparse entries |

The record contains **631 assertion entries**, mostly repeated authentication checks. This is not a claim of 631 independent tests. Two in-memory receipt comparison diagnostics rejected a changed jsonschema version and a changed wheel hash; they did not mutate installed dependencies.

The verification child called the actual `s0_i0.cli.main` handlers with no test doubles. Its observation wrapper appended tagged metadata to stderr after the handler returned and left CLI stdout unchanged. The authenticated [JSON record](verification/test-results.json) retains exact child arguments, complete stdout/stderr, exit codes, observations, and pre/post measurements. The [transcript](verification/test-stdout.txt) records the same command outputs. No network command was requested by TEST; no enforced network isolation is claimed.

## Use the existing read-only CLI

Run these commands in PowerShell on this prepared host. The working directory must be the repository root because the existing CLI resolves its public inputs from the current directory. Each command uses the explicit A04 implementation path, real environment dependencies, isolated Python flags, and no bytecode writes. It prints JSON to the terminal and does not write a fixture or verification artifact.

```powershell
Set-Location -LiteralPath 'C:\Users\SSAFY\Documents\ai-development-tradition'

& '.\.venv-public\Scripts\python.exe' -I -B -X utf8 -c "import sys; sys.path.insert(0, 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation'); from s0_i0.cli import main; raise SystemExit(main(['integrity']))"

& '.\.venv-public\Scripts\python.exe' -I -B -X utf8 -c "import sys; sys.path.insert(0, 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation'); from s0_i0.cli import main; raise SystemExit(main(['schema-check']))"

& '.\.venv-public\Scripts\python.exe' -I -B -X utf8 -c "import sys; sys.path.insert(0, 'C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation'); from s0_i0.cli import main; raise SystemExit(main(['verify']))"
```

These are direct calls to the authenticated existing entry point, not a new launcher. The recorded test used the same interpreter flags, implementation directory, and handler arguments with the additional observation wrapper described above. DOCUMENTATION checked these commands against admitted source but did not execute them.

## Environment and setup provenance

The [lock file](requirements.lock.txt) freezes 18 package names, versions, and wheel SHA-256 values, including the original A04 `jsonschema[format]==4.26.0` requirement. CODE's handoff reports creating the previously absent `.venv-public` with the pinned base Python's standard `venv` module, then installing with standard pip; both setup commands returned `0`. Only `.venv-public/` was appended to the existing `.gitignore` entries. The generated environment and install receipt remain local and ignored; binaries are not part of this candidate's manifest.

CONTROL's setup handoff reports a Python 3.12.10 / pip 25.0.1 dry run that selected 18 wheels totaling about 1.4 MB and cross-checked each wheel URL, size, and SHA-256 against the official PyPI version JSON. An earlier planning dry run failed while printing its report with a `cp949` `UnicodeEncodeError`; selecting UTF-8 resolved that reporting issue. It was not a dependency-resolution failure or an A04 code correction. These planning and setup observations are attributed to CONTROL/CODE; DOCUMENTATION did not repeat network or installer operations.

The completed setup used these standard command shapes, with absolute paths to the pinned base Python, environment, lock, and receipt:

```text
base-python -I -B -X utf8 -m venv <repository>/.venv-public
env-python -I -B -X utf8 -m pip --isolated install --require-hashes --only-binary=:all: --no-cache-dir --disable-pip-version-check --timeout 20 --retries 1 --index-url https://pypi.org/simple --report <repository>/.venv-public/install-report.json -r <candidate>/requirements.lock.txt
```

These describe completed installation, not a daily rerun instruction. There was no custom downloader, verifier, or launcher and no requested system/global installation. CODE reported no base or documentation-environment package mutation; the TEST record authenticated the base executable, not the complete base/documentation package trees.

The authenticated standard pip receipt contains 18 HTTPS wheel URLs on `files.pythonhosted.org` with versions and digests matching the lock. Installed metadata and `pip check` support ordinary dependency consistency. The receipt is not independent publisher, redirect-chain, hostile-index, or supply-chain attestation.

## Evidence and preservation

Repository: `C:/Users/SSAFY/Documents/ai-development-tradition`.

| Identity | Frozen value |
| --- | --- |
| Branch | `codex/windows-build-toolchain-environment-v0.1` |
| HEAD | `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a` |
| HEAD tree | `82c02f37fd13ecfc8c7b888bb66127989b6d4f34` |
| Candidate | `s0-lab/audit-remediation/a07-public-cli-readiness-v0.1` |
| Lock SHA-256 | `58a76393ebeb1d098c09bd74713704673d4b2c768162bb903145e7d2acbd9c71` |
| TEST producer SHA-256 | `b29360f0844a405dbc72bbeece4d98552eb21ade006efee064fbd638bd7b5625` |
| JSON result SHA-256 | `011fb8de441c82ac975e649648495e752cf7afa581bfd9df4131a5f764f6a1ea` |
| Transcript SHA-256 | `0f3beb4f388b518c7fc34bfa3a0b9762b412c106e8530a9826ba36045f6d6607` |

The completed parent test command was:

```powershell
& 'C:\Users\SSAFY\AppData\Local\Python\pythoncore-3.12-64\python.exe' -I -S -B -X utf8 'C:\Users\SSAFY\Documents\ai-development-tradition\s0-lab\audit-remediation\a07-public-cli-readiness-v0.1\tests\verify_public_cli.py'
```

This is a record of the completed run, not a harmless daily command: the runner creates its two result files exclusively and refuses to overwrite existing outputs. Preserve the frozen run. Any newly authorized verification must retain the old evidence and its original input pins; do not rewrite an old expected `AGENTS.md` hash to force a historical run to pass.

[SCOPE-AND-CHECKLIST.md](SCOPE-AND-CHECKLIST.md) records roles, exact input authorities, the earlier CONTROL checklist, and claim limits. It was authored after CODE and TEST. [artifact-files.sha256](artifact-files.sha256) contains exactly eight candidate-relative entries: the lock, three TEST artifacts, and two Markdown/sidecar pairs. It excludes itself, any future disposition, `.gitignore`, and the local environment. `.gitignore` is separately pinned as an external configuration prerequisite.

## Limits and remaining work

The native `rpds.cp312-win_amd64.pyd` dependency was loaded as part of ordinary jsonschema dependency execution. This is not project-native preloader execution, Win32 runtime rehearsal, or validation of historical native evidence. The historical 36-test suite was not rerun.

Interpreter, standard-library, and native-library closure; hostile concurrent replacement; Windows ACL, root/volume authority, retained handles, rename/rebinding, and TOCTOU protection remain unverified. Ordinary path observations and pre/post hashes do not prove these properties or enforced role isolation. Those limits constrain broader safety claims; they do not erase the recorded bounded public CLI success.

Fresh independent review is planned to assess source/configuration and neutral requirements before seeing test counts, results, or these documents, then inspect evidence after its primary assessment. That sequence is a plan, not a completed review or proof of enforced read isolation. CONTROL's final disposition and the remaining audit/maintenance work are still required. No publication approval, Git mutation, F0-content gate, S0/E0 execution gate, or wider project completion is granted here; the unclassified Git-status blocker remains in force.
