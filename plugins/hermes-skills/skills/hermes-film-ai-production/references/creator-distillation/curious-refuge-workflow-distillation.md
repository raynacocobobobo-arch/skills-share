# Curious Refuge Workflow Distillation

## Purpose

将 Curious Refuge 的 AI 影视实践转化为 Hermes 可复用工作流。

不是工具评测，不记录模型新闻。

重点提炼：

- 制作流程
- 导演方法
- 可复用生产原则

---

# Core Contribution

Curious Refuge 的核心价值不是某个 AI 模型，而是展示了一套 AI 影视生产流程：

```
Story
↓
Shot Design
↓
Asset Preparation
↓
Reference Control
↓
Generation
↓
Review
↓
Iteration
↓
Final Edit
```

---

# Workflow 1: Asset Bible → Shot Reference Pack → Generation

AI 影视不是直接从文字进入生成。

流程：

```
Asset Bible

角色
场景
道具
风格

↓

Shot Reference Pack

↓

Generation
```

Shot Reference Pack 用于单个镜头：

- 当前角色
- 当前场景
- 当前道具
- 风格参考
- 摄影参考
- 生成目标

原则：

只保留当前镜头需要的参考，不无限堆叠素材。

---

# Workflow 2: Shot Based Production

不要尝试一个 Prompt 生成完整影片。

推荐：

```
影片需求
↓
镜头拆解
↓
单镜头设计
↓
生成
↓
剪辑组合
```

AI 生成更适合镜头级生产。

---

# Workflow 3: Generation Review Loop

生成不是结束。

导演流程：

```
Generate
↓
Review
↓
Identify Issue
↓
Adjust
↓
Regenerate
↓
Lock Shot
```

检查：

- 人物一致性
- 动作逻辑
- 空间关系
- 摄影机运动
- 时间连续性

问题定位：

资产问题 → 修改 Asset

镜头问题 → 修改 Shot Design

描述问题 → 修改 Prompt

---

# Workflow 4: Timeline Prompt

视频 Prompt 不只是描述画面。

需要描述变化：

```
Start State
↓
Action Development
↓
Camera Movement
↓
End State
```

包含：

- 开始状态
- 动作变化
- 镜头运动
- 最终状态

---

# Comparison With Hermes

已有：

- Project Start
- Visual Analysis
- Asset Bible
- Storyboard
- Prompt Pattern

新增强化：

## Shot Reference Pack

解决：

资产如何进入具体镜头。

## Generation Review Loop

解决：

生成后如何导演式修改。

## Timeline Prompt

解决：

视频 Prompt 如何描述时间变化。

---

# Excluded

不进入 Hermes Film Skill：

- 模型排行榜
- 工具数据库
- 模型新闻
- 成本追踪系统

原因：

工具变化快，不能形成长期能力。

---

# Final Principle

AI 影视生产不是：

```
Prompt → Video
```

而是：

```
Story
↓
Shot
↓
Asset
↓
Reference
↓
Generation
↓
Review
↓
Iteration
↓
Edit
```
