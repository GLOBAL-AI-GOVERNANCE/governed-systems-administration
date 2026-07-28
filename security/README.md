# Public-Boundary Scan Configuration

The public verifier always checks common credential patterns, email addresses,
IPv4 addresses, high-entropy tokens, and repository safety invariants.

Maintainers may also run a release-specific private-term scan without
committing private names or hashed confirmations.

1. Create a UTF-8 file outside the repository, or use the ignored local path
   `security/private-terms.local`.
2. Put one private term per line. Blank lines and `#` comments are ignored.
3. Run:

```bash
GSA_PRIVATE_TERMS_FILE=/secure/path/private-terms.txt \
  python tools/verify_repository.py
```

The verifier normalizes each term in memory and does not print the terms.
The private input file and derived hashes must not be committed, archived, or
included in public audit artifacts.

A generic automated scan cannot prove that every unknown trade secret or
proprietary phrase is absent. Final public release still requires a human
source and privacy review.
