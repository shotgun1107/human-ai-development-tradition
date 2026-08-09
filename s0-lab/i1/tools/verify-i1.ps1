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
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
$i1Root = (Resolve-Path -LiteralPath (Join-Path $repoRoot 's0-lab\i1')).Path
$manifestPath = Join-Path $i1Root 'verification\implementation-files.sha256'
$manifestSidecarPath = Join-Path $i1Root 'verification\implementation-manifest.sha256'
$priorPythonPath = $env:PYTHONPATH
$priorNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)

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

function Assert-TextBytes {
    param(
        [byte[]]$Bytes,
        [string]$Label,
        [string]$Phase,
        [switch]$AsciiOnly
    )
    if ($Bytes.Length -eq 0) {
        throw ("{0} empty check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:non-empty" -f $Label)

    $hasUtf8Bom = $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xef -and $Bytes[1] -eq 0xbb -and $Bytes[2] -eq 0xbf
    if ($hasUtf8Bom) {
        throw ("{0} BOM check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:BOM(EF-BB-BF)" -f $Label)

    try {
        $text = $strictUtf8.GetString($Bytes)
    }
    catch {
        throw ("{0} UTF-8 check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:UTF-8" -f $Label)

    if ($Bytes -contains 0x0d) {
        throw ("{0} LF-only check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:LF-only" -f $Label)

    if ($Bytes[$Bytes.Length - 1] -ne 0x0a) {
        throw ("{0} final-LF check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:final-LF" -f $Label)

    if ($text -match '(?m)[ \t]+$') {
        throw ("{0} trailing-whitespace check failed" -f $Label)
    }
    Write-Pass $Phase ("{0}:trailing-whitespace" -f $Label)

    if ($AsciiOnly -and ($Bytes | Where-Object { $_ -gt 0x7f })) {
        throw ("{0} ASCII check failed" -f $Label)
    }
    if ($AsciiOnly) {
        Write-Pass $Phase ("{0}:ASCII" -f $Label)
    }
    return $text
}

function Get-I1PayloadSnapshot {
    param([string]$Phase)

    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
        throw 'I1 implementation payload manifest is missing'
    }
    $manifestBytes = [System.IO.File]::ReadAllBytes($manifestPath)
    $actualManifestHash = Get-BytesSha256 -Bytes $manifestBytes
    if ($actualManifestHash -cne $ExpectedManifestSha256) {
        throw ("external expected-manifest check failed: expected {0}, observed {1}" -f $ExpectedManifestSha256, $actualManifestHash)
    }
    Write-Pass $Phase 'external-expected-manifest-sha256'

    $manifestText = Assert-TextBytes -Bytes $manifestBytes -Label 'payload-manifest' -Phase $Phase -AsciiOnly

    if (-not (Test-Path -LiteralPath $manifestSidecarPath -PathType Leaf)) {
        throw 'I1 implementation manifest sidecar is missing'
    }
    $sidecarBytes = [System.IO.File]::ReadAllBytes($manifestSidecarPath)
    $sidecarText = Assert-TextBytes -Bytes $sidecarBytes -Label 'manifest-sidecar' -Phase $Phase -AsciiOnly
    if ($sidecarText -cnotmatch '^([0-9a-f]{64})  implementation-files\.sha256\n$') {
        throw 'manifest sidecar-format check failed'
    }
    Write-Pass $Phase 'manifest-sidecar:format'
    if ($Matches[1] -cne $ExpectedManifestSha256) {
        throw 'manifest sidecar corroboration check failed'
    }
    Write-Pass $Phase 'manifest-sidecar:corroborates-external-anchor'

    $listed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $observedRows = [System.Collections.Generic.List[string]]::new()
    $payloadBytes = [System.Collections.Generic.Dictionary[string,byte[]]]::new([System.StringComparer]::Ordinal)
    $manifestLines = $manifestText.Substring(0, $manifestText.Length - 1).Split("`n")
    foreach ($line in $manifestLines) {
        if ($line -cnotmatch '^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$') {
            throw ("implementation manifest row-format check failed: {0}" -f $line)
        }
        $expected = $Matches[1]
        $relative = $Matches[2]
        $parts = $relative.Split('/')
        if ($relative.Contains('\') -or $relative.StartsWith('/') -or
            $parts -contains '' -or $parts -contains '.' -or $parts -contains '..' -or
            $relative.Contains(':')) {
            throw ("unsafe implementation manifest path: {0}" -f $relative)
        }
        if (-not $listed.Add($relative)) {
            throw ("duplicate implementation manifest path: {0}" -f $relative)
        }
        $candidate = [System.IO.Path]::GetFullPath((Join-Path $i1Root $relative))
        if (-not $candidate.StartsWith($i1Root + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw ("implementation manifest path escaped I1: {0}" -f $relative)
        }
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            throw ("implementation manifest file missing: {0}" -f $relative)
        }
        $item = Get-Item -Force -LiteralPath $candidate
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw ("implementation manifest file is reparse-backed: {0}" -f $relative)
        }
        $candidateBytes = [System.IO.File]::ReadAllBytes($candidate)
        $actual = Get-BytesSha256 -Bytes $candidateBytes
        if ($actual -cne $expected) {
            throw ("implementation file hash mismatch: {0}" -f $relative)
        }
        $payloadBytes.Add($relative, $candidateBytes)
        $observedRows.Add(("{0}  {1}" -f $actual, $relative))
    }
    Write-Pass $Phase 'payload-manifest:row-format-paths-hashes'

    if ($listed.Count -ne 26) {
        throw ("I1 implementation manifest must contain exactly 26 rows; found {0}" -f $listed.Count)
    }
    Write-Pass $Phase 'payload-manifest:exact-26-row-count'

    $reparseDirectory = Get-ChildItem -Force -Directory -Recurse -LiteralPath $i1Root |
        Where-Object { ($_.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 } |
        Select-Object -First 1
    if ($null -ne $reparseDirectory) {
        throw 'I1 namespace contains a reparse-backed directory'
    }
    $disk = Get-ChildItem -Force -File -Recurse -LiteralPath $i1Root |
        Where-Object {
            $_.FullName -ne $manifestPath -and
            $_.FullName -ne $manifestSidecarPath
        } |
        ForEach-Object { $_.FullName.Substring($i1Root.Length + 1).Replace('\', '/') }
    $diskSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($relative in $disk) { [void]$diskSet.Add($relative) }
    if (-not $listed.SetEquals($diskSet)) {
        throw 'I1 implementation manifest exact-file-set check failed'
    }
    Write-Pass $Phase 'payload-manifest:forced-hidden-exact-file-set'

    $fingerprintInput = (@($actualManifestHash) + @($observedRows | Sort-Object)) -join "`n"
    $fingerprintBytes = [System.Text.Encoding]::ASCII.GetBytes($fingerprintInput + "`n")
    $fingerprint = Get-BytesSha256 -Bytes $fingerprintBytes
    return [PSCustomObject]@{
        ManifestSha256 = $actualManifestHash
        PayloadFingerprint = $fingerprint
        RowCount = $listed.Count
        ManifestBytes = $manifestBytes
        SidecarBytes = $sidecarBytes
        PayloadBytes = $payloadBytes
    }
}

function New-AuthenticatedSnapshot {
    param([object]$Snapshot)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    $snapshotRoot = [System.IO.Path]::Combine(
        $tempBase,
        's0-i1-public-verify-' + [System.Guid]::NewGuid().ToString('N')
    )
    $snapshotRoot = [System.IO.Path]::GetFullPath($snapshotRoot)
    if (-not $snapshotRoot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or
        $snapshotRoot -eq $tempBase) {
        throw 'authenticated snapshot path escaped the temporary directory'
    }
    [void][System.IO.Directory]::CreateDirectory($snapshotRoot)
    foreach ($entry in $Snapshot.PayloadBytes.GetEnumerator()) {
        $destination = [System.IO.Path]::GetFullPath((Join-Path (Join-Path $snapshotRoot 's0-lab\i1') $entry.Key))
        $snapshotI1 = [System.IO.Path]::GetFullPath((Join-Path $snapshotRoot 's0-lab\i1'))
        if (-not $destination.StartsWith($snapshotI1 + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw 'authenticated snapshot payload path escaped I1'
        }
        [void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($destination))
        [System.IO.File]::WriteAllBytes($destination, $entry.Value)
    }
    $snapshotVerification = Join-Path $snapshotRoot 's0-lab\i1\verification'
    [void][System.IO.Directory]::CreateDirectory($snapshotVerification)
    [System.IO.File]::WriteAllBytes(
        (Join-Path $snapshotVerification 'implementation-files.sha256'),
        $Snapshot.ManifestBytes
    )
    [System.IO.File]::WriteAllBytes(
        (Join-Path $snapshotVerification 'implementation-manifest.sha256'),
        $Snapshot.SidecarBytes
    )
    Write-Pass 'pre-execution' 'authenticated-byte-snapshot-created'
    return $snapshotRoot
}

$snapshotRoot = $null
try {
    # This pure-PowerShell authentication completes before PYTHONPATH is set or
    # any candidate Python module, test, or CLI can execute.
    $initialSnapshot = Get-I1PayloadSnapshot -Phase 'pre-execution'
    $snapshotRoot = New-AuthenticatedSnapshot -Snapshot $initialSnapshot
    $snapshotImplementationRoot = Join-Path $snapshotRoot 's0-lab\i1\implementation'

    $env:PYTHONPATH = $snapshotImplementationRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location -LiteralPath $snapshotRoot
    try {
        python -c "import sys; assert (3, 12) <= sys.version_info[:2] < (4, 0), sys.version"
        if ($LASTEXITCODE -ne 0) { throw 'Python runtime compatibility check failed' }

        python -c "from importlib.metadata import version; assert version('jsonschema') == '4.26.0'"
        if ($LASTEXITCODE -ne 0) { throw 'Pinned jsonschema version check failed' }

        python -m unittest discover -s s0-lab/i1/tests -v
        if ($LASTEXITCODE -ne 0) { throw 'I1 unittest suite failed' }

        python -m s0_i1.cli verify
        if ($LASTEXITCODE -ne 0) { throw 'I1 structural verification failed' }
    }
    finally {
        Pop-Location
    }

    $finalSnapshot = Get-I1PayloadSnapshot -Phase 'final-stability'
    if ($finalSnapshot.ManifestSha256 -cne $initialSnapshot.ManifestSha256 -or
        $finalSnapshot.PayloadFingerprint -cne $initialSnapshot.PayloadFingerprint -or
        $finalSnapshot.RowCount -ne $initialSnapshot.RowCount) {
        throw 'I1 final snapshot equality check failed'
    }
    Write-Pass 'final-stability' 'snapshot-equals-pre-execution'
}
finally {
    $env:PYTHONPATH = $priorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $priorNoBytecode
    if ($null -ne $snapshotRoot -and (Test-Path -LiteralPath $snapshotRoot)) {
        $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
        $resolvedSnapshot = [System.IO.Path]::GetFullPath($snapshotRoot)
        if (-not $resolvedSnapshot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or
            $resolvedSnapshot -eq $tempBase) {
            throw 'refusing to remove an unsafe authenticated snapshot path'
        }
        Remove-Item -LiteralPath $resolvedSnapshot -Recurse -Force
    }
}
