# Portfolio Interoperability

Governed Systems Administration remains a **pre-alpha preimplementation** repository with **no execution capability**.

Its portfolio integration is intentionally reference-only.

## Agent trust reference

`AdministrativeActionRequest.requester.trust_reference` may carry a supported external trust reference for an `AGENT` requester.

The field is a bounded string reference. This repository does not embed, reinterpret, or redefine the Agent Trust Passport, signature, revocation, evidence-binding, validity, or action-authority semantics owned by `agentic-ai-governance`.

A receiving implementation, if one is later authorized by the repository's hard implementation gate, must validate the referenced object through a supported adapter before relying on it.

## System configuration reference

A future adapter may associate a request or evidence record with a System Configuration Passport reference owned by `ai-cyber-resilience-framework`.

That relationship does not change the current six-artifact alpha.1 contract and does not authorize execution.

## Fail-closed handoff rule

Unsupported, missing, expired, revoked, or semantically incompatible foreign references must never be converted into implied authority.

No portfolio handoff may:

- execute submitted command text;
- authenticate a reviewer;
- grant privilege;
- prove an administrative action occurred; or
- bypass the independent semantic-review and ADR gates.

The existing repository verifier and contract tests remain the controlling local evidence.
