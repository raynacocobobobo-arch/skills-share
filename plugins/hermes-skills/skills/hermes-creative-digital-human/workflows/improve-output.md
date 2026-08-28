# Improve Output Workflow V2.1

## Diagnose the Failed Layer
Identity: wrong person, face drift, age drift, structural facial changes.

Body: wrong mass/proportions or unstable synthetic completion.

Pose/Prop: unnatural anatomy, hand placement, load bearing, camera/monopod/tool geometry.

Reality/Scene: perspective, scale, contact, lighting, color, depth, texture.

## Candidate Hard Stop
When an identity-bearing candidate fails Identity Gate, that candidate must not continue downstream into wardrobe, scene polish, action continuity, batch production, or future reference inputs.

Candidate Hard Stop applies to the failed asset lineage only. It does not terminate the whole production workflow; recovery resumes from the latest approved upstream master.

## Identity Recovery Loop
Identity failure rejects the current candidate; it does **not** terminate the whole production workflow.

Required recovery:
1. mark failed output `REJECTED`
2. remove it from every identity/reference input
3. return first to the latest approved IDENTITY MASTER
4. return to SOURCE only if the approved master itself is invalid, disputed, or unavailable
5. diagnose the failed variable: identity conditioning, view angle, pose/prop complexity, scene complexity, or conflicting references
6. change strategy before retrying
7. explicitly re-attach the latest approved IDENTITY MASTER; re-attach BODY MASTER too when body geometry matters
8. generate a fresh candidate from the approved upstream anchor rather than from the failed image or chat history
9. run Identity Gate again
10. PASS → resume downstream work; FAIL → continue the workflow in recovery mode within the Retry Budget

Forbidden:
- failed candidate → next candidate as identity reference
- previous chat history → assumed identity source
- repeated prompt emphasis such as "same exact face" without changing strategy
- promoting a scene/style output to identity master
- using shared helmet, glasses, clothing, age, or ethnicity as evidence that identity passed

## Retry Budget
A retry is useful only when at least one causal variable changes. Examples: isolate identity from scene, simplify pose, remove conflicting references, switch reference angle, or move to a stronger identity-aware path.

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
If identity is correct but action/equipment is wrong, preserve and explicitly re-attach the approved identity anchor, then prototype the pose/prop separately before reintegration.

## Reality Recovery
If identity/body/pose are correct, adjust one scene layer at a time: perspective/scale → contact → lighting/shadow → color → depth/sharpness/noise → skin/edge/weather integration.

## Decision Rule
- identity wrong, master valid → Candidate Hard Stop → latest approved IDENTITY MASTER → explicit re-attachment → Recovery Loop
- identity master itself wrong → SOURCE → rebuild Identity Master
- identity right, body wrong → BODY MASTER rebuild
- identity/body right, pose/prop wrong → pose prototype
- identity/body/pose right, scene wrong → scene integration only

Goal: repair the failed layer, preserve good upstream assets, and keep the workflow moving without contaminating identity lineage.
