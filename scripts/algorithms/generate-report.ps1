<#
.SYNOPSIS
    Regenerates docs/algorithms/progress.md by scanning the algorithms/ tree.

.DESCRIPTION
    Counts solved problems per category based on the presence of a
    solution.ts file, and rewrites the progress dashboard table.
    Difficulty tagging (Easy/Medium/Hard) is expected as front-matter or a
    tag inside each problem's README.md; extend the parsing logic below as
    that convention is adopted.
#>

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
$algoRoot = Join-Path $repoRoot "algorithms"
$progressFile = Join-Path $repoRoot "docs/algorithms/progress.md"

$categories = Get-ChildItem -Path $algoRoot -Directory | Sort-Object Name

$rows = foreach ($category in $categories) {
    $problems = Get-ChildItem -Path $category.FullName -Directory -ErrorAction SilentlyContinue
    $total = ($problems | Where-Object {
        Test-Path (Join-Path $_.FullName "solution.ts")
    }).Count

    [PSCustomObject]@{
        Category = $category.Name
        Easy     = 0
        Medium   = 0
        Hard     = 0
        Total    = $total
    }
}

$lines = @()
$lines += "# Progress Dashboard"
$lines += ""
$lines += "| Category | Easy | Medium | Hard | Total |"
$lines += "|---|---|---|---|---|"

foreach ($row in $rows) {
    $lines += "| $($row.Category) | $($row.Easy) | $($row.Medium) | $($row.Hard) | $($row.Total) |"
}

$lines += ""
$lines += "_Updated automatically by scripts/algorithms/generate-report.ps1 on $(Get-Date -Format 'yyyy-MM-dd')_"

Set-Content -Path $progressFile -Value ($lines -join "`n") -Encoding UTF8
Write-Host "progress.md regenerated at: $progressFile" -ForegroundColor Green
