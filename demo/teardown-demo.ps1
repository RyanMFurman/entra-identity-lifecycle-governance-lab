#Requires -Version 7.4
[CmdletBinding(SupportsShouldProcess)] param()
$ErrorActionPreference = 'Stop'
if ($PSCmdlet.ShouldProcess('generated local lab state','Remove')) { python -m automation.lab teardown; exit $LASTEXITCODE }
