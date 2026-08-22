# KnightRunner_Test：图片积分器（score.png + 0-9.png）

## 触发场景

用户要求把文字 `ScoreText` 替换成桌面上的图片计分器，例如：

- `score.png`
- `0.png` 到 `9.png`
- “替换积分器/分数显示/图片数字分数”

## 官方依据先行

处理前必须先确认/引用：

- Sprite：Sprite 对象用于显示图片或一组图片动画帧。
- Events：事件驱动游戏逻辑。
- JavaScript Code events：官方说明 JS 事件中可访问 `runtimeScene`，代表正在运行的场景。
- Variables：本项目分数仍使用 `GlobalVariable(Score)`。
- Expressions：继续保留项目中已验证的 `GlobalVariable(Score)` 表达式，不改分数来源。

## 稳定实现方案

### 1. 不改计分逻辑，只替换显示层

保留：

```text
CompareTimer("ScoreTimer") >= 0.1
Score += 10
ResetTimer("ScoreTimer")
RunSpeed = ...
```

不要改：

```text
ScoreTimer
GlobalVariable(Score)
RunSpeed
Retry
Double Jump
ObstacleHitbox / NewSprite12
Dragon2
跳跃音效
```

### 2. 资源复制进项目目录并改名

从桌面读：

```text
assets/examples/score.png
assets/examples/0.png ... assets/examples/9.png
```

复制到项目目录并使用防冲突资源名：

```text
score_counter_score.png
score_counter_0.png ... score_counter_9.png
```

加入 `resources.resources`，`kind=image`，`smoothed=false`。

### 3. 对象结构

推荐：

```text
ScoreLabel：Sprite，单帧 score_counter_score.png
ScoreDigit：Sprite，10 个 animation，每个 animation 一张 0-9 图片
```

不要创建 `ScoreDigit0` 到 `ScoreDigit5` 六个不同对象；用同一个 `ScoreDigit` 对象创建 6 个实例更轻。

### 4. 实例结构

删除场景中的 `ScoreText` 实例，但可以保留 `ScoreText` 对象定义和旧 TextContainer 动作，避免误伤历史事件。

新增：

```text
ScoreLabel 实例：x=30, y=20, zOrder=9999
6 个 ScoreDigit 实例：zOrder=9999
每个 ScoreDigit 实例带初始变量 DigitIndex = 0..5
```

尺寸可按源图比例缩到 UI 高度，例如：

```text
score.png 原图 2508x627 -> 显示 168x42
0-9.png 原图 134x201 -> 显示 28x42
```

### 5. JS 更新事件

在 ScoreTimer 计分事件之后插入 1 个 JavaScript Code event：

```js
// Image score counter: score.png + 0-9.png.
// Keep the existing GlobalVariable(Score) logic; only update Sprite animations.
const scoreVariable = runtimeScene.getGame().getVariables().get("Score");
const score = Math.max(0, Math.floor(scoreVariable.getAsNumber()));
const paddedScore = String(score).padStart(6, "0").slice(-6);
const digits = runtimeScene.getObjects("ScoreDigit");
for (const digitObject of digits) {
  const index = digitObject.getVariables().get("DigitIndex").getAsNumber();
  if (index >= 0 && index < 6) {
    digitObject.setAnimationIndex(Number(paddedScore[index]));
  }
}
```

JSON 事件形态：

```json
{
  "type": "BuiltinCommonInstructions::JsCode",
  "inlineCode": "...",
  "parameterObjects": "",
  "eventsSheetExpanded": false
}
```

## 距离倒计时显示：不要直接反转 Score

当用户要求“记分系统变成倒计时，例如预设 500M，每秒 10m”时，优先新增显示变量，不要直接把 `GlobalVariable(Score)` 从累计分改成倒计时。

原因：当前项目中 `Score` 同时驱动 RunSpeed、障碍组概率、复杂障碍解锁等难度系统；如果把 `Score` 改成递减，难度曲线会反向或失效。

稳定方案：

```text
保留 GlobalVariable(Score)：累计进度/难度依据，继续给 RunSpeed 和障碍概率使用。
新增 GlobalVariable(DistanceLeft)：显示用剩余距离。
SceneJustBegins：DistanceLeft = 500。
每 1 秒：DistanceLeft = max(0, DistanceLeft - 10)。
图片数字 JS：从 Score 改读 DistanceLeft。
DistanceLeft <= 0 时再按需求触发胜利/停止/结算，不和显示层一次性混改。
```

如果用户要求显示 `M`，需要先确认/添加 `M.png` 或文字/Sprite 标签；不要假设现有 0-9 数字资源能显示单位。

## 修改流程

1. 先查官方文档/本地文档缓存。
2. 保存并退出 GDevelop。
3. 比较正式 `.json` 与 `.json.autosave`，优先最新源。
4. 备份正式文件和 autosave。
5. 复制图片资源到项目目录。
6. 加资源、加对象、加实例、插入 JS 事件。
7. 同步写回正式 `.json` 与 `.json.autosave`。
8. 回读验证并重新打开 GDevelop。

## 回读验证清单

```text
正式 JSON 与 autosave SHA 一致
ScoreLabel 对象存在
ScoreDigit 对象存在且 animations 数量为 10
ScoreLabel 实例数量 = 1
ScoreDigit 实例数量 = 6
ScoreText 场景实例数量 = 0
存在 1 条 BuiltinCommonInstructions::JsCode，inlineCode 包含 Image score counter
ScoreTimer / RunSpeed / DoubleJumpAvailable / ObstacleHitbox 仍存在
图片资源文件实际存在于项目目录
```

## 避坑

- 不要把分数变量从全局变量改成场景变量。
- 不要删除 `ScoreText` 对象定义；只移除实例即可，降低误伤旧事件风险。
- 不要把图片直接引用桌面绝对路径；应复制到项目目录并注册资源。
- 不要用未验证的旧式 Text 动作替换当前项目已验证的 TextContainer 动作。
- 如果用户说“没看到变化”，先让其关闭旧预览窗口；同时重新回读 autosave 和正式 JSON，不要只根据上一轮写入输出判断。