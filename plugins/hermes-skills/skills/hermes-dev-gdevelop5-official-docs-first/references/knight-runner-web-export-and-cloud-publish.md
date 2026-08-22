# KnightRunner_Test：网页版导出与云端发布流程

适用：用户要求“导出网页版 / 发布一个网页版 / 发到云端”。

## 核心原则

1. **先区分导出与发布**：
   - “导出”只在本地生成可运行 `index.html` 包。
   - “发布”才涉及上传/覆盖云端目录。
2. **发布前必须确认云端位置**：不要猜目录或 URL。通过 `hermes-mesh` 询问云端部署目录、对外 URL、是否可覆盖 nginx/静态服务目录。
3. **用户选择“先只导出”时，禁止上传云端。**
4. 导出后必须本地 HTTP 验证，不要只看文件存在。

## 已验证本地导出方案

### 方案 A：GDevelop GUI 正常导出

GDevelop 菜单入口：

```text
File → Export (web, iOS, Android)…
```

若 GUI 自动化可用，按界面导出 HTML5/web 包到：

```text
~/Desktop/hermes/GDevelop/KnightRunner_Test_web/
```

并打 zip：

```text
~/Desktop/hermes/GDevelop/KnightRunner_Test_web.zip
```

### 方案 B：使用 GDevelop preview 目录作为本地 web 包

当没有可直接调用的 CLI，且 GUI 辅助功能无法可靠读取 Electron 内容时，可使用 GDevelop 生成的预览目录作为网页版包。典型位置：

```text
/var/folders/.../T/GDTMP-501/preview/
```

查找：

```bash
find /var/folders -name code0.js 2>/dev/null
```

预览目录应包含：

```text
index.html
code0.js
data.js
运行时 JS
项目资源图片/音频
```

**注意：preview 可能是旧产物。** 使用前必须确认：

- GDevelop 已加载当前项目。
- 最好刚运行过预览，或至少 preview 目录 mtime 晚于最近关键修改。
- 关键资源存在，例如当前项目：`VC.mp3`、`castle.png`、`V3.png`。
- 本地 HTTP 服务能打开 `index.html`、`code0.js`、`data.js`。

复制导出：

```bash
mkdir -p ~/Desktop/hermes/GDevelop
cp -R <preview_dir> ~/Desktop/hermes/GDevelop/KnightRunner_Test_web
```

可选：把 `index.html` 标题改为 `KnightRunner_Test`。

打包：

```bash
cd ~/Desktop/hermes/GDevelop
zip -r KnightRunner_Test_web.zip KnightRunner_Test_web
```

## 验证步骤

1. 回读文件数、目录大小、zip 大小和 SHA。
2. 检查关键文件：

```text
index.html
code0.js
data.js
VC.mp3
castle.png
V3.png
```

3. 起本地 HTTP 服务：

```bash
cd ~/Desktop/hermes/GDevelop/KnightRunner_Test_web
python3 -m http.server 8765 --bind 127.0.0.1
```

4. 请求验证：

```bash
curl -I http://127.0.0.1:8765/
curl -I http://127.0.0.1:8765/code0.js
curl -I http://127.0.0.1:8765/data.js
```

## 云端发布流程

1. 先通过 `hermes-mesh` 问云端：

```text
请确认 KnightRunner_Test GDevelop 网页版游戏部署位置：
1. 云端应放在哪个目录？
2. 对外访问 URL/域名是什么？
3. 是否已有 nginx/静态服务目录可直接覆盖？
请简短回复路径和 URL。
```

2. 用户确认目录/URL 后再上传。
3. 上传后由云端或本地验证公网 URL 返回 `index.html`。
4. 不要把本地绝对路径 `/Users/rayna/...` 发给云端作为部署路径。

## 常见坑

- app.asar 里未必有稳定公开 CLI；不要假装已经用 CLI 导出。
- Electron 界面对 macOS Accessibility 可能只暴露少量按钮，GUI 自动化不一定能读到导出面板内容。
- preview 包含调试文件不一定影响运行；除非确认不被引用，不要随意删运行时目录。
- 只说“已导出”前必须验证 HTTP 可访问。
- 用户说“先只导出”时，不能继续发布云端。
