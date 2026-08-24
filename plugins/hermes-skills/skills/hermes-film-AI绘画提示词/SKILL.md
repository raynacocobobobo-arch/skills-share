---
name: AI绘画提示词
description: 根据分镜描述生成国产AI绘画软件的中文提示词，六要素公式+三大视觉矛盾内部验证
version: 4.0.0
triggers:
  - 生成绘画提示词
  - 分镜转提示词
  - AI绘画提示词
  - 绘图提示词
  - 画面提示词
  - 肖像提示词
  - 人物肖像
  - 半身像
  - 给我一个提示词
migrated_from: OpenClaw Verita Scriptora v4.0.0
---

# AI绘画提示词兼容入口

> 这是历史兼容入口，不再拥有独立的 canonical 提示词方法。

保留本 Skill 仅为了兼容旧 Router、旧项目和旧调用名 `AI绘画提示词`。收到任务后必须立即按任务类型转入当前 canonical Skill；不要继续执行旧版六要素工作流，也不要在这里维护第二套提示词规则。

## 路由规则

### 单张图 / 静帧

包括：

- 海报、插画、商业视觉；
- 人物肖像、角色设定图；
- 建筑效果图、场景静帧；
- 单个分镜画面的文生图提示词；
- 单张参考图的风格分析与提示词转换。

必须读取并执行：

`plugins/hermes-skills/skills/hermes-image-prompt-design/SKILL.md`

即：`hermes-image-prompt-design` 是单图提示词的 canonical Skill。

### 影视 / 连续镜头 / 视频

包括：

- AI 影视制作；
- 连续镜头和镜头组；
- 多镜头角色 / 场景一致性；
- 资产 Bible；
- 图生视频；
- 视频 Prompt；
- AI 影视生产计划与结果复核。

必须读取并执行：

`plugins/hermes-skills/skills/hermes-film-ai-production/SKILL.md`

即：`hermes-film-ai-production` 是影视生产与视频 Prompt 的 canonical Skill。

## 与分镜 Skill 的关系

如果用户还没有可执行分镜，而任务本质是镜头设计，先路由：

`plugins/hermes-skills/skills/hermes-film-影视分镜/SKILL.md`

分镜锁定后：

- 只需要单张分镜图 → `hermes-image-prompt-design`；
- 需要连续镜头、视频、图生视频或生产一致性 → `hermes-film-ai-production`。

## 兼容边界

- 本文件不得重新发展成第二套图片提示词方法。
- 新工作流不得把 `AI绘画提示词` 作为 Primary Skill。
- 新配置、watchlist、workflow 和 router 扩展应直接使用 canonical Skill 名称。
- 只有历史入口仍引用 `AI绘画提示词` 时才经过这里转发。
