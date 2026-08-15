# S0 v0.14 public assembly build and runtime materialization acceptance plan v0.5

## 1. Purpose and limit

This plan tests only the two v0.5 design corrections. It uses authenticated
PUBLIC design bytes and clearly fake in-memory packages. It does not compile,
build, materialize, load, or execute a runtime and does not call a native API,
provider, model, executor, judge, S0, or E0 task.

Schema success is diagnostic only. A PASS under this plan means only that the
PUBLIC design is eligible for CONTROL integration consideration.

## 2. Input authentication

Before substantive review:

1. authenticate the exact Git commit, tree, sole parent, candidate ref, and
   initially clean worktree;
2. run the canonical text-artifact validator SelfTest;
3. authenticate the v0.1 through v0.5 build/runtime package manifests before
   reading only their literal targets and sidecars;
4. authenticate the v0.4 independent review pair;
5. validate every admitted Markdown pair and JSON pair independently;
6. reject duplicate JSON keys; and
7. validate the v0.1 through v0.5 schemas against Draft 2020-12 and resolve
   every absolute `$ref` only through the authenticated schema registry.

Any mismatch invalidates the review before semantic work.

## 3. Relation-patch reconstruction

Use two independent in-memory serializers. Starting with the authenticated
v0.4 relation array, require 68 entries and the underscore spelling at
zero-based index 15. Replace only that entry with the exact hyphenated v0.3
value. Prove every other index and byte string is unchanged and the result is
unique.

Serialize the exact `S0-BRM-SEMANTIC-RELATIONS-5` ASCII/LF preimage. Both
serializers must produce 6,805 bytes and SHA-256:

`5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`

Required hostile cases include:

- old value absent, duplicated, or at another index;
- no replacement, underscore retained as active, or a second replacement;
- insertion, deletion, reorder, count drift, duplicate relation, case drift,
  or punctuation drift at any index;
- zero-padded, skipped, repeated, or reordered index lines;
- missing header/count/final LF, extra line, CR, BOM, non-ASCII, blank line, or
  trailing whitespace; and
- hashing raw JSON, a sorted relation set, or any preimage other than the exact
  published grammar.

Every case must stop as `BR-AUTH/0` before semantic-validator import or process
creation, with output-created false.

## 4. Policy-authority reconstruction

Resolve the sole normative object path
`base_profile.publication_no_replace_policy` in a fake schema-valid v0.5
package. Require exactly the 20 authenticated fields and values. Use two
independent RFC 8785-compatible JCS serializers, append one LF, and require
896 bytes and SHA-256:

`3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`

Require the embedded v0.4 digest, outer v0.5 digest, prepublication record
digest, and final record digest to equal that value.

Required hostile cases include:

- hashing the 17-field v0.4 interface-map summary;
- treating the historical summary as a second normative policy;
- missing, additional, renamed, or changed policy fields;
- changed array order or content in `source_handle_required_access`;
- false flag-set Booleans, different flags, API, class, access, handle source,
  terminal failure, or retry value;
- hashing without the final LF, hashing the enclosing package, using ordinary
  pretty JSON, or using a non-JCS key order;
- accepting any lowercase 64-hex value without recomputation; and
- binding a different digest in either record package.

Every case must stop as `BR-AUTH/0` before policy hashing completes, record
freeze, candidate import, or process creation, with output-created false.

## 5. Schema and package closure

Build a clearly fake PUBLIC nested package that validates through the exact
v0.1, v0.2, v0.3, v0.4, and v0.5 schemas. It must contain the authenticated
v0.4 base profile with the recomputed policy digest and the exact v0.5 overlay.

At every v0.5 object depth:

- delete each required property one at a time;
- inject one unknown property;
- mutate each const Boolean, count, identifier, relation value, path, and
  digest; and
- test uppercase, short, long, and all-zero meaningful hashes.

Every mutation must reject. No callback, default, base-profile fallback, or
schema-only success may stand in for the required semantic recomputation.

## 6. Matrix and nonregression

Independently reconstruct the exact effective matrix:

- authenticated v0.4 effective rows: 111;
- published v0.5 additional rows: 4;
- effective total: 115.

Require unique IDs, exact order, one nonempty primary failure, and one Boolean
output bit per row. The `/0` or `/1` primary suffix must agree with the bit.

Confirm that v0.5 changes only:

1. semantic relation zero-based index 15; and
2. publication policy hash authority.

All other v0.4 relation bytes, Windows directory rules, no-replace transaction,
record schemas and phase order, resource values, authority pins, runtime and
binary rules, failure precedence, and claim limits remain effective.

## 7. Acceptance rule

The design is eligible for a PASS-only CONTROL integration gate only if:

- both prior findings close without ambiguity;
- there are zero BLOCKING and zero MAJOR findings;
- every authentication, schema, reconstruction, hostile, matrix, and
  nonregression check passes; and
- the reviewer states the closed evidence boundary without claiming a build,
  runtime, rehearsal, or S0 result.

Any finding yields `REVISE-AND-REVIEW`. An integrity, input, independence, or
F0 boundary failure yields `INVALID-REVIEW`.
