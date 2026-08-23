"""Generate research-input.md from collected raw assets.

Reads metadata.json + transcript.md from all collected YouTube assets,
structures them into a ChatGPT-ready input file with NO analysis or judgment.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


RAW_YOUTUBE_DIR = Path("shared/knowledge-library/raw/youtube")
ANALYSIS_QUEUE = Path("shared/knowledge-library/analysis-queue.jsonl")
OUTPUT_DIR = Path("data/latest")
OUTPUT_FILE = OUTPUT_DIR / "research-input.md"

CHINA_TZ = timezone(datetime.now().astimezone().utcoffset() or __import__("datetime").timedelta(hours=8))


def load_assets():
    """Load all collected assets from raw youtube directory."""
    assets = []
    if not RAW_YOUTUBE_DIR.exists():
        return assets

    for metadata_path in sorted(RAW_YOUTUBE_DIR.glob("*/*/metadata.json")):
        try:
            metadata = json.loads(metadata_path.read_text())
        except json.JSONDecodeError:
            continue

        asset_dir = metadata_path.parent
        transcript_path = asset_dir / "transcript.md"
        transcript = ""
        if transcript_path.exists():
            transcript = transcript_path.read_text().strip()

        assets.append({
            "metadata": metadata,
            "transcript": transcript,
            "directory": str(asset_dir),
        })

    return assets


def load_queue():
    """Load pending analysis queue items."""
    items = []
    if not ANALYSIS_QUEUE.exists():
        return items
    for line in ANALYSIS_QUEUE.read_text().splitlines():
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return items


def is_today(date_str):
    """Check if a date string is from today (China time)."""
    try:
        dt = datetime.fromisoformat(date_str)
        now = datetime.now(CHINA_TZ)
        return dt.date() == now.date()
    except (ValueError, TypeError):
        return False


def extract_summary(transcript, max_chars=800):
    """Extract first N characters as summary — no analysis, just truncation."""
    if not transcript:
        return "（无字幕）"
    return transcript[:max_chars] + ("..." if len(transcript) > max_chars else "")


def extract_entities(transcript):
    """Extract mentioned entities from transcript — no analysis, just keyword matching."""
    entities = {"stocks": [], "industries": [], "topics": []}

    keywords = {
        "stocks": ["NVDA", "NVIDIA", "TSLA", "Tesla", "AAPL", "Apple", "MSFT", "Microsoft",
                    "GOOGL", "Google", "META", "Meta", "AMZN", "Amazon", "AMD", "ARM",
                    "SMCI", "PLTR", "SNOW", "CRWD", "NET", "DDOG"],
        "industries": ["AI", "半导体", "芯片", "云计算", "SaaS", "自动驾驶", "机器人",
                       "新能源", "金融科技", "生物医药", "电商", "社交"],
        "topics": ["ChatGPT", "GPT", "Claude", "Gemini", "LLM", "大模型", "Agent",
                   "RAG", "fine-tuning", "prompt", "workflow", "automation"],
    }

    for category, terms in keywords.items():
        for term in terms:
            if term.lower() in transcript.lower():
                if term not in entities[category]:
                    entities[category].append(term)

    return entities


def extract_key_quote(transcript, max_len=200):
    """Extract first substantive paragraph as key quote."""
    if not transcript:
        return ""
    paragraphs = [p.strip() for p in transcript.split("\n\n") if len(p.strip()) > 50]
    if not paragraphs:
        paragraphs = [p.strip() for p in transcript.split("\n") if len(p.strip()) > 30]
    if not paragraphs:
        return transcript[:max_len]
    return paragraphs[0][:max_len]


def generate():
    now = datetime.now(CHINA_TZ)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = load_assets()
    queue = load_queue()

    today_assets = [a for a in assets if is_today(a["metadata"].get("collected_at", ""))]
    all_assets = assets

    lines = []
    lines.append("# Hermes Research Input")
    lines.append("")
    lines.append(f"日期：{now.strftime('%Y-%m-%d')}")
    lines.append(f"生成时间：{now.strftime('%Y-%m-%d %H:%M:%S')} CST")
    lines.append("")

    # Data sources
    lines.append("## 数据来源")
    lines.append("")
    channels = sorted(set(a["metadata"]["channel"] for a in all_assets))
    for channel in channels:
        lines.append(f"- YouTube: {channel}")
    lines.append("")

    # Today's new content
    lines.append("## 今日新增内容")
    lines.append("")

    if not today_assets:
        lines.append("（今日无新增采集内容）")
        lines.append("")

    for asset in today_assets:
        meta = asset["metadata"]
        transcript = asset["transcript"]

        lines.append(f"### {meta['channel']}")
        lines.append("")
        lines.append(f"视频/文章：{meta['title']}")
        lines.append(f"链接：{meta['url']}")
        published = meta.get("published", "未知")
        lines.append(f"发布时间：{published}")
        lines.append("")

        summary = extract_summary(transcript)
        lines.append("原始内容摘要（仅整理，不判断）：")
        lines.append(f"- {summary}")
        lines.append("")

        entities = extract_entities(transcript)
        lines.append("涉及对象：")
        lines.append(f"股票：{', '.join(entities['stocks']) if entities['stocks'] else '（无）'}")
        lines.append(f"行业：{', '.join(entities['industries']) if entities['industries'] else '（无）'}")
        lines.append(f"主题：{', '.join(entities['topics']) if entities['topics'] else '（无）'}")
        lines.append("")

        quote = extract_key_quote(transcript)
        if quote:
            lines.append("关键原文：")
            lines.append(f"> {quote}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # All material index
    lines.append("## 今日全部素材索引")
    lines.append("")

    for asset in all_assets:
        meta = asset["metadata"]
        lines.append(f"- `{asset['directory']}`")
        lines.append(f"  - {meta['title']}")
        lines.append(f"  - {meta['url']}")
        lines.append("")

    lines.append(f"文件：{len(all_assets)} 个目录")
    lines.append(f"路径：{RAW_YOUTUBE_DIR}")
    lines.append(f"数量：{len(all_assets)} 个素材")
    lines.append("")

    # Pending analysis queue
    if queue:
        pending = [q for q in queue if q.get("status") == "pending"]
        if pending:
            lines.append("## 待分析队列")
            lines.append("")
            for item in pending:
                lines.append(f"- {item['source_id']} → {item['task']}")
            lines.append("")

    output = OUTPUT_FILE
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(output)


if __name__ == "__main__":
    path = generate()
    print(f"Generated: {path}")