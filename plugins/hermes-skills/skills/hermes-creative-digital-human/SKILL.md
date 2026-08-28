---
name: hermes-creative-digital-human
description: Use when creating or maintaining a realistic digital human, virtual creator, AI blogger, outfit variant, pose variant, or real-scene composite where identity consistency across generations matters.
version: 2.0.0
triggers:
  - 数字人
  - 虚拟博主
  - AI博主
  - 真人数字人
  - 小红书数字人
  - 实景融合
  - 人物一致性
  - 锁脸
  - 人脸跑偏
---

# Hermes Creative Digital Human V2

## Purpose
Build a reusable digital-human production asset with explicit identity control. V2 separates WHO the person is from body/appearance, pose, props, and scene.

**Core principle: identity is an upstream asset, not a prompt adjective. A three-view sheet is not proof of facial identity.**

## V2 Asset Architecture
| Layer | Asset | Responsibility | May define identity? |
|---|---|---|---|
| L0 SOURCE | Original user photos + factual data | Ground truth evidence | Yes |
| L1 IDENTITY MASTER | Human-approved face identity set | WHO this person is | Yes |
| L1 BODY MASTER | Human-approved body/proportion set | Body geometry | Body only |
| L2 APPEARANCE | Clothing, hair styling, PPE, accessories | Presentation | No |
| L2 POSE / PROP | Pose, hands, equipment, camera, monopod, etc. | Action and prop geometry | No |
| L2 SCENE | Environment, camera position, perspective, lighting | Scene | No |
| L3 CONTENT | Final composites, lifestyle/social images | Publishable output | Never |

Only L0 SOURCE and explicitly approved L1 masters may be upstream identity anchors.

## Identity Master Requirements
Prefer original, high-quality, minimally stylized photos. Build a Face ID Set from the strongest available views: front, left 30–45°, right 30–45°, optional genuine profiles, neutral/mild expression, consistent age and recognizable facial structure.

A contact sheet or three-view character sheet may be useful for review, but must not automatically become the identity source. Crop/route individual face views when possible so identity evidence is not diluted by clothing, scene, labels, or unrelated tasks.

## Identity Gate
Before body variants, wardrobe, complex poses, props, or scene integration, identity must pass. Check face ratio, eye shape/spacing, brows, nose, mouth, jaw/chin, ears when visible, hairline, age impression, and overall recognizability.

If the user says the person does not look like the reference, treat that candidate as **Identity Gate = FAIL**. Shared clothing, glasses, helmet, age, or ethnicity are not proof of identity.

## Approved Reference Pool
Every generated asset is `CANDIDATE`, `APPROVED`, or `REJECTED`. Only `APPROVED` assets may enter the reusable reference pool. `REJECTED` assets must never be reused as identity references.

## No Generation Chaining
Forbidden: `SOURCE → generated A → generated B → generated C`

Required star topology:
`SOURCE / IDENTITY_MASTER → candidate A`
`SOURCE / IDENTITY_MASTER → candidate B`
`SOURCE / IDENTITY_MASTER → candidate C`

Downstream content must not redefine upstream identity.

## Separate Identity From Appearance
Three-view sheets primarily define height impression, body proportions, silhouette, clothing/PPE, and visible equipment. They are `APPEARANCE/BODY` references unless explicitly validated as identity masters. Do not claim a three-view sheet locks the face merely because it contains a face.

## Pose Prototype Rule
For complex actions or props, solve pose/prop geometry before final identity integration when practical.

Example: `stand-in → correct walking pose + shoulder load + monopod + camera geometry → identity integration → scene integration`

## Tool Capability Tiers
### Tier A — Identity-aware
Explicit identity conditioning such as face embedding, FaceID/InstantID/PuLID/PhotoMaker-class conditioning, or a platform feature documented to preserve character identity.

### Tier B — Multi-reference image generation
Accepts reference images but has no verified identity-specific conditioning. It may produce strong resemblance, but must not be described as guaranteed identity lock.

### Tier C — Prompt / ordinary generation
No reliable identity conditioning. Use for scene design, pose prototypes, wardrobe exploration, stand-ins, and composition.

Tier B/C drift should trigger the Identity Recovery Loop. Repeated failure should change strategy or escalate tool capability rather than repeat the same prompt indefinitely.

## Production Pipeline
1. SOURCE INTAKE
2. IDENTITY MASTER Face ID Set
3. IDENTITY TEST GRID
4. IDENTITY GATE
5. BODY MASTER
6. BODY GATE
7. APPEARANCE / WARDROBE
8. SHOT DESIGN
9. POSE + PROP PROTOTYPE when complex
10. IDENTITY INTEGRATION
11. IDENTITY GATE again
12. SCENE INTEGRATION
13. REALISM QC
14. APPROVED CONTENT
15. optional image-to-video / reference-to-video continuity

## Identity Test Grid
Before production, prefer a simple neutral-background validation set: front, left 45°, right 45°, supported near-profiles, slight look down, slight look up, and medium shot. The purpose is to expose identity drift before scene complexity hides it.

## Identity Recovery Loop
Identity failure rejects the **candidate**, not the entire workflow.

1. Mark the failed candidate `REJECTED` and remove it from identity/reference inputs.
2. Return first to the latest approved `IDENTITY MASTER`.
3. Return to L0 SOURCE only if the approved master itself is missing, disputed, or invalid.
4. Diagnose whether drift came from identity conditioning, angle, pose/prop complexity, scene complexity, or conflicting references.
5. Change strategy: simplify the shot, isolate pose/prop, reduce conflicting references, or use a stronger identity-aware path.
6. Generate a fresh candidate from the approved upstream anchor.
7. Re-run Identity Gate.
8. PASS → continue downstream. FAIL → remain in recovery mode within a bounded retry budget.
9. If the retry budget is exhausted without a meaningful strategy change available, escalate the tool/path limitation to the user.

Never repair drift by regenerating from an already-drifted image.

## Video Continuity
For multi-shot video, preserve the same approved identity asset across shots. Where supported, use reference-to-video or an approved continuity frame, but never promote a drifted video frame into the identity master pool.

## Workflow Routing
New character: `workflows/create-character.md`

Build reusable asset: `workflows/build-character-asset.md`

Existing character / real-scene content: `workflows/generate-realistic-content.md`

Bad output / identity drift: `workflows/improve-output.md`

## Asset Naming
Examples: `SOURCE_001`, `IDENTITY_MASTER_V1_FRONT`, `IDENTITY_MASTER_V1_LEFT45`, `IDENTITY_MASTER_V1_RIGHT45`, `BODY_MASTER_V1_FRONT`, `POSE_CAMERA_MONOPOD_WALK_01`, `SCENE_DRILLING_SITE_01`, `CONTENT_CANDIDATE_001`, `CONTENT_APPROVED_001`, `CONTENT_REJECTED_001`.
