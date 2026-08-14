# S0 v0.14 public assembly build and runtime materialization v0.2 review response v0.1

- `responds_to_review_sha256`: `85c917496b04246be173dafa2ffd729fa80e836d363de0ab982f593c42efa292`
- `prior_verdict`: `REVISE-AND-REVIEW`
- `prior_findings`: `0 BLOCKING / 5 MAJOR / 0 MINOR`
- `author_claim`: proposal-text closure only; independent rereview required
- `implementation_status`: not implemented

## 1. BRM-IR-001 response

### Prior defect

The v0.1 closed authority object omitted baseline commit, baseline tree,
bounded verification manifest, and integration v0.1 manifest. The ten-pin
closure had no separate pre-execution runtime-tree profile identity.

### v0.2 change

The new admission wrapper requires the four omitted current authorities, the
exact v0.2 package hash, and fresh approving review hash. It represents all
ten external classes without self-reference: eight exact manifest identities,
the canonical embedded base-profile hash, and approving-review hash.

The runtime-tree profile is a distinct manifest identity and cannot be
substituted by the output runtime-package manifest. Each manifest identity
binds manifest SHA-256, target count, total bytes, and target-set SHA-256.
Six overlapping v0.1/v0.2 closures must compare byte-identical.

### Closure evidence requested

The reviewer must remove and mutate every field, test all ten hostile pin
families, and prove failure before candidate import or process creation.

## 2. BRM-IR-002 response

### Prior defect

The binary schema could not encode the complete guard export, PE, relocation,
resource, manifest, debug, CLR, import, loader, FFI, path, and timestamp policy.

### v0.2 change

The wrapper requires exactly one preloader and one guard profile. Both bind
the exact artifact and every section/import/export/relocation/resource/
manifest/load-config inspection product. Fourteen named forbidden predicates
are exact zero counts. Relocations and four mitigations are mandatory.

The preloader and guard receive exact role-specific direct imports, and the
guard receives its exact initialization export. Complete authenticated import
and export allowlist manifests remain controlling. The inspector must not load
the image, and inspected, built, materialized, and later loaded bytes must form
one identity chain.

### Closure evidence requested

The reviewer must mutate every required field and zero predicate, attack role
assignment and allowlist equality, and verify that no tool PASS string can
replace parsed byte-bound facts.

## 3. BRM-IR-003 response

### Prior defect

The runtime-package schema lacked exact CPython ABI and flags, source-only
module mapping, DLL selection, jsonschema identity, ambient denials, and the
complete required runtime-role set.

### v0.2 change

Fourteen exact role keys are mandatory and must cover every base runtime row
exactly once. CPython 3.12 Windows AMD64, ordered `-I/-S/-B`, jsonschema
4.26.0, exact module and DLL maps, application selection, and DLL search are
closed fields.

Host Python, user site, `site`, `PYTHONPATH`, current directory, PATH,
registry, package installation, bytecode, namespace fallback, unlisted module
or DLL, and unclassified runtime rows are expressly forbidden.

### Closure evidence requested

The reviewer must test every missing/extra/duplicate role and every ambient
fallback, then independently trace every module/DLL binding to one exact base
runtime row and authenticated byte hash.

## 4. BRM-IR-004 response

### Prior defect

The 46-row base matrix omitted an explicit output-state bit and grouped
missing/extra output, resource-bound timing, and retry histories that require
different first failures.

### v0.2 change

The effective matrix is exactly 63 rows. Forty-three retained rows receive an
explicit primary failure and Boolean output-state value. Three ambiguous base
rows are removed and replaced by twenty rows:

- three missing/partial/extra-output cases;
- eight before/after-output resource-bound cases; and
- nine retry cases preserving every prior primary class.

The composition algorithm fixes order and insertion positions. The first
primary failure is immutable; later cleanup, quarantine, record, and retry
events are secondary.

### Closure evidence requested

The reviewer must reconstruct all 63 rows from authenticated bytes, verify
unique IDs and Boolean/suffix agreement, and inject every later failure after
every primary class.

## 5. BRM-IR-005 response

### Prior defect

v0.1 froze a record before publication even though that record was required
to contain publication facts. It also did not preselect which identical A/B
root was published.

### v0.2 change

A is the immutable publication owner and B the comparison peer before build.
After equality, B is quarantined before any A publication. A prepublication
record contains only facts already observed and expressly excludes rename
success and final identity. A is then renamed once into a private,
nonauthoritative destination, reopened, identity-checked, enumerated, and
rehashed. Only then is the final diagnostic record written.

A later-stage failure quarantines the candidate and grants no authority. The
published candidate path and all records remain diagnostic-only.

### Closure evidence requested

The reviewer must permute, omit, duplicate, and fabricate every phase; attempt
B selection and result-based owner selection; and prove no record claims a
fact before it exists.

## 6. Author-side disposition

All five findings are addressed at proposal-text and machine-contract level.
This response is not independent evidence and does not change the prior
verdict. The design remains unapproved until a fresh reviewer authenticates
the exact package and returns zero BLOCKING and zero MAJOR findings.

No source, compiler, build, binary, runtime tree, native execution, F0 input,
provider/model call, S0, or E0 result was created or observed.
