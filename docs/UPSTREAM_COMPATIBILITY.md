# Proposed Upstream Compatibility Contract

**Document version:** `alpha1-upstream-0.2-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Not started

## Supported Reference Profile

```text
agentic-ai-governance/alpha.1
```

This repository consumes a trust reference through a bounded adapter. It does not redefine passport identity, signatures, validity, action authority, evidence binding, or revocation.

## Adapter Contracts

- [`authority-adapter-input.schema.json`](../schemas/authority-adapter-input.schema.json)
- [`authority-adapter-output.schema.json`](../schemas/authority-adapter-output.schema.json)

## Output States

- `WITHIN_CEILING`
- `EXCEEDS_CEILING`
- `MISSING`
- `UNSUPPORTED`
- `INVALID`
- `EXPIRED`
- `REVOKED`
- `UNTRUSTED`

`NOT_APPLICABLE_HUMAN` is produced locally for human-request context and is not an upstream passport judgment.

## Version Handling

- Exact supported profile: evaluate the synthetic fixture.
- Unknown or unsupported profile: `UNSUPPORTED`.
- Missing agent reference: `MISSING`.
- No fallback to a different profile.
- No local restoration of expired or revoked authority.

Synthetic lifecycle fixtures are stored in [`tests/conformance/authority-adapter-vectors.json`](../tests/conformance/authority-adapter-vectors.json).
