#!/usr/bin/python3
"""Bilibili provider for Hermes Knowledge Scout.

Reuses the WBI-signing + SESSDATA-cookie + AI-subtitle logic proven in
bilibili-tracker.py, but emits assets shaped like the YouTube provider so the
knowledge-library pipeline (generate-research-input.py) treats them uniformly.

Runs under the SYSTEM python (/usr/bin/python3) because it needs bilibili_api,
which is not installed in the Knowledge Scout venv.
"""

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from urllib.parse import urlencode

import requests

try:
    from bilibili_api import user, sync
    HAS_BILIBILI_API = True
except ImportError:
    HAS_BILIBILI_API = False

VIDEO_URL = "https://www.bilibili.com/video/{bvid}"

MIXIN_ENC = [46,47,18,2,53,8,23,32,15,50,10,31,58,3,45,35,27,43,5,49,33,9,42,19,29,28,14,39,12,38,41,13,37,48,7,16,24,55,40,61,26,17,0,1,60,51,30,4,22,25,54,21,56,59,6,63,57,62,11,36,20,34,44,52]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'Referer': 'https://www.bilibili.com'}

COOKIE_FILE = os.path.expanduser("~/.hermes/data/bilibili/cookies.json")

_sessdata = None
_mixin_key = None


def get_sessdata():
    global _sessdata
    if _sessdata is None:
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE) as f:
                _sessdata = json.load(f).get("SESSDATA", "")
    return _sessdata


def get_mixin_key():
    global _mixin_key
    if _mixin_key is None:
        try:
            nav = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=HEADERS, timeout=10).json()
            img = nav['data']['wbi_img']['img_url'].split('/')[-1].split('.')[0]
            sub = nav['data']['wbi_img']['sub_url'].split('/')[-1].split('.')[0]
            _mixin_key = ''.join((img + sub)[i] for i in MIXIN_ENC)[:32]
        except Exception:
            _mixin_key = ""
    return _mixin_key


def wbi_sign(params):
    mk = get_mixin_key()
    sorted_str = '&'.join(f'{k}={params[k]}' for k in sorted(params.keys()))
    return hashlib.md5((sorted_str + mk).encode()).hexdigest()


def get_latest_videos(source, limit=5, cookie_path=None):
    """Return the UP主's N latest videos as asset dicts (bvid/title/url/published)."""
    uid = source.get("uid")
    if not uid:
        return []

    name = source.get("name", "")

    if HAS_BILIBILI_API:
        try:
            u = user.User(uid)
            data = sync(u.get_media_list(ps=limit))
            entries = data.get("media_list", [])
        except Exception:
            entries = []
    else:
        entries = _fetch_videos_wbi(uid, limit)

    videos = []
    for v in entries:
        bvid = v.get("bv_id") or v.get("bvid") or ""
        if not bvid:
            continue
        pubtime = v.get("pubtime", 0) or v.get("created", 0)
        videos.append({
            "video_id": bvid,
            "title": v.get("title", ""),
            "channel": name,
            "url": VIDEO_URL.format(bvid=bvid),
            "published": datetime.fromtimestamp(pubtime, tz=timezone.utc).isoformat() if pubtime else None,
        })
    return videos


def _fetch_videos_wbi(uid, limit):
    """Fallback video list via WBI-signed x/space/wbi/arc/search."""
    params = {"mid": uid, "ps": limit, "pn": 1, "order": "pubdate"}
    params["wts"] = int(time.time())
    params["w_rid"] = wbi_sign(params)
    query = urlencode(params)
    try:
        r = requests.get(f"https://api.bilibili.com/x/space/wbi/arc/search?{query}",
                         headers=HEADERS, cookies={'SESSDATA': get_sessdata()}, timeout=10)
        data = r.json()
        if data.get("code") != 0:
            return []
        return data.get("data", {}).get("list", {}).get("vlist", [])
    except Exception:
        return []


def fetch_subtitle(bvid, cookie_path=None):
    """Fetch the AI/CC subtitle text for a video, or None."""
    sessdata = get_sessdata()
    try:
        r = requests.get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}',
                         headers=HEADERS, timeout=10)
        info = r.json()
        if info.get('code') != 0:
            return None
        aid = info['data']['aid']
        cid = info['data']['cid']

        params = {'aid': aid, 'cid': cid, 'wts': int(time.time())}
        params['w_rid'] = wbi_sign(params)
        query = '&'.join(f'{k}={params[k]}' for k in sorted(params.keys()))
        r2 = requests.get(f'https://api.bilibili.com/x/player/wbi/v2?{query}',
                          headers=HEADERS, cookies={'SESSDATA': sessdata}, timeout=10)
        pdata = r2.json()
        if pdata.get('code') != 0:
            return None

        subs = pdata.get('data', {}).get('subtitle', {}).get('subtitles', [])
        if not subs:
            return None

        sub_url = subs[0].get('subtitle_url', '')
        if sub_url.startswith('//'):
            sub_url = 'https:' + sub_url

        r3 = requests.get(sub_url, headers={'Referer': 'https://www.bilibili.com'}, timeout=10)
        body = r3.json().get('body', [])
        text = ' '.join(item.get('content', '') for item in body)
        return text if text else None
    except Exception:
        return None


def build_metadata(bvid, title, channel, url=None, published=None, collected_at=None):
    return {
        "source_id": f"bilibili:{bvid}",
        "platform": "bilibili",
        "channel": channel,
        "title": title,
        "url": url or VIDEO_URL.format(bvid=bvid),
        "published": published,
        "collected_at": collected_at or datetime.now(timezone.utc).isoformat(),
    }
