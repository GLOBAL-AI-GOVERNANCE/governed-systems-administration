# Alpha.1 Reference Policy

**Document version:** `alpha1-policy-0.3-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Not started

## Invariant

Every outcome has:

```yaml
authorization_effect: NONE
execution_authorized: false
```

The policy does not grant approval, authenticate a reviewer, issue privilege, or execute an action.

## First-Match Rules

| ID | Condition | Disposition |
|---|---|---|
| POL-001 | Explicitly excluded construct or prohibited baseline capability | Prohibited |
| POL-002 | Unsupported syntax, shell, or command | Prohibited |
| POL-004 | Missing or contradictory required context | Indeterminate |
| POL-005 | Unresolved or unsupported target state | Indeterminate |
| POL-006 | Missing or unsupported agent authority | Indeterminate |
| POL-007 | Invalid, expired, revoked, untrusted, or over-ceiling authority | Prohibited |
| POL-008 | Tier B family explicitly marked prohibited | Prohibited |
| POL-009 | Other Tier B or supported redirection requiring review | Human review |
| POL-010 | Elevated privilege | Human review |
| POL-011 | Unknown privilege | Indeterminate |
| POL-012 | Unknown source classification | Indeterminate |
| POL-013 | Synthetic sensitive source | Human review |
| POL-014 | More than 32 resolved targets | Human review |
| POL-015 | Every no-escalation condition is satisfied | No escalation by reference policy |
| POL-016 | Remaining supported state | Human review |

Apply the first matching rule. `POL-001` concerns excluded syntax and baseline capabilities, not Tier B family policy. `POL-008` is therefore reachable and unshadowed.

## No-Escalation Conditions

All conditions must be true:

1. Tier A supported form.
2. Complete and noncontradictory context.
3. Supported platform, shell, catalog, schema, and policy versions.
4. Standard privilege.
5. Synthetic public source.
6. Target state is not applicable, empty, or within the 32-target limit.
7. Human authority is not applicable, or agent authority is within ceiling.
8. Observational intent.
9. No declared state change.
10. Effects are limited to the approved observational set.
11. No remote target condition or other residual review condition.
12. No higher-priority rule matches.

## Reachability Evidence

[`policy/reachability.json`](../policy/reachability.json) identifies one natural fixture for every retained rule under first-match semantics. CI rejects shadowed, duplicate, or unreachable rules.
