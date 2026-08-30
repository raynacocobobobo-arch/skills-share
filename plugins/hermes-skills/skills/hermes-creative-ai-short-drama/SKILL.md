---
name: hermes-creative-ai-short-drama
description: Plan and direct pure-AI serialized short dramas from concept through Series Bible, Episode Card, continuity-first Shot Specs, Seedance-oriented Production Pack, QA, targeted retakes, and next-episode state. Use for AI短剧、连载短剧、AI爽剧、一分钟/分集短剧、剧本转分镜或短剧 Seedance 生产包; do not use for digital-human portraits, LoRA training, face compositing, or ordinary talking-avatar work.
version: 1.0.0
triggers:
  - AI短剧
  - 连载短剧
  - AI爽剧
  - 一分钟短剧
  - 分集短剧
  - 剧本转分镜
  - 短剧Seedance生产包
---

# Hermes Creative AI Short Drama V1

Create coherent, resumable production plans for roughly one-minute serialized AI drama. Preserve canonical story and production state across episodes, and hand Generation Segments to downstream image/video executors without pretending ungenerated media exists.

## Mode routing

| Mode | Use when | Workflow |
| --- | --- | --- |
| Greenlight | evaluate a concept and decide whether to pilot | [create-series](workflows/create-series.md), stop after the decision |
| Series | build the Series Bible and 3–5 episode pilot | [create-series](workflows/create-series.md) |
| Episode | write/continue one episode from canonical state | [create-episode](workflows/create-episode.md) |
| Storyboard | compile a screenplay into continuity and Shot Specs | [screenplay-to-shots](workflows/screenplay-to-shots.md) |
| Produce | compile valid shots into a Seedance-oriented Production Pack | [shots-to-seedance](workflows/shots-to-seedance.md) |
| Review | inspect executor media, pass it, or issue a targeted retake | [review-and-retake](workflows/review-and-retake.md) |

For an end-to-end request, run:

`create-series -> create-episode -> screenplay-to-shots -> shots-to-seedance -> review-and-retake when real media is available`

Create the 3–5 episode pilot plan once, then run the episode chain separately for each requested episode while inheriting approved state. If no media executor/output is available, stop at a complete Production Pack and report `READY`, `BLOCKED`, or `NEEDS_REVIEW`; do not simulate Review or claim `PASS`.

## Artifact chain

`idea -> Series Bible -> Episode Card -> screenplay -> Continuity State -> Shot Spec -> asset/keyframe plan -> Generation Segment -> Production Pack -> QA/Retake Patch -> State Delta -> Continuation Capsule`

Use the templates in [templates](templates/) as fillable shapes. Read only the reference required by the selected workflow; source and license treatment is authoritative in [source-map.md](references/source-map.md).

## Hard boundaries

- Keep this Skill independent from `hermes-creative-digital-human`. Route portrait identity masters, face compositing, talking avatars, and LoRA tasks there or to another appropriate skill.
- Default to a 3–5 episode pilot. Do not auto-expand a season before pilot review.
- Preserve the latest approved Series Bible, State Delta, Continuation Capsule, Continuity State, asset state, and accepted takes. Conflicts are `NEEDS_REVIEW`, not permission to reset.
- A Shot is an editing/narrative unit; a Generation Segment is one model-call unit.
- One visible action per Shot unless a specific tested model safely supports the planned complexity.
- Missing required assets/keyframes/media make only affected work `BLOCKED`. Never fabricate an asset, take, or completion status.
- `PASS` requires inspection of actual executor output. Planning-only handoff can be `READY` but never media `PASS`.
- P0 failures require a targeted Retake Patch that preserves accepted variables. Do not regenerate the whole episode for one isolated failure.
- Do not add web UI, databases, task platforms, media API clients, FFmpeg automation, publishing automation, digital humans, LoRA, or ComfyUI workflows to V1.

## Status

- `READY`: inputs and assets are sufficient for the named next step.
- `BLOCKED`: a required asset, state, capability, or real output is missing; name it.
- `NEEDS_REVIEW`: artifacts conflict or a human/story/QA decision is unresolved.
- `PASS`: actual reviewed output meets the applicable contract.

Update canonical episode state only after story/production review confirms what occurred. Rejected or uninspected media never becomes a reference, tail frame, State Delta, or Continuation Capsule fact.
