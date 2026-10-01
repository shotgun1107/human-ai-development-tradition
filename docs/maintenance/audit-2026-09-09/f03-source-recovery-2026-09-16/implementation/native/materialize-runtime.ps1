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
    [Parameter(Mandatory = $true)][string]$FinalManifestPath,
    [Parameter(Mandatory = $true)][string]$RepositoryRoot,
    [Parameter(Mandatory = $true)][string]$NativeMaterializerExe,
    [Parameter(Mandatory = $true)][string]$NativeMaterializerSha256,
    [Parameter(Mandatory = $true)][string]$BuildTracePath,
    [Parameter(Mandatory = $true)][string]$BuildTraceSha256,
    [Parameter(Mandatory = $true)][string]$RunNonce,
    [Parameter(Mandatory = $true)][string]$ExternalPinDigest
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# This wrapper has no output-file, copying, renaming or publication authority.
# The caller is the externally authenticated CONTROL launcher; hashes passed
# here are only locators for its frozen authority, not a caller-minted trust root.
foreach ($digest in @($OverlayManifestSha256, $OverlayContractSha256,
    $NativeMaterializerSha256, $BuildTraceSha256, $RunNonce, $ExternalPinDigest)) {
    if ($digest -cnotmatch '^[0-9a-f]{64}$') { throw 'CONTROL digest is not canonical' }
}
if ($NativeMaterializerExe -cnotmatch '^[A-Z]:\\' -or $BuildTracePath -cnotmatch '^[A-Z]:\\') {
    throw 'explicit absolute native materializer and build trace paths are required'
}
if ((Get-FileHash -LiteralPath $NativeMaterializerExe -Algorithm SHA256).Hash.ToLowerInvariant() -ne $NativeMaterializerSha256 -or
    (Get-FileHash -LiteralPath $BuildTracePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $BuildTraceSha256) {
    throw 'native materializer or build trace differs from external CONTROL pin'
}
$trace = Get-Content -LiteralPath $BuildTracePath -Raw | ConvertFrom-Json
$producerRows = @($trace.outputs | Where-Object { $_.filename -ceq 's0_runtime_materializer_v0_5.exe' })
if ($trace.schema_id -cne 'S0-RUNTIME-PRELOADER-V0.5-BUILD-TRACE-1' -or
    $trace.effective_interface_map_sha256 -cne 'f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623' -or
    $trace.effective_schema_sha256 -cne '04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e' -or
    $producerRows.Count -ne 1 -or $producerRows[0].sha256 -cne $NativeMaterializerSha256) {
    throw 'native materializer build provenance does not bind the effective design'
}
$arguments = @(
    '--base-root', $BaseRuntimeRoot, '--base-manifest', $BaseManifestPath,
    '--overlay-root', $OverlayRoot, '--overlay-manifest', $OverlayManifestPath,
    '--overlay-sha256', $OverlayManifestSha256, '--overlay-contract', $OverlayContractPath,
    '--contract-sha256', $OverlayContractSha256, '--repository-root', $RepositoryRoot,
    '--output-root', $OutputRoot, '--final-manifest', $FinalManifestPath,
    '--producer-path', $NativeMaterializerExe, '--producer-sha256', $NativeMaterializerSha256,
    '--run-nonce', $RunNonce, '--external-pin-digest', $ExternalPinDigest,
    '--build-trace', $BuildTracePath, '--build-trace-sha256', $BuildTraceSha256
)
& $NativeMaterializerExe @arguments
$materializerExitCode = $LASTEXITCODE
if ($materializerExitCode -ne 0) {
    throw "native materialization rejected with exit $materializerExitCode; any partial transaction root is non-authoritative"
}
