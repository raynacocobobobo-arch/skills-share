---
name: hermes-creative-digital-human
description: Use when creating or maintaining a realistic digital human, virtual creator, AI blogger, outfit variant, pose variant, or real-scene composite where identity consistency across generations matters.
version: 2.2.0
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

# Hermes Creative Digital Human V2.2

## Purpose
Build a reusable digital-human production asset with explicit identity control. V2.2 separates WHO the person is from body/appearance, pose, props, and scene, makes identity binding session-safe for ChatGPT Web production, and adds a lightweight per-character Identity Anchor for deterministic asset addressing.

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

## Identity Anchor Card
Maintain one Identity Anchor Card, **one per character**. It is a lightweight address card for approved identity assets; it is not another global manifest, workflow engine, or face model. **Do not create a global digital-human registry.**

Minimum fields:

```yaml
character_id: DH001
active_identity:
  version: V1
  state: ACTIVE
references:
  - tag: "@DH001_ID_V1_FRONT"
    role: IDENTITY_ONLY
    view: front
    status: APPROVED
  - tag: "@DH001_ID_V1_L45"
    role: IDENTITY_ONLY
    view: left_45
    status: APPROVED
  - tag: "@DH001_ID_V1_R45"
    role: IDENTITY_ONLY
    view: right_45
    status: APPROVED
```

Tags are stable aliases, not image payloads. They make assets addressable and auditable, but a tag alone does not satisfy Explicit Master Re-attachment when the active tool requires the actual image input. The exact approved asset must still be selected/re-attached from the project, library, saved-reference system, or equivalent tool input.

### Identity Version Lifecycle
Approved identity masters are immutable. Never overwrite an approved master in place. If the authoritative face set changes, create a new version such as `V2`, set it `ACTIVE`, and mark the previous approved version `DEPRECATED`. Keep deprecated versions for traceability; never silently mutate their contents.

### Reference Priority
Use symbolic priority only: `CRITICAL / HIGH / NORMAL`.

- IDENTITY = normally `CRITICAL`
- BODY = normally `HIGH` when full-body geometry matters
- WARDROBE / POSE / SCENE = normally `NORMAL` unless the shot requires stronger attention

Do not invent numeric reference weights unless the active tool exposes a real documented weight control.

## ChatGPT Web Session Contract
For long-running production, use **one project + multiple short chats + permanent master assets**. Project/chat context can carry goals, naming, status, and production notes, but **conversation history is not an identity source**.

### Explicit Master Re-attachment
Every new production chat and every identity-critical generation must resolve the character's ACTIVE Identity Anchor and explicitly re-attach the exact approved `IDENTITY_MASTER` asset. Re-attach `BODY_MASTER` as well when full-body geometry matters. A phrase such as “use the same person as before” or “refer to the person above” is not a substitute for the master asset.

If the correct master is not actually present in the current task inputs, stop before generation and restore the approved master input rather than guessing from chat history or a tag alone.

### Reference Role Mapping
Every reference image must have one declared role. Identity authority must never be inferred from visual similarity alone.

| Role | May control |
|---|---|
| `IDENTITY ONLY` | Face identity and age impression |
| `BODY ONLY` | Body proportions and silhouette |
| `WARDROBE ONLY` | Clothing, PPE, accessories, footwear |
| `POSE ONLY` | Pose, hands, action, prop interaction |
| `SCENE ONLY` | Environment, camera geometry, lighting, perspective |

A non-identity reference cannot redefine the face.

### Reference Map
Before every identity-critical generation, number the active inputs so the model or operator does not have to infer which image controls which layer.

```text
REF01 = @DH001_ID_V1_FRONT | IDENTITY ONLY | CRITICAL
REF02 = @DH001_BODY_V1_FRONT | BODY ONLY | HIGH
REF03 = @DH001_WARDROBE_RIG_01 | WARDROBE ONLY | NORMAL
REF04 = @POSE_PHOTOGRAPHER_MONOPOD_03 | POSE ONLY | NORMAL
REF05 = @SCENE_RIG_RAIN_02 | SCENE ONLY | NORMAL
```

The tag is the stable address; the attached image is the actual visual evidence.

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

## Edit-first / Generate-second
When an approved identity-bearing image already exists and the active tool supports reference-preserving edits, prefer an edit/transform path that preserves the approved person while changing only the requested layer. Use a fresh generation path when edit constraints cannot solve the required composition, pose, geometry, or scene change.

Both paths still require Explicit Master Re-attachment. Edit-first is a production preference, not permission to chain from an unapproved or drifted image. Generate-second never weakens the Identity Gate.

## Candidate Hard Stop
If an identity-bearing candidate fails Identity Gate, that candidate **must not continue downstream** into wardrobe, scene polishing, action continuity, batch production, or future identity inputs. Mark it `REJECTED` and enter the Identity Recovery Loop from the latest approved upstream master.

Candidate Hard Stop blocks contamination; it does not terminate the whole production workflow.

## 8-Step Production Flow
Use this as the user-facing production sequence. Internal gates and prototypes may add checks inside a step, but must not change the order or identity authority.

1. SOURCE INTAKE — register original person references and factual data; assign stable `character_id`.
2. IDENTITY MASTER — build and human-approve the authoritative face identity set; create/update the per-character Identity Anchor Card.
3. STANDARD THREE-VIEW — build the standard front/side/back body/appearance asset from approved upstream identity and factual body evidence.
4. IDENTITY VALIDATION — verify the same person across the master set and three-view output; reject drift before downstream production.
5. WARDROBE — create approved clothing/PPE variants without redefining identity.
6. ENVIRONMENT — integrate the approved person into real or designed scenes with perspective/light matching.
7. ACTION — add pose, prop, camera, and interaction complexity while re-running Identity Gate when identity-bearing output changes.
8. BATCH CONTENT — produce multiple approved outputs from the same ACTIVE anchor and explicit masters; never promote batch content into identity authority.

## Detailed Production Pipeline
1. SOURCE INTAKE
2. IDENTITY MASTER Face ID Set
3. IDENTITY TEST GRID
4. IDENTITY GATE
5. IDENTITY ANCHOR CARD
6. BODY MASTER
7. BODY GATE
8. APPEARANCE / WARDROBE
9. SESSION BOOTSTRAP + REFERENCE MAP
10. SHOT DESIGN
11. POSE + PROP PROTOTYPE when complex
12. IDENTITY INTEGRATION
13. IDENTITY GATE again
14. SCENE INTEGRATION
15. REALISM QC
16. APPROVED CONTENT
17. optional image-to-video / reference-to-video continuity

## Identity Test Grid
Before production, prefer a simple neutral-background validation set: front, left 45°, right 45°, supported near-profiles, slight look down, slight look up, and medium shot. The purpose is to expose identity drift before scene complexity hides it.

## Identity Recovery Loop
Identity failure rejects the **candidate**, not the entire workflow.

1. Mark the failed candidate `REJECTED` and remove it from identity/reference inputs.
2. Resolve the ACTIVE Identity Anchor Card and return to its latest approved `IDENTITY_MASTER`.
3. Return to L0 SOURCE only if the approved master itself is missing, disputed, or invalid.
4. Diagnose whether drift came from identity conditioning, angle, pose/prop complexity, scene complexity, or conflicting references.
5. Change strategy: simplify the shot, isolate pose/prop, reduce conflicting references, or use a stronger identity-aware path.
6. Explicitly re-attach the approved master and generate a fresh candidate from that upstream anchor.
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
Examples: `SOURCE_001`, `@DH001_ID_V1_FRONT`, `@DH001_ID_V1_L45`, `@DH001_ID_V1_R45`, `@DH001_BODY_V1_FRONT`, `@DH001_WARDROBE_RIG_01`, `@POSE_CAMERA_MONOPOD_WALK_01`, `@SCENE_DRILLING_SITE_01`, `CONTENT_CANDIDATE_001`, `CONTENT_APPROVED_001`, `CONTENT_REJECTED_001`.
