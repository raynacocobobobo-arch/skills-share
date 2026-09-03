---
name: hermes-creative-chongqing-time-atmosphere
description: Use when creating, revising, or reviewing environment atmosphere images, core episode spaces, environment masters, setting visualizations, or Seedance-ready environment prompts for 《重庆时间》, especially when the request says “重庆时间，按设定出图”, “核心空间”, “场景气氛图”, “环境母图”, or references EP01–EP10.
version: 1.0.0
triggers:
  - 重庆时间，按设定出图
  - 重庆时间
  - 按设定出图
  - 核心空间
  - 核心剧情空间
  - 场景气氛图
  - 环境母图
  - 大场景
  - EP01
  - EP02
  - EP03
  - EP04
  - EP05
  - EP06
  - EP07
  - EP08
  - EP09
  - EP10
---

# Hermes Creative — Chongqing Time Atmosphere

Use the live 《重庆时间》 project repository as the authority for scene facts and visual production rules. This skill is a router/executor for environment atmosphere work; it must not freeze project Canon inside the skill itself.

## Live project authority

Project repository:

> `raynacocobobo-arch/lora`

Project root:

> `重庆时间/`

Always start from:

> `重庆时间/ACTIVE-DOCS-INDEX.md`

Then read only the active files required by the current task. Read [the source map](references/chongqing-time-source-map.md) for the repository contract.

**Do not rely on an embedded stale canon summary.** If GitHub or the current project repository cannot be read, report the missing source instead of silently reconstructing Canon from memory.

## Core workflow

For major environment work, follow the live `重庆时间/SCENE-PROMPT-TEMPLATE-V3.md`.

The production sequence is:

> **Canon → shot mode → dominant action geography → scene identity → parent space → narrative affordances → composition → active visual style → Seedance structural compression → prompt/generation → QC.**

### Shot mode

When the user asks for `核心空间`, `场景气氛图`, `环境母图`, `大场景`, or equivalent, default to a **wide atmosphere master**, not a local device room by default. Use the project default aspect ratio from the live visual workflow; currently major environment masters are normally 2.35:1.

Only switch to a local functional shot when the user explicitly asks for a `局部`, `节点`, `设备`, `机房`, `操作位`, or `特写`.

### Core-space gate

For an episode core space, identify the **dominant action geography** rather than the most memorable named node. Check:

- runtime coverage;
- dominant physical-action coverage;
- state-change coverage.

A relay, controller, machine, or room may be a key node without being the episode's atmosphere-master space.

### Identity and action gate

Before prompting, lock:

- parent-space direction and entry/exit logic;
- 2–4 large physical identity anchors that survive removal of signage;
- structures/surfaces the later episode action will actually use.

If changing the sign could turn the frame into another generic district, reject the concept.

## Composition

Choose a composition family intentionally from the live V3 method. Strong options include axial/center-symmetrical, near-symmetrical with one controlled break, oblique structural panorama, and layered cross-space wide.

Center symmetry is useful for procedural/infrastructural spaces, but it is not a universal default.

## Seedance rule

Seedance optimization means **structural compression**, not indiscriminate simplification.

Preserve large silhouette, route, void, structural frames, identity anchors, major repair landmarks, light direction, and large cast-shadow masses. Merge repeated rails, catwalks, windows, small bridges, pipes, lamps, signs, and distant machinery into fewer stable groups.

> **删噪声，不删身份；合并结构，不削平空间。**

## Ask vs proceed

Ask the user only when the unresolved choice changes Canon geography, episode blocking, major object/function, meaningful orientation, reveal timing, or meaningful time-of-day/local-time state.

For ordinary art direction—camera distance within the chosen shot mode, minor prop placement, detail reduction, sign placement, and Seedance cleanup—proceed from the active project method and visual style without unnecessary clarification.

## Routing boundaries

- If the user is changing episode story, Canon, character arc, or screenplay structure, add/route to `hermes-creative-ai-short-drama` as the story workflow.
- If the task is specifically an environment atmosphere/master image or its prompt for 《重庆时间》, this skill remains primary.
- If the user asks only for analysis/prompt text, do not generate an image.
- If the user explicitly asks to generate the image and an image-generation tool is available, generate from the resolved live Canon and current visual method.

## Acceptance tests

Before accepting a major atmosphere master, apply the live V3 QC, including:

1. **Thumbnail:** main mass, void, route, and light direction still read small.
2. **Relabel:** location still reads correctly without signage.
3. **Story-action:** episode action can occur in the space without redesigning it.
4. **Seedance-motion:** repeated high-frequency structures are compressed enough to avoid obvious flicker/mutation risk.
