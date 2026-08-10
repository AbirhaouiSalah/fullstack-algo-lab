<#
.SYNOPSIS
    Runs the full Vitest suite with formatted output.
#>

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
Push-Location $repoRoot

try {
    Write-Host "Running full algorithm test suite..." -ForegroundColor Cyan
    npx vitest run --reporter=verbose
}
finally {
    Pop-Location
}
