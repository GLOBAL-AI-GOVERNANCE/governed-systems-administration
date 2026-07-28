# Governance

## 1. Roles

- **Repository Maintainer:** repository and release hygiene.
- **Specification Reviewer:** grammar, schemas, classifications, policy, fixtures, and traceability.
- **Security Reviewer:** threats, public/private boundary, no-execution verification, and security tests.
- **Upstream Compatibility Reviewer:** versioned trust interoperability without local redefinition.
- **Release Approver:** gate and claims decisions.

## 2. Pre-Implementation Hard Gate

No product implementation source for the parser, classifier, semantic registry, target resolver, authority adapter, policy engine, review builder, validation-plan builder, evidence builder, or product CLI may be introduced until versioned JSON Schemas for all six artifacts exist and validate; machine-readable acceptance fixtures cover every Tier A form, every Tier B family, every named excluded construct, and every reference-policy branch; a bidirectional requirement, threat, and test traceability matrix is present and reviewed; the pre-implementation baseline passes independent V&V; and ADR-0001 is explicitly accepted.

Validation scripts, CI checks, schema validators, and test harnesses introduced before ADR acceptance must not execute submitted administrative command text, access live administrative state, issue credentials, elevate privilege, or modify a system.

## 3. Nonexecution Boundary

Changing the no-execution boundary requires a separate architecture, credential and privilege model, isolation, rollback, recovery, tests, independent security review, public/private review, accepted ADR, and Release Approver authorization.

## 4. ADR Requirements

An ADR is required for active-increment approval, incompatible schemas, grammar expansion, classification or policy changes, canonicalization changes, upstream compatibility changes, collectors, credentials, privilege, execution, and release policy.

## 5. Document Precedence

1. `GOVERNANCE.md`
2. accepted ADRs
3. `STATUS.md`
4. `docs/ENGINEERING_DOSSIER.md`
5. `docs/SUPPORTED_SYNTAX.md`
6. `docs/REFERENCE_POLICY.md`
7. schemas and `docs/CANONICAL_JSON.md`
8. `docs/ACCEPTANCE_TEST_PLAN.md` and fixtures
9. `docs/THREAT_MODEL.md`
10. `docs/PUBLIC_PRIVATE_BOUNDARY.md`
11. `docs/CLAIMS_REGISTER.md`
12. informative documentation

A lower-precedence document may narrow but never relax a higher-precedence restriction. The most restrictive applicable requirement controls.

## 6. Emergency Changes

Emergency changes may preserve or narrow boundaries but may not expand execution, credentials, privilege, or production use.

## 7. Supersession and Rollback

Only a later accepted ADR supersedes an accepted decision. Roll back when boundaries, claims, compatibility, privacy, or acceptance criteria fail.


## baseline-r5.2 Hard Gate

No product implementation source may be introduced until baseline-r5.2 passes independent semantic V&V and ADR-0001 is explicitly accepted. Verification tooling must not execute submitted administrative command text or access live administrative state.
