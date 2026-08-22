# KnightRunner_Test：Game Over 结算 UI / Best Record / Flag 记录点

适用：用户在 GDevelop 场景里手动新增或复制 `go`、`re`、`Best`、`M`、`ScoreDigit`、`flag` 等 UI/标记实例后，要求它们只在死亡/结算或历史记录点出现。

## 核心原则

- 用户刚在编辑器里加的对象/实例，优先从最新正式 JSON 或 autosave 读取，避免覆盖用户拖好的位置。
- 对用户新增的视觉资源（例如 `Best`、结尾 `M`、`flag`）默认不改资源、不改尺寸、不替换图片，只加变量和事件逻辑。
- 如果不确定隐藏/显示动作的 JSON 内部类型，不要硬写新动作；本项目稳定做法是把对象移到屏幕外 `(-2000, -2000)` 隐藏，显示时移回实例记录的 `HomeX/HomeY`。
- 多个同名 `ScoreDigit` / `M` 实例必须用对象变量区分用途，不能只按对象名全量更新。

## 已验证对象分工

```text
顶部倒计时：
- ScoreDigit，DigitRole = "distance"，DigitIndex = 0/1/2
- M，DigitRole = "distance"

Game Over 结算：
- go
- re
- Best
- 结尾 M，DigitRole = "best"
- 结尾 3 个 ScoreDigit，DigitRole = "best"，DigitIndex = 0/1/2

赛道历史记录点：
- flag
```

## 实例变量约定

对需要隐藏/显示的位置敏感对象写入：

```text
HomeX = 当前编辑器中的 X
HomeY = 当前编辑器中的 Y
```

对同名数字/单位写入：

```text
DigitRole = "distance" 或 "best"
DigitIndex = 0/1/2
```

这样用户之后在编辑器里拖位置时，下一次修改应先回读当前位置并同步 `HomeX/HomeY`，不要用旧硬编码位置覆盖。

## Best record 语义

当前项目倒计时为 `DistanceLeft`，从 `666M` 递减。结尾 best record 不显示剩余米数，而显示“本局已跑过米数”：

```text
progressMeters = 666 - DistanceLeft
BestScoreM = max(BestScoreM, progressMeters)
```

`BestScoreM` 是全局变量，不在 `SceneJustBegins` 重置。Retry 重载场景后仍保留，作为历史最好成绩。

## Game Over 显示逻辑

运行中：

```text
go/re/Best/结尾M/结尾3个ScoreDigit → (-2000, -2000)
```

死亡后 `GameOver = 1`：

```text
回到各自 HomeX/HomeY
结尾3个ScoreDigit 显示 paddedBest = String(BestScoreM).padStart(3, "0")
```

顶部倒计时的 `ScoreDigit/M` 不隐藏，继续按 `DistanceLeft` 显示。

## re 居中

如果用户说 Retry 不居中，本项目 1280 宽画布、`re` 视觉宽约 169px，水平居中可用：

```text
re.X = (1280 - 169) / 2 ≈ 556
```

Y 保留用户编辑器当前位置，除非用户明确要求上下移动。

## flag 历史记录点

`flag` 是赛道上的“历史最远点路标”，不是 Game Over 结算 UI。

逻辑：

```text
如果 BestScoreM <= 0：隐藏
如果 GameOver = 1：隐藏
运行中：
  currentMeters = 666 - DistanceLeft
  metersUntilBest = BestScoreM - currentMeters
  flag.X = KnightHorse参考X + metersUntilBest * 像素倍率
  flag.Y = HomeY
```

当前已验证参考值：

```text
KnightHorse参考X = 297
像素倍率 = 6
显示范围：-220 < flag.X < 1450，否则隐藏到 -2000,-2000
```

效果：下一局玩家接近历史最好成绩时，flag 从右侧进入；追平时 flag 在骑士附近；Game Over 画面不显示 flag。

## JS 事件注意

- 可用一个 JS 事件统一处理：顶部距离数字、Game Over 结算隐藏/显示、best 数字刷新。
- flag 可单独 JS 事件处理，插在 best UI 事件之后，确保 `BestScoreM` 已更新。
- 避免把所有 `ScoreDigit` 都按距离更新；必须判断 `DigitRole`。
- 对重复对象用 `runtimeScene.getObjects("ScoreDigit")` 后逐实例读取变量。

## 回读验证清单

```text
正式 JSON 与 autosave SHA 一致
BestScoreM 全局变量存在且 SceneJustBegins 不重置
Best / go / re / 结尾 M / 结尾 3 个 ScoreDigit 均有 HomeX/HomeY
结尾 3 个 ScoreDigit 的 DigitRole=best，DigitIndex=0/1/2
顶部 3 个 ScoreDigit 的 DigitRole=distance
结尾 M 的 DigitRole=best，顶部 M 的 DigitRole=distance
存在包含 BestScoreM 的 JS 事件
存在包含 Best record flag marker 的 JS 事件
flag 对象与实例仍存在，资源未改
```

## 常见坑

- 用户说“best 和 M 都是我加的，不需要动”时，意思通常是“不改视觉资源/不要删”，不是不加运行逻辑。
- 编辑器里同名 `M` 有两个实例时，不能按对象名整体隐藏；必须按 y 坐标/变量识别顶部 M 与结尾 M。
- 用户刚拖了 `go/re` 位置后，autosave 可能不是最新；必须比较正式 JSON 与 autosave 的 mtime/hash，以最新有用户实例的位置为准。
- 若 GDevelop 退出被用户取消，不要盲写旧 autosave 覆盖用户新增对象；先回读确认新增对象是否已落盘。
