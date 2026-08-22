---
name: gdevelop5-official-docs-first
display_name: GDevelop 5 Official-Docs-First 工程修改技能
description: GDevelop 5 官方文档优先工程修改技能——用于修改、分析、修复、扩展 GDevelop 5 项目 JSON、事件、对象、变量、碰撞、平台行为、UI、音频、场景切换、计分、障碍生成等。最高原则：先查官方文档，再查项目 JSON，只做最小改动；没有官方依据就停止。
triggers:
  - GDevelop
  - GDevelop 5
  - GDevelop5
  - GDevelop JSON
  - KnightRunner_Test
  - GDevelop 项目
  - GDevelop 事件
  - GDevelop 官方文档
  - NewSprite12
  - ObstacleHitbox
  - KnightHorse
related_skills:
  - gdevelop5-click-adventure-director
---

# GDevelop 5 Official-Docs-First 工程修改技能

## 0. 最高原则

本技能用于辅助修改、分析、修复、扩展 GDevelop 5 项目，尤其是 `.json` 项目文件、事件系统、对象系统、变量系统、碰撞系统、平台行为、UI、音频、场景切换、计分、障碍生成等功能。

**最高原则：先查 GDevelop 官方文档，再写实现方案。**

- 没有官方依据，不许凭模型内部逻辑硬写。
- 如果当前文档库没有相关依据，必须继续查 GDevelop 官方文档。
- 如果仍然找不到依据，必须停止，不做。
- 所有 GDevelop 5 项目任务都必须先加载本技能。

---

## 1. 官方文档优先原则

每次处理 GDevelop 相关任务前，必须先判断任务涉及哪些官方机制。

例如：

- 要改事件：先查 Events / Standard events / Events editor
- 要改对象：先查 Objects / Objects Reference
- 要改变量：先查 Variables / Scene variables / Global variables / Object variables / Local variables
- 要改表达式：先查 Expressions
- 要循环处理对象：先查 For Each object event
- 要写 JavaScript 事件：先查 JavaScript Code events
- 要封装复用逻辑：先查 Functions / External Events / Link Events
- 要做对象分组：先查 Object groups
- 要做平台跳跃：先查 Platformer behavior / Platform behavior
- 要做声音音乐：先查 Audio / Sounds and music
- 要做场景跳转或重开：先查 Scene management / Change scene / Restart scene 相关文档
- 要做对象创建、删除、移动、位置判断：先查 Objects Reference 和 Common instructions reference

---

## 2. 官方文档入口清单

### 2.1 官方总入口

- GDevelop 官方文档首页：<https://wiki.gdevelop.io/>
- GDevelop 5 文档入口：<https://wiki.gdevelop.io/gdevelop5/>

### 2.2 事件系统

- Events：<https://wiki.gdevelop.io/gdevelop5/events/>
- Standard events：<https://wiki.gdevelop.io/gdevelop5/events/standard/>
- Events editor：<https://wiki.gdevelop.io/gdevelop5/interface/events-editor/>
- For Each object event：<https://wiki.gdevelop.io/gdevelop5/events/foreach/>
- Group of events：<https://wiki.gdevelop.io/gdevelop5/events/group/>
- Link events：<https://wiki.gdevelop.io/gdevelop5/events/link/>
- External Events：<https://wiki.gdevelop.io/gdevelop5/interface/events-editor/external-events/>
- Functions：<https://wiki.gdevelop.io/gdevelop5/events/functions/>
- JavaScript Code events：<https://wiki.gdevelop.io/gdevelop5/events/js-code/>

### 2.3 对象系统

- Objects：<https://wiki.gdevelop.io/gdevelop5/objects/>
- Objects Reference：<https://wiki.gdevelop.io/gdevelop5/all-features/object/reference/>
- Object groups：<https://wiki.gdevelop.io/gdevelop5/objects/object-groups/>
- Scene Editor：<https://wiki.gdevelop.io/gdevelop5/interface/scene-editor/>

### 2.4 变量系统

- Variables：<https://wiki.gdevelop.io/gdevelop5/all-features/variables/>
- Global variables：<https://wiki.gdevelop.io/gdevelop5/all-features/variables/global-variables/>
- Scene variables：<https://wiki.gdevelop.io/gdevelop5/all-features/variables/scene-variables/>
- Object variables：<https://wiki.gdevelop.io/gdevelop5/all-features/variables/object-variables/>
- Local variables：<https://wiki.gdevelop.io/gdevelop5/all-features/variables/local-variables/>

### 2.5 表达式与通用指令

- Expressions：<https://wiki.gdevelop.io/gdevelop5/events/expressions/>
- Events and control flow Reference：<https://wiki.gdevelop.io/gdevelop5/all-features/common-instructions/reference/>

### 2.6 允许的官方来源

优先且主要使用：

- <https://wiki.gdevelop.io/>
- <https://wiki.gdevelop.io/gdevelop5/>
- <https://docs.gdevelop.io/>
- <https://github.com/4ian/GDevelop>

非官方论坛、视频、博客只能作为辅助理解，不能作为最终实现依据。

---

## 3. 每次工作必须执行的流程

### Step 1：拆解任务涉及的 GDevelop 机制

先写出本次任务涉及哪些系统。

格式：

```text
本次任务涉及：
1. 事件系统：因为要……
2. 对象系统：因为要……
3. 变量系统：因为要……
4. 表达式系统：因为要……
5. 行为系统：因为要……
```

如果任务只涉及其中一部分，就只列相关部分。

### Step 2：查本地文档库

先检查已有的《GDevelop 官方文档摘录库》。默认文件名：

```text
GDEVELOP_OFFICIAL_DOC_CACHE.md
```

建议位置：

```text
references/AI专用/GDEVELOP_OFFICIAL_DOC_CACHE.md
```

如果文档库或本技能 references 里已经有本次任务相关条目，可以直接使用，不必每次重新联网查官方说明；但必须说明：

```text
已找到本地文档依据：
- 文档标题 / references 文件：
- 原始官方链接：
- 已验证项目：
- 适用机制：
- 本次使用方式：
```

对已经在 `references/` 中沉淀过、且用户确认“功能基本正常”的同类任务，优先读取对应 reference 作为依据；只要本次需求没有超出 reference 的适用范围，就不需要重复查官方文档。若需求超出 reference，仍必须补查官方文档。

### Step 3：如果本地文档库 / references 没有，就查官方文档

如果文档库没有对应依据，必须去 GDevelop 官方文档查。

优先查：

```text
https://wiki.gdevelop.io/gdevelop5/
```

只能优先使用官方 GDevelop 文档。非官方内容不能作为最终实现依据。

对于直接编辑项目 JSON 的任务，先用官方 Reference 确认机制语义、内部类型和参数，
再用当前项目中已经能够成功编译的同类事件确认实际序列化格式。Reference 页面描述的是
当前编辑器接口，但不能保证把表达式形式直接手写进任意历史项目 JSON 后仍可编译。

旧式内部类型不能盲目复制，新式内部类型也不能只看名称就盲写。每次新增或迁移指令后，
必须启动全新的 GDevelop 进程加载磁盘文件、生成预览，并检查生成的 JavaScript：

```text
不得出现 badVariable
不得出现 Unknown instruction - skipped
变量必须落到实际的 getVariables()/getGame().getVariables() 访问
对象能力动作必须落到实际 behavior/capability 调用
```

例如当前 `KnightRunner_Test` 的直接 JSON 中，变量动作必须沿用已验证可编译的
`ModVarGlobal` / `ModVarScene` 与 `VarGlobal` / `VarScene` 序列化格式；不能把
`GlobalVariable(Score)` 或 `SceneVariable(GameOver)` 当作字符串参数塞给
`SetNumberVariable` / `NumberVariable`。

### Step 4：把查到的内容写入文档库

每次查到新文档，都必须追加到 `GDEVELOP_OFFICIAL_DOC_CACHE.md`。

追加格式：

```text
## 文档条目：<机制名称>
- 官方标题：
- 官方链接：
- 查询日期：
- 适用范围：
- 关键结论：
1.
2.
3.
- 对本项目的用法：
- 不允许误用的地方：
```

示例：

```text
## 文档条目：Events
- 官方标题：Events - GDevelop documentation
- 官方链接：https://wiki.gdevelop.io/gdevelop5/events/
- 查询日期：2026-06-21
- 适用范围：GDevelop 事件系统、条件、动作、游戏逻辑
- 关键结论：
1. GDevelop 使用事件定义游戏逻辑。
2. 事件由条件和动作构成。
3. 条件会影响哪些对象实例被动作处理。
- 对本项目的用法：
修改障碍物生成、碰撞、Retry、Score、跳跃时，必须先确认事件条件和动作顺序。
- 不允许误用的地方：
不能只凭变量名猜测事件执行顺序。
```

### Step 5：再读取当前项目 JSON

在查完相关官方文档后，才允许读取或修改当前 GDevelop 项目 JSON。

读取时必须先列出：

```text
当前项目中与任务相关的对象：
当前项目中与任务相关的变量：
当前项目中与任务相关的事件：
当前项目中不能触碰的系统：
```

例如修改障碍物系统时：

```text
可触碰：
- NewSprite12
- ObstacleHitbox
- NextObstacleX
- LastObstacleX
- MaxObstacles
- ObstacleCount
- ObstacleGapRoll
不可触碰：
- KnightHorse 动画
- Ground_A / Ground_B 循环
- Mount1 背景循环
- ScoreText 显示
- Retry 逻辑
- BGM 音乐
- PlatformerObject 跳跃参数
```

### Step 6：只做最小改动

修改规则：

1. 只改本次任务必须改的事件。
2. 不重写整个 JSON。
3. 不删除无关对象。
4. 不改无关变量。
5. 不改资源路径。
6. 不改动画资源。
7. 不改已稳定的跳跃、地面、背景、音乐、Retry，除非任务明确要求。
8. 所有新增变量必须说明用途。
9. 所有新增事件必须说明触发条件。
10. 所有删除事件必须说明为什么删除。

### Step 7：输出修改报告

每次修改后，必须输出：

```text
修改了什么：
1.
2.
3.
没有改什么：
1.
2.
3.
依据的官方文档：
1. 文档标题 + 链接
2. 文档标题 + 链接
可能风险：
1.
2.
测试步骤：
1.
2.
3.
```

---

## 4. 硬性禁止规则

以下行为禁止：

1. 禁止只靠“模型内部逻辑”写 GDevelop 事件。
2. 禁止没查文档就直接改 JSON。
3. 禁止凭猜测写 GDevelop action / condition 参数。
4. 禁止把 JavaScript 逻辑硬塞进事件，除非先查 JavaScript Code events 文档。
5. 禁止为了一个问题重写整个项目。
6. 禁止修障碍物时顺手改地面、背景、跳跃、音乐、Retry。
7. 禁止没有说明依据就改变变量作用域。
8. 禁止把全局变量、场景变量、对象变量混用。
9. 禁止没有对象选择依据就批量操作实例。
10. 禁止文档里查不到还继续做。

---

## 5. “文档里没有就不做”规则

如果当前任务需要某个机制，但官方文档库和官方文档都没有查到明确依据，必须停止，并输出：

```text
我不能继续做这个修改。
原因：
当前任务需要使用 <机制名称>，但我没有在 GDevelop 官方文档中找到足够明确的依据。
如果继续写，会变成模型猜测，容易破坏项目。
我已经查过：
1. <链接>
2. <链接>
3. <链接>
目前能安全做的是：
1.
2.
目前不能安全做的是：
1.
2.
```

---

## 6. 本项目专用规则：《KnightRunner_Test》

本项目是 GDevelop 5 横版自动跑酷游戏。

已知核心对象：

```text
KnightHorse：玩家骑士
Ground_A / Ground_B：循环地面
Ground_Physics：隐形地面碰撞层
Mount1：远景山体背景
NewSprite12：树桩视觉障碍
ObstacleHitbox：障碍碰撞盒
go：Game Over 图案
re：Retry 按钮
ScoreText：分数 UI
```

已知核心变量：

```text
GlobalVariable(Score)
GlobalVariable(RunSpeed)
SceneVariable(GameOver)
SceneVariable(MaxObstacles)
SceneVariable(ObstacleCount)
SceneVariable(ObstacleState)
SceneVariable(GroupSize)
SceneVariable(GroupStartX)
SceneVariable(GroupLastX)
SceneVariable(GroupGap)
SceneVariable(PatternRoll)
SceneVariable(LastPattern)
SceneVariable(SamePatternCount)
SceneVariable(SpawnTriggerX)
SceneVariable(DoubleJumpAvailable)
SceneVariable(JumpKeyReleasedAfterFirstJump)
SceneVariable(DragonState)
SceneVariable(DragonWait)
```

项目修改底线：

```text
修障碍物时，不碰跳跃。
修跳跃时，不碰障碍物。
修 Retry 时，不碰地面循环。
修 Score 时，不碰碰撞盒。
修音乐时，不碰游戏逻辑。
```

---

## 7. 障碍物系统专用检查清单

每次修改木桩/障碍物前，必须先查或确认：

```text
1. Events 文档：事件条件和动作如何执行
2. Objects 文档：对象实例如何被事件操作
3. Objects Reference：创建、删除、移动对象的官方动作
4. Variables 文档：场景变量和全局变量如何使用
5. Expressions 文档：RandomInRange、GlobalVariable、Variable 等表达式用法
6. For Each 文档：如果要逐个处理对象实例，必须查 For Each
```

没有完成以上检查，不允许修改障碍物系统。

### 7.1 KnightRunner_Test 障碍组修复参考

已沉淀本项目障碍组生成修复细节：`references/knight-runner-obstacle-group-fix.md`。

处理 `NewSprite12 + ObstacleHitbox`、Chrome Dino 式障碍组、`GroupSize / GroupStartX / GroupLastX / GroupGap`、`ObstacleState`、`ScoreText`、Retry 残留清理时，先读该参考。

关键坑：替换生成 block 时不能从第一个 `GroupStartX` 事件开始，因为开局初始化事件也可能包含 `GroupStartX`；必须从障碍移动事件之后定位生成 block，并回读验证第 0 条事件仍是当前官方 `SceneJustBegins`。

### 7.2 KnightRunner_Test 大木桩尺寸变体参考

已沉淀 30% 概率生成大木桩、20% 放大、底部对齐、独立大碰撞盒的稳定做法：`references/knight-runner-big-stump-variant.md`。

当用户要求木桩随机大小变化/大木桩时，优先用独立对象 `NewSprite12Big` + `ObstacleHitboxBig`，不要直接缩放多实例 `NewSprite12`；每个木桩创建点单独 roll `ObstacleVariant`，并同步覆盖移动、删除、碰撞、开局清理。底部对齐时大木桩 Y 需要上移，不能只改尺寸。

已沉淀 Castle/V3/Retry 接入后木桩大小与频率回归排查：`references/knight-runner-obstacle-regression-compare-restore.md`。

当用户反馈“木桩大小和频率不对 / 跟 Castle 前能玩的版本不一样”时，不能只看对象定义或最近备份。必须检查 Create 动作是否实际创建 `NewSprite12Medium/NewSprite12Big`，并按用户指定的历史基准对齐；不要擅自换成更早/更晚的“看起来更完整”的版本。

已沉淀木桩分布回归审计与最小调参：`references/knight-runner-obstacle-distribution-audit-and-tuning.md`。

当用户反馈“木桩分布太平均 / 大小变化又没了 / 别动其他系统”时，必须只改障碍生成相关事件，并做回读审计：资源、对象、实例、变量是否 unchanged；明确列出 changed_event_indexes。常用稳定调参包括：`ObstacleCount >= 2` 放宽到 `>=3` 再强制单木桩、恢复每个创建点单独 roll 的普通/中号/大号三档尺寸、以及三段式 `GroupGap`（紧凑/普通/长间距）。

已沉淀木桩分布体感微调：`references/knight-runner-obstacle-distribution-tuning.md`。

当结构化 diff 显示木桩对齐历史版、但用户仍觉得分布不对时，要区分“代码一致”和“体感分布”。可用模拟统计屏幕内木桩数量、GroupSize 分布和 GroupGap；若用户明确同意，可只把两处 `ObstacleCount >= 2 && GroupSize > 1 -> GroupSize = 1` 放宽为 `ObstacleCount >= 3`，并验证资源/对象/实例/变量未改。

已沉淀按指定历史基准全量回归、只保留 Castle/V3/VC 终点流程的做法：`references/knight-runner-baseline-restore-keep-castle.md`。

当用户明确说“完整对照 17:00 那版 / Castle 之前那版，Castle 及相关事件保持，其他全面对齐”时，应以指定历史 JSON 为母版，只迁移 Castle/V3/VC 资源、对象、实例、变量、事件，并对障碍生成追加 `CastleVisible=0` 门控；不要在当前脏版本上继续叠补丁。

### 7.3 KnightRunner_Test 动态难度与音乐加速参考

已沉淀从指定分数开始加速、压缩障碍组间距、音乐随分数分档加速的稳定做法：`references/knight-runner-dynamic-difficulty-audio-speed.md`。

当用户反馈“还是简单 / 从某分数开始加速 / 间隔太大 / 音乐也跟着加速”时，优先调 `RunSpeed` 曲线与 `GroupGap`，不要先改跳跃；音乐变速优先复用当前项目已验证的 `PlayMusic` 第 5 参数，并用 `MusicSpeedLevel` 分档门控，避免每帧重放音乐。

### 7.3 KnightRunner_Test 核心系统回归修复参考

已沉淀二段跳、Retry、Score、跳高、Dragon2 速度、BestScore/flag、m1死亡动画、手机/鼠标点击跳跃的回归修复清单：`references/knight-runner-core-systems-regression-fix.md`。

当用户反馈“二段跳没了 / retry 没了 / 分数不走 / 跳不过木桩 / 红龙速度不对 / 跳太高会碰龙 / 鼠标点击和 Space 不一样 / flag 不对 / m1 位置不对”时，先读该参考。重点是：`SceneJustBegins` 保持项目约定的第一条顶层初始化事件；JSON 内部类型与参数必须以当前官方 Reference 为准；Retry 按用户要求选择“重载当前场景”或“显式原地重置”其中一种，禁止同时堆两套；Score 的周期与增量、Dragon2 的速度倍率、跳跃高度都属于需求参数，不能在技能中写死。跳跃手感目标通常是“第一段能过木桩且有约 30% 容错，二段跳不能碰到 Dragon2”，先小步调 `jumpSpeed / gravity / jumpSustainTime`，不要直接回到 1000+ 高跳；手机/鼠标点击要优先用官方 runtime `InputManager + simulateJumpKey()` 模拟 Space 按住，不再回退到普通 `MouseButtonFromTextReleased` 事件。

### 7.4 KnightRunner_Test Castle 终点 / Victory 参考

已沉淀 Castle 终点、终点前清障、胜利画面 V1/V3、胜利后隐藏顶部 UI 与骑士置顶规则：`references/knight-runner-castle-victory-finish.md`。

当用户新增 `Castle`、`V1/V3` 或要求“城堡是终点 / 城堡前没有障碍 / 胜利画面 / 骑士消失 / save the-pricess-M-数字消失”时，先读该参考。注意用户口头对象名可能和 JSON 实际对象名不同，必须先回读 objects/instances；Castle 是本局终点，不要和 `flag` 历史纪录点逻辑混用。

当前 Castle 稳定流程：正式终点放到 `297 + DistanceStart * 105`（当前 `DistanceStart=666`，即 `X=70227`）；骑士碰到 Castle 主体后隐藏骑士、停止 BGM、播放 `VC.mp3` 一次，Castle 继续滑出左侧后再显示 `V3` 和 `re`，不显示 `go/M/Best/ScoreDigit`。Castle 后清障必须带接近门槛（如 `Castle.X < 2600`），否则会开局就没有木桩；所有障碍生成链路加 `CastleVisible=0` 门控，但 `SceneJustBegins` 初始化事件条件必须保持只有 `SceneJustBegins`。不要依赖自定义 JSON 字段定位事件，GDevelop 保存可能清掉未知字段。

当 Castle/V3/VC 接入后用户要求“对照某个历史版本，Castle 相关保留，其他全面对齐”时，必须先读 `references/knight-runner-baseline-restore-keep-feature.md`；本次 17:00 基准对齐与木桩/鼠标回归细节另见 `references/knight-runner-baseline-alignment-keep-castle.md`。不要继续在当前脏版本上叠补丁；以用户指定历史版为母版，只白名单移植 Castle/V3/VC 相关资源、对象、实例、变量和事件，并做排除保留功能后的全量差异审计。用户只要求改 A 时，结果必须说明只改 A、未改 B/C；严禁修鼠标顺手动木桩、修 Castle 顺手动跳跃、修 UI 顺手动碰撞。

已沉淀基准版固化与网页版本地导出流程：`references/knight-runner-web-export-and-baseline.md`。

当用户说“保存这版作为基准版 / 发布网页版 / 先只导出网页版”时，必须先保护当前 JSON 与 autosave，同步写入 `BASELINE_CURRENT`，再导出。发布云端前先确认部署目录和 URL；若用户选择只导出，则只生成本地 `~/Desktop/hermes/GDevelop/KnightRunner_Test_web/` 与 zip，不上传。

已沉淀网页版 ZIP 与工程 JSON 成套恢复流程：`references/knight-runner-web-json-pair-restore.md`。

当用户要求恢复某个历史“完整备份”、8MB 优化版、或某时间点网页版时，先区分 Web zip/目录与工程 JSON；列出候选 ZIP 和候选 JSON，按 mtime/size/SHA 说明关系，用户确认后再恢复 JSON。恢复 Web 包需同步 `KnightRunner_Test_web/`、`KnightRunner_Test_web.zip`、`public-transfer/KnightRunner_Test_web.zip`；恢复 JSON 需先退出 GDevelop，并同步正式 JSON 与 `.autosave`。恢复前备份当前版本，替换目录用 Trash/Finder delete，不用 `rm`；恢复后回读验证 SHA、文件数、目录大小和 JSON parse OK。

已沉淀素材清理审计与网页版首局 BGM 解锁：`references/knight-runner-asset-cleanup-and-web-audio.md`。

当用户要求“检查素材、没用的删掉”时，必须先审计 JSON/resources/autosave/baseline/export 包引用，输出孤儿文件和坏引用清单，确认后才用 Trash 清理；不要直接删。用户反馈“网页版第一次没背景音乐，第二次才有”时，按浏览器 autoplay 策略处理：BGM 只在首次鼠标/触屏/Space 用户手势后启动，新增 `AudioUnlocked` 门控，并保留 Castle/GameOver 胜利门控，禁止顺手改木桩、跳跃、Castle 或 Retry。

已沉淀素材清理审计与网页版首局 BGM 解锁：`references/knight-runner-asset-cleanup-and-web-audio.md`。

当用户要求“检查素材/没用的素材删掉”时，必须先列出 JSON 引用、resources 缺失、孤儿文件和导出包引用情况；确认后用 Trash，不用 `rm`。当用户反馈“网页版第一次没背景音乐，第二次才有”时，按浏览器 autoplay 策略处理：BGM 只在首次鼠标/触屏/Space 用户手势后启动，保留 GameOver/Castle/Victory 门控，不动木桩、跳跃、Retry。

已沉淀素材审计清理与网页版首局 BGM 自动播放修复：`references/knight-runner-material-cleanup-and-audio-web.md`。

当用户要求“检查素材/没用的删掉”时，先按 JSON/autosave/BASELINE/导出包全量审计，列清单并确认后再移到废纸篓，不直接删；当网页版首局无背景音乐、第二局才有时，按浏览器自动播放策略处理：BGM 等首次鼠标/触屏/Space 用户手势后再启动，并同步更新导出包与 zip。

已沉淀素材瘦身、资源表清理和导出包减重流程：`references/knight-runner-asset-prune-size-optimization.md`，补充细节见 `references/knight-runner-web-asset-slimming.md`，本轮 Web BGM 与资源表严格瘦身补充见 `references/knight-runner-asset-pruning-audio-web-export.md`。

当用户反馈“包还是大/画面大小还能不能压缩/没用素材删掉”时，不要只压 PNG。必须检查未实例化、无事件引用的旧对象、`resources` 表残留、导出包 `.map` 和非活跃图片/音频；删除走废纸篓，同步 JSON/autosave 和导出包，验证 active resources 不缺失。关键坑：只删文件或只删导出包不够，GDevelop 会因为 JSON 对象和资源表残留继续把大图带进包；要按“活跃对象实例 + 事件文件引用”重算 active files，再清对象、resources、web 包三处。

当用户反馈“网页版第一次没背景音乐，第二次才有”时，按浏览器 autoplay 策略处理：开局先尝试播放以保留 GDevelop 预览体验；网页若被拦截，则在首次 Space/鼠标/触屏用户手势后补播。不要只加 `AudioUnlocked` 门控导致 GDevelop 预览开局 BGM 消失；也不要顺手改木桩、跳跃、Retry、Castle/V3/VC。

---

## 8. Retry 系统专用检查清单

每次修改 Retry 前，必须先查或确认：

```text
1. Events 文档
2. Scene / scene management 相关文档
3. Objects Reference：删除对象、创建对象
4. Variables 文档：重置全局变量和场景变量
5. Input / mouse / touch 相关文档
```

Retry 必须只有一个权威入口，并按需求选择一种策略：

1. **重载当前场景**：使用官方 `Scene` 动作切换到当前场景。官方定义是“停止当前场景并启动指定场景”，因此场景对象、场景变量、场景计时器和行为运行态会重新创建；`SceneJustBegins` 负责重新初始化全局分数与速度。
2. **原地重置**：只有用户明确要求不重载场景时，才逐项显式重置。

禁止在同一个 Retry 事件里先手工重置几十项、最后再 `Scene` 重载。这是重复逻辑，也容易让技能和项目状态互相矛盾。

原地重置策略才需要明确重置：

```text
Score
RunSpeed
GameOver
障碍物实例
go / re UI
玩家位置
跳跃相关状态
障碍生成状态
```

当前项目已通过预览编译验证的 JSON 内部类型：

```text
光标/触摸命中对象：IsCursorOnObject
鼠标按钮释放：MouseButtonFromTextReleased，参数含内部空参数和带引号的按钮字符串
切换/重载场景：Scene
场景计时器比较：CompareTimer
启动或重置场景计时器：ResetTimer
按键刚按下：KeyFromTextJustPressed
按键刚释放：KeyFromTextReleased
场景刚开始：SceneJustBegins
全局数值变量赋值/加减：ModVarGlobal，变量参数使用变量名（例如 Score）
场景数值变量赋值/加减：ModVarScene，变量参数使用变量名（例如 GameOver）
全局数值变量比较：VarGlobal
场景数值变量比较：VarScene
文字对象内容：TextContainerCapability::TextContainerBehavior::SetValue，行为参数为 Text
```

警告：`SetNumberVariable("GlobalVariable(Score)")` 和
`NumberVariable("SceneVariable(GameOver)")` 在本项目预览中会编译为 `badVariable`；
旧式 `Text` 动作会编译为 `Unknown instruction - skipped`。JSON 回读通过不代表运行有效。

### 8.1 运行时代码验收（直接修改 JSON 时强制执行）

1. 修改前比较正式 `.json` 与 `.json.autosave` 的 mtime/hash；如果 autosave 更新，优先从 autosave 读入，避免覆盖用户刚在编辑器内调过的参数。
2. 如果用户刚在编辑器里新增/调整了对象或实例（例如说“我加了一个 X 先别动”），必须先回读正式 JSON 和 autosave，确认该对象/实例已经落盘。若磁盘中都没有，或 AppleScript 保存/退出返回“用户已取消”，必须停止并让用户手动保存；禁止继续写入导致覆盖用户未保存编辑。
3. 同步写入正式文件与 `.autosave`。
4. 用新的 GDevelop 进程重新打开磁盘项目，避免编辑器内存中的旧版本覆盖文件。
4. 启动预览，定位本次预览生成的 `code0.js`。
5. 搜索 `badVariable` 和 `Unknown instruction - skipped`，任一出现即判定失败。
6. 搜索本次修改涉及的变量、对象和动作，确认生成了实际运行调用。
7. 最后再核对正式文件与 `.autosave` 内容一致。

### 8.2 KnightRunner_Test autosave 与 Dragon2 方向高度 / 层级安全

已沉淀本项目 autosave 取源、正式文件/自动保存同步、Dragon2 左→右/右→左分方向设 Y 的细节：`references/knight-runner-autosave-dragon-direction-y.md`。

### 8.3 KnightRunner_Test 网页版导出 / 云端发布

已沉淀本项目 GDevelop 网页版导出、preview 目录打包、本地 HTTP 验证、以及通过 mesh 先确认云端部署路径再发布的流程：`references/knight-runner-web-export-and-cloud-publish.md`。

当用户要求“导出网页版 / 发布一个网页版 / 发到云端”时，先区分导出与发布：用户选择“先只导出”时禁止上传云端；发布前必须通过 `hermes-mesh` 确认云端目录和对外 URL。若没有稳定 CLI，可用 GDevelop 生成的 `GDTMP-501/preview` 目录打包，但必须确认关键资源和本地 HTTP 可访问。

当用户刚在 GDevelop 里改过跳跃手感，又要求继续改 Dragon2 高度/方向运动时，必须先比较 `.json` 与 `.json.autosave`，优先保留较新的用户编辑状态；只改对应方向的状态切换事件，不要改全局实例初始 Y 后导致两个方向一起变。

已沉淀 Dragon2 避开骑士二段跳、公主和 UI 的当前项目稳定值：`references/knight-runner-dragon-height-layer-safety.md`。

用户明确纠正过：如果问题是“骑士二段跳最高碰到龙”，应改 Dragon2 高度/层级，不要改骑士跳跃高度。当前稳定方向值：右→左 `Y=90,zOrder=10000`；左→右 `Y=70,zOrder=9`；UI 数字/M/pricess 保持 `zOrder=10001/10002/10003`。

### 8.4 KnightRunner_Test 图片积分器

已沉淀本项目用桌面 `score.png` + `0.png`~`9.png` 替换文字分数 UI 的稳定做法：`references/knight-runner-image-score-counter.md`。

当用户要求“替换积分器/图片数字分数/score.png + 0-9.png”时，只替换显示层：新增 `ScoreLabel` 和 6 个 `ScoreDigit` 实例，用 `ScoreDigit` 的 10 个 animation 显示数字；保留 `GlobalVariable(Score)`、`ScoreTimer`、`RunSpeed` 原逻辑。可移除场景里的 `ScoreText` 实例，但不要删除 `ScoreText` 对象定义和旧 TextContainer 动作，降低误伤历史事件风险。

### 8.4.1 KnightRunner_Test 距离倒计时 / 速度波动 / 红龙安全高度

已沉淀本项目 `pricess + 3 位数字 + M` 距离倒计时、`SpeedPhase` 大幅波动速度、音乐跟随 RunSpeed、红龙避开 UI 与二段跳最高点的稳定做法：`references/knight-runner-distance-speed-dragon-tuning.md`。

当用户要求“倒计时从 666/999 开始、每秒减几米、速度有加速有减速、音乐跟着变、龙不能碰二段跳最高点”时，先读该参考。重点：不要把 `Score` 改成倒计时；新增/使用 `DistanceLeft`。调整“二段跳最高不碰龙”时优先改 Dragon2 高度，不改骑士跳跃，除非用户明确要求改跳跃手感。

### 8.4 KnightRunner_Test 图片积分器

已沉淀本项目用桌面 `score.png` + `0.png`~`9.png` 替换文字分数 UI 的稳定做法：`references/knight-runner-image-score-counter.md`。

当用户要求“替换积分器/图片数字分数/score.png + 0-9.png”时，只替换显示层：新增 `ScoreLabel` 和 6 个 `ScoreDigit` 实例，用 `ScoreDigit` 的 10 个 animation 显示数字；保留 `GlobalVariable(Score)`、`ScoreTimer`、`RunSpeed` 原逻辑。可移除场景里的 `ScoreText` 实例，但不要删除 `ScoreText` 对象定义和旧 TextContainer 动作，降低误伤历史事件风险。

### 8.4.1 KnightRunner_Test 距离倒计时 / 速度波动 / 红龙安全高度

已沉淀本项目 `pricess + 3 位数字 + M` 距离倒计时、`SpeedPhase` 大幅波动速度、音乐跟随 RunSpeed、红龙避开 UI 与二段跳最高点的稳定做法：`references/knight-runner-distance-speed-dragon-tuning.md`。

当用户要求“倒计时从 666/999 开始、每秒减几米、速度有加速有减速、音乐跟着变、龙不能碰二段跳最高点”时，先读该参考。重点：不要把 `Score` 改成倒计时；新增/使用 `DistanceLeft`。调整“二段跳最高不碰龙”时优先改 Dragon2 高度，不改骑士跳跃，除非用户明确要求改跳跃手感。

已沉淀 `pricess.png + 3位数字 + m.png` 距离倒计时做法：`references/knight-runner-distance-countdown-pricess.md`。

当用户要求“倒计时/米数/每秒 -N M/999M/pricess + M”时，不要反转 `Score`。新增并显示 `GlobalVariable(DistanceLeft)`；`Score` 继续作为内部累计进度。开局 `DistanceLeft=999` 和非开局 `DistanceTimer` 递减事件必须分开修改，避免把初始化误改成递减表达式。若用户要求“游戏本身速度每8s加一次速”，从 `ScoreTimer` 中移除连续 `RunSpeed` 公式，新增 `SpeedTimer >= 8` 的分档加速事件。

### 8.4.2 KnightRunner_Test Game Over UI / Best Record / Flag 记录点

已沉淀本项目 Game Over 结算 UI、`BestScoreM` 最高纪录、结尾 3 位 `ScoreDigit`、`Best/M` 只在死亡时显示、以及 `flag` 插在历史纪录地面点并跟随地面移动的稳定做法：`references/knight-runner-gameover-best-flag.md`。

当用户要求“game over/retry 显示出来让我调位置 / best score 记录 / 结尾 M 隐藏 / flag 是最高纪录点”时，先读该参考。重点：Game Over UI 保留场景实例方便拖动，运行时移到屏幕外隐藏；`BestScoreM` 必须用独立标准事件在运行中实时刷新，不要只在 Game Over JS 里顺手更新；`flag` 要使用本局开始时锁定的 `RunStartBestScoreM`，出现后跟地面 `RunSpeed * 60 * TimeDelta()` 左移，不要每帧重算成屏幕提示点。

### 8.5 KnightRunner_Test 二段跳单独降高度 + 死亡音效

### 8.6 KnightRunner_Test Game Over / Best Record / Flag 记录点

已沉淀本项目 Game Over 结算 UI、`BestScoreM` 历史最好成绩、结尾 `Best + 3位ScoreDigit + M`、以及赛道 `flag` 历史最远点路标的稳定做法：`references/knight-runner-gameover-best-flag-ui.md`。

当用户在编辑器中新增/复制 `Best`、结尾 `M`、额外 `ScoreDigit` 或 `flag` 后，先读该参考。重点：用户新增视觉资源默认不改；同名 `ScoreDigit/M` 必须用 `DigitRole` 区分顶部倒计时和结尾 best record；Game Over UI 用 `HomeX/HomeY` 显示、`(-2000,-2000)` 隐藏；`flag` 是运行中赛道记录点，不是结算 UI。

### 8.7 KnightRunner_Test 二段跳单独降高度 + 死亡音效

当用户要求“第一段跳不变，第二段跳高度降低”时，不改 `KnightHorse.PlatformerObject` 的 `jumpSpeed/gravity/jumpSustainTime` 基础参数；基础参数会影响第一段跳。稳定做法是在手动二段跳事件中，`PlatformBehavior::SetCanJump` + `PlatformBehavior::SimulateJumpKey` 后追加：

```text
PlatformBehavior::CurrentJumpSpeed(KnightHorse, PlatformerObject, =, <基础 jumpSpeed 的一半>)
```

当前基础 `jumpSpeed=820` 时，二段跳半高用 `410`。这样只改二段跳的当前上升速度，第一段跳保持原样。

当用户要求“骑士死亡时停止背景音乐并播放某个音效”时：

1. 将音频复制进项目目录，注册为 `kind=audio`、`preloadAsSound=true`。
2. 新增场景变量 `DeathAudioPlayed=0`，并在 `SceneJustBegins` 重置。
3. 不要把音效直接塞到两个碰撞事件里重复播放；新增一个独立死亡音频事件，条件等价于 `GameOver=1 && DeathAudioPlayed=0`，执行一次后置 `DeathAudioPlayed=1`。
4. 若普通事件内部类型无法确认，可用 JS Code 事件调用已存在的 `gdjs.evtTools.sound.stopMusic/stopMusicOnChannel/playSound/playSoundOnChannel`，但必须回读 JSON 并尽量启动预览检查 `badVariable`/`Unknown instruction - skipped`。

---

## 9. 输出格式模板

每次执行 GDevelop 任务时，必须按这个格式回答：

```text
# 本次任务：<任务名称>
## 1. 涉及机制
-
-
-
## 2. 已查官方文档
| 机制 | 官方文档 | 本次用途 |
|---|---|---|
| Events | <链接> | |
| Objects | <链接> | |
| Variables | <链接> | |
## 3. 当前项目检查
### 相关对象
-
### 相关变量
-
### 相关事件
-
### 不触碰系统
-
## 4. 修改方案
-
-
-
## 5. 修改内容
-
-
-
## 6. 为什么不会影响其他系统
-
-
-
## 7. 测试步骤
1.
2.
3.
## 8. 风险与限制
-
-
```

---

## 10. 最终工作原则

```text
先查官方文档。
再查项目 JSON。
只做最小改动。
每次记录文档。
没有文档，不做。
```

本技能不是为了“快速给答案”，而是为了避免 GDevelop 项目被模型误改。
