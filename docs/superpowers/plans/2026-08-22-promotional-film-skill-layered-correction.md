# Promotional Film Skill Layered Correction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Correct the Hermes promotional-film workflow so it adapts to audience, use case, revision mode, source authority, data priority, and Word-based editing without overfitting to a single project.

**Architecture:** Keep `宣传片创作` as the content-domain primary skill. Add a focused audience/revision reference for conditional behavior, update three core writing references to remove absolute rules that caused regressions, add mid-conversation re-routing in the Web router, and make `doc-reviewer` the document-preservation layer when an existing Word file is being revised. Remove the accidental GDevelop cache duplicate from the promotional-film reference tree.

**Tech Stack:** Markdown skill documents, GitHub branch workflow, repository validation via `scripts/validate-skills.py --write-registry` on a local/Codex runtime.

**Spec:** User-approved layered correction design from 2026-08-22 conversation.

## Global Constraints

- Do not encode customer names, scripts, meeting notes, or project-specific wording.
- Preserve the existing six-stage greenfield workflow, but make revision tasks branch before it.
- Customer/user-confirmed facts and structure override generic methodology defaults.
- Core data may be spoken when audience/use-case requires it; detailed parameters remain preferred for subtitles/graphics.
- Literary devices and memorable lines are optional tools, not mandatory score targets.
- Existing Word revision requests must preserve the source document structure/format unless the user explicitly requests a rebuild.

---

### Task 1: Add regression scenarios and promotional-film decision layer

**Files:**
- Modify: `plugins/hermes-skills/skills/hermes-film-宣传片创作/SKILL.md`
- Create: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/宣传片创作-受众适配与改稿模式.md`

**Regression scenarios (RED baseline against current docs):**
1. Government/industry briefing film requires several decisive scale/result figures in narration; current rules forbid them.
2. User says “基于这个版本改，不要重写”; current six-stage workflow has no revision branch and can regenerate structure.
3. Client explicitly locks a phrase/positioning; current methodology can keep re-questioning it because no source-status hierarchy exists.
4. Three-minute film has many facts; current workflow has no mandatory information/time budget before writing.
5. Corporate briefing needs direct prose; current scoring can reward literary/golden-line density over clarity.

**Desired behavior (GREEN):**
- Classify task mode: greenfield / structural rewrite / revision / local polish / existing-Word edit.
- Classify audience/use case before structure/style decisions.
- Build source authority and LOCKED/CONFIRMED/TENTATIVE/CONFLICT status.
- Build time/information budget at outline stage.
- Load the new reference for revision tasks and government/investment/industry briefing tasks.

### Task 2: Correct the three core references

**Files:**
- Modify: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/宣传片创作-解说词写作精要.md`
- Modify: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/宣传片创作-文学技法与评估.md`
- Modify: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/宣传片创作-叙述结构与开场.md`

**Desired behavior:**
- Replace “narration = emotion, subtitles = facts” with priority-based channel assignment.
- Remove numeric narration penalties and mandatory golden-line requirements.
- Make the four-stage persuasion model one optional model, not a mandatory completeness test.
- Add a government/corporate briefing total-part-total structure model.
- Define pseudo-golden-line checks and audience-specific evaluation weights.

### Task 3: Add mid-conversation re-routing and Word preservation

**Files:**
- Modify: `manifests/web-chatgpt-router.md`
- Modify: `plugins/hermes-skills/skills/hermes-business-doc-reviewer/SKILL.md`

**Desired behavior:**
- Re-evaluate routing when the user changes deliverable mode, uploads an existing artifact, or switches from analysis to direct editing.
- Keep the domain skill primary and add artifact/document skills as an execution layer.
- Existing Word + “在此基础上改” means copy/preserve original document and edit in-place in the copy; do not synthesize a new parallel document.

### Task 4: Clean reference contamination

**Files:**
- Delete: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/GDEVELOP_OFFICIAL_DOC_CACHE.md`
- Verify canonical file remains at `plugins/hermes-skills/skills/hermes-dev-gdevelop5-official-docs-first/references/GDEVELOP_OFFICIAL_DOC_CACHE.md`.

### Task 5: Coordination and validation

**Files:**
- Modify: `manifests/agent-activity-log.md`

**Checks:**
- Search promotional-film docs for absolute numeric-ban language and mandatory golden-line scoring.
- Check new reference is linked from `宣传片创作/SKILL.md`.
- Check router contains follow-up re-routing rule.
- Check doc-reviewer contains existing-Word preservation rule.
- Check accidental GDevelop cache is absent from promotional-film references and canonical copy remains.
- Run `python3 scripts/validate-skills.py --write-registry` in Codex/local runtime before merge (GitHub Web connector cannot execute repository scripts).
