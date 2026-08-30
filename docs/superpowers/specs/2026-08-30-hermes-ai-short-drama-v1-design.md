# Hermes AI Short Drama V1 Design

## Goal

Build an independent Hermes Skill for pure AI serialized short-drama production, targeting roughly 1-minute episodes. V1 must be assembled primarily from proven open-source short-drama Skills and architectures rather than rewritten from scratch.

The target chain is:

`idea -> series bible -> pilot/episode -> screenplay -> continuity compile -> storyboard/shot spec -> asset/keyframe plan -> generation segments -> Seedance-ready production pack -> QA/retake -> episode state delta -> next episode`

This Skill is independent from `hermes-creative-digital-human`. Digital-human/LoRA workflows are out of scope.

## Design Principle: Reuse First

V1 uses a module-composition strategy:

1. Reuse legally compatible public structures, schemas, contracts, and workflow fragments where practical.
2. Adapt mature concepts into the existing Hermes Skill layout.
3. Write only the minimum glue required to reconcile naming, state, routing, and conflicting assumptions.
4. Do not copy code or text from sources whose licenses do not permit the intended reuse. Such sources may inform architecture only.
5. Record provenance and license treatment in `references/source-map.md`.

## Primary Sources

### Hao0321/ai-short-drama — narrative and serialization backbone

Reuse/adapt:
- Scout / Greenlight / Bible / Season / Episode / Studio / Produce / Audit separation
- Series Bible
- entity registry
- reveal ladder
- antagonist ladder
- payoff debt ledger
- pilot-first strategy
- dominant turn
- episode state delta
- continuation capsule
- production contract separation between narrative and media generation

### MrMO0802/short-drama-agent — continuity-first production

Reuse/adapt:
- asset inventory
- scene geography
- character continuity
- prop state
- clue reveal state
- action causality
- screen direction
- asset approval state
- shot start state / end state / next-shot connection
- one visible action per shot
- blocked-by-missing-asset behavior
- representative-shot-first generation strategy
- review/retry guidance

### zouchenzhen/short-drama-prompt-director — Seedance compilation

Reuse/adapt:
- beat sheet
- generation segment planning
- scene snapshots
- shot cards
- Seedance-ready prompt pack
- NOT constraints
- 4–15 second generation segments
- P0/P1/P2 QA
- first-frame / last-frame / reference binding logic where applicable

### ouyangevan/codex-short-drama-pipeline-skill — production package and QC state

Reuse/adapt:
- story bible / series engine / character bible / scene bible / prop-evidence ledger separation
- generation log
- QC report
- explicit blocked state when assets or media have not been verified

Simplify its gates to Hermes states:
- READY
- BLOCKED
- NEEDS_REVIEW
- PASS

### Architecture-only references

Use Huobao, Toonflow, Jellyfish, ArcReel, VideoClaw, ai-fusion-video and other researched projects for architecture patterns where useful, without copying incompatible implementation text/code.

Patterns of interest:
- Huobao: Agent -> Skill -> Tool -> structured entities
- Toonflow: Story Agent / Production Agent split and memory
- Jellyfish: shot workspace and production state
- ArcReel: continuity, checkpoints, async generation and rollback
- VideoClaw: generation-mode routing (first frame, first+last frame, references)
- ai-fusion-video: persistent agent workspace/run state

## V1 Scope

V1 owns:
- concept evaluation and pilot setup
- series/season/episode narrative state
- screenplay compilation
- continuity state
- storyboard and shot specification
- asset/keyframe requirements
- generation-segment compilation
- Seedance-oriented prompt packaging
- generation handoff records
- shot-level QA
- retake patches
- episode state update and next-episode handoff

V1 does not require:
- a web UI
- database infrastructure
- login/billing
- its own media-generation API client
- its own FFmpeg editor
- task queues or distributed workers
- LoRA/digital-human workflows
- full autonomous publishing

Those remain downstream executors or future versions.

## Target Skill Layout

```text
plugins/hermes-skills/skills/hermes-creative-ai-short-drama/
├── SKILL.md
├── references/
│   ├── story-architecture.md
│   ├── episode-contract.md
│   ├── continuity-rules.md
│   ├── storyboard-rules.md
│   ├── generation-segment-rules.md
│   ├── seedance-rules.md
│   ├── qa-rules.md
│   └── source-map.md
├── templates/
│   ├── series-bible.md
│   ├── episode-card.md
│   ├── continuity-state.json
│   ├── storyboard.json
│   ├── production-pack.json
│   └── retake-patch.json
└── workflows/
    ├── create-series.md
    ├── create-episode.md
    ├── screenplay-to-shots.md
    ├── shots-to-seedance.md
    └── review-and-retake.md
```

This follows the existing Hermes pattern of `SKILL.md + references + templates + workflows` rather than introducing a new framework.

## Core Workflow

1. Greenlight
2. Series Bible
3. Pilot planning (default 3–5 episodes before season expansion)
4. Episode Card
5. Screenplay
6. Continuity Compile
7. Storyboard / Shot Spec
8. Asset + Keyframe Plan
9. Generation Segment Compile
10. Seedance Prompt Pack
11. QA
12. Retake Patch when required
13. Episode State Delta
14. Continuation Capsule / next episode

## Core Contracts

### Episode Card

Minimum fields:
- episode_id
- opening_hook
- dominant_turn
- core_conflict
- payoff_or_progress
- ending_cliffhanger
- state_delta

### Continuity State

Must cover only production-relevant persistent facts:
- character state
- costume/injury state where relevant
- scene geography
- screen direction
- prop/evidence state
- clue reveal state
- action causality dependencies

### Shot Spec

A shot is a narrative/editing unit, not necessarily a model call.

Minimum fields:
- shot_id
- scene_id
- duration_target
- framing/camera intent
- start_state
- visible_action
- end_state
- next_shot_connection
- reference_assets
- tail_frame_need
- prohibited_changes
- information_gain

Hard rule: one visible action per shot unless a tested target model explicitly supports a more complex action safely.

### Generation Segment

A generation segment is the model-call unit and may contain one or more compatible shots.

Minimum fields:
- segment_id
- shot_ids
- target_duration
- generation_mode
- target_model
- references
- continuity_priority
- motion_priority
- prompt
- not_constraints

Generation modes:
- first_frame
- first_last_frame
- reference_images
- reference_video when supported
- text_to_video

Default Seedance-oriented segment duration: 4–15 seconds, subject to verified model capability.

### QA

- P0: factual/identity/continuity failure; mandatory retake
- P1: material performance/camera/pacing problem; normally retake
- P2: polish issue; optional improvement

P0 examples:
- wrong character identity
- unexplained costume change
- screen-direction reversal that breaks geography
- key prop disappears/resets
- incorrect story information
- wrong dialogue/action causality

### Retake Patch

Retakes modify only failed variables while preserving accepted state.

Minimum fields:
- shot_or_segment_id
- severity
- preserve[]
- fix[]
- reason
- retry_count

## State and Resumability

The system must be restartable from persisted project artifacts. It must not require re-generating an entire episode because one shot failed.

Expected unit of revision:
- story change -> affected episode and downstream state
- continuity change -> affected shots/segments
- shot failure -> affected shot/segment only
- prompt failure -> prompt/segment only

Generation history should record accepted/rejected takes without requiring V1 to implement a database.

## Source-to-Target Mapping Rule

Before implementation, create `references/source-map.md` containing a table with:
- source repository
- source file/path
- source license
- target Hermes file
- treatment: copy / adapt / architecture-only
- retained concepts
- removed concepts
- local modifications

No source fragment enters the Skill without a provenance entry.

## Router and Registry

V1 is a separate Skill from digital-human production.

Trigger examples:
- AI短剧
- 连载短剧
- AI爽剧
- 一分钟短剧
- 分集短剧
- 剧本转分镜
- 短剧Seedance生产包

Do not route ordinary digital-human portrait/compositing/LoRA tasks here.

Registry changes must be minimal. Do not redesign `skill-registry.json` as part of this project.

## Validation Strategy

V1 is accepted only after a benchmark pilot demonstrates the full contract chain.

Benchmark:
- one original serialized short-drama premise
- 3–5 pilot episodes
- roughly 1 minute target duration per episode
- at least two recurring characters
- at least one recurring location
- at least one continuity-sensitive prop/clue
- at least one failed-shot retake simulation

Validation must verify:
1. Episode N+1 correctly inherits Episode N state.
2. Storyboard shots preserve scene geography and prop state.
3. Every shot has start/end state and a next-shot connection.
4. Generation segments reference valid shots/assets.
5. A P0 failure creates a targeted retake patch rather than whole-episode regeneration.
6. Missing assets produce BLOCKED rather than fabricated completion.
7. The Skill can hand a complete production pack to a downstream image/video executor.

## Success Criteria

V1 succeeds when ChatGPT/Codex can take an original short-drama concept through a 3–5 episode pilot and produce coherent, resumable, shot-level production packs without depending on digital-human assets or pretending ungenerated media exists.

The goal is not a new all-in-one platform. The goal is a reliable Hermes director/showrunner/production-planning Skill assembled from proven open-source methods.