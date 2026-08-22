# 技能迁移：本地 → 企微/云端

将一个技能从本地 Mac 迁移到其他 Hermes 节点的标准流程。

## 步骤

### 1. 诊断（检查原始技能）
- 查看 SKILL.md 是否为空/残缺
- 搜索 OpenClaw 依赖：`grep -r "openclaw\|OpenClaw" path/to/skill/`
- 搜索旧路径：`grep -r "Desktop/openclaw\|/root/.openclaw" path/to/skill/`

常见问题：
- SKILL.md 为空（0字节）→ 需从 Python 脚本/textbank 推断重写
- 引用 `openclaw` 模块 → 去除或用标准库替代
- 引用不存在的依赖技能（如 `word-reader`）→ 改为 LLM 直接处理
- 路径写死 OpenClaw 路径 → 改为 Hermes 路径
- 技能藏在 zip 里没解压 → 先解压

### 2. 修复
- 写/重写 SKILL.md：加 Hermes frontmatter（name/description/triggers），保持核心框架
- 清理 Python 脚本：去掉 openclaw/wecom_mcp 等不可用依赖
- 统一输出路径：`~/Desktop/hermes/`
- 保持 textbank/library 等配套文件不变

### 3. 打包
```bash
cd parent/dir
tar -czf /tmp/skill-name.tar.gz skill-directory/
ls -lh /tmp/skill-name.tar.gz  # 确认大小
```
150KB 以内可单次发送，超过需分段。

### 4. 发送（mesh-bridge）
```python
import base64, json, subprocess
with open('/tmp/skill-name.tar.gz', 'rb') as f:
    data = base64.b64encode(f.read()).decode()

msg = f"""【SKILL BUNDLE】skill-name.tar.gz
描述...
base64 -d << 'B64EOF' > /tmp/skill-name.tar.gz
{data}
B64EOF
tar -xzf /tmp/skill-name.tar.gz -C ~/.hermes/skills/business/
装完回信箱确认。"""

payload = json.dumps({"sender": "local", "content": msg})
subprocess.run(['curl', '-s', '-X', 'POST',
    'http://<REDACTED_HOST>:9000/send',
    '-H', 'Authorization: Bearer <REDACTED_TOKEN>',
    '-H', 'Content-Type: application/json', '-d', payload])
```

### 5. 多文件间距
⚠️ 同分钟内同 sender 消息会互相覆盖。连续发多个 tar.gz 时，每段间隔 ≥65 秒（`time.sleep(65)`）。

## 陷阱
- **不要替目标节点"优化"** — 不了解它的实际情况，让它自己判断
- 目标节点回信说缺参考文件（如 Obsidian 笔记路径）→ 那些路径是本地 Mac 独有的，目标节点需自行获取或让用户提供
- 检查不止一个位置：`~/Desktop/云/1/skills/`、`~/.openclaw/workspace-custis-ordo/skills/`、`~/Desktop/云/ai备份/` 都可能藏有技能
