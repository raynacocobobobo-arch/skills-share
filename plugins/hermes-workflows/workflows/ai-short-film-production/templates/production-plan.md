# AI Production Plan

```ini
PRODUCTION_LOCKED=false
BASELINE_LOCKED=false
```

## Project Folder Template

```text
project/
  story/
    story-lock.md
  visual/
    visual-bible.md
  assets/
    characters/
    environments/
    props/
  storyboard/
    shot-list.md
  production/
    prompts/
    renders/
    review/
  final/
```

## Prompt Strategy

```text
render_order:

reference_assets:

character_consistency_rules:

environment_consistency_rules:

prompt_batch_plan:

negative_prompt_rules:

iteration_rule:
```

## Render Review

```text
shot_id:
matches_story_lock:
matches_visual_lock:
matches_asset_bible:
ai_drift:
regenerate_or_keep:
delta_modification:
```

## Revision Control

When the user accepts a version, record it as baseline. Later revisions should change only the requested delta.
