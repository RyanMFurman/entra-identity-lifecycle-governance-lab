# Reproducibility Report

Evidence: `IMPLEMENTED LOCALLY`. Date: 2026-07-14.

Python 3.11.9 and PowerShell 7.6.3 were used. `python -m pytest` passed 3 tests. The PowerShell demo initialized state, introduced three deterministic findings, generated investigation evidence, remediated stale access and an expired contractor, passed final validation, reset, tolerated a second setup, and removed generated state during teardown. No undocumented environment variables or vendor access were used.

Advanced Entra capabilities outside the reversible user/group scenario remain `FUTURE PRODUCTION VALIDATION`.

## Authorized extension

On 2026-07-15, the separate authorized adapter completed tenant discovery and a reversible live mover scenario using disabled synthetic identities. It detected a deliberately retained Finance group membership after an Engineering transfer, remediated the membership, and verified the final tenant state. Advanced premium controls remain future validation.
