#Requires -Version 7.4
<#[.SYNOPSIS]
Performs read-only Microsoft Entra capability discovery for an authorized tenant.
.DESCRIPTION
Uses delegated Microsoft Graph scopes and writes only sanitized capability metadata.
It does not create, update, or delete tenant objects.
#>
[CmdletBinding()]
param(
    [string]$TenantId,
    [switch]$UseDeviceAuthentication
)
$ErrorActionPreference = 'Stop'
$scopes = @('User.Read','Organization.Read.All')
$connect = @{ Scopes = $scopes; NoWelcome = $true }
if ($TenantId) { $connect.TenantId = $TenantId }
if ($UseDeviceAuthentication) { $connect.UseDeviceAuthentication = $true }
Connect-MgGraph @connect
$context = Get-MgContext
try {
    $organizationResponse = Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/organization?$select=id,displayName,verifiedDomains,assignedPlans'
}
catch {
    if ($_.Exception.Message -match 'not supported for MSA accounts') {
        Disconnect-MgGraph | Out-Null
        throw 'A personal Microsoft account was selected. Find the Directory (tenant) ID in Microsoft Entra ID > Overview, then rerun this script with -TenantId. Sign in with an account that exists in or is authorized for that directory.'
    }
    throw
}
$organization = @($organizationResponse.value)[0]
$result = [ordered]@{
    evidence_classification = 'IMPLEMENTED IN AUTHORIZED TENANT/LAB'
    operation = 'read-only capability discovery'
    tenant_id = $context.TenantId
    account = $context.Account
    scopes = $context.Scopes
    organization = $organization.displayName
    verified_domain_count = @($organization.verifiedDomains).Count
    assigned_plan_count = @($organization.assignedPlans).Count
    discovered_at_utc = [DateTime]::UtcNow.ToString('o')
}
$output = Join-Path $PSScriptRoot '..\..\generated\authorized-entra'
New-Item -ItemType Directory -Path $output -Force | Out-Null
$result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $output 'capabilities.json') -Encoding utf8
$result | Format-List
Write-Warning 'Review generated output before sharing; tenant and account identifiers are intentionally excluded from Git.'
