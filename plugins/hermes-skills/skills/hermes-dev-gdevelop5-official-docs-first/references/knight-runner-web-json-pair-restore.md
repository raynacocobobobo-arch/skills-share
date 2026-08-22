# KnightRunner_Test 网页版 ZIP 与 JSON 成套恢复

## 触发场景

用户要求恢复某个历史网页版、8MB 优化版、20:01/22:26 等时间点备份，或说“我要那个完整备份 / JSON 也要对应那版”。

## 核心规则

1. **先区分 ZIP/目录 与 JSON**：`KnightRunner_Test_web*.zip` 只代表网页版导出包，不一定包含当前工程 JSON。
2. **不要自动假设“完整备份”=改 JSON**：先列出候选 ZIP 与候选 JSON，按时间、文件名、SHA、大小说明关系；用户确认后再恢复 JSON。
3. **成套恢复时要同步三处**：
   - `~/Desktop/hermes/GDevelop/KnightRunner_Test_web/`
   - `~/Desktop/hermes/GDevelop/KnightRunner_Test_web.zip`
   - `~/Desktop/hermes/public-transfer/KnightRunner_Test_web.zip`
4. **JSON 恢复时要同步两处**：
   - `/Users/rayna/Documents/GDevelop projects/My project3/KnightRunner_Test.json`
   - `/Users/rayna/Documents/GDevelop projects/My project3/KnightRunner_Test.json.autosave`
5. **恢复 JSON 前先退出 GDevelop**，避免编辑器内存/autosave 反向覆盖磁盘文件。
6. **恢复前必须备份当前版本**，备份名带 `before_restore..._YYYYMMDD_HHMMSS`。
7. 删除/替换目录时用 Trash/Finder delete，不用 `rm`。
8. 恢复后必须回读验证：ZIP SHA、目录文件数/总大小/目录签名、JSON/autosave SHA、JSON parse OK。

## 候选选择方法

- 先列 `~/Desktop/hermes/GDevelop/` 下相关 `KnightRunner_Test_web*.zip`，按 mtime、size、SHA 分组。
- 再列项目目录下 `KnightRunner_Test.json*`，重点匹配：
  - 文件名里的恢复/瘦身/导出时间戳；
  - mtime 与 ZIP 的创建时间；
  - 文件大小是否符合该阶段（例如 8MB 瘦身版常对应较小 JSON）；
  - SHA 是否与当前/历史备份重复。
- 如果候选超过一个，只能给出“最像”的判断，必须问用户确认。

## 本轮已验证的稳定流程示例

### 只恢复 20:01 对应的完整 Web 包，不动 JSON

来源 ZIP：

```text
~/Desktop/hermes/GDevelop/KnightRunner_Test_web_bak_bgm_20260621_205319.zip
SHA16: c4fa5adf8f47a6ff
大小: 33,039,011 bytes
```

恢复到：

```text
~/Desktop/hermes/GDevelop/KnightRunner_Test_web/
~/Desktop/hermes/GDevelop/KnightRunner_Test_web.zip
~/Desktop/hermes/public-transfer/KnightRunner_Test_web.zip
```

验证 JSON/autosave 未变化。

### 恢复 8MB 优化版 Web 包

来源 ZIP：

```text
~/Desktop/hermes/GDevelop/KnightRunner_Test_web_current_8mb_before_restore_20260622_004102.zip
SHA16: bc8dcdb2b88f680a
大小: 8,622,973 bytes
```

恢复后验证：

```text
web 目录文件数: 132
web 目录总大小约: 9,642,499 bytes
```

### 恢复 8MB 优化版对应 JSON

先列候选并确认。最像 8MB 包对应的 JSON：

```text
/Users/rayna/Documents/GDevelop projects/My project3/KnightRunner_Test.json.bak_before_restore_35mb_20260622_004102
SHA16: a6fc0d0c5898cdfa
大小: 109,589 bytes
```

用户确认后：

1. 退出 GDevelop。
2. 备份当前 `KnightRunner_Test.json` 和 `.autosave`。
3. 将候选 JSON 同步复制到正式 JSON 与 autosave。
4. 回读解析验证：两个文件 SHA 一致、JSON parse OK。

## 输出要求

回复用户时只说结果，不展开内部过程；但必须包含：

- 恢复来源；
- 已覆盖目标；
- SHA/大小/文件数等校验；
- JSON 是否被改动；
- 恢复前备份路径。
