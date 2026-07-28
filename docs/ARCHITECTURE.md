# Architecture

**Status:** Pre-alpha design  
**Active increment:** `v0.1.0-alpha.1 — Command Governance Foundation`  
**Execution capability:** None

## 1. Purpose

This document defines the architecture for a bounded, non-executing systems-administration analyzer.

The architecture separates declared intent, context, analysis, authority comparison, escalation, validation planning, and evidence. No executor exists in the active increment.

## 2. Context

```text
Human or AI-assisted requester
        |
        v
AdministrativeActionRequest
        |
        v
Context validation --------> SystemContext
        |
        v
Bounded parser
        |
        v
Semantic and effect analysis
        |
        +--------------------> Supported Syntax Registry
        |
        +--------------------> Command Semantics Registry
        |
        v
Authority compatibility ----> Upstream trust reference
        |
        v
Deterministic reference policy
        |
        v
ReviewRequirement
        |
        v
ValidationPlan
        |
        v
AdministrationEvidenceRecord
```

## 3. Architectural Invariants

1. The active increment contains no command executor.
2. Analysis never grants operating authority.
3. Every output carries `authorization_effect: NONE`.
4. Every output carries `execution_authorized: false`.
5. Unsupported input is explicit.
6. Missing context is explicit.
7. Unknown semantics cannot produce a no-escalation disposition.
8. Upstream trust semantics are referenced and validated, not redefined.
9. Evidence describes the analysis package, not a real-world event.
10. Synthetic public-safe data is the only accepted public fixture class.

## 4. Components

### 4.1 Request Ingest

Responsibilities:

- strict artifact parsing;
- schema and version checks;
- 4,096-byte command-input limit;
- UTF-8 validation;
- NUL rejection;
- duplicate-key rejection;
- source classification; and
- required-field validation.

### 4.2 Context Validator

Responsibilities:

- platform and shell consistency;
- working-directory form;
- identity and privilege declaration;
- synthetic-resource-manifest references;
- executable-resolution inputs;
- remote-scope declaration; and
- context provenance.

### 4.3 Bounded Parser

Responsibilities:

- parse only the versioned Alpha.1 envelope;
- preserve token and quoting boundaries;
- identify one optional pipeline and allowed operators;
- classify coverage tier;
- return `UNSUPPORTED` for excluded constructs;
- return `INDETERMINATE` when sufficient semantics cannot be established; and
- avoid shell invocation, expansion, evaluation, or execution.

### 4.4 Semantics Registry

A versioned registry maps recognized commands or cmdlets to:

- intent;
- state-change assessment;
- effects;
- context requirements;
- tier; and
- escalation rules.

The registry is conservative:

- aliases are unsupported unless explicitly canonicalized from trusted synthetic context;
- unknown commands produce `UNKNOWN_EFFECT`;
- Tier B families always escalate or are prohibited;
- options may change effects; and
- semantic classification does not prove live target state.

### 4.5 Synthetic Target Resolver

Alpha.1 may resolve targets only against supplied synthetic manifests.

It must not read a live filesystem, registry, service manager, network stack, identity store, package database, or remote host.

Resolution outputs include:

- exact synthetic target set;
- unresolved target;
- wildcard present;
- target count;
- synthetic path category; and
- uncertainty.

### 4.6 Classifier

Produces:

- coverage status;
- coverage tier;
- intent;
- state-change assessment;
- non-exclusive effects;
- uncertainty; and
- reasons.

Examples:

- a network query may have `OBSERVATIONAL_INTENT`, `NO_DECLARED_STATE_CHANGE`, and `NETWORK_OBSERVATION`;
- a pipeline may combine `FILE_READ` and `DATA_DISCLOSURE_POTENTIAL`;
- an unknown command receives `UNKNOWN_INTENT`, `UNKNOWN_STATE_CHANGE`, and `UNKNOWN_EFFECT`;
- dynamic evaluation adds `DYNAMIC_EXECUTION`.

### 4.7 Authority Compatibility Layer

Responsibilities:

- identify a supported upstream trust version;
- validate references through an approved compatibility mechanism;
- read the declared authority ceiling;
- reject unsupported, invalid, expired, untrusted, or revoked states; and
- produce a comparison result without issuing privilege.

### 4.8 Deterministic Reference Policy

Normative behavior is defined in [REFERENCE_POLICY.md](REFERENCE_POLICY.md).


Inputs:

- coverage and tier;
- intent;
- state-change assessment;
- effects;
- uncertainty;
- target scope;
- privilege;
- remote scope;
- authority comparison;
- rollback readiness; and
- validation readiness.

Outputs:

- reference-policy disposition;
- reasons;
- required reviewer role;
- conditions;
- expiration;
- `authorization_effect: NONE`; and
- `execution_authorized: false`.

### 4.9 Validation Planner

Creates a plan, not a live validation result.

It records:

- expected outcome;
- checks required after execution by a separate authorized system;
- rollback prerequisites;
- recovery notes; and
- residual risks.

### 4.10 Evidence Builder

Produces deterministic linked artifacts.

Targeted Alpha.1 properties:

- canonical serialization;
- content hashes;
- tool, policy, schema, and registry versions;
- linked identifiers;
- redaction status; and
- explicit assurance limitations.

## 5. Data Flow States

```text
RECEIVED
→ STRUCTURALLY_VALID | REJECTED
→ SUPPORTED | UNSUPPORTED | INDETERMINATE
→ TIER_A | TIER_B | TIER_C
→ ANALYZED | INDETERMINATE
→ REFERENCE_POLICY_DISPOSITION_ASSIGNED
→ EVIDENCE_EMITTED
```

There is no `EXECUTED` state.

## 6. Planned Package Boundaries

```text
src/gsa/
├── artifacts/
├── parsing/
├── semantics/
├── context/
├── classification/
├── authority/
├── policy/
├── validation/
├── evidence/
└── cli/
```

This structure is planned, not implemented.

## 7. Dependency Policy

- Prefer the Python standard library where practical.
- Add dependencies only for a documented requirement.
- Pin development dependencies.
- Record dependency purpose.
- Run vulnerability and license checks.
- Avoid libraries that execute shell syntax to analyze it.
- Treat parser and canonicalization dependencies as security-critical.

## 8. Future Execution Boundary

Any future controlled executor must be designed as a separate security boundary with independent review, credentials, policy enforcement, isolation, logging, rollback, and release gates.

Its existence is not implied or authorized by this architecture.
