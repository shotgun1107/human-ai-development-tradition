# A01 public boundary helpers v0.1

This auxiliary audit-remediation candidate contains two bounded helper corrections: F-02 parses the flags in an `os.open` audit event whose mode is `None`; F-04 rejects stream-enumeration errors and a failed stream-handle close. It does not assemble or validate the complete system. The active project baseline remains `central-system-v2.1-s0-preparation`.

Read [REMEDIATION-REPORT.md](REMEDIATION-REPORT.md) for ownership, the CONTROL-supplied pre-CODE requirements, original and candidate pins, the exact review packet, reproduction, and limitations. [artifact-files.sha256](artifact-files.sha256) covers the 17 candidate implementation, test, evidence, and documentation files; it excludes itself. A path appearing in source or evidence does not expand any role's input allowlist.

The authenticated TEST/VERIFICATION evidence records 23 tests and 88 subtests, with zero failures, errors, or skips: 13 isolated child cases and 36 stream API-double scenarios. These counts overlap and must not be added into a single test total. Independent review is **PENDING**; the documentation role makes no acceptance decision.

The original seven pinned implementation inputs remain unchanged. This version is a separate candidate, not a replacement of historical frozen bytes or proof of native publication, an OS sandbox, integration, operational safety, economic value, model transfer, or S0/E0 execution. Git publication remains unauthorized and blocked by the CONTROL-reported opaque unclassified status item.
