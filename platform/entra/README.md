# Authorized Entra Connection

Evidence before execution: `DESIGNED FOR ENTRA`. Successful read-only discovery in your approved tenant: `IMPLEMENTED IN AUTHORIZED TENANT/LAB`.

Prerequisites: PowerShell 7, the installed Microsoft Graph modules, an Entra account authorized to consent to `User.Read` and `Organization.Read.All`, and permission from the tenant owner.

```powershell
pwsh ./platform/entra/Connect-EntraLab.ps1
```

If the WAM browser window is hidden or unavailable, use device authentication:

```powershell
pwsh ./platform/entra/Connect-EntraLab.ps1 -TenantId 'your-tenant-id' -UseDeviceAuthentication
```

For a reusable local configuration, create `platform/entra/tenant.local.json` containing `{"tenant_id":"your-tenant-id"}`. The filename is gitignored, and the connector will use it automatically when `-TenantId` is omitted.

If you know the tenant ID, use `-TenantId`. The script performs discovery only and writes sanitized output below gitignored `generated/authorized-entra/`. Inspect that output before sharing it. Do not commit tenant IDs, account names, access tokens, or exported directory data.

If Graph reports that the organization API is unsupported for an MSA account, the personal Microsoft account was authenticated outside an Entra directory context. In the Azure portal, open **Microsoft Entra ID > Overview**, copy the **Tenant ID**, disconnect the current Graph session, and rerun with `-TenantId`. An Azure subscription associated only with a personal account is not by itself sufficient for organization-level Microsoft Graph queries.

Advanced PIM, access reviews, entitlement management, Identity Protection, and Conditional Access depend on tenant roles and licenses. They must be discovered and approved separately before any mutation adapter is enabled.
