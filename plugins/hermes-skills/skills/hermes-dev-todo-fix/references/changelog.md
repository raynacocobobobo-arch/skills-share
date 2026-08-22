# 变更记录

## 2026-06-10 v20: 图标/语音/删除 第二轮精修

### 图标白板 · 真根因定位
- 🐛 v18 resize 后仍白 → 根因不在尺寸，在 pbxproj：`Assets.xcassets` 是 PBXGroup 空壳 + "Recovered References" → `actool` 跳过编译，无 Assets.car
- 🐛 第二个根因：根目录 Assets.xcassets 的 icon-1024.png 是 JPEG 格式，iOS 拒绝
- ✅ pbxproj 改为 `PBXFileReference` + `lastKnownFileType = folder.assetcatalog`，移入 HermesTodo group
- ✅ `sips -s format png` JPEG→PNG，sips -z 1024 1024 resize
- ✅ 生成珊瑚色勾号图标（`#FF6B55` 圆角方形 + 白色 ✓）

### 语音闪退 · 真根因定位
- 🐛 v18 `.playAndRecord` + `.allowBluetooth` 中 `.allowBluetooth` 已在 iOS 8 弃用，真机 crash
- 🐛 `SFSpeechRecognizer(locale: "zh-CN")` 可能 nil → 缺 `isAvailable` 检查
- ✅ 改 `setCategory(.record, mode: .default)` 纯录音；加 `guard sr?.isAvailable` 前置检查
- ✅ audio session 错误时 return 不继续，stop() 时 release session

### 删除/改名 · 真根因定位
- 🐛 v18 `onTapGesture` 替代 Button 后仍不生效 → 真根因：`swipeActions` 只在 `List` 内响应，`ScrollView` 不触发
- ✅ `ScrollView{VStack{ForEach{...}}}` → `List{ForEach{...}}.listStyle(.plain).scrollContentBackground(.hidden)`

### AI · 拆除桥接
- ✅ 用户反馈"不可能一直带电脑"→ 直连 DeepSeek API
- ✅ 移除 `@AppStorage("aiServerURL")` + 旧 `sendAIMessage`/`clearAIChat`/`handleAIResponse`
- ✅ 新增 `deepseekKey/deepseekURL` 常量、`chatHistory` 本地状态、`systemPrompt` 嵌入
- ✅ `parseAIResponse` → `retryParseJSON` → `handleAIResult` 三步管线
- ✅ 旧 `ai_bridge.py` 已停止

## 2026-06-10 v19: 架构升级——AI 直连 DeepSeek，拆除桥接

- ✅ 用户反馈"不可能一直带电脑"→ 方案B：App 直接 POST DeepSeek API
- ✅ 移除 `@AppStorage("aiServerURL")`，改 `let deepseekKey` + `let deepseekURL` 常量
- ✅ 删除 `ai_bridge.py` 依赖：`sendAIMessage()` 直接构建消息数组调 `api.deepseek.com/chat/completions`
- ✅ `chatHistory: [(role,content)]` 本地 `@State` 维护对话历史（最近6条/3轮）
- ✅ `clearAIChat()` 纯本地操作，无网络调用
- ✅ `systemPrompt` 多行字符串嵌入 Swift 代码（与旧桥接 prompt 一致）
- ✅ JSON 解析管线完整迁移：markdown围栏去壳 → JSONSerialization.jsonObject → 失败则 `retryParseJSON` 让 AI 转 JSON → 仍失败降级纯文本
- ✅ `parseAIResponse` / `retryParseJSON` / `handleAIResult` 三步分离
- ✅ 旧 `ai_bridge.py` 已停止，文件保留待清理
- ✅ 不需要 ATS 例外（直连 HTTPS 的 `api.deepseek.com`）

## 2026-06-10 v18: 5个真机 bug 修复

### Bug 1: 桌面图标白板（两重根因）
- 🐛 根因一：pbxproj 中 Assets.xcassets 是 PBXGroup 空壳（Recovered References）→ actool 跳过不编译，无 Assets.car
- 🐛 根因二：根目录 Assets.xcassets 里 icon-1024.png 是 JPEG 格式，iOS 要求 PNG
- ✅ pbxproj：CBBC68BBB 从 PBXGroup 改 PBXFileReference（lastKnownFileType=folder.assetcatalog），从 Recovered References 移到 HermesTodo group
- ✅ `sips -s format png` 将 JPEG 转 PNG；`sips -z 1024 1024` resize
- ✅ 验证：build 日志必须出现 `CompileAssetCatalogVariant thinned .../Assets.car`

### Bug 2: 语音按钮闪退
- 🐛 真机 AVAudioEngine 未配置 AVAudioSession
- ✅ 录音前 `setCategory(.playAndRecord)`+`setActive(true)`，停止后释放
- ✅ recognitionTask 回调增加 error 参数处理

### Bug 3: AI 真机无响应
- 🐛 `localhost:8765` 指向 iPhone 自己，Mac 桥接不可达
- ✅ 改用 `@AppStorage("aiServerURL")` + Mac 局域网 IP（172.20.10.2 热点模式）
- ✅ Info.plist 加 `NSAllowsLocalNetworking` ATS 例外

### Bug 4: 情境无法删除
- 🐛 `swipeActions` 附着在 `Button` 上，tap 拦截 swipe
- ✅ 改用 `onTapGesture`+`contentShape(Rectangle())`

### Bug 5: 情境无法改名
- ✅ 左滑"改名"按钮（`.swipeActions(edge:.leading)`），`.alert`+`TextField` 弹窗

---

## 2026-06-10 v17: AI 桥接 v5 · 真机安装成功

### 桥接 v5 落地（JSON 重试 + 用户驱动设计）
- ✅ 用户明确反馈"我希望是 to do list 肯定不是自然语言"——废弃纯降级，改为**重试→结构化→才降级**三级策略
- ✅ ai_bridge.py 版本号 v4→v5
- ✅ 代码见 `ai_bridge.py`，协议见 `references/ai-bridge.md`

### 真机安装
- ✅ 首次用 `xcrun devicectl device install app` 成功安装到 iPhone 16 Pro
- ✅ 设备：张三，UDID `00008140-001E34122111801C`
- 文档：`references/real-device-deploy.md`

### 参数终态
- MAX_HISTORY = 6（3轮），经 20→10→6 调优确认最优
- DeepSeek 参数：temperature=0.7, max_tokens=2000，**不加 response_format**
- 历史不存 UI 格式，只存 `result["reply"]` 原始文本
- 选项按钮发全文（非编号），AI 语义理解

---

## 2026-06-10 v16: 真机部署流程打通

### 真机（张三·iPhone 16 Pro）部署
- ✅ 设备通过 Xcode Devices 窗口同步安装 DDI
- ✅ iOS 开发者模式开启（设置→隐私与安全性→最底部）
- ✅ Xcode 自动签名 + provisioning（需用户在 Signing & Capabilities 选 Team）
- 文档：`references/real-device-deploy.md`

---

## 2026-06-10 v15: JSON 重试机制 + 日常页删情境

### JSON 重试——用户诉求驱动
- 🐛 用户反馈"我希望是 to do list 肯定不是自然语言"——v14 的纯降级策略在 AI 输出跑偏时变成聊天，不符合待办清单定位
- ✅ json.loads 失败→**重试一次**：另起请求让 AI 把内容转 JSON（system="你只输出JSON。"，temperature=0.3）→再 json.loads → 仍失败才降级
- 测试：10轮连续对话全部通过，零报错
- 代码见 `references/ai-bridge.md` v5 协议

### 日常页删情境
- ✅ 文件夹左滑出现红色删除按钮（swipeActions）
- ✅ 点击弹出确认框"删除情境「xxx」？任务不会被删除，但会移出该情境"
- ✅ 点取消关闭，点确认删除 Folder（TaskItem.folder 自动 nullify）

### 选项按钮发全文
- 从 `aiText = String(idx+1)` 改回 `aiText = o`（选项全文）
- 原因：历史不存编号列表，AI 无法从 "2" 反推选项内容
- AI 通过语义理解这是选择了某个方向

---

## 2026-06-10 v14: DeepSeek 稳定性加固

### response_format 陷阱
- 🐛 试加 `response_format: {"type": "json_object"}` 强制 JSON 输出 → 第5轮开始 API 返回空响应
- ✅ 回滚：**不用 `response_format`**，只靠 prompt 约束格式。DeepSeek 对 json_object 模式兼容性差

### JSON 降解（最终防线，v15 被重试取代）
- 🐛 DeepSeek 在多轮对话中偶发不按 JSON 格式输出。裸调 `json.loads` → 用户看到 `Expecting value`
- ✅ 嵌套 try/except 降级

### 历史轮次调优
- MAX_HISTORY: 20 → 10 → 6（3轮）
- 20轮时 DeepSeek 输出不稳定，6轮是最佳平衡点
- 原则：**对话历史是语义记忆，不存 UI 格式**

### 选项按钮回改
- 点按钮发编号 "2"→改回发选项全文，AI 语义理解

---

## 2026-06-10 v13: 历史污染修复

- 🐛 历史里拼接了编号文本 → DeepSeek 误判输出格式 → 返回空
- ✅ 历史只存原始 reply

---

## 2026-06-10 v12: 重构 AI 反问架构（"脱了裤子放屁"）

- 🐛 AI 反问 reply 写编号 + UI 正则解析 = 同样内容两遍
- ✅ 废弃 regex，新增 `options` JSON 字段，ChatMessage 自带 options
- 删除 `parseOptions()` 和 `AIOption` 结构体

---

## 2026-06-10 v11: 选项按钮发编号 + Debug 清理
## 2026-06-10 v10: parseOptions + 对话历史（桥接 v3）
## 2026-06-10 v9: ⊕ toggle + 选项不可点修复
## 2026-06-09 v8: AI Tab · DeepSeek自动回复 · 逐条⊕添加
## 2026-06-09 v7: 配色 A/B → 选B（明亮现代）
## 2026-06-09 v6: 韦斯·安德森分散互补配色
## 2026-06-09 v5: 情境命名 · 优先级颜色 · 搜索始终可见
## 2026-06-09 v4: 场景文件夹 · 去预设
## 2026-06-09 v3: 纯黑白 · 日历先
## 2026-06-09 v2: 花叔Design · 去标签 · 铁锈红配色
