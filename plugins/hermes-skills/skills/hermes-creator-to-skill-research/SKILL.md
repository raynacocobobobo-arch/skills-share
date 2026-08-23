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

Creator Distillation 是 source-grounded extraction。

唯一事实来源：

1. 原始字幕文件
2. index.json 提供的定位信息

禁止：

- 根据标题推测内容
- 根据 Creator 印象总结
- 根据 research-input.md 直接蒸馏
- 根据摘要、搜索结果、历史记忆替代原文

---

# Mandatory Source Pipeline

执行 Creator Distillation 时必须严格执行：

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

不得使用替代信息继续。

---

# Source Discovery Rules

字幕库存在索引时，唯一入口：

```
index.json
↓
entries[]
↓
up_name
↓
repository_path
↓
原始字幕 txt
```

禁止：

- 使用 GitHub Search 作为字幕定位方式
- 扫目录猜测 Creator
- 根据文件名判断内容

---

# Creator Distillation Tracking

Creator Distillation 状态唯一存储位置：

```
hermes-daily-report/data/creators.json
```

禁止：

- 在 skills-share 创建额外 Creator 状态文件
- 创建重复 registry
- 使用其他文件替代 creators.json

Creator Distillation 状态以 Creator 为单位维护，不以单个字幕文件为主要单位。

执行前：

读取：

```
hermes-daily-report/data/creators.json
```

判断：

```
completed → 跳过
pending → 执行
processing → 继续检查状态
```

状态：

```
pending
↓
processing
↓
completed
↓
rejected
```

完成后必须记录：

- creator_name
- source_files
- distillation_status
- completed_date
- target_path
- distillation_output

---

# Batch Distillation

同一 Creator 必须批量分析。

流程：

```
同一 Creator 多条字幕
↓
完整阅读原文
↓
寻找重复出现的方法
↓
去除新闻和一次性工具信息
↓
提取稳定工作流
↓
验证迁移价值
↓
更新 Creator 状态
```

---

# Completion Requirement

Creator Distillation 只有满足以下条件才算完成：

```
原始字幕已读取
↓
方法论已提取
↓
沉淀文件生成
↓
hermes-daily-report/data/creators.json 更新
```

不能减少实际项目时间、错误或决策成本的内容，不进入 Hermes。
