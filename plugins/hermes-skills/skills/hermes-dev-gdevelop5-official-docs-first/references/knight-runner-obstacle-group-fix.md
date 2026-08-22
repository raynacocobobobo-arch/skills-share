# KnightRunner_Test：障碍组生成修复与 JSON 直改坑

适用：GDevelop 5 横版跑酷项目，视觉障碍 `NewSprite12` + 碰撞盒 `ObstacleHitbox`，按 Chrome Dino 风格生成“障碍组”。

## 官方依据先行

本类任务至少需要本地官方文档缓存中有这些条目：

- Events / Standard events：确认事件由条件和动作构成，并按事件表顺序执行。
- Objects / Objects Reference：确认对象与多实例关系、创建/删除/移动动作。
- Variables：确认全局变量、场景变量、对象变量作用域。
- Expressions：确认 `RandomInRange`、`GlobalVariable()`、`Variable()`、对象坐标表达式。
- For Each object event：涉及逐个处理对象实例时使用，避免多实例选择歧义。

缓存文件默认：

```text
references/GDEVELOP_OFFICIAL_DOC_CACHE.md
```

## 本次形成的稳定修法

### 1. 生成门控必须有“距离/阈值”，不能只看数量

错误模式：

```text
GameOver = 0
ObstacleCount < MaxObstacles
→ 直接生成障碍组
```

这会导致开局或同一帧连续填满 3 个木桩，`GroupGap` 实际失效。

推荐门控如下。本项目使用 `ObstacleState`（0=等待，1=本帧生成），不要再添加同义变量：

```text
ObstacleState = 0

GameOver = 0
ObstacleCount = 0
→ ObstacleState = 1
→ GroupStartX = 1400

GameOver = 0
ObstacleCount > 0
ObstacleCount < MaxObstacles
GroupLastX < 1400
→ ObstacleState = 1
→ GroupStartX = GroupLastX + GroupGap
```

后续所有 Roll / GroupSize / Create / GroupGap / LastPattern 事件都必须使用同一个门控条件：

```text
ObstacleState = 1
```

### 2. `GroupLastX` 要跟随世界移动

如果 `NewSprite12` 和 `ObstacleHitbox` 每帧左移，但 `GroupLastX` 不动，下一组位置会基于旧坐标，组间距会漂。

应在障碍移动事件后追加：

```text
GameOver = 0
ObstacleCount > 0
→ GroupLastX -= GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

### 3. 多实例对象不要用 `NewSprite12.X()` 猜当前新建实例

风险模式：

```text
Create NewSprite12 at GroupStartX + RandomInRange(...)
Create ObstacleHitbox at NewSprite12.X() + 39
GroupLastX = NewSprite12.X()
```

`NewSprite12` 有多个实例时，表达式依赖对象选择上下文，容易歧义。

稳定模式：先把目标 X 写入场景变量，再用该变量创建视觉与 hitbox：

```text
GroupLastX = GroupStartX + RandomInRange(460,560)
Create NewSprite12 at GroupLastX, 565
Create ObstacleHitbox at GroupLastX + 39, 594
```

### 4. `ScoreText` 不要置空

错误模式：

```text
ScoreText = ""
```

稳定模式：

```text
ScoreText = "Score: " + ToString(GlobalVariable(Score))
```

GameOver 时再单独显示：

```text
"GAME OVER  Score: " + ToString(GlobalVariable(Score))
```

### 5. Retry 残留要和主 Retry 区分

使用当前官方 JSON 内部类型的 Retry 形态：

```text
GameOver = 1
IsCursorOnObject(re)
MouseButtonFromTextReleased("Left")
→ Scene("未命名场景")
```

疑似残留：

```text
MouseButtonFromTextPressed(go, "Left")
→ Scene("未命名场景")
```

如果用户明确要求清理，可删除 `go` 触发的 Retry 残留；不要动主 Retry。

新增教训：`MouseButtonFromTextReleased` 是当前官方 Mouse and touch Reference 给出的内部类型，
不是兼容补丁；旧式 `MouseButtonReleased` 才不应继续复制。不要额外添加硬编码
`CursorX/CursorY` 坐标范围 fallback。Retry 保留一个对象命中版本即可：

```text
GameOver = 1
IsCursorOnObject(re)
MouseButtonFromTextReleased("Left")
→ Scene("未命名场景")
```

## 2026-06 更新：Chrome Dino 式障碍组精确落地参数

当用户明确要求“参考 Chrome Dino，不要单个障碍 + 固定随机间距，改成障碍组”时，当前项目稳定做法是：

```text
Score < 1500：GroupSize = 1
1500 <= Score < 4000：Roll 1~100，<=70 为 1，>70 为 2
Score >= 4000：Roll 1~100，<=55 为 1，56~90 为 2，>90 为 3
```

组内位置必须用场景变量承接，避免多实例 `NewSprite12.X()` 歧义：

```text
第 1 个：X = GroupStartX
GroupSize=2：第 2 个 X = GroupStartX + RandomInRange(460,560)
GroupSize=3：第 2 个 X = GroupStartX + RandomInRange(460,540)
             第 3 个 X = 第 2 个 X + RandomInRange(600,720)
```

如果用户指定“当前对象 NewSprite12 是木桩视觉，ObstacleHitbox 是碰撞盒”，应按指定对象生成，不要顺手保留此前的中/大木桩随机变体参与新逻辑；中/大对象可以保留定义和清理事件，但新生成 block 只创建 `NewSprite12 + ObstacleHitbox`。每个木桩对应一个 hitbox：

```text
NewSprite12.Y = 565
ObstacleHitbox.X = 木桩X + 39
ObstacleHitbox.Y = 594
```

组后距离按速度和组宽放大：

```text
GroupGap = RandomInRange(430 + GlobalVariable(RunSpeed) * 38,
                         620 + GlobalVariable(RunSpeed) * 55)
GroupSize=2：GroupGap += RandomInRange(80,160)
GroupSize=3：GroupGap += RandomInRange(180,300)
```

连续重复限制的稳定事件顺序：先按分数和 Roll 决定候选 `GroupSize`，再按屏幕内数量上限修正，再在 `SamePatternCount >= 2 && GroupSize == LastPattern` 时强制换另一种允许的组大小，最后再次执行屏幕内数量上限修正，然后才更新 `SamePatternCount`。屏幕内最多 3 个木桩时，`MaxObstacles=3`，且：

```text
ObstacleCount >= 2 且 GroupSize > 1 → GroupSize = 1
ObstacleCount = 1 且 GroupSize > 2 → GroupSize = 2
```

不要保留“短间距 Roll 小概率贴脸”事件；这会违背“不要连续两个木桩贴在一起”。

## JSON 直改定位坑

修复生成 block 时，不要从第一个出现 `GroupStartX` 的事件盲目作为替换起点。开局初始化事件也可能包含 `GroupStartX`，如果误替换，会删掉 `SceneJustBegins` 开局事件，导致音乐、Score、RunSpeed、删除旧障碍等初始化消失。

安全定位流程：

1. 找到障碍移动事件：同时包含 `MettreX`、`NewSprite12`、`ObstacleHitbox`、`GlobalVariable(RunSpeed)`。
2. 在该事件后插入 `GroupLastX -= ...`。
3. 只在障碍移动事件之后，寻找生成 block 的起点。
4. 生成 block 终点可用 `LastPattern = Variable(GroupSize)` 作为边界。
5. 替换后必须回读验证开局事件仍然存在。

## 回读验证清单

写入 formal JSON 和 `.autosave` 后必须验证：

```text
formal JSON 与 autosave SHA 一致
第 0 条事件条件包含 SceneJustBegins
Ground_A / Ground_B / Mount1 事件仍存在
NewSprite12 / ObstacleHitbox 移动事件仍存在
存在 GroupLastX -= GlobalVariable(RunSpeed) * 60 * TimeDelta()
旧障碍变量 NextObstacleX / LastObstacleX / ObstacleGapMin / ObstacleGapMax / ObstacleGapRoll 已清理或无引用
门控变量只保留一套（当前项目为 ObstacleState）
ScoreText 不再被设置为空字符串
事件中不再出现 NewSprite12.X()
Retry 使用 IsCursorOnObject + MouseButtonFromTextReleased，不存在 go 触发残留
不存在 KnightHorse 的 MettreY / SetY / SetXY
碰撞仍为 KnightHorse collision ObstacleHitbox，不是 NewSprite12
```

## 备份规则

- 修改前同时备份 `.json` 和 `.json.autosave`。
- 如中途发现误删开局事件，先用刚才备份恢复，再做 v2 patch；不要在坏状态上继续堆补丁。
