# GDevelop autosave 与实际打开文件同步排障

适用场景：用户反馈“JSON 明明改了，但 GDevelop 里一点没变”“打开最新版还是旧逻辑”。

## 核心判断

GDevelop 可能优先恢复同目录的 `<project>.json.autosave`。如果 autosave 比正式 JSON 旧，编辑器里看到的会是旧事件，导致：

- 正式 JSON 回读验证全对；
- 但 GDevelop UI/预览仍显示旧逻辑；
- 用户会反馈“一点没改”。

## 必查顺序

1. 关闭 GDevelop，避免保存旧内存状态覆盖文件。
2. 同时检查正式文件和 autosave：
   - `<project>.json`
   - `<project>.json.autosave`
3. 对比：mtime、事件数量、关键事件字符串、对象列表。
4. 如果正式 JSON 是新版而 autosave 是旧版：
   - 先备份旧 autosave：`<project>.json.autosave.bak_old_autosave_<timestamp>`
   - 再把正式 JSON 复制覆盖 autosave。
5. 重新用参数方式打开 GDevelop：
   - `open '/Applications/GDevelop 5.app' --args '<project>.json'`
6. 用 `pgrep -fl 'GDevelop'` 验证进程参数里带了正式 JSON 路径。

## 关键验证项示例

不要只说“已改”。要回读正式 JSON 和 autosave 都包含目标逻辑，例如：

- `ChangeScene` 不存在；
- `RandomInRange(...)` 存在；
- `Score + 100` 存在；
- `TimeDelta() * 60` 不存在；
- `ObstacleHitbox` 存在；
- 骑士二段跳参数存在。

## 用户体验规则

如果用户说“没改”“一点没改”，不要继续解释 JSON 已写入。优先怀疑：

1. GDevelop 打开了备份文件；
2. GDevelop 恢复了旧 autosave；
3. 编辑器内存状态覆盖了磁盘文件；
4. 打开命令没有把项目路径作为参数传进进程。

先查这些，再回复。