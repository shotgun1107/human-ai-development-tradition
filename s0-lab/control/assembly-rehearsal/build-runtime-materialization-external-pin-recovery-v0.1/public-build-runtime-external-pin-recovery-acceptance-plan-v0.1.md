# S0 v0.14 public build/runtime external-pin recovery acceptance plan v0.1

## 1. Scope

This plan judges only the recovery selection and a later download-only
acquisition snapshot. It does not authorize source authoring, compiler
execution, installation, build, binary inspection, runtime materialization,
native calls, platform probes, rehearsal, S0, or E0.

## 2. Selection-package checks

Reject unless all of the following hold:

1. the exact base main commit and tree match;
2. all six predecessor Git/artifact authorities match their recorded hashes;
3. the recovery class order exactly matches the frozen ten-class design order;
4. every unavailable class remains explicitly unavailable;
5. no local path, user identifier, credential, secret, F0 content, moving
   branch, ambient installation, or PASS object is used as a pin;
6. all claim bits remain false; and
7. the package does not claim any manifest identity for bytes not acquired and
   fully enumerated.

## 3. Toolchain acquisition checks

The later acquisition must use a fixed-version Build Tools bootstrapper. An
evergreen URL, silent version substitution, installer-selected extra workload,
locale drift, or post-download update rejects.

The isolated offline layout must contain only the selected workload,
components, their exact installer-required dependencies, and one language.
Before installation or compiler use, record:

- bootstrapper byte length and SHA-256;
- product and fixed release version;
- channel-manifest identities;
- every layout target path, byte length, and SHA-256;
- target count, aggregate target bytes, and target-set SHA-256; and
- total layout size against the inherited 24 GiB ceiling.

Any symlink, junction, reparse point, alternate stream, path alias, duplicate
logical path, installer cache, telemetry output, mutable download, or
unclassified target rejects.

## 4. CPython acquisition checks

The downloaded CPython zip must equal SHA-256
`4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3`.
The official SPDX and Sigstore materials must be retained as separately hashed
evidence.

Extraction occurs only into a fresh empty out-of-repository root. Reject path
traversal, duplicate archive names, case-fold collisions, links, alternate
streams, extra files, modified bytes, or ambient Python substitution. Produce
the four-field manifest identity only after the exact extracted target set is
closed.

No extracted interpreter is launched in the acquisition gate.

## 5. Python dependency acquisition checks

The root wheel must equal SHA-256
`d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce`
and size 90,630 bytes.

Resolve all mandatory, format-extra, and transitive distributions for CPython
3.12 Windows AMD64. Every artifact needs an exact name, version, URL, size,
SHA-256, wheel tag, and dependency edge. Reject source builds, ambient cache,
unhashed packages, incompatible tags, yanked files, moving indexes, duplicate
projects, dependency cycles not represented in the graph, or installation.

The resolution result remains a candidate until an independent reviewer
reconstructs the graph from authenticated metadata.

## 6. Missing-source and platform stops

Acquisition must stop with a named missing status for:

- native source;
- materializer and inspector source;
- authenticated Windows platform manifest; and
- runtime-tree profile.

No source may be generated, copied from conversation memory, reverse
engineered, or inferred from toolchain availability in this gate.

## 7. Publication and review boundary

Downloaded toolchain, CPython, dependency, platform, and runtime bytes are
external acquisition material. They must not be committed unless a later
publication-eligibility decision explicitly classifies each byte.

Only PUBLIC selection records, canonical manifests, hashes, and review records
may become candidate Git changes. Before any commit or push, require exact
scope review, canonical text validation, F0 aggregate 32 / 11 / 10, quiet F0
parent comparison, zero unclassified status, and explicit Git approval.

A fresh independent security reviewer must examine the exact acquisition
records before any source-authoring, installation, compiler, build, or
materialization gate can be considered.
