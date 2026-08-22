# AI 直连 DeepSeek 架构 (v19)

v19 起拆除 ai_bridge.py，App 直接调 DeepSeek API。

## 架构对比

| | v17 (桥接) | v19 (直连) |
|---|---|---|
| 调用链路 | App → localhost:8765 → ai_bridge.py → DeepSeek | App → DeepSeek |
| 依赖 | Mac 跑 Python 进程 | 无外部依赖 |
| 真机 | 需同网络 + ATS 例外 | 任何网络（HTTPS） |
| API key | 存在 /tmp 文件 | 嵌入 Swift 代码 |
| 对话历史 | 桥接内存 | App 本地 @State |
| 清对话 | POST /clear | 本地数组置空 |

## 数据流

```
用户输入 aiText
  → sendAIMessage()
    → 构建 messages:[system, ...chatHistory(最近6条), user]
    → POST api.deepseek.com/chat/completions
    → 回调 parseAIResponse(content, userMsg)
      → 去 markdown 围栏
      → JSONSerialization.jsonObject
      → 成功: handleAIResult
      → 失败: retryParseJSON (让AI转JSON)
        → 成功: handleAIResult
        → 失败: 原始文本当 reply 降级
```

## 关键参数

- model: "deepseek-chat"
- temperature: 0.7 (正常), 0.3 (retry)
- max_tokens: 2000
- MAX_HISTORY: 6 (最近3轮)

## 重试策略

1. 主请求 temperature=0.7
2. JSON 解析失败 → retryParseJSON: system="你只输出JSON。", temperature=0.3
3. 仍失败 → 原始文本当 reply，无 suggestions/options

## 不用的 API 参数

- 不用 `response_format` — DeepSeek 多轮下返回空响应
- 不用 `stream: true` — 不需要流式输出
