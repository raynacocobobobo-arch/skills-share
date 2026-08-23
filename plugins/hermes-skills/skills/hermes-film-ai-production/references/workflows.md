# AI Film Workflows

整体流程：

```text
用户需求 -> Project Start -> Concept Development -> Visual Analysis -> Asset Bible -> Shot Design -> Prompt Engineering -> Review
```

## Asset To Video Pipeline

AI影视生产不要直接从文字进入视频。

推荐流程：

```text
创意需求
↓
视觉资产
↓
图片验证
↓
镜头设计
↓
视频生成
↓
迭代优化
```

规则：

- 角色、场景、关键道具先稳定，再进入视频。
- 图片资产用于确定视觉基准。
- 视频阶段重点描述动作变化、镜头运动和时间关系。
- 发现问题时优先回到对应阶段修改，不要重复堆 Prompt。

## Shot Production Workflow

不要使用一个 Prompt 直接生成完整影片。

推荐：

```text
影片需求
↓
镜头拆解
↓
单镜头设计
↓
Shot Reference Pack
↓
视频生成
↓
剪辑组合
```

## Generation Review Loop

生成不是结束，而是进入导演审核循环。

```text
Generate
↓
Review
↓
Identify Issue
↓
Adjust
↓
Regenerate
↓
Lock Shot
```

检查：

- 人物是否一致。
- 动作是否符合逻辑。
- 空间关系是否正确。
- 摄影机运动是否符合设计。
- 时间变化是否连续。

修改优先级：

- 资产问题 → 修改 Asset。
- 镜头问题 → 修改 Shot Design。
- 描述问题 → 修改 Prompt。

## 镜头设计

每个镜头需要：

- 主体
- 动作
- 环境
- 景别
- 构图
- 运镜
- 情绪目标

镜头不是漂亮画面集合，而是叙事单位。

## Prompt 工程

Prompt 负责意图和视觉语言。

参考图负责一致性。

控制方式负责结构。

## 质量检查

检查：

- 创意是否明确。
- 资产是否统一。
- 镜头是否可生成。
- 视频动作是否具有连续性。
- 下一轮修改是否明确。