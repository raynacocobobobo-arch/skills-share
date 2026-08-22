# GDevelop 跑酷 JSON：分层重构与屎山清理规则

适用：KnightRunner / Dino 类横版跑酷项目，用户反馈事件表混乱、地面/山/木桩/Retry 互相影响、JSON 里堆了重复事件或临时兜底。

## 1. 先确认权限：分析 ≠ 执行重构

用户贴外部建议、指出问题、让“看看/判断/debug”时，只能先审计并列问题；不要自动重构事件系统。

只有用户明确选择/下令“清理 / 重构 / 按这套改 / 回滚后改”时，才写文件。

## 2. 跑酷事件必须分层

### 世界滚动层 WorldMove
只移动：
- `Ground_A`
- `Ground_B`
- `Mount1`

唯一运行门控：`GameOver = 0`。

禁止混入：
- `NewSprite12`
- `ObstacleHitbox`
- `SpawnGateX`
- `ObstacleAlive`
- Retry / go / re

### 障碍层 ObstacleMove / Spawn / Delete
障碍如果仍采用视觉 + 隐形碰撞体，就继续用：
- `NewSprite12`：视觉木桩
- `ObstacleHitbox`：碰撞与计分状态

不要擅自合并成新对象 `Obstacle`，除非用户明确要求重构对象结构。

推荐变量：
- `ObstacleAlive`：当前是否已有障碍组
- `NextObstacleX`：下一组出生 X
- `LastObstacleX`：上一组出生 X
- `SpawnCooldown` / `SpawnCooldownTimer` / `SpawnCooldownDelay`：离屏后短冷却

生成规则：
- `GameOver = 0`
- `ObstacleAlive = 0`
- `SpawnCooldown = 0`
- `ObstacleHitbox count < 1`
- Create `NewSprite12` at `NextObstacleX`
- Create `ObstacleHitbox` at `NextObstacleX + offset`
- `ObstacleAlive = 1`
- `LastObstacleX = NextObstacleX`
- `NextObstacleX = LastObstacleX + RandomInRange(900, 1100)`

删除规则必须成对：
- 条件：`ObstacleHitbox.X < -200`
- 动作：Delete `NewSprite12` + Delete `ObstacleHitbox` + `ObstacleAlive = 0`

### GameOver 层
只管状态和 UI：
- `GameOver = 1`
- 创建/显示 `go`、`re`
- 设置 `ScoreText`
- Reset `RetryDelayTimer`

不要在 GameOver 层控制地面、山、木桩生成节奏或角色 Y。

### Retry 层
Retry 必须二选一：

1. **ChangeScene 模式（用户已要求/验证时优先）**
   - 条件：`GameOver = 1` + `MouseButtonReleased Left` + `SourisSurObjet(re)`
   - 动作：只 `ChangeScene` 当前场景
   - 不要在 ChangeScene 前堆一整套 reset/delete/timer，都是冗余且容易打架。

2. **原场景硬重置模式**
   - 不用 `ChangeScene`
   - 才需要按顺序清：`GameOver=0`、`Score=0`、`RunSpeed=6`、delete all obstacles/go/re、reset timers、reset spawn variables、ScoreText。

## 3. 清理屎山检查清单

写入前先备份正式 JSON 和 autosave；写入后必须回读两者一致。

可清理项：
- 空 `JsCode` 动作（无 inlineCode、无有效 parameters）
- 不再被事件引用的废场景变量，如旧版 `ObstacleSpawnDelay` / `ObstacleMaxCount` / `SpawnGateX`
- 重复二段跳事件：通常一套是 `['Space']`，另一套是 `['', 'Space']`。用户确认二段跳可用时，只删明显重复的一套；保留已验证更可能有效的正常 `['Space']` 版。
- 混合移动事件：同一个事件同时移动 `Ground_A/B/Mount1` 和 `NewSprite12/ObstacleHitbox` 时，应拆成 WorldMove + ObstacleMove。
- Retry 中“硬重置 + ChangeScene”同时存在时，按当前策略删一边。

禁止清理项：
- 不要动 `KnightHorse` 的 `MettreY` / `SetY` / `SetXY`（清理时也不要新增）。
- 不要碰用户手动验证有效的 `PlayMusic ABBB.MP3`，即使参数看起来脏；除非用户明确说音乐不响并要求修。
- 不要改用户手动调过的 `ObstacleHitbox` collision mask / 坐标，除非用户明确要求。

## 4. 回读验证

至少验证：
- 正式 JSON 与 `.autosave` SHA 一致。
- 无空 `JsCode`。
- 废变量从 `layout.variables` 移除。
- 无混合移动事件。
- 二段跳只剩一套 `SetCanJump + SimulateJumpKey`（或明确保留多套的理由）。
- Retry 只执行当前策略：ChangeScene 或硬重置，不要二者叠加。
- 无 `KnightHorse` Y/XY 事件。
- `PlayMusic ABBB.MP3` 仍存在。
- GDevelop 以项目路径打开。
