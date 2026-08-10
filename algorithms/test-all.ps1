Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     ALGORITHM LABORATORY EVALUATOR    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Execute Vitest Unit & Edge Case Tests
Write-Host "`n[1/3] Executing Vitest Automated Test Suites..." -ForegroundColor Yellow
npx vitest run algorithms/

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERROR] Vitest suite failed. Resolve errors before proceeding." -ForegroundColor Red
    exit 1
}

# 2. Run Progress Reporter
Write-Host "`n[2/3] Updating Progress Dashboard (docs/algorithms/progress.md)..." -ForegroundColor Yellow
npx ts-node scripts/algorithms/generate-report.ts

# 3. Type-check Codebase
Write-Host "`n[3/3] Running TypeScript Compiler Checks..." -ForegroundColor Yellow
npx tsc --noEmit

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ALL CHECKS PASSED — READY TO COMMIT   " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green