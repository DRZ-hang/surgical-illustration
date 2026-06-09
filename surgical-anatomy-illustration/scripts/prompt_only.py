#!/usr/bin/env python3
"""Print a copy-ready prompt package from a medical illustration task/job."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from med_illustration_job import build_task_job


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a copy-ready medical illustration prompt.")
    parser.add_argument("topic", nargs="?", help="Illustration topic when --input is not provided.")
    parser.add_argument("--input", help="Path to task JSON.")
    parser.add_argument("--target", default="universal", help="universal, chatgpt, gemini, jimeng, or midjourney")
    parser.add_argument("--mode", default="surgical")
    parser.add_argument("--style", default="nejm")
    parser.add_argument("--composition", default="plate")
    parser.add_argument("--extra", default="")
    parser.add_argument("--output", help="Write the copy-ready prompt package to this path.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.input:
        task = json.loads(Path(args.input).read_text(encoding="utf-8"))
        platform_result = task.get("platform_result") if isinstance(task, dict) else {}
        if isinstance(platform_result, dict) and platform_result.get("copy_prompt"):
            text = str(platform_result["copy_prompt"])
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
                return 0
            sys.stdout.reconfigure(encoding="utf-8")
            print(text)
            return 0
    else:
        if not args.topic:
            raise SystemExit("Provide a topic or --input task JSON.")
        task = {
            "topic": args.topic,
            "mode": args.mode,
            "style": args.style,
            "composition": args.composition,
            "extra": args.extra,
            "output": {
                "prompt_target": args.target,
                "generate_image": False,
            },
        }

    task.setdefault("output", {})
    task["output"]["prompt_target"] = args.target
    task["output"]["generate_image"] = False
    job = build_task_job(task)
    text = str(job["platform_result"]["copy_prompt"])
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        return 0

    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
