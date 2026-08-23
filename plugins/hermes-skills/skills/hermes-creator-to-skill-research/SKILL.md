# Hermes Creator To Skill Research

## Purpose

将优秀创作者的真实经验转化为 Hermes 可复用能力。

目标不是创建 Creator 分身，而是提取：

- 可执行工作流
- 方法论
- 判断标准
- 实际项目改进方式

---

# Core Principle

Creator Distillation 是 source-grounded extraction。

唯一事实来源：

1. 原始字幕文件
2. index.json 提供的定位信息

禁止：

- 根据标题推测内容
- 根据 Creator 印象总结
- 根据摘要替代原文
- 根据历史记忆替代原始素材

---

# Mandatory Source Pipeline

执行 Creator Distillation 必须：

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

如果原始字幕没有读取成功：

```
停止分析
禁止输出蒸馏结果
```

---

# Batch Distillation

同一 Creator 必须批量分析：

```
同一 Creator 多条字幕
↓
完整阅读原文
↓
寻找重复出现的方法
↓
去除新闻和一次性信息
↓
提取稳定工作流
↓
验证迁移价值
```

---

# Workflow Pattern Extraction Stage

在 Capability Extraction 前，必须先识别 Workflow Pattern。

禁止只提取功能名称或主题。

每个工作流必须拆解：

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

分析目标：

- 什么时候触发该流程
- 需要什么输入
- 中间有哪些阶段
- AI 和人的职责如何分配
- 最终产生什么资产
- 如何验证结果

---

# Capability Extraction Stage

Batch Distillation 后，必须进入 Capability Extraction。

禁止直接从 Creator 方法映射 Skill。

强制流程：

```
Creator Methods
↓
Workflow Pattern Extraction
↓
Capability Extraction
↓
Capability Map
↓
Skill Impact Mapping
↓
Implementation
```

每个 Capability 必须记录：

```yaml
capability:
  name:
  category:
  problem_solved:
  reusable_value:
  workflow_pattern:
    trigger:
    inputs:
    stages:
    ai_role:
    human_role:
    artifacts:
    verification:
  candidate_skills:
  decision:
    enhance_existing | create_new
```

---

# Creator Is Not Capability

Creator 是输入来源，不是知识架构。

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

# Skill Impact Mapping Rules

Capability Extraction 后进入 Skill Impact 阶段。

正确流程：

```
Capability Map
↓
查看已有 plugins/hermes-skills/skills/
↓
读取候选 Skill 的 SKILL.md
↓
判断能力边界
↓
增强已有 Skill
或
创建新 Skill
```

强制：

1. MUST inspect existing skills before creating new capability.
2. MUST read candidate SKILL.md before deciding destination.
3. MUST prioritize extending existing skills.
4. 不允许仅根据 Creator 类型、领域或名称猜测 Skill。

新建 Skill 必须证明：

- 现有 Skill 无法覆盖
- 能力可重复调用
- 具有长期复用价值

---

# Creator Distillation Tracking

唯一状态文件：

```
hermes-daily-report/data/creators.json
```

完成后记录：

- creator_name
- source_files
- distillation_status
- completed_date
- target_path
- distillation_output

---

# Completion Requirement

只有满足：

```
原始字幕已读取
↓
Workflow Pattern 已提取
↓
Capability Map 已生成
↓
沉淀文件生成
↓
creators.json 更新
```

才算 Creator Distillation 完成。
