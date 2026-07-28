# Requirement–Threat–Test Traceability

`matrix.json` is the machine-readable source. `matrix.csv` is generated as an equivalent review view.

The verifier checks:

- every catalog requirement and threat appears;
- every mapped test ID is known;
- every fixture declares reverse edges;
- JSON and CSV edges are identical;
- every source has at least one test.

Traceability proves declared mapping completeness, not universal semantic completeness. Coverage obligations and independent V&V remain separate gates.
