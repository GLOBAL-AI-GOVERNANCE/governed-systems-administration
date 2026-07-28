# Non-Goals

## Active Increment Non-Goals

The pre-alpha Command Governance Foundation is not intended to:

1. execute Bash, PowerShell, Command Prompt, or any other command;
2. open a shell, terminal, remote session, or subprocess;
3. connect to a real host, cloud account, directory, service, or network;
4. elevate privilege or issue just-in-time access;
5. authenticate a human reviewer;
6. modify files, identities, permissions, services, packages, storage, networking, scheduled tasks, or power state;
7. validate a command by running it;
8. fully parse Bash or PowerShell;
9. infer live-state facts not supplied in synthetic context;
10. guarantee that a command is safe;
11. replace administrator judgment;
12. replace endpoint protection, PAM, SIEM, EDR, configuration management, or change management;
13. certify a system, agent, operator, or organization;
14. guarantee compliance with a law, regulation, framework, or policy;
15. provide non-repudiation, trusted timestamps, or independent attestation;
16. ingest real credentials or operational evidence;
17. host personal, customer, supplier, or private deployment data;
18. claim first-to-market status;
19. claim measured time savings or risk reduction without empirical evidence; or
20. perform autonomous remediation, containment, or recovery.

## Planned Work Is Not Current Authorization

Discussion of Script Assurance, Infrastructure Correlation, Synthetic Evidence Intake, privilege brokerage, or controlled execution does not authorize implementation or deployment.

Each planned capability requires:

- scope;
- threat-model update;
- acceptance tests;
- public/private review;
- governance approval; and
- an ADR when required.

## Reference-Policy Output Is Not Authorization

The analyzer may produce a reference-policy disposition. That output is not permission to execute and does not replace organizational authorization, change control, safety review, or system-owner approval.

Every output is intended to state:

```yaml
authorization_effect: NONE
execution_authorized: false
```
