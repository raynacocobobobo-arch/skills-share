# Episode Contract

Use an Episode Card to approve the narrative unit before writing screenplay prose. The card locks story architecture, not every downstream detail.

## Required Episode Card

```yaml
episode_id: EP01
episode_function: ""
opening_hook: ""
dominant_turn: ""
core_conflict: ""
conflict_grammar: ""
novelty_vs_prior: ""
progression:
  reveal_or_knowledge: ""
  pressure_or_public_action: ""
  relationship_or_capability: ""
callback_or_debt: ""
cost_after_solution: ""
payoff_or_progress: ""
ending_cliffhanger_or_image: ""
mechanism_status: TBD
dialogue_status: TBD
state_delta: []
continuation_capsule: ""
```

A progression field may be `N/A`; do not invent movement on every track merely to fill the form.

Also record dependencies from the previous episode, participating entity IDs, debts/clues opened or resolved, and target duration.

## Rules

- Exactly one `dominant_turn` changes power, information, relationship, goal, legitimacy, or cost.
- `episode_function` states what this episode uniquely contributes to the season.
- `conflict_grammar` describes the structural pattern, not the prop: e.g. “two valid duties collide,” not “bridge problem.”
- `novelty_vs_prior` must explain why this is not a reskin of a previous episode.
- A/B lines are allowed only when they converge on the same dominant turn, cost, or thematic action.
- `payoff_or_progress` must be observable; mood alone is not progress.
- `ending_cliffhanger_or_image` must create a consequential next prediction or change the meaning of what was just seen.
- `cost_after_solution` is mandatory when a third path appears. A clever solution may redistribute cost but may not silently delete it.
- `mechanism_status` and `dialogue_status` are separate from structural approval. Use `TBD`, `CANDIDATE`, `LOCKED_DIRECTION`, or `LOCKED` as appropriate.
- Approval is scoped. A user can approve the episode structure while rejecting all dialogue.
- `state_delta` contains only persistent facts that occurred on screen or were established unambiguously. Draft it during writing; approve it only after story/production review.
- `continuation_capsule` summarizes the minimum state needed to open the next episode.
- Screenplay prose is downstream of the card and may not contradict the approved Series Bible or inherited state.
- Use stable entity IDs. Do not invent a replacement character, location, prop, clue, or rule when a required dependency is unknown; mark it `TBD` and affected downstream work `BLOCKED` when necessary.

## Episode Function Audit

Before approving the card, compare it against earlier episodes:

| Episode | Dominant turn | Conflict grammar | Pressure type | Key device | Callback/payoff |
| --- | --- | --- | --- | --- | --- |

Reject the card if “novelty” comes only from swapping the key device while the dramatic function stays the same.

Reusing an earlier device is encouraged when its meaning changes—for example, the place once saved becomes the place later relinquished, or a solution later becomes a political problem.

## Screenplay output

The screenplay must name scene IDs, location IDs, participating character IDs, visible actions, dialogue, and each scene's end-state change. Internal thoughts must become visible behavior, dialogue, or an explicitly approved voice-over.

Apply an explanation budget:

- show consequence before explanation when possible;
- explain only facts needed to judge the current choice;
- keep research trails, engineering derivations, and thematic interpretation backstage unless the plot requires them.

After review, publish:

1. approved Episode Card;
2. screenplay;
3. approved State Delta;
4. Continuation Capsule.

Episode N+1 must be writable from the latest Series Bible, applicable canon patches, and these final two handoff artifacts. A conflict is `NEEDS_REVIEW`, not permission to infer a reset.
