---
name: todo-fix
description: HermesTodo iOS App 修改追踪——每次修改和错误都记录在此，修改前必读。编译坑见 swiftui-swiftdata-pitfalls。
triggers:
  - 修改 HermesTodo
  - todo app 改版
  - todo 待办
  - 待办 bug
  - iOS todo
  - 情境
  - AI 待办
  - 语音崩溃/闪退
  - 图标白板/空白
  - 真机无反应/no response
  - 手机上不能用/手机端不能用/打不开/没更新/hermes to do 用不了
  - 无法删除/改名
---

# HermesTodo 修改追踪

## 项目档案

- **路径**: `${HERMES_TODO_ROOT:-/path/to/HermesTodo}/`
- **主文件**: `HermesTodo/HermesTodo.swift` (单文件 SwiftUI App)
- **AI 架构**: 直连火山 Ark Code API（`ark.cn-beijing.volces.com/api/coding/v3/chat/completions`），模型 `ark-code-latest`，API key + system prompt 嵌入代码。无外部桥接依赖。旧桥接 `ai_bridge.py` 已废弃但保留于项目根目录。
- **架构**: SwiftUI + SwiftData, iOS 真机/模拟器双目标
- **数据模型**: Folder, TaskItem, ChatMessage, AISuggestion
- **UI 结构**: ContentView → 日历Tab(MonthCal+TaskList) | 日常Tab(folderList→TaskList) | AI Tab(aiChatView+建议列表)

## 项目快照 (v20 · 当前)

- **三Tab**: 首页 / 情境 / AI（sparkles图标）；日历退为首页里的 Dashboard/今日任务入口。
- **配色 · 当前方向**: 奶油白 + 暖棕黑字 + 珊瑚/芥末/鼠尾草/淡蓝灰点缀；避免纯黑白、高饱和和紫色系。
- **AI Tab · 直连火山 Ark Code**: App 内直接调 `https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions`，模型 `ark-code-latest`。维护本地 `chatHistory:[(role,content)]`（最近6条/3轮）。支持 JSON 解析 → 重试 → 降级三级策略。`systemPrompt` 内嵌在 Swift 代码中。`clearAIChat()` 只清本地数组，不发网络请求。
- **AI输出规范**: AI 是「任务规划器」不是说明书。`reply` 最多一句短话；`suggestions[].title` 必须是短待办（物品类只写物品名，如“身份证”，不要写“身份证放包里内部夹层”）。选项必须走 `options:[String]`，不要从正文正则解析。
- **AI页当前交互**: 多轮对话中累计 `aiSuggestions`，按清洗后的标题去重，统一沿用 `aiConversationContext`。用户不再逐条点 ⊕；只点「汇总成待办」，`importAISuggestionsToContext()` 一次性把去重后的所有建议导入同一个情境，并跳过该情境里已有同名任务。
- **导入列表质量要求**: 用户明确反感“按原文导入后被过度总结/简化”。导入列表必须 AI 完整解析优先：`title` 短，但原文里的数量、条件、地点、时间、提醒、说明、注意事项必须保留到 `note`；`category` 优先沿用原文分组/表头/段落名。本地兜底只能兜底，不能抢活；兜底时一行一任务、备注保留原行/后续列信息，不要按逗号/表格单元格拆碎成低信息量清单。
- **AI 多轮汇总新方向**: AI 页不要依赖用户手动框选/逐条挑选选项。多轮对话中 AI 可以反问和给候选项，但应维护一份会话级候选池；用户点击“汇总/生成待办清单”后，自动把多轮中的所有候选项去重、清洗标题，并统一写入同一个情境。情境名沿用会话的第一个明确 context / `aiConversationContext`，没有则由最终汇总生成一个短情境名。
- **键盘行为**: 输入框聚焦时隐藏底部 FloatingTabBar，只保留输入栏，避免「首页/情境/AI」浮在键盘上方；底部输入区必须用 `.safeAreaInset(edge: .bottom)` 承载，让页面内容自动让位，不能用 `ZStack/overlay + safeAreaPadding` 硬垫高度；不要在根视图全局 `.ignoresSafeArea(.keyboard)`。输入字幕/普通输入/AI输入时，点击页面空白区域必须收起键盘：可加 `hideKeyboard()` helper + 根视图 `.simultaneousGesture(TapGesture().onEnded { inputFocused=false; aiInputFocused=false; hideKeyboard() })`，切 Tab 时也同步 resign focus。
- **ChatMessage 模型**: `options: [String]` 属性，每条消息自己带选项按钮，非全局状态。
- **VoiceBtn**: AVAudioSession `.record` 模式（纯录音），`isAvailable` 前置检查。识别错误静默停止，不抛异常。
- **情境卡片**: LazyVGrid 卡片 + 卡片内按钮/长按菜单；支持删除；编辑入口统一进入 `FolderEditSheet`，在一个 Sheet 内修改名称、图标、颜色。不要再拆成“重命名 Alert + FolderIconSheet”两套入口，也不要依赖 `LazyVGrid` 里的 `swipeActions`。
- **任务排序**: 情境内任务支持 `TaskSortMode`：按优先级 / 截止时间 / 创建时间。默认优先级；Section header 放 `Menu` 切换排序。`active` 列表用 Swift 侧 `.sorted { sortTasks($0,$1) }`，避免改 SwiftData schema。
- **AI 标题清洗**: `handleAIResult` 创建 `AISuggestion` 前必须走 `cleanAITitle` + `normalizedPriority`。清洗编号前缀、括号说明、逗号/句号/冒号后的解释，并去掉“建议/确保/避免/提前/记得/检查/最好/需要/把/放在/放到”等词，超长截到 12 字，防止模型把说明书塞进待办标题。
- **图标**: `icon_1024.png` 精确 1024×1024；AI 新建情境时可按 context 名称猜 SF Symbol，已有情境可通过 `FolderIconSheet` 更换图标。
- **构建**: `env -u TMPDIR xcodebuild -scheme HermesTodo -destination "id=<device-id>" -allowProvisioningUpdates build`（⚠️ WiFi 无线调试下用 `id=` 不带 `platform:iOS,` 前缀，否则 xcodebuild 找不到设备）
- **安装**: `xcrun devicectl device install app --device <devicectl-device-id> <app_path>`
- ⚠️ **禁止卸载旧版**：`uninstall` 会清空 SwiftData 数据库（用户所有情境、任务全丢）。只做 `install` 覆盖更新，数据保留。

## 用户偏好速查

### HermesTodo 重构方向（2026-06）

- 产品定位从「Todo App + AI聊天」升级为「首页控制台 + 情境管理 + AI任务规划 + 执行/专注系统」。
- 重构优先级：① HomeDashboard 首页 ② ContextGrid 情境卡片 ③ AIPlanner 任务规划；先做观感提升最大的 70%，不要一次性全拆模型/文件。
- 一级 Tab 推荐从「日历 / 日常 / AI」改为「首页 / 情境 / AI」；Calendar 不再作为核心入口。
- AI 页弱化聊天气泡，主流程改为「我想完成什么？」→ AIPlan → 待办建议逐条添加；ChatMessage 可过渡保留，不要第一刀硬删。
- 情境页适合卡片网格；若用 LazyVGrid，原 swipeActions 不稳定，应改长按菜单/卡片按钮。
- 任务详情符合用户偏好的是底部 Sheet（TaskDetailSheet），不是传统页面跳转详情页。
- 文件拆分放后期：先在单文件内用 MARK 分区稳定 UI，再拆 Models/Views/Theme，降低 Xcode/pbxproj 和 private 作用域风险。

- UI 叫"情境"不叫"文件夹"
- 日常页只显示情境列表，不进情境不显示 todo
- **配色**：干净明亮不冷——不要纯黑白、不要低饱和暗沉、不要紫/紫蓝渐变。B方案是三轮迭代后选定的
- **AI交互**：建议列表逐条⊕添加是旧版过渡方案；新方向是不让用户手动框选。AI 多轮对话结束后，一键汇总所有候选项，自动去重并放进一个情境；中间反问选项只用于推进对话，不要求用户逐条挑待办。
- **AI质量**：需求宽泛时反问2-3个具体方向确认，不要编造宏大无用的答案
- **一个对话/一个回答一个情境**：不要分子情境；必须在代码层硬约束，不能只靠 prompt。AI 返回多个 `context` 时，`handleAIResult` 统一取第一个非空 context；同一轮多轮对话要维护 `aiConversationContext`，后续 suggestions 继续沿用第一个情境，除非用户清空/新对话；所有 suggestions 强制归入同一情境。
- **情境间移动**：任务行滑动菜单要有「移动」，触发 `FolderPop`，可从情境A移动到情境B。主任务移动 folder；编辑页里的子任务默认跟随父任务，不单独移动。
- **选项可点、底部不重叠、可单独复制问题**
- **情境/情境内待办一键复制**：情境卡片和长按菜单要有「复制待办」；进入某个情境后，待办列表顶部也要有「复制」。复制到 `UIPasteboard.general.string`，格式优先：`【情境名】` 换行 + `○ 未完成任务` / `● 已完成任务`，不要另存文件，不要弹复杂分享页。
- **UI不重复**：不要文字里写一遍编号又在下面重复按钮（"脱了裤子放屁"）
- **左滑按钮**：用"修改名称"不用"改名"
- **AI提示示例**：用户场景化（如"罗马必打卡景点"），不用通用模板

## 编译坑

| 坑 | 表现 | 解决 |
|----|------|------|
| **🆕 macOS Calendar 默认日历源统一** | 用户反馈“日历账号切换不了”或发现同一行程散落在 `工作`、QQ/iCloud 等多个日历源 | 先列出当前日程所属日历，确认目标日历名；用户确认后，把当天/相关事件从旧日历复制到目标日历再删除旧事件，并用 AppleScript 回读核验。以后默认写入用户指定日历源（当前为 `271009949@qq.com`），不要写入 `工作`。迁移时注意不要漏掉重叠/不同源事件；迁完再按标题+时间核对总数。 |
| **🆕 导入列表过滤要同时防误入和防丢** | 收紧章节/解释句过滤后，容易只验证“第五部分/第六部分没进待办”，但没验证真实物品、数量、备注是否被误删 | 改导入过滤后必须跑夹具：章节标题/解释句不进待办，同时真实行如“布洛芬 2盒 | 退烧止痛，成人用”“护照 | 有效期6个月以上”必须保留 title/category/note。注意 Swift raw string 里 `#(cnNum)` 不会插值；“部分”不能写成字符类 `[章节部分...]`，要用分组 `(章节|章|节|部分|部|...)`。详见 `references/import-list-validation-fixtures.md`。 |
| **🆕 导入列表点了但没生成情境** | 用户在 AI 页导入表格/清单后，AI 页可能显示处理中或预览，但情境页没有新情境 | 不要只依赖 AI 返回 `suggestions`。导入时保存 `pendingImportListRaw/pendingImportContextHint`，先 `clearAIChat()` 再设置 `autoImportAfterAIResponse=true`，请求用 `resetConversation:false` 避免状态被清掉。所有失败路径都必须兜底：`sendAIRequest` 创建请求失败/API 无返回、`parseAIResponse` 空内容、`retryParseJSON` 请求失败/仍非 JSON，都调用 `finishPendingImportLocally()`，不能只 `aiLoading=false` 静默返回。`handleAIResult()` 中如果 AI 没解析出 suggestions，则用 `localParseImportedList()` 本地按行/表格分隔符兜底生成 `AISuggestion`，再调用 `importAISuggestionsToContext()`。详见 `references/import-list-autofallback.md`。 |
| **🆕 真机 App 没改但编译成功** | 用户打开手机 App 看不到新功能，实际只是 build 成功，没有安装到手机 | 汇报前必须完成覆盖安装验证：`xcodebuild` 看到 `BUILD SUCCEEDED` 只代表编译；还要执行 `xcrun devicectl device install app --device <coredevice-id> <App.app>` 并看到 `App installed:`。禁止 `uninstall`，避免清空 SwiftData 数据。 |
| **🆕 无线调试下 xcodebuild destination 找不到设备** | `-destination 'platform=iOS,id=00008140-...'` 报 `Unable to find a destination`，但 `xcrun xctrace list devices` 显示在线 | 无线/WiFi 连接（tunnelState=connected）的设备用 `id=xxx` 不带 `platform:iOS,` 前缀。ChatGPT 脚本就是这么写的。正确：`xcodebuild -destination "id=$UDID" ...`。检查无线状态：`xcrun devicectl device info details --device $UDID \| grep tunnelState` |
| **🆕 情境内新增任务默认不带日期** | 用户在具体情境里添加东西，结果任务默认带了今天日期 | 只有首页/今日视图添加任务才默认 `dueDate = 今天`。进入具体情境 `selFolder != nil` 时，快速输入和 AddSheet 都必须默认 `dueDate = nil`；判断写成 `(currentTab == .home && selFolder == nil) ? today : nil`，不要只看 `currentTab == .home`。 |
| **🆕 情境/情境内待办需要一键复制** | 用户想把某个情境里的 todo list 直接发给别人/粘贴到别处 | 在情境卡片按钮区和 contextMenu 加「复制待办」；在情境内 TaskList header 加「复制」。实现用 `UIPasteboard.general.string = lines.joined(separator: "\\n")`，格式：`【情境名】` + `○/● 任务标题`。注意脚本生成 Swift 源码时要写 `"\\n"`，不要写成真实换行导致 unterminated string。 |
| **🆕 同一 AI 对话再次拆多个情境** | 单次回答已统一 context，但连续追问后又出现多个情境 | 只在 `handleAIResult` 里取本次 suggestions 的第一个 context 不够。新增 `@State aiConversationContext: String?`；第一次有 suggestions 时写入，后续 suggestions 全部强制用它；`clearAIChat()` 时清空。Prompt 同时写「后续追问沿用第一个情境」，但代码层兜底才是关键。 |
| **🆕 点击空白收起键盘** | 输入字幕/任务/AI 文本后，点页面空白区域键盘不收起 | 加全局 helper：`UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to:nil, from:nil, for:nil)`；根视图加 `.simultaneousGesture(TapGesture().onEnded { inputFocused=false; aiInputFocused=false; hideKeyboard() })`；切 Tab 时也 resign focus。配合 `if !inputFocused && !aiInputFocused { FloatingTabBar(...) }`，避免 AI 输入时 TabBar 浮在键盘上。 |
| **🆕 底部输入框遮挡页面内容** | 用户打字或浏览底部内容时，输入文字框仍盖住首页/情境/AI 页面内容；只调 `.safeAreaPadding(.bottom, 76/130)` 不够 | **根因**：底部栏放在 `ZStack/overlay` 里是悬浮层，页面布局不知道它占空间。**修复**：把根 `ZStack(alignment:.bottom)` 改为普通 `NavigationStack`，底部输入区放进 `.safeAreaInset(edge: .bottom, spacing: 0) { bottomBar }`。这样系统会自动为页面内容让出底部空间。保留 FocusState 逻辑：聚焦时隐藏 `FloatingTabBar`，只显示输入框；不要用全局 `.ignoresSafeArea(.keyboard)`。 |
| **🆕 safeAreaInset 已改但真机仍遮挡** | 已确认无 overlay/ZStack/ignoresSafeArea，FocusState 正常、TabBar 会隐藏、`.scrollDismissesKeyboard(.interactively)` 已加，但键盘/底栏仍压住页面底部内容 | **根因**：`NavigationStack + safeAreaInset + 内部 List/ScrollView` 在真机上可能高度计算不同步，内部滚动容器不知道外层 inset。**修复**：给内部滚动容器单独加底部留白：`List` 后加 `.safeAreaPadding(.bottom, 110)`；`ScrollView` 末尾的 `Color.clear.frame(height: 20)` 改为 `130`。Sheet 内 TextField 遮挡时，外层 `.sheet { View().presentationDetents([.medium, .large]) }`。 |
| **🆕 键盘弹出时底部 Tab 浮在键盘上** | 用户打字时「首页/情境/AI」一直浮在键盘上方，遮挡且干扰 | 给普通输入框和 AI 输入框分别绑定 `@FocusState`（如 `inputFocused` / `aiInputFocused`）。底部容器里 `if !inputFocused && !aiInputFocused { FloatingTabBar(...) }`，并用 `.transition(.move(edge:.bottom).combined(with:.opacity))` + `.animation(...)`。聚焦时只保留输入栏。底部容器仍应放在 `.safeAreaInset(edge:.bottom)` 里，而不是 overlay。不要用全局 `.ignoresSafeArea(.keyboard)` |
| **🆕 AI 待办太像说明书** | 例如用户只需要「身份证」，AI 输出「身份证放包里内部夹层」 | Prompt 要把 AI 定义成「只产出待办清单，不是说明书」。`suggestions[].title` ≤12个汉字，物品/证件/打包类只写物品名；禁止写解释、方法、位置、确保、检查、提前、记得。`reply` 最多12字；反问只用 `options:[String]` |
| **🆕 情境内缺轻重缓急** | 用户在情境里看不出任务重要度排序 | 不新增复杂模型，复用 `TaskItem.Priority`。给 `Priority` 增加 `rank`（high=0, medium=1, low=2），`active` 列表 `.sorted` 按 `priority.rank → dueDate → order → createdAt`。任务行用优先级文字胶囊按钮替代小圆点，点胶囊打开 `PriPop`；滑动菜单也加「优先级」 |
| **🆕 编辑情境入口分散** | 情境卡片上“修改名称”和“更换图标”分开，后续加颜色会更乱 | 统一为 `@State private var folderToEdit: Folder?` + `.sheet(item:$folderToEdit){ FolderEditSheet(folder:$0) }`。`FolderEditSheet` 用 `@Bindable var folder`，本地 `@State name/icon/col` 承载编辑草稿，保存时一次性写回 `folder.name/iconName/colorHex`。卡片按钮和 contextMenu 都进入“编辑情境”，不要再维护 `folderToRename/folderToIcon/renameText` 三套状态。 |
| **🆕 情境任务排序系统** | 用户需要在情境里切换“轻重缓急 / 时间 / 新旧”，但不想动复杂模型 | 新增普通 Swift enum `TaskSortMode: priority/dueDate/createdAt`，放在 View 状态 `@State private var sortMode`。`active` 列表过滤后 `.sorted { sortTasks($0,$1) }`。Section header 用 `Menu` 切换排序。默认 `.priority`；按截止时间时 nil 日期排后面；按创建时间用 `createdAt >` 新任务在前。不要新增 SwiftData 字段。 |
| **🆕 AI 标题代码层清洗** | Prompt 已要求短待办，但模型仍会输出“建议/确保/提前/放在…”这类说明书标题 | 在 `handleAIResult` 创建 `AISuggestion` 前调用 `cleanAITitle(_:)`：去编号前缀、括号说明、逗号/句号/冒号后的解释，删除“建议/确保/避免/提前/记得/检查/最好/需要/把/放在/放到”等词，trim 后最多 12 字。priority 同时走 `normalizedPriority`，兼容中文“高/低”和英文 high/low。 |
| **🆕 外部上传整文件含占位实现/截断括号** | 用户发来新 `HermesTodo.swift` 要替换编译，文件里可能有 `/* 省略 */`、`[REDACTED]`、单行 struct 缺右括号；直接替换会让 AI 功能静默失效或编译炸 | 替换前先扫 `REDACTED|省略|sendAIMessage() { /*|copyAIChat() { /*`，统计 `{}` 差值；若有占位，用旧版备份里的真实实现/配置回填；长单行 Sheet/struct 优先展开重写，不靠盲目补括号。写入后 read 验证，再 build |
| **🆕 AI 一次回复拆多个情境** | 用户在一个对话里让 AI 生成待办，结果 App 按每条 suggestion 的 `context` 建了 4 个子情境 | **代码层统一 context**：在 `handleAIResult` 里不要信任每条 suggestion 自带 context。先从本次 `sugs` 取第一个非空 context 作为 `unifiedContext`，再让所有 `AISuggestion(..., context: unifiedContext, ...)`。Prompt 写“一个回答一个情境”不够，必须硬约束 |
| **🆕 AI 输入栏与键盘重合** | AI 页点输入框后底部输入栏/浮动 Tab 被键盘盖住 | 检查根视图或外层容器是否加了 `.ignoresSafeArea(.keyboard, edges: .bottom)`；若有先去掉，让 SwiftUI 默认键盘安全区把底部栏顶上去。修复后 read 验证并 `env -u TMPDIR xcodebuild ... CODE_SIGNING_ALLOWED=NO` 编译 |
| **🆕 pbxproj Assets 空壳** | `CompileAssetCatalog` 跑了但 `Assets.car` 不生成 / 图标白色 | pbxproj 中 `isa=PBXGroup` + 空 `children` → 改为 `isa=PBXFileReference` + `lastKnownFileType=folder.assetcatalog`。如果挂在 "Recovered References" 下需挪到主 group |
| **🆕 Contents.json 多尺寸** | thinning 步骤裁掉图标，`Assets.car` 16KB 无 AppIcon | 用最简单格式：`{"images":[{"filename":"icon-1024.png","idiom":"universal","platform":"ios","size":"1024x1024"}]}` ，不要逐尺寸声明 |
| **🆕 图标 JPEG 格式** | iOS 不认 JPEG 图标，显示白色占位 | `sips -s format png` 转 PNG，`RGBA` 转 `RGB` 去透明 |
| xcodebuild 沙箱 | `couldNotFindTmpDir` | `env -u TMPDIR xcodebuild...` 或 `TMPDIR=/tmp` |
| overlay三元表达式 | `mismatching types 'some View'` | `@ViewBuilder var` 属性 |
| switch缺分支 | `switch must be exhaustive` | 新增Tab enum后补全所有switch |
| **🆕 AI 一次回复拆出多个情境** | 用户说“一个对话里，你给我建了4个子情景” | prompt 约束不够，必须代码层兜底：在 `handleAIResult` 里先取 `sugs` 的第一个非空 `context` 为 `unifiedContext`，再让所有 `AISuggestion(..., context: unifiedContext, ...)`。原则：用户一次 AI 回复 = 一个情境；不信任模型逐条 context。 |
| **🆕 情境间移动任务** | 用户希望“从情景A移到情景B” | 任务行 `TaskRow` 的 swipeActions 增加「移动」按钮，调用已有 `onFolder` / `FolderPop`，从现有情境列表选择后设置 `task.folder=f`。注意：主任务移动 folder；编辑页里的子任务默认跟随父任务，不单独移动。 |
| **⊕ toggle 静态图标** | 点 ⊕ 添加后变 ✓，但 ✓ 不能点 | `if s.added { Image } else { Button }` → 始终用 `Button{...}label:{Image(systemName:ternary)}`，不要一边 Button 一边静态 View |
| **AI 桥接 追问失败** | 用户点"2"或输入编号，AI 回复"请告诉我具体事项"——忘了上一轮在聊什么 | 桥接没维护对话历史。整改：桥接加 `CONVERSATION_HISTORY` + 每次请求带上最近消息 + `POST /clear` 端点 + App 端"新对话"按钮 |
| **parseOptions 正则丢末项** | `1）2）3）` 只识别出 1 和 2，3 丢失 | 前瞻断言末项后遇尾行文字时 `$` 不触发。改 `([^\\n]+)` 逐行匹配 |
| **脱了裤子放屁** | AI 反问时 reply 里写编号列表，UI 又解析成相同按钮——用户看到两遍 | 废弃 regex 解析。新增 `options` JSON 字段。Prompt 要求反问时 reply 只写引导语。ChatMessage 带 `options: [String]` 属性。删除 `parseOptions()` 和 `AIOption` |
| **历史污染→API空响应** | 第二轮请求 DeepSeek 返回 `Expecting value`，json.loads 抛异常 | 历史里存了编号格式文本，DeepSeek 把编号当输出格式要求 → 输出乱掉。修复：`CONVERSATION_HISTORY` 只存 `result["reply"]` 原始文本，不拼接 options 编号行。原则：**对话历史是语义记忆，不存 UI 格式** |
| **🆕 response_format 陷阱** | 加 `response_format: {"type": "json_object"}` 后 DeepSeek 多轮返回空响应 | **不要用** `response_format`。只靠 prompt 约束输出格式。测试中第5轮必出空响应 |
| **🆕 JSON 重试（v15）** | DeepSeek 偶发不按 JSON 输出。用户说"我希望是to do list不是自然语言" | 不直接降级。先重试一次让 AI 转 JSON（system="你只输出JSON。"，temperature=0.3），再 json.loads。仍失败才降级。代码见 references/ai-bridge.md v5 |
| **🆕 日常页删情境（v15）** | 文件夹左滑无反应 | swipeActions + .alert 确认弹窗。"任务不会被删除，但会移出该情境" |
| **🆕 Assets.xcassets 是 PBXGroup 空壳** | build 成功但无 Assets.car，真机图标白板。build 日志无 CompileAssetCatalog 步骤。`ls app.app/` 有 `Assets.xcassets` 目录而非 `Assets.car` 文件 | pbxproj 三步修复：① 在 PBXFileReference section 新增 `Assets.xcassets = {isa=PBXFileReference; lastKnownFileType=folder.assetcatalog; path=Assets.xcassets; sourceTree="<group>";};` ② 在 HermesTodo source group 的 children 中加入该 ref ③ 从 Recovered References group 和原 PBXGroup section 中删除旧条目。关键：PBXGroup（空 children + path）→ Xcode 当普通文件夹拷贝；PBXFileReference（folder.assetcatalog）→ Xcode 调 `actool` 编译成 `Assets.car` |
| **🆕 调试用 actool 手动编译** | 怀疑 Assets.car 问题时可单步验证 | `xcrun actool Assets.xcassets --compile "$APP" --platform iphoneos --minimum-deployment-target 18.0 --app-icon AppIcon --output-partial-info-plist /tmp/partial.plist`。编译成功后删掉 bundle 中的 `Assets.xcassets` 目录（若有），保留 `Assets.car` |
| **🆕 真机白图标（尺寸）** | 桌面图标显示为白色方块 | AppIcon 图片尺寸不精确——iOS 要求精确 1024×1024，1206×1217 等无效。`sips -z 1024 1024` resize |
| **🆕 真机白图标（格式）** | 图片是 JPEG 格式 | iOS 图标只认 PNG。JPEG 即使 1024×1024 也显示白色。`sips -s format png input.jpg --out output.png` 转换 |
| **🆕 语音真机闪退** | 点语音按钮 App 退出 | ① `SFSpeechRecognizer(locale: "zh-CN")` 可能返回 nil → 加 `guard sr?.isAvailable ?? false else { return }` 前置检查。② `AVAudioSession.setCategory(.playAndRecord, options: [.allowBluetooth])` 中 `.allowBluetooth` 已弃用、真机 crash → 改用 `.record` 纯录音模式。③ audio session 错误时 return 不继续 |
| **🆕 AI 真机无反应** | 真机上 AI 对话完全不工作 | 经历两轮：v18 `localhost`→Mac IP `172.20.10.2`（临时方案）。v19 **彻底拆除桥接**，App 直连 `api.deepseek.com/chat/completions`（HTTPS），不再需要 Mac |
| **🆕 情境卡片 swipeActions 不生效** | 左滑/右滑无反应 | 经历两轮：v18 以为 Button 手势冲突→改 onTapGesture，不生效。v19 发现根因：`swipeActions` 只在 `List` 内生效，`ScrollView`+`VStack`+`ForEach` 中不响应。最终修复：`ScrollView{VStack{ForEach{...}}}` → `List{ForEach{...}}.listStyle(.plain).scrollContentBackground(.hidden)` |
| **🆕 情境左滑删除无反应** | 情境卡片左滑不显示删除按钮 | `swipeActions` 附着在 `Button` 上时手势被 tap 拦截。改用 `onTapGesture`+`contentShape(Rectangle())` 替代 Button 包装 |
| **真机部署** | Developer Mode disabled / no DDI / 无 Team | 见 `references/real-device-deploy.md`。核心：Xcode Devices 窗口同步→手机开开发者模式→选 Team→`-allowProvisioningUpdates` 编译 |
| **🆕 真机 App 没变化：只 build 不会更新手机** | 用户看手机 App 发现没改；根因是只做了源码修改/`xcodebuild`，没有成功 `devicectl device install app` 覆盖安装到真机 | 对 HermesTodo 这类真机 App 改动，汇报“能在 App 里看到/改好了”前必须满足三段验证：①源码写入并 read 回读关键代码；②真机 destination build 成功；③覆盖安装成功。若第③步失败，要明确说“手机上还没更新”，不要让用户误以为已生效。禁止卸载旧版，避免清空 SwiftData 数据。 |
| **🆕 用户说“手机上不能用/打不开/没更新”** | 不要先假设是代码 bug。先按真机部署链路排查：设备是否在线 → build 是否成功 → 是否覆盖安装成功 | 标准顺序：① `xcrun xctrace list devices` 查 `张三` 是否在线；② Offline 时先打开 Xcode Devices and Simulators 刷新；③ `env -u TMPDIR xcodebuild ... -destination 'platform=iOS,id=<device-id>' -allowProvisioningUpdates build`；④ `xcrun devicectl device install app --device <device-id> <App.app>` 覆盖安装；⑤ 只有看到 `App installed:` 才能说手机端已更新。全程禁止 `uninstall`，避免清 SwiftData 数据。 |
| **🆕 真机显示 Offline** | `xcrun xctrace list devices` 里 iPhone 出现在 `Devices Offline`，无法覆盖安装 | 先让用户解锁手机/保持屏幕亮/拔插线/信任电脑；如果仍 Offline，可主动打开 Xcode 的 Devices and Simulators 刷新设备：`osascript -e 'tell application "Xcode" to activate' -e 'delay 2' -e 'tell application "System Events" to tell process "Xcode" to click menu item "Devices and Simulators" of menu "Window" of menu bar 1'`，等 5 秒后重新 `xcrun xctrace list devices`。实测该操作可让 `张三` 从 Offline 变为在线。 |
| **🆕 一键刷新脚本** | 签名每 7 天过期需要重新编译安装 | `~/Desktop/hermes/HermesTodo一键刷新.command`，双击即跑：检查设备在线（含 Offline 唤醒）→ 编译 → 装手机 → 启动。支持 WiFi 无线调试（不插线）。⚠️ 脚本使用 `set -euo pipefail`，中文变量名（如 `DEVICE_NAME="张三"`）可能触发 `unbound variable` 导致脚本炸掉。此时改用手动流程：唤醒设备 → `env -u TMPDIR xcodebuild ... build` → `xcrun devicectl device install app` → 启动。 |
| **🆕 检查无线调试状态** | 不确定设备是 USB 还是 WiFi 连接 | `xcrun devicectl device info details --device $UDID \| grep tunnelState`。`connected` = 无线在线，不需要插线。 |
| **🆕 devicectl 覆盖安装失败 3002/4000** | 构建成功，但 `devicectl device install app` 报 `device disconnected immediately` 或 `Could not get service com.apple.remote.installcoordination_proxy` | 通常是设备连接/锁屏/安装协调服务临时异常，不要无脑重复同命令。先让用户解锁手机、保持屏幕亮、重新插拔数据线/重新信任，再重试覆盖安装；仍失败再打开 Xcode Devices 窗口刷新设备服务。不要 uninstall，避免清空 SwiftData 数据。 |
| **🆕 Assets.car 不生成** | `CompileAssetCatalog` 在 build 日志消失，bundle 无 Assets.car，真机白图标 | pbxproj 中 Assets.xcassets 是空壳 PBXGroup → 改为 PBXFileReference `folder.assetcatalog` 并移入主 group。见 swiftui-swiftdata-pitfalls #28 |
| **🆕 AppIcon Contents.json 坑** | actool 手动编译出图标，xcodebuild thinned 后裁掉 | 多尺寸逐个声明（iphone 20x20@2x...）导致 thinning 丢弃 AppIcon → 改用 universal 1024×1024 单条格式。见 swiftui-swiftdata-pitfalls #30 |
| **🆕 语音真机闪退** | 点语音按钮 App 退出 | 三层：①`SFSpeechRecognizer.isAvailable` 检查 ②AVAudioSession 用 `.record` 不用 `.playAndRecord` ③`stop()` 里释放音频会话。见 swiftui-swiftdata-pitfalls #26 |
| **🆕 真机白图标** | 图标显示白色占位图 | 三项：①图片精确 1024×1024 ②必须是 PNG 不是 JPEG ③Contents.json 用 universal 单条格式。见 swiftui-swiftdata-pitfalls #24/#29/#30 |

所有 SwiftUI/SwiftData 编译坑见 `swiftui-swiftdata-pitfalls`。

## 真机部署

见 `references/real-device-deploy.md`。关键点：命令行无法触发开发者模式，必须 Xcode GUI → Devices 窗口同步。

## AI架构

**当前**: 直连 DeepSeek（v19）。模式见 `references/swift-deepseek-direct.md`。
**旧版**: 桥接架构见 `references/ai-bridge.md`。模板见 `templates/ai_bridge.py`。

## 参考资料

- `references/ai-structured-suggestions.md`：AI 页结构化建议协议（title/category/note/context/priority）、按分类展示、一键汇总导入同情境、备注写入 `TaskItem.notes` 的实现约定。
- `references/import-list-autofallback.md`：导入列表自动生成情境的兜底解析与真机覆盖安装验证流程；避免“导入了但没生成情境”。
- `references/import-list-quality-filters.md`：导入列表质量过滤规则；章节标题、解释句、原因句、说明句不能进入待办，只能作为分类/备注或忽略。关键坑：不能硬编码“第五部分”这类个例，必须用通用结构标题识别，覆盖“第N部分/第N章/第N节/Part N/Section N/Chapter N”等所有 N；并且在最终 `importAISuggestionsToContext()` 写库前再过滤一次，防止 AI 结果漏网。
- `references/import-list-validation-fixtures.md`：导入列表防丢验证夹具；改过滤逻辑后必须验证“坏标题不进待办”与“真实物品/数量/备注/分类不丢”两边同时成立，避免只修误入导致有效信息被删。

## 变更记录

## 2026-06-10 v19: 架构升级——AI 直连 DeepSeek，拆除桥接

- ✅ 用户反馈"必须带电脑"→ 方案B：App 直接 POST DeepSeek API
- ✅ 移除 `@AppStorage("aiServerURL")`，改 `let deepseekKey` + `let deepseekURL`
- ✅ 删除 `ai_bridge.py` 依赖：`sendAIMessage()` 直接构建 `messages` 数组调 DeepSeek
- ✅ `chatHistory: [(role,content)]` 本地维护对话历史（最近6条），`clearAIChat()` 纯本地操作
- ✅ `systemPrompt` 多行字符串嵌入 Swift 代码
- ✅ JSON 解析逻辑完整迁移：markdown围栏去壳 → json decode → 失败重试 → 降级
- ✅ `parseAIResponse` / `retryParseJSON` / `handleAIResult` 三步管线
- ✅ 旧 `ai_bridge.py` 停止运行，保留文件待清理

## 2026-06-10 v18: 5个真机 bug 修复

### Bug 1: 桌面图标白板
- 🐛 AppIcon 图片 1206×1217，iOS 要求精确 1024×1024
- ✅ `sips -z 1024 1024` resize 到标准尺寸

### Bug 2: 语音按钮闪退
- 🐛 `SFSpeechRecognizer` 可能 nil，`AVAudioSession` 配置过激（`.allowBluetooth` 已弃用）
- ✅ 加 `isAvailable` 检查 + 改 `.record` 模式 + error 静默处理

### Bug 3: AI 真机无响应
- 🐛 `localhost:8765` 在 iPhone 上指向手机自己
- v18 ✅ 临时方案 `@AppStorage("aiServerURL")` → v19 ✅ 直连 DeepSeek API，彻底拆除桥接

### Bug 4: 情境无法删除
- 🐛 `swipeActions` 在 `ScrollView` 里不生效（两轮修复最终定位）
- ✅ `ScrollView` → `List(.plain, .scrollContentBackground(.hidden))`

### Bug 5: 情境无法改名
- ✅ 新增左滑"改名"按钮（`.swipeActions(edge:.leading)`）
- ✅ 弹出 `.alert` 带 `TextField`，确认后直接修改 `folderToRename?.name`

---

见 `references/changelog.md`