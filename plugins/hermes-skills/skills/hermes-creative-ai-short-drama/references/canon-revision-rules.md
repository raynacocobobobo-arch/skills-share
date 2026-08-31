# Canon Revision Rules

Use this reference when a serialized drama already has historical bibles, Git patches, transcripts, summaries, or multiple conversations that do not perfectly agree.

The objective is **not** to merge every past idea. The objective is to reconstruct the latest approved state while preserving useful provenance and unresolved uncertainty.

## Core precedence rule

Order sources chronologically when possible.

A later explicit decision overrides an earlier decision **only on the same scope**.

Examples of separate scopes:

- episode function;
- causal mechanism;
- character relationship;
- dialogue;
- name;
- visual design;
- exact timing;
- engineering implementation;
- theme label.

Therefore:

> “The episode structure works, but the dialogue is bad”  
> locks the structure and leaves dialogue unresolved.

Approval never propagates automatically from one scope to another.

## Decision-state taxonomy

Classify recovered material before writing it into canon:

| State | Meaning |
| --- | --- |
| `LOCKED` | explicitly approved persistent fact |
| `LOCKED_FUNCTION` | dramatic/causal function approved; implementation open |
| `LOCKED_DIRECTION` | bounded direction approved; exact form open |
| `CANDIDATE` | useful option discussed but not approved |
| `TBD` | intentionally unresolved |
| `VALIDATE_LATER` | causal/engineering claim only needs plausibility validation later |
| `NEEDS_REVIEW` | sources conflict or approval cannot be determined |
| `SUPERSEDED` | later decision replaced it |
| `NOT_CANON` | brainstorm/provenance only |

Do not convert `TBD`, `CANDIDATE`, or `NEEDS_REVIEW` into `LOCKED` to make a document feel complete.

## Recovery procedure

For each claim worth recovering, record mentally or in a conflict table:

1. **claim** — what is being asserted;
2. **scope** — function, mechanism, dialogue, etc.;
3. **earliest evidence** — where it first appeared;
4. **later changes** — every revision that touches the same scope;
5. **latest explicit approval** — if any;
6. **resolution** — current state label;
7. **provenance note** — only when knowing the old intent helps future writing.

Older material may restore:

- original intent;
- character engine;
- causal motivation;
- production constraint;
- setup/payoff reason;
- a missing origin for a later rule;

only when later canon does not contradict it.

Older material may not resurrect:

- replaced episode order;
- discarded mechanism;
- rejected dialogue;
- superseded relationship direction;
- brainstorm examples explicitly marked non-canon.

## Narrow-patch rule

When canon changes:

- patch only the affected scope;
- name what the patch supersedes;
- keep unrelated locked facts intact;
- preserve unresolved fields;
- avoid rewriting the entire bible just because one function changed.

A later consolidated snapshot may summarize many patches, but its purpose is navigation—not permission to erase provenance.

## Canonical entrypoint

Long-running projects should have one obvious entrypoint such as `CURRENT.md`, an index, or a latest consolidated snapshot.

It should state:

- latest authoritative documents;
- read order;
- superseded documents that must not be treated as current;
- current `TBD` / `NEEDS_REVIEW`;
- canonical-through episode or milestone.

When a revision is persisted, update this entrypoint in the same task.

## Historical transcripts as evidence

Conversation transcripts contain multiple epistemic states:

- proposal;
- critique;
- revision;
- user approval;
- Git confirmation;
- later reversal.

Do not treat “assistant proposed it” as approval.

Strong signals include:

- explicit user acceptance;
- explicit user rejection;
- “git / lock this” scoped to the immediately confirmed material;
- later correction;
- a persisted canonical patch confirmed after write.

If a transcript contains both “this is good” and later “no, this repeats EP03,” the later scoped correction wins.

## Readback verification

After any canon write:

1. refetch/reopen the changed file;
2. refetch/reopen the canonical entrypoint;
3. confirm the new text exists;
4. confirm superseded text was not accidentally reactivated;
5. confirm `TBD` / `NEEDS_REVIEW` stayed unresolved unless explicitly decided.

Do not claim completion from a write response alone.

## When to stop with NEEDS_REVIEW

Use `NEEDS_REVIEW` rather than guessing when:

- chronology is ambiguous;
- two sources conflict but neither has a later explicit approval;
- approval wording could refer to multiple scopes;
- a summary contradicts a more specific locked patch and precedence is unknown;
- a missing mechanism materially changes the moral or causal choice.

Uncertainty preserved correctly is better canon than false completeness.
