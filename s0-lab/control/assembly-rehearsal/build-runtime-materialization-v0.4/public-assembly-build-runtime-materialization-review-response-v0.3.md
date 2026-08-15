# S0 v0.14 public assembly build and runtime materialization review response v0.3

## 1. Source review

This response addresses the authenticated v0.3 independent review with
SHA-256
`e84775d2cb07ea5353192bd3c3cbe80dec487af5bafa4ea36a91ade8b74914cc`.

That review returned `REVISE-AND-REVIEW` with zero BLOCKING, two MAJOR, and
zero MINOR findings. This response is an author claim only. A fresh reviewer
must independently verify every disposition.

## 2. `BRM-V03-IR-001` disposition

### Prior defect

v0.3 removed only byte-identical directory parents. Case or separator aliases
could therefore receive different indices while identifying the same Windows
directory.

### v0.4 correction

v0.4 now defines:

- one strict forward-slash ASCII path grammar with empty, trailing, doubled,
  dot, dotdot, trailing-dot, backslash, colon, control, non-ASCII, and DOS
  device segments rejected;
- one locale-free ASCII lowercase identity key;
- duplicate-key rejection before hashing or index assignment;
- one exact identity-key preimage and final LF;
- identity-key rather than raw-path sort order;
- pairwise-distinct `FILE_ID_INFO` physical identities;
- reparse-point rejection; and
- DLL bindings that include path, parent identity key, index, and target hash.

Mutation rows `BRM-V04-DLLALIAS-001` through `008` cover the prior
counterexample and adjacent alias paths.

Author disposition: `PROPOSED-CLOSED`. It is not independently closed until a
fresh review reconstructs both the byte identity and physical identity rules.

## 3. `BRM-V03-IR-002` disposition

### Prior defect

v0.3 separated destination absence observation from an ambiguous atomic
rename. A replacement-capable rename could overwrite a destination created
during the race and still produce pass-looking final evidence.

### v0.4 correction

v0.4 binds the exact publication call to:

- `kernel32.dll!SetFileInformationByHandle`;
- `FileRenameInfoEx` numeric class `22`;
- `FILE_RENAME_INFO.Flags=0`;
- replace-if-exists and POSIX-semantics flags unset;
- the retained runtime-A source handle;
- the same retained destination-parent handle and final name as the recheck;
- exact UTF-16LE name-byte length; and
- same-volume operation.

The policy hash has one JCS/UTF-8/final-LF construction. Source and parent
handle identity hashes have fixed ASCII/LF preimages, and both records carry
the exact filename byte length.

The absence observation is explicitly diagnostic. The successful no-replace
call is the only linearization point. Destination creation after the recheck
must make the call fail without overwrite. Any call failure freezes
`BR-MATERIALIZE/1`, grants no authority, and permits no retry or fallback.

New closed prepublication and final record schemas bind the primitive, class,
flags, handles, name, policy hash, result, linearization point, and subsequent
rehash evidence. Mutation rows `BRM-V04-NOREPLACE-001` through `006` cover
primitive drift, replacement flags, identity drift, the race, false success,
and retry.

Author disposition: `PROPOSED-CLOSED`. It is not independently closed until a
fresh reviewer proves the exact no-replace semantics and record boundaries.

## 4. Nonregression claim

The v0.4 profile embeds the exact v0.3 profile and forbids direct v0.3
execution. The effective matrix is 97 retained rows plus 14 v0.4 rows. The
exact twelve resource values are unchanged. Existing target-set, import-role,
runtime-map, record-hash, owner-selection, quarantine, and claim boundaries
remain effective unless v0.4 explicitly replaces them.

No source, compiler, build, binary, runtime tree, native call, platform probe,
provider/model task, rehearsal, S0, or E0 result was created or observed by
this revision.
