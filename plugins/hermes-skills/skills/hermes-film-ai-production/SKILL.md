---
name: hermes-film-ai-production
description: AI导演工作流技能，用于AI短片、宣传片、品牌片、世界观视觉开发、AI资产设计、分镜设计和生成提示词。
---

# Hermes AI Film Production

用于 AI 短片、宣传片、品牌片、世界观视觉开发、AI 角色/场景设计、AI 分镜设计和生成提示词优化。目标不是教学 AI 视频工具，也不是建立复杂资产管理系统，而是让 Hermes 具备实用的 AI 导演工作流。

核心判断：AI 影视不是一句 Prompt 生产，而是从项目启动、创意开发、视觉分析、轻量资产规范、镜头设计到生成提示词和质量检查的导演流程。

路由边界：影视、连续镜头、视频、图片转视频、分镜组、宣传片、故事片和世界观视觉开发使用本 skill。单张图任务，如海报、插画、角色设定图、建筑效果图、商业视觉图和风格探索图，使用 `hermes-image-prompt-design`。

## 工作原则

- 先做审美和创意判断，再选工具或写 Prompt。
- 先验证角色、场景、氛围和风格一致性，再扩展完整故事。
- 避免复制热门视觉标签；如果用户给出常见方向，如赛博朋克，要主动寻找更具体、更差异化的时代、材质、技术和文化线索。
- 所有输出都要服务后续生成或制作执行，少写抽象评价，多给可转换为画面、资产或镜头的描述。
- AI 生成内容要加入使用痕迹、磨损、污渍、不规则细节和环境关系，避免过度完美的 AI 感。
- 使用简单资产命名：`character_robot`、`location_factory`、`prop_vehicle`、`shot_001`，需要版本时用 `character_robot_v02`。不要使用企业级审批命名。

## 路由

根据用户需求选择最小可用流程：

- 用户只有模糊需求，如“做一个 AI 宣传片”或“我要做一个 AI 科幻短片”：先读 [references/project-start.md](references/project-start.md)，完成需求补全后进入 [references/workflows.md](references/workflows.md) 的概念开发。
- 用户提供参考图片、海报、截图或视觉参考：读 [references/visual-analysis.md](references/visual-analysis.md)，输出视觉拆解和视觉规范，再进入资产设计或镜头设计。
- 用户需要连续角色、连续场景、稳定世界观或多镜头一致性：读 [references/asset-bible.md](references/asset-bible.md)，先建立核心资产卡，再生成镜头。
- 用户需要分镜、镜头组或单个镜头设计：读 [references/storyboard-template.md](references/storyboard-template.md)，用统一镜头模板输出。
- 用户需要连续动作分镜、四格动作序列、图片转视频、关键帧转视频或 Motion Prompt：读 [references/sequence-storyboard.md](references/sequence-storyboard.md)，先拆 Beat Board，再做 Sequence Board，最后写 Motion Prompt。
- 用户需要图像/视频生成 Prompt、参考风格迁移、Negative Prompt、生成控制方式或提示词迭代：读 [references/prompt-patterns.md](references/prompt-patterns.md)，按“视觉概念 -> 结构化描述 -> 生成语言”处理。
- 用户要完整 AI 影视方案：按 [references/workflows.md](references/workflows.md) 的「Project Start -> Concept Development -> Visual Analysis -> Asset Bible -> Shot Design -> Prompt Engineering -> Review」组织输出。
- 用户只要局部建议时，不要加载所有 references；只读当前任务需要的文件。

## 边界

不要创建新的子 skill。不要添加 `asset-manifest.json`、数据库、企业级 DAM、大量版本流程、复杂审批流程或模型列表维护。

## 输出习惯

- 默认用中文输出。
- 不输出内部验证过程。
- 不把 Prompt 写成单句关键词堆砌；使用主体、动作、环境、视觉风格、摄影语言、情绪目标和限制条件组织。
- 不把所有问题都交给 Prompt；需要一致性、构图控制、局部修复或运动时，要说明应使用参考图、控制图、局部重绘、图生视频等生产方式。
- 当用户只给一个模糊想法时，先给可执行的视觉方向和实验路径；只有关键信息缺失到无法判断题材或用途时才追问。
