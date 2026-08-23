# Asset Bible

用于解决 AI 生成中的角色、场景和道具一致性问题。这是轻量视觉规范，不是资产管理系统。

使用原则：先建立核心资产，再生成镜头。不要直接用一句 Prompt 生成完整影片。

## 命名规则

简单使用 `类别_名称`：

- 角色：`character_robot`
- 场景：`location_factory`
- 道具：`prop_vehicle`
- 镜头：`shot_001`
- 需要版本：`character_robot_v02`

不要使用 `CHAR_ROBOT_V001_APPROVED_FINAL` 这类企业级命名。

## Character Asset Card

```text
角色：

一句话定位：

外观：

服装：

材质：

颜色：

关键识别点：

禁止变化：
```

## Location Asset Card

```text
场景：

地点：

时代：

建筑语言：

材质：

色彩：

光线：

固定元素：

禁止变化：
```

## Prop Asset Card

```text
道具：

功能：

结构：

材质：

时代：

识别元素：
```

## Asset Lifecycle

资产不是一次生成后直接使用，而是经过轻量迭代：

```text
Draft 初版探索

↓

Review 检查视觉方向

↓

Locked 锁定核心特征

↓

Production 进入镜头生产
```

规则：

- 不要在镜头阶段反复改变核心资产。
- 如果角色、场景发生重大变化，应重新生成版本，而不是覆盖旧资产。
- 版本只用于追踪变化，不需要复杂企业资产管理。

## Shot Reference Pack

资产进入具体镜头前，需要根据单个 Shot 组织引用包。

目的：不是保存素材，而是为生成提供明确输入。

```text
Shot:

Character:

Location:

Props:

Style Reference:

Camera Reference:

Reference Images:

Generation Purpose:
```

流程：

```text
Asset Bible
↓
Shot Reference Pack
↓
Generation
↓
Review
```

## 输出原则

- 先做 1-3 个核心资产，不要一次铺开全片资产库。
- 每个资产只保留生成时必须稳定的特征。
- “禁止变化”只写真正影响一致性的内容。
- 资产卡完成后，再进入分镜或 Prompt。
- Shot Reference Pack 只保留当前镜头真正需要的资产，不要无目的堆叠参考。