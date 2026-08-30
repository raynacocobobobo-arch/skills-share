# Episode Contract

Use an Episode Card to approve the narrative unit before writing screenplay prose.

## Required Episode Card

```yaml
episode_id: EP01
opening_hook: ""
dominant_turn: ""
core_conflict: ""
payoff_or_progress: ""
ending_cliffhanger: ""
state_delta: []
continuation_capsule: ""
```

Also record dependencies from the previous episode, participating entity IDs, debts/clues opened or resolved, and the target duration.

## Rules

- Exactly one `dominant_turn` changes power, information, relationship, goal, or cost.
- `payoff_or_progress` must be observable; mood alone is not progress.
- `ending_cliffhanger` must create a consequential next prediction.
- `state_delta` contains only persistent facts that occurred on screen or were established unambiguously. Draft it during writing, but approve it only after story/production review.
- `continuation_capsule` summarizes the minimum state needed to open the next episode.
- Screenplay prose is downstream of the card and may not contradict the approved Series Bible or inherited state.
- Use stable entity IDs. Do not invent a replacement character, location, prop, clue, or rule when a required dependency is unknown; mark it `TBD` and the affected downstream work `BLOCKED`.

## Screenplay output

The screenplay must name scene IDs, location IDs, participating character IDs, visible actions, dialogue, and each scene's end-state change. Internal thoughts must become visible behavior, dialogue, or an explicitly approved voice-over.

After review, publish:

1. approved Episode Card;
2. screenplay;
3. approved State Delta;
4. Continuation Capsule.

Episode N+1 must be writable from the latest Series Bible plus these final two handoff artifacts. A conflict between them is `NEEDS_REVIEW`, not permission to infer a reset.
