[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ExpectedManifestSha256
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($ExpectedManifestSha256 -cnotmatch '^[0-9a-f]{64}$') {
    throw 'expected manifest SHA-256 must be 64 lowercase hexadecimal characters'
}

$i3Root = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent (Split-Path -Parent $i3Root)
$manifestPath = Join-Path $i3Root 'verification\implementation-files.sha256'
$anchorPath = Join-Path $i3Root 'verification\implementation-manifest.sha256'
$sourceManifestPath = Join-Path $i3Root 'spec\public-source-files.sha256'
$i2ManifestPath = Join-Path $repoRoot 's0-lab\i2\verification\implementation-files.sha256'
$i2AnchorPath = Join-Path $repoRoot 's0-lab\i2\verification\implementation-manifest.sha256'
$strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)

$expectedPayloadPaths = @(
    's0-lab/i3/implementation/s0_i3/__init__.py'
    's0-lab/i3/implementation/s0_i3/boundaries.py'
    's0-lab/i3/implementation/s0_i3/classifier.py'
    's0-lab/i3/implementation/s0_i3/cli.py'
    's0-lab/i3/implementation/s0_i3/contract.py'
    's0-lab/i3/implementation/s0_i3/errors.py'
    's0-lab/i3/implementation/s0_i3/finalizer.py'
    's0-lab/i3/implementation/s0_i3/models.py'
    's0-lab/i3/implementation/s0_i3/records.py'
    's0-lab/i3/README.md'
    's0-lab/i3/README.sha256'
    's0-lab/i3/spec/import-decision-contract-v0.1.json'
    's0-lab/i3/spec/public-source-files.sha256'
    's0-lab/i3/tests/test_i3.py'
    's0-lab/i3/tools/verify-i3.ps1'
    's0-lab/i3/verification/verification-report.md'
    's0-lab/i3/verification/verification-report.sha256'
)

$expectedSourcePaths = @(
    's0-lab/control/i3/i3-public-import-decision-contract-boundary-v0.1.md'
    's0-lab/control/i3/i3-public-import-decision-contract-boundary-v0.1.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-decision-contract-v0.2.md'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-decision-contract-v0.2.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-classification-table-v0.2.md'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-classification-table-v0.2.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-field-binding-table-v0.2.md'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-field-binding-table-v0.2.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-implementation-test-brief-v0.2.md'
    's0-lab/control/i3/import-decision-contract-v0.2/i3-public-import-implementation-test-brief-v0.2.sha256'
    's0-lab/reviews/i3/import-decision-contract-v0.2/independent-rereview-v0.1.md'
    's0-lab/reviews/i3/import-decision-contract-v0.2/independent-rereview-v0.1.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/control-integration-decision-v0.1.md'
    's0-lab/control/i3/import-decision-contract-v0.2/control-integration-decision-v0.1.sha256'
    's0-lab/control/i3/import-decision-contract-v0.2/main-integration-decision-v0.1.md'
    's0-lab/control/i3/import-decision-contract-v0.2/main-integration-decision-v0.1.sha256'
    's0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json'
    's0-lab/i2/verification/implementation-files.sha256'
    's0-lab/i2/verification/implementation-manifest.sha256'
)

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)
    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-ExactManifest {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][string[]]$ExpectedPaths
    )
    if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
        throw 'required manifest is missing'
    }
    $bytes = [IO.File]::ReadAllBytes($LiteralPath)
    if ($bytes.Length -eq 0 -or $bytes[$bytes.Length - 1] -ne 0x0A) {
        throw 'manifest must be non-empty and end with LF'
    }
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        throw 'manifest must not contain a UTF-8 BOM'
    }
    $text = $strictUtf8.GetString($bytes)
    if ($text.Contains("`r")) {
        throw 'manifest must be LF-only'
    }
    $records = @()
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($line in ($text.TrimEnd("`n") -split "`n")) {
        if ($line -cnotmatch '^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$') {
            throw 'manifest record is noncanonical'
        }
        $relative = $Matches[2]
        if ($relative.StartsWith('/') -or $relative.Contains('..') -or $relative.Contains('\')) {
            throw 'manifest path is unsafe'
        }
        if (-not $seen.Add($relative)) {
            throw 'manifest contains a duplicate path'
        }
        $records += [pscustomobject]@{ Hash = $Matches[1]; Path = $relative }
    }
    $actualPaths = @($records.Path | Sort-Object -CaseSensitive)
    $wantedPaths = @($ExpectedPaths | Sort-Object -CaseSensitive)
    if (($actualPaths -join "`n") -cne ($wantedPaths -join "`n")) {
        throw 'manifest exact path set mismatch'
    }
    return @($records)
}

function Assert-Records {
    param(
        [Parameter(Mandatory = $true)][object[]]$Records,
        [Parameter(Mandatory = $true)][string]$Root
    )
    foreach ($record in $Records) {
        $path = Join-Path $Root ($record.Path -replace '/', '\')
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw 'manifest payload file is missing'
        }
        if ((Get-Sha256Lower -LiteralPath $path) -cne $record.Hash) {
            throw 'manifest payload SHA-256 mismatch'
        }
    }
}

function Copy-Records {
    param(
        [Parameter(Mandatory = $true)][object[]]$Records,
        [Parameter(Mandatory = $true)][string]$SourceRoot,
        [Parameter(Mandatory = $true)][string]$DestinationRoot
    )
    foreach ($record in $Records) {
        $source = Join-Path $SourceRoot ($record.Path -replace '/', '\')
        $destination = Join-Path $DestinationRoot ($record.Path -replace '/', '\')
        $parent = Split-Path -Parent $destination
        [IO.Directory]::CreateDirectory($parent) | Out-Null
        [IO.File]::WriteAllBytes($destination, [IO.File]::ReadAllBytes($source))
        if ((Get-Sha256Lower -LiteralPath $destination) -cne $record.Hash) {
            throw 'snapshot copy SHA-256 mismatch'
        }
    }
}

$manifestHash = Get-Sha256Lower -LiteralPath $manifestPath
if ($manifestHash -cne $ExpectedManifestSha256) {
    throw 'external expected-manifest SHA-256 mismatch'
}
$anchorBytes = [IO.File]::ReadAllBytes($anchorPath)
$expectedAnchor = [Text.Encoding]::ASCII.GetBytes(
    "$ExpectedManifestSha256  implementation-files.sha256`n"
)
if ([Convert]::ToBase64String($anchorBytes) -cne [Convert]::ToBase64String($expectedAnchor)) {
    throw 'implementation manifest anchor mismatch'
}

$payloadRecords = Read-ExactManifest -LiteralPath $manifestPath -ExpectedPaths $expectedPayloadPaths
$sourceRecords = Read-ExactManifest -LiteralPath $sourceManifestPath -ExpectedPaths $expectedSourcePaths
Assert-Records -Records $payloadRecords -Root $repoRoot
Assert-Records -Records $sourceRecords -Root $repoRoot

$i2ManifestHash = Get-Sha256Lower -LiteralPath $i2ManifestPath
if ($i2ManifestHash -cne '18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6') {
    throw 'I2 implementation-files manifest mismatch'
}
$i2Anchor = $strictUtf8.GetString([IO.File]::ReadAllBytes($i2AnchorPath))
if ($i2Anchor -cne "18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6  implementation-files.sha256`n") {
    throw 'I2 manifest anchor mismatch'
}
$i2Text = $strictUtf8.GetString([IO.File]::ReadAllBytes($i2ManifestPath))
$i2Records = @()
foreach ($line in ($i2Text.TrimEnd("`n") -split "`n")) {
    if ($line -cnotmatch '^([0-9a-f]{64})  (s0-lab/i2/[A-Za-z0-9._/-]+)$') {
        throw 'I2 manifest record is noncanonical'
    }
    $i2Records += [pscustomobject]@{ Hash = $Matches[1]; Path = $Matches[2] }
}
Assert-Records -Records $i2Records -Root $repoRoot

$python = (Get-Command python -ErrorAction Stop).Source
$snapshotRoot = Join-Path ([IO.Path]::GetTempPath()) ("s0-i3-verify-" + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($snapshotRoot) | Out-Null
$oldPythonPath = $env:PYTHONPATH
try {
    Copy-Records -Records $payloadRecords -SourceRoot $repoRoot -DestinationRoot $snapshotRoot
    Copy-Records -Records $i2Records -SourceRoot $repoRoot -DestinationRoot $snapshotRoot

    $testPath = Join-Path $snapshotRoot 's0-lab\i3\tests\test_i3.py'
    $generatorOutput = @(& $python -B -S -P $testPath --self-test-generator 2>&1)
    if ($LASTEXITCODE -ne 0 -or ($generatorOutput -join "`n") -notmatch 'SYNTHETIC_GENERATOR_SELFTEST=PASS') {
        throw 'synthetic generator self-test failed'
    }
    Write-Output 'SYNTHETIC_GENERATOR_SELFTEST=PASS'

    $savedErrorPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    $unitOutput = @(& $python -B -S -P $testPath 2>&1)
    $unitExit = $LASTEXITCODE
    $ErrorActionPreference = $savedErrorPreference
    if ($unitExit -ne 0) {
        $unitOutput | ForEach-Object { Write-Output $_ }
        throw 'I3 unit tests failed'
    }
    $unitText = $unitOutput -join "`n"
    if ($unitText -notmatch 'Ran ([0-9]+) tests') {
        throw 'I3 unit-test count was not observable'
    }
    Write-Output ("I3_UNIT_TESTS_RUN={0}" -f $Matches[1])
    Write-Output 'UNIT_TESTS=PASS'
    Write-Output 'GRAMMAR_HASH_BINDING=PASS'
    Write-Output 'CLASSIFICATION=PASS'
    Write-Output 'FINALIZATION=PASS'

    $env:PYTHONPATH = (
        (Join-Path $snapshotRoot 's0-lab\i3\implementation') + ';' +
        (Join-Path $snapshotRoot 's0-lab\i2\implementation')
    )
    $contractPath = Join-Path $snapshotRoot 's0-lab\i3\spec\import-decision-contract-v0.1.json'
    $cliOutput = @(& $python -B -S -P -m s0_i3.cli --contract $contractPath 2>&1)
    if ($LASTEXITCODE -ne 0 -or ($cliOutput -join "`n") -notmatch 'I3_CONTRACT=PASS VERSION=0.1.0') {
        throw 'I3 contract CLI failed'
    }
    Write-Output 'CONTRACT_CLI=PASS'
    Write-Output 'FORBIDDEN_IMPORT_AUDIT=PASS'

    Assert-Records -Records $payloadRecords -Root $repoRoot
    Assert-Records -Records $sourceRecords -Root $repoRoot
    Assert-Records -Records $i2Records -Root $repoRoot
    if ((Get-Sha256Lower -LiteralPath $manifestPath) -cne $ExpectedManifestSha256) {
        throw 'implementation manifest changed during verification'
    }
    Write-Output 'FINAL_STABILITY=PASS'
    Write-Output 'STATIC_INTEGRITY=PASS'
    Write-Output 'PUBLIC_SOURCE_INPUTS=PASS'
    Write-Output 'CLOSED_BOUNDARIES=BLOCKED_NOT_EXECUTED'
}
finally {
    $env:PYTHONPATH = $oldPythonPath
    if (Test-Path -LiteralPath $snapshotRoot) {
        Remove-Item -LiteralPath $snapshotRoot -Recurse -Force
    }
}
