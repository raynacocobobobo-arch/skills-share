# Build Character Asset Workflow V2

## Preconditions
Required:
- L0 SOURCE
- approved L1 IDENTITY MASTER
- Identity Gate = PASS

## Body Master
Build body candidates from SOURCE + approved IDENTITY MASTER + factual body data when available. Neutral front/side/back views define proportions and silhouette, not facial identity.

If body regions are unseen in SOURCE, label them `synthetic completion`.

## Body Gate
Check height impression, body mass, shoulder width, torso/waist, leg proportions, posture, age/body compatibility, and preservation of approved face identity.

FAIL → reject candidate and regenerate from SOURCE + approved IDENTITY MASTER. Never chain from failed body output.

## Three-View Rule
A three-view sheet is primarily a BODY/APPEARANCE asset. It does not become an identity master simply because faces are visible in the sheet.

## Appearance Layer
After body approval, define clothing, PPE, accessories, hair styling, footwear, and photography direction. Appearance may change presentation but cannot redefine identity.

## Pose / Prop Assets
Complex poses and equipment should be treated as separate assets. Prototype difficult hand placement, load-bearing, cameras, monopods, tools, or other geometry before final identity integration when practical.

## Approved Reference Pool
Every generated asset is CANDIDATE, APPROVED, or REJECTED. Only APPROVED assets may be reused. REJECTED assets never enter identity inputs.

## Output
A traceable package containing SOURCE, IDENTITY MASTER, BODY MASTER, APPEARANCE assets, approved pose/prop assets where needed, and uncertainty notes.
