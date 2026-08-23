# Agent Collaboration Guide

This repository is the shared source of truth for Hermes-derived skills,
methodology notes, and source-library material.

## Core Boundaries

- Treat GitHub `main` as the accepted shared source.
- Treat local copies, Library copies, archives, and feature branches as
  candidates until merged.
- Before using or changing a skill, read the current repository file, then read
  only the referenced files needed for the task.
- Keep Hermes as a capability library. Do not add governance frameworks,
  approval systems, workflow engines, or extra manifest layers unless a separate
  task explicitly requires them.

## Safety Rules

Never commit:

- API keys, bearer tokens, cookies, passwords, SSH private keys, Apple app
  passwords, or cloud credentials.
- Customer scripts, contracts, quotes, contact details, unpublished project
  files, or private meeting notes unless explicitly cleared.
- Machine-specific absolute paths when an environment variable, placeholder, or
  relative path can be used.

Use placeholders such as:

- `<REDACTED_TOKEN>`
- `<LOCAL_OBSIDIAN_PROJECTVAULT>`
- `${HERMES_TODO_ROOT}`
- `<REPO_ROOT>`

## Modification Levels

### Level 1: Documentation Changes

Use Level 1 for typo fixes, wording cleanup, clarification, and reference-link
adjustments that do not change skill behavior, routing behavior, registry
content, or published package structure.

Rules:

- Make the smallest scoped edit.
- Do not rewrite the registry for pure documentation cleanup.
- Run the lightweight relevant check, normally `python3 scripts/validate-skills.py`.
- Commit with a message that makes the documentation-only scope clear.

### Level 2: Capability Changes

Use Level 2 for any change that affects:

- skill behavior or frontmatter;
- router behavior;
- registry or manifest content;
- bundled references that a skill depends on;
- validation, packaging, or publish behavior.

Rules:

- Make the smallest scoped edit.
- Update generated registry content when skill metadata or referenced paths
  change.
- Run `python3 scripts/validate-skills.py`; for publish/merge preparation, run
  the repository's publish validation path when available.
- Do not remove, move, or merge a skill until callers and routes have been
  checked.

## Commit Principles

- Work on a branch, not directly on `main`.
- Sync or re-read the latest repository state before editing.
- Keep unrelated cleanup out of the diff.
- Do not force-push `main` unless recovering from a documented mistake.
- If two agents touch the same skill, compare both intent streams and keep the
  simpler version unless the more complex version has clear task evidence.

## Entry Points

- ChatGPT Web routing: `manifests/web-chatgpt-router.md`
- Machine-readable skill inventory: `manifests/skill-registry.json`
- Capability policy: `manifests/execution-capability-policy.md`
- Skill root: `plugins/hermes-skills/skills/`
- Shared methodology and source library: `shared/`
- Validation: `scripts/validate-skills.py`
