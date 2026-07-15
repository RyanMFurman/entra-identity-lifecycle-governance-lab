# Common Demo Failures

- `pwsh` missing: install PowerShell 7.4+ and reopen the terminal.
- Wrong directory: run commands from the repository root.
- State missing: run `pwsh ./demo/setup-demo.ps1`.
- Unexpected state: run `pwsh ./demo/reset-demo.ps1`.
- Recording cleanup: run `pwsh ./demo/teardown-demo.ps1 -Confirm:$false`.
