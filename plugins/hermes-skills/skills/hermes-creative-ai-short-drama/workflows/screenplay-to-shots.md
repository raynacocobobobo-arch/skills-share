# Screenplay to Shots

Stage order: `screenplay -> asset inventory -> continuity compile -> shot breakdown -> Shot Spec validation`

## Inputs

- approved Episode Card and screenplay;
- latest Series Bible/Entity Registry;
- inherited canonical state and any approved asset records.

Read [continuity rules](../references/continuity-rules.md) and [storyboard rules](../references/storyboard-rules.md). Use [continuity-state.json](../templates/continuity-state.json) and [storyboard.json](../templates/storyboard.json) as shapes, not fixed story content.

## Procedure

1. **Screenplay:** identify visible actions, dialogue, scene end states, and production-critical facts.
2. **Asset inventory:** list required character, location, costume, prop/clue, UI-overlay, and keyframe IDs. Mark each `approved`, `needs_regeneration`, `missing`, or `TBD`.
3. **Continuity compile:** declare scene geography/axis, character state, relevant costume/injury, prop/clue ownership/reveal, action causality, and transitions.
4. **Shot breakdown:** create the fewest readable Shot Specs; one visible action per shot. Carry each `end_state` into the next `start_state`.
5. **Validate:** reject missing start/end/connection fields, unrelated multi-actions, unknown required assets, invalid entity IDs, or unexplained axis reversals.

Unknown required assets do not prevent planning, but they make the affected shot `BLOCKED`. Contradictory inherited state makes it `NEEDS_REVIEW`.

## Outputs

- asset inventory with readiness states;
- Continuity State;
- validated Storyboard/Shot Specs;
- per-shot `READY`, `BLOCKED`, or `NEEDS_REVIEW` status for `shots-to-seedance.md`.
