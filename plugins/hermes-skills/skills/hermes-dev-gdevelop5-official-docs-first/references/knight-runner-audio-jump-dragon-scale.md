# Knight Runner：死亡音乐、二段跳高度、红龙缩放修正参考

## 适用场景
GDevelop 5 项目 `KnightRunner_Test.json` 中：
- 死亡时停止背景音乐；
- 第二段二段跳高度降低；
- Dragon2 某一方向飞行时变大。

## 官方依据
- Audio Reference：
  - `PlayMusic` 参数：`[internal, audio resource, repeat, volume, pitch]`。
  - `UnloadAllAudio` 会停止并卸载所有声音和音乐。
  - `StopMusicChannel` 只停止指定音乐频道。
- Platform behavior Reference：
  - `PlatformBehavior::JumpSpeed` 可在事件中修改角色 Jump speed。
  - `PlatformBehavior::SetCanJump` 可用于允许空中再次跳跃。
  - `PlatformBehavior::SimulateJumpKey` 模拟跳跃键。
- JavaScript Code events：可在事件表中使用 JS 访问 runtimeScene/runtime objects。

## 已验证做法
1. 背景音乐播放动作不要把旧资源塞到参数 0：
   - 正确：`PlayMusic ["", "ABBB.MP3", "yes", "70", "1"]`
2. 死亡碰撞事件里，在 `GameOver = 1` 后立即加：
   - `UnloadAllAudio [""]`
   这样比 JS `sound.stopMusic(...)` 更稳，且符合官方 Audio Reference。
3. 死亡音效如仍需播放，放到独立事件：
   - 条件：`GameOver = 1` 且 `DeathAudioPlayed = 0`
   - 动作：`PlaySound ["", "A.mp3", "no", "100", "1"]`，然后 `DeathAudioPlayed = 1`
4. 二段跳降低高度（修正后的稳定做法）：
   - 不要在二段跳事件里临时 `JumpSpeed=410` 后立刻恢复；用户实测会被同帧恢复抵消，效果不明显。
   - 稳定做法：二段跳事件中 `SetCanJump` 后设置 `PlatformBehavior::Gravity = 3200`，再 `SimulateJumpKey`；不要立刻恢复。
   - 在 `IsOnFloor` 落地重置事件和 `SceneJustBegins` 初始化里恢复 `PlatformBehavior::Gravity = 1650`。
5. Dragon2 左→右变大 30%（修正后的稳定做法）：
   - 不要用 `dragon.setScale(1.3)`；它会按原始大图缩放，导致红龙突然巨大。
   - 稳定做法：保留当前实例尺寸基准 `155x159`，左→右飞行（`DragonState == 2`）时用 JS 设置 `setWidth(202)`、`setHeight(207)`；其他状态恢复 `setWidth(155)`、`setHeight(159)`。
   - 不需要新增 `DragonScaleState`。

## 修改注意
- 写正式 JSON 后同步 `.autosave`。
- 写后必须重新读取 JSON 验证格式、关键事件和 SHA。
- 改音频不碰障碍生成；改二段跳不碰普通跳跃事件；改红龙缩放不碰红龙移动速度与等待时间。