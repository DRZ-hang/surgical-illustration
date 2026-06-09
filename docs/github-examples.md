# GitHub Example Set

These examples exercise the standalone `surgical-anatomy-illustration` skill.
Run all commands from the skill folder:

```bash
cd surgical-anatomy-illustration
```

## Example 1: Laparoscopic Cholecystectomy CVS Storyboard

Brief:

```text
laparoscopic cholecystectomy Critical View of Safety storyboard
```

Purpose:

- surgical sequence planning
- Critical View of Safety anatomy constraints

Reproduce (job + copy-ready prompt):

```bash
python scripts/med_illustration_job.py "laparoscopic cholecystectomy Critical View of Safety storyboard" --mode surgical --style nejm --composition sequence --output outputs/lap_chole_cvs_storyboard_job.json
python scripts/prompt_only.py --input outputs/lap_chole_cvs_storyboard_job.json --output outputs/lap_chole_cvs_storyboard_prompt.txt
```

## Example 2: Couinaud Liver Segment Plate

Brief:

```text
Couinaud liver segments I-VIII with hepatic veins
```

Purpose:

- anatomy plate generation
- liver segment orientation constraints

Reproduce:

```bash
python scripts/med_illustration_job.py "Couinaud liver segments I-VIII with hepatic veins" --mode anatomy --style netter --composition plate --output outputs/couinaud_liver_segments_job.json
python scripts/prompt_only.py --input outputs/couinaud_liver_segments_job.json --output outputs/couinaud_liver_segments_prompt.txt
```

## Example 3: Extrahepatic Biliary Tree Anatomy

Brief:

```text
extrahepatic biliary tree anatomy with gallbladder cystic duct common hepatic duct common bile duct and portal triad relationships
```

Purpose:

- pure anatomy plate workflow
- biliary tract label terminology
- portal triad relationship constraints

Reproduce:

```bash
python scripts/med_illustration_job.py "extrahepatic biliary tree anatomy with gallbladder cystic duct common hepatic duct common bile duct and portal triad relationships" --mode anatomy --style nejm --composition plate --output outputs/biliary_tree_anatomy_job.json
python scripts/prompt_only.py --input outputs/biliary_tree_anatomy_job.json --output outputs/biliary_tree_anatomy_prompt.txt
```

## Validation

```bash
python scripts/validate_job.py outputs/lap_chole_cvs_storyboard_job.json
python scripts/validate_job.py outputs/couinaud_liver_segments_job.json
python scripts/validate_job.py outputs/biliary_tree_anatomy_job.json
```

## Closed-Loop Scientific Review Example

This is the only example whose artifacts are committed under
`surgical-anatomy-illustration/assets/examples/`, because it demonstrates the
skill's main value beyond direct image generation.

Brief:

```text
laparoscopic cholecystectomy complete surgical process diagram
```

Purpose:

- plan a complete procedure-specific storyboard instead of a generic four-panel figure
- create a structured scientific review form
- generate a correction prompt from failed or uncertain review items

Artifacts:

- `assets/examples/lap_chole_complete_process_job.json`
- `assets/examples/lap_chole_complete_process_prompt.txt`
- `assets/examples/lap_chole_complete_process_review.json`
- `assets/examples/lap_chole_complete_process_review_example_failed.json`
- `assets/examples/lap_chole_complete_process_correction.json`
- `assets/examples/lap_chole_complete_process_correction_prompt.txt`

Reproduce:

```bash
python scripts/workflow.py "laparoscopic cholecystectomy complete surgical process diagram" --generate-image --output-dir assets/examples --prefix lap_chole_complete_process
python scripts/correction_prompt.py assets/examples/lap_chole_complete_process_review_example_failed.json --job assets/examples/lap_chole_complete_process_job.json --output assets/examples/lap_chole_complete_process_correction.json --text-output assets/examples/lap_chole_complete_process_correction_prompt.txt
```
