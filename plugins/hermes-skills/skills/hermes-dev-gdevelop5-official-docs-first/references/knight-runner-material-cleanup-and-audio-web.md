# KnightRunner_Test：素材审计、清理与网页版首局音频

适用场景：
- 用户要求“检查素材，没用的删掉”。
- 用户反馈“网页版第一次没背景音乐，第二次才有”。
- 已有本地网页版导出包，需要同步修复 `data.js/code0.js/zip`。

## 1. 素材清理原则

### 必须先审计，不直接删
按以下集合分类：
1. 项目目录中的媒体文件：`.png/.jpg/.jpeg/.webp/.gif/.mp3/.aac/.wav/.ogg/.m4a/.flac`
2. `KnightRunner_Test.json` / `.autosave` 的 `resources.resources[].file/name`
3. 全量 JSON 字符串引用（对象动画、事件 JS、音频动作等）
4. `BASELINE_CURRENT.json` 引用
5. 已导出的 `~/Desktop/hermes/GDevelop/KnightRunner_Test_web/` 是否包含该文件

只有同时满足以下条件才可视为孤儿素材：
- 不在当前 JSON 文本中出现；
- 不在 `.autosave` 中出现；
- 不在 `BASELINE_CURRENT` 中出现；
- 不在当前导出包中出现。

### 删除方式
用户确认后才处理。删除文件必须移到 Trash，不用 `rm`。处理后回读验证：
- 文件不在项目目录；
- Trash 中存在或系统移动成功；
- JSON 正式文件与 autosave SHA 一致；
- 如移除资源表缺失项，确认对象/事件/变量未改。

### 缺失资源引用
如果资源表引用了不存在的媒体文件（例如 `resources` 中有文件名但项目目录没有），不要当作“删除文件”。应单独报告并在用户确认后从 `resources.resources` 移除该条。删除前确认该文件名不在对象动画/事件/JS 中实际使用。

## 2. 网页版首局无 BGM 的修复

现象：本地/网页版第一次开局没有背景音乐，Retry 第二局才有。

原因：浏览器自动播放策略拦截了没有用户手势的 `playMusicOnChannel`。Retry 由用户点击触发，所以第二局已有用户手势。

稳定做法：
1. 新增场景变量 `AudioUnlocked=0`，在 `SceneJustBegins` 重置。
2. BGM JS 不再开局立即 `playMusicOnChannel`。
3. 每帧检测真实用户输入：
   - `input.isMouseButtonPressed(gdjs.InputManager.MOUSE_LEFT_BUTTON)`
   - `input.getAllTouchIdentifiers()/getStartedTouchIdentifiers()`
   - `input.isKeyPressed("Space")`
4. 第一次检测到输入时：`AudioUnlocked=1`。
5. 只有 `AudioUnlocked==1` 且 `GameOver/VictoryPending/CastleTouched/Win` 全为 0 时，才播放/变速 BGM。
6. 保留原来的 RunSpeed pitch 逻辑与 Castle/VC 停 BGM 门控。

关键：只改音频事件和 `AudioUnlocked` 初始化，不动木桩、跳跃参数、Castle、Retry。

## 3. 已导出网页版包同步

如果用户已经有本地导出包：
`~/Desktop/hermes/GDevelop/KnightRunner_Test_web/`

修改 JSON 后必须同步：
1. 更新 `data.js` 中的 `gdjs.projectData` 为当前项目 JSON；
2. 若不能重新跑 GDevelop 导出，至少 patch `code0.js` 的 BGM 编译代码，加入 `AudioUnlocked` guard；
3. 重新生成 `KnightRunner_Test_web.zip`；
4. 用本地 HTTP 服务验证：
   - `/` 200
   - `/code0.js` 200
   - `/data.js` 200
   - `/ABBB.MP3` 200
5. 回报 zip SHA。

## 4. 审计输出建议

给用户只报可行动结果：
- 可删孤儿素材清单；
- 缺失资源引用清单；
- 是否需要用户确认删除；
- 明确“先不删/已移废纸篓”。

避免把大量过程日志刷到聊天里。