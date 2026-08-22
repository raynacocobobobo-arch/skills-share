# Story Skill Canonical Recovery — Design

## Classification
Architectural process-document change. This promotes a previously developed Story Skill candidate into the canonical Hermes repository without copying project-private examples or bypassing version governance.

## Goal
Replace the canonical `故事片创作` v11.1.0 with a de-projectized, validated successor based on the proven v13 candidate, while preserving the new Canonical Latest + Version Guard rules.

## Source-of-truth model
- Runtime authority: GitHub `main` only.
- Current canonical baseline: `故事片创作` v11.1.0.
- Library v13.0.0: candidate/evidence only.
- Promotion target: a new canonical version greater than 11.1.0, proposed as 13.1.0.

## What v13 already solved
Recover rather than reinvent:
- source priority and minimum-change revision discipline;
- task mode recognition for new writing, major revision, local revision, diagnosis, formatting;
- project modes for fiction, commissioned realism, and documentary-fiction hybrids;
- causal story engine and choice-based character arc;
- fact/HSE/permission/continuity checks;
- templates such as three-act/15 beats/hero journey as optional diagnostic tools;
- dialogue naturalness checks;
- narration roles and picture/narration redundancy check;
- feedback diagnosis before rewriting;
- non-professional actor feasibility;
- commissioned-film ending rules.

## Remaining improvements added during recovery
1. **Unified fact-state vocabulary**
   - LOCKED: explicitly approved/immutable unless reopened.
   - CONFIRMED: supported by authoritative evidence.
   - TENTATIVE: usable only with visible uncertainty / pending confirmation.
   - CONFLICT: sources disagree; do not silently choose.
   - INFERRED: non-professional connective inference only.
   - DO_NOT_INVENT: professional/safety/history/private facts that may not be invented.

2. **Referential integrity after structural edits**
   Any rename, renumber, merge, split, move, or deletion must trigger a search for all dependent references: scene numbers, character names, appendices, production notes, cross-references, tables, and downstream deliverables.

3. **No local/private project assumptions**
   Remove machine-specific paths and project-specific examples. Tests will reject known project-specific tokens from entering the canonical skill.

## File design
### Main skill
`plugins/hermes-skills/skills/hermes-film-故事片创作/SKILL.md`
- stays decision-oriented;
- declares v13.1.0;
- contains triggers, routing-relevant modes, workflow, quality gates;
- links only to references that actually exist.

### Supporting references
`references/revision-control.md`
- scope lock, source precedence, fact states, minimal diff, referential integrity.

`references/dialogue-vo-naturalness.md`
- dialogue role/scene/identity/oral tests, narration responsibilities, anti-redundancy.

`references/commissioned-realism.md`
- professional realism, permissions/HSE, non-professional actors, documentary-fiction boundaries.

Existing methodology directories remain available as optional background; they are no longer universal hard constraints.

## TDD contract
A new repository test must fail against v11.1.0 and pass only when the canonical Story Skill:
- is versioned >=13.1.0;
- no longer contains machine-specific project paths;
- declares and links the three new references;
- distinguishes revision modes;
- has minimum-change/source-priority behavior;
- uses the unified fact states;
- explicitly treats structural templates as optional tools;
- contains referential-integrity propagation rules;
- contains no private project/customer identifiers from the evidence project.

## Out of scope
- rewriting promotional-film skill;
- changing doc-reviewer unless regression evidence shows a failure;
- committing the old project scripts/chat history;
- creating a new duplicate Story Skill;
- changing Router behavior already fixed by PR #2.

## Success criteria
1. RED test fails on canonical v11.1.0 for the intended reasons.
2. New Story Skill passes contract tests and general Hermes validator.
3. Registry changes from v11.1.0 to v13.1.0 and version guard recognizes it as an upgrade.
4. No missing declared supporting reference.
5. No customer/private project content or machine-specific path enters the repository.
6. Draft PR CI is fully green before any merge claim.
