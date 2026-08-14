# Public assembly runtime profile and neutral preloader implementation candidate report v0.3

## 1. Scope and provenance

This package is a bounded public revision of the v0.2 offline implementation
candidate. It responds to the authenticated v0.2 independent implementation
rereview result. It is not a runtime-profile materialization, native neutral
preloader, implementation acceptance, platform result, or public assembly
rehearsal.

- repository: `human-ai-development-tradition`;
- revision baseline commit:
  `43d06493e8d1fdab6a76eb8c1a873ec3be02e3e2`;
- revision baseline tree:
  `3e2764b5c83a1bd42429d78b96b5f105f55cd4a1`;
- implementation branch:
  `codex/s0-rpnp-v03-implementation-revision-v01`;
- v0.2 candidate commit:
  `34f0422531499e342aecddc9c25c65e074658759`;
- v0.2 independent-rereview preservation-record SHA-256:
  `0b55f7af3c63d497702b581de5c809367ac0dd2ac59e1bba46b0f803aca2a4f5`;
- v0.4 design-package manifest SHA-256:
  `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589`;
- approving v0.4 design-rereview preservation-record SHA-256:
  `9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71`;
- v0.3 implementation-manifest SHA-256:
  `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2`.

The implementation manifest covers ten package sources and one test source.
No runtime profile, executable, persisted synthetic fixture, hidden oracle, or
F0 content was created or read.

## 2. v0.2 rereview findings and v0.3 response

| v0.2 finding | v0.3 response | Current bounded disposition |
|---|---|---|
| MAJOR: runtime-file targets were verified and then reread from a caller-held stateful mapping | The caller bundle is reconstructed into one private snapshot. Byte mappings accept only exact `dict` or implementation-created `mappingproxy` values, are copied, and are consumed through the same snapshot for manifest verification, launch material, identity, and evidence. The private preparation helper also snapshots at its own boundary. | CLOSED by deterministic stateful-mapping regression and Daybreak Blue exploit reproduction. |
| MAJOR: a mutated `PostcreationObservation.source` entered locator-free admission bytes | Every postcreation field is reconstructed through the exact dataclass validator. The admission builder consumes only that private observation and rejects locator-shaped string values. | CLOSED by `object.__setattr__` locator regression and Daybreak Blue exploit reproduction. |
| MINOR: `FixedDraft202012Validator` retained the caller schema dictionary | The validator recursively copies JSON-only schema values before keyword audit and retains only the private copy. It also rejects non-finite numbers, malformed schema-node types, and wrong supported-keyword value types. | CLOSED for caller clear and nested mutation, malformed `uniqueItems`, property-member, and `prefixItems` probes. Direct mutation of the conventional-private `_schema` attribute is outside the authenticated high-level path and is not presented as authority. |

## 3. Additional implementation-subreview corrections

A fresh `gpt-daybreak-blue-latest` implementation and security subreview was
used during the revision. It was read-only and was not the formal independent
candidate gate.

The subreview found and the candidate closed:

1. mutable inner system-image export rows, by requiring exact tuple pairs and
   reconstructing each pair into the private static snapshot;
2. malformed supported schema-keyword values and non-object nested schema
   nodes, by auditing keyword value types before instance validation; and
3. named Path and file-metadata diagnostic gaps including `iterdir`, `glob`,
   `rglob`, `stat`, `lstat`, `exists`, `resolve`, `is_file`, and `walk`.

The final subreview reported BLOCKING `0`, MAJOR `0`, and one explicit MINOR
limitation for the non-authoritative source diagnostic. Section 6 preserves
that limitation rather than misclassifying the diagnostic as a security proof.

## 4. Implemented bounded behavior

The v0.3 package preserves the v0.2 offline-only behavior and adds:

1. one private static-material snapshot per preparation operation;
2. reconstruction of predecessor, artifact, system-image, manifest-target,
   and effective-package material into immutable exact-type containers;
3. exact reconstruction and revalidation of postcreation observations before
   relation checking or admission serialization;
4. locator-shaped admission-value rejection;
5. a private JSON-only schema copy with supported-keyword value-type and
   schema-node audits; and
6. deterministic regressions for the three v0.2 findings and adjacent
   system-image, schema, and source-diagnostic mutations.

The candidate still returns only openly constructible `candidate_only` data.
There is no native invocation method, and every prepared result has
`native_api_reachable=False`.

## 5. Verification results

CONTROL ran the complete bounded offline suites with
`PYTHONDONTWRITEBYTECODE=1`:

- v0.3 revision suite: `20 / 20 PASS`;
- v0.1 runtime/preloader regression suite: `13 / 13 PASS`;
- existing public assembly candidate regression suite: `47 / 47 PASS`;
- total: `80 / 80 PASS`.

The Daybreak Blue subreview independently ran the exact allowlist-safe suites:

- v0.3 revision suite: `20 / 20 PASS`;
- v0.1 runtime/preloader regression suite: `13 / 13 PASS`.

It did not run the old 47-test suite because that suite's additional component
and design inputs were outside its role allowlist. It did not broaden the
boundary. CONTROL's separate `47 / 47 PASS` is the evidence for that suite.

The v0.3 suite also confirmed:

- all four pinned schema-family samples accepted;
- required-property deletion mutations: `185 / 185` rejected;
- closed-object unknown-property mutations: `28 / 28` rejected;
- fixed-constant mutations: `106 / 106` rejected;
- all eleven Python files strict UTF-8, LF-only, final-LF, BOM-free, and
  successfully AST-parsed;
- exact 32-row and 6-row integration target closures; and
- the stateful mapping, mutated observation, caller schema mutation, mutable
  export pair, malformed schema node, wrong keyword type, and named source
  diagnostic probes rejected.

## 6. Known non-authoritative diagnostic limitation

`source_audit.py` is defense in depth over already supplied bytes. It is not a
capability proof, sandbox, admission predicate, manifest authority, or
implementation-acceptance authority.

The final implementation subreview demonstrated that synthetic expressions
using ambiguous method names such as `value.replace(...)`, `value.read()`, and
`value.write(...)` are not all rejected by its name-based AST checks. A blanket
ban on `replace` would also reject the candidate's ordinary string processing,
while name inspection alone cannot prove the receiver's runtime type.

This limitation is explicitly accepted for candidate packaging because:

- no consumer treats the diagnostic result as authority;
- exact manifest authentication and independent source review remain
  mandatory; and
- the candidate makes no claim of complete capability exclusion from this
  diagnostic.

The formal independent rereview may reject this disposition or require a
different positive source-analysis design. This candidate does not pre-approve
that decision.

## 7. Deliberately unexecuted and unproved work

This candidate does not prove or claim:

- authenticated runtime-profile or executable materialization;
- PE parsing, source-to-binary provenance, file identity, loaded-image
  identity, export address, or direct-import observation;
- native guard, compiler, linker, import table, CRT, or system-image closure;
- actual application, token, security-attribute, mitigation, job, or process
  creation behavior;
- live handle inheritance, current PID, kernel semantics, or platform probe;
- production admission-frame acceptance;
- native API invocation, child creation, provider/model access, F0 access,
  hidden-oracle access, or public assembly rehearsal; or
- implementation acceptance, CONTROL integration, commit, push, PR, merge,
  or main integration.

The three deferred static relations still require separately authenticated
native or platform-derived evidence. Candidate-only offline checks do not
complete that future work.

## 8. Candidate disposition

The v0.3 bytes are suitable for an independent implementation rereview with
the Section 6 MINOR limitation explicitly admitted. They must not be treated
as live authority or as approval to materialize a runtime package, invoke
native APIs, run a platform probe, or open an assembly rehearsal.

The next candidate gate, if separately and explicitly opened, is:

`S0 V0.14 PUBLIC ASSEMBLY RUNTIME PROFILE + NEUTRAL PRELOADER BOUNDED PUBLIC IMPLEMENTATION CANDIDATE V0.3 INDEPENDENT REREVIEW OPEN`
