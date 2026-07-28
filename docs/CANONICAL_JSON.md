# GSA-CJSON-1 Canonical JSON Profile

**Document version:** `gsa-cjson-1-draft`  
**Approval status:** Under review  
**Normative status:** Proposed normative  
**Implementation status:** Verification tooling implemented; product not started

GSA-CJSON-1 defines the exact bytes used for identifiers and SHA-256 hashes.

## Rules

1. Input data must be valid JSON data with no duplicate object keys.
2. Object keys are sorted lexicographically by Unicode code point.
3. No insignificant whitespace is emitted.
4. Arrays preserve order.
5. Strings are encoded as UTF-8.
6. JSON quotation mark, reverse solidus, and control-character escapes follow the JSON grammar.
7. Solidus `/` is not escaped.
8. Non-ASCII characters are emitted directly as UTF-8, not `\u` escapes.
9. Unpaired UTF-16 surrogate values are rejected.
10. Numbers are prohibited in canonical artifact fields except schema-defined integers. Integers use base-10 with no leading zero, plus sign, exponent, or decimal point.
11. NaN and infinities are rejected.
12. The final canonical representation has no trailing newline.
13. SHA-256 is computed over the canonical UTF-8 bytes.

Reference expression:

```python
json.dumps(
    value,
    ensure_ascii=False,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

The expression is informative; the rules and conformance vectors are controlling.

## Conformance

[`tests/conformance/canonical-json-vectors.json`](../tests/conformance/canonical-json-vectors.json) provides input values, canonical bytes encoded as Base64, and expected SHA-256 values.

Hash equality proves byte equality only. It does not prove truth, authorship, trusted time, collection integrity, signer authority, or event occurrence.
