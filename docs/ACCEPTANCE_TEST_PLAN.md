# Alpha.1 Acceptance-Test Plan

**Document version:** `alpha1-tests-0.3-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Product not started; verification fixtures implemented

## Semantic Fixture Identity

The semantic identity of an acceptance case is the SHA-256 of canonical JSON containing:

```text
input.kind
input.value
profiles.context
profiles.requester
profiles.target
```

Profiles contain the complete context, authority, and target states. Two cases with the same semantic identity must have byte-identical expected outcomes.

## Legal Outcome Vocabulary

Every fixture validates against exactly one versioned outcome:

- `AnalysisSucceeded`
- `InputRejected`
- `UnsupportedInput`
- `IndeterminateAnalysis`
- `InternalFailure`

Free-floating `REJECTED`, `NONE`, or fixture-only semantic states are prohibited.

## Coverage by Obligation

Coverage is generated from:

- every Tier A rule;
- every Tier B family;
- every excluded construct;
- every redirection state;
- every retained policy branch;
- every authority state;
- every target state;
- structural and lexical boundaries;
- evidence linkage;
- privacy detection;
- no-execution guards;
- schema-negative mutations; and
- verifier-negative seeds.

[`coverage/obligations.json`](../coverage/obligations.json) is controlling for coverage accounting. A category label or duplicate case cannot satisfy an obligation.

## Repository Assurance Tests

Evidence, privacy, no-execution, schema-negative, and verifier-negative tests are separate from command-analysis fixtures. They perform category-specific mutations and executable assertions.

## Traceability

Every fixture identifies requirement and threat IDs. [`traceability/matrix.json`](../traceability/matrix.json) and [`traceability/matrix.csv`](../traceability/matrix.csv) must be identical and bidirectional.

## Gate

Executable verification contracts must pass before ADR review. Product tests must still be committed before product implementation logic.
