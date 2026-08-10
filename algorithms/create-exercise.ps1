<#
.SYNOPSIS
    Creates an exercise workspace by copying an existing problem folder from algorithms/ into an exercise/ tree.

.PARAMETER SourcePath
    Relative path to the source problem, e.g. "arrays/two-sum".

.PARAMETER DestinationFolderName
    Name of the folder that will receive the copied exercise. Defaults to "exercice".
#>

param(
    [Parameter(Mandatory)]
    [string]$SourcePath,

    [string]$DestinationFolderName = "exercice"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$algorithmsRoot = Join-Path $repoRoot "algorithms"
$sourceAbsolutePath = Join-Path $algorithmsRoot $SourcePath
$destinationPath = Join-Path $algorithmsRoot $DestinationFolderName
$destinationExercisePath = Join-Path $destinationPath $SourcePath

if (-not (Test-Path $sourceAbsolutePath -PathType Container)) {
    throw "Source exercise path does not exist: $sourceAbsolutePath"
}

New-Item -ItemType Directory -Path $destinationExercisePath -Force | Out-Null

$copiedFiles = New-Object System.Collections.Generic.List[string]

Get-ChildItem -Path $sourceAbsolutePath -Force | ForEach-Object {
    $destinationItemPath = Join-Path $destinationExercisePath $_.Name

    if ($_.PSIsContainer) {
        Copy-Item -Path $_.FullName -Destination $destinationItemPath -Recurse -Force
        return
    }

    Copy-Item -Path $_.FullName -Destination $destinationItemPath -Force
    $copiedFiles.Add($_.Name)
}

$exerciseDoc = @"
# Exercise Copy

Source: $SourcePath

## Goal
Create a working copy of the problem scaffold for hands-on practice and verification.

## Suggested Workflow
1. Review the problem statement and constraints.
2. Implement the solution in the copied source files.
3. Run the tests and measure complexity.
4. Document the approach and performance trade-offs.
"@

Set-Content -Path (Join-Path $destinationExercisePath "exercise.md") -Value $exerciseDoc -Encoding UTF8
$copiedFiles.Add("exercise.md")

Write-Host "Exercise scaffold created at: $destinationExercisePath" -ForegroundColor Green
Write-Host "Copied files: $($copiedFiles -join ', ')" -ForegroundColor Cyan
