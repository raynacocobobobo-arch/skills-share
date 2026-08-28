# Create Character Workflow

## Goal

Create a reusable digital-human identity without allowing generated derivatives to become accidental identity anchors.

## Input

Collect the strongest available SOURCE evidence first:
- original user photos
- age / visual age
- height / weight when known
- occupation or persona
- content direction
- style preference

Do not start with wardrobe or scene generation when identity is not locked.

## Process

### 1. Register SOURCE

Treat user-provided original photos and factual body data as L0 SOURCE.

Record what is visible and what is unknown. Do not infer unseen geometry as fact.

### 2. Define Identity Spec

Describe only stable identity traits supported by SOURCE:
- face shape
- eyes and eye spacing
- nose
- mouth
- jawline
- hair / hairline
- skin and age cues
- visible body build
- temperament / occupational vibe

### 3. Build FACE MASTER Candidates

Generate independently from SOURCE:
- front
- left 15–20°
- right 15–20°

Do not generate one angle from another generated angle.

If only one frontal SOURCE photo exists, wider side/profile geometry remains synthetic completion.

### 4. Face QC Gate

Check:
- face shape
- eye spacing and shape
- nose structure
- mouth shape
- jawline
- hairline
- age impression
- overall recognizability

FAIL means regenerate from SOURCE. Never use the failed result as the next identity reference.

### 5. Human Approval

Only approved face candidates become L1 FACE MASTER assets.

Do not proceed to body, three-view, wardrobe, or scene work until FACE MASTER is approved.

## Required Output

- SOURCE inventory
- written identity spec
- FACE MASTER candidates
- face QC result
- explicit note of any synthetic completion / uncertainty

Goal: lock the person first; build the rest only after approval.
