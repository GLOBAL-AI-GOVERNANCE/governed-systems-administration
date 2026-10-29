#!/usr/bin/env bash
# Live-resolve every schema $id and require the published JSON to match the local file.
# Offline form checks stay in tools/check_schema_ids.py (no network imports there).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/tools/check_schema_ids.py"
fail=0
count=0
while IFS= read -r -d '' file; do
  id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1],encoding="utf-8"))["$id"])' "$file")"
  case "$id" in
    http://*|https://*) ;;
    *) continue ;;
  esac
  count=$((count + 1))
  tmp="$(mktemp)"
  if ! curl -fsSL --retry 5 --retry-delay 2 --max-time 30 "$id" -o "$tmp"; then
    echo "$id: fetch failed" >&2
    rm -f "$tmp"
    fail=1
    continue
  fi
  if ! python3 -c 'import json,sys; a=json.load(open(sys.argv[1],encoding="utf-8")); b=json.load(open(sys.argv[2],encoding="utf-8")); raise SystemExit(0 if a==b else 1)' "$file" "$tmp"; then
    echo "$id: published document differs from ${file#$ROOT/}" >&2
    fail=1
  fi
  rm -f "$tmp"
done < <(find "$ROOT/schemas" -name '*.json' -print0)
if [[ "$fail" -ne 0 ]]; then
  exit 1
fi
echo "schema \$id check passed for ${count} schema(s) (online)"
