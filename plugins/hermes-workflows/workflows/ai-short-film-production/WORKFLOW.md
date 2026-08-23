# AI Short Film Production Pipeline

Use this workflow when the user wants to make an AI story short, AI microfilm, AI film experiment, or to turn a concept into a short narrative video.

This is an orchestrator, not a replacement for specialist skills. It decides the phase order, lock points, handoffs, and review gates. Do not merge the underlying skills into this workflow.

## Trigger

Enter this workflow for requests such as:

- 制作 AI 故事短片
- 做 AI 微电影
- 从概念生成短片
- 做 AI 影视实验
- 做一个 AI 故事短片

Do not start by writing generation prompts. Start by locking the story.

## Pipeline

```text
Idea
↓
Story Development
↓
Visual Development
↓
Asset Bible
↓
Storyboard
↓
AI Production
↓
Review / Iteration
```

## Skill Dispatch

Phase 1 Story Development:

- Primary skill: `hermes-film-故事片创作`
- Read: `plugins/hermes-skills/skills/hermes-film-故事片创作/SKILL.md`
- For 1-5 minute AI shorts, also read: `plugins/hermes-skills/skills/hermes-film-故事片创作/references/short-form-visual-story.md`
- Output: `templates/story-lock.md`

Phase 2 Visual Development:

- Primary skill: `hermes-film-ai-production`
- Read: `plugins/hermes-skills/skills/hermes-film-ai-production/SKILL.md`
- If visual references are provided, read: `plugins/hermes-skills/skills/hermes-film-ai-production/references/visual-analysis.md`
- Output: `templates/visual-bible.md`

Phase 3 Asset Bible:

- Primary skill: `hermes-film-ai-production`
- Read: `plugins/hermes-skills/skills/hermes-film-ai-production/references/asset-bible.md`
- Output: character, environment, and prop cards inside `templates/visual-bible.md`

Phase 4 Storyboard:

- Primary skill: `影视分镜`
- Read: `plugins/hermes-skills/skills/hermes-film-影视分镜/SKILL.md`
- Supporting template: `plugins/hermes-skills/skills/hermes-film-ai-production/references/storyboard-template.md`
- Output: `templates/storyboard.md`

Phase 5 AI Production:

- Primary skill: `AI绘画提示词` for still-image prompts when needed.
- Supporting skill: `hermes-film-ai-production` for prompt strategy, visual consistency, and production review.
- Output: `templates/production-plan.md`

## Locks

Locks prevent prompt-first production, drifting characters, drifting style, and full rewrites after a workable direction has emerged.

Story Lock:

- Required before visual development.
- Must include `logline`, `premise`, `protagonist`, `desire`, `conflict`, `ending`, and `emotional_goal`.
- Set `STORY_LOCKED=true` when accepted.
- After lock, do not change core conflict, ending, or character motivation unless the user explicitly unlocks story.

Visual Lock:

- Required before asset generation.
- Must include `visual_style`, `color_system`, `world_rules`, `character_design`, and `environment_design`.
- Set `VISUAL_LOCKED=true` when accepted.
- After lock, all generated assets inherit these rules.

Production Lock:

- Required before prompt batches or render planning.
- Must include `storyboard`, `shot_list`, `asset_list`, and `prompt_strategy`.
- Set `PRODUCTION_LOCKED=true` when accepted.

Baseline Lock:

- When the user says “方向对了”, “大概意思对”, “这个版本可以”, or equivalent, treat the current version as the baseline.
- Set `BASELINE_LOCKED=true`.
- Future changes must be delta modifications against the baseline.
- Do not redesign the whole project unless the user explicitly asks to unlock or restart.

## Execution Rules

- Keep phase deliverables short enough to use in production.
- Ask only for blocking information; otherwise make a clearly labeled working assumption.
- Each phase ends with a checkpoint from `checkpoints.md`.
- Do not proceed to the next phase if its required lock is missing.
- If the user asks for a change after a lock, identify whether it is a delta modification or requires unlocking.
- Store project outputs using the project template in `templates/production-plan.md` when the user asks to create files.

## First Validation Scenario

Use `《誓言之外》` as the first validation project. Starting from one sentence, the workflow should produce:

```text
Story Lock
↓
Visual Bible
↓
Asset Bible
↓
Storyboard
↓
AI Production Plan
```
