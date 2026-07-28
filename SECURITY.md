# Security Policy

## Project Security Boundary

Governed Systems Administration is in pre-alpha planning and has no authorized command-execution, privilege-elevation, credential-use, production-connection, or autonomous-remediation capability.

A code path that unexpectedly executes commands, opens a shell, connects to a host, mutates a system, or handles real credentials is a security defect and a release-blocking boundary violation.

## Reporting a Security Issue

Do not disclose sensitive vulnerability details in a public issue.

Use GitHub private vulnerability reporting for this repository when available. If private reporting is unavailable, open a minimal public issue requesting a secure contact channel without including exploit details, secrets, personal data, host information, or proof-of-concept payloads.

## High-Priority Report Categories

Reports are especially valuable when they concern:

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

## Safe Research Expectations

Security research must:

- use synthetic fixtures or systems you are authorized to test;
- avoid real credentials and operational data;
- avoid testing against third-party systems without permission;
- minimize collection and retention of sensitive information; and
- provide enough detail for reproducible, bounded validation.

## Supported Versions

There is no software release. Security fixes apply to the active default branch and any explicitly identified pre-release tags.

## No Guarantee

This policy does not create a service-level agreement, bug bounty, certification, warranty, or guaranteed response time. Reports will be assessed according to severity, reproducibility, and project scope.
