[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-f]{64}$')]
    [string]$ExpectedManifestSha256
)

$ErrorActionPreference = 'Stop'
if ($ExpectedManifestSha256 -cnotmatch '^[0-9a-f]{64}$') {
    throw 'expected manifest SHA-256 must be exactly 64 lowercase hexadecimal characters'
}

$scriptPath = [System.IO.Path]::GetFullPath($MyInvocation.MyCommand.Path)
$i2Root = [System.IO.Path]::GetFullPath((Join-Path (Split-Path $scriptPath -Parent) '..'))
$repositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $i2Root '..\..'))
$manifestPath = [System.IO.Path]::GetFullPath(
    (Join-Path $i2Root 'verification\implementation-files.sha256')
)
$manifestRelativePath = 's0-lab/i2/verification/implementation-files.sha256'
$manifestAnchorPath = [System.IO.Path]::GetFullPath(
    (Join-Path $i2Root 'verification\implementation-manifest.sha256')
)
$manifestAnchorRelativePath = 's0-lab/i2/verification/implementation-manifest.sha256'
$publicSourceManifestRelativePath = 's0-lab/i2/spec/public-source-files.sha256'
$requiredPublicSourcePaths = @(
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.md'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/control-integration-decision-v0.1.sha256'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.md'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/trust-root-role-isolation-design-revision-v0.4.sha256'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.md'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/identity-authority-matrix-addendum-v0.4.sha256'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.md'
    's0-lab/control/isolation/trust-root-role-isolation-v0.4/isolation-acceptance-plan-addendum-v0.4.sha256'
    's0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.md'
    's0-lab/control/isolation/order-eight-public-vector-v0.1/tri2-vec-02-control-final-freeze-decision-v0.1.sha256'
    's0-lab/i1/spec/public-runtime-files.sha256'
    's0-lab/i1/spec/public-runtime-v0.14.json'
)
$strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
$priorPythonPath = $env:PYTHONPATH
$priorNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$priorNoUserSite = $env:PYTHONNOUSERSITE
$priorHashSeed = $env:PYTHONHASHSEED
$priorSafePath = $env:PYTHONSAFEPATH

function Write-Pass {
    param([string]$Phase, [string]$Check)
    Write-Host ("PASS [{0}] {1}" -f $Phase, $Check)
}

function Get-BytesSha256 {
    param([byte[]]$Bytes)
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [System.BitConverter]::ToString($hasher.ComputeHash($Bytes)).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $hasher.Dispose()
    }
}

function Assert-DescendantPath {
    param(
        [string]$Candidate,
        [string]$Root,
        [string]$Label
    )
    $candidateFull = [System.IO.Path]::GetFullPath($Candidate)
    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $prefix = $rootFull + [System.IO.Path]::DirectorySeparatorChar
    if (-not $candidateFull.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw ("{0} escaped its authenticated root" -f $Label)
    }
    return $candidateFull
}

function Assert-ManifestTextBytes {
    param(
        [byte[]]$Bytes,
        [string]$Phase
    )
    if ($Bytes.Length -eq 0) {
        throw 'I2 payload manifest empty check failed'
    }
    Write-Pass $Phase 'payload-manifest:non-empty'

    $hasUtf8Bom = $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xef -and $Bytes[1] -eq 0xbb -and $Bytes[2] -eq 0xbf
    if ($hasUtf8Bom) {
        throw 'I2 payload manifest BOM check failed'
    }
    Write-Pass $Phase 'payload-manifest:BOM(EF-BB-BF)'

    try {
        $text = $strictUtf8.GetString($Bytes)
    }
    catch {
        throw 'I2 payload manifest UTF-8 check failed'
    }
    Write-Pass $Phase 'payload-manifest:UTF-8'

    if ($Bytes -contains 0x0d) {
        throw 'I2 payload manifest LF-only check failed'
    }
    Write-Pass $Phase 'payload-manifest:LF-only'

    if ($Bytes[$Bytes.Length - 1] -ne 0x0a) {
        throw 'I2 payload manifest final-LF check failed'
    }
    Write-Pass $Phase 'payload-manifest:final-LF'

    if ($text -match '(?m)[ \t]+$') {
        throw 'I2 payload manifest trailing-whitespace check failed'
    }
    Write-Pass $Phase 'payload-manifest:trailing-whitespace'

    if ($Bytes | Where-Object { $_ -gt 0x7f }) {
        throw 'I2 payload manifest ASCII check failed'
    }
    Write-Pass $Phase 'payload-manifest:ASCII'
    return $text
}

function Assert-PublicSourceManifestTextBytes {
    param(
        [byte[]]$Bytes,
        [string]$Phase
    )
    if ($Bytes.Length -eq 0) {
        throw 'I2 public-source manifest empty check failed'
    }
    Write-Pass $Phase 'public-source-manifest:non-empty'

    $hasUtf8Bom = $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xef -and $Bytes[1] -eq 0xbb -and $Bytes[2] -eq 0xbf
    if ($hasUtf8Bom) {
        throw 'I2 public-source manifest BOM check failed'
    }
    Write-Pass $Phase 'public-source-manifest:BOM(EF-BB-BF)'

    try {
        $text = $strictUtf8.GetString($Bytes)
    }
    catch {
        throw 'I2 public-source manifest UTF-8 check failed'
    }
    Write-Pass $Phase 'public-source-manifest:UTF-8'

    if ($Bytes -contains 0x0d) {
        throw 'I2 public-source manifest LF-only check failed'
    }
    Write-Pass $Phase 'public-source-manifest:LF-only'

    if ($Bytes[$Bytes.Length - 1] -ne 0x0a) {
        throw 'I2 public-source manifest final-LF check failed'
    }
    Write-Pass $Phase 'public-source-manifest:final-LF'

    if ($text -match '(?m)[ \t]+$') {
        throw 'I2 public-source manifest trailing-whitespace check failed'
    }
    Write-Pass $Phase 'public-source-manifest:trailing-whitespace'

    if ($Bytes | Where-Object { $_ -gt 0x7f }) {
        throw 'I2 public-source manifest ASCII check failed'
    }
    Write-Pass $Phase 'public-source-manifest:ASCII'
    return $text
}

function Assert-ManifestAnchorBytes {
    param(
        [byte[]]$Bytes,
        [string]$Phase
    )
    if ($Bytes.Length -eq 0) {
        throw 'I2 manifest anchor empty check failed'
    }
    Write-Pass $Phase 'manifest-anchor:non-empty'

    $hasUtf8Bom = $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xef -and $Bytes[1] -eq 0xbb -and $Bytes[2] -eq 0xbf
    if ($hasUtf8Bom) {
        throw 'I2 manifest anchor BOM check failed'
    }
    Write-Pass $Phase 'manifest-anchor:BOM(EF-BB-BF)'

    try {
        $text = $strictUtf8.GetString($Bytes)
    }
    catch {
        throw 'I2 manifest anchor UTF-8 check failed'
    }
    Write-Pass $Phase 'manifest-anchor:UTF-8'

    if ($Bytes -contains 0x0d) {
        throw 'I2 manifest anchor LF-only check failed'
    }
    Write-Pass $Phase 'manifest-anchor:LF-only'

    if ($Bytes[$Bytes.Length - 1] -ne 0x0a) {
        throw 'I2 manifest anchor final-LF check failed'
    }
    Write-Pass $Phase 'manifest-anchor:final-LF'

    if ($text -match '(?m)[ \t]+$') {
        throw 'I2 manifest anchor trailing-whitespace check failed'
    }
    Write-Pass $Phase 'manifest-anchor:trailing-whitespace'

    if ($Bytes | Where-Object { $_ -gt 0x7f }) {
        throw 'I2 manifest anchor ASCII check failed'
    }
    Write-Pass $Phase 'manifest-anchor:ASCII'

    if ($text -cnotmatch '^([0-9a-f]{64})  implementation-files\.sha256\n$') {
        throw 'I2 manifest anchor format check failed'
    }
    Write-Pass $Phase 'manifest-anchor:format'
    return [PSCustomObject]@{
        Text = $text
        ManifestSha256 = $Matches[1]
    }
}

function Get-PlainRepositoryFile {
    param([string]$RelativePath)

    $repositoryItem = Get-Item -Force -LiteralPath $repositoryRoot
    if (-not $repositoryItem.PSIsContainer -or
        ($repositoryItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or
        ($repositoryItem.Attributes -band [System.IO.FileAttributes]::Device) -ne 0) {
        throw 'repository root is not a plain directory'
    }
    $parts = $RelativePath.Split('/')
    $current = $repositoryRoot
    for ($index = 0; $index -lt $parts.Length; $index++) {
        $current = Assert-DescendantPath -Candidate (Join-Path $current $parts[$index]) -Root $repositoryRoot -Label 'public-source path'
        if (-not (Test-Path -LiteralPath $current)) {
            throw 'I2 public-source input is missing'
        }
        $item = Get-Item -Force -LiteralPath $current
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or
            ($item.Attributes -band [System.IO.FileAttributes]::Device) -ne 0) {
            throw 'I2 public-source path is reparse-backed or device-backed'
        }
        $isFinal = $index -eq ($parts.Length - 1)
        if ($isFinal -and ($item.PSIsContainer -or $item -isnot [System.IO.FileInfo])) {
            throw 'I2 public-source input is not a plain regular file'
        }
        if (-not $isFinal -and -not $item.PSIsContainer) {
            throw 'I2 public-source parent is not a plain directory'
        }
    }
    return $current
}

function Get-NamespaceFiles {
    param(
        [string]$NamespaceRoot,
        [string]$Phase
    )
    $rootItem = Get-Item -Force -LiteralPath $NamespaceRoot
    if (-not $rootItem.PSIsContainer -or
        ($rootItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'I2 namespace root is not a plain directory'
    }

    $files = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $directories = [System.Collections.Generic.Stack[string]]::new()
    $directories.Push($rootItem.FullName)
    while ($directories.Count -gt 0) {
        $current = $directories.Pop()
        foreach ($item in Get-ChildItem -Force -LiteralPath $current) {
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw 'I2 namespace contains a reparse-backed path'
            }
            if (($item.Attributes -band [System.IO.FileAttributes]::Device) -ne 0) {
                throw 'I2 namespace contains a device-backed path'
            }
            if ($item.PSIsContainer) {
                $directories.Push($item.FullName)
                continue
            }
            if ($item -isnot [System.IO.FileInfo]) {
                throw 'I2 namespace contains a non-regular filesystem entry'
            }
            $relative = $item.FullName.Substring($repositoryRoot.Length + 1).Replace('\', '/')
            if (-not $files.Add($relative)) {
                throw 'I2 namespace contains a duplicate normalized file path'
            }
        }
    }
    Write-Pass $Phase 'namespace:no-reparse-device-or-special-entries'
    return ,$files
}

function Get-I2PayloadSnapshot {
    param([string]$Phase)

    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
        throw 'I2 implementation payload manifest is missing'
    }
    $manifestItem = Get-Item -Force -LiteralPath $manifestPath
    if (($manifestItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw 'I2 implementation payload manifest is reparse-backed'
    }
    $manifestBytes = [System.IO.File]::ReadAllBytes($manifestPath)
    $actualManifestHash = Get-BytesSha256 -Bytes $manifestBytes
    if ($actualManifestHash -cne $ExpectedManifestSha256) {
        throw ("external expected-manifest check failed: expected {0}, observed {1}" -f $ExpectedManifestSha256, $actualManifestHash)
    }
    Write-Pass $Phase 'external-expected-manifest-sha256'

    $manifestText = Assert-ManifestTextBytes -Bytes $manifestBytes -Phase $Phase

    if (-not (Test-Path -LiteralPath $manifestAnchorPath -PathType Leaf)) {
        throw 'I2 implementation manifest anchor is missing'
    }
    $anchorItem = Get-Item -Force -LiteralPath $manifestAnchorPath
    if ($anchorItem -isnot [System.IO.FileInfo] -or
        ($anchorItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or
        ($anchorItem.Attributes -band [System.IO.FileAttributes]::Device) -ne 0) {
        throw 'I2 implementation manifest anchor is not a plain regular file'
    }
    $anchorBytes = [System.IO.File]::ReadAllBytes($manifestAnchorPath)
    $anchor = Assert-ManifestAnchorBytes -Bytes $anchorBytes -Phase $Phase
    if ($anchor.ManifestSha256 -cne $ExpectedManifestSha256) {
        throw 'I2 manifest anchor does not corroborate the external lowercase SHA-256 pin'
    }
    Write-Pass $Phase 'manifest-anchor:corroborates-external-anchor'

    $listed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $payloadBytes = [System.Collections.Generic.Dictionary[string,byte[]]]::new([System.StringComparer]::Ordinal)
    $observedRows = [System.Collections.Generic.List[string]]::new()
    $manifestLines = $manifestText.Substring(0, $manifestText.Length - 1).Split("`n")
    foreach ($line in $manifestLines) {
        if ($line -cnotmatch '^([0-9a-f]{64})  (s0-lab/i2/[A-Za-z0-9._/-]+)$') {
            throw 'I2 payload manifest row-format check failed'
        }
        $expectedHash = $Matches[1]
        $relative = $Matches[2]
        $parts = $relative.Split('/')
        if ($relative.Contains('\') -or $relative.StartsWith('/') -or
            $parts -contains '' -or $parts -contains '.' -or $parts -contains '..' -or
            $relative.Contains(':')) {
            throw 'I2 payload manifest contains an unsafe path'
        }
        if ($relative -ceq $manifestRelativePath) {
            throw 'I2 payload manifest must not contain itself'
        }
        if ($relative -ceq $manifestAnchorRelativePath) {
            throw 'I2 payload manifest must not contain its corroborating anchor'
        }
        if (-not $listed.Add($relative)) {
            throw 'I2 payload manifest contains a duplicate path'
        }

        $candidate = Assert-DescendantPath -Candidate (
            Join-Path $repositoryRoot ($relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        ) -Root $i2Root -Label 'I2 payload path'
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            throw 'I2 payload manifest file is missing'
        }
        $item = Get-Item -Force -LiteralPath $candidate
        if ($item -isnot [System.IO.FileInfo] -or
            ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or
            ($item.Attributes -band [System.IO.FileAttributes]::Device) -ne 0) {
            throw 'I2 payload manifest path is not a plain regular file'
        }
        $bytes = [System.IO.File]::ReadAllBytes($candidate)
        $actualHash = Get-BytesSha256 -Bytes $bytes
        if ($actualHash -cne $expectedHash) {
            throw 'I2 payload file hash check failed'
        }
        $payloadBytes.Add($relative, $bytes)
        $observedRows.Add(("{0}  {1}" -f $actualHash, $relative))
    }
    if ($listed.Count -eq 0) {
        throw 'I2 payload manifest row-count check failed: no payload rows'
    }
    Write-Pass $Phase ("payload-manifest:exact-row-count={0}" -f $listed.Count)

    if (-not $listed.Contains($publicSourceManifestRelativePath)) {
        throw 'I2 payload manifest does not authenticate the public-source manifest'
    }
    Write-Pass $Phase 'payload-manifest:public-source-manifest-included'

    $startupHooks = @($listed | Where-Object {
        $_ -cmatch '(?:^|/)(?:sitecustomize\.py|usercustomize\.py|pyvenv\.cfg)$' -or
        $_ -cmatch '\.pth$'
    })
    if ($startupHooks.Count -ne 0) {
        throw 'I2 payload contains a forbidden Python startup hook'
    }
    Write-Pass $Phase 'payload-manifest:no-Python-startup-hooks'

    $diskFiles = Get-NamespaceFiles -NamespaceRoot $i2Root -Phase $Phase
    if (-not $diskFiles.Remove($manifestRelativePath)) {
        throw 'I2 namespace enumeration did not contain its payload manifest'
    }
    if (-not $diskFiles.Remove($manifestAnchorRelativePath)) {
        throw 'I2 namespace enumeration did not contain its corroborating manifest anchor'
    }
    if (-not $listed.SetEquals($diskFiles)) {
        throw 'I2 payload manifest exact-file-set check failed'
    }
    Write-Pass $Phase 'payload-manifest:forced-hidden-exact-file-set'

    $behaviorTests = @($listed | Where-Object {
        $_ -cmatch '^s0-lab/i2/tests/test_[A-Za-z0-9._-]+\.py$'
    })
    if ($behaviorTests.Count -eq 0) {
        throw 'I2 behavior tests unavailable: manifest contains no test_*.py payload'
    }
    Write-Pass $Phase ("behavior-test-payloads:present={0}" -f $behaviorTests.Count)

    $contractCandidates = @($listed | Where-Object {
        $_ -cmatch '^s0-lab/i2/spec/trust-root-role-isolation-contract-v[0-9]+(?:\.[0-9]+)*\.json$'
    })
    if ($contractCandidates.Count -ne 1) {
        throw ("I2 contract selection check failed: expected exactly one versioned contract, found {0}" -f $contractCandidates.Count)
    }
    Write-Pass $Phase 'contract-selection:exactly-one-versioned-public-contract'

    $fingerprintInput = (@($actualManifestHash) + @($observedRows | Sort-Object)) -join "`n"
    $fingerprintBytes = [System.Text.Encoding]::ASCII.GetBytes($fingerprintInput + "`n")
    return [PSCustomObject]@{
        ManifestSha256 = $actualManifestHash
        ManifestAnchorSha256 = Get-BytesSha256 -Bytes $anchorBytes
        PayloadFingerprint = Get-BytesSha256 -Bytes $fingerprintBytes
        RowCount = $listed.Count
        ManifestBytes = $manifestBytes
        ManifestAnchorBytes = $anchorBytes
        PayloadBytes = $payloadBytes
        ContractRelativePath = $contractCandidates[0]
    }
}

function Get-PublicSourceSnapshot {
    param(
        [byte[]]$ManifestBytes,
        [string]$Phase
    )

    $manifestText = Assert-PublicSourceManifestTextBytes -Bytes $ManifestBytes -Phase $Phase
    $manifestSha256 = Get-BytesSha256 -Bytes $ManifestBytes
    $required = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($relative in $requiredPublicSourcePaths) {
        [void]$required.Add($relative)
    }
    if ($required.Count -ne 12) {
        throw 'internal public-source allowlist count is not exactly 12'
    }

    $listed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $sourceBytes = [System.Collections.Generic.Dictionary[string,byte[]]]::new([System.StringComparer]::Ordinal)
    $observedRows = [System.Collections.Generic.List[string]]::new()
    $lines = $manifestText.Substring(0, $manifestText.Length - 1).Split("`n")
    foreach ($line in $lines) {
        if ($line -cnotmatch '^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$') {
            throw 'I2 public-source manifest row-format check failed'
        }
        $expectedHash = $Matches[1]
        $relative = $Matches[2]
        $parts = $relative.Split('/')
        if ($relative.Contains('\') -or $relative.StartsWith('/') -or
            $parts -contains '' -or $parts -contains '.' -or $parts -contains '..' -or
            $relative.Contains(':')) {
            throw 'I2 public-source manifest contains an unsafe path'
        }
        if (-not $required.Contains($relative)) {
            throw 'I2 public-source manifest contains a path outside the exact public allowlist'
        }
        if (-not $listed.Add($relative)) {
            throw 'I2 public-source manifest contains a duplicate path'
        }

        $candidate = Get-PlainRepositoryFile -RelativePath $relative
        $bytes = [System.IO.File]::ReadAllBytes($candidate)
        $actualHash = Get-BytesSha256 -Bytes $bytes
        if ($actualHash -cne $expectedHash) {
            throw 'I2 public-source input hash check failed'
        }
        $sourceBytes.Add($relative, $bytes)
        $observedRows.Add(("{0}  {1}" -f $actualHash, $relative))
    }
    if ($listed.Count -ne 12 -or -not $listed.SetEquals($required)) {
        throw ("I2 public-source exact-12-row allowlist check failed: found {0}" -f $listed.Count)
    }
    Write-Pass $Phase 'public-source-manifest:exact-12-row-allowlist'
    Write-Pass $Phase 'public-source-inputs:plain-files-and-sha256'

    $fingerprintInput = (@($manifestSha256) + @($observedRows | Sort-Object)) -join "`n"
    $fingerprintBytes = [System.Text.Encoding]::ASCII.GetBytes($fingerprintInput + "`n")
    return [PSCustomObject]@{
        ManifestSha256 = $manifestSha256
        InputFingerprint = Get-BytesSha256 -Bytes $fingerprintBytes
        RowCount = $listed.Count
        InputBytes = $sourceBytes
    }
}

function New-AuthenticatedSnapshot {
    param(
        [object]$Snapshot,
        [object]$PublicSources
    )

    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $snapshotRoot = [System.IO.Path]::Combine(
        $tempBase,
        's0-i2-public-verify-' + [System.Guid]::NewGuid().ToString('N')
    )
    $snapshotRoot = Assert-DescendantPath -Candidate $snapshotRoot -Root $tempBase -Label 'authenticated snapshot path'
    [void][System.IO.Directory]::CreateDirectory($snapshotRoot)

    foreach ($entry in $Snapshot.PayloadBytes.GetEnumerator()) {
        $destination = Assert-DescendantPath -Candidate (
            Join-Path $snapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        ) -Root $snapshotRoot -Label 'authenticated snapshot payload path'
        [void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($destination))
        [System.IO.File]::WriteAllBytes($destination, $entry.Value)
    }
    foreach ($entry in $PublicSources.InputBytes.GetEnumerator()) {
        if ($Snapshot.PayloadBytes.ContainsKey($entry.Key) -or
            $entry.Key -ceq $manifestRelativePath -or
            $entry.Key -ceq $manifestAnchorRelativePath) {
            throw 'authenticated snapshot public-source path collides with I2 payload'
        }
        $destination = Assert-DescendantPath -Candidate (
            Join-Path $snapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        ) -Root $snapshotRoot -Label 'authenticated snapshot public-source path'
        [void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($destination))
        [System.IO.File]::WriteAllBytes($destination, $entry.Value)
    }
    $snapshotManifest = Assert-DescendantPath -Candidate (
        Join-Path $snapshotRoot ($manifestRelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    ) -Root $snapshotRoot -Label 'authenticated snapshot manifest path'
    [void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($snapshotManifest))
    [System.IO.File]::WriteAllBytes($snapshotManifest, $Snapshot.ManifestBytes)
    $snapshotManifestAnchor = Assert-DescendantPath -Candidate (
        Join-Path $snapshotRoot ($manifestAnchorRelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    ) -Root $snapshotRoot -Label 'authenticated snapshot manifest anchor path'
    [System.IO.File]::WriteAllBytes($snapshotManifestAnchor, $Snapshot.ManifestAnchorBytes)

    foreach ($entry in $Snapshot.PayloadBytes.GetEnumerator()) {
        $destination = Join-Path $snapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        $observed = Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($destination))
        $expected = Get-BytesSha256 -Bytes $entry.Value
        if ($observed -cne $expected) {
            throw 'authenticated snapshot write verification failed'
        }
    }
    foreach ($entry in $PublicSources.InputBytes.GetEnumerator()) {
        $destination = Join-Path $snapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        $observed = Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($destination))
        $expected = Get-BytesSha256 -Bytes $entry.Value
        if ($observed -cne $expected) {
            throw 'authenticated snapshot public-source write verification failed'
        }
    }
    if ((Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($snapshotManifest))) -cne $Snapshot.ManifestSha256) {
        throw 'authenticated snapshot manifest write verification failed'
    }
    if ((Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($snapshotManifestAnchor))) -cne $Snapshot.ManifestAnchorSha256) {
        throw 'authenticated snapshot manifest anchor write verification failed'
    }
    Write-Pass 'pre-execution' 'authenticated-byte-snapshot-created-and-rehashed'
    return $snapshotRoot
}

function Assert-SnapshotStable {
    param(
        [string]$SnapshotRoot,
        [object]$Snapshot,
        [object]$PublicSources
    )

    $expectedFiles = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    [void]$expectedFiles.Add($manifestRelativePath)
    [void]$expectedFiles.Add($manifestAnchorRelativePath)
    foreach ($relative in $Snapshot.PayloadBytes.Keys) {
        [void]$expectedFiles.Add($relative)
    }
    foreach ($relative in $PublicSources.InputBytes.Keys) {
        [void]$expectedFiles.Add($relative)
    }

    $actualFiles = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $directories = [System.Collections.Generic.Stack[string]]::new()
    $directories.Push([System.IO.Path]::GetFullPath($SnapshotRoot))
    while ($directories.Count -gt 0) {
        $current = $directories.Pop()
        foreach ($item in Get-ChildItem -Force -LiteralPath $current) {
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw 'authenticated snapshot gained a reparse-backed path'
            }
            if ($item.PSIsContainer) {
                $directories.Push($item.FullName)
                continue
            }
            $relative = $item.FullName.Substring($SnapshotRoot.Length + 1).Replace('\', '/')
            [void]$actualFiles.Add($relative)
        }
    }
    if (-not $actualFiles.SetEquals($expectedFiles)) {
        throw 'authenticated snapshot exact-file-set stability check failed'
    }
    $snapshotManifestPath = Join-Path $SnapshotRoot ($manifestRelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if ((Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($snapshotManifestPath))) -cne $Snapshot.ManifestSha256) {
        throw 'authenticated snapshot manifest stability check failed'
    }
    $snapshotAnchorPath = Join-Path $SnapshotRoot ($manifestAnchorRelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if ((Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($snapshotAnchorPath))) -cne $Snapshot.ManifestAnchorSha256) {
        throw 'authenticated snapshot manifest anchor stability check failed'
    }
    foreach ($entry in $Snapshot.PayloadBytes.GetEnumerator()) {
        $path = Join-Path $SnapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        $observed = Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($path))
        $expected = Get-BytesSha256 -Bytes $entry.Value
        if ($observed -cne $expected) {
            throw 'authenticated snapshot payload stability check failed'
        }
    }
    foreach ($entry in $PublicSources.InputBytes.GetEnumerator()) {
        $path = Join-Path $SnapshotRoot ($entry.Key.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
        $observed = Get-BytesSha256 -Bytes ([System.IO.File]::ReadAllBytes($path))
        $expected = Get-BytesSha256 -Bytes $entry.Value
        if ($observed -cne $expected) {
            throw 'authenticated snapshot public-source stability check failed'
        }
    }
    Write-Pass 'snapshot-stability' 'no-pycache-extra-file-or-byte-mutation-including-public-sources'
}

$snapshotRoot = $null
$initialSnapshot = $null
$initialPublicSources = $null
try {
    # No candidate Python code is executed before this pure-PowerShell byte
    # authentication and exact-file-set capture completes.
    $initialSnapshot = Get-I2PayloadSnapshot -Phase 'pre-execution-static-integrity'
    $initialPublicSources = Get-PublicSourceSnapshot -ManifestBytes (
        $initialSnapshot.PayloadBytes[$publicSourceManifestRelativePath]
    ) -Phase 'pre-execution-public-source-integrity'
    $snapshotRoot = New-AuthenticatedSnapshot -Snapshot $initialSnapshot -PublicSources $initialPublicSources
    $snapshotImplementationRoot = Join-Path $snapshotRoot 's0-lab\i2\implementation'
    $snapshotTestsRoot = Join-Path $snapshotRoot 's0-lab\i2\tests'
    $snapshotContractPath = Join-Path $snapshotRoot (
        $initialSnapshot.ContractRelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    )

    $env:PYTHONPATH = $snapshotImplementationRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONNOUSERSITE = '1'
    $env:PYTHONHASHSEED = '0'
    $env:PYTHONSAFEPATH = '1'
    Push-Location -LiteralPath $snapshotRoot
    try {
        & python -B -S -P -c "import sys; assert (3, 12) <= sys.version_info[:2] < (4, 0), sys.version"
        if ($LASTEXITCODE -ne 0) {
            throw 'Python runtime compatibility check failed'
        }
        Write-Pass 'runtime' 'Python>=3.12,<4.0; site-disabled; safe-path-enabled'

        $testRunner = @'
import sys
import unittest

suite = unittest.defaultTestLoader.discover('s0-lab/i2/tests', pattern='test_*.py')
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(f'I2_UNIT_TESTS_RUN={result.testsRun}')
print(f'I2_UNIT_TESTS_SKIPPED={len(result.skipped)}')
ok = (
    result.wasSuccessful()
    and result.testsRun > 0
    and not result.skipped
    and not result.expectedFailures
    and not result.unexpectedSuccesses
)
raise SystemExit(0 if ok else 1)
'@
        & python -B -S -P -c $testRunner
        if ($LASTEXITCODE -ne 0) {
            throw 'I2 behavior test suite failed, was empty, or contained non-pass outcomes'
        }
        Write-Pass 'behavior' 'unit-tests-nonempty-all-pass-no-skip-or-expected-failure'
        Write-Output 'UNIT_TESTS=PASS'

        & python -B -S -P -m s0_i2.cli verify --contract $snapshotContractPath
        if ($LASTEXITCODE -ne 0) {
            throw 'I2 public structural CLI verification failed'
        }
        Write-Pass 'behavior' 'public-structural-CLI'
        Write-Output 'CONTRACT_CLI=PASS'

        $importAudit = @'
import ast
import importlib
import pkgutil
import sys
from pathlib import Path

package = importlib.import_module('s0_i2')
package_root = Path(package.__file__).resolve().parent
implementation_root = package_root.parent
expected_implementation_root = Path(sys.argv[1]).resolve()
if implementation_root != expected_implementation_root:
    raise AssertionError('s0_i2 import did not originate from the authenticated snapshot')
for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
    module = importlib.import_module(module_info.name)
    origin = getattr(module, '__file__', None)
    if origin is None or not Path(origin).resolve().is_relative_to(implementation_root):
        raise AssertionError(f'package module escaped authenticated snapshot: {module_info.name}')

forbidden = {
    'ctypes', 'ftplib', 'http', 'multiprocessing', 'openai', 'requests',
    'smtplib', 'socket', 'ssl', 'subprocess', 'urllib', 'winreg',
}
for source in sorted(package_root.rglob('*.py')):
    tree = ast.parse(source.read_bytes(), filename=str(source))
    for node in ast.walk(tree):
        roots = []
        if isinstance(node, ast.Import):
            roots = [alias.name.split('.', 1)[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots = [node.module.split('.', 1)[0]]
        for root in roots:
            if root in forbidden:
                raise AssertionError(f'forbidden implementation import: {root}')
            if root not in sys.stdlib_module_names and root != 's0_i2':
                raise AssertionError(f'non-stdlib implementation import: {root}')
print('I2_IMPORT_AUDIT=PASS_PUBLIC_STDLIB_SNAPSHOT_ONLY')
'@
        & python -B -S -P -c $importAudit $snapshotImplementationRoot
        if ($LASTEXITCODE -ne 0) {
            throw 'I2 authenticated-snapshot import audit failed'
        }
        Write-Pass 'behavior' 'all-package-imports-public-stdlib-snapshot-only'
        Write-Output 'FORBIDDEN_IMPORT_AUDIT=PASS'

        $closedBoundaryAudit = @'
import json
import sys
from pathlib import Path

required_unsupported = {
    'import-admission-exact-grammar',
    'import-outcome-exact-grammar',
    'complete-outcome-classification',
    'durable-ledger',
    'witness-validation',
}
required_forbidden = {
    'key-generation',
    'private-key-custody',
    'signature-generation-or-verification',
    'ledger-or-witness-provider',
    'provider-or-model-session',
    'protected-material',
    'fixture-or-hidden-oracle',
    'e0-or-s0-execution',
}
document = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
if document.get('complete_validation_status') != 'BLOCKED':
    raise AssertionError('complete_validation_status must be exactly BLOCKED')
unsupported = document.get('unsupported_boundaries')
if not isinstance(unsupported, list) or not all(isinstance(value, str) for value in unsupported):
    raise AssertionError('unsupported_boundaries must be a string list')
forbidden = document.get('forbidden_capabilities')
if not isinstance(forbidden, list) or not all(isinstance(value, str) for value in forbidden):
    raise AssertionError('forbidden_capabilities must be a string list')
if required_unsupported.difference(unsupported):
    raise AssertionError('required unsupported boundary declaration is missing')
if required_forbidden.difference(forbidden):
    raise AssertionError('required forbidden capability declaration is missing')
print('I2_COMPLETE_VALIDATION_STATUS=BLOCKED')
print('I2_UNSUPPORTED_BOUNDARIES=AUTHENTICATED_NOT_EXECUTED')
print('I2_FORBIDDEN_CAPABILITIES=AUTHENTICATED_NOT_EXECUTED')
'@
        & python -B -S -P -c $closedBoundaryAudit $snapshotContractPath
        if ($LASTEXITCODE -ne 0) {
            throw 'I2 closed-boundary declaration audit failed'
        }
        Write-Host 'BLOCKED [closed-boundaries] exact admission/outcome/classification and durable ledger/witness validation remain unavailable'
        Write-Host 'BLOCKED [forbidden-capabilities] key/signature/provider/model/protected/oracle/E0/S0 execution was not attempted'
    }
    finally {
        Pop-Location
    }

    Assert-SnapshotStable -SnapshotRoot $snapshotRoot -Snapshot $initialSnapshot -PublicSources $initialPublicSources

    $finalSnapshot = Get-I2PayloadSnapshot -Phase 'post-execution-original-stability'
    if ($finalSnapshot.ManifestSha256 -cne $initialSnapshot.ManifestSha256 -or
        $finalSnapshot.ManifestAnchorSha256 -cne $initialSnapshot.ManifestAnchorSha256 -or
        $finalSnapshot.PayloadFingerprint -cne $initialSnapshot.PayloadFingerprint -or
        $finalSnapshot.RowCount -ne $initialSnapshot.RowCount) {
        throw 'I2 original namespace changed after authenticated-snapshot execution'
    }
    Write-Pass 'post-execution-original-stability' 'manifest-file-set-and-byte-fingerprint-equal-pre-execution'

    $finalPublicSources = Get-PublicSourceSnapshot -ManifestBytes (
        $finalSnapshot.PayloadBytes[$publicSourceManifestRelativePath]
    ) -Phase 'post-execution-public-source-stability'
    if ($finalPublicSources.ManifestSha256 -cne $initialPublicSources.ManifestSha256 -or
        $finalPublicSources.InputFingerprint -cne $initialPublicSources.InputFingerprint -or
        $finalPublicSources.RowCount -ne $initialPublicSources.RowCount) {
        throw 'I2 authenticated public-source inputs changed during verification'
    }
    Write-Pass 'post-execution-public-source-stability' 'manifest-and-exact-12-input-byte-fingerprint-equal-pre-execution'
    Write-Output 'FINAL_STABILITY=PASS'

    Write-Output ("MANIFEST_SHA256={0}" -f $initialSnapshot.ManifestSha256)
    Write-Output ("AUTHENTICATED_PAYLOAD_ROWS={0}" -f $initialSnapshot.RowCount)
    Write-Output 'STATIC_INTEGRITY=PASS'
    Write-Output 'PUBLIC_SOURCE_INPUTS=PASS'
    Write-Output 'MODEL_FREE_BEHAVIOR_TESTS=PASS'
    Write-Output 'CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED'
    Write-Output 'VERIFICATION_SCOPE=PUBLIC_I2_CANDIDATE_ONLY_NO_S0_OR_EFFECT_CLAIM'
}
finally {
    $env:PYTHONPATH = $priorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $priorNoBytecode
    $env:PYTHONNOUSERSITE = $priorNoUserSite
    $env:PYTHONHASHSEED = $priorHashSeed
    $env:PYTHONSAFEPATH = $priorSafePath
    if ($null -ne $snapshotRoot -and (Test-Path -LiteralPath $snapshotRoot)) {
        $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd(
            [System.IO.Path]::DirectorySeparatorChar,
            [System.IO.Path]::AltDirectorySeparatorChar
        )
        $resolvedSnapshot = Assert-DescendantPath -Candidate $snapshotRoot -Root $tempBase -Label 'snapshot cleanup path'
        Remove-Item -LiteralPath $resolvedSnapshot -Recurse -Force
    }
}
