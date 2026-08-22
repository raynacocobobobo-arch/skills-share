# KnightRunner_Test：素材清理审计 + Web 首局 BGM 解锁

适用：用户反馈“素材没用的该删”“网页版第一次没背景音乐，第二次才有”。

## 1. 素材清理必须先审计，不直接删

流程：

1. 读取最新源：比较 `KnightRunner_Test.json` 与 `.autosave`，优先较新的文件。
2. 扫描项目目录媒体文件：`.png/.jpg/.webp/.gif/.mp3/.aac/.wav/.ogg/.m4a/.flac`。
3. 对比三类引用：
   - `resources.resources[].file/name`
   - 整个 JSON 深度字符串引用
   - 已导出的 web 包目录是否存在同名文件
4. 输出清单：
   - JSON 正在引用的素材
   - 资源表有但文件缺失的坏引用
   - 完全未引用的孤儿文件
5. 只有用户确认后才清理；删除文件必须走 Trash，不用 `rm`。
6. 清理 JSON 资源表坏引用时，不动事件、对象、实例、变量、玩法逻辑。
7. 清理后必须回读验证，并重新导出 web 包。

本次已验证的审计维度：当前 JSON、autosave、`BASELINE_CURRENT`、已导出的 `KnightRunner_Test_web/` 都要查；不要只看当前 JSON。

## 2. 浏览器首局 BGM 被拦截的修复

症状：

- GDevelop 预览/网页版第一局没有背景音乐；
- Retry 后第二局有音乐。

原因：浏览器 autoplay policy 拦截未经过用户手势的 `playMusicOnChannel()`。Retry 是用户点击后触发，所以第二局能播。

稳定修法：

1. 新增场景变量 `AudioUnlocked=0`。
2. `SceneJustBegins` 重置 `AudioUnlocked=0`。
3. BGM JS 不要开局直接播放；先检测真实用户手势：
   - `input.isMouseButtonPressed(gdjs.InputManager.MOUSE_LEFT_BUTTON)`
   - `input.getAllTouchIdentifiers()/getStartedTouchIdentifiers()`
   - `input.isKeyPressed("Space")`
4. 任一成立后 `AudioUnlocked=1`，之后才执行：
   - `playMusicOnChannel(runtimeScene, "ABBB.MP3", 1, true, 70, targetPitch)`
   - 或 `setMusicOnChannelPitch()`
5. 保留 Castle/胜利/GameOver 门控：`GameOver/VictoryPending/CastleTouched/Win` 时直接 return，防止胜利音乐后 BGM 重启。

## 3. 修改边界

修 Web 首局音乐时只动：

- BGM JS 事件；
- `AudioUnlocked` 场景变量；
- `SceneJustBegins` 的 `AudioUnlocked=0` 初始化；
- 已导出 web 包中的 `data.js/code0.js` 或重新导出。

禁止顺手改：木桩、跳跃参数、Castle 流程、Retry、对象尺寸、实例位置。

## 4. 回读验证

必须验证：

```text
AudioUnlocked_var: True
AudioUnlocked_init: True
bgm_has_unlock_guard: True
bgm_has_user_inputs: True
formal_autosave_same: True
```

若已存在本地导出包，还要确认：

```text
data.js contains AudioUnlocked
code0.js contains AudioUnlocked
/ABBB.MP3 HTTP 200
```
