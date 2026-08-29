# Generate Realistic Content Workflow V2.4

## Preconditions
Required:
- L0 SOURCE
- approved IDENTITY MASTER
- Identity Gate = PASS
- approved BODY MASTER when full body matters
- per-character Identity Anchor Card
- current Digital Human Session State

Optional identity-support asset: approved `FACE_CROP_PACK`.

Optional presentation assets: APPEARANCE, POSE/PROP, SCENE.

## 0. Production State / Identity Session Bootstrap
Before every new production chat and every identity-critical generation, resolve the current Digital Human Session State and the character's Identity Anchor Card.

Confirm:
- active skill binding = `hermes-creative-digital-human`
- `character_id` is resolved
- `current_step` and `next_allowed_action` are known
- ACTIVE identity version is known

A tag such as `@DH001_ID_V1_FRONT` is a stable alias, not a magic lookup. Tags are stable aliases, not image payloads, and tag alone does not satisfy Explicit Master Re-attachment.

Verify that the exact approved `IDENTITY_MASTER` referenced by the ACTIVE anchor is physically attached to the current task. Re-attach the approved `BODY_MASTER` as well when full-body geometry matters.

If the exact ACTIVE master is present and its status is APPROVED, declare:

`IDENTITY ANCHOR READY`

If the master is absent, unresolved, disputed, rejected, or only mentioned by tag/history without the actual required image input, declare:

`IDENTITY ANCHOR MISSING`

Do not generate an identity-bearing candidate while the anchor is MISSING. Restore the exact approved master from the project/library/saved-reference system available in the active tool.

Do not rely on a long chat, a previous generation, or instructions such as “same person as before” to recover identity. Project/chat history may carry task context, but conversation history is not an identity source.

If the user mentions a later-stage request while the current workflow step has not passed its required gate, record that request as a deferred requirement. Do not silently skip the current step.

## Reference Map
Before generation, number every active reference. Every reference image has **one declared role**; bind each numbered reference to that one role. Use symbolic priority `CRITICAL / HIGH / NORMAL`. Do not invent numeric reference weights unless the active tool exposes a real documented weight control.

Example:

```text
REF01 = @DH001_ID_V1_FRONT
ROLE = IDENTITY ONLY
PRIORITY = CRITICAL

REF02 = @DH001_BODY_V1_FRONT
ROLE = BODY ONLY
PRIORITY = HIGH

REF03 = @DH001_WARDROBE_RIG_01
ROLE = WARDROBE ONLY
PRIORITY = NORMAL

REF04 = @POSE_PHOTOGRAPHER_MONOPOD_03
ROLE = POSE ONLY
PRIORITY = NORMAL

REF05 = @SCENE_RIG_RAIN_02
ROLE = SCENE ONLY
PRIORITY = NORMAL
```

Allowed roles:
- `IDENTITY ONLY` — face identity and age impression
- `BODY ONLY` — body geometry and proportions
- `WARDROBE ONLY` — clothing, PPE, accessories, footwear
- `POSE ONLY` — pose, hands, action, prop interaction
- `SCENE ONLY` — environment, camera geometry, lighting, perspective

If a reference has no clear role, resolve its role or remove it. A BODY/WARDROBE/POSE/SCENE reference must not redefine identity.

During an eligible `FACE_REPAIR`, add the matching approved FACE_CROP_PACK view(s) as additional `IDENTITY ONLY | CRITICAL` references. They support the ACTIVE Identity Master; they do not replace it as identity authority.

## Generation Preflight
Before any identity-bearing generation or identity-bearing edit, verify:

- active skill binding is still `hermes-creative-digital-human`
- requested action is allowed by `current_step` / `next_allowed_action`
- required upstream gates are PASS
- ACTIVE Identity Anchor is resolved
- required identity master image is actually attached
- BODY master is attached when body geometry matters
- Reference Map is complete and role-bound

If all required checks pass, declare `PREFLIGHT PASS` and continue.

If any required check fails, declare `PREFLIGHT BLOCKED`, name the missing/failed prerequisite, restore it, and update the Session State if needed. **Do not execute an identity-bearing generation** while preflight is blocked.

A non-identity stand-in or pose/prop prototype may proceed only when the current workflow step explicitly allows it and it must never be promoted into identity authority.

## 1. Capability Check
Classify the active image path as Tier A identity-aware, Tier B multi-reference, or Tier C ordinary generation. Tier B/C must not be described as guaranteed face lock.

## 2. Edit-first / Generate-second Decision
When a valid approved identity-bearing image and a reference-preserving edit path are available, prefer Edit-first: preserve the approved person and change only the requested layer.

Use Generate-second when edit constraints cannot solve the required composition, pose, prop geometry, view change, or scene transformation. A generated candidate still starts from an `IDENTITY ANCHOR READY` + `PREFLIGHT PASS` state and must pass Identity Gate before downstream approval.

Never use Edit-first as permission to edit from a drifted or rejected candidate, except for the narrowly scoped eligible `FACE_REPAIR` path below where the candidate is used only as a composition carrier and never as identity authority.

## 3. Shot Design
Analyze camera angle/height, perspective, focal-length impression, subject scale, placement, light direction, color temperature, depth of field, and noise/sharpness.

## 4. Pose / Prop Prototype
If action or equipment is complex, solve geometry before final identity integration. Use a stand-in if needed to validate pose, hands, weight distribution, camera/monopod/tool geometry, and interaction with the environment.

## 5. Identity Integration
Use REF01 / the explicitly re-attached approved IDENTITY MASTER as identity authority. SOURCE may support genuine identity evidence where needed. BODY/APPEARANCE/POSE/SCENE assets guide only their declared layers and must not redefine the face.

Do not use previous L3 content as the main identity reference for the next shot.

## 6. Identity Gate / Candidate Hard Stop
Verify same person and same age impression.

If identity fails:
- mark the current candidate `REJECTED` for identity/reference reuse
- remove it from future identity/reference inputs
- route recovery into `improve-output.md`
- run `Final Image Triage` before deciding whether the whole image must be discarded
- update the Digital Human Session State; do not advance `current_step`

The failed candidate must never become identity authority. It may remain only as a temporary composition carrier when `Final Image Triage = FACE_REPAIR` and Face Repair Eligibility passes.

This Candidate Hard Stop blocks contamination of later identity lineage; it does not require throwing away good composition/pose/scene work when the failure is genuinely face-only.

## 7. Scene Integration
For candidates whose identity is usable enough to continue the current shot path, optimize perspective/scale, ground contact, lighting/shadow, color, depth of field, sharpness/noise, skin texture, rain/mud/contact effects, and edge integration.

Do not use scene polish to hide an identity failure. Final approval still requires Identity Gate PASS after any repair.

## 8. Final Image Triage
After the candidate's overall shot layers are visible, classify exactly one outcome:

- `APPROVED` — identity plus composition/body/pose/prop/scene pass.
- `FACE_REPAIR` — the shot is worth preserving and only localized facial identity/age drift remains.
- `REGENERATE` — the failure involves head angle, body, pose, prop, composition, scene geometry, or any larger structural conflict that makes local face repair unsafe.

### Face Repair Eligibility
Before choosing `FACE_REPAIR`, confirm:
- composition and subject placement are good enough to preserve
- body and pose are good enough to preserve
- prop/camera/monopod/tool interaction is good enough to preserve
- scene perspective/contact/major lighting are good enough to preserve
- head angle, head size, neck connection, and gross skull orientation are compatible with the intended face
- the failure is localized to face identity, facial structure, or age impression

If any of those structural conditions fail, choose `REGENERATE`.

## 9. FACE_REPAIR Pass
When eligible, use the current candidate only as the base composition. It is not an identity source.

Required repair inputs:
- ACTIVE approved `IDENTITY_MASTER`
- matching approved `FACE_CROP_PACK` view(s), such as `@DH001_FACE_FRONT_CLOSE`, `@DH001_FACE_L45_CLOSE`, or `@DH001_FACE_R45_CLOSE`

Prefer the narrowest reference-preserving edit supported by the active tool. Preserve composition, body, pose, wardrobe, prop geometry, scene, and major lighting structure. Correct only the face-identity layer: face shape, eye structure/spacing, brows, nose, mouth, jaw/chin, visible hairline, and age impression.

After the edit:
1. run Identity Gate again
2. verify the preserved non-face layers did not regress
3. run Final Image Triage again

A repaired output may become `CONTENT_APPROVED` after human approval, but it **must not automatically become** an Identity Master or `IDENTITY_MASTER`. It must never enter upstream identity authority unless the user explicitly approves a new master version through the normal Identity Master lifecycle.

## 10. Output State / State Checkpoint
New scene output begins as `CONTENT_CANDIDATE`. Human-approved output may become `CONTENT_APPROVED`. Failed identity becomes `CONTENT_REJECTED` for identity/reference reuse and must never feed the identity reference pool.

An eligible FACE_REPAIR candidate may remain temporarily available only as a composition carrier until repair completes; its identity is still rejected.

After every state-changing action, checkpoint the Digital Human Session State: approval/rejection, triage result, gate result, step completion, step transition, master-version change, or next-action change.

For batch production, bootstrap each identity-critical shot from the ACTIVE anchor and explicit approved masters rather than chaining from the prior content image.

Goal: preserve the approved person first, preserve good composition/pose/scene work when the failure is truly face-only, and use full regeneration only when the broader image structure actually requires it.
