# Create Episode

Stage order: `load canonical state -> Episode Card -> screenplay -> State Delta draft -> Continuation Capsule draft`

## Inputs

- latest approved Series Bible;
- previous approved State Delta and Continuation Capsule, except EP01;
- requested episode/pilot objective.

Read [episode contract](../references/episode-contract.md) and use [episode-card.md](../templates/episode-card.md).

## Procedure

1. **Load canonical state:** apply the previous approved State Delta, then load the Continuation Capsule, open debts, clue/reveal state, prop ownership, and opening connection. Mark conflicts `NEEDS_REVIEW`.
2. **Episode Card:** approve the opening hook, one dominant turn, conflict, payoff/progress, cliffhanger, participating entity IDs, and target duration.
3. **Screenplay:** write scene IDs, visible action, dialogue, and scene end states. Do not contradict approved state or silently add a rule/entity to solve the plot.
4. **State Delta draft:** list only persistent facts the screenplay intends to establish.
5. **Continuation Capsule draft:** capture the last visible handoff, character knowledge/relationship changes, prop/clue state, active constraints, open debts, and next allowed reveal.

The State Delta and Continuation Capsule remain drafts until story/production review confirms what actually occurred. Do not update canonical state from intention alone.

## Outputs

- approved Episode Card;
- screenplay;
- draft State Delta;
- draft Continuation Capsule;
- status `READY`, `NEEDS_REVIEW`, or `BLOCKED` for `screenplay-to-shots.md`.
