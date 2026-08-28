# Improve Output Workflow V2

## Diagnose the Failed Layer
Identity: wrong person, face drift, age drift, structural facial changes.

Body: wrong mass/proportions or unstable synthetic completion.

Pose/Prop: unnatural anatomy, hand placement, load bearing, camera/monopod/tool geometry.

Reality/Scene: perspective, scale, contact, lighting, color, depth, texture.

## Identity Drift = Hard Stop
If identity is wrong, do not continue normal refinement and do not generate "one more" from the failed image.

Required recovery:
1. mark failed output `REJECTED`
2. remove it from every identity/reference input
3. identify latest approved SOURCE / IDENTITY MASTER
4. return to that upstream anchor
5. reduce complexity to a neutral identity test when necessary
6. run Identity Gate again
7. resume downstream work only after PASS

Forbidden:
- bad output → next generation
- repeated prompt emphasis such as "same exact face" as the only recovery method
- promoting a scene/style output to identity master
- using shared helmet, glasses, clothing, age, or ethnicity as evidence that identity passed

## Tool Limitation Escalation
If Tier B/C repeatedly produces a different person, stop retries and state that the active generation path lacks reliable identity conditioning. Recommend an identity-aware Tier A path rather than pretending prompt changes will solve it.

## Pose / Prop Recovery
If identity is correct but action/equipment is wrong, freeze identity and scene assumptions where possible and prototype the pose/prop separately before reintegration.

## Reality Recovery
If identity/body/pose are correct, adjust one scene layer at a time: perspective/scale → contact → lighting/shadow → color → depth/sharpness/noise → skin/edge/weather integration.

## Decision Rule
- identity wrong → SOURCE / IDENTITY MASTER
- identity right, body wrong → BODY MASTER rebuild
- identity/body right, pose/prop wrong → pose prototype
- identity/body/pose right, scene wrong → scene integration only

Goal: repair the failed layer without contaminating upstream identity assets.
