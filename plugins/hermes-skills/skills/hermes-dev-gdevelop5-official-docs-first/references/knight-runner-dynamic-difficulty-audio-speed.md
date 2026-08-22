# KnightRunner_Test：动态难度、组间距压缩与音乐加速

适用：用户反馈“还是简单”“从 1000 分开始加速”“间隔太大”“音乐也跟着加速”。

## 官方/项目依据

- 使用已验证的 GDevelop 事件动作：`ModVarGlobal` 修改 `RunSpeed`、`ModVarScene` 修改场景变量、`PlayMusic` 播放音乐。
- 当前项目中 `PlayMusic` 参数形态已验证为：

```text
PlayMusic: ["", "ABBB.aac", "yes", "70", "1"]
```

第 5 个参数是音乐播放速度/音高。若不能确认运行时修改 pitch 的内部动作名，不要盲写未知动作；优先用“分数档位触发时重新 PlayMusic 同一首音乐并改变第 5 个参数”的稳定方案。

## 稳定做法

### 1. 速度从指定分数后开始增长

如果用户要求“从 1000 分开始加速”，不要继续用开局就增长的 `sqrt(Score)` 曲线。使用带门槛的线性/缓动公式：

```text
RunSpeed = min(11.0, 5.2 + max(0, GlobalVariable(Score) - 1000) / 2200)
```

含义：

```text
0~1000 分保持 5.2
1000 分后逐步提速
约 16000 分封顶 11.0
```

如果用户仍嫌简单，优先调小分母（例如 2000/1800）或略提上限（例如 11.5），不要先改跳跃。

### 2. 障碍组间距要随难度压缩，不能让速度增长被 GroupGap 抵消

旧问题：`RunSpeed` 变快时，`GroupGap` 也随速度变大，玩家看到的“每组间隔秒数”下降不明显，体感仍简单。

较紧凑但不至于不可玩的当前参考：

```text
普通间距：RandomInRange(300 + RunSpeed * 10, 410 + RunSpeed * 18)
紧凑间距：RandomInRange(240 + RunSpeed * 7, 310 + RunSpeed * 12)
长间距：RandomInRange(480 + RunSpeed * 20, 640 + RunSpeed * 32)
GroupSize=2 追加：RandomInRange(10,45)
GroupSize=3 追加：RandomInRange(35,95)
```

验证体感时估算“秒数”比像素更直观：

```text
平均组间秒数 ≈ 平均 GroupGap / (RunSpeed * 60)
```

当前参考值约：

```text
RunSpeed 5.2：约 1.44 秒/组
RunSpeed 8：约 1.03 秒/组
RunSpeed 11：约 0.81 秒/组
```

### 3. 音乐加速：不要用分档重复 `PlayMusic`，用频道音乐 + pitch

用户实测：用 `MusicSpeedLevel` 分档重复执行 `PlayMusic("ABBB.MP3", ..., pitch)` 会出现音乐重叠。

已在 GDevelop 运行时源码确认安全 API：

```text
gdjs.evtTools.sound.playMusicOnChannel(runtimeScene, "ABBB.aac", 1, true, 70, pitch)
gdjs.evtTools.sound.isMusicOnChannelPlaying(runtimeScene, 1)
gdjs.evtTools.sound.setMusicOnChannelPitch(runtimeScene, 1, pitch)
```

稳定做法：

```text
不用普通 PlayMusic 反复重播。
新增一个 JS 事件每帧计算 targetPitch：
RunSpeed 5.2 -> 1.00x
RunSpeed 11+ -> 约 1.32x
如果频道 1 没在播放：playMusicOnChannel 播放一次
如果频道 1 正在播放：setMusicOnChannelPitch 只改速度/音高
```

示例：

```js
const channel = 1;
const baseSpeed = 5.2;
const runSpeed = Math.max(baseSpeed, runtimeScene.getGame().getVariables().get("RunSpeed").getAsNumber());
const targetPitch = Math.min(1.32, Math.max(1.0, 1 + (runSpeed - baseSpeed) * 0.055));
if (runtimeScene.getVariables().get("GameOver").getAsNumber() === 0) {
  if (!gdjs.evtTools.sound.isMusicOnChannelPlaying(runtimeScene, channel)) {
    gdjs.evtTools.sound.playMusicOnChannel(runtimeScene, "ABBB.aac", channel, true, 70, targetPitch);
  } else {
    gdjs.evtTools.sound.setMusicOnChannelPitch(runtimeScene, channel, targetPitch);
  }
}
```

死亡时已有 `UnloadAllAudio` 可停止频道音乐。不要再添加分档 `PlayMusic` 事件。

### 4. 上一版 12 档定时波动方案（已停用，保留回滚参考）

每 6 秒切换一档，低速与高速交错并逐步抬高峰值：

```text
6.0, 8.8, 6.4, 10.0, 6.8, 11.2,
7.2, 12.0, 7.8, 12.5, 8.2, 13.0
```

音乐继续由频道 1 单实例播放，pitch 公式同步扩大为：

```js
Math.min(1.42, Math.max(1.0, 1 + (runSpeed - 5.2) * 0.060))
```

只修改 `RunSpeed` 档位和频道音乐 pitch，不顺带修改 `GroupGap`、跳跃、碰撞或 Castle 终点锁速。

### 5. 当前音乐节奏同步方案（2026-06-22）

`ABBB.aac` 离线分析结果约为 `108 BPM`。按每 8 拍（约 4.44 秒）统计 RMS 与 onset 强度，生成 38 段速度时间轴：低能量间奏使用约 `6.0~8.0`，高能量段使用约 `11.0~13.0`。

运行时不再依靠 `SpeedTimer` 累加；使用本机 GDevelop runtime 已验证 API：

```js
gdjs.evtTools.sound.getMusicOnChannelPlayingOffset(runtimeScene, 1)
```

每帧按频道 1 的实际播放秒数选择速度段。音乐固定 `1.0x`，避免改变 pitch 后节拍时间轴漂移。`CastleSpeedLocked=1` 时禁止节奏控制器覆盖终点锁速。

旧 12 档事件不删除，但 `SceneJustBegins` 将 `SpeedPhase=-1`，因此全部休眠，便于安全回滚。原 `SpeedTimer` 事件替换为音乐同步 JS 事件。

### 6. 音乐基速叠加随机倍率与木桩安全窗口（2026-06-22）

- 在 38 段 `rhythmSpeeds` 上叠加 `0.6~1.2` 随机倍率，每 4 拍尝试更新一次。
- 随机倍率保存在 `RhythmRandomMultiplier`，拍段保存在 `RhythmRandomStep`。
- 目标速度使用约 0.4 秒平滑靠近，避免普通切段也瞬间跳速。
- 检查 `ObstacleHitbox/Medium/Big`：当碰撞盒位于骑士前缘到半个骑士身宽之间时，冻结倍率和速度变化；离开危险窗口后再更新。
- `CastleSpeedLocked=1` 后停止节奏/随机控制，保留进入终点时的当前速度。

## 必须避免

- 不要为了增加难度去改 `KnightHorse` 跳跃参数，除非用户明确要求“跳矮/跳高”。
- 不要盲写未知音频动作名（例如猜测 `SetMusicPitch`）；先查官方或复用当前项目已验证的 `PlayMusic` 参数。
- 不要只加速不压间距；否则速度增长会被 GroupGap 系数抵消。
- 不要每帧调用 `PlayMusic`；必须用 `MusicSpeedLevel` 门控。

## 回读验证

```text
formal JSON 与 autosave SHA 一致
SceneJustBegins 重置 RunSpeed=6.0、SpeedPhase=-1、GameOver=0
生成代码包含 getMusicOnChannelPlayingOffset、rhythmStarts、rhythmSpeeds
旧 SpeedTimer >= 6 不再进入生成代码
频道音乐固定 pitch=1.0，音频资源为 ABBB.aac
节奏控制器检查 CastleSpeedLocked，不覆盖进入终点时锁住的当前 RunSpeed
生成代码包含 0.6 + Math.random() * 0.6、halfBody、obstacleTooClose
Retry / Double Jump / Collision / Dragon2 事件未被改动
```
