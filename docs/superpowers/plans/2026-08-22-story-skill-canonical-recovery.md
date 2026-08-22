# Story Skill Canonical Recovery — Implementation Plan

## Task 1 — Add RED contract tests
**Files**
- Create `tests/test_story_skill_contract.py`

**Goal**
Prove the current canonical v11.1.0 fails the desired recovered contract before modifying the skill.

**Checks**
- version >= 13.1.0;
- no local machine path;
- three supporting references declared and present;
- source priority + minimum-change rule;
- task-mode distinction;
- unified fact states;
- templates explicitly optional;
- referential integrity rule;
- no evidence-project private identifiers.

**Acceptance**
CI/test run fails against v11.1.0 for expected contract reasons.

## Task 2 — Create de-projectized references
**Files**
- Create `plugins/hermes-skills/skills/hermes-film-故事片创作/references/revision-control.md`
- Create `plugins/hermes-skills/skills/hermes-film-故事片创作/references/dialogue-vo-naturalness.md`
- Create `plugins/hermes-skills/skills/hermes-film-故事片创作/references/commissioned-realism.md`

**Goal**
Move reusable rules out of project-specific v13 examples and keep the main skill decision-focused.

**Acceptance**
References contain observable triggers and generic rules only; no customer/project/private data.

## Task 3 — Promote Story Skill to v13.1.0
**File**
- Modify `plugins/hermes-skills/skills/hermes-film-故事片创作/SKILL.md`

**Goal**
Recover proven v13 behavior, remove project examples and old local-path assumptions, add the two remaining generic improvements.

**Acceptance**
- all Story contract tests pass;
- legacy mandatory template rules are absent;
- v13-proven revision/realism/dialogue/VO behavior remains;
- declared references exist.

## Task 4 — Regenerate registry and activity log
**Files**
- Modify `manifests/skill-registry.json` via validator output
- Modify `manifests/agent-activity-log.md`

**Goal**
Record canonical candidate version 13.1.0 and the recovery rationale.

**Acceptance**
Version guard treats 11.1.0 -> 13.1.0 as an upgrade; registry has no drift.

## Task 5 — Draft PR and verification
**Actions**
1. Open Draft PR to `main`.
2. Run repository CI.
3. Verify Story contract tests, version tests, validator, registry consistency.
4. Review changed-file diff for accidental project/private content or unrelated edits.
5. Keep Draft until fresh verification is green.

**Acceptance**
- all CI steps green;
- no secrets/local paths/customer-private content;
- no unrelated skill changes;
- PR remains unmerged until explicit merge decision.
