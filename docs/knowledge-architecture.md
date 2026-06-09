# Knowledge Architecture And Design Notes (v0.1)

This document records the core design for `surgical-anatomy-illustration`. The skill is not meant to be a static encyclopedia. Its value is a repeatable medical illustration workflow: structured intake, explicit anatomical constraints, trust status, and post-generation scientific review.

## Core Position

The image model already knows a large amount of surgical and anatomical content. The skill should not try to retrain that knowledge. It should make the model behave like a careful biomedical illustrator:

1. Ask only the few questions that change anatomical correctness.
2. Fill safe defaults when the user does not specify details.
3. Inject required structures, spatial rules, forbidden errors, and safety concepts.
4. Return a checklist for scientific review after the image is generated.

In short:

```text
skill = workflow + structured surgical knowledge + model generation
```

## Target User

The primary user is a biomedical or medical illustrator. They understand visual communication and common anatomical terms, but may not know every surgical safety landmark or step order. The skill therefore supplies operative constraints and verification logic, not general drawing advice.

Clinicians are also supported because the workflow exposes assumptions and review points clearly. Pure non-medical users remain a later mode.

## Four-Step Workflow

1. **Intake**: present the correctness-changing questions (figure type, side/laterality, approach, teaching focus, clinical context) as choices and let the user pick — do not self-answer and barrel ahead. Reconcile anatomically inconsistent answers (e.g. posterior retroperitoneal approach with spleen/pancreas reflection) before building.
2. **Defaults**: only if the user explicitly defers, use medically standard defaults and state them.
3. **Constrain**: build the image prompt from must-have anatomy, spatial rules, forbidden mistakes, safety concept, phases, and clean label terminology.
4. **Verify**: produce a structured checklist so the final image can be reviewed for anatomical and surgical accuracy.

## Trust Status

There is one knowledge schema and one generation path. `tier` describes the source and confidence status of each entry:

| tier | Meaning | Use |
| --- | --- | --- |
| `model_generated` | Structured from model/textbook-level knowledge, not yet clinician verified | usable, but review required |
| `verified` | Clinician-reviewed and source-backed | preferred for direct production |
| `source_constrained` | Built from user-provided sources for uncommon or novel procedures | depends on source quality |

When no bundled entry matches, the job must mark `knowledge.matched=false` and `scientific_review.status=source_required`.

## Knowledge Schema

Each procedure or anatomy topic lives in one JSON file under `surgical-anatomy-illustration/knowledge/`.

Required conceptual fields:

- `id`, `name`, `aliases`, `region`, `kind`
- `tier`, `confidence`, `sources`, `last_verified_by`, `review_note`
- `labels`
- `intake`
- `figure_scopes`
- `laterality`
- `must_have`
- `spatial_rules`
- `forbidden_errors`
- `safety_concept`
- `phases`
- `verify`

Production details such as image provider, output size, style, and file paths stay outside this schema.

## Current State

- 12 entries in `knowledge/*.json` (incl. `adrenalectomy`, side/approach-aware, built on demand via the intake loop and reviewed by the user).
- `scripts/knowledge.py` loads and matches entries by id, name, and aliases.
- `scripts/med_illustration_job.py` builds prompts and scientific review from the knowledge loader, not hardcoded dictionaries.
- Jobs include `knowledge` and `scientific_review` blocks.
- `scripts/workflow.py` provides one command path for the brief (job + prompt + review) and optional scored review. The skill does not generate images.
- The interactive intake loop is enforced: for an un-built procedure, **no skeleton, no image** — generate the constraint set first, run the intake → constrain → verify loop, then save it as `knowledge/<id>.json`.

## Next Work

1. Promote `lap_chole` (and now `adrenalectomy`) to `verified` after clinician/source review.
2. Regenerate bundled examples so they reflect the new `knowledge` and `scientific_review` blocks.
3. Add an explicit error fixability tag (text-correctable vs geometry-hard) so the correction step does not loop blindly on geometry errors.
