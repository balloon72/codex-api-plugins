$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$marketplacePath = Join-Path $repoRoot '.agents\plugins\marketplace.json'
$githubPluginManifest = Join-Path $repoRoot 'plugins\github-gh\.codex-plugin\plugin.json'
$gitlabPluginManifest = Join-Path $repoRoot 'plugins\gitlab-mcp\.codex-plugin\plugin.json'
$gitlabMcpConfig = Join-Path $repoRoot 'plugins\gitlab-mcp\.mcp.json'
$fetchComments = Join-Path $repoRoot 'plugins\github-gh\skills\gh-address-comments\scripts\fetch_comments.py'
$inspectChecks = Join-Path $repoRoot 'plugins\github-gh\skills\gh-fix-ci\scripts\inspect_pr_checks.py'

$marketplace = Get-Content -LiteralPath $marketplacePath -Raw | ConvertFrom-Json
$null = Get-Content -LiteralPath $githubPluginManifest -Raw | ConvertFrom-Json
$null = Get-Content -LiteralPath $gitlabPluginManifest -Raw | ConvertFrom-Json
$gitlabMcp = Get-Content -LiteralPath $gitlabMcpConfig -Raw | ConvertFrom-Json

if ($marketplace.plugins.name -notcontains 'github-gh') {
    throw "Marketplace is missing github-gh."
}

if ($marketplace.plugins.name -notcontains 'gitlab-mcp') {
    throw "Marketplace is missing gitlab-mcp."
}

if (-not $gitlabMcp.mcpServers.'gitlab-mcp') {
    throw "GitLab MCP config is missing the gitlab-mcp server entry."
}

python -m py_compile $fetchComments $inspectChecks
if ($LASTEXITCODE -ne 0) {
    throw "Python compile validation failed."
}

@(
    'README.md',
    'docs\install.md',
    'docs\usage\github-gh.md',
    'docs\usage\gitlab-mcp.md',
    'docs\troubleshooting.md',
    'docs\development.md',
    'scripts\install-home-local.ps1',
    'plugins\gitlab-mcp\.mcp.json',
    'plugins\gitlab-mcp\.codex-plugin\plugin.json',
    'plugins\gitlab-mcp\skills\gitlab\SKILL.md',
    'plugins\gitlab-mcp\skills\gitlab-review\SKILL.md',
    'plugins\gitlab-mcp\skills\gitlab-pipeline\SKILL.md'
) | ForEach-Object {
    $full = Join-Path $repoRoot $_
    if (-not (Test-Path $full)) {
        throw "Missing required file: $full"
    }
}

Write-Host 'Repository validation passed.'
