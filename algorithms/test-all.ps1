param(
    [string]$TestFile = "",
    [string]$TestName = ""
)

# 1. Résolution stricte de la racine du dépôt
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# 2. Détection dynamique des binaires
$nodeExe = "C:\Program Files\nodejs\node.exe"
$vitestExe = Join-Path $repoRoot "node_modules\.bin\vitest.cmd"
$tsNodeExe = Join-Path $repoRoot "node_modules\.bin\ts-node.cmd"
$tscExe = Join-Path $repoRoot "node_modules\.bin\tsc.cmd"

$env:PATH = "$env:PATH;C:\Program Files\nodejs"

foreach ($exe in @($nodeExe, $vitestExe, $tsNodeExe, $tscExe)) {
    if (-not (Test-Path $exe)) {
        throw "Exécutable introuvable : $exe. Vérifiez l'installation dans $repoRoot."
    }
}

function Invoke-LocalCommand {
    param(
        [Parameter(Mandatory)] [string]$CommandPath,
        [Parameter(Mandatory)] [string[]]$Arguments
    )

    & $CommandPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Commande échouée avec le code d'erreur $LASTEXITCODE : $CommandPath $($Arguments -join ' ')"
    }
}

function Invoke-Vitest {
    param(
        [string[]]$testFile,
        [string]$testName
    )

    $vitestArgs = @("run", "--config", "vitest.config.ts")

    if ($testName -and $testName.Trim() -ne "") {
        $vitestArgs += @("-t", $testName)
    }

    if ($testFile -and $testFile.Count -gt 0) {
        # Normalisation des chemins : conversion des antislashs Windows en slashs POSIX
        $normalizedFiles = $testFile | ForEach-Object { $_.Replace("\", "/") }
        $vitestArgs += $normalizedFiles
    } else {
        $vitestArgs += "algorithms/"
    }

    Invoke-LocalCommand -CommandPath $vitestExe -Arguments $vitestArgs
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     ALGORITHM LABORATORY EVALUATOR    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Push-Location $repoRoot
try {
    # Step 1: Exécution des tests Vitest
    Write-Host "`n[1/3] Exécution des tests automatisés Vitest..." -ForegroundColor Yellow

    if (($TestName -and $TestName.Trim() -ne "") -and (-not $TestFile -or $TestFile.Trim() -eq "")) {
        Write-Host "Recherche des fichiers de test correspondant au motif : $TestName" -ForegroundColor Cyan
        $algoPath = Join-Path $repoRoot "algorithms"

        # Conversion du motif pour cibler les dossiers/fichiers (ex: "two-sum" ou "two sum")
        $cleanPattern = $TestName.ToLower().Replace(" ", "-")

        # 1. Recherche par nom de fichier ou sous-dossier
        $matchesList = Get-ChildItem -Path $algoPath -Recurse -Filter "*.test.ts" -File -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName.ToLower().Contains($cleanPattern) -or $_.Name.ToLower().Contains($cleanPattern) } |
            Select-Object -ExpandProperty FullName

        # 2. Repli : recherche textuelle si aucune correspondance de nom
        if (-not $matchesList -or $matchesList.Count -eq 0) {
            $matchesList = Get-ChildItem -Path $algoPath -Recurse -Filter "*.test.ts" -File -ErrorAction SilentlyContinue |
                Select-String -Pattern $TestName -SimpleMatch -List -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty Path -Unique
        }

        if ($matchesList -and $matchesList.Count -gt 0) {
            $TestFile = $matchesList
            Write-Host "Fichiers de test identifiés :`n$($TestFile -join "`n")" -ForegroundColor Green
        } else {
            Write-Host "Aucun fichier spécifique trouvé pour '$TestName'. Exécution globale avec filtre -t." -ForegroundColor Yellow
        }
    }

    Invoke-Vitest -testFile $TestFile -testName $TestName

    # Step 2: Mise à jour du rapport de progression
    # Write-Host "`n[2/3] Mise à jour du rapport de progression (docs/algorithms/progress.md)..." -ForegroundColor Yellow
    # Invoke-LocalCommand -CommandPath $tsNodeExe -Arguments @("scripts/algorithms/generate-report.ts")

    # Step 2: Mise à jour du rapport de progression (docs/algorithms/progress.md)
    Write-Host "`n[2/3] Mise à jour du rapport de progression (docs/algorithms/progress.md)..." -ForegroundColor Yellow
    
    $reportScript = Join-Path $repoRoot "scripts\algorithms\generate-report.ts"
    $tsConfig = Join-Path $repoRoot "tsconfig.json"

    Invoke-LocalCommand -CommandPath $tsNodeExe -Arguments @("--project", $tsConfig, $reportScript)


    # Step 3: Contrôle de type TypeScript
    Write-Host "`n[3/3] Contrôle de type TypeScript (tsc)..." -ForegroundColor Yellow
    Invoke-LocalCommand -CommandPath $tscExe -Arguments @("--noEmit")
}
finally {
    Pop-Location
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   TOUS LES CONTRÔLES SONT VALIDÉS     " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green