# Create Character Workflow V2

## Goal
Create a reusable digital-human identity before solving body, wardrobe, pose, props, or scenes.

## 1. Register SOURCE
Use original user-provided photos and factual body data as L0 SOURCE. Record what is observed versus unknown. Never treat generated completion as factual evidence.

## 2. Build the Face ID Set
Select/crop the strongest identity views from SOURCE where available: front, left 30–45°, right 30–45°, and optional genuine profiles. Prefer clean, minimally stylized, recognizable views.

## 3. Tool Capability Check
Classify the active generation path as Tier A identity-aware, Tier B multi-reference, or Tier C ordinary/prompt generation. Do not promise guaranteed identity lock with Tier B/C.

## 4. Identity Test Grid
Before body or scene production, test identity on a simple neutral background across front, 45° views, supported near-profiles, slight look up/down, and medium shot.

## 5. Identity Gate
Check face ratio, eyes/spacing, brows, nose, mouth, jaw/chin, ears when visible, hairline, age impression, and overall recognizability.

If the user says it is not the same person, Gate = FAIL.

FAIL:
- mark candidate REJECTED
- never reuse it as an identity reference
- if an approved IDENTITY MASTER already exists, return to that master first
- return to SOURCE only if the master is missing, disputed, or itself invalid
- enter the Identity Recovery Loop in `improve-output.md`
- change strategy before retrying; do not rerun an identical prompt

PASS:
- require human approval before promotion to `IDENTITY_MASTER`

## Required Output
- SOURCE inventory
- Face ID Set
- tool capability tier
- Identity Test Grid
- Identity Gate result
- approved IDENTITY MASTER set
- uncertainty/synthetic-completion notes

Do not proceed to body, wardrobe, complex pose, props, or scene work until identity is approved; identity failure should remain an active recovery workflow rather than silently contaminating downstream assets.
