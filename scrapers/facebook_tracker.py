from datetime import datetime, timezone
from pathlib import Path

from config import FACEBOOK_DATA_DIR
from scrapers.common import SocialMetric, fetch_html, load_competitors, now_iso, parse_followers_from_text, save_json, soup_text


def track_facebook():
    rows = load_competitors()
    results = []
    for row in rows:
        fb = (row.get("facebook_url") or "").strip()
        if not fb:
            continue
        try:
            html = fetch_html(fb)
            text = soup_text(html)
            followers = parse_followers_from_text(text)
            results.append(SocialMetric(
                market=row["market"],
                name=row["name"],
                url_or_handle=fb,
                platform="facebook",
                followers=followers,
                posts=None,
                engagement_rate=None,
                last_post_age_days=None,
                last_checked=now_iso(),
                status="ok" if followers is not None else "partial",
                error=None if followers is not None else "followers_not_found_on_public_page",
            ).__dict__)
        except Exception as e:
            results.append(SocialMetric(
                market=row["market"],
                name=row["name"],
                url_or_handle=fb,
                platform="facebook",
                followers=None,
                posts=None,
                engagement_rate=None,
                last_post_age_days=None,
                last_checked=now_iso(),
                status="error",
                error=str(e)[:240],
            ).__dict__)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    payload = {"date": stamp, "platform": "facebook", "count": len(results), "results": results}
    save_json(Path(FACEBOOK_DATA_DIR) / f"{stamp}.json", payload)
    save_json(Path(FACEBOOK_DATA_DIR) / "latest.json", payload)
    return payload


if __name__ == "__main__":
    out = track_facebook()
    print(f"Tracked Facebook entries: {out['count']}")
