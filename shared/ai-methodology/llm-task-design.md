# LLM Task Design Principles

## Purpose

这是 Hermes 的底层 AI 使用方法论。

不是人物视角，不模拟某个人表达。

用于提升所有 AI 工作流的任务设计质量。

## Core Principle

不要直接要求模型完成结果。

先设计任务系统：

```
目标
↓
上下文
↓
模型能力判断
↓
执行
↓
验证
↓
迭代
```

## Before Using AI

执行 AI 任务前检查：

1. 目标是否明确？
2. 模型是否适合解决这个问题？
3. 是否提供了足够上下文？
4. 输出标准是什么？
5. 如何验证结果？

## Capability Boundary

区分：

### 模型内部能力

适合：

- 语言处理
- 模式识别
- 创意生成
- 信息整理

### 外部工具能力

需要：

- 最新事实
- 数据查询
- 文件修改
- 精确计算

### 人类判断

负责：

- 目标选择
- 价值判断
- 最终决策

## Context Engineering

高质量输出来自高质量上下文。

上下文包括：

- 背景资料
- 约束条件
- 示例
- 判断标准
- 已知失败案例

## Verification Loop

AI输出不能直接等同事实。

流程：

```
生成
↓
检查依据
↓
发现问题
↓
修正
```

## Application

适用于：

- Skill执行前
- Creator Distillation
- AI创作流程
- Research分析
- Coding任务

## Boundary

不要把这个方法论变成新的复杂流程。

目标只是减少：

- 错误任务定义
- 无效提示词
- 不可靠输出
- 重复返工
