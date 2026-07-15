#Requires -Version 7.4
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
python -m automation.lab demo
exit $LASTEXITCODE
