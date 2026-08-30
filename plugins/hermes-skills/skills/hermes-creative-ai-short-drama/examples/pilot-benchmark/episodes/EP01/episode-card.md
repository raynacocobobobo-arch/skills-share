# Episode Card — EP01: The Key

```yaml
episode_id: EP01
target_duration_sec: 60
opening_hook: "The blue-thread brass key falls from Lin's parcel onto Zhao's counter."
dominant_turn: "Zhao's involuntary eyeline reveals that the key is connected to a hidden drawer."
core_conflict: "Lin needs an answer; Zhao tries to hide recognition without moving the evidence."
payoff_or_progress: "Lin confirms that her mother's key belongs to the shop's history."
ending_cliffhanger: "A matching blue thread is visible on the closed drawer handle."
state_delta:
  - "CHAR_ZHAO knows CHAR_LIN holds PROP_KEY."
  - "CHAR_LIN knows the hidden drawer is linked to PROP_KEY."
  - "PROP_KEY remains with CHAR_LIN; the drawer remains closed."
continuation_capsule: "Reconnect on the closed hidden drawer. Lin stands screen-left and holds PROP_KEY; Zhao remains screen-right behind the counter. Both know the key matters, Lin distrusts Zhao, and DEBT_KEY_ORIGIN plus DEBT_ZHAO_ROLE are open."
```

Dependencies: pilot-start canonical state. Entities: `CHAR_LIN`, `CHAR_ZHAO`, `LOC_REPAIR_SHOP`, `PROP_KEY`.
