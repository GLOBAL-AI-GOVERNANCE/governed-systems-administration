# Project Status

## Current State

| Field | Status |
|---|---|
| Repository baseline | `baseline-r5.2` |
| Active increment | `v0.1.0-alpha.1 — Command Governance Foundation` |
| Baseline type | Preimplementation candidate |
| Normative documents | Proposed normative, under review |
| Schemas and fixtures | Implemented as verification contracts |
| Product analyzer | Not started |
| Execution capability | None |
| ADR-0001 | Proposed |
| Production use | Not authorized |
| Data boundary | Synthetic, public-safe only |

## Hard Gate

No product parser, classifier, semantic registry, target resolver, authority adapter, policy engine, review builder, validation-plan builder, evidence builder, or product CLI source may be introduced until baseline-r5.2 passes independent semantic V&V and ADR-0001 is explicitly accepted.

Permitted before ADR acceptance:

- schemas;
- synthetic fixtures;
- validators;
- mutation tests;
- traceability;
- documentation;
- CI;
- security scanners; and
- repository verification tools that never execute submitted administrative command text.

## Status Boundary

`STATUS.md` may report or narrow the current boundary. It may not expand scope, maturity, accepted data, authorization, execution, privilege, or production use. Governance and accepted ADRs control any expansion. The most restrictive applicable requirement controls during conflict.

## Authorized Work

- close and review proposed normative contracts;
- validate schemas and fixtures;
- test deterministic policy reachability;
- test canonical evidence;
- scan public/private boundaries;
- verify no-execution controls;
- prepare an independent audit;
- review ADR-0001 after the audit.

## Prohibited Work

- product analyzer implementation before gate completion;
- submitted-command execution;
- live administrative state access;
- credentials or privilege;
- real customer, supplier, personal, or production data;
- autonomous remediation;
- production-readiness or compliance claims.

## Completion Rule

A passing local verifier is necessary but not sufficient. The baseline is eligible for ADR review only after an independent semantic audit reports zero open high findings and zero local failures.
