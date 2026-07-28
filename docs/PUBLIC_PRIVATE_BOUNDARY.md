# Public and Private Boundary

## 1. Purpose

This boundary protects source integrity, privacy, security, confidentiality, trade-secret interests, and the separation between a reusable public reference project and private operational environments.

## 2. Allowed in the Public Repository

- original generalized documentation;
- public-safe schemas;
- synthetic Bash and PowerShell examples;
- fictional identities and organizations;
- reserved example domains and addresses;
- synthetic filesystem, identity, service, package, and network manifests;
- deterministic test fixtures;
- non-executing analyzer code after approval;
- compatibility tests using public synthetic upstream artifacts;
- threat models;
- claims and limitations;
- public contribution and security policies; and
- generated evidence records based only on synthetic inputs.

## 3. Prohibited in the Public Repository

### Personal, Confidential, and Proprietary Information

- personal names when unnecessary;
- personal contact information;
- private correspondence;
- employee, student, partner, customer, or supplier records;
- trade secrets;
- unpublished commercial strategy;
- non-public partnerships;
- proprietary assessments; or
- confidential contractual or operational information.

### Credentials and Secrets

- passwords;
- API keys;
- access tokens;
- cookies;
- private keys;
- certificates containing private material;
- recovery codes;
- real connection strings; or
- copied environment variables.

### Infrastructure and Operations

- real hostnames or internal addresses;
- network diagrams;
- account inventories;
- real shell history;
- production commands tied to actual systems;
- service configurations;
- cloud account identifiers;
- vulnerability details not ready for disclosure;
- security-control bypass information; or
- real operational evidence.

### Source and Training Materials

- copied proprietary prose;
- screenshots;
- institutional branding;
- source-author or participant details;
- lab addresses;
- lab credentials;
- certificates;
- proprietary instructions; or
- claims of endorsement by a source organization.

### Private Domain-Specific Deployments

- real organization or product names when not required for interoperability;
- real supplier submissions;
- material or technical certificates;
- characterization or test results;
- customer requirements;
- internal policies;
- infrastructure inventories;
- private funding or partnership records;
- credentials; or
- deployment evidence.

## 4. Synthetic Data Rules

Synthetic fixtures must:

- use fictional names;
- avoid realistic secrets;
- use obviously synthetic identifiers;
- avoid copying source wording;
- avoid reproducing private directory structures;
- be tagged with a source classification;
- contain no hidden metadata from real files; and
- be reviewed before publication.

Recommended conventions:

```text
organization: Example Systems Laboratory
host: gsa-demo-host-01
domain: example.invalid
user: synthetic-admin
linux_path: /srv/gsa-fixture/
windows_path: C:\GSA-Fixture\
token: TEST_ONLY_NOT_A_SECRET
```

## 5. Public Transformation Rule

Knowledge may inform design, but public artifacts must be newly written and generalized.

```text
source concept
→ abstract engineering principle
→ original requirement
→ synthetic public-safe example
→ review for copied language and private identifiers
```

## 6. Review Before Commit

Before any public commit:

- scan for secrets;
- scan for personal names and contact details;
- scan for private-company, product, customer, and supplier references;
- scan for hosts, IP addresses, domains, emails, accounts, and paths;
- inspect file metadata;
- confirm fixtures are synthetic;
- confirm no copied proprietary source text;
- verify claims against `CLAIMS_REGISTER.md`; and
- confirm no execution path was added.

## 7. Leakage Response

If prohibited content is committed:

1. stop further distribution;
2. assess sensitivity;
3. revoke exposed credentials immediately;
4. remove material from the active branch;
5. determine whether history rewriting is required;
6. document the incident privately;
7. notify affected parties when appropriate; and
8. add a preventive control or test.

Deleting a file in a later commit may not remove it from repository history.

## 8. Future Private Implementations

A private deployment may consume public schemas and logic, but requires:

- a separate threat model;
- credential and key management;
- data classification;
- access control;
- logging and retention policy;
- deployment authorization;
- rollback and recovery;
- customer and supplier handling rules; and
- independent security review.

Public project maturity does not authorize private operational deployment.

## Maintainer-Only Private Release Scan

Private organization, program, supplier, customer, course, and personal-name
denylist terms must not be committed in raw or reversibly confirmable hashed
form.

Maintainers may supply an ignored local denylist through
`GSA_PRIVATE_TERMS_FILE` as documented in
[`security/README.md`](../security/README.md). The local input and any derived
values remain outside the public repository and release archive.
