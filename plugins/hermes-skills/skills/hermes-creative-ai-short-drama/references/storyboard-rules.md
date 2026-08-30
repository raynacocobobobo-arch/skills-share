# Storyboard and Shot Spec Rules

A Shot is a narrative/editing unit. It is not automatically a video-model call; Generation Segments are compiled later.

## Shot Spec

Every shot must contain:

```json
{
  "shot_id": "EP01-SC01-SH01",
  "scene_id": "SC01",
  "duration_target_sec": 2.5,
  "framing": "medium",
  "camera_intent": "static reaction",
  "start_state": {},
  "visible_action": "",
  "end_state": {},
  "next_shot_connection": "",
  "reference_assets": [],
  "tail_frame_need": false,
  "prohibited_changes": [],
  "information_gain": ""
}
```

## Hard rules

- One shot contains one visible action. A reaction caused by that action may remain in the same shot; unrelated actions must be split.
- `start_state` and `end_state` must describe the facts changed or preserved by the shot.
- `end_state` must satisfy the next shot's `start_state` or name an explicit transition.
- `next_shot_connection` states the matched action, gaze, prop, audio, movement, or reveal that makes the cut intentional. The final shot connects to the episode handoff.
- `reference_assets` uses approved stable IDs. A required unknown/missing asset blocks the shot.
- `prohibited_changes` protects identity, costume, geography, prop state, revealed information, and other accepted facts.
- `information_gain` names what the audience learns or sees change; use `none — performance/transition` only when the shot has a necessary editing function.

Reject the Shot Spec when it has multiple unrelated visible actions, lacks start/end/connection fields, references an unknown required asset, or reverses screen direction without an explicit re-establishing shot.

## Practical breakdown

Break at a change of action goal, subject, spatial axis, required reference set, or meaningful end state. Prefer the fewest shots that keep action readable and continuity controllable. Do not split merely to hit a fixed duration.

Before generation compilation, verify:

1. all shot IDs and scene IDs are unique;
2. every referenced entity exists in Continuity State;
3. shot state forms an unbroken chain;
4. the scene's last shot produces the screenplay's intended scene end state;
5. every shot is `READY`, `BLOCKED`, or `NEEDS_REVIEW` with an honest reason.
