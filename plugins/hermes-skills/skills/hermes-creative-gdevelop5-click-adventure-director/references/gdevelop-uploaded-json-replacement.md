# GDevelop 外部 JSON / 上传文件替换工作流

适用：用户让其他工具（如 ChatGPT）修改了 `KnightRunner_Test.json`，再把完整 JSON 文件发回，要求替换本机项目。

## 背景坑

GDevelop 项目同目录常有：

- `Project.json`
- `Project.json.autosave`

如果只替换正式 `.json`，GDevelop 可能恢复旧 autosave，用户会看到“明明替换了但一点没改”。因此外部 JSON 替换必须同时处理 autosave。

## 稳定流程

1. 先确认本轮意图：用户只是上传文件时，不要默认替换；用户明确说“替换到项目/用这个文件覆盖/打开测试”才继续。
2. 从用户文字里提取“本次声称已修复”的关键断言，例如 `ignoreDefaultControls=true`、`SetCanJump`、`SimulateJumpKey`、`MouseButtonFromTextReleased`、速度上限、生成间隔、X 范围等。
3. 关闭 GDevelop，避免编辑器内存状态覆盖文件。
4. 验证上传 JSON 能解析，并检查关键对象/事件是否存在。
5. **先验收上传文件是否真的包含用户声称的修改**：如果关键断言明显缺失，不要覆盖正式项目；直接报告“上传文件与说明不一致”，列出缺失项，让用户重传或授权按说明修当前 JSON。
6. 备份当前正式文件：`Project.json.bak_before_uploaded_replace_<timestamp>`。
7. 备份当前 autosave：`Project.json.autosave.bak_before_uploaded_replace_<timestamp>`。
8. 用上传 JSON 写入正式文件。
9. 同步写入 autosave：正式文件和 `.autosave` 内容保持一致。
10. 回读正式文件和 autosave，验证关键逻辑都一致。
11. 用参数方式打开 GDevelop：
   ```bash
   open '/Applications/GDevelop 5.app' --args '/path/to/Project.json'
   ```
12. 打开后读取进程参数/窗口标题，确认实际打开的项目路径。
13. 再次回读正式文件和 autosave，确认没有被 GDevelop 覆盖回旧版。

## 推荐验证项

- `ChangeScene` 是否已移除（如果 Retry 改为原地重置）。
- `Score` 是否不再按 `TimeDelta()` 自动增长。
- 过障碍是否 `Score += 100`。
- `ObstacleHitbox` 是否存在。
- `NewSprite12` 是否没有 Platformer/Physics 行为。
- `KnightHorse` 是否没有 `SetY/SetXY/MettreY/MettreXY/Y()` 锁高度事件。
- 正式 `.json` 与 `.autosave` 的关键检查结果是否一致。

## 回报标准

不要只说“已替换”。必须报告：

- 上传文件验证结果。
- 正式文件备份路径。
- autosave 备份路径。
- 正式文件与 autosave 均已写入并回读验证。
- GDevelop 窗口标题或进程参数中的实际项目路径。
