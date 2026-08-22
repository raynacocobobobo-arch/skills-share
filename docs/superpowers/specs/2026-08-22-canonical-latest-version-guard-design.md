# Canonical Latest Version Guard Design

## Goal

Ensure Hermes always executes the latest **approved canonical** skill from GitHub `main`, while preventing a lower-version skill from silently replacing a newer accepted version.

## Source-of-truth rule

- GitHub `main` remains the only runtime authority.
- Library files, local copies, feature branches, and prior-chat copies are candidates or development artifacts, not runtime authority.
- “Latest” means **latest approved canonical version on `main`**, not the numerically highest version found anywhere.

## Four defenses

### 1. Registry carries skill versions

`manifests/skill-registry.json` must record each skill frontmatter `version`.

The registry continues to be generated from `plugins/hermes-skills/skills/**/SKILL.md`; it does not become a second manually maintained source of truth.

### 2. Router verifies registry ↔ SKILL consistency

For an explicitly Hermes-routed task:

1. Read `manifests/web-chatgpt-router.md`.
2. Match the skill.
3. Read `manifests/skill-registry.json` and resolve the canonical `skill_path` and `version`.
4. Read that `SKILL.md` from GitHub `main`.
5. Verify the SKILL frontmatter version equals the registry version.
6. If they disagree, stop and report repository inconsistency; do not fall back to memory, Library, local copies, or an older/newer branch.

### 3. Validator blocks version downgrade

`scripts/validate-skills.py` must compare the proposed skill versions with a baseline registry or baseline skill set supplied by CI.

A change that lowers a skill version fails validation unless an explicit emergency override is used.

Required regression cases:

- baseline `13.0.0`, candidate `11.1.0` → FAIL
- baseline `11.1.0`, candidate `13.0.0` → PASS
- equal versions → PASS
- malformed versions → FAIL clearly
- newly introduced skill with no baseline → PASS

The override must be explicit and visible in logs; normal validation must never silently permit a downgrade.

### 4. Pull-request CI enforces the contract

Add a GitHub Actions workflow that, for pull requests and pushes to `main`:

- runs validator/tests;
- checks generated registry consistency;
- compares candidate versions against the PR base branch;
- rejects version downgrade;
- keeps existing local-path/secret/reference validation.

## Migration/import rule

Incoming copies from Library, local Hermes, Codex, archives, or migration scripts are candidates only.

Before replacing a canonical skill:

- incoming version > canonical → may enter normal review/PR flow;
- incoming version == canonical → compare content normally;
- incoming version < canonical → reject replacement unless explicit documented rollback.

Copying a file never grants it authority. Merge to `main` is the promotion event.

## Scope

This change modifies Hermes infrastructure only. It does **not** restore or edit any business-domain skill content in this PR.

## Non-goals

- Do not route directly to Library versions.
- Do not auto-select the highest version across branches.
- Do not keep multiple runtime versions of one skill.
- Do not modify Story, Promo, or other business methodology rules here.

## Verification contract

The change is acceptable only when:

1. unit/regression tests prove downgrade detection;
2. registry includes version fields;
3. router documents canonical resolution and mismatch stop behavior;
4. workflow runs validation using the PR base as downgrade baseline;
5. `python3 scripts/validate-skills.py --write-registry` still succeeds for the accepted repository state;
6. no secrets, customer-private content, or local absolute paths are introduced.
