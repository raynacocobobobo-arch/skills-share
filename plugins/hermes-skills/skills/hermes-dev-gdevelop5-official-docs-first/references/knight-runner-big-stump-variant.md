# KnightRunner_Test：木桩尺寸变体（1.2x/1.4x 放大 + 底部对齐）

适用：用户要求木桩随机出现不同大小，例如“加一个更大的木桩，比现在大 20%/40%”“30% 概率出现大木桩，底部保持一样高度”“再加一个原来 1.2 倍的木桩，出现概率 30%左右”。

## 官方依据先行

本类任务至少确认：

- Objects / Objects Reference：对象、多实例、创建/删除/位置/碰撞。
- Scalable objects Reference：GDevelop 支持对象缩放能力，但多实例障碍直接缩放会受对象选择上下文影响。
- Variables / Expressions：用场景变量做随机概率门控，例如 `ObstacleVariant = RandomInRange(1,100)`。

## 稳定实现选择

对本项目，优先用“独立对象 + 独立资源 + 独立碰撞盒”，不要在同一个 `NewSprite12` 多实例上运行时缩放。

原因：

1. 障碍组一次可能创建 1~3 个 `NewSprite12`，直接对 `NewSprite12` 做缩放容易受当前对象选择影响。
2. 大木桩需要对应更大的碰撞盒；视觉缩放但碰撞不变会让玩家感觉“不准”。
3. 独立对象可以沿用同一套生成门控、移动、删除、碰撞逻辑，回读验证清晰。

## 本项目已验证形态

新增对象/资源：

```text
NewSprite12Big：大木桩视觉，当前图片约 224x94（原 160x67 放大约 40%）
ObstacleHitboxBig：大木桩碰撞盒，透明图 115x53（原 82x38 放大约 40%）
NewSprite12Medium：中号木桩视觉，图片约 192x80（原 160x67 放大约 20%，即 1.2x）
ObstacleHitboxMedium：中号木桩碰撞盒，透明图 98x46（原 82x38 放大约 20%）
ObstacleVariant：场景变量，1~100 随机；常见拆分为 <=30 出中号木桩、>30 且 <=60 出大木桩、>60 出普通木桩；若只启用一种变体，则 <=30 出该变体、>30 出普通木桩
```

### 四档尺寸（2026-06-22）

新增 1.5x 版本时继续使用独立对象与独立碰撞盒：

```text
NewSprite12XL：240x101，Y=531
ObstacleHitboxXL：123x57，X=木桩X+59，Y=575

ObstacleVariant 1~30：NewSprite12Medium（1.2x，30%）
ObstacleVariant 31~55：NewSprite12Big（1.4x，25%）
ObstacleVariant 56~65：NewSprite12XL（1.5x，10%）
ObstacleVariant 66~100：NewSprite12（普通，35%）
```

四个动态木桩创建点都必须独立 roll，并同步覆盖初始化清理、移动、出屏删除、Castle 清障、碰撞 Game Over，以及“木桩接近骑士半个身位时不突变速度”的碰撞盒名单。

底部对齐坐标：

```text
普通木桩：NewSprite12.Y = 565
中号 1.2x 木桩：NewSprite12Medium.Y = 552
大号 1.4x 木桩：NewSprite12Big.Y = 538

普通碰撞盒：ObstacleHitbox.X = 木桩X + 39，Y = 594
中号碰撞盒：ObstacleHitboxMedium.X = 木桩X + 47，Y = 586
大号碰撞盒：ObstacleHitboxBig.X = 木桩X + 55，Y = 579
```

说明：普通木桩底部约 `565 + 67 = 632`；中号 `552 + 80 = 632`；大号 `538 + 94 = 632`，视觉底部保持同一高度。碰撞盒同理向上/向右微调以贴合尺寸。旧 20% 版本资源是 `192x80 / 98x46 / Y=552 / hitbox Y=586`；40% 版本资源是 `224x94 / 115x53 / Y=538 / hitbox Y=579`。

## 生成事件改法

原始每个木桩创建点：

```text
Create NewSprite12 at X, 565
Create ObstacleHitbox at X + 39, 594
```

只启用一种大/中变体时，可替换为三段：

```text
ObstacleVariant = RandomInRange(1,100)

ObstacleVariant > 30
→ Create NewSprite12 at X, 565
→ Create ObstacleHitbox at X + 39, 594

ObstacleVariant <= 30
→ Create NewSprite12Big 或 NewSprite12Medium at X, 对应Y
→ Create ObstacleHitboxBig 或 ObstacleHitboxMedium at X + 对应偏移, 对应Y
```

同时启用 1.2x 中号与 1.4x 大号时，使用三档概率，避免互相覆盖：

```text
ObstacleVariant = RandomInRange(1,100)

ObstacleVariant <= 30
→ Create NewSprite12Medium at X, 552
→ Create ObstacleHitboxMedium at X + 47, 586

ObstacleVariant > 30 且 <= 60
→ Create NewSprite12Big at X, 538
→ Create ObstacleHitboxBig at X + 55, 579

ObstacleVariant > 60
→ Create NewSprite12 at X, 565
→ Create ObstacleHitbox at X + 39, 594
```

多木桩组里每一个木桩都要单独 roll 一次；不要只在组开头 roll 一次，否则整组会全大或全小。

## 间距/难度不平均化补丁

当用户反馈“木桩太平均 / 没难度”，可在不改跳跃手感的前提下调整障碍生成节奏：

1. 提高多木桩组概率：
   - 中期（Score 600~2500）：`PatternRoll > 55 -> GroupSize=2`（原 >65）。
   - 后期（Score >=2500）：`PatternRoll 36~80 -> GroupSize=2`，`>80 -> GroupSize=3`（原 46~85 / >85）。
2. 组间距用三段式随机，不再单一均匀区间：
   - 先 `Roll = RandomInRange(1,100)`。
   - 默认普通间距：`RandomInRange(580 + RunSpeed*24, 760 + RunSpeed*42)`。
   - `Roll <= 30` 时紧凑间距：`RandomInRange(420 + RunSpeed*16, 520 + RunSpeed*24)`。
   - `Roll > 80` 时长间距：`RandomInRange(860 + RunSpeed*45, 1180 + RunSpeed*70)`。
3. 组内最小间隔要留“至少一个木桩”距离，尤其 40% 大木桩宽 224：
   - GroupSize=2 内间距用 `RandomInRange(460,580)`。
   - GroupSize=3 第一段用 `RandomInRange(460,560)`，第二段用 `RandomInRange(620,780)`。
4. 组后距离附加值可减小波动尾巴：GroupSize=2 `+ RandomInRange(40,130)`；GroupSize=3 `+ RandomInRange(100,240)`。

不要把组内间距压到低于 400，否则大木桩会接近重叠；用户明确要求“不能两个完全叠一起，至少中间隔一个木桩”。

## 必须同步修改的事件

1. `SceneJustBegins`：初始化 `ObstacleVariant = 0`，并删除所有变体对象：`NewSprite12Big / ObstacleHitboxBig / NewSprite12Medium / ObstacleHitboxMedium`。
2. 移动事件：所有变体视觉对象和碰撞盒都跟随 `RunSpeed` 左移。
3. 删除事件：
   - `NewSprite12Big.X < -220 -> Delete NewSprite12Big`
   - `ObstacleHitboxBig.X < -220 -> Delete ObstacleHitboxBig`，并和普通 hitbox 一样更新 `ObstacleCount`。
   - `NewSprite12Medium.X < -220 -> Delete NewSprite12Medium`
   - `ObstacleHitboxMedium.X < -220 -> Delete ObstacleHitboxMedium`，并和普通 hitbox 一样更新 `ObstacleCount`。
4. 碰撞事件：复制普通 `ObstacleHitbox` 的 GameOver 事件，碰撞对象分别改为 `ObstacleHitboxBig` / `ObstacleHitboxMedium`。
5. 生成事件：所有 GroupSize=1/2/3 的每个创建点都要接入 `ObstacleVariant`。如果后续新增尺寸变体，要改概率分段，而不是在同一个阈值上叠加多个分支。

## 重要坑

- 如果 GDevelop 正开着，先保存并退出，再直改 JSON；否则编辑器内存可能覆盖磁盘补丁。
- 修改 `.json` 时必须同步写 `.json.autosave`。
- 修改前备份正式 JSON 和 autosave。
- 不要只改视觉对象而不改碰撞盒。
- 不要改 `KnightHorse` 跳跃参数来适配大木桩，除非用户明确要求调手感。
- 不要把 `ObstacleCount` 变成按视觉对象统计；仍以碰撞盒出屏删除来递减，普通和大 hitbox 都要覆盖。

## 回读验证清单

```text
formal JSON 与 autosave SHA 一致
layout.events[0] 仍是 SceneJustBegins
存在 NewSprite12Big / ObstacleHitboxBig 对象
存在 ObstacleVariant 初始化与 RandomInRange(1,100)
每个木桩创建点都有 >30 普通 / <=30 大木桩分支
NewSprite12Big / ObstacleHitboxBig 都随 RunSpeed 移动
NewSprite12Big / ObstacleHitboxBig 都有出屏删除事件
ObstacleHitboxBig 有 CollisionNP -> GameOver 事件
普通 NewSprite12 / ObstacleHitbox 逻辑仍保留
Retry / Score / Double Jump / RunSpeed / Dragon 未被修改
```
