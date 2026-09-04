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

$nativeRoot = $PSScriptRoot
$header = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_runtime_v0_4.h')) 'ABI header'
$preloaderSource = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_neutral_preloader_v0_4.cpp')) 'preloader source'
$guardSource = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 's0_runtime_handle_guard_v0_4.cpp')) 'guard source'
$buildRecipe = Resolve-ExactFile $MyInvocation.MyCommand.Path 'build recipe'
$buildContract = Resolve-ExactFile ([IO.Path]::Combine($nativeRoot, 'build-contract.json')) 'build contract'
$preloaderOutput = [IO.Path]::Combine($output.FullName, 's0_neutral_preloader_v0_4.exe')
$guardOutput = [IO.Path]::Combine($output.FullName, 's0_runtime_handle_guard_v0_4.pyd')
$preloaderObject = [IO.Path]::Combine($output.FullName, 's0_neutral_preloader_v0_4.obj')
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

$sourceRows = @($buildContract, $buildRecipe, $header, $preloaderSource, $guardSource) | Sort-Object | ForEach-Object {
    $item = Get-Item -LiteralPath $_
    [ordered]@{
        path = $item.FullName
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        size = $item.Length
    }
}
$outputRows = @($preloaderOutput, $guardOutput) | ForEach-Object {
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
    outputs = $outputRows
    preloader_compiler_argv = $preloaderCompilerArgv
    preloader_linker_argv = $preloaderLinkerArgv
    python_import_library = [ordered]@{
        path = $pythonLibrary
        sha256 = (Get-FileHash -LiteralPath $pythonLibrary -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    schema_id = 'S0-RUNTIME-PRELOADER-V0.4-BUILD-TRACE-1'
    sources = $sourceRows
}
$tracePath = [IO.Path]::Combine($output.FullName, 'build-trace.json')
$traceBytes = [Text.UTF8Encoding]::new($false).GetBytes(($trace | ConvertTo-Json -Depth 8 -Compress) + "`n")
[IO.File]::WriteAllBytes($tracePath, $traceBytes)
[ordered]@{
    output_root = $output.FullName
    preloader_sha256 = $outputRows[0].sha256
    guard_sha256 = $outputRows[1].sha256
    trace_sha256 = (Get-FileHash -LiteralPath $tracePath -Algorithm SHA256).Hash.ToLowerInvariant()
}
