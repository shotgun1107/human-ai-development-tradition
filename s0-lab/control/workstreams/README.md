# Workstream structural index

This directory is the canonical stage-oriented navigation layer for current
technical work. It does not replace or relocate authenticated project
artifacts.

## Why this layer exists

Historical artifacts are stored by role and local version:

- design and CONTROL decisions under `s0-lab/control/`;
- implementations and TEST evidence under `s0-lab/assembly-rehearsal/`; and
- independent reviews under exact public paths in `s0-lab/reviews/`.

Those paths are bound by manifests, sidecars, reports, source constants, and
Git history. Moving them for cosmetic organization would invalidate current
authentication. Workstream maps therefore provide a non-destructive ordered
view over those immutable paths.

## Required map structure

Every active technical workstream map must contain:

1. an exact evidence-baseline `main` commit and tree plus the containing Git
   commit as publication identity;
2. the requested project outcome;
3. ordered stages with work-package-local versions;
4. exact current evidence paths for every stage;
5. explicit dependency edges;
6. completed, missing, blocked, pending, and closed states;
7. one structurally eligible work package, while withholding a literal gate
   phrase until the current value-first assessment is complete; and
8. update triggers and authority precedence.

Version numbers must never be compared across work packages. A controller
`v0.1` may be later in the dependency chain than a design `v0.5`, while a
runtime `v0.7` may be complete before a preloader `v0.4` implementation.

The protocol semantic version, question-contract version, design version,
implementation version, review revision, runtime-materialization version, and
environment version are separate namespaces. Candidate-time status fields
such as `commit_or_push_authorized: false` remain true historical statements
inside their artifacts even after a later Git integration; current presence
is determined from Git and this routing layer, not by rewriting the artifact.

## Current maps

- [Public end-to-end assembly rehearsal](./public-end-to-end-assembly-rehearsal.md)

## Change rule

Existing authenticated artifact directories remain in place. A physical move,
rename, deduplication, or deletion requires a separately authorized migration
with complete manifest, sidecar, source-reference, documentation-link, and
consumer compatibility analysis. Ordinary cleanup must use this index layer
instead.
