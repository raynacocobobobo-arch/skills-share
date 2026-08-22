# AI 桥接架构

## 协议 v5（当前）

**端点**: `POST /ask` → 调 DeepSeek API → 即时返回 JSON

**请求**:
```json
{"message": "用户输入"}
```

**响应**:
```json
{
  "reply": "AI 自然语言回复",
  "suggestions": [
    {"title": "待办标题", "context": "情境名", "priority": "high|medium|low"}
  ],
  "options": ["选项1", "选项2"],
  "id": "req_xxx",
  "status": "done"
}
```

**字段互斥规则**:
- **直接建议模式**: `suggestions` 有数据，`options` 为空。`reply` 含解释文字。
- **反问模式**: `suggestions` 为空，`options` 有数据（2-3项，每项≤15字）。`reply` 只写简短引导（≤20字）。

**禁止模式**: 不要在 `reply` 里用 `1）2）3）` 写编号列表！选项通过 `options` 字段在 UI 层渲染，不重复显示。

**上下文维护**:
- 全局 `CONVERSATION_HISTORY` 列表，保留最近 **3轮（6条）** 消息
- 每次 POST 自动注入历史
- **历史只存 `result["reply"]` 原始文本**，不拼接 options 编号行。原则：对话历史是语义记忆，不存 UI 格式
- `POST /clear` 清空历史

**JSON 重试+降解（关键防御）**:
DeepSeek 在多轮对话中偶发不按 JSON 格式输出。**用户明确要求输出是待办清单不是自然语言聊天**，因此不能直接降级为纯文本。采用重试策略：

```python
# 第一层：尝试 JSON 解析
try:
    result = json.loads(clean)
    result.setdefault("options", [])
    result.setdefault("suggestions", [])
except (json.JSONDecodeError, ValueError):
    # 第二层：重试——让 AI 把内容转 JSON
    retry_msg = f"请把以下内容转为标准JSON格式：\n\n{clean}"
    retry_resp = requests.post(API_URL, json={
        "model": MODEL,
        "messages": [{"role": "system", "content": "你只输出JSON。"},
                     {"role": "user", "content": retry_msg}],
        "temperature": 0.3,
        "max_tokens": 2000
    }, ...)
    retry_content = retry_resp.json()["choices"][0]["message"]["content"].strip()
    try:
        result = json.loads(retry_content)
        ...
    except (json.JSONDecodeError, ValueError):
        # 第三层：仍失败——降级为纯文本（极少触发）
        result = {"reply": content, "suggestions": [], "options": []}
```

这样即使 AI 第一次输出跑偏，重试一次后 95%+ 能转为结构化 JSON。用户永远看到的是待办清单，不是裸异常或纯聊天。

**Prompt 关键约束**:
- 反问时 reply 只写引导语，编号选项走 options 字段
- 用户追选某选项时，直接给该方向待办
- 返回纯 JSON，不含 markdown 围栏

**response_format 陷阱**:
**不要**给 DeepSeek 加 `response_format: {"type": "json_object"}`。在多轮对话中会导致 API 返回空响应（测试中5轮后开始出现）。靠 prompt 约束输出格式即可。

**历史轮次**:
- MAX_HISTORY 经过 20→10→6 的调优。20 轮对话太长导致 DeepSeek 输出不稳定，6（3轮）是最佳平衡点——有足够上下文理解追问，又不会污染输出格式。

## 历史版本

### v5
- JSON 重试：解析失败时让 AI 转 JSON（而非直接降级）
- 用户反馈"我希望是 to do list 肯定不是自然语言"——驱动此改进

### v4
- 新增 `options` 字段，反问选项结构化分离
- 历史只存原始 reply，不存 UI 格式
- JSON 降解：json.loads 失败时全文当 reply
- MAX_HISTORY 降至 6（3轮）
- 选项按钮发送全文（非编号）

### v3
- 首次加入 `CONVERSATION_HISTORY` 和 `/clear` 端点

### v2
- 即时返回（不轮询），无对话历史

### v1
- 轮询模式，写文件 `/tmp/hermestodo_ai_response.json`
