# Hermes Overengineering Audit Final

Scope: Phase 1 read-only audit for minimum contraction cleanup.

Repository scanned:

- `AGENTS.md`
- `manifests/*`
- `plugins/hermes-skills/skills/*`
- `scripts/*`
- `.agents/*`
- Related `shared/` and repository entry points where needed to understand runtime impact.

Current shape:

- 23 primary migrated skills plus 5 nested `huashu-nuwa` perspective examples are present in the generated registry.
- `plugins/hermes-skills/skills/` contains 156 reference files under skill-local `references/`.
- `shared/` contains 40 files; `shared/source-library/` contains 14 source-library files, including several `.index.md` entry files.
- `scripts/validate-skills.py` currently reports `skills: 28` and `errors: 0`.

## KEEP

Must keep:

- `plugins/hermes-skills/skills/` as the core capability library.
  - Most directories represent real reusable task abilities, not empty prompt wrappers.
  - Do not delete effective skills during this cleanup.
- `shared/source-library/`.
  - It is a compact professional knowledge base, not yet an overbuilt platform.
  - Existing `.index.md` files are useful lightweight entry points.
- `shared/film-methodology/`, `shared/marketing-methodology/`, and `shared/creative-framework/` as shared methodology assets.
  - They preserve reusable knowledge outside a single skill.
- `manifests/execution-capability-policy.md`.
  - It solves a real runtime question: distinguish GitHub account permission, connector permission, current tool capability, and local execution capability.
  - Do not replace it with a broader `governance-policy.md`.
- `manifests/skill-registry.json`.
  - It is the useful machine-readable inventory for skill path, triggers, version, and references.
- `.agents/plugins/marketplace.json`.
  - It is small and directly supports local plugin discovery.
- Secret/local-path scanning in `scripts/validate-skills.py`.
  - This is a low-cost safety check and should remain in the basic validation path.
- Reference hygiene tests and skill contract tests.
  - They guard against known regressions without creating runtime process burden.

## MODIFY

Needs adjustment:

- `AGENTS.md`
  - Current issue: it reads like a full operations manual and applies the same heavy write path to all edits.
  - It mixes actors, canonical-version governance, read workflow, branch naming, activity logging, validation, merge rules, security, conflict handling, and repository layout.
  - Recommendation: shrink it to core boundaries, safety rules, modification principles, and commit principles.
  - Add two modification levels:
    - Level 1 documentation changes: typo, wording, reference-link adjustment. Allow lightweight validation and no registry rewrite unless references change.
    - Level 2 capability changes: skill behavior, router behavior, manifest/registry changes. Require full validation and registry consistency.

- `manifests/web-chatgpt-router.md`
  - Current issue: it is both a router and a governance file.
  - It contains useful skill matching, routing entry points, and multi-skill routing.
  - It also repeats canonical-latest/version-promotion rules that belong in `AGENTS.md` or validation tests.
  - Recommendation: keep the runtime routing table and "read matched SKILL.md" rule; remove or shorten version governance, promotion language, and generic process rules.
  - Target shape: "entry point + skill matching + minimal load order." It should not become the total rulebook.

- `manifests/dependency-manifest.json`
  - Current issue: it is named like a runtime dependency manifest, but the contents are migration/copy/rewrite records.
  - It records `skill_copy_records`, `external_reference_records`, `shared_reference_records`, `rewritten_skill_files`, and `redacted_files`.
  - Recommendation: reposition as migration archive, either by renaming later or documenting it as non-runtime.
  - Runtime code and routing should not depend on it.

- `manifests/skills-manifest.json`
  - Current issue: it is a simple skill-name list that overlaps with `skill-registry.json`.
  - Recommendation: defer deletion until callers are checked, but prefer registry as the canonical machine-readable inventory.

- `scripts/validate-skills.py`
  - Current issue: one command combines daily structural checks, secret scan, registry generation, and version-downgrade governance.
  - Recommendation: split behavior by CLI mode, not by adding a new framework.
    - Basic/default check: file existence, frontmatter, secret scan, local path scan, referenced paths.
    - Publish check: registry write, baseline registry comparison, version removal/downgrade guard.
  - Keep one script if possible; add flags or subcommands only if they reduce daily cost.

- `plugins/hermes-skills/skills/hermes-hermes-hermes-mesh/`
  - Current issue: this is infrastructure, not a user task skill.
  - Evidence: it covers multi-Hermes communication, mesh bridge, node routing, service files, transfer checklists, WeCom routing, and troubleshooting.
  - Recommendation: evaluate moving to `infrastructure/` in a later phase.
  - Do not delete automatically; first verify registry, router, README, marketplace, and external runtime callers.

- Deep or broad reference sets.
  - `hermes-dev-gdevelop5-official-docs-first` has 29 reference files.
  - `hermes-creative-gdevelop5-click-adventure-director` has 33 reference files.
  - `hermes-film-宣传片创作` has 19 reference files.
  - `hermes-film-故事片创作` has 18 reference files.
  - Recommendation: add or improve simple local `references/index.md` files only where agents need a clear "read this first" entry. Do not restructure the knowledge library into a platform.

- Missing or stale reference metadata.
  - Registry currently reports `references/godot-click-adventure-scaffold.md` missing for `gdevelop5-click-adventure-director`; the file exists under `hermes-creative-interactive-game-design`.
  - Recommendation: in a later phase, either fix that SKILL reference path or make it an explicit cross-skill reference.

- `huashu-nuwa` and nested perspective examples.
  - Registry descriptions show `description: "|"`, which is weak machine-readable metadata.
  - Recommendation: improve frontmatter descriptions later without changing behavior.

## REMOVE / DEFER

Delete or defer:

- Do not create `governance-policy.md`.
  - Existing `execution-capability-policy.md` covers the real capability question.
- Do not create an "anti-overengineering" skill.
  - The cleanup goal should be implemented as simpler repository rules, not a new skill/process layer.
- Do not add approval systems, workflow engines, or another manifest layer.
- Defer deleting any skill.
  - The audit found overlap candidates, but no safe automatic deletion target.
- Defer moving `hermes-mesh` until caller checks are complete.
  - Likely move target: `infrastructure/hermes-mesh/`.
  - Required caller checks: router references, registry generation, marketplace packaging, README entry points, tests, and external local Hermes expectations.
- Defer deleting `skills-manifest.json`.
  - It is redundant with `skill-registry.json`, but caller checks must come first.
- Defer renaming `dependency-manifest.json`.
  - First update docs and references so runtime users do not treat it as a dependency source.
- Defer broad reference tree reshaping.
  - Add indexes where useful; avoid reorganizing large knowledge folders for aesthetics.

## NOT TOUCH

Do not touch in this contraction pass:

- Skill behavior content for effective business, film, document, game, lifestyle, and development skills.
- `shared/source-library/` content.
- Redaction placeholders and security posture.
- Existing tests except where Phase 2/3 changes require focused updates.
- Existing `docs/superpowers/*` history documents.
  - They are historical implementation artifacts. Do not make runtime depend on them.
- Knowledge collector scripts under `scripts/knowledge-collector/`.
  - They are outside the core governance contraction unless a separate task asks for collector cleanup.

## Skill Layer Findings

Do not delete effective skills.

Potential overlap or consolidation candidates for later review:

- `marketing-copilot` and `marketing-plan`
  - Keep both for now. They differ by advice/analysis versus complete plan deliverable.
- `document-editing`, `transcript-cleanup`, and `doc-reviewer`
  - Keep all for now. They differ by plain document cleanup, recorded speech sync constraints, and Word-native review/edit output.
- `interactive-game-design`, `gdevelop5-click-adventure-director`, and `gdevelop5-official-docs-first`
  - Keep all for now. They differ by game concept/design, GDevelop point-and-click direction, and GDevelop engineering/debugging.
- `影视分镜`, `storyboard-revision`, and `石化简易分镜`
  - Keep all for now. They differ by general storyboard, fact-correction/pre-shoot verification, and industrial/petrochemical shooting practicality.
- `AI绘画提示词`, `内容标签`, and `中文剧本格式`
  - These are small focused utility skills. Do not merge unless routing confusion appears.

Infrastructure candidate:

- `hermes-mesh`
  - Move candidate, not delete candidate.
  - It should probably leave `plugins/hermes-skills/skills/` because it describes infrastructure operations rather than a user-facing task ability.

Prompt-wrapper candidates:

- No obvious empty prompt-wrapper primary skill should be deleted automatically.
- Metadata cleanup is needed for `huashu-nuwa` and nested perspective examples because their registry descriptions are not informative.

## References And Source Library Findings

- Keep `shared/source-library`.
- Keep current source files and existing `.index.md` entry files.
- Do not build a knowledge platform.
- For deep skill reference folders, prefer a simple local index that tells agents what to read first:
  - "core workflow references"
  - "task-specific troubleshooting references"
  - "archive or examples"
- Do not require agents to traverse every reference file before using a skill.

## Minimal Modification Plan

Recommended next phases:

1. Shrink `AGENTS.md`.
   - Add Level 1 and Level 2 modification rules.
   - Remove duplicate detailed version-governance prose that can be enforced by validation/tests.

2. Trim `manifests/web-chatgpt-router.md`.
   - Keep routing table and skill loading rules.
   - Remove duplicated governance, promotion, and generic process language.

3. Reposition `dependency-manifest.json`.
   - Document it as migration/archive, not runtime dependency input.
   - Check callers before any rename.

4. Make validation cheaper.
   - Keep default validation focused on basic checks.
   - Move registry write and baseline version guard behind publish-mode flags.

5. Evaluate moving `hermes-mesh`.
   - First perform caller search.
   - If no runtime packaging blocker exists, move to `infrastructure/hermes-mesh/` and update router/registry behavior accordingly.

6. Add reference indexes only where they reduce read cost.
   - Prioritize GDevelop and large film/story reference folders.
   - Keep index files simple.

## Pre-Commit Check Answers

1. Deleted or moved content has actual callers?
   - Phase 1 did not delete or move anything.
   - `hermes-mesh`, `skills-manifest.json`, and `dependency-manifest.json` all need caller checks before move/delete/rename.

2. Does the proposed direction lower execution cost?
   - Yes, if implemented as scoped edits: lighter Level 1 doc path, router limited to routing, and validation split between daily/basic and publish checks.

3. Does the proposed direction add new rule files?
   - No.
   - Explicitly do not add `governance-policy.md`, approval systems, workflow engines, or new manifest layers.

## Verification

Commands run:

```bash
git status --short
python3 scripts/validate-skills.py
```

Observed validation result:

```text
skills: 28
errors: 0
```

