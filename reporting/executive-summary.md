# Executive Summary

Northstar Health Systems needed to prevent access accumulation during workforce changes. The project implements a deterministic local identity digital twin and a reversible authorized Entra extension. The primary mover scenario detected stale Finance access after an Engineering transfer, remediated the membership, and verified compliance. A secondary contractor scenario detects expiration failure and removes local access.

The highest residual risks are premium controls unavailable in the Entra Free tenant: Conditional Access, PIM, access reviews, entitlement management, Identity Protection, and lifecycle workflows. Their configurations and validators are `DESIGNED FOR ENTRA`, not claimed as deployed.

## 30/60/90-day roadmap

- 30 days: stabilize HR attributes, ownership, JML metrics, and exception handling.
- 60 days: pilot report-only Conditional Access and formal application ownership in a licensed tenant.
- 90 days: introduce PIM, access reviews, access packages, and workload credential governance with measured rollback plans.

## Resume-ready result

Built and verified a deterministic IAM lifecycle lab with transactional state, authorized Entra user/group operations, toxic-access detection, simulated investigation, automated remediation, CI, and reproducible evidence reporting.
