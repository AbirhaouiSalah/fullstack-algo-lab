<#
.SYNOPSIS
    Scaffolds a new algorithm problem directory, including a benchmark-ready
    solution template.

.PARAMETER Category
    The algorithm category folder (must already exist under algorithms/).

.PARAMETER Name
    Kebab-case problem name, e.g. "course-schedule".

.PARAMETER Difficulty
    Easy | Medium | Hard. Written into README.md so generate-report.ts can
    pick it up automatically. Defaults to "Medium".

.EXAMPLE
    .\create-problem.ps1 -Category "graphs" -Name "course-schedule" -Difficulty "Hard"
#>

param(
    [Parameter(Mandatory)]
    [string]$Category,

    [Parameter(Mandatory)]
    [string]$Name,

    [ValidateSet("Easy", "Medium", "Hard")]
    [string]$Difficulty = "Medium"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
$categoryPath = Join-Path $repoRoot "algorithms/$Category"
$problemPath = Join-Path $categoryPath $Name

if (-not (Test-Path $categoryPath)) {
    Write-Warning "Category '$Category' does not exist under algorithms/. Creating it."
    New-Item -ItemType Directory -Path $categoryPath -Force | Out-Null
}

if (Test-Path $problemPath) {
    Write-Warning "Problem directory already exists: $problemPath"
    exit 1
}

New-Item -ItemType Directory -Path $problemPath -Force | Out-Null

$titleCase = ($Name -split '-' | ForEach-Object { $_.Substring(0,1).ToUpper() + $_.Substring(1) }) -join ' '

$readme = @"
# $titleCase

difficulty: $Difficulty

## Problem Statement

TODO

## Intuition

TODO

## Complexity

See [complexity.md](./complexity.md).
"@

$solutionTs = @"
/**
 * benchmarkInput is consumed by scripts/algorithms/benchmark.ts to invoke
 * the exported solution function repeatedly with a representative payload.
 * Replace with realistic argument(s) once the solution is implemented.
 */
export const benchmarkInput: unknown[] = [];

export function solve(): void {
  // TODO: implement solution
}
"@

$solutionPy = @"
def solve():
    # TODO: implement solution
    pass
"@

$testTs = @"
import { describe, expect, it } from "vitest";
import { solve } from "./solution";

describe("$Name", () => {
  it.todo("add test cases");
});
"@

$complexity = @"
# Complexity Analysis: $titleCase

## Time Complexity

TODO

## Space Complexity

TODO
"@

Set-Content -Path (Join-Path $problemPath "README.md") -Value $readme -Encoding UTF8
Set-Content -Path (Join-Path $problemPath "solution.ts") -Value $solutionTs -Encoding UTF8
Set-Content -Path (Join-Path $problemPath "solution.py") -Value $solutionPy -Encoding UTF8
Set-Content -Path (Join-Path $problemPath "solution.test.ts") -Value $testTs -Encoding UTF8
Set-Content -Path (Join-Path $problemPath "complexity.md") -Value $complexity -Encoding UTF8

Write-Host "Created new problem scaffold ($Difficulty) at: $problemPath" -ForegroundColor Green
