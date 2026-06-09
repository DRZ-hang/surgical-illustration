#!/usr/bin/env python3
"""Generate a correction prompt from a scientific review report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ACTION_BY_CATEGORY = {
    "required_anatomy": "Add or clarify the missing required anatomy.",
    "spatial_relationships": "Correct the anatomical spatial relationship.",
    "forbidden_errors": "Remove the unsafe or scientifically wrong depiction.",
    "step_completeness": "Add or redraw the missing procedural step.",
    "post_generation_review": "Revise the image to satisfy the post-generation safety check.",
    "segment_geometry": "Correct liver segment geometry and label ownership.",
    "vascular_planes": "Correct vascular planes and vessel identity.",
    "duct_connections": "Correct biliary duct connections.",
}


def _load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")
    return data


def _problem_items(review: dict[str, Any]) -> list[dict[str, str]]:
    problems: list[dict[str, str]] = []
    sections = review.get("sections") if isinstance(review.get("sections"), list) else []
    for section in sections:
        if not isinstance(section, dict):
            continue
        category = str(section.get("category") or "uncategorized")
        results = section.get("results") if isinstance(section.get("results"), list) else []
        for result in results:
            if not isinstance(result, dict):
                continue
            status = str(result.get("status") or "").strip().lower()
            if status not in {"wrong", "needs_manual_verification", "cannot_verify"}:
                continue
            item = str(result.get("item") or "").strip()
            if not item:
                continue
            problems.append(
                {
                    "category": category,
                    "status": status,
                    "item": item,
                    "evidence": str(result.get("evidence") or "").strip(),
                    "correction_needed": str(result.get("correction_needed") or "").strip(),
                }
            )
    return problems


def _base_prompt_from_job(job: dict[str, Any] | None) -> str:
    if not job:
        return ""
    prompt = str(job.get("prompt") or "").strip()
    negative = str(job.get("negative_prompt") or "").strip()
    if not prompt:
        return ""
    if negative:
        return f"{prompt}\n\nNEGATIVE PROMPT:\n{negative}"
    return prompt


def build_correction_prompt(review: dict[str, Any], job: dict[str, Any] | None = None) -> dict[str, Any]:
    problems = _problem_items(review)
    topic = str(review.get("topic") or (job or {}).get("topic") or "").strip()
    template = str(review.get("template") or ((job or {}).get("skill") or {}).get("surgical_template") or "").strip()
    base_prompt = _base_prompt_from_job(job)

    severity = "pass"
    if any(item["status"] == "wrong" for item in problems):
        severity = "must_regenerate_or_revise"
    elif any(item["status"] in {"needs_manual_verification", "cannot_verify"} for item in problems):
        severity = "needs_targeted_revision"

    lines = [
        "CORRECTION PROMPT",
        "",
        f"Topic: {topic or 'same surgical/anatomy illustration'}",
        f"Template: {template or 'unspecified'}",
        "",
    ]
    if not problems:
        lines.extend(
            [
                "No failed or uncertain scientific review items were provided.",
                "Do not regenerate unless the reviewer adds a specific correction target.",
            ]
        )
    else:
        lines.extend(
            [
                "Revise or regenerate the image to fix the scientific accuracy issues below.",
                "Preserve all panels and anatomy that were already correct.",
                "Do not introduce new ducts, vessels, nerves, tissue planes, or operative steps.",
                "",
                "Problems to fix:",
            ]
        )
        for idx, item in enumerate(problems, start=1):
            action = ACTION_BY_CATEGORY.get(item["category"], "Correct this scientific issue.")
            lines.append(f"{idx}. [{item['status'].upper()}] {item['category']}: {item['item']}")
            lines.append(f"   Required action: {item['correction_needed'] or action}")
            if item["evidence"]:
                lines.append(f"   Evidence: {item['evidence']}")
        lines.extend(
            [
                "",
                "Hard constraints for the revision:",
                "- Keep the figure non-gory and publication-appropriate.",
                "- Keep anatomical laterality and spatial relationships coherent.",
                "- If a corrected structure cannot be shown clearly, simplify the panel rather than guessing.",
                "- After revision, re-run the scientific review checklist.",
            ]
        )
    if base_prompt:
        lines.extend(["", "Original generation prompt for context:", base_prompt])

    return {
        "topic": topic,
        "template": template,
        "severity": severity,
        "problem_count": len(problems),
        "problems": problems,
        "correction_prompt": "\n".join(lines).strip(),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a correction prompt from a scientific review JSON.")
    parser.add_argument("review", help="Scientific review JSON scored with the four-category scale (wrong / needs_manual_verification / cannot_verify drive correction).")
    parser.add_argument("--job", help="Optional original job JSON for prompt context.")
    parser.add_argument("--output", help="Write correction JSON to this path.")
    parser.add_argument("--text-output", help="Write only the correction prompt text to this path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    review = _load_json(args.review)
    job = _load_json(args.job) if args.job else None
    result = build_correction_prompt(review, job)
    if args.text_output:
        Path(args.text_output).write_text(str(result["correction_prompt"]) + "\n", encoding="utf-8")
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
