# KnightRunner_Test：核心系统回归修复清单（二段跳 / Retry / Score / 跳高 / Dragon2）

适用：修改障碍组、计分、Retry 或平台行为后，用户反馈“二段跳没了 / retry 没了 / 分数不走 / 跳不过木桩 / 红龙速度不对”时。

## 官方依据先行

本类修复至少要确认本地官方文档缓存中这些条目：

- Events / Standard events：事件由条件和动作组成，顶层事件顺序会影响初始化、输入和状态重置。
- Objects / Objects Reference：对象创建、删除、位置重置、碰撞对象不要误改。
- Variables：全局变量 `Score/RunSpeed` 与场景变量 `GameOver/DoubleJumpAvailable/...` 作用域要分清。
- Expressions：`GlobalVariable()`、`TimeDelta()`、`Timer`、文本拼接表达式要回读验证。
- Platformer behavior：跳跃高度、重力、二段跳属于 `KnightHorse.PlatformerObject` 行为参数，不应在障碍修复中被误回退。

## 关键坑与稳定修法

### 1. `SceneJustBegins` 保持第一条顶层初始化事件（项目约定）

这不是 GDevelop 官方要求的通用顺序，而是本项目的可维护性约定。补丁不要把输入事件插到初始化事件之前。

回读验证：

```text
layout.events[0].conditions 包含 SceneJustBegins
```

### 2. Retry 使用当前官方对象命中、鼠标释放和 Scene 动作

错误模式：

```text
沿用旧式 SourisSurObjet / MouseButtonReleased
先手工重置几十项，最后又 Scene 重载
```

当前需求的正确事件：

```text
GameOver = 1
IsCursorOnObject(re)
MouseButtonFromTextReleased("Left")
→ Scene("未命名场景")
```

回读验证重点：

```text
retry_event_count == 1
该事件包含 IsCursorOnObject + MouseButtonFromTextReleased + Scene
Scene 动作是唯一动作，不再保留原地重置动作
SceneJustBegins 负责重新设置 Score / RunSpeed 并启动 ScoreTimer
```

### 3. 分数使用当前官方场景计时器内部类型

稳定事件：

```text
GameOver = 0
CompareTimer("ScoreTimer") >= 0.1
→ Score += 10
→ ResetTimer("ScoreTimer")
→ ScoreText = "Score: " + ToString(GlobalVariable(Score))
→ RunSpeed = min(8.4, 5.2 + sqrt(GlobalVariable(Score) / 100) * 0.18)
```

`SceneJustBegins` 中执行：

```text
ResetTimer("ScoreTimer")
ScoreText = "Score: 0"
```

回读验证：

```text
条件内部类型为 CompareTimer，参数包含内部空参数、带引号的 "ScoreTimer"、比较符和 0.1
ResetTimer 参数包含内部空参数和带引号的 "ScoreTimer"
存在 Score += 10 事件
```

### 4. 二段跳与跳高要同时看“行为参数”和“手动事件”

官方 Platformer behavior 可确认的可调属性：

```text
jumpSpeed
gravity
jumpSustainTime
maxFallingSpeed
ignoreDefaultControls
useRepeatedJump
```

当前项目的跳跃调参经验（不要再把 1120 当默认标准）：

```text
旧高跳版本：
jumpSpeed = 1120
gravity = 1320
jumpSustainTime = 0.24
maxFallingSpeed = 980
问题：二段跳会飞太高，骑士能碰到 Dragon2。

压低弧线候选版本：
jumpSpeed = 700
gravity = 1700
jumpSustainTime = 0.12
maxFallingSpeed = 980
目标：第一段跳能过 NewSprite12/ObstacleHitbox，保留约 30% 容错；二段跳不应碰到龙。
```

后续调手感只微调 `jumpSpeed / gravity / jumpSustainTime`，不要为了“能过木桩”直接回到 1000+。若第一段差一点，优先小步把 `jumpSpeed` 从 700 提到 730/760；若二段仍碰龙，优先降 `jumpSustainTime` 或升 `gravity`。

`allowDoubleJump`、`numberOfJumpsMax`、`maxJumpCount`、`jumpCountMax` 不是当前官方
Platformer behavior 属性，运行时不会读取，禁止写入项目 JSON。

每次落地重新补充空中跳：

```text
GameOver = 0
IsOnFloor(KnightHorse.PlatformerObject)
→ DoubleJumpAvailable = 1
→ JumpKeyReleasedAfterFirstJump = 0
```

手动二段跳事件必须只在空中触发：

```text
GameOver = 0
NOT IsOnFloor(KnightHorse.PlatformerObject)
KeyFromTextReleased("Space")
→ JumpKeyReleasedAfterFirstJump = 1

GameOver = 0
NOT IsOnFloor(KnightHorse.PlatformerObject)
DoubleJumpAvailable = 1
JumpKeyReleasedAfterFirstJump = 1
KeyFromTextJustPressed("Space")
→ SetCanJump
→ SimulateJumpKey
→ DoubleJumpAvailable = 0
→ JumpKeyReleasedAfterFirstJump = 0
```

不要把 `IsOnFloor` 写成正向条件，否则会变成“在地面按空格消耗二段跳”，用户会感知为二段跳被改没。

### 5. Dragon2 当前需求为旧速度的 50%

地面使用：

```text
GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

旧表达式为 `RunSpeed * 120 * TimeDelta()`，降低 50% 后左右移动都应使用：

```text
GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

回读验证：

```text
Dragon2 的 60 表达式出现 2 次（左移、右移）
Dragon2 不再残留 120 表达式
```

## 运行时代码验证（强制新增）

用户/Codex 实测确认：只看项目 JSON 不够，GDevelop 预览可能运行旧实例或把 JSON 指令编译失败。修复核心系统后必须以新 GDevelop 进程重新载入磁盘文件，并检查预览生成的 `code0.js`。

关键坑：

```text
SetNumberVariable("GlobalVariable(Score)") 会在实际编译结果里变成 badVariable，运行时不会正确修改全局分数。
旧式 Text 动作可能在编译结果里显示 Unknown instruction - skipped，JSON 看起来有 ScoreText 更新，但运行代码会跳过。
本项目分数每次增加整数 10，不需要取整；大写 `Round(...)` 会让当前文字表达式编译为空字符串。
```

本项目直接 JSON 的已验证写法：

```text
全局变量动作/条件：ModVarGlobal / VarGlobal，参数传变量名
场景变量动作/条件：ModVarScene / VarScene，参数传变量名
ScoreText：TextContainerCapability::TextContainerBehavior::SetValue，行为参数为 Text
```

因此回归验证不能只检查 JSON 字符串，必须同时检查：

```text
1. 关闭/避开旧 GDevelop 预览实例，确认新窗口从当前磁盘 JSON 启动。
2. 找到当前预览生成的 code0.js。
3. 搜索 badVariable、Unknown instruction - skipped、ScoreTimer、ScoreText、Retry/re、DoubleJumpAvailable、JumpKeyReleasedAfterFirstJump、Dragon2、NewSprite12/ObstacleHitbox。
4. 如果 code0.js 里出现 badVariable 或 Unknown instruction - skipped，本次修复视为失败，即使 JSON 表面看起来正确。
5. 以 code0.js 中实际执行的指令为准倒推 JSON 内部 action/condition 类型和参数，不要照参考页硬写。
```

## 最小补丁验证清单

写入正式 JSON 和 `.autosave` 后必须回读：

```text
formal JSON 与 autosave SHA 一致
layout.events[0] 是 SceneJustBegins
存在 1 条 Retry：IsCursorOnObject + MouseButtonFromTextReleased + Scene
Retry 不再混用原地重置与 Scene
存在 CompareTimer 0.1 秒 +10 分事件，ResetTimer 使用当前参数格式
KnightHorse.PlatformerObject 只保留官方属性
存在落地重置 DoubleJumpAvailable 的事件
手动二段跳 KeyFromTextJustPressed/KeyFromTextReleased 事件都带 NOT IsOnFloor
Dragon2 左右移动都是 RunSpeed * 60 * TimeDelta()
碰撞仍为 KnightHorse collision ObstacleHitbox
```

## 2026-06 补充：手机/鼠标点击跳跃输入（官方 runtime 方式）

用户连续实测纠正：普通事件里的 `MouseButtonFromTextJustPressed` 不行；改成 `MouseButtonFromTextReleased` 也“不和空格一样”。原因是 Space 的平台跳跃是“按住期间持续输入”，而不是一次性的点击/释放动作。

稳定做法：不要再用普通鼠标条件拼地面跳/二段跳。新增一个 JS Code 事件，直接读取 GDevelop 官方运行时 `InputManager` 的左键/触摸按住状态，并在按住期间每帧调用 `PlatformerObject.simulateJumpKey()`，这样才接近 Space 按住逻辑。

官方运行时依据来自本机 GDevelop 源码：

```text
runtimeScene.getGame().getInputManager()
input.isMouseButtonPressed(gdjs.InputManager.MOUSE_LEFT_BUTTON)
PlatformerObjectRuntimeBehavior.simulateJumpKey()
```

当前项目稳定 JS 形态：

```js
const input = runtimeScene.getGame().getInputManager();
const leftDown = input.isMouseButtonPressed(gdjs.InputManager.MOUSE_LEFT_BUTTON);
const touchDown = input.getStartedTouchIdentifiers && input.getStartedTouchIdentifiers().length > 0
  ? true
  : (input.getAllTouchIdentifiers && input.getAllTouchIdentifiers().length > 0);
const down = leftDown || touchDown;
const vars = runtimeScene.getVariables();
const gameOver = vars.get("GameOver").getAsNumber();
const wasDownVar = vars.get("MouseJumpWasDown");
const wasDown = wasDownVar.getAsNumber() === 1;
const knight = runtimeScene.getObjects("KnightHorse")[0];

if (knight && gameOver === 0) {
  const behavior = knight.getBehavior("PlatformerObject");
  if (down) behavior.simulateJumpKey();

  if (!down && wasDown && !behavior.isOnFloor()) {
    vars.get("JumpKeyReleasedAfterFirstJump").setNumber(1);
  }

  if (down && !wasDown && !behavior.isOnFloor()
      && vars.get("DoubleJumpAvailable").getAsNumber() === 1
      && vars.get("JumpKeyReleasedAfterFirstJump").getAsNumber() === 1) {
    behavior.setCanJump();
    behavior.setGravity(3200);
    behavior.simulateJumpKey();
    vars.get("DoubleJumpAvailable").setNumber(0);
    vars.get("JumpKeyReleasedAfterFirstJump").setNumber(0);
    gdjs.evtTools.sound.playSound(runtimeScene, "1234.mp3", false, 80, 1);
  }

  if (down && !wasDown && behavior.isOnFloor()) {
    gdjs.evtTools.sound.playSound(runtimeScene, "1234.mp3", false, 80, 1);
  }
}
wasDownVar.setNumber(down ? 1 : 0);
```

初始化必须加：

```text
SceneJustBegins → MouseJumpWasDown = 0
```

Retry 不冲突：Retry 条件是 `GameOver = 1` + `re` 命中；JS 跳跃在 `GameOver = 0` 时才生效。

回读验证：

```text
不存在旧的 hermesMobileTapJump 普通事件
存在一个 BuiltinCommonInstructions::JsCode，包含 getInputManager/isMouseButtonPressed/simulateJumpKey
SceneJustBegins 初始化 MouseJumpWasDown=0
键盘 Space 原事件不删除，作为桌面键盘输入继续保留
Retry 仍只在 GameOver=1 生效
```

## 操作原则

- 用户报多个核心系统回归时，先回读 JSON 定位，再只改对应系统；不要重写障碍生成。
- 检查字符串时避免误把 `SceneJustBegins` 初始化中的 `JumpKeyReleasedAfterFirstJump` 当成跳跃输入事件；判断输入事件要看条件里是否有 `KeyFromTextJustPressed/KeyFromTextReleased`。
- 如果用户说“骑士二段跳最高不能碰到龙/二段跳会碰龙”，默认先调 `Dragon2` 的飞行高度，不要擅自压低 `KnightHorse` 跳跃高度；只有用户明确要求改跳跃手感时才动 Platformer 行为参数或二段跳事件。
- 修完必须重新打开 GDevelop，并报告可验证结果，不要只说“应该好了”。
