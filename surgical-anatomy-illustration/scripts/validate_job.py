#!/usr/bin/env python3
"""Lightweight validation for generated medical illustration jobs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = (
    "prompt",
    "negative_prompt",
    "review_checklist",
    "params",
    "platform_result",
    "knowledge",
    "scientific_review",
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a medical illustration job JSON file.")
    parser.add_argument("job")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    job = json.loads(Path(args.job).read_text(encoding="utf-8"))
    errors = []
    for key in REQUIRED:
        if key not in job:
            errors.append(f"Missing required key: {key}")
    if not str(job.get("prompt") or "").strip():
        errors.append("Prompt is empty.")
    if not isinstance(job.get("review_checklist"), list) or not job.get("review_checklist"):
        errors.append("review_checklist must be a non-empty list.")
    if job.get("watermark") is not False:
        errors.append("Skill job must set watermark=false.")
    knowledge = job.get("knowledge")
    if not isinstance(knowledge, dict):
        errors.append("knowledge must be an object.")
    else:
        if not isinstance(knowledge.get("matched"), bool):
            errors.append("knowledge.matched must be a boolean.")
        if not str(knowledge.get("tier") or "").strip():
            errors.append("knowledge.tier is required.")
        if knowledge.get("matched") and not str(knowledge.get("id") or "").strip():
            errors.append("knowledge.id is required when knowledge.matched=true.")

    scientific_review = job.get("scientific_review")
    if not isinstance(scientific_review, dict):
        errors.append("scientific_review must be an object.")
    else:
        status = str(scientific_review.get("status") or "").strip()
        if not status:
            errors.append("scientific_review.status is required.")
        if not isinstance(scientific_review.get("checks"), list) or not scientific_review.get("checks"):
            errors.append("scientific_review.checks must be a non-empty list.")
        if isinstance(knowledge, dict) and knowledge.get("matched") is False and status != "source_required":
            errors.append("scientific_review.status must be source_required when knowledge.matched=false.")

    sys.stdout.reconfigure(encoding="utf-8")
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
