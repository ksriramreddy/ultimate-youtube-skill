# Install the Ultimate YouTube skill for Claude Code (Windows PowerShell).
#   .\install.ps1            -> %USERPROFILE%\.claude\skills\ultimate-youtube (all projects)
#   .\install.ps1 -Project   -> .\.claude\skills\ultimate-youtube (current project only)
param([switch]$Project)

$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "skills\ultimate-youtube"
if (-not (Test-Path (Join-Path $src "SKILL.md"))) {
    Write-Error "Run this from the repository root (SKILL.md not found at $src)"
}

if ($Project) {
    $dest = Join-Path (Get-Location) ".claude\skills\ultimate-youtube"
} else {
    $dest = Join-Path $env:USERPROFILE ".claude\skills\ultimate-youtube"
}

New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
if (Test-Path $dest) {
    Write-Host "Updating existing install at $dest"
    Remove-Item -Recurse -Force $dest
}
Copy-Item -Recurse $src $dest
Get-ChildItem $dest -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Write-Host "Installed skill to $dest"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "uv found: scripts can run with 'uv run' and need no pip install."
} else {
    $py = Get-Command python -ErrorAction SilentlyContinue
    if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
    if (-not $py) {
        Write-Warning "Python 3.10+ not found. Install Python, then: pip install -r `"$dest\requirements.txt`""
    } else {
        Write-Host "Installing Python dependencies with $($py.Source) ..."
        & $py.Source -m pip install --user -r (Join-Path $dest "requirements.txt")
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "pip install failed. Try a virtualenv, or install uv (https://docs.astral.sh/uv/)."
        }
    }
}

Write-Host ""
Write-Host 'Next: open Claude Code and say "set up the YouTube skill".'
