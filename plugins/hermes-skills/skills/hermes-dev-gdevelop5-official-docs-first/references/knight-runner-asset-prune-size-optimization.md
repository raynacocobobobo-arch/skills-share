# KnightRunner_Test：素材瘦身、孤儿清理、导出包减重

适用：用户要求“检查素材/没用的删掉/压缩画面大小/包太大”。

## 核心原则

1. **先审计，不先删**：同时检查当前 `KnightRunner_Test.json`、`.autosave`、`BASELINE_CURRENT`、已导出 `web/data.js`/`code0.js`/`index.html`。
2. **删除只进废纸篓**：项目素材、导出包素材、临时文件都移动到 `~/.Trash/<timestamp>/`，不用 `rm`。
3. **只改素材和资源表**：除非明确发现无实例、无事件引用的旧对象，否则不改玩法事件、碰撞、跳跃、木桩、Castle、Retry、音乐。
4. **导出包大不等于当前画面大**：GDevelop 会把 `resources` 表里仍存在的旧素材一起导出，即使当前场景没有实例。

## 审计步骤

### 1. 找孤儿素材

定义孤儿素材：项目目录顶层图片/音频文件名不出现在：

- 当前 JSON
- autosave
- BASELINE_CURRENT
- 当前导出包 `data.js/code0.js/index.html`

这些可以移动到废纸篓，但先输出清单、大小、总节省量。

### 2. 找坏资源引用

检查 `data.resources.resources[].file` 是否存在于项目目录。不存在的从 `resources` 表删除；不要误判成需要下载。

### 3. 找“资源表活着但运行不用”的大文件

仅看文件名是否在 JSON 中出现不够。必须区分：

- 对象动画引用的图片
- 对象是否有场景实例
- 对象是否被事件引用（事件 JSON 中精确出现对象名）
- 音频/图片是否被事件 JS 或普通事件直接引用
- 导出包里的 `.map` 调试文件

分类建议：

```text
ACTIVE: 有实例对象图片 / 事件引用音频或图片 / runtime JS/HTML
NOT_RUNTIME: 无实例、无事件引用的旧对象素材或资源表残留
DEBUG_MAP: *.map，可从发布包删除
```

## 实际瘦身流程

1. 备份：
   - `KnightRunner_Test.json.bak_prune_unused_assets_<timestamp>`
   - `KnightRunner_Test_web_before_prune_<timestamp>/`
   - 旧 zip 另存一份
2. 删除无实例、无事件引用、且有图片动画的旧对象。
   - 同步清理 `objectsFolderStructure`，否则编辑器对象树仍残留。
3. 重新计算实际活跃资源：
   - 剩余对象动画里的图片
   - 事件文本中直接引用的资源文件名（如 `ABBB.MP3`, `VC.mp3`, `1234.mp3`）
4. `resources` 表只保留实际活跃资源。
5. 项目目录中不再活跃的资源文件移动到废纸篓。
6. 导出包中删除：
   - 不在活跃资源表里的图片/音频
   - 所有 `.map` 调试文件
   - 保留 `index.html`, `data.js`, `code0.js`, runtime `.js`, `.wasm`, `.css`
7. 更新导出包的 `data.js` 为当前 JSON，并重新 zip。
8. 验证：
   - `formal_autosave_same=True`
   - `missing_project_active_resources=[]`
   - `missing_web_active_resources=[]`
   - 本地 HTTP 访问 `/`, `/code0.js`, `/data.js`, 关键资源（`ABBB.MP3`, `AAA.png`, `castle.png`, `V3.png`）返回 200。

## 图片尺寸压缩规则

按“实际显示尺寸 × 2（Retina 余量）”降采样，适合：

- UI 图标（如 `M`）
- 胜利/Best/flag 图
- 死亡动画帧
- 龙动画帧
- 隐形碰撞图（可极小化）

谨慎处理：

- 木桩和碰撞盒图片，不要为了瘦身改变跳跃/碰撞体感。
- 关键背景图（如 `AAA.png`）压缩前先看是否铺满屏。
- 分数字体可压但先确认清晰度。

## 关键坑

### 1. “看似删除对象，实际没删”

不要用带副作用的 list comprehension，例如：

```python
ly['objects']=[o for o in ly['objects'] if not (condition and pruned_objs.append(o.get('name')))]
```

`list.append()` 返回 `None`，会让条件逻辑失真。必须显式循环：

```python
kept=[]
removed=[]
for obj in ly['objects']:
    if should_remove(obj):
        removed.append(obj['name'])
    else:
        kept.append(obj)
ly['objects']=kept
```

之后必须回读验证：

```text
objects_removed_verified True
```

### 2. 资源表残留会继续撑大导出包

即使对象没有实例，只要旧对象还在 `objects` 或旧文件还在 `resources` 表里，GDevelop 导出包可能继续带上大图。瘦身必须同时处理：对象定义、对象树、资源表、导出包文件。

### 3. BGM 网页首局与 GDevelop 预览不同

浏览器会拦截未经过用户手势的有声自动播放。不要简单写成 `AudioUnlocked != 1 return`，否则 GDevelop 预览里开局音乐也会消失。

稳定做法：

```text
BGM 控制事件每帧先尝试 playMusicOnChannel。
GDevelop 预览通常会立即播放。
网页版如果浏览器拦截，首次鼠标/触屏/Space 后继续重试并补播。
Castle/GameOver/Victory 状态下仍 return，避免胜利或死亡后重启 BGM。
```

## 已验证效果参考

一次有效清理后，`KnightRunner_Test_web.zip` 可从约 `26.8MB` 降到约 `8.2MB`。主要收益来自：

- 删除旧背景/旧对象大图：约 9~10MB
- 删除未用音频/旧帧：约 8MB
- 删除 `.map`：约 1.6MB
- 显示尺寸压缩：约 4~5MB

不要只压 PNG；如果资源表和旧对象没清，包仍会很大。