# GDevelop 跑酷项目：障碍 / 计分 / Retry / 二段跳修复细节

适用场景：用户上传或要求替换/修复 `KnightRunner_Test.json` 这类 GDevelop 横版跑酷项目，重点涉及二段跳、Retry、障碍生成间距、分数和 GameOver。

## 1. 外部 JSON 与用户描述不一致时

不要只按用户描述汇报“已替换”。必须：

1. 替换前解析上传 JSON。
2. 搜索关键逻辑是否真的存在：
   - `ignoreDefaultControls`
   - `JumpCount`
   - `SetCanJump` / `setCanJump`
   - `SimulateJumpKey` / `simulateJumpKey`
   - `MouseButtonFromTextReleased`
   - `SourisSurObjet(re)` 是否仍在
   - `RunSpeed` 上限表达式
   - `ObstacleSpawnDelay` 范围
   - `NextObstacleX` 范围
3. 如果上传 JSON 和用户文字不一致，先如实说明；用户确认后再直接按描述修。

## 2. 替换文件必须同步 autosave

GDevelop 会从 `.json.autosave` 恢复旧状态。外部 JSON 替换或直改时必须：

1. 关闭 GDevelop。
2. 备份正式文件：`<project>.json.bak_<purpose>_<timestamp>`。
3. 备份 autosave：`<project>.json.autosave.bak_<purpose>_<timestamp>`。
4. 同时写入正式 `.json` 和 `.json.autosave`。
5. 回读两者并比对 SHA。
6. 用参数打开：
   ```bash
   open '/Applications/GDevelop 5.app' --args '/path/to/KnightRunner_Test.json'
   ```
7. `pgrep -fl GDevelop` 验证进程参数包含项目路径。

## 3. 二段跳：事件 ID 不确定时用 JSCode 调 runtime API

GDevelop 官方行为内部 runtime 方法可在本机源码里确认：

`/Applications/GDevelop 5.app/Contents/Resources/GDJS/Runtime-sources/Extensions/PlatformBehavior/platformerobjectruntimebehavior.ts`

关键方法：

- `setCanJump()`
- `simulateJumpKey()`
- `isOnFloor()`
- `ignoreDefaultControls(ignore: boolean)`

如果 JSON 事件动作 ID 不好确认，稳定做法是：

1. `KnightHorse` 的 `PlatformBehavior::PlatformerObjectBehavior` 设置：
   - `ignoreDefaultControls = true`
   - 可关闭字段型 double jump，避免和事件型跳跃叠加：`useRepeatedJump=false`、`allowDoubleJump=false`、最大跳数相关字段设 1。
2. 新增场景变量：`JumpCount = 0`。
3. 每帧检测落地：
   ```js
   const objs = runtimeScene.getObjects('KnightHorse');
   for (const obj of objs) {
     const b = obj.getBehavior('PlatformerObject');
     if (b && b.isOnFloor && b.isOnFloor()) {
       runtimeScene.getVariables().get('JumpCount').setNumber(0);
       break;
     }
   }
   ```
4. `Space just pressed` 或 `KeyFromTextPressed('Space')` 时：
   ```js
   const jumpVar = runtimeScene.getVariables().get('JumpCount');
   const objs = runtimeScene.getObjects('KnightHorse');
   for (const obj of objs) {
     const b = obj.getBehavior('PlatformerObject');
     if (!b) continue;
     if (jumpVar.getAsNumber() < 2) {
       if (b.setCanJump) b.setCanJump();
       if (b.simulateJumpKey) b.simulateJumpKey();
       jumpVar.setNumber(jumpVar.getAsNumber() + 1);
     }
   }
   ```
5. 可保留按住空格续跳事件：`PlatformBehavior::SimulateJumpKey`，条件 `GameOver=0` + `KeyPressed('Space')`。

注意：不要用任何 `SetY` / `SetXY` / `MettreY` / `MettreXY` 修跳跃，角色 Y 交给 Platformer 行为。

## 4. Retry 稳定重置

如果 `re` 图片透明区域/碰撞范围导致点不到，不要依赖：

- `SourisSurObjet(re)`

更稳做法：GameOver 后任意鼠标左键释放触发重置，配合用户可见 `re` 图作为提示：

条件：

- `GameOver = 1`
- `MouseButtonFromTextReleased('Left')`

动作：

- 删除 `go` / `re`
- 删除 `NewSprite12`
- 删除 `ObstacleHitbox`
- `Score = 0`
- `RunSpeed = 6`
- `GameOver = 0`
- `JumpCount = 0`
- `ObstacleSpawnDelay = RandomFloatInRange(1.75, 2.45)`
- `ResetTimer('ObstacleSpawnTimer')`
- `ScoreText = "Score: 0"`
- `NextObstacleX = RandomInRange(1380, 1460)`
- 重新创建开局障碍和 hitbox

另外加 R 键重试便于测试：`GameOver=1` + `KeyFromTextReleased('r')` 触发同一组 reset actions。

## 5. 障碍间距和速度曲线

避免木桩贴脸连续出现：

- 生成间隔：`RandomFloatInRange(1.75, 2.45)`
- X 抖动：`RandomInRange(1380, 1460)`
- 速度曲线：
  ```plain
  RunSpeed = min(8.2, 6 + sqrt(GlobalVariable(Score) / 100) * 0.22)
  ```

开局/Retry 和常规 Spawn 都要统一使用这套范围，不能只改一个地方。

## 6. 回读验证清单

完成后必须验证：

- 正式 `.json` 与 `.autosave` SHA 一致。
- `KnightHorse ignoreDefaultControls=true`。
- `JumpCount` 存在。
- `setCanJump` / `simulateJumpKey` 或对应平台行为事件存在。
- Retry 不再依赖 `SourisSurObjet(re)`。
- `MouseButtonFromTextReleased` 存在。
- R 键 Retry 存在。
- `RunSpeed` 上限为 `8.2`。
- `RandomFloatInRange(1.75, 2.45)` 同时用于开局/Retry 和 Spawn。
- `RandomInRange(1380, 1460)` 同时用于开局/Retry 和 Spawn。
- `Score + 100` 事件仍在。
- 无 `ChangeScene`。
- 无 `KnightHorse` 的 SetY/SetXY/MettreY/MettreXY。
- GDevelop 进程参数含正式项目路径。
