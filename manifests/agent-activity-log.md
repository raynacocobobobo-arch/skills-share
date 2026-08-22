# Agent Activity Log

Record changes made by Codex, local Hermes, cloud Hermes, and ChatGPT web.

## 2026-08-23 Codex — ChatGPT Web main fallback exception

- Branch: `codex/allow-chatgpt-web-main-fallback-exception`.
- Added a controlled fallback exception because some ChatGPT Web GitHub connectors can read repository files or edit files but cannot create branches.
- Clarified that ChatGPT Web sessions with write-capable GitHub tools may create `web-chatgpt/<task-name>` branches directly and use those tools to commit, push, and open PRs.
- Scope: collaboration rules only. Updated `AGENTS.md` to require explicit user authorization for fallback, small scoped changes, activity-log updates, validation, unchanged sensitive-data handling, and continued prohibition on direct `main` edits without explicit authorization.
- No skill content was modified.

## 2026-08-22 ChatGPT Web — Story Skill short-form visual upgrade

- Branch: `web-chatgpt/story-short-form-visual-v13-2`.
- Upgraded `故事片创作` candidate from v13.1.0 to v13.2.0 with general-purpose But/Therefore causality checks, delete-before-explain hard-flaw handling, irreversible-dilemma six-question validation, reference-work abstraction instead of role reskinning, setup/payoff meaning-shift checks, and an action water-cut filter.
- Strengthened revision control with soft-approval baseline locking and delta-only local revisions so narrow follow-up changes do not accidentally redesign already accepted story elements.
- Added `references/short-form-visual-story.md` for 1–5 minute / three-minute / image-led stories: charged openings, information budget, visual rule-setting, montage third meaning, repetition/meaning shift, rhythm contrast, and making large backgrounds participate in the drama.
- Extended `tests/test_story_skill_contract.py` to lock the new v13.2 behavior.
- No customer/private project story text or identifying project examples were copied into the skill; only generic reusable rules were distilled.
- Validation note: ChatGPT Web cannot execute the repository validator directly. Open a PR to trigger CI; use the generated registry output to synchronize `manifests/skill-registry.json` before merge.

## 2026-08-22 ChatGPT Web — reference hygiene locks

- Branch: `web-chatgpt/reference-hygiene-locks`.
- Removed clearly misplaced GDevelop and promotional-film reference files from the Story Skill reference bundle, plus the misplaced GDevelop cache from `shared/film-methodology`.
- Added `tests/test_promotional_skill_contract.py` to lock the already-accepted promotional-film rules for revision modes, minimum change, LOCKED facts, spoken core numbers, time/information budget, and existing-Word + doc-reviewer behavior.
- Added `tests/test_reference_hygiene.py` to prevent GDevelop cache files from leaking into film references and promotional-film reference bundles from leaking into Story references.
- No Story/Promo methodology rules were changed; this branch only removes obvious reference pollution and adds cheap CI regression locks.

## 2026-08-22 ChatGPT Web — Story Skill canonical recovery

- Branch: `web-chatgpt/story-skill-canonical-recovery`.
- Started from the post-version-guard `main` and treated the older Library v13 Story Skill only as a candidate/evidence source, not runtime authority.
- Added RED contract tests for Story Skill version, revision modes, minimum-change behavior, source/fact states, optional structural templates, dialogue/VO behavior, commissioned realism, local-path removal, and referential integrity.
- Confirmed RED against canonical v11.1.0: 9 Story contract failures while all 8 version-governance tests remained green.
- Added generic `revision-control.md`, `dialogue-vo-naturalness.md`, and `commissioned-realism.md` references with no customer/private project material.
- Promoted the candidate Story Skill to v13.1.0 with source priority, LOCKED/CONFIRMED/TENTATIVE/CONFLICT/INFERRED/DO_NOT_INVENT states, task-mode routing, minimum-diff revision discipline, optional templates, dialogue/VO checks, professional realism, and rename/renumber/delete reference propagation.
- Final GREEN verification: all 17 tests passed; repository validation reported 28 skills / 0 errors; generated registry matched the committed registry; the 11.1.0 -> 13.1.0 upgrade passed the version guard.
- Diff/privacy review confirmed no customer project identifiers, unpublished script text, local machine paths, or unrelated business-skill edits.
- Draft PR: `#3` (`feat: recover canonical Story Skill v13 behavior`).

## 2026-08-22 ChatGPT Web — canonical latest version guard

- Branch: `web-chatgpt/canonical-latest-version-guard`.
- Added Canonical Latest policy: GitHub `main` is the only runtime authority; Library/local/archive/feature-branch copies remain candidates until validated merge.
- Updated `manifests/web-chatgpt-router.md` so routed tasks resolve the registry entry, read the canonical `SKILL.md` from `main`, and stop on declared-version mismatch instead of falling back to remembered or candidate copies.
- Updated `scripts/validate-skills.py` so generated registry records include declared skill versions and an accepted baseline can reject version removal or downgrade; emergency rollback requires explicit `--allow-version-downgrade`.
- Added `tests/test_validate_skills.py` covering version field generation, downgrade, upgrade, equality, new skill, malformed version, version removal, and explicit rollback override.
- Added `.github/workflows/validate-skills.yml` to run regression tests, validate against the pull-request base registry, regenerate the registry, and require the committed registry to match generated output.
- Updated `AGENTS.md` with canonical promotion/version rules.
- Added Superpowers design and implementation plan under `docs/superpowers/`.
- Draft PR: `#2` (`feat: guard canonical Hermes skill versions`).
- CI run #1: regression tests passed; validator/regeneration passed; the run failed only at the intentional committed-registry consistency gate. The generated registry artifact was retrieved and committed to the branch for the next CI run.

## 2026-08-22 ChatGPT Web

- Branch: `web-chatgpt/promo-skill-layered-correction`.
- Updated `manifests/web-chatgpt-router.md` with follow-up/mid-conversation re-routing and domain-skill + artifact-skill layering.
- Updated `宣传片创作` to distinguish greenfield, structural rewrite, existing-draft revision, local polish, and existing-Word edit modes.
- Added audience/use-case-aware data strategy, source status/locking, and outline-stage time/information budgeting.
- Added `references/AI专用/宣传片创作-受众适配与改稿模式.md`.
- Updated `宣传片创作-解说词写作精要.md`, `宣传片创作-文学技法与评估.md`, and `宣传片创作-叙述结构与开场.md` to remove the absolute narration-number ban, mandatory golden-line scoring, and mandatory four-stage persuasion structure.
- Updated `doc-reviewer` so existing Word documents are treated as the revision baseline; domain skills decide content changes and doc-reviewer preserves/applies them to the original-file copy.
- Removed misplaced `GDEVELOP_OFFICIAL_DOC_CACHE.md` from the promotional-film references; canonical copy remains under `hermes-dev-gdevelop5-official-docs-first/references/`.
- Added Superpowers implementation plan at `docs/superpowers/plans/2026-08-22-promotional-film-skill-layered-correction.md`.
- Validation note: ChatGPT Web GitHub connector cannot execute repository scripts. Before merge, Codex/local agent must run `python3 scripts/validate-skills.py --write-registry` and commit any generated registry changes.

## 2026-08-22 Codex validation

- Branch: `web-chatgpt/promo-skill-layered-correction`.
- Ran `python3 scripts/validate-skills.py --write-registry`: 28 skills, 0 errors.
- Ran Codex plugin validation: passed.
- Ran local path and secret scan: no issues.
- Committed generated `manifests/skill-registry.json` update back to the PR branch.

## 2026-08-22 Codex

- Created shared GitHub repository package for Hermes-derived skills.
- Added Codex plugin marketplace manifests.
- Added multi-agent collaboration protocol.
- Commit: current commit
