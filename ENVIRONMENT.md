# Environment Assessment

Evidence classification: `IMPLEMENTED LOCALLY`

Assessment date: 2026-07-14  
Execution mode: architecture-only local development  
Assessment host: Windows 11 Home, 64-bit

## Tool inventory

| Tool | Observed version/state | Project decision |
|---|---|---|
| Windows PowerShell | 5.1.26100.8875 | Available, not the target runtime |
| PowerShell 7 (`pwsh`) | 7.6.3 | Installed and verified |
| Python | 3.11.9 | Primary supported Python runtime |
| Python launcher | 3.14.0 | Available, not the baseline runtime |
| pip | 25.3 for Python 3.11 | Available |
| Python SQLite | SQLite 3.45.1 | Available; selected local state engine |
| SQLite CLI | Not installed | Optional |
| Git | 2.51.2.windows.1 | Available |
| VS Code | 1.128.1 | Available |
| Azure CLI | 2.88.0 | Installed and verified; optional for local mode and available for authorized discovery |
| Microsoft Graph PowerShell | 2.38.1 identity modules | Installed for the optional authorized adapter; no tenant login performed |
| Microsoft Graph Python SDK | Not installed | Authorized adapter only |
| Pester | 6.0.0 current-user module; Windows PowerShell also retains 3.4.0 | Use PowerShell 7 so Pester 6 is selected |
| Docker | Client 29.2.1; engine stopped | Optional, never a local-demo requirement |
| Docker Compose | 5.0.2 | Optional |
| Make | Not installed | Optional |

## Authorized access

| Capability | Status |
|---|---|
| Authorized Microsoft Entra tenant | Unverified |
| Entra license level | Unverified |
| Microsoft Graph permissions | Unverified |
| Azure subscription | Unverified |

The absence of local tools or environment-variable indicators is not proof that access does not exist. No authentication was attempted during assessment.

## Execution model

Local mode will use deterministic synthetic source feeds, SQLite mutable state, versioned policy configuration, Python policy/analysis code, and PowerShell administration workflows. Authorized Entra execution will be a separate, explicit adapter with no automatic fallback to simulation. The Microsoft Graph modules were installed without authenticating to a tenant.

## Compatibility target

- Windows 11 with PowerShell 7.4+ and Python 3.11
- Ubuntu CI with PowerShell 7 and Python 3.11 is proposed for a later phase
- Paths and commands must remain cross-platform where practical
- Docker and the SQLite command-line client will not be required

## Evidence limitations

No policy, identity, application, role, or integration has been deployed to Microsoft Entra. Architecture artifacts are `DESIGNED FOR ENTRA`. Future local automation can be labeled `IMPLEMENTED LOCALLY` only after execution and testing. Tenant operations can be labeled `IMPLEMENTED IN AUTHORIZED TENANT/LAB` only after approved execution and post-change verification.
