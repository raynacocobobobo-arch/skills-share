# Image Prompt Patterns

用途：把单张图的视觉概念转成结构化描述，再转成可生成提示词。它不是 Prompt 示例库，也不是影视分镜流程。

适用任务：

- 海报、插画、角色设定图、建筑效果图、商业视觉图、风格探索图。
- 单张肖像、单张场景、单个产品视觉、单张概念图。
- 参考图转风格，但不能复刻原图、品牌、人物或标语。

不适用任务：

- 连续镜头、故事片、宣传片、分镜组、图片转视频、图生视频、镜头运动设计。这些进入 `hermes-film-ai-production`。

## 四层结构

写 Prompt 前先拆成四层：

1. 图像目标：用途、受众、传播/审美目标。
2. 视觉系统：风格锚点、构图、色彩、材质、光影、摄影/绘画语言。
3. 画面内容：主体、动作/姿态、环境、道具、文字或图形元素。
4. 生成控制：画幅、参考图、控制图、局部重绘、扩图、负面约束、迭代重点。

## Style Card

```yaml
style_name:
style_summary:
style_fidelity_anchors:
composition:
color_system:
material_texture:
lighting:
camera_or_render:
typography_or_graphics:
source_content_to_avoid:
negative_prompt:
```

字段要求：

- `style_fidelity_anchors`：必须保留的可见视觉特征，通常 5-8 条。
- `composition`：主体位置、留白、前中后景、裁切、透视。
- `color_system`：主色、辅助色、色温、比例关系。
- `material_texture`：服装、建筑、产品、皮肤、金属、玻璃、纸张等材质。
- `lighting`：光源位置、强弱、色温、阴影、空气感。
- `camera_or_render`：摄影、插画、3D 渲染、建筑可视化或平面设计语言。
- `typography_or_graphics`：海报、品牌图、包装图、界面图才需要。
- `source_content_to_avoid`：不能复制的 Logo、标语、真实人物、品牌包装、原始构图。

## Prompt 组装顺序

```text
图像目标 -> 主体 -> 姿态/动作 -> 环境 -> 风格锚点 -> 构图 -> 色彩/光影/材质 -> 输出限制 -> Negative Prompt
```

写法原则：

- 主体必须和环境绑定，不写漂浮在干净背景里的孤立物体，除非用户明确要产品白底图。
- 风格要落到可见特征，不只写“高级、电影感、赛博朋克、大师风格”。
- 参考图转写时，只提取视觉系统，不复刻具体人物、品牌、标语或原始构图。
- 商业视觉要明确文字区域、产品可读性、Logo 占位和禁止生成真实品牌标识。
- 建筑效果图要明确时代、材料、结构、周边环境、光照和尺度参照。

## 生成控制路由

| 任务 | 优先方式 | Prompt 重点 |
| --- | --- | --- |
| 风格探索 | 文生图 | 风格锚点、构图、色彩、情绪 |
| 角色/产品/空间一致 | 参考图 / 图生图 | 资产常量、禁止变化、材质细节 |
| 姿态或构图稳定 | 控制图 / 线稿 / 姿态 / 深度 | 内容、风格、光影，不重复控制图已承担的信息 |
| 局部修复 | 局部重绘 | 修复区域目标、边缘融合、材质延续 |
| 扩展画面 | 扩图 | 新增空间关系、光线延续、边缘一致性 |
| 最终增强 | 放大 / 精修 | 保真、纹理、清晰度、不要改变构图 |

## Negative Prompt

只排除当前图像真正容易失败的内容：

- 风格漂移：错误时代、错误材质、错误摄影/绘画语言。
- 内容错误：不可见细节、矛盾动作、错误空间关系、文字乱码。
- 来源风险：Logo、水印、二维码、真实品牌包装、明星脸、官方标语。
- AI 痕迹：过度光滑、塑料皮肤、畸形肢体、漂浮物体、无意义装饰。

## 输出模板

```yaml
image_goal:
style_card:
  style_name:
  style_fidelity_anchors:
  composition:
  color_system:
  material_texture:
  lighting:
  camera_or_render:
positive_prompt:
negative_prompt:
control_route:
iteration_focus:
```
