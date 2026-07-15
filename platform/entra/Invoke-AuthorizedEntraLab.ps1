#Requires -Version 7.4
<#
.SYNOPSIS
Deploys, demonstrates, or removes a reversible synthetic Entra lab.
.DESCRIPTION
Creates only disabled users and security groups prefixed with LAB-NSH. Object IDs
are stored under gitignored generated/authorized-entra for safe teardown.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [ValidateSet('Deploy','Demo','Teardown')]
    [string]$Action = 'Deploy',
    [switch]$UseDeviceAuthentication
)
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$localConfigPath = Join-Path $PSScriptRoot 'tenant.local.json'
$outputPath = Join-Path $root 'generated\authorized-entra'
$manifestPath = Join-Path $outputPath 'deployment-manifest.json'
if (-not (Test-Path -LiteralPath $localConfigPath)) { throw 'Missing gitignored tenant.local.json.' }
$tenantId = (Get-Content -Raw -LiteralPath $localConfigPath | ConvertFrom-Json).tenant_id
$scopes = @('User.ReadWrite.All','Group.ReadWrite.All','Organization.Read.All')
$connect = @{ TenantId = $tenantId; Scopes = $scopes; NoWelcome = $true }
if ($UseDeviceAuthentication) { $connect.UseDeviceAuthentication = $true }
Connect-MgGraph @connect

function Get-InitialDomain {
    $response = Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/organization?$select=verifiedDomains'
    $domain = @($response.value[0].verifiedDomains | Where-Object isInitial)[0].name
    if (-not $domain) { throw 'The tenant initial domain could not be discovered.' }
    return $domain
}
function New-RandomPassword {
    $bytes = [byte[]]::new(24)
    [Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
    return ('N5!' + [Convert]::ToBase64String($bytes).Replace('/','x').Replace('+','Y') + 'a9')
}
function Get-LabUser([string]$Upn) {
    return Get-MgUser -Filter "userPrincipalName eq '$Upn'" -ConsistencyLevel eventual -All | Select-Object -First 1
}
function Get-LabGroup([string]$Name) {
    return Get-MgGroup -Filter "displayName eq '$Name'" -ConsistencyLevel eventual -All | Select-Object -First 1
}
function Test-Membership([string]$GroupId,[string]$UserId) {
    return [bool](Get-MgGroupMember -GroupId $GroupId -All | Where-Object Id -eq $UserId)
}

New-Item -ItemType Directory -Path $outputPath -Force | Out-Null

if ($Action -eq 'Deploy') {
    $domain = Get-InitialDomain
    $userSpecs = @(
        @{ alias='lab.alex.morgan'; display='LAB-NSH Alex Morgan (Synthetic Manager)'; department='Management'; title='Finance Director' },
        @{ alias='lab.jasmine.reed'; display='LAB-NSH Jasmine Reed (Synthetic)'; department='Finance'; title='Financial Analyst' },
        @{ alias='lab.evan.cole'; display='LAB-NSH Evan Cole (Synthetic Contractor)'; department='Engineering'; title='Contractor' }
    )
    $users = @{}
    foreach ($spec in $userSpecs) {
        $upn = "$($spec.alias)@$domain"
        $user = Get-LabUser $upn
        if (-not $user -and $PSCmdlet.ShouldProcess($upn,'Create disabled synthetic user')) {
            $profile = @{ Password = New-RandomPassword; ForceChangePasswordNextSignIn = $true }
            $user = New-MgUser -AccountEnabled:$false -DisplayName $spec.display -MailNickname $spec.alias.Replace('.','-') -UserPrincipalName $upn -Department $spec.department -JobTitle $spec.title -PasswordProfile $profile
        }
        if (-not $user) { throw "Synthetic user was not available: $upn" }
        $users[$spec.alias] = @{ id=$user.Id; upn=$upn; display=$spec.display }
    }
    $groupSpecs = @(
        @{ key='finance'; name='LAB-NSH-Finance-Base'; nick='lab-nsh-finance-base' },
        @{ key='engineering'; name='LAB-NSH-Engineering-Base'; nick='lab-nsh-engineering-base' }
    )
    $groups = @{}
    foreach ($spec in $groupSpecs) {
        $group = Get-LabGroup $spec.name
        if (-not $group -and $PSCmdlet.ShouldProcess($spec.name,'Create synthetic security group')) {
            $group = New-MgGroup -DisplayName $spec.name -Description 'Northstar synthetic authorized-lab object; safe to remove via teardown.' -MailEnabled:$false -MailNickname $spec.nick -SecurityEnabled
        }
        if (-not $group) { throw "Synthetic group was not available: $($spec.name)" }
        $groups[$spec.key] = @{ id=$group.Id; name=$spec.name }
    }
    $jasmineId = $users['lab.jasmine.reed'].id
    if (-not (Test-Membership $groups.finance.id $jasmineId)) {
        New-MgGroupMemberByRef -GroupId $groups.finance.id -BodyParameter @{ '@odata.id'="https://graph.microsoft.com/v1.0/directoryObjects/$jasmineId" }
    }
    $manifest = [ordered]@{
        evidence_classification='IMPLEMENTED IN AUTHORIZED TENANT/LAB'
        lab_id='northstar-entra-authorized-v1'
        tenant_id=$tenantId
        domain=$domain
        users=$users
        groups=$groups
        deployed_at_utc=[DateTime]::UtcNow.ToString('o')
    }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
    Write-Host 'AUTHORIZED ENTRA LAB DEPLOYED: 3 disabled synthetic users, 2 security groups, Finance baseline membership.' -ForegroundColor Green
}
elseif ($Action -eq 'Demo') {
    if (-not (Test-Path -LiteralPath $manifestPath)) { throw 'Deploy the authorized lab first.' }
    $m = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
    $jasmine = $m.users.'lab.jasmine.reed'
    Update-MgUser -UserId $jasmine.id -Department 'Engineering' -JobTitle 'Software Engineer'
    if (-not (Test-Membership $m.groups.engineering.id $jasmine.id)) {
        New-MgGroupMemberByRef -GroupId $m.groups.engineering.id -BodyParameter @{ '@odata.id'="https://graph.microsoft.com/v1.0/directoryObjects/$($jasmine.id)" }
    }
    $financeBefore = Test-Membership $m.groups.finance.id $jasmine.id
    $engineeringBefore = Test-Membership $m.groups.engineering.id $jasmine.id
    if (-not ($financeBefore -and $engineeringBefore)) { throw 'Intentional toxic membership was not created.' }
    Write-Host 'DETECTED ENTRA-SOD-001: Jasmine has both Finance and Engineering group access.' -ForegroundColor Yellow
    Remove-MgGroupMemberByRef -GroupId $m.groups.finance.id -DirectoryObjectId $jasmine.id
    $financeAfter = Test-Membership $m.groups.finance.id $jasmine.id
    $engineeringAfter = Test-Membership $m.groups.engineering.id $jasmine.id
    $report = [ordered]@{
        evidence_classification='IMPLEMENTED IN AUTHORIZED TENANT/LAB'
        scenario='authorized-jasmine-mover-v1'
        detected=@{ finance=$financeBefore; engineering=$engineeringBefore; finding='ENTRA-SOD-001' }
        remediated=@{ finance=$financeAfter; engineering=$engineeringAfter; compliant=(-not $financeAfter -and $engineeringAfter) }
        verified_at_utc=[DateTime]::UtcNow.ToString('o')
    }
    $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $outputPath 'authorized-demo-report.json') -Encoding utf8
    if (-not $report.remediated.compliant) { throw 'Post-remediation verification failed.' }
    Write-Host 'AUTHORIZED ENTRA DEMO PASS: failure detected, Finance membership removed, compliant state verified.' -ForegroundColor Green
}
else {
    if (-not (Test-Path -LiteralPath $manifestPath)) { Write-Host 'No authorized deployment manifest found; nothing to remove.'; return }
    $m = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
    foreach ($entry in $m.users.PSObject.Properties.Value) {
        $current = Get-MgUser -UserId $entry.id -ErrorAction SilentlyContinue
        if ($current -and $current.DisplayName -like 'LAB-NSH*' -and $PSCmdlet.ShouldProcess($current.UserPrincipalName,'Remove synthetic user')) { Remove-MgUser -UserId $entry.id }
    }
    foreach ($entry in $m.groups.PSObject.Properties.Value) {
        $current = Get-MgGroup -GroupId $entry.id -ErrorAction SilentlyContinue
        if ($current -and $current.DisplayName -like 'LAB-NSH-*' -and $PSCmdlet.ShouldProcess($current.DisplayName,'Remove synthetic group')) { Remove-MgGroup -GroupId $entry.id }
    }
    Remove-Item -LiteralPath $manifestPath -Force
    Write-Host 'AUTHORIZED ENTRA LAB REMOVED.' -ForegroundColor Green
}
