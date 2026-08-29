---
name: hermes-digital-human-character-card
description: Use when establishing or rebuilding a reusable digital-human character from real-person full-body photos, face close-ups, and factual profile data, especially for 人物卡、数字人建模、人物三视图、面部三视图、锁定人物 or reusable master-asset requests.
version: 1.0.0
triggers:
  - 人物卡
  - 数字人人物卡
  - 数字人建模
  - 建立人物
  - 锁定人物
  - 人物三视图
  - 面部三视图
  - character card
---

# Hermes Digital Human Character Card V1

## Purpose
Turn real-person source evidence into a small, reusable upstream character package before wardrobe, environment, action, or content production.

**Core rule: establish who the person is first, then generate six separate standard assets. Identity accuracy is more important than beautification.**

## Scope
This skill starts from original person evidence and ends at `CHARACTER_CARD_READY`.

It does not perform:
- wardrobe production
- scene compositing
- action production
- batch content production

After the card is ready, hand off to `hermes-creative-digital-human` and resume production there.

## Required Inputs
Register inputs by role. Do not let a visually similar generated image silently become source evidence.

### SOURCE FULL-BODY
Original full-body or near-full-body photos used for height impression, body proportions, silhouette, posture, and visible physical geometry.

Prefer front and side evidence when available. A genuine back view is useful but not mandatory; unseen back details must be treated as inferred rather than factual.

### SOURCE FACE CLOSE-UP
Original high-quality face photos used for identity. Prefer:
- front
- left 30–45°
- right 30–45°
- optional genuine profile views

Use minimally stylized images with visible eyes, nose, mouth, jaw, hairline, and age impression.

### FACTUAL PROFILE
User-provided facts and character settings. Record facts separately from visual observations.

Minimum useful fields when known:
- `age`
- `height`
- `weight`
- sex/gender presentation when explicitly provided and relevant to the requested asset
- hairstyle or other continuity-critical settings explicitly provided by the user

Do not invent missing facts. Do not infer ethnicity, health status, personality, or other sensitive traits from appearance.

## Output Contract
Produce:

1. one `QUANTITATIVE PROFILE CARD`
2. exactly six standard image assets

The six images are separate outputs, not one combined sheet:

### Face Standard Set
- `DH001_FACE_FRONT`
- `DH001_FACE_LEFT45`
- `DH001_FACE_RIGHT45`

Do not substitute a face-back view for an identity-useful angle. A back-of-head image may be created later when a project specifically needs hairstyle continuity, but it is not part of this six-image V1 card.

### Body Standard Set
- `DH001_BODY_FRONT`
- `DH001_BODY_SIDE`
- `DH001_BODY_BACK`

Replace `DH001` with the active `character_id`.

## QUANTITATIVE PROFILE CARD
Create a concise character description that can be checked against the images. Prefer reproducible observations over decorative prose.

Suggested fields:

```yaml
character_id: DH001
facts:
  age: user-provided or unknown
  height: user-provided or unknown
  weight: user-provided or unknown
body:
  build:
  shoulder_to_hip_relation:
  torso_leg_relation:
  visible_posture:
face:
  face_shape:
  eye_shape_spacing:
  brow_shape:
  nose_structure:
  mouth_lip_structure:
  jaw_chin:
  hairline:
  hairstyle:
  skin_tone_visible:
identity_marks:
  - only visible or user-provided continuity features
uncertainty:
  - anything not supported by SOURCE
```

Do not invent fake millimeter precision or numeric face weights. If a measurement is not known, describe the visible proportion or mark it unknown.

## Workflow

### Step 1 — SOURCE INTAKE
1. Assign or confirm `character_id`.
2. Classify every original input as `SOURCE FULL-BODY`, `SOURCE FACE CLOSE-UP`, or `FACTUAL PROFILE`.
3. Identify the strongest source face views and strongest body evidence.
4. If the supplied evidence is too weak to recognize the person reliably, stop and ask for better source photos instead of guessing.

### Step 2 — PROFILE EXTRACTION
Build the `QUANTITATIVE PROFILE CARD` from user facts plus visible morphology.

Separate:
- confirmed facts
- visual observations
- uncertain/inferred details

The profile card guides consistency but never overrides actual SOURCE images.

### Step 3 — IDENTITY LOCK
Create an identity evidence set from the strongest original `SOURCE FACE CLOSE-UP` images. This is a source-selection step, not a generated new face.

Ask the user to confirm that the selected evidence represents the intended person. Record:

`Identity Lock = APPROVED`

or

`Identity Lock = REJECTED`

**Do not generate the six standard assets before Identity Lock is approved.**

If rejected, return to SOURCE selection or request better source images.

### Step 4 — FACE STANDARD SET
Generate each face view independently from approved SOURCE identity evidence:

1. `FACE_FRONT`
2. `FACE_LEFT45`
3. `FACE_RIGHT45`

Standardization target:
- same person and age impression
- neutral or very mild expression
- plain neutral background
- simple even lighting
- minimal beautification or stylization
- consistent crop and camera feel
- hairline and facial structure clearly visible

Review each view against SOURCE. If the user says “不像”“不是这个人”“脸跑了”, mark that candidate `REJECTED` and regenerate from the approved SOURCE evidence, not from the failed generated view.

After all three face views receive explicit human approval, the approved set may be recorded as `IDENTITY_MASTER V1`.

There is **no automatic promotion** from generated face candidate to identity master.

### Step 5 — BODY STANDARD SET
After `IDENTITY_MASTER V1` is approved, generate each body view independently using:
- original `SOURCE FULL-BODY` evidence for body geometry
- approved identity evidence / `IDENTITY_MASTER V1` for identity continuity
- the quantitative profile only as supporting description

Generate:
1. `BODY_FRONT`
2. `BODY_SIDE`
3. `BODY_BACK`

Standardization target:
- full body visible head-to-toe
- same height/build impression across all views
- neutral standing pose
- simple fitted neutral clothing that does not redefine body shape
- consistent camera height, focal-length feel, scale, background, and lighting
- side view close to true 90°; back view close to true 180°

After all three body views receive explicit human approval, record the set as `BODY_MASTER V1`.

There is **no automatic promotion** from generated body candidate to body master.

### Step 6 — CHARACTER CARD APPROVAL
Set `CHARACTER_CARD_READY` only when all are true:
- Identity Lock = APPROVED
- Quantitative Profile Card reviewed
- FACE_FRONT = APPROVED
- FACE_LEFT45 = APPROVED
- FACE_RIGHT45 = APPROVED
- BODY_FRONT = APPROVED
- BODY_SIDE = APPROVED
- BODY_BACK = APPROVED
- `IDENTITY_MASTER V1` resolved
- `BODY_MASTER V1` resolved

Then hand off to `hermes-creative-digital-human` and resume production for wardrobe, environment, action, or batch content.

## STAR TOPOLOGY
Every standard image is generated from approved upstream evidence, never from another generated standard view.

Required pattern:

```text
SOURCE + approved identity evidence → FACE_FRONT
SOURCE + approved identity evidence → FACE_LEFT45
SOURCE + approved identity evidence → FACE_RIGHT45

SOURCE + IDENTITY_MASTER V1 → BODY_FRONT
SOURCE + IDENTITY_MASTER V1 → BODY_SIDE
SOURCE + IDENTITY_MASTER V1 → BODY_BACK
```

Never use `BODY_FRONT` to generate `BODY_SIDE`.
Never use `FACE_FRONT` to generate `FACE_LEFT45`.

A generated candidate cannot become SOURCE. Failed or rejected candidates must not be reused as identity evidence.

## Approval Rules
- SOURCE is ground-truth evidence.
- A generated image begins as `CANDIDATE`.
- User rejection means `REJECTED`; do not reuse it as a reference.
- `IDENTITY_MASTER V1` requires explicit human approval of the face standard set.
- `BODY_MASTER V1` requires explicit human approval of the body standard set.
- No generated output gains upstream authority through visual similarity alone.
- A contact sheet may be used for review, but it does not replace the six separate approved assets.

## Completion Record
Use a compact handoff card:

```yaml
character_id: DH001
status: CHARACTER_CARD_READY
quantitative_profile: APPROVED
identity_master: V1
body_master: V1
face_assets:
  - DH001_FACE_FRONT
  - DH001_FACE_LEFT45
  - DH001_FACE_RIGHT45
body_assets:
  - DH001_BODY_FRONT
  - DH001_BODY_SIDE
  - DH001_BODY_BACK
next_skill: hermes-creative-digital-human
```
