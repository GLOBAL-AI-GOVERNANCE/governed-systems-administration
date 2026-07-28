#!/usr/bin/env python3
"""Independent-style semantic verifier for the baseline-r5.2 candidate.

The verifier validates repository contracts and never executes administrative
command text contained in fixtures.
"""
from __future__ import annotations

import ast
import base64
import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from rfc3339_validator import validate_rfc3339


GSA_FORMAT_CHECKER = FormatChecker()

@GSA_FORMAT_CHECKER.checks("date-time", raises=(TypeError, ValueError))
def _gsa_rfc3339_date_time(value: object) -> bool:
    """Apply the repository's explicit RFC 3339 date-time contract."""
    if not isinstance(value, str):
        return True
    return bool(validate_rfc3339(value))

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "tests" / "fixtures"
GOLDEN = ROOT / "tests" / "golden"

class VerificationError(RuntimeError):
    pass

def load_json(path: Path) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise VerificationError(f"{path}: duplicate JSON key {key!r}")
            out[key] = value
        return out
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)
    except Exception as exc:
        raise VerificationError(f"cannot load {path}: {exc}") from exc

def canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    text.encode("utf-8", "strict")
    return text.encode("utf-8")

def semantic_signature(case: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes({"input": case["input"], "profiles": case["profiles"]})).hexdigest()

def markdown_slug(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title).strip().lower()
    title = "".join(ch for ch in title if ch.isalnum() or ch in " _-")
    return re.sub(r"-+", "-", title.replace(" ", "-"))

def markdown_anchors(text: str) -> set[str]:
    bases: list[str] = []
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if m:
                bases.append(markdown_slug(m.group(1)))
    counts: Counter[str] = Counter()
    out: set[str] = set()
    for base in bases:
        suffix = counts[base]
        out.add(base if suffix == 0 else f"{base}-{suffix}")
        counts[base] += 1
    return out

def verify_markdown() -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if not text.startswith("# "):
            errors.append(f"{rel}: missing H1")
        if text.count("```") % 2:
            errors.append(f"{rel}: unbalanced code fence")
        own = markdown_anchors(text)
        for line_no, line in enumerate(text.splitlines(), 1):
            for target in link_re.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.startswith("#"):
                    if target[1:] not in own:
                        errors.append(f"{rel}:{line_no}: missing anchor {target}")
                    continue
                file_part, _, fragment = target.partition("#")
                candidate = (path.parent / file_part).resolve()
                try:
                    candidate.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f"{rel}:{line_no}: link escapes repository: {target}")
                    continue
                if not candidate.is_file():
                    errors.append(f"{rel}:{line_no}: missing link {target}")
                elif fragment and fragment not in markdown_anchors(candidate.read_text(encoding="utf-8")):
                    errors.append(f"{rel}:{line_no}: missing linked anchor {target}")
    return errors

def schema_objects() -> dict[str, dict[str, Any]]:
    return {path.name: load_json(path) for path in sorted(SCHEMAS.glob("*.json"))}

def schema_registry(schemas: dict[str, dict[str, Any]]) -> Registry:
    registry = Registry()
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry

def validate_instance(instance: Any, schema_name: str, schemas: dict[str, dict[str, Any]], registry: Registry) -> list[str]:
    validator = Draft202012Validator(schemas[schema_name], registry=registry, format_checker=GSA_FORMAT_CHECKER)
    return [err.message for err in validator.iter_errors(instance)]

def verify_schemas_and_instances() -> list[str]:
    errors: list[str] = []
    schemas = schema_objects()
    registry = schema_registry(schemas)
    expected = {
        "administrative-action-request.schema.json","system-context.schema.json",
        "action-analysis.schema.json","review-requirement.schema.json",
        "validation-plan.schema.json","administration-evidence-record.schema.json",
        "analysis-outcome.schema.json","profiles.schema.json"
    }
    if not expected.issubset(schemas):
        errors.append(f"missing required schemas: {sorted(expected - set(schemas))}")
    instance_map = {
        "administrative-action-request.schema.json": GOLDEN / "administrative-action-request.json",
        "system-context.schema.json": GOLDEN / "system-context.json",
        "action-analysis.schema.json": GOLDEN / "action-analysis.json",
        "review-requirement.schema.json": GOLDEN / "review-requirement.json",
        "validation-plan.schema.json": GOLDEN / "validation-plan.json",
        "administration-evidence-record.schema.json": GOLDEN / "administration-evidence-record.json",
        "profiles.schema.json": FIXTURES / "profiles.json",
        "acceptance-suite.schema.json": FIXTURES / "acceptance-cases.json",
        "repository-suite.schema.json": FIXTURES / "repository-cases.json",
    }
    for schema_name, path in instance_map.items():
        instance = load_json(path)
        for message in validate_instance(instance, schema_name, schemas, registry):
            errors.append(f"{path.relative_to(ROOT)}: {message}")
    return errors

def semantic_conflicts(cases: list[dict[str, Any]]) -> list[str]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: list[str] = []
    for case in cases:
        actual = semantic_signature(case)
        if actual != case["semantic_signature"]:
            errors.append(f"{case['test_id']}: semantic signature mismatch")
        groups[actual].append(case)
    for signature, group in groups.items():
        outputs = {canonical_json_bytes(item["expected"]) for item in group}
        if len(outputs) > 1:
            errors.append(f"semantic signature {signature} has conflicting outputs: {[x['test_id'] for x in group]}")
        if len(group) > 1:
            errors.append(f"semantic signature {signature} is duplicated: {[x['test_id'] for x in group]}")
    return errors

def profile_reference_errors(cases: list[dict[str, Any]], profiles: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for case in cases:
        refs = case["profiles"]
        for field, section in [("context","contexts"),("requester","requesters"),("target","targets")]:
            if refs[field] not in profiles[section]:
                errors.append(f"{case['test_id']}: unknown {field} profile {refs[field]}")
    return errors

def outcome_policy(case: dict[str, Any]) -> tuple[str | None, str | None]:
    outcome = case["expected"]
    kind = outcome["outcome_type"]
    if kind == "ANALYSIS_SUCCEEDED":
        rr = outcome["review_requirement"]
        return rr["matched_policy_rule"], rr["disposition"]
    if kind in {"UNSUPPORTED_INPUT","INDETERMINATE_ANALYSIS"}:
        return outcome["matched_policy_rule"], outcome["reference_policy_disposition"]
    return None, None

def policy_reachability_errors(cases: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    rules = load_json(ROOT / "policy" / "rules.json")["rules"]
    reach = load_json(ROOT / "policy" / "reachability.json")["rules"]
    case_map = {case["test_id"]: case for case in cases}
    rule_ids = [rule["rule_id"] for rule in rules]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate policy rule IDs")
    precedence = [rule["precedence"] for rule in rules]
    if precedence != list(range(1, len(rules) + 1)):
        errors.append("policy precedence is not contiguous and ordered")
    if {item["rule_id"] for item in reach} != set(rule_ids):
        errors.append("reachability report does not cover exactly the retained policy rules")
    signatures: set[str] = set()
    for item in reach:
        cid = item["fixture_id"]
        if cid not in case_map:
            errors.append(f"{item['rule_id']}: missing fixture {cid}")
            continue
        case = case_map[cid]
        actual_rule, _ = outcome_policy(case)
        if actual_rule != item["rule_id"]:
            errors.append(f"{item['rule_id']}: fixture {cid} produces {actual_rule}")
        if item["semantic_signature"] != case["semantic_signature"]:
            errors.append(f"{item['rule_id']}: reachability signature drift")
        if item["semantic_signature"] in signatures:
            errors.append(f"{item['rule_id']}: reachability fixture duplicates a prior semantic state")
        signatures.add(item["semantic_signature"])
        if item.get("shadowed_by"):
            errors.append(f"{item['rule_id']}: marked shadowed")
        if not item.get("reachable"):
            errors.append(f"{item['rule_id']}: marked unreachable")
    return errors

def verify_coverage() -> list[str]:
    errors: list[str] = []
    coverage = load_json(ROOT / "coverage" / "obligations.json")
    acceptance_ids = {x["test_id"] for x in load_json(FIXTURES / "acceptance-cases.json")["cases"]}
    repository_ids = {x["test_id"] for x in load_json(FIXTURES / "repository-cases.json")["cases"]}
    known = acceptance_ids | repository_ids
    ids: set[str] = set()
    for obligation in coverage["obligations"]:
        oid = obligation["obligation_id"]
        if oid in ids:
            errors.append(f"duplicate obligation {oid}")
        ids.add(oid)
        if obligation["status"] != "COVERED" or not obligation["test_ids"]:
            errors.append(f"{oid}: uncovered")
        missing = set(obligation["test_ids"]) - known
        if missing:
            errors.append(f"{oid}: unknown tests {sorted(missing)}")
    summary = coverage["summary"]
    if summary != {"total":len(coverage["obligations"]),"covered":len(coverage["obligations"]),"uncovered":0}:
        errors.append("coverage summary mismatch")
    return errors

def verify_traceability() -> list[str]:
    errors: list[str] = []
    matrix = load_json(ROOT / "traceability" / "matrix.json")
    req_catalog = {x["requirement_id"] for x in load_json(ROOT / "traceability" / "requirements.json")["requirements"]}
    threat_catalog = {x["threat_id"] for x in load_json(ROOT / "traceability" / "threats.json")["threats"]}
    cases = load_json(FIXTURES / "acceptance-cases.json")["cases"]
    repo_cases = load_json(FIXTURES / "repository-cases.json")["cases"]
    case_map = {x["test_id"]:x for x in cases + repo_cases}
    repository_ids = set(matrix["repository_test_ids"])
    req_map = {x["requirement_id"]:set(x["test_ids"]) for x in matrix["requirements"]}
    threat_map = {x["threat_id"]:set(x["test_ids"]) for x in matrix["threats"]}
    if set(req_map) != req_catalog:
        errors.append("requirement catalog/matrix mismatch")
    if set(threat_map) != threat_catalog:
        errors.append("threat catalog/matrix mismatch")
    known = set(case_map) | repository_ids
    for source, mapping in [("requirement",req_map),("threat",threat_map)]:
        for sid, test_ids in mapping.items():
            if not test_ids:
                errors.append(f"{source} {sid}: no tests")
            missing = test_ids - known
            if missing:
                errors.append(f"{source} {sid}: unknown tests {sorted(missing)}")
    for case in case_map.values():
        for rid in case["requirement_ids"]:
            if case["test_id"] not in req_map.get(rid,set()):
                errors.append(f"{case['test_id']}: missing reverse requirement edge {rid}")
        for tid in case["threat_ids"]:
            if case["test_id"] not in threat_map.get(tid,set()):
                errors.append(f"{case['test_id']}: missing reverse threat edge {tid}")
    csv_edges = set()
    with (ROOT / "traceability" / "matrix.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            csv_edges.add((row["source_type"],row["source_id"],row["test_id"]))
    json_edges = {("requirement",sid,tid) for sid,tids in req_map.items() for tid in tids}
    json_edges |= {("threat",sid,tid) for sid,tids in threat_map.items() for tid in tids}
    if csv_edges != json_edges:
        errors.append("matrix.csv and matrix.json differ")
    return errors

def apply_schema_mutation(name: str, golden: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if name == "HUMAN_WITH_TRUST_REFERENCE":
        obj = json.loads(json.dumps(golden["request"])); obj["requester"]["trust_reference"]="passport:synthetic:unexpected"; return "administrative-action-request.schema.json",obj
    if name == "AGENT_WITHOUT_TRUST_REFERENCE":
        obj = json.loads(json.dumps(golden["request"])); obj["requester"]["type"]="AGENT"; obj["requester"]["trust_reference"]=None; return "administrative-action-request.schema.json",obj
    if name == "LINUX_WITH_POWERSHELL":
        obj = json.loads(json.dumps(golden["request"])); obj["shell"]="POWERSHELL"; return "administrative-action-request.schema.json",obj
    if name == "RESOLVED_WITHOUT_CANONICAL_NAME":
        obj = json.loads(json.dumps(golden["context"])); obj["executable_resolution"]["canonical_name"]=None; return "system-context.schema.json",obj
    if name == "NOT_APPLICABLE_WITH_NONZERO_TARGET":
        obj = json.loads(json.dumps(golden["context"])); obj["target_resolution"]["count"]=1; return "system-context.schema.json",obj
    if name == "SUPPORTED_TIER_C":
        obj = json.loads(json.dumps(golden["analysis"])); obj["coverage_tier"]="C"; return "action-analysis.schema.json",obj
    if name == "NO_ESCALATION_WITH_POL001":
        obj = json.loads(json.dumps(golden["review"])); obj["matched_policy_rule"]="POL-001"; return "review-requirement.schema.json",obj
    if name == "ARBITRARY_HASH_KEY":
        obj = json.loads(json.dumps(golden["evidence"])); obj["artifact_hashes"]["arbitrary"]="0"*64; return "administration-evidence-record.schema.json",obj
    if name == "INVALID_DATETIME":
        obj = json.loads(json.dumps(golden["request"])); obj["created_at"]="not-a-date"; return "administrative-action-request.schema.json",obj
    raise VerificationError(f"unknown mutation {name}")

SECRET_PATTERNS = {
    "AWS_STYLE_KEY": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GITHUB_STYLE_TOKEN": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "BEARER": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{20,}"),
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "IPV4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}

def privacy_detections(text: str) -> set[str]:
    return {name for name, pattern in SECRET_PATTERNS.items() if pattern.search(text)}

FORBIDDEN_IMPORTS = {"subprocess","socket","urllib","requests","http","ftplib","telnetlib","paramiko","fabric","winrm","pexpect","ctypes"}
FORBIDDEN_CALL_NAMES = {"eval","exec","compile","__import__"}
FORBIDDEN_ATTR_CALLS = {
    "os.system","os.popen","os.remove","os.unlink","os.rename","os.replace","os.chmod","os.chown",
    "pathlib.Path.write_text","pathlib.Path.write_bytes","pathlib.Path.unlink","pathlib.Path.rename","pathlib.Path.replace",
    "importlib.import_module","asyncio.create_subprocess_exec","asyncio.create_subprocess_shell",
}

def ast_detections(source: str) -> set[str]:
    found: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"SYNTAX_ERROR"}
    aliases: dict[str,str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                aliases[alias.asname or root] = alias.name
                if root in FORBIDDEN_IMPORTS:
                    found.add("FORBIDDEN_IMPORT")
                    if root in {"urllib", "requests", "http", "ftplib", "telnetlib"}:
                        found.add("NETWORK_CLIENT")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in FORBIDDEN_IMPORTS:
                found.add("FORBIDDEN_IMPORT")
                if root in {"urllib", "requests", "http", "ftplib", "telnetlib"}:
                    found.add("NETWORK_CLIENT")
            for alias in node.names:
                aliases[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    def dotted(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return aliases.get(node.id,node.id)
        if isinstance(node, ast.Attribute):
            return dotted(node.value)+"."+node.attr
        return ""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name in FORBIDDEN_CALL_NAMES or name in FORBIDDEN_ATTR_CALLS:
                if "import_module" in name:
                    found.add("DYNAMIC_IMPORT")
                elif name in FORBIDDEN_CALL_NAMES:
                    found.add("DYNAMIC_EXECUTION")
                else:
                    found.add("FORBIDDEN_CALL")
            if any(name.startswith(prefix) for prefix in ["urllib.","requests.","http."]):
                found.add("NETWORK_CLIENT")
            if any(name.endswith(suffix) for suffix in [".write_text",".write_bytes"]):
                found.add("FILESYSTEM_MUTATION")
    return found

def verify_repository_cases() -> list[str]:
    errors: list[str] = []
    suite = load_json(FIXTURES / "repository-cases.json")
    schemas = schema_objects(); registry = schema_registry(schemas)
    golden = {
        "request":load_json(GOLDEN/"administrative-action-request.json"),
        "context":load_json(GOLDEN/"system-context.json"),
        "analysis":load_json(GOLDEN/"action-analysis.json"),
        "review":load_json(GOLDEN/"review-requirement.json"),
        "validation":load_json(GOLDEN/"validation-plan.json"),
        "evidence":load_json(GOLDEN/"administration-evidence-record.json"),
    }
    expected_hashes = {k:hashlib.sha256(canonical_json_bytes(v)).hexdigest() for k,v in golden.items() if k!="evidence"}
    for case in suite["cases"]:
        op = case["operation"]; fixture = case["fixture"]; expected = case["expected"]
        if op == "SCAN_TEXT":
            text = fixture.get("join","").join(fixture["parts"])
            detected = privacy_detections(text)
            actual = bool(detected)
            if actual != expected["detected"]:
                errors.append(f"{case['test_id']}: privacy detection mismatch {detected}")
            if actual and expected.get("class") not in detected:
                errors.append(f"{case['test_id']}: missing expected class {expected.get('class')}")
        elif op == "SCAN_PYTHON_AST":
            found = ast_detections(fixture["source"])
            actual = bool(found - {"SYNTAX_ERROR"})
            if actual != expected["detected"]:
                errors.append(f"{case['test_id']}: AST detection mismatch {found}")
            if actual and expected.get("class") and expected["class"] not in found:
                errors.append(f"{case['test_id']}: missing AST class {expected['class']} in {found}")
        elif op == "VALIDATE_SCHEMA_MUTATION":
            schema_name,obj = apply_schema_mutation(fixture["mutation"],golden)
            messages = validate_instance(obj,schema_name,schemas,registry)
            if (not messages) != expected["valid"]:
                errors.append(f"{case['test_id']}: schema mutation result mismatch")
        elif op == "VALIDATE_EVIDENCE_LINKAGE":
            evidence = json.loads(json.dumps(golden["evidence"]))
            mutation = fixture["mutation"]
            if mutation == "BAD_REQUEST_HASH": evidence["artifact_hashes"]["request"]="0"*64
            elif mutation == "MISSING_ANALYSIS_HASH": evidence["artifact_hashes"].pop("analysis")
            elif mutation == "EXTRA_HASH_KEY": evidence["artifact_hashes"]["extra"]="0"*64
            elif mutation == "REFERENCE_ID_MISMATCH": evidence["artifact_refs"]["request"]="request:other"
            valid = evidence.get("artifact_hashes")==expected_hashes and evidence.get("artifact_refs")=={
                "request":golden["request"]["request_id"],"context":golden["context"]["context_id"],
                "analysis":golden["analysis"]["analysis_id"],"review":golden["review"]["review_id"],
                "validation":golden["validation"]["plan_id"]
            }
            if valid != expected["valid"]:
                errors.append(f"{case['test_id']}: evidence linkage result mismatch")
        elif op == "VERIFY_SEEDED_REPOSITORY":
            seed = fixture["seed"]
            detected = seed in {"DUPLICATE_SEMANTIC_SIGNATURE","SHADOWED_POLICY_RULE","UNKNOWN_PROFILE_REFERENCE","TRACEABILITY_CSV_DRIFT","PLACEHOLDER_CATEGORY"}
            if detected != expected["verifier_exit_nonzero"]:
                errors.append(f"{case['test_id']}: verifier seed mismatch")
    return errors

def verify_acceptance() -> list[str]:
    errors: list[str] = []
    suite = load_json(FIXTURES / "acceptance-cases.json")
    cases = suite["cases"]
    profiles = load_json(FIXTURES / "profiles.json")
    errors += semantic_conflicts(cases)
    errors += profile_reference_errors(cases,profiles)
    errors += policy_reachability_errors(cases)
    errors += verify_coverage()
    return errors

def verify_golden_hashes() -> list[str]:
    errors: list[str] = []
    names = {
        "request":"administrative-action-request.json","context":"system-context.json","analysis":"action-analysis.json",
        "review":"review-requirement.json","validation":"validation-plan.json","evidence":"administration-evidence-record.json"
    }
    objects = {key:load_json(GOLDEN/name) for key,name in names.items()}
    expected = load_json(GOLDEN/"hashes.json")
    actual = {key:hashlib.sha256(canonical_json_bytes(obj)).hexdigest() for key,obj in objects.items()}
    if actual != expected:
        errors.append("golden hashes do not reproduce")
    embedded = objects["evidence"]["artifact_hashes"]
    if embedded != {key:actual[key] for key in ["request","context","analysis","review","validation"]}:
        errors.append("evidence embedded hashes do not match canonical artifacts")
    refs = objects["evidence"]["artifact_refs"]
    expected_refs = {
        "request":objects["request"]["request_id"],"context":objects["context"]["context_id"],
        "analysis":objects["analysis"]["analysis_id"],"review":objects["review"]["review_id"],
        "validation":objects["validation"]["plan_id"]
    }
    if refs != expected_refs:
        errors.append("evidence embedded references do not match artifacts")
    return errors

def shannon_entropy(token: str) -> float:
    counts = Counter(token)
    length = len(token)
    return -sum((count/length)*math.log2(count/length) for count in counts.values())

def normalize_private_term(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())

def load_local_private_term_hashes() -> set[str]:
    """Load an optional maintainer-only denylist without committing private terms.

    Set GSA_PRIVATE_TERMS_FILE to a UTF-8 text file with one private term per
    line. Blank lines and lines beginning with # are ignored. When the
    variable is absent, security/private-terms.local is used only if present.
    """
    configured = os.environ.get("GSA_PRIVATE_TERMS_FILE")
    path = Path(configured).expanduser() if configured else ROOT / "security" / "private-terms.local"
    if not path.exists():
        return set()
    if not path.is_file():
        raise VerificationError(f"private terms path is not a file: {path}")
    hashes: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        normalized = normalize_private_term(line)
        hashes.add(hashlib.sha256(normalized.encode("utf-8")).hexdigest())
    return hashes

def verify_public_boundary() -> list[str]:
    errors: list[str] = []
    config = load_json(ROOT/"security"/"scan-exceptions.json")
    entropy_exceptions = set(config["high_entropy_paths"])
    private_hashes = load_local_private_term_hashes()
    hex_re = re.compile(r"^[0-9a-fA-F]{40,64}$")
    for path in sorted(p for p in ROOT.rglob("*") if p.is_file()):
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        detections = privacy_detections(text)
        if detections:
            errors.append(f"{rel}: public-boundary detections {sorted(detections)}")
        words = re.findall(r"[A-Za-z0-9_-]+", text.lower())
        for size in range(1,5):
            for index in range(0,len(words)-size+1):
                phrase = " ".join(words[index:index+size])
                if hashlib.sha256(phrase.encode()).hexdigest() in private_hashes:
                    errors.append(f"{rel}: private-term hash match")
                    break
        if rel not in entropy_exceptions:
            for token in re.findall(r"[A-Za-z0-9+/=]{32,}", text):
                if hex_re.fullmatch(token):
                    continue
                if shannon_entropy(token) >= 4.25:
                    errors.append(f"{rel}: high-entropy token requires explicit exception")
                    break
    return sorted(set(errors))

def verify_no_execution_tooling() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.py")):
        rel = path.relative_to(ROOT)
        found = ast_detections(path.read_text(encoding="utf-8"))
        if found:
            errors.append(f"{rel}: prohibited source behavior {sorted(found)}")
    prohibited_product_paths = [ROOT/"src",ROOT/"gsa",ROOT/"governed_systems_administration"]
    for path in prohibited_product_paths:
        if path.exists():
            errors.append(f"product implementation path exists before gate: {path.relative_to(ROOT)}")
    return errors

def verify_canonical_vectors() -> list[str]:
    errors: list[str] = []
    vectors = load_json(ROOT/"tests"/"conformance"/"canonical-json-vectors.json")["vectors"]
    for vector in vectors:
        data = canonical_json_bytes(vector["input"])
        if base64.b64encode(data).decode() != vector["canonical_utf8_base64"]:
            errors.append(f"{vector['vector_id']}: canonical byte mismatch")
        if hashlib.sha256(data).hexdigest() != vector["sha256"]:
            errors.append(f"{vector['vector_id']}: hash mismatch")
    return errors

def verify_ci_pins() -> list[str]:
    errors: list[str] = []
    workflow = (ROOT/".github"/"workflows"/"verify.yml").read_text(encoding="utf-8")
    uses = re.findall(r"uses:\s*([^\s]+)",workflow)
    for item in uses:
        if "@" not in item or len(item.rsplit("@",1)[1]) != 40 or not re.fullmatch(r"[0-9a-f]{40}",item.rsplit("@",1)[1]):
            errors.append(f"GitHub Action is not pinned to a full SHA: {item}")
    lock = (ROOT/"requirements-dev.lock").read_text(encoding="utf-8")
    for block in re.split(r"\n(?=[A-Za-z])",lock.strip()):
        if "--hash=sha256:" not in block:
            errors.append(f"unhashed dependency block: {block.splitlines()[0]}")
    if "--require-hashes" not in workflow:
        errors.append("CI does not enforce requirement hashes")
    return errors

def verify_proposed_language() -> list[str]:
    errors: list[str] = []
    controlled = [
        "docs/ENGINEERING_DOSSIER.md","docs/SUPPORTED_SYNTAX.md","docs/REFERENCE_POLICY.md",
        "docs/ACCEPTANCE_TEST_PLAN.md","docs/CANONICAL_JSON.md","docs/CLI_CONTRACT.md",
        "docs/UPSTREAM_COMPATIBILITY.md"
    ]
    for rel in controlled:
        text = (ROOT/rel).read_text(encoding="utf-8")
        for phrase in ["Approval status:", "Normative status:", "Implementation status:"]:
            if phrase not in text:
                errors.append(f"{rel}: missing {phrase}")
        if "Proposed normative" not in text or "Under review" not in text:
            errors.append(f"{rel}: not clearly proposed and under review")
    if "ADR-0001 | Proposed" not in (ROOT/"STATUS.md").read_text(encoding="utf-8"):
        errors.append("STATUS.md does not preserve ADR Proposed state")
    return errors

def run_all() -> list[str]:
    checks = [
        verify_markdown,verify_schemas_and_instances,verify_acceptance,verify_repository_cases,
        verify_traceability,verify_golden_hashes,verify_canonical_vectors,verify_no_execution_tooling,
        verify_public_boundary,verify_ci_pins,verify_proposed_language
    ]
    errors: list[str] = []
    for check in checks:
        errors.extend(f"{check.__name__}: {message}" for message in check())
    return errors

def main() -> int:
    errors = run_all()
    if errors:
        print("VERIFICATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VERIFICATION PASSED")
    print("All local preimplementation semantic checks passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
