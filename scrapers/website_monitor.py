import difflib
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from config import SNAPSHOTS_DIR, WEBSITE_CHANGE_THRESHOLD, WEBSITE_DATA_DIR
from scrapers.common import fetch_html, load_competitors, now_iso, save_json, soup_text


def normalized_text(html: str) -> str:
    return " ".join(soup_text(html).split())


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def monitor_websites():
    rows = load_competitors()
    results = []
    changes = []

    for row in rows:
        url = (row.get("website_url") or "").strip()
        if not url:
            continue
        key = hashlib.md5(f"{row['market']}::{row['name']}::{url}".encode()).hexdigest()[:12]
        snap = Path(SNAPSHOTS_DIR) / f"{key}.txt"
        try:
            html = fetch_html(url)
            current = normalized_text(html)
            prev = snap.read_text(encoding="utf-8") if snap.exists() else ""
            sim = similarity(prev, current) if prev else 1.0
            change_ratio = round(1 - sim, 4)
            changed = bool(prev) and change_ratio >= WEBSITE_CHANGE_THRESHOLD
            if changed:
                diff_preview = "\n".join(list(difflib.unified_diff(prev.splitlines()[:200], current.splitlines()[:200], lineterm=""))[:80])
                changes.append({
                    "market": row["market"], "name": row["name"], "url": url,
                    "change_ratio": change_ratio, "detected_at": now_iso(), "diff_preview": diff_preview,
                })
            snap.parent.mkdir(parents=True, exist_ok=True)
            snap.write_text(current, encoding="utf-8")
            results.append({
                "market": row["market"], "name": row["name"], "url": url,
                "status": "ok", "change_ratio": change_ratio, "changed": changed, "last_checked": now_iso(),
            })
        except Exception as e:
            results.append({
                "market": row["market"], "name": row["name"], "url": url,
                "status": "error", "error": str(e)[:240], "last_checked": now_iso(),
                "change_ratio": None, "changed": False,
            })

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = {"date": stamp, "count": len(results), "results": results, "changes": changes}
    save_json(Path(WEBSITE_DATA_DIR) / f"{stamp}.json", payload)
    save_json(Path(WEBSITE_DATA_DIR) / "latest.json", payload)
    return payload


if __name__ == "__main__":
    out = monitor_websites()
    print(f"Tracked websites: {out['count']}, significant changes: {len(out['changes'])}")
