# Pilot Benchmark Report — Midnight Repair

Result: **PASS for V1 planning/orchestration contracts**. Media generation was not run and no fixture claims real video `PASS`.

## Scope

- 3 original serialized episodes, each targeted at 60 seconds;
- recurring `CHAR_LIN`, `CHAR_ZHAO`, and `LOC_REPAIR_SHOP`;
- continuity-sensitive `PROP_KEY`, followed by `PROP_CASSETTE`;
- Series Bible, Episode Card, screenplay, Continuity State, Storyboard/Shot Specs, and Production Pack for every episode;
- one simulated P0 take failure and one deliberately missing asset.

Fixture asset URIs use `fixture://` to test binding only. They are not media files. Production Packs keep `media_verified: false`.

## Acceptance evidence

| Criterion | Evidence | Result |
| --- | --- | --- |
| 3–5 episode pilot, ~1 minute each | EP01–EP03 each contain six Shot Specs totaling 60 seconds | PASS |
| Cross-episode State Delta inheritance | EP02 inherits EP01 `drawer=closed`, `PROP_KEY=CHAR_LIN`, recognition/debts; EP03 inherits EP02 `drawer=open`, key/cassette with Lin, and remaining debt | PASS |
| Continuity/geography | All episodes retain `LIN left / ZHAO right`, fixed counter/drawer/door geography, and explicit prop handlers | PASS |
| Shot Spec completeness | Every shot has start state, one visible action, end state, next-shot connection, references, prohibited changes, and information gain | PASS |
| Generation Segment integrity | Every segment references an existing Shot and declared asset; durations are 4–15 seconds | PASS |
| P0 targeted retake | `qa/retake-patch-EP02-SG04.json` fixes only the disappearing key while preserving identity, costume, axis, dialogue, surrounding segments, and drawer state | PASS |
| Missing asset behavior | EP03 `ASSET_MOTHER_PORTRAIT` is `missing`; only `EP03-SC01-SG03` and the episode handoff are `BLOCKED` | PASS |
| No fabricated completion | all packs use `media_verified: false`; EP02 remains `NEEDS_REVIEW`, EP03 remains `BLOCKED` | PASS |
| Downstream handoff | prompts, model/mode, duration, reference IDs, continuity/motion priorities, NOT constraints, take log, and blocked reasons are present | PASS |

## Episode handoff trace

1. EP01 ends with the drawer closed and key with Lin; EP02 opens on that exact state.
2. EP02 opens the drawer, keeps the key with Lin, transfers the cassette to her, and pays `DEBT_KEY_ORIGIN`; EP03 opens on that exact state.
3. EP03's planned memory insert needs the mother's identity reference. Because it is missing, the segment is blocked and the draft State Delta is not promoted to canonical state.

## P0 simulation

The simulated rejected take `TAKE_EP02_SG04_01` makes `PROP_KEY` disappear before the drawer-opening segment. The Retake Patch targets `EP02-SC01-SG04` only, keeps the key visibly inserted under Lin's right hand, and preserves every accepted surrounding variable. No episode-wide regeneration is requested.

## Known benchmark limit

This is a deterministic artifact/dry-run benchmark. It proves state, contracts, readiness, blocking, and retake scope. It does not prove a provider's visual quality, dialogue generation, or identity consistency; those require real executor output followed by the Review workflow.
