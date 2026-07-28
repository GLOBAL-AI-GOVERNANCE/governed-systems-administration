# Pull Request

## Purpose

Describe the problem, the proposed change, and why it belongs in the current authorized increment.

## Change class

- [ ] Routine documentation
- [ ] Normative specification
- [ ] Schema or contract
- [ ] Acceptance fixture or traceability
- [ ] Repository verification or CI
- [ ] Security-boundary change
- [ ] Upstream compatibility
- [ ] Product implementation (not authorized before ADR-0001 acceptance)

## Required evidence

- [ ] Linked requirements and threats
- [ ] Added or updated uniquely identified tests
- [ ] Updated Claims Register when public behavior or wording changes
- [ ] Updated threat model when a trust boundary changes
- [ ] Public/private scan completed
- [ ] No submitted command text is executed
- [ ] No live administrative state is accessed
- [ ] `authorization_effect: NONE` is preserved
- [ ] `execution_authorized: false` is preserved

## Safety and data boundary

- [ ] Uses synthetic, public-safe data only
- [ ] Contains no credentials, personal data, customer data, supplier data, private infrastructure, or proprietary source text
- [ ] Introduces no shell, subprocess, remote-session, network-client, privilege, credential, or system-mutation path

## Verification

Paste the relevant local verification output and identify any checks that could not be run.
