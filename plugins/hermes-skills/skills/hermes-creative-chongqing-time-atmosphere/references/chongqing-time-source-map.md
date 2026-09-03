# 《重庆时间》Live Source Map

This skill intentionally points to the live project repository instead of copying Canon into Hermes.

## Repository

- GitHub repository: `raynacocobobobo-arch/lora`
- Project root: `重庆时间/`
- Default accepted source: repository `main`, unless the user explicitly names another branch/commit.

## Required entrypoint

Read first:

> `重庆时间/ACTIVE-DOCS-INDEX.md`

It declares the currently active Canon, episode authorities, spatial patches, visual workflow, and style route. Follow its current links even if filenames/version numbers later change.

## Live read order

For a normal environment-atmosphere request:

1. `重庆时间/ACTIVE-DOCS-INDEX.md`
2. `重庆时间/CURRENT.md`
3. `重庆时间/CANON-PRECEDENCE-V4.md` or the current precedence file named by the active index
4. active spatial/environment patches relevant to the requested location, as named by the active index
5. the relevant episode's current snapshot / outline / screenplay named by the active index
6. `重庆时间/SCENE-PROMPT-TEMPLATE-V3.md` or its current successor named by the active visual workflow
7. `重庆时间/VISUAL-STYLE-ROUTING-INDEX-V2.md` or its current successor
8. the active visual style lock / prompt package named by the router/index
9. `重庆时间/VISUAL-CONSISTENCY-BIBLE-V2.md` when functional visual grammar, bridge scale, gravity/time visualization, signage, or scene QC is relevant
10. approved visual anchor/master files referenced by the current visual index when continuity requires them

Read only the files needed for the current task; do not load the entire project indiscriminately.

## Relevant episode resolution

For `EP01`–`EP10`, do not hardcode a snapshot version in this Hermes skill. Resolve the current episode authority from `ACTIVE-DOCS-INDEX.md`, then read the relevant episode file(s).

When the user asks for an episode's `核心空间`, inspect enough of the relevant episode story to determine:

- runtime coverage;
- dominant physical-action coverage;
- state-change coverage;
- the route/space system that actually carries that action.

A named machine, relay, room, bridgehead, or controller is not automatically the atmosphere-master location.

## Freshness rule

When GitHub access is available, read the current repository state at execution time. Do not rely on an embedded stale canon summary from this skill, a prior conversation, or a cached prose description when the live project files are available.

If the repository cannot be read:

- state which required project source is unavailable;
- do not invent a replacement Canon;
- continue only with facts the user explicitly supplies in the current task.

## Cross-skill routing

- Story/Canon/episode writing changes: `hermes-creative-ai-short-drama` may become primary or supporting.
- 《重庆时间》 environment atmosphere/master image or environment prompt: `hermes-creative-chongqing-time-atmosphere` is primary.
- Generic image-prompt wording may use a generic prompt skill only as support; it must not override the live 《重庆时间》 Canon or Scene Prompt workflow.
