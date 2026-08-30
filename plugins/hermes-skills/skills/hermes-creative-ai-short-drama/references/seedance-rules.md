# Seedance-Oriented Prompt Rules

Use this layer after valid Shot Specs have been compiled into Generation Segments. It prepares model-call prompts; it does not claim that video was generated.

## Capability check

Record the exact target model/version, provider or UI route, supported duration, input modalities, reference limits, audio behavior, and first/last-frame support before execution. As verified on 2026-08-30, ByteDance's official Seedance 2.0 launch describes 15-second multimodal audio-video output, while the official Seedance 2.5 launch describes up-to-30-second generation and expanded references. Therefore V1 keeps 4–15 seconds as a conservative 2.0-oriented planning default, not a universal limit.

Official checks:

- <https://seed.bytedance.com/en/blog/seedance-2-0-%E6%AD%A3%E5%BC%8F%E5%8F%91%E5%B8%83>
- <https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5>

If the selected model changes, re-check capability and record the result in the Production Pack. Do not silently stretch or truncate segments.

## Prompt contract

Each model-ready prompt must express, in concrete visible terms:

1. scene snapshot and fixed geography;
2. bound reference roles and what each must control;
3. participating character identity/costume/position;
4. ordered visible action compatible with the segment duration;
5. required ending state and tail-frame behavior;
6. camera framing/movement;
7. dialogue/sound intent when supported, otherwise post-production policy;
8. concise `NOT` constraints protecting continuity.

Keep planning notes, QA, agent reasoning, and blocked-state explanations outside the model-ready prompt.

## Reference discipline

- Bind each reference to one or more named roles; never assume the provider understands an unlabeled asset list.
- Use an approved first frame to lock opening composition and an approved last frame only when the route supports it.
- Use identity, scene, and prop references for recurring continuity; use video references only when rights and route capability are confirmed.
- Resolve conflicting references before generation. If two assets disagree about costume, geography, or prop state, mark `NEEDS_REVIEW`.

## Text and dialogue

Plot-critical dialogue is story information and must remain in the Production Pack. If the chosen route cannot produce reliable dialogue/audio, preserve timing and performance intent for dubbing/editing rather than deleting it.

Do not ask the video model to render complex readable Chinese UI, messages, signage, or evidence text. Generate a clean plate/screen and specify the exact text as a post-production overlay.

## NOT constraints

Use a short risk-specific list: no identity drift, no costume reset, no prop disappearance, no axis reversal, no extra characters, no unintended text, and no end-state change beyond the Shot Specs. Avoid generic negative-prompt spam.
