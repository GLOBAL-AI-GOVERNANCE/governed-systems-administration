# Claims Register

**Baseline:** `baseline-r5.2`  
**Approval status:** Under review  
**ADR-0001:** Proposed

## Status Vocabulary

- **Baseline fact:** directly observable in this repository.
- **Designed:** specified but not implemented as product behavior.
- **Hypothesis:** requires empirical evidence.
- **Rejected:** prohibited wording.

## Claim Index

| ID | Claim | Status |
|---|---|---|
| C-001 | The repository contains no product analyzer implementation | Baseline fact |
| C-002 | The repository contains versioned preimplementation schemas and fixtures | Baseline fact |
| C-003 | Submitted administrative command text is not executed by verification tooling | Baseline fact, subject to verifier scope |
| C-004 | Fixture outcomes are deterministic | Designed; must pass independent audit |
| C-005 | Policy branches are reachable and unshadowed | Designed; must pass independent audit |
| C-006 | Evidence hashes establish byte equality only | Baseline fact |
| C-007 | The future analyzer is fail-closed | Designed |
| C-008 | Alpha.1 improves administrative safety | Hypothesis |
| C-009 | The project is production-ready or compliant | Rejected |
| C-010 | The project makes agents safe | Rejected |

## C-001 — No product implementation

- **Permitted:** “Product analyzer implementation has not started.”
- **Evidence:** no product source package, parser, classifier, resolver, adapter, policy engine, artifact builder, or product CLI exists.
- **Limitation:** verification and test tooling is executable code.

## C-002 — Preimplementation contracts

- **Permitted:** “The repository contains proposed normative schemas, catalogs, fixtures, traceability, and verification tooling.”
- **Limitation:** presence and structural validity do not establish semantic correctness. Independent V&V remains required.

## C-003 — Nonexecution

- **Permitted:** “Repository verification is designed and tested not to execute submitted administrative command text.”
- **Limitation:** static checks are not universal proof against every possible future bypass.

## C-004 and C-005 — Determinism and reachability

- **Permitted before audit:** “The baseline includes machine-enforced determinism and reachability checks.”
- **Permitted after passing independent audit:** “The reviewed baseline passed the documented determinism and reachability checks.”
- **Not permitted:** universal correctness or proof about future implementations.

## C-006 — Evidence

Hashes show whether canonical bytes match. They do not establish truth, authorship, trusted time, collector integrity, signer authority, custody, event occurrence, immutability, or non-repudiation.

## C-007 — Fail-closed product behavior

The product behavior is designed, not implemented. Do not claim a working fail-closed analyzer before product tests and implementation exist.

## Rejected Wording

- production-ready;
- certified or compliant;
- prevents all destructive actions;
- guarantees safe administration;
- independently verified product;
- working analyzer or policy engine;
- autonomous secure administration;
- measured time savings without measurement.
