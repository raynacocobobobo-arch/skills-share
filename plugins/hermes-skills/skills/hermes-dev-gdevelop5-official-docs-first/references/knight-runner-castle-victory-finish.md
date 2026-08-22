# KnightRunner_Test：Castle 终点 / Victory 画面 / 终点前清障

适用：用户新增 `Castle` 作为终点标志，以及胜利画面对象（本次实际对象名为 `V3`，用户口头称 `V1`）。

## 触发信号

用户说：

```text
castle 是终点标志，像旗子一样放在地面和地面一起动。
骑士碰到城堡体积后胜利结束。
城堡出现后，城堡前面要完全没有障碍物。
save the / pricess / M / 数字全部消失。
骑士碰到城堡后骑士消失，然后出 V1，正常时 V1 隐藏。
骑士在最前面的图层。
```

## 当前项目对象名注意

- 城堡对象名：`Castle`
- 用户口头说 `V1`，但本次磁盘里实际对象名是 `V3`。后续必须先回读对象列表确认，不要凭口头硬写。
- 顶部 UI：`pricess`、`M`、`ScoreDigit`、`ScoreLabel`
- 玩家：`KnightHorse`

## 稳定实现

### 1. 骑士在最前

```text
KnightHorse.zOrder = 49000
SceneJustBegins → ChangePlan KnightHorse = 49000
```

### 2. Castle 像地面物体移动，并在中心落点锁定

测试阶段用户要求先放 20m：

```text
Castle.X = 297 + 20 * 105
Castle.Y = 用户摆放的 Castle.Y（本次为 -32）
Castle.zOrder = 39999
```

运行中：

```text
GameOver = 0
→ Castle.X -= GlobalVariable(RunSpeed) * 60 * TimeDelta()
```

用户后续要求“城堡到达 / 城堡中心 X 轴落点要对到画面中心”。当前项目窗口宽 1280，画面中心 X=640；如果 Castle 需要停在正中，应按视觉中心锁定：

```js
const width = castle.getWidth ? castle.getWidth() : 729;
const centerX = castle.getX() + width / 2;
if (centerX > 640) castle.setX(castle.getX() - runSpeed * 60 * dt);
if (castle.getX() + width / 2 < 640) castle.setX(640 - width / 2);
```

`105 px/m` 来自同项目 flag 记录点体感通过参数；终点正式距离后续可替换 `20`。

### 3. 城堡出现后，城堡前面清障，并降速

当城堡接近/出现时，删除所有障碍，并把后续生成点推到城堡后方至少 10m：

```text
GameOver = 0
Castle.X < 2600（若要更贴近“出现后”可用 1400）
→ ObstacleState = 0
→ Delete NewSprite12 / ObstacleHitbox
→ Delete NewSprite12Big / ObstacleHitboxBig
→ Delete NewSprite12Medium / ObstacleHitboxMedium
→ ObstacleCount = 0
→ GroupLastX = Castle.X() + 10 * 105
→ GroupStartX = Castle.X() + 10 * 105
```

当前用户已取消“城堡出现后强制降速”。`Castle.X < 2600` 时只设置 `CastleSpeedLocked=1`，保留进入终点时的当前速度；禁止再次强制 `RunSpeed=2`，否则结尾会突然慢下来。

当前 500M / 每秒 4M 的终点同步方式：Castle 在屏幕外以 `541.016 px/s` 接近，125 秒时恰好到 `X=2600`；锁定后再按当前 `RunSpeed * 60` 移动。

```text
GameOver = 0
Castle.X < 2600
→ CastleVisible = 1
→ CastleSpeedLocked = 1
→ 不修改 RunSpeed
```

如果用户后续要求改为 4/开始速度，只改 CastleVisible/keep-speed 两个 Castle 事件里的 `RunSpeed`，不要改 SpeedPhase 表。

同时开局/首个障碍生成点也应避开测试终点：

```text
GroupStartX = 297 + 30 * 105
```

这样 20m 的 Castle 前 10m 不会有木桩。

### 4. 胜利触发：Castle 是胜利终点，不是死亡点

用户纠正过：骑士到达 Castle 后**不要出 `go/re`，也不要播放死亡音效**。Castle 终点应只显示胜利图（当前实际对象 `V3`），不是 Game Over 结算。

通关胜利声音：用户把桌面 `VC.mp3` 作为通关音效。稳定接法：复制到项目目录并注册音频资源，新增/使用 `VictoryAudioPlayed` 场景变量，`SceneJustBegins → VictoryAudioPlayed=0`；在 Castle 胜利触发事件内，先 `UnloadAllAudio` 停背景音乐，然后仅当 `VictoryAudioPlayed=0` 时播放一次 `VC.mp3` 并置 `VictoryAudioPlayed=1`。不要复用死亡音效 `A.mp3`。

```js
if (vars.get("VictoryAudioPlayed").getAsNumber() === 0) {
  gdjs.evtTools.sound.playSound(runtimeScene, "VC.mp3", false, 100, 1);
  vars.get("VictoryAudioPlayed").setNumber(1);
}
```

不要使用整张 Castle 图片的完整 bbox 作为结束碰撞：当前 Castle 视觉图很大，按整图外框会导致“刚碰到城堡边缘就死/结束”。稳定做法是用 Castle 视觉中心到达画面中心附近作为胜利触发，或后续另建小型 `CastleHitbox`。已验证当前体感规则：

```text
GameOver = 0
Castle centerX <= 650（画面中心 640 附近）
→ Win = 1
→ GameOver = 1（只作为暂停全局移动/生成的状态，不代表死亡）
→ DeathAudioPlayed = 1（阻止通用 GameOver 死亡音效事件）
→ UnloadAllAudio（停止背景音乐）
→ VictoryAudioPlayed=0 时播放一次 VC.mp3，然后 VictoryAudioPlayed=1
→ KnightHorse X/Y = -2000
→ V3 X/Y = HomeX/HomeY（当前 374,88）
→ V3 zOrder = 50000
→ pricess / M / ScoreDigit / ScoreLabel 隐藏
→ go / re 隐藏，不显示
```

重要坑：后面的 Best 结算 UI 脚本会因为 `GameOver=1` 把结算 `M`、Best 数字、`go/re` 再显示回来。Castle 胜利使用 `GameOver=1` 暂停世界时，必须在 Best UI JS 中额外读取 `Win`，只在 `gameOver && !win` 时显示结算 UI：

```js
const gameOver = sceneVars.get("GameOver").getAsNumber() === 1;
const win = sceneVars.get("Win").getAsNumber() === 1;
// best digits / best M / Best / go / re
setHomeOrHidden(object, gameOver && !win);
```

如果用户要求“胜利后可重玩”，不要复用死亡结算的 `re`；应另做胜利页按钮或等待用户明确要求。

如果用户要求“胜利后可重玩”，不要复用死亡结算的 `re`；应另做胜利页按钮或等待用户明确要求。

### 5. V1/V3 正常隐藏

`SceneJustBegins`：

```text
V3/V1 X = -2000
V3/V1 Y = -2000
V3/V1 zOrder = 50000
```

给胜利图实例保存：

```text
HomeX = 当前实例 X
HomeY = 当前实例 Y
```

### 6. 2026-06 追加：Castle 中心落点、降速与碰撞事件互斥修复

用户反馈：

```text
1. 城堡到达 / 城堡中心 x 轴落点要对到画面中心
2. 如果碰撞城堡，没有 game over 和死亡声音
3. 城堡出现后，速度自动降回 4
```

本次确认的坑：

1. Castle 曾同时存在两套移动事件，导致城堡双倍速度左移；继续改前必须搜索所有包含 `Castle` 的运行时事件，删除重复移动/碰撞事件，只保留一套权威逻辑。
2. Castle 曾存在两套碰撞事件：第一套先把 `GameOver=1`，第二套显示 `go/re` 的事件条件也是 `GameOver=0`，因此第二套同帧无法执行，表现为“碰到城堡没有 Game Over UI”。修复时必须把状态设置、UI 显示、声音触发放在同一个权威碰撞事件里，或确保显示事件不依赖已被前一事件改掉的条件。
3. `DeathAudioPlayed` 可能已在死亡事件里使用；如果 Castle 胜利碰撞也希望播放现有死亡音效事件，可在碰撞里设置 `GameOver=1` 且 `DeathAudioPlayed=0`，让独立音效事件 `GameOver=1 && DeathAudioPlayed=0 → PlaySound A.mp3 → DeathAudioPlayed=1` 接管。若先 `UnloadAllAudio`，之后仍要保证音效事件能触发一次。

稳定做法：

```text
Castle 出现/接近屏幕：
GameOver = 0 && Castle.X < 1400
→ CastleVisible = 1
→ CastleSpeedLocked = 1
→ GlobalVariable(RunSpeed) = 2（用户当前确认值；如后续要求再改）
→ 删除所有木桩视觉和 Hitbox
→ ObstacleCount = 0
→ GroupLastX / GroupStartX = Castle.X() + 10 * 105

CastleVisible = 1 && GameOver = 0
→ 每帧强制 GlobalVariable(RunSpeed) = 2
```

降速事件要放在 `SpeedPhase` 分档改速事件之后，或者单独每帧锁速，否则 `SpeedPhase` 会把 `RunSpeed=2` 覆盖回 6.6/8.1/11.5 等。

Castle 中心落点对齐画面中心：

```js
// 画面宽 1280，中心 X = 640。
// Castle 继续随地面移动，直到 visual center <= 640，然后锁住中心。
const runSpeed = runtimeScene.getGame().getVariables().get("RunSpeed").getAsNumber();
for (const castle of runtimeScene.getObjects("Castle")) {
  const width = typeof castle.getWidth === "function" ? castle.getWidth() : 729;
  const centerX = castle.getX() + width / 2;
  if (centerX > 640) {
    castle.setX(castle.getX() - runSpeed * 60 * runtimeScene.getElapsedTime() / 1000);
    if (castle.getX() + width / 2 < 640) castle.setX(640 - width / 2);
  } else {
    castle.setX(640 - width / 2);
  }
}
```

Castle 碰撞建议用一套权威事件；如果 `CollisionNP(KnightHorse, Castle)` 与用户对“城堡体积”的预期不一致，可用 JS bbox 重叠判定，避免透明像素/碰撞 mask 导致体感不触发：

```js
const overlap = k.getX() < c.getX() + cw && k.getX() + kw > c.getX()
  && k.getY() < c.getY() + ch && k.getY() + kh > c.getY();
if (overlap) {
  vars.get("Win").setNumber(1);
  vars.get("GameOver").setNumber(1);
  vars.get("DeathAudioPlayed").setNumber(0);
  gdjs.evtTools.sound.unloadAllAudio(runtimeScene);
  k.setPosition(-2000, -2000);
  // 显示 V3、go、re，隐藏 pricess/M/ScoreDigit/ScoreLabel。
}
```

回读验收：

```text
- 搜索所有运行时 Castle 事件：不得有两套 Castle 左移事件。
- 搜索所有 Castle 碰撞/胜利触发事件：不得使用整张 Castle bbox 导致触发过早；当前稳定为 Castle centerX <= 650。
- Castle 胜利事件：不显示 go/re，不播放 A.mp3；设置 DeathAudioPlayed=1 阻止通用死亡音效。
- Castle 胜利事件：播放 VC.mp3 一次，并设置 VictoryAudioPlayed=1。
- Best UI JS：必须有 win 判断，Best/M/go/re/结算数字只在 gameOver && !win 显示，避免通关后 M 又冒出来。
- 正式 json 与 autosave SHA 一致。
- Castle runtime block 至少包含：visible/clear/RunSpeed=2、keep speed=2、move center=640、center reached show V3 + VC.mp3。
```

## 2026-06 最新稳定版：Castle 触碰后滑出再显示 V3

用户最终确认的胜利节奏不是“城堡中心到画面中心就立刻出 V3”，而是三段式：

```text
1. 骑士碰到 Castle
   → KnightHorse X/Y = -2000
   → 停止背景音乐频道 + unloadAllAudio
   → 播放 VC.mp3 一次
   → VictoryPending = 1
   → CastleTouched = 1
   → Win = 1
   → DeathAudioPlayed = 1（阻止通用死亡音效）
   → 暂不显示 V3，不显示 go/re/M/Best/结算数字

2. Castle 继续向左滑动
   → 不能再锁在画面中心
   → 继续按 RunSpeed * 60 * TimeDelta() 左移

3. Castle 完全滑出画面左侧后
   → GameOver = 1（只用于停止全局移动/生成，不代表死亡）
   → 显示 V3
   → 继续隐藏 go/re/M/Best/结算数字
```

### 关键实现点

- 新增/使用场景变量：`CastleTouched`、`VictoryPending`、`VictoryAudioPlayed`，并在 `SceneJustBegins` 重置为 `0`。
- Castle 出现后速度当前稳定要求为 `RunSpeed = 2`，且要持续锁速；只设置一次会被 `SpeedPhase` 覆盖。
- Castle 出现后后方不要再有木桩：
  - Castle 可见/接近时删除所有 `NewSprite12/NewSprite12Big/NewSprite12Medium` 与对应 `ObstacleHitbox*`。
  - 设置 `MaxObstacles = 0`。
  - 所有障碍生成/GroupSize/GroupGap/ObstacleState 事件都加 `CastleVisible = 0` 门控。
  - `GroupStartX` / `GroupLastX` 可推到 `Castle.X() + 99999`，作为额外保险。
- 播放成功音乐时背景音乐必须停：
  - 在触碰 Castle 的胜利事件中执行 `gdjs.evtTools.sound.stopMusicOnChannel(runtimeScene, 1)` 后再 `unloadAllAudio`。
  - 播放 `gdjs.evtTools.sound.playSound(runtimeScene, "VC.mp3", false, 100, 1)`。
  - BGM JS 事件的播放条件必须排除 `VictoryPending=1`、`CastleTouched=1`、`Win=1`，否则下一帧会把背景音乐重新拉起来。
- `VC.mp3` 必须复制到项目目录并注册为 `kind=audio`、`preloadAsSound=true`。
- 通关时 `GameOver=1` 会触发 Best 结算 UI 脚本把 `M/Best/go/re` 显示回来；UI 脚本必须加 `Win` 判断：`gameOver && !win` 才显示结算 UI。死亡 Game Over 仍正常显示结算 UI。

### 重要工具/流程坑

GDevelop 重新保存项目时会清掉事件 JSON 里的非官方自定义字段（例如 `hermesCastleFinish`）。后续不能依赖这类自定义 marker 定位事件；必须按 `inlineCode` 内容、对象名、变量名或事件动作结构定位。可用注释字符串作为 JS 事件内部标记，但不要假设顶层自定义字段会保留。

## 2026-06 最终确认：正式终点、通关音效、Castle 滑出后再显示 V3

用户最终确认的 Castle 通关流程：

```text
1. Castle 位置从测试 20m 移到倒计时 0M 的正式终点：
   Castle.X = 297 + 666 * 105 = 70227
   Castle.Y = -32

2. Castle 接近/进入终点阶段后：
   RunSpeed 锁定为 2
   删除所有木桩视觉和碰撞盒
   MaxObstacles = 0
   ObstacleState = 0
   ObstacleCount = 0
   GroupStartX / GroupLastX = Castle.X() + 99999
   所有障碍生成事件额外加 CastleVisible = 0 门控

3. 骑士碰到 Castle 后：
   KnightHorse X/Y = -2000
   播放 VC.mp3 一次
   背景音乐频道停止，并阻止 BGM JS 在 Win/CastleTouched/VictoryPending 状态下重启
   不显示 V3
   不显示 go/re/M/Best/结算数字

4. Castle 继续向左滑动，不再锁在画面中心。

5. Castle 完全滑出画面左边后：
   GameOver = 1（仅用于停止移动/生成，不代表死亡）
   V3 X/Y = 374,88，zOrder = 50000
   re X/Y = 556,496，zOrder = 50002
   仍不显示 go/M/Best/结算数字
```

关键坑：

- GDevelop 保存后会清掉自定义事件字段（例如 `hermesCastleFinish`），后续定位 Castle 事件不能依赖自定义 marker；应按 `inlineCode` 中的注释/关键对象内容定位。
- “Castle 后面还有木桩”通常不是新生成，而是已经在远处生成的木桩继续滑进画面；只给生成事件加门控不够，必须在 CastleVisible 后每帧硬删除所有木桩和 hitbox。
- Castle 通关不是死亡：`DeathAudioPlayed=1` 用来阻止通用 GameOver 死亡音效；通关音效用 `VC.mp3` 独立播放一次。
- V3 出现后要显示 Retry 时，不能只在通关事件里摆 `re`；Best UI 脚本如果按 `gameOver && !win` 隐藏 `re`，会同帧覆盖。应在 UI 脚本里允许 `victoryFinal = win && gameOver && VictoryPending=0` 时显示 `re`。

## 7. 2026-06 追加：正式终点 0M、通关三段式与终点清障边界

用户最终确认的 Castle 终点流程不是“到中心立刻显示 V3”，而是三段式：

```text
1. 骑士碰到 Castle 的主体区域
→ KnightHorse X/Y = -2000
→ 停止 BGM 音乐频道 + unloadAllAudio
→ 播放 VC.mp3 一次
→ Win = 1
→ CastleTouched = 1
→ VictoryPending = 1
→ 不显示 V3 / go / re / M / Best / ScoreDigit

2. Castle 继续向左滑出屏幕
→ Castle 仍按 RunSpeed * 60 * TimeDelta 左移
→ 不要再锁中心 640

3. Castle 完全从画面左侧消失后
→ GameOver = 1（只用于暂停全局系统，不代表死亡）
→ VictoryPending = 0
→ 显示 V3
→ 显示 re Retry
→ 仍不显示 go / M / Best / ScoreDigit
```

### 正式终点位置

测试阶段曾用 `297 + 20 * 105`；正式终点应对应倒计时 `0M`：

```text
Castle.X = 297 + 666 * 105 = 70227
Castle.Y = -32
```

如果后续 `DistanceLeft` 起始值不是 666，要同步改这里的距离系数，不要只改 UI 倒计时。

### Castle 后面无木桩：必须有“接近终点”门槛

曾踩坑：把“硬清木桩/停生成”写成无距离门槛，导致开局 Castle 虽在 0M 远处，但 `CastleVisible=1` 直接触发，所有木桩从开局就没了。

稳定做法：

```text
运行中清障事件：
GameOver = 0
Castle.X < 2600
→ CastleVisible = 1
→ CastleSpeedLocked = 1
→ RunSpeed = 2
→ Delete NewSprite12 / ObstacleHitbox / NewSprite12Big / ObstacleHitboxBig / NewSprite12Medium / ObstacleHitboxMedium
→ ObstacleCount = 0
→ ObstacleState = 0
→ MaxObstacles = 0
→ GroupLastX = Castle.X() + 99999
→ GroupStartX = Castle.X() + 99999
```

同时，所有障碍生成事件（ObstacleState/GroupSize/GroupGap/Create/LastPattern 等生成链路）应加：

```text
CastleVisible = 0
```

但 `SceneJustBegins` 初始化事件绝不能加 `Castle.X < 2600` 或 `GameOver=0` 这类运行条件；初始化事件条件必须保持只有 `SceneJustBegins`。否则初始化会失效或逻辑混乱。

### V3 后显示 Retry，避免结算 UI 脚本覆盖

V3 出现后要显示 `re`，但 `go/M/Best/ScoreDigit` 不显示。注意 Best 结算 UI 脚本可能每帧根据 `GameOver=1` 重新显示/隐藏结算对象；因此要在 UI 脚本里区分：

```js
const win = sceneVars.get("Win").getAsNumber() === 1;
const victoryFinal = win && gameOver && sceneVars.get("VictoryPending").getAsNumber() === 0;

// best/M/go 仍然只在死亡 GameOver 显示：gameOver && !win
// re 在死亡 GameOver 或 victoryFinal 显示：
setHomeOrHidden(reObject, (gameOver && !win) || victoryFinal);
```

### 胜利音效与 BGM

播放 `VC.mp3` 时必须阻止背景音乐被下一帧 BGM 脚本拉起来：

```js
gdjs.evtTools.sound.stopMusicOnChannel(runtimeScene, 1);
gdjs.evtTools.sound.unloadAllAudio(runtimeScene);
gdjs.evtTools.sound.playSound(runtimeScene, "VC.mp3", false, 100, 1);
```

BGM 脚本播放条件要排除胜利相关状态：

```js
GameOver == 0 && VictoryPending == 0 && CastleTouched == 0 && Win == 0
```

### GDevelop 会清掉自定义事件字段

不要依赖手写 JSON 里的自定义字段（例如 `hermesCastleFinish`）作为长期定位标记；GDevelop 保存项目时可能移除这些未知字段。后续修改应通过事件内容、对象名、动作/条件组合定位 Castle 相关事件，并回读验证。

## 避坑

1. 用户刚在 GDevelop 里新增 `Castle` 或 `V1` 后，必须先比较正式 JSON 和 autosave，优先保留较新的用户编辑；如果新对象只在正式 JSON 中，不能用旧 autosave 覆盖。
2. 用户口头对象名可能和项目实际对象名不同；必须回读对象和实例列表确认。
3. Castle 终点不要和 flag 逻辑混用：flag 是历史纪录点；Castle 是本局终点。
4. 清障时要删视觉对象和 hitbox 两套，否则“看不见但还能撞死”。
5. 如果用户说城堡触发太早，再新增专门 `CastleHitbox`，不要缩放/移动 Castle 视觉资源。
6. Castle 图片很大时，不能直接用整张 Castle 外框/BBox 做胜利碰撞；用户实测会变成“刚碰到城堡边就死”。稳定修法：要么用专门小 `CastleHitbox`，要么用 Castle 视觉中心到达画面中心附近（例如 centerX <= 650，移动锁到 640）作为终点触发，再显示 `V3/go/re` 和播放死亡/结束音效。
