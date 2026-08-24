# Hermes Creative Digital Human

## Purpose

Create a consistent AI digital human creator asset and generate realistic social media photography.

This skill is not for one-off AI portraits. It builds a reusable character and places that character into real environments.

## Trigger

Use for:
- 创建数字人
- 虚拟博主
- AI博主
- 数字人与真实环境融合
- 数字人换装
- 小红书真人感内容

## Core Rules

### Identity First

A digital human must maintain identity consistency.

Before generating content:
- check whether a character asset exists
- create identity references if missing

Do not regenerate a different person every time.

### Reality First

Output target is realistic photography.

Match:
- camera perspective
- lighting
- depth of field
- color
- environment relationship

## Workflow Routing

New character:
`workflows/create-character.md`

Existing character:
`workflows/generate-realistic-content.md`

Bad output:
`workflows/improve-output.md`

## Asset Minimum

A character should have:
- face reference
- three view reference
- body reference
- style reference

## Quality Check

Before output check:
- same person
- correct perspective
- matching light
- natural skin
- believable photography
