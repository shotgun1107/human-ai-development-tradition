# a04 CONTROL disposition

Date: 2026-09-16. Candidate: `a04-i0-cli-authentication-v0.1`.

CONTROL `/root` supplied the decision **ACCEPT-BOUNDED-CLI-MANIFEST-GUARD** for the exact frozen artifacts below. This record is authored by DOCUMENTATION `/root/audit_a04_cli_docs_replacement` from that handoff; it is not DOCUMENTATION's independent approval.

| Frozen target | SHA-256 |
| --- | --- |
| `artifact-files.sha256` | `3188bfb5d5745b83a0f07f8134e2021d63285c8591db1698eca02e6086fc3f68` |
| `README.md` | `6ca9be7101e7268c81288d64c7e308a5297af4f2076ca948e2cecf67a005e631` |
| `implementation/s0_i0/cli.py` | `819edaf785558b620aa7b79036560d4fb895d7ce513a5cc4173fad04df8e43f9` |

Branch: `codex/windows-build-toolchain-environment-v0.1`; HEAD: `cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a`; tree: `82c02f37fd13ecfc8c7b888bb66127989b6d4f34`.

The fresh read-only INDEPENDENT REVIEW role `/root/audit_a04_cli_review` returned primary **PASS** for the frozen bounded F-07 claim, with no actionable P0-P3 findings, as supplied by CONTROL. CONTROL adopted that verdict and made the decision above.

CONTROL reports that review authenticated all 35 allowed input/artifact pins, the seventeen unique manifest entries and README sidecar, original twelve source files and manifest, public two inputs, validator, and Git identity. The reviewer did not rerun substantive tests or canonical text validation.

The accepted correction changes only the CLI import and guarded call: the existing fixed manifest digest is checked before parsing and before exactly `integrity`, `schema-check`, and `verify` handlers, inside the existing JSON exception boundary. This decision covers that bounded guard claim only.

The reviewed evidence reports 29 tests, 26 observations, zero failures/errors/skips, unchanged pre/post identity and 28 input pins, and scratch cleanup. Baseline guard absence and authentic-manifest dispatch are distinguished. Altered/matching-replacement, malformed, missing, and injected-unreadable manifests reject before handler dispatch.

Content-only mutation passes the manifest guard as designed and is rejected by a narrow digest handler double. Other command entry paths remain unchanged. Import-only `jsonschema` and handler doubles, permission injection, and static full-content wiring are explicitly bounded evidence.

No complete ninety-file execution, real dependency/full CLI integration, answer/schema/transform validation, ACL/import security, authority rebinding, concurrency, TOCTOU, Windows path-lifecycle defense, or secure evidence producer is claimed. Existing README nonclaims remain in force. No native-environment or S0/E0 validation follows from this decision.

The prior DOCUMENTATION role's pre-hash reads of three authorized TEST files remain the attributed procedural lapse in the frozen README. CONTROL reported no denied/F0 read or writes by that role; replacement and later matching hashes do not retroactively validate its procedure.

This disposition and its sidecar are outside the frozen seventeen-entry manifest. That manifest and all seventeen artifact bytes remain unchanged. The README's PENDING status describes its earlier packet freeze; this separate record supplies the later disposition without rewriting that history.

Before writing, DOCUMENTATION reauthenticated all 35 existing input/artifact hashes and Git identity without substantive test reruns. Only these two disposition files are added; canonical validation and final hashes are reported separately to CONTROL.

The opaque unclassified Git-status blocker remains, according to CONTROL. This acceptance grants no staging, commit, push, merge, F0-content access, experimental execution, installation, or broader gate permission. No Git mutation occurred in this documentation step.
