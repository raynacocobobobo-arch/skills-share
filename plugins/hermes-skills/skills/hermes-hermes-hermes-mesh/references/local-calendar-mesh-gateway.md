# 本地 Mac 日历网关（mesh → iCloud Calendar）

## 背景

云端 Hermes 需要创建用户主机/iCloud 日程，但不应把 Apple ID / App 专用密码放到云服务器。更安全的模式是：云端只把结构化日程请求写入 mesh-bridge，本地 Mac 定时拉取并用 macOS Calendar 写入 iCloud「日历」。

## 已验证部署形态

- 本地脚本：`~/.hermes/scripts/calendar_mesh_gateway.py`
- Hermes cron：`no_agent=true`
- 频率：每 3 小时
- 默认目标日历：`日历`
- 不消耗模型 token
- 不暴露 Apple 凭据到云端

## 消息格式

云端写入 mesh 的内容必须是固定块：

```text
CALENDAR_ADD
title=出发去北京南站
start=2026-06-14 17:20
end=2026-06-14 18:05
calendar=日历
location=北京南站
note=可选备注
```

字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `title` | 是 | 事件标题 |
| `start` | 是 | `YYYY-MM-DD HH:MM` |
| `end` | 是 | `YYYY-MM-DD HH:MM` |
| `calendar` | 否 | 默认 `日历` |
| `location` | 否 | 地点 |
| `note` | 否 | 备注 |

一条 mesh 消息可包含多个 `CALENDAR_ADD` 块。

## 本地脚本规则

1. `GET /` 拉取 mesh 消息。
2. 只处理包含 `CALENDAR_ADD` 的消息。
3. 解析字段，缺 `title/start/end` 不写入。
4. 用 AppleScript 写入 macOS Calendar。
5. 写入前按 `summary + start date + end date` 查重，避免重复。
6. 写入成功后调用 `/mark/<filename>` 标记已读。
7. 空信箱/无日历消息时保持静默。

## 创建 cron 示例

```python
cronjob(
  action="create",
  name="本地日历网关：每3小时查mesh写入iCloud日历",
  schedule="0 */3 * * *",
  script="calendar_mesh_gateway.py",
  no_agent=True,
  deliver="local",
  enabled_toolsets=["terminal"],
)
```

注意：Hermes cron 的 `script` 参数必须是相对 `~/.hermes/scripts/` 的文件名，不能传绝对路径。

## 关键坑

- 不要让云端写自然语言请求给本地解析；必须用固定格式，否则会把“零 token”方案变成 AI 理解任务。
- 不要把 iCloud 凭据放云端。此网关的目的就是避免云端保存 Apple 凭据。
- mesh-bridge 文件名精度到分钟，同一分钟同 sender 多条可能覆盖；云端连续发多条时应合并到一条消息或间隔 65 秒。
- AppleScript 查到事件不等于手机/小组件已同步。若用户反馈不可见，应回到 `macos-calendar-automation.md` 的同步核验流程。
