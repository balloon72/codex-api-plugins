param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

function Convert-ToCodexSourcePath {
    param([string]$PathValue)

    $resolved = (Resolve-Path $PathValue).Path
    if ($resolved.StartsWith('\\?\')) {
        return $resolved
    }
    return '\\?\' + $resolved
}

function Upsert-TomlBlock {
    param(
        [string]$Content,
        [string]$Header,
        [string]$Block
    )

    $escapedHeader = [regex]::Escape($Header)
    $pattern = "(?ms)^\Q$Header\E\s*`r?`n.*?(?=^\[[^\]]+\]|`z)"
    if ([regex]::IsMatch($Content, $pattern)) {
        return [regex]::Replace($Content, $pattern, $Block.TrimEnd() + "`r`n`r`n")
    }

    $trimmed = $Content.TrimEnd()
    if ([string]::IsNullOrWhiteSpace($trimmed)) {
        return $Block.TrimEnd() + "`r`n"
    }
    return $trimmed + "`r`n`r`n" + $Block.TrimEnd() + "`r`n"
}

$configDir = Join-Path $HOME '.codex'
$configPath = Join-Path $configDir 'config.toml'
if (-not (Test-Path $configPath)) {
    throw "Codex config not found at $configPath"
}

$backupPath = "$configPath.bak.$((Get-Date).ToUniversalTime().ToString('yyyyMMddHHmmss'))"
Copy-Item -LiteralPath $configPath -Destination $backupPath -Force

$sourcePath = Convert-ToCodexSourcePath -PathValue $RepoRoot
$timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')

$marketplaceBlock = @"
[marketplaces.codex-api-plugins]
last_updated = "$timestamp"
source_type = "local"
source = '$sourcePath'
"@

$pluginBlock = @'
[plugins."github-gh@codex-api-plugins"]
enabled = true
'@

$content = Get-Content -LiteralPath $configPath -Raw
$content = Upsert-TomlBlock -Content $content -Header '[marketplaces.codex-api-plugins]' -Block $marketplaceBlock
$content = Upsert-TomlBlock -Content $content -Header '[plugins."github-gh@codex-api-plugins"]' -Block $pluginBlock

Set-Content -LiteralPath $configPath -Value $content -Encoding utf8

Write-Host "Updated $configPath"
Write-Host "Backup created at $backupPath"
Write-Host "Marketplace source: $sourcePath"
Write-Host "Enabled plugin: github-gh@codex-api-plugins"
Write-Host "Restart Codex Desktop to refresh the plugin list."
