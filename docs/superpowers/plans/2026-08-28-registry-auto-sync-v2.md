# Registry Auto-Sync V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically regenerate and commit `manifests/skill-registry.json` whenever skill metadata changes on a feature branch, while removing registry staleness as a manual CI failure mode.

**Architecture:** `SKILL.md` remains authoritative. `scripts/validate-skills.py` generates the registry. A non-main branch workflow auto-commits the generated registry when needed; the normal validation workflow validates skills and versions without requiring a pre-synced committed registry.

**Tech Stack:** GitHub Actions YAML, Python 3 standard library, unittest, GitHub contents/branch workflow.

**Spec:** `docs/superpowers/specs/2026-08-28-registry-auto-sync-v2.md`

## Global Constraints

- `SKILL.md` is the single source of truth.
- Do not add another manifest/database.
- Preserve version downgrade protection and existing validation.
- Auto-sync writes only `manifests/skill-registry.json` and never writes to `main`.

---

### Task 1: Define auto-sync workflow contract

**Files:**
- Create: `tests/test_registry_auto_sync.py`
- Create: `.github/workflows/sync-skill-registry.yml`

**Interfaces:**
- Consumes: `scripts/validate-skills.py --write-registry`
- Produces: generated registry commit on non-main branches.

- [ ] Write failing tests asserting the workflow triggers on non-main pushes, has `contents: write`, runs the validator, commits only registry changes, and exits cleanly when there is no diff.
- [ ] Run tests and confirm failure because workflow does not exist.
- [ ] Add the minimal workflow.
- [ ] Run tests and confirm success.

### Task 2: Remove manual registry-match failure from validation

**Files:**
- Modify: `.github/workflows/validate-skills.yml`
- Modify: `tests/test_registry_auto_sync.py`

**Interfaces:**
- Consumes: committed base registry for version comparison.
- Produces: validation status based on skill correctness, not stale generated-file state.

- [ ] Add a failing test asserting validation no longer uses `--check-registry` / `Require semantic registry match`.
- [ ] Remove committed-registry capture and semantic-match step while preserving baseline version validation and generated artifact upload.
- [ ] Run tests.

### Task 3: Verify generator and repository contract

**Files:**
- Test: all `tests/test_*.py`
- Generated: `manifests/skill-registry.json`

**Interfaces:**
- Consumes: all `SKILL.md` frontmatter.
- Produces: deterministic registry JSON.

- [ ] Run all unittest tests.
- [ ] Regenerate registry and verify no unintended skill metadata changes.
- [ ] Review branch diff to confirm only workflow/tests/docs and generated registry are touched.
- [ ] Open PR and wait for CI.
