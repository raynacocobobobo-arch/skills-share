# KnightRunner_Test：以历史基准版为母版，仅保留指定功能的回归恢复流程

## 触发场景

用户反馈“Castle 之后一堆 bug / 木桩大小和频率不对 / 对比某个时间点版本 / 除某功能外全面对齐某版本”时使用。

典型指令：

```text
完整对照 17:00 那版看，castle及相关事件保持，其他全面对齐17:00
```

## 核心原则

不要在当前脏版本上继续叠补丁。正确做法是：

1. 找到用户指定的历史基准 JSON。
2. 以该基准 JSON 作为母版。
3. 只把用户明确要求保留的新功能对象/资源/实例/变量/事件移植过去。
4. 对移植功能需要的最小门控做局部 patch。
5. 做“排除保留功能后的全量差异审计”。

## 这次确认过的 17:00 基准事实

基准文件：

```text
KnightRunner_Test.json.bak_mobile_tap_direct_double_20260621_170107
```

该版木桩系统实际特征：

```text
只生成普通 NewSprite12 / ObstacleHitbox
NewSprite12Medium/NewSprite12Big 对象存在，但生成事件不创建它们
开局预置普通木桩：X=1400、X=1900
MaxObstacles = 3
GroupGap = RandomInRange(430 + GlobalVariable(RunSpeed) * 38, 620 + GlobalVariable(RunSpeed) * 55)
GroupSize = 2 时 GroupGap += RandomInRange(80,160)
GroupSize = 3 时 GroupGap += RandomInRange(180,300)
Score 门槛：1500 / 4000
```

注意：不能只看对象定义判断“有中/大木桩”。必须统计 `Create` 动作实际创建了哪些对象。

## Castle/V3/VC 保留范围

当用户要求“Castle 及相关事件保持”时，保留范围通常仅包括：

```text
资源：castle.png、V3.png、VC.mp3
对象：Castle、V3
实例：Castle、V3
场景变量：CastleVisible、CastleSpeedLocked、VictoryAudioPlayed、CastleTouched、VictoryPending、Win
事件：Castle 接近清障/降速、Castle 移动、Castle 触碰播放 VC、Castle 滑出后显示 V3/retry
必要门控：障碍生成链路加 CastleVisible=0
必要音频门控：VictoryPending/CastleTouched/Win 时 BGM 不重启
必要 UI 覆盖：Win=1 时隐藏 go/M/Best/ScoreDigit，只显示 V3 和 re
```

## 推荐实现流程

### 1. 退出 GDevelop

先让编辑器退出，避免 autosave 覆盖。

### 2. 备份当前正式 JSON 和 autosave

命名建议：

```text
.bak_full_align_<baseline>_keep_<feature>_<timestamp>
```

### 3. 读取三份文件

```text
baseline = 用户指定历史版本
current = 当前含新功能版本
autosave = 当前自动保存版本
```

如果当前 autosave 更新且包含用户刚做的对象/实例，先以 autosave 作为 current。

### 4. 以 baseline 深拷贝作为 new

```python
new = copy.deepcopy(baseline)
```

不要从 current 删除无关内容来“恢复”，那样很容易漏脏状态。

### 5. 从 current 移植保留功能

按白名单移植：

```text
resources：名称/路径含 Castle、V3、VC.mp3
objects：Castle、V3
instances：Castle、V3
variables：CastleVisible、CastleSpeedLocked、VictoryAudioPlayed、CastleTouched、VictoryPending、Win
runtime events：只含 Castle/V3/VC/VictoryPending/CastleTouched/CastleVisible 的终点事件
```

不要移植障碍系统、跳跃系统、Score、Retry、龙、地面等非白名单内容。

### 6. 对 baseline 的障碍生成事件加最小 Castle 门控

只给“生成链路”加：

```text
CastleVisible = 0
```

不要加到：

```text
SceneJustBegins 初始化事件
障碍移动事件
离屏删除事件
碰撞死亡事件
```

否则会导致开局无木桩、木桩不移动、碰撞失效等回归。

### 7. 验证点

必须验证：

```text
正式 JSON 和 autosave SHA 一致
排除 Castle/V3/VC/胜利变量/必要门控后，非 Castle 对象定义与 baseline 一致
排除 Castle/V3 后，场景实例与 baseline 一致
木桩 Create 动作数量与 baseline 一致
GroupGap / MaxObstacles / 开局预置障碍与 baseline 一致
Castle 事件存在：接近清障、触碰 VC、滑出后 V3+re
VC.mp3 / castle.png / V3.png 文件存在且资源注册
```

## 关键坑

1. **不要默认“最近备份”就是用户认为好玩的版本。** 用户说 17:00，就必须用 17:00。
2. **对象存在不等于参与生成。** 必须统计 `Create` 动作。
3. **不要在脏版本上连续 patch。** 多轮 patch 后事件顺序、初始化动作、门控很容易叠坏。
4. **GDevelop 会清理未知 JSON 字段。** 不要依赖自定义 `hermesXXX` 标记定位事件。
5. **Castle 清障必须有接近门槛。** 如 `Castle.X < 2600`；否则 Castle 在远方终点时也会关掉木桩。
6. **SceneJustBegins 条件必须保持干净。** 不能给初始化事件加 Castle 条件。
7. **保留功能要白名单移植。** 不是把 current 的所有新增内容都搬过去。
