# KnightRunner_Test：pricess + 3位数字 + M 距离倒计时

## 触发场景

用户把原 `score` 标签替换为 `pricess.png`，新增 `m.png`，要求游戏 UI 从计分器改成米数倒计时，例如：

```text
pricess + 999 + M
每秒递减若干米
```

## 稳定原则

1. **不要把 `GlobalVariable(Score)` 改成倒计时。**  
   `Score` 仍作为内部累计进度，继续驱动障碍难度、复杂障碍解锁、音乐/速度等系统。

2. **新增 `GlobalVariable(DistanceLeft)` 只负责显示距离。**

3. **开局初始化和倒计时事件必须分开改。**  
   避免误把 `SceneJustBegins` 里的 `DistanceLeft = 999` 也替换成递减表达式。

## 当前项目稳定形态

### 变量

```text
GlobalVariable(DistanceLeft) = 999
```

### 开局事件 SceneJustBegins

```text
ModVarGlobal DistanceLeft = 999
ResetTimer("DistanceTimer")
ResetTimer("SpeedTimer")  // 如果速度改为按时间分档
```

### 倒计时事件

当前用户最终要求：每秒 `-9M`。

```text
GameOver = 0
CompareTimer("DistanceTimer") >= 1
→ DistanceLeft = max(0, GlobalVariable(DistanceLeft) - 9)
→ ResetTimer("DistanceTimer")
```

如果用户后续改成 -5/-6，只改非 `SceneJustBegins` 的 `DistanceTimer` 事件，不改开局 999。

### 图片显示 JS

```js
// Distance counter: pricess + 3 digits + M, backed by GlobalVariable(DistanceLeft).
// Score remains an internal progress variable for RunSpeed and obstacle difficulty.
const distanceVariable = runtimeScene.getGame().getVariables().get("DistanceLeft");
const distance = Math.max(0, Math.min(999, Math.floor(distanceVariable.getAsNumber())));
const paddedDistance = String(distance).padStart(3, "0").slice(-3);
const digits = runtimeScene.getObjects("ScoreDigit");
for (const digitObject of digits) {
  const index = digitObject.getVariables().get("DigitIndex").getAsNumber();
  if (index >= 0 && index < 3) {
    digitObject.setAnimationIndex(Number(paddedDistance[index]));
  }
}
```

### 实例与层级

当前 UI 结构：

```text
pricess：zOrder 10003
M：zOrder 10002
ScoreDigit 三位：zOrder 10001
Dragon2 普通前景：zOrder 10000
Dragon2 左→右：zOrder 9（骑士后面）
KnightHorse：zOrder 10
```

三个 `ScoreDigit` 实例必须按 x 从左到右设置：

```text
DigitIndex = 0
DigitIndex = 1
DigitIndex = 2
```

曾出现用户手动添加后 3 个实例 `DigitIndex` 都是 `2` 的情况，必须回读修正。

## 速度按时间加速

用户最终要求“游戏本身的速度每 8s 加一次速”。稳定形态：

```text
SceneJustBegins
→ RunSpeed = 5.2
→ ResetTimer("SpeedTimer")

GameOver = 0
CompareTimer("SpeedTimer") >= 8
→ RunSpeed = min(11.0, GlobalVariable(RunSpeed) + 0.35)
→ ResetTimer("SpeedTimer")
```

同时从原 `ScoreTimer` 事件中移除连续 RunSpeed 公式，保留 `Score += 10` 给内部难度/累计进度使用。

## 回读验证清单

```text
正式 JSON 与 autosave SHA 一致
GlobalVariable(DistanceLeft) 存在且默认 999
SceneJustBegins 里 DistanceLeft = 999
非 SceneJustBegins 的 DistanceTimer 事件里是 DistanceLeft = max(0, DistanceLeft - N)
ScoreTimer 事件仍有 Score += 10，但不再连续写 RunSpeed（若用户选择 8s 加速）
SpeedTimer 事件存在：>=8 秒，RunSpeed = min(11.0, RunSpeed + 0.35)
ScoreDigit 三个实例 DigitIndex = 0/1/2
pricess/M/数字/Dragon2/KnightHorse zOrder 不互相遮挡
```

## 避坑

- 搜索替换 `DistanceLeft` 时一定排除 `SceneJustBegins`，否则会把初始 999 改坏。
- 不要删除 `Score`；它是内部进度变量。
- 不要把 `M` 做成文字对象；用户已提供 `m.png`，应保留 Sprite。
- GDevelop 打开状态可能写 autosave 覆盖修改；改完后退出 GDevelop、重写 formal/autosave、再重新打开。