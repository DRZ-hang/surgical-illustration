#!/usr/bin/env python3
"""Run the surgical anatomy illustration planning + review workflow.

Outputs the scientific brief: the job (prompt + constraints + assumptions),
a copy-ready prompt, and the four-category review form. It does NOT generate
images — render the prompt in your own image tool, then bring the image back
for the scientific review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from correction_prompt import build_correction_prompt
from med_illustration_job import build_task_job
from review_scientific_accuracy import build_review


def _slug(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return text[:80] or "surgical_anatomy_illustration"


def _load_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON input must be an object.")
    return data


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _task_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.task:
        task = _load_json(args.task)
    else:
        if not args.topic:
            raise SystemExit("Provide a topic or --task JSON.")
        task = {
            "topic": args.topic,
            "mode": args.mode,
            "style": args.style,
            "composition": args.composition,
            "size": args.size,
            "extra": args.extra,
            "surgical_template": args.surgical_template,
            "output": {
                "platform": args.platform,
                "prompt_target": args.prompt_target,
            },
        }
    task.setdefault("output", {})
    if args.prompt_target:
        task["output"]["prompt_target"] = args.prompt_target
    if args.platform:
        task["output"]["platform"] = args.platform
    return task


def run_workflow(args: argparse.Namespace) -> dict[str, Any]:
    task = _task_from_args(args)
    job = build_task_job(task)
    topic = str(job.get("topic") or task.get("topic") or "")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or _slug(topic)

    job_path = output_dir / f"{prefix}_job.json"
    prompt_path = output_dir / f"{prefix}_prompt.txt"
    review_path = output_dir / f"{prefix}_review.json"

    review = build_review(job)
    _write_json(job_path, job)
    prompt_path.write_text(str(job["platform_result"]["copy_prompt"]) + "\n", encoding="utf-8")
    _write_json(review_path, review)

    result: dict[str, Any] = {
        "topic": topic,
        "template": str((job.get("skill") or {}).get("surgical_template") or ""),
        "job": str(job_path),
        "prompt": str(prompt_path),
        "review": str(review_path),
        "correction": None,
        "correction_prompt": None,
        "next_step": "Render the prompt in your own image tool, then score review.json on the result with the four-category scale (correct / wrong / needs_manual_verification / cannot_verify).",
    }

    if args.scored_review:
        scored_review = _load_json(args.scored_review)
        correction = build_correction_prompt(scored_review, job)
        correction_path = output_dir / f"{prefix}_correction.json"
        correction_prompt_path = output_dir / f"{prefix}_correction_prompt.txt"
        _write_json(correction_path, correction)
        correction_prompt_path.write_text(str(correction["correction_prompt"]) + "\n", encoding="utf-8")
        result["correction"] = str(correction_path)
        result["correction_prompt"] = str(correction_prompt_path)
        result["next_step"] = "Use correction_prompt.txt to revise the figure, then re-score the review."

    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the job + prompt + scientific review brief (no image generation).")
    parser.add_argument("topic", nargs="?", help="Surgical or anatomy illustration topic.")
    parser.add_argument("--task", help="Optional task JSON instead of topic arguments.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for workflow artifacts.")
    parser.add_argument("--prefix", help="Output filename prefix. Defaults to a topic slug.")
    parser.add_argument("--mode", default="surgical", choices=["surgical", "anatomy", "edit"])
    parser.add_argument("--style", default="nejm", choices=["nejm", "netter", "vector"])
    parser.add_argument("--composition", default="sequence", choices=["plate", "hero", "sequence"])
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--platform", default="auto")
    parser.add_argument("--prompt-target", default="universal")
    parser.add_argument("--extra", default="")
    parser.add_argument("--surgical-template", default="")
    parser.add_argument("--scored-review", help="Already scored review JSON; generate correction artifacts too.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = run_workflow(args)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
