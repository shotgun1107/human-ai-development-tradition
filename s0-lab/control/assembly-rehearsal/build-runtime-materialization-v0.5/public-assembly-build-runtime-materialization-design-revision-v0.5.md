# S0 v0.14 public assembly build and runtime materialization design revision v0.5

## 1. Status and scope

This is a PUBLIC design-only mandatory overlay over the authenticated v0.4
package. It corrects exactly the two MAJOR findings in the authenticated v0.4
independent review. It does not authorize a build, compiler, binary, runtime
tree, native call, process, rehearsal, provider/model task, S0, or E0 run.

The exact base identities are:

- v0.4 package manifest SHA-256:
  `7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884`;
- v0.4 independent review SHA-256:
  `7cc81d81c12a4ca1ffec7db8c1bb10fcae161b8ed5fac6e5fe96add550334313`;
- v0.4 profile schema SHA-256:
  `6b55b98aa56111a1ffdc589eda90a605e58b04005bb5449015ed44b6ab4d7882`;
- v0.4 mutation matrix SHA-256:
  `9d2522bdce4a64b612fbac300ff3090d317da32e7bb85b7c021e2ae030a8bf0e`.

The effective composition is the authenticated v0.4 base plus every mandatory
v0.5 correction in this package. Direct v0.4 execution is forbidden. No
consumer may select one version or silently ignore this overlay.

## 2. Exact semantic-relation correction

### 2.1 One-position patch

The authenticated v0.4 semantic relation array has 68 entries. Its zero-based
index 15 is exactly:

`application-directory-equals-parent-of-verifier_application-runtime-row`

The effective v0.5 array replaces only that entry with the exact authenticated
v0.3 byte string:

`application-directory-equals-parent-of-verifier-application-runtime-row`

Every other index, byte string, order position, and the count 68 must remain
byte-identical to v0.4. The patch is invalid if the required old value is not
at index 15, if it occurs at another index, if more than one index changes, or
if the resulting array contains a duplicate.

### 2.2 Effective relation preimage

The effective relation digest uses exact ASCII with one LF after every line,
including the last. It has no BOM, CR, blank line, trailing whitespace, or
extra field. Its grammar is:

```text
S0-BRM-SEMANTIC-RELATIONS-5
relation_count=68
index=<canonical unsigned decimal>
relation=<exact ASCII relation byte string>
```

The last two lines repeat for indices 0 through 67 in ascending order.
Canonical unsigned decimal is `0` or a nonzero digit followed by zero or more
digits. The preimage is 6,805 bytes and its SHA-256 is:

`5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`

The outer semantic validator must reconstruct this preimage from the
authenticated v0.4 array and the exact one-position patch before importing a
candidate or creating a process. The underscore spelling is retained only as
the required old value used to authenticate the patch. It is not an active
effective relation.

This closes `BRM-V04-IR-001` without declaring a new runtime behavior.

## 3. Single publication-policy hash authority

### 3.1 Sole normative object

There is exactly one normative policy hash preimage:

`base_profile.publication_no_replace_policy`

The authenticated v0.4 base profile schema closes that object to exactly these
20 fields:

1. `api_dll`;
2. `api_name`;
3. `destination_name_source`;
4. `destination_overwrite_allowed`;
5. `file_information_class_name`;
6. `file_information_class_numeric`;
7. `file_name_length_rule`;
8. `flags_numeric`;
9. `linearization_point`;
10. `posix_semantics_flag_numeric`;
11. `posix_semantics_flag_set`;
12. `precheck_authority`;
13. `replace_if_exists_flag_numeric`;
14. `replace_if_exists_flag_set`;
15. `retry_allowed`;
16. `root_directory_handle_source`;
17. `same_volume_required`;
18. `source_handle_required_access`;
19. `source_handle_source`; and
20. `terminal_failure`.

The v0.5 interface map deliberately does not republish another same-named
policy object. Its `publication_no_replace_policy_authority` is a binding
record only. The 17-field v0.4 interface-map object is an authenticated
historical summary but is nonauthoritative for hashing. The unconstrained
v0.4 instance digest is also nonauthoritative until v0.5 recomputation.

### 3.2 Exact hash construction

Serialize only the normative 20-field object using RFC 8785 JCS UTF-8, append
exactly one LF byte, and hash those 896 bytes with SHA-256. The only accepted
digest is:

`3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`

The v0.5 outer schema requires the embedded v0.4 profile's
`publication_no_replace_policy_sha256` to equal that digest and publishes the
same digest as its outer policy identity. The prepublication and final record
policy fields must equal it. A map summary hash, an object with 17 fields, an
object with reordered array values, a missing or additional field, a different
JCS result, or any other source path fails `BR-AUTH/0` before record freeze,
candidate import, or process creation.

This closes `BRM-V04-IR-002` while retaining the v0.4 no-replace API, access,
flags, handle, phase, failure, and no-retry rules unchanged.

## 4. Machine package and records

The v0.5 profile is an outer admission overlay. It embeds one exact v0.4
profile, validates that profile through the authenticated v0.4 schema, and
then requires the relation patch and policy authority above. Schema validity
alone is diagnostic and never grants build or execution authority.

The v0.4 prepublication and final record schemas remain the only record
schemas:

- prepublication schema SHA-256:
  `39f8bc081c7d60c4d560704cbe92737b255cc75da922b7f1c1cf13d31c1d8b58`;
- final schema SHA-256:
  `db385701a3a4a6130734e94b0f238b006b8eb5bd9d96f677c3559337a5399430`.

No record field, order, publication phase, Windows directory rule, resource
limit, import rule, binary rule, or claim boundary is replaced by v0.5.

## 5. Failure matrix

The effective matrix is the authenticated 111-row v0.4 matrix followed by the
four published v0.5 rows, for 115 unique IDs. The four rows reject:

- failure to apply the one exact relation patch;
- any other relation byte, order, count, preimage, or digest drift;
- use of any nonnormative policy object as the hash preimage; and
- any policy object, digest, or record binding inconsistent with the unique
  20-field authority.

Every row retains one primary failure and one output-created Boolean whose
`/0` or `/1` suffix agrees with that Boolean. Cleanup, record, quarantine, and
retry observations never replace the first primary failure.

## 6. Nonregression and closed gates

All v0.4 behavior not explicitly replaced in Sections 2 and 3 remains exact.
In particular, the v0.4 Windows directory identity and no-replace publication
closures remain mandatory. The 12 resource values, record packages, authority
pins, binary/import rules, runtime policy, and design-only claim limits are
unchanged.

No source, toolchain, compiler, build, binary, runtime tree, native API,
platform probe, provider/model, executor, judge, S0, or E0 action is opened.
F0 content remains denied. A fresh independent PUBLIC design review must
authenticate the exact package and reconstruct both corrections before any
CONTROL integration or implementation consideration.
