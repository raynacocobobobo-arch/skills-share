# KnightRunner_Test 木桩分布微调：只改限制阈值

## 适用场景

用户反馈木桩分布“感觉不太对”，但要求保留 17:00 基准的整体木桩逻辑，只想让中后期更容易出现 2 个木桩组。

## 用户偏好/硬约束

- 只改用户指定项；修木桩不碰跳跃、Castle、Retry、UI、音乐。
- 不要把“代码与基准一致”当作“体感一定正确”。需要区分：
  - 结构化 diff 一致；
  - 模拟/实玩分布是否符合预期。
- 每次改动后明确列出：改了哪些事件；哪些资源/对象/实例/变量未改。

## 已验证基准

17:00 基准文件：

```text
KnightRunner_Test.json.bak_mobile_tap_direct_double_20260621_170107
```

17:00 木桩特征：

- 只实际生成普通 `NewSprite12` + `ObstacleHitbox`。
- `NewSprite12Medium/NewSprite12Big` 对象存在，但 Create 动作数量为 0。
- `MaxObstacles = 3`。
- 开局预置两个普通木桩：`X=1400`、`X=1900`。
- `GroupGap = RandomInRange(430 + GlobalVariable(RunSpeed) * 38, 620 + GlobalVariable(RunSpeed) * 55)`。

## 分布问题根因

17:00 逻辑中有两处事件会把多木桩组压成单木桩：

```text
条件：ObstacleCount >= 2 且 GroupSize > 1
动作：GroupSize = 1
```

由于屏幕里常驻 1~2 个木桩，`ObstacleCount >= 2` 很容易成立，导致中后期 2/3 木桩组几乎生成不出来。

## 推荐微调

只把两处条件改为：

```text
ObstacleCount >= 3 且 GroupSize > 1
→ GroupSize = 1
```

当前已验证目标事件索引为 42、49（索引可能随事件插入变化；不要硬编码索引，应按条件+动作精确匹配）：

匹配规则：

- action 包含 `ModVarScene ['GroupSize','=','1']`
- condition 包含 `VarScene ['GroupSize','>','1']`
- condition 包含 `VarScene ['ObstacleCount','>=','2']`

修改后验证：

- 不再存在 `ObstacleCount >= 2` 的强制单木桩事件。
- 只存在两处 `ObstacleCount >= 3` 的强制单木桩事件。
- resources / objects / instances / variables 必须保持不变。
- 正式 JSON 与 `.autosave` hash 一致。

## 典型验证输出

```text
changed_event_indexes [42, 49]
remaining_force_limit_2 []
force_limit_3 [(42, ['ObstacleCount', '>=', '3']), (49, ['ObstacleCount', '>=', '3'])]
unchanged_non_events {'resources': True, 'objects': True, 'instances': True, 'variables': True}
formal_autosave_same True
```

## 注意

如果用户要求“对齐 17:00”，不要做此微调；这属于有意偏离 17:00 分布。只有用户明确同意把阈值从 2 改到 3 时再做。
