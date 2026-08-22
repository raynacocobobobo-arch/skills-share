# HermesTodo AI 页：结构化建议与一键汇总

## 适用场景
修改 `${HERMES_TODO_ROOT}` 的 AI 页待办生成流程时参考。目标是让 AI 像任务规划器，而不是长篇说明书。

## 当前推荐交互
- 用户可多轮和 AI 聊需求。
- App 累计每轮 `suggestions`，不在新一轮覆盖旧建议。
- 点击“汇总成待办”后，一次性导入同一个情境/Folder。
- 不再让用户手动框选、逐条点选添加。
- AI 页支持“导入列表”：用户粘贴表格/清单/攻略/别人发来的文字，AI 解析为结构化 `suggestions`，自动生成/复用一个情境并批量导入；AI 页保留结构化预览。

## AI JSON 协议
建议使用结构化字段：

```json
{
  "reply": "给你列好了",
  "suggestions": [
    {
      "title": "身份证",
      "category": "核心证件与财务",
      "note": "检查有效期须在6个月以上。",
      "context": "欧洲旅行清单",
      "priority": "high"
    }
  ],
  "options": []
}
```

字段约定：
- `title`：短标题，≤12 个汉字；不要写解释、方法、位置、提醒语。
- `category`：短分类名，用于 AI 页分组展示。
- `note`：详细提醒/使用场景/注意事项，写入 `TaskItem.notes`。
- `context`：同一轮和后续追问保持一个情境，不拆子情境。
- `priority`：`high` / `medium` / `low`。

## UI 展示规则
- AI 页按 `category` 分组展示。
- 每条显示短标题；有 `note` 时在标题下用小字号显示，最多两行。
- 顶部保留“汇总成待办”按钮；导入后显示“已汇总到情境”。

## 导入规则
- 导入时所有建议进入同一个 `Folder`。
- 新建 `TaskItem` 时，`title` 使用短标题。
- `notes` 保存分类与备注，例如：

```swift
let noteLines = [s.category.isEmpty ? "" : "【\(s.category)】", s.note].filter { !$0.isEmpty }
let task = TaskItem(title: s.title, notes: noteLines.joined(separator: "\n"), priority: priMap[s.priority] ?? .medium, folder: folder)
```

## 去重规则
- App 端继续按清洗后的标题 key 去重，避免重复创建。
- Prompt 端要求 AI 先做语义去重：例如“酒店订单 / 机酒行程单 / 行程单”合并为一项，并把细节写入 `note`。

## 验证命令
```bash
env -u TMPDIR xcodebuild -project ${HERMES_TODO_ROOT}/HermesTodo.xcodeproj -scheme HermesTodo -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build
```

`onChange(of:perform:)` 的 iOS 17 deprecated warning 可暂时忽略，不影响本次功能验证。
