---
name: hermes-creative-digital-human
description: Use when creating or maintaining a realistic digital human, virtual creator, AI blogger, outfit variant, pose variant, or real-scene composite where identity consistency across generations matters.
version: 2.5.0
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
  - 换衣
  - 换工装
---

# Hermes Creative Digital Human V2.5

## Purpose
Build a reusable digital-human production asset with explicit identity control. V2.5 keeps the V2.4 identity-anchor, hard-stop, face-repair, sticky-session, and star-topology rules, and adds automatic natural-language reference-role resolution plus a contamination firewall for wardrobe/body/pose/scene references.

**Core principle: identity is an upstream asset, not a prompt adjective. A three-view sheet, outfit photo, pose photo, scene photo, or prior generated image does not become identity authority merely because a person is visible in it.**

## Hard Execution Contract
When this skill is the resolved Hermes route, the operator/assistant must actually read this `SKILL.md` before any identity-bearing image generation or edit.

Do not claim that Hermes routing, preflight, reference mapping, or identity locking was executed if the skill was not loaded in the current execution path.

For identity-bearing image work, the order is:

`ROUTE -> LOAD SKILL -> RESOLVE TASK OBJECT -> RESOLVE REFERENCES -> BUILD INTERNAL REFERENCE MAP -> PREFLIGHT -> SELECT EDIT/GENERATE STRATEGY -> IMAGE OPERATION -> IDENTITY GATE`

Never jump directly from the user request to an image-generation call when Hermes routing was requested.

## V2 Asset Architecture
| Layer | Asset | Responsibility | May define identity? |
|---|---|---|---|
| L0 SOURCE | Original user photos + factual data | Ground-truth evidence | Yes |
| L1 IDENTITY MASTER | Human-approved face identity set | WHO this person is | Yes |
| L1 BODY MASTER | Human-approved body/proportion set | Body geometry | Body only |
| L1 IDENTITY SUPPORT | Approved FACE_CROP_PACK | Close-view identity support | Supports approved identity only |
| L2 APPEARANCE | Clothing, PPE, accessories, footwear | Presentation | No |
| L2 POSE / PROP | Pose, hands, equipment, camera, monopod, etc. | Action and prop geometry | No |
| L2 SCENE | Environment, camera position, perspective, lighting | Scene | No |
| L3 CONTENT | Final composites, lifestyle/social images | Publishable output | Never |

Only L0 SOURCE and explicitly approved L1 Identity Masters may be upstream identity anchors. `FACE_CROP_PACK` supports the approved master but never replaces its authority.

## Identity Master Requirements
Prefer original, high-quality, minimally stylized photos. Build a Face ID Set from the strongest available views: front, left 30-45 degrees, right 30-45 degrees, optional genuine profiles, neutral/mild expression, consistent age and recognizable facial structure.

A contact sheet or three-view character sheet may be useful for review, but must not automatically become the identity source. Crop/route individual face views when possible so identity evidence is not diluted by clothing, scene, labels, or unrelated tasks.

## FACE_CROP_PACK
Maintain an optional approved `FACE_CROP_PACK` derived from SOURCE or approved Identity Master views when face identity is too small or diluted in full-body/scene references.

Typical aliases:

```text
@DH001_FACE_FRONT_CLOSE
@DH001_FACE_L45_CLOSE
@DH001_FACE_R45_CLOSE
```

Rules:
- crops must preserve the same approved identity and age impression
- use minimally stylized, high-quality close views
- choose the crop whose view most closely matches the target head angle
- every crop used in generation/repair is `IDENTITY ONLY | CRITICAL`
- FACE_CROP_PACK supports the approved identity; it is not an independent person definition
- generated/repaired content cannot automatically become a FACE_CROP_PACK source

## Identity Gate
Before body variants, wardrobe, complex poses, props, scene integration, or batch production, identity must pass. Check face ratio, eye shape/spacing, brows, nose, mouth, jaw/chin, ears when visible, hairline, age impression, and overall recognizability.

If the user says the person does not look like the reference, treat that candidate as **Identity Gate = FAIL**. Shared clothing, glasses, helmet, age, ethnicity, hairstyle, or body type are not proof of identity.

## Approved Reference Pool
Every generated asset is `CANDIDATE`, `APPROVED`, or `REJECTED`. Only `APPROVED` assets may enter a reusable reference pool. `REJECTED` assets must never be reused as identity references.

## Identity Anchor Card
Maintain one Identity Anchor Card per character. Do not create a global digital-human registry.

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

Tags are stable addresses, not image payloads. The exact approved asset still has to be attached/selected when the active image tool requires visual input.

Approved identity masters are immutable. If identity authority changes, create `V2`, mark it ACTIVE, and mark the previous version DEPRECATED. Never silently overwrite an approved master.

## Natural-Language Reference Resolver
The user should not have to write `REF01`, `IDENTITY ONLY`, `BODY ONLY`, or priority labels manually.

Before every identity-critical operation, resolve roles automatically from the user's current natural-language instructions and the actual attached images.

### User wording has highest authority
Examples:
- `图1锁脸 / 图1是面部基准 / 面部特征为图1` -> `IDENTITY ONLY | CRITICAL`
- `图2作为身体三视图 / 保持图2体型` -> `BODY ONLY | HIGH`
- `图3只参考衣服 / 换成图3工装 / 参考图3穿搭` -> `WARDROBE ONLY | NORMAL`
- `只参考这个动作` -> `POSE ONLY | NORMAL`
- `只参考这个环境` -> `SCENE ONLY | NORMAL`

When the user explicitly states a role, do not let visual similarity override it.

### Automatic role inference
If wording is concise but the intended role is still clear, infer the role instead of asking the user to write technical labels.

Typical pattern:

```text
User: 图1锁脸，图2三视图，换图3衣服。
Internal map:
REF01 = image 1 | IDENTITY ONLY | CRITICAL
REF02 = image 2 | BODY ONLY | HIGH
REF03 = image 3 | WARDROBE ONLY | NORMAL
```

The internal map is execution metadata. Do not make the user repeat it unless they explicitly ask to inspect it.

### Ambiguity rule
Ask a clarifying question only when identity authority or another required role cannot be determined safely, for example:
- multiple different people are uploaded and none is identified as the identity source
- two different face sets are both presented as authoritative
- the user says "换这个" but it is unclear whether they mean person, clothing, pose, or scene

Do not ask merely because the user omitted technical REF syntax.

## Reference Contamination Firewall
Every active reference has one declared control role. Information outside that role is non-authoritative and must be actively excluded from the operation.

| Role | May control | Must NOT control by default |
|---|---|---|
| `IDENTITY ONLY` | face identity, age impression | wardrobe, body pose, scene |
| `BODY ONLY` | height impression, body proportions, silhouette | face identity, facial age, hairstyle |
| `WARDROBE ONLY` | clothing, PPE, accessories explicitly requested, footwear | face, age, facial hair, hair, head shape, ethnicity, body identity, unrelated pose |
| `POSE ONLY` | pose, hands, action, prop interaction | face identity, age, wardrobe identity, scene identity |
| `SCENE ONLY` | environment, camera geometry, lighting, perspective | identities of people visible in the scene, wardrobe identity |

### Wardrobe-person firewall
A wardrobe/PPE reference containing another person is especially high risk. Unless the user explicitly requests a visible accessory from that person, ignore that person's:
- face and facial proportions
- age impression
- glasses
- hairstyle and hairline
- head/skull shape
- facial hair
- skin identity cues
- body identity cues not required to reproduce garment fit

Read only the requested apparel/PPE properties: garment cut, color, panels, reflective strips, patches/logos where permitted, closures, pockets, helmet/PPE style, footwear, and other explicitly requested accessories.

Example: if an orange workwear photo shows a different man wearing glasses, the glasses and that man's face are **not** part of `WARDROBE ONLY` unless the user explicitly says to copy the glasses.

### Body-face firewall
A body three-view sheet that contains a visible face does not gain identity authority when its role is `BODY ONLY`. When an `IDENTITY ONLY` reference is present, the face must come from the identity reference, not from the body sheet.

## Operation Classifier
Before choosing an image path, classify the requested operation.

### Appearance-preserving edit
Phrases such as:
- 换衣 / 换工装 / 换穿搭
- 保持人物不变
- 脸不要变
- 图1锁脸，把图3衣服换到图2人物上

resolve to `APPEARANCE_EDIT` unless the user asks to redesign the person.

For `APPEARANCE_EDIT`:
1. preserve the approved identity
2. preserve body geometry if a BODY reference is supplied
3. change only the requested appearance layer
4. use Edit-first when a reference-preserving edit path is available
5. do not silently turn the task into "generate a new person wearing similar clothes"

### Fresh generation
Use fresh generation only when the requested view/composition/pose/scene cannot reasonably be achieved through a preserving edit, or when no valid editable base exists.

Fresh generation never weakens identity authority. It must still start from the ACTIVE approved identity evidence and pass Identity Gate.

### Runtime truth rule
Do not describe an operation as a preserving edit merely because the prompt says "edit". If the active runtime/tool cannot confirm a preserving edit path, or runtime metadata indicates a fresh generation (for example an edit operation is absent/null), treat the result as a **fresh candidate generation** and apply the stricter Identity Gate. Never claim that identity was preserved by editing when the tool actually regenerated the image.

## ChatGPT Web Session Contract
For long-running production, use one project + multiple short chats + permanent master assets. Project/chat context may carry naming, workflow status, and production notes, but conversation history is not an identity source.

### Sticky Skill Binding
Once a digital-human task object is routed here, keep the active skill binding on `hermes-creative-digital-human` for ordinary follow-ups about the same character: likeness, clothing, scene, pose, camera, props, continuity, review, or batch outputs.

Release/re-route only when the user changes the primary task object or explicitly ends/switches the workflow.

### Digital Human Session State
Maintain a lightweight state card in the active production context. Do not create a global state registry.

```yaml
active_skill: hermes-creative-digital-human
skill_version: 2.5.0
character_id: DH001
current_step: 3
active_identity: V1
identity_anchor: READY
completed:
  - SOURCE_INTAKE
  - IDENTITY_MASTER
pending:
  - STANDARD_THREE_VIEW
  - IDENTITY_VALIDATION
next_allowed_action:
  - build_standard_three_view
deferred_requirements: []
```

Update state after approval/rejection, master-version change, gate result, step completion/transition, or next-action change. Do not rewrite it for casual discussion.

In a new chat, re-bootstrap only from approved assets and known gate results actually available. Do not infer identity from invisible chat history.

## Explicit Master Re-attachment
Every new production chat and every identity-critical generation/edit must resolve the ACTIVE Identity Anchor and explicitly attach/select the exact approved `IDENTITY_MASTER`. Attach `BODY_MASTER` when body geometry matters.

"Same person as before" or a symbolic tag alone is not sufficient when the active tool needs the actual image.

If the correct master is absent, stop before generation and restore the approved master rather than guessing.

## Internal Reference Map
Before every identity-critical operation, build an internal map from the Natural-Language Reference Resolver.

```text
REF01 = @DH001_ID_V1_FRONT | IDENTITY ONLY | CRITICAL
REF02 = @DH001_BODY_V1_FRONT | BODY ONLY | HIGH
REF03 = @DH001_WARDROBE_RIG_01 | WARDROBE ONLY | NORMAL
REF04 = @POSE_PHOTOGRAPHER_MONOPOD_03 | POSE ONLY | NORMAL
REF05 = @SCENE_RIG_RAIN_02 | SCENE ONLY | NORMAL
```

The user is not required to type this map. The operator creates it automatically whenever the roles are clear.

During `FACE_REPAIR`, add matching approved FACE_CROP_PACK views as `IDENTITY ONLY | CRITICAL`; the ACTIVE Identity Master remains authoritative.

## Generation Preflight
Before any identity-bearing generation/edit, verify:
- active skill binding is `hermes-creative-digital-human`
- character/task object is resolved
- requested operation type is resolved
- required upstream gates are PASS or the workflow is explicitly at the step that creates that gate's candidate
- ACTIVE identity is resolved
- exact identity master images required by the tool are attached
- BODY master is present when body geometry matters
- internal Reference Map exists
- each reference has exactly one control role
- contamination firewall exclusions are applied
- edit/generate strategy has been selected intentionally

If all required checks pass: `PREFLIGHT PASS` and proceed.

If any required check fails: `PREFLIGHT BLOCKED`, name the missing prerequisite, restore it, and **do not execute identity-bearing image generation**.

## No Generation Chaining
Forbidden:

`SOURCE -> generated A -> generated B -> generated C`

Required star topology:

`SOURCE / IDENTITY_MASTER -> candidate A`
`SOURCE / IDENTITY_MASTER -> candidate B`
`SOURCE / IDENTITY_MASTER -> candidate C`

A failed candidate is not an upstream reference simply because it is the latest image in the chat.

The only narrow exception is eligible `FACE_REPAIR`: the failed image may be used as a temporary composition carrier while identity still comes from approved `IDENTITY_MASTER + FACE_CROP_PACK`.

## Tool Capability Tiers
### Tier A — Identity-aware
Explicit identity conditioning such as face embedding, FaceID/InstantID/PuLID/PhotoMaker-class conditioning, or a documented platform identity-preservation feature.

### Tier B — Multi-reference image generation
Accepts references but has no verified identity-specific conditioning. It may resemble the source but must not be described as guaranteed identity lock.

### Tier C — Prompt/ordinary generation
No reliable identity conditioning. Use for scene design, pose prototypes, wardrobe exploration, stand-ins, and composition. Identity-bearing output requires stronger caution and strict gate review.

Repeated Tier B/C identity failure should change strategy or escalate tool capability, not repeat the same prompt indefinitely.

## Edit-first / Generate-second
When a valid approved identity-bearing image exists and the active tool supports preserving edits, prefer editing the requested layer only.

Use fresh generation when preserving edit constraints cannot solve the required view, pose, geometry, or scene change.

Both paths require explicit master attachment and preflight. Edit-first is not permission to start from a drifted/rejected image, except for eligible FACE_REPAIR.

## Final Image Triage
After an identity-bearing candidate is visible, classify exactly one:
- `APPROVED` — identity and relevant shot layers pass
- `FACE_REPAIR` — composition/body/pose/prop/scene/head geometry are worth preserving; only localized facial identity/age needs correction
- `REGENERATE` — failure is broader than face-only or local repair is structurally unsafe

### Face Repair Eligibility
Choose `FACE_REPAIR` only when composition, body, pose, prop interaction, scene perspective/contact/lighting, head angle, head size, neck connection, and gross skull orientation are already acceptable.

If head angle, body, pose, prop, composition, scene geometry, or head/body relationship is wrong, choose `REGENERATE`.

### FACE_REPAIR
Required identity evidence:
1. ACTIVE approved `IDENTITY_MASTER`
2. matching approved `FACE_CROP_PACK` view(s)

Use the rejected candidate only as a composition carrier. Preserve non-face layers as far as the tool supports. Correct face shape, eye structure/spacing, brows, nose, mouth, jaw/chin, visible hairline, and age impression.

After repair:
- run Identity Gate again
- verify non-face layers did not regress
- run Final Image Triage again

A repaired output may become `CONTENT_APPROVED` after human approval, but it must not automatically become an Identity Master or other upstream identity source.

## Candidate Hard Stop
If an identity-bearing candidate fails Identity Gate:
- mark it `REJECTED` for identity/reference reuse
- exclude it from automatic image selection for the next attempt
- do not use it in wardrobe, scene, action continuity, batch production, or future identity inputs
- recover from the latest approved upstream master

If `Final Image Triage = FACE_REPAIR`, keep it only as a temporary composition carrier. Its identity remains rejected.

This rule specifically prevents chat-history contamination: a recently generated wrong face must not be reused merely because it is visually or temporally close to the current request.

## 8-Step Production Flow
1. SOURCE INTAKE — register original person references and factual data; assign stable `character_id`.
2. IDENTITY MASTER — build and human-approve authoritative face identity; create/update Identity Anchor Card and optional FACE_CROP_PACK.
3. STANDARD THREE-VIEW — build front/side/back body/appearance asset from approved upstream identity and factual body evidence.
4. IDENTITY VALIDATION — verify the same person across master set and three-view; reject drift.
5. WARDROBE — create clothing/PPE variants without redefining identity.
6. ENVIRONMENT — integrate approved person into scenes with perspective/light matching.
7. ACTION — add pose, prop, camera, and interaction complexity; re-run Identity Gate.
8. BATCH CONTENT — produce multiple outputs from the same ACTIVE anchor; never promote batch content into identity authority.

## Detailed Production Pipeline
1. SOURCE INTAKE
2. IDENTITY MASTER Face ID Set
3. FACE_CROP_PACK when useful
4. IDENTITY TEST GRID
5. IDENTITY GATE
6. IDENTITY ANCHOR CARD
7. BODY MASTER
8. BODY GATE
9. APPEARANCE / WARDROBE
10. SESSION BOOTSTRAP
11. NATURAL-LANGUAGE REFERENCE RESOLUTION
12. INTERNAL REFERENCE MAP + CONTAMINATION FIREWALL
13. GENERATION PREFLIGHT
14. OPERATION CLASSIFICATION: EDIT-FIRST / GENERATE-SECOND
15. SHOT DESIGN
16. POSE + PROP PROTOTYPE when complex
17. IDENTITY INTEGRATION
18. IDENTITY GATE again
19. SCENE INTEGRATION
20. FINAL IMAGE TRIAGE
21. FACE_REPAIR when eligible, otherwise REGENERATE
22. REALISM QC
23. APPROVED CONTENT
24. optional image-to-video continuity

## Identity Recovery Loop
1. Mark failed candidate `REJECTED` and remove it from identity/reference inputs.
2. Run Final Image Triage.
3. FACE_REPAIR only if structurally eligible, with approved master + matching FACE_CROP_PACK re-attached.
4. Otherwise resolve ACTIVE Identity Anchor and restart from the latest approved IDENTITY_MASTER.
5. Return to L0 SOURCE only if the approved master is missing, disputed, or invalid.
6. Diagnose drift source: weak identity conditioning, angle mismatch, pose complexity, scene complexity, or conflicting references.
7. Check for reference-role contamination, especially a BODY/WARDROBE/POSE/SCENE image containing another person's face.
8. Change strategy: simplify shot, isolate pose/prop, reduce conflicting references, switch matching face-crop angle, or use a stronger identity-aware path.
9. Rebuild the internal Reference Map from approved inputs only.
10. Re-run preflight and create a fresh candidate from the approved upstream anchor.
11. Re-run Identity Gate.
12. PASS -> continue. FAIL -> remain in bounded recovery; do not create an endless generation chain.

Never repair identity by allowing an already-drifted image to redefine who the person is.

## Identity Test Grid
Before complex production, prefer neutral-background validation: front, left 45, right 45, supported near-profiles, slight look down/up, and medium shot. The goal is to expose drift before scene complexity hides it.

## Video Continuity
For multi-shot video, preserve the same approved identity assets across shots. A continuity frame may guide temporal/pose continuity if approved, but a drifted frame must never enter the identity master pool.

## Workflow Routing
- New character: `workflows/create-character.md`
- Build reusable asset: `workflows/build-character-asset.md`
- Existing character / wardrobe / real-scene content: `workflows/generate-realistic-content.md`
- Bad output / identity drift: `workflows/improve-output.md`

## Asset Naming
Examples: `SOURCE_001`, `@DH001_ID_V1_FRONT`, `@DH001_ID_V1_L45`, `@DH001_ID_V1_R45`, `@DH001_FACE_FRONT_CLOSE`, `@DH001_FACE_L45_CLOSE`, `@DH001_FACE_R45_CLOSE`, `@DH001_BODY_V1_FRONT`, `@DH001_WARDROBE_RIG_01`, `@POSE_CAMERA_MONOPOD_WALK_01`, `@SCENE_DRILLING_SITE_01`, `CONTENT_CANDIDATE_001`, `CONTENT_APPROVED_001`, `CONTENT_REJECTED_001`.