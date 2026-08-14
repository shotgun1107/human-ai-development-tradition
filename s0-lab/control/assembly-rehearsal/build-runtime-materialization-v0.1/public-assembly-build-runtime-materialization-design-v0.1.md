# S0 v0.14 public assembly build and runtime materialization design v0.1

- `status`: public design candidate; fresh independent review required
- `gate`: `S0 V0.14 PUBLIC END-TO-END ASSEMBLY REHEARSAL BUILD AND RUNTIME MATERIALIZATION DESIGN OPEN`
- `baseline_commit`: `64077a5862aa5678a83ba2f9f48fc71493ed2808`
- `baseline_tree`: `db271b4f08cabcdb038d17ce0d1705d2897b5115`
- `implementation_status`: not implemented
- `build_status`: not executed
- `runtime_materialization_status`: not executed
- `native_execution_status`: not executed
- `F0_content_access`: none

## 1. Purpose and exact boundary

The current public lineage proves a bounded offline adapter and its exact
public byte closures. It does not prove which compiler, linker, Windows SDK,
CPython distribution, dependency files, native source, build recipe, binary,
or runtime tree will be used by a future live candidate.

This design defines the missing public source-to-runtime chain. It separates:

1. authenticated source and authority inputs;
2. an externally pinned offline toolchain closure;
3. two clean deterministic native builds;
4. static PE, import, and package inspection;
5. exact runtime-tree materialization; and
6. a later independently authenticated launch input.

This gate writes design artifacts only. It does not add native source, compile
anything, install a toolchain, invoke a process, create a runtime tree, load a
DLL, call a Windows API, or run a platform probe or rehearsal.

## 2. Authenticated predecessor basis

The future implementation must authenticate the original bytes, not a prior
validation object, for every row below before any build or materialization
process starts.

| Public authority | Exact SHA-256 | Rows or meaning |
|---|---|---|
| assembly implementation manifest v0.1 | `0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623` | 32 exact targets |
| RPNP implementation manifest v0.3 | `5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2` | 11 exact targets; offline-only implementation |
| RPNP design manifest v0.4 | `abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589` | 6 exact targets |
| assembly/RPNP integration design manifest v0.1 | `f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b` | 5 exact targets |
| assembly/RPNP integration design manifest v0.2 | `1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c` | 6 exact targets |
| bounded integration implementation manifest v0.1 | `7469f62d67c9d5f416f38db7e4a14b5f3819e739cf38a71f1fec452421a7fabe` | 3 exact targets |
| bounded integration verification manifest | `8f8140d678e5846639ff382b32035c342dc8b2dd7d929da5ff37a759f8aa9d7b` | 4 exact targets |
| assembly design manifest v0.5 | `6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802` | 5 exact targets |
| I0 implementation manifest | `f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae` | 15 exact targets; later runtime uses only the frozen child closure |
| I1 implementation manifest | `668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c` | 26 exact targets; later runtime uses only the frozen child closure |
| I2 implementation manifest | `18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6` | 16 exact targets; later runtime preserves the no-import disposition |
| I3 implementation manifest | `e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648` | 17 exact targets; later runtime preserves the no-import disposition |
| public practice bundle manifest | `e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637` | 90 exact public targets |
| bounded integration CONTROL decision | `acdbc42e75197ca22a078c4e8c8353f834be17dd6332f0c9ca361d70c6722d1a` | integrated bounded offline candidate only |

The effective public design remains assembly v0.3 plus v0.4 and v0.5
replacements, composed with RPNP v0.1 through v0.4 and integration v0.1 plus
v0.2. Selective predecessor use is forbidden.

## 3. Current implementation fact and successor split

The authenticated current implementation is Python source. Its public bridge:

- reauthenticates public manifest closures;
- creates only immutable in-memory snapshots and offline plans;
- fixes `candidate_only=true`, `native_api_reachable=false`, and
  `rehearsal_pass=false`; and
- deliberately does not create a native root, process, handle guard, witness,
  commit transaction, or live decision.

The future materialized runtime therefore has three separately authenticated
payload classes.

### 3.1 Retained public Python source

The future runtime source manifest must enumerate the exact assembly child,
verifier, bootstrap, and I0-I3 component source bytes admitted by the
effective assembly design. Every runtime `.py` file is copied byte-for-byte;
no source generation, line-ending conversion, template expansion, bytecode
generation, or source rewrite is permitted.

The RPNP v0.3 Python package remains offline plan and validation code. It is
build evidence and may be used by an offline verifier, but it is not silently
promoted into the native preloader or live guard.

### 3.2 New native source closure

A later implementation gate must provide a separately manifested, public,
exact source closure for:

- one native x64 preloader executable;
- one CPython 3.12 x64 extension named
  `s0_runtime_handle_guard_v0_4` with entry point
  `PyInit_s0_runtime_handle_guard_v0_4`;
- any private common headers or generated constant tables;
- the deterministic build recipe; and
- the static PE/import/package inspector and materializer source.

No native file exists by implication. No source may be synthesized from a
binary, downloaded during a build, selected from a working directory, or
substituted through an environment variable.

### 3.3 External runtime distribution closure

The future profile must receive an exact offline CPython 3.12 x64 runtime
distribution manifest and exact dependency manifest. They include every
interpreter executable, DLL, standard-library archive or file, distribution
metadata file, `jsonschema` 4.26.0 file, transitive dependency file, and
app-local CRT file actually used. Ambient site packages, user site, registry
discovery, `PATH`, `PYTHONPATH`, package installation, and network resolution
are forbidden.

## 4. External pins required before implementation

The following values are intentionally not selected by this design and must
be supplied by CONTROL as exact lowercase SHA-256 pins in a later
implementation gate:

1. native source manifest;
2. materializer and static-inspector source manifest;
3. offline toolchain bundle manifest;
4. exact compiler, linker, resource compiler if any, Windows SDK, headers,
   libraries, and CRT identities;
5. exact CPython 3.12 x64 distribution manifest;
6. exact Python dependency manifest;
7. exact admitted Windows build and system-image manifest;
8. exact build profile and canonical command plan;
9. exact runtime-tree profile; and
10. approving independent design review Markdown.

Until every pin exists and is authenticated by an outer verifier before any
candidate import or tool execution, the implementation state is
`BLOCKED-MISSING-EXTERNAL-PIN`. A placeholder, moving version label, package
name, PATH lookup, registry lookup, installer result, web URL, newest-version
selection, or candidate-selected hash is not a pin.

## 5. Offline toolchain closure

The toolchain is one immutable, offline, exact-file-set bundle. Its manifest
must include every executable, DLL, header, library, response-file template,
SDK metadata file, and license file used by the build. Each row binds the
canonical virtual path, byte length, and SHA-256. Executable tools additionally
bind PE machine, file version identity, and static import identity.

The build controller may address tools only by manifest virtual path resolved
inside its authenticated snapshot. It must use:

- no shell;
- no command search;
- no inherited PATH;
- no registry or Visual Studio discovery;
- no network;
- no package manager;
- no response file not already represented by canonical bytes;
- no system temp outside the admitted build root; and
- no compiler cache, incremental database, telemetry, plugin, extension, or
  user profile.

The actual compiler family and version remain an external decision. The
future build profile freezes the exact executable hashes and every argv item;
passing this design never approves an arbitrary compiler.

## 6. Canonical build plan

The future `S0-PUBLIC-ASSEMBLY-BUILD-PROFILE-1` is strict canonical JSON. Its
schema is supplied in this package. It binds all source, toolchain, dependency,
platform, design, and review pins and a complete ordered command list.

JSON Schema cannot prove cross-object equality or uniqueness by a nested
subfield. The profile therefore binds an independently authenticated semantic
validator implementation. That validator must execute every named semantic
relation, including command-to-tool identity, all provenance chains, A/B byte
identity, and exact Windows path/object policy. Merely listing a relation ID
is never acceptance evidence.

Each command binds:

- a stable command ID;
- an exact tool-manifest row;
- an argv array with no shell quoting interpretation;
- an exact virtual working directory;
- an exact environment map;
- closed stdin;
- bounded captured stdout and stderr;
- timeout, maximum output bytes, and acceptable exit code;
- exact declared input rows; and
- exact declared output rows.

The environment contains only keys listed in the profile. Locale, code page,
timezone, temporary directories, home/profile paths, source date, processor
count, and deterministic-tool switches are explicit. Unlisted environment
values are removed. Build parallelism is one unless a later reviewed profile
proves deterministic parallel output.

No absolute host path may be embedded in an output. The profile supplies one
fixed virtual source root and path-remapping policy. The inspector rejects a
host username, drive-specific build path, temporary path, random GUID,
wall-clock timestamp, nonprofile build identifier, or other unbound entropy in
an output.

## 7. Two-build reproducibility transaction

A future build candidate performs exactly two builds, `A` and `B`, from the
same authenticated byte snapshots in two previously absent roots. Neither
root, cache, object file, generated source, environment object, or tool process
is reused.

The ordered transaction is:

1. authenticate every external manifest and target;
2. copy exact bytes into private immutable input snapshots;
3. create fresh build roots A and B;
4. execute the same canonical command plan once per root;
5. close all build processes and file handles;
6. enumerate only the declared output set;
7. reject missing, extra, reparse, hard-link, ADS, case-fold-colliding, or
   nonregular output;
8. independently hash every output and perform static binary inspection;
9. require byte-for-byte equality for every corresponding A/B output;
10. construct the runtime package independently from A and B;
11. require the two runtime manifests and every runtime file byte-identical;
    and
12. freeze build and materialization records only after all comparisons pass.

Equal source hashes or equal compiler exit codes are not reproducibility.
Every shipped byte must match. Any mismatch rejects the complete candidate;
no output from either root may be patched, selected, normalized after the
fact, or used to seed a retry.

## 8. Native binary and import closure

The initial public candidate is unsigned. Authenticode certificate-table size
must be zero. No key, signing service, timestamp service, or signature claim
is part of this gate. A future signing policy requires a separate gate.

The static inspector must reject unless each native output satisfies its
future frozen profile, including:

- PE32+ AMD64 machine identity;
- exact image size, section table, characteristics, entry point, subsystem,
  import table, export table, relocation table, load-config table, and
  manifest/resource hashes;
- no delay import, bound import, TLS callback, CLR header, writable-executable
  section, embedded absolute host path, debug directory, CodeView record, or
  PDB reference;
- required ASLR, high-entropy VA, NX, and Control Flow Guard policy;
- no `LoadLibrary*`, `GetProcAddress`, generic FFI, shell, network, provider,
  or plugin import;
- direct `kernel32.dll!CreateProcessW` and `ntdll.dll!NtCreateFile` bindings
  where assigned by the effective design;
- the guard's exact initialization export and exact semantic Windows-call
  import closure; and
- equality between each admitted binary byte hash and the image later loaded
  from the runtime tree.

The complete import allowlist is a future profile value derived from reviewed
source and the exact toolchain. This design does not treat an omitted import
from a guessed list as safe.

## 9. Runtime tree materialization

The materializer writes only to a new, dedicated staging root. Its input is an
authenticated mapping from canonical POSIX virtual path to exact bytes. A
valid path is relative, nonempty, UTF-8, slash-separated, free of `.` and
`..`, drive syntax, UNC syntax, colon, NUL, trailing dot/space, reserved
Windows device names, and case-fold collision.

The runtime tree must contain exactly the future runtime manifest rows and no
side file. Every row binds:

- virtual path;
- semantic role;
- source or build-output provenance row;
- byte length;
- SHA-256;
- executable/data classification; and
- load or read phase.

The initial package has no `.pyc`, PDB, build log, source tree, test file,
toolchain file, private key, signature, cache, temp file, user data, or F0
artifact. Directories and files must be regular, non-reparse objects with no
ADS or hard-link alias. The materializer must use create-new semantics, write
exact length, flush, close, reopen by retained parent-relative authority,
rehash, and reject identity change. The final root is published once by an
atomic same-volume rename only after the exact manifest and record are frozen.

An existing destination, cross-volume move, path reopen outside retained
parents, partial publication, duplicate publication, cleanup-and-retry, or
post-publication modification rejects. Any created residue is quarantined.

## 10. Runtime load and import rules

CONTROL authenticates the complete runtime manifest and every file before
launching the preloader. The preloader executable is selected by exact final
path, bytes, file identity, and runtime-manifest row. It is not selected by
extension, PATH, current directory, or registry.

The verifier application, Python DLL, standard library, native guard, Python
dependencies, bootstrap, assembly source, component source, profiles, and
fixed public inputs are each exact runtime rows. The launch profile fixes the
application path, writable command line, environment block, current directory,
and DLL-search assumptions. It requires isolated Python operation equivalent
to `-I -S -B`, no user site, no bytecode writes, no ambient module discovery,
and source-only loading from the authenticated runtime allowlist.

The runtime must revalidate loaded-image identities against the static
runtime manifest before authority-bearing child work. The v0.4 known-five
handle guard remains limited to its observable handles. Build and package
authentication do not replace the separately gated Windows handle-inheritance
and atomic-root platform probes.

## 11. Records, failure classes, and authority

The future candidate emits three canonical public records:

1. `S0-PUBLIC-ASSEMBLY-BUILD-RECORD-1` for input pins, command results, output
   hashes, and A/B equality;
2. `S0-PUBLIC-ASSEMBLY-RUNTIME-MATERIALIZATION-RECORD-1` for the exact runtime
   tree, publication transaction, and final identity; and
3. `S0-PUBLIC-ASSEMBLY-BINARY-INSPECTION-RECORD-1` for static PE/import
   predicates.

Records are diagnostic. They are not reusable capabilities, live decisions,
or rehearsal PASS. A later launcher must reauthenticate original manifest and
runtime bytes in its own operation.

The first primary failure is preserved:

| Class | Meaning |
|---|---|
| `BR-AUTH/0` | missing or mismatched public authority before any process |
| `BR-SOURCE/0` | source or dependency closure defect before any process |
| `BR-TOOLCHAIN/0` | toolchain or command-profile defect before any process |
| `BR-BUILD/0` | first build failed before creating a declared output |
| `BR-BUILD/1` | build failed after creating any declared output |
| `BR-REPRO/1` | A/B output or runtime-tree mismatch |
| `BR-BINARY/1` | PE, import, export, resource, or loaded-image profile defect |
| `BR-MATERIALIZE/1` | runtime-tree construction or publication defect |
| `BR-RECORD/1` | canonical record, hash, or close/read-back defect |

`/0` means no admitted output was created. `/1` means created residue is
quarantined. Cleanup failure never replaces the first class. A retry requires
new roots and a new gate-approved candidate version; it cannot reuse objects
or choose the better of two outputs.

## 12. Resource bounds

The future profile must remain within these public upper bounds:

- authenticated source bytes: 256 MiB;
- offline toolchain bundle: 24 GiB;
- CPython and dependency bundle: 4 GiB;
- each clean build root: 32 GiB;
- each materialization staging root: 4 GiB;
- final runtime tree: 2 GiB and 20,000 files;
- aggregate child-process private bytes: 16 GiB;
- concurrent build processes: 1;
- wall time per clean build: 3,600 seconds;
- captured stdout plus stderr per command: 16 MiB; and
- materialization wall time: 1,800 seconds.

Crossing a bound stops the transaction and preserves the correct first
failure class. Bounds are maximums, not expected consumption or performance
claims.

## 13. Review and later gate order

The required order is:

1. fresh independent review of this exact design package;
2. CONTROL disposition and integration of a zero-blocking/zero-major design;
3. a separately opened public implementation candidate gate with every
   external pin in Section 4;
4. fresh source, toolchain-profile, build-controller, schema, semantic-
   validator, inspector, and materializer implementation review;
5. a separately opened bounded build and materialization execution gate;
6. independent reproducibility, binary/import, build-record, and runtime-tree
   review of the materialized outputs;
7. a separately opened bounded real-Windows platform-probe gate;
8. live assembly candidate reconsideration; and
9. only afterward, official public rehearsal reconsideration.

No step starts automatically. In particular, design acceptance does not
authorize compilation, package installation, runtime materialization, native
execution, or a platform probe.

## 14. Closed boundaries and maximum claim

This design does not authorize or establish:

- any actual native source, compiler, linker, SDK, build, binary, runtime
  package, loaded image, Windows behavior, or performance result;
- F0 content, hidden oracle, fixture, executor, judge, scoring, provider/model,
  network, S0, or E0 work;
- central-system or Project Brain implementation;
- operational safety, economic value, production readiness, or model transfer;
  or
- commit, push, PR, main integration, release, signing, or deployment.

Maximum claim: v0.1 defines a bounded public design for authenticating sources
and tools, building twice, statically inspecting native outputs, and
materializing an exact runtime tree while keeping every live and rehearsal
authority closed.
