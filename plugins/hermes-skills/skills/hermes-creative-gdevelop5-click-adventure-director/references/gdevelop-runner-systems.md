# GDevelop 5 横版自动跑酷系统落地笔记

适用：Chrome Dino / 骑士骑马跑酷类原型，在已有 `KnightHorse`、循环地面、视觉背景的项目中继续加障碍、分数、动态速度。

## 1. 障碍系统：生成、移动、删除

对象示例：`NewSprite12`（树桩/障碍物）。

原则：
- 障碍物是视觉障碍，不加 `Platformer`、`Platform`、`Physics` 行为。
- 障碍移动速度必须与地面一致，避免“滑地”。
- 同屏数量控制在 2～3 个。
- 障碍由事件生成，不建议保留编辑器里手动摆放的样板实例。

事件结构：

```text
EVT_InitObstacle
Conditions:
- At the beginning of the scene
Actions:
- Set scene variable ObstacleSpawnDelay = RandomFloatInRange(0.8, 2.4)
- Reset timer "ObstacleSpawnTimer"
```

```text
EVT_SpawnObstacle
Conditions:
- Timer "ObstacleSpawnTimer" > Variable(ObstacleSpawnDelay)
- Number of NewSprite12 objects < Variable(ObstacleMaxCount)
Actions:
- Create NewSprite12 at X = 1400, Y = ObstacleTopY
- Set Z order of NewSprite12 = 5
- Set scene variable ObstacleSpawnDelay = RandomFloatInRange(0.8, 2.4)
- Reset timer "ObstacleSpawnTimer"
```

```text
EVT_MoveObstacle
Conditions:
- None
Actions:
- Change X position of NewSprite12: subtract GlobalVariable(RunSpeed)
```

```text
EVT_DeleteObstacle
Conditions:
- X position of NewSprite12 < -200
Actions:
- Delete NewSprite12
```

## 2. 贴地位置：不要把地面线当 top-left Y

GDevelop Sprite 的位置通常是对象左上角，不是脚底。

如果用户说“地面高度 Y=600”，树桩应底部贴在 600，而不是对象左上角放在 600。

计算方式：

```text
ObstacleTopY = GroundLineY - ObstacleDisplayedHeight
```

示例：`ABC.png` 树桩原图 `267×112`，有效像素到底部；若显示尺寸为 `211×89`，地面线为 `Y=600`：

```text
ObstacleTopY = 600 - 89 = 511
```

因此生成坐标应是：

```text
Create NewSprite12 at X = 1400, Y = 511
```

验证方法：读取 PNG alpha 边界，找到有效像素 bbox；如果有效底部就是图片底部，直接用显示高度修正；如果底部有透明边，则用 bbox 缩放后的有效底部来修正。

## 3. 生成节奏不要太平均

`1.0 ~ 2.0 秒` 容易像节拍器。跑酷障碍推荐更松散：

```text
ObstacleSpawnDelay = RandomFloatInRange(0.8, 2.4)
```

如果后续加难度曲线，可随分数略微压缩上限，但仍保持随机波动。

## 4. 记分系统

全局变量：

```text
GlobalVariable(Score) = 0
```

60fps 适配增长：

```text
Score += TimeDelta() * 60
```

显示：创建 `ScoreText` 文本对象，放 UI 左上角，例如：

```text
X = 30
Y = 30
ZOrder = 100
```

每帧更新：

```text
Set text of ScoreText = "Score: " + ToString(Round(GlobalVariable(Score)))
```

## 5. 动态速度曲线

全局变量：

```text
GlobalVariable(RunSpeed) = 6
```

推荐平滑且封顶的曲线：

```text
RunSpeed = min(13, 6 + sqrt(GlobalVariable(Score)) * 0.2)
```

特点：
- 初始速度 6。
- 前期逐渐加速。
- 后期不会爆炸。
- 最高速度 13。

地面和障碍统一使用：

```text
Ground_A.X -= GlobalVariable(RunSpeed)
Ground_B.X -= GlobalVariable(RunSpeed)
NewSprite12.X -= GlobalVariable(RunSpeed)
```

## 6. 与既有系统关系

- `KnightHorse` 仍只固定 X，不写任何锁 Y 事件。
- `Ground_A / Ground_B` 是视觉滚动层，只改 X。
- `Ground_Physics` 是透明固定碰撞层，不移动。
- `Mount1` 等远景层可保留独立慢速视差，例如 `-2` 或 `RunSpeed / 3`，不要和近景地面同速。

## 7. 回读验证清单

完成后至少验证：

```text
NewSprite12 exists = true
NewSprite12 behaviors = []
ScoreText exists = true
Global variables include Score, RunSpeed
Scene variables include ObstacleSpawnDelay, ObstacleMaxCount
Obstacle spawn Y = GroundLineY - displayed obstacle height
Ground_A/B movement uses RunSpeed
NewSprite12 movement uses same RunSpeed
KnightHorse has no SetY / SetXY / Y() lock events
GDevelop can reopen project
```
