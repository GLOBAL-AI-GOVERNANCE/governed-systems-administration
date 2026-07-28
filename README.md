# Governed Systems Administration

Human-governed, evidence-driven reference tooling for AI-assisted systems administration across commands, identities, storage, services, networks, validation, and recovery.

## Status

**Pre-alpha preimplementation candidate under independent semantic review**

- **Repository baseline revision:** `baseline-r5.2`
- **Active engineering increment:** `v0.1.0-alpha.1 — Command Governance Foundation`
- **ADR-0001:** Proposed
- **Product analyzer implementation:** Not started
- **Execution capability:** None
- **Accepted public data:** Synthetic, public-safe fixtures only

No product parser, classifier, resolver, authority adapter, policy engine, artifact builder, or product CLI exists in this baseline.

## Start Here

- [Current status and hard gate](STATUS.md)
- [Baseline review status](docs/BASELINE_STATUS.md)
- [Mobile review guide](docs/MOBILE_REVIEW_GUIDE.md)
- [Governance](GOVERNANCE.md)
- [Engineering dossier](docs/ENGINEERING_DOSSIER.md)
- [Supported syntax](docs/SUPPORTED_SYNTAX.md)
- [Reference policy](docs/REFERENCE_POLICY.md)
- [Acceptance-test plan](docs/ACCEPTANCE_TEST_PLAN.md)
- [Schemas](schemas/README.md)
- [Coverage obligations](coverage/README.md)
- [Traceability](traceability/README.md)
- [Canonical JSON](docs/CANONICAL_JSON.md)
- [CLI contract](docs/CLI_CONTRACT.md)
- [Upstream compatibility](docs/UPSTREAM_COMPATIBILITY.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Claims Register](docs/CLAIMS_REGISTER.md)
- [ADR-0001](decisions/ADR-0001-command-governance-alpha1.md)
- [Public-boundary scan configuration](security/README.md)

## Intended Alpha.1 Flow

```text
AdministrativeActionRequest
→ SystemContext validation
→ bounded non-executing analysis
→ authority comparison
→ deterministic reference policy
→ ReviewRequirement
→ ValidationPlan
→ AdministrationEvidenceRecord
```

The flow is a proposed contract. Product implementation begins only after the independent baseline audit passes and ADR-0001 is explicitly accepted.

## Six Artifacts

- `AdministrativeActionRequest`
- `SystemContext`
- `ActionAnalysis`
- `ReviewRequirement`
- `ValidationPlan`
- `AdministrationEvidenceRecord`

## Outcome Contract

Fixtures use only versioned outcomes:

- `ANALYSIS_SUCCEEDED`
- `INPUT_REJECTED`
- `UNSUPPORTED_INPUT`
- `INDETERMINATE_ANALYSIS`
- `INTERNAL_FAILURE`

Every outcome has no authorization effect and never authorizes execution.

## Nonexecution Boundary

This repository does not:

- invoke Bash or PowerShell;
- create a subprocess from submitted command text;
- resolve live files, identities, services, packages, or networks;
- use credentials or elevate privilege;
- modify a system;
- authenticate a reviewer; or
- claim that an administrative action occurred.

## Hard Implementation Gate

No product implementation source may be introduced until:

1. all schemas and fixtures pass semantic verification;
2. every policy branch is reachable and unshadowed;
3. requirement–threat–test traceability is complete;
4. the independent baseline audit reports zero open high findings and zero local failures; and
5. ADR-0001 is explicitly accepted.

Verification tooling may exist before acceptance only when it cannot execute submitted administrative command text or access live administrative state.

## Relationship to Agentic AI Governance

This project may consume supported trust references from `GLOBAL-AI-GOVERNANCE/agentic-ai-governance`. It does not redefine the Agent Trust Passport, validity, signature, action-authority, evidence-binding, or revocation semantics.

## License

[Apache License 2.0](LICENSE). The license does not imply endorsement, certification, production readiness, or authorization to operate on systems.
