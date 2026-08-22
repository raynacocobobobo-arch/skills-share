# Hermes Knowledge

## For ChatGPT Web

When using this private repository from ChatGPT Web through the GitHub connection, use the router as the canonical entry point:

`manifests/web-chatgpt-router.md`

Recommended invocation:

> 请按 Hermes skill 路由执行这个任务。

ChatGPT Web should read the router first, select the matching Hermes skill, then read that skill's `SKILL.md` and any required `references/` / `shared/` files before answering. **Do not simulate a Hermes skill from memory or prior chat history when the GitHub source is available.**

For strict file-grounded execution:

> 请按 Hermes skill 路由执行。先从 GitHub 读取路由文件和匹配的 `SKILL.md`，不要凭记忆模拟。

---

Private knowledge and skill repository for Hermes-derived Codex skills.

## What Is Included

- `plugins/hermes-skills/` - local Codex plugin package.
- `plugins/hermes-skills/skills/` - bundled skills copied from the curated Hermes migration set.
- `shared/` - Obsidian-readable methodology mirrors.
- `manifests/` - generated migration, dependency, and redaction reports.

The plugin currently contains 23 primary migrated skills plus 5 nested perspective example skills from `huashu-nuwa`.

## Usage

Open this repository as an Obsidian vault to browse and edit the methodology notes. Use the `hermes-skills` plugin folder for Codex plugin packaging.

Important paths:

- Web ChatGPT router: `manifests/web-chatgpt-router.md`
- Plugin root: `plugins/hermes-skills/`
- Skill directory: `plugins/hermes-skills/skills/`
- Dependency manifest: `manifests/dependency-manifest.json`
- Redaction report: `manifests/redaction-report.md`

## Security

This repository is intended to be private. Do not commit real API keys, bearer tokens, cookies, SSH keys, customer confidential material, or machine-specific secrets.
