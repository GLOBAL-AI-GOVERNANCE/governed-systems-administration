from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PortfolioInteropTests(unittest.TestCase):
    def test_agent_trust_remains_reference_only(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "administrative-action-request.schema.json").read_text(encoding="utf-8")
        )
        trust = schema["properties"]["requester"]["properties"]["trust_reference"]
        self.assertEqual(trust["type"], ["string", "null"])
        self.assertNotIn("$ref", trust)

    def test_document_preserves_nonexecution_and_foreign_semantics(self) -> None:
        text = (ROOT / "PORTFOLIO_INTEROP.md").read_text(encoding="utf-8")
        required = (
            "pre-alpha preimplementation",
            "no execution capability",
            "does not embed, reinterpret, or redefine the Agent Trust Passport",
            "does not authorize execution",
            "must never be converted into implied authority",
        )
        lowered = text.lower()
        for phrase in required:
            self.assertIn(phrase.lower(), lowered)


if __name__ == "__main__":
    unittest.main()
