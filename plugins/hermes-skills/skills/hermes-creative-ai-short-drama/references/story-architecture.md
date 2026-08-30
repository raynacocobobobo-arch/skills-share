# Story Architecture

Use this reference when creating or extending a serialized short-drama project. Keep only facts that affect story choices or production continuity.

## Greenlight contract

Before outlining, state:

- premise: protagonist + pressure + distinctive mechanism + irreversible goal;
- audience promise: the repeatable emotion/payoff each micro-arc delivers;
- escalation runway: how pressure changes rather than merely grows louder;
- production repeatability: recurring characters, locations, and visual grammar that can be regenerated consistently;
- central cost: why the protagonist cannot solve everything immediately.

Choose `GO_PILOT`, `REVISE`, or `STOP`. Stop or revise when escalation runway, production repeatability, or episode-to-episode differentiation is missing.

## Series Bible

The Series Bible is the canonical persistent story record. It contains:

- the approved premise and audience promise;
- character IDs, wants, false beliefs, leverage, relationships, and production anchors;
- world/system rules, including limits and costs;
- recurring location and entity IDs;
- Reveal Ladder: staged evidence or truths, who knows them, and when they may surface;
- Antagonist Ladder: changing sources of pressure and how they learn;
- Payoff Debt Ledger: promises/injustices opened, due window, and payment state;
- current canonical state.

Approved persistent facts are immutable unless an explicit revision is recorded. Do not silently reset relationships, knowledge, injuries, possessions, rules, or paid debts.

## Pilot first

Default to a 3–5 episode pilot. Each episode must test a distinct part of the promise and contain one dominant turn. Do not expand the full season until the pilot proves:

1. the premise is understandable quickly;
2. the payoff mechanism works more than once;
3. escalation changes choices or power;
4. the production design is repeatable;
5. the ending creates a genuine next-episode question.

## Episode shape

Use this flexible order for a roughly one-minute episode:

`Cold Open -> Pressure -> Turn -> Payoff/Progress -> Cliffhanger -> State Delta`

- Cold Open makes the immediate imbalance, anomaly, or danger visible.
- Pressure forces a choice; context exists only to make that choice legible.
- Turn is the episode's single dominant change in power, information, relationship, goal, or cost.
- Payoff/Progress either repays a debt or moves a promised thread measurably forward.
- Cliffhanger creates a consequential prediction, not an arbitrary sentence cut.
- State Delta records only persistent changes that actually occurred.

## Ladders and ledgers

- Reveal Ladder prevents dumping the core truth at once. Each reveal changes what someone can decide or do.
- Antagonist Ladder changes the type of opposition: local pressure, gatekeeper, institution, informed counter-player, or moral mirror.
- Payoff Debt Ledger records `debt_id`, opened episode, promise/injustice, due window, current state, and paid episode. A pilot must repay at least one small early debt.
- Entity Registry gives stable IDs to recurring characters, locations, props, clues, and production-relevant states.

## State inheritance

To start Episode N+1, load:

1. the latest Series Bible canonical state;
2. Episode N's approved State Delta;
3. Episode N's Continuation Capsule;
4. unresolved payoff debts, clues, and reveal constraints.

Apply the approved State Delta to the canonical state, then use the Continuation Capsule as the compact writing handoff. If they conflict, stop and mark the episode `NEEDS_REVIEW`; do not choose a convenient reset.

## Continuation Capsule

Keep the capsule short enough to write the next episode without rereading the whole transcript. Include:

- current dramatic question and immediate pressure;
- character knowledge, relationship, and goal changes;
- prop/clue ownership and reveal state;
- location, costume, injury, or time facts that constrain the opening;
- unresolved payoff debts and the next allowed reveal;
- the last visible action/image that the next episode must reconnect to.
