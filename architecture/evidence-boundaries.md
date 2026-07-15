# Evidence Boundaries

| Classification | Use in this repository |
|---|---|
| `IMPLEMENTED LOCALLY` | Code or controls executed and verified against the local digital twin |
| `IMPLEMENTED IN AUTHORIZED TENANT/LAB` | Approved tenant execution with sanitized request/result evidence and post-change verification |
| `DESIGNED FOR ENTRA` | Microsoft-aligned architecture or configuration not verified in an authorized tenant |
| `DESIGNED FOR CYBERARK` | Not applicable to Entra artifacts; reserved for the separate PAM repository |
| `SIMULATED INVESTIGATION` | Analysis produced from explicitly synthetic events and state |
| `FUTURE PRODUCTION VALIDATION` | Behavior, licensing, integration, or scale requiring later platform validation |

## Promotion rule

An artifact cannot be relabeled as `IMPLEMENTED IN AUTHORIZED TENANT/LAB` merely because code exists or a dry run succeeds. Promotion requires authorization, identity and permission preflight, successful execution, sanitized correlation metadata, independent post-change verification, and an auditable record of the tested environment and limitations.
