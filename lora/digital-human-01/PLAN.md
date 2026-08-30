# Digital Human LoRA V1 — Dataset Expansion Plan

Status: dataset expansion in progress
Updated: 2026-08-30

## 1. Goal

Train a reusable identity LoRA for the approved digital human so that future generation can change clothing, pose, action, camera angle, and environment while preserving the same person.

Primary downstream use: realistic Xiaohongshu-style street photography and lifestyle content.

## 2. Canonical identity references

Every new candidate image MUST directly use both original references. Generated candidates are never promoted to canonical identity references.

### AAAA — full-body three-view reference

AAAA is the body geometry Ground Truth and controls:

- shoulder width
- shoulder/neck relationship
- head-to-body ratio
- chest/waist/hip relationship
- waist height
- arm length
- leg length and thigh/calf proportions
- overall slim body silhouette
- hair length and body-level hair silhouette

### BBBB — close-up three-view reference

BBBB is the facial identity Ground Truth and controls:

- face shape
- forehead and hairline
- eyebrows
- eye shape and eye spacing
- nose bridge, tip, and nostril structure
- lips and mouth shape
- jawline and chin
- front/three-quarter/profile facial geometry
- overall recognizability

### Fixed priority

`AAAA + BBBB identity geometry > current pose/action > clothing > environment/styling`

Rules:

- Change clothes, not identity.
- Change action, not identity.
- Do not generate from the previous candidate alone.
- Do not rely only on a text description of the character.
- If identity or body geometry drifts, reject and regenerate from AAAA + BBBB.

## 3. Existing dataset status

The foundational candidate rounds have already been generated and manually approved in chat. The user also saved additional usable images outside the explicitly tracked list; exact local image count is intentionally not treated as authoritative at this stage.

Known approved coverage already includes:

- front close-up
- left/right 45-degree close-up
- left/right profile
- slight camera-angle variation
- front half-body
- half-body light action
- full-body front and three-quarter views
- multiple clothing changes
- back/turning pose
- phone interaction
- camera handling
- cup holding
- hand-in-pocket pose
- walking
- light hand gesture

Incorrect intermediate generations (wrong action, collage/triptych, identity drift, wrong task) must not enter the training dataset.

## 4. Current strategy: skip another slow pre-filter pass

Do not pause now for a detailed A/B/C grading of all existing images.

Instead:

1. Treat previously approved images as the current baseline dataset.
2. Generate S01–S16 as a dedicated street/lifestyle expansion set.
3. Validate each S image immediately.
4. After S01–S16 are complete, perform one consolidated final dataset review.
5. If the resulting set is high quality, stop adding images and move to captions/training rather than mechanically targeting 50 images.

## 5. S01–S16 street expansion

The expansion set should shift the dataset distribution away from studio/reference-sheet imagery and toward natural, realistic urban lifestyle photography.

### S01–S04 — street close-up / half-body

- S01: outdoor street close-up, natural front-facing candid portrait
- S02: street half-body, natural 45-degree angle / light hair-adjusting gesture
- S03: street half-body holding takeaway coffee
- S04: street half-body looking at phone naturally

### S05–S08 — street full-body static

- S05: full-body standing naturally in front of an urban building
- S06: full-body 45-degree standing pose near architectural facade
- S07: full-body relaxed roadside/sidewalk waiting pose, light bag interaction allowed
- S08: full-body pose near cafe/store entrance

### S09–S12 — natural movement

- S09: normal walking stride, candid street-photo feeling
- S10: walking/standing with natural look-back toward camera
- S11: walking while glancing at phone
- S12: exiting a cafe/store while holding a drink or small everyday object

### S13–S16 — lifestyle / creator actions

- S13: commuting with a handbag/crossbody bag
- S14: relaxed urban pose near railing/wall, no fashion-editorial exaggeration
- S15: waiting near a crosswalk / street corner, natural side-front body angle
- S16: holding or using a camera in a believable lifestyle-blogger context

## 6. Clothing policy for S01–S16

Clothing should feel random to the user, but use controlled randomness to protect dataset diversity.

### Randomization rules

- Do not pre-assign a fixed outfit to every S image.
- Randomly select clothing for each image.
- Avoid repeating a very similar silhouette/outfit within the previous ~3 accepted S images.
- Favor varied everyday silhouettes across the 16 images.
- Keep clothing subordinate to identity.

Possible wardrobe categories include:

- T-shirt / simple top
- casual shirt
- blouse + trousers
- knit top + trousers/skirt
- jeans-based casual outfit
- simple dress
- light suit / blazer look
- trench/light outerwear
- refined commuting outfit

Avoid:

- strong visible logos
- hats/sunglasses that obscure identity
- heavy accessories
- extreme editorial styling
- costumes
- clothing that hides most body geometry

## 7. Street-photo visual target

Target:

- realistic urban photography
- natural daylight / believable ambient light
- candid or lightly directed poses
- clean but real streets, cafes, storefronts, architecture
- Xiaohongshu lifestyle/commuting/street-photo feel
- natural body mechanics

Avoid:

- excessive studio-gray backgrounds in S01–S16
- fashion-magazine hard posing
- exaggerated perspective
- extreme low/high angles
- strong motion blur that destroys identity
- dense crowds covering the subject
- over-retouched skin / plastic AI look
- overly dramatic cinematic lighting

## 8. Per-image generation and QC protocol

For every S image:

1. Re-load/re-use ORIGINAL AAAA + ORIGINAL BBBB as direct references.
2. Lock the current S task/action explicitly before generation.
3. Randomize clothing under the controlled-random rules.
4. Choose a realistic street/lifestyle environment compatible with the task.
5. Generate a SINGLE final image, never a contact sheet/triptych.
6. Self-check before presenting.
7. User approves/rejects.
8. Only approved images enter the candidate set.

### Self-check order

1. Same person as BBBB?
2. Face geometry stable: eyes, nose, mouth, chin, hairline?
3. AAAA shoulder width and shoulder/neck relationship preserved?
4. Head/body and limb proportions consistent with AAAA?
5. Is the requested S action actually present?
6. Are hands/props anatomically and mechanically believable?
7. Is it one image rather than a collage?
8. Does the street/lifestyle image look natural rather than staged/AI-like?

Any failure means regenerate before moving to the next S number.

## 9. After S01–S16

When the expansion round is complete:

### Final dataset review

- remove identity-drift images
- remove geometry-drift images
- remove duplicate/redundant poses
- remove poor hands/props if materially distracting
- verify angle distribution
- verify close-up / half-body / full-body distribution
- verify studio / street / lifestyle distribution
- verify clothing diversity

Do not optimize for a specific image count. Prefer a smaller high-quality set over padding the dataset.

### Caption stage

Then prepare a consistent caption set with:

- one unique identity trigger token
- identity wording kept stable
- angle/action/background described when useful
- clothing described objectively
- clothing wording varied enough to avoid binding identity to a specific outfit

### Training package stage

After captions are approved:

- normalize filenames
- pair image/caption files
- create validation prompts
- create training config
- train LoRA V1 using Codex/local GPU/cloud GPU workflow

### V1 validation

Stress-test at least:

- baseline identity
- new outfit
- walking
- sitting
- phone action
- camera action
- indoor lifestyle scene
- outdoor street scene
- front / 45-degree / profile angles

Success criterion: change clothing, action, camera angle, and environment without changing the person.

## 10. Current next action

Start S01 and proceed sequentially through S16. Do not start caption/training configuration until the street expansion and consolidated dataset review are complete.
