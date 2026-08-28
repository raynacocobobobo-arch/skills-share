# Improve Output Workflow

## First Diagnose the Failure Layer

Identity:
- face drift
- inconsistent person
- age drift
- style reference changing facial structure

Body:
- wrong mass / proportions
- synthetic completion becoming inconsistent

Reality:
- pasted feeling
- wrong lighting / color / depth

Composition:
- wrong scale
- wrong perspective / ground contact

## Identity Drift Recovery

If identity drift is present, do not continue normal refinement.

Required recovery:
1. stop downstream generation
2. identify the last approved SOURCE / MASTER
3. demote drifting outputs to L2 DERIVATIVE or L3 CONTENT
4. remove those drifting outputs from identity-reference inputs
5. regenerate directly from SOURCE / approved MASTER
6. run face/body QC again

Forbidden recovery:
- using the bad output as the next face reference
- repeatedly editing a drifted lifestyle image until it looks closer
- promoting a scene/style output to MASTER without explicit human approval

## Reality / Composition Recovery

If identity is correct and only realism fails, keep the approved identity anchors fixed and adjust one layer at a time:
1. perspective / scale
2. lighting / shadow
3. color temperature
4. depth of field / sharpness / noise
5. skin / edge integration

Do not optimize all variables simultaneously.

## Decision Rule

- Identity wrong → return upstream to SOURCE / MASTER.
- Identity right, body wrong → rebuild from SOURCE + approved FACE MASTER.
- Identity/body right, scene wrong → keep identity fixed and repair scene integration.

Goal: fix the failed layer without contaminating upstream identity assets.
