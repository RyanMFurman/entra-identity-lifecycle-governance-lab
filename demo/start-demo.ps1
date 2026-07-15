#Requires -Version 7.4
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
Write-Host 'LOCAL IDENTITY GOVERNANCE SIMULATOR - SYNTHETIC DATA'
python --version
& (Join-Path $PSScriptRoot 'run-demo.ps1')
exit $LASTEXITCODE
