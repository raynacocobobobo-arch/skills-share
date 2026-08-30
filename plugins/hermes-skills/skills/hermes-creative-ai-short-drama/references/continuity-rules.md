# Continuity Rules

Continuity State records only persistent facts needed to stage, generate, edit, or inherit the story. It is a production ledger, not a catalog of decorative description.

## Required state

- `characters`: position, facing/screen direction, current goal, knowledge, relationship, and only relevant costume/injury changes;
- `locations`: stable geography, entrances/exits, screen axis, and established camera-side rules;
- `props_and_clues`: owner/handler, physical location, condition, visibility, and reveal state;
- `causality`: action or information that must occur before a later action can make sense;
- `time`: only deadlines, elapsed time, or time-of-day facts that constrain production;
- `transition`: the visible or motivated connection into the next scene/shot.

Use stable entity IDs from the Series Bible. Represent unknown required facts as `TBD`, never as a confident invention.

## Compile procedure

1. Load the approved Series Bible, Episode Card, previous State Delta, and Continuation Capsule.
2. Extract only facts visible or established in the screenplay.
3. For each scene, declare the spatial axis, entrances/exits, character positions, and prop/clue placement before breaking shots.
4. Carry each accepted shot's `end_state` into the next shot's `start_state`.
5. Record the final production-confirmed changes as the candidate episode State Delta.

## Screen direction and geography

Keep a stable axis while characters share a scene. A character established screen-left does not jump screen-right without one of:

- visible movement across the frame;
- a neutral/re-establishing shot that resets the axis;
- an explicitly motivated viewpoint reversal recorded in state.

Doors, windows, counters, and recurring props must keep their declared relationships. If geography is not established, define it conservatively before shot design.

## Prop, clue, and knowledge state

Track who owns, holds, sees, or knows a critical item or fact. Reveal state uses `hidden`, `visible_to_audience`, `known_to:<character_id>`, or `public`. A clue cannot be acted upon before the relevant character learns it. A prop cannot disappear, reset, change hands, or change condition without a visible action or approved transition.

## Relevance filter

Persist a fact only if changing it would break identity, causality, geography, a later shot, or episode inheritance. Do not track incidental colors, gestures, background objects, or wardrobe detail unless the story or locked asset depends on them.

## Blocking conditions

Mark the affected shot/segment `BLOCKED` when a required character, location, prop, clue, or keyframe has no known identity/state or approved asset. Mark a contradiction `NEEDS_REVIEW`. Do not fabricate a resolution to keep the pipeline moving.
