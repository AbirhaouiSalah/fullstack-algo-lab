<#
.SYNOPSIS
    Scaffolds a new algorithm problem directory with templates.

.EXAMPLE
    .\create-problem.ps1 -Category "graphs" -Name "course-schedule"
#>

param(
    [Parameter(Mandatory)]
    [string]$Category,

    [Parameter(Mandatory)]
    [string]$Name
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
$problemPath = Join-Path $repoRoot "algorithms/$Category/$Name"

if (Test-Path $problemPath) {
    Write-Warning "Problem directory already exists: $problemPath"
    exit 1
}

New-Item -ItemType Directory -Path $problemPath -Force | Out-Null

$readme = @"
# $($Name -replace '-', ' ')

## Problem Statement

TODO

## Intuition

TODO

## Complexity

See [complexity.md](./complexity.md).
"@

$solutionTs = @"
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
# Complexity Analysis: $($Name -replace '-', ' ')

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

Write-Host "Created new problem scaffold at: $problemPath" -ForegroundColor Green
