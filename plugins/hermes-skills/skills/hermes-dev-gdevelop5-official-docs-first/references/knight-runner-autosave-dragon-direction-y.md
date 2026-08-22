# KnightRunner_Test：autosave 取源与 Dragon2 方向分层高度

## 触发场景

用户在 GDevelop 编辑器中刚改过跳跃/手感参数，随后要求继续直接修改 JSON，例如：

- “dragon 从画左往画右飞的那个可以再低一点”
- 修改 Dragon2 的单方向高度、速度、等待时间
- 修改项目 JSON 时发现正式 `.json` 与 `.json.autosave` 不一致

## 关键经验

1. **正式文件不是永远的最新源。**  
   如果 `KnightRunner_Test.json.autosave` 的 mtime 晚于正式 `KnightRunner_Test.json`，且内容 hash 不一致，优先用 autosave 作为读入源，否则可能覆盖用户刚在编辑器里改出的跳跃/手感参数。

2. **写回必须同步正式文件与 autosave。**  
   直接修改后，将同一份 JSON 同步写入：
   - `KnightRunner_Test.json`
   - `KnightRunner_Test.json.autosave`

3. **修改前分别备份正式文件和 autosave。**  
   备份名要带任务语义和时间戳，例如：
   - `.bak_dragon_left_to_right_lower_YYYYMMDD_HHMMSS`

4. **Dragon2 左→右与右→左是状态机，不要只改实例初始 Y。**  
   当前项目中：
   - `DragonState = 0`：右侧出发，向左飞
   - `DragonState = 1`：左侧等待
   - `DragonState = 2`：左侧出发，向右飞
   - `DragonState = 3`：右侧等待

5. **只降低左→右飞行时，应在状态切换事件里设 Y。**  
   例：用户说“从画左往画右飞低 50”，不是把 Dragon2 全局初始 Y 改低，而是：
   - 在 `DragonState = 1` 且 `DragonWait >= 5` 的事件中，`MettreX Dragon2 = -420` 后插入 `MettreY Dragon2 = 74`（原 24 + 50）
   - 在 `DragonState = 3` 且 `DragonWait >= 5` 的事件中，`MettreX Dragon2 = 1500` 后插入 `MettreY Dragon2 = 24`，恢复右→左原高度

6. **必须验证不覆盖核心手感参数。**  
   修改后回读 `KnightHorse.PlatformerObject`，确认用户刚调过的参数仍保留，例如：
   - `jumpSpeed`
   - `gravity`
   - `jumpSustainTime`
   - `maxFallingSpeed`
   - `ignoreDefaultControls`
   - `useRepeatedJump`

## 最小验证清单

修改后至少回读确认：

```text
1. 正式文件与 autosave hash 一致
2. DragonState=1 / DragonWait>=5 事件里包含 MettreY Dragon2 = 目标低位 Y
3. DragonState=3 / DragonWait>=5 事件里包含 MettreY Dragon2 = 原始 Y
4. SceneJustBegins 仍是第 0 条初始化事件
5. KnightHorse 平台跳跃参数未被回滚
```

## 用户要求“你拉吧/你来打开项目”的安全流程

当 GDevelop 已经打开且用户反馈“没变/没有啊”后，不要继续在打开状态下反复写 JSON 再 `open`。稳定流程：

```text
1. 先把当前确认正确的 formal JSON 备份。
2. 用 osascript 退出 GDevelop 5，并用 pgrep 确认已退出。
3. 若仍有 GDevelop 进程，必要时 pkill，防止编辑器内存/autosave 再覆盖磁盘文件。
4. 退出后，把确认正确的同一份 JSON 写回 formal 与 .autosave。
5. 回读 formal/.autosave SHA、关键事件值、实例值。
6. 再 open -a "GDevelop 5" <项目 JSON>。
```

这类场景的“完成”标准不是只写入文件，而是：退出旧编辑器 → 写回 → 回读一致 → 新进程打开。

## Dragon2 方向层级

若用户要求“从画左往画右飞时放在骑士后面”，当前项目可用已验证动作 `ChangePlan` 设置 zOrder：

```text
KnightHorse zOrder = 10
DragonState=1 -> DragonState=2 左→右起飞事件：ChangePlan Dragon2 = 9
DragonState=3 -> DragonState=0 右→左起飞事件：ChangePlan Dragon2 = 10000
SceneJustBegins 右→左初始：ChangePlan Dragon2 = 10000
```

注意：只改实例初始 zOrder 不够，方向状态切换事件也会决定运行时前后关系。

## 避坑

- 不要因为正式 `.json` 存在就忽略 `.autosave`；GDevelop 打开状态下 autosave 常常包含最新编辑器状态。用户刚预览/打开编辑器后，autosave 可能立刻变成最新源，必须重新比较 mtime/hash。
- 不要只改 Dragon2 实例初始 `y`；状态机重置 X 时会决定下一段飞行，应在对应方向的起飞事件里改 Y。
- 如果用户说“没看见改/没变化”，不要坚持“文件已改”。按用户预览体感判定为未达标：重新读取最新 autosave，回读所有 `MettreY Dragon2` 和实例初始 `y`，必要时再按当前磁盘值继续增量调整，并同步正式文件/autosave。
- 重新打开 GDevelop 不等于预览已加载新状态；最终以 JSON 回读数值 + 用户新预览反馈为准。
- 不要为了改龙高度顺手改跳跃、Retry、Score、障碍组。