# Threat Model

**Status:** Pre-alpha draft  
**Scope:** Public reference repository and bounded non-executing analyzer  
**Method:** Structured threat analysis; not a claim of exhaustive formal verification

## 1. Security Objectives

1. Never execute submitted administrative commands in the active increment.
2. Never issue a no-escalation disposition for unsupported or insufficiently understood input.
3. Preserve the distinction between intent, effects, escalation, authorization, and execution.
4. Prevent accidental disclosure of personal, secret, proprietary, or operational data.
5. Make analysis reasons, uncertainty, versions, and evidence limitations explicit.
6. Prevent local redefinition of upstream trust semantics.
7. Produce deterministic, content-hashed analysis artifacts without overstating assurance.

## 2. Assets

- parser and classification correctness;
- integrity of syntax and semantics registries;
- authority-compatibility rules;
- reference-policy rules;
- artifact schemas;
- canonicalization and hashing;
- synthetic fixtures;
- test expectations;
- repository history and release process;
- public/private boundary;
- project claims and maturity status; and
- user trust.

## 3. Threat Actors and Failure Sources

- well-intentioned administrator making a mistake;
- AI system generating plausible but unsafe syntax;
- malicious user crafting parser-confusing input;
- compromised or over-authorized agent;
- contributor introducing permissive semantics;
- dependency or build-system attacker;
- maintainer accidentally publishing private data;
- fixture author encoding misleading context;
- future file source providing malformed or hostile content; and
- integrator treating advisory output as authorization.

## 4. Trust Boundaries

1. Untrusted request input → strict artifact ingest
2. Command text → bounded parser
3. Parsed tokens → semantics registry
4. Declared context → context validator
5. Synthetic manifest → target resolver
6. Upstream trust reference → compatibility validator
7. Analysis → reference-policy evaluation
8. Artifacts → evidence canonicalization
9. Repository source → CI and release process
10. Public output → downstream integrator

## 5. Threats and Controls

| ID | Threat | Potential consequence | Required controls |
|---|---|---|---|
| T-001 | Hidden execution path | Real system mutation | Ban execution APIs; scans; tests; review |
| T-002 | Tier C input treated as Tier A | False no-escalation result | Exact registry; tier tests; fail closed |
| T-003 | Parser differential | Misread command or target | Preserve tokens; adversarial fixtures; no shell evaluation |
| T-004 | Quoting or escaping confusion | Wrong arguments or targets | Exact grammar; reject excluded constructs |
| T-005 | Wildcard under-resolution | Broad unintended scope | Synthetic manifest only; target count; indeterminate if absent |
| T-006 | Redirection misclassification | Overwrite or disclosure | Explicit allowed operator set; escalation |
| T-007 | Unknown executable assigned benign semantics | False no-escalation result | Tier C; `UNKNOWN_EFFECT`; indeterminate |
| T-008 | Alias or function confusion | Different behavior | Unsupported unless explicitly canonicalized |
| T-009 | Dynamic evaluation | Static-analysis bypass | Detect; Tier C; prohibit or mark indeterminate |
| T-010 | Context spoofing | Incorrect classification | Context provenance; contradiction handling |
| T-011 | Authority inflation | Action appears within scope | Validate supported upstream reference; compare ceiling |
| T-012 | Expired or revoked authority accepted | Invalid trust comparison | Validity and revocation checks when applicable |
| T-013 | Local passport redefinition | Semantic divergence | No duplicate passport schema; pinned compatibility |
| T-014 | Hash overclaim | False assurance | Explicit limitations; no authenticity claim |
| T-015 | Non-deterministic serialization | Unstable evidence | Canonicalization tests |
| T-016 | Secret or private-data leakage | Exposure | Synthetic-only policy; scans; safe errors |
| T-017 | Malicious fixture | Misleading tests or payload | Review; size limits; controlled formats |
| T-018 | Dependency compromise | Analyzer or CI compromise | Minimal dependencies; pinning; audit |
| T-019 | Claims drift | Public overstatement | Claims Register; governance review |
| T-020 | Advice treated as authorization | Unauthorized action | Mandatory nonauthorization fields; no executor |
| T-021 | Resource exhaustion | Denial of service | Input size and complexity limits |
| T-022 | Unicode deception | Misread command or path | UTF-8 policy; raw and normalized display; tests |
| T-023 | Duplicate structured keys | Conflicting interpretation | Strict parser rejects duplicates |
| T-024 | Path traversal in future intake | File escape or overwrite | Deferred isolated extraction; canonical-path checks |
| T-025 | Archive bomb in future intake | Resource exhaustion | Deferred size, depth, and expansion quotas |
| T-026 | Personal or proprietary reference leakage | Boundary and confidentiality harm | Pre-commit scans; public/private review |
| T-027 | Status-only boundary expansion | Unauthorized scope or execution expansion | Governance precedence; monotonic narrowing-only rule; ADR review |
| T-028 | Tier B recognition overrides excluded syntax | Dynamic or compound input misclassified as bounded | Normative evaluation order; adversarial tests |
| T-029 | Incomplete lexical grammar | Parser disagreement and nondeterministic tests | Exact grammar; ASCII policy; bounds; normalization rule |
| T-030 | Policy branch ambiguity | Inconsistent review versus prohibition | Versioned deterministic decision matrix; first-match tests |

## 6. Misuse Cases

- A user submits a wildcard deletion and treats an explanation as permission.
- An agent supplies expired authority but omits revocation state.
- A command uses an alias that resolves differently in a live session.
- A command embeds dynamic evaluation.
- A contributor adds an execution API to “validate” behavior.
- A synthetic fixture contains a real token or private hostname.
- A downstream system interprets `NO_ESCALATION_REQUIRED_BY_REFERENCE_POLICY` as authorization.
- A content hash is presented as proof that a command executed.

Each misuse case requires a design control, test, documentation warning, or explicit prohibition.

## 7. Security Test Categories

- no-execution static scan;
- Tier A, Tier B, and Tier C tests;
- ambiguous-parse tests;
- quoting and escaping tests;
- wildcard and redirection tests;
- unknown-command tests;
- dynamic-evaluation tests;
- missing-context tests;
- authority-mismatch tests;
- expired or revoked trust tests;
- duplicate-key and malformed-artifact tests;
- Unicode-deception tests;
- size and complexity tests;
- deterministic-evidence tests;
- configured sensitive-pattern tests; and
- public/private boundary scans.

## 8. Residual Risks

Even when tests pass:

- static analysis may miss live runtime behavior;
- semantics may vary by platform, version, module, environment, and state;
- synthetic target resolution does not predict a real system;
- authority artifacts may contain false declarations;
- configured sensitive-pattern detection may miss unknown secret formats;
- hashes do not prove event occurrence or identity;
- downstream systems may misuse advisory output; and
- dependency and maintainer compromise remain possible.

## 9. Change Rule

Update this threat model when a change:

- adds syntax;
- adds a dependency;
- changes canonicalization;
- introduces live-state access;
- introduces file or archive parsing;
- changes authority compatibility;
- changes dispositions;
- adds a collector;
- creates an execution path; or
- expands accepted data beyond synthetic public-safe fixtures.
