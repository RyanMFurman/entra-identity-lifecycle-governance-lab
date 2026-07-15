# Expired Contractor Investigation

Evidence: `SIMULATED INVESTIGATION`.

Evan Cole is a deterministic synthetic contractor whose end date passed while the local identity remained enabled. Synthetic events additionally model a risky sign-in, sensitive SharePoint access, application consent, guest access, and privileged-role activation.

## Evidence distinctions

| Claim | Status |
|---|---|
| Lifecycle control failed | Confirmed in local state |
| Authentication occurred | Simulated sign-in event only |
| SharePoint resource access | Simulated audit event only |
| Privileged activation | Simulated governance event only |
| Credential compromise | Suspicion, not confirmed |
| Malicious misuse | Not confirmed |

## Investigation sequence

1. Detect expired active contractor and retained entitlement.
2. Correlate identity, sign-in, audit, consent, and role-activation timestamps.
3. Confirm source-of-truth end date and search for an approved extension.
4. Contain by disabling the identity and removing entitlements.
5. Recommend session revocation and application-consent review.
6. Recalculate state and verify no active entitlement remains.

## Search surfaces

Microsoft Sentinel KQL, adapted to the connected table schema:

```kusto
SigninLogs
| where UserPrincipalName == "synthetic.contractor@northstar.example"
| project TimeGenerated, UserPrincipalName, AppDisplayName, IPAddress, ResultType, RiskLevelDuringSignIn
```

Microsoft 365 Audit/Sentinel `OfficeActivity` example:

```kusto
OfficeActivity
| where UserId == "synthetic.contractor@northstar.example"
| project TimeGenerated, OfficeWorkload, Operation, Site_Url, UserId
```

Microsoft Graph targets `/auditLogs/signIns`, `/auditLogs/directoryAudits`, and `/oauth2PermissionGrants`. Purview eDiscovery uses KeyQL rather than KQL; examples must not be copied between surfaces.

## Root cause and lessons

The local root cause is a missed expiration-state transition. The corrective action is scheduled expiration validation, atomic disablement and access removal, exception ownership, and verification using the same policy engine that detected the failure.
