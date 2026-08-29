# Xiaohongshu Digital Human Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the over-engineered digital-human pipeline with a lightweight staged/direct-entry Xiaohongshu production workflow.

**Architecture:** Keep two skills only: `hermes-digital-human-character-card` for optional staged identity setup, and `hermes-creative-digital-human` for direct Xiaohongshu content production. Add one supporting pose/shot preset library. Normal generation stays simple; source re-anchoring and atomic split rendering are recovery paths only.

**Tech Stack:** Markdown skills, Python unittest contract tests, existing GitHub skill-registry auto-sync.

**Spec:** Current conversation requirements: staged face→body→outfit flow; direct entry from any stage; real-scene compositing; outfit/pose/shot modules; Xiaohongshu pose presets; original user photos remain primary identity evidence.

## Global Constraints

- Do not create a new global registry or session-state system.
- Do not require users to complete earlier steps when enough source material exists for the requested later step.
- Default identity setup is semi-automatic: face sheet first, then ask whether to continue to body sheet.
- Content production may start directly from face + full-body + wardrobe/pose/scene inputs.
- Original user images remain primary identity evidence; generated outputs do not silently replace them.
- Pose/shot presets are optional accelerators, not mandatory IDs the user must memorize.
- Atomic one-view rendering is fallback recovery for failed three-view generation, not the normal path.

---

### Task 1: Replace heavy identity contracts with staged identity setup

**Files:**
- Modify: `plugins/hermes-skills/skills/hermes-digital-human-character-card/SKILL.md`
- Modify: `tests/test_digital_human_character_card_contract.py`
- Delete: `tests/test_digital_human_identity_anchor_contract.py`
- Delete: `tests/test_digital_human_master_reattachment_contract.py`
- Delete: `tests/test_digital_human_session_state_contract.py`
- Delete: `tests/test_digital_human_face_repair_contract.py`
- Delete: `tests/test_digital_human_recovery_contract.py`

**Interfaces:**
- Consumes: uploaded face/full-body SOURCE and optional factual profile.
- Produces: optional face three-view sheet, optional body three-view sheet, and a clean handoff to content production.

- [ ] **Step 1: Write failing contract tests** for staged default, direct face/body entry, user confirmation between face/body, source priority, and atomic fallback only after failure.
- [ ] **Step 2: Run validation** and confirm the new contract fails against the current heavy/atomic default skill.
- [ ] **Step 3: Rewrite the skill minimally** so the normal path is face sheet → ask → body sheet → ask for outfit/scene, while allowing direct face-only/body-only invocation.
- [ ] **Step 4: Remove obsolete heavy contract tests** that enforce anchors, session-state registries, mandatory preflight, and face-repair subsystems.
- [ ] **Step 5: Run validation** and confirm the identity contracts pass.

### Task 2: Refocus creative digital human on Xiaohongshu production

**Files:**
- Modify: `plugins/hermes-skills/skills/hermes-creative-digital-human/SKILL.md`
- Create: `plugins/hermes-skills/skills/hermes-creative-digital-human/references/xhs-pose-shot-library.md`
- Create: `tests/test_digital_human_xhs_workflow_contract.py`

**Interfaces:**
- Consumes: any sufficient combination of identity face/full-body references, outfit references, pose references, scene photos, and natural-language shot requests.
- Produces: single Xiaohongshu images or coherent 4–6 image sets with stable identity, wardrobe, pose, camera, and scene intent.

- [ ] **Step 1: Write failing contract tests** for direct entry, four modules (`IDENTITY / OUTFIT / POSE / SCENE` plus shot control), real-scene compositing, pose presets, set generation, and source re-anchoring.
- [ ] **Step 2: Run validation** and confirm failure against V2.4.
- [ ] **Step 3: Rewrite `hermes-creative-digital-human`** as a concise Xiaohongshu production skill with staged and direct modes.
- [ ] **Step 4: Add pose/shot reference library** with practical lifestyle, street, cafe, travel, mirror-selfie, walking, seated, bag, coffee, phone, and camera poses plus framing presets.
- [ ] **Step 5: Run full validation** and confirm all repository tests and registry regeneration pass.

### Task 3: Final verification and PR cleanup

**Files:**
- Modify PR #35 metadata only.

- [ ] **Step 1: Compare branch to main** and ensure changes are limited to the two skills, pose/shot reference, focused tests, plan, and auto-synced registry.
- [ ] **Step 2: Run fresh GitHub Actions validation** on the final head and require `success`.
- [ ] **Step 3: Update PR #35 title/body** to describe the lightweight staged/direct Xiaohongshu workflow instead of the abandoned default atomic-render design.
