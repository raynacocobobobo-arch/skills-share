# Shots to Seedance

Stage order: `valid shots -> asset/keyframe readiness -> segment grouping -> generation-mode selection -> Seedance prompt pack -> READY/BLOCKED`

## Inputs

- validated Shot Specs and Continuity State;
- asset inventory with approved/missing state;
- exact downstream model/provider capability when available.

Read [Generation Segment rules](../references/generation-segment-rules.md) and [Seedance rules](../references/seedance-rules.md). Use [production-pack.json](../templates/production-pack.json).

## Procedure

1. **Valid shots:** accept only Shot Specs that passed continuity validation.
2. **Asset/keyframe readiness:** bind stable IDs and roles. Missing/rejected required assets block only affected segments.
3. **Segment grouping:** combine adjacent shots only when geography, identity, reference set, action, transition, and retake scope are compatible.
4. **Generation-mode selection:** choose `first_frame`, `first_last_frame`, `reference_images`, `reference_video`, or `text_to_video` from the segment's control risk.
5. **Seedance prompt pack:** record the capability check, scene snapshot, references, fixed facts, visible action, ending state, camera/sound policy, prompt, and NOT constraints.
6. **Status:** set the Production Pack and each segment honestly to `READY`, `BLOCKED`, or `NEEDS_REVIEW`.

The 4–15 second segment range is a Seedance 2.0-oriented default. Re-check the exact selected model/version before execution and record any verified override. Never claim a take or media file exists before a downstream executor returns it.

## Outputs

- Production Pack with asset/keyframe status;
- ordered Generation Segments and prompt blocks;
- blocked reasons or a `READY` downstream handoff;
- empty generation/take log ready for executor results.
