[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..')).Path
$implementationRoot = Join-Path $repoRoot 's0-lab\i1\implementation'
$manifestPath = Join-Path $repoRoot 's0-lab\i1\verification\implementation-files.sha256'
$manifestAnchorPath = Join-Path $repoRoot 's0-lab\i1\verification\implementation-manifest.sha256'
$priorPythonPath = $env:PYTHONPATH
$priorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

try {
    $env:PYTHONPATH = $implementationRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'
    Push-Location -LiteralPath $repoRoot
    try {
        python -c "import sys; assert (3, 12) <= sys.version_info[:2] < (4, 0), sys.version"
        if ($LASTEXITCODE -ne 0) { throw 'Python runtime compatibility check failed' }

        python -c "from importlib.metadata import version; assert version('jsonschema') == '4.26.0'"
        if ($LASTEXITCODE -ne 0) { throw 'Pinned jsonschema version check failed' }

        python -m unittest discover -s s0-lab/i1/tests -v
        if ($LASTEXITCODE -ne 0) { throw 'I1 unittest suite failed' }

        python -m s0_i1.cli verify
        if ($LASTEXITCODE -ne 0) { throw 'I1 structural verification failed' }

        if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
            throw 'I1 implementation manifest is missing'
        }
        if (-not (Test-Path -LiteralPath $manifestAnchorPath -PathType Leaf)) {
            throw 'I1 implementation manifest anchor is missing'
        }
        $anchorBytes = [System.IO.File]::ReadAllBytes($manifestAnchorPath)
        if ($anchorBytes.Length -eq 0 -or $anchorBytes[0] -eq 0xef -or $anchorBytes -contains 0x0d -or ($anchorBytes | Where-Object { $_ -gt 0x7f })) {
            throw 'I1 implementation manifest anchor must be non-empty BOM-free LF-only ASCII'
        }
        $anchorText = [System.Text.Encoding]::ASCII.GetString($anchorBytes)
        if ($anchorText -notmatch '^([0-9a-f]{64})  implementation-files\.sha256\n$') {
            throw 'I1 implementation manifest anchor format mismatch'
        }
        $expectedManifestHash = $Matches[1]
        $actualManifestHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $manifestPath).Hash.ToLowerInvariant()
        if ($actualManifestHash -ne $expectedManifestHash) {
            throw 'I1 implementation manifest anchor hash mismatch'
        }
        $i1Root = (Resolve-Path -LiteralPath (Join-Path $repoRoot 's0-lab\i1')).Path
        $listed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
        foreach ($line in Get-Content -LiteralPath $manifestPath -Encoding utf8) {
            if ($line -notmatch '^([0-9a-f]{64})  (.+)$') {
                throw "Invalid implementation manifest line: $line"
            }
            $expected = $Matches[1]
            $relative = $Matches[2]
            if ($relative.Contains('\') -or $relative.StartsWith('/') -or $relative.Split('/') -contains '..') {
                throw "Unsafe implementation manifest path: $relative"
            }
            if (-not $listed.Add($relative)) {
                throw "Duplicate implementation manifest path: $relative"
            }
            $candidate = [System.IO.Path]::GetFullPath((Join-Path $i1Root $relative))
            if (-not $candidate.StartsWith($i1Root + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
                throw "Implementation manifest path escaped I1: $relative"
            }
            $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $candidate).Hash.ToLowerInvariant()
            if ($actual -ne $expected) {
                throw "Implementation file hash mismatch: $relative"
            }
        }
        if ($listed.Count -ne 26) {
            throw "I1 implementation manifest must contain exactly 26 rows; found $($listed.Count)"
        }
        $disk = Get-ChildItem -Force -File -Recurse -LiteralPath $i1Root |
            Where-Object {
                $_.FullName -ne $manifestPath -and
                $_.FullName -ne $manifestAnchorPath
            } |
            ForEach-Object { $_.FullName.Substring($i1Root.Length + 1).Replace('\', '/') }
        $diskSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
        foreach ($relative in $disk) { [void]$diskSet.Add($relative) }
        if (-not $listed.SetEquals($diskSet)) {
            throw 'I1 implementation manifest file-set mismatch'
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    $env:PYTHONPATH = $priorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $priorNoBytecode
}
