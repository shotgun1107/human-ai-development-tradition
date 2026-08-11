[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-f]{64}$')]
    [string]$ExpectedManifestSha256
)

$ErrorActionPreference = 'Stop'
$scriptPath = [System.IO.Path]::GetFullPath($MyInvocation.MyCommand.Path)
$i2Root = [System.IO.Path]::GetFullPath((Join-Path (Split-Path $scriptPath -Parent) '..'))
$repositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $i2Root '..\..'))
$manifestPath = [System.IO.Path]::GetFullPath(
    (Join-Path $i2Root 'verification\implementation-files.sha256')
)

function Get-LowerSha256([string]$LiteralPath) {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $LiteralPath).Hash.ToLowerInvariant()
}

if ((Get-LowerSha256 $manifestPath) -cne $ExpectedManifestSha256) {
    throw 'I2 implementation manifest external-anchor mismatch'
}

$manifestBytes = [System.IO.File]::ReadAllBytes($manifestPath)
if ($manifestBytes.Length -eq 0 -or $manifestBytes[-1] -ne 10) {
    throw 'I2 manifest must be non-empty and end with LF'
}
if ($manifestBytes -contains 13) {
    throw 'I2 manifest must be LF-only'
}
$manifestText = [System.Text.UTF8Encoding]::new($false, $true).GetString($manifestBytes)
$records = $manifestText.TrimEnd("`n").Split("`n")
$seen = @{}
foreach ($record in $records) {
    if ($record -cnotmatch '^([0-9a-f]{64})  (s0-lab/i2/[a-zA-Z0-9._/-]+)$') {
        throw 'I2 manifest record is noncanonical'
    }
    $expectedHash = $Matches[1]
    $relativePath = $Matches[2]
    if ($seen.ContainsKey($relativePath)) {
        throw 'I2 manifest contains a duplicate path'
    }
    $seen[$relativePath] = $true
    $candidate = [System.IO.Path]::GetFullPath(
        (Join-Path $repositoryRoot ($relativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)))
    )
    $requiredPrefix = $i2Root.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    if (-not $candidate.StartsWith($requiredPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw 'I2 manifest path escaped its public directory'
    }
    if (-not [System.IO.File]::Exists($candidate)) {
        throw 'I2 manifest payload is missing'
    }
    if ((Get-LowerSha256 $candidate) -cne $expectedHash) {
        throw 'I2 manifest payload hash mismatch'
    }
}

$priorPythonPath = $env:PYTHONPATH
$priorNoBytecode = $env:PYTHONDONTWRITEBYTECODE
try {
    $env:PYTHONPATH = Join-Path $i2Root 'implementation'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $contractPath = Join-Path $i2Root 'spec\trust-root-role-isolation-contract-v0.1.json'
    & python -B -m s0_i2.cli verify --contract $contractPath
    if ($LASTEXITCODE -ne 0) {
        throw 'I2 contract verification failed'
    }
    & python -B -c "from pathlib import Path; [compile(p.read_bytes(), str(p), 'exec') for p in Path(r'$i2Root').joinpath('implementation','s0_i2').glob('*.py')]; print('SYNTAX=PASS')"
    if ($LASTEXITCODE -ne 0) {
        throw 'I2 syntax verification failed'
    }
}
finally {
    $env:PYTHONPATH = $priorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $priorNoBytecode
}

Write-Output "MANIFEST_SHA256=$ExpectedManifestSha256"
Write-Output 'PAYLOAD_HASHES=PASS'
Write-Output 'UNIT_TESTS=NOT_RUN_GATE_CLOSED'
Write-Output 'I2_PUBLIC_IMPLEMENTATION_CANDIDATE=PASS'
