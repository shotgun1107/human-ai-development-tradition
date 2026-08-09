# I1 public runtime v0.2 independent review

## Review authority and result

- Gate: `S0 V0.14 PUBLIC IMPLEMENTATION PREREQUISITES V0.2 INDEPENDENT REVIEW OPEN`
- Review date: 2026-08-09 KST
- Candidate branch: `codex/s0-i1-public-runtime-v02`
- Candidate commit: `a008d99dce8104e8e9c05c10902255a3f434ec71`
- Candidate parent: `5b3b6b1ce7a231613e7ab64f093b6f2a07718323`
- Review role: fresh public-only hostile reviewer
- Official verdict: `REVISE-AND-REVIEW`

The six predecessor major findings and the predecessor minor finding are closed
within the expressly limited public construction scope. One new minor API
contract defect remains. There is no fundamental contradiction and therefore
no basis for `FAIL`, but the rule for this gate does not permit a pass while a
minor defect remains.

No candidate code was changed. No fixture, oracle, key, role, executor, model
call, score, sealed/E0 access, S0 run, commit, push, or other-agent evidence was
used.

## Baseline and input authentication

| Check | Observed result |
|---|---|
| origin | exact `https://github.com/shotgun1107/human-ai-development-tradition.git` |
| branch | exact `codex/s0-i1-public-runtime-v02` |
| HEAD | exact `a008d99dce8104e8e9c05c10902255a3f434ec71` |
| remote-tracking ref | exact candidate HEAD |
| first parent | exact `5b3b6b1ce7a231613e7ab64f093b6f2a07718323` |
| initial worktree and index | clean |
| candidate diff | 24 paths, all under `s0-lab/i1/**` |
| mode/scope check | no create/delete/mode change and no path outside I1 |
| candidate I1 tree | 28 tracked regular files, all mode `100644` |

Every allowlisted Markdown file was read in full. Every same-basename sidecar
authenticated its Markdown bytes. The expected and observed Markdown SHA-256
values were identical:

| Input | SHA-256 |
|---|---|
| `AGENTS.md` | `ff2dd3950486864aa2c3fbfa8c6d5af4b2204c20b50ce8efbc8be181e6474844` |
| S0 protocol v0.3 | `b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c` |
| universal response contract v0.14 candidate | `49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0` |
| public falsification plan v0.11 | `a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee` |
| review response v0.9 | `b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9` |
| URC v0.14 independent review v0.1 | `537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605` |
| CONTROL integration decision v0.1 | `f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65` |
| predecessor I1 independent review v0.1 | `fbd0a2d730010d3de5c451663836627c0cae55746191a402af3b0cea1c434882` |

The canonical text-artifact validator passed all 11 self-tests before use.
Every allowlisted pair passed its independent UTF-8, BOM, final-LF,
sidecar-format, and sidecar-hash checks. The frozen S0 protocol retained its
authenticated, pre-existing Markdown hard-break trailing spaces on lines 3-6;
the validator accurately reports that one trailing-whitespace check as failed.
Those bytes are unchanged by this candidate and are not an I1 v0.2 regression.

All 28 candidate I1 files were read in full. Their namespace authentication
was exact:

| I1 identity | Observed result |
|---|---|
| public-spec manifest | `9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e`, exactly 7 rows |
| implementation payload manifest | `55f1c0e46d934f6fac5a7cf2a41a9dcc3324cf09c1eb01649038016272ad3a94`, exactly 26 rows |
| implementation manifest sidecar file | SHA-256 `441180a0fa26db6215778d0c7b77234b8a627210cfaa18f7807618e5546aaae0` |
| sidecar content | exact payload-manifest digest and exact basename |
| complete I1 set | exact 26 payload files plus the manifest and its sidecar |

No authentication, baseline, role-boundary, or permission blocker occurred.

## Executed verification

The shipped verifier was run independently with bytecode writes disabled and
the required external anchor:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File s0-lab/i1/tools/verify-i1.ps1 -ExpectedManifestSha256 55f1c0e46d934f6fac5a7cf2a41a9dcc3324cf09c1eb01649038016272ad3a94
```

It exited 0. Pre-execution and final-stability external-anchor, text,
26-row, forced-hidden exact-set, and snapshot-equality checks passed. The
authenticated OS-temporary execution snapshot was removed. The unit suite ran
60 tests: 59 passed and the direct Windows symlink-creation case was skipped
because the host denied unprivileged symlink creation; its privilege-free
reparse sentinel and mocked rejection path ran. Python was 3.14.6 and
`jsonschema` was exactly 4.26.0. The CLI returned machine-readable `pass` with
7 public-spec files, 6 Draft 2020-12 schemas, 39 accepted positive instances,
12 rejected negative instances, 0 topology issues, and 0 forbidden runtime
imports.

The shipped result was not treated as self-proving. Separate hostile harnesses
performed these checks:

- M01: 6 labeled checks over the pinned positive path, plain object,
  equivalent grant, self-authored substitution, unsupported direct
  constructor, zero-call behavior, and the documented trusted-caller boundary.
- M02-M04: 69 labeled checks over nested mutation, detached capabilities,
  signer mutation, all receipt identities, bundle branches, every status
  relation, namespace/content mutation, returned-byte stability, and the
  documented post-return filesystem boundary.
- M05: 21 labeled checks over exact frame types, Boolean-as-integer,
  empty/257-frame streams, exact 8,192 and rejected 8,193 bytes, `1e999`,
  `NaN`, `Infinity`, a 21-digit integer, cleanup precedence, and output
  collision before invocation.
- M06: 19 labeled checks over E43/E45 roles, ordering, equality, source
  envelope/record hashes, named digest, exact-Boolean signature result,
  E54/E55 equality, E56 full-envelope binding, full ROOT-through-E56 status
  order, premature E56, and non-increasing time.
- m01: five isolated OS-temporary attacks. Coordinated payload + manifest +
  sidecar mutation under the unchanged external anchor, a forced-hidden extra
  file, a cache file, an uppercase external digest, and an uppercase manifest
  row all rejected before the fake Python sentinel was called. All temporary
  attack directories were removed.

A deliberate mutation immediately after the last namespace enumeration can
still occur after a successful return. The returned first-read bytes remain
unchanged and authenticated. This confirms the implementation's stated
snapshot claim and also confirms that it is not an atomic or hostile
mutable-filesystem guarantee.

## Predecessor finding closure

| Finding | Closure | Independent conclusion |
|---|---|---|
| I1-M01 | CLOSED in this gate's trusted-caller API scope | The runner binds the exact caller-held grant, independent manifest/path/purpose expectations, request provenance, and same bytes before and after its sole call. Plain, direct, equivalent, and substituted authority paths reject with zero calls. A caller that chooses and authenticates its own grant is accepted; this is the explicitly documented same-process trust boundary, not process security. |
| I1-M02 | CLOSED | Topology values are recursively frozen and provenance, manifest pin, full snapshot digest, and audit are rechecked at receipt, store, signer, and policy boundaries. The shallow `MappingProxyType` plus nested mutable attack and post-load mutations reject. |
| I1-M03 | CLOSED | Direct Draft 2020-12 validation enforces the 17 receipt tuples, exact bundle branches/counts, and all 15 sequence/event/mask/status relations including zero genesis previous hash. Runtime-only byte, hash, signature, equality, chain, and time relations are separately identified and enforced in code. |
| I1-M04 | CLOSED for the claimed authenticated returned-byte snapshot | Deterministic namespace and content mutations during the observation sequence reject. Returned first-read bytes are stable. The code and report truthfully disclaim atomic snapshots, post-return stability, and privileged concurrent-writer resistance. |
| I1-M05 | CLOSED | Exact scalar types, bounded decimal parsing, exact/non-empty frames, the 256-frame and 8,192-byte limits, first-final handling, close behavior, primary-error precedence, strict JSON numbers, and pre-invocation output reservation were independently exercised. |
| I1-M06 | CLOSED | E43/E45 source envelopes, extracted records, roles/order, byte equality, custodian, and named digest are recomputed. E54/E55 delivered bytes are equal and rebound. E56 hashes the complete signed publication envelope once, and status ordering permits it only at the final prefix position. |
| I1-m01 | CLOSED | A mandatory independently supplied lowercase manifest digest is checked before candidate execution; adjacent self-authentication is insufficient. Exact case-sensitive syntax, coordinated mutation, forced-hidden/cache files, pre/post equality, separately labeled text diagnostics, and the verifier-bootstrap limitation were confirmed. |

Closing these findings does not turn module-private Python markers into an
adversarial same-process boundary, an observed byte snapshot into filesystem
atomicity, or an injected signature decision into cryptographic verification.

## New finding

### I1-v02-m01 — concrete `pathlib.Path` inputs contradict the advertised API

Severity: **minor**.

`implementation/s0_i1/auth.py` declares `_safe_relative(value: str | Path)`
and the public `authenticate_manifest_entry(..., value: str | Path, ...)`
entry point repeats that union. The check is nevertheless:

```python
if type(value) not in {str, Path}:
    raise UnsafePathError("path must be exact string or Path text")
```

`Path(...)` returns a concrete `WindowsPath` or `PosixPath`, never an object
whose exact type is the abstract `Path` factory. An independently authenticated
entry succeeded with the canonical string `n/x.bin` and the same call with
`Path("n/x.bin")` failed with:

```text
UnsafePathError: path must be exact string or Path text
```

This is fail-closed: it does not permit an unauthorized read, and all current
internal manifest paths are strings. It is still a real public API/type/error
contract contradiction and leaves an advertised integration input untested
and unusable. Closure requires either securely accepting concrete `Path`
instances with canonical relative-path tests or narrowing the annotation and
diagnostic to exact string input, followed by a regression test. This reviewer
has no authority to implement that correction.

No other blocking, major, or minor defect was found in the reviewed public
prerequisite scope.

## A-D symmetry, leakage, and forbidden future scope

The candidate contains no D-targeting selection rule, D-favoring vocabulary,
post-result threshold mutation, answer hint, oracle access, scoring path, or
condition-specific model path. Its A-D statements are explicit denials that
these construction results establish A-D fairness or equality.

I1 does not implement or validate that A-D receive the same source
information, authority, model revision or reasoning conditions, elapsed time,
questions, retries, or scoring opportunities. It therefore supplies no
evidence for operational fairness. Those facts must be frozen and enforced in
later separately authorized executor and scoring phases; they cannot be
inferred from a synthetic topology/codec/runner construction test.

The candidate tree contains no key or cryptographic implementation, trust
root, registry artifact, bank, oracle, S0 fixture, provider/network/model call,
executor creation, scoring, sealed/E0 access, or S0 execution. Role names and
boundary disclaimers are topology vocabulary, not implemented actors or
operational controls. No empirical, security, safety, economic, production,
transfer, or central-system conclusion follows.

## Maximum justified claim and remaining boundaries

At the authenticated candidate commit, the implementation materially closes
all seven predecessor findings as public construction logic under trusted
injected inputs. It authenticates and freezes a public topology snapshot,
enforces the reviewed schema and runtime relations, provides a bounded
provider-neutral one-shot API, and bootstraps candidate tests from externally
anchored authenticated bytes. The new concrete-`Path` API contradiction keeps
the artifact from a defect-free next-gate pass.

The remaining non-defect boundaries are:

- manifest pins, signer assignments, the verifier copy, and the integration
  caller must be independently trusted;
- hostile code in the same Python process can bypass module-private markers,
  so later process/VM role isolation is still required;
- filesystem observations are not atomic and do not resist a privileged
  writer after return;
- signatures are decisions from an injected verifier, not cryptographic or
  registry proof;
- stores, durable ACLs, atomic E51/E54 writes, duplicate-publication
  prevention, keys, roots, registries, providers, and models remain absent;
- A-D information/model/time/scoring equality, sealed compatibility,
  execution, scoring, and every S0 outcome remain untested.

## Official verdict

`REVISE-AND-REVIEW`

This verdict authorizes no correction, commit, push, trust-root work,
role-isolation work, sealed work, executor creation, model call, scoring, or S0
run. After the minor API contract defect is corrected under separate authority,
a fresh review is required. Even a later pass could permit only CONTROL/user
consideration of the next separately approved phase.
