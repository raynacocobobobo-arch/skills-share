# Prompt Patterns

用途：把视觉概念转成结构化描述，再转成可生成语言。它不是 Prompt 示例库，也不是模型参数手册。

适用场景：

- 用户要把参考图、风格方向、分镜或资产卡转成图像/视频 Prompt。
- 用户需要稳定角色、场景、品牌视觉或世界观风格。
- 用户问“怎么写得更像这个方向”，但不能直接复制参考图内容。
- 用户需要判断应该靠 Prompt 解决，还是靠参考图、控制图、局部修复或视频流程解决。

## 四层结构

写 Prompt 前先拆成四层：

1. 意图层：故事目标、品牌目标、镜头目标、观众情绪。
2. 视觉系统层：风格锚点、构图、色彩、材质、光影、摄影语言。
3. 内容层：主体、动作、环境、角色/场景/道具资产常量。
4. 控制层：画幅、参考来源、控制方式、负面约束、下一轮迭代目标。

不要直接从“概念”跳到“长 Prompt”。先确定视觉系统，再生成语言。

## Style Card

当用户给出参考图、参考风格或需要多镜头一致性时，先建立轻量 Style Card：

```yaml
style_name:
style_summary:
style_fidelity_anchors:
composition:
color_system:
material_texture:
lighting:
camera:
typography_or_graphics:
source_content_to_avoid:
negative_prompt:
```

字段要求：

- `style_summary`：一句话说明风格，不超过一个短段落。
- `style_fidelity_anchors`：必须保留的可见视觉特征，通常 5-8 条。
- `composition`：主体位置、画面层次、留白、裁切、透视。
- `color_system`：主色、辅助色、色温、比例关系。
- `material_texture`：建筑、服装、道具、皮肤、金属、玻璃、纸张等材质。
- `lighting`：光源位置、强弱、色温、阴影、空气感。
- `camera`：景别、焦段感、视角、运动方式、摄影质感。
- `typography_or_graphics`：只有海报、品牌片、包装、界面等需要文字或图形系统时填写。
- `source_content_to_avoid`：不能复制的具体标识、构图、标语、品牌、人物、Logo 或受保护内容。
- `negative_prompt`：只写会伤害项目一致性的排除项。

## Prompt 组装顺序

推荐顺序：

```text
镜头目标 -> 主体 -> 动作 -> 环境 -> 风格锚点 -> 构图/摄影 -> 色彩/光影/材质 -> 连续性规则 -> 输出限制 -> Negative Prompt
```

写法原则：

- 主体必须和环境绑定，避免“干净背景里的孤立物体”。
- 风格要落到可见特征，不只写“高级、电影感、赛博朋克、大片感”。
- 参考图转写时，描述视觉系统，不复刻具体人物、品牌、标语或原始构图。
- 多镜头项目先继承 Asset Card 和 Style Card，再写单个镜头 Prompt。
- 视频 Prompt 必须写动作连续性和镜头运动，不能只写静态画面。

## Negative Prompt

Negative Prompt 不要堆砌通用禁词。优先排除本项目最容易失败的内容：

- 风格漂移：不属于世界观的时代、材质、色彩或摄影风格。
- 资产漂移：角色外观、服装、场景固定元素、道具结构变化。
- 画面错误：不可见细节、矛盾动作、错误空间关系、文字乱码。
- 来源风险：Logo、水印、UI、二维码、真实品牌包装、明星脸、官方标语。
- AI 痕迹：过度光滑、塑料皮肤、无意义装饰、畸形肢体、漂浮物体。

## 生产控制路由

不要把所有控制都塞进 Prompt。先判断生成任务属于哪类：

| 任务 | 优先方式 | Prompt 重点 |
| --- | --- | --- |
| 快速探索风格 | 文生图 | 风格锚点、色彩、构图、情绪 |
| 保持角色或场景一致 | 参考图 / 图生图 | 资产常量、禁止变化、材质细节 |
| 保持构图、姿态或空间 | 控制图 / 深度 / 线稿 / 姿态 | 内容、风格、光影，不重复控制图已经承担的信息 |
| 局部修复 | 局部重绘 | 修复区域目标、边缘融合、材质连续 |
| 扩展画面 | 扩图 | 新增空间关系、光线延续、边缘一致性 |
| 生成运动 | 图生视频 / 文生视频 | 起止动作、镜头运动、运动幅度、时长感 |
| 最终增强 | 放大 / 精修 | 保真、纹理、清晰度、不要改变构图 |

核心原则：Prompt 负责意图和视觉语言，控制图负责结构，参考图负责一致性，局部修复负责小范围错误。

## 输出模板

```yaml
style_card:
  style_name:
  style_summary:
  style_fidelity_anchors:
  composition:
  color_system:
  material_texture:
  lighting:
  camera:
  source_content_to_avoid:

prompt:
  shot_goal:
  positive_prompt:
  negative_prompt:
  control_route:
  iteration_focus:
```

## 检查清单

输出前检查：

- 是否从视觉概念拆成了构图、色彩、材质、光影、摄影，而不是堆风格词。
- 是否明确哪些内容必须稳定，哪些内容可以变化。
- 是否把参考图变成视觉语言，而不是复刻原图。
- 是否选择了合适的控制方式，而不是强行用一条 Prompt 解决全部问题。
- 下一轮迭代是否只有一个优先目标。
