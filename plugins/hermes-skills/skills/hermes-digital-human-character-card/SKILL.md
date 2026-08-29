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
Create the smallest useful reusable character package from real-person source evidence before wardrobe, environment, action, or content production.

**Core rule: preserve identity first. The character card is a compact source-derived asset, not a beauty redesign.**

## Scope
This skill starts from original person evidence and produces exactly three deliverables:

1. `DH001_PROFILE_CARD`
2. `DH001_FACE_3VIEW_SHEET`
3. `DH001_BODY_3VIEW_SHEET`

It does not perform:
- wardrobe production
- scene compositing
- action production
- batch content production

After final approval, hand off to hermes-creative-digital-human and resume production there.

## Required Inputs
Classify original inputs by role.

### SOURCE FULL-BODY
Original full-body or near-full-body photos used for height impression, body proportions, silhouette, posture, and visible body geometry.

Prefer front and side evidence when available. A genuine back view is useful but not mandatory; unseen details must remain inferred rather than factual.

### SOURCE FACE CLOSE-UP
Original high-quality face photos used for identity. Prefer:
- front
- left 30–45°
- right 30–45°
- optional genuine profile views

Use minimally stylized images with visible eyes, nose, mouth, jaw, hairline, and age impression.

### FACTUAL PROFILE
User-provided facts and settings. Record facts separately from visual observations.

Minimum useful fields when known:
- `age`
- `height`
- `weight`
- explicitly provided hairstyle or other continuity-critical settings

Do not invent missing facts. Do not infer sensitive traits from appearance.

## Output Contract

### 1. DH001_PROFILE_CARD
Create a concise quantitative profile card from user facts plus visible morphology.

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
  visible_skin_tone:
identity_marks:
  - only visible or user-provided continuity features
uncertainty:
  - anything not supported by SOURCE
```

Do not invent fake millimeter precision, numeric face weights, or unsupported measurements.

### 2. DH001_FACE_3VIEW_SHEET
Generate one face three-view sheet containing exactly:
- `FACE_FRONT`
- `FACE_LEFT45`
- `FACE_RIGHT45`

Do not substitute a face-back view. A back-of-head reference is optional later, but is not part of this V1 character card.

Sheet target:
- same person across all three panels
- same age impression
- neutral or mild expression
- plain neutral background
- even soft lighting
- minimal beautification or stylization
- consistent crop, scale, and camera feel
- clearly visible hairline and facial structure
- no decorative layout that reduces useful face size

### 3. DH001_BODY_3VIEW_SHEET
Generate one full-body three-view sheet containing exactly:
- `BODY_FRONT`
- `BODY_SIDE`
- `BODY_BACK`

Sheet target:
- full body visible head-to-toe
- same height/build impression across all panels
- neutral standing pose
- simple fitted neutral clothing that does not redefine body shape
- consistent camera height, focal-length feel, scale, background, and lighting
- side view close to true 90°
- back view close to true 180°

Replace `DH001` with the active `character_id`.

## FULL AUTO MODE
A normal character-card request runs continuously after the user supplies sufficient SOURCE and factual profile information.

No intermediate user reply is required.

Default sequence:

```text
PROFILE_CARD → FACE_3VIEW_SHEET → BODY_3VIEW_SHEET
```

Do not ask the user to say next between these three deliverables.

The user may still interrupt, reject, or revise any result at any time.

## Workflow

### Step 1 — SOURCE INTAKE
1. Assign or confirm `character_id`.
2. Classify original images as `SOURCE FULL-BODY` or `SOURCE FACE CLOSE-UP`.
3. Record `FACTUAL PROFILE` separately.
4. Identify the strongest identity and body evidence.
5. If SOURCE is too weak to identify the person reliably, stop rather than guess.

### Step 2 — PROFILE CARD
Create `DH001_PROFILE_CARD`.

Separate:
- confirmed facts
- visible observations
- uncertainty

The profile card supports consistency but never overrides SOURCE images.

### Step 3 — FACE THREE-VIEW SHEET
Generate `DH001_FACE_3VIEW_SHEET` directly from original SOURCE FACE CLOSE-UP evidence.

Do not derive one panel from another generated panel. Treat the sheet as one controlled multi-view output whose identity authority still comes from SOURCE.

### Step 4 — INTERNAL IDENTITY QC
Compare the generated face sheet against SOURCE before continuing.

Check:
- overall recognizability
- face ratio
- eye shape and spacing
- brows
- nose
- mouth
- jaw/chin
- visible hairline
- age impression

If the face is visibly wrong, use a bounded automatic retry with a materially changed strategy. Do not ask the user to say next during an ordinary retry.

Default retry budget: up to 2 automatic strategy-changing retries for the face sheet.

If identity remains unreliable after the retry budget, stop only when SOURCE is insufficient or the active image tool cannot preserve identity reliably enough. State the limitation instead of silently producing a false master.

### Step 5 — BODY THREE-VIEW SHEET
Generate `DH001_BODY_3VIEW_SHEET` from:
- original SOURCE FULL-BODY evidence for body geometry
- original SOURCE FACE CLOSE-UP evidence for identity
- `DH001_PROFILE_CARD` only as supporting text

The face sheet is not required as upstream identity authority.

### Step 6 — INTERNAL BODY QC
Check:
- height/build impression
- shoulder/hip relation
- torso/leg relation
- neutral pose
- front/side/back orientation
- same-person appearance

A visibly wrong body sheet may receive up to 2 automatic strategy-changing retries from SOURCE.

### Step 7 — PRESENT CHARACTER CARD
Present all three deliverables together as the character-card package:

```text
DH001_PROFILE_CARD
DH001_FACE_3VIEW_SHEET
DH001_BODY_3VIEW_SHEET
```

No mid-process confirmation is required. The user can review the completed package once all three are available.

## STAR TOPOLOGY
Generated character-card assets do not generate each other.

Required pattern:

```text
SOURCE → PROFILE_CARD
SOURCE → FACE_3VIEW_SHEET
SOURCE → BODY_3VIEW_SHEET
```

Never use FACE_3VIEW_SHEET to generate BODY_3VIEW_SHEET.

A generated candidate cannot become SOURCE.

If an output is rejected, regenerate from SOURCE rather than from the rejected output.

## Approval and Master Promotion
Every generated sheet begins as `CANDIDATE`.

After the three deliverables are shown, final human approval may promote validated assets:
- approved `DH001_FACE_3VIEW_SHEET` → `IDENTITY_MASTER V1`
- approved `DH001_BODY_3VIEW_SHEET` → `BODY_MASTER V1`

There is no automatic promotion. A generated sheet does not become upstream identity authority merely because it looks plausible.

If the user rejects likeness, treat identity as failed and regenerate from SOURCE.

After final human approval:

```yaml
character_id: DH001
status: CHARACTER_CARD_READY
profile_card: DH001_PROFILE_CARD
identity_master: IDENTITY_MASTER V1
body_master: BODY_MASTER V1
face_sheet: DH001_FACE_3VIEW_SHEET
body_sheet: DH001_BODY_3VIEW_SHEET
next_skill: hermes-creative-digital-human
```
