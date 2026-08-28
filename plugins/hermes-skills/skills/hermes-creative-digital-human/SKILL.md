---
name: hermes-creative-digital-human
description: Use when creating or maintaining a realistic digital human, virtual creator, AI blogger, outfit variant, or real-scene composite where identity consistency across generations matters.
version: 1.1.0
triggers:
  - 数字人
  - 虚拟博主
  - AI博主
  - 真人数字人
  - 小红书数字人
  - 实景融合
---

# Hermes Creative Digital Human

## Purpose

Create a reusable, realistic digital-human asset while preventing identity drift across face angles, body completion, outfits, poses, and real-scene composites.

**Core principle: identity evidence flows downward only. Never let downstream generations redefine the person.**

## Identity Source Hierarchy

| Level | Asset | Identity use |
|---|---|---|
| L0 SOURCE | User-provided original photos and factual body data | Primary anchor |
| L1 MASTER | Human-approved face/body identity assets derived directly from SOURCE | Primary anchor |
| L2 DERIVATIVE | Three-view, expression, pose, wardrobe, angle variants | Auxiliary only |
| L3 CONTENT | Lifestyle, scene composite, social/promo output | Never an upstream identity anchor |

A DERIVATIVE becomes MASTER only after explicit human approval.

## Non-Negotiable Rules

### Identity First

Identity stability is more important than beauty score, styling, or scene richness.

### No Identity Backflow

Never use lifestyle images, wardrobe outputs, scene composites, promotional images, or unapproved derivatives as upstream identity evidence.

### No Generation Chaining

Forbidden:
`SOURCE → generated A → generated B → generated C`

Required star topology:
`SOURCE / approved MASTER → output A`
`SOURCE / approved MASTER → output B`
`SOURCE / approved MASTER → output C`

Every major output must trace back to SOURCE or an approved MASTER.

### Face Lock Before Body Lock

Do not create three-view sheets, wardrobe systems, or scene composites before face identity passes QC.

Recommended sequence:
1. SOURCE intake
2. FACE MASTER: front, left 15–20°, right 15–20°
3. face QC
4. BODY MASTER
5. body QC
6. wardrobe
7. scene integration
8. batch production

### Single-Photo Safety Rule

If only one frontal photo exists, treat unseen side profile, rear head shape, full-body proportions, leg length, waist/hip geometry, and natural stance as **synthetic completion**, not verified identity evidence.

Do not promote synthetic completion to MASTER without explicit human approval.

### Style Cannot Override Identity

Style references may affect clothing, location, pose, framing, lighting, mood, and expression range. They must not redefine face shape, eye spacing, eye shape, nose, mouth, jawline, hairline, age impression, or body identity.

## Workflow Routing

New character:
`workflows/create-character.md`

Build approved reusable asset:
`workflows/build-character-asset.md`

Existing character / real-scene content:
`workflows/generate-realistic-content.md`

Bad output or identity drift:
`workflows/improve-output.md`

## Quality Check Order

Check one failure layer at a time:
1. identity consistency
2. age consistency
3. body proportion
4. perspective and scale
5. lighting and color
6. depth of field / sharpness / noise
7. skin texture
8. social-media style

## Drift Recovery

If the person becomes progressively more generic, younger/older, or structurally different:
1. stop downstream generation
2. demote drifting assets to L2/L3
3. remove them from identity inputs
4. return to the latest approved SOURCE / MASTER
5. regenerate from that anchor
6. run QC again

Never repair drift by regenerating from an already-drifted image.

## Asset Naming

Use traceable names such as:
- `SOURCE_001`
- `FACE_MASTER_V1_FRONT`
- `FACE_MASTER_V1_LEFT15`
- `FACE_MASTER_V1_RIGHT15`
- `BODY_MASTER_V1_FULL`
- `WARDROBE_BUSINESS_01`
- `CONTENT_XHS_001`

Avoid ambiguous lineage names such as `final2.png` or `new-final.png`.
