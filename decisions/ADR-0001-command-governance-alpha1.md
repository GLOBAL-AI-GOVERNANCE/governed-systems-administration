# ADR-0001: Command Governance Alpha.1

- **Status:** Proposed
- **Baseline:** `baseline-r5.2`
- **Increment:** `v0.1.0-alpha.1 — Command Governance Foundation`

## Proposed Decision

Adopt the six-artifact bounded non-executing design represented by baseline-r5.2's proposed normative documents, schemas, fixtures, traceability, and repository controls.

## Excluded

Product implementation before acceptance, shell/subprocess invocation, live state, credentials, privilege, mutation, reviewer authentication, autonomous remediation, full shell support, and real operational data.

## Pre-Implementation Hard Gate

No product implementation source for the parser, classifier, semantic registry, target resolver, authority adapter, policy engine, review builder, validation-plan builder, evidence builder, or product CLI may be introduced until versioned JSON Schemas for all six artifacts exist and validate; machine-readable acceptance fixtures cover every Tier A form, every Tier B family, every named excluded construct, and every reference-policy branch; a bidirectional requirement, threat, and test traceability matrix is present and reviewed; the pre-implementation baseline passes independent V&V; and ADR-0001 is explicitly accepted.

Validation scripts, CI checks, schema validators, and test harnesses introduced before ADR acceptance must not execute submitted administrative command text, access live administrative state, issue credentials, elevate privilege, or modify a system.

## Approval Conditions

Independent V&V must confirm named findings closed, schemas and fixture coverage valid, traceability complete, no product source, claims accurate, and designated reviewer approval. A passing audit makes this ADR eligible for review but does not accept it automatically.


## baseline-r5.2 Hard Gate

No product implementation source may be introduced until baseline-r5.2 passes independent semantic V&V and ADR-0001 is explicitly accepted. Verification tooling must not execute submitted administrative command text or access live administrative state.
