<#
.SYNOPSIS
Validates public Markdown artifacts and their same-basename SHA-256 sidecars.

.DESCRIPTION
Performs byte-level UTF-8 BOM detection, strict UTF-8 decoding, final-LF and
trailing-whitespace checks, then verifies the canonical sidecar record and hash.
Each check is reported independently so one failure cannot be mislabeled as
another. Use -SelfTest to run the in-memory regression suite.

.EXAMPLE
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  s0-lab/control/tools/verify-text-artifacts.ps1 `
  -Path s0-lab/reviews/f0-public/question-contract-v0.8/urc-v0.8-independent-review-v0.1.md
#>

[CmdletBinding(DefaultParameterSetName = 'Files')]
param(
    [Parameter(Mandatory = $true, Position = 0, ParameterSetName = 'Files')]
    [ValidateNotNullOrEmpty()]
    [string[]]$Path,

    [Parameter(Mandatory = $true, ParameterSetName = 'SelfTest')]
    [switch]$SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:StrictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
$script:PlainUtf8 = [System.Text.UTF8Encoding]::new($false)

function Test-CanonicalTextBytes {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [byte[]]$Bytes
    )

    $hasUtf8Bom = (
        $Bytes.Length -ge 3 -and
        $Bytes[0] -eq 0xEF -and
        $Bytes[1] -eq 0xBB -and
        $Bytes[2] -eq 0xBF
    )

    $utf8Valid = $true
    $text = $null
    try {
        $text = $script:StrictUtf8.GetString($Bytes)
    }
    catch [System.Text.DecoderFallbackException] {
        $utf8Valid = $false
    }

    $finalLf = $Bytes.Length -gt 0 -and $Bytes[$Bytes.Length - 1] -eq 0x0A
    $noTrailingWhitespace = $false
    if ($utf8Valid) {
        $noTrailingWhitespace = -not [regex]::IsMatch(
            $text,
            '(?m)[\x20\x09]+(?=\r?$)'
        )
    }

    [pscustomobject]@{
        Utf8Valid           = $utf8Valid
        Utf8BomAbsent       = -not $hasUtf8Bom
        FinalLf             = $finalLf
        NoTrailingWhitespace = $noTrailingWhitespace
        Valid               = (
            $utf8Valid -and
            -not $hasUtf8Bom -and
            $finalLf -and
            $noTrailingWhitespace
        )
        Text                = $text
    }
}

function Test-CanonicalSidecarRecord {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedHash,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedFileName
    )

    $expected = "$ExpectedHash  $ExpectedFileName`n"
    return [string]::Equals($Text, $expected, [System.StringComparison]::Ordinal)
}

function Format-CheckResult {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Check,

        [Parameter(Mandatory = $true)]
        [bool]$Passed
    )

    $state = if ($Passed) { 'PASS' } else { 'FAIL' }
    return "CHECK=$Check RESULT=$state"
}

function Invoke-RegressionSelfTest {
    $validLf = [byte[]]$script:PlainUtf8.GetBytes("# U`n")
    $validSidecarPrefix = [byte[]]$script:PlainUtf8.GetBytes("9bc`n")
    $validCrlf = [byte[]]$script:PlainUtf8.GetBytes("ok`r`n")
    $bom = [byte[]](@(0xEF, 0xBB, 0xBF) + @($validLf))
    $missingLf = [byte[]]$script:PlainUtf8.GetBytes('missing')
    $trailingSpace = [byte[]]$script:PlainUtf8.GetBytes("bad `n")
    $trailingTabCrlf = [byte[]]$script:PlainUtf8.GetBytes("bad`t`r`n")
    $invalidUtf8 = [byte[]](0xC3, 0x28, 0x0A)
    $empty = [byte[]]@()

    $cases = @(
        [pscustomobject]@{ Name = 'markdown-prefix-no-bom'; Bytes = $validLf; Expected = $true },
        [pscustomobject]@{ Name = 'sidecar-prefix-no-bom'; Bytes = $validSidecarPrefix; Expected = $true },
        [pscustomobject]@{ Name = 'valid-crlf'; Bytes = $validCrlf; Expected = $true },
        [pscustomobject]@{ Name = 'actual-utf8-bom'; Bytes = $bom; Expected = $false },
        [pscustomobject]@{ Name = 'missing-final-lf'; Bytes = $missingLf; Expected = $false },
        [pscustomobject]@{ Name = 'trailing-space'; Bytes = $trailingSpace; Expected = $false },
        [pscustomobject]@{ Name = 'trailing-tab-crlf'; Bytes = $trailingTabCrlf; Expected = $false },
        [pscustomobject]@{ Name = 'invalid-utf8'; Bytes = $invalidUtf8; Expected = $false },
        [pscustomobject]@{ Name = 'empty-file'; Bytes = $empty; Expected = $false }
    )

    $failed = $false
    foreach ($case in $cases) {
        $actual = (Test-CanonicalTextBytes -Bytes $case.Bytes).Valid
        $passed = $actual -eq $case.Expected
        "SELF_TEST_CASE=$($case.Name) RESULT=$(if ($passed) { 'PASS' } else { 'FAIL' })"
        if (-not $passed) {
            $failed = $true
        }
    }

    $dummyHash = ('a' * 64) -join ''
    $canonicalRecord = "$dummyHash  artifact.md`n"
    $sidecarPass = Test-CanonicalSidecarRecord `
        -Text $canonicalRecord `
        -ExpectedHash $dummyHash `
        -ExpectedFileName 'artifact.md'
    "SELF_TEST_CASE=canonical-sidecar RESULT=$(if ($sidecarPass) { 'PASS' } else { 'FAIL' })"
    if (-not $sidecarPass) {
        $failed = $true
    }

    $badRecord = "$dummyHash artifact.md`n"
    $badSidecarRejected = -not (Test-CanonicalSidecarRecord `
        -Text $badRecord `
        -ExpectedHash $dummyHash `
        -ExpectedFileName 'artifact.md')
    "SELF_TEST_CASE=noncanonical-sidecar-rejected RESULT=$(if ($badSidecarRejected) { 'PASS' } else { 'FAIL' })"
    if (-not $badSidecarRejected) {
        $failed = $true
    }

    if ($failed) {
        'SELF_TEST=FAIL'
        exit 1
    }

    'SELF_TEST=PASS'
}

function Invoke-FileValidation {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$InputPath
    )

    $overallFailed = $false

    foreach ($input in $InputPath) {
        $resolvedPath = $null
        try {
            $resolvedPath = (Resolve-Path -LiteralPath $input -ErrorAction Stop).Path
            $item = Get-Item -LiteralPath $resolvedPath -Force -ErrorAction Stop
            if ($item.PSIsContainer) {
                throw "Path is a directory: $input"
            }
            if (-not [string]::Equals(
                [System.IO.Path]::GetExtension($item.Name),
                '.md',
                [System.StringComparison]::OrdinalIgnoreCase
            )) {
                throw "Expected a Markdown .md file: $input"
            }
        }
        catch {
            "FILE=$input"
            'CHECK=FILE_PRESENT RESULT=FAIL'
            "DETAIL=$($_.Exception.Message)"
            $overallFailed = $true
            continue
        }

        "FILE=$resolvedPath"
        'CHECK=FILE_PRESENT RESULT=PASS'

        $artifactBytes = [System.IO.File]::ReadAllBytes($resolvedPath)
        $artifact = Test-CanonicalTextBytes -Bytes $artifactBytes
        Format-CheckResult -Check 'UTF8_VALID' -Passed $artifact.Utf8Valid
        Format-CheckResult -Check 'UTF8_BOM_ABSENT' -Passed $artifact.Utf8BomAbsent
        Format-CheckResult -Check 'FINAL_LF' -Passed $artifact.FinalLf
        Format-CheckResult -Check 'TRAILING_WHITESPACE_ABSENT' -Passed $artifact.NoTrailingWhitespace

        $sidecarPath = [System.IO.Path]::ChangeExtension($resolvedPath, '.sha256')
        $sidecarPresent = Test-Path -LiteralPath $sidecarPath -PathType Leaf
        Format-CheckResult -Check 'SIDECAR_PRESENT' -Passed $sidecarPresent

        $sidecarTextValid = $false
        $sidecarRecordValid = $false
        if ($sidecarPresent) {
            $sidecarBytes = [System.IO.File]::ReadAllBytes($sidecarPath)
            $sidecar = Test-CanonicalTextBytes -Bytes $sidecarBytes
            $sidecarTextValid = $sidecar.Valid
            Format-CheckResult -Check 'SIDECAR_UTF8_VALID' -Passed $sidecar.Utf8Valid
            Format-CheckResult -Check 'SIDECAR_UTF8_BOM_ABSENT' -Passed $sidecar.Utf8BomAbsent
            Format-CheckResult -Check 'SIDECAR_FINAL_LF' -Passed $sidecar.FinalLf
            Format-CheckResult -Check 'SIDECAR_TRAILING_WHITESPACE_ABSENT' -Passed $sidecar.NoTrailingWhitespace

            if ($sidecarTextValid) {
                $actualHash = (Get-FileHash -LiteralPath $resolvedPath -Algorithm SHA256).Hash.ToLowerInvariant()
                $sidecarRecordValid = Test-CanonicalSidecarRecord `
                    -Text $sidecar.Text `
                    -ExpectedHash $actualHash `
                    -ExpectedFileName ([System.IO.Path]::GetFileName($resolvedPath))
            }
            Format-CheckResult -Check 'SIDECAR_RECORD_AND_HASH' -Passed $sidecarRecordValid
        }

        $filePassed = $artifact.Valid -and $sidecarPresent -and $sidecarTextValid -and $sidecarRecordValid
        Format-CheckResult -Check 'ARTIFACT_OVERALL' -Passed $filePassed
        if (-not $filePassed) {
            $overallFailed = $true
        }
    }

    if ($overallFailed) {
        'OVERALL=FAIL'
        exit 1
    }

    'OVERALL=PASS'
}

if ($PSCmdlet.ParameterSetName -eq 'SelfTest') {
    Invoke-RegressionSelfTest
}
else {
    Invoke-FileValidation -InputPath $Path
}
