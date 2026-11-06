<#
.SYNOPSIS
    Scaffolds the algo-evaluation automation structure (CI workflow,
    benchmarking scripts, and Vitest performance config).

.DESCRIPTION
    Creates/updates:
      .github/workflows/algo-evaluation-pipeline.yml
      scripts/algorithms/benchmark.ts
      scripts/algorithms/generate-report.ts
      scripts/algorithms/test-all.ps1
      scripts/algorithms/create-problem.ps1
      vitest.config.ts

    Idempotent: existing files are skipped unless -Force is passed.

.PARAMETER RootPath
    Path to the existing repository root (the folder that already contains
    algorithms/, docs/, scripts/, etc). Defaults to the current directory.

.PARAMETER Force
    Overwrite existing files with the generated content.

.EXAMPLE
    .\build-automation-structure.ps1
    .\build-automation-structure.ps1 -RootPath C:\Projects\fullstack-algo-lab -Force
#>

[CmdletBinding()]
param(
    [string]$RootPath = (Get-Location).Path,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

function New-FileWithContent {
    param(
        [string]$Path,
        [string]$Content = ''
    )
    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }

    if ((Test-Path -LiteralPath $Path) -and -not $Force) {
        Write-Host "  [skip] $Path (already exists)" -ForegroundColor Yellow
        return
    }

    Set-Content -LiteralPath $Path -Value $Content -Encoding UTF8
    Write-Host "  [file] $Path" -ForegroundColor Green
}

$root = $RootPath
Write-Host "`nBuilding automation structure at: $root`n" -ForegroundColor Cyan

if (-not (Test-Path -LiteralPath $root)) {
    New-Item -ItemType Directory -Path $root -Force | Out-Null
}

# ---------------------------------------------------------------------------
# .github/workflows/algo-evaluation-pipeline.yml
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root '.github/workflows/algo-evaluation-pipeline.yml') @'
name: Algorithm Evaluation Pipeline

on:
  pull_request:
    paths:
      - "algorithms/**"
      - "scripts/algorithms/**"
      - "vitest.config.ts"
  push:
    branches: [main]
    paths:
      - "algorithms/**"
      - "scripts/algorithms/**"

jobs:
  validate:
    name: Validate & Benchmark
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Type-check
        run: npx tsc --noEmit

      - name: Run test suite
        run: npx vitest run --reporter=verbose

      - name: Run benchmarks
        run: npx ts-node scripts/algorithms/benchmark.ts

      - name: Regenerate progress report
        run: npx ts-node scripts/algorithms/generate-report.ts

      - name: Upload benchmark results
        uses: actions/upload-artifact@v4
        with:
          name: benchmark-results
          path: reports/benchmarks/*.json
          if-no-files-found: ignore

      - name: Check for uncommitted report changes
        run: |
          if [ -n "$(git status --porcelain docs/algorithms/progress.md)" ]; then
            echo "::warning::progress.md is out of date. Run scripts/algorithms/generate-report.ts and commit the result."
          fi
'@

# ---------------------------------------------------------------------------
# scripts/algorithms/benchmark.ts
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root 'scripts/algorithms/benchmark.ts') @'
/**
 * benchmark.ts
 *
 * Profiles execution time and heap allocation for every solution.ts found
 * under algorithms/**. Each solution module is expected to export a default
 * (or named) function plus an optional `benchmarkInput` export used to
 * invoke it. Results are written to reports/benchmarks/<timestamp>.json.
 *
 * Usage:
 *   npx ts-node scripts/algorithms/benchmark.ts
 *   npx ts-node scripts/algorithms/benchmark.ts --category=graphs
 *   npx ts-node scripts/algorithms/benchmark.ts --iterations=500
 */

import { performance } from "node:perf_hooks";
import { readdirSync, statSync, mkdirSync, writeFileSync } from "node:fs";
import { join, relative } from "node:path";
import { pathToFileURL } from "node:url";

interface BenchmarkResult {
  problem: string;
  category: string;
  iterations: number;
  avgTimeMs: number;
  minTimeMs: number;
  maxTimeMs: number;
  heapUsedDeltaKb: number;
}

const ALGO_ROOT = join(process.cwd(), "algorithms");
const REPORT_DIR = join(process.cwd(), "reports", "benchmarks");
const DEFAULT_ITERATIONS = 100;

function parseArg(name: string, fallback: string): string {
  const flag = process.argv.find((arg) => arg.startsWith(`--${name}=`));
  return flag ? flag.split("=")[1] : fallback;
}

function findSolutionFiles(dir: string): string[] {
  const results: string[] = [];
  for (const entry of readdirSync(dir)) {
    const fullPath = join(dir, entry);
    const stats = statSync(fullPath);
    if (stats.isDirectory()) {
      results.push(...findSolutionFiles(fullPath));
    } else if (entry === "solution.ts") {
      results.push(fullPath);
    }
  }
  return results;
}

async function benchmarkSolution(
  filePath: string,
  iterations: number
): Promise<BenchmarkResult | null> {
  const mod = await import(pathToFileURL(filePath).href);
  const fn: unknown = mod.default ?? Object.values(mod).find((v) => typeof v === "function");
  const input: unknown[] = Array.isArray(mod.benchmarkInput) ? mod.benchmarkInput : [];

  if (typeof fn !== "function") {
    console.warn(`  [skip] ${filePath} — no callable export found`);
    return null;
  }

  const relPath = relative(ALGO_ROOT, filePath);
  const [category, problem] = relPath.split(/[\\/]/);

  const timings: number[] = [];
  const heapBefore = process.memoryUsage().heapUsed;

  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    fn(...input);
    timings.push(performance.now() - start);
  }

  const heapAfter = process.memoryUsage().heapUsed;

  return {
    problem,
    category,
    iterations,
    avgTimeMs: Number((timings.reduce((a, b) => a + b, 0) / timings.length).toFixed(4)),
    minTimeMs: Number(Math.min(...timings).toFixed(4)),
    maxTimeMs: Number(Math.max(...timings).toFixed(4)),
    heapUsedDeltaKb: Number(((heapAfter - heapBefore) / 1024).toFixed(2)),
  };
}

async function main() {
  const categoryFilter = parseArg("category", "");
  const iterations = Number(parseArg("iterations", String(DEFAULT_ITERATIONS)));

  console.log("Discovering solution files...");
  let files = findSolutionFiles(ALGO_ROOT);

  if (categoryFilter) {
    files = files.filter((f) => f.includes(`${categoryFilter}${require("node:path").sep}`));
  }

  console.log(`Benchmarking ${files.length} solution(s) with ${iterations} iterations each...\n`);

  const results: BenchmarkResult[] = [];

  for (const file of files) {
    try {
      const result = await benchmarkSolution(file, iterations);
      if (result) {
        results.push(result);
        console.log(
          `  [ok] ${result.category}/${result.problem} — avg ${result.avgTimeMs}ms, heap Δ ${result.heapUsedDeltaKb}KB`
        );
      }
    } catch (err) {
      console.error(`  [fail] ${file}:`, (err as Error).message);
    }
  }

  mkdirSync(REPORT_DIR, { recursive: true });
  const outFile = join(REPORT_DIR, `${Date.now()}.json`);
  writeFileSync(outFile, JSON.stringify(results, null, 2), "utf-8");

  console.log(`\nBenchmark report written to: ${outFile}`);
}

main().catch((err) => {
  console.error("Benchmark run failed:", err);
  process.exit(1);
});
'@

# ---------------------------------------------------------------------------
# scripts/algorithms/generate-report.ts
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root 'scripts/algorithms/generate-report.ts') @'
/**
 * generate-report.ts
 *
 * Scans algorithms/** and rewrites docs/algorithms/progress.md with an
 * up-to-date count of solved problems per category. Difficulty is read
 * from an optional `difficulty:` line in each problem's README.md
 * (expected values: Easy | Medium | Hard); problems without a tag are
 * counted as "Untagged" and still contribute to the category total.
 *
 * Usage:
 *   npx ts-node scripts/algorithms/generate-report.ts
 */

import { readdirSync, statSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const ALGO_ROOT = join(process.cwd(), "algorithms");
const PROGRESS_FILE = join(process.cwd(), "docs", "algorithms", "progress.md");

type Difficulty = "Easy" | "Medium" | "Hard" | "Untagged";

interface CategoryStats {
  category: string;
  Easy: number;
  Medium: number;
  Hard: number;
  Untagged: number;
  total: number;
}

function detectDifficulty(readmePath: string): Difficulty {
  if (!existsSync(readmePath)) return "Untagged";
  const content = readFileSync(readmePath, "utf-8");
  const match = content.match(/difficulty:\s*(Easy|Medium|Hard)/i);
  if (!match) return "Untagged";
  const value = match[1][0].toUpperCase() + match[1].slice(1).toLowerCase();
  return value as Difficulty;
}

function collectStats(): CategoryStats[] {
  const categories = readdirSync(ALGO_ROOT).filter((entry) =>
    statSync(join(ALGO_ROOT, entry)).isDirectory()
  );

  return categories
    .sort()
    .map((category) => {
      const categoryPath = join(ALGO_ROOT, category);
      const problems = readdirSync(categoryPath).filter((entry) =>
        statSync(join(categoryPath, entry)).isDirectory()
      );

      const stats: CategoryStats = {
        category,
        Easy: 0,
        Medium: 0,
        Hard: 0,
        Untagged: 0,
        total: 0,
      };

      for (const problem of problems) {
        const solutionExists = existsSync(join(categoryPath, problem, "solution.ts"));
        if (!solutionExists) continue;

        const difficulty = detectDifficulty(join(categoryPath, problem, "README.md"));
        stats[difficulty] += 1;
        stats.total += 1;
      }

      return stats;
    });
}

function renderMarkdown(stats: CategoryStats[]): string {
  const lines: string[] = [];
  lines.push("# Progress Dashboard");
  lines.push("");
  lines.push("| Category | Easy | Medium | Hard | Total |");
  lines.push("|---|---|---|---|---|");

  for (const row of stats) {
    lines.push(
      `| ${row.category} | ${row.Easy} | ${row.Medium} | ${row.Hard} | ${row.total} |`
    );
  }

  const grandTotal = stats.reduce((sum, row) => sum + row.total, 0);
  lines.push("");
  lines.push(`**Total problems solved:** ${grandTotal}`);
  lines.push("");
  lines.push(
    `_Updated automatically by scripts/algorithms/generate-report.ts on ${new Date().toISOString().split("T")[0]}_`
  );

  return lines.join("\n");
}

function main() {
  const stats = collectStats();
  const markdown = renderMarkdown(stats);
  writeFileSync(PROGRESS_FILE, markdown, "utf-8");
  console.log(`progress.md regenerated at: ${PROGRESS_FILE}`);
}

main();
'@

# ---------------------------------------------------------------------------
# scripts/algorithms/test-all.ps1
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root 'scripts/algorithms/test-all.ps1') @'
<#
.SYNOPSIS
    Local runner for the full Vitest test suite plus benchmarking, with
    formatted console output.

.PARAMETER SkipBenchmark
    Skip the benchmark.ts pass and only run tests.

.PARAMETER Category
    Restrict benchmarking to a single algorithm category (e.g. "graphs").

.PARAMETER Iterations
    Number of benchmark iterations per solution. Defaults to 100.

.EXAMPLE
    .\test-all.ps1
    .\test-all.ps1 -Category "dynamic-programming" -Iterations 250
    .\test-all.ps1 -SkipBenchmark
#>

param(
    [switch]$SkipBenchmark,
    [string]$Category = "",
    [int]$Iterations = 100
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "../..")
Push-Location $repoRoot

try {
    Write-Host "==> Running Vitest suite" -ForegroundColor Cyan
    npx vitest run --reporter=verbose
    if ($LASTEXITCODE -ne 0) {
        throw "Vitest suite failed with exit code $LASTEXITCODE"
    }

    if (-not $SkipBenchmark) {
        Write-Host "`n==> Running benchmarks" -ForegroundColor Cyan

        $benchArgs = @("scripts/algorithms/benchmark.ts", "--iterations=$Iterations")
        if ($Category) {
            $benchArgs += "--category=$Category"
        }

        npx ts-node @benchArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Benchmark run failed with exit code $LASTEXITCODE"
        }
    }

    Write-Host "`nAll checks completed successfully." -ForegroundColor Green
}
finally {
    Pop-Location
}
'@

# ---------------------------------------------------------------------------
# scripts/algorithms/create-problem.ps1  (expanded, with benchmark template)
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root 'scripts/algorithms/create-problem.ps1') @'
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
'@

# ---------------------------------------------------------------------------
# vitest.config.ts (with performance profiling)
# ---------------------------------------------------------------------------

New-FileWithContent (Join-Path $root 'vitest.config.ts') @'
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["algorithms/**/*.test.ts", "fullstack/**/*.test.ts"],
    environment: "node",
    globals: false,

    // Performance profiling
    benchmark: {
      include: ["algorithms/**/*.bench.ts"],
      reporters: ["verbose"],
      outputJson: "reports/benchmarks/vitest-bench.json",
    },

    coverage: {
      provider: "v8",
      reporter: ["text", "html", "json-summary"],
      reportsDirectory: "reports/coverage",
    },

    // Surface slow tests so regressions in algorithmic complexity are
    // visible directly in CI output rather than only in benchmark.ts.
    slowTestThreshold: 200,

    reporters: ["default"],
    outputFile: {
      json: "reports/vitest-results.json",
    },
  },
});
'@

Write-Host "`nAutomation structure created successfully at: $root`n" -ForegroundColor Cyan