[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ClExe,
    [Parameter(Mandatory = $true)][string]$LinkExe,
    [Parameter(Mandatory = $true)][string]$PythonInclude,
    [Parameter(Mandatory = $true)][string]$PythonImportLibrary,
    [Parameter(Mandatory = $true)][string[]]$ToolchainIncludeRoots,
    [Parameter(Mandatory = $true)][string[]]$ToolchainLibraryRoots,
    [Parameter(Mandatory = $true)][string]$OutputRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Resolve-ExactFile([string]$Path, [string]$Label) {
    if ($Path -notmatch '^[A-Za-z]:\\') {
        throw "$Label must be an absolute path"
    }
    $item = Get-Item -LiteralPath $Path -Force
    if (-not $item.PSIsContainer -and -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        return $item.FullName
    }
    throw "$Label must be one non-link file"
}

function Resolve-ExactDirectory([string]$Path, [string]$Label) {
    if ($Path -notmatch '^[A-Za-z]:\\') {
        throw "$Label must be an absolute path"
    }
    $item = Get-Item -LiteralPath $Path -Force
    if ($item.PSIsContainer -and -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        return $item.FullName
    }
    throw "$Label must be one non-link directory"
}

$compiler = Resolve-ExactFile $ClExe 'compiler'
$linker = Resolve-ExactFile $LinkExe 'linker'
$pythonIncludeRoot = Resolve-ExactDirectory $PythonInclude 'Python include root'
$pythonLibrary = Resolve-ExactFile $PythonImportLibrary 'Python import library'
$includeRoots = @($ToolchainIncludeRoots | ForEach-Object { Resolve-ExactDirectory $_ 'toolchain include root' })
$libraryRoots = @($ToolchainLibraryRoots | ForEach-Object { Resolve-ExactDirectory $_ 'toolchain library root' })
if ($includeRoots.Count -eq 0 -or $libraryRoots.Count -eq 0 -or
    $includeRoots.Count -ne (@($includeRoots | Sort-Object -Unique)).Count -or
    $libraryRoots.Count -ne (@($libraryRoots | Sort-Object -Unique)).Count) {
    throw 'toolchain include/library roots must be nonempty and unique'
}
if ($OutputRoot -notmatch '^[A-Za-z]:\\') {
    throw 'output root must be absolute'
}
if (Test-Path -LiteralPath $OutputRoot) {
    throw 'output root must be absent'
}
$parent = Resolve-ExactDirectory ([IO.Path]::GetDirectoryName($OutputRoot)) 'output parent'
$leaf = [IO.Path]::GetFileName($OutputRoot)
if ($leaf -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$') {
    throw 'output leaf is not canonical'
}
$output = New-Item -ItemType Directory -Path ([IO.Path]::Combine($parent, $leaf))
if ($output.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw 'created output root is a link'
}

$expectedTools = @{
    $compiler = '88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d'
    $linker = 'ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d'
    $pythonLibrary = 'f55daa479f2d82a073efbe6315c2164eb6c955cb1cc722ce03705afa8c93544f'
}
foreach ($tool in $expectedTools.Keys) {
    if ((Get-FileHash -LiteralPath $tool -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedTools[$tool]) {
        throw 'compiler, linker or Python import-library pin differs'
    }
}
if ((Get-FileHash -LiteralPath ([IO.Path]::Combine($pythonIncludeRoot, 'Python.h')) -Algorithm SHA256).Hash.ToLowerInvariant() -ne
    '6831c7fd01fff4553e50322422a1a09a0de2757caf3a6e883861d3433cfa6512') {
    throw 'Python header pin differs'
}
$nativeRoot = $PSScriptRoot
$header = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_runtime_v0_5.h')) 'ABI header'
$preloaderSource = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_neutral_preloader_v0_5.cpp')) 'preloader source'
$guardSource = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_runtime_handle_guard_v0_5.cpp')) 'guard source'
$materializerSource = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_runtime_materializer_v0_5.cpp')) 'materializer source'
$materializerOutput = [IO.Path]::Combine($output.FullName, 's0_runtime_materializer_v0_5.exe')
$materializerObject = [IO.Path]::Combine($output.FullName, 's0_runtime_materializer_v0_5.obj')
$buildRecipe = Resolve-ExactFile $MyInvocation.MyCommand.Path 'build recipe'
$buildContract = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 'build-contract.json')) 'build contract'
$preloaderOutput = [IO.Path]::Combine($output.FullName, 's0_neutral_preloader_v0_5.exe')
$guardOutput = [IO.Path]::Combine($output.FullName, 's0_runtime_handle_guard_v0_4.pyd')
$preloaderObject = [IO.Path]::Combine($output.FullName, 's0_neutral_preloader_v0_5.obj')
$guardObject = [IO.Path]::Combine($output.FullName, 's0_runtime_handle_guard_v0_4.obj')
$guardImportLibrary = [IO.Path]::Combine($output.FullName, 's0_runtime_handle_guard_v0_4.lib')

$common = @(
    '/nologo', '/std:c++17', '/EHsc', '/O2', '/W4', '/WX', '/GS', '/guard:cf',
    '/Qspectre', '/sdl', '/MT', '/DUNICODE', '/D_UNICODE',
    '/DWIN32_LEAN_AND_MEAN', '/DNOMINMAX', "/I$nativeRoot"
 ) + @($includeRoots | ForEach-Object { "/I$_" })
$link = @(
    '/DYNAMICBASE', '/HIGHENTROPYVA', '/NXCOMPAT', '/CETCOMPAT',
    '/GUARD:CF', '/INCREMENTAL:NO', '/OPT:REF', '/OPT:ICF'
)

$libraryArgs = @($libraryRoots | ForEach-Object { "/LIBPATH:$_" })
$preloaderCompilerArgv = @($common) + @('/c', "/Fo:$preloaderObject", $preloaderSource)
$guardCompilerArgv = @($common) + @('/c', "/I$pythonIncludeRoot", "/Fo:$guardObject", $guardSource)
$preloaderLinkerArgv = @($preloaderObject, "/OUT:$preloaderOutput", 'bcrypt.lib', 'ntdll.lib', 'kernel32.lib') + $libraryArgs + $link
$guardLinkerArgv = @($guardObject, '/DLL', "/OUT:$guardOutput", "/IMPLIB:$guardImportLibrary", $pythonLibrary, 'ntdll.lib', 'kernel32.lib') + $libraryArgs + $link
$materializerCompilerArgv = @($common) + @('/c', "/Fo:$materializerObject", $materializerSource)
$materializerLinkerArgv = @($materializerObject, "/OUT:$materializerOutput", 'advapi32.lib', 'bcrypt.lib', 'ntdll.lib', 'kernel32.lib') + $libraryArgs + $link
$sourceBefore = @{}
foreach ($source in @($buildContract, $buildRecipe, $header, $preloaderSource, $guardSource, $materializerSource)) {
    $sourceBefore[$source] = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
}
$savedInclude = $env:INCLUDE
$savedLib = $env:LIB
$savedCl = $env:CL
$savedClAfter = $env:_CL_
$savedLink = $env:LINK
try {
    $env:INCLUDE = ''
    $env:LIB = ''
    $env:CL = ''
    $env:_CL_ = ''
    $env:LINK = ''
    & $compiler @preloaderCompilerArgv
    if ($LASTEXITCODE -ne 0) { throw "preloader compile failed with exit $LASTEXITCODE" }
    & $compiler @guardCompilerArgv
    if ($LASTEXITCODE -ne 0) { throw "guard compile failed with exit $LASTEXITCODE" }
    & $compiler @materializerCompilerArgv
    if ($LASTEXITCODE -ne 0) { throw "materializer compile failed with exit $LASTEXITCODE" }
    & $linker @materializerLinkerArgv
    if ($LASTEXITCODE -ne 0) { throw "materializer link failed with exit $LASTEXITCODE" }
    & $linker @preloaderLinkerArgv
    if ($LASTEXITCODE -ne 0) { throw "preloader link failed with exit $LASTEXITCODE" }
    & $linker @guardLinkerArgv
    if ($LASTEXITCODE -ne 0) { throw "guard link failed with exit $LASTEXITCODE" }
}
finally {
    $env:INCLUDE = $savedInclude
    $env:LIB = $savedLib
    $env:CL = $savedCl
    $env:_CL_ = $savedClAfter
    $env:LINK = $savedLink
}

foreach ($source in $sourceBefore.Keys) {
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceBefore[$source]) {
        throw 'source bytes changed during build'
    }
}
$sourceRows = @($buildContract, $buildRecipe, $header, $preloaderSource, $guardSource, $materializerSource) | Sort-Object | ForEach-Object {
    $item = Get-Item -LiteralPath $_
    [ordered]@{
        path = $item.FullName
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        size = $item.Length
    }
}
$outputRows = @($preloaderOutput, $guardOutput, $materializerOutput) | ForEach-Object {
    $item = Get-Item -LiteralPath $_
    [ordered]@{
        filename = $item.Name
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        size = $item.Length
    }
}
$trace = [ordered]@{
    architecture = 'x64'
    compiler = [ordered]@{
        path = $compiler
        sha256 = (Get-FileHash -LiteralPath $compiler -Algorithm SHA256).Hash.ToLowerInvariant()
        version = (Get-Item -LiteralPath $compiler).VersionInfo.FileVersion
    }
    guard_compiler_argv = $guardCompilerArgv
    guard_linker_argv = $guardLinkerArgv
    include_roots = $includeRoots
    library_roots = $libraryRoots
    linker = [ordered]@{
        path = $linker
        sha256 = (Get-FileHash -LiteralPath $linker -Algorithm SHA256).Hash.ToLowerInvariant()
        version = (Get-Item -LiteralPath $linker).VersionInfo.FileVersion
    }
    materializer_compiler_argv = $materializerCompilerArgv
    materializer_linker_argv = $materializerLinkerArgv
    effective_interface_map_sha256 = 'f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623'
    effective_schema_sha256 = '04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e'
    source_observation = 'pre-post-sha256-equality-not-concurrent-build-input-proof'
    outputs = $outputRows
    preloader_compiler_argv = $preloaderCompilerArgv
    preloader_linker_argv = $preloaderLinkerArgv
    python_import_library = [ordered]@{
        path = $pythonLibrary
        sha256 = (Get-FileHash -LiteralPath $pythonLibrary -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    schema_id = 'S0-RUNTIME-PRELOADER-V0.5-BUILD-TRACE-1'
    sources = $sourceRows
}
$tracePath = [IO.Path]::Combine($output.FullName, 'build-trace.json')
$sortedTrace = [ordered]@{}
[string[]]$traceKeys = @($trace.Keys)
[Array]::Sort($traceKeys, [StringComparer]::Ordinal)
foreach ($key in $traceKeys) { $sortedTrace.Add($key, $trace[$key]) }
$traceBytes = [Text.UTF8Encoding]::new($false).GetBytes(($sortedTrace | ConvertTo-Json -Depth 8 -Compress) + "`n")
[IO.File]::WriteAllBytes($tracePath, $traceBytes)
[ordered]@{
    output_root = $output.FullName
    preloader_sha256 = $outputRows[0].sha256
    guard_sha256 = $outputRows[1].sha256
    materializer_sha256 = $outputRows[2].sha256
    trace_sha256 = (Get-FileHash -LiteralPath $tracePath -Algorithm SHA256).Hash.ToLowerInvariant()
}
