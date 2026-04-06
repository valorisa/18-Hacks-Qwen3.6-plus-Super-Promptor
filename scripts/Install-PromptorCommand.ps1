<#
.SYNOPSIS
  Injecte automatiquement la matrice Promptor dans opencode.json via le slash command /promptor.
.DESCRIPTION
  - Lit la matrice depuis un fichier texte
  - Sauvegarde l'original avant modification
  - Met à jour le JSON en préservant la config existante
  - Utilise l'échappement natif PowerShell (zéro risque de corruption JSON)
.EXAMPLE
  .\Install-PromptorCommand.ps1
.EXAMPLE
  .\Install-PromptorCommand.ps1 -MatrixFile ".\custom_promptor.md"
#>

[CmdletBinding()]
param(
    [string]$MatrixFile = "$env:USERPROFILE\.config\opencode\.promptor_starter.md",
    [string]$ConfigFile = "$env:USERPROFILE\.config\opencode\opencode.json"
)

$ErrorActionPreference = "Stop"

try {
    Write-Host "🔍 Vérification des prérequis..." -ForegroundColor Cyan

    if (-not (Test-Path $MatrixFile)) {
        throw "Fichier matrice introuvable : $MatrixFile"
    }

    if (-not (Test-Path $ConfigFile)) {
        Write-Host "⚠️ opencode.json introuvable. Création d'une structure de base..." -ForegroundColor Yellow
        $configDir = Split-Path $ConfigFile -Parent
        if (-not (Test-Path $configDir)) { New-Item -ItemType Directory -Path $configDir -Force | Out-Null }
        @'
{
  "$schema": "https://opencode.ai/config.json",
  "provider": { "openrouter": { "options": { "apiKey": "{env:OPENROUTER_API_KEY}" } } },
  "model": "openrouter/qwen/qwen3.6-plus-preview:free"
}
'@ | Set-Content -Path $ConfigFile -Encoding utf8
    }

    Write-Host "📖 Lecture de la matrice..." -ForegroundColor Cyan
    $rawMatrix = Get-Content -Path $MatrixFile -Raw

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "$ConfigFile.backup_$timestamp.json"
    Copy-Item -Path $ConfigFile -Destination $backupPath
    Write-Host "💾 Sauvegarde créée : $backupPath" -ForegroundColor Green

    Write-Host "⚙️ Mise à jour de opencode.json..." -ForegroundColor Cyan
    $config = Get-Content -Path $ConfigFile -Raw | ConvertFrom-Json

    if (-not ($config.PSObject.Properties.Name -match 'command')) {
        $config | Add-Member -NotePropertyName 'command' -NotePropertyValue ([ordered]@{})
    }

    $config.command | Add-Member -NotePropertyName 'promptor' -NotePropertyValue ([ordered]@{
        'template'    = $rawMatrix
        'description' = 'Active la matrice expert Promptor (Reverse Engineering & optimisation)'
    }) -Force

    $config | ConvertTo-Json -Depth 10 | Set-Content -Path $ConfigFile -Encoding utf8

    Write-Host "✅ Matrice injectée avec succès !" -ForegroundColor Green
    Write-Host "🚀 Lance 'opencode' et tape '/promptor' pour activer le mode." -ForegroundColor Magenta
}
catch {
    Write-Host "❌ Échec : $($_.Exception.Message)" -ForegroundColor Red
    if (Test-Path $backupPath) {
        Copy-Item -Path $backupPath -Destination $ConfigFile -Force
        Write-Host "💾 Fichier original restauré." -ForegroundColor Green
    }
    exit 1
}
