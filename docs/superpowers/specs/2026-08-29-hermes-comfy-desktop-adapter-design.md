# Hermes Digital Human → Comfy Desktop Adapter Design

Date: 2026-08-29
Status: Proposed for implementation after user review
Target repository: `raynacocobobobo-arch/skills-share`
Target host: Windows desktop, NVIDIA RTX 4060 8 GB VRAM, 16 GB system RAM
Parent skill: `plugins/hermes-skills/skills/hermes-creative-digital-human`

## 1. Goal

Add a thin, local-first Comfy Desktop adapter for `hermes-creative-digital-human` so the existing Hermes digital-human rules can be executed as a reproducible local image-generation workflow without OpenAI Image API usage.

The first release must let Codex configure the user's Windows machine so Comfy Desktop can accept these inputs:

- approved face / identity reference
- approved body reference
- wardrobe reference
- pose reference
- scene reference
- textual shot description

and produce:

1. one controlled 3:4 digital-human image for validation; then
2. a three-shot variant that shares the same upstream identity/body/wardrobe/scene assets while allowing shot-specific pose, prompt, and seed.

The adapter does not replace Hermes. Hermes remains the policy and production-rule layer; Comfy Desktop becomes one execution backend.

## 2. Non-goals

V1 will not:

- create a new global digital-human registry;
- overwrite or redefine the existing Identity Anchor lifecycle;
- treat generated images as new identity masters;
- silently promote rejected outputs into reusable references;
- require paid OpenAI image APIs;
- attempt a heavy FLUX-class workflow on the RTX 4060 as the default path;
- provide a separate public web application in V1;
- guarantee exact identity preservation when the installed Comfy components cannot provide identity-aware conditioning;
- run three expensive branches concurrently by default on an 8 GB GPU.

The existing Hermes V2.4 rules remain authoritative for identity gating, explicit master re-attachment, reference roles, no-generation-chaining, final triage, and face-repair eligibility.

## 3. Design principles

### 3.1 Hermes is the contract; Comfy is the executor

The adapter translates Hermes concepts into Comfy bindings. It must not invent a parallel identity system.

Canonical mapping:

| Hermes role | V1 Comfy responsibility | Identity authority |
|---|---|---|
| `IDENTITY ONLY` | identity-aware face conditioning | yes, upstream only |
| `BODY ONLY` | low-strength body / silhouette reference | body only |
| `WARDROBE ONLY` | appearance / clothing reference | no |
| `POSE ONLY` | pose extraction + ControlNet | no |
| `SCENE ONLY` | environment / composition reference | no |

### 3.2 Explicit assets, never inferred roles

Every image input must be selected into a named slot. The workflow must never infer role from visual similarity.

The adapter uses stable slot names:

- `face`
- `body`
- `wardrobe`
- `pose`
- `scene`

Each slot resolves to exactly one Hermes role in configuration.

### 3.3 Star topology is mandatory

Every candidate must originate from the approved upstream identity/body references, not from a previous generated candidate.

Allowed:

```text
IDENTITY_MASTER + BODY_MASTER + references -> candidate_01
IDENTITY_MASTER + BODY_MASTER + references -> candidate_02
IDENTITY_MASTER + BODY_MASTER + references -> candidate_03
```

Forbidden:

```text
candidate_01 -> candidate_02 -> candidate_03
```

Face repair remains the narrow Hermes exception: a failed candidate may serve only as composition carrier while approved identity evidence remains authoritative.

### 3.4 RTX 4060 first

V1 must be designed around 8 GB VRAM and 16 GB system RAM.

Defaults:

- SDXL-class realistic checkpoint as the baseline model family;
- 3:4 generation target around `768x1024` for first-pass validation;
- single-image execution first;
- sequential three-shot execution for the triple workflow;
- optional face-detail pass only after the base candidate exists;
- no simultaneous loading of unnecessary large model stacks;
- no default 1024x1536 high-cost pipeline;
- no default heavy multi-ControlNet stack.

If the installed Comfy build exposes documented memory-saving flags or device/offload controls, the local runbook may enable them only after detecting the actual installation and without assuming a fixed path.

## 4. Repository layout

The adapter lives with the parent skill so ChatGPT/Codex and Comfy-specific execution rules evolve together.

```text
plugins/hermes-skills/skills/hermes-creative-digital-human/
└── comfy-adapter/
    ├── README.md
    ├── config/
    │   ├── asset-role-map.yaml
    │   ├── node-list.json
    │   └── model-recommendations.yaml
    ├── docs/
    │   ├── setup-windows-rtx4060.md
    │   ├── workflow-design.md
    │   ├── codex-local-runbook.md
    │   └── troubleshooting.md
    ├── scripts/
    │   ├── collect-system-info.ps1
    │   ├── bootstrap-comfy.ps1
    │   ├── validate-comfy-env.ps1
    │   └── link-workflows.ps1
    ├── templates/
    │   ├── shot-contract-template.md
    │   └── generation-checklist.md
    └── workflows/
        ├── hermes-dh-v1-single.json
        ├── hermes-dh-v1-triple.json
        └── workflow-notes.md
```

The adapter must not modify `manifests/skill-registry.json` merely because a backend adapter was added. This is not a new top-level skill.

## 5. Components

### 5.1 `README.md`

The adapter entry point. It explains:

- what the adapter is;
- supported machine profile;
- that Comfy Desktop executes images while Hermes supplies production rules;
- prerequisites;
- install order;
- single-workflow validation first;
- triple-workflow activation second;
- links to troubleshooting and Codex runbook.

### 5.2 `asset-role-map.yaml`

Machine-readable role mapping. It is intentionally small and is not a new registry.

Required conceptual shape:

```yaml
schema_version: 1
parent_skill: hermes-creative-digital-human
slots:
  face:
    hermes_role: IDENTITY_ONLY
    priority: CRITICAL
    comfy_strategy: identity_conditioning
  body:
    hermes_role: BODY_ONLY
    priority: HIGH
    comfy_strategy: reference_low_strength
  wardrobe:
    hermes_role: WARDROBE_ONLY
    priority: NORMAL
    comfy_strategy: reference_appearance
  pose:
    hermes_role: POSE_ONLY
    priority: NORMAL
    comfy_strategy: pose_controlnet
  scene:
    hermes_role: SCENE_ONLY
    priority: NORMAL
    comfy_strategy: reference_scene
```

No numeric weights are part of the Hermes role contract. Numeric node parameters, when needed by a concrete workflow, belong in the workflow and workflow notes because they are backend implementation details.

### 5.3 `node-list.json`

Declares required and optional Comfy custom-node packages by repository URL / package identity and purpose. It must distinguish:

- required for V1 single workflow;
- optional enhancement;
- required only for triple workflow if any.

Codex uses this file to check what is installed before making changes.

The install scripts must not assume a node's folder name proves that the node loaded successfully; environment validation must also inspect Comfy startup/output where practical.

### 5.4 `model-recommendations.yaml`

Declares model families and expected Comfy model categories, not copyrighted model binaries.

V1 categories:

- realistic SDXL checkpoint;
- identity-conditioning model files required by the selected identity node;
- CLIP Vision / adapter weights required by the selected reference adapter;
- SDXL-compatible pose ControlNet;
- pose preprocessor model files where required.

The repository stores only metadata, expected destination folders, and source/retrieval guidance. Large model weights do not belong in `skills-share`.

### 5.5 PowerShell scripts

All scripts must be idempotent where possible and fail visibly rather than guessing.

#### `collect-system-info.ps1`

Read-only diagnostics:

- Windows version;
- GPU name and reported VRAM;
- system RAM;
- candidate Comfy Desktop locations;
- candidate custom-node and model paths;
- git availability;
- PowerShell version.

It must not install anything.

#### `bootstrap-comfy.ps1`

Local installation helper executed by Codex after inspection. Responsibilities:

- accept an explicit Comfy root when auto-detection is ambiguous;
- verify git exists before cloning custom nodes;
- install only packages declared by `node-list.json`;
- avoid deleting or overwriting unrelated custom nodes;
- skip already-present repositories when the remote matches;
- stop on mismatched repositories instead of force-resetting them;
- never download multi-gigabyte model weights without an explicit Codex/user action derived from the runbook.

#### `validate-comfy-env.ps1`

Read-only validator with non-zero exit on required failures. Checks:

- Comfy root resolved;
- required node directories present;
- expected model directories present;
- required workflow JSON files are syntactically valid;
- workflow files do not contain unresolved placeholder node types;
- enough disk-space information can be reported;
- optional components are marked warning, not failure.

It must print a compact PASS / WARN / FAIL summary suitable for Codex to quote back.

#### `link-workflows.ps1`

Copies (or, if explicitly requested, links) the versioned workflow JSON files into a user-selected Comfy workflow location. Default behavior is copy, not symlink, to avoid Windows permission/developer-mode assumptions.

It must not overwrite a changed destination workflow silently. Existing destination content is compared; conflicting copies get a timestamped backup or the operation stops according to an explicit flag documented in the runbook.

## 6. V1 workflow architecture

### 6.1 Baseline model family

V1 uses SDXL because the target hardware is 8 GB VRAM and the required identity/reference/pose ecosystem is mature enough for a first controlled workflow.

A realistic checkpoint is selected locally. The repository does not hard-code a single aesthetic model as identity truth.

### 6.2 Identity path

`face` is the only slot that may control facial identity.

Preferred implementation tier is an identity-aware node stack compatible with the chosen SDXL workflow (for example InstantID-class or equivalent supported by the installed Comfy environment). The exact supported node implementation must be verified during implementation against current upstream documentation.

The workflow notes must label this path `IDENTITY ONLY | CRITICAL`.

Wardrobe, scene, body, and pose references must not be routed into identity-conditioning inputs.

### 6.3 Pose path

`pose` is processed by a pose detector such as DWPose/OpenPose and applied through an SDXL-compatible pose ControlNet. The extracted pose, not the reference person's identity, is the intended information carrier.

If pose extraction fails or produces implausible skeleton geometry, generation is blocked for that shot until the pose input is corrected or pose control is disabled explicitly.

### 6.4 Wardrobe / body / scene references

These are non-identity reference paths.

V1 should use an IPAdapter-class / reference-adapter strategy where current node compatibility allows:

- `body`: low-strength global body/silhouette support;
- `wardrobe`: appearance/clothing support;
- `scene`: environment/composition support.

Because multiple simultaneous adapters can increase VRAM use and create competing conditioning, V1 is allowed to use staged or simplified reference application rather than forcing all references at maximum strength.

If an exact clothing transfer cannot be achieved reliably with reference conditioning alone, the workflow must report this as a backend limitation rather than claiming Hermes identity rules failed.

### 6.5 Prompt path

The workflow accepts a user shot description plus a generated/edited Hermes shot contract. Prompt text can describe:

- framing;
- camera angle;
- subject orientation;
- action details not fully represented by pose;
- lighting intent;
- realism and lens/photography language;
- exclusions that reduce unwanted visual contamination.

Prompt text cannot replace the explicit identity master.

### 6.6 Sampling and output

The single workflow produces one candidate at a time.

The triple workflow creates three explicit shot tasks sharing the same upstream asset set. On RTX 4060 8 GB, shots execute sequentially. Each shot may have an independent:

- prompt suffix;
- pose image;
- seed;
- framing/camera instruction.

Output filenames must include at minimum:

- character / project token supplied by operator;
- workflow version;
- shot id;
- seed or execution identifier.

Generated files remain downstream content and are never automatically written into the upstream identity directories.

## 7. Three-shot behavior

The three-shot workflow is not `batch=3` random variation. It is three separate shot contracts.

Example:

```text
shared: face + body + wardrobe + scene

SHOT01: front medium-close, direct gaze, pose A
SHOT02: 45-degree medium, look toward poster, pose B
SHOT03: half-body candid turn, pose C
```

For 8 GB VRAM, the implementation must prefer queueing these as three sequential executions rather than constructing a graph that keeps three full sampler branches resident simultaneously.

If Comfy's workflow format makes true sequential subjobs impractical inside one graph, the adapter may provide a queue helper or duplicated workflow submission instructions, but the user-facing semantics remain "one task package, three explicit shots".

## 8. Face repair

V1 may document and prepare for Hermes `FACE_REPAIR`, but the first acceptance milestone does not require a fully automated face-repair graph.

A later repair workflow may accept:

- failed candidate as composition carrier;
- active approved identity master;
- matching approved face crop;

and edit only the face region while preserving body, wardrobe, pose, scene, and major lighting.

No repair output is promoted to Identity Master automatically.

## 9. Codex local runbook contract

Codex is the local operator. The GitHub runbook must tell it to:

1. pull the latest `skills-share`;
2. read this design and adapter README;
3. run system-info collection;
4. detect the actual Comfy Desktop root and stop for ambiguity;
5. inspect existing custom nodes and models before installation;
6. install only missing required node packages;
7. report model files that require download and their destination;
8. validate the environment;
9. copy the single workflow;
10. launch/restart Comfy Desktop as appropriate;
11. run the single-image smoke test with user-provided references;
12. collect the resulting errors/output if the smoke test fails;
13. enable/copy the triple workflow only after the single workflow passes.

Codex must not force-reset the user's unrelated repositories, remove arbitrary nodes, or overwrite unknown model files.

## 10. Acceptance criteria

### Milestone A — repository adapter is complete

Pass when:

- all documented adapter files exist;
- configuration parses;
- PowerShell scripts parse and have clear exit behavior;
- workflow JSON parses;
- README and Codex runbook give an unambiguous install order;
- no new global skill registry is introduced.

### Milestone B — local single workflow is installed

Pass when Codex verifies on the target machine:

- Comfy Desktop starts;
- required nodes load;
- required model paths resolve;
- `hermes-dh-v1-single.json` opens without missing-node errors;
- one 3:4 candidate can be generated from explicit asset slots;
- the output is saved to downstream output only.

### Milestone C — identity and role behavior is usable

Pass is a human decision. A candidate must:

- be recognizably the approved identity;
- not inherit the pose/wardrobe/scene reference person's face;
- follow pose strongly enough to be useful;
- preserve plausible body perspective;
- integrate scene lighting/perspective sufficiently for iteration.

If identity fails, Hermes Identity Gate fails regardless of how attractive the image is.

### Milestone D — three-shot workflow

Pass when:

- three explicit shot contracts can be queued from the same approved upstream asset set;
- they run sequentially on the 8 GB GPU without intentional simultaneous full-branch execution;
- each shot can vary pose/prompt/seed;
- all three outputs retain independent traceable filenames.

## 11. Testing strategy

Repository-level tests are lightweight because Comfy execution requires the user's local runtime.

Implementation must include checks for:

- JSON/YAML parseability;
- PowerShell syntax / PSScriptAnalyzer-compatible basic correctness where available;
- idempotent dry-run / validation behavior;
- conflict-safe workflow copying;
- explicit failure for unresolved Comfy root;
- explicit failure for missing required nodes;
- warning-only behavior for optional nodes;
- workflow JSON free of textual placeholder node types.

Local acceptance tests are executed by Codex on the user's machine and recorded in its response, not committed as evidence that identity passed unless the user explicitly approves the resulting image.

## 12. Error handling

The adapter follows "stop rather than guess" for identity-critical or filesystem-destructive ambiguity.

Hard failures:

- Comfy root ambiguous or missing;
- required custom node missing after installation attempt;
- required workflow cannot parse;
- required model component missing at generation time;
- destination workflow conflict when overwrite policy is not explicit;
- pose preprocessing failure when pose is declared required.

Warnings:

- optional FaceDetailer / repair component missing;
- optional quality enhancement unavailable;
- hardware differs from the tuned RTX 4060 profile but remains potentially compatible.

## 13. Security and maintenance

- Scripts execute only local filesystem and git operations described in documentation.
- No API keys are required for core V1.
- Node repositories and model metadata are explicit and reviewable.
- No arbitrary remote script piping into PowerShell.
- Git repositories are cloned normally so Codex can inspect changes.
- Future upstream node compatibility changes should update `node-list.json`, `model-recommendations.yaml`, and workflow notes without rewriting Hermes identity semantics.

## 14. Implementation order

1. Add adapter configs, documentation skeleton, and validation tests.
2. Add read-only system detection and environment validation scripts.
3. Add safe bootstrap and workflow-copy scripts.
4. Build and validate the V1 single workflow against current Comfy custom-node schemas.
5. Complete the RTX 4060 setup guide and Codex runbook from the actual workflow dependencies.
6. Validate locally through Codex.
7. Add/enable the triple sequential shot task after the single path passes.

This order deliberately prevents spending time on the three-shot production layer before the core identity-controlled single-image path works on the target machine.
