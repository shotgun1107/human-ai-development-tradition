# I1 public runtime v0.2 minor rereview

## Review authority and result

- Gate: `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES V0.2 MINOR REREVIEW OPEN`
- Review date: 2026-08-09 KST
- Candidate branch: `codex/s0-i1-public-runtime-v02`
- Candidate commit: `105aa12c93bdbca9b693ae600806d0359d621d7e`
- Candidate parent: `8160c8a86e93d8339787fd56209fb5060ab30850`
- Review role: fresh independent limited public-only rereviewer
- Sole predecessor review authority:
  `i1-public-runtime-v02-independent-review-v0.1.md`
- Official verdict: `PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`

`I1-v02-m01` is **CLOSED**. No blocking, major, or minor defect and no
changed-line regression remains in this limited rereview scope.

No candidate input was changed. No fixture, oracle, key, role, executor,
model call, score, sealed/E0 access, S0 run, commit, push, or other-agent
evidence was used.

## Baseline and input authentication

| Check | Observed result |
|---|---|
| origin | exact `https://github.com/shotgun1107/human-ai-development-tradition.git` |
| branch | exact `codex/s0-i1-public-runtime-v02` |
| HEAD | exact `105aa12c93bdbca9b693ae600806d0359d621d7e` |
| remote-tracking ref | exact candidate HEAD |
| first parent | exact `8160c8a86e93d8339787fd56209fb5060ab30850` |
| initial worktree and index | clean |
| parent-to-HEAD paths | exactly the six authorized modified files |
| mode/scope check | all six remain mode `100644`; no create, delete, mode change, or path outside `s0-lab/i1/**` |
| candidate I1 tree | exactly 28 tracked regular files, all mode `100644` |

The parent-to-HEAD changes were exactly:

- `s0-lab/i1/README.md`
- `s0-lab/i1/implementation/s0_i1/auth.py`
- `s0-lab/i1/tests/test_auth.py`
- `s0-lab/i1/verification/implementation-files.sha256`
- `s0-lab/i1/verification/implementation-manifest.sha256`
- `s0-lab/i1/verification/verification-report.md`

Frozen-input authentication passed before substantive rereview:

| Input | Observed SHA-256 or binding |
|---|---|
| `AGENTS.md` | `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` |
| predecessor review Markdown | `0f488a479d2feaa7de1afc10316e20f635017265ba9d95268993953582dd050d` |
| predecessor review sidecar | exact Markdown digest and basename; sidecar file SHA-256 `5b46ee4c9c2c315201edf32a9edb3295cb3c65246846532718f5450b05bd691d` |
| public-spec manifest | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e`, exactly 7 canonical rows |
| implementation payload manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c`, exactly 26 canonical rows |
| implementation-manifest file | `1a2599c4da568cce2ade6eb9cb3ccfa6d14fc556c4823dca69329a9eb6bffee6` |
| implementation-manifest content | exact payload-manifest digest and exact basename |

Every public-spec and implementation manifest target matched its recorded
digest. The 26 payload rows were unique and exactly equal to the complete I1
tree excluding the payload manifest and its one-line binding file. Together,
those checks authenticated all 28 candidate I1 files.

The canonical text-artifact validator passed all 11 self-tests before use. The
predecessor review and all 28 candidate I1 files were then read in full. No
authentication, baseline, role-boundary, or permission blocker occurred.

## Executed verification

The shipped verifier was run independently with bytecode writes disabled and
the exact external anchor:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1 -ExpectedManifestSha256 668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c
```

It exited 0. Its pre-execution and final-stability external-anchor, text,
26-row, forced-hidden exact-file-set, and snapshot-equality checks passed. The
authenticated OS-temporary execution snapshot was removed. Python was 3.14.6
and `jsonschema` was exactly 4.26.0. The unit suite ran 61 tests: 60 passed and
the direct Windows symlink-creation case was skipped because the host denied
unprivileged symlink creation. The privilege-free reparse sentinel and mocked
rejection path ran. The CLI returned machine-readable `pass` with 7
authenticated spec files, 6 Draft 2020-12 schemas, 39 accepted positive
instances, 12 rejected negative instances, 0 topology issues, and 0 forbidden
runtime imports.

The shipped result was not treated as self-proving. A separate automatically
removed OS-temporary harness established all of the following:

- `get_type_hints` resolves the `value` parameter of
  `authenticate_manifest_entry`, `_safe_relative`, and `_read_once` to exact
  `str`;
- the `workspace_root` parameter of the public entry function and `_read_once`
  remains `pathlib.Path`;
- the canonical POSIX-relative string `inputs/n/x.bin` authenticates and
  returns its exact sentinel bytes;
- the concrete Windows host value `WindowsPath('inputs/n/x.bin')` rejects with
  exact `UnsafePathError: path must be exact string text`;
- the same concrete `Path` rejects through `_safe_relative` and `_read_once`,
  and the diagnostic does not advertise `Path` support; and
- a `str` subclass, traversal, an absolute path, backslashes, an ADS colon, and
  a null byte all fail closed.

The harness left no temporary directory or Python bytecode cache.

## Finding decision

### I1-v02-m01 — CLOSED

Facts from the authenticated candidate:

- `authenticate_manifest_entry(..., value: str, ...)` now advertises the
  supported public contract.
- `_safe_relative(value: str)` requires `type(value) is str`, retains the
  canonical POSIX-relative checks, and reports `path must be exact string
  text` for a concrete `Path`.
- `_read_once(..., value: str, ...)` no longer retains a conflicting union.
- README and verification-report statements agree that manifest, namespace,
  and entry identifiers are exact canonical POSIX-relative strings, while the
  filesystem workspace root remains a `Path`.
- The shipped regression test and the independent harness both exercised a
  successful canonical string and a rejected concrete `Path`.

Conclusion: the annotation, runtime behavior, diagnostic, helper contracts,
tests, and public documentation now describe the same exact-string API. The
predecessor minor finding is closed without broadening accepted path types.

No new blocking, major, or minor finding was identified.

## Limited non-regression review

The executable change is limited to narrowing three identifier annotations,
requiring exact `str`, and removing the former `str(value)` conversion. The
existing checks for empty values, backslashes, null bytes, absolute paths,
`.`/`..` normalization, drive/ADS colons, and noncanonical POSIX spelling are
unchanged. Manifest revalidation, granted-path membership, read-once behavior,
namespace enumeration, and snapshot semantics are unchanged.

The other changed lines add the matching regression test and documentation,
update the accurate 61/60/1 test count, and refresh the authenticated manifest
digests. The 26-row manifest, its one-line binding, the test result, and the
report agree. The public-spec manifest authority and topology snapshot inputs
did not change.

The exact six-file diff contains no key, root, registry, bank, oracle,
provider/network/model call, executor, scoring, sealed/E0, fixture, or S0 work.
A targeted scan of the authenticated I1 tree found no D-favoring vocabulary,
condition-specific model path, post-result threshold change, answer hint,
oracle access, or scoring path. Mentions of answers, oracles, models, scoring,
and A-D occur only in explicit closed-boundary or no-claim statements.

## A-D symmetry, leakage, and claim limit

I1 does not implement or test whether A-D receive the same source information,
authority, model revision or reasoning conditions, elapsed time, questions,
retries, or scoring opportunities. It therefore supplies no operational
fairness evidence. Nothing in this limited contract correction changes that
boundary.

The maximum justified claim is narrow: at the authenticated candidate commit,
the public manifest-entry API consistently requires exact canonical
POSIX-relative string identifiers, intentionally rejects concrete
`pathlib.Path` identifiers, and preserves the previously reviewed public
construction behavior under trusted injected inputs.

The remaining non-defect boundaries are unchanged:

- manifest pins, signer assignments, the verifier copy, and the integration
  caller must be independently trusted;
- hostile code in the same Python process can bypass module-private markers,
  so later process/VM role isolation remains required;
- filesystem observations are not atomic and do not resist a privileged writer
  after return;
- signatures are decisions from an injected verifier, not cryptographic or
  registry proof;
- stores, durable ACLs, atomic E51/E54 writes, duplicate-publication
  prevention, keys, roots, registries, providers, and models remain absent;
  and
- A-D information/model/time/scoring equality, sealed compatibility,
  execution, scoring, and every S0 outcome remain untested.

No empirical, security, operational-safety, economic, production,
model-to-model transfer, Project Brain, central-system, or S0 conclusion
follows from this synthetic public construction check.

## Official verdict

`PASS-FOR-NEXT-GATE-CONSIDERATION-ONLY`

This pass opens no trust-root, role-isolation, key, sealed, executor,
model-call, scoring, E0, or S0 gate. It permits only CONTROL/user consideration
of the next separately approved phase. No commit or push is authorized by this
rereview.
