# AI 直连 DeepSeek（v6，替代桥接）

## 架构变更（2026-06-10）

废弃了 `ai_bridge.py`（Python HTTP 桥接），App 直接调 DeepSeek API。

**优点**: 不需要 Mac 开机、不需要同网络、不需要配置 IP。手机有网就能用。

## Swift 侧实现要点

### 常量
```swift
private let deepseekKey = "sk-..."
private let deepseekURL = "https://api.deepseek.com/chat/completions"
```

### 对话历史
```swift
@State private var chatHistory: [(role: String, content: String)] = []
// 最多保留 6 条（3 轮）
```

### System Prompt
内嵌为 Swift 多行字符串 `systemPrompt`，内容与旧 `ai_bridge.py` 的 `SYSTEM_PROMPT` 一致。

### 请求流程
1. `sendAIMessage()` — 构建 `messages` 数组（system + history.suffix(6) + user），POST 到 DeepSeek
2. `parseAIResponse()` — 去 markdown 围栏，尝试 `JSONSerialization.jsonObject`
3. JSON 解析失败 → `retryParseJSON()` — 另起请求让 AI 把内容转 JSON（temperature=0.3）
4. 彻底失败 → 原始文本当纯回复

### clearAIChat
只清本地数组，无网络请求。

## pbxproj 修复

Assets.xcassets 从 PBXGroup 空壳改为 PBXFileReference `folder.assetcatalog`，从 "Recovered References" 移到 HermesTodo group。

## Contents.json 格式

必须用 universal 单条格式（见 swiftui-swiftdata-pitfalls #30）。
