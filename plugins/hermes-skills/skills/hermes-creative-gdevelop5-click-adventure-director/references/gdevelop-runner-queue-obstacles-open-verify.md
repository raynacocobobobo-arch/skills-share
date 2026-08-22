# GDevelop 跑酷 JSON 调试：三木桩队列、手感调参、打开验证

本参考来自 KnightRunner_Test.json 调试。用于后续同类 GDevelop 5 横版跑酷项目，避免再次把事件写成屎山或误判项目已打开。

## 1. 用户反馈/工作流硬约束

- 用户说“Retry 我做好了”后，Retry 逻辑视为用户手动确认有效模块：后续不要再清理、重构、替换 Retry 条件/动作，除非用户明确点名改 Retry。
- 用户只是转述建议或分析问题，不等于授权重构。涉及结构性改动（例如把 `NewSprite12 + ObstacleHitbox` 合成单对象、重写生成系统）必须先确认。
- 不能删“看起来重复但用户已验证有效”的兼容事件。二段跳里 `KeyPressed:["Space"]` 与 `KeyPressed:["", "Space"]` 可能一个是 GDevelop 当前 JSON 兼容写法，清理前必须保留/对照备份，不要凭肉眼判定重复。
- 每次写 JSON 前：优先保存 GUI 当前改动或以最新可解析 autosave 为底稿，避免覆盖用户在 GDevelop 里刚手动修好的事件。
- 写入后同步 formal JSON 与 `.autosave`，并 readback 验证；但不要把“JSON 中存在事件”说成“预览已验证”。

## 2. GDevelop 项目打开验证

本项目/同类项目上，`open -n GDevelop --args <json>` 可能让进程参数里显示项目路径，但 GDevelop 实际空开；`open -a GDevelop <json>` 也可能空开，因为 app 未注册 JSON 文档类型。

可靠验证方式：用 System Events 读窗口/Window 菜单标题，确认出现：

```text
GDevelop 5 - /path/to/project.json - Your computer
```

不要只用 `pgrep -fl 'GDevelop 5'` 的进程参数判断“已带项目路径打开”。进程参数只能作为弱信号。

## 3. 三木桩队列系统（Dino 类）

适用：视觉木桩 `NewSprite12` + 碰撞体 `ObstacleHitbox` 分离，但要求成对生成/移动/删除。

场景变量：

```text
MaxObstacles = 3
ObstacleCount = 0
LastObstacleX = 0
NextObstacleX = 1400
ObstacleGapMin = 650
ObstacleGapMax = 1100
ObstacleGapRoll = 0
```

核心规则：

```text
GameOver = 0
ObstacleCount < MaxObstacles
```

生成动作：

```text
Create NewSprite12 at X = NextObstacleX, Y = 565
Create ObstacleHitbox at X = NextObstacleX + 39, Y = 594
ObstacleHitbox.Scored = 0
ObstacleCount += 1
LastObstacleX = NextObstacleX
```

移动动作必须统一：

```text
NewSprite12.X -= RunSpeed * 60 * TimeDelta()
ObstacleHitbox.X -= RunSpeed * 60 * TimeDelta()
LastObstacleX -= RunSpeed * 60 * TimeDelta()
```

删除动作：视觉和碰撞体可以分别离屏删除，但只有 Hitbox 删除时递减队列计数：

```text
NewSprite12.X < -240 -> Delete NewSprite12
ObstacleHitbox.X < -200 -> Delete ObstacleHitbox; ObstacleCount = max(0, ObstacleCount - 1)
```

## 4. 避免“太平均”的伪随机节奏

不要只用固定 `RandomInRange(ObstacleGapMin, ObstacleGapMax)`，体感会像节拍器。推荐先 roll，再分段：

```text
ObstacleGapRoll = RandomInRange(1, 100)

70%: NextObstacleX = LastObstacleX + RandomInRange(620, 880)
20%: NextObstacleX = LastObstacleX + RandomInRange(1050, 1450)
10%: NextObstacleX = LastObstacleX + RandomInRange(500, 620)
```

这样形成“普通 / 长空档 / 紧张”的节奏，而不是平均刷怪。

## 5. 速度与跳跃的数学校验

如果马的碰撞框大，速度过慢会导致单跳横向位移不足，玩家感觉“不二段跳一定碰撞”。先用跳跃滞空估算：

```text
airtime ≈ 2 * jumpSpeed / gravity
horizontal_pass ≈ RunSpeed * 60 * airtime
```

本项目已知：

```text
jumpSpeed = 780
gravity = 1320
airtime ≈ 1.18s
```

速度曲线可用：

```text
RunSpeed = min(8.4, 6.6 + sqrt(GlobalVariable(Score) / 100) * 0.18)
```

对应上限横向通过距离约：

```text
8.4 * 60 * 1.18 ≈ 596px
```

比旧 `min(6.5, 5.2 + ...)` 的约 461px 更适合大马碰撞框。

## 6. 清理/验证清单

- Retry 主事件保留，且无“硬重置一遍 + ChangeScene 一遍”的混合屎山。
- 二段跳兼容事件保留：`SetCanJump + SimulateJumpKey`，不要随便删 `KeyPressed:["", "Space"]` 版本。
- 不写任何 `KnightHorse MettreY / SetY / SetXY`。
- 音乐 `PlayMusic ABBB.MP3` 保留。
- `Ground_A/Ground_B/Mount1` 世界滚动只看 `GameOver = 0`，不依赖木桩变量。
- `NewSprite12` 与 `ObstacleHitbox` 生成、移动同步；删除时只有 Hitbox 负责 `ObstacleCount -= 1`。
- 读回 formal JSON 与 autosave SHA 一致；打开验证用窗口标题，不用进程参数冒充。