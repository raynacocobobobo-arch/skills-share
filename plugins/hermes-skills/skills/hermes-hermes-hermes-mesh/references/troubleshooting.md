# 双 Hermes 通信故障排查

## KIKI 恢复（第一手段）

当 Mac 无法 SSH/HTTP 连云端时，通过腾讯云 KIKI 执行命令：

### 基本操作
- **检查状态**: `hostname && ss -tlnp | grep LISTEN && ps aux | grep mesh-bridge`
- **重启服务**: `pkill -f mesh-bridge && sleep 1 && nohup python3 /home/ubuntu/.hermes/scripts/mesh-bridge.py 9000 > /dev/null 2>&1 &`
- **管理安全组**: KIKI 可直接修改安全组入方向规则（开放/关闭端口）

### 远程部署文件
当需要把本地脚本部署到云端但无法 SSH 时：
1. 本地 `base64` 编码脚本
2. `POST /send` 发送到云端 `_inbox`（base64 作为 content）
3. KIKI 解码写入: `python3 -c "import base64; b64=open('/home/ubuntu/Desktop/hermes/_inbox/FILENAME').read(); open('TARGET','w').write(base64.b64decode(b64).decode())"`
4. KIKI 重启服务

### 添加 SSH 公钥
1. 本地生成密钥对: `ssh-keygen -t ed25519 -f /tmp/hermes_mesh_key -N ""`
2. KIKI 执行: `echo 'PUBLIC_KEY_CONTENT' >> ~/.ssh/authorized_keys`

## mesh-bridge 同名覆盖陷阱（文件名冲突）⚠️ 新增

**症状**: 同一分钟内连续发多条 POST /send，最后 inbox 只保留最后一条，前面的全部丢失。

**根因**: mesh-bridge 文件命名格式为 `YYYY-MM-DD_HHmm_{sender}.txt`，精度只到分钟。同一分钟内同一 sender 的多条消息写入同名文件，后发覆盖先发。

**重现场景**:
- 文件分段传输时，多条消息在同一分钟发出 → 只留最后一段
- 指令消息紧跟数据段 → 指令覆盖数据，或数据覆盖指令

**正确做法——大文件分段传输协议**:
```
1. 打包: tar -czf bundle.tar.gz <files>
2. 编码: base64 -i bundle.tar.gz > bundle.b64
3. 分段: split -b 150000 bundle.b64 part_（或用 Python 切片）
4. 逐段发送，每段间隔 ≥60 秒穿越分钟边界
5. 每段加前缀: 【FILE:PART N/TOTAL】
6. 发完所有段后，再发一条拼装指令:
   - 用 grep -v "^【FILE:" 去前缀
   - cat p1 p2 | base64 -d > bundle.tar.gz
   - 验证完整性
```

**macOS base64 注意**: macOS 的 `base64` 命令语法是 `base64 -i input -o output`，不同于 Linux 的 `base64 input`。

**公网 IP 查询备选**: `curl -s ifconfig.me` 可能在 Mac 上超时，用 `curl -s icanhazip.com` 更稳。

## mesh-bridge 进程挂死（端口监听但不响应）

**症状**: 
- `curl` mesh-bridge 返回超时（不是 `Connection refused`）
- 但 `ss -tlnp | grep 9000` 显示端口在监听
- `ps aux | grep mesh-bridge` 显示进程存在
- 就是 HTTP 请求不响应

**根因**: 进程挂死（hung），socket 还占着但事件循环或某个请求处理卡住了，不再 accept 新连接。

**修复**:
```bash
# KIKI 执行
pkill -f mesh-bridge
sleep 1
nohup python3 /home/ubuntu/.hermes/scripts/mesh-bridge.py 9000 > /dev/null 2>&1 &

# 验证
curl -s -H "Authorization: Bearer <REDACTED_TOKEN>" http://localhost:9000/health
```

**预防**: 给 mesh-bridge 加 systemd 自启服务，云服务器重启后自动拉起。示例 unit 文件见 `references/mesh-bridge.service`。

## 安全组端口不匹配（诊断陷阱）

**症状**: SSH 连接报 `Operation timed out`（不是 `Connection refused`），但 `ping` 也可能不通（云服禁 ICMP 是正常的）。

**根因**: 安全组开放的端口（如 2222）与 SSHD 实际监听端口（22）不一致。安全组允许流量到达但服务器端口上没服务监听，TCP SYN 包被丢弃，表现为超时而非拒绝。

**区分**:
- `Connection refused` → 端口可达但无服务监听（RST 包）
- `Operation timed out` → 安全组丢弃包，或网络层不可达
- 当且仅当安全组端口 ≠ SSHD 端口时，表现类似网络不通

**修复**: 要么在安全组加 22 端口，要么改 SSHD 监听端口。用 KIKI 执行。

## Cron 投递目标错误

**症状**: Cron job `last_status=ok` 但 `last_delivery_error: session timeout`，用户收不到推送。

**根因**: 通道（微信/飞书）在云端，本地 Hermes 的 `send_message→weixin` 会超时。反之亦然。

**检查清单**（每次改架构后）:
| Cron 位置 | 推送目标 | 应否 |
|-----------|----------|------|
| 本地 Mac | weixin | ❌ 改成 origin（飞书） |
| 云端 | origin（飞书） | ❌ 改成 weixin |
| 本地 Mac | origin | ✅ |
| 云端 | weixin | ✅ |
| 任意 | local | ✅ 不推送，无影响 |

**修复**: `cronjob action=update job_id=XXX deliver=origin` (或 weixin，取决于所在位置)
