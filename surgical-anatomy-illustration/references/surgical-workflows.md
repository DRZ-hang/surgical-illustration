# Surgical Workflows

Use this reference before generating surgical sequence figures. The goal is not
to teach operative performance, but to create medically coherent academic
illustrations with correct phase order and safety-critical anatomy.

## General Surgical Storyboard Method

1. Identify the procedure and indication context if provided.
2. List the canonical phases at a high level.
3. Mark safety-critical anatomy and "do-not-confuse" structures.
4. Choose panel count:
   - 1 panel: anatomy overview or single safety concept.
   - 3 panels: setup -> key dissection/safety view -> final step/outcome.
   - 4-6 panels: procedural sequence, suitable for teaching or review figures.
5. Avoid graphic blood, gore, realistic trauma, and entertainment-style drama.
6. Keep instruments simplified unless instrument position is the teaching point.
7. Add a review checklist after generation.

## Common Template Coverage

Use built-in templates first for these common surgical/anatomical illustration
requests:

- `lap_chole`: laparoscopic cholecystectomy and Critical View of Safety.
- `lap_appendectomy`: laparoscopic appendectomy anatomy and appendiceal base control.
- `inguinal_hernia`: inguinal hernia anatomy, direct/indirect comparison, and repair-plane figures.
- `thyroidectomy`: thyroidectomy anatomy with recurrent laryngeal nerve and parathyroid preservation.
- `colectomy_vascular`: right/left/sigmoid colectomy vascular anatomy and mesocolic planes.
- `breast_axilla`: breast/axillary surgery anatomy, nodal levels, sentinel pathway, and nerve-sparing views.
- `carotid_endarterectomy`: carotid bifurcation, plaque, ICA/ECA identity, and endarterectomy concepts.
- `hepatectomy_anatomy`: liver resection anatomy, inflow/outflow landmarks, and transection planes.

Each template should drive:

- must-have anatomy
- spatial rules
- forbidden mistakes
- panel plan
- review checklist

## Uncommon Or Innovative Procedures

Do not invent uncommon, new, modified, or institution-specific operative steps.
When no bundled template fits, first ask for or extract one of these source
materials:

- operative note or technique description
- user-provided step list
- paper methods section
- society guideline or consensus statement
- surgical atlas chapter or peer-reviewed technique review
- device IFU or manufacturer surgical technique guide when device-specific

Build a source-constrained illustration plan:

1. Extract only stated steps, anatomy, instruments, and safety landmarks.
2. Separate confirmed details from assumptions.
3. Ask for clarification when a missing detail could create an unsafe or wrong
   figure.
4. Use generic anatomy only for background context, not for invented operative
   maneuvers.
5. Include a review checklist that cites source gaps and uncertainty.

For innovative procedures, the output should say "source-constrained draft" if
the figure depends on user-provided or early-stage material.

## Laparoscopic Cholecystectomy

Authoritative basis to check when needed:

- SAGES guidelines for laparoscopic biliary tract surgery.
- SAGES Safe Cholecystectomy Multi-Society Practice Guideline.
- Tokyo Guidelines 2018 for acute cholecystitis safe surgical steps.

### Core Safety Concept

Use the Critical View of Safety (CVS) as the central safety frame:

- expose and clear the hepatocystic triangle
- identify only two structures entering the gallbladder: cystic duct and cystic artery
- separate the lower gallbladder from the liver bed before division
- if CVS cannot be achieved in severe inflammation/fibrosis, indicate a bail-out
  concept rather than forcing unsafe duct/artery division

### Suggested 4-Panel Storyboard

Panel A: Port/instrument context and gross anatomy

- inferior liver edge
- gallbladder fundus/body/neck
- hepatocystic triangle region
- atraumatic retraction direction

Panel B: Calot/hepatocystic triangle exposure

- cystic duct
- common hepatic duct
- common bile duct
- cystic artery
- right hepatic artery if relevant
- dashed safe-dissection zone

Panel C: Critical View of Safety

- only cystic duct and cystic artery entering gallbladder
- lower third of gallbladder dissected off liver bed
- no extra duct entering the gallbladder
- clear "do not divide before CVS" visual logic

Panel D: Clip/divide and gallbladder separation

- clips on cystic duct and cystic artery
- gallbladder separated from liver bed
- optional extraction bag, low detail

### Single-Plate Anatomy Version

For a single anatomy plate, show:

- main gallbladder/biliary anatomy
- inset zoom of Calot/hepatocystic triangle
- cystic duct joining common hepatic duct to form common bile duct
- cystic artery within the triangle
- no confusing extra ducts or mirrored orientation

### Forbidden Mistakes

- cystic duct confused with common bile duct
- cystic artery placed outside the hepatocystic triangle without explanation
- right hepatic artery mislabeled as cystic artery
- common bile duct clipped or divided
- hepatocystic triangle shown as a vague decorative triangle with no anatomic boundaries
- gore, blood splatter, dramatic operative-field realism

### Label Set

- Gallbladder
- Cystic duct
- Common hepatic duct
- Common bile duct
- Cystic artery
- Right hepatic artery
- Hepatocystic triangle / Calot triangle
- Liver edge
- Critical View of Safety
- Lower gallbladder dissected from liver bed
