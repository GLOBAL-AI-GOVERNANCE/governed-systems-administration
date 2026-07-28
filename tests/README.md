# Verification Tests

This directory contains preimplementation verification contracts, not product analyzer tests.

- `fixtures/acceptance-cases.json`: deterministic command-analysis and policy outcomes
- `fixtures/profiles.json`: versioned context, requester, authority, and target profiles
- `fixtures/repository-cases.json`: evidence, privacy, no-execution, schema-negative, and verifier-negative cases
- `golden/`: canonical six-artifact evidence package and hashes
- `conformance/`: canonical JSON and upstream adapter vectors
- `test_repository_contracts.py`: executable repository-contract checks

No test executes administrative command text or accesses live administrative state.
