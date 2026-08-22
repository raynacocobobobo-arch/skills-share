---
name: hermes-mesh
description: 多 Hermes 部署通讯协议——本地 Mac + 腾讯云 ×2，HTTP mesh-bridge 留言板，分工协作
version: 3.0.0
triggers:
  - 云端
  - 企微
  - 三Hermes
  - 双Hermes
  - 留言板
  - _inbox
  - 给云端发消息
  - 查收件箱
  - mesh-bridge
---

# 三 Hermes 部署 & 通讯协议

## 架构

```
              ┌─ mesh-bridge:9000 ─┐
              │  <REDACTED_HOST>      │
              │  ~/_inbox/         │
              └──┬──────┬──────┬──┘
           HTTP │ HTTP │      │ 本地读写
                │      │      │
             [本地]  [企微]  [云端]
             飞书    企微    微信
```

**所有节点通过 HTTP mesh-bridge (<REDACTED_HOST>:9000) 通信。** 云端是 mesh-bridge 的宿主机，本地读写 `_inbox/`；本地和企微作为客户端通过 HTTP 收发。

## 节点清单

| 名字 | IP | 通道 | 角色 |
|------|-----|------|------|
| **本地** | Mac (公网 <REDACTED_HOST>) | 🔵 飞书 | 客户端 — 创作/分镜/文案/日报/情报速递 |
| **云端** | <REDACTED_HOST> | 🟢 微信 | Hub 宿主机 — B站研报(22:20)/午盘(12:50)/日常对话 |
| **企微** | <REDACTED_HOST> | 🟣 企业微信 | 客户端 — 企微通道对话 |

## 分工

| 通道 | 节点 | 职责 |
|------|------|------|
| 🟢 微信 | 云端 <REDACTED_HOST> | B站研报(22:20)、午盘速报(12:50)、日常对话 |
| 🔵 飞书 | Mac 本地 | 创作(分镜/文案/剧本)、日报、情报速递 |
| 🟣 企业微信 | 企微 <REDACTED_HOST> | 企微通道对话 |

## 通信方式：HTTP mesh-bridge

云端运行 mesh-bridge v2，端口 9000，Bearer Token 认证。

**Token:** `vMEUYSO57CA0Zhde-fZc8m4BebqaI6FqVjzObG42nig`

**安全组：** 腾讯云只开放 TCP 9000（<REDACTED_HOST>/0），token 防未授权访问。

### 读收件箱（GET /）
```bash
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" \
  http://<REDACTED_HOST>:9000/
```

### 发消息（POST /send）
```bash
curl -s -X POST \
  -H "Authorization: Bearer <REDACTED_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"sender":"local","content":"消息内容"}' \
  http://<REDACTED_HOST>:9000/send
```

### 标记已读（GET /mark/文件名）
```bash
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" \
  http://<REDACTED_HOST>:9000/mark/2026-05-31_1705_local.txt
```

### 健康检查（GET /health）
```bash
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" \
  http://<REDACTED_HOST>:9000/health
```

## 留言板协议

**位置：** 云端 `/home/ubuntu/Desktop/hermes/_inbox/`

**规则：**
- 文件名：`YYYY-MM-DD_HHmm_{local|cloud|deploy|reminder}.txt`
- 读完调用 `/mark/文件名` 加 `.done` 后缀
- **本地 Hermes 每次回复前，先 GET / 检查新消息**
- 云端 Hermes 本地直接读写 `_inbox/`，无需走 HTTP
- 用户说“告诉云端 Hermes / 通知云端 / 跟微信端说一声”时：用 `POST /send` 发一条简短、可执行的规则/任务说明；成功后必须看到 `{"ok": true, "file": "..."}` 再说已通知。不要把本地操作日志、token、调试细节发给云端。

⚠️ **同名覆盖陷阱**：文件名只到分钟（`HHmm`），同一分钟内同一 sender 的多条消息会互相覆盖，只保留最后一条。**传输多段文件时，每段必须间隔 ≥60 秒**（跨越分钟边界），或用不同 sender 标识区分。

### 飞书/微信输出长度纪律（强制）

读 mesh 时经常会拿到超长消息、base64 分片、审计包或完整报告。**不要把 GET / 的原始结果直接贴回聊天**，否则飞书/微信可能超长投递失败。

执行规则：
1. 拉取 mesh 后，先把完整 JSON/正文保存到本地文件（如 `~/Desktop/hermes/mesh/mesh_inbox_latest.json`），聊天里只发短摘要。
2. 飞书/微信单条默认控制在 **800 字以内**；cron/研报 final 建议 **500 字以内**。
3. 长内容先发“结论 + 目录”；必要时按 `1/3、2/3、3/3` 分段，每段只讲一个主题。
4. 超过 **1200 字**，或含全量持仓表、候选池、审计报告、研报正文、代码审计、base64 分片时，一律落为 `.md/.txt/.html/.docx` 文件；聊天只发摘要 + 路径/附件。
5. base64/大包只汇报 manifest、size、sha256、part 文件名和是否齐全，不贴正文。
6. 用户要求“看下 mesh / 完整阅读后告诉我”时：完整阅读发生在本地文件/脚本层，最终回复只给可执行结论，不输出原始长日志。

详细规则见 `references/output-length-discipline.md`。

### 本地 Mac 日历网关协议（零 token）

当云端需要创建主机/iCloud 日程且不希望云端持有 Apple 凭据时：云端只把固定格式消息写入 mesh-bridge，由本地 Mac cron 定时读取并写入 macOS Calendar。

**重要分支：** 如果用户明确要求“云端直写共享日历 / 1小时更新一次 / 不走本地网关”，则不要继续推进本地 mesh 网关；应切到 `hermes-agent` 中的 CalDAV 云端直写方案，先确认：个人行程写哪个日历、家庭/媳妇通道写哪个共享日历、cron 频率、Apple App 专用密码如何安全放置。

**本地已部署：**
- 脚本：`~/.hermes/scripts/calendar_mesh_gateway.py`
- cron：每 3 小时检查一次 mesh，`no_agent=true`，不消耗模型 token
- 默认目标日历：iCloud「日历」

**云端发送格式（必须结构化，不要自然语言）：**

```text
CALENDAR_ADD
title=事件标题
start=YYYY-MM-DD HH:MM
end=YYYY-MM-DD HH:MM
calendar=日历
location=可选地点
note=可选备注
```

**处理规则：**
- 本地脚本只解析 `CALENDAR_ADD` 块；字段缺 `title/start/end` 则不写入。
- 写入前按 `summary + start + end` 查重，避免重复事件。
- 写入成功后调用 `/mark/<filename>` 标记已读。
- 这条路径不走 AI，不费 token；mesh-bridge 只是留言板，真正写 iCloud 的动作发生在本地 Mac。

### 大文件传输协议

当需要传输文件（如技能包、原文）时，mesh-bridge 单条消息约 150KB 可行。超大文件分段规则：

1. `tar -czf` 打包 → `base64` 编码
2. 每段 ≤150000 字符，每隔 60+ 秒发一段避免覆盖
3. 每段前缀标记：`【FILE:PART N/TOTAL】`
4. 额外发一条拼装指令：`grep -v "^【FILE:"` 去前缀 → `cat p1 p2 | base64 -d > bundle.tar.gz`
5. 组装后验证：`wc -l` 检查行数

## 已部署资产（云端）

- mesh-bridge v2: `/home/ubuntu/.hermes/scripts/mesh-bridge.py`（nohup 后台运行）
- 每日同步 cron（本地）: `693fec83559f`（9:00 拉云端消息 + 推本地摘要）
- 25个自定义技能
- B站研报 cron（22:20）
- 午盘速报 cron（12:50）
- B站 Cookie（2026.11过期）
- Tavily API Key 已配
- **企微文件路由表**：见 `references/wecom-routing-table.md`（发文件到企微实例时按此结构归类）

### FileBrowser 不可用时的降级方案

云端 FileBrowser（端口 9001）可能因服务未启动或安全组未放行而不可达。此时通过 mesh-bridge 让云端 Hermes 直接交付内容：

1. `POST /send` 发请求给云端，说明需要的文件路径
2. 等待云端 Hermes 查信箱回复（云端是对话驱动，需用户在微信触发）
3. 从云端回复的信箱消息中提取内容

不依赖 FileBrowser 作唯一交付通道。

## 服务管理

```bash
# 查看进程
ps aux | grep mesh-bridge

# 停止
pkill -f mesh-bridge

# 启动
nohup python3 /home/ubuntu/.hermes/scripts/mesh-bridge.py 9000 > /dev/null 2>&1 &

# 健康检查
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" http://<REDACTED_HOST>:9000/health
```

⚠️ **已知故障模式**：mesh-bridge 可能进入"挂死"状态——端口监听但 HTTP 不响应。此时 `pkill` 重启即可。详见 `references/troubleshooting.md`。

**systemd 自启**：部署 `references/mesh-bridge.service` 到 `/etc/systemd/system/`，确保重启后自动拉起。

## 故障排查

详见 `references/troubleshooting.md`，涵盖：
- **KIKI 恢复流程**：Mac 断连时的第一恢复手段
- **安全组端口不匹配**：`Operation timed out` vs `Connection refused` 诊断
- **Cron 投递目标错误**：通道分属不同实例时的 `session timeout` 定位

- **本地 Mac 日历网关**：mesh → iCloud「日历」零 token 写入协议见 `references/local-calendar-mesh-gateway.md`。云端只发固定 `CALENDAR_ADD` 块，本地 cron 定时写 Calendar。

## 企微节点文件路由表（由企微 Hermes 维护）

往企微 <REDACTED_HOST> 发文件时，参照以下目录结构归类。不要发 Mac 路径（`/Users/rayna/`、`~/Desktop/`），技能中的路径应做环境判断，不要写死。

```
~/hermes-knowledge/          ← 知识原文
  ├ 参考书原文/专业书/
  │  ├ 市场营销.md
  │  └ 好战略坏战略.md
  ├ 营销引用/
  └ 历史项目/

~/.hermes/crm/wedding/       ← 婚礼CRM（8765/8766）

~/.hermes/skills/<cat>/      ← 技能目录

~/hermes-output/             ← 产出文档
  ├ 营销方案/
  ├ CRM报表/
  └ 工作日志/
```

> 详细路由表（含分类建议和发送最佳实践）见企微本地 `~/.hermes/skills/devops/workspace-conventions/references/cloud-routing-table.md`

## 跨实例通信原则

1. **不给其他实例写死优化指令**：发送技能/文件到另一个 Hermes 时，只传内容和安装指令，不要附带具体的"你应该这样优化"建议——你不了解对方的运行环境和业务场景。正确做法：发技能 + 说"根据你实际情况自行调整"。
2. **路径做环境判断**：技能中引用文件路径时，不做绝对路径假设（`/Users/rayna/`），用环境变量或相对路径。
3. **文件名中的空格**：避免文件名含空格（`监听哨 -20260419.docx`），用连字符代替（`监听哨-20260419.docx`）。

- **技能迁移**：完整的本地→企微/云端技能迁移流程（诊断→修复→打包→发送→间距控制）见 `references/skill-migration.md`
- 向其他节点发送指令时，只说"做什么"，不说"怎么做"——目标节点更了解自己的实际情况

### 跨节点委托原则

向另一 Hermes 实例发送技能/指令时：
- **指令说"做什么"，不说"怎么优化"**。你对对方的业务环境不了解，不要帮它定优化方向。只说"安装并根据你的实际情况优化"。
- 发送技能前，先检查 SKILL.md 是否为空、是否含 OpenClaw/旧环境路径。本次对话发现 3 个技能 SKILL.md 为空或损坏（medical-content-compliance、client-requirements-analyzer、medical-short-video-monthly-plan），修复后才可用。
- 技能跨节点传输 checklist 见 `references/skill-transfer-checklist.md`。

## 新节点接入流程

当新增一个 Hermes 节点（如企微）接入 mesh-bridge 时：

1. **验证连通性**：新节点 `curl -s http://<REDACTED_HOST>:9000/health` — 返回 401（缺 Token）说明端口通
2. **下发 Token**：`vMEUYSO57CA0Zhde-fZc8m4BebqaI6FqVjzObG42nig`
3. **教会读写**：新节点学会 `GET /`（拉收件箱）+ `POST /send`（发消息，指定 sender 标识）
4. **写入规则**：新节点 SOUL/memory 中写入"每次回复前先查收件箱"
5. **安全加固**（新节点是云服务器时）：
   - 本地 Mac 提供公网 IP + SSH 公钥
   - 云端通过 mesh-bridge 下发 ufw 规则：只放行本地 IP + 云端 IP 的 SSH
   - 关闭密码登录，只允许密钥认证
   - 公网 IP 查询：`curl -s icanhazip.com`（ifconfig.me 可能超时，icanhazip.com 更稳）

## 故障恢复

### KIKI 恢复路径（SSH不通时第一手段）
当 Mac 无法 SSH 连云端时，通过腾讯云控制台的 KIKI 智能助手执行命令：
1. 打开 https://console.cloud.tencent.com/ → 找云服务器实例
2. 跟 KIKI 用自然语言说："在 <REDACTED_HOST> 上执行 [命令]"
3. KIKI 可执行命令、管理安全组规则、修改防火墙

### 安全组端口不匹配排查
常见故障：安全组开了端口A，但服务监听在端口B。
- SSH: 确认安全组端口 = `ss -tlnp | grep sshd` 中的端口
- mesh-bridge: 安全组 + 监听端口必须一致
- 用 KIKI 查：`ss -tlnp | grep LISTEN`
- 用 KIKI 查安全组："查看安全组入方向规则"

### mesh-bridge 服务管理
```bash
# 查看进程
ps aux | grep mesh-bridge
# 停止
pkill -f mesh-bridge
# 启动
nohup python3 /home/ubuntu/.hermes/scripts/mesh-bridge.py 9000 > /dev/null 2>&1 &
# 验证
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" http://localhost:9000/health
```

### mesh-bridge 部署/更新流程
1. 本地 base64 编码新脚本 → POST /send 到云端 _inbox
2. KIKI 执行：解码 → 写入 → pkill 旧进程 → nohup 启动
3. 注意：KIKI 默认以 root 运行，需指定 `/home/ubuntu/` 完整路径

### 云端 Hermes 响应检查
- 云端 Hermes 是对话驱动的，不会主动查 _inbox
- 需在其 memory/cron prompt 中写"每次回复前先 GET / 检查 _inbox"
- 验证方式：去微信跟云端说"信箱"，观察它是否先读了 _inbox 再回复
