---
name: creator-to-skill-research
description: Creator 研究与 Skill 蒸馏工作流——基于原始字幕批量提取稳定 Workflow Pattern 和 Capability，并映射到现有 Hermes Skill 或新 Skill。
triggers:
  - Creator Distillation
  - creator distillation
  - Creator 蒸馏
  - KOL 蒸馏
  - KOL 研究
  - 创作者研究
  - 创作者蒸馏
  - 工作流蒸馏
  - 能力蒸馏
  - creator to skill
---

# Hermes Creator To Skill Research

## Purpose

将优秀 Creator 的真实经验转化为 Hermes 可复用能力。

目标不是创建 Creator 分身，而是提取：

- 可执行工作流
- 方法论
- 判断标准
- 项目改进方式

---

# Core Principle

Creator Distillation 必须 source-grounded。

唯一事实来源：

1. 原始字幕文件
2. index.json 定位信息

禁止：

- 根据标题推测内容
- 根据 Creator 印象总结
- 用摘要替代原文
- 用历史记忆替代素材

---

# Mandatory Source Pipeline

必须执行：

```
Creator Distillation 请求
↓
data/creators.json 状态检查
↓
读取 subtitles/YYYY-MM-DD/index.json
↓
解析 entries[]
↓
过滤 up_name
↓
获取 repository_path
↓
GitHub API 读取完整 txt 字幕
↓
确认 source_loaded=true
↓
开始分析
```

如果字幕读取失败：

```
停止分析
禁止生成蒸馏结果
```

---

# Batch Distillation

同一 Creator 必须批量分析：

```
多条字幕
↓
完整阅读
↓
寻找重复出现的方法
↓
去除一次性新闻
↓
提取稳定 Workflow
↓
验证迁移价值
```

---

# Workflow Pattern Extraction

禁止直接从主题或功能名称创建 Skill。

首先提取 Workflow：

```yaml
workflow_pattern:
  name:
  trigger:
  inputs:
  stages:
    - step:
      action:
      ai_role:
      human_role:
  artifacts:
  verification:
```

必须回答：

- 什么时候启动？
- 需要什么输入？
- 有哪些阶段？
- AI 做什么？
- 人做什么？
- 输出什么资产？
- 如何验证质量？

---

# Capability Extraction

流程：

```
Creator Methods
↓
Workflow Pattern
↓
Capability Extraction
↓
Capability Map
↓
Skill Impact Mapping
```

Capability 记录：

```yaml
capability:
  name:
  problem_solved:
  reusable_value:
  workflow_pattern:
  candidate_skills:
  decision:
```

---

# Skill Impact Decision Rules

Capability 不等于 Skill。

必须先检查已有：

```
plugins/hermes-skills/skills/
```

并读取候选 SKILL.md。

## 优先增强已有 Skill

如果：

- 属于已有领域
- 只是增加 Workflow 阶段
- 丰富已有能力

则：

```
Enhance Existing Skill
```

例如：

Business Question → Research → Storyline → Strategy Deck

属于：

```
hermes-business-marketing-copilot
```

不是新建 Research Skill。

---

## 创建新 Skill 条件

必须同时满足：

- 现有 Skill 无法覆盖
- 有独立触发场景
- 有独立输入输出
- 有长期复用价值

否则不要创建。

---

## Shared 方法库规则

不要把单个 Skill 内部阶段提升为 shared。

只有满足：

- 多个 Skill 共用
- 跨领域复用
- 不依赖具体业务场景

才进入 shared。

---

# Creator Is Not Capability

正确关系：

```
Creator
↓
Methods
↓
Workflow Pattern
↓
Capability
↓
Skill
```

禁止：

```
Creator
↓
Creator 专属 Skill
```

---

# Skill Impact Mapping

执行：

```
Capability Map
↓
检查已有 Skills
↓
读取候选 SKILL.md
↓
增强已有 Skill
或
创建新 Skill
```

---

# Tracking

状态文件：

```
hermes-daily-report/data/creators.json
```

记录：

- creator_name
- source_files
- distillation_status
- completed_date
- skills_created
- skills_enhanced

---

# Completion Requirement

完成 Creator Distillation 必须满足：

```
原始字幕已读取
↓
Workflow Pattern 已提取
↓
Capability Map 已生成
↓
Skill Impact 已判断
↓
Skill 创建或增强完成
↓
creators.json 更新
```
