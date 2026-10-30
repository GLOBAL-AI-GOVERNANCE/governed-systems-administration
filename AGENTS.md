# AGENTS.md

Instructions for coding agents working in this repository.

## Setup and checks

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install --require-hashes -r requirements-dev.lock
python tools/verify_repository.py
python tools/check_schema_ids.py
python -m pytest
```

## Rules

- Specification only. This repository must not gain execution capability that modifies systems until a separate, explicit decision.
- Accept only synthetic, public-safe fixtures.
- Every public result keeps `authority_effect: "NONE"`. Do not add a path that approves, certifies, or authorizes.
- Prefer squash-merge through green CI. Do not force-push `main`.

## Setup guide

End-to-end local setup for the toolkit and MCP: [AGENT_SETUP](https://ai-governance.solutions/AGENT_SETUP.html).
