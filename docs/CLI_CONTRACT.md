# Proposed CLI Contract

**Document version:** `alpha1-cli-0.2-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Not started

The future CLI is JSON-first and non-executing.

## Commands

```text
gsa validate --request FILE --context FILE
gsa analyze --request FILE --context FILE
gsa version
```

Submitted command text is data. It is never executed.

## Streams

- Successful machine-readable results: one JSON object on stdout.
- Errors: one JSON object on stderr.
- No banners, progress text, or logs appear on stdout.
- UTF-8 is required.

## Exit Codes

| Code | Meaning | Schema |
|---:|---|---|
| 0 | Valid request or completed analysis outcome | `cli-result.schema.json` |
| 2 | CLI usage error | `cli-error.schema.json` |
| 3 | Input rejected | `cli-error.schema.json` |
| 4 | Unsupported input | `cli-error.schema.json` |
| 5 | Indeterminate analysis | `cli-error.schema.json` |
| 6 | Contract or schema version unsupported | `cli-error.schema.json` |
| 70 | Internal failure | `cli-error.schema.json` |

A policy prohibition is a completed analysis outcome, not a CLI process failure; it exits 0 while still stating `execution_authorized: false`.

## Result and Error Contracts

- [`schemas/cli-result.schema.json`](../schemas/cli-result.schema.json)
- [`schemas/cli-error.schema.json`](../schemas/cli-error.schema.json)
- [`schemas/analysis-outcome.schema.json`](../schemas/analysis-outcome.schema.json)

The CLI cannot issue credentials, elevate privilege, resolve live state, or execute commands.
