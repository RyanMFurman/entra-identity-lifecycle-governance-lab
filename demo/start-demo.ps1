#Requires -Version 7.4
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
Write-Host 'LOCAL IDENTITY GOVERNANCE SIMULATOR - SYNTHETIC DATA'
python --version
python -m automation.lab demo
exit $LASTEXITCODE
