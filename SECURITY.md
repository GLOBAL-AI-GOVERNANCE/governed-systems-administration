# Security Policy

This repository does not operate an external security-report intake. Do not place secrets, credentials, personal data, sensitive operational information, or vulnerability material in public GitHub surfaces.

## Project Security Boundary

Governed Systems Administration is a reference design under independent review and has no authorized command-execution, privilege-elevation, credential-use, production-connection, or autonomous-remediation capability.

A code path that unexpectedly executes commands, opens a shell, connects to a host, mutates a system, or handles real credentials is a security defect and a release-blocking boundary violation.

## Security-Relevant Failure Classes

The following are treated as security defects:

- an unexpected execution path;
- a reference-policy disposition that can be mistaken for authorization;
- permissive analysis of unsupported or ambiguous syntax;
- parser confusion that changes interpreted targets or effects;
- command, path, wildcard, quoting, redirection, or pipeline misclassification;
- bypass of an authority or escalation requirement;
- inconsistent evidence canonicalization;
- secret exposure in logs, fixtures, errors, or generated artifacts;
- unsafe archive or file handling in a future evidence-intake capability;
- dependency or build-system compromise; or
- a public/private boundary violation.

## Supported Versions

There is no software release. Security fixes apply to the active default branch and any explicitly identified pre-release tags.

## No Guarantee

This policy does not create a service-level agreement, bug bounty, certification, warranty, or guaranteed response time.
