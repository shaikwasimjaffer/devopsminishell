Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  DevOps Mini Shell - Launch Helper (PowerShell)  " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$projDir = $PSScriptRoot
if (-not $projDir) { $projDir = Get-Location }

try {
    $wslPath = (wsl.exe wslpath -a -u "$projDir").Trim()
    Write-Host "Launching in WSL Ubuntu: $wslPath" -ForegroundColor Green
    wsl.exe -d Ubuntu bash -c "cd '$wslPath' && gcc -Wall -Wextra devops_shell.c -o devops-shell && ./devops-shell"
} catch {
    Write-Host "Error launching via WSL: $_" -ForegroundColor Red
}
