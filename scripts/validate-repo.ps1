$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$marketplacePath = Join-Path $repoRoot '.agents\plugins\marketplace.json'
$pluginManifest = Join-Path $repoRoot 'plugins\github-gh\.codex-plugin\plugin.json'
$fetchComments = Join-Path $repoRoot 'plugins\github-gh\skills\gh-address-comments\scripts\fetch_comments.py'
$inspectChecks = Join-Path $repoRoot 'plugins\github-gh\skills\gh-fix-ci\scripts\inspect_pr_checks.py'

$null = Get-Content -LiteralPath $marketplacePath -Raw | ConvertFrom-Json
$null = Get-Content -LiteralPath $pluginManifest -Raw | ConvertFrom-Json

python -m py_compile $fetchComments $inspectChecks
if ($LASTEXITCODE -ne 0) {
    throw "Python compile validation failed."
}

@(
    'README.md',
    'docs\install.md',
    'docs\usage\github-gh.md',
    'docs\troubleshooting.md',
    'docs\development.md',
    'scripts\install-home-local.ps1'
) | ForEach-Object {
    $full = Join-Path $repoRoot $_
    if (-not (Test-Path $full)) {
        throw "Missing required file: $full"
    }
}

Write-Host 'Repository validation passed.'
