# Create Series

Stage order:

`Greenlight -> Series Bible -> progression tracks -> 3–5 episode pilot outline -> Episode Function Audit -> persist canonical state`

For an existing project with historical or conflicting sources, run [revise-canon](revise-canon.md) before expanding the series.

## Inputs

- original concept or adaptation brief;
- target audience, format, approximate episode length, and production constraints when known;
- existing approved Series Bible when revising rather than starting;
- any known “must keep / must not do” constraints.

Read [story architecture](../references/story-architecture.md) and use [series-bible.md](../templates/series-bible.md).

## Procedure

1. **Greenlight:** express the premise, audience promise, repeatable episode grammar, central cost, escalation runway, production repeatability, and cheapest pilot test. Choose `GO_PILOT`, `REVISE`, or `STOP`.
2. **Lock macro before detail:** define character dramatic functions, authority boundaries, world limits, causal engine, and the series-level moral question before names, dialogue, exact technology, or lore that does not yet affect choices.
3. **Series Bible:** on `GO_PILOT`, assign stable IDs and fill premise, characters, world rules, recurring locations, Entity Registry, Payoff Debt Ledger, and current unresolved items.
4. **Progression tracks:** define the tracks the series actually needs. Usually separate:
   - Reveal/Knowledge;
   - Pressure/Public Action;
   - Relationship/Capability.
   Do not create all three mechanically when one is irrelevant.
5. **Recurring carriers:** identify any recurring place, person, institution, infrastructure, or motif whose meaning can change across episodes. Prefer causal callbacks over disposable case-of-the-week repetition.
6. **Pilot outline:** plan 3–5 episodes. Give each one:
   - distinct opening hook;
   - one dominant turn;
   - episode function;
   - conflict grammar;
   - pressure/progression step;
   - payoff/callback;
   - cliffhanger/end image;
   - intended State Delta;
   - pilot hypothesis.
7. **Episode Function Audit:** compare the pilot episodes side by side. Reject “new setting, same function” duplication. Confirm each episode asks a materially different dramatic question.
8. **Cost check:** if any episode uses a third path, write the remaining cost. If a solution makes everyone whole, re-check whether the series' central cost has been accidentally removed.
9. **Persist canonical state:** version the approved Series Bible and record `canonical through: EP00`. Keep unapproved mechanisms/dialogue/names as `TBD`, `CANDIDATE`, or `VALIDATE_LATER`.

Stop expansion and return `REVISE` or `STOP` when the concept lacks escalation runway, repeatable production anchors, or meaningful differentiation across the pilot. Do not outline the full season by default.

## Outputs

- Greenlight decision with one reason and next action;
- versioned Series Bible;
- named progression tracks;
- 3–5 episode pilot outline with Function Audit;
- canonical initial state ready for `create-episode.md`;
- explicit unresolved list.
