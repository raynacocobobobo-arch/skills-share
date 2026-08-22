# GDevelop Sprite 局部重染（骑士披风/盾牌等）

适用：用户希望在不重画素材、不改动画结构的情况下，把已有 Sprite 动画帧中的某个局部（如披风、盾牌、衣服）改成指定颜色。

## 安全流程

1. 先保存并关闭 GDevelop，避免编辑器旧状态覆盖 JSON。
2. 从项目 JSON 中读取目标对象动画帧引用，不按文件名猜测。
3. 生成坐标/帧预览图，让用户确认要改的区域（如“身后深褐色/黑色那块”），避免误染马、盔甲、描边。
4. 备份当前帧到 `_backup_<object>_<purpose>_<timestamp>/`。
5. 生成新帧文件，命名用后缀，例如 `_redcape.png`，不要覆盖原图。
6. 替换对象动画 sprite 的 `image` 字段，并在 `resources.resources` 中追加新图资源：`kind='image'`、`smoothed=false`、`userAdded=true`。
7. 回读验证所有帧都指向新图、文件存在、资源已注册、`BAD_Y_EVENTS []`。
8. 重开 GDevelop。

## 区域识别原则

- 先用 PIL 读取 RGBA，限定 ROI（如骑士上半身/身后区域），再按颜色条件筛选。
- 对深褐/黑色披风或盾牌：候选像素可用 `a>30`、`r<92`、`g<78`、`b<75`，并结合“棕黑/近黑”条件。
- 做连通域分析，优先选择最大连续深色块；不要全局替换所有黑色，否则会污染描边、马鬃、阴影、盔甲。
- 保留 alpha 和明暗，用亮度映射到目标颜色，而不是统一涂纯色。这样动画阴影仍然自然。

## 红披风示例色彩映射

对选中像素计算亮度：

```python
lum = (0.2126*r + 0.7152*g + 0.0722*b) / 255.0
nr = int(95 + lum*150)
ng = int(8 + lum*35)
nb = int(10 + lum*30)
pix[x, y] = (min(210, nr), min(60, ng), min(55, nb), a)
```

这会得到偏暗的深红披风，保留原本阴影。如果用户觉得红色太暗，可提高 `nr` 下限或上限，做更鲜明的战旗红。

## 预览输出

生成 before/after contact sheet，放到用户默认输出目录下，例如：

`~/Desktop/hermes/分镜/knight_redcape_preview.png`

在最终回复中附 `MEDIA:<path>` 让用户直接看效果。
