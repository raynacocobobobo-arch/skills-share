# Review and Retake

Stage order: `media review -> P0/P1/P2 -> PASS or Retake Patch -> retry -> accept take -> update episode state`

## Inputs

- executor-returned media/take metadata;
- approved Episode Card, Continuity State, Shot Specs, Production Pack, and references;
- draft State Delta and Continuation Capsule.

Read [QA rules](../references/qa-rules.md) and use [retake-patch.json](../templates/retake-patch.json).

## Procedure

1. **Media review:** verify the actual output/take ID, then compare visible facts and boundaries against the approved artifacts.
2. **Classify:** assign P0/P1/P2 with an observable reason. Do not use `PASS` when required media has not been inspected.
3. **Decide:** accept clean media, record optional P2, or create a Retake Patch for the affected shot/segment. P0 requires retake; P1 normally does.
4. **Retry:** preserve accepted variables and change only diagnosed `fix` variables. If the same failure repeats, reassess references, simplify/split the segment, or change to a verified generation mode.
5. **Accept take:** append the executor result and QA decision to the take log. Rejected takes cannot become canonical references or tail frames.
6. **Update episode state:** after required segments pass, finalize the State Delta and Continuation Capsule from what actually occurred, then update the Series Bible canonical state.

An isolated failed shot/segment never triggers whole-episode regeneration. Missing media or assets remains `BLOCKED`; contradictory evidence remains `NEEDS_REVIEW`.

## Outputs

- per-take QA result and segment `PASS`/`NEEDS_REVIEW`/`BLOCKED` status;
- targeted Retake Patch when required;
- accepted take log;
- approved State Delta, Continuation Capsule, and updated canonical state when the episode passes.
