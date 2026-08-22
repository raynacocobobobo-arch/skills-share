# KnightRunner / GDevelop 5：网页版音乐与素材瘦身经验

适用场景：GDevelop 5 跑酷项目导出 HTML5/Web 包后，首局音乐不播、导出包异常偏大、旧素材被打包。

## 首局 BGM：浏览器自动播放限制

现象：GDevelop 预览有/无音乐不一致，网页版第一局无 BGM，Retry 后第二局才有。

原因：浏览器会拦截未经过用户手势的有声自动播放。Retry 属于用户点击后，音频上下文已解锁，所以第二局可播。

推荐修法：
- 不要只改成 `AudioUnlocked=1 才播放`，这会让 GDevelop 预览开局音乐也被挡住。
- 应采用“双路径”：
  1. 场景开始时先尝试播放 BGM（让 GDevelop 预览和允许自动播放的环境正常）；
  2. 若网页环境被拦截，则在首次 Space/鼠标/触屏输入后补播；
  3. GameOver/Castle/VC/V3 阶段保持不重启 BGM。

核查点：
- `ABBB.MP3` 仍在 resources 和导出包。
- BGM 事件未误伤 Castle/VC 停音乐逻辑。
- `data.js` 和正式 JSON/autosave 同步。

## 素材瘦身：不要只看文件夹孤儿文件

GDevelop 导出是否带素材主要看 JSON resources 与对象动画引用，不只是项目目录里有没有文件。

审计分层：
1. 当前 JSON/autosave/基准/导出包是否引用；
2. 对象是否有实例；
3. 事件是否引用对象名；
4. 剩余对象动画真正引用了哪些图片；
5. 事件/JS 字面量真正引用了哪些音频/图片文件名；
6. 导出包里 `.map` 调试文件是否可移除。

安全清理流程：
1. 先退出 GDevelop，避免 autosave 覆盖。
2. 备份正式 JSON、autosave、导出包、即将移动的素材。
3. 只移除“无实例 + 事件不引用 + 有图片动画”的旧对象。
4. 重算 active_files：剩余对象动画图片 + 事件里实际出现的资源文件名。
5. 从 `resources.resources` 移除非 active_files 条目。
6. 项目目录和导出目录里的非 active 资源移到废纸篓，不用 rm。
7. 删除导出包 `.map` 文件；它们是调试 sourcemap，网页运行不需要。
8. 重写 `web/data.js = 'gdjs.projectData = ' + compact_json + ';'`。
9. 重新 zip。
10. 验证 active resources 在项目目录和 web 目录都存在，正式 JSON 与 autosave SHA 一致。

常见大头：
- 旧背景/旧角色/旧分数图仍挂在 NewSprite2~NewSprite10、ScoreLabel 等未用对象上；如果对象未真正从 JSON objects 移除，resources 仍会保留，导出包仍大。
- `.map` 文件可省 1MB+。
- 未用 bgm.aac、旧 score_counter_score.png、旧透明背景图常被 resources 表保留。

注意：
- 压缩图片文件本身前先看“实际显示尺寸 × 2 Retina 余量”；不要压 UI 数字、碰撞盒替代图到影响识别。
- 优先删未用资源，再考虑压 `ABBB.MP3`；音频通常是最后的大头。
- 修改脚本要验证对象确实被移除，不能只依赖 list comprehension 的副作用。输出 `objects_removed_verified=True`。

## 用户偏好

用户在 GDevelop 项目里非常在意“改 A 不动 B”：素材清理/网页导出/音乐修复都必须明确不碰跳跃、障碍、Retry、Castle/V3/VC、Score、RunSpeed 等无关系统。清理文件必须走废纸篓并给可恢复路径。