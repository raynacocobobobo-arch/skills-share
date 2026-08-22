# KnightRunner_Test：Game Over 结算 UI、Best 纪录与地面 Flag 记录点

适用：用户新增/调整 `go`、`re`、`Best`、结尾 `M`、结尾 3 个 `ScoreDigit`、`flag`，要求它们只在 Game Over 或历史记录点出现。

## 官方/项目依据

- GDevelop 事件系统：用条件筛选状态，动作只处理当前状态下的对象。
- 对象实例：同一个对象可有多个实例，必须用对象变量区分顶部倒计时数字与结算数字。
- 变量作用域：`DistanceLeft` 是全局倒计时；`BestScoreM` 是全局历史最好成绩；本局开始时要用场景变量锁定旧纪录。
- 本项目已验证 JSON 内部类型：`ModVarGlobal` / `VarGlobal`、`ModVarScene` / `VarScene`、`MettreX` / `MettreY`、`PosX`、`BuiltinCommonInstructions::JsCode`。

## 2026-06 补充：flag 赛道记录点与 m1 死亡贴地体感修正

### flag 应是真正赛道记录点，不是临近提示点

实测用户反馈“flag 还是不对”后，稳定方案不是“快到纪录前再突然生成”，而是：开局先隐藏，等官方 Storage 读取出的 `RunStartBestScoreM > 0` 后，立刻把 flag 放到赛道上对应历史纪录距离的位置，然后只随地面左移。

当前项目体感通过参数：

```text
SceneJustBegins：flag.X = -2000, flag.Y = 466, FlagSpawned = 0
运行中：GameOver = 0 && FlagSpawned = 0 && RunStartBestScoreM > 0
→ flag.X = max(1500, 297 + Variable(RunStartBestScoreM) * 105)
→ flag.Y = 466
→ FlagSpawned = 1

GameOver = 0 && FlagSpawned = 1
→ flag.X -= GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

不要再使用 `DistanceLeft <= 666 - RunStartBestScoreM + N` 的临近触发方式；它更像屏幕提示点，而且在当前速度下容易“不显示/出现时机不对”。

### m1 死亡动画：不要只按外框贴底，要按用户体感下压

用户反馈“m1 死亡时还是高，离地面大概还有 retry 按键实体高度的 1/2”。原因是 `m6.png` 透明边很多，按对象外框或 alpha bbox 计算仍会显得高。

已验证体感通过参数：

```text
m1.Y = 472
m1.zOrder = 40000
```

死亡碰撞事件（普通/中/大 hitbox）都要同步设置：

```text
m1 X = 252
m1 Y = 472
m1 zOrder = 40000
KnightHorse X/Y = -2000
```

旧值 `m1.Y=404`（外框贴木桩底部）和 `m1.Y=442`（alpha 可见底部贴木桩底部）都被用户实测判定仍偏高，不要再回退。

m1 X = 252
m1 Y = 472
m1 zOrder = 40000
KnightHorse X/Y = -2000
```

如果用户继续说“还是高/低”，优先按用户预览体感做 20~50px 微调，不要反复引用外框公式。

## 稳定做法

### 1. 可编辑但运行时隐藏的 Game Over UI

如果用户要在编辑器里拖 `go/re/Best/M/结尾数字`，不要死亡时 `Create`，也不要开局 `Delete`。稳定做法：

1. 把这些对象作为场景实例保留，方便用户拖位置。
2. 给结算对象保存 `HomeX/HomeY` 初始变量。
3. `SceneJustBegins` 时移动到屏幕外：`X=-2000,Y=-2000`。
4. Game Over 时移动回 `HomeX/HomeY`。

注意：如果用户刚在编辑器里调过位置，必须先保存并以最新正式 JSON 为源；autosave 可能旧。不要覆盖用户刚拖的位置。

### 2. 区分顶部倒计时数字和结尾 Best 数字

同一个 `ScoreDigit` 对象有两组实例：

- 顶部倒计时：`DigitRole = "distance"`，`DigitIndex = 0/1/2`。
- 结尾 Best：`DigitRole = "best"`，按 X 从左到右设置 `DigitIndex = 0/1/2`，并保存 `HomeX/HomeY`。

JS 更新时必须按 `DigitRole` 分流：

```js
if (role === "best") {
  setHomeOrHidden(digitObject, gameOver);
  digitObject.setAnimationIndex(Number(paddedBest[index]));
} else {
  digitObject.setAnimationIndex(Number(paddedDistance[index]));
}
```

结尾 `M` 也要标记 `DigitRole="best"` 并只在 Game Over 时显示；顶部 `M` 保持常显。

### 3. BestScoreM 不要只在 Game Over UI JS 里顺手更新

已踩坑：如果 `BestScoreM` 只在 Game Over UI 的 JS 里根据 `gameOver` 刷新，用户实测会出现“旗子只记录第一次，后面更远不更新”。

稳定做法：独立成标准事件，游戏运行中实时刷新历史最佳：

```text
GameOver = 0
DistanceLeft < 666 - GlobalVariable(BestScoreM)
→ BestScoreM = 666 - GlobalVariable(DistanceLeft)
```

含义：`BestScoreM` 是“已跑过的米数”，不是剩余米数。比如剩 `500M`，成绩是 `166M`。

不要在 `SceneJustBegins` 重置 `BestScoreM`；它是跨 Retry/重开场景保留的历史纪录。

### 4. Flag 是地面记录点，不是屏幕提示 UI

用户纠正：“旗子应该插在最高历史记录地面上，然后跟着地面移动并消失。”

错误做法：每帧根据 `bestMeters-currentMeters` 重新计算屏幕 X，这会像 UI 提示点，不像插在地面上的物体。

另一个容易被用户判定“不对”的做法：临近记录点时才把 flag 突然从右侧生成到屏幕边缘。这更像提示牌，不像从开局就存在于赛道某个里程碑的实体。

稳定做法：

1. 开局读取旧纪录到场景变量，锁定本局要追的历史点：

```text
SceneJustBegins
→ RunStartBestScoreM = GlobalVariable(BestScoreM) 或官方 Storage 读出的 BestScoreM
→ FlagSpawned = 0
→ flag 先移到 -2000, 466，等待记录读完
```

2. 只要 `RunStartBestScoreM > 0` 且 `FlagSpawned = 0`，立刻把 flag 放到赛道记录点，而不是等玩家临近：

```text
GameOver = 0
FlagSpawned = 0
RunStartBestScoreM > 0
→ flag.X = max(1500, 297 + Variable(RunStartBestScoreM) * 105)
→ flag.Y = 用户摆放的地面 Y（当前为 466）
→ FlagSpawned = 1
```

`105` 是当前项目的体感比例，让历史纪录点从开局就作为远处赛道物存在并随地面移入屏幕；不是官方常量。若用户反馈太早/太晚，调这个系数或最小 X，不要改回“临近生成”。

3. 出现后 flag 只跟地面同速移动，不再重算位置：

```text
GameOver = 0
FlagSpawned = 1
→ flag.X -= GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

4. 出屏隐藏：

```text
FlagSpawned = 1
flag.X < -220 或 -260
→ flag.X = -2000
→ flag.Y = -2000
```

5. Game Over 碰撞事件里也可追加隐藏 `flag`，避免它残留在结算画面。

Storage 读取可能不是同一帧完成；flag 放置事件必须允许在后续帧 `RunStartBestScoreM` 变为正数时再触发。

## 调位置注意

- `re` 居中可以用用户当前按钮宽度估算：若按钮视觉宽约 `169`，1280 屏水平居中 X 约 `(1280-169)/2 = 556`。
- `flag.Y` 以用户在编辑器里摆的地面位置为准；不要随意改高度。
- 若用户继续拖 `Best/re/flag`，下次应重新读取实例当前位置并更新 `HomeX/HomeY` 或 flag 的地面 Y。

## 回读验证清单

```text
正式 JSON 与 autosave SHA 一致
BestScoreM 是 global number，SceneJustBegins 不重置它
SceneJustBegins 存在 RunStartBestScoreM = GlobalVariable(BestScoreM)
存在独立标准事件：DistanceLeft < 666 - GlobalVariable(BestScoreM) → BestScoreM = 666 - DistanceLeft
顶部 ScoreDigit 为 DigitRole=distance
结尾 3 个 ScoreDigit 为 DigitRole=best 且 DigitIndex=0/1/2
结尾 M 为 DigitRole=best
flag 开局隐藏
flag spawn 使用 RunStartBestScoreM，不使用动态 BestScoreM
flag 出现后只有 RunSpeed*60*TimeDelta 左移
旧的“Best record flag marker on the track” JS 不再存在
```
