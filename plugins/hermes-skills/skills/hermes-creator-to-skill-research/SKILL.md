# Hermes Creator To Skill Research

## Purpose

将优秀创作者的真实经验转化为 Hermes 可复用能力。

目标不是生成内容摘要，而是发现：

- 新工作流
- 新方法论
- 新判断标准
- 可提升实际项目效率的能力

---

# Core Principle

研究对象是创作者的方法，不是视频内容。

不要：

- 生成视频摘要
- 罗列工具新闻
- 根据单个案例新增 Skill
- 建立无法使用的资料库

必须回答：

1. 创作者解决什么问题？
2. 使用什么稳定流程？
3. 哪些方法可以迁移？
4. Hermes 是否已有？
5. 最小如何补充？

---

# Source Discovery

## 唯一优先入口

字幕库存在索引时，必须使用索引定位素材。

流程：

```
index.json
↓
解析 JSON
↓
遍历 entries[]
↓
过滤 up_name
↓
获取 repository_path
↓
读取原始素材
```

索引字段：

- up_name
- repository_path
- title
- sha256
- size_bytes

## Important

不要根据工具返回的截断文本判断结果。

必须把 index.json 当 JSON 解析。

不要：

- 使用 GitHub 搜索作为主要定位方式
- 搜索不到就认为不存在
- 根据文件名猜内容

GitHub 搜索只能辅助验证。

---

# Raw Material Rule

必须读取原始字幕、文章或项目文件。

禁止：

- 根据标题生成结论
- 根据摘要生成结论
- 根据频道印象推测

---

# Creator Batch Distillation

同一个创作者优先批量分析。

流程：

```
多条素材
↓
整体阅读
↓
寻找重复方法
↓
去除单案例和工具信息
↓
提取稳定工作流
↓
判断 Hermes 缺口
```

规则：

- 单条视频只能作为证据。
- 重复出现的方法优先。
- 不因为一次技巧新增能力。

---

# Output

必须包含：

## Creator Core Contribution

创作者真正贡献的能力。

## Repeated Workflow Patterns

多个素材重复出现的方法。

## Workflow Extraction

输入、步骤、输出、适用场景。

## Hermes Comparison

分类：

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

- 保存视频摘要
- 建立工具数据库
- 堆叠无实际价值资料

原则：

不能减少实际项目时间、错误或决策成本的内容，不进入 Hermes。