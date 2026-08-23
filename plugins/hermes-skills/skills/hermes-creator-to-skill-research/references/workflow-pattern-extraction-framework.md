# Workflow Pattern Extraction Framework

用于 Creator Distillation 中识别可复用 Workflow，而不是简单总结 Creator 内容。

## 核心原则

Creator 蒸馏目标不是提取观点，而是提取可执行系统。

分析单位：

```
Creator Content
↓
Workflow Pattern
↓
Capability
↓
Skill
```

## Workflow 分析模板

每个候选能力必须分析：

```yaml
workflow:
  name:
  trigger:
  problem:
  input:
  stages:
    - step:
      purpose:
      ai_role:
      human_role:
  outputs:
  artifacts:
  verification:
  reusable_value:
```

## 必须识别的元素

### Trigger

什么时候使用这个 Workflow。

例如：

- 面对业务决策问题
- 准备客户会议
- 从零创建内容
- 从想法构建产品

### Input

AI 工作前需要什么上下文：

- 文档
- 数据
- 用户需求
- 历史资料
- 目标约束

### Stages

必须拆解实际步骤：

```
Input
↓
Analysis
↓
Transformation
↓
Review
↓
Artifact
```

不能只描述“AI帮助完成任务”。

### AI Role / Human Role

明确：

- AI负责什么
- 人负责什么
- 哪些节点需要判断

### Artifact

必须识别最终生成物：

例如：

- Strategy Deck
- Meeting Brief
- Content Draft
- Prototype
- Research Report

## Skill 判断标准

Workflow 不是 Skill 的情况下：

- 只是某个案例
- 只是工具介绍
- 只是一次性技巧

Workflow 可以成为 Skill：

- 有稳定步骤
- 有明确输入输出
- 可以跨项目复用
- 可以形成长期方法论资产

## 禁止

不要根据：

- 视频标题
- Creator 身份
- 工具名称

直接创建 Skill。

必须经过：

```
字幕原文
↓
Workflow Pattern
↓
Capability Map
↓
Skill Impact
```
