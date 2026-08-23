# Hermes Creator To Skill Research

## Purpose

将优秀创作者的真实经验转化为 Hermes 可复用能力。

目标不是生成内容摘要，而是发现：

- 新工作流
- 新方法论
- 新判断标准
- 可提升实际项目效率的能力

---

# Core Rule

不要：

- 生成普通视频摘要
- 罗列工具名称
- 因为一个案例新增 Skill
- 建立无法使用的复杂知识体系

重点回答：

1. 创作者解决了什么问题？
2. 使用了什么工作流程？
3. 哪些经验可以迁移？
4. Hermes 是否已经具备？
5. 最小如何补充？

---

# Source Discovery Rule

素材定位必须先使用真实索引，不依赖搜索结果。

## Discovery Priority

执行顺序：

```
用户指定入口

↓

research-input.md / index.json

↓

根据索引字段过滤 creator

↓

repository_path

↓

读取原始字幕/文章/项目文件
```

## Index First Rule

如果存在字幕索引：

例如：

```
subtitles/YYYY-MM-DD/index.json
```

必须优先读取。

索引字段：

- up_name
- repository_path
- title
- sha256
- size_bytes

流程：

```
index.json

↓

过滤 up_name

↓

获得全部 repository_path

↓

批量读取素材
```

禁止：

- 优先使用 GitHub 搜索找字幕
- 搜索不到就判断文件不存在
- 根据文件名猜测内容

## GitHub Search Limitation

GitHub 搜索可能存在索引延迟。

搜索只能作为辅助。

---

# Raw Material Rule

必须读取原始素材。

禁止：

- 根据标题生成结论
- 根据摘要生成结论
- 根据频道印象推测

---

# Creator Batch Distillation

同一个创作者优先批量分析。

流程：

```
同一创作者多条素材

↓

整体阅读

↓

寻找重复方法

↓

去除工具新闻和单案例

↓

提取稳定工作流

↓

判断 Hermes 缺口
```

规则：

- 单条视频只能作为证据。
- 多素材重复出现的方法优先。
- 不因为单个技巧新增 Skill。

---

# Output

必须包含：

## Creator Core Contribution

这个创作者真正贡献的能力。

## Repeated Workflow Patterns

多个素材反复出现的方法。

## Workflow Extraction

输入、步骤、输出、适用场景。

## Hermes Comparison

- 已覆盖
- 部分缺失
- 完全缺失

## Skill Impact

只提出最小必要修改。

---

# Boundary

负责：

- 蒸馏创作者经验
- 提出能力改进建议

不负责：

- 建立工具数据库
- 保存大量视频摘要
- 直接堆叠知识资料

原则：

不能减少实际项目时间、错误或决策成本的内容，不进入 Hermes。