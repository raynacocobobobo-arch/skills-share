# KnightRunner_Test：Castle 后木桩大小/频率回归对比与恢复

适用：Castle/终点/V3/Retry 等逻辑接入后，用户反馈“木桩大小不对 / 频率不对 / 没木桩 / 跟之前能玩的版本不一样”。

## 背景结论

不要只拿最近一个“Castle 前”备份做基准。曾出现过这样的坑：

- `KnightRunner_Test.json.bak_mobile_tap_direct_double_20260621_170107` 虽然在 Castle 接入前，但障碍生成事件已经退化为只创建普通 `NewSprite12`。
- 它仍保留 `NewSprite12Medium / NewSprite12Big` 对象定义，所以只看对象表会误判“大小变体还在”。
- 真正带中/大/普通三档随机、频率也更接近用户满意状态的基准是：
  - `KnightRunner_Test.json.bak_dino_obstacle_group_20260621_164036`
  - SHA 前缀：`f63211b23da07414`

## 先做的验证

对比时不能只看事件数量或对象是否存在，必须同时检查：

```text
1. Create 动作是否实际创建：
   - NewSprite12
   - NewSprite12Medium
   - NewSprite12Big
   - ObstacleHitbox
   - ObstacleHitboxMedium
   - ObstacleHitboxBig
2. 每个创建点是否单独 ObstacleVariant = RandomInRange(1,100)
3. 中/大/普通三档概率是否仍在：
   - <=30：Medium
   - >30 且 <=60：Big
   - >60：Normal
4. GroupGap 是否仍是 16:37 那套较紧凑频率，而不是后续简化版：
   - 默认：RandomInRange(417 + RunSpeed*17, 542 + RunSpeed*28)
   - Roll <=20：RandomInRange(240 + RunSpeed*7, 310 + RunSpeed*12)
   - Roll >80：RandomInRange(633 + RunSpeed*32, 817 + RunSpeed*48)
   - GroupSize=2 追加 RandomInRange(17,75)
   - GroupSize=3 追加 RandomInRange(50,150)
5. 组内距离是否为：
   - GroupSize=2：RandomInRange(460,580)
   - GroupSize=3 第一段：RandomInRange(460,560)
   - GroupSize=3 第二段：RandomInRange(620,780)
```

## 恢复策略

如果当前项目的 Castle / V3 / Retry / 音频等后续功能需要保留，不要直接整文件回滚。

推荐做法：

1. 从 `bak_dino_obstacle_group_20260621_164036` 提取障碍运行时事件块：移动、生成、大小变体、频率、删除、碰撞。
2. 替换当前项目的障碍运行时事件块。
3. 保留当前 Castle 终点事件。
4. 给所有“生成/GroupSize/GroupGap/ObstacleVariant/ObstacleState”类事件追加 `CastleVisible = 0` 门控。
5. 不要给移动、出屏删除、碰撞事件加 `CastleVisible = 0`，否则终点阶段清理/碰撞状态会变脏。
6. `SceneJustBegins` 中恢复 16:37 障碍初始化和预置首组：
   - `GroupStartX = 1400`
   - `GroupGap = 900`
   - 开局创建两个普通木桩：`1400 / 1900`
   - `ObstacleCount = 2`
   - `GroupLastX = 1900`
   - `LastPattern = 2`
   - `SamePatternCount = 1`
7. Castle 清障事件只能在接近终点时触发，例如 `Castle.X < 2600`。

## 必须回读验证

恢复后用脚本校验：

```text
old_block 61
cur_norm 61
mismatches 0
Create counts:
  NewSprite12 = 6
  NewSprite12Medium = 6
  NewSprite12Big = 6
  ObstacleHitbox = 6
  ObstacleHitboxMedium = 6
  ObstacleHitboxBig = 6
Castle clear only one event:
  GameOver = 0 && Castle.X < 2600
formal JSON 与 autosave SHA 一致
```

其中 `cur_norm` 对比时允许删除 `CastleVisible=0` 条件再比，因为这是 Castle 终点新增门控，不属于木桩本体算法。

## 重要坑

- 只看“对象定义存在”不够；必须看 Create 动作是否真的创建中/大木桩。
- 只恢复 `GroupStartX=1400` 不够；大小变体和频率可能仍是简化版。
- 不要把 Castle 清障条件写进 `SceneJustBegins`。
- 不要把 `GroupStartX / GroupLastX = Castle.X() + 99999` 留在初始化里；它会导致开局没有木桩。
- 如果用户说“之前 Castle 前那版木桩蛮好”，先找真正包含大小变体 Create 动作的最近备份，而不是按时间最近的 Castle 前备份。