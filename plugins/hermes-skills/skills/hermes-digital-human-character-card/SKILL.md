---
name: hermes-digital-human-character-card
description: Use when establishing or rebuilding a reusable digital-human character from real-person full-body photos, face close-ups, and partial or complete factual profile information, especially for 人物卡、数字人建模、人物三视图、面部三视图、锁定人物 or reusable master-asset requests.
version: 1.2.0
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

# Hermes Digital Human Character Card V1.2

## Purpose
Create a small reusable upstream character package from real-person SOURCE evidence before wardrobe, environment, action, or batch content production.

**Core rule: identity first, ATOMIC RENDER second, deterministic assembly last.**

This version exists because ChatGPT Web and general image models tend to visually aggregate all visible character information into one poster. The workflow therefore separates image creation from sheet layout.

The skill has exactly three final deliverables:

1. `DH001_PROFILE_CARD` — text / structured information
2. `DH001_FACE_3VIEW_SHEET` — deterministic assembly of three atomic face views
3. `DH001_BODY_3VIEW_SHEET` — deterministic assembly of three atomic body views

The image model must never create those three deliverables as one combined visual object.

## Shorthand Invocation
Treat phrases such as:
- `路由到 Hermes 人物卡技能`
- `用 Hermes 人物卡`
- `建立人物卡`
- `锁定这个人物`
- `用 hermes-digital-human-character-card`
- `做一个人物卡`
- `数字人人物卡`

as a request to use this skill in `FULL AUTO MODE`.

Default shorthand behavior:
- original uploaded photos remain the sole `SOURCE` authority
- identity consistency has priority over beautification
- partial factual profile information is allowed
- do not ask the user to repeat this contract when shorthand intent is clear
- continue automatically through atomic renders, QC, deterministic assembly, and final delivery unless SOURCE is insufficient

Minimum useful SOURCE:
- at least one usable full-body or near-full-body image
- at least one usable face or close-up image

Missing age, weight, hairstyle, or similar profile fields must not block execution when sufficient visual SOURCE exists.

## Required Inputs

### SOURCE FULL-BODY
Original full-body or near-full-body photos used for body proportions, silhouette, visible posture, and height impression.

Prefer front and side evidence when available. A genuine back view is useful but not mandatory. Unseen back details may be conservatively inferred for a generated back view, but must not be presented as observed fact.

### SOURCE FACE CLOSE-UP
Original clear face photos used as primary identity evidence. Prefer:
- front
- left 30–45°
- right 30–45°
- optional genuine profile views

Use minimally stylized images with visible eyes, nose, mouth, jaw, and hairline when possible.

### FACTUAL PROFILE
User-provided information may include:
- `name_or_id`
- `sex`
- `age`
- `height`
- `weight`
- `hairstyle`
- `hair_color`
- `body_type`
- `glasses`
- visible marks or other continuity-critical settings

All profile fields are optional.

## Information Confidence
Use four labels in `PROFILE_CARD`:
- `USER_CONFIRMED` — explicitly provided by the user
- `OBSERVED` — directly visible in SOURCE
- `ESTIMATED` — conservative modeling-oriented estimate
- `UNKNOWN` — insufficient evidence

Rules:
- user-confirmed facts override visual estimates
- never present `ESTIMATED` as fact
- do not infer sensitive traits such as ethnicity from appearance
- do not invent exact weight, exact age, hidden measurements, biography, occupation, or personality facts
- if evidence is weak, use `UNKNOWN`

## PROFILE_CARD
Build `DH001_PROFILE_CARD` internally from user facts plus visible morphology.

Suggested structure:

```yaml
character_id: DH001
facts:
  name_or_id: {value: null, source: UNKNOWN}
  sex: {value: null, source: UNKNOWN}
  age: {value: null, source: UNKNOWN}
  height: {value: null, source: UNKNOWN}
  weight: {value: null, source: UNKNOWN}
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
  hair_color:
  visible_skin_tone:
identity_marks:
  - only user-confirmed or visible continuity features
uncertainty:
  - unsupported or weakly supported details
```

`PROFILE_CARD is text-only`.

Do not pass PROFILE_CARD into any image-generation job.

Do not present the full PROFILE_CARD before the six atomic renders are complete. Build it internally, use only the minimum render-critical facts when needed, and present the full card during `FINAL DELIVERY`.

Render-critical facts may include only user-confirmed facts that materially affect the requested visual asset, such as age impression, height impression, sex/presentation, glasses, or an explicitly required hairstyle. Do not pass biography-style profile text into visual generation.

## ATOMIC RENDER
Visual creation consists of six separate ATOMIC IMAGE JOBS:

### Face atomic jobs
1. `FACE_FRONT`
2. `FACE_LEFT45`
3. `FACE_RIGHT45`

### Body atomic jobs
4. `BODY_FRONT`
5. `BODY_SIDE`
6. `BODY_BACK`

Hard execution rule: `one view per image-generation call`.

Each atomic render must contain:
- one person only
- one requested camera/view orientation only
- plain neutral background
- simple even lighting
- no text
- no title
- no labels
- no grid
- no extra panels
- no biography
- no statistics
- no reference-image gallery
- no character-design layout

The image model must never be asked to generate a character card.
The image model must never be asked to generate a face three-view sheet.
The image model must never be asked to generate a body three-view sheet.
The image model must never be asked to generate an infographic.

### ChatGPT Web execution note
ChatGPT Web image generation may infer intent from the surrounding conversation rather than from a fully isolated API prompt. Before every image-generation call, make the immediately active execution instruction about one atomic view only. Do not restate the total package, future views, PROFILE_CARD, or sheet layout immediately before the call.

Do not ask the image model to add view labels. Labels belong to deterministic assembly.

## Atomic View Targets

### FACE_FRONT
- head-and-shoulders
- near-frontal camera
- neutral or mild expression
- preserve SOURCE face ratio, eyes, brows, nose, mouth, jaw/chin, hairline, and age impression

### FACE_LEFT45
- head-and-shoulders
- approximately left 45°
- same age and identity as SOURCE
- preserve visible facial structure without beautification redesign

### FACE_RIGHT45
- head-and-shoulders
- approximately right 45°
- same age and identity as SOURCE
- preserve visible facial structure without beautification redesign

### BODY_FRONT
- full body head-to-toe
- neutral standing pose
- front orientation
- simple fitted neutral clothing or source-continuity workwear when identity/presentation requires it
- preserve height/build impression from SOURCE and user-confirmed facts

### BODY_SIDE
- full body head-to-toe
- neutral standing pose
- close to true 90° side orientation
- preserve body proportions and same-person identity from SOURCE

### BODY_BACK
- full body head-to-toe
- neutral standing pose
- close to true 180° back orientation
- infer unseen details conservatively; do not present inferred back details as observed facts

## ATOMIC VIEW QC
After each atomic render, compare that single image against original SOURCE before rendering the next dependent deliverable stage.

Face checks:
- recognizability
- face ratio
- eye shape and spacing
- brows
- nose
- mouth
- jaw/chin
- hairline
- age impression
- requested angle

Body checks:
- height/build impression
- shoulder/hip relation
- torso/leg relation
- neutral pose
- correct front/side/back orientation
- same-person appearance

If one atomic view fails, regenerate only that failed view from SOURCE.

Do not regenerate or redesign the whole sheet.

Do not use a failed atomic view as reference evidence for another view.

Default automatic retry budget: up to 2 materially changed retries for the failed atomic view. If identity remains unreliable, stop and report the tool/SOURCE limitation instead of inventing a false master.

## DETERMINISTIC SHEET ASSEMBLY
After all three face atomic views pass QC, build `DH001_FACE_3VIEW_SHEET` using Python/PIL or an equivalent non-generative compositor.

Assembly input:

```text
FACE_FRONT + FACE_LEFT45 + FACE_RIGHT45
```

Assembly rules:
- three equal panels
- order: FRONT | LEFT45 | RIGHT45
- consistent canvas height and visual scale
- neutral outer margin
- optional simple labels applied by the compositor only
- no biography or statistics
- no decorative character-card design

After all three body atomic views pass QC, build `DH001_BODY_3VIEW_SHEET` using Python/PIL or an equivalent non-generative compositor.

Assembly input:

```text
BODY_FRONT + BODY_SIDE + BODY_BACK
```

Assembly rules:
- three equal panels
- order: FRONT | SIDE | BACK
- full body must remain head-to-toe in every panel
- consistent canvas height and visual scale
- neutral outer margin
- optional simple labels applied by the compositor only
- no biography or statistics

Do not call image generation during sheet assembly.

The compositor may crop, pad, resize, align, and label. It must not synthesize new facial features, body geometry, clothing, background content, or missing anatomy.

## FULL AUTO MODE
FULL AUTO means automatic orchestration, not visual aggregation.

Required sequence:

```text
SOURCE INTAKE
→ PROFILE BUILD (internal)
→ 6 ATOMIC RENDERS
→ ATOMIC VIEW QC / targeted retries
→ 2 DETERMINISTIC ASSEMBLIES
→ FINAL DELIVERY
```

No intermediate user reply is required during a normal successful run.

The user may interrupt or reject any result at any time.

## STAR TOPOLOGY
Every atomic view is generated directly from original SOURCE evidence.

Required pattern:

```text
SOURCE → FACE_FRONT
SOURCE → FACE_LEFT45
SOURCE → FACE_RIGHT45
SOURCE → BODY_FRONT
SOURCE → BODY_SIDE
SOURCE → BODY_BACK
```

A generated atomic view must never become SOURCE.

Forbidden:

```text
FACE_FRONT → FACE_LEFT45
FACE_3VIEW_SHEET → BODY_FRONT
BODY_FRONT → BODY_SIDE
failed candidate → next candidate
```

The assembled sheets are downstream review assets. They do not create or redefine the six atomic views.

## FINAL DELIVERY
Present exactly these three final deliverables:

```text
DH001_PROFILE_CARD
DH001_FACE_3VIEW_SHEET
DH001_BODY_3VIEW_SHEET
```

Keep them separate:
- PROFILE_CARD as text / structured content
- FACE sheet as one assembled image file
- BODY sheet as another assembled image file

Do not create a fourth combined poster.

## Approval and Master Promotion
All generated atomic views and assembled sheets begin as `CANDIDATE`.

After final human approval:
- approved face atomic set + `DH001_FACE_3VIEW_SHEET` may be promoted to `IDENTITY_MASTER V1`
- approved body atomic set + `DH001_BODY_3VIEW_SHEET` may be promoted to `BODY_MASTER V1`

There is no automatic promotion; `no automatic promotion` is allowed.

If the user rejects likeness, mark the affected atomic view(s) rejected and regenerate from SOURCE only.

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

## MANUAL REGRESSION CASE
Use this real failure pattern when validating the skill in ChatGPT Web.

Input:

```text
SOURCE: multiple person photos
height: 180cm
sex: 男
age: 40岁
instruction: 路由到 Hermes 人物卡技能
```

PASS:
- six image-generation calls, each containing one requested view only
- no image-generation call creates a multi-panel character sheet
- FACE sheet is assembled non-generatively from three passed face views
- BODY sheet is assembled non-generatively from three passed body views
- PROFILE_CARD is delivered as text after the atomic renders

FAIL / `ARCHITECTURE FAIL`:
- any image-generation call produces `PROFILE + FACE + BODY` in one visual
- any image-generation call invents biography/statistics because it was prompted as a character card
- a combined failed poster is cropped and promoted as the formal FACE or BODY deliverable
- one generated view becomes the identity source for another generated view
