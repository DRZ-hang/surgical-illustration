#!/usr/bin/env python3
"""Build a standalone surgical anatomy illustration prompt job.

Procedure knowledge lives outside the code, one JSON file per procedure under
`knowledge/` (see `docs/knowledge-architecture.md`). This module loads the
matching entry through `knowledge.py` and assembles the prompt, review
checklist, and structured scientific review from it.

When no entry matches, the script still produces a usable generic prompt and a
`source_required` review; the agent (per SKILL.md) is expected to generate a
model_generated constraint set on demand for known procedures, or ask for a
source for genuinely novel ones.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from knowledge import get_entry, match_topic


STYLE_PROFILES: dict[str, dict[str, str]] = {
    "nejm": {
        "name": "NEJM-style clinical figure",
        "positive": (
            "publication-grade medical illustration, muted academic palette, "
            "soft airbrushed tissue rendering, thin precise dark-grey outlines, "
            "off-white background, clean journal figure composition"
        ),
        "avoid": "glossy CGI, cinematic lighting, neon saturation, poster-like contrast",
    },
    "netter": {
        "name": "Netter-style anatomy atlas plate",
        "positive": (
            "hand-painted medical atlas illustration, warm anatomical colors, "
            "subtle gouache texture, soft contour transitions, textbook clarity"
        ),
        "avoid": "photorealistic CGI, industrial blueprint look, generic flat icon style",
    },
    "vector": {
        "name": "clean vector surgical teaching figure",
        "positive": (
            "clean vector medical illustration, restrained color coding, crisp shapes, "
            "clear hierarchy, editorial teaching figure on white background"
        ),
        "avoid": "cartoon exaggeration, decorative gradients, messy icon collage",
    },
}


COMPOSITIONS: dict[str, str] = {
    "plate": "single anatomy plate with one dominant view and optional small inset only when needed",
    "hero": "single focused hero view with strong anatomical hierarchy and generous margins",
    "sequence": "procedure-specific multi-panel storyboard; use the template panel plan and do not force all procedures into four panels",
}


def _read_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")
    return data


def _parse_size(size: str) -> tuple[int, int]:
    raw = (size or "1024x1024").lower().replace("*", "x")
    left, _, right = raw.partition("x")
    try:
        return max(320, int(left)), max(320, int(right or left))
    except ValueError:
        return 1024, 1024


def _resolve_entry(task: dict[str, Any]) -> dict[str, Any] | None:
    """Resolve a knowledge entry from an explicit id/alias or the topic text."""
    explicit = str(task.get("surgical_template") or task.get("template") or "").strip()
    if explicit:
        entry = get_entry(explicit) or match_topic(explicit)
        if entry:
            return entry
    return match_topic(str(task.get("topic") or ""))


def _labels_for(task: dict[str, Any], entry: dict[str, Any] | None) -> list[str]:
    raw = task.get("required_labels")
    if isinstance(raw, list):
        labels = [str(item).strip() for item in raw if str(item).strip()]
        if labels:
            return labels
    if entry:
        return [str(label).strip() for label in (entry.get("labels") or []) if str(label).strip()]
    return []


def _forbidden_lines(entry: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for item in entry.get("forbidden_errors") or []:
        if isinstance(item, dict):
            error = str(item.get("error") or "").strip()
            severity = str(item.get("severity") or "").strip()
        else:
            error, severity = str(item).strip(), ""
        if error:
            out.append(f"Forbidden mistake [{severity}]: {error}" if severity else f"Forbidden mistake: {error}")
    return out


def _entry_rules(entry: dict[str, Any] | None) -> list[str]:
    """Build the '## TEMPLATE' constraint lines from a knowledge entry."""
    if not entry:
        return []
    out: list[str] = []
    if entry.get("safety_concept"):
        out.append(f"Core safety concept: {entry['safety_concept']}")
    if entry.get("laterality"):
        out.append(f"Orientation / laterality: {entry['laterality']}")
    out.extend(f"Must show: {value}" for value in (entry.get("must_have") or []))
    out.extend(f"Spatial anatomy rules: {value}" for value in (entry.get("spatial_rules") or []))
    out.extend(_forbidden_lines(entry))
    return out


def _phases(entry: dict[str, Any] | None) -> list[str]:
    return list(entry.get("phases") or []) if entry else []


def _assumptions(entry: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Surface the decisions this figure depends on, with the assumed default and
    the alternatives, so the user can redirect even on a non-interactive host
    that did not stop to ask. Built from the entry's `intake` questions."""
    if not entry:
        return []
    out: list[dict[str, Any]] = []
    for question in entry.get("intake") or []:
        if not isinstance(question, dict):
            continue
        ask = str(question.get("ask") or "").strip()
        if not ask:
            continue
        default = str(question.get("default") or "").strip()
        options = [str(o).strip() for o in (question.get("options") or []) if str(o).strip()]
        alternatives = [o for o in options if o != default]
        out.append(
            {
                "decision": ask,
                "assumed_default": default,
                "alternatives": alternatives,
                "why": str(question.get("why") or "").strip(),
            }
        )
    return out


def _prompt_adapter(target: str) -> str:
    adapters = {
        "chatgpt": "Adapter for ChatGPT/OpenAI image models: keep instructions explicit, avoid dense text inside the image, and prioritize clean publication layout.",
        "gemini": "Adapter for Gemini/Nano Banana: preserve exact composition, white background, and strict anatomy relationships.",
        "jimeng": "Adapter for Chinese image tools: keep the task brief, but include English anatomical terms for key structures.",
        "midjourney": "Adapter for Midjourney-style models: put anatomy constraints first, then compact style words; avoid long embedded labels.",
        "universal": "Universal adapter: use this prompt with ChatGPT, Gemini, Jimeng, or other image models; keep anatomy constraints and negative prompt together.",
    }
    return adapters.get(target, adapters["universal"])


def _build_prompt(task: dict[str, Any], entry: dict[str, Any] | None, labels: list[str]) -> str:
    topic = str(task["topic"]).strip()
    style_key = str(task.get("style") or "nejm").lower()
    style = STYLE_PROFILES.get(style_key, STYLE_PROFILES["nejm"])
    composition = str(task.get("composition") or "plate").lower()
    panel_plan = _phases(entry)
    if composition == "sequence" and panel_plan:
        composition_text = (
            f"{len(panel_plan)}-panel procedure storyboard following the exact panel plan below; "
            "do not compress this procedure into four panels"
        )
    else:
        composition_text = COMPOSITIONS.get(composition, COMPOSITIONS["plate"])
    extra = str(task.get("extra") or "").strip()
    mode = str(task.get("mode") or task.get("work_mode") or "surgical").lower()
    if mode == "anatomy":
        mode = "anatomical"

    lines = [
        "SYSTEM_INSTRUCTION_MODE: SURGICAL_ANATOMY_ACADEMIC",
        "",
        f"Topic: {topic}",
        f"Task type: {mode} illustration",
        f"Visual style: {style['name']}",
        f"Style cues: {style['positive']}.",
        f"Composition: {composition_text}.",
        "Background: clean white or off-white publication background.",
        "Rendering: non-gory, atraumatic, didactic, anatomy-first medical illustration.",
        "",
        "## NON-NEGOTIABLE ANATOMY RULES",
        "- Anatomy correctness outranks visual style.",
        "- Preserve left/right, medial/lateral, superior/inferior, and anterior/posterior relationships.",
        "- Do not invent vessels, ducts, nerves, tissue planes, or operative steps.",
        "- If a structure is uncertain, simplify or omit it rather than labeling it incorrectly.",
        "- Keep surgical instruments simplified unless instrument position is the teaching point.",
    ]
    rules = _entry_rules(entry)
    if rules:
        lines.extend(["", f"## TEMPLATE: {entry.get('id')}"])
        lines.extend(f"- {rule}" for rule in rules)
    if labels:
        lines.extend(["", "## LABEL TERMINOLOGY"])
        lines.extend(f"- {label}" for label in labels)
    if panel_plan:
        lines.extend(["", "## PROCEDURE PANEL PLAN"])
        lines.append(f"- Required panel count: {len(panel_plan)}")
        lines.append("- Use all listed panels unless the user explicitly requests a shorter figure.")
        lines.append("- Do not replace this plan with a generic four-panel storyboard.")
        lines.extend(f"- {item}" for item in panel_plan)
    elif composition == "sequence":
        lines.extend(
            [
                "",
                "## STORYBOARD STRUCTURE",
                "- Panel A: orientation and gross anatomy.",
                "- Panel B: key exposure or dissection plane.",
                "- Panel C: safety-critical verification view.",
                "- Panel D: final state or outcome, only if useful.",
            ]
        )
    if extra:
        lines.extend(["", "## USER CONSTRAINTS", extra])
    return "\n".join(lines)


def _review_checklist(entry: dict[str, Any] | None) -> list[str]:
    checklist = [
        "Verify anatomy positions, proportions, orientation, and layer relationships.",
        "Confirm no invented ducts, arteries, veins, nerves, or operative steps are shown.",
        "Check labels and leader lines do not obscure critical anatomy.",
    ]
    if entry:
        for item in reversed([str(v).strip() for v in (entry.get("verify") or []) if str(v).strip()]):
            checklist.insert(1, item)
    if not any("non-gory" in item.lower() for item in checklist):
        checklist.append("Confirm the figure is non-gory and suitable for academic publication or teaching.")
    return checklist


def _scientific_review(entry: dict[str, Any] | None) -> dict[str, Any]:
    if not entry:
        return {
            "status": "source_required",
            "scope": "No bundled knowledge entry matched. Generate a model_generated constraint set on demand, or use a source-constrained review before image generation.",
            "checks": [
                {
                    "category": "source",
                    "items": [
                        "Confirm operative note, technique description, guideline, atlas chapter, or paper methods section is available.",
                        "Separate source-confirmed steps from assumptions before drawing.",
                    ],
                }
            ],
        }

    checks: list[dict[str, Any]] = []
    if entry.get("must_have"):
        checks.append({"category": "required_anatomy", "items": list(entry["must_have"])})
    if entry.get("spatial_rules"):
        checks.append({"category": "spatial_relationships", "items": list(entry["spatial_rules"])})
    forbidden = [line.split(": ", 1)[-1] for line in _forbidden_lines(entry)]
    if forbidden:
        checks.append({"category": "forbidden_errors", "items": forbidden})
    if entry.get("phases"):
        checks.append({"category": "step_completeness", "items": list(entry["phases"])})
    if entry.get("verify"):
        checks.append({"category": "post_generation_review", "items": list(entry["verify"])})

    return {
        "status": "requires_visual_review_after_generation",
        "scope": "Use this structured checklist to judge whether the generated scientific illustration is anatomically and surgically correct.",
        "tier": entry.get("tier"),
        "confidence": entry.get("confidence"),
        "review_note": entry.get("review_note", ""),
        "checks": checks,
    }


def _build_copy_prompt(job: dict[str, Any], target: str) -> str:
    return (
        f"{_prompt_adapter(target)}\n\n"
        "MAIN PROMPT:\n"
        f"{job['prompt']}\n\n"
        "NEGATIVE PROMPT:\n"
        f"{job['negative_prompt']}\n\n"
        "POST-GENERATION CHECK:\n"
        + "\n".join(f"- {item}" for item in job["review_checklist"])
    )


def build_task_job(task: dict[str, Any]) -> dict[str, Any]:
    topic = str(task.get("topic") or "").strip()
    if not topic:
        raise ValueError("Missing required field: topic")

    output = task.get("output") if isinstance(task.get("output"), dict) else {}
    prompt_target = str(output.get("prompt_target") or task.get("prompt_target") or "universal").lower()
    platform = str(output.get("platform") or task.get("platform") or "auto").lower()
    generate_image = bool(output.get("generate_image", task.get("generate_image", False)))
    entry = _resolve_entry(task)
    labels = _labels_for(task, entry)
    assumptions = _assumptions(entry)
    size = str(task.get("size") or "1024x1024")
    width, height = _parse_size(size)

    prompt = _build_prompt(task, entry, labels)
    negative = (
        "low quality, bad anatomy, mirrored anatomy, invented anatomy, blurry labels, "
        "text artifacts, messy handwriting, overlapping lines, garish colors, cartoon gore, "
        "blood splatter, watermark"
    )

    if entry:
        knowledge_block = {
            "matched": True,
            "id": entry.get("id"),
            "name": entry.get("name"),
            "kind": entry.get("kind"),
            "tier": entry.get("tier"),
            "confidence": entry.get("confidence"),
            "sources": entry.get("sources", []),
            "review_note": entry.get("review_note", ""),
        }
    else:
        knowledge_block = {
            "matched": False,
            "id": None,
            "tier": "no_match",
            "confidence": None,
            "review_note": "No structured knowledge entry matched. Generate constraints on demand (model_generated) and verify against an authoritative source.",
        }

    job: dict[str, Any] = {
        "topic": topic,
        "prompt": prompt,
        "negative_prompt": negative,
        "review_checklist": _review_checklist(entry),
        "scientific_review": _scientific_review(entry),
        "knowledge": knowledge_block,
        "assumptions": assumptions,
        "params": {
            "size": size,
            "width": width,
            "height": height,
            "steps": int(task.get("steps") or 30),
            "cfg": float(task.get("cfg") or 7.0),
            "style": str(task.get("style") or "nejm"),
            "composition": str(task.get("composition") or "plate"),
        },
        "watermark": False,
        "tier": "skill",
        "skill": {
            "name": "surgical-anatomy-illustration",
            "platform": platform,
            "prompt_target": prompt_target,
            "generate_image": generate_image,
            "surgical_template": entry.get("id") if entry else "",
        },
    }
    notes = [
        "Standalone skill job; no legacy web-agent dependency.",
        "This skill does not generate images. Take copy_prompt to your own image tool, then bring the image back for the scientific review.",
    ]
    tier = knowledge_block.get("tier")
    if tier != "verified":
        note = f"Knowledge tier: {tier}"
        if knowledge_block.get("confidence"):
            note += f" (confidence {knowledge_block['confidence']})"
        note += ". Constraints are not clinician-verified; review against an authoritative source."
        notes.append(note)
        if knowledge_block.get("review_note"):
            notes.append(f"Review focus: {knowledge_block['review_note']}")

    if assumptions:
        notes.append(
            "ASSUMPTIONS — these decisions drive the figure; medical-standard defaults were used unless you said otherwise. Tell me to change any:"
        )
        for item in assumptions:
            alt = f"; alternatives: {', '.join(item['alternatives'])}" if item["alternatives"] else ""
            notes.append(f"- {item['decision']} = {item['assumed_default']}{alt}")

    job["platform_result"] = {
        "type": "image_requested" if generate_image else "prompt_only",
        "image_path": None,
        "copy_prompt": _build_copy_prompt(job, prompt_target),
        "notes": notes,
    }
    return job


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a surgical anatomy illustration prompt job.")
    parser.add_argument("topic", nargs="?", help="Illustration topic when --input is not provided.")
    parser.add_argument("--input", help="Path to task JSON.")
    parser.add_argument("--output", help="Write job JSON to this path.")
    parser.add_argument("--mode", default="surgical", choices=["surgical", "anatomy", "edit"])
    parser.add_argument("--style", default="nejm", choices=["nejm", "netter", "vector"])
    parser.add_argument("--composition", default="plate", choices=["plate", "hero", "sequence"])
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--prompt-target", default="universal")
    parser.add_argument("--platform", default="auto")
    parser.add_argument("--extra", default="")
    parser.add_argument("--surgical-template", default="", help="Force a knowledge entry by id or alias.")
    parser.add_argument("--generate-image", action="store_true", help="Mark the job for direct image rendering.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.input:
        task = _read_json(args.input)
    else:
        if not args.topic:
            raise SystemExit("Provide a topic or --input task JSON.")
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
                "generate_image": args.generate_image,
            },
        }

    job = build_task_job(task)
    text = json.dumps(job, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
