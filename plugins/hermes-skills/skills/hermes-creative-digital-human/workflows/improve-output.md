# Improve Output Workflow V2.4

## Diagnose the Failed Layer
Identity: wrong person, face drift, age drift, structural facial changes.

Body: wrong mass/proportions or unstable synthetic completion.

Pose/Prop: unnatural anatomy, hand placement, load bearing, camera/monopod/tool geometry.

Reality/Scene: perspective, scale, contact, lighting, color, depth, texture.

## Final Image Triage
After an identity-bearing content candidate is generated and the overall shot has been reviewed, route it to exactly one outcome:

- `APPROVED` — identity and the usable shot layers pass.
- `FACE_REPAIR` — composition, body, pose, prop interaction, scene, and head geometry are worth preserving, but facial identity/age impression has a localized correctable drift.
- `REGENERATE` — the failure is broader than the face-only layer, or the head/pose/prop/scene geometry is not a safe base for local identity repair.

Do not use `FACE_REPAIR` merely because the face is wrong. First verify that the rest of the image is genuinely worth preserving.

## Face Repair Eligibility
`FACE_REPAIR` is a recovery path, not the default generation path.

It is eligible only when all relevant non-face layers already pass well enough to preserve:
- composition and subject placement
- body proportions needed by the shot
- pose and anatomy
- prop / camera / monopod / tool geometry
- scene perspective, contact, and major lighting direction
- head angle, head size, neck connection, and gross skull orientation
- expression direction is compatible with the intended identity repair

Use `REGENERATE` instead when the head angle is wrong, head/body relationship is structurally wrong, pose or prop geometry is wrong, scene geometry is wrong, or the facial failure is entangled with a larger anatomical/compositional failure.

## FACE_REPAIR Procedure
When eligible, preserve the good candidate as the base composition and repair only the identity-bearing face region as narrowly as the active tool allows.

Required identity inputs:
1. the ACTIVE approved `IDENTITY_MASTER`
2. the approved `FACE_CROP_PACK` views that best match the target head angle

The repair should preserve composition, body, pose, wardrobe, prop geometry, scene, and major lighting structure. Correct only identity-relevant facial structure such as face shape, eye shape/spacing, brows, nose, mouth, jaw/chin, hairline where visible, and age impression.

The candidate being repaired is a composition carrier only. It does not gain identity authority because its pose or scene is good.

After repair, run Identity Gate again and then re-run Final Image Triage:
- PASS and overall shot still passes → `APPROVED`
- localized face drift remains but another materially different repair strategy is available → remain in `FACE_REPAIR` within the Retry Budget
- repair damages geometry/composition or the failure is no longer face-only → `REGENERATE`

A repaired output may become `CONTENT_APPROVED` after human approval, but it **must not automatically become** an Identity Master, `IDENTITY_MASTER`, or other upstream identity authority. Upstream identity authority changes require the normal explicit master/version approval process.

## Candidate Hard Stop
When an identity-bearing candidate fails Identity Gate, that candidate must not continue downstream into wardrobe, scene polish, action continuity, batch production, or future reference inputs unless it is explicitly routed into an eligible `FACE_REPAIR` operation as a composition carrier.

Candidate Hard Stop applies to the failed asset lineage only. It does not terminate the whole production workflow; recovery resumes from the latest approved upstream master or the narrowly scoped Face Repair path defined above.

## Identity Recovery Loop
Identity failure rejects the current candidate as an identity authority; it does **not** terminate the whole production workflow.

Required recovery:
1. mark failed output `REJECTED` for identity/reference reuse
2. remove it from every future identity/reference input
3. run Final Image Triage to decide `FACE_REPAIR` versus `REGENERATE`
4. for `REGENERATE`, return first to the latest approved IDENTITY MASTER
5. return to SOURCE only if the approved master itself is invalid, disputed, or unavailable
6. diagnose the failed variable: identity conditioning, view angle, pose/prop complexity, scene complexity, or conflicting references
7. change strategy before retrying
8. explicitly re-attach the latest approved IDENTITY MASTER; re-attach BODY MASTER too when body geometry matters
9. generate a fresh candidate from the approved upstream anchor rather than from the failed image or chat history, unless an eligible `FACE_REPAIR` is preserving the already-good non-face layers
10. run Identity Gate again
11. PASS → resume downstream work; FAIL → continue the workflow in recovery mode within the Retry Budget

Forbidden:
- failed candidate → next candidate as identity reference
- previous chat history → assumed identity source
- repeated prompt emphasis such as "same exact face" without changing strategy
- promoting a scene/style output to identity master
- promoting a repaired content output to Identity Master without explicit master approval/versioning
- using shared helmet, glasses, clothing, age, or ethnicity as evidence that identity passed

## Retry Budget
A retry is useful only when at least one causal variable changes. Examples: isolate identity from scene, simplify pose, remove conflicting references, switch reference angle, switch FACE_CROP_PACK angle, use a narrower edit/repair mask, or move to a stronger identity-aware path.

Default recovery budget: up to 2 strategy-changing retries for the same failure mode. This is not an image-count quota; materially different failure modes may start a new diagnosis. Do not spend the budget on identical prompt reruns.

## Tool Escalation
When the same identity failure remains after the Retry Budget:
1. stop repeating the same generation strategy
2. state what failed and which variables were already changed
3. change strategy or escalate to a stronger identity-aware tool/path when available
4. ask for a stronger SOURCE view only when missing evidence is actually the bottleneck
5. if no stronger path or evidence exists, report the capability limit instead of pretending another identical retry will solve it

Tool escalation is a production decision, not a failure of the entire digital-human project.

## Pose / Prop Recovery
If identity is correct but action/equipment is wrong, preserve and explicitly re-attach the approved identity anchor, then prototype the pose/prop separately before reintegration. This is `REGENERATE` / pose-prototype territory, not `FACE_REPAIR`.

## Reality Recovery
If identity/body/pose are correct, adjust one scene layer at a time: perspective/scale → contact → lighting/shadow → color → depth/sharpness/noise → skin/edge/weather integration.

## Decision Rule
- overall shot passes including identity → `APPROVED`
- composition/body/pose/prop/scene/head geometry pass, only localized face identity drifts → `FACE_REPAIR` using approved `IDENTITY_MASTER + FACE_CROP_PACK`
- head angle, pose, prop, body, composition, or scene geometry is wrong → `REGENERATE`
- identity wrong, master valid, face repair not eligible → Candidate Hard Stop → latest approved IDENTITY MASTER → explicit re-attachment → Recovery Loop
- identity master itself wrong → SOURCE → rebuild Identity Master
- identity right, body wrong → BODY MASTER rebuild
- identity/body right, pose/prop wrong → pose prototype
- identity/body/pose right, scene wrong → scene integration only

Goal: preserve good downstream work when the failure is truly face-only, repair the failed layer without contaminating identity lineage, and avoid unnecessary full-image regeneration.
