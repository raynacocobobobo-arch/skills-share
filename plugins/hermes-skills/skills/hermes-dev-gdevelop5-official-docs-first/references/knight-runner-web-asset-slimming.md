# KnightRunner_Test：网页版素材瘦身与资源表清理

适用：用户反馈 GDevelop 网页版 zip 太大、素材“反正也看不清”、要删除没用素材或压缩画面大小。

## 核心原则

1. **先审计再删除**：必须同时检查当前 JSON、`.autosave`、`BASELINE_CURRENT`（若有）和已导出的 web 包，确认资源不是运行时需要的。
2. **删除只走 Trash**：项目目录素材、导出包素材、临时文件都移动到 `~/.Trash/<带时间戳目录>/`，不要 `rm`。
3. **只改本次目标**：素材瘦身不改木桩、跳跃、Castle、Retry、音乐事件等玩法逻辑。
4. **JSON 资源表很关键**：只删除文件不够；GDevelop 的 `resources.resources` 和未使用对象仍会让导出包继续带上大图。
5. **导出包要同步**：改完项目目录后，更新 `~/Desktop/hermes/GDevelop/KnightRunner_Test_web/data.js`，同步复制被压缩的素材到导出目录，重新 zip。

## 审计方法

### 1. 识别真正运行需要的资源

- 活跃对象 = 场景 `instances` 中出现的对象 + `events` 中被引用的对象。
- 活跃图片 = 活跃对象动画帧里的图片。
- 活跃音频/媒体 = `events` 里实际出现的资源文件名（例如 `ABBB.MP3`、`VC.mp3`、`1234.mp3`）。
- 其它资源表条目、未实例化且事件不引用的对象，多数只是历史残留。

### 2. 分类导出包体积

按文件体积列出 web 目录，并按三类看：

```text
active_runtime      真正运行需要：当前对象/事件资源 + runtime JS/html
not_runtime_assets  资源表/导出包残留，但当前运行不用
debug_maps          .map 调试文件，可从发布包移除
```

用户问“为什么还是大”时，优先输出这个分类，而不是继续盲目压图。

### 3. 常见大头

- 没有实例、事件也不引用的旧 `NewSprite2~NewSprite10` 背景/测试对象。
- 旧音频如 `bgm.aac`，如果事件只用 `ABBB.MP3`，则不是运行资源。
- `.map` 文件只用于调试，发布包可删除。
- 背景图 `AAA.png`、BGM `ABBB.MP3`、`V3.png`、`castle.png` 才是真正运行大头。

## 安全压缩策略

### 图片

按“实际显示尺寸 × 2（Retina 余量）”压缩，避免肉眼可见变糊。

- 运行中小图：目标尺寸约为显示尺寸 2 倍。
- 隐形碰撞/物理图：如果纯透明或不可见，可大幅缩小；但必须确认不被可见对象共用。
- 木桩、碰撞盒、数字 UI 这类手感/清晰度敏感资源，除非明确确认，不优先压。
- 用 ImageMagick 压缩时失败要停下来回读，清理临时 `.tmp.png` 到 Trash。

示例命令逻辑：

```bash
magick input.png -resize '<cap_w>x<cap_h}>' -strip -define png:compression-level=9 output.png
```

注意：上面命令里的实际 resize 参数要由脚本生成；不要手打带错括号。

### 音频

`ABBB.MP3` 往往是 2~3MB 大头。若用户还嫌大，可单独询问是否接受低码率压缩 BGM；不要默认降音质。

## 清理顺序

1. 备份当前 JSON/autosave：`KnightRunner_Test.json.bak_<reason>_<timestamp>`。
2. 备份导出目录：`KnightRunner_Test_web_before_<reason>_<timestamp>`。
3. 用活跃对象/事件计算 `active_files`。
4. 从 `layouts[0].objects` 删除未实例化且事件不引用的旧图片对象。
5. 同步清理 `objectsFolderStructure` 中对应对象。
6. 从 `resources.resources` 删除不在 `active_files` 的资源条目。
7. 项目目录中被移除资源文件移动到 Trash。
8. 导出包中删除非活跃图片/音频和所有 `.map`。
9. 写回 `data.js = gdjs.projectData = <当前项目 JSON>;`。
10. 重新打包 `KnightRunner_Test_web.zip`。
11. 验证：
    - formal JSON 与 autosave SHA 一致；
    - 所有 active resources 在项目目录和 web 目录都存在；
    - 本地 HTTP 能访问 `/`, `/code0.js`, `/data.js`, `/ABBB.MP3`, `/AAA.png`, `/castle.png`, `/V3.png`。

## 已验证效果参考

一次成功清理中：

```text
未使用对象：NewSprite2~NewSprite10、ScoreLabel
资源表残留：旧背景、旧 UI、旧音频、旧骑士帧等
zip：26.8MB -> 8.22MB
web 目录：约 9.20MB
```

关键经验：第一次只删 `.map` 和孤儿文件通常不够；必须真正从 JSON 对象列表和资源表移除未用对象/资源，否则 GDevelop 导出仍会把素材带上。

## 输出给用户时

用户要的是“能小多少”和“有没有影响游戏”。输出应简洁给：

```text
当前 zip 大小 / SHA
删了哪些类别
保留哪些运行大头
备份/废纸篓路径
验证结果
```
