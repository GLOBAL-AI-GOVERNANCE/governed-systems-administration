# Mobile Review Guide

This page provides a narrow-screen review path for the proposed Alpha.1 contracts. The detailed Markdown tables and machine-readable files remain controlling.

## Status

- baseline-r5.2 is a preimplementation candidate.
- ADR-0001 is Proposed.
- Product implementation has not started.
- Execution capability is none.

## Artifacts

1. AdministrativeActionRequest
2. SystemContext
3. ActionAnalysis
4. ReviewRequirement
5. ValidationPlan
6. AdministrationEvidenceRecord

## Outcome Types

- Analysis succeeded
- Input rejected
- Unsupported input
- Indeterminate analysis
- Internal failure

Every outcome has no authorization effect and does not authorize execution.

## Syntax Review

Tier A contains 15 exact observational forms. Review them in [`catalog/tier-a.json`](../catalog/tier-a.json).

Tier B contains bounded high-risk families. Review them in [`catalog/tier-b.json`](../catalog/tier-b.json).

Excluded syntax has precedence over Tier B recognition. Review the complete list in [`catalog/excluded-constructs.json`](../catalog/excluded-constructs.json).

Redirection states and effects are in [`catalog/redirection.json`](../catalog/redirection.json).

## Policy Review

The first-match sequence is:

1. Excluded construct or prohibited baseline capability
2. Unsupported syntax or command
3. Missing or contradictory context
4. Unresolved target
5. Missing or unsupported agent authority
6. Invalid, expired, revoked, untrusted, or over-ceiling authority
7. Tier B family marked prohibited
8. Other Tier B
9. Elevated privilege
10. Unknown privilege
11. Unknown source
12. Synthetic sensitive source
13. Over-limit targets
14. All no-escalation conditions
15. Remaining supported state

Machine-readable policy: [`policy/rules.json`](../policy/rules.json)  
Reachability evidence: [`policy/reachability.json`](../policy/reachability.json)

## Coverage and Traceability

Coverage is measured by obligations, not raw fixture count.

- [Coverage obligations](../coverage/obligations.json)
- [Requirement and threat matrix](../traceability/matrix.json)
- [Acceptance fixtures](../tests/fixtures/acceptance-cases.json)
- [Repository assurance fixtures](../tests/fixtures/repository-cases.json)

## Review Sequence

1. Read [STATUS](../STATUS.md).
2. Confirm the [hard gate](../GOVERNANCE.md).
3. Review [Supported Syntax](SUPPORTED_SYNTAX.md).
4. Review the [Reference Policy](REFERENCE_POLICY.md).
5. Review [Schemas](../schemas/README.md).
6. Review [Acceptance Tests](ACCEPTANCE_TEST_PLAN.md).
7. Review [Claims](CLAIMS_REGISTER.md).
8. Review [ADR-0001](../decisions/ADR-0001-command-governance-alpha1.md).

This guide is informative and does not override the controlling documents.
