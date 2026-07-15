#Requires -Version 7.4
[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
python -m automation.lab demo
if ($LASTEXITCODE) { exit $LASTEXITCODE }
python -m automation.controls ca config/conditional-access/safe.json
if ($LASTEXITCODE) { exit $LASTEXITCODE }
python -m automation.controls governance config/governance.json
if ($LASTEXITCODE) { exit $LASTEXITCODE }
python -m automation.controls ca config/conditional-access/unsafe.json
if ($LASTEXITCODE -ne 2) { Write-Error 'Unsafe Conditional Access fixture did not fail with exit code 2.'; exit 5 }
python -m automation.controls apps config/applications.json
if ($LASTEXITCODE -ne 2) { Write-Error 'Unsafe application fixture did not fail with exit code 2.'; exit 6 }
python -m automation.evidence_site
Write-Host 'FULL DEMO PASS: lifecycle, governance, Conditional Access, and application controls behaved as expected.' -ForegroundColor Green
exit 0
