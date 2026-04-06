<#
.SYNOPSIS
  Répare opencode.json en supprimant les clés non supportées et en validant la syntaxe.
.DESCRIPTION
  - Crée une sauvegarde automatique
  - Supprime la section "command" si elle cause des erreurs
  - Valide le JSON final
.EXAMPLE
  .\Fix-OpenCodeConfig.ps1
#>

[CmdletBinding()]
param([string]$ConfigFile = "$env:USERPROFILE\.config\opencode\opencode.json")

$ErrorActionPreference = "Stop"

try {
    Write-Host "🔧 Réparation de opencode.json..." -ForegroundColor Cyan

    if (-not (Test-Path $ConfigFile)) {
        throw "Fichier de configuration introuvable : $ConfigFile"
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "$ConfigFile.backup_fix_$timestamp.json"
    Copy-Item -Path $ConfigFile -Destination $backupPath
    Write-Host "💾 Sauvegarde créée : $backupPath" -ForegroundColor Green

    $content = Get-Content -Path $ConfigFile -Raw
    $config = $content | ConvertFrom-Json

    if ($config.PSObject.Properties.Name -match 'command') {
        $config.PSObject.Properties.Remove('command')
        Write-Host "🗑️ Clé 'command' supprimée (non supportée par ta version OpenCode)." -ForegroundColor Yellow
    }

    $config | ConvertTo-Json -Depth 10 | Set-Content -Path $ConfigFile -Encoding utf8
    Write-Host "✅ Configuration réparée et validée !" -ForegroundColor Green
}
catch {
    Write-Host "❌ Échec de la réparation : $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
