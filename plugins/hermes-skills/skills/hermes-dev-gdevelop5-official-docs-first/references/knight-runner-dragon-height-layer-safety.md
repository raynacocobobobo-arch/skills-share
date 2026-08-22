# KnightRunner_Test：Dragon2 高度、层级与骑士/公主/UI 避让

## 触发场景

用户连续反馈：

- “龙整体往上/往下”
- “龙不能碰到骑士”
- “不能碰到公主和分数”
- “骑士二段跳最高不能碰到龙”
- “从画左往画右飞的动作放在骑士图层的后面”

## 关键原则

1. **如果用户说二段跳最高碰到龙，优先改 Dragon2 高度，不改骑士跳跃。**  
   用户明确纠正过：这是龙高度问题，不是骑士跳跃高度问题。

2. **左→右与右→左是两套状态机高度。**

```text
DragonState = 0：右侧出发，向左飞
DragonState = 1：左侧等待
DragonState = 2：左侧出发，向右飞
DragonState = 3：右侧等待
```

3. **层级要按飞行方向切换。**

```text
右→左：Dragon2 zOrder = 10000
左→右：Dragon2 zOrder = 9，放在 KnightHorse(zOrder=10) 后面
UI：ScoreDigit 10001，M 10002，pricess 10003
```

## 当前项目最终稳定值

用户最终要求：龙不能碰骑士二段跳最高点，同时不碰公主/数字/M。

当前稳定值：

```text
开局 / 右→左：Y = 90, zOrder = 10000
左→右：Y = 70, zOrder = 9
回右侧 / 右→左：Y = 90, zOrder = 10000
Dragon2 实例初始 y = 90, zOrder = 10000
```

注意：GDevelop 坐标 Y 越小越靠上。用户说“龙太低”时，要减小 Y。

## 修改位置

### SceneJustBegins

```text
MettreX Dragon2 = 1400
MettreY Dragon2 = 90
FlipX Dragon2 = no
ChangePlan Dragon2 = 10000
```

### DragonState = 1 且 DragonWait >= 5（左→右起飞）

```text
MettreX Dragon2 = -420
MettreY Dragon2 = 70
FlipX Dragon2 = yes
ChangePlan Dragon2 = 9
DragonState = 2
DragonWait = 0
```

### DragonState = 3 且 DragonWait >= 5（右→左起飞）

```text
MettreX Dragon2 = 1500
MettreY Dragon2 = 90
FlipX Dragon2 = no
ChangePlan Dragon2 = 10000
DragonState = 0
DragonWait = 0
```

## 避坑

- 不要只改 Dragon2 场景实例初始 y；状态切换事件会覆盖运行时高度。
- 不要在等待事件或越界切状态事件里插入孤立 `ChangePlan Dragon2`；只在真正起飞/开局定位事件里设置层级。
- 不要因为用户说“二段跳碰龙”就降低 `KnightHorse` 跳跃参数；用户明确要求动龙，不动骑士。
- 如果 GDevelop 正在打开，autosave 可能覆盖正式 JSON：修改前比较 formal/autosave；修改后退出 GDevelop、重写 formal/autosave、再打开。
- 回答时如果只是回读 JSON，不要说“确定有效”；以用户新预览为准。

## 回读验证清单

```text
formal JSON 与 autosave SHA 一致
Dragon2 场景实例 y=90, zOrder=10000
SceneJustBegins 中 Dragon2 MettreY=90 + ChangePlan=10000
左→右起飞事件中 MettreY=70 + ChangePlan=9
右→左起飞事件中 MettreY=90 + ChangePlan=10000
没有其他孤立 Dragon2 ChangePlan 动作
KnightHorse PlatformerObject 参数未变
跳跃事件未被改动
UI zOrder：ScoreDigit 10001，M 10002，pricess 10003
```