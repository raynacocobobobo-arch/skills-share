# 企微 Hermes 文件路由表

> 来源：企微 Hermes 回复，2026-06-07 18:10
> 发送文件到企微实例时，按此结构归类，不发送 Mac 路径

```
~/hermes-knowledge/          ← 知识原文
  ├ 参考书原文/专业书/
  │  ├ 市场营销.md
  │  └ 好战略坏战略.md
  ├ 营销引用/
  └ 历史项目/

~/.hermes/crm/wedding/       ← 婚礼CRM（8765/8766）

~/.hermes/skills/<cat>/      ← 技能目录

~/hermes-output/             ← 产出文档
  ├ 营销方案/
  ├ CRM报表/
  └ 工作日志/
```

## 注意事项
- 不要发 Mac 路径（`/Users/rayna/`、`~/Desktop/`）到企微
- 技能中的路径做环境判断，不写死
- tar.gz 分片发送标清楚 PART 和文件名
- 技能：`workspace-conventions`，路径：`~/.hermes/skills/devops/workspace-conventions/`
