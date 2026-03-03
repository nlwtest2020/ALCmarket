from datetime import datetime, timezone
from pathlib import Path

from config import INSTAGRAM_DATA_DIR
from scrapers.common import SocialMetric, fetch_html, load_competitors, now_iso, parse_followers_from_text, save_json, soup_text


def track_instagram():
    rows = load_competitors()
    results = []
    for row in rows:
        handle = (row.get("instagram_handle") or "").strip()
        if not handle:
            continue
        url = f"https://www.instagram.com/{handle}/"
        try:
            html = fetch_html(url)
            text = soup_text(html)
            followers = parse_followers_from_text(text)
            results.append(SocialMetric(
                market=row["market"],
                name=row["name"],
                url_or_handle=handle,
                platform="instagram",
                followers=followers,
                posts=None,
                engagement_rate=None,
                last_post_age_days=None,
                last_checked=now_iso(),
                status="ok" if followers is not None else "partial",
                error=None if followers is not None else "followers_not_found_on_public_profile",
            ).__dict__)
        except Exception as e:
            results.append(SocialMetric(
                market=row["market"],
                name=row["name"],
                url_or_handle=handle,
                platform="instagram",
                followers=None,
                posts=None,
                engagement_rate=None,
                last_post_age_days=None,
                last_checked=now_iso(),
                status="error",
                error=str(e)[:240],
            ).__dict__)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = {"date": stamp, "platform": "instagram", "count": len(results), "results": results}
    save_json(Path(INSTAGRAM_DATA_DIR) / f"{stamp}.json", payload)
    save_json(Path(INSTAGRAM_DATA_DIR) / "latest.json", payload)
    return payload


if __name__ == "__main__":
    out = track_instagram()
    print(f"Tracked Instagram entries: {out['count']}")
