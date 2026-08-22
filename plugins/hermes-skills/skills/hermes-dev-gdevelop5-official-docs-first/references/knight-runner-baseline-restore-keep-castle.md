# KnightRunner_Test：按历史基准全量回归，同时保留 Castle/V3/VC 终点流程

适用：用户明确要求“对照某个 Castle 前版本 / 17:00 那版 / 其它都对齐，只保留 Castle 相关事件”。

## 核心原则

不要只对比木桩事件。用户说“完整对照某版”时，应以指定历史 JSON 为母版，再把 Castle/V3/VC 终点流程作为最小增量移植回去。

## 推荐流程

1. 关闭 GDevelop，避免 autosave 覆盖。
2. 备份当前正式 JSON 和 autosave。
3. 读取用户指定基准文件，例如：
   - `KnightRunner_Test.json.bak_mobile_tap_direct_double_20260621_170107`
4. 以基准 JSON 为 `new` 母版，而不是在当前脏版本上继续补丁。
5. 从当前版本只迁移 Castle 相关：
   - 资源：`castle.png`、`V3.png`、`VC.mp3`
   - 对象：`Castle`、`V3`
   - 实例：`Castle`、`V3`
   - 场景变量：`CastleVisible`、`CastleSpeedLocked`、`VictoryAudioPlayed`、`CastleTouched`、`VictoryPending`、`Win`
   - 事件：Castle 接近清障/降速、Castle 移动、骑士碰 Castle 播 VC、Castle 出画后显示 V3 + re
6. 对基准障碍生成链路只追加 `CastleVisible = 0` 门控；不要改基准的 GroupGap、GroupSize、对象大小、开局预置木桩。
7. 若胜利状态会触发旧 GameOver UI/BGM，允许最小补丁：
   - BGM 事件增加 `VictoryPending/CastleTouched/Win = 0` 门控，避免 VC 播放后 BGM 重启。
   - GameOver UI 脚本在 `Win=1` 时隐藏 `go/M/Best/ScoreDigit`，但保留 `re` 在 V3 后显示。
8. 同步写入正式 JSON 和 `.autosave`，并重新打开 GDevelop。

## 验证清单

- 除 `Castle/V3/VC` 外，对象定义与基准一致。
- 除 `Castle/V3` 外，场景实例与基准一致。
- 资源差异只包含 Castle/V3/VC 相关文件。
- 基准木桩创建计数保持一致。例如 17:00 版实际只生成普通木桩：
  - `NewSprite12: 6`
  - `NewSprite12Medium: 0`
  - `NewSprite12Big: 0`
  - `ObstacleHitbox: 6`
- `SceneJustBegins` 仍是第 0 条顶层初始化事件。
- Castle 清障必须有接近门槛，例如 `Castle.X < 2600`，不能开局就清空木桩。
- 生成障碍事件可加 `CastleVisible=0`，但初始化事件条件不能加这个门控。

## 重要坑

### 1. 不要凭对象存在判断木桩大小

历史版本可能有 `NewSprite12Medium/NewSprite12Big` 对象定义，但生成事件并不创建它们。必须统计 `Create` 动作，而不是只看 objects。

### 2. V3 对象可能引用错图

迁移 `V3` 对象后必须检查动画帧实际 `image` 字段。曾出现项目目录有 `V3.png`，但对象引用 `V4.png/V5.png/V6.png` 的情况。若只迁移了 `V3.png`，必须把 `V3` 对象动画收敛为单帧 `V3.png`，并验证：

```text
v3_images == ['V3.png']
missing == []
```

### 3. 全量对齐历史版会回退鼠标/触屏跳跃

某些历史基准（如 17:00）鼠标跳跃用 `MouseButtonFromTextReleased`，不是后续稳定的“按住模拟 Space”。如果用户反馈“鼠标没有二段跳 / 第一段高度不对”，应恢复 core-systems 里的官方 runtime JS：

```text
getInputManager()
isMouseButtonPressed(MOUSE_LEFT_BUTTON)
simulateJumpKey()
MouseJumpWasDown
```

并删除旧的三个鼠标释放跳跃事件，保留 Retry 的 `GameOver=1 + IsCursorOnObject(re) + MouseButtonFromTextReleased`。

### 4. 自定义事件标记不可靠

不要依赖自定义 JSON 字段（如 `hermesCastleFinish`）定位事件。GDevelop 保存可能清掉未知字段。应按对象/变量/代码内容定位。
