# Agent Activity Log

Record changes made by Codex, local Hermes, cloud Hermes, and ChatGPT web.

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
