---
name: hermes-creative-digital-human
description: 创建真人感数字人博主，并将数字人与真实环境、服装和摄影条件融合，用于小红书等内容生产。
version: 1.0.0
---

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

Identity stability is more important than beauty score.

Before generating content:
- check whether a character asset exists
- create identity references if missing

Do not regenerate a different person every time.

Minimum identity reference:
- face reference
- three view reference
- body reference
- style reference

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

## Quality Check Order

When improving output, check in this order:

1. identity consistency
2. body proportion
3. perspective
4. lighting
5. skin texture
6. social media style

Do not optimize all variables at the same time.

## Quality Check

Before output check:
- same person
- correct perspective
- matching light
- natural skin
- believable photography
