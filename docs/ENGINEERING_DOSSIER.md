# Governed Systems Administration Engineering Dossier

**Document version:** `0.2-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Baseline:** `baseline-r5.2`  
**Implementation status:** Not started  
**Execution capability:** None

## Contents

1. [Document Control](#1-document-control)
2. [Decision](#2-decision)
3. [Mission and Problem](#3-mission-and-problem)
4. [Scope](#4-scope)
5. [Artifact Family](#5-artifact-family)
6. [Analysis Model](#6-analysis-model)
7. [Syntax and Policy](#7-syntax-and-policy)
8. [Schemas and Evidence](#8-schemas-and-evidence)
9. [Fixtures and Traceability](#9-fixtures-and-traceability)
10. [Threat and Privacy Boundaries](#10-threat-and-privacy-boundaries)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Decision Gate](#12-decision-gate)

## 1. Document Control

```text
GOVERNANCE.md
→ accepted ADRs
→ STATUS.md
→ ENGINEERING_DOSSIER.md
→ SUPPORTED_SYNTAX.md
→ REFERENCE_POLICY.md
→ schemas and CANONICAL_JSON.md
→ ACCEPTANCE_TEST_PLAN.md and fixtures
→ THREAT_MODEL.md
→ PUBLIC_PRIVATE_BOUNDARY.md
→ CLAIMS_REGISTER.md
```

Lower-precedence documents may narrow but never relax higher restrictions. This dossier is proposed normative until ADR-0001 is accepted.

## 2. Decision

The active objective is a bounded, non-executing analyzer for explicitly supported Bash and PowerShell forms. It represents and analyzes administrative intent without invoking a shell or operating on a system.

## 3. Mission and Problem

Administrative commands are often detached from purpose, context, target scope, authority, validation, and recovery. AI-generated commands can amplify this gap. The project connects these elements before consequential action.

## 4. Scope

Included: structured artifacts, bounded parsing design, exact classifications, synthetic target resolution, authority states, deterministic reference policy, review requirements, validation plans, canonical evidence, schemas, fixtures, traceability, and verification controls.

Excluded: execution, live resolution, credentials, privilege issuance, reviewer authentication, mutation, full shell-language support, and real operational data.

## 5. Artifact Family

### 5.1 AdministrativeActionRequest

Requester, purpose, platform, shell, command text, targets, privilege, remote scope, and source classification.

### 5.2 SystemContext

Synthetic host, directory, identity, privilege, executable resolution, resources, target status, and authority status.

### 5.3 ActionAnalysis

Coverage, tier, rule, normalized command, intent, state change, effects, uncertainty, target and authority status, reasons, limitations, and nonauthorization fields.

### 5.4 ReviewRequirement

Required review, prohibition, or indeterminate disposition. It does not authenticate approval or grant authority.

### 5.5 ValidationPlan

Expected outcomes, checks, rollback prerequisites, recovery notes, and residual risks. No live validation is performed.

### 5.6 AdministrationEvidenceRecord

Artifact references, versions, canonical hashes, redaction status, and assurance limitations. It does not claim an action occurred.

## 6. Analysis Model

Coverage is `SUPPORTED`, `UNSUPPORTED`, or `INDETERMINATE`. Tiers are A, B, and C. Intent, state change, effects, uncertainty, authority, and policy are independent dimensions.

Every result has `authorization_effect: NONE` and `execution_authorized: false`.

## 7. Syntax and Policy

[Supported Syntax](SUPPORTED_SYNTAX.md) defines grammar, whitespace, Tier A forms, Tier B matrices, exclusions, wildcard limits, redirection, and evaluation order. [Reference Policy](REFERENCE_POLICY.md) defines deterministic first-match outcomes.

## 8. Schemas and Evidence

Six schemas define the artifact family. [GSA-CJSON-1](CANONICAL_JSON.md) defines canonical serialization and SHA-256 hashing. Hashes prove byte equality only.

## 9. Fixtures and Traceability

Machine-readable fixtures cover every Tier A form, Tier B family, excluded construct, policy rule, malformed class, redirection state, authority state, evidence class, privacy class, and no-execution class.

Traceability is bidirectional: `requirement ↔ threat ↔ test`.

## 10. Threat and Privacy Boundaries

Threats include hidden execution, parser confusion, context spoofing, authority inflation, dynamic evaluation, policy ambiguity, evidence overclaim, private-data leakage, dependency compromise, and downstream misuse. Public artifacts use only synthetic, public-safe data.

## 11. Acceptance Criteria

### 11.1 Documentation and Governance

Zero broken links; one precedence hierarchy; proposed-normative language; prior findings closed.

### 11.2 Grammar and Classification

Exact whitespace, shell-specific grammar, complete Tier A and B matrices, closed exclusions, deterministic wildcard and redirection behavior.

### 11.3 Schemas and Evidence

Six schemas validate; canonical hashes reproduce; evidence claims no execution or authorization.

### 11.4 Fixtures and Traceability

Unique IDs, complete required coverage, valid schemas, and complete requirement/threat mappings.

### 11.5 Repository Safety

No product implementation source, no execution path, privacy scans pass, and CI/control files exist.

### 11.6 ADR Eligibility

A passing audit makes ADR-0001 eligible for explicit review. It does not accept it automatically.

## 12. Decision Gate

No product implementation source for the parser, classifier, semantic registry, target resolver, authority adapter, policy engine, review builder, validation-plan builder, evidence builder, or product CLI may be introduced until versioned JSON Schemas for all six artifacts exist and validate; machine-readable acceptance fixtures cover every Tier A form, every Tier B family, every named excluded construct, and every reference-policy branch; a bidirectional requirement, threat, and test traceability matrix is present and reviewed; the pre-implementation baseline passes independent V&V; and ADR-0001 is explicitly accepted.

Validation scripts, CI checks, schema validators, and test harnesses introduced before ADR acceptance must not execute submitted administrative command text, access live administrative state, issue credentials, elevate privilege, or modify a system.


## baseline-r5.2 Hard Gate

No product implementation source may be introduced until baseline-r5.2 passes independent semantic V&V and ADR-0001 is explicitly accepted. Verification tooling must not execute submitted administrative command text or access live administrative state.
