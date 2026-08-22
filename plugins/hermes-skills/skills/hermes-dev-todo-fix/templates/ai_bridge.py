#!/usr/bin/env python3
"""HermesTodo AI Bridge — localhost:8765
v5: JSON retry on parse failure, 3-round history, options field
Copy and customize DEEPSEEK_KEY path.
"""
import json, os, uuid, requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# Read API key — customize this path
with open("/tmp/hermestodo_api_key.txt") as f:
    DEEPSEEK_KEY = f.read().strip()

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

SYSTEM_PROMPT = """你是一个实用的待办清单助手。

工作流程：
1. 用户需求足够具体 → 直接列出待办清单（suggestions），reply 简短解释。
2. 用户需求太宽泛 → reply 一句话反问引导，options 列出2-3个具体方向（每项≤15字），suggestions空。
   reply 不要包含编号列表！编号列表会通过UI按钮显示。

输出规则：
- 每条待办必须具体可执行。
- 一个回答的所有待办归入同一个情境（context）。
- priority：high=不做会出问题，medium=最好做。
- 返回纯JSON：{"reply":"...","suggestions":[{"title":"...","context":"情境名","priority":"high"}],"options":[]}
- 反问时：{"reply":"简短引导","suggestions":[],"options":["选项1","选项2","选项3"]}
- 用户后续输入可能是对选项的选择，直接给出该方向的待办清单。"""

CONVERSATION_HISTORY = []
MAX_HISTORY = 6  # 保留最近3轮对话
RESP_CACHE = {}

class Bridge(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/clear":
            CONVERSATION_HISTORY.clear()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "cleared"}).encode())
            return

        if self.path != "/ask":
            self.send_error(404); return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        msg = body.get("message", "")
        rid = str(uuid.uuid4())[:8]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(CONVERSATION_HISTORY[-MAX_HISTORY:])
        messages.append({"role": "user", "content": msg})

        try:
            resp = requests.post(API_URL, json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }, headers={
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
                "Content-Type": "application/json"
            }, timeout=30)
            data = resp.json()
            content = data["choices"][0]["message"]["content"].strip()

            if not content:
                raise ValueError("Empty response")

            # Strip markdown wrapping
            clean = content
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1] if "\n" in clean else clean[3:]
                if clean.endswith("```"):
                    clean = clean[:-3]
                clean = clean.strip()
            if clean.startswith("json"):
                clean = clean[4:].strip()

            # Try JSON parse; retry once if fails
            try:
                result = json.loads(clean)
                if not isinstance(result, dict):
                    raise json.JSONDecodeError("Not a dict", clean, 0)
                result.setdefault("options", [])
                result.setdefault("suggestions", [])
            except (json.JSONDecodeError, ValueError):
                # Retry: ask AI to reformat as JSON
                retry_resp = requests.post(API_URL, json={
                    "model": MODEL,
                    "messages": [{"role": "system", "content": "你只输出JSON。"},
                                 {"role": "user", "content": f"请把以下内容转为标准JSON格式（必须包含reply、suggestions、options字段）：\n\n{clean}"}],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }, headers={
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                    "Content-Type": "application/json"
                }, timeout=30)
                retry_content = retry_resp.json()["choices"][0]["message"]["content"].strip()
                try:
                    result = json.loads(retry_content)
                    if not isinstance(result, dict):
                        result = {"reply": retry_content, "suggestions": [], "options": []}
                    result.setdefault("options", [])
                    result.setdefault("suggestions", [])
                except (json.JSONDecodeError, ValueError):
                    result = {"reply": content, "suggestions": [], "options": []}

            result["id"] = rid
            result["status"] = "done"

            CONVERSATION_HISTORY.append({"role": "user", "content": msg})
            CONVERSATION_HISTORY.append({"role": "assistant", "content": result.get("reply", "")})

        except Exception as e:
            result = {
                "id": rid, "status": "done",
                "reply": f"出了点问题：{str(e)[:80]}。请重试。",
                "suggestions": [], "options": []
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

    def do_GET(self):
        if self.path.startswith("/response"):
            rid = self.path.split("id=")[-1] if "id=" in self.path else ""
            resp = RESP_CACHE.get(rid, {"status": "pending"})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode())
        elif self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("AI Bridge v5 running on http://localhost:8765")
    HTTPServer(("127.0.0.1", 8765), Bridge).serve_forever()
