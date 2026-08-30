# QA and Targeted Retake Rules

Review real executor output against the approved Episode Card, Continuity State, Shot Specs, Generation Segment, and bound references. Planning completeness alone cannot produce `PASS` for media.

## Severity

### P0 — mandatory retake

- wrong or drifting character identity;
- unexplained costume, injury, relationship, or state reset;
- broken scene geography or screen-direction reversal;
- missing, reset, transformed, or incorrectly handled critical prop/clue;
- incorrect story information or plot-critical dialogue;
- broken action causality or ending state.

P0 makes the affected shot/segment `NEEDS_REVIEW` and requires a Retake Patch. Accepted unrelated segments remain accepted.

### P1 — normally retake

- performance fails the intended emotion or readable reaction;
- camera motion/framing hides the story event;
- pacing makes the beat unclear or unusable in the target edit;
- obvious light, visual, or audio discontinuity across the cut.

Retake unless the editor can correct it without changing story/continuity and records that decision.

### P2 — optional polish

Minor composition, atmosphere, texture, or timing issues that do not break identity, story, continuity, or editability. Record them; do not block delivery unless the user raises the quality bar.

## Review order

1. Verify the output exists and belongs to the expected task/take.
2. Check P0 identity, facts, continuity, prop/clue state, geography, and causality.
3. Check P1 performance, camera, pacing, light, and cut continuity.
4. Record P2 polish only after blockers are clear.
5. Set the take to `accepted`, `rejected`, or `needs_review`; set the segment to `PASS` only after the required checks pass.

## Retake Patch

A Retake Patch targets one failed shot or Generation Segment and includes:

- `shot_or_segment_id`;
- `severity`;
- accepted variables in `preserve`;
- diagnosed variables in `fix`;
- observable `reason` and acceptance criteria;
- `retry_count` and previous take reference.

The retry must preserve every accepted variable unless the diagnosis explicitly moves it into `fix`. Do not randomize composition, identity, costume, geography, dialogue, camera, action, prop state, and sound together to repair one failure.

If the same diagnosis fails repeatedly, stop blind retries. Reassess asset/reference quality, split the segment, simplify the action, or select a more suitable verified generation mode. This is still a targeted change; do not regenerate the whole episode for an isolated failure.

## State update

Only accepted media and approved story review may finalize the episode State Delta. Rejected takes never become references, tail frames, or canonical evidence. After all required segments pass, update the Continuation Capsule and canonical state with what actually occurred, not what the prompt intended.
