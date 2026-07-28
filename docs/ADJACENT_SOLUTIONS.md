# Adjacent Solutions and Differentiation

## 1. Positioning Rule

Governed Systems Administration does not claim to be the first:

- shell or script analyzer;
- command approval wrapper;
- policy-as-code engine;
- privileged-access system;
- agent control plane;
- endpoint monitoring product;
- audit recorder;
- infrastructure scanner; or
- human-in-the-loop workflow.

Differentiation must be demonstrated through architecture, semantics, interoperability, evidence, tests, and measured outcomes rather than novelty language.

## 2. Adjacent Categories

### Shell and Script Static Analysis

Common strengths:

- syntax and style checks;
- known anti-pattern detection;
- language-specific diagnostics.

Intended distinction here:

- administrative intent and effects;
- authority comparison;
- structured escalation;
- validation planning;
- linked evidence artifacts.

### Command Approval and Execution Wrappers

Common strengths:

- interception;
- operator confirmation;
- execution control;
- local policy enforcement.

Intended distinction here:

- non-executing public reference model;
- explicit unsupported and indeterminate states;
- composable artifacts;
- upstream agent-authority interoperability.

### Privileged Access Management

Common strengths:

- identity, credential, session, and privilege controls;
- just-in-time access;
- session recording.

Intended distinction here:

- pre-execution command semantics;
- cross-shell effect classification;
- evidence-linked validation planning.

PAM integration is planned future work and is not implemented.

### Agent Control Planes and Policy Engines

Common strengths:

- tool authorization;
- runtime policy;
- sandboxing;
- audit.

Intended distinction here:

- systems-administration-specific semantics;
- explicit wildcard, service, package, identity, storage, and network effects;
- upstream trust compatibility.

### Endpoint, Detection, and Monitoring Platforms

Common strengths:

- live telemetry;
- detection;
- correlation;
- response.

Intended distinction here:

- structured proposed-action package before execution;
- escalation requirement;
- expected validation and recovery plan.

### Infrastructure as Code and Configuration Policy

Common strengths:

- declarative desired state;
- reviewable changes;
- repeatability.

Intended distinction here:

- imperative administrative commands;
- mixed human and agent intent;
- uncertainty and command-context analysis.

### Audit and Session Recording

Common strengths:

- historical event capture;
- investigation support.

Intended distinction here:

- linking purpose, declared authority, proposed action, analysis, escalation, validation plan, and evidence limitations before execution.

## 3. Intended Differentiation

The design hypotheses are:

1. a composable administrative-action artifact family;
2. explicit separation of analysis, escalation, authorization, execution, validation, and evidence;
3. bounded Bash and PowerShell systems-administration semantics;
4. explicit `SUPPORTED`, `UNSUPPORTED`, and `INDETERMINATE` coverage;
5. Tier A, Tier B, and Tier C analysis;
6. separate intent, state-change, and effect models;
7. structured human-review requirements;
8. versioned interoperability with upstream trust semantics;
9. synthetic target resolution;
10. validation and recovery planning linked to the action;
11. deterministic evidence records with honest limitations; and
12. a path to later administrative and evidence-intake domains.

## 4. Evidence Required

Before making strong differentiation claims, the project needs:

- documented comparison criteria;
- reproducible fixtures;
- cross-tool evaluation;
- false-permissive and false-escalation measurements;
- usability testing;
- integration demonstrations; and
- independent review.

## 5. Current Position

The project is a pre-alpha design. Its differentiation remains a hypothesis until implemented and evaluated.
