# Creator Distillation Capability Extraction Framework

## Purpose

Creator Distillation 的目标不是把 Creator 内容直接映射到 Skill，而是提取可复用 Capability。

## Architecture

```
Creator Source
↓
Methods
↓
Capability
↓
Skill Impact Mapping
↓
Implementation
```

## Capability Extraction

分析 Creator 字幕后，必须先回答：

- 这个方法解决什么问题？
- 是否跨项目复用？
- 是否减少时间、错误或决策成本？
- 是否应该增强已有 Skill？
- 是否需要新 Skill？

## Skill Decision

```
Capability
↓
Inspect existing skills
↓
Read candidate SKILL.md
↓
Enhance existing skill OR create new skill
```

## Do Not

禁止：

- Creator = Skill
- Creator 领域 = Skill 领域
- 根据名称直接创建能力

## Output

每次蒸馏需要产出 Capability Map：

- capability_name
- workflow_pattern
- reusable_value
- target_skill
- implementation_status
