# Series Bible — Midnight Repair / 零点修表铺

- Version: benchmark-v1
- Canonical through: EP00 (episode deltas are exercised in the episode fixtures)
- Format: 3 × approximately 60-second vertical live-action AI drama
- Status: structural benchmark; no media is claimed

## Premise

Courier Lin Xia finds a blue-thread brass key among her missing mother's belongings. At a repair shop that opens only near midnight, guarded shopkeeper Zhao recognizes the key but refuses to explain. Each episode turns a physical repair clue into a change in who Lin can trust.

- Audience promise: one tactile clue, one relationship reversal, and one larger question per episode.
- Core pressure: Lin must uncover the truth without alerting whoever made her mother disappear.
- Distinctive mechanism: repair objects preserve causal evidence that dialogue tries to hide.
- Cost: using each clue exposes Lin's search to the watcher behind the disappearance.
- Pilot success condition: the same shop, two leads, and one key sustain three different turns without a state reset.

## Characters

| ID | Role | Want | False belief/cost | Relationship state at EP00 | Production anchor |
| --- | --- | --- | --- | --- | --- |
| `CHAR_LIN` | courier; missing woman's daughter | learn why her mother vanished | assumes Zhao caused the disappearance | distrusts Zhao | dark delivery jacket, tied-back hair |
| `CHAR_ZHAO` | guarded repair-shop keeper | keep Lin alive and the evidence hidden | believes secrecy is safer than trust | protective but evasive | grey shop apron, old wristwatch |

## World Rules and Recurring Location

- `RULE_01`: clues are ordinary physical objects; no supernatural solution.
- `RULE_02`: generated readable evidence text is added as a post overlay.
- `LOC_REPAIR_SHOP`: front door west/screen-left background; counter center; hidden drawer behind counter east/screen-right; red tool wall behind Zhao. The Lin-left/Zhao-right axis persists unless re-established.

## Entity Registry

| ID | Type | Canonical state at EP00 | Production relevance |
| --- | --- | --- | --- |
| `PROP_KEY` | brass key/clue with blue thread | held by Lin; Zhao has not seen it | must not disappear/change hands without action |
| `PROP_CASSETTE` | microcassette clue | hidden in locked drawer | first appears after `PROP_KEY` opens drawer |
| `ASSET_MOTHER_PORTRAIT` | identity reference | required for EP03 memory insert; deliberately missing in benchmark | demonstrates `BLOCKED` |

## Reveal Ladder

| ID | Reveal | Earliest episode | Status at EP00 |
| --- | --- | --- | --- |
| `REV_01` | Zhao recognizes the key and hidden drawer | EP01 | hidden |
| `REV_02` | the key belonged to Lin's mother | EP02 | hidden |
| `REV_03` | Zhao protected the mother; she may be alive | EP03 | hidden |

## Antagonist Ladder

| Level | Pressure | Pilot use |
| --- | --- | --- |
| 1 | Zhao's secrecy blocks access | EP01–EP02 |
| 2 | an unseen watcher outside the shop | EP03 cliffhanger |

## Payoff Debt Ledger

| Debt ID | Opened | Promise | Due | Status at EP00 |
| --- | --- | --- | --- | --- |
| `DEBT_KEY_ORIGIN` | EP01 | explain why Zhao knows the key | EP02 | not opened |
| `DEBT_ZHAO_ROLE` | EP01 | reveal whether Zhao betrayed the mother | EP03 | not opened |
| `DEBT_MOTHER_ALIVE` | EP03 | resolve where the mother is | after pilot | not opened |

## Pilot Outline

| Episode | Opening hook | Dominant turn | Payoff/progress | Cliffhanger | Intended State Delta |
| --- | --- | --- | --- | --- | --- |
| EP01 | the key falls onto Zhao's counter | Zhao's gaze betrays the hidden drawer | Lin confirms the key belongs to this shop's history | matching blue thread hangs from the drawer handle | Zhao knows Lin has the key; Lin knows the drawer matters; key stays with Lin |
| EP02 | Lin reconnects from the closed drawer/key state | Zhao permits Lin to open the drawer | the key's origin is paid; cassette clue appears | overlay: “For Lin, play after midnight” | drawer open; Lin holds key and cassette; Zhao admits the key was her mother's |
| EP03 | cassette is played beside the open drawer | recording recasts Zhao as protector | `DEBT_ZHAO_ROLE` is paid; mother may be alive | outside door handle carries matching blue thread | Lin provisionally trusts Zhao; unseen watcher becomes active; final delta remains draft while one segment is blocked |

## Current Canonical State at Pilot Start

- Lin holds `PROP_KEY`; Zhao has not seen it.
- `PROP_CASSETTE` is inside the closed hidden drawer.
- Lin distrusts Zhao; Zhao protects Lin without admitting it.
- `REV_01`–`REV_03` are hidden and no payoff debt is yet opened.
