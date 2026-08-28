# Build Character Asset Workflow V2.1

## Preconditions
Required:
- L0 SOURCE
- approved L1 IDENTITY MASTER
- Identity Gate = PASS

At the start of a new chat or asset-building session, explicitly re-attach the approved IDENTITY MASTER. Do not rely on conversation history to recover the face.

## Body Master
Build body candidates from SOURCE + explicitly re-attached approved IDENTITY MASTER + factual body data when available. Neutral front/side/back views define proportions and silhouette, not facial identity.

If body regions are unseen in SOURCE, label them `synthetic completion`.

## Standard Three-View
Create the standard front/side/back asset as the user-facing Step 3 after Identity Master approval. Its primary authority is BODY/APPEARANCE geometry; visible faces must still preserve the approved identity anchor.

Each view begins as a candidate. Do not use one generated view as the identity source for generating the next view. Keep the topology star-shaped around SOURCE / approved IDENTITY MASTER.

## Body Gate
Check height impression, body mass, shoulder width, torso/waist, leg proportions, posture, age/body compatibility, and preservation of approved face identity.

FAIL → reject candidate and regenerate from SOURCE + explicitly re-attached approved IDENTITY MASTER. Never chain from failed body output.

## Three-View Rule
A three-view sheet is primarily a BODY/APPEARANCE asset. It does not become an identity master simply because faces are visible in the sheet.

The completed three-view set must pass the user-facing Step 4 Identity Validation before wardrobe or environment production. If a visible face drifts, apply Candidate Hard Stop to that candidate and return to the approved master.

## Appearance Layer
After body and identity validation, define clothing, PPE, accessories, hair styling, footwear, and photography direction. Appearance may change presentation but cannot redefine identity.

## Pose / Prop Assets
Complex poses and equipment should be treated as separate assets. Prototype difficult hand placement, load-bearing, cameras, monopods, tools, or other geometry before final identity integration when practical.

## Approved Reference Pool
Every generated asset is CANDIDATE, APPROVED, or REJECTED. Only APPROVED assets may be reused. REJECTED assets never enter identity inputs.

## Output
A traceable package containing SOURCE, IDENTITY MASTER, STANDARD THREE-VIEW / BODY MASTER, APPEARANCE assets, approved pose/prop assets where needed, stable asset names, and uncertainty notes.
