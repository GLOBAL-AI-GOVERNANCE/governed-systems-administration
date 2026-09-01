# Proposed future CODEOWNERS team model

The live `.github/CODEOWNERS` file names only the current valid owner, `@GLOBAL-AI-GOVERNANCE`. The role model below is design documentation only. It is not an enforceable ownership assignment and must not move into the live CODEOWNERS file unless the account becomes an organization and the listed teams are actually created.

| Proposed role | Proposed team slug | Intended scope |
|---|---|---|
| Maintainers | `governed-systems-administration-maintainers` | Repository-wide maintenance, governance, status, and packaging |
| Security reviewers | `governed-systems-administration-security-reviewers` | Security policy, threat model, workflows, tools, policy, and sensitive dependency files |
| Specification reviewers | `governed-systems-administration-specification-reviewers` | Decisions, schemas, tests, traceability, coverage, and specification documents |
| Upstream compatibility reviewers | `governed-systems-administration-upstream-compatibility-reviewers` | Integration contracts and upstream compatibility |

Revisit this model only when real multi-maintainer governance requires organization teams and central role delegation.
