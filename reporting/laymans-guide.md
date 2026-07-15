# Plain-English Project Guide

## What problem does this solve?

When an employee changes jobs, companies often give them new access but forget to remove the old access. That creates security risk. This project proves that I can identify the correct access, detect leftover access, investigate why it happened, remove it, and verify the person is compliant afterward.

## What happens in the demonstration?

Jasmine Reed is a synthetic employee who moves from Finance to Engineering. The workflow intentionally leaves her with sensitive Finance access. The system catches the mistake, explains the risk, removes the Finance access, and reruns the same check to prove the issue is fixed.

The second synthetic scenario finds a contractor whose end date passed while the identity remained active. Remediation disables the contractor and removes the local entitlements.

## What did I build?

- A reproducible identity system using Python, PowerShell, SQLite, and versioned JSON policy.
- Joiner, mover, expiration, access-calculation, audit, detection, investigation, remediation, and reset workflows.
- Passing, failing, and boundary tests that run locally and in GitHub Actions.
- Conditional Access, governance, and application-control validators with intentionally unsafe examples.
- A reversible authorized Entra extension using disabled synthetic users and groups.

## What is real versus simulated?

The local automation, tests, database changes, reports, and authorized Entra user/group scenario were executed. The contractor investigation uses clearly labeled synthetic evidence. Premium capabilities unavailable in the Entra Free tenant—such as Conditional Access, PIM, access reviews, and entitlement management—are designed and locally validated but not claimed as deployed.

## Why does this matter for an IAM Analyst role?

The project demonstrates access analysis, lifecycle operations, RBAC reasoning, segregation-of-duties detection, evidence handling, remediation, stakeholder reporting, Microsoft Graph fundamentals, PowerShell, Python, testing, and honest control validation.
