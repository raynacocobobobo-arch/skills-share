# KnightRunner_Test：跳跃音效接入参考

适用：用户要求“骑士跳跃时播放某个声音/音效”。

## 官方依据

- Audio / Sounds and music Reference：`Play a sound` 的 JSON 内部类型是 `PlaySound`。
- `PlaySound` 参数结构：内部空参数、音频资源名、是否循环、音量、音高。
- 短音效用 sound，不要当 BGM/music 播放；BGM 继续用现有 music 逻辑。

## 本项目稳定做法

1. 先比较正式 `.json` 与 `.json.autosave`，优先使用较新的 autosave，避免覆盖用户刚在 GDevelop 编辑器里调过的参数。
2. 将音频文件复制到项目目录，例如：
   - `/Users/rayna/Documents/GDevelop projects/My project3/1234.mp3`
3. 在 `resources.resources` 追加或修正 audio resource：

```json
{
  "file": "1234.mp3",
  "kind": "audio",
  "metadata": "",
  "name": "1234.mp3",
  "preloadAsMusic": false,
  "preloadAsSound": true,
  "preloadInCache": true,
  "userAdded": true
}
```

4. 若需求是“每次骑士跳跃都有声音”，优先新增一个独立标准事件，而不是把音效塞进二段跳事件：

```text
条件：
- GameOver = 0
- KeyFromTextJustPressed("Space")
动作：
- PlaySound("1234.mp3", no, 80, 1)
```

JSON 结构示例：

```json
{
  "type": "BuiltinCommonInstructions::Standard",
  "conditions": [
    {"type": {"value": "VarScene"}, "parameters": ["GameOver", "=", "0"]},
    {"type": {"value": "KeyFromTextJustPressed"}, "parameters": ["", "\"Space\""]}
  ],
  "actions": [
    {"type": {"value": "PlaySound"}, "parameters": ["", "1234.mp3", "no", "80", "1"]}
  ]
}
```

## 为什么不要直接塞进二段跳事件

本项目存在手动二段跳事件，动作里有：

```text
PlatformBehavior::SetCanJump
PlatformBehavior::SimulateJumpKey
```

如果只给这个事件加 `PlaySound`，只会在手动二段跳时响，普通第一段跳未必响。用户说“每次骑士跳跃的时候”时，应使用 `KeyFromTextJustPressed("Space") + GameOver=0` 的独立事件，覆盖第一段和二段。

## 回归验证

写入正式 JSON 和 `.autosave` 后回读检查：

```text
formal JSON 与 autosave SHA 一致
layout.events[0] 仍是 SceneJustBegins
存在 1 条 PlaySound 事件，条件包含 GameOver=0 + KeyFromTextJustPressed("Space")
音频资源存在 kind=audio、preloadAsSound=true
不要修改 Retry、Score、RunSpeed、障碍、碰撞、Dragon、跳跃手感参数
```

## 常见坑

- `PlaySound` 参数 0 是 GDevelop 内部空参数，不能省略。
- 短跳跃音效用 `preloadAsSound=true`，不要设置成 music。
- 如果此前误把音效插入二段跳动作，改成独立事件时要删除旧位置，避免重复响。
- 不要因为加音效而改 `KnightHorse.PlatformerObject` 的跳跃参数。
