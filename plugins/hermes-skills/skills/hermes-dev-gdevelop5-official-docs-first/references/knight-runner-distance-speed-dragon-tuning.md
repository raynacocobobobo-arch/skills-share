# KnightRunner_Test：距离倒计时、波动速度与红龙安全高度

## 触发场景

用户要求：

- 记分系统改成距离倒计时，例如 `666M`、每秒减少固定米数。
- 已加入 `m.png` 单位图片、`pricess.png` 公主/标题图片。
- 游戏速度不要单调匀加速，要有明显加速和减速，音乐跟着变化。
- 红龙不能碰到骑士二段跳最高点，也不能压到公主、数字、M。

## 核心原则

1. **不要把 `Score` 改成倒计时。**  
   `GlobalVariable(Score)` 继续做内部进度/难度依据，避免 RunSpeed、障碍概率、复杂障碍门槛反向失效。

2. **新增/使用 `GlobalVariable(DistanceLeft)` 做显示。**  
   开局设置目标距离，当前值：

   ```text
   DistanceLeft = 500
   ```

   不再用 `CompareTimer + ResetTimer`，因为每次重置会丢失超过 1 秒的帧间零头。当前稳定做法使用场景变量 `DistanceAccumulator` 累加真实帧时间：

   ```text
   GameOver = 0
   DistanceAccumulator += elapsed seconds
   completedSeconds = floor(DistanceAccumulator)
   → DistanceLeft -= completedSeconds * 4
   → DistanceAccumulator -= completedSeconds
   ```

   注意：修改倒计时减数时，只改非 `SceneJustBegins` 的 `DistanceTimer` 事件；不要误把开局 `DistanceLeft = 666/999` 初始化一起替换。

3. **图片显示改读 `DistanceLeft`，只显示 3 位数字。**

   当前 UI 结构：

   ```text
   pricess + 3 个 ScoreDigit + M
   ```

   三个 `ScoreDigit` 实例按 X 排序，`DigitIndex` 必须分别是 `0/1/2`。用户手动复制实例后可能三个都还是 `2`，必须回读修正。

4. **速度用 `SpeedPhase` 做大幅波动，不用单调 `RunSpeed += x`。**

   场景变量：

   ```text
   SpeedPhase = 0
   ```

   开局：

   ```text
   RunSpeed = 6.6
   ResetTimer("SpeedTimer")
   ```

   每 8 秒：

   ```text
   SpeedPhase += 1
   RunSpeed = Choose(Variable(SpeedPhase) % 12,
     6.6, 8.1, 7.0, 9.0, 7.4, 10.2,
     8.0, 11.3, 8.7, 10.8, 9.2, 11.5)
   ResetTimer("SpeedTimer")
   ```

   这会产生“加速—回落—再冲刺”的节奏。音乐无需单独重写，已有 BGM JS 使用 `setMusicOnChannelPitch` 跟随 `RunSpeed`。

5. **红龙安全高度优先改龙，不改骑士跳跃。**

   用户明确纠正过：当“骑士二段跳最高不能碰龙”时，应该调 Dragon2 高度，而不是调 `KnightHorse` 跳跃高度，除非用户明确要求改跳跃手感。

   当前稳定参考值：

   ```text
   右→左：Dragon2 Y = 90，zOrder = 10000
   左→右：Dragon2 Y = 70，zOrder = 9（在骑士后面）
   回右侧：Dragon2 Y = 90，zOrder = 10000
   ```

   如果用户说“龙太低”，增大 Y；如果“会碰二段跳最高点”，减小 Y。每次小步 20~40px 调整。

## GDevelop 打开状态/Autosave 避坑

- GDevelop 打开时可能用内存状态把 `.autosave` 写回旧值，导致你刚写入正式 JSON 后被覆盖。
- 稳定流程：

```text
1. 读取 formal/autosave，选 mtime 最新为源。
2. 备份 formal/autosave。
3. 修改并写入 formal/autosave。
4. 退出 GDevelop。
5. 确认进程结束；如仍在运行再终止。
6. 重新写入同一份 desired JSON 到 formal/autosave。
7. 回读 SHA、关键事件值。
8. 重新打开 GDevelop。
```

## BestScoreM / flag 历史最高纪录点（已验证修法）

当用户要求“best score 记录 / flag 插在历史最高纪录地面上 / 后续更远要刷新纪录”时：

1. 不要用裸 `localStorage` 直接读写。应使用 GDevelop 官方运行时 Storage API。官方源码位于本机：

```text
/Applications/GDevelop 5.app/Contents/Resources/GDJS/Runtime-sources/events-tools/storagetools.ts
```

已确认函数签名：

```js
gdjs.evtTools.storage.writeNumberInJSONFile(name, elementPath, value)
gdjs.evtTools.storage.readNumberFromJSONFile(name, elementPath, instanceContainer, variable)
```

2. 本项目记录值使用：

```text
GlobalVariable(BestScoreM) = 500 - GlobalVariable(DistanceLeft)
```

即“已跑过米数”，不是剩余米数。

3. 场景开始时用 Storage 读取旧纪录，同时锁定本局开始时的纪录点：

```js
gdjs.evtTools.storage.readNumberFromJSONFile("KnightRunner", "BestScoreM", runtimeScene, bestVariable);
runStartBestVariable.setNumber(bestVariable.getAsNumber());
```

4. 运行中只要超过旧纪录，立即刷新并写入 Storage。注意不要加 `!gameOver` 限制，避免死亡同帧/事件顺序导致最终距离没写入：

```js
if (progressMeters > bestMeters) {
  bestMeters = progressMeters;
  bestVariable.setNumber(bestMeters);
  gdjs.evtTools.storage.writeNumberInJSONFile("KnightRunner", "BestScoreM", bestMeters);
}
```

5. flag 不能用“每帧按当前记录重新定位”的屏幕提示逻辑，也不能太早生成。正确逻辑：

```text
RunStartBestScoreM = 本局开始时的旧纪录
RunStartBestScoreM > 30 才允许生成 flag，避免小纪录一开局就显示
当 DistanceLeft <= 666 - RunStartBestScoreM + 30 时：flag X=1400, Y=地面位置, FlagSpawned=1
FlagSpawned=1 且 GameOver=0 时：flag X -= RunSpeed * 60 * TimeDelta()
flag X < -220 时隐藏
```

这样 flag 是插在历史纪录地面上的物体，会跟地面同速移动并消失；本局刷新的新纪录从下一局开始生效。

## 回读验证清单

```text
formal JSON 与 autosave SHA 一致
SceneJustBegins 包含 DistanceLeft 初始化和 ResetTimer("DistanceTimer") / ResetTimer("SpeedTimer")
非开局 DistanceTimer 事件只包含每秒减数和 ResetTimer
SpeedPhase 场景变量存在，SpeedTimer 事件每 8 秒切 RunSpeed 曲线
BGM JS 仍包含 setMusicOnChannelPitch，未改回重复 PlayMusic
ScoreDigit 三个实例 DigitIndex = 0/1/2
M/pricess 的 zOrder 高于 Dragon2
Dragon2 三个起飞事件分别设置 Y 和 zOrder
KnightHorse PlatformerObject 参数未被修改
```
