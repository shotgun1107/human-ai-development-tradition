[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$BaseRuntimeRoot,
    [Parameter(Mandatory = $true)][string]$BaseManifestPath,
    [Parameter(Mandatory = $true)][string]$OverlayRoot,
    [Parameter(Mandatory = $true)][string]$OverlayManifestPath,
    [Parameter(Mandatory = $true)][string]$OverlayManifestSha256,
    [Parameter(Mandatory = $true)][string]$OverlayContractPath,
    [Parameter(Mandatory = $true)][string]$OverlayContractSha256,
    [Parameter(Mandatory = $true)][string]$OutputRoot,
    [Parameter(Mandatory = $true)][string]$FinalManifestPath
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$baseManifestSha256 = '8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798'
$baseFileCount = 174
$baseTotalBytes = 24138847L
$baseEvidenceHashes = [ordered]@{
    'evidence/payload-manifest.json' = '8e151f7ad7d1bd71b8e7375fce28b86e6b614814e7702a40baf1c6e7a0d95798'
    'evidence/prepublication-record.json' = '0281893dce01d1aa54a1ad16cd621786615340844fcec35940095768e7dda9ca'
    'evidence/runtime-record.json' = '5d6b61194b5a7f0e53aeb78ac0bdee40f6edea294adecb0f8a7462751f6e6a84'
    'evidence/status.json' = 'c8878e9df9d8c5979517efa3a9495b8e65c640b6f2c195fff029def6c262bbc6'
}
$shaPattern = '^[0-9a-f]{64}$'
$pathPattern = '^[A-Za-z0-9._/-]+$'

function Require-Absolute([string]$Path, [string]$Label) {
    if ($Path -notmatch '^[A-Za-z]:\\' -or $Path.IndexOf([char]0) -ge 0) {
        throw "$Label must be one absolute drive path"
    }
    return [IO.Path]::GetFullPath($Path)
}

function Require-Directory([string]$Path, [string]$Label) {
    $full = Require-Absolute $Path $Label
    $item = Get-Item -LiteralPath $full -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "$Label must be one non-reparse directory"
    }
    return $item.FullName
}

function Require-File([string]$Path, [string]$Label) {
    $full = Require-Absolute $Path $Label
    $item = Get-Item -LiteralPath $full -Force
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "$Label must be one non-reparse file"
    }
    return $item.FullName
}

function Test-AtOrUnder([string]$Candidate, [string]$Root) {
    $candidateFull = [IO.Path]::GetFullPath($Candidate).TrimEnd([IO.Path]::DirectorySeparatorChar)
    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar)
    return [StringComparer]::OrdinalIgnoreCase.Equals($candidateFull, $rootFull) -or
           $candidateFull.StartsWith($rootFull + [IO.Path]::DirectorySeparatorChar,
                                     [StringComparison]::OrdinalIgnoreCase)
}

function Require-SafeVirtualPath([string]$Path) {
    if ($Path -notmatch $pathPattern -or $Path.StartsWith('/') -or $Path.EndsWith('/') -or
        $Path.Contains('//') -or $Path.Contains('\') -or $Path.Contains(':')) {
        throw 'manifest virtual path is not canonical'
    }
    foreach ($part in $Path.Split('/')) {
        if ($part -in @('', '.', '..') -or $part.EndsWith('.') -or $part.EndsWith(' ')) {
            throw 'manifest virtual path segment is not canonical'
        }
    }
    return $Path
}

function Read-Manifest([string]$Path, [string]$ExpectedSha256, [int]$ExpectedRows) {
    if ($ExpectedSha256 -notmatch $shaPattern) { throw 'manifest pin is malformed' }
    $raw = [IO.File]::ReadAllBytes((Require-File $Path 'manifest'))
    if ($raw.Length -eq 0 -or $raw[-1] -ne 10 -or $raw -contains 13 -or
        (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedSha256) {
        throw 'manifest bytes or pin differ'
    }
    $text = [Text.UTF8Encoding]::new($false, $true).GetString($raw)
    $lines = @($text.Substring(0, $text.Length - 1).Split("`n"))
    if ($ExpectedRows -ge 0 -and $lines.Count -ne $ExpectedRows) { throw 'manifest row count differs' }
    $rows = [ordered]@{}
    $previous = $null
    foreach ($line in $lines) {
        if ($line -notmatch '^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$') { throw 'manifest row syntax differs' }
        $digest = $Matches[1]
        $virtualPath = Require-SafeVirtualPath $Matches[2]
        if ($null -ne $previous -and [StringComparer]::Ordinal.Compare($virtualPath, $previous) -le 0) {
            throw 'manifest rows are not unique ASCII-sorted paths'
        }
        $rows.Add($virtualPath, $digest)
        $previous = $virtualPath
    }
    return $rows
}

function Assert-NoDuplicateJsonObjectKeys([string]$Text) {
    $script:s0JsonText = $Text
    $script:s0JsonIndex = 0

    function Read-S0JsonString {
        if ($script:s0JsonIndex -ge $script:s0JsonText.Length -or
            $script:s0JsonText[$script:s0JsonIndex] -ne '"') { throw 'JSON string is absent' }
        $start = $script:s0JsonIndex
        $script:s0JsonIndex++
        while ($script:s0JsonIndex -lt $script:s0JsonText.Length) {
            $character = $script:s0JsonText[$script:s0JsonIndex]
            $script:s0JsonIndex++
            if ($character -eq '"') {
                $token = $script:s0JsonText.Substring($start, $script:s0JsonIndex - $start)
                return ($token | ConvertFrom-Json)
            }
            if ([int][char]$character -lt 0x20) { throw 'JSON string contains a control character' }
            if ($character -eq '\') {
                if ($script:s0JsonIndex -ge $script:s0JsonText.Length) { throw 'JSON escape is partial' }
                $escape = $script:s0JsonText[$script:s0JsonIndex]
                $script:s0JsonIndex++
                if ('"\/bfnrt'.IndexOf($escape) -lt 0) { throw 'JSON escape differs' }
                if ($escape -eq 'u') {
                    if ($script:s0JsonIndex + 4 -gt $script:s0JsonText.Length) { throw 'JSON unicode escape is partial' }
                    $hex = $script:s0JsonText.Substring($script:s0JsonIndex, 4)
                    if ($hex -notmatch '^[0-9A-Fa-f]{4}$') { throw 'JSON unicode escape differs' }
                    $script:s0JsonIndex += 4
                }
            }
        }
        throw 'JSON string is unterminated'
    }

    function Read-S0JsonNumber {
        $start = $script:s0JsonIndex
        while ($script:s0JsonIndex -lt $script:s0JsonText.Length -and
               '-+0123456789.eE'.IndexOf($script:s0JsonText[$script:s0JsonIndex]) -ge 0) {
            $script:s0JsonIndex++
        }
        $token = $script:s0JsonText.Substring($start, $script:s0JsonIndex - $start)
        if ($token -notmatch '^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$') {
            throw 'JSON number differs'
        }
    }

    function Read-S0JsonValue {
        if ($script:s0JsonIndex -ge $script:s0JsonText.Length) { throw 'JSON value is absent' }
        $character = $script:s0JsonText[$script:s0JsonIndex]
        if ($character -eq '{') { Read-S0JsonObject; return }
        if ($character -eq '[') { Read-S0JsonArray; return }
        if ($character -eq '"') { [void](Read-S0JsonString); return }
        if ($character -eq '-' -or [char]::IsDigit($character)) { Read-S0JsonNumber; return }
        foreach ($literal in @('true', 'false', 'null')) {
            if ($script:s0JsonText.Substring($script:s0JsonIndex).StartsWith($literal, [StringComparison]::Ordinal)) {
                $script:s0JsonIndex += $literal.Length
                return
            }
        }
        throw 'JSON value token differs'
    }

    function Read-S0JsonObject {
        $script:s0JsonIndex++
        $keys = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        if ($script:s0JsonIndex -lt $script:s0JsonText.Length -and
            $script:s0JsonText[$script:s0JsonIndex] -eq '}') { $script:s0JsonIndex++; return }
        while ($true) {
            $key = Read-S0JsonString
            if (-not $keys.Add($key)) { throw 'JSON object contains a duplicate key' }
            if ($script:s0JsonIndex -ge $script:s0JsonText.Length -or
                $script:s0JsonText[$script:s0JsonIndex] -ne ':') { throw 'JSON object colon differs' }
            $script:s0JsonIndex++
            Read-S0JsonValue
            if ($script:s0JsonIndex -ge $script:s0JsonText.Length) { throw 'JSON object is partial' }
            $separator = $script:s0JsonText[$script:s0JsonIndex]
            $script:s0JsonIndex++
            if ($separator -eq '}') { return }
            if ($separator -ne ',') { throw 'JSON object separator differs' }
        }
    }

    function Read-S0JsonArray {
        $script:s0JsonIndex++
        if ($script:s0JsonIndex -lt $script:s0JsonText.Length -and
            $script:s0JsonText[$script:s0JsonIndex] -eq ']') { $script:s0JsonIndex++; return }
        while ($true) {
            Read-S0JsonValue
            if ($script:s0JsonIndex -ge $script:s0JsonText.Length) { throw 'JSON array is partial' }
            $separator = $script:s0JsonText[$script:s0JsonIndex]
            $script:s0JsonIndex++
            if ($separator -eq ']') { return }
            if ($separator -ne ',') { throw 'JSON array separator differs' }
        }
    }

    Read-S0JsonValue
    if ($script:s0JsonIndex -ne $script:s0JsonText.Length) { throw 'JSON has trailing bytes or whitespace' }
}

function Read-BasePayloadManifest([string]$Path) {
    $manifest = Require-File $Path 'base payload manifest'
    $raw = [IO.File]::ReadAllBytes($manifest)
    if ($raw.Length -eq 0 -or $raw[-1] -ne 10 -or $raw -contains 13 -or
        (Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $baseManifestSha256) {
        throw 'base payload manifest bytes or pin differ'
    }
    $text = [Text.UTF8Encoding]::new($false, $true).GetString($raw)
    $body = $text.Substring(0, $text.Length - 1)
    Assert-NoDuplicateJsonObjectKeys $body
    $value = $body | ConvertFrom-Json
    $topFields = @($value.PSObject.Properties.Name | Sort-Object)
    if ((Compare-Object @('file_count', 'files', 'python_stdlib_zip', 'schema_id', 'total_bytes') $topFields) -or
        $value.schema_id -ne 'S0-PUBLIC-BRM-V0.7-PAYLOAD-MANIFEST-1' -or
        $value.file_count -isnot [int64] -or $value.file_count -ne $baseFileCount -or
        $value.total_bytes -isnot [int64] -or $value.total_bytes -ne $baseTotalBytes -or
        $value.files -isnot [array] -or $value.files.Count -ne $baseFileCount) {
        throw 'base payload manifest top-level contract differs'
    }
    $stdlibFields = @($value.python_stdlib_zip.PSObject.Properties.Name | Sort-Object)
    if ((Compare-Object @('entry_count', 'uncompressed_bytes') $stdlibFields) -or
        $value.python_stdlib_zip.entry_count -isnot [int64] -or
        $value.python_stdlib_zip.entry_count -le 0 -or
        $value.python_stdlib_zip.uncompressed_bytes -isnot [int64] -or
        $value.python_stdlib_zip.uncompressed_bytes -le 0) {
        throw 'base stdlib inventory contract differs'
    }
    $rows = [ordered]@{}
    $sizes = [ordered]@{}
    $previous = $null
    $caseKeys = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    $total = 0L
    foreach ($row in $value.files) {
        $rowFields = @($row.PSObject.Properties.Name | Sort-Object)
        if ((Compare-Object @('path', 'provenance_pin_id', 'sha256', 'size') $rowFields) -or
            $row.path -isnot [string] -or $row.sha256 -isnot [string] -or
            $row.sha256 -notmatch $shaPattern -or $row.size -isnot [int64] -or $row.size -lt 0 -or
            $row.provenance_pin_id -isnot [string] -or
            $row.provenance_pin_id -notmatch '^[ -~]{1,256}$') {
            throw 'base payload row contract differs'
        }
        $virtualPath = Require-SafeVirtualPath $row.path
        if (($null -ne $previous -and [StringComparer]::Ordinal.Compare($virtualPath, $previous) -le 0) -or
            -not $caseKeys.Add($virtualPath)) {
            throw 'base payload rows are not unique ASCII-sorted without Windows aliases'
        }
        $rows.Add($virtualPath, $row.sha256)
        $sizes.Add($virtualPath, [long]$row.size)
        $total += [long]$row.size
        $previous = $virtualPath
    }
    if ($rows.Count -ne $baseFileCount -or $total -ne $baseTotalBytes) {
        throw 'base payload row aggregate differs'
    }
    return [pscustomobject]@{ Rows = $rows; Sizes = $sizes }
}

function Get-ExactFileInventory([string]$Root) {
    $pending = [Collections.Generic.Queue[string]]::new()
    $pending.Enqueue($Root)
    $paths = [Collections.Generic.List[string]]::new()
    while ($pending.Count -gt 0) {
        $directory = $pending.Dequeue()
        foreach ($entryPath in [IO.Directory]::EnumerateFileSystemEntries($directory)) {
            $entry = Get-Item -LiteralPath $entryPath -Force
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw 'runtime inventory contains a reparse entry'
            }
            if ($entry.PSIsContainer) {
                $pending.Enqueue($entry.FullName)
            }
            else {
                $relative = [IO.Path]::GetRelativePath($Root, $entry.FullName).Replace('\', '/')
                [void]$paths.Add((Require-SafeVirtualPath $relative))
            }
        }
    }
    $array = @($paths | Sort-Object)
    if ($array.Count -ne (@($array | Sort-Object -Unique)).Count) { throw 'runtime inventory path collision' }
    return $array
}

function Verify-Root([string]$Root, [Collections.IDictionary]$Rows, [long]$ExpectedBytes) {
    $observed = @(Get-ExactFileInventory $Root)
    $expected = @($Rows.Keys)
    if ($observed.Count -ne $expected.Count -or (Compare-Object $expected $observed)) {
        throw 'runtime exact-set differs from manifest'
    }
    $total = 0L
    foreach ($virtualPath in $expected) {
        $native = [IO.Path]::Combine($Root, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
        $file = Require-File $native 'runtime target'
        $item = Get-Item -LiteralPath $file -Force
        $total += $item.Length
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Rows[$virtualPath]) {
            throw 'runtime target hash differs'
        }
    }
    if ($total -ne $ExpectedBytes) { throw 'runtime total byte count differs' }
    return $total
}

function Verify-BaseRoot(
    [string]$Root,
    [Collections.IDictionary]$Rows,
    [Collections.IDictionary]$Sizes
) {
    $expected = [Collections.Generic.List[string]]::new()
    foreach ($virtualPath in $Rows.Keys) {
        if ($virtualPath.StartsWith('evidence/', [StringComparison]::Ordinal)) {
            throw 'base payload manifest attempts to absorb the evidence authority area'
        }
        [void]$expected.Add($virtualPath)
    }
    foreach ($evidencePath in $baseEvidenceHashes.Keys) {
        [void]$expected.Add($evidencePath)
        [void]$expected.Add("$evidencePath.sha256")
    }
    $expectedArray = @($expected | Sort-Object)
    $observed = @(Get-ExactFileInventory $Root)
    if ($observed.Count -ne ($baseFileCount + 8) -or
        $expectedArray.Count -ne ($baseFileCount + 8) -or
        (Compare-Object $expectedArray $observed)) {
        throw 'base root is not the exact payload plus authenticated evidence set'
    }
    $total = 0L
    foreach ($virtualPath in $Rows.Keys) {
        $native = [IO.Path]::Combine($Root, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
        $file = Require-File $native 'base payload target'
        $item = Get-Item -LiteralPath $file -Force
        if ($item.Length -ne $Sizes[$virtualPath] -or
            (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Rows[$virtualPath]) {
            throw 'base payload target size or hash differs'
        }
        $total += $item.Length
    }
    if ($Rows.Count -ne $baseFileCount -or $total -ne $baseTotalBytes) {
        throw 'base payload exact-set aggregate differs'
    }
    foreach ($evidencePath in $baseEvidenceHashes.Keys) {
        $native = [IO.Path]::Combine($Root, $evidencePath.Replace('/', [IO.Path]::DirectorySeparatorChar))
        $expectedHash = $baseEvidenceHashes[$evidencePath]
        if ((Get-FileHash -LiteralPath (Require-File $native 'base evidence target') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedHash) {
            throw 'base evidence target hash differs'
        }
        $sidecar = "$native.sha256"
        $filename = [IO.Path]::GetFileName($native)
        $expectedSidecar = [Text.Encoding]::ASCII.GetBytes("$expectedHash  $filename`n")
        $actualSidecar = [IO.File]::ReadAllBytes((Require-File $sidecar 'base evidence sidecar'))
        if ($actualSidecar.Length -ne $expectedSidecar.Length) {
            throw 'base evidence sidecar length differs'
        }
        for ($index = 0; $index -lt $actualSidecar.Length; $index++) {
            if ($actualSidecar[$index] -ne $expectedSidecar[$index]) {
                throw 'base evidence sidecar bytes differ'
            }
        }
    }
}

function Copy-Authenticated([string]$Source, [string]$Destination, [string]$ExpectedSha256) {
    $parent = [IO.Path]::GetDirectoryName($Destination)
    [void][IO.Directory]::CreateDirectory($parent)
    $input = [IO.File]::Open($Source, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try {
        $output = [IO.File]::Open($Destination, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        try { $input.CopyTo($output) }
        finally { $output.Dispose() }
    }
    finally { $input.Dispose() }
    if ((Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedSha256) {
        throw 'copied runtime target hash differs'
    }
}

$baseRoot = Require-Directory $BaseRuntimeRoot 'base runtime root'
$overlayRootValue = Require-Directory $OverlayRoot 'overlay root'
$baseManifest = Require-File $BaseManifestPath 'base manifest'
$overlayManifest = Require-File $OverlayManifestPath 'overlay manifest'
$overlayContract = Require-File $OverlayContractPath 'overlay contract'
$output = Require-Absolute $OutputRoot 'output root'
$finalManifest = Require-Absolute $FinalManifestPath 'final manifest'
if ((Test-AtOrUnder $output $baseRoot) -or (Test-AtOrUnder $output $overlayRootValue) -or
    (Test-AtOrUnder $finalManifest $baseRoot) -or (Test-AtOrUnder $finalManifest $overlayRootValue) -or
    (Test-AtOrUnder $finalManifest $output) -or (Test-AtOrUnder $baseRoot $overlayRootValue) -or
    (Test-AtOrUnder $overlayRootValue $baseRoot)) {
    throw 'base, overlay, output, and final-manifest locations are not isolated'
}
if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $finalManifest)) {
    throw 'output root and final manifest must both be absent'
}
if ($OverlayManifestSha256 -notmatch $shaPattern -or $OverlayContractSha256 -notmatch $shaPattern) {
    throw 'overlay authority pin is malformed'
}
if ((Get-FileHash -LiteralPath $overlayContract -Algorithm SHA256).Hash.ToLowerInvariant() -ne $OverlayContractSha256) {
    throw 'overlay contract pin differs'
}
$contractRaw = [IO.File]::ReadAllBytes($overlayContract)
$contract = [Text.UTF8Encoding]::new($false, $true).GetString($contractRaw) | ConvertFrom-Json
$contractFields = @($contract.PSObject.Properties.Name | Sort-Object)
$expectedContractFields = @('overlay_file_count', 'overlay_manifest_sha256', 'overlay_total_bytes',
                            'platform_evidence_state', 'required_rows', 'schema_id')
if ((Compare-Object $expectedContractFields $contractFields) -or
    $contract.schema_id -ne 'S0-RUNTIME-PRELOADER-V0.4-OVERLAY-CONTRACT-1' -or
    $contract.overlay_manifest_sha256 -ne $OverlayManifestSha256 -or
    $contract.platform_evidence_state -ne 'explicitly-pinned-unverified-until-stage70' -or
    $contract.overlay_file_count -isnot [int64] -or $contract.overlay_file_count -le 0 -or
    $contract.overlay_total_bytes -isnot [int64] -or $contract.overlay_total_bytes -le 0 -or
    $contract.required_rows -isnot [array] -or $contract.required_rows.Count -eq 0) {
    throw 'overlay contract shape or platform boundary differs'
}

$expectedBaseManifest = [IO.Path]::Combine($baseRoot, 'evidence', 'payload-manifest.json')
if ([StringComparer]::Ordinal.Compare($baseManifest, $expectedBaseManifest) -ne 0) {
    throw 'base payload manifest path differs'
}
$baseInfo = Read-BasePayloadManifest $baseManifest
$baseRows = $baseInfo.Rows
$baseSizes = $baseInfo.Sizes
Verify-BaseRoot $baseRoot $baseRows $baseSizes
$overlayRows = Read-Manifest $overlayManifest $OverlayManifestSha256 ([int]$contract.overlay_file_count)
$overlayBytes = [long]$contract.overlay_total_bytes
[void](Verify-Root $overlayRootValue $overlayRows $overlayBytes)

$required = [ordered]@{}
$requiredClasses = @('admitted-system-image', 'bounded-integration-adapter', 'loaded-pe-manifest',
                     'native-guard', 'native-preloader', 'platform-manifest',
                     'pre-import-bootstrap', 'public-assembly-verifier',
                     'runtime-preloader-python')
$observedClasses = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($row in $contract.required_rows) {
    $rowFields = @($row.PSObject.Properties.Name | Sort-Object)
    if ((Compare-Object @('class', 'path', 'sha256') $rowFields) -or
        $row.path -isnot [string] -or $row.sha256 -isnot [string] -or
        $row.sha256 -notmatch $shaPattern -or $row.class -isnot [string] -or
        $row.class -notin $requiredClasses) {
        throw 'overlay contract required row differs'
    }
    $virtualPath = Require-SafeVirtualPath $row.path
    if ($required.Contains($virtualPath)) { throw 'overlay contract required row is duplicated' }
    $required.Add($virtualPath, $row.sha256)
    [void]$observedClasses.Add($row.class)
}
if ($required.Count -ne $overlayRows.Count -or
    (Compare-Object $requiredClasses @($observedClasses | Sort-Object))) {
    throw 'overlay contract does not classify the exact overlay and all required families'
}
foreach ($virtualPath in $required.Keys) {
    if (-not $overlayRows.Contains($virtualPath) -or $overlayRows[$virtualPath] -ne $required[$virtualPath]) {
        throw 'required overlay row is absent or changed'
    }
}

$finalRows = [ordered]@{}
foreach ($virtualPath in $baseRows.Keys) { $finalRows.Add($virtualPath, $baseRows[$virtualPath]) }
foreach ($virtualPath in $overlayRows.Keys) {
    if ($finalRows.Contains($virtualPath)) { throw 'overlay attempts to replace a v0.7 base row' }
    $finalRows.Add($virtualPath, $overlayRows[$virtualPath])
}
$sortedRows = [ordered]@{}
[string[]]$finalPaths = @($finalRows.Keys)
[Array]::Sort($finalPaths, [StringComparer]::Ordinal)
for ($index = 1; $index -lt $finalPaths.Count; $index++) {
    if ([StringComparer]::Ordinal.Equals($finalPaths[$index - 1], $finalPaths[$index])) {
        throw 'final runtime path set contains an ordinal duplicate'
    }
}
foreach ($virtualPath in $finalPaths) { $sortedRows.Add($virtualPath, $finalRows[$virtualPath]) }

$outputParent = Require-Directory ([IO.Path]::GetDirectoryName($output)) 'output parent'
$outputLeaf = [IO.Path]::GetFileName($output)
if ($outputLeaf -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$') { throw 'output leaf differs' }
$staging = [IO.Path]::Combine($outputParent, ".s0-rpnp-v04-$([Guid]::NewGuid().ToString('N'))")
if (Test-Path -LiteralPath $staging) { throw 'fresh staging collision' }
[void][IO.Directory]::CreateDirectory($staging)
$marker = [IO.Path]::Combine($staging, '.s0-runtime-materialization-owner')
[IO.File]::WriteAllText($marker, $OverlayContractSha256, [Text.Encoding]::ASCII)
foreach ($virtualPath in $baseRows.Keys) {
    $source = [IO.Path]::Combine($baseRoot, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
    $destination = [IO.Path]::Combine($staging, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
    Copy-Authenticated $source $destination $baseRows[$virtualPath]
}
foreach ($virtualPath in $overlayRows.Keys) {
    $source = [IO.Path]::Combine($overlayRootValue, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
    $destination = [IO.Path]::Combine($staging, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar))
    Copy-Authenticated $source $destination $overlayRows[$virtualPath]
}
[IO.File]::Delete($marker)
$finalBytes = 0L
foreach ($virtualPath in $sortedRows.Keys) {
    $finalBytes += (Get-Item -LiteralPath ([IO.Path]::Combine($staging, $virtualPath.Replace('/', [IO.Path]::DirectorySeparatorChar)))).Length
}
[void](Verify-Root $staging $sortedRows $finalBytes)
[IO.Directory]::Move($staging, $output)
[void](Verify-Root $output $sortedRows $finalBytes)

$manifestText = (($sortedRows.Keys | ForEach-Object { "$($sortedRows[$_])  $_" }) -join "`n") + "`n"
$manifestBytes = [Text.Encoding]::ASCII.GetBytes($manifestText)
$manifestParent = Require-Directory ([IO.Path]::GetDirectoryName($finalManifest)) 'final manifest parent'
$manifestLeaf = [IO.Path]::GetFileName($finalManifest)
if ($manifestLeaf -ne 'runtime-files.sha256') { throw 'final manifest name differs' }
$stream = [IO.File]::Open([IO.Path]::Combine($manifestParent, $manifestLeaf), [IO.FileMode]::CreateNew,
                          [IO.FileAccess]::Write, [IO.FileShare]::None)
try { $stream.Write($manifestBytes, 0, $manifestBytes.Length) }
finally { $stream.Dispose() }
$manifestReadback = [IO.File]::ReadAllBytes($finalManifest)
if ($manifestReadback.Length -ne $manifestBytes.Length) {
    throw 'final manifest readback length differs'
}
for ($index = 0; $index -lt $manifestBytes.Length; $index++) {
    if ($manifestReadback[$index] -ne $manifestBytes[$index]) {
        throw 'final manifest readback bytes differ'
    }
}
$finalManifestSha256 = (Get-FileHash -LiteralPath $finalManifest -Algorithm SHA256).Hash.ToLowerInvariant()
$reparsedRows = Read-Manifest $finalManifest $finalManifestSha256 $sortedRows.Count
[string[]]$reparsedPaths = @($reparsedRows.Keys)
if ($reparsedPaths.Count -ne $finalPaths.Count) {
    throw 'final manifest reparsed row count differs'
}
for ($index = 0; $index -lt $finalPaths.Count; $index++) {
    if (-not [StringComparer]::Ordinal.Equals($reparsedPaths[$index], $finalPaths[$index]) -or
        $reparsedRows[$reparsedPaths[$index]] -ne $sortedRows[$finalPaths[$index]]) {
        throw 'final manifest reparsed path, order, or hash differs'
    }
}

[ordered]@{
    base_file_count = $baseRows.Count
    base_manifest_sha256 = $baseManifestSha256
    final_file_count = $sortedRows.Count
    final_manifest_sha256 = $finalManifestSha256
    final_total_bytes = $finalBytes
    output_root = $output
    platform_evidence_state = 'explicitly-pinned-unverified-until-stage70'
    schema_id = 'S0-RUNTIME-PRELOADER-V0.4-MATERIALIZATION-RESULT-1'
}
