# Contributing

Thank you for helping build Governed Systems Administration.

This repository uses an evidence-first, fail-closed contribution model. Safety boundaries, public claims, and supported syntax are part of the engineering system, not optional documentation.

## Start Before You Contribute

Review:

- [Project status](STATUS.md)
- [Governance](GOVERNANCE.md)
- [Engineering dossier](docs/ENGINEERING_DOSSIER.md)
- [Supported syntax](docs/SUPPORTED_SYNTAX.md)
- [Reference policy](docs/REFERENCE_POLICY.md)
- [Acceptance-test plan](docs/ACCEPTANCE_TEST_PLAN.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Public/private boundary](docs/PUBLIC_PRIVATE_BOUNDARY.md)
- [Claims Register](docs/CLAIMS_REGISTER.md)

## Current Contribution Scope

During pre-alpha planning, welcome contributions include:

- documentation corrections;
- threat-model improvements;
- synthetic test cases;
- schema proposals;
- parser test vectors;
- effect-taxonomy refinements;
- evidence and canonicalization test designs;
- interoperability fixtures; and
- bounded non-executing analyzer proposals after the Alpha.1 gate is accepted.

## Prohibited Contributions

Do not submit:

- real credentials, tokens, keys, cookies, or secrets;
- personal data or private organizational information;
- real hostnames, addresses, account names, internal paths, or infrastructure inventories;
- customer, supplier, employee, student, or partner data;
- copied proprietary source text, screenshots, lab instructions, or training credentials;
- command-execution, shell-spawning, privilege-elevation, or autonomous-remediation paths;
- malware, exploit payloads, persistence mechanisms, or unauthorized-access workflows;
- claims of safety, compliance, certification, novelty, or measured impact without evidence; or
- unnecessary or unreviewed dependencies.

## Engineering Requirements

A contribution that changes behavior must:

1. identify the supported syntax or artifact version affected;
2. identify the coverage tier and exact grammar rule;
3. describe intent, state-change assessment, effects, and uncertainty;
4. preserve fail-closed handling for unsupported or ambiguous input;
5. add positive, negative, boundary, malformed, and adversarial tests;
6. update the threat model when a trust boundary changes;
7. update the Claims Register when public behavior or wording changes;
8. use synthetic, public-safe fixtures;
9. avoid creating an execution path; and
10. preserve these output invariants:

```yaml
authorization_effect: NONE
execution_authorized: false
```

## Decision Vocabulary

Coverage:

- `SUPPORTED`
- `UNSUPPORTED`
- `INDETERMINATE`

Coverage tier:

- `A`
- `B`
- `C`

Reference-policy disposition:

- `NO_ESCALATION_REQUIRED_BY_REFERENCE_POLICY`
- `HUMAN_REVIEW_REQUIRED`
- `PROHIBITED_BY_REFERENCE_POLICY`
- `INDETERMINATE`

These values describe a reference analyzer result. They do not authorize execution.

## Local Verification Setup

Hosted verification uses Python 3.12 and the hash-pinned development lock.

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --require-hashes -r requirements-dev.lock
python tools/verify_repository.py
python -m pytest
```

On POSIX shells outside Windows Git Bash, activate with `source .venv/bin/activate`.

These commands validate repository contracts and fixtures only. They do not execute submitted administrative command text, access live administrative state, use credentials, elevate privilege, or modify a managed system.

## Pull Request Checklist

- [ ] The change is within the current authorized scope.
- [ ] No personal, private, proprietary, or operational data is included.
- [ ] No command or script is executed.
- [ ] New syntax is documented in `docs/SUPPORTED_SYNTAX.md`.
- [ ] Tests cover Tier A, Tier B, Tier C, malformed, and indeterminate paths as applicable.
- [ ] Threat-model implications are documented.
- [ ] Claims are updated and evidence status is accurate.
- [ ] Upstream trust semantics are referenced rather than duplicated.
- [ ] Documentation avoids unsupported safety, novelty, performance, or compliance claims.
- [ ] Required governance and ADR review is complete.

## License

By contributing, you agree that your contribution is licensed under the repository's Apache License 2.0 unless a later documented license policy states otherwise.


## baseline-r5.2 Hard Gate

No product implementation source may be introduced until baseline-r5.2 passes independent semantic V&V and ADR-0001 is explicitly accepted. Verification tooling must not execute submitted administrative command text or access live administrative state.
