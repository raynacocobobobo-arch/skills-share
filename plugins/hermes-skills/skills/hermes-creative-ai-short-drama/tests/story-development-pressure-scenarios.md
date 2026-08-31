# Story Development Pressure Scenarios

These are regression scenarios for `hermes-creative-ai-short-drama` story-development behavior. They are not project canon.

## Scenario 1 — historical canon collision

Input: an existing project has an early transcript, a middle revision, and a later transcript. The early version contains a strong scene that the later version replaced.

Expected:
- load latest canon first;
- order sources chronologically;
- later explicit decision wins on the same scope;
- early material may restore intent only where later canon is silent;
- replaced scene is `SUPERSEDED`, not silently revived.

## Scenario 2 — same episode in new clothes

Input: earlier episodes already used “two systems disagree -> confirm minimum shared facts -> open a passage.” A new episode proposes a different location and different civilians but the same grammar.

Expected:
- Episode Function Audit flags repetition before screenplay;
- agent states what prior episode already paid off;
- revise to a genuinely new dramatic question or pressure type.

## Scenario 3 — scoped approval

Input: user says, “The structure works. The dialogue is bad. Git the rest.”

Expected:
- structure/function may become `LOCKED`;
- dialogue remains `TBD` or rejected candidate;
- no dialogue is copied into canon merely because the episode was otherwise approved.

## Scenario 4 — over-explained solution

Input: the causal solution is valid, but the assistant can explain five files, three permissions, and a long search trail that led the character to it.

Expected:
- lock causal justification backstage;
- expose only the minimum fact/action needed to understand why the choice is available;
- no research-chain exposition unless it affects the decision.

## Scenario 5 — third path without a cost

Input: A and B are both bad; a clever character proposes C and everyone keeps everything.

Expected:
- fail the Cost Gate;
- identify the assumption C rejects;
- require an irreversible loss, degradation, redistributed burden, or other established cost unless the premise explicitly supports a free solution.

## Scenario 6 — finale sacrifice shortcut

Input: finale introduces a new device that only exists to kill/sacrifice a beloved character. The character volunteers, leaving the protagonist with no meaningful choice.

Expected:
- reject or revise;
- private cost must grow from an earlier-established rule;
- affected character may have agency, but protagonist/public decision retains independent moral ownership;
- no unearned survival loophole after the cost is paid.
