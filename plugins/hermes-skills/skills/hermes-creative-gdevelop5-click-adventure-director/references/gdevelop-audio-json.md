# GDevelop JSON 直改：背景音乐 / 音频资源

适用：用户要求给 GDevelop 项目加背景音乐，或反馈“你没加音乐 / 预览没声音”。

## 稳定流程

1. 先保存并关闭 GDevelop，避免编辑器内存覆盖 JSON。
2. 备份正式 `.json` 和 `.json.autosave`。
3. 音频文件不要只引用桌面路径；复制到项目目录，例如：
   - 源：`~/Desktop/ABBB.MP3`
   - 目标：`/Users/rayna/Documents/GDevelop projects/<project>/ABBB.MP3`
4. 在 `data["resources"]["resources"]` 注册资源，推荐字段：
   ```json
   {
     "alwaysLoaded": false,
     "file": "ABBB.MP3",
     "kind": "audio",
     "metadata": "",
     "name": "ABBB.MP3",
     "preloadAsMusic": true,
     "preloadAsSound": false,
     "preloadInCache": true,
     "userAdded": true
   }
   ```
5. 不要只依赖 `PlayMusicCanal` / `RePlayMusicCanal` 这类内部动作名；不同 GDevelop 版本/语言下可能写入 JSON 后预览不执行。更稳做法是在场景开始事件里加 JS 动作。
6. 场景开始播放音乐事件：
   ```json
   {
     "type": "BuiltinCommonInstructions::Standard",
     "conditions": [
       {"type": {"value": "DepartScene"}, "parameters": [""]}
     ],
     "actions": [
       {
         "type": {"value": "BuiltinCommonInstructions::JsCode"},
         "parameters": [
           "// Hermes: play background music ABBB.MP3 once when scene starts\nif (!runtimeScene.getVariables().get('ABBBMusicStarted').getAsBoolean()) {\n  runtimeScene.getVariables().get('ABBBMusicStarted').setBoolean(true);\n  gdjs.evtTools.sound.playMusicOnChannel(runtimeScene, \"ABBB.MP3\", 0, true, 55, 1);\n}"
         ]
       }
     ]
   }
   ```
7. 写入正式 `.json` 和 `.json.autosave`，然后回读验证：
   - 项目目录存在音频文件；
   - `resources.resources` 中存在 `kind="audio"`、`file/name="ABBB.MP3"`；
   - 事件中存在 `BuiltinCommonInstructions::JsCode`；
   - 事件代码中存在 `gdjs.evtTools.sound.playMusicOnChannel` 和目标文件名；
   - 正式文件与 autosave 一致。
8. 重新用项目路径打开 GDevelop，并确认进程参数包含项目 JSON 路径。

## 排障口径

- 如果资源和 JS 播放事件都回读存在，只能说“已写入，待预览验证”，不要直接说“游戏里一定有声音”。
- 如果用户预览仍无声，优先考虑浏览器/预览端自动播放策略：把播放事件改到首次用户交互（如第一次按空格/第一次鼠标点击）里触发，而不是继续重复注册资源。
- 如果检查字符串时匹配失败，注意 JSON 会转义引号；应解析 JSON 检查事件参数，或用更宽松的 `playMusicOnChannel` / 文件名存在检查，不要误判写入失败。

## 与外部上传 JSON 结合

用户上传新的完整 JSON 并要求“你改下 JSON”时：

1. 先验证上传 JSON 可解析。
2. 若上传 JSON 本身不含音频资源/事件，不要报告“已包含”；以上传 JSON 为底稿，重新执行本流程补音乐。
3. 再覆盖正式 JSON + autosave，避免用户上传的新逻辑被旧项目或 autosave 覆盖。