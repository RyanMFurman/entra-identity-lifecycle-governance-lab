# Project Status

| Phase | Status | Evidence classification |
|---|---|---|
| 0 — Environment and evidence assessment | Complete | `IMPLEMENTED LOCALLY` |
| 1 — Business and identity architecture | Complete | `DESIGNED FOR ENTRA` |
| 2 — Identity data model and RBAC | Local MVP complete | `IMPLEMENTED LOCALLY` |
| 3 — JML automation | Primary mover and expired-contractor workflows complete | `IMPLEMENTED LOCALLY` |
| 4 — Authentication and Conditional Access | Safe/unsafe specifications and executable validator complete | `IMPLEMENTED LOCALLY` / `DESIGNED FOR ENTRA` |
| 5 — Identity governance | Access-package, review, guest, and PIM specifications with validator complete | `IMPLEMENTED LOCALLY` / `DESIGNED FOR ENTRA` |
| 6 — Applications and workload identities | OIDC, SCIM, ownership, permission, and credential-risk validation complete | `IMPLEMENTED LOCALLY` / `DESIGNED FOR ENTRA` |
| 7 — Automation and validation | Local MVP complete | `IMPLEMENTED LOCALLY` |
| 8 — Investigation | Primary synthetic investigation complete | `SIMULATED INVESTIGATION` |
| 9 — Tests and CI | Seven tests, expected-exit validation, repository quality checks, and GitHub Actions complete | `IMPLEMENTED LOCALLY` |
| 10 — Portfolio polish | Plain-English guide, executive reporting, screenshots, video scripts, and reproducibility evidence complete | Mixed, explicitly labeled |

## Current limitations

- PowerShell 7.6.3 and current-user Pester 6.0.0 are installed.
- Microsoft Graph PowerShell identity modules 2.38.1 are installed; no tenant authentication has been performed.
- Azure CLI 2.88.0 is installed and verified; no Azure authentication has been performed by this project.
- Authorized Entra tenant access, licensing, and Graph permissions are unverified.
- The local MVP is not a complete implementation of every Microsoft Entra feature described in the roadmap; Conditional Access deployment, PIM, access packages, SSO, SCIM, and workload-identity operations require later authorized validation.

The repository must not be described as complete until the Phase 10 clean-room test passes.

## Authorized tenant validation

On 2026-07-15, read-only capability discovery succeeded in an authorized Microsoft Entra ID Free tenant. The reversible authorized lab then created three disabled synthetic `LAB-NSH` users and two synthetic security groups. The live mover scenario created a Finance/Engineering membership conflict, detected `ENTRA-SOD-001`, removed the stale Finance membership, and verified the resulting compliant state. Tenant identifiers and object IDs remain only in gitignored local output.
