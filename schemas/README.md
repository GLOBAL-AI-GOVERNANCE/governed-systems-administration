# Proposed Alpha.1 Schemas

**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Verification contracts implemented; product not started

## Primary Artifacts

- `administrative-action-request.schema.json`
- `system-context.schema.json`
- `action-analysis.schema.json`
- `review-requirement.schema.json`
- `validation-plan.schema.json`
- `administration-evidence-record.schema.json`

## Outcome Contracts

- `analysis-outcome.schema.json`
- `analysis-succeeded.schema.json`
- `input-rejected.schema.json`
- `unsupported-input.schema.json`
- `indeterminate-analysis.schema.json`
- `internal-failure.schema.json`

## Verification Contracts

- `profiles.schema.json`
- `acceptance-case.schema.json`
- `acceptance-suite.schema.json`
- `repository-case.schema.json`
- `repository-suite.schema.json`
- CLI and authority-adapter schemas

Schemas use Draft 2020-12, reject duplicate JSON keys through the verifier, enforce declared formats, and include cross-field invariants. A structurally valid artifact is not proof that its claims are true.


## Portable date-time enforcement

The `date_time` definition uses two layers:

1. a schema pattern that rejects lexically invalid values even when an external
   validator does not implement `format`; and
2. an explicitly registered RFC 3339 checker in `tools/verify_repository.py`,
   backed by the hash-locked `rfc3339-validator` dependency.

Missing verification dependencies cause setup or import failure rather than
silently weakening the repository's validation contract.
