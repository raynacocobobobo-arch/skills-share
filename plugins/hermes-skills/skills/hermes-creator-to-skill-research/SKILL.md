# Hermes Creator To Skill Research

## Purpose

将优秀创作者的真实经验转化为 Hermes 可复用能力。

目标不是创建人物分身，而是提取：

- 可执行工作流
- 方法论
- 判断标准
- 实际项目改进方式

---

# Core Principle

研究对象：创作者如何解决问题。

不是：

- 视频摘要
- 工具列表
- 人物模仿
- 单案例技巧收集

必须回答：

1. 创作者解决什么实际问题？
2. 使用什么稳定流程？
3. 哪些方法可以迁移？
4. Hermes 哪个能力需要补充？

---

# Source Discovery

字幕库存在索引时，唯一入口：

```
index.json
↓
解析完整 JSON
↓
entries[]
↓
过滤 up_name
↓
repository_path
↓
读取原始素材
```

禁止：

- 使用 GitHub 搜索作为主要定位
- 根据标题推测内容
- 根据截断文本判断不存在

---

# Creator Distillation Tracking

Creator Distillation 必须记录状态。

状态以 Creator 为单位维护，不以单个字幕文件为主要单位。

流程：

```
pending
↓
processing
↓
completed
↓
rejected
```

Creator Distillation 完成后必须记录：

- creator_name
- source_files
- distillation_status
- completed_date
- target_path
- distillation_output

示例：

```json
{
  "creator_distillation": {
    "creator": "Matthew Berman",
    "status": "completed",
    "target": "shared/ai-workflow",
    "output": "shared/ai-workflow/sources/matthew-berman.md"
  }
}
```

目的：

- 避免重复蒸馏同一 Creator
- 区分已完成 Creator 和待研究 Creator
- 保持字幕资产与方法论资产关联

---

# Batch Distillation

同一创作者必须批量分析。

流程：

```
同一 Creator 多条素材
↓
整体阅读
↓
寻找重复出现的方法
↓
去除单次新闻和工具信息
↓
提取稳定工作流
↓
验证是否值得沉淀
↓
更新 Creator Distillation 状态
```

重点提取：

## Workflow

输入 → 步骤 → 输出 → 适用场景

## Method

为什么这样做。

## Decision Rules

什么时候使用，什么时候不用。

---

# Workflow Validation

任何发现必须经过判断。

判断：

1. 是否只是观点？
2. 是否只是工具介绍？
3. 是否只是一次案例？
4. 是否可以形成重复执行流程？
5. 是否有明确输入和输出？
6. 是否能减少时间、错误或决策成本？

只有具备可迁移价值的内容进入 Hermes。

---

# Distillation Decision

每次 Creator Distillation 完成后，只判断四种结果：

## 1. 补充已有 Skill

已有能力缺少部分方法。

## 2. 新增 Workflow 能力

出现稳定、可重复使用的执行流程。

## 3. 进入 Shared Methodology

适用于多个 Skill 的通用原则。

## 4. 不沉淀

只是新闻、工具介绍或一次性技巧。

---

# Output

输出：

## Creator Core Contribution

核心贡献。

## Workflow Extraction

可执行流程。

## Hermes Impact

应该修改什么。

## Not Included

为什么不进入系统。

完成后同步更新 Creator Distillation 状态。

---

# Boundary

不负责：

- 创建人物人格 Skill
- 保存视频摘要
- 建立工具数据库
- 堆叠知识资料

原则：

不能减少实际项目时间、错误或决策成本的内容，不进入 Hermes。