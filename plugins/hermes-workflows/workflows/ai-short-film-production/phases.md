# Phases

## Phase 1: Story Development

Goal: turn the idea into a locked short-form story.

Inputs:

- one-sentence idea
- theme or emotional target
- optional reference works
- target length, normally 1-5 minutes

Use:

- `hermes-film-故事片创作`
- `short-form-visual-story.md`

Deliverable:

- completed `templates/story-lock.md`
- `STORY_LOCKED=true`

Do not proceed if the ending, protagonist desire, or central conflict is still vague.

## Phase 2: Visual Development

Goal: turn the locked story into a visual system.

Inputs:

- Story Lock
- reference images or style references, if any
- production constraints

Use:

- `hermes-film-ai-production`
- `visual-analysis.md` when references are present

Deliverable:

- completed visual system in `templates/visual-bible.md`
- `VISUAL_LOCKED=true`

Do not generate final assets before visual style, color system, world rules, character design, and environment design are fixed.

## Phase 3: Asset Bible

Goal: create lightweight continuity rules for recurring characters, locations, and props.

Inputs:

- Story Lock
- Visual Bible

Use:

- `asset-bible.md`

Deliverable:

- 1-3 core character cards
- 1-3 environment cards
- critical prop cards only

Keep this lightweight. Do not create a DAM, database, manifest, or approval system.

## Phase 4: Storyboard

Goal: convert story and assets into executable shots.

Inputs:

- Story Lock
- Visual Bible
- Asset Bible

Use:

- `影视分镜`
- `storyboard-template.md`

Deliverable:

- completed `templates/storyboard.md`
- shot list with story function for each shot

Do not include shots that only look cinematic but do not change information, relationship, suspense, setup/payoff, or emotional state.

## Phase 5: AI Production

Goal: prepare prompt batches, render order, and iteration plan.

Inputs:

- Storyboard
- Asset Bible
- Visual Bible

Use:

- `AI绘画提示词` for still-image prompt conversion
- `hermes-film-ai-production` for prompt strategy and review

Deliverable:

- completed `templates/production-plan.md`
- `PRODUCTION_LOCKED=true`

Do not change locked story or visual rules during prompt writing.

## Phase 6: Review / Iteration

Goal: compare outputs against locks and decide the smallest useful revision.

Inputs:

- current render or prompt output
- Story Lock
- Visual Lock
- Production Lock

Use:

- `checkpoints.md`

Deliverable:

- issue list ordered by story, visual, and production impact
- delta modification plan

If the user approves a version, set or update Baseline Lock and preserve it.
