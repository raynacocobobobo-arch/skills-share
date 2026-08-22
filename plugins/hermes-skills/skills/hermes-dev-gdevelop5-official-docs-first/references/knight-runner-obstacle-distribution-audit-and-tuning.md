# KnightRunner_Test：木桩分布回归审计与最小调参

适用：用户反馈“木桩大小没了 / 频率不对 / 分布太平均 / 跟某个历史版不一样”，尤其是在 Castle/V3/VC 终点流程接入后。

## 核心原则

1. 用户让改 A，只改 A；不要顺手动跳跃、Castle、Retry、Score、BGM、对象资源。
2. 用户指定历史基准（如“17:00 那版”）时，先按该基准做结构化对比；不要擅自换成更早/更晚的版本。
3. “对象存在”不等于“生成逻辑使用”。必须检查 `Create` 动作是否实际创建 `NewSprite12Medium/NewSprite12Big`。
4. 如果用户既要“对齐历史版”又要“木桩大小变化”，要明确：历史版可能不含大小变体；此时只恢复大小变体生成，不改频率/跳跃/终点流程。

## 本次沉淀的稳定状态

在保留 Castle/V3/VC 的前提下，木桩可用状态为：

- 每个动态木桩创建点单独 roll：`ObstacleVariant = RandomInRange(1,100)`。
- `<=30`：`NewSprite12Medium` + `ObstacleHitboxMedium`。
- `>30 && <=60`：`NewSprite12Big` + `ObstacleHitboxBig`。
- `>60`：`NewSprite12` + `ObstacleHitbox`。
- 频率限制从 `ObstacleCount >= 2` 改为 `ObstacleCount >= 3` 时才强制 `GroupSize = 1`。
- GroupGap 改成三段式：紧凑 / 普通 / 长间距，避免平均撒点。

## 精确修改点

### 1. 放宽多木桩组限制

只改两条“强制 GroupSize=1”的事件条件：

```text
ObstacleCount >= 2 且 GroupSize > 1
改为：ObstacleCount >= 3 且 GroupSize > 1
```

验证：

```text
remaining_force_limit_2 == []
force_limit_3 包含两条事件
资源/对象/实例/变量均 unchanged
```

### 2. 恢复木桩大小变体

动态创建点不是 3 个，而是 4 个：

1. GroupSize>=1 的第一个木桩
2. GroupSize=2 的第二个木桩
3. GroupSize=3 的第二个木桩
4. GroupSize=3 的第三个木桩

每个创建点都要拆成：

```text
Roll ObstacleVariant
Medium 分支
Big 分支
Normal 分支
原来的 GroupLastX / ObstacleCount 等副作用事件
```

不要只在组开头 roll 一次，否则整组同尺寸。

### 3. 三段式 GroupGap

替换运行时基础 GroupGap，不改开局初始化里的 GroupGap：

```text
Roll = RandomInRange(1,100)
Roll <= 30:
  GroupGap = RandomInRange(420 + RunSpeed*16, 520 + RunSpeed*24)
Roll > 30 && Roll <= 80:
  GroupGap = RandomInRange(580 + RunSpeed*24, 760 + RunSpeed*42)
Roll > 80:
  GroupGap = RandomInRange(860 + RunSpeed*45, 1180 + RunSpeed*70)
```

组后附加：

```text
GroupSize=2: + RandomInRange(40,130)
GroupSize=3: + RandomInRange(100,240)
```

## 回归审计方法

修改前后必须输出以下检查，避免用户再次质疑“是不是又动了木桩/跳跃”：

```text
resources unchanged?
objects unchanged?
instances unchanged?
variables unchanged?
formal/autosave same?
changed_event_indexes?
```

针对大小变体：

```text
dynamic_create_counts_excluding_init:
NewSprite12: 4
NewSprite12Medium: 4
NewSprite12Big: 4
ObstacleHitbox: 4
ObstacleHitboxMedium: 4
ObstacleHitboxBig: 4
```

针对频率限制：

```text
limit2_remaining []
limit3 两条
```

针对三段式间距：

```text
tight True
normal True
long True
old_runtime False
add2_new True
add3_new True
old_add_runtime False
```

## 重要坑

- GDevelop 保存后会清理未知自定义字段，不能依赖自定义 JSON 标记定位事件。
- 插入/拆分事件后事件编号会变化，不能硬编码 53/55/57/59/76；只能用条件和动作内容定位。
- 只对运行时 `ObstacleState=1` 的 GroupGap 改三段式；开局初始化 `SceneJustBegins` 里的 GroupGap 可以保持原值。
- 用户对“只改这个，别动别的”非常敏感。最终回复必须明确列出未改项，并用回读校验支撑。
