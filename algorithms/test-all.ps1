$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$repoRoot = $repoRoot.Path
$nodeExe = "C:\Program Files\nodejs\node.exe"
$vitestExe = Join-Path $repoRoot "node_modules\.bin\vitest.cmd"
$tsNodeExe = Join-Path $repoRoot "node_modules\.bin\ts-node.cmd"
$tscExe = Join-Path $repoRoot "node_modules\.bin\tsc.cmd"

$env:PATH = "$env:PATH;C:\Program Files\nodejs"

if (-not (Test-Path $nodeExe)) {
    throw "Node.js executable not found at $nodeExe"
}

if (-not (Test-Path $vitestExe)) {
    throw "Vitest executable not found at $vitestExe"
}

if (-not (Test-Path $tsNodeExe)) {
    throw "ts-node executable not found at $tsNodeExe"
}

if (-not (Test-Path $tscExe)) {
    throw "tsc executable not found at $tscExe"
}

function Invoke-LocalCommand {
    param(
        [Parameter(Mandatory)] [string]$CommandPath,
        [Parameter(Mandatory)] [string[]]$Arguments
    )

    & $CommandPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $CommandPath $($Arguments -join ' ')"
    }
}

function Invoke-Vitest {
    Invoke-LocalCommand -CommandPath $vitestExe -Arguments @("run", "--config", "vitest.config.ts", "algorithms/")
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     ALGORITHM LABORATORY EVALUATOR    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Push-Location $repoRoot
try {
    # 1. Execute Vitest Unit & Edge Case Tests
    Write-Host "`n[1/3] Executing Vitest Automated Test Suites..." -ForegroundColor Yellow
    Invoke-Vitest

    # 2. Run Progress Reporter
    Write-Host "`n[2/3] Updating Progress Dashboard (docs/algorithms/progress.md)..." -ForegroundColor Yellow
    Invoke-LocalCommand -CommandPath $tsNodeExe -Arguments @("algorithms/generate-report.ts")

    # 3. Type-check Codebase
    Write-Host "`n[3/3] Running TypeScript Compiler Checks..." -ForegroundColor Yellow
    Invoke-LocalCommand -CommandPath $tscExe -Arguments @("--noEmit")
}
finally {
    Pop-Location
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ALL CHECKS PASSED — READY TO COMMIT   " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green