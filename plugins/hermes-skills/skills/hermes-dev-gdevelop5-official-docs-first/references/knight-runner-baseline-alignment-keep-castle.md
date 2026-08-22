# KnightRunner_Test：按指定基准版全量对齐，同时保留 Castle/V3/VC

适用场景：用户要求“对比 17:00 那版 / Castle 前那版 / 除 Castle 相关外全面对齐某个备份”。

## 核心原则

1. **用户指定的基准优先**：不要擅自改用“看起来更合理”的更早/更晚备份。
2. **以基准为母版最安全**：当用户要求全面对齐时，用基准 JSON 做底，再移植当前明确要保留的系统（如 Castle/V3/VC），不要在当前脏状态上继续叠补丁。
3. **允许差异白名单必须先列清楚**：例如 `Castle`、`V3`、`VC.mp3`、Castle 终点事件、胜利 BGM/UI 门控、鼠标/触屏修复。除此之外都应回到基准。
4. **不要把对象存在误判为实际生成**：对象定义里有 `NewSprite12Big/Medium` 不代表运行时会创建；必须统计 `Create` 动作。
5. **不要用自定义 JSON 字段定位事件**：GDevelop 保存可能清掉未知字段。用条件/动作/inlineCode 内容定位。

## 17:00 基准版事实

基准文件：`KnightRunner_Test.json.bak_mobile_tap_direct_double_20260621_170107`

该版本木桩事实：

```text
只实际生成普通木桩：
NewSprite12: 6
NewSprite12Medium: 0
NewSprite12Big: 0
ObstacleHitbox: 6
ObstacleHitboxMedium: 0
ObstacleHitboxBig: 0
```

虽然项目对象里存在中号/大号木桩对象，但 17:00 运行事件不会创建它们。

17:00 木桩频率：

```text
MaxObstacles = 3
开局预置 NewSprite12 X=1400 / 1900
GroupGap = RandomInRange(430 + GlobalVariable(RunSpeed) * 38,
                         620 + GlobalVariable(RunSpeed) * 55)
GroupSize = 2 时 GroupGap += RandomInRange(80,160)
GroupSize = 3 时 GroupGap += RandomInRange(180,300)
```

17:00 鼠标输入事实：

```text
MouseButtonFromTextReleased("Left")
```

这不是 Space 那种按住持续跳。若用户反馈鼠标第一段跳高度不对/鼠标没有二段跳，应只替换鼠标/触屏输入为 runtime JS，不能顺手改木桩或 Platformer 参数。

## 推荐合并流程

1. 退出 GDevelop，避免 autosave 覆盖。
2. 备份当前正式 JSON 和 autosave。
3. 读取指定基准 JSON 与当前 JSON。
4. 以基准 JSON 深拷贝为 `new`。
5. 从当前迁移白名单内容：
   - resources: `castle.png`、`V3.png`、`VC.mp3`
   - objects: `Castle`、`V3`
   - instances: `Castle`、`V3`
   - scene variables: `CastleVisible`、`CastleSpeedLocked`、`VictoryAudioPlayed`、`CastleTouched`、`VictoryPending`、`Win`
   - events: Castle 清障/移动/触碰/胜利显示相关事件
6. 给基准版木桩生成链路加 `CastleVisible=0` 门控，但不要改 `SceneJustBegins` 条件；Castle 清障必须带接近门槛（如 `Castle.X < 2600`）。
7. BGM/UI 只加胜利门控，不能改变死亡 GameOver 逻辑。
8. 写入正式 JSON 和 `.autosave`。

## 验证脚本逻辑

必须做语义归一化对比，避免 `1.0` vs `1` 误报。

对比项目：

```text
- resources：只允许多 castle.png / V3.png / VC.mp3
- objects：只允许多 Castle / V3；其他对象语义一致
- instances：只允许多 Castle / V3；其他实例语义一致
- scene variables：只允许多 Castle/Victory 变量和明确输入变量
- KnightHorse.PlatformerObject：必须与基准一致，除非用户明确要求改跳跃参数
- obstacle runtime events：剥掉 CastleVisible 门控后必须与基准一致
- obstacle Create 统计：必须与基准一致
- Retry 事件：仍为 GameOver=1 + IsCursorOnObject(re) + MouseButtonFromTextReleased + Scene
```

示例验证结果应包含：

```text
object_KnightHorse True
object_NewSprite12 True
object_ObstacleHitbox True
obstacle_runtime_17_match True
platform_behavior_match True
OLD/CUR obstacle_create_counts 一致
```

## 沟通要求

- 不要在只做了局部比对时说“完全一致”。
- 准确说法：`除 Castle/V3/VC/鼠标修复等白名单差异外，核心玩法系统已对齐基准`。
- 用户质疑“你确定吗”时，必须给验证项和不确定边界，不要用笼统保证。
- 用户提醒“让你改啥不要动其他的”时，后续每次改动都要先限定范围，并在结果里说明“未改哪些系统”。
