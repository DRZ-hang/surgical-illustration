#!/usr/bin/env python3
"""Load and match surgical/anatomy knowledge entries.

Knowledge lives outside the code, one JSON file per procedure under
`knowledge/`, following the schema in `docs/knowledge-architecture.md`.
This lets the library grow over time and lets verified, expert-reviewed
entries persist (the skill's "memory"), while everything else is generated
on demand and stored as `tier: model_generated`.

Stored as JSON (not YAML) on purpose: the whole codebase stays pure-stdlib
with zero third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def _load_all() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not KNOWLEDGE_DIR.is_dir():
        return entries
    for path in sorted(KNOWLEDGE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("id"):
            data["_file"] = path.name
            entries.append(data)
    return entries


def list_entries() -> list[dict[str, Any]]:
    """Return all knowledge entries."""
    return _load_all()


def get_entry(entry_id: str) -> Optional[dict[str, Any]]:
    """Return one entry by exact id."""
    for entry in _load_all():
        if str(entry.get("id")) == entry_id:
            return entry
    return None


def match_topic(topic: str) -> Optional[dict[str, Any]]:
    """Match a free-text topic to an entry by id, name, or alias.

    Prefers the longest matching key so that, e.g., "lap splenectomy"
    beats a shorter generic alias. Returns None when nothing matches;
    the caller should then generate a model_generated entry on demand.
    """
    text = (topic or "").lower()
    best: Optional[tuple[dict[str, Any], int]] = None
    for entry in _load_all():
        keys = [str(entry.get("id", "")), str(entry.get("name", ""))]
        keys += [str(a) for a in (entry.get("aliases") or [])]
        for key in keys:
            k = key.strip().lower()
            if k and k in text and (best is None or len(k) > best[1]):
                best = (entry, len(k))
    return best[0] if best else None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect the knowledge library.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="List all entries with id, tier, and confidence.")
    p_get = sub.add_parser("get", help="Print one entry by id.")
    p_get.add_argument("id")
    p_match = sub.add_parser("match", help="Match a free-text topic to an entry.")
    p_match.add_argument("topic")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    if args.cmd == "list":
        rows = [
            {
                "id": e.get("id"),
                "name": e.get("name"),
                "tier": e.get("tier"),
                "confidence": e.get("confidence"),
                "file": e.get("_file"),
            }
            for e in list_entries()
        ]
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "get":
        entry = get_entry(args.id)
        if not entry:
            print(json.dumps({"ok": False, "reason": "not_found", "id": args.id}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "match":
        entry = match_topic(args.topic)
        if not entry:
            print(json.dumps({"ok": False, "reason": "no_match", "topic": args.topic, "next": "generate model_generated entry on demand"}, ensure_ascii=False, indent=2))
            return 1
        print(json.dumps({"ok": True, "id": entry.get("id"), "tier": entry.get("tier"), "name": entry.get("name")}, ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
