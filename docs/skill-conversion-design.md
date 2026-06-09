# Surgical Anatomy Illustration Skill Design

## Product Decision

The first public-facing skill should focus on **surgical + anatomical
illustration** only.

This is a better first release than a broad "medical illustration" skill because
surgery, anatomy, research mechanisms, and abstract-to-graphical-abstract work
require different expert logic. A narrower first skill can be more professional,
easier to validate, and easier to explain on GitHub.

## First Skill Scope

Name:

- `surgical-anatomy-illustration`

Primary use cases:

- operative anatomy plates
- surgical step storyboards
- anatomy teaching figures
- safety-critical landmarks
- dissection planes and anatomical orientation
- structured scientific-accuracy review and correction prompts

Explicitly out of scope for v1:

- molecular pathway diagrams
- omics/research mechanism figures
- abstract-to-graphical-abstract automation
- broad scientific infographics

Those should become separate skills after this one is stable.

## Skill Family Roadmap

### Skill 1: Surgical Anatomy Illustration

Goal: high-accuracy surgical/anatomical images.

Core strengths:

- named surgery -> standard phase plan
- anatomy constraints and forbidden mistakes
- structured scientific-accuracy review and correction prompts
- a constrained, copy-ready prompt the user renders in their own image tool
- review of any returned image for anatomical errors

### Skill 2: Research Mechanism Illustration

Goal: molecular, cellular, pathway, and disease mechanism figures.

Core strengths:

- trigger -> cascade -> outcome logic
- cell/tissue compartment mapping
- journal graphical abstract styles
- structured pathway labels
- mechanism error checks

### Skill 3: Abstract-To-Figure

Goal: convert paper abstract, methods, or manuscript text into a figure concept.

Core strengths:

- extract study design, cohort, intervention, outcomes
- suggest graphical abstract or Figure 1 structure
- prevent fabricated claims
- map evidence to panels
- produce prompt package or figure draft

## Current Repository Structure

This is a **standalone skill project**. It was inspired by an earlier broad
medical-illustration *agent* (a separate project), but shares no code with it;
only skill-relevant content is kept here.

```text
medical-illustration-agent/
|- surgical-anatomy-illustration/   # the installable skill
|  |- SKILL.md
|  |- agents/openai.yaml
|  |- scripts/
|  |- references/
|  |- knowledge/                    # per-procedure knowledge entries (*.json)
|  |- assets/examples/
|- docs/
|- README.md
|- .gitignore
```

The installable folder is named `surgical-anatomy-illustration/`, matching the
frontmatter skill name.

## Interaction Design

The skill does not generate images. For a Create request it runs a short intake
(figure type, side, approach, focus) and returns a three-part brief: a short
overview, a constrained copy-ready prompt, and a bilingual QC checklist. The user
renders the prompt in their own image tool and can bring any image back for the
four-category review.

## Surgical Quality Strategy

For common surgeries, use bundled templates first. For uncommon or high-risk
procedures, look up authoritative sources before generating:

- society guidelines
- surgical textbooks or atlases
- peer-reviewed reviews or guidelines
- user-provided operative notes or papers

Do not use random blogs or image-search results as source of truth for surgical
steps.

For laparoscopic cholecystectomy, the first template is based on the safe
cholecystectomy concept and Critical View of Safety:

- expose hepatocystic triangle
- identify only cystic duct and cystic artery entering gallbladder
- separate lower gallbladder from liver bed before dividing structures
- show bail-out concept if safe view cannot be achieved

## Implementation Status

Completed:

- standalone skill folder
- installable folder renamed to `surgical-anatomy-illustration/`
- clean `SKILL.md`
- `agents/openai.yaml`
- prompt/job wrapper script
- prompt-only script
- validation script
- structured scientific-accuracy review and correction-prompt scripts
- laparoscopic cholecystectomy workflow reference
- committed closed-loop review example for laparoscopic cholecystectomy
- reproducible commands for Couinaud liver segments and extrahepatic biliary tree
- common surgery template library for lap chole, lap appendectomy, inguinal
  hernia, thyroidectomy, colectomy vascular anatomy, breast/axilla, carotid
  endarterectomy, and hepatectomy anatomy
- uncommon/innovative procedure source-constrained workflow

Next suggested work:

- add README hero / before-after / error-review images before going public
- optionally add an `AGENTS.md` for first-class Codex support
