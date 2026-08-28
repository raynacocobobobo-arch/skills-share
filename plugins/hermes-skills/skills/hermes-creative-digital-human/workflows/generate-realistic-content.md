# Generate Realistic Content Workflow V2.1

## Preconditions
Required:
- L0 SOURCE
- approved IDENTITY MASTER
- Identity Gate = PASS
- approved BODY MASTER when full body matters

Optional presentation assets: APPEARANCE, POSE/PROP, SCENE.

## 0. Session Start / Explicit Master Re-attachment
Before every new production chat and every identity-critical generation, explicitly re-attach the latest approved `IDENTITY_MASTER`. Re-attach the approved `BODY_MASTER` when full-body geometry matters.

Do not rely on a long chat, a previous generation, or instructions such as “same person as before” to recover identity. Project/chat history may carry task context, but conversation history is not an identity source.

Bind each reference to **one declared role** before generation:

- `IDENTITY ONLY` — face identity and age impression
- `BODY ONLY` — body geometry and proportions
- `WARDROBE ONLY` — clothing, PPE, accessories, footwear
- `POSE ONLY` — pose, hands, action, prop interaction
- `SCENE ONLY` — environment, camera geometry, lighting, perspective

If a reference has no clear role, resolve its role or remove it. A BODY/WARDROBE/POSE/SCENE reference must not redefine identity.

## 1. Capability Check
Classify the active image path as Tier A identity-aware, Tier B multi-reference, or Tier C ordinary generation. Tier B/C must not be described as guaranteed face lock.

## 2. Edit-first / Generate-second Decision
When a valid approved identity-bearing image and a reference-preserving edit path are available, prefer Edit-first: preserve the approved person and change only the requested layer.

Use Generate-second when edit constraints cannot solve the required composition, pose, prop geometry, view change, or scene transformation. A generated candidate still starts from Explicit Master Re-attachment and must pass Identity Gate before downstream work.

Never use Edit-first as permission to edit from a drifted or rejected candidate.

## 3. Shot Design
Analyze camera angle/height, perspective, focal-length impression, subject scale, placement, light direction, color temperature, depth of field, and noise/sharpness.

## 4. Pose / Prop Prototype
If action or equipment is complex, solve geometry before final identity integration. Use a stand-in if needed to validate pose, hands, weight distribution, camera/monopod/tool geometry, and interaction with the environment.

## 5. Identity Integration
Use the explicitly re-attached approved IDENTITY MASTER as identity authority. SOURCE may support genuine identity evidence where needed. BODY/APPEARANCE/POSE/SCENE assets guide only their declared layers and must not redefine the face.

Do not use previous L3 content as the main identity reference for the next shot.

## 6. Identity Gate / Candidate Hard Stop
Before polishing realism, verify same person and same age impression.

If identity fails:
- mark the current candidate `REJECTED`
- the failed candidate must not continue downstream
- remove it from future identity/reference inputs
- route recovery into `improve-output.md`
- re-attach the latest approved IDENTITY MASTER before the next attempt

This Candidate Hard Stop blocks contamination of later stages; it does not terminate the whole production workflow.

## 7. Scene Integration
Only after identity passes, optimize perspective/scale, ground contact, lighting/shadow, color, depth of field, sharpness/noise, skin texture, rain/mud/contact effects, and edge integration.

## 8. Output State
New scene output begins as `CONTENT_CANDIDATE`. Human-approved output may become `CONTENT_APPROVED`. Failed identity becomes `CONTENT_REJECTED` and must never feed the identity reference pool.

For batch production, start each identity-critical shot from the explicit approved masters rather than chaining from the prior content image.

Goal: preserve the approved person first, recover intelligently when a candidate drifts, then make the approved person look naturally photographed in the scene.
