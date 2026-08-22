# ChatGPT GitHub 写入能力判断方法论

## 背景

在 Hermes Skills 使用过程中，需要区分：

- GitHub 仓库权限
- ChatGPT GitHub 连接能力
- 当前会话是否具备写入工具
- Codex 本地开发能力

不能根据过去经验直接判断“ChatGPT 不能写 GitHub”。

## 判断原则

### 1. 不看理论能力，直接验证

判断当前环境是否支持 GitHub 写入，唯一可靠方式：

1. 读取目标仓库。
2. 创建一个无害测试文件。
3. 查看 GitHub 是否返回 commit SHA。
4. 删除测试文件。

如果创建和删除均成功，说明当前会话具备 GitHub 写入能力。

## 2. 权限层级区分

```text
GitHub账号权限
        ≠
GitHub App / Connector权限
        ≠
当前ChatGPT会话工具权限
```

仓库显示 admin/push 权限，只说明 GitHub 身份授权，不代表所有 ChatGPT 环境都具备写入接口。

## 3. Hermes执行规则

当用户要求：

“按 Hermes skill 路由执行”

流程：

```text
用户任务
 ↓
读取 manifests/web-chatgpt-router.md
 ↓
匹配 skill
 ↓
读取 canonical SKILL.md
 ↓
执行 workflow
 ↓
根据当前环境能力决定：

读取分析
或
直接修改并commit
```

## 4. 避免思维惯性

旧经验：

> ChatGPT Web 不能写 GitHub

不应作为固定规则。

正确判断：

> 当前会话是否拥有 GitHub 写入工具，需要实际测试。

## 5. 多端职责

推荐：

```text
ChatGPT Web
- 路由
- 分析
- 审核
- 修改建议
- 直接commit（如果具备写入能力）

Codex
- 本地代码修改
- 大规模工程操作
- 测试验证
- 分支管理
```

两者不是替代关系，而是根据任务复杂度选择。
