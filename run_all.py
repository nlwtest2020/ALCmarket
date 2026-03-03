from pathlib import Path
import json
from datetime import datetime, timezone

from scrapers.facebook_tracker import track_facebook
from scrapers.instagram_tracker import track_instagram
from scrapers.website_monitor import monitor_websites


def status_breakdown(results):
    out = {"ok": 0, "partial": 0, "error": 0}
    for r in results:
        s = r.get("status", "error")
        out[s] = out.get(s, 0) + 1
    return out


def build_summary(fb, ig, web):
    by_name = {}
    for item in fb["results"]:
        rec = by_name.setdefault(item["name"], {"market": item["market"], "name": item["name"]})
        rec["facebook_followers"] = item.get("followers")
        rec["facebook_status"] = item.get("status")
        rec["facebook_error"] = item.get("error")
    for item in ig["results"]:
        rec = by_name.setdefault(item["name"], {"market": item["market"], "name": item["name"]})
        rec["instagram_followers"] = item.get("followers")
        rec["instagram_status"] = item.get("status")
        rec["instagram_error"] = item.get("error")
    for item in web["results"]:
        rec = by_name.setdefault(item["name"], {"market": item["market"], "name": item["name"]})
        rec["website_change_ratio"] = item.get("change_ratio")
        rec["website_status"] = item.get("status")
        rec["website_error"] = item.get("error")

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "totals": {
            "facebook_tracked": fb["count"],
            "instagram_tracked": ig["count"],
            "websites_tracked": web["count"],
            "website_changes": len(web.get("changes", [])),
        },
        "status": {
            "facebook": status_breakdown(fb["results"]),
            "instagram": status_breakdown(ig["results"]),
            "website": status_breakdown(web["results"]),
        },
        "competitors": sorted(by_name.values(), key=lambda x: (x.get("market", ""), x["name"])),
        "website_changes": web.get("changes", []),
    }


def main():
    fb = track_facebook()
    ig = track_instagram()
    web = monitor_websites()
    summary = build_summary(fb, ig, web)

    paths = [
        Path("data/dashboard/latest_summary.json"),
        Path("alc-presentation/public/data/latest_summary.json"),
    ]
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Monitoring run complete.")


if __name__ == "__main__":
    main()
