# Generate Realistic Content Workflow V2

## Preconditions
Required:
- L0 SOURCE
- approved IDENTITY MASTER
- Identity Gate = PASS
- approved BODY MASTER when full body matters

Optional presentation assets: APPEARANCE, POSE/PROP, SCENE.

## 1. Capability Check
Classify the active image path as Tier A identity-aware, Tier B multi-reference, or Tier C ordinary generation. Tier B/C must not be described as guaranteed face lock.

## 2. Shot Design
Analyze camera angle/height, perspective, focal-length impression, subject scale, placement, light direction, color temperature, depth of field, and noise/sharpness.

## 3. Pose / Prop Prototype
If action or equipment is complex, solve geometry before final identity integration. Use a stand-in if needed to validate pose, hands, weight distribution, camera/monopod/tool geometry, and interaction with the environment.

## 4. Identity Integration
Use SOURCE + approved IDENTITY MASTER as identity evidence. BODY/APPEARANCE/POSE/SCENE assets may guide their own layers but must not redefine the face.

Do not use previous L3 content as the main identity reference for the next shot.

## 5. Identity Gate
Before polishing realism, verify same person and same age impression. If identity fails, STOP and route to `improve-output.md`.

## 6. Scene Integration
Only after identity passes, optimize perspective/scale, ground contact, lighting/shadow, color, depth of field, sharpness/noise, skin texture, rain/mud/contact effects, and edge integration.

## 7. Output State
New scene output begins as `CONTENT_CANDIDATE`. Human-approved output may become `CONTENT_APPROVED`. Failed identity becomes `CONTENT_REJECTED` and must never feed the identity reference pool.

Goal: preserve the approved person first, then make that person look naturally photographed in the scene.
