"""
Flask dashboard for ALC Competitive Intelligence Tracker
Displays competitor social media, engagement, and website change analytics
"""
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from flask import Flask, render_template, request, jsonify

from config import (
    COMPETITORS_CSV,
    FACEBOOK_DATA_DIR,
    INSTAGRAM_DATA_DIR,
    WEBSITE_DATA_DIR,
)

# Create Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_SORT_KEYS"] = False

logger = logging.getLogger(__name__)


# Helper functions
def load_competitors_csv() -> pd.DataFrame:
    """Load competitors from CSV"""
    try:
        return pd.read_csv(COMPETITORS_CSV)
    except Exception as e:
        logger.error(f"Error loading competitors CSV: {e}")
        return pd.DataFrame()


def load_latest_facebook_data(market: Optional[str] = None) -> Dict:
    """Load latest Facebook scraping data"""
    facebook_files = sorted(FACEBOOK_DATA_DIR.glob("*.json"), reverse=True)

    for file_path in facebook_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if market is None or any(
                    c.get("market") == market for c in data.get("competitors", [])
                ):
                    return data
        except Exception as e:
            logger.debug(f"Error loading {file_path}: {e}")

    return {"competitors": [], "scraped_at": None}


def load_latest_instagram_data(market: Optional[str] = None) -> Dict:
    """Load latest Instagram scraping data"""
    instagram_files = sorted(INSTAGRAM_DATA_DIR.glob("*.json"), reverse=True)

    for file_path in instagram_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if market is None or any(
                    c.get("market") == market for c in data.get("competitors", [])
                ):
                    return data
        except Exception as e:
            logger.debug(f"Error loading {file_path}: {e}")

    return {"competitors": [], "scraped_at": None}


def load_website_changes(days: int = 30) -> List[Dict]:
    """Load recent website change detection results"""
    changes = []
    cutoff_date = datetime.now() - timedelta(days=days)

    for file_path in WEBSITE_DATA_DIR.glob("changes_*.json"):
        try:
            file_date = datetime.strptime(file_path.stem.split("_")[1], "%Y-%m-%d")
            if file_date >= cutoff_date:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    changes.extend(data.get("changes_detected", []))
        except Exception as e:
            logger.debug(f"Error loading {file_path}: {e}")

    return sorted(changes, key=lambda x: x.get("checked_at", ""), reverse=True)


def get_market_summary(market: str) -> Dict:
    """Get summary data for a market"""
    competitors = load_competitors_csv()
    market_competitors = competitors[competitors["market"] == market]

    facebook_data = load_latest_facebook_data(market)
    instagram_data = load_latest_instagram_data(market)

    summary = {
        "market": market,
        "total_competitors": len(market_competitors),
        "facebook_competitors": len(facebook_data.get("competitors", [])),
        "instagram_competitors": len(instagram_data.get("competitors", [])),
        "competitors": [],
    }

    # Aggregate competitor data
    facebook_dict = {c["competitor_name"]: c for c in facebook_data.get("competitors", [])}
    instagram_dict = {c["competitor_name"]: c for c in instagram_data.get("competitors", [])}

    for _, row in market_competitors.iterrows():
        comp_data = {
            "name": row["name"],
            "market": row["market"],
            "website_url": row["website_url"],
        }

        # Add Facebook data
        if row["name"] in facebook_dict:
            fb = facebook_dict[row["name"]]
            comp_data["facebook"] = {
                "followers": fb.get("followers"),
                "posting_frequency": fb.get("engagement_metrics", {}).get("posts_per_week", 0),
                "engagement_rate": fb.get("engagement_metrics", {}).get("avg_engagement_rate", 0),
            }

        # Add Instagram data
        if row["name"] in instagram_dict:
            ig = instagram_dict[row["name"]]
            comp_data["instagram"] = {
                "followers": ig.get("followers"),
                "posting_frequency": ig.get("engagement_metrics", {}).get("posts_per_week", 0),
                "engagement_rate": ig.get("engagement_metrics", {}).get("avg_engagement_rate", 0),
            }

        summary["competitors"].append(comp_data)

    return summary


def get_follower_trends(market: str, days: int = 90) -> Dict:
    """Get follower growth trends over time"""
    cutoff_date = datetime.now() - timedelta(days=days)

    facebook_files = sorted(FACEBOOK_DATA_DIR.glob("*.json"))
    instagram_files = sorted(INSTAGRAM_DATA_DIR.glob("*.json"))

    facebook_trends = {}
    instagram_trends = {}

    # Process Facebook data
    for file_path in facebook_files:
        try:
            file_date_str = file_path.stem.split("_")[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if file_date >= cutoff_date:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for comp in data.get("competitors", []):
                        if comp.get("market") == market:
                            name = comp["competitor_name"]
                            if name not in facebook_trends:
                                facebook_trends[name] = []
                            facebook_trends[name].append(
                                {
                                    "date": file_date_str,
                                    "followers": comp.get("followers", 0),
                                }
                            )
        except Exception as e:
            logger.debug(f"Error processing {file_path}: {e}")

    # Process Instagram data
    for file_path in instagram_files:
        try:
            file_date_str = file_path.stem.split("_")[0]
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            if file_date >= cutoff_date:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for comp in data.get("competitors", []):
                        if comp.get("market") == market:
                            name = comp["competitor_name"]
                            if name not in instagram_trends:
                                instagram_trends[name] = []
                            instagram_trends[name].append(
                                {
                                    "date": file_date_str,
                                    "followers": comp.get("followers", 0),
                                }
                            )
        except Exception as e:
            logger.debug(f"Error processing {file_path}: {e}")

    return {
        "facebook_trends": facebook_trends,
        "instagram_trends": instagram_trends,
        "market": market,
    }


# Routes
@app.route("/")
def index():
    """Main market overview page"""
    competitors = load_competitors_csv()
    markets = competitors["market"].unique().tolist()
    selected_market = request.args.get("market", markets[0] if markets else None)

    if not selected_market or selected_market not in markets:
        selected_market = markets[0] if markets else None

    market_summary = get_market_summary(selected_market) if selected_market else {}

    return render_template(
        "index.html", markets=markets, selected_market=selected_market, summary=market_summary
    )


@app.route("/trends")
def trends():
    """Trends page with follower growth charts"""
    competitors = load_competitors_csv()
    markets = competitors["market"].unique().tolist()
    selected_market = request.args.get("market", markets[0] if markets else None)
    date_range = request.args.get("range", "30")  # 30, 60, or 90 days

    if not selected_market or selected_market not in markets:
        selected_market = markets[0] if markets else None

    trends_data = get_follower_trends(selected_market, int(date_range)) if selected_market else {}

    return render_template(
        "trends.html",
        markets=markets,
        selected_market=selected_market,
        trends_data=trends_data,
        date_range=date_range,
    )


@app.route("/content-analysis")
def content_analysis():
    """Content analysis page with engagement metrics"""
    competitors = load_competitors_csv()
    markets = competitors["market"].unique().tolist()
    selected_market = request.args.get("market", markets[0] if markets else None)

    if not selected_market or selected_market not in markets:
        selected_market = markets[0] if markets else None

    market_summary = get_market_summary(selected_market) if selected_market else {}

    return render_template(
        "content_analysis.html",
        markets=markets,
        selected_market=selected_market,
        summary=market_summary,
    )


@app.route("/website-changes")
def website_changes():
    """Website changes detection page"""
    competitors = load_competitors_csv()
    markets = competitors["market"].unique().tolist()
    days = request.args.get("days", "30", type=int)

    changes = load_website_changes(days)
    changes_by_market = {}
    for change in changes:
        market = change.get("market")
        if market not in changes_by_market:
            changes_by_market[market] = []
        changes_by_market[market].append(change)

    return render_template(
        "website_changes.html",
        markets=markets,
        changes_by_market=changes_by_market,
        days=days,
    )


@app.route("/api/market-summary/<market>")
def api_market_summary(market):
    """API endpoint for market summary data"""
    return jsonify(get_market_summary(market))


@app.route("/api/trends/<market>")
def api_trends(market):
    """API endpoint for trends data"""
    days = request.args.get("days", 30, type=int)
    return jsonify(get_follower_trends(market, days))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template("error.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}", exc_info=True)
    return render_template("error.html", error="Internal server error"), 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=5000)
