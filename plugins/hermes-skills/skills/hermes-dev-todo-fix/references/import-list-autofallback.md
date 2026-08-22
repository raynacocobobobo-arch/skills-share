# 导入列表自动生成情境：兜底解析与安装验证

## 触发场景
用户在 AI 页点击“导入列表”并粘贴表格/清单/攻略后，预期是**立刻生成/复用一个情境并批量写入待办**，不是只在 AI 页显示预览，更不是等待用户再点一次。

## 容易踩坑

### 1. 只依赖 AI suggestions 会导致“导入了但没生成情境”
如果 AI 返回慢、返回非 JSON、或 JSON 中 `suggestions` 为空，旧逻辑不会调用 `importAISuggestionsToContext()`，用户在情境页看不到新情境。

**修复模式**：导入列表必须有本地兜底解析。
- `analyzeImportedList()` 中保存 `pendingImportListRaw` 和 `pendingImportContextHint`。
- 先 `clearAIChat()`，再设置 `pendingImport...` 和 `autoImportAfterAIResponse = true`。
- `sendAIRequest(... resetConversation: false)`，避免再次触发清空。
- `handleAIResult()` 中如果 `autoImportAfterAIResponse == true` 且 `aiSuggestions.isEmpty`，调用 `localParseImportedList(raw, contextHint:)` 兜底生成 `AISuggestion`。
- 只要兜底或 AI 任一路径得到 suggestions，就调用 `importAISuggestionsToContext()`。

### 2. 状态顺序要防止被 clearAIChat 冲掉
错误模式：`sendAIRequest(resetConversation: true)` 内部会调用 `clearAIChat()`，如果自动导入状态或 pending 原文在错误时机设置，可能被清掉。

推荐顺序：
```swift
showImportList = false
currentTab = .ai
clearAIChat()
pendingImportListRaw = raw
pendingImportContextHint = ctxHint
autoImportAfterAIResponse = true
sendAIRequest(userMessage: prompt, displayMessage: "导入列表：...", resetConversation: false)
```

### 3. 本地兜底解析规则
本地兜底不追求 AI 语义完美，但必须保证“有情境、有待办”。
- 按换行拆行。
- 每行再按 `tab / | / ｜ / ， / , / ； / ;` 拆单元格。
- 跳过表头词：名称、事项、待办、清单、类别、分类、备注、优先级、序号、title、note、priority。
- 每项走 `cleanAITitle()`，标题最长 12 字。
- 用 `normalizeAITitleKey()` 去重。
- 情境名：用户填了就固定；没填则 `guessContextName(from:)`，常见旅行/拍摄/婚礼/财务关键词兜底，否则叫“导入清单”。

### 4. 验证闭环
用户看 App 没变时，不要只说“编译过了”。必须确认是否已经覆盖安装到真机。

验证顺序：
1. `xcodebuild ... build` 看到 `BUILD SUCCEEDED`。
2. `xcrun devicectl device install app --device <coredevice-id> <DerivedData/.../HermesTodo.app>` 看到 `App installed:`。
3. 只做覆盖安装，禁止 `uninstall`，避免清空 SwiftData 数据。
4. 让用户重新打开 App，再试导入。

## 用户体验标准
导入列表是“生成情境”的强动作：点“生成情境”后，无论 AI JSON 是否稳定，都应尽量生成一个可见情境。AI 负责优化结构，本地兜底负责不掉链子。