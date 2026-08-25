# S0 v0.14 Windows Authenticode verifier v0.1 independent code and security review

## 1. Review result

Verdict: `REVISE-AND-REREVIEW`.

The authenticated PUBLIC v0.1 implementation candidate does not pass the
independent code and security review. Its bounded synthetic verification
passes, and static x64 ctypes layout checks found no discrepancy, but six
security-authority and native-lifecycle gaps remain blocking.

| Severity | Count | Finding IDs |
|---|---:|---|
| HIGH / BLOCKING | 5 | `BRM-AUTHV01-IR-001` through `BRM-AUTHV01-IR-005` |
| MEDIUM / BLOCKING | 1 | `BRM-AUTHV01-IR-006` |

This result does not authorize a live artifact, native trust operation,
download, installer, build, runtime materialization, rehearsal, F0 role, S0,
or E0 gate. Revision and another fresh independent review are required.

## 2. Role, identity, and boundary

Facts:

- review gate:
  `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION WINDOWS AUTHENTICODE VERIFIER IMPLEMENTATION V0.1 INDEPENDENT CODE AND SECURITY REVIEW OPEN`;
- role: fresh independent PUBLIC code and security reviewer;
- reviewer runtime: `gpt-5.6-sol`, reasoning level `ultra`;
- reviewed handoff commit:
  `0f9b1b2c06bb2257db63c218f20e29237be1f81e`;
- reviewed handoff tree:
  `61a387eb49d902b8c6388f25a8dfa62119b30636`;
- reviewed implementation commit and handoff sole parent:
  `9b32090c06ab8f8c38f9540f07c04ee3b785a364`;
- implementation tree:
  `90ec2aa376cf9532d54a240619442b3a9ee823b9`;
- implementation sole parent:
  `2709a46faf5502e96c24bc7731e201398042b6b6`;
- implementation-manifest SHA-256:
  `11e2f27fc4993f8b60bca17852f2112fb1d20c901b7044572deb325147cafc6f`;
- verification-manifest SHA-256:
  `5f70306946c4ac70f314abe373f7b415e785a845fcca1e77f34a8e8748e81ebc`;
- review date: `2026-08-25`; and
- F0 content access: none.

The reviewer inherited no author conversation, called no other agent, used
only the frozen PUBLIC manifest closure and named handoff records, and made no
repository change. The three F0 families were used only as aggregate
inventory and quiet-state evidence.

## 3. Input authentication and bounded verification

Facts and test results:

- pinned commit, tree, sole-parent, and ancestry checks: PASS;
- worktree and index: clean before and after review;
- F0 aggregate inventory: `32 / 11 / 10`;
- every F0 worktree/index quiet query and untracked, ignored, skip-worktree,
  and assume-unchanged anomaly count: zero;
- both top manifests matched their supplied SHA-256 pins;
- outer manifest rows: `12 / 4`, all target hashes matched;
- subordinate manifests: four, with `1 / 1 / 3 / 3` rows, all target hashes
  matched;
- canonical validator SelfTest: PASS;
- README, implementation report, and both handoff Markdown/sidecar pairs:
  PASS;
- focused PUBLIC synthetic tests, run from the authenticated snapshot with
  bytecode writes disabled: `13 / 13 PASS` in `0.052s`;
- static x64 ctypes sizes and offsets: no discrepancy found, including
  `WINTRUST_DATA=88`, `CRYPT_PROVIDER_SGNR=64`, `CERT_CHAIN_PARA=96`, and
  `CERT_CHAIN_CONTEXT=72`; and
- final manifest hashes and repository clean state remained exact.

The candidate's `verify_candidate.py` was not invoked by the reviewer because
its predecessor inputs extended beyond the review's frozen allowlist. The
allowlisted 13-test suite was run directly. No x86 runtime was available.

No native trust API, certificate store, network, download, installer,
candidate process, build, live executable, F0 role, S0, or E0 invocation
occurred.

## 4. Blocking findings

### BRM-AUTHV01-IR-001 — HIGH — acquisition and URL provenance are not bound to the retained file

Evidence:

- `verifier.py:13` accepts `requested_uri`, `final_uri`, `redirect_count`,
  path, and handle as independent caller inputs.
- `win32.py:659` checks only that the requested URI string equals the fixed
  constant, and `win32.py:782` copies the caller claims into the observation.
- `semantic.py:320` tests literal URI equality and zero redirects, not
  acquisition evidence.
- `win32.py:785` emits `original_file_handle_retained` as a literal.

Failure path: a caller can open unrelated PE bytes that satisfy the remaining
signature, timestamp, chain, and Microsoft-root checks, then supply the fixed
Build Tools URL twice with `redirect_count=0`. The fixed-URL supplier
component passes without evidence that the retained bytes came from that
transfer.

Affected claim: the exact Microsoft-operated URL, retained original download
handle, and project supplier composite.

Required correction: authenticate an acquisition record that binds the
request URI, final URI, redirects, transfer completion, file identity, byte
length, SHA-256, and exact retained handle or file object. Alternatively,
place acquisition inside the authenticated immutable verifier boundary.

### BRM-AUTHV01-IR-002 — HIGH — provider and chain resources are not closed on every failure path

Evidence:

- `win32.py:694` calls `WinVerifyTrust` with `WTD_STATEACTION_VERIFY`.
- A null returned state raises at `win32.py:695`, before the cleanup
  `try/finally` beginning at line 705. CLOSE occurs only at lines 760-762.
- `_build_chain` obtains a chain context at `win32.py:577` and calls
  `_chain_rows` at line 591 without a local cleanup guard. A parsing failure
  can occur before the outer owner receives the pointer freed at lines
  755-759.

Official Windows contracts require `WTD_STATEACTION_CLOSE` for every VERIFY
use and require every returned chain context to be released:
[WINTRUST_DATA](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_data),
[CertGetCertificateChain](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certgetcertificatechain).

Failure path: a malformed/provider-error input returns no state, or an
allocated chain fails structural parsing. Repeated verification can leak
native resources and violates the claimed deterministic lifecycle.

Required correction: establish cleanup immediately around every VERIFY call
and always issue CLOSE. `_build_chain` must own and free its context until a
successful, explicit ownership transfer.

### BRM-AUTHV01-IR-003 — HIGH — the retained handle does not establish immutable bytes

Evidence:

- `win32.py:657` checks only that the supplied handle is a positive integer.
  It does not establish read-only rights, deny-write/delete sharing, or
  process-owned acquisition.
- File hash and identity A are sampled at lines 677-678, WinTrust reads later
  at lines 684-694, and hashes are sampled again at lines 751-765.
- `semantic.py:331` checks equality of these discrete samples.
- `_hash_handle` uses `DuplicateHandle` at `win32.py:425`. Duplicated file
  handles share the same current file position under the documented Windows
  contract.

Official references:
[DuplicateHandle](https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle),
[CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew).

Inferred exploit path: retain the same file object and identity, present bytes
A for the hashes, temporarily expose signed bytes B while WinTrust reads, and
restore A before the later samples. Concurrent handle use can also disturb the
shared file position.

Required correction: require a process-owned read-only acquisition handle
whose sharing contract denies write/delete access, reject writable mappings
or handles, use synchronized or position-independent hashing, and prove that
WinTrust and all hashes cover one immutable byte state.

### BRM-AUTHV01-IR-004 — HIGH — trust snapshots are incomplete and enumeration errors can appear normal

Evidence:

- `_store_snapshot` enumerates only `ROOT`, `CA`, and `Disallowed` at
  `win32.py:452`.
- Null enumeration results are always treated as end-of-store at lines
  468-476, and `CertCloseStore` failure is ignored at line 484.
- `win32.py:847` nevertheless claims scope
  `EFFECTIVE-WINDOWS-DISALLOWED-CTL`.
- `semantic.py:426` accepts stable effective trust authority by comparing
  these snapshot hashes.

Windows documents that null enumeration can also mean failure and must be
distinguished with `GetLastError`. The chain engine's effective inputs can
include Root, CA, My, and Trust stores:
[CertEnumCertificatesInStore](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certenumcertificatesinstore),
[CertEnumCTLsInStore](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certenumctlsinstore),
[CERT_CHAIN_ENGINE_CONFIG](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_chain_engine_config).

Failure path: an enumeration error can produce the same truncated prefix
before and after, or a chain-affecting store or automatic-CTL input can remain
outside both snapshots.

Required correction: use an authenticated deliberately constructed chain
engine namespace, or snapshot every effective input and cache/policy source.
Only documented end-of-enumeration statuses may be accepted, and store close
must succeed.

### BRM-AUTHV01-IR-005 — HIGH — disk manifests do not bind the code objects already executing

Evidence:

- `__init__.py:3` imports the authority, native, semantic, and orchestrator
  modules before runtime authentication.
- `verifier.py:25` authenticates the installed implementation only after
  those imports.
- `authority.py:53` hashes current filesystem bytes, not imported bytecode or
  in-memory function objects.
- `test_authenticode_verifier.py:228` derives its authority pin from the same
  local manifest.

Failure path: import altered code and restore the authenticated disk bytes, or
replace mutable global functions in the host process. Disk authentication can
pass while different code produces the decision.

Affected claim: independent implementation authority and complete closure of
`BRM-AUTH02-IR-001`.

Required correction: use a minimal independently trusted launcher that
authenticates before import, load only from a fresh immutable authenticated
snapshot, exclude uncontrolled bytecode/import paths, isolate execution, and
bind launcher and interpreter authority. Otherwise narrow the claim to a
trusted-host consistency check.

### BRM-AUTHV01-IR-006 — MEDIUM / BLOCKING — revocation reference time is asserted, not observed

Evidence:

- `win32.py:676` captures `reference_time` before store enumeration and
  WinTrust.
- Chain construction occurs later at lines 726 and 741.
- `_chain_rows` assigns the earlier value to
  `freshness_reference_filetime` at `win32.py:533`; Windows does not return
  that value as the time it used.
- `semantic.py:415` only compares the assigned label.

Microsoft defines `dwFreshnessTime` relative to current time, while
`CERT_CHAIN_PARA` provides no explicit current-time input:
[CERT_REVOCATION_INFO](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_revocation_info),
[CERT_CHAIN_PARA](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_chain_para).

Failure path: network delay or a clock change between the captured time and
chain calls makes the claimed exact reference instant differ from the one
Windows used.

Required correction: record a conservative before/after interval around each
chain call and reject clock discontinuity, or use a documented API path with
an explicit current-time input. Do not claim an exact instant that Windows did
not return.

## 5. Predecessor finding dispositions

| Predecessor finding | Result | Reason |
|---|---|---|
| `BRM-AUTH02-IR-001` | **PARTIALLY CLOSED** | Disk manifests, authority-copy equality, canonical observation hashing, computed relation rows, and trace-to-decision binding exist, but `BRM-AUTHV01-IR-005` leaves executed-code authority unbound. |
| `BRM-AUTH02-IR-002` | **PARTIALLY CLOSED** | Event ordering, fixed indexes, `pTime`, policy IDs, chain inputs, and freshness rejection exist, but `BRM-AUTHV01-IR-002/003/004/006` leave lifecycle, immutable bytes, effective trust, and exact reference-time claims open. |
| `BRM-AUTH02-IR-003` | **PARTIALLY CLOSED** | The unsupported official leaf guarantee was removed and Microsoft-root policy is correctly limited, but `BRM-AUTHV01-IR-001` leaves the fixed-URL supplier component unevidenced. |

The negative source claim `official_leaf_guarantee_claimed=false` is correct.
Microsoft documents `CERT_CHAIN_POLICY_MICROSOFT_ROOT` as a Microsoft-root
public-key check on the last element of the first simple chain, not a complete
leaf-publisher policy:
[CertVerifyCertificateChainPolicy](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certverifycertificatechainpolicy).

## 6. Additional limitations

- The static x64 ABI result is not live ABI proof, and x86 behavior remains
  unexecuted.
- Application-level upper bounds are absent for provider `csCertChain`,
  rebuilt `cElement`, store enumeration, observation size, and file hashing.
  The revision must address these bounds.
- Synthetic tests establish bounded internal behavior only. They do not
  establish acquisition provenance, immutable-byte authority, native resource
  closure, complete effective trust state, or executed-code authority.

## 7. Scope and next decision

This review establishes only that the authenticated PUBLIC v0.1 source and
its bounded synthetic checks were independently inspected. It establishes no
real signature, acquisition, certificate, timestamp, revocation response,
Windows trust state, build, runtime materialization, operational safety,
process authority, rehearsal, F0 result, S0, or E0 result.

The next live-artifact gate must not open. A bounded v0.2 revision must correct
all six findings, update the affected authority and test closures, and then
undergo a fresh independent code and security rereview.

`REVISE-AND-REREVIEW`
