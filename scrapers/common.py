import csv
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import COMPETITORS_CSV, REQUEST_TIMEOUT, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}


@dataclass
class SocialMetric:
    market: str
    name: str
    url_or_handle: str
    platform: str
    followers: Optional[int]
    posts: Optional[int]
    engagement_rate: Optional[float]
    last_post_age_days: Optional[int]
    last_checked: str
    status: str
    error: Optional[str] = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_competitors():
    with open(COMPETITORS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch_html(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r.text


def parse_followers_from_text(text: str) -> Optional[int]:
    # Examples: "12,345 followers", "12.3K followers", "1.2M"
    m = re.search(r"([\d.,]+)\s*([KMB])?\s+followers", text, re.IGNORECASE)
    if not m:
        return None
    num = float(m.group(1).replace(",", ""))
    suffix = (m.group(2) or "").upper()
    mult = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
    return int(num * mult)


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def soup_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return " ".join(soup.stripped_strings)
