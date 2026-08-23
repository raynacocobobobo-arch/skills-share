# AI Short Film Production Workflow Validation

Manual validation scenario:

```text
做一个 AI 故事短片，片名《誓言之外》
```

Expected routing:

1. Enter `plugins/hermes-workflows/workflows/ai-short-film-production/WORKFLOW.md`.
2. Do not generate prompts first.
3. Load `hermes-film-故事片创作` and `short-form-visual-story.md`.
4. Produce Story Lock before Visual Bible.
5. Produce Visual Bible before Asset Bible.
6. Produce Asset Bible before Storyboard.
7. Produce Storyboard before AI Production Plan.
8. Treat “方向对了 / 大概意思对 / 这个版本可以” as Baseline Lock.

Expected deliverables:

```text
Story Lock
Visual Bible
Asset Bible
Storyboard
AI Production Plan
```

Failure conditions:

- direct prompt generation from the first idea;
- changed protagonist desire after Story Lock;
- changed color system after Visual Lock;
- full redesign after baseline acceptance;
- storyboard shots that do not serve story, information, suspense, setup/payoff, or emotional state.
