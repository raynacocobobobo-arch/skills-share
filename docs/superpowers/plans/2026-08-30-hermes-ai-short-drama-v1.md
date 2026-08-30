# Hermes AI Short Drama V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `hermes-creative-ai-short-drama` as a reuse-first Hermes Skill that converts an original serialized short-drama idea into coherent, resumable, shot-level Seedance-oriented production packs with continuity, QA, retakes, and next-episode state inheritance.

**Architecture:** Preserve the repository's existing `SKILL.md + references + templates + workflows` convention. Assemble narrative/state logic primarily from Hao0321, continuity/shot logic from MrMO0802, generation-segment logic from zouchenzhen, and production/QC state from ouyangevan; add only minimal Hermes routing and contract glue. V1 is planning/orchestration-first and hands media generation/editing to downstream executors.

**Tech Stack:** Markdown Skills, JSON templates/contracts, existing Hermes router/registry conventions, deterministic text/JSON validation where existing repository tooling permits.

**Spec:** `docs/superpowers/specs/2026-08-30-hermes-ai-short-drama-v1-design.md`

## Global Constraints

- Reuse-first: copy/adapt legally compatible proven material before writing new logic.
- Every reused/adapted source fragment must be recorded in `references/source-map.md`.
- License-restricted sources are architecture-only unless their license permits the intended reuse.
- Keep `hermes-creative-ai-short-drama` independent from `hermes-creative-digital-human`.
- Do not add web UI, database, billing, media API clients, FFmpeg automation, distributed queues, LoRA, or publishing automation in V1.
- Do not redesign `manifests/skill-registry.json`; make only the minimum registration change required by existing repository conventions.
- Missing assets/media must yield `BLOCKED`, never fabricated completion.
- Default pilot is 3–5 episodes; do not auto-expand an entire season before pilot validation.
- A Shot is an editing/narrative unit; a Generation Segment is a model-call unit.
- Default Seedance-oriented Generation Segment duration is 4–15 seconds, subject to verified model capability.
- P0 failures require targeted retakes; do not regenerate an entire episode for an isolated shot failure.

---

## File Map

### New Skill

- `plugins/hermes-skills/skills/hermes-creative-ai-short-drama/SKILL.md` — orchestration, trigger boundaries, modes, workflow ownership, status rules.
- `references/source-map.md` — provenance/license/treatment map for every imported or adapted source.
- `references/story-architecture.md` — Series Bible, pilot, season/episode structure, hooks, dominant turn, state delta, continuation capsule.
- `references/episode-contract.md` — Episode Card and screenplay output contract.
- `references/continuity-rules.md` — geography, screen direction, character/prop/clue/action state.
- `references/storyboard-rules.md` — continuity-first Shot Spec and one-visible-action rule.
- `references/generation-segment-rules.md` — shot-to-segment grouping and generation-mode routing.
- `references/seedance-rules.md` — Seedance-oriented prompt contract, references, NOT constraints and duration behavior.
- `references/qa-rules.md` — P0/P1/P2 review and retake policy.
- `templates/series-bible.md` — persistent series template.
- `templates/episode-card.md` — episode narrative/state template.
- `templates/continuity-state.json` — machine-readable continuity state example/contract.
- `templates/storyboard.json` — machine-readable Shot Spec example/contract.
- `templates/production-pack.json` — generation segments, assets, prompts, status and handoff.
- `templates/retake-patch.json` — targeted retry contract.
- `workflows/create-series.md` — idea through Series Bible/pilot setup.
- `workflows/create-episode.md` — Episode Card through screenplay/state delta.
- `workflows/screenplay-to-shots.md` — continuity compile and storyboard.
- `workflows/shots-to-seedance.md` — asset/keyframe plan, generation segments and Seedance prompt pack.
- `workflows/review-and-retake.md` — QA, targeted retake, acceptance and state update.

### Existing Files, Minimal Changes Only

- `manifests/web-chatgpt-router.md` — add short-drama routing entry following existing format.
- `manifests/skill-registry.json` — add one registry entry only if required by current repository convention.

---

### Task 1: Build the Source-to-Target Provenance Map

**Files:**
- Create: `plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/source-map.md`

**Interfaces:**
- Consumes: public source repositories and the V1 design spec.
- Produces: authoritative provenance decisions used by all later tasks.

- [ ] **Step 1: Verify source licenses and exact reusable files**

Inspect at minimum:
- `Hao0321/ai-short-drama`
- `MrMO0802/short-drama-agent`
- `zouchenzhen/short-drama-prompt-director`
- `ouyangevan/codex-short-drama-pipeline-skill`

For each, record repository URL, license file, exact source paths, and whether treatment is `copy`, `adapt`, or `architecture-only`.

- [ ] **Step 2: Write the provenance table**

Required columns:

```markdown
| Source repo | Source path | License | Target file | Treatment | Retain | Remove | Local changes |
```

Every planned target reference/workflow must have at least one provenance row or be explicitly labeled `Hermes glue`.

- [ ] **Step 3: Self-check for unsupported copying**

Search the map for every `copy` row and verify the license explicitly permits repository reuse. Downgrade uncertain rows to `adapt` or `architecture-only`.

- [ ] **Step 4: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/source-map.md
git commit -m "docs: map AI short drama skill sources"
```

---

### Task 2: Assemble Narrative and Episode Contracts

**Files:**
- Create: `references/story-architecture.md`
- Create: `references/episode-contract.md`
- Create: `templates/series-bible.md`
- Create: `templates/episode-card.md`

**Interfaces:**
- Consumes: provenance-approved Hao0321 narrative/state material.
- Produces: Series Bible and Episode Card contracts consumed by continuity and storyboard tasks.

- [ ] **Step 1: Assemble `story-architecture.md`**

Retain/adapt the proven concepts:
- premise contract
- character bible
- world/system rules
- entity registry
- reveal ladder
- antagonist ladder
- payoff debt ledger
- 3–5 episode pilot-first rule
- one dominant turn per episode
- Cold Open -> Pressure -> Turn -> Payoff/Progress -> Cliffhanger -> State Delta
- continuation capsule

Remove media-generator-specific dependencies not needed by Hermes V1.

- [ ] **Step 2: Assemble `episode-contract.md`**

Require this minimum Episode Card contract:

```yaml
episode_id: EP01
opening_hook: ""
dominant_turn: ""
core_conflict: ""
payoff_or_progress: ""
ending_cliffhanger: ""
state_delta: []
continuation_capsule: ""
```

State that screenplay prose is downstream of this card and may not contradict approved persistent series state.

- [ ] **Step 3: Create `series-bible.md` template**

Sections must include premise, audience promise, characters, world rules, recurring locations, entity IDs, reveal ladder, antagonist ladder, payoff debt ledger, and current canonical state.

- [ ] **Step 4: Create `episode-card.md` template**

Include the Episode Card fields plus dependencies from previous episode and unresolved debts/clues.

- [ ] **Step 5: Contract review**

Manually verify that EP02 can be written from `series-bible.md + EP01 state_delta + continuation_capsule` without rereading an entire season transcript.

- [ ] **Step 6: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/story-architecture.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/episode-contract.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/series-bible.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/episode-card.md
git commit -m "feat: add short drama narrative contracts"
```

---

### Task 3: Assemble Continuity and Shot Contracts

**Files:**
- Create: `references/continuity-rules.md`
- Create: `references/storyboard-rules.md`
- Create: `templates/continuity-state.json`
- Create: `templates/storyboard.json`

**Interfaces:**
- Consumes: Episode Card + screenplay + approved entity IDs.
- Produces: continuity state and Shot Specs consumed by generation-segment compilation.

- [ ] **Step 1: Assemble continuity rules from provenance-approved MrMO material**

Require:
- scene geography
- character state
- costume/injury state only when continuity-relevant
- screen direction
- prop/evidence state
- clue reveal state
- action causality
- transition motivation

Explicitly prohibit recording irrelevant descriptive trivia as persistent state.

- [ ] **Step 2: Define Shot Spec**

Every shot must contain:

```json
{
  "shot_id": "EP01-SC01-SH01",
  "scene_id": "SC01",
  "duration_target_sec": 2.5,
  "framing": "medium",
  "camera_intent": "static reaction",
  "start_state": {},
  "visible_action": "",
  "end_state": {},
  "next_shot_connection": "",
  "reference_assets": [],
  "tail_frame_need": false,
  "prohibited_changes": [],
  "information_gain": ""
}
```

- [ ] **Step 3: Encode hard rules**

Reject a Shot Spec when:
- it contains multiple unrelated visible actions
- start/end state is absent
- next-shot connection is absent
- a required prop/character asset is unknown
- screen direction contradicts the continuity state without an explicit re-establishing shot

- [ ] **Step 4: Create templates**

`continuity-state.json` must include at least two characters, one recurring location, and one continuity-sensitive prop/clue so the example exercises the contract.

`storyboard.json` must contain at least three connected shots demonstrating state transition.

- [ ] **Step 5: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/continuity-rules.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/storyboard-rules.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/continuity-state.json plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/storyboard.json
git commit -m "feat: add continuity-first storyboard contracts"
```

---

### Task 4: Assemble Generation Segment and Seedance Contracts

**Files:**
- Create: `references/generation-segment-rules.md`
- Create: `references/seedance-rules.md`
- Create: `templates/production-pack.json`

**Interfaces:**
- Consumes: valid Shot Specs + asset/keyframe status.
- Produces: model-call Generation Segments and Seedance-ready production pack.

- [ ] **Step 1: Define Shot vs Segment boundary**

State explicitly:
- Shot = narrative/editing unit.
- Generation Segment = model-call unit.
- A Segment may contain one or more adjacent compatible shots.
- Do not combine shots when identity, geography, action complexity, or transition risk makes one-call generation unsafe.

- [ ] **Step 2: Assemble generation-mode routing**

Allowed values:

```text
first_frame
first_last_frame
reference_images
reference_video
text_to_video
```

Routing heuristics:
- stable dialogue/reaction -> `first_frame`
- explicit A-to-B visual state -> `first_last_frame`
- recurring/multi-character identity-critical shot -> `reference_images`
- source-motion transformation when supported -> `reference_video`
- non-identity-critical establishing/spectacle shot -> `text_to_video`

- [ ] **Step 3: Assemble Seedance prompt contract**

Each Segment must carry:
- scene snapshot
- shot IDs
- target duration
- references
- fixed continuity facts
- visible action(s) compatible with the Segment
- ending state
- camera behavior
- sound/dialogue policy when relevant
- NOT constraints

Do not ask the video model to render complex readable Chinese UI/text; reserve it for post overlays.

- [ ] **Step 4: Create `production-pack.json`**

Include:
- episode metadata
- asset status
- keyframe requirements
- generation segments
- prompts
- blocked reasons
- generation/take log placeholders
- handoff status

Use status enum:

```json
["READY", "BLOCKED", "NEEDS_REVIEW", "PASS"]
```

- [ ] **Step 5: Validate the 4–15 second default**

Document it as a Seedance-oriented default, not a universal truth. Require capability re-check when the downstream model changes.

- [ ] **Step 6: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/generation-segment-rules.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/seedance-rules.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/production-pack.json
git commit -m "feat: add short drama generation segment contracts"
```

---

### Task 5: Assemble QA and Targeted Retake Contracts

**Files:**
- Create: `references/qa-rules.md`
- Create: `templates/retake-patch.json`

**Interfaces:**
- Consumes: generated-media review observations or dry-run validation failures.
- Produces: PASS decision or targeted Retake Patch.

- [ ] **Step 1: Define severity rules**

P0 mandatory retake:
- wrong identity
- unexplained costume/state reset
- broken scene geography/screen direction
- missing/reset critical prop
- incorrect story information/dialogue
- broken action causality

P1 normally retake:
- materially weak performance
- inappropriate camera motion/framing
- pacing failure
- obvious light/visual discontinuity

P2 optional polish:
- minor composition/atmosphere issues that do not break story or continuity

- [ ] **Step 2: Define targeted retake contract**

```json
{
  "shot_or_segment_id": "EP01-SC01-SG02",
  "severity": "P0",
  "preserve": ["character_identity", "costume", "scene", "dialogue"],
  "fix": ["prop_state"],
  "reason": "Phone disappears before the reveal insert.",
  "retry_count": 1
}
```

- [ ] **Step 3: Add anti-randomization rule**

A retry must preserve all accepted variables unless the failure diagnosis explicitly identifies them as targets for change.

- [ ] **Step 4: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/references/qa-rules.md plugins/hermes-skills/skills/hermes-creative-ai-short-drama/templates/retake-patch.json
git commit -m "feat: add short drama QA and retake contracts"
```

---

### Task 6: Assemble the Five Workflows

**Files:**
- Create: `workflows/create-series.md`
- Create: `workflows/create-episode.md`
- Create: `workflows/screenplay-to-shots.md`
- Create: `workflows/shots-to-seedance.md`
- Create: `workflows/review-and-retake.md`

**Interfaces:**
- Consumes: contracts from Tasks 2–5.
- Produces: executable operator/agent procedures used by `SKILL.md`.

- [ ] **Step 1: Write `create-series.md`**

Exact stage order:

```text
Greenlight -> Series Bible -> 3–5 episode pilot outline -> persist canonical state
```

Stop expansion when the premise lacks escalation runway, production repeatability, or sufficient pilot differentiation.

- [ ] **Step 2: Write `create-episode.md`**

Exact stage order:

```text
load canonical state -> Episode Card -> screenplay -> state delta draft -> continuation capsule draft
```

Do not finalize the state delta until production/story review confirms what actually occurred in the episode.

- [ ] **Step 3: Write `screenplay-to-shots.md`**

Exact stage order:

```text
screenplay -> asset inventory -> continuity compile -> shot breakdown -> Shot Spec validation
```

- [ ] **Step 4: Write `shots-to-seedance.md`**

Exact stage order:

```text
valid shots -> asset/keyframe readiness -> segment grouping -> generation-mode selection -> Seedance prompt pack -> READY/BLOCKED
```

- [ ] **Step 5: Write `review-and-retake.md`**

Exact stage order:

```text
media review -> P0/P1/P2 -> PASS or Retake Patch -> retry -> accept take -> update episode state
```

- [ ] **Step 6: Cross-workflow review**

Verify every workflow names the exact artifact it consumes and produces. Remove duplicated narrative/continuity rules and link to the authoritative reference instead.

- [ ] **Step 7: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/workflows
git commit -m "feat: add AI short drama workflows"
```

---

### Task 7: Assemble the Hermes Orchestrator SKILL.md

**Files:**
- Create: `plugins/hermes-skills/skills/hermes-creative-ai-short-drama/SKILL.md`

**Interfaces:**
- Consumes: all V1 references/templates/workflows.
- Produces: one routable Hermes Skill with clear mode selection and handoffs.

- [ ] **Step 1: Follow the existing Hermes frontmatter/style convention**

Use name:

```yaml
name: hermes-creative-ai-short-drama
```

Description must clearly distinguish AI serialized drama from digital-human portrait/compositing tasks.

- [ ] **Step 2: Define modes without duplicating reference content**

Minimum modes:
- Greenlight
- Series
- Episode
- Storyboard
- Produce
- Review

Route each mode to one or more of the five workflows.

- [ ] **Step 3: Define hard boundaries**

Include:
- no digital-human/LoRA routing
- no claim that media exists without actual executor output
- missing required asset -> BLOCKED
- pilot-first default
- preserve canonical approved state
- targeted retakes

- [ ] **Step 4: Define default full-chain behavior**

When the user asks to make an AI short drama end-to-end, run:

```text
create-series -> create-episode -> screenplay-to-shots -> shots-to-seedance -> review-and-retake when media is available
```

If media execution is unavailable, stop at a complete `production-pack.json` handoff and report `READY` or `BLOCKED` accurately.

- [ ] **Step 5: Commit**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama/SKILL.md
git commit -m "feat: assemble Hermes AI short drama skill"
```

---

### Task 8: Add Minimal Router and Registry Integration

**Files:**
- Modify: `manifests/web-chatgpt-router.md`
- Modify only if required: `manifests/skill-registry.json`

**Interfaces:**
- Consumes: finalized Skill name and trigger boundary.
- Produces: ChatGPT/Codex discoverability without changing unrelated routing.

- [ ] **Step 1: Inspect current router/registry format before editing**

Do not infer schema from memory. Follow current file conventions exactly.

- [ ] **Step 2: Add routing triggers**

Cover terms such as:
- AI短剧
- 连载短剧
- AI爽剧
- 一分钟短剧
- 分集短剧
- 剧本转分镜
- 短剧 Seedance 生产包

Add an explicit negative boundary against digital-human/LoRA/compositing requests.

- [ ] **Step 3: Make the minimum registry change**

If registration is still required, add exactly one valid entry. Do not refactor or regenerate unrelated registry content.

- [ ] **Step 4: Verify diff scope**

Run:

```bash
git diff -- manifests/web-chatgpt-router.md manifests/skill-registry.json
```

Expected: only the new short-drama route/entry changes.

- [ ] **Step 5: Commit**

```bash
git add manifests/web-chatgpt-router.md manifests/skill-registry.json
git commit -m "feat: route Hermes AI short drama skill"
```

---

### Task 9: Run the 3–5 Episode Benchmark Pilot

**Files:**
- Create benchmark artifacts under the repository's existing test/fixture convention; if no convention exists, use `plugins/hermes-skills/skills/hermes-creative-ai-short-drama/examples/pilot-benchmark/`.
- Modify V1 files only when benchmark failures expose a contract defect.

**Interfaces:**
- Consumes: complete V1 Skill.
- Produces: evidence that the chain works before declaring V1 ready.

- [ ] **Step 1: Create one original benchmark premise**

Requirements:
- 3–5 pilot episodes
- ~1 minute target per episode
- two recurring characters minimum
- one recurring location minimum
- one continuity-sensitive prop/clue
- a cliffhanger/state delta between episodes

- [ ] **Step 2: Run EP01 through the full planning chain**

Expected artifacts:
- Series Bible
- Episode Card
- screenplay
- continuity state
- storyboard
- production pack

- [ ] **Step 3: Verify EP02 inheritance**

Check that EP02 correctly inherits EP01's state delta, clue state, prop state, and unresolved payoff debt without inventing resets.

- [ ] **Step 4: Simulate one P0 failure**

Example: critical phone/prop disappears in one generated segment.

Expected: create a Retake Patch targeting only the affected shot/segment while preserving accepted identity, costume, geography, dialogue and other segments.

- [ ] **Step 5: Simulate a missing asset**

Remove/mark one required character or keyframe asset as missing.

Expected: affected segment status becomes `BLOCKED`; the Skill must not claim generated media exists.

- [ ] **Step 6: Review benchmark against acceptance criteria**

PASS only if:
- state inheritance works
- all shots have start/end/connection fields
- segments reference valid shots/assets
- P0 creates targeted retake
- missing asset blocks correctly
- production pack is sufficient for downstream executor handoff

- [ ] **Step 7: Commit benchmark evidence**

```bash
git add plugins/hermes-skills/skills/hermes-creative-ai-short-drama
git commit -m "test: validate AI short drama pilot workflow"
```

---

### Task 10: Final Verification and PR

**Files:**
- Review all files changed by Tasks 1–9.

**Interfaces:**
- Consumes: benchmark-passing branch.
- Produces: reviewable PR ready for user merge decision.

- [ ] **Step 1: Verify no scope leakage**

Confirm no changes were made to `hermes-creative-digital-human` and no unrelated registry/router sections were rewritten.

- [ ] **Step 2: Verify provenance completeness**

Every copied/adapted source fragment must be traceable through `references/source-map.md`.

- [ ] **Step 3: Verify JSON templates parse**

Run a JSON parser against:
- `templates/continuity-state.json`
- `templates/storyboard.json`
- `templates/production-pack.json`
- `templates/retake-patch.json`

Expected: all parse successfully.

- [ ] **Step 4: Verify contract terminology**

Search for inconsistent aliases. Canonical terms are:
- Series Bible
- Episode Card
- Continuity State
- Shot Spec
- Generation Segment
- Production Pack
- Retake Patch
- State Delta
- Continuation Capsule

- [ ] **Step 5: Inspect final diff and commit history**

Expected: focused commits matching the tasks above; no unrelated edits.

- [ ] **Step 6: Open PR**

PR description must summarize:
- reuse-first source composition
- V1 scope/non-scope
- benchmark result
- router/registry impact
- known V1 limitations

Do not merge automatically; leave final merge decision to the user.
