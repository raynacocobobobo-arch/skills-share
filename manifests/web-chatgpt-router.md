# Hermes Skills Router for ChatGPT Web

This file is the routing entry point for using Hermes skills from ChatGPT Web
through the GitHub connection. It is an index, not the full repository rulebook.

## Execution Rule

When the user says **“请按 Hermes skill 路由执行这个任务”**, or otherwise asks to use Hermes skills:

1. Read this file first.
2. Match the task to one or more skills below.
3. Resolve the matched skill path from this table or `manifests/skill-registry.json`.
4. Before answering or executing, read the matched `SKILL.md`.
5. Follow that `SKILL.md` as the authoritative workflow.
6. Read required `references/`, `shared/`, or supporting skills only when the matched skill or current task requires them.
7. If a required GitHub file cannot be read, say which file is unavailable. Do not silently replace it with an approximate workflow.
8. If several skills match, load the primary workflow skill first, then load supporting skills only when needed.
9. Re-check routing whenever the task changes materially during a follow-up turn.

## Task-object ambiguity guard

**Skill routing and task-object resolution are separate decisions.**

ChatGPT may infer the correct skill from the user's task type, but it must **not** infer the current task object merely because a historical project, file, or conversation is semantically similar.

If the user specifies the task type but does not identify the object to operate on — for example:

- “帮我修改一个宣传片”
- “帮我看看一个方案”
- “帮我改个文档”
- “分析一个项目”

then the router may load the relevant skill, but must stop before selecting a historical object or executing edits.

### Forbidden object inference

When the current object is not uniquely identified, do **not** choose it from:

- previous conversations;
- saved memory or user profile context;
- the most recent project;
- file-library search ranking;
- recently uploaded or recently modified files;
- semantic similarity to prior work;
- “most likely” historical context.

Historical context may help interpret **how** to work, but must not silently decide **what current artifact/project** the user means.

### Object may be treated as resolved only when at least one condition is met

1. The user identifies the project, file, artifact, URL, or other target in the current request.
2. The user uploads or attaches the target in the current conversation and the intended operation is clear.
3. The user makes an explicit continuation reference such as “继续刚才那个”“接着上一版”“就是博川那个”, and that reference resolves uniquely in the active conversation.
4. The active conversation already has exactly one clearly established working object, and the user's follow-up unambiguously refers to it.

If none applies, finish the Hermes skill routing/read step, state that the task object is not yet identified, and wait for the user's target/materials. **Do not search the library or prior chats in order to guess the object.**

This guard has priority over convenience-oriented context reuse. Routing can be inferred; the current task object cannot be guessed.

Primary skill root:

`plugins/hermes-skills/skills/`

Workflow root:

`plugins/hermes-workflows/workflows/`

Shared methodology mirrors:

`shared/`

---

## Routing table

### 1. Business / marketing

#### Document review
Use when the user asks to review, annotate, revise, mark up, or visually comment on a Word document, proposal, contract, script, resume, or report.

- Skill: `doc-reviewer`
- Path: `plugins/hermes-skills/skills/hermes-business-doc-reviewer/SKILL.md`

#### Marketing analysis / marketing copilot
Use for marketing analysis, positioning, STP, 4P, pricing, customer acquisition, channels, brand, competition, value proposition, wedding-video marketing, video-production business marketing, or general marketing diagnosis.

- Skill: `marketing-copilot`
- Path: `plugins/hermes-skills/skills/hermes-business-marketing-copilot/SKILL.md`
- Required methodology when the skill calls for it: `plugins/hermes-skills/skills/hermes-business-marketing-copilot/references/市场营销.md`
- Shared mirror: `shared/marketing-methodology/市场营销.md`

#### Full marketing plan
Use when the user explicitly wants a marketing plan, go-to-market plan, acquisition plan, promotion plan, regional expansion plan, or an executable marketing strategy document.

- Skill: `marketing-plan`
- Path: `plugins/hermes-skills/skills/hermes-business-marketing-plan/SKILL.md`
- Required methodology: `plugins/hermes-skills/skills/hermes-business-marketing-plan/references/市场营销.md`
- Required methodology: `plugins/hermes-skills/skills/hermes-business-marketing-plan/references/Good_Strategy_Bad_Strategy_Full.md`

Routing note: use `marketing-copilot` for analysis/advice; use `marketing-plan` when the deliverable is a complete plan.

---

### 2. Document / transcript editing

#### Chinese document editing
Use for transcript cleanup, filler-word deletion, typo cleanup, news-release edits, difference marking, deletion-line revisions, or `python-docx` document processing.

- Skill: `document-editing`
- Path: `plugins/hermes-skills/skills/hermes-content-document-editing/SKILL.md`

#### Filmed-video transcript cleanup
Use when the source is already-recorded speech/audio and edits must preserve sync, especially when the user says only deletion is allowed.

- Skill: `transcript-cleanup`
- Path: `plugins/hermes-skills/skills/hermes-film-transcript-cleanup/SKILL.md`

Routing note: prefer `transcript-cleanup` for recorded-video/audio word-stripping tasks; use `document-editing` for broader Chinese document editing workflows.

---

### 3. Film / video creation

#### AI story short film workflow
Use when the user wants to make an AI story short, AI microfilm, AI film experiment, or to turn one idea into a short narrative video production pipeline.

- Workflow: `ai-short-film-production`
- Path: `plugins/hermes-workflows/workflows/ai-short-film-production/WORKFLOW.md`
- Supporting phases: `plugins/hermes-workflows/workflows/ai-short-film-production/phases.md`
- Supporting checkpoints: `plugins/hermes-workflows/workflows/ai-short-film-production/checkpoints.md`
- Templates: `plugins/hermes-workflows/workflows/ai-short-film-production/templates/`

Routing note: load this workflow before individual film skills when the request is an end-to-end AI short-film pipeline. It should orchestrate `故事片创作`, `hermes-film-ai-production`, `影视分镜`, and `AI绘画提示词`. Do not generate prompts before Story Lock.

#### Corporate / brand / product promotional film
Use for enterprise films, brand films, product films, investment-promotion films, government/corporate briefing films, promotional-film copywriting, structure, creative direction, or full promotional-film workflows.

- Skill: `宣传片创作`
- Path: `plugins/hermes-skills/skills/hermes-film-宣传片创作/SKILL.md`
- Bundled methodology: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/方法论参考/`
- Bundled AI excerpts: `plugins/hermes-skills/skills/hermes-film-宣传片创作/references/AI专用/`
- Shared mirrors: `shared/film-methodology/方法论参考/` and `shared/film-methodology/AI专用/`

**Existing Word revision note:** if the content task is promotional-film work but the user later says “在这个 Word/版本上改”, keep `宣传片创作` as the primary content skill and add `doc-reviewer` as the document-preservation/output skill.

#### Narrative film / screenplay / short film
Use for story films, screenplays, short-film scripts, microfilms, character arcs, dramatic conflict, story structure, scene writing, or narrative-film creation.

- Skill: `故事片创作`
- Path: `plugins/hermes-skills/skills/hermes-film-故事片创作/SKILL.md`
- Mandatory methodology when required by the skill: `plugins/hermes-skills/skills/hermes-film-故事片创作/references/方法论参考/`
- Mandatory AI excerpts when required by the skill: `plugins/hermes-skills/skills/hermes-film-故事片创作/references/AI专用/`
- Additional integrated methodology: `plugins/hermes-skills/skills/hermes-film-故事片创作/references/影视方法论已整合/`
- Shared mirrors: `shared/film-methodology/`

Supporting skill when final screenplay formatting is needed:

- `plugins/hermes-skills/skills/hermes-film-中文剧本格式/SKILL.md`

#### General film storyboard
Use for shot lists, storyboards, dialogue scenes, action scenes, visual coverage, camera blocking, shot rhythm, and executable filming plans.

- Skill: `影视分镜`
- Path: `plugins/hermes-skills/skills/hermes-film-影视分镜/SKILL.md`
- Supporting references: `plugins/hermes-skills/skills/hermes-film-影视分镜/references/动作分镜.md`
- Supporting references: `plugins/hermes-skills/skills/hermes-film-影视分镜/references/对话分镜.md`

#### Storyboard correction / pre-shoot verification
Use when the user wants to verify facts, locations, workflows, equipment, or scene accuracy before producing/fixing a storyboard.

- Skill: `storyboard-revision`
- Path: `plugins/hermes-skills/skills/hermes-film-storyboard-revision/SKILL.md`

#### Petrochemical / industrial storyboard
Use for petrochemical, oilfield, industrial, state-owned-enterprise, factory, drilling, refining, or other industrial-film storyboard work where real scenes and shootability dominate.

- Skill: `石化简易分镜`
- Path: `plugins/hermes-skills/skills/hermes-film-石化简易分镜/SKILL.md`

#### Chinese screenplay formatting
Use when the task is primarily screenplay formatting, scene-heading formatting, dialogue formatting, or standard Chinese screenplay layout.

- Skill: `中文剧本格式`
- Path: `plugins/hermes-skills/skills/hermes-film-中文剧本格式/SKILL.md`

#### AI image prompt from storyboard
Use when converting a shot/storyboard description into a Chinese AI-image prompt, including portrait and scene prompts.

- Skill: `AI绘画提示词`
- Path: `plugins/hermes-skills/skills/hermes-film-AI绘画提示词/SKILL.md`

#### Content tags for film/project knowledge base
Use when extracting standardized `#` tags from promotional-film copy, scripts, storyboards, or project documents.

- Skill: `内容标签`
- Path: `plugins/hermes-skills/skills/hermes-film-内容标签/SKILL.md`

Common film chaining:

- Promotional film: `宣传片创作` → `影视分镜` when detailed shots are required → `AI绘画提示词` when visual-generation prompts are required → `内容标签` when archiving/tagging is required.
- Promotional-film existing Word revision: `宣传片创作` (content) + `doc-reviewer` (preserve/edit the original Word copy).
- Narrative film: `故事片创作` → `中文剧本格式` for formal screenplay layout → `影视分镜` for shot design → `AI绘画提示词` for visual prompts.
- Accuracy-sensitive industrial storyboard: `storyboard-revision` or `石化简易分镜` first, depending on whether the main problem is factual verification or industrial shooting design.

---

### 4. Games / GDevelop

#### Overall interactive game design
Use for point-and-click adventures, environmental puzzles, no-dialogue storytelling, puzzle structure, interaction loops, or Machinarium-like game concepts.

- Skill: `interactive-game-design`
- Path: `plugins/hermes-skills/skills/hermes-creative-interactive-game-design/SKILL.md`
- Read referenced design resources when the skill requires them.

#### GDevelop point-and-click / lightweight demo direction
Use for producing a 10–20 minute GDevelop point-and-click demo, scene logic, hotspots, puzzle states, light inventory, no-dialogue narrative, or detailed GDevelop production direction.

- Skill: `gdevelop5-click-adventure-director`
- Path: `plugins/hermes-skills/skills/hermes-creative-gdevelop5-click-adventure-director/SKILL.md`
- The skill contains a large task-specific reference map under its own `references/`; load the referenced file that matches the current issue before answering.

#### GDevelop project engineering / JSON / debugging
For any task that modifies, analyzes, fixes, or extends a GDevelop 5 project, JSON, events, objects, variables, collisions, platform behavior, UI, audio, scene switching, scoring, or spawning, load this skill first.

- Skill: `gdevelop5-official-docs-first`
- Path: `plugins/hermes-skills/skills/hermes-dev-gdevelop5-official-docs-first/SKILL.md`
- Official-doc cache: `plugins/hermes-skills/skills/hermes-dev-gdevelop5-official-docs-first/references/GDEVELOP_OFFICIAL_DOC_CACHE.md`

Routing note: for GDevelop implementation/debugging, `gdevelop5-official-docs-first` is primary. Add `gdevelop5-click-adventure-director` for game/level/narrative design questions, and `interactive-game-design` for broader game structure.

---

### 5. Development / tooling

#### Android ADB / APK / pinned shortcuts
Use for Android or Redmi Pad ADB tasks, installed-app checks, APK extraction/installation, pinned shortcuts, or packaging a desktop shortcut as an APK.

- Skill: `android-adb-apk-shortcuts`
- Path: `plugins/hermes-skills/skills/hermes-dev-android-adb-apk-shortcuts/SKILL.md`

#### HermesTodo iOS app
Use for HermesTodo changes, bugs, SwiftUI/SwiftData behavior, AI Todo changes, device issues, deletion/rename problems, or any continuation of that app.

- Skill: `todo-fix`
- Path: `plugins/hermes-skills/skills/hermes-dev-todo-fix/SKILL.md`

#### Analytical / research-report presentation style
Use when the user wants an investment-research style report, industry analysis, competitor analysis, dialectical bull/bear framing, dense actionable reporting, report-section design, or the established Hermes report style.

- Skill: `research-report-style`
- Path: `plugins/hermes-skills/skills/hermes-dev-research-report-style/SKILL.md`

---

### 6. Skill creation / Hermes infrastructure

#### Create or distill a new thinking/persona skill
Use when the user asks to create a skill, distill a person/thinker, build a perspective, create a thinking framework, or use “女娲”.

- Skill: `huashu-nuwa`
- Path: `plugins/hermes-skills/skills/hermes-creative-nuwa-skill/SKILL.md`

The nested perspective/example skills inside this package are not top-level routes. Enter them only when the parent skill explicitly directs it or when the user names one directly.

#### Hermes multi-node mesh / cloud communication
Use for the local Mac + cloud + WeCom Hermes deployment, mesh bridge, `_inbox`, inter-node messages, or multi-Hermes coordination.

- Skill: `hermes-mesh`
- Path: `plugins/hermes-skills/skills/hermes-hermes-hermes-mesh/SKILL.md`

Do not reconstruct redacted infrastructure values from memory or guesses. Use only the current repository content and user-provided runtime information.

---

### 7. Lifestyle / special-purpose

#### Graduation copy / graduation video
Use for graduation speeches, graduation-video copy, parallel-universe graduation concepts, student-to-copy generation, or the established graduation-project system.

- Skill: `graduation-speech`
- Path: `plugins/hermes-skills/skills/hermes-lifestyle-graduation-speech/SKILL.md`

#### Fitness tracking
Use for the user's Hermes fitness-tracking workflow, logging exercise, calories, training plans, weight progress, or “today what should I train” requests.

- Skill: `健身追踪`
- Path: `plugins/hermes-skills/skills/hermes-lifestyle-健身追踪/SKILL.md`

Because fitness data can change, treat the current `SKILL.md` as the stored workflow state rather than relying on remembered values.

---

## Multi-skill routing rules

When multiple skills could apply:

1. Choose the skill that defines the **overall workflow/content judgment** as primary.
2. Read its `SKILL.md` first.
3. Follow dependencies declared by that skill.
4. Add a supporting skill for a distinct execution layer or subtask.
5. Do not merge conflicting instructions by intuition. If two loaded skills conflict, follow the more task-specific skill; if still ambiguous, surface the conflict.

### Follow-up / mid-conversation re-routing

Routing is not a one-time decision. Re-run skill matching when an observable condition changes:

- the user uploads an existing Word/PDF/spreadsheet/slide after earlier analysis;
- the request changes from “分析/给方向” to “直接修改/生成文件”;
- the user says “在这个版本上改 / 不要重写 / 保留原格式”;
- the requested output changes from copywriting to storyboard, prompt, formatting, or document review;
- a new accuracy-sensitive or domain-specific requirement appears.

Use this model:

**domain skill = what should change**

**artifact/execution skill = how to apply the change to the user's existing artifact**

Do not replace the domain skill merely because a Word file appears. Add the artifact skill when both are needed.

Examples:

- “写企业宣传片并做分镜” → `宣传片创作` first, then `影视分镜`.
- “宣传片先给修改方向，后来上传Word说在这个版本上改” → keep `宣传片创作`, add `doc-reviewer`.
- “把故事大纲优化成完整短片剧本” → `故事片创作` first; load `中文剧本格式` only when formal script layout is needed.
- “检查油田分镜是否现实并修正” → `storyboard-revision` first; add `石化简易分镜` for industrial shot execution.
- “分析婚礼摄影公司的营销问题” → `marketing-copilot`; use `marketing-plan` only if a full executable plan is requested.
- “改 GDevelop 项目里的跳跃/计分/Retry” → `gdevelop5-official-docs-first` first.

---

## Reference loading policy

The route table is an index, not a replacement for skill instructions.

After opening a matched `SKILL.md`:

- If it says **must / 强制 / required / 必须加载** a reference, read that reference before continuing.
- If it gives a task-to-reference map, select the reference based on the current task and read it.
- If it depends on another skill, read that skill only when the dependency is relevant to the requested output.
- Prefer the copy bundled inside the skill folder. Use `shared/` as a methodology mirror or fallback index, not as a substitute for reading the actual skill.

---

## Failure behavior

If ChatGPT Web cannot access a path:

1. Report the exact unavailable path.
2. Do not claim the Hermes skill was followed if the required `SKILL.md` was not read.
3. If the user wants to proceed without the file, clearly label the result as a non-Hermes fallback.

---

## Canonical user invocation

Recommended phrase:

> 请按 Hermes skill 路由执行这个任务。

For a specific skill:

> 请按 Hermes skill 路由执行，并优先使用 `故事片创作`。

For strict file-grounded execution:

> 请按 Hermes skill 路由执行。先从 GitHub 读取路由文件和匹配的 `SKILL.md`，不要凭记忆模拟。