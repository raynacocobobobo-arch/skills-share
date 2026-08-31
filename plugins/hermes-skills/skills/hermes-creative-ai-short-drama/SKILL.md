---
name: hermes-creative-ai-short-drama
description: Use when developing, revising, continuing, storyboarding, producing, or reviewing a pure-AI serialized short drama / AI短剧 / 连载短剧 / AI爽剧 / 一分钟或分集短剧, especially when canon, episode differentiation, continuity, recurring payoffs, or Seedance-oriented production state must persist across episodes.
version: 1.1.0
triggers:
  - AI短剧
  - 连载短剧
  - AI爽剧
  - 一分钟短剧
  - 分集短剧
  - 剧本转分镜
  - 短剧Seedance生产包
---

# Hermes Creative AI Short Drama V1.1

Develop coherent, resumable pure-AI serialized drama from story architecture through production handoff. Preserve what has actually been approved, keep unresolved details unresolved, and prevent a long-running project from drifting because a newer conversation forgot why an older decision existed.

## Mode routing

| Mode | Use when | Workflow |
| --- | --- | --- |
| Greenlight | evaluate a concept and decide whether to pilot | [create-series](workflows/create-series.md), stop after the decision |
| Series | build the Series Bible and 3–5 episode pilot | [create-series](workflows/create-series.md) |
| Canon Revision | an existing project has prior bibles, patches, transcripts, or conflicting historical decisions | [revise-canon](workflows/revise-canon.md) |
| Episode | write/continue one episode from canonical state | [create-episode](workflows/create-episode.md) |
| Storyboard | compile a screenplay into continuity and Shot Specs | [screenplay-to-shots](workflows/screenplay-to-shots.md) |
| Produce | compile valid shots into a Seedance-oriented Production Pack | [shots-to-seedance](workflows/shots-to-seedance.md) |
| Review | inspect executor media, pass it, or issue a targeted retake | [review-and-retake](workflows/review-and-retake.md) |

For a new end-to-end project:

`create-series -> create-episode -> screenplay-to-shots -> shots-to-seedance -> review-and-retake when real media is available`

For an existing long-running project with historical material:

`revise-canon -> create-episode -> downstream production chain`

Create the 3–5 episode pilot plan once, then run the episode chain separately for each requested episode while inheriting approved state. If no media executor/output is available, stop at a complete Production Pack and report `READY`, `BLOCKED`, or `NEEDS_REVIEW`; do not simulate Review or claim `PASS`.

## Story-development gates

Before screenplay prose, enforce these gates:

1. **Canon gate:** load the latest authoritative state. If historical sources disagree, resolve them by scoped precedence; never blend them silently. Read [canon revision rules](references/canon-revision-rules.md).
2. **Architecture gate:** lock the episode/arc function and causal relationship before exact engineering, dialogue, names, or decorative detail. Keep unjustified specifics `TBD`.
3. **Differentiation gate:** compare the proposed episode's dramatic function and conflict grammar against prior episodes. A new prop, location, or casualty does not make a repeated episode new.
4. **Progression gate:** advance the relevant information, pressure/public-action, or relationship/capability track. Do not force every kind of progression into one Reveal Ladder.
5. **Cost gate:** if a third path escapes a binary choice, state what still becomes worse, irreversible, lost, or morally owned. A third path is not a free perfect answer.
6. **Explanation gate:** distinguish internal causal justification from on-screen exposition. Show the minimum evidence needed for the audience to understand the choice; do not narrate the entire research, permissions, engineering, or philosophy chain.
7. **Approval-scope gate:** approval is not transitive. “Structure works, dialogue does not” locks structure only. Dialogue, mechanism, names, visuals, and exact timing remain separate decision scopes unless explicitly approved.

Read [story architecture](references/story-architecture.md) and [episode contract](references/episode-contract.md) for the detailed story rules.

## Artifact chain

`idea -> Series Bible -> Episode Function Map -> Episode Card -> screenplay -> Continuity State -> Shot Spec -> asset/keyframe plan -> Generation Segment -> Production Pack -> QA/Retake Patch -> State Delta -> Continuation Capsule`

For existing projects, Canon Revision may also produce:

`chronology -> conflict table -> narrow canon patch -> updated canonical entrypoint/read order`

Use the templates in [templates](templates/) as fillable shapes. Read only the references required by the selected workflow; source and license treatment is authoritative in [source-map.md](references/source-map.md).

## Canon decision states

Use explicit state labels rather than treating every useful idea as approved:

- `LOCKED`: approved persistent fact.
- `LOCKED_FUNCTION` / `LOCKED_DIRECTION`: approved dramatic or causal function; exact implementation remains open.
- `CANDIDATE`: promising option, not canon.
- `TBD`: intentionally unresolved.
- `NEEDS_REVIEW`: unresolved conflict or decision requiring review.
- `SUPERSEDED` / `NOT_CANON`: historical material retained only for provenance.

A later decision overrides an earlier one only on the same scope. An older source may restore origin, intent, or constraints where later canon is silent; it may not resurrect a superseded plot.

## Hard boundaries

- Keep this Skill independent from `hermes-creative-digital-human`. Route portrait identity masters, face compositing, talking avatars, and LoRA tasks there or to another appropriate skill.
- Default to a 3–5 episode pilot. Do not auto-expand a season before pilot review proves both repeatability and differentiation.
- Preserve the latest approved Series Bible, canon patches, State Delta, Continuation Capsule, Continuity State, asset state, and accepted takes. Conflicts are `NEEDS_REVIEW`, not permission to reset.
- Do not invent a villain, conspiracy, or “final boss” merely because the story needs opposition. Rational institutions, incompatible interests, procedures, and moral mirrors can carry pressure.
- Do not invent a new finale-only exception, sacrifice switch, or technology to manufacture emotion. Major private cost should grow from rules already demonstrated earlier.
- When one character voluntarily accepts a cost, preserve other characters' independent agency; voluntary sacrifice must not erase the protagonist's moral choice.
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

Update canonical episode state only after story/production review confirms what occurred. Rejected, superseded, merely proposed, or uninspected material never becomes a reference, tail frame, State Delta, or Continuation Capsule fact.
