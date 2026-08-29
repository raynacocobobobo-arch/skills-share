---
name: hermes-digital-human-character-card
description: Use when establishing or rebuilding a reusable digital-human character from real-person full-body photos, face close-ups, and partial or complete profile information, especially for 人物卡、数字人建模、人物三视图、面部三视图、锁定人物 or reusable master-asset requests.
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
Create the smallest useful reusable character package from real-person source evidence before wardrobe, environment, action, or batch content production.

**Core rule: preserve identity first. The character card is a source-derived working asset, not a beauty redesign.**

The skill has exactly three core deliverables:

1. `DH001_PROFILE_CARD`
2. `DH001_FACE_3VIEW_SHEET`
3. `DH001_BODY_3VIEW_SHEET`

Keep the workflow practical. Do not add extra deliverables, complex scoring systems, or unnecessary engineering unless the user explicitly asks.

## Hard Execution Contract
When Hermes routing resolves to this character-card skill, the operator/assistant must load this `SKILL.md` before any identity-bearing image operation.

Required execution order:

```text
ROUTE → LOAD SKILL → RESOLVE SOURCE → PROFILE_CARD → FACE_3VIEW_SHEET → FACE QC → BODY_3VIEW_SHEET → BODY QC → DELIVERY
```

Rules:
- Never jump directly from a Hermes character-card request to image generation.
- Do not claim that the character-card skill was executed if this SKILL.md was not loaded in the current execution path.
- The original uploaded images remain the visual authority throughout the run; conversation history does not replace SOURCE.
- A later generated image is not automatically a better reference than the original SOURCE.

## Shorthand Invocation
The user should not need to repeat the long character-card prompt every time.

Treat phrases such as:
- `路由到 Hermes 人物卡技能`
- `用 Hermes 人物卡`
- `建立人物卡`
- `锁定这个人物`
- `用 hermes-digital-human-character-card`
- `做一个人物卡`
- `数字人人物卡`

as a request to use this skill in `FULL AUTO MODE` and produce exactly:

1. `PROFILE_CARD`
2. `FACE_3VIEW_SHEET`
3. `BODY_3VIEW_SHEET`

Default shorthand behavior:
- identity consistency is the first priority
- original uploaded photos remain the sole `SOURCE` authority
- partial factual profile information is allowed
- missing useful information may be supplemented as `OBSERVED`, `ESTIMATED`, or `UNKNOWN`
- keep `USER_CONFIRMED / OBSERVED / ESTIMATED / UNKNOWN` distinct
- keep the three deliverables separate
- never combine PROFILE + FACE + BODY into one poster
- generate FACE and BODY directly from original SOURCE, not from prior generated outputs
- do not ask the user to repeat this contract if the shorthand intent is clear

Minimum source requirement:
- at least one usable full-body or near-full-body image
- at least one usable face or close-up image

Only ask for more input when one of those minimum source requirements is missing or the SOURCE is too weak to preserve identity reliably. Missing age, weight, hairstyle, or similar profile fields must not block normal execution.

## Required Inputs
The user may provide as much or as little factual information as they know. Do not block normal execution just because some profile fields are missing.

### SOURCE FULL-BODY
Original full-body or near-full-body photos used for height impression, body proportions, silhouette, posture, and visible body geometry.

Prefer front and side evidence when available. A genuine back view is useful but not mandatory. Unseen details may be conservatively inferred for a generated back view, but must not be presented as observed fact.

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

All fields are optional.

If the user asks what information to provide, offer this lightweight form:

```yaml
人物资料:
  姓名/代号:
  性别:
  年龄:
  身高:
  体重:
  发型:
  发色:
  体型:
  眼镜:
  特殊面部特征:
  痣/疤痕/胎记:
  其他必须锁定的信息:
```

The user may leave unknown fields blank.

## Information Confidence
PROFILE_CARD should be useful even when factual profile data is incomplete. Supplement missing information only when the SOURCE supports a useful visual description or conservative estimate.

Use four source labels:
- `USER_CONFIRMED` — explicitly provided by the user
- `OBSERVED` — directly visible in SOURCE images
- `ESTIMATED` — reasonable modeling-oriented visual estimate
- `UNKNOWN` — insufficient evidence

Rules:
- user-confirmed facts override visual estimates
- never present `ESTIMATED` information as fact
- useful morphology such as lean/average/stocky build, face shape, shoulder-to-hip relation, posture, or approximate age impression may be estimated when visually supportable
- do not infer sensitive traits such as ethnicity from appearance
- do not invent exact weight, exact age, clothing-hidden measurements, or fake biometric precision
- if evidence is weak, use `UNKNOWN`

## Output Contract

### 1. DH001_PROFILE_CARD
Create a concise practical profile card from user facts plus visible morphology.

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

Each useful non-factual visual field should indicate `OBSERVED`, `ESTIMATED`, or `UNKNOWN` when ambiguity matters.

`PROFILE_CARD` is a text / structured-information deliverable. Do not call image generation merely to turn it into a poster or infographic.

### 2. DH001_FACE_3VIEW_SHEET
Generate one face three-view sheet containing exactly:
- `FACE_FRONT`
- `FACE_LEFT45`
- `FACE_RIGHT45`

Sheet target:
- same person across all three panels
- same age impression
- neutral or mild expression
- plain neutral background
- even soft lighting
- minimal beautification or stylization
- consistent crop, scale, and camera feel
- large, useful head-and-shoulders views
- preserve continuity-critical glasses, helmet, or other identity presentation when removing them would require unsupported invention

Hard output isolation:
- FACE sheet must contain face views only
- no PROFILE_CARD
- no BODY_3VIEW
- no biography/statistics table
- no combined character-design poster

#### Face Source Lock
Each of FACE_FRONT, FACE_LEFT45, and FACE_RIGHT45 must be solved from original SOURCE FACE CLOSE-UP evidence.

Do not generate a side/45-degree identity by treating a generated front view as the new identity source.

Generated FACE panels are siblings, not parents. They may be displayed together as one sheet, but none of them gains upstream identity authority over another panel.

If a requested angle is not directly photographed in SOURCE, infer only the view transformation conservatively while preserving identity from the strongest original face evidence. Do not solve missing-angle identity by chaining from a generated panel.

### 3. DH001_BODY_3VIEW_SHEET
Generate one full-body three-view sheet containing exactly:
- `BODY_FRONT`
- `BODY_SIDE`
- `BODY_BACK`

Sheet target:
- full body visible head-to-toe
- same height/build impression across all panels
- neutral standing pose
- same-person identity
- simple fitted neutral clothing or source-continuity workwear when clothing is identity-critical
- consistent camera height, focal-length feel, scale, background, and lighting
- side view close to true 90°
- back view close to true 180°

Hard output isolation:
- BODY sheet must contain body views only
- no PROFILE_CARD
- no FACE_3VIEW
- no biography/statistics table
- no combined character-design poster

#### Body Source Lock
For BODY_3VIEW generation:
- original SOURCE FULL-BODY controls body geometry
- original SOURCE FACE CLOSE-UP controls facial identity
- PROFILE_CARD is supporting text only

Do not use the generated FACE_3VIEW_SHEET as upstream identity authority for BODY_3VIEW_SHEET.

Replace `DH001` with the active `character_id`.

## FULL AUTO MODE
After sufficient SOURCE is supplied, a normal FULL AUTO request runs continuously:

```text
PROFILE_CARD → FACE_3VIEW_SHEET → BODY_3VIEW_SHEET
```

Do not ask the user to say “next” between stages.

**FULL AUTO means continuous execution, not a single combined image.**

All three deliverables must remain separate.

## Workflow

### Step 1 — SOURCE INTAKE
1. Assign or confirm `character_id`.
2. Classify original images as `SOURCE FULL-BODY` or `SOURCE FACE CLOSE-UP`.
3. Record user-provided facts separately.
4. Identify strongest identity and body evidence.
5. If SOURCE is too weak to identify the person reliably, stop rather than guess.

### Step 2 — PROFILE CARD
Create `DH001_PROFILE_CARD`.

Separate:
- `USER_CONFIRMED`
- `OBSERVED`
- `ESTIMATED`
- `UNKNOWN`

The profile card supports consistency but never overrides SOURCE images.

### Step 3 — FACE THREE-VIEW SHEET
Generate `DH001_FACE_3VIEW_SHEET` directly from original SOURCE FACE CLOSE-UP evidence.

Do not derive one panel from another generated panel. The identity authority remains SOURCE.

Before invoking an image tool, re-select/re-attach the strongest original face SOURCE available to the current runtime rather than relying on a previously generated image in the chat.

### Step 4 — INTERNAL FACE QC
Compare the generated face sheet against SOURCE.

Check:
- recognizability
- face ratio
- eye shape and spacing
- brows
- nose
- mouth
- jaw/chin
- age impression

If visibly wrong, retry with a materially changed strategy. Default budget: up to 2 automatic retries.

If the image contains PROFILE + FACE + BODY or any combined infographic layout, mark it `LAYOUT_FAIL`; do not present it as the formal FACE deliverable. Retry with stricter output isolation.

### Step 5 — BODY THREE-VIEW SHEET
Generate `DH001_BODY_3VIEW_SHEET` directly from:
- original SOURCE FULL-BODY for body geometry
- original SOURCE FACE CLOSE-UP for identity
- PROFILE_CARD as supporting text only

Do not use a generated FACE sheet as upstream identity authority.

Before invoking an image tool, re-select/re-attach the original full-body and face SOURCE required for the BODY sheet. Do not rely on the FACE sheet merely because it is the most recent character image.

### Step 6 — INTERNAL BODY QC
Check:
- height/build impression
- shoulder/hip relation
- torso/leg relation
- neutral pose
- front/side/back orientation
- same-person appearance

If visibly wrong, retry with a materially changed strategy. Default budget: up to 2 automatic retries.

If the image contains PROFILE + FACE + BODY or any combined infographic layout, mark it `LAYOUT_FAIL`; do not present it as the formal BODY deliverable. Retry with stricter output isolation.

### Step 7 — FINAL DELIVERY
Present all three deliverables together, but as separate outputs:

```text
DH001_PROFILE_CARD
DH001_FACE_3VIEW_SHEET
DH001_BODY_3VIEW_SHEET
```

Do not finish with image links alone. The final delivery must also include the PROFILE_CARD content.

## Likeness Rejection Hard Stop
A user statement such as `不像本人`, `不是这个人`, `脸跑了`, `人脸不对`, or an equivalent likeness rejection is authoritative QC feedback.

On such feedback:
1. mark the affected candidate `IDENTITY_FAIL`
2. exclude the rejected candidate from all subsequent identity/reference inputs
3. do not let it become SOURCE, a master, or an implicit chat-history reference
4. restart from original SOURCE with a materially changed strategy
5. re-run the relevant FACE or BODY QC before continuing

The latest generated image is never preferred merely because it is recent in the chat.

Do not repair identity by chaining from the wrong person. A rejected candidate may not become the parent of another character-card candidate.

## STAR TOPOLOGY
Generated character-card assets do not generate each other.

Required pattern:

```text
SOURCE → PROFILE_CARD
SOURCE → FACE_3VIEW_SHEET
SOURCE → BODY_3VIEW_SHEET
```

A generated candidate cannot become SOURCE.

If an output is rejected, regenerate from original SOURCE rather than from the rejected output.

## Approval and Master Promotion
Every generated sheet begins as `CANDIDATE`.

After the three deliverables are shown, final human approval may promote:
- approved `DH001_FACE_3VIEW_SHEET` → `IDENTITY_MASTER V1`
- approved `DH001_BODY_3VIEW_SHEET` → `BODY_MASTER V1`

There is no automatic promotion.

After final approval:

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
