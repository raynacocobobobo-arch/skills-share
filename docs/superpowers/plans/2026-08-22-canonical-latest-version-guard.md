# Canonical Latest Version Guard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make GitHub `main` the latest-approved canonical skill source and prevent silent skill-version downgrade.

**Architecture:** Keep one runtime source of truth: the skill files on `main`. Extend the generated registry with versions, make the router verify registry-to-file consistency, teach the validator to compare against a baseline registry, and enforce the contract in pull-request CI.

**Tech Stack:** Python 3 standard library, pytest/unittest-compatible regression tests, GitHub Actions YAML, Markdown router documentation.

**Spec:** `docs/superpowers/specs/2026-08-22-canonical-latest-version-guard-design.md`

## Global Constraints

- Do not change business-domain skill content in this PR.
- Do not execute Library/local/feature-branch skill copies as runtime authority.
- No customer-private material, credentials, cookies, tokens, or machine-specific absolute paths.
- Existing reference/local-path/secret validation must continue to work.

---

### Task 1: Add failing version-regression tests

**Files:**
- Create: `tests/test_validate_skills.py`

**Produces:** Regression coverage for registry versions, downgrade detection, equal/upgrade/new-skill cases, and malformed versions.

- [ ] Write tests that load `scripts/validate-skills.py` in a temporary repository fixture.
- [ ] Verify current validator fails the new expectations because registry records do not contain `version` and no downgrade comparator exists.
- [ ] Keep test fixtures synthetic and domain-neutral.

**Acceptance:** At least the downgrade/version-field tests fail against the current validator for the expected missing behavior.

---

### Task 2: Add version-aware registry and downgrade validation

**Files:**
- Modify: `scripts/validate-skills.py`
- Generated: `manifests/skill-registry.json`

**Produces:**
- Registry records contain `version`.
- Validator accepts an optional baseline registry path.
- Candidate semantic versions lower than baseline fail.
- Malformed versions fail clearly.
- New skills pass when absent from baseline.
- Explicit `--allow-version-downgrade` override exists for documented emergency rollback.

- [ ] Implement minimal semantic numeric version parser for `N.N.N`-style skill versions.
- [ ] Include parsed frontmatter `version` in every registry record.
- [ ] Add baseline-registry comparison keyed by `skill_path`.
- [ ] Add downgrade errors before registry write is treated as successful.
- [ ] Run Task 1 tests and verify GREEN.

**Acceptance:** All regression tests pass; existing local-path, secret, and missing-reference checks remain intact.

---

### Task 3: Add canonical-version resolution to Router

**Files:**
- Modify: `manifests/web-chatgpt-router.md`

**Produces:** A mandatory runtime resolution contract:

1. route skill;
2. read registry entry;
3. read canonical SKILL from GitHub `main`;
4. compare versions;
5. mismatch → stop;
6. never substitute Library/local/branch copies.

- [ ] Add the version-resolution rule near the mandatory execution rule.
- [ ] Define “latest” as latest approved canonical on `main`.
- [ ] Preserve existing mid-conversation rerouting and multi-skill rules unchanged.

**Acceptance:** Router contains one canonical rule, not a duplicate alternate routing system.

---

### Task 4: Add PR CI enforcement

**Files:**
- Create: `.github/workflows/validate-skills.yml`

**Produces:** Pull-request and main-branch validation.

- [ ] Checkout full history/base ref.
- [ ] Generate a baseline registry from the PR base in a temporary worktree/directory.
- [ ] Run tests.
- [ ] Run candidate validator with baseline registry and `--write-registry`.
- [ ] Fail if generated registry differs from committed `manifests/skill-registry.json`.

**Acceptance:** A synthetic downgrade PR would fail; normal equal/upgrade changes can pass.

---

### Task 5: Document migration/promotion rule and activity

**Files:**
- Modify: `AGENTS.md`
- Modify: `manifests/agent-activity-log.md`

**Produces:** Shared-agent rule that incoming copies are candidates; merge to `main` is the authority promotion event.

- [ ] Add concise version/promotion rule to collaboration workflow.
- [ ] Record branch, files changed, tests/validation status, and any connector limitation.

**Acceptance:** No business-project or customer-private evidence is committed.

---

### Task 6: Final verification and Draft PR

**Verification:**

- [ ] Run regression tests locally/CI.
- [ ] Run `python3 scripts/validate-skills.py --write-registry`.
- [ ] Inspect registry version fields.
- [ ] Compare branch with `main`; verify only planned infrastructure/docs/tests changed.
- [ ] Scan for secrets/local paths/customer-private material.
- [ ] Create Draft PR; do not merge.
- [ ] Confirm workflow status before making any completion claim.

**Acceptance:** Fresh evidence shows tests and validation green; Draft PR contains only scoped changes.
