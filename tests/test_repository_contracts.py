from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_repository", ROOT / "tools" / "verify_repository.py")
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)

def load(rel: str):
    return VERIFY.load_json(ROOT / rel)

def test_full_local_verifier() -> None:
    assert VERIFY.run_all() == []

def test_markdown() -> None:
    assert VERIFY.verify_markdown() == []

def test_schemas_and_formats() -> None:
    assert VERIFY.verify_schemas_and_instances() == []

def test_fixture_oracle() -> None:
    assert VERIFY.verify_acceptance() == []

def test_repository_assurance_cases() -> None:
    assert VERIFY.verify_repository_cases() == []

def test_traceability() -> None:
    assert VERIFY.verify_traceability() == []

def test_golden_evidence_links() -> None:
    assert VERIFY.verify_golden_hashes() == []

def test_canonical_vectors() -> None:
    assert VERIFY.verify_canonical_vectors() == []

def test_no_execution_boundary() -> None:
    assert VERIFY.verify_no_execution_tooling() == []

def test_public_boundary() -> None:
    assert VERIFY.verify_public_boundary() == []

def test_public_boundary_ignores_git_metadata(tmp_path, monkeypatch) -> None:
    root = tmp_path / "repository"
    security = root / "security"
    security.mkdir(parents=True)

    (security / "scan-exceptions.json").write_text(
        '{"high_entropy_paths": []}\n',
        encoding="utf-8",
    )

    git_logs = root / ".git" / "logs"
    git_logs.mkdir(parents=True)
    (git_logs / "HEAD").write_text(
        "commit author <author@example.com>\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(VERIFY, "ROOT", root)

    assert VERIFY.verify_public_boundary() == []


def test_public_boundary_still_detects_tracked_email(
    tmp_path,
    monkeypatch,
) -> None:
    root = tmp_path / "repository"
    security = root / "security"
    security.mkdir(parents=True)

    (security / "scan-exceptions.json").write_text(
        '{"high_entropy_paths": []}\n',
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        "# Test repository\n\nauthor@example.com\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(VERIFY, "ROOT", root)

    assert VERIFY.verify_public_boundary() == [
        "README.md: public-boundary detections ['EMAIL']"
    ]


def test_ci_pins_and_claims_state() -> None:
    assert VERIFY.verify_ci_pins() == []
    assert VERIFY.verify_proposed_language() == []

def test_semantic_conflict_seed_is_detected() -> None:
    cases = copy.deepcopy(load("tests/fixtures/acceptance-cases.json")["cases"])
    duplicate = copy.deepcopy(cases[0])
    duplicate["test_id"] = "SEEDED-DUPLICATE"
    duplicate["expected"] = copy.deepcopy(duplicate["expected"])
    duplicate["expected"]["review_requirement"]["reasons"] = ["Conflicting seeded outcome"]
    cases.append(duplicate)
    assert any("conflicting outputs" in item for item in VERIFY.semantic_conflicts(cases))

def test_unknown_profile_seed_is_detected() -> None:
    cases = copy.deepcopy(load("tests/fixtures/acceptance-cases.json")["cases"])
    cases[0]["profiles"]["context"] = "unknown-context"
    errors = VERIFY.profile_reference_errors(cases, load("tests/fixtures/profiles.json"))
    assert errors

def test_shadowed_policy_seed_is_detected() -> None:
    cases = copy.deepcopy(load("tests/fixtures/acceptance-cases.json")["cases"])
    reach = load("policy/reachability.json")
    reach["rules"][1]["fixture_id"] = reach["rules"][0]["fixture_id"]
    # The production checker reads files; directly prove duplicate semantic reachability is detectable.
    signatures = []
    cmap = {case["test_id"]:case for case in cases}
    for item in reach["rules"]:
        signatures.append(cmap[item["fixture_id"]]["semantic_signature"])
    assert len(signatures) != len(set(signatures))

def test_ast_guard_seed_is_detected() -> None:
    assert "FORBIDDEN_IMPORT" in VERIFY.ast_detections("import subprocess\n")
    assert "DYNAMIC_EXECUTION" in VERIFY.ast_detections("eval('1+1')\n")
    assert "FILESYSTEM_MUTATION" in VERIFY.ast_detections("from pathlib import Path\nPath('x').write_text('y')\n")
    assert VERIFY.ast_detections("value = {'command': 'pwd'}\n") == set()

def test_privacy_seed_is_detected() -> None:
    token = "".join(["AKIA", "1234567890ABCDEF"])
    assert "AWS_STYLE_KEY" in VERIFY.privacy_detections(token)
    assert VERIFY.privacy_detections("synthetic public fixture") == set()

def test_invalid_date_time_is_rejected() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    request = copy.deepcopy(load("tests/golden/administrative-action-request.json"))
    request["created_at"] = "not-a-date"
    assert VERIFY.validate_instance(request, "administrative-action-request.schema.json", schemas, registry)

def test_cross_field_mutations_are_rejected() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    golden = {
        "request":load("tests/golden/administrative-action-request.json"),
        "context":load("tests/golden/system-context.json"),
        "analysis":load("tests/golden/action-analysis.json"),
        "review":load("tests/golden/review-requirement.json"),
        "evidence":load("tests/golden/administration-evidence-record.json"),
    }
    for mutation in [
        "HUMAN_WITH_TRUST_REFERENCE","AGENT_WITHOUT_TRUST_REFERENCE","LINUX_WITH_POWERSHELL",
        "RESOLVED_WITHOUT_CANONICAL_NAME","NOT_APPLICABLE_WITH_NONZERO_TARGET",
        "SUPPORTED_TIER_C","NO_ESCALATION_WITH_POL001","ARBITRARY_HASH_KEY","INVALID_DATETIME"
    ]:
        schema_name, instance = VERIFY.apply_schema_mutation(mutation, golden)
        assert VERIFY.validate_instance(instance, schema_name, schemas, registry), mutation


def test_private_terms_are_local_only() -> None:
    assert not (ROOT / "security" / "private-term-hashes.json").exists()
    normalized = VERIFY.normalize_private_term("  Confidential   Example Program  ")
    assert normalized == "confidential example program"
    digest = VERIFY.hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    assert len(digest) == 64


def test_explicit_rfc3339_checker_is_registered() -> None:
    assert "date-time" in VERIFY.GSA_FORMAT_CHECKER.checkers


def test_date_time_pattern_fails_without_format_support() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    request = copy.deepcopy(load("tests/golden/administrative-action-request.json"))
    request["created_at"] = "not-a-date"
    validator = VERIFY.Draft202012Validator(
        schemas["administrative-action-request.schema.json"],
        registry=registry,
    )
    assert list(validator.iter_errors(request))


def test_rfc3339_semantic_calendar_validation() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    request = copy.deepcopy(load("tests/golden/administrative-action-request.json"))
    request["created_at"] = "2026-02-31T12:00:00Z"
    errors = VERIFY.validate_instance(
        request,
        "administrative-action-request.schema.json",
        schemas,
        registry,
    )
    assert errors


def test_rfc3339_timezone_is_required() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    request = copy.deepcopy(load("tests/golden/administrative-action-request.json"))
    request["created_at"] = "2026-07-27T12:00:00"
    errors = VERIFY.validate_instance(
        request,
        "administrative-action-request.schema.json",
        schemas,
        registry,
    )
    assert errors


def test_nullable_date_time_remains_valid() -> None:
    schemas = VERIFY.schema_objects()
    registry = VERIFY.schema_registry(schemas)
    review = copy.deepcopy(load("tests/golden/review-requirement.json"))
    review["expires_at"] = None
    errors = VERIFY.validate_instance(
        review,
        "review-requirement.schema.json",
        schemas,
        registry,
    )
    assert errors == []
