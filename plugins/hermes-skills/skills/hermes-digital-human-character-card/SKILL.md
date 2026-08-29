---
name: hermes-digital-human-character-card
description: Use when the user wants to establish, review, or rebuild a reusable digital-human identity from real-person face/full-body references, especially for 人物卡、锁定人物、面部三视图、全身三视图 or identity setup before content production.
version: 1.3.1
triggers:
  - 人物卡
  - 数字人人物卡
  - 锁定人物
  - 面部三视图
  - 全身三视图
  - 人物三视图
  - character card
---

# Hermes Digital Human Character Card V1.3.1

## Overview
这是一个轻量身份建立 Skill，不是完整数字人生产系统。

**原则：先解决“这个人是谁”，需要哪一步就做哪一步。**

`FACTUAL PROFILE` 可选，只记录用户明确提供或从 SOURCE 可安全观察的信息；它不是必交付项，也不应被做成海报。

原始上传图是第一身份依据。任何 generated output 只能作为辅助参考，不得静默替代 SOURCE。

## STAGED MODE
当用户只是说“路由到 Hermes 人物卡技能 / 锁定这个人物 / 做人物卡”，默认半自动分步：

### Stage 1 — FACE_3VIEW_SHEET
基于原始面部 SOURCE，生成一张简洁面部三视图：

`正脸 / 左45° / 右45°`

目标：同一人物、同年龄感、自然轻表情、统一背景与光线，不添加资料表或全身内容。

完成后停止并问：**“是否继续生成全身三视图？”**

### Stage 2 — BODY_3VIEW_SHEET
用户确认后，基于原始面部图 + 原始全身图生成：

`正面 / 侧面 / 背面`

目标：同一人物、相同身高/体型印象、中性站姿、头到脚完整、统一服装与背景。

完成后必须停止，不自动进入下一次图像生成。固定询问：

**“全身三视图已完成。下一步要换衣服吗？如果要换，请上传服装参考图或描述穿搭；如果不换，也可以直接给环境、姿势或镜头要求。”**

如果继续，交给 `hermes-creative-digital-human` 处理换装、姿势、镜头、环境合成或小红书内容。

## NEXT TURN GATE
Stage 2 完成后，下一次生成必须有明确目标。

**“下一步”不等于自动换装。** 用户只说“下一步 / 继续 / 然后呢”时，只询问选择，不生成图片。

允许继续生成的条件：
- 用户上传服装参考图；或
- 用户明确描述穿搭；或
- 用户明确授权“你来搭 / 随便穿 / 你决定服装”；或
- 用户明确要求环境、姿势、镜头或其他内容任务，并且该任务不需要改变现有服装。

用户说“换衣服”但没有提供服装目标时，先问服装参考图或穿搭描述，**不得自行决定穿搭并生成**。

用户直接给环境/姿势/镜头而未要求换装时，默认保留当前服装，不擅自改衣服。

## DIRECT MODE
用户可以从任意身份步骤直接开始，不要求补跑前置步骤。

典型直达：
- `只做面部三视图` → 直接生成 FACE_3VIEW_SHEET
- `只做全身三视图` → 面部 + 全身 SOURCE 足够时直接生成 BODY_3VIEW_SHEET
- 已有可信身份素材，只想进入换装/环境/姿势 → 直接路由 `hermes-creative-digital-human`

不要为了流程完整性强迫用户重新做人脸或人物卡。

## SOURCE
### SOURCE FACE
优先使用用户原始面部近照；正面和左右 30–45°越完整越好。

### SOURCE FULL-BODY
用于身高印象、体型、肩胯关系和整体比例。没有真实背面时可以保守推断背面，但不能把推断写成观察事实。

### FACTUAL PROFILE
年龄、身高、性别、体重、发型等均为可选。用户没有提供的精确信息不要虚构。

## NORMAL THREE-VIEW
正常情况下，一次生成一张三视图 sheet：
- FACE 任务只包含三张脸部视图
- BODY 任务只包含三张全身视图
- 不做 PROFILE + FACE + BODY 综合海报

每个阶段只把当前阶段的任务交给图像生成器；不要在 FACE 阶段同时介绍 BODY、人物资料卡或未来内容生产。

## QC
FACE 重点检查：五官结构、脸型、发际线、年龄感、左右视角是否仍像同一个人。

BODY 重点检查：体型、身高印象、头身比、肩胯关系、正侧背方向和脸部身份。

用户说“脸跑了 / 不是这个人”时，回到原始 SOURCE 重做，不用跑偏的生成图继续套娃。

## ATOMIC FALLBACK
仅在三视图生成失败时启用；不是默认流程。

适用情况：
- 三视图被模型做成综合人物卡
- 三个面孔明显不是同一个人
- 某一视角结构严重错误，整张 sheet 无法使用

恢复方式：分别生成单视角，再用非生成式拼接组成 sheet：

```text
FACE_FRONT + FACE_LEFT45 + FACE_RIGHT45 → FACE_3VIEW_SHEET
BODY_FRONT + BODY_SIDE + BODY_BACK → BODY_3VIEW_SHEET
```

单视角仍直接回挂原始 SOURCE；不要让一个 generated output 生成下一个角度。

## Handoff
身份建立不是终点。用户要继续时，进入 `hermes-creative-digital-human`：
- 换装
- 改姿势
- 环境合成
- 特定角度内容图
- 小红书成组内容
