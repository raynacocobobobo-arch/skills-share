# Swift 直连 DeepSeek API —— 代码模式

> HermesTodo v19+ 不再依赖 ai_bridge.py。所有 AI 逻辑嵌入 Swift。

## 常量声明

```swift
private let deepseekKey = "sk-xxx"
private let deepseekURL = "https://api.deepseek.com/chat/completions"
@State private var chatHistory: [(role: String, content: String)] = []
```

## System Prompt（嵌入 Swift 多行字符串）

```swift
private let systemPrompt = """
你是一个实用的待办清单助手。

工作流程：
1. 用户需求足够具体 → 直接列出待办清单（suggestions），reply 简短解释。
2. 用户需求太宽泛 → reply 一句话反问引导，options 列出2-3个具体方向。

输出规则：
- 返回纯JSON：{"reply":"...","suggestions":[...],"options":[]}
- 反问时：{"reply":"简短引导","suggestions":[],"options":["选项1","选项2","选项3"]}
- reply 不要包含编号列表！编号列表会通过UI按钮显示。
"""
```

## sendAIMessage —— 核心请求函数

```swift
private func sendAIMessage() {
    let msg = aiText.trimmingCharacters(in: .whitespaces)
    guard !msg.isEmpty else { return }
    let userMsg = ChatMessage(role: .user, content: msg)
    aiMessages.append(userMsg); aiText = ""; aiLoading = true

    // 构建 messages: system + 最近3轮历史 + 当前
    var messages: [[String: String]] = [["role": "system", "content": systemPrompt]]
    for h in chatHistory.suffix(6) { messages.append(["role": h.role, "content": h.content]) }
    messages.append(["role": "user", "content": msg])

    let body: [String: Any] = ["model": "deepseek-chat", "messages": messages,
                                "temperature": 0.7, "max_tokens": 2000]
    guard let json = try? JSONSerialization.data(withJSONObject: body),
          let url = URL(string: deepseekURL) else { aiLoading = false; return }

    var req = URLRequest(url: url); req.httpMethod = "POST"
    req.setValue("application/json", forHTTPHeaderField: "Content-Type")
    req.setValue("Bearer \(deepseekKey)", forHTTPHeaderField: "Authorization")
    req.httpBody = json; req.timeoutInterval = 35

    let currentMsg = msg
    URLSession.shared.dataTask(with: req) { data, _, error in
        guard let data = data, error == nil,
              let resp = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let choices = resp["choices"] as? [[String: Any]],
              let choice = choices.first,
              let message = choice["message"] as? [String: Any],
              let content = message["content"] as? String else {
            DispatchQueue.main.async { aiLoading = false }
            return
        }
        DispatchQueue.main.async { parseAIResponse(content, userMsg: currentMsg) }
    }.resume()
}
```

## JSON 解析三级管线

```swift
// 第一级：markdown 围栏去壳 + json decode
private func parseAIResponse(_ raw: String, userMsg: String) {
    var content = raw.trimmingCharacters(in: .whitespaces)
    if content.hasPrefix("```") {
        if let nl = content.firstIndex(of: "\n") { content = String(content[content.index(after: nl)...]) }
        if content.hasSuffix("```") { content = String(content.dropLast(3)) }
        content = content.trimmingCharacters(in: .whitespaces)
    }
    if content.lowercased().hasPrefix("json") { content = String(content.dropFirst(4)).trimmingCharacters(in: .whitespaces) }
    guard !content.isEmpty else { aiLoading = false; return }

    if let data = content.data(using: .utf8),
       let result = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
        handleAIResult(result, userMsg: userMsg)
    } else {
        retryParseJSON(raw: content, userMsg: userMsg)  // 第二级
    }
}

// 第二级：重试——让 AI 把内容转 JSON
private func retryParseJSON(raw: String, userMsg: String) {
    let retryMsg = "请把以下内容转为标准JSON格式：\n\n\(raw)"
    let messages: [[String: String]] = [
        ["role": "system", "content": "你只输出JSON。"],
        ["role": "user", "content": retryMsg]
    ]
    // ... POST 同上模式，temperature=0.3 ...
    // 成功 → handleAIResult；失败 → 第三级降级
}

// 第三级：降级——原始文本当 reply
// handleAIResult(["reply": raw, "suggestions": [], "options": []], ...)
```

## 对话历史维护

```swift
private func handleAIResult(_ result: [String: Any], userMsg: String) {
    aiLoading = false; aiAddedTasks = [:]
    let reply = result["reply"] as? String ?? ""
    let opts = result["options"] as? [String] ?? []
    if !reply.isEmpty { aiMessages.append(ChatMessage(role: .assistant, content: reply, options: opts)) }
    if let sugs = result["suggestions"] as? [[String: Any]] {
        aiSuggestions = sugs.map { s in AISuggestion(...) }
    }
    chatHistory.append((role: "user", content: userMsg))
    chatHistory.append((role: "assistant", content: reply))
    if chatHistory.count > 6 { chatHistory = Array(chatHistory.suffix(6)) }
}

// 清空
private func clearAIChat() {
    aiMessages = []; aiSuggestions = []; aiAddedTasks = [:]; aiLoading = false
    chatHistory = []
}
```

## 关键注意事项

1. **不用 `response_format: {"type": "json_object"}`** — DeepSeek 多轮对话中返回空响应（第5轮开始）
2. **历史只存 reply 文本**，不存 options 编号格式（避免格式污染）
3. **MAX_HISTORY = 6**（3轮），经 20→10→6 调优确认最稳定
4. **所有 @State 修改必须 dispatch 到 main queue** — URLSession callback 在后台线程
5. **HTTPS 直连无需 ATS 例外** — `api.deepseek.com` 已是 HTTPS
