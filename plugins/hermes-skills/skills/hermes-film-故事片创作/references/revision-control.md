# Story Revision Control

Use this reference whenever the task modifies an existing outline, screenplay, treatment, Word document, or previously approved story version.

## 1. Determine revision mode first

Classify the request before editing:

- **新写**: no accepted baseline exists.
- **大改**: the user explicitly permits structural reconstruction.
- **局部改**: only named scenes, sections, lines, or problems may change.
- **诊断**: analyze without rewriting unless asked.
- **格式化**: preserve content; change presentation only.

If an existing artifact is present, the artifact itself is the baseline. A clean copy is still a revision of that baseline, not permission to recreate a similar document from scratch.

## 2. Information-source priority

When sources conflict, use this precedence:

1. user's latest explicit instruction;
2. client/owner approved requirement or wording;
3. authoritative professional or official evidence;
4. user's accepted previous version;
5. current project lock table;
6. reasonable non-professional inference;
7. generic writing theory or templates.

Lower-priority methodology must never overwrite higher-priority confirmed information.

## 3. State model

Track important facts and decisions with one of these states:

- **LOCKED** — explicitly approved or declared not to change. Reopen only when the user/client explicitly does so.
- **CONFIRMED** — supported by authoritative evidence and safe to use.
- **TENTATIVE** — currently plausible or supplied but still awaiting confirmation. Preserve uncertainty.
- **CONFLICT** — two or more authoritative inputs disagree. Do not silently choose one.
- **INFERRED** — a non-professional connective inference used only when it does not create factual or safety claims.
- **DO_NOT_INVENT** — professional procedures, safety actions, historical facts, private facts, legal/medical/technical details, or other material that may not be fabricated.

## 4. Minimum-diff protocol

Before editing, internally sort requested material into:

| Keep | Must change | May change only if necessary |
|---|---|---|
| approved structure, facts, lines, characters | items named by the user/client | immediate upstream/downstream dependencies |

Default rule: **用户要求“修改”时，默认不是“重写”。**

Do not:
- fix one line by changing the character relationship;
- fix pacing by replacing the ending unless the pacing issue truly requires it;
- use a new idea to overwrite accepted assets without comparison;
- expand a local request into a full rewrite because a full rewrite is easier for the agent.

## 5. Scope lock

Treat these phrases as permission boundaries, not casual preferences:

- “前面定稿”
- “这段别动”
- “只改这一场/这一句”
- “结构锁了”
- “在这个版本上改”
- “保留原格式”

Once a scope lock appears, later edits must remain inside it unless the user explicitly reopens scope.

## 6. Referential integrity

Any structural edit can invalidate downstream references. After **重命名、重编号、合并、拆分、移动、删除** an entity, search all dependent material before declaring the revision complete.

Check at least:
- scene/section numbers;
- character names and aliases;
- chronology references;
- appendix and production-note references;
- tables, summaries, beat sheets, shot lists, and continuity notes;
- downstream deliverables that cite the changed entity.

A screenplay can be narratively correct and still be revision-broken if its production notes point to old scene numbers or renamed characters.

## 7. Feedback diagnosis

User feedback is often symptom language. Diagnose before rewriting:

| Feedback | First check | Do not start with |
|---|---|---|
| 怪 | local logic or language | full structural replacement |
| 不是人话 | dialogue/VO register | adding more subtext |
| 没意思 | objective, choice, consequence, turn | adding decorative detail |
| 流水账 | causal scene chain | deleting random life scenes |
| 偏了 | theme hierarchy and locked brief | inventing a new theme |
| 太复杂 | information load and execution cost | more explanation |
| 不合理 | fact/time/role/permission | narration that explains it away |

## 8. Completion check

Before handing back a revision:
- Did the requested problem actually change?
- Did anything outside scope change unintentionally?
- Did any LOCKED item drift?
- Did any TENTATIVE/CONFLICT item become falsely definite?
- Did rename/renumber/delete changes propagate to every reference?
