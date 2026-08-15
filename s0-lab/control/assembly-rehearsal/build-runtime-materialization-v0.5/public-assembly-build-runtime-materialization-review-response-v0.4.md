# S0 v0.14 build/runtime materialization v0.4 review response

## 1. Review disposition

The authenticated v0.4 independent review returned `REVISE-AND-REVIEW` with
zero BLOCKING, two MAJOR, and zero MINOR findings. v0.5 accepts both findings.
It does not reinterpret either as formatting-only and does not expand the
design into implementation.

## 2. `BRM-V04-IR-001`

### Finding

v0.4 changed one supposedly retained semantic relation from the authenticated
v0.3 hyphenated byte string to an underscore spelling without declaring a
replacement.

### Correction

v0.5 authenticates the 68-entry v0.4 array, requires the underscore spelling
at zero-based index 15, and replaces only that entry with:

`application-directory-equals-parent-of-verifier-application-runtime-row`

All other indices and bytes remain identical. The effective array is bound by
the exact 6,805-byte `S0-BRM-SEMANTIC-RELATIONS-5` ASCII/LF preimage and
SHA-256:

`5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db`

Two new mutation rows reject a missing or altered patch and any other array or
preimage drift before candidate import or process creation.

### Claim

This is a proposed exact closure. It is not independent evidence until a fresh
review reconstructs the patch and digest.

## 3. `BRM-V04-IR-002`

### Finding

The v0.4 interface map and profile schema published different same-named
policy objects. Their 17-field and 20-field JCS preimages had different hashes.

### Correction

v0.5 defines one normative hash-preimage path only:

`base_profile.publication_no_replace_policy`

The v0.5 interface map contains a binding record, not another policy object.
It explicitly marks the historical v0.4 interface-map summary as
nonauthoritative for hashing. The embedded v0.4 profile must carry the exact
20-field object and its digest is constrained to the independently reproduced
896-byte RFC 8785 JCS UTF-8 plus final-LF hash:

`3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b`

The outer package and both record packages must bind the same digest. Two new
mutation rows reject alternate source objects, field-set drift, wrong
serialization, wrong digest, or record divergence before record freeze,
candidate import, or process creation.

### Claim

This is a proposed single-authority closure. It does not claim that the
publication API was called or that platform behavior was observed.

## 4. Nonregression

The v0.4 Windows directory and no-replace transaction corrections remain
unchanged. v0.5 retains the v0.4 record schemas, 12 resource values, authority
pins, runtime/binary rules, failure precedence, and claim boundaries. The
effective matrix is 111 authenticated v0.4 rows followed by four v0.5 rows,
for 115.

No source, build, binary, runtime tree, native call, platform probe,
provider/model task, executor, judge, S0, or E0 operation was performed. F0
content was not accessed.
