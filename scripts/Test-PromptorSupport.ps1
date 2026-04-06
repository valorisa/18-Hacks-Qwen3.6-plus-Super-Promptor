<#
.SYNOPSIS
  Vérifie si ta version d'OpenCode supporte les slash commands personnalisés.
.DESCRIPTION
  - Affiche la version OpenCode
  - Teste la validité du JSON de config
  - Indique la méthode d'activation recommandée
.EXAMPLE
  .\Test-PromptorSupport.ps1
#>

[CmdletBinding()]
param([string]$ConfigFile = "$env:USERPROFILE\.config\opencode\opencode.json")

Write-Host "🔍 Vérification support /promptor..." -ForegroundColor Cyan

try {
    $version = (opencode --version 2>$null) -join " "
    Write-Host "📦 Version OpenCode : $version"

    if (Test-Path $ConfigFile) {
        $config = Get-Content -Path $ConfigFile -Raw | ConvertFrom-Json
        if ($config.PSObject.Properties.Name -match 'command' -and $config.command.promptor) {
            Write-Host "✅ Config 'promptor' détectée dans opencode.json" -ForegroundColor Green
        } else {
            Write-Host "ℹ️ Aucune commande 'promptor' trouvée dans la config." -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Fichier opencode.json introuvable." -ForegroundColor Yellow
    }

    Write-Host "`n💡 Pour tester /promptor : lance 'opencode' puis tape '/promptor'" -ForegroundColor Yellow
    Write-Host "💡 Si échec, utilise : @~/.config/opencode/.promptor_starter.md" -ForegroundColor Yellow
}
catch {
    Write-Host "❌ Erreur lors du test : $($_.Exception.Message)" -ForegroundColor Red
}
