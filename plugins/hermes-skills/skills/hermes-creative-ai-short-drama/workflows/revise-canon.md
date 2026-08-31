# Revise Canon

Stage order:

`collect authoritative state -> order historical sources -> classify decisions -> resolve scoped conflicts -> write narrow patch -> update entrypoint -> readback verify`

Use this workflow for an existing drama when the user supplies old/middle/latest conversations, prior bibles, Git patches, or asks to recover/continue earlier work.

## Inputs

- canonical entrypoint/index when one exists;
- latest approved Series Bible and episode snapshots/patches;
- historical source material in known or inferable chronology;
- requested revision scope.

Read [canon revision rules](../references/canon-revision-rules.md) and [story architecture](../references/story-architecture.md).

## Procedure

1. **Load current authority first.** Read the canonical entrypoint and the latest documents it points to. Do not begin by copying the oldest transcript into the project.
2. **Establish chronology.** Order historical sources from earliest to latest. If chronology is uncertain, mark the affected conflict `NEEDS_REVIEW`.
3. **Extract decisions, not prose.** For each useful item, identify its scope and whether it is approved, rejected, superseded, candidate, or unresolved.
4. **Apply scoped precedence.** Later explicit decisions override earlier ones only on the same scope. Do not let a later mechanism rewrite an earlier locked character function unless it actually conflicts.
5. **Restore missing origins carefully.** Older sources may supply intent, setup logic, character engine, or production constraints where current canon is silent. They may not resurrect a discarded plot.
6. **Preserve approval boundaries.** Structure, mechanism, dialogue, names, visuals, and exact engineering are independent approval scopes.
7. **Write the smallest useful patch.** Prefer a narrow patch/snapshot update over rewriting every canon file.
8. **Update the canonical entrypoint/read order.** Record which file now has precedence and which old material is `SUPERSEDED / NOT_CANON`.
9. **Readback verify.** Refetch the patch and entrypoint. Confirm intended text, supersession, and unresolved fields.

## Conflict-table shape

Use when the history is complex:

| Claim | Scope | Older state | Later state | Resolution | Canon action |
| --- | --- | --- | --- | --- | --- |
| ... | episode function | ... | ... | `LOCKED_FUNCTION` | patch |
| ... | dialogue | ... | rejected | `TBD` | do not copy |

Do not expose the whole table unless useful to the user; it is primarily a reasoning and audit device.

## Outputs

- concise revision summary;
- conflict resolutions that materially changed canon;
- narrow canon patch/update;
- updated canonical entrypoint/read order;
- unresolved `TBD` / `NEEDS_REVIEW`;
- readback verification status.

Do not call historical brainstorm “canon recovered” merely because it is interesting.
