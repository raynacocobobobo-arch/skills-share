# KnightRunner_Test 网页版导出与基准版保护

## 适用场景
用户要求“保存这版作为基准版”“导出/发布网页版”“先只导出，不发布云端”时使用。

## 基准版固化
1. 先确认正式 JSON 与 `.autosave`，以较新的为源；写回两者保持一致。
2. 生成两个基准副本：
   - `KnightRunner_Test.BASELINE_<YYYYMMDD_HHMMSS>.json`
   - `KnightRunner_Test.BASELINE_CURRENT.json`
3. 生成 `KnightRunner_Test.BASELINE_CURRENT.txt`，记录 SHA、时间、说明。
4. 回读验证：formal/autosave hash 一致、两个 baseline hash 等于源 SHA、manifest 可读。

## 网页版导出优先级
1. 若 GDevelop CLI/官方导出器可用，优先用官方导出。
2. 若本机 GDevelop Electron 没有可用 CLI，且用户只要求“本地导出”，可使用当前预览产物目录作为可运行网页版包：
   - 常见位置：`/var/folders/.../T/GDTMP-501/preview/`
   - 必须存在 `index.html`、`code0.js`、`data.js`。
3. 复制到：`~/Desktop/hermes/GDevelop/KnightRunner_Test_web/`。
4. 打包：`~/Desktop/hermes/GDevelop/KnightRunner_Test_web.zip`。
5. 启动本地 `python3 -m http.server <port>` 验证 `/`、`/index.html`、`/code0.js`、`/data.js` HTTP 200。

## 发布云端前确认
- 如果用户要求“发布网页版”，但云端路径/URL不明确，必须先通过 mesh 或用户确认部署目录与访问 URL。
- 用户选择“先只导出网页版”时，不上传、不覆盖云端目录。

## 验证清单
- 统计文件数、目录大小、zip 大小、zip SHA。
- 检查关键资源：`VC.mp3`、`castle.png`、`V3.png`。
- 不把预览产物存在当作云端发布完成；本地导出和公网部署必须分开汇报。

## 坑
- GDevelop GUI 菜单有 `Export (web, iOS, Android)…`，但 Electron 界面对 AppleScript 辅助功能暴露可能不完整；不要在 GUI 点不动时反复盲点。
- 预览目录是临时目录；复制完成后必须以桌面导出目录为交付物，不要把 `/var/folders/.../preview` 当长期路径。