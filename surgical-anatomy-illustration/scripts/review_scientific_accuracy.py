#!/usr/bin/env python3
"""Create a structured scientific accuracy review checklist for a job.

This script does not claim to inspect pixels by itself. It turns the skill's
template constraints into a review form that a clinician, illustrator, or
vision-capable model can score after image generation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_job(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Job JSON must be an object.")
    return data


def _blank_result(item: str) -> dict[str, str]:
    return {
        "item": item,
        "status": "unchecked",
        "evidence": "",
        "correction_needed": "",
    }


def build_review(job: dict[str, Any]) -> dict[str, Any]:
    skill = job.get("skill") if isinstance(job.get("skill"), dict) else {}
    review = job.get("scientific_review") if isinstance(job.get("scientific_review"), dict) else {}
    checks = review.get("checks") if isinstance(review.get("checks"), list) else []

    sections: list[dict[str, Any]] = []
    for section in checks:
        if not isinstance(section, dict):
            continue
        items = section.get("items") if isinstance(section.get("items"), list) else []
        sections.append(
            {
                "category": str(section.get("category") or "uncategorized"),
                "results": [_blank_result(str(item)) for item in items if str(item).strip()],
            }
        )

    return {
        "topic": str(job.get("topic") or ""),
        "template": str(skill.get("surgical_template") or ""),
        "review_status": "pending_visual_review",
        "review_scale": {
            "correct": "Visible and anatomically correct. | 可见且解剖正确。",
            "wrong": "Visible but anatomically wrong, unsafe, or misleading; state the correct relationship. | 可见但解剖错误/不安全/有误导；写明正确关系。",
            "needs_manual_verification": "Suspicious or borderline; a human expert should confirm. | 可疑或拿不准；需专家确认。",
            "cannot_verify": "Image too unclear or occluded to judge; verify manually. | 图像太糊/被遮挡，无法判断；请人工核。",
            "not_applicable": "Not required for this specific requested figure. | 本图不要求此项。",
        },
        "sections": sections,
        "overall_decision": {
            "status": "unchecked",
            "acceptable_for_draft": "",
            "must_regenerate": "",
            "notes": "",
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a structured scientific review checklist from a job JSON.")
    parser.add_argument("job")
    parser.add_argument("--output", help="Write review JSON to this path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = build_review(_load_job(args.job))
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
