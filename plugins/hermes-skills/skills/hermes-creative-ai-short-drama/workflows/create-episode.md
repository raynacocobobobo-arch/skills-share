# Create Episode

Stage order:

`load canon -> prior-function audit -> Episode Card -> macro approval -> screenplay -> State Delta draft -> Continuation Capsule draft`

## Inputs

- latest approved Series Bible and applicable canon revision patches;
- previous approved State Delta and Continuation Capsule, except EP01;
- Episode Function Map for prior episodes or enough canon to reconstruct it;
- requested episode/pilot objective.

Read [episode contract](../references/episode-contract.md), [story architecture](../references/story-architecture.md), and use [episode-card.md](../templates/episode-card.md).

## Procedure

1. **Load canonical state:** apply explicit canon precedence, previous approved State Delta, Continuation Capsule, open debts, progression state, prop ownership, and opening connection. Mark conflicts `NEEDS_REVIEW`.
2. **Prior-function audit:** summarize previous episodes' dominant turns and conflict grammar. State in one sentence what this episode does that none of them already did.
3. **Episode Card:** define the episode at macro level:
   - episode function;
   - opening hook;
   - one dominant turn;
   - core conflict;
   - conflict grammar;
   - relevant progression step(s);
   - causal callback/debt when useful;
   - cost after the solution;
   - payoff/progress;
   - cliffhanger/end image;
   - target duration.
4. **Novelty gate:** if the episode repeats an earlier functional grammar, revise before screenplay. A different bridge, baby, train, hospital, AI fault, casualty, or timeline device does not count as novelty by itself.
5. **Mechanism gate:** specify only enough mechanism to make the causal choice valid. Exact engineering remains `TBD`/`VALIDATE_LATER` when it does not affect the decision.
6. **Approval-scope gate:** do not infer that approval of the Episode Card approves dialogue, names, shot design, or exact mechanism. Record their states separately.
7. **Screenplay:** write scene IDs, visible action, dialogue, and scene end states. Do not contradict canon or silently add a rule/entity to solve the plot.
8. **Explanation budget:** prefer visible evidence and consequences. Do not dramatize the whole internal search/research/permission chain unless the audience must understand it to judge the choice.
9. **Agency/cost check:** if an AI, ally, or secondary character proposes or accepts the decisive action, preserve the protagonist/public authority's separate responsibility where the series requires it.
10. **State Delta draft:** list only persistent facts the screenplay intends to establish, with scope. Do not lock candidate dialogue by accident.
11. **Continuation Capsule draft:** capture the last visible handoff, character knowledge/relationship/capability changes, active constraints, open debts, callbacks due, and next allowed progression.

The State Delta and Continuation Capsule remain drafts until story/production review confirms what actually occurred. Do not update canonical state from intention alone.

## Outputs

- Episode Function Audit note;
- approved Episode Card;
- screenplay;
- draft State Delta with scoped decision states;
- draft Continuation Capsule;
- status `READY`, `NEEDS_REVIEW`, or `BLOCKED` for `screenplay-to-shots.md`.
