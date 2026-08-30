# Generation Segment Rules

A Shot is a narrative/editing unit. A Generation Segment is one downstream model call. A segment may contain one or more adjacent compatible shots, but its shot IDs remain visible so generated media can be edited and reviewed against the Storyboard.

## Required contract

Each segment contains:

- `segment_id` and ordered `shot_ids`;
- `target_duration_sec`;
- `generation_mode` and exact `target_model`/version when known;
- bound `references` with asset ID and role;
- `continuity_priority` and `motion_priority`;
- scene snapshot, fixed continuity facts, compatible visible actions, ending state, and camera behavior;
- model-ready `prompt` and `not_constraints`;
- readiness `status` and `blocked_reasons`.

## Grouping

Group adjacent shots only when they share scene geography, character identity/costume, reference set, temporal continuity, and a model-safe action chain. Do not group when:

- identity or prop continuity needs separate locking;
- the spatial axis changes without a controlled transition;
- actions compete or require several independent outcomes;
- a shot needs a different start/end frame or generation mode;
- one failed result would make a targeted retake unnecessarily broad.

Prefer a representative identity/geography-critical segment first. Accept its reusable anchors before expanding similar segments.

## Generation mode routing

Allowed values:

- `first_frame`: stable dialogue, reaction, or controlled motion that begins from an approved composition;
- `first_last_frame`: an explicit A-to-B visual state where both boundary frames must be locked;
- `reference_images`: recurring or multi-character identity, costume, scene, or prop continuity is critical;
- `reference_video`: source motion/camera transformation when the selected model and rights permit it;
- `text_to_video`: non-identity-critical establishing, atmospheric, or spectacle material.

Choose the smallest reference set that controls the risk. Every binding names its role, such as `character_identity`, `scene`, `prop`, `first_frame`, `last_frame`, or `motion`.

## Readiness

All required shots must be valid, and all required assets/keyframes must be approved and accessible. Otherwise mark the affected segment `BLOCKED` with asset IDs and reasons. Do not emit a generation-success or take record before an executor returns real output.

The Seedance-oriented V1 planning default is 4–15 seconds per segment. This is not a universal model limit: re-check the selected version/provider and record an approved override when its supported duration differs.
