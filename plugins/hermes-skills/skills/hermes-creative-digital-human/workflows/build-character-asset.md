# Build Character Asset Workflow

## Purpose

Convert an approved FACE MASTER into a reusable character asset while preserving asset lineage.

## Preconditions

Required:
- L0 SOURCE
- approved L1 FACE MASTER
- face QC = PASS

Do not use lifestyle, wardrobe, scene-composite, or unapproved derivative images as identity anchors.

## Body Build

Create BODY MASTER candidates from:
- SOURCE
- approved FACE MASTER
- factual height / weight / body data when available

Recommended neutral outputs:
- full-body front
- side
- back when needed

If body regions were not visible in SOURCE, label them **synthetic completion**.

## Body QC Gate

Check:
- height impression
- weight / body mass
- shoulder width
- torso and waist proportion
- leg proportion
- posture
- age/body compatibility
- face identity consistency

FAIL means regenerate from SOURCE + approved FACE MASTER. Do not chain from the failed body output.

## Three-View Rule

Three-view sheets are L2 DERIVATIVE assets unless explicitly approved as BODY MASTER.

Each important view must remain anchored to SOURCE / approved MASTER. Do not create a new identity by repeatedly regenerating from the previous view.

## Style / Wardrobe

Only after body QC passes, define:
- clothing direction
- accessory direction
- photography direction

Style may change presentation, never identity.

## Output

A traceable character package containing:
- SOURCE inventory
- FACE MASTER
- BODY MASTER
- approved three-view derivatives when needed
- wardrobe direction
- uncertainty / synthetic-completion notes

Goal: a stable reusable asset, not a chain of increasingly synthetic generations.
