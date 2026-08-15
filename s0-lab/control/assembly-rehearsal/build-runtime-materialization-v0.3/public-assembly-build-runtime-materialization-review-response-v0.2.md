# S0 v0.14 public assembly build and runtime materialization v0.3 review response v0.2

- `responds_to_review_sha256`: `d5066d11172cdc33441e39087898a33ab14b5371533a0f4f529de92eb80be051`
- `prior_verdict`: `REVISE-AND-REVIEW`
- `prior_findings`: `0 BLOCKING / 4 MAJOR / 0 MINOR`
- `author_claim`: proposal-text closure only; independent review required
- `implementation_status`: not implemented

## 1. BRM-V02-IR-001 response

v0.3 defines the complete ASCII/LF preimage for every target-set digest. It
fixes header and row field order, path grammar and ordering, duplicate and
empty rules, canonical decimals, target lengths and hashes, and the final LF.
The interface map and schema add exact semantic relations; the mutation
matrix adds eight hostile rows.

Requested review evidence: independently construct the same preimage and
hash, then attack every byte, order, path, count, length, digest, duplicate,
and empty-set rule before import or process.

## 2. BRM-V02-IR-002 response

v0.3 assigns both `CreateProcessW` and `NtCreateFile` to the native preloader.
It assigns the exact eleven RPNP v0.4 observation-call imports and the PyInit
export to the guard. The guard does not import `NtCreateFile`; the complete
role import sets still equal their authenticated allowlist manifests. Six
hostile rows cover role, order, omission, owner-DLL, export, and allowlist
mutations.

Requested review evidence: reconstruct both role lists from RPNP v0.4 and
reject every swapped, omitted, extra, reordered, or wrongly owned import.

## 3. BRM-V02-IR-003 response

v0.3 carries an ordered DLL-search-directory inventory and exact resolution
bindings. The application directory is index zero. Remaining entries are the
sorted unique DLL-map parent directories. Every DLL binding carries exact
path, parent, index, and SHA-256; host, PATH, registry, current-directory, and
environment fill are forbidden. Eight hostile rows cover the closure.

Requested review evidence: independently derive the inventory and bindings
from one fake PUBLIC runtime map and reject all alternate directories,
orders, derivations, duplicate names, paths, indices, and hashes.

## 4. BRM-V02-IR-004 response

v0.3 adds separate closed Draft 2020-12 schemas for prepublication and final
record packages. They fix the body fields and order, forbid cross-boundary
and unknown fields, define a canonical package codec, and require canonical,
closed-file, and retained-parent readback body hashes to match.

The machine phase order now includes
`DESTINATION-ABSENT-RECHECK-PASSED` after prepublication readback and
immediately before rename. The recheck binds the same retained parent and
intended name. Twelve hostile rows cover record structure, hash/readback,
recheck, race, and final-rehash failures.

Requested review evidence: validate both record schemas, permute every phase,
inject every forbidden field and destination race, and prove no rename or
authority follows a failed recheck.

## 5. Nonregression and author-side disposition

The authenticated v0.2 effective matrix remains intact and gains only 34
targeted rows, for 97 total. All nonreplaced v0.2 relations and twelve
resource limits remain effective. v0.3 is a mandatory successor wrapper;
direct v0.2 execution is forbidden.

The v0.3 authority extension separately binds the v0.3 package, approving
review, and both record-schema byte hashes while retaining the exact v0.2
package and review pins.

This response is not independent evidence. No source, compiler, build,
binary, runtime tree, native API, platform probe, F0 content, provider/model,
S0, or E0 task was created or observed.
