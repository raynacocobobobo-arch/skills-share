# Generate Realistic Content Workflow V2.5

## Preconditions
Required:
- L0 SOURCE
- approved IDENTITY MASTER
- Identity Gate = PASS for an existing production identity
- approved BODY MASTER when full body matters
- per-character Identity Anchor Card
- current Digital Human Session State

Optional identity support: approved `FACE_CROP_PACK`.

Optional presentation assets: APPEARANCE, POSE/PROP, SCENE.

## 0. Production State / Identity Session Bootstrap
Before every new production chat and every identity-critical image operation, resolve the Digital Human Session State and Identity Anchor Card.

Confirm:
- active skill binding = `hermes-creative-digital-human`
- `character_id` is resolved
- `current_step` and `next_allowed_action` are known
- ACTIVE identity version is known
- exact approved IDENTITY MASTER visual input is available
- BODY MASTER is available when body geometry matters

A tag is an address, not a visual payload. Conversation history and previous generated images are not identity sources.

If the ACTIVE identity master is actually available, declare `IDENTITY ANCHOR READY`.

If it is absent, unresolved, disputed, rejected, or only referenced by chat history/tag, declare `IDENTITY ANCHOR MISSING` and stop identity-bearing generation until it is restored.

## 1. Natural-Language Reference Resolution
The user is not required to write REF syntax or role labels.

Resolve roles automatically from the user's current wording and attached images.

Examples:

```text
"图1锁脸 / 面部特征为图1"
=> image 1 | IDENTITY ONLY | CRITICAL

"图2作为身体三视图 / 保持图2体型"
=> image 2 | BODY ONLY | HIGH

"图3只参考衣服 / 换图3工装"
=> image 3 | WARDROBE ONLY | NORMAL

"只参考这个动作"
=> POSE ONLY | NORMAL

"只参考这个环境"
=> SCENE ONLY | NORMAL
```

When the intended roles are clear, infer them and continue. Ask the user only when identity authority or another required role is genuinely ambiguous.

Do not ask the user to restate internal control syntax such as `REF01 = ...`.

## 2. Internal Reference Map
Build the execution map automatically after resolving roles.

Example:

```text
REF01 = attached image 1 | IDENTITY ONLY | CRITICAL
REF02 = attached image 2 | BODY ONLY | HIGH
REF03 = attached image 3 | WARDROBE ONLY | NORMAL
```

Allowed control roles:
- `IDENTITY ONLY` — face identity and age impression
- `BODY ONLY` — height impression, body geometry, proportions, silhouette
- `WARDROBE ONLY` — clothing, PPE, explicitly requested accessories, footwear
- `POSE ONLY` — pose, hands, action, prop interaction
- `SCENE ONLY` — environment, camera geometry, lighting, perspective

Every active reference gets exactly one control role for the operation. A non-identity reference cannot redefine identity.

During eligible FACE_REPAIR, add the matching approved FACE_CROP_PACK view(s) as `IDENTITY ONLY | CRITICAL`. They support, not replace, the ACTIVE Identity Master.

## 3. Reference Contamination Firewall
Role assignment is not only descriptive; it is an exclusion rule.

### WARDROBE ONLY
Read:
- garment cut and fit
- color and paneling
- reflective strips
- pockets, closures, patches/logos where permitted
- PPE style
- footwear
- accessories explicitly requested by the user

Ignore by default:
- the reference person's face
- age impression
- glasses unless explicitly requested
- hairstyle/hairline
- head/skull shape
- facial hair
- skin identity cues
- ethnicity/identity cues
- unrelated pose/body identity

If a workwear reference contains a different person, that person's face must not influence the target identity.

### BODY ONLY
Read body geometry and proportions. Ignore visible facial identity, facial age, and hairstyle. When an IDENTITY ONLY reference exists, the target face comes from it.

### POSE ONLY
Read pose, hands, weight distribution, action, and prop interaction. Ignore face identity, age, wardrobe identity, and unrelated scene identity.

### SCENE ONLY
Read environment, camera geometry, perspective, light, atmosphere, and depth. Ignore identities of people visible in the scene.

## 4. Operation Classification
Classify the user's requested change before choosing an image path.

### `APPEARANCE_EDIT`
Use when the user says things like:
- 换衣 / 换工装 / 换穿搭
- 保持人物不变
- 脸不要变
- 图1锁脸，把图3衣服换到图2人物上

For `APPEARANCE_EDIT`:
1. preserve IDENTITY ONLY authority
2. preserve BODY ONLY geometry when provided
3. change only the requested wardrobe/PPE layer
4. prefer Edit-first
5. never reinterpret the task as "create a new person who resembles the references"

### `POSE_EDIT`, `SCENE_EDIT`, `COMPOSITE`, `FRESH_GENERATION`
Use the narrowest operation that satisfies the request. Fresh generation is a fallback, not the default for a simple layer replacement.

## 5. Generation Preflight
Before any identity-bearing generation/edit, verify:
- active skill binding is still `hermes-creative-digital-human`
- task object/character is resolved
- requested operation type is resolved
- required upstream gates are satisfied for the current workflow step
- ACTIVE Identity Anchor is resolved
- required identity master image is actually attached/selected
- BODY master is attached when body geometry matters
- internal Reference Map is complete
- every reference has one control role
- contamination firewall exclusions are active
- edit/generate strategy is intentional

If all pass: `PREFLIGHT PASS` and proceed.

If any fail: `PREFLIGHT BLOCKED`, identify the missing prerequisite, restore it, and do not perform identity-bearing generation.

## 6. Capability Check
Classify the active image path:
- Tier A — identity-aware conditioning
- Tier B — multi-reference but not identity-specific
- Tier C — ordinary generation

Tier B/C output must not be described as guaranteed face lock.

## 7. Edit-first / Generate-second
When a valid identity/body-bearing base image exists and the active tool supports a reference-preserving edit, prefer Edit-first and modify only the requested layer.

Use Generate-second only when the required view, composition, pose, prop geometry, or scene cannot be achieved by preserving edit.

### Runtime truth
Do not infer success from prompt wording. If the runtime cannot confirm a preserving edit path, or metadata shows no edit operation / a null edit operation, classify the result as a fresh candidate generation. Apply the stricter Identity Gate and do not claim that the person was preserved by editing.

Never use Edit-first from a drifted/rejected candidate except for narrowly eligible FACE_REPAIR, where the candidate is only a composition carrier.

## 8. Shot / Geometry Design
Analyze only what the operation requires: camera angle/height, perspective, focal-length impression, subject scale, placement, pose, hand geometry, props, ground contact, light direction, color temperature, depth of field, and integration.

For complex actions or equipment, solve pose/prop geometry with a stand-in before identity integration when practical.

## 9. Identity Integration
Identity comes from the explicitly re-attached ACTIVE approved IDENTITY MASTER and matching FACE_CROP_PACK when used.

BODY/WARDROBE/POSE/SCENE references guide only their declared layers.

Do not use the most recent L3 output as the next shot's main identity reference.

## 10. Identity Gate / Candidate Hard Stop
Verify same person and same age impression.

If identity fails:
- mark candidate `REJECTED` for identity/reference reuse
- exclude it from automatic reference selection in subsequent attempts
- do not advance `current_step`
- run Final Image Triage
- route recovery through `improve-output.md`

The failed image may remain only as a temporary composition carrier if `Final Image Triage = FACE_REPAIR` and eligibility passes.

A recently generated wrong face must never be reused merely because it is the latest image in the chat.

## 11. Scene / Realism Integration
For an identity-valid candidate, refine perspective/scale, ground contact, shadows, color, depth of field, sharpness/noise, skin texture, rain/mud/contact effects, and edges.

Do not use scene polish to hide an identity failure.

## 12. Final Image Triage
Classify exactly one:
- `APPROVED` — identity plus relevant composition/body/pose/prop/scene layers pass
- `FACE_REPAIR` — shot structure is worth preserving and only localized face identity/age drift remains
- `REGENERATE` — head angle, body, pose, prop, composition, scene geometry, or other structural conflict makes local face repair unsafe

### FACE_REPAIR eligibility
All of these must already be acceptable:
- composition/placement
- body/pose
- prop interaction
- scene perspective/contact/major lighting
- head angle and head size
- neck connection and gross skull orientation

If not, use `REGENERATE`.

## 13. FACE_REPAIR
Use rejected candidate only as base composition, never as identity source.

Required:
- ACTIVE approved IDENTITY MASTER
- matching approved FACE_CROP_PACK view(s)

Preserve non-face layers. Correct face shape, eye structure/spacing, brows, nose, mouth, jaw/chin, visible hairline, and age impression.

After repair:
1. run Identity Gate again
2. verify preserved layers did not regress
3. run Final Image Triage again

A repaired result may become `CONTENT_APPROVED` after human approval but does not automatically become an Identity Master or upstream reference.

## 14. No Generation Chaining
Forbidden:

`SOURCE -> generated A -> generated B -> generated C`

Required:

`SOURCE / IDENTITY_MASTER -> candidate A`
`SOURCE / IDENTITY_MASTER -> candidate B`
`SOURCE / IDENTITY_MASTER -> candidate C`

A failed output is removed from the next attempt's identity/reference set. FACE_REPAIR is the only narrow exception and uses the failed output only as composition carrier.

## 15. Output State / Checkpoint
New output begins as `CONTENT_CANDIDATE`.

Human-approved output may become `CONTENT_APPROVED`.

Identity-failed output becomes `CONTENT_REJECTED` for reference reuse.

After every state-changing action, checkpoint approval/rejection, triage result, gate result, step transition, master-version change, or next action.

For batch production, bootstrap every identity-critical shot from ACTIVE approved masters rather than chaining from prior content.

## Common wardrobe-change example
User says:

```text
按 Hermes 路由。图1锁定面部身份，图2作为身体三视图，把图3工装换到图2人物上。
```

Resolve automatically:

```text
operation = APPEARANCE_EDIT
REF01 = 图1 | IDENTITY ONLY | CRITICAL
REF02 = 图2 | BODY ONLY | HIGH
REF03 = 图3 | WARDROBE ONLY | NORMAL
firewall = ignore REF03 face/age/glasses/hair/head identity
strategy = EDIT-FIRST when supported
```

The user does not need to type the internal map or firewall text.

Goal: preserve the approved person first, isolate reference roles automatically, block cross-reference identity contamination, and only regenerate when a preserving edit cannot satisfy the shot.