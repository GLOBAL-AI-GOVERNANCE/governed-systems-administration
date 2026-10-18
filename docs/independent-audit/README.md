# Independent Semantic Audit Kit for baseline-r5.2

**Document status:** Informative audit procedure. It does not change any normative document, accept ADR-0001, or authorize product implementation.

`STATUS.md` requires an independent semantic audit that "reports zero open high findings and zero local failures" before the baseline is eligible for ADR review. `docs/BASELINE_STATUS.md` states that a passing audit makes ADR-0001 eligible for explicit human review and does not accept it. This kit defines what is audited, how, and what a usable result looks like.

## Baseline under audit

| Field | Value |
|---|---|
| Baseline | `baseline-r5.2` |
| Audit commit | `f90587b2d63d40e0f97037d70354a5ddc4036bc6` |
| Audit tree | `1714379a1e3bd98fe442b92d68eb57b028d468f0` |
| Publication commit | `2205beffeaa14999027fce8f389f58b2ab6e14dd` |
| Manifest | [`manifest.json`](manifest.json) |

The manifest lists the SHA-256 of 62 normative artifacts and 5 verification-tooling files at the audit commit. All 62 normative artifacts are byte-identical to the publication commit. The verification tooling (verifier, tests, lock file, workflow) has changed since publication. Audit the tooling as it exists at the audit commit.

The repository changes after this kit is added, but the files it lists do not. A result applies only to files whose hashes match the manifest.

## Normative artifacts

- Governance and status: `GOVERNANCE.md`, `STATUS.md`, `decisions/ADR-0001-command-governance-alpha1.md`.
- Controlled documents: `docs/ENGINEERING_DOSSIER.md`, `docs/SUPPORTED_SYNTAX.md`, `docs/REFERENCE_POLICY.md`, `docs/CANONICAL_JSON.md`, `docs/ACCEPTANCE_TEST_PLAN.md`, `docs/CLI_CONTRACT.md`, `docs/UPSTREAM_COMPATIBILITY.md`.
- Boundary and claims: `docs/THREAT_MODEL.md`, `docs/PUBLIC_PRIVATE_BOUNDARY.md`, `docs/CLAIMS_REGISTER.md`, `docs/BASELINE_STATUS.md`.
- Contracts: `schemas/`, `policy/`, `catalog/`, `coverage/`, `traceability/`.
- Fixtures and vectors: `tests/fixtures/`, `tests/golden/`, `tests/conformance/`.

Precedence follows `GOVERNANCE.md` section 5.

## Commands

Run from a clean checkout of the audit commit.

```text
git checkout f90587b2d63d40e0f97037d70354a5ddc4036bc6
git rev-parse HEAD^{tree}
python -m pip install --require-hashes -r requirements-dev.lock
python tools/verify_repository.py
python -m pytest
```

Confirm each manifest hash with `sha256sum` or an equivalent tool of your own. CI uses Python 3.12. Record the version you use.

The local commands show only that the project's own checks pass. They are not the audit. An audit that only re-runs them does not qualify.

## Semantic criteria

Assess each criterion against the normative text, not against the verifier's output.

1. **Fixture identity.** Cases with the same semantic identity, as defined in `docs/ACCEPTANCE_TEST_PLAN.md`, have byte-identical expected outcomes. Every fixture uses exactly one legal outcome type.
2. **Policy reachability.** In `policy/reachability.json`, every rule is reachable under first-match semantics, no rule is shadowed by a higher-precedence rule, and each rule's fixture exercises its condition and expected outcome. Check this independently, not by trusting the `reachable` and `shadowed_by` fields.
3. **Schema strictness.** Schemas reject the cross-field combinations the controlled documents prohibit. Golden instances validate, and nothing the documents forbid is accepted.
4. **Coverage.** `coverage/obligations.json` covers every Tier A rule, Tier B family, and excluded construct in `catalog/`, with no obligation lacking a test.
5. **Traceability.** Every requirement in `traceability/requirements.json` and every threat in `traceability/threats.json` maps to at least one test in `traceability/matrix.csv`. The CSV and JSON matrices agree, and each mapped test exists and checks what the requirement states.
6. **Canonical JSON and evidence.** `tests/conformance/canonical-json-vectors.json` and `tests/golden/hashes.json` match `docs/CANONICAL_JSON.md` exactly, including the error cases.
7. **Contracts.** The CLI, upstream-compatibility, and authority-adapter contracts are internally consistent and agree with the schemas and vectors.
8. **No product source.** The repository contains no product parser, classifier, semantic registry, target resolver, authority adapter, policy engine, review, validation-plan or evidence builder, or product CLI source, as listed in the `STATUS.md` hard gate.
9. **No execution.** No tooling executes submitted administrative command text, accesses live administrative state, or uses credentials or privilege.
10. **Claims.** `README.md`, `STATUS.md`, and `docs/CLAIMS_REGISTER.md` make no claim beyond the evidence, and C-004 and C-005 remain subject to independent audit.
11. **Supply chain.** CI actions are pinned and the lock file is hash-locked.

## Severity

| Severity | Meaning |
|---|---|
| High | A normative contradiction, an unreachable or shadowed rule, an accepted prohibited input, a broken traceability link for a requirement or threat, a canonical-JSON mismatch, product source or an execution path, or a claim the evidence does not support. Any open high finding blocks ADR review eligibility. |
| Medium | An ambiguity that could produce two conforming but different results, or missing negative coverage, without a demonstrated incorrect outcome. |
| Low | Editorial or consistency issues that cannot change a result. |
| Informational | Observations and suggestions. |

The maintainers may disposition a finding as fixed, accepted with rationale, or disputed with evidence. They may not downgrade a finding's severity without the auditor's agreement or a recorded rationale.

## Independence

An audit qualifies only when all of these hold:

- the auditor is outside the project's control boundary and is not a maintainer, contributor, or reviewer of this repository;
- the method and any tooling are the auditor's own and reuse no project decision logic, verifier code, or expected outputs as the source of truth;
- the auditor reports every finding, including findings unfavorable to the project.

Project-authored or otherwise same-control-boundary audits do not qualify.

## Required audit evidence

The audit evidence consists of one receipt based on [`AUDIT_RECEIPT_TEMPLATE.json`](AUDIT_RECEIPT_TEMPLATE.json) and one record per finding based on [`FINDING_TEMPLATE.md`](FINDING_TEMPLATE.md). Use only synthetic, public-safe content. Do not include credentials, personal data, or private system details.

## Boundary

A qualifying audit with zero open high findings and zero local failures makes ADR-0001 eligible for human review. It does not accept the ADR, authorize product implementation, or establish production readiness, compliance, or safety.
