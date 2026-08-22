# Agent Collaboration Guide

This repository is the shared source of truth for Hermes-derived skills and methodology notes.

## Actors

- `codex-local`: Codex on Rayna's Mac.
- `hermes-local`: local Hermes on Rayna's Mac.
- `hermes-cloud`: cloud Hermes.
- `chatgpt-web`: ChatGPT web with GitHub repository access.

## Golden Rule

Before using or changing a skill, read the latest repository state. Before publishing a change, validate it, commit it, and push it.

## Canonical latest and version promotion

- GitHub `main` is the only runtime authority for accepted Hermes skills.
- Library copies, local copies, archives, and feature branches are candidates only; a higher version outside `main` is not automatically authoritative.
- Promotion happens by validated merge to `main`, not by copying a file into a workspace.
- `manifests/skill-registry.json` records declared skill versions. Once an accepted skill declares a version, a later candidate must not remove or lower it silently.
- A lower-version rollback requires an explicit documented override and must remain visible in validation logs/review history.

## Read Workflow

1. Read `manifests/web-chatgpt-router.md` or `manifests/skill-registry.json`.
2. Select the matching skill.
3. Read the selected `SKILL.md`.
4. Read only the referenced `references/`, `shared/`, `assets/`, or `scripts/` files required by that skill.
5. Execute the user task using the repository files as the current authority.

## Write Workflow

1. Sync first:
   - Local Git clients: `git pull --ff-only`.
   - ChatGPT web: re-read the GitHub repo files before proposing edits.
2. Create a branch:
   - Codex: `codex/<task-name>`.
   - Local Hermes: `local-hermes/<task-name>`.
   - Cloud Hermes: `cloud-hermes/<task-name>`.
   - ChatGPT web: `web-chatgpt/<task-name>`.
3. Make the smallest scoped edit.
4. Update `manifests/agent-activity-log.md`.
5. Run `python3 scripts/validate-skills.py --baseline-registry manifests/skill-registry.json --write-registry` before the registry is overwritten; for a bootstrap repository without a registry, run without `--baseline-registry`.
6. Commit and push.
7. Merge only after validation succeeds.

## ChatGPT Web fallback exception

When ChatGPT web cannot create a branch because the connected GitHub tool lacks branch creation capability:

- The user must explicitly authorize the fallback.
- Only small scoped changes are allowed.
- The change must still update `manifests/agent-activity-log.md`.
- Validation must still run.
- Sensitive data rules remain unchanged.
- Direct `main` edits without explicit user authorization remain forbidden.

## Main Branch Rules

- `main` contains the shared accepted skill set.
- Do not force-push `main` unless replacing a known bootstrap commit or recovering from a documented mistake.
- Do not commit local-only paths, credentials, cookies, tokens, or customer-private documents.

## Sensitive Data

Never commit:

- API keys, bearer tokens, cookies, passwords, SSH private keys, Apple app passwords, or cloud credentials.
- Customer scripts, contracts, quotes, contact details, unpublished project files, or private meeting notes unless explicitly cleared.
- Machine-specific absolute paths when an environment variable or relative path can be used.

Use placeholders such as:

- `<REDACTED_TOKEN>`
- `<LOCAL_OBSIDIAN_PROJECTVAULT>`
- `${HERMES_TODO_ROOT}`
- `<REPO_ROOT>`

## Conflict Handling

If two agents modify the same skill:

1. Preserve both intent streams in a temporary branch.
2. Compare `SKILL.md`, `references/`, and registry changes.
3. Keep the simpler version unless the more complex version has clear task evidence.
4. Re-run validation before merge.

## Repository Layout

- `plugins/hermes-skills/`: Codex plugin package.
- `plugins/hermes-skills/skills/`: skill directories.
- `shared/`: shared methodology notes for Obsidian and skill references.
- `manifests/skill-registry.json`: generated skill inventory.
- `manifests/web-chatgpt-router.md`: routing instructions for ChatGPT web.
- `scripts/validate-skills.py`: validation and registry generation.
- `scripts/sync-hermes-knowledge.sh`: pull latest repository updates.
