---
name: knowledge-scout
description: Hermes 外部知识侦察与采集入口——发现值得研究的 Creator、AI 工具、工作流与行业来源，获取原始素材、完成价值初筛，并路由给后续研究能力。
triggers:
  - Knowledge Scout
  - knowledge scout
  - 知识侦察
  - 外部知识采集
  - YouTube 研究
  - Bilibili 研究
  - AI 工作流追踪
  - KOL 追踪
  - Creator 追踪
  - watchlist
  - 字幕采集
---

# Hermes Knowledge Scout

## Purpose

Knowledge Scout 是 Hermes 的外部知识发现、采集和初筛入口。

它负责：

- 发现值得长期关注的 Creator 和信息源
- 获取字幕、文章、PDF、GitHub 等原始资料
- 判断素材是否值得继续研究
- 将高价值素材路由给正确的 Hermes Skill

它不是新闻摘要器，也不负责 Creator 深度蒸馏。

---

## Core Workflow

```text
External World
↓
Source Discovery
↓
Source Acquisition
↓
Verify Original Material
↓
Value Triage
↓
Research Routing
```

---

## Boundary

Knowledge Scout 负责：

```text
找到
↓
拿到原始资料
↓
验证
↓
判断是否值得研究
```

Creator To Skill Research 负责：

```text
完整阅读原始字幕
↓
批量分析
↓
Workflow Pattern
↓
Capability Extraction
↓
Skill Impact
```

如果用户要求完整拆解某个 Creator：

```text
Knowledge Scout
↓
hermes-creator-to-skill-research
```

---

## Watchlist

Creator 和长期来源统一由：

```text
config/watchlist.yaml
```

管理。

不要把 Creator 名单硬编码在 `SKILL.md` 中。

优先保留：

* 有稳定产出的 Creator
* 有真实工作流演示
* 有可复用方法论
* 能持续提供新能力信号

降低优先级：

* 纯新闻搬运
* 纯产品发布转述
* 只有观点没有方法
* 高度重复的信息源

---

## Source Rules

原始素材优先级：

1. 完整字幕 / transcript
2. 官方文章
3. PDF
4. GitHub / 官方技术资料
5. 官方产品文档
6. 其他可验证的一手来源

禁止：

```text
标题
↓
猜测内容
↓
生成方法论
```

也禁止：

```text
二手摘要
↓
再次总结
↓
直接修改 Skill
```

如果没有获得原始资料，必须明确标记：

```text
source_not_loaded
```

不能假装已经完成研究。

---

## Transcript Rule

视频研究优先获取完整字幕。

允许使用：

* 官方字幕
* 平台字幕
* 公开 transcript
* 已保存字幕文件

如果字幕无法获取：

```text
transcript_unavailable
```

不要根据标题继续编造分析。

除非用户明确要求，否则不要自动启动高成本语音转写。

---

## Value Triage

重点判断：

```yaml
value_triage:
  novelty:
  workflow_value:
  repeatability:
  transferability:
  evidence_quality:
  hermes_relevance:
```

重点寻找：

* 新 AI Workflow
* Human + AI 分工方式
* Agent 流程
* AI 影视工作流
* Prompt 工作流
* Coding 工作流
* Research 工作流
* 旧流程被新流程替代的信号

---

## Routing

### Creator 方法论研究

```text
Knowledge Scout
↓
hermes-creator-to-skill-research
```

### 具体项目研究

```text
Knowledge Scout
↓
对应项目 Skill
```

### 行业或趋势研究

```text
Knowledge Scout
↓
Research Workflow
```

### 低价值内容

如果内容：

* 重复
* 缺乏原始资料
* 只有短期新闻价值
* 没有稳定 Workflow
* 与 Hermes 无明显关系

则：

```text
archive / ignore
```

不要强行蒸馏。

---

## Output

一次完整 Scout 至少说明：

```markdown
## Source
原始来源与素材状态。

## Discovery
发现了什么。

## Why It Matters
为什么值得继续研究。

## Evidence Status
是否获得完整原始资料。

## Recommended Route
- Creator Distillation
- Project Skill
- General Research
- Archive
- Ignore
```

---

## Quality Rules

1. 原始资料优先于摘要。
2. 来源事实与分析判断分开。
3. 单条内容不能自动升级成方法论。
4. 没有读取原始资料时不得假装已经研究。
5. Creator 名单由 watchlist 管理。
6. 新知识先研究，再影响正式 Skill。
7. 优先发现 Workflow，而不是追逐工具名称。
8. 优先长期可迁移能力，而不是短期热点。

---

## Final Principle

```text
Discover
↓
Acquire
↓
Verify
↓
Triage
↓
Research
↓
Distill
↓
Validate
↓
Evolve
```

Knowledge Scout 只负责前四步：

```text
Discover
↓
Acquire
↓
Verify
↓
Triage
```

后续深度研究和 Skill Evolution 交给对应 Hermes Skill。
